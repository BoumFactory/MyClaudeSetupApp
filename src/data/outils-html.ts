/**
 * Outils web autonomes (un fichier HTML à ouvrir dans le navigateur),
 * distribués par le panier. Chaque outil a sa page :
 *   /claude-code/applications/logiciels/<slug>
 */
import type { CartItem } from '@/types/cart-theme'

export interface OutilHtml {
  slug: string
  nom: string
  /** Pastille affichée à côté du titre */
  badge: string
  description: string
  tags: string[]
  item: CartItem
  /** Le fichier HTML, servi par le site : s'ouvre dans le navigateur ou se télécharge */
  fichier: string
  /** Lien facultatif vers une fiche technique */
  ficheTechnique?: string
  couleur: 'violet' | 'emerald' | 'amber'
}

export const OUTILS_HTML: OutilHtml[] = [
  {
    slug: 'loiseau-generator',
    nom: 'Loiseau Generator',
    badge: 'Word',
    description:
      'Générateur de documents Word avec mise en page professionnelle style « Loiseau ». Créez des cours, exercices et évaluations avec un rendu imprimable soigné, directement depuis votre navigateur.',
    tags: ['Word .docx', 'Mise en page pro', 'Hors ligne'],
    item: { id: 'loiseau-generator', name: 'Loiseau Generator', type: 'logiciel', path: 'logiciels-enseignant/debutant/loiseau-generator', description: 'Generateur Word mise en page pro' },
    fichier: '/download/logiciels-enseignant/debutant/loiseau-generator/loiseau-generator.html',
    ficheTechnique: '/download/logiciels-enseignant/debutant/loiseau-generator/fiche_technique_ia_word.pdf',
    couleur: 'violet',
  },
  {
    slug: 'h5p-moodle',
    nom: 'Générateur H5P / Moodle',
    badge: 'H5P',
    description:
      'Créez des contenus interactifs H5P (QCM, glisser-déposer, textes à trous…) exportables directement dans Moodle ou tout LMS compatible. Interface visuelle, aucune connaissance technique requise.',
    tags: ['H5P interactif', 'Export Moodle', 'Hors ligne'],
    item: { id: 'h5p-generator', name: 'Générateur H5P/Moodle', type: 'logiciel', path: 'logiciels-enseignant/debutant/h5p-moodle', description: 'Contenus interactifs H5P exportables Moodle' },
    fichier: '/download/logiciels-enseignant/debutant/h5p-moodle/h5p-generator.html',
    couleur: 'emerald',
  },
  {
    slug: 'stats-datagouv',
    nom: 'Stats DataGouv',
    badge: 'Stats',
    description:
      'Générateur d’exercices de statistiques à partir de données réelles issues de data.gouv.fr. Donnez du sens aux maths avec des données authentiques (démographie, environnement, économie…).',
    tags: ['Données réelles', 'data.gouv.fr', 'Hors ligne'],
    item: { id: 'stats-datagouv', name: 'Stats DataGouv', type: 'logiciel', path: 'logiciels-enseignant/debutant/stats-datagouv', description: 'Exercices stats avec donnees reelles data.gouv.fr' },
    fichier: '/download/logiciels-enseignant/debutant/stats-datagouv/generateur-stats-datagouv.html',
    couleur: 'amber',
  },
]
