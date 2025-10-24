import { NextRequest, NextResponse } from 'next/server'
import { createDownloadRateLimiter } from '@/lib/rate-limiter'
import { createAnalyticsTracker } from '@/lib/analytics-tracker'

/**
 * API pour enregistrer un téléchargement
 */
export async function POST(request: NextRequest) {
  try {
    // Récupérer l'IP du client
    const forwarded = request.headers.get('x-forwarded-for')
    const ip = forwarded ? forwarded.split(',')[0] : request.ip || 'unknown'

    // Récupérer les métadonnées du téléchargement
    const body = await request.json()
    const { fileCount, totalSize, selectedPaths } = body

    // Vérifier à nouveau le rate limiting (double sécurité)
    const rateLimiter = createDownloadRateLimiter()
    const result = await rateLimiter.canDownload(ip)

    if (!result.allowed) {
      return NextResponse.json(
        { error: 'Rate limit dépassé' },
        { status: 429 }
      )
    }

    // Enregistrer le téléchargement dans le rate limiter
    await rateLimiter.recordDownload(ip)

    // Enregistrer l'événement dans analytics
    const tracker = createAnalyticsTracker()
    await tracker.trackEvent(ip, 'download', 'files', {
      fileCount,
      totalSize,
      paths: selectedPaths?.slice(0, 10) // Garder max 10 chemins pour pas trop alourdir
    })

    return NextResponse.json({
      success: true,
      remaining: (result.remaining || 0) - 1,
      message: 'Téléchargement enregistré avec succès'
    })
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement du téléchargement:', error)
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    )
  }
}
