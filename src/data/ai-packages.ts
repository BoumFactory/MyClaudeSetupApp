export type PackageTier = 'generaliste' | 'latex' | 'avance'

export interface AIPackage {
  id: PackageTier
  name: string
  subtitle: string
  description: string
  icon: string
  color: string
  tier: number // 1 = base, 2 = spécialisé, 3 = complet
  skills: string[]
  agentPaths: string[]
  commandPaths: string[]
  dataPaths: string[]
  agentsDataPaths: string[]
  claudeMdFile: string
  highlights: string[]
}

// Skills de base partagés par tous les bundles
const BASE_SKILLS = [
  'grill-me',
  'wayfinder',
  'domain-modeling',
  'specs-creator',
  'resource-to-skill',
]

// Agents de base partagés par tous les bundles
const BASE_AGENTS = [
  'meta/error-investigator.md',
  'meta/self-improvement-agent.md',
  'meta/meta-high.md',
  'meta/meta-mid.md',
  'meta/meta-low.md',
]

// Commandes de base partagées par tous les bundles
const BASE_COMMANDS = [
  'do.md',
]

// Skills pédagogiques sans LaTeX, partagés par le bundle LaTeX et le Power User
const CONTENT_SKILLS = [
  'programmes-officiels',
  'progression-builder',
  'h5p-branching-scenario',
  'h5p-gamemap',
  'moodle-course-creator',
  'make-blueprint-eval',
  'bareme-actions-eleves',
  'audit-accessibilite-eval',
  'stats-datagouv',
  'reveals-presentation',
]

export const AI_PACKAGES: AIPackage[] = [
  {
    id: 'generaliste',
    name: 'Généraliste',
    subtitle: 'Briques de base pour expérimenter',
    description: 'Le socle commun pour ceux qui veulent explorer Claude Code librement. Interview pour affiner une idée, cahier des charges prêt à construire, transformation d\'une ressource en skill. Idéal pour construire sa propre configuration.',
    icon: '🧩',
    color: 'emerald',
    tier: 1,
    skills: [
      ...BASE_SKILLS,
    ],
    agentPaths: BASE_AGENTS,
    commandPaths: BASE_COMMANDS,
    dataPaths: [
      'user-settings.json',
    ],
    agentsDataPaths: [],
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Interview serrée pour affiner une idée (grill-me)',
      'Carte de chantier sur plusieurs sessions (wayfinder)',
      'Cahier des charges prêt à construire (specs-creator)',
      'Transformer une ressource en skill (resource-to-skill)',
      'Agents de base (diagnostic, auto-amélioration)',
    ],
  },
  {
    id: 'latex',
    name: 'LaTeX Enseignant',
    subtitle: 'Documents pédagogiques LaTeX',
    description: 'Le bundle Généraliste + l\'arsenal complet LaTeX : cours, exercices, évaluations, QCM, présentations Reveal.js, contenus H5P et Moodle, programmes officiels et progressions.',
    icon: '📐',
    color: 'cosmic',
    tier: 2,
    skills: [
      ...BASE_SKILLS,
      // LaTeX
      'bfcours-latex',
      'latex',
      'adaptTex',
      'tex-document-creator',
      'tex-compiling-skill',
      'latex-geometry',
      'latex-visual-review',
      'pdf2tikz',
      'qcm-creator',
      'html-katex-compiler',
      // Typst
      'bfcours-typst',
      // Évaluation & contenus pédagogiques
      ...CONTENT_SKILLS,
    ],
    agentPaths: [
      ...BASE_AGENTS,
      'creer/latex',
      'creer/documentation',
      'creer/evaluation',
      'creer/html',
      'outillage/latex',
      'outillage/extraction',
      'outillage/gestion',
    ],
    commandPaths: [
      ...BASE_COMMANDS,
      'creer/latex',
      'creer/evaluation',
      'creer/html',
      'creer/moodle',
      'modifier/latex',
      'modifier/html',
      'outillage/chargement',
      'outillage/recherche',
    ],
    dataPaths: [
      'user-settings.json',
      'competences',
      'competences.json',
      'competence-server-user-preferences.json',
      'create-document-user-preferences.json',
      'latex-compiler-preferences.json',
      'latex-modeles',
      'progression-6eme.json',
      'progression-server-user-preferences.json',
      'reveal-templates',
    ],
    agentsDataPaths: [
      'main-latex-knowledge.md',
      'tkz-euclide-master',
      'nicematrix-expert',
      'proflycee-expert',
    ],
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Tout le bundle Généraliste inclus',
      'Package bfcours pour documents éducatifs (LaTeX et Typst)',
      'Compilation LaTeX automatisée et relecture visuelle',
      'QCM au format bfcours et barèmes',
      'Présentations Reveal.js',
      'Contenus H5P et Moodle',
      'Programmes officiels sourcés et progressions',
      'Géométrie LaTeX et conversion PDF→TikZ',
    ],
  },
  {
    id: 'avance',
    name: 'Power User',
    subtitle: 'L\'arsenal complet',
    description: 'Tous les bundles réunis + les skills avancés : capsules vidéo animées, notebooks Jupyter, cartes mentales, et bien plus. Avec le CLAUDE.md auto-amélioration.',
    icon: '🚀',
    color: 'purple',
    tier: 3,
    skills: [
      ...BASE_SKILLS,
      ...CONTENT_SKILLS,
      'bfcours-latex', 'latex', 'adaptTex', 'tex-document-creator', 'tex-compiling-skill',
      'latex-geometry', 'latex-visual-review', 'pdf2tikz', 'qcm-creator', 'html-katex-compiler',
      'bfcours-typst', 'capsule-video', 'jupyter-notebook', 'mind-map-creator',
    ],
    agentPaths: ['*'],
    commandPaths: ['*'],
    dataPaths: ['*'],
    agentsDataPaths: ['*'],
    claudeMdFile: 'CLAUDE-autoAmelioration.md',
    highlights: [
      'Tous les bundles précédents inclus',
      'Capsules vidéo animées avec voix de synthèse',
      'Notebooks Jupyter et cartes mentales',
      'CLAUDE.md avec auto-amélioration',
      'Tous les agents et commandes',
    ],
  },
]

/**
 * Returns true if pkgA fully includes pkgB.
 * Power User (tier 3) includes everything.
 * Tier 2 package (latex) includes Généraliste (tier 1).
 * Same package includes itself.
 */
export function packageIncludes(pkgAId: PackageTier, pkgBId: PackageTier): boolean {
  if (pkgAId === pkgBId) return true
  const a = AI_PACKAGES.find(p => p.id === pkgAId)
  const b = AI_PACKAGES.find(p => p.id === pkgBId)
  if (!a || !b) return false
  // Power User includes everything
  if (a.tier === 3) return true
  // Tier 2 includes only tier 1
  if (a.tier === 2 && b.tier === 1) return true
  return false
}

/**
 * Find redundant packages in a list.
 * Returns packages that are already included by another package in the list.
 */
export function findRedundantPackages(packageIds: PackageTier[]): {
  redundant: PackageTier[]
  reason: Record<PackageTier, PackageTier> // redundant → included by
} {
  const redundant: PackageTier[] = []
  const reason: Record<string, PackageTier> = {}

  for (const id of packageIds) {
    for (const otherId of packageIds) {
      if (id === otherId) continue
      if (packageIncludes(otherId, id)) {
        redundant.push(id)
        reason[id] = otherId
        break
      }
    }
  }

  return { redundant, reason: reason as Record<PackageTier, PackageTier> }
}

/**
 * Shared folders always included in every package
 */
export const SHARED_FOLDERS = [
  'hooks',
  'scripts',
  'base-scripts',
  'assets',
]
