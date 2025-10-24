import { getRedisClient } from './redis'

/**
 * Interface pour les données de rate limiting
 */
interface RateLimitData {
  dailyIPs: {
    date: string
    ips: string[]
  }
  ipDownloads: {
    [ip: string]: {
      date: string
      count: number
    }
  }
}

/**
 * Gestionnaire de rate limiting pour les téléchargements
 */
export class RateLimiter {
  private dataKey: string
  private maxDownloadsPerIP: number
  private maxDailyNewIPs: number

  constructor(
    namespace: string = 'ratelimit',
    maxDownloadsPerIP: number = 5,
    maxDailyNewIPs: number = 20
  ) {
    this.dataKey = `${namespace}:data`
    this.maxDownloadsPerIP = maxDownloadsPerIP
    this.maxDailyNewIPs = maxDailyNewIPs
  }

  /**
   * Charger les données de rate limiting
   */
  private async loadData(): Promise<RateLimitData> {
    try {
      const redis = await getRedisClient()
      const result = await redis.get(this.dataKey)
      const data = result ? JSON.parse(result) : null
      return data || {
        dailyIPs: {
          date: this.getToday(),
          ips: []
        },
        ipDownloads: {}
      }
    } catch (error) {
      // Erreur de connexion, retourner des données vides
      return {
        dailyIPs: {
          date: this.getToday(),
          ips: []
        },
        ipDownloads: {}
      }
    }
  }

  /**
   * Sauvegarder les données de rate limiting
   */
  private async saveData(data: RateLimitData): Promise<void> {
    const redis = await getRedisClient()
    await redis.set(this.dataKey, JSON.stringify(data))
  }

  /**
   * Obtenir la date du jour au format YYYY-MM-DD
   */
  private getToday(): string {
    const now = new Date()
    return now.toISOString().split('T')[0]
  }

  /**
   * Nettoyer les données expirées
   */
  private cleanExpiredData(data: RateLimitData): RateLimitData {
    const today = this.getToday()

    // Réinitialiser les IPs quotidiennes si on change de jour
    if (data.dailyIPs.date !== today) {
      data.dailyIPs = {
        date: today,
        ips: []
      }
    }

    // Nettoyer les compteurs d'IP qui ne sont pas d'aujourd'hui
    const cleanedIpDownloads: typeof data.ipDownloads = {}
    for (const [ip, ipData] of Object.entries(data.ipDownloads)) {
      if (ipData.date === today) {
        cleanedIpDownloads[ip] = ipData
      }
    }
    data.ipDownloads = cleanedIpDownloads

    return data
  }

  /**
   * Vérifier si une IP peut télécharger
   * @param ip - Adresse IP
   * @returns { allowed: boolean, reason?: string, remaining?: number }
   */
  async canDownload(ip: string): Promise<{
    allowed: boolean
    reason?: string
    remaining?: number
    totalNewIPs?: number
  }> {
    let data = await this.loadData()
    data = this.cleanExpiredData(data)

    const today = this.getToday()

    // Vérifier si c'est une nouvelle IP aujourd'hui
    const isNewIP = !data.dailyIPs.ips.includes(ip)

    // Vérifier la limite globale de nouvelles IPs
    if (isNewIP && data.dailyIPs.ips.length >= this.maxDailyNewIPs) {
      return {
        allowed: false,
        reason: 'global_limit_reached',
        totalNewIPs: data.dailyIPs.ips.length
      }
    }

    // Vérifier le nombre de téléchargements de cette IP
    const ipData = data.ipDownloads[ip]
    if (ipData && ipData.date === today) {
      if (ipData.count >= this.maxDownloadsPerIP) {
        return {
          allowed: false,
          reason: 'ip_limit_reached',
          remaining: 0
        }
      }
      return {
        allowed: true,
        remaining: this.maxDownloadsPerIP - ipData.count
      }
    }

    // Nouvelle IP ou premier téléchargement du jour
    return {
      allowed: true,
      remaining: this.maxDownloadsPerIP
    }
  }

  /**
   * Enregistrer un téléchargement
   * @param ip - Adresse IP
   */
  async recordDownload(ip: string): Promise<void> {
    let data = await this.loadData()
    data = this.cleanExpiredData(data)

    const today = this.getToday()

    // Ajouter l'IP aux IPs quotidiennes si nouvelle
    if (!data.dailyIPs.ips.includes(ip)) {
      data.dailyIPs.ips.push(ip)
    }

    // Incrémenter le compteur de téléchargements
    if (data.ipDownloads[ip] && data.ipDownloads[ip].date === today) {
      data.ipDownloads[ip].count++
    } else {
      data.ipDownloads[ip] = {
        date: today,
        count: 1
      }
    }

    await this.saveData(data)
  }

  /**
   * Obtenir les statistiques actuelles
   */
  async getStats(): Promise<{
    dailyNewIPs: number
    maxDailyNewIPs: number
    totalDownloadsToday: number
    ipDownloads: Array<{ ip: string; count: number }>
  }> {
    let data = await this.loadData()
    data = this.cleanExpiredData(data)

    const today = this.getToday()
    const ipDownloads = Object.entries(data.ipDownloads)
      .filter(([_, ipData]) => ipData.date === today)
      .map(([ip, ipData]) => ({
        ip: this.anonymizeIP(ip),
        count: ipData.count
      }))

    const totalDownloadsToday = ipDownloads.reduce((sum, item) => sum + item.count, 0)

    return {
      dailyNewIPs: data.dailyIPs.ips.length,
      maxDailyNewIPs: this.maxDailyNewIPs,
      totalDownloadsToday,
      ipDownloads
    }
  }

  /**
   * Anonymiser une adresse IP (garder seulement les 2 premiers octets)
   * @param ip - Adresse IP
   */
  private anonymizeIP(ip: string): string {
    const parts = ip.split('.')
    if (parts.length === 4) {
      return `${parts[0]}.${parts[1]}.xxx.xxx`
    }
    // IPv6 ou autre format
    return ip.substring(0, Math.min(ip.length, 10)) + '...'
  }
}

/**
 * Créer une instance de RateLimiter pour les téléchargements
 */
export function createDownloadRateLimiter(): RateLimiter {
  return new RateLimiter('ratelimit', 5, 20)
}
