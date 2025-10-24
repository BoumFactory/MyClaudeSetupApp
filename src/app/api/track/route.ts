import { NextRequest, NextResponse } from 'next/server'
import { createAnalyticsTracker, EventType } from '@/lib/analytics-tracker'

/**
 * API pour tracker un événement (vue de page, présentation, tutoriel, etc.)
 */
export async function POST(request: NextRequest) {
  try {
    // Récupérer l'IP du client
    const forwarded = request.headers.get('x-forwarded-for')
    const ip = forwarded ? forwarded.split(',')[0] : 'unknown'

    // Récupérer les données de l'événement
    const body = await request.json()
    const { eventType, resource, metadata } = body

    // Validation
    if (!eventType || !resource) {
      return NextResponse.json(
        { error: 'eventType et resource sont requis' },
        { status: 400 }
      )
    }

    // Vérifier que le type d'événement est valide
    const validEventTypes: EventType[] = ['download', 'view_presentation', 'view_tutorial', 'page_view']
    if (!validEventTypes.includes(eventType)) {
      return NextResponse.json(
        { error: `eventType doit être l'un de: ${validEventTypes.join(', ')}` },
        { status: 400 }
      )
    }

    // Enregistrer l'événement
    try {
      const tracker = createAnalyticsTracker()
      await tracker.trackEvent(ip, eventType, resource, metadata)
    } catch (redisError) {
      // Redis non disponible (ex: en dev local) - on continue sans tracker
      console.warn('Analytics non disponible:', redisError)
    }

    return NextResponse.json({
      success: true,
      message: 'Événement enregistré avec succès'
    })
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement de l\'événement:', error)
    return NextResponse.json(
      { error: 'Erreur serveur' },
      { status: 500 }
    )
  }
}
