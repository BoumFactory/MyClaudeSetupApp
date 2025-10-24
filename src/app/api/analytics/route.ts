import { NextResponse } from 'next/server'
import { createAnalyticsTracker } from '@/lib/analytics-tracker'
import { createDownloadRateLimiter } from '@/lib/rate-limiter'

/**
 * API pour récupérer les statistiques d'utilisation
 */
export async function GET() {
  try {
    // Récupérer les stats du tracker
    const tracker = createAnalyticsTracker()
    const analyticsStats = await tracker.getStats()

    // Récupérer les stats du rate limiter
    const rateLimiter = createDownloadRateLimiter()
    const rateLimitStats = await rateLimiter.getStats()

    return NextResponse.json({
      analytics: analyticsStats,
      rateLimit: rateLimitStats,
      timestamp: new Date().toISOString()
    })
  } catch (error) {
    console.error('Erreur lors de la récupération des statistiques:', error)

    // Mode dégradé : retourner des données vides au lieu d'une erreur
    // (utile en dev local sans Redis)
    return NextResponse.json({
      analytics: {
        totalEvents: 0,
        eventsByType: {},
        topResources: [],
        dailyStats: [],
        lastUpdated: new Date().toISOString()
      },
      rateLimit: {
        dailyNewIPs: 0,
        maxDailyNewIPs: 20,
        totalDownloadsToday: 0,
        ipDownloads: []
      },
      timestamp: new Date().toISOString(),
      warning: 'Redis non disponible - données vides retournées'
    })
  }
}
