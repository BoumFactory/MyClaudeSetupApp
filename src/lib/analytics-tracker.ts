import fs from 'fs/promises'
import path from 'path'

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
  private eventsPath: string
  private statsPath: string
  private maxEventsToKeep: number

  constructor(
    dataDir: string,
    maxEventsToKeep: number = 10000
  ) {
    this.eventsPath = path.join(dataDir, 'events.json')
    this.statsPath = path.join(dataDir, 'stats.json')
    this.maxEventsToKeep = maxEventsToKeep
  }

  /**
   * Charger les événements
   */
  private async loadEvents(): Promise<AnalyticsEvent[]> {
    try {
      const content = await fs.readFile(this.eventsPath, 'utf-8')
      return JSON.parse(content)
    } catch (error) {
      return []
    }
  }

  /**
   * Sauvegarder les événements
   */
  private async saveEvents(events: AnalyticsEvent[]): Promise<void> {
    const dir = path.dirname(this.eventsPath)
    await fs.mkdir(dir, { recursive: true })

    // Garder seulement les N derniers événements
    const eventsToSave = events.slice(-this.maxEventsToKeep)
    await fs.writeFile(this.eventsPath, JSON.stringify(eventsToSave, null, 2), 'utf-8')
  }

  /**
   * Charger les statistiques
   */
  private async loadStats(): Promise<AnalyticsStats | null> {
    try {
      const content = await fs.readFile(this.statsPath, 'utf-8')
      return JSON.parse(content)
    } catch (error) {
      return null
    }
  }

  /**
   * Sauvegarder les statistiques
   */
  private async saveStats(stats: AnalyticsStats): Promise<void> {
    const dir = path.dirname(this.statsPath)
    await fs.mkdir(dir, { recursive: true })

    await fs.writeFile(this.statsPath, JSON.stringify(stats, null, 2), 'utf-8')
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
  const dataDir = path.join(process.cwd(), 'src', 'data', 'analytics')
  return new AnalyticsTracker(dataDir)
}
