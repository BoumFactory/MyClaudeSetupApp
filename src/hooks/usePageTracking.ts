import { useEffect, useRef } from 'react'

/**
 * Type d'événement trackable
 */
export type TrackEventType = 'view_presentation' | 'view_tutorial' | 'page_view'

/**
 * Hook pour tracker automatiquement une vue de page
 * @param eventType - Type d'événement à tracker
 * @param resource - Nom de la ressource (slug, titre, etc.)
 * @param metadata - Métadonnées optionnelles
 * @param enabled - Si false, ne track pas (défaut: true)
 */
export function usePageTracking(
  eventType: TrackEventType,
  resource: string,
  metadata?: Record<string, any>,
  enabled: boolean = true
) {
  const hasTracked = useRef(false)

  useEffect(() => {
    // Ne tracker qu'une seule fois par montage de composant
    if (!enabled || hasTracked.current || !resource) {
      return
    }

    hasTracked.current = true

    // Envoyer l'événement de tracking
    const trackEvent = async () => {
      try {
        await fetch('/api/track', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            eventType,
            resource,
            metadata,
          }),
        })
      } catch (error) {
        // Ne pas afficher d'erreur à l'utilisateur si le tracking échoue
        console.warn('Erreur lors du tracking:', error)
      }
    }

    // Exécuter après un court délai pour ne pas bloquer le rendu
    const timeoutId = setTimeout(trackEvent, 100)

    return () => {
      clearTimeout(timeoutId)
    }
  }, [eventType, resource, metadata, enabled])
}

/**
 * Hook simplifié pour tracker une vue de présentation
 */
export function usePresentationTracking(slug: string, title?: string) {
  usePageTracking('view_presentation', slug, title ? { title } : undefined)
}

/**
 * Hook simplifié pour tracker une vue de tutoriel
 */
export function useTutorialTracking(slug: string, title?: string) {
  usePageTracking('view_tutorial', slug, title ? { title } : undefined)
}
