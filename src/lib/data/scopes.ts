import { Scope, YouTubeVideo } from '@/types'

/**
 * Configuration des scopes disponibles
 */

/**
 * Liste des scopes de l'application
 */
export const scopes: Scope[] = [
  {
    id: 'claude-code',
    title: 'Claude Code',
    slug: 'claude-code',
    description:
      "Découvrez comment utiliser Claude Code pour créer des applications éducatives, générer des présentations et automatiser vos tâches d'enseignement.",
    icon: 'Code2',
    color: 'cosmic-600',
    gradient: 'from-cosmic-500 to-cosmic-700',
    path: '/claude-code',
  },
  // Ajoutez facilement de nouveaux scopes ici
]

/**
 * Obtenir un scope par son slug
 * @param slug - Slug du scope
 * @returns Scope ou undefined
 */
export function getScopeBySlug(slug: string): Scope | undefined {
  return scopes.find((scope) => scope.slug === slug)
}

/**
 * Vidéos YouTube pour le scope Claude Code
 */
export const claudeCodeVideos: YouTubeVideo[] = [
  // Exemple de vidéo - À remplacer par vos vraies vidéos
  {
    id: 'demo-claude-code',
    title: 'Introduction à Claude Code',
    url: 'https://www.youtube.com/playlist?list=PLdhRy3n11XGD3kVAQGtgL9UhmvqBqaeh3',
    videoId: 'EXAMPLE',
    thumbnail: 'https://i.ytimg.com/vi/EXAMPLE/maxresdefault.jpg',
    description:
      'Voir en vidéo mon utilisation de Claude Code',
    category: 'tutorial',
  },
  // Ajoutez vos vidéos ici
]

/**
 * Obtenir les vidéos d'un scope
 * @param scopeSlug - Slug du scope
 * @returns Liste des vidéos
 */
export function getVideosForScope(scopeSlug: string): YouTubeVideo[] {
  switch (scopeSlug) {
    case 'claude-code':
      return claudeCodeVideos
    default:
      return []
  }
}
