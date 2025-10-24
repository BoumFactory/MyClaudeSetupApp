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
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    )
  }
}
