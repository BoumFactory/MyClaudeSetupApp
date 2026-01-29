/**
 * Structures de prompts prédéfinies
 * Combinaisons de briques pour des cas d'usage fréquents
 */

export const DEFAULT_STRUCTURES = [
  {
    id: 'revision_chapitre',
    label: 'Réviser un chapitre',
    description: 'Pour revoir un chapitre avant une évaluation',
    bricks: ['context_eleve', 'context_cours', 'demande_resume', 'demande_fiche', 'format_structure'],
    icon: '📚',
    enabled: true
  },
  {
    id: 'comprendre_notion',
    label: 'Comprendre une notion',
    description: 'Quand tu ne comprends pas quelque chose',
    bricks: ['context_eleve', 'context_difficulte', 'demande_explication', 'demande_exemples', 'format_simple', 'format_etapes'],
    icon: '💡',
    enabled: true
  },
  {
    id: 'faire_exercices',
    label: 'S\'entraîner avec des exercices',
    description: 'Pour pratiquer sur un thème',
    bricks: ['context_eleve', 'context_cours', 'demande_exercices', 'contrainte_niveau'],
    icon: '🏋️',
    enabled: true
  },
  {
    id: 'corriger_travail',
    label: 'Faire corriger un travail',
    description: 'Pour avoir un retour sur ton travail',
    bricks: ['context_eleve', 'demande_correction', 'format_structure'],
    icon: '✏️',
    enabled: true
  },
  {
    id: 'preparer_controle',
    label: 'Préparer un contrôle',
    description: 'Révision complète avant un contrôle',
    bricks: ['context_eleve', 'context_cours', 'demande_resume', 'demande_exercices', 'format_structure', 'contrainte_temps'],
    icon: '📝',
    enabled: true
  },
  {
    id: 'aide_rapide',
    label: 'Aide rapide',
    description: 'Question rapide sur un point précis',
    bricks: ['demande_explication', 'format_court'],
    icon: '⚡',
    enabled: true
  },
  {
    id: 'approfondir_sujet',
    label: 'Approfondir un sujet',
    description: 'Aller plus loin dans la compréhension',
    bricks: ['context_eleve', 'context_cours', 'demande_explication', 'demande_exemples', 'format_structure'],
    icon: '🔬',
    enabled: true
  },
  {
    id: 'methode_resolution',
    label: 'Méthode de résolution',
    description: 'Apprendre une méthode pas à pas',
    bricks: ['context_eleve', 'demande_explication', 'format_etapes', 'demande_exemples'],
    icon: '🎯',
    enabled: true
  }
];
