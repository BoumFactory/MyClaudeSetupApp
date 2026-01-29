/**
 * Configuration des matières disponibles
 * Modifiable via les paramètres de l'application
 */

export const DEFAULT_SUBJECTS = [
  { id: 'maths', label: 'Mathématiques', emoji: '🔢', enabled: true },
  { id: 'francais', label: 'Français', emoji: '📜', enabled: true },
  { id: 'histoire', label: 'Histoire', emoji: '🏛️', enabled: true },
  { id: 'geo', label: 'Géographie', emoji: '🌍', enabled: true },
  { id: 'physique', label: 'Physique-Chimie', emoji: '⚗️', enabled: true },
  { id: 'svt', label: 'SVT', emoji: '🌿', enabled: true },
  { id: 'anglais', label: 'Anglais', emoji: '🇬🇧', enabled: true },
  { id: 'espagnol', label: 'Espagnol', emoji: '🇪🇸', enabled: false },
  { id: 'allemand', label: 'Allemand', emoji: '🇩🇪', enabled: false },
  { id: 'philo', label: 'Philosophie', emoji: '🤔', enabled: false },
  { id: 'ses', label: 'SES', emoji: '📈', enabled: false },
  { id: 'nsi', label: 'NSI', emoji: '💻', enabled: false },
  { id: 'art', label: 'Arts', emoji: '🎨', enabled: false },
  { id: 'musique', label: 'Musique', emoji: '🎵', enabled: false },
  { id: 'eps', label: 'EPS', emoji: '⚽', enabled: false },
  { id: 'autre', label: 'Autre', emoji: '📁', enabled: true }
];

export const DEFAULT_LEVELS = [
  { id: '6eme', label: '6ème', enabled: true },
  { id: '5eme', label: '5ème', enabled: true },
  { id: '4eme', label: '4ème', enabled: true },
  { id: '3eme', label: '3ème', enabled: true },
  { id: '2nde', label: '2nde', enabled: true },
  { id: '1ere', label: '1ère', enabled: true },
  { id: 'term', label: 'Terminale', enabled: true },
  { id: 'sup', label: 'Supérieur', enabled: false }
];
