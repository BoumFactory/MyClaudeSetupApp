import type { AnimationId } from '@/contexts/BackgroundAnimationContext'

/**
 * Thème allégorique du panier, lié à l'animation de fond active
 */
export interface CartTheme {
  /** Nom allégorique du panier (ex: "Besace du Dragon") */
  name: string
  /** Emoji représentatif */
  icon: string
  /** Verbe pour ajouter un item */
  verbAdd: string
  /** Verbe pour retirer un item */
  verbRemove: string
  /** Verbe pour télécharger / ouvrir le panier */
  verbDownload: string
  /** Verbe pour vider le panier */
  verbClear: string
  /** Message quand le panier est vide */
  emptyMessage: string
  /** Notification après ajout */
  notification: string
  /** Nom de couleur Tailwind (sans préfixe) ou classe custom */
  color: string
}

/**
 * Item dans le panier
 */
export interface CartItem {
  /** Identifiant unique */
  id: string
  /** Nom affiche */
  name: string
  /** Type d'item */
  type: 'app' | 'logiciel' | 'setup' | 'file' | 'package'
  /** Chemin relatif pour le téléchargement */
  path: string
  /** Description optionnelle */
  description?: string
}

export type CartThemeMap = Record<AnimationId, CartTheme>
