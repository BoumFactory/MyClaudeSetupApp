"use client"

import { usePresentationTracking, useTutorialTracking } from '@/hooks/usePageTracking'

/**
 * Composant client pour tracker une vue de présentation
 */
export function PresentationTracker({ slug, title }: { slug: string; title?: string }) {
  usePresentationTracking(slug, title)
  return null
}

/**
 * Composant client pour tracker une vue de tutoriel
 */
export function TutorialTracker({ slug, title }: { slug: string; title?: string }) {
  useTutorialTracking(slug, title)
  return null
}
