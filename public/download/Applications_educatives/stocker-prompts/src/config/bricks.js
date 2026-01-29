/**
 * Briques de construction pour le fabricateur de prompts
 * Chaque brique est un élément textuel paramétrable
 */

export const DEFAULT_BRICKS = [
  // Briques de contexte
  {
    id: 'context_eleve',
    category: 'contexte',
    label: 'Je suis élève',
    template: 'Je suis un élève de {niveau} en {matiere}.',
    params: ['niveau', 'matiere'],
    enabled: true
  },
  {
    id: 'context_cours',
    category: 'contexte',
    label: 'J\'étudie un chapitre',
    template: 'J\'étudie actuellement le chapitre sur {theme}.',
    params: ['theme'],
    enabled: true
  },
  {
    id: 'context_difficulte',
    category: 'contexte',
    label: 'J\'ai des difficultés',
    template: 'J\'ai des difficultés avec {sujet_difficile}.',
    params: ['sujet_difficile'],
    enabled: true
  },

  // Briques de demande
  {
    id: 'demande_explication',
    category: 'demande',
    label: 'Explique-moi',
    template: 'Peux-tu m\'expliquer {concept} de manière simple ?',
    params: ['concept'],
    enabled: true
  },
  {
    id: 'demande_exemples',
    category: 'demande',
    label: 'Donne-moi des exemples',
    template: 'Donne-moi {nombre} exemples concrets de {sujet}.',
    params: ['nombre', 'sujet'],
    enabled: true
  },
  {
    id: 'demande_exercices',
    category: 'demande',
    label: 'Propose des exercices',
    template: 'Propose-moi {nombre} exercices sur {theme} de niveau {difficulte}.',
    params: ['nombre', 'theme', 'difficulte'],
    enabled: true
  },
  {
    id: 'demande_correction',
    category: 'demande',
    label: 'Corrige mon travail',
    template: 'Peux-tu corriger ce travail et m\'expliquer mes erreurs ?',
    params: [],
    enabled: true
  },
  {
    id: 'demande_resume',
    category: 'demande',
    label: 'Fais un résumé',
    template: 'Fais-moi un résumé clair de {sujet} en {longueur}.',
    params: ['sujet', 'longueur'],
    enabled: true
  },
  {
    id: 'demande_fiche',
    category: 'demande',
    label: 'Crée une fiche',
    template: 'Crée-moi une fiche de révision sur {theme} avec les points essentiels.',
    params: ['theme'],
    enabled: true
  },

  // Briques de format
  {
    id: 'format_simple',
    category: 'format',
    label: 'Langage simple',
    template: 'Utilise un langage simple et accessible pour un élève de {niveau}.',
    params: ['niveau'],
    enabled: true
  },
  {
    id: 'format_structure',
    category: 'format',
    label: 'Réponse structurée',
    template: 'Structure ta réponse avec des titres et des puces.',
    params: [],
    enabled: true
  },
  {
    id: 'format_etapes',
    category: 'format',
    label: 'Étape par étape',
    template: 'Explique-moi étape par étape.',
    params: [],
    enabled: true
  },
  {
    id: 'format_court',
    category: 'format',
    label: 'Réponse courte',
    template: 'Fais une réponse concise, pas plus de {lignes} lignes.',
    params: ['lignes'],
    enabled: true
  },

  // Briques de contrainte
  {
    id: 'contrainte_niveau',
    category: 'contrainte',
    label: 'Adapté à mon niveau',
    template: 'N\'utilise que des notions vues en {niveau}.',
    params: ['niveau'],
    enabled: true
  },
  {
    id: 'contrainte_temps',
    category: 'contrainte',
    label: 'Temps limité',
    template: 'J\'ai {temps} pour comprendre/faire cela.',
    params: ['temps'],
    enabled: true
  },
  {
    id: 'contrainte_sans_calculatrice',
    category: 'contrainte',
    label: 'Sans calculatrice',
    template: 'Les calculs doivent être faisables sans calculatrice.',
    params: [],
    enabled: true
  }
];

export const BRICK_CATEGORIES = {
  contexte: { label: 'Contexte', color: '#2196F3', icon: '📍' },
  demande: { label: 'Demande', color: '#4CAF50', icon: '❓' },
  format: { label: 'Format', color: '#FF9800', icon: '📐' },
  contrainte: { label: 'Contrainte', color: '#E91E63', icon: '⚠️' }
};
