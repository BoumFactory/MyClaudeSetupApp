export type PackageTier = 'generaliste' | 'latex' | 'word' | 'avance'

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
  'meta-prompt',
  'skill-creator',
  'image-generator',
  'adversarial-optimisation',
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
  'meta',
]

// Skills bureautiques partagés par Word enseignant et le généraliste
const OFFICE_SKILLS = [
  'docx',
  'xlsx',
  'pptx',
  'pdf',
  'odt',
]

export const AI_PACKAGES: AIPackage[] = [
  {
    id: 'generaliste',
    name: 'Généraliste',
    subtitle: 'Briques de base pour expérimenter',
    description: 'Le socle commun pour ceux qui veulent explorer Claude Code librement. Skills de base, outils bureautiques, création de prompts et d\'images. Idéal pour construire sa propre configuration.',
    icon: '🧩',
    color: 'emerald',
    tier: 1,
    skills: [
      ...BASE_SKILLS,
      ...OFFICE_SKILLS,
    ],
    agentPaths: BASE_AGENTS,
    commandPaths: BASE_COMMANDS,
    dataPaths: [
      'user-settings.json',
    ],
    agentsDataPaths: [],
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Skills bureautiques (Word, Excel, PowerPoint, PDF)',
      'Générateur de prompts optimisés',
      'Création d\'images IA',
      'Créateur de skills personnalisés',
      'Agents de base (diagnostic, auto-amélioration)',
      'Review adversariale (optimisation multi-agents)',
    ],
  },
  {
    id: 'latex',
    name: 'LaTeX Enseignant',
    subtitle: 'Documents pédagogiques LaTeX',
    description: 'Le bundle Généraliste + l\'arsenal complet LaTeX : cours, exercices, évaluations, présentations Beamer et Reveal.js, QCM, contenus H5P et Moodle, programmes officiels.',
    icon: '📐',
    color: 'cosmic',
    tier: 2,
    skills: [
      ...BASE_SKILLS,
      ...OFFICE_SKILLS,
      // LaTeX
      'bfcours-latex',
      'tex-document-creator',
      'tex-compiling-skill',
      'beamer-presentation',
      'latex',
      'latex-geometry',
      'pdf2tikz',
      'programmes-officiels',
      'reveals-presentation',
      // Évaluation & contenus pédagogiques
      'qcm-creator',
      'h5p-branching-scenario',
      'h5p-gamemap',
      'moodle-course-creator',
      'make-blueprint-eval',
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
      'outillage/documentation',
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
      'QF-models',
    ],
    agentsDataPaths: [
      'main-latex-knowledge.md',
      'tkz-euclide-master',
      'nicematrix-expert',
      'proflycee-expert',
      'tcolorbox-expert',
    ],
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Tout le bundle Généraliste inclus',
      'Package bfcours pour documents éducatifs',
      'Compilation LaTeX automatisée',
      'Présentations Beamer et Reveal.js',
      'QCM et évaluations automatisées',
      'Contenus H5P et Moodle',
      'Extraction des programmes officiels',
      'Géométrie LaTeX et conversion PDF→TikZ',
    ],
  },
  {
    id: 'word',
    name: 'Word Enseignant',
    subtitle: 'Documents pédagogiques Word',
    description: 'Le bundle Généraliste + le générateur de documents Word style "Loiseau", les skills Moodle et les outils bureautiques avancés pour l\'enseignement.',
    icon: '📝',
    color: 'sky',
    tier: 2,
    skills: [
      ...BASE_SKILLS,
      ...OFFICE_SKILLS,
      // Word spécialisé
      'docx-loiseau',
      // Contenus pédagogiques
      'qcm-creator',
      'h5p-branching-scenario',
      'h5p-gamemap',
      'moodle-course-creator',
      'programmes-officiels',
      'make-blueprint-eval',
    ],
    agentPaths: [
      ...BASE_AGENTS,
      'creer/documentation',
      'creer/evaluation',
      'creer/html',
    ],
    commandPaths: [
      ...BASE_COMMANDS,
      'creer/evaluation',
      'creer/html',
      'creer/moodle',
      'modifier/html',
      'outillage/documentation',
      'outillage/recherche',
    ],
    dataPaths: [
      'user-settings.json',
      'competences',
      'competences.json',
      'competence-server-user-preferences.json',
      'QF-models',
    ],
    agentsDataPaths: [],
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Tout le bundle Généraliste inclus',
      'Générateur Word "L\'Oiseau" (mise en page pro)',
      'QCM et évaluations automatisées',
      'Contenus H5P et Moodle',
      'Extraction des programmes officiels',
      'Skills bureautiques complets',
    ],
  },
  {
    id: 'avance',
    name: 'Power User',
    subtitle: 'L\'arsenal complet',
    description: 'Tous les bundles réunis + les skills avancés : applications éducatives, animations interactives, fiches techniques, infographies, notebooks Jupyter, et bien plus. Avec le CLAUDE.md auto-amélioration.',
    icon: '🚀',
    color: 'purple',
    tier: 3,
    skills: [
      ...BASE_SKILLS,
      ...OFFICE_SKILLS,
      'bfcours-latex', 'tex-document-creator', 'tex-compiling-skill', 'beamer-presentation',
      'latex', 'latex-geometry', 'pdf2tikz', 'programmes-officiels', 'reveals-presentation',
      'docx-loiseau',
      'qcm-creator', 'h5p-branching-scenario', 'h5p-gamemap', 'moodle-course-creator',
      'tex-fiche-technique', 'educational-app-builder', 'infography-generator',
      'interactive-animation', 'jupyter', 'jsxgraph', 'html-katex-compiler',
      'mind-map-creator', 'icons-generator', 'agent-generator', 'make-blueprint-eval',
      'bareme-actions-eleves', 'self-improve', 'stats-datagouv', 'teamPlay',
    ],
    agentPaths: ['*'],
    commandPaths: ['*'],
    dataPaths: ['*'],
    agentsDataPaths: ['*'],
    claudeMdFile: 'CLAUDE-autoAmelioration.md',
    highlights: [
      'Tous les bundles précédents inclus',
      'Création d\'applications éducatives Flask',
      'Animations interactives HTML/JS',
      'Fiches techniques pédagogiques',
      'Infographies et notebooks Jupyter',
      'CLAUDE.md avec auto-amélioration',
      'Tous les agents et commandes',
    ],
  },
]

/**
 * Returns true if pkgA fully includes pkgB.
 * Power User (tier 3) includes everything.
 * Tier 2 packages (latex, word) include Généraliste (tier 1) but NOT each other.
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
