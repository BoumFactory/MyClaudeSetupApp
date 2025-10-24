import { getRedisClient } from './redis'

/**
 * Type d'événement trackable
 */
export type EventType = 'download' | 'view_presentation' | 'view_tutorial' | 'page_view'

/**
 * Interface pour un événement
 */
interface AnalyticsEvent {
  timestamp: string
  ip: string
  eventType: EventType
  resource: string
  metadata?: Record<string, any>
}

/**
 * Interface pour les statistiques agrégées
 */
export interface AnalyticsStats {
  totalEvents: number
  eventsByType: Record<EventType, number>
  topResources: Array<{ resource: string; count: number; type: EventType }>
  dailyStats: Array<{ date: string; count: number }>
  lastUpdated: string
}

/**
 * Gestionnaire de tracking analytics
 */
export class AnalyticsTracker {
  private eventsKey: string
  private statsKey: string
  private maxEventsToKeep: number

  constructor(
    namespace: string = 'analytics',
    maxEventsToKeep: number = 10000
  ) {
    this.eventsKey = `${namespace}:events`
    this.statsKey = `${namespace}:stats`
    this.maxEventsToKeep = maxEventsToKeep
  }

  /**
   * Charger les événements
   */
  private async loadEvents(): Promise<AnalyticsEvent[]> {
    try {
      const redis = await getRedisClient()
      const data = await redis.get(this.eventsKey)
      return data ? JSON.parse(data) : []
    } catch (error) {
      return []
    }
  }

  /**
   * Sauvegarder les événements
   */
  private async saveEvents(events: AnalyticsEvent[]): Promise<void> {
    // Garder seulement les N derniers événements
    const eventsToSave = events.slice(-this.maxEventsToKeep)
    const redis = await getRedisClient()
    await redis.set(this.eventsKey, JSON.stringify(eventsToSave))
  }

  /**
   * Charger les statistiques
   */
  private async loadStats(): Promise<AnalyticsStats | null> {
    try {
      const redis = await getRedisClient()
      const data = await redis.get(this.statsKey)
      return data ? JSON.parse(data) : null
    } catch (error) {
      return null
    }
  }

  /**
   * Sauvegarder les statistiques
   */
  private async saveStats(stats: AnalyticsStats): Promise<void> {
    const redis = await getRedisClient()
    await redis.set(this.statsKey, JSON.stringify(stats))
  }

  /**
   * Anonymiser une adresse IP
   */
  private anonymizeIP(ip: string): string {
    const parts = ip.split('.')
    if (parts.length === 4) {
      return `${parts[0]}.${parts[1]}.xxx.xxx`
    }
    return ip.substring(0, Math.min(ip.length, 10)) + '...'
  }

  /**
   * Enregistrer un événement
   */
  async trackEvent(
    ip: string,
    eventType: EventType,
    resource: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    const events = await this.loadEvents()

    const event: AnalyticsEvent = {
      timestamp: new Date().toISOString(),
      ip: this.anonymizeIP(ip),
      eventType,
      resource,
      metadata
    }

    events.push(event)
    await this.saveEvents(events)

    // Régénérer les stats
    await this.regenerateStats()
  }

  /**
   * Régénérer les statistiques à partir des événements
   */
  private async regenerateStats(): Promise<void> {
    const events = await this.loadEvents()

    // Calculer les stats
    const eventsByType: Record<string, number> = {}
    const resourceCounts: Map<string, { count: number; type: EventType }> = new Map()
    const dailyCounts: Map<string, number> = new Map()

    for (const event of events) {
      // Compter par type
      eventsByType[event.eventType] = (eventsByType[event.eventType] || 0) + 1

      // Compter par ressource
      const key = `${event.eventType}:${event.resource}`
      const current = resourceCounts.get(key) || { count: 0, type: event.eventType }
      resourceCounts.set(key, { count: current.count + 1, type: event.eventType })

      // Compter par jour
      const date = event.timestamp.split('T')[0]
      dailyCounts.set(date, (dailyCounts.get(date) || 0) + 1)
    }

    // Top ressources
    const topResources = Array.from(resourceCounts.entries())
      .map(([key, value]) => ({
        resource: key.split(':')[1],
        type: value.type,
        count: value.count
      }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 20)

    // Stats quotidiennes (derniers 30 jours)
    const dailyStats = Array.from(dailyCounts.entries())
      .map(([date, count]) => ({ date, count }))
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 30)
      .reverse()

    const stats: AnalyticsStats = {
      totalEvents: events.length,
      eventsByType: eventsByType as Record<EventType, number>,
      topResources,
      dailyStats,
      lastUpdated: new Date().toISOString()
    }

    await this.saveStats(stats)
  }

  /**
   * Obtenir les statistiques
   */
  async getStats(): Promise<AnalyticsStats> {
    const stats = await this.loadStats()
    if (!stats) {
      // Générer les stats si elles n'existent pas
      await this.regenerateStats()
      return await this.loadStats() || this.getEmptyStats()
    }
    return stats
  }

  /**
   * Obtenir des stats vides
   */
  private getEmptyStats(): AnalyticsStats {
    return {
      totalEvents: 0,
      eventsByType: {} as Record<EventType, number>,
      topResources: [],
      dailyStats: [],
      lastUpdated: new Date().toISOString()
    }
  }

  /**
   * Nettoyer les événements anciens (garder seulement les 90 derniers jours)
   */
  async cleanOldEvents(): Promise<void> {
    const events = await this.loadEvents()
    const ninetyDaysAgo = new Date()
    ninetyDaysAgo.setDate(ninetyDaysAgo.getDate() - 90)

    const filteredEvents = events.filter(event => {
      const eventDate = new Date(event.timestamp)
      return eventDate >= ninetyDaysAgo
    })

    if (filteredEvents.length !== events.length) {
      await this.saveEvents(filteredEvents)
      await this.regenerateStats()
    }
  }
}

/**
 * Créer une instance globale du tracker
 */
export function createAnalyticsTracker(): AnalyticsTracker {
  return new AnalyticsTracker('analytics')
}
