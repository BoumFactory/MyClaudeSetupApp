/**
 * Configuration des actions disponibles dans l'application
 * Les actions "enabled: true" sont affichées par défaut dans le wizard
 */

export const ACTIONS = [
  // Actions de base (activées par défaut)
  { id: 'creer', label: 'Créer', emoji: '✨', description: 'Générer du nouveau contenu', enabled: true, category: 'production' },
  { id: 'reviser', label: 'Réviser', emoji: '📚', description: 'Revoir et mémoriser des notions', enabled: true, category: 'apprentissage' },
  { id: 'expliquer', label: 'Expliquer', emoji: '💡', description: 'Obtenir des explications claires', enabled: true, category: 'comprehension' },
  { id: 'corriger', label: 'Corriger', emoji: '✏️', description: 'Faire corriger un travail', enabled: true, category: 'amelioration' },
  { id: 'resumer', label: 'Résumer', emoji: '📝', description: 'Condenser une information', enabled: true, category: 'synthese' },
  { id: 'comparer', label: 'Comparer', emoji: '⚖️', description: 'Mettre en parallèle des concepts', enabled: true, category: 'analyse' },

  // Actions supplémentaires (désactivées par défaut)
  { id: 'traduire', label: 'Traduire', emoji: '🌍', description: 'Traduire dans une autre langue', enabled: false, category: 'langue' },
  { id: 'reformuler', label: 'Reformuler', emoji: '🔄', description: 'Dire autrement', enabled: false, category: 'amelioration' },
  { id: 'simplifier', label: 'Simplifier', emoji: '🎯', description: 'Rendre plus accessible', enabled: false, category: 'comprehension' },
  { id: 'approfondir', label: 'Approfondir', emoji: '🔬', description: 'Aller plus loin dans un sujet', enabled: false, category: 'comprehension' },
  { id: 'illustrer', label: 'Illustrer', emoji: '🎨', description: 'Donner des exemples concrets', enabled: false, category: 'comprehension' },
  { id: 'debattre', label: 'Débattre', emoji: '💬', description: 'Argumenter pour/contre', enabled: false, category: 'reflexion' },
  { id: 'analyser', label: 'Analyser', emoji: '🔍', description: 'Décortiquer en détail', enabled: false, category: 'analyse' },
  { id: 'synthetiser', label: 'Synthétiser', emoji: '🧩', description: 'Rassembler des informations', enabled: false, category: 'synthese' },
  { id: 'memoriser', label: 'Mémoriser', emoji: '🧠', description: 'Créer des moyens mnémotechniques', enabled: false, category: 'apprentissage' },
  { id: 'pratiquer', label: 'Pratiquer', emoji: '🏋️', description: 'S\'exercer avec des exemples', enabled: false, category: 'apprentissage' },
  { id: 'definir', label: 'Définir', emoji: '📖', description: 'Obtenir une définition précise', enabled: false, category: 'comprehension' },
  { id: 'demontrer', label: 'Démontrer', emoji: '📐', description: 'Prouver pas à pas', enabled: false, category: 'raisonnement' },
  { id: 'contextualiser', label: 'Contextualiser', emoji: '🗺️', description: 'Situer dans un contexte', enabled: false, category: 'comprehension' },
  { id: 'vulgariser', label: 'Vulgariser', emoji: '👶', description: 'Expliquer simplement', enabled: false, category: 'comprehension' },
  { id: 'critiquer', label: 'Critiquer', emoji: '🎭', description: 'Analyser forces et faiblesses', enabled: false, category: 'reflexion' },
  { id: 'planifier', label: 'Planifier', emoji: '📅', description: 'Organiser un travail', enabled: false, category: 'organisation' },
  { id: 'structurer', label: 'Structurer', emoji: '🏗️', description: 'Organiser des idées', enabled: false, category: 'organisation' },
  { id: 'evaluer', label: 'Évaluer', emoji: '📊', description: 'Estimer la qualité', enabled: false, category: 'analyse' },
  { id: 'questionner', label: 'Questionner', emoji: '❓', description: 'Générer des questions', enabled: false, category: 'reflexion' },
  { id: 'rediger', label: 'Rédiger', emoji: '✍️', description: 'Écrire un texte complet', enabled: false, category: 'production' }
];

export const ACTION_CATEGORIES = {
  production: { label: 'Production', color: '#4CAF50' },
  apprentissage: { label: 'Apprentissage', color: '#2196F3' },
  comprehension: { label: 'Compréhension', color: '#9C27B0' },
  amelioration: { label: 'Amélioration', color: '#FF9800' },
  synthese: { label: 'Synthèse', color: '#00BCD4' },
  analyse: { label: 'Analyse', color: '#E91E63' },
  reflexion: { label: 'Réflexion', color: '#673AB7' },
  raisonnement: { label: 'Raisonnement', color: '#3F51B5' },
  organisation: { label: 'Organisation', color: '#795548' },
  langue: { label: 'Langue', color: '#607D8B' }
};
