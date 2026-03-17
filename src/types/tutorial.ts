/**
 * Types pour le systeme de capsules tutoriels et suivi de progression
 */

/** Represente une capsule de tutoriel */
export interface Capsule {
  id: string
  title: string
  description: string
  parcours: string
  order: number
  sections: {
    info: string
    exemple: string
    pratique: string
  }
  duration?: string
  tags?: string[]
}

/** Represente un parcours de formation */
export interface Parcours {
  id: string
  title: string
  description: string
  icon: string
  color: string
  capsules: string[]
}

/** Etat de progression de l'utilisateur */
export interface TutorialProgress {
  completedCapsules: string[]
  lastVisited?: string
  updatedAt: string
}
