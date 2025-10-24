import { NextRequest, NextResponse } from 'next/server'
import { createDownloadRateLimiter } from '@/lib/rate-limiter'

/**
 * API pour vérifier si une IP peut télécharger
 */
export async function GET(request: NextRequest) {
  try {
    // Récupérer l'IP du client
    const forwarded = request.headers.get('x-forwarded-for')
    const ip = forwarded ? forwarded.split(',')[0] : 'unknown'

    // Vérifier le rate limiting
    try {
      const rateLimiter = createDownloadRateLimiter()
      const result = await rateLimiter.canDownload(ip)

      if (!result.allowed) {
        return NextResponse.json(
          {
            allowed: false,
            reason: result.reason,
            message:
              result.reason === 'global_limit_reached'
                ? 'Nombre maximal de téléchargements quotidien atteint. Réessayez demain !'
                : 'Vous avez atteint votre limite de téléchargements pour aujourd\'hui. Réessayez demain !',
            totalNewIPs: result.totalNewIPs
          },
          { status: 429 }
        )
      }

      return NextResponse.json({
        allowed: true,
        remaining: result.remaining,
        message: `Vous pouvez encore télécharger ${result.remaining} fois aujourd'hui.`
      })
    } catch (redisError) {
      // Redis non disponible (ex: en dev local) - autoriser le téléchargement
      console.warn('Rate limiter non disponible, autorisation par défaut:', redisError)
      return NextResponse.json({
        allowed: true,
        remaining: 5,
        message: 'Rate limiting désactivé (mode développement)'
      })
    }
  } catch (error) {
    console.error('Erreur lors de la vérification du rate limit:', error)
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    )
  }
}
