export type PackageTier = 'generaliste' | 'latex' | 'typst' | 'avance'

/** Packs dédiés à un skill (le skill + les skills qu'il appelle + leurs dépendances) */
export type SkillPackId = 'skill-latex' | 'skill-reveals' | 'skill-capsule-video' | 'skill-bareme' | 'skill-typst'
  | 'skill-grill-me' | 'skill-programmes-progression'

/** Tout identifiant téléchargeable par /api/download-package */
export type PackageId = PackageTier | SkillPackId

export interface AIPackage<Id extends string = PackageTier> {
  id: Id
  name: string
  subtitle: string
  description: string
  icon: string
  color: string
  tier: number // 0 = pack d'un skill, 1 = base, 2 = spécialisé, 3 = complet
  skills: string[]
  agentPaths: string[]
  commandPaths: string[]
  dataPaths: string[]
  agentsDataPaths: string[]
  /** Fichiers de claude-setup/mcp_servers/ requis par les scripts des skills ('*' = tout) */
  mcpServerPaths?: string[]
  claudeMdFile: string
  highlights: string[]
  /**
   * Pack d'un skill : l'archive ne contient que .claude/ (skills, mcp_servers, datas)
   * et un LISEZMOI dans .claude/ — pas de CLAUDE.md, settings.json, hooks ni scripts partagés.
   * Elle peut donc se décompresser directement dans un projet existant.
   */
  skillOnly?: boolean
  /** Modules pip nécessaires aux scripts des skills (affichés dans la page et le LISEZMOI) */
  pythonDeps?: string
  /**
   * Ligne finale de la liste du contenu, sur la page du pack.
   * Absente : « Les modèles, guides et scripts Python dont ces skills ont besoin » ; null : aucune ligne.
   */
  annexes?: string | null
  /**
   * Prérequis du LISEZMOI pour un pack de skill sans page de skill (SKILL_PAGES) :
   * par exemple un pack téléchargé depuis un tutoriel.
   */
  prerequis?: string[]
}

/**
 * Serveurs Python importés par les scripts de tex-document-creator et tex-compiling-skill
 * (ils remontent de quatre niveaux jusqu'à .claude/mcp_servers/).
 */
const LATEX_MCP_SERVERS = [
  'document_creator_server.py',
  'latex_compiler_server.py',
  'requirements.txt',
]

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

// Skills pédagogiques du bundle Typst : ceux qui ne passent ni par LaTeX ni par des fichiers .tex.
// Exclus : bareme-actions-eleves, make-blueprint-eval, audit-accessibilite-eval (lisent des sujets .tex)
// et stats-datagouv (sortie LaTeX bfcours). reveals-presentation : seules ses figures TikZ sont facultatives.
const TYPST_CONTENT_SKILLS = [
  'programmes-officiels',
  'progression-builder',
  'h5p-branching-scenario',
  'h5p-gamemap',
  'moodle-course-creator',
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
    mcpServerPaths: LATEX_MCP_SERVERS,
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Tout le bundle Généraliste inclus',
      'Package bfcours pour documents éducatifs en LaTeX',
      'Compilation LaTeX automatisée et relecture visuelle',
      'QCM au format bfcours et barèmes',
      'Présentations Reveal.js',
      'Contenus H5P et Moodle',
      'Programmes officiels sourcés et progressions',
      'Géométrie LaTeX et conversion PDF→TikZ',
    ],
  },
  {
    id: 'typst',
    name: 'Typst Enseignant',
    subtitle: 'Documents pédagogiques Typst',
    description: 'Le bundle Généraliste + les skills Typst : cours, fiches d\'exercices et évaluations avec la suite farfadet, versions professeur et élève, préconversion d\'un cours LaTeX bfcours. Avec les skills de contenus pédagogiques qui ne dépendent pas de LaTeX. La suite farfadet elle-même s\'installe à part (page Packages Typst).',
    icon: '🪶',
    color: 'teal',
    tier: 2,
    skills: [
      ...BASE_SKILLS,
      'bfcours-typst',
      'typst',
      ...TYPST_CONTENT_SKILLS,
    ],
    agentPaths: BASE_AGENTS,
    commandPaths: BASE_COMMANDS,
    dataPaths: [
      'user-settings.json',
    ],
    agentsDataPaths: [],
    pythonDeps: 'typst pymupdf',
    claudeMdFile: 'CLAUDE-simple.md',
    highlights: [
      'Tout le bundle Généraliste inclus',
      'Documents Typst avec la suite farfadet (bfcours-typst et typst)',
      'Préconversion d\'un cours LaTeX bfcours en Typst',
      'Compilation des versions professeur et élève',
      'Programmes officiels, progressions, Reveal.js, contenus H5P et Moodle',
      'La suite farfadet s\'installe à part : voir la page Packages Typst',
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
      'bfcours-typst', 'typst', 'capsule-video', 'jupyter-notebook', 'mind-map-creator',
    ],
    agentPaths: ['*'],
    commandPaths: ['*'],
    dataPaths: ['*'],
    agentsDataPaths: ['*'],
    mcpServerPaths: ['*'],
    claudeMdFile: 'CLAUDE-autoAmelioration.md',
    highlights: [
      'Tous les bundles précédents inclus',
      'Documents Typst (bfcours-typst et typst)',
      'Capsules vidéo animées avec voix de synthèse',
      'Notebooks Jupyter et cartes mentales',
      'CLAUDE.md avec auto-amélioration',
      'Tous les agents et commandes',
    ],
  },
]

/**
 * Packs dédiés à un skill, téléchargeables depuis la page de présentation du skill.
 * Chaque pack = le skill + les skills qu'il enchaîne + les fichiers dont leurs scripts ont besoin.
 * Pour en déclarer un nouveau : ajouter l'id à SkillPackId, puis une entrée ici (tier 0, skillOnly).
 */
export const SKILL_PACKS: AIPackage<SkillPackId>[] = [
  {
    id: 'skill-latex',
    name: 'Skill latex',
    subtitle: 'De la demande au PDF relu',
    description: 'Le skill latex et les skills qu\'il enchaîne : créer le document à partir d\'un modèle, l\'écrire avec bfcours, le compiler, puis relire le PDF et en améliorer la mise en page.',
    icon: '📄',
    color: 'cosmic',
    tier: 0,
    skills: [
      'latex',                // orchestrateur
      'tex-document-creator', // 1. créer
      'bfcours-latex',        // 2. écrire
      'choix-didactiques',    // 2. écrire : le fond pédagogique (cité par le diaporama)
      'tex-compiling-skill',  // 3. compiler
      'latex-visual-review',  // 4. regarder et améliorer
      'pdf2tikz',             // étape 0 : reprendre les figures d'un PDF source
      'programmes-officiels', // étape 0 : attendus du BO (cité par le diaporama et appelé par latex)
    ],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [
      'latex-modeles',
      'create-document-user-preferences.json',
      'latex-compiler-preferences.json',
    ],
    agentsDataPaths: [],
    mcpServerPaths: LATEX_MCP_SERVERS,
    claudeMdFile: '',
    skillOnly: true,
    // mcp : serveurs de création/compilation ; pymupdf, numpy, Pillow : capture et mesure des pages
    pythonDeps: 'mcp pymupdf numpy Pillow',
    highlights: [
      'latex : enchaîne les quatre étapes',
      'tex-document-creator : crée le document à partir d\'un modèle',
      'bfcours-latex : écrit le contenu avec les environnements bfcours',
      'choix-didactiques : le fond pédagogique (jeux de données, symétrie énoncé / corrigé, format de fiche)',
      'tex-compiling-skill : compile et corrige les erreurs',
      'latex-visual-review : relit le PDF et améliore la mise en page',
      'pdf2tikz : reprend les figures d\'un PDF source',
      'programmes-officiels : les attendus du BO du niveau visé',
    ],
  },
  {
    id: 'skill-reveals',
    name: 'Skill reveals',
    subtitle: 'De la demande au diaporama prêt à projeter',
    description: 'Le skill reveals-presentation : un diaporama reveal.js à partir d\'une demande ou d\'un document, sur trois gabarits (collège, lycée, conférence), fil de la séance de gauche à droite et détails en dessous, figures TikZ reprises en images.',
    icon: '🎞️',
    color: 'cosmic',
    tier: 0,
    // Le skill est autonome : gabarits et exemples dans assets/, guides dans references/,
    // scripts en bibliothèque standard Python (LuaLaTeX et pdftoppm/Ghostscript/ImageMagick
    // seulement pour les figures TikZ). L'agent reveals-creator et la commande /createReveals
    // ne sont pas inclus : propres à Claude Code et redondants avec le skill.
    skills: ['reveals-presentation'],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    highlights: [
      'reveals-presentation : cadre, construit et contrôle le diaporama',
      'Trois gabarits au design figé : collège, lycée, académique',
      'Guides : cours en quatre niveaux, exercices à une diapo par question, navigation 2D',
      'Deux présentations complètes servant de modèles (cours, exercices)',
      'Scripts : figures TikZ et PDF en images, version autonome à partager',
    ],
  },
  {
    id: 'skill-capsule-video',
    name: 'Skill capsules vidéo',
    subtitle: 'De la demande à la vidéo animée',
    description: 'Le skill capsule-video : une correction ou une explication devient une vidéo MP4 dont chaque geste suit la voix. L\'agent relit l\'exercice, écrit le texte comme une copie modèle, le fait lire par une voix de synthèse locale (ou part de votre enregistrement), cale chaque geste sur un mot puis filme la vidéo.',
    icon: '🎬',
    color: 'cosmic',
    tier: 0,
    // Le skill est autonome : moteur canvas (MathJax, GSAP, polices, three.js embarqués) dans assets/,
    // scripts Python dans scripts/, installeur des logiciels dans installation/.
    // Exclus : config.json (chemins du poste, voix clonée personnelle ; l'installeur en écrit un neuf),
    // tout échantillon de voix, et les outils lourds (Chromium, FFmpeg, Pocket TTS, MFA, Parakeet,
    // Whisper, Piper : ≈ 6 Go) que l'installeur télécharge dans le dossier choisi.
    skills: ['capsule-video'],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    // Pas de pythonDeps : l'installeur crée ses propres environnements Python (rendu, Pocket, Parakeet, MFA)
    highlights: [
      'capsule-video : prépare, écrit, fait dire et anime la capsule',
      'Moteur d\'animation canvas : formules, figures, tableaux, tuiles algébriques, scènes 3D',
      'Guides : rigueur d\'une copie modèle, écriture pour l\'oreille, catalogue des gestes, design',
      'Six capsules d\'exemple (correction, figure, tableau croisé, tuiles, tutoriel logiciel)',
      'Installeur Windows (et Linux/macOS non testé) des logiciels gratuits, sans aucune voix clonée',
    ],
  },
  {
    id: 'skill-bareme',
    name: 'Skill barème détaillé',
    subtitle: 'Du sujet corrigé au barème justifié',
    description: 'Le skill bareme-actions-eleves et la commande /bareme : l\'agent lit le sujet et son corrigé, découpe chaque corrigé en actions d\'élève visibles sur la copie, calcule les points (actions × coefficient), la conversion sur 20 et la densité du sujet.',
    icon: '⚖️',
    color: 'cosmic',
    tier: 0,
    // Aucun script : le skill n'a qu'une fiche (SKILL.md) et une interface HTML autonome (templates/bareme.html).
    // La commande /bareme déroule le protocole ; bfcours-latex n'est pas embarqué (le sujet existe déjà).
    skills: ['bareme-actions-eleves'],
    agentPaths: [],
    commandPaths: ['creer/evaluation/bareme.md'],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    highlights: [
      'bareme-actions-eleves : règles d\'atomisation, coefficients, formules, seuils de densité',
      'Commande /bareme : le protocole pas à pas, du .tex au barème',
      'Interface bareme.html : relire et ajuster le barème, synthèse, export CSV',
    ],
    annexes: 'Aucun script ni module Python : l\'agent lit, compte et écrit lui-même',
  },
  {
    id: 'skill-typst',
    name: 'Skill Typst',
    subtitle: 'De la demande aux PDF professeur et élève',
    description: 'Le skill bfcours-typst et le skill typst : l\'agent part de votre cours LaTeX bfcours (préconversion automatique) ou d\'un document modèle, écrit avec la suite farfadet, compile les versions professeur et élève puis regarde les pages avant de livrer.',
    icon: '🪶',
    color: 'cosmic',
    tier: 0,
    // Skills autonomes : scripts Python (bibliothèque standard + module typst ; PyMuPDF pour les images
    // de contrôle), index des fonctions dans bfcours-typst/scripts/donnees/. Aucun mcp_servers ni datas.
    // La suite farfadet elle-même (paquets, polices, bfwatch) s'installe par la page Packages Typst
    // (installateur de la Forge) : localiser.py la retrouve sans chemin en dur.
    // Non inclus : typst-creation et typst-documentation (développement de paquets, pas de documents élèves).
    skills: [
      'bfcours-typst',     // partir, écrire, compiler, regarder
      'typst',             // le langage en plus long (facultatif)
      'choix-didactiques', // fond pédagogique d'un document élève (cité par le diaporama)
    ],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    pythonDeps: 'typst pymupdf',
    highlights: [
      'bfcours-typst : convertit, écrit, compile et contrôle les documents farfadet',
      'convertir.py : préconversion d\'un .tex bfcours, rapport des points à reprendre',
      'compiler.py : versions professeur et élève, extraits LaTeX, images de contrôle',
      'chercher.py : la bonne fonction et ses options, aussi par nom de commande LaTeX',
      'Documents complets à imiter : cours, fiche d\'exercices, évaluation, QCM',
      'typst : le langage, les figures cetz, la correspondance LaTeX → Typst',
      'choix-didactiques : le fond pédagogique d\'un document élève',
    ],
    annexes: 'La suite farfadet elle-même s\'installe à part, en une commande (page Packages Typst)',
  },
  {
    id: 'skill-grill-me',
    name: 'Skill grill-me',
    subtitle: 'Se faire interviewer avant de se lancer',
    description: 'Le skill grill-me seul : avant de produire, l\'agent vous interroge par manches de questions à choix, chacune avec sa recommandation, jusqu\'à ce que rien ne reste implicite. Il sert notamment à préciser un skill avant de le faire écrire par skill-creator. skill-creator n\'est pas inclus : il est fourni et maintenu par Anthropic.',
    icon: '🎤',
    color: 'cosmic',
    tier: 0,
    // Skill autonome : SKILL.md, guide du format de manche (references/), gabarit HTML et exemple (assets/),
    // deux scripts en bibliothèque standard Python (page de manche, petit serveur local pour la dictée).
    // Ni mcp_servers ni datas. wayfinder (qui peut l'appeler) n'est pas inclus.
    // Téléchargé depuis le tutoriel « Créer son propre skill » (pas de page de skill dédiée).
    skills: ['grill-me'],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    highlights: [
      'grill-me : interview par manches, une recommandation argumentée par question',
      'Deux modes : questions dans le terminal, ou page web cliquable avec dictée vocale',
      'Récapitulatif des décisions, validé par vous avant toute action',
    ],
    annexes: 'Aucun module Python à installer : les scripts n\'utilisent que la bibliothèque standard',
    prerequis: [
      'Claude Code (ou Codex). Le mode terminal s\'appuie sur les questions à choix de Claude Code ; avec Codex, préférez la page web.',
      'Python 3, seulement pour le mode page web (aucun module à installer).',
      'Chrome ou Edge pour la dictée vocale de la page web (facultatif ; sinon Win + H sous Windows).',
      'skill-creator n\'est pas inclus : il est fourni et maintenu par Anthropic. Claude Code : /plugin install skill-creator@claude-plugins-official. Codex : $skill-creator, intégré.',
      'Tutoriel pas à pas : https://bfcours.dev/claude-code/tutorials/creer-un-skill',
    ],
  },
  {
    id: 'skill-programmes-progression',
    name: 'Skills programmes et progression',
    subtitle: 'Du BO 2026 à la progression annuelle',
    description: 'Les skills programmes-officiels et progression-builder : l\'agent cherche dans les programmes de mathématiques de la rentrée 2026 (CM1 à Terminale), cite le BO mot pour mot avec le PDF et la page, puis construit avec vous une progression annuelle dans une fiche HTML interactive et la vérifie.',
    icon: '🏛️',
    color: 'cosmic',
    tier: 0,
    // progression-builder lit ../programmes-officiels/data/json/ : les deux skills voyagent ensemble.
    // Consultation et construction : bibliothèque standard Python (sqlite3 pour la recherche).
    // PyMuPDF (facultatif) ne sert qu'à régénérer les images de pages du BO (scripts/regenerer_pages.py) et à reconstruire la base avec un nouveau BO ; jsonschema à la validation.
    // Archive allégée (≈ 20 Mo décompressés) : PDF du BO, fiches vierges avec BO embarqué ; les images de pages ne sont pas fournies.
    skills: ['programmes-officiels', 'progression-builder'],
    agentPaths: [],
    commandPaths: [],
    dataPaths: [],
    agentsDataPaths: [],
    mcpServerPaths: [],
    claudeMdFile: '',
    skillOnly: true,
    highlights: [
      'programmes-officiels : 13 niveaux, 1 738 compétences, formulation du BO extraite du PDF',
      'Un script par question : recherche, fiche d\'une compétence, démonstrations, algorithmes, progression d\'une notion, comparaison de niveaux',
      'Preuves : PDF du BO, texte de chaque page, image de page régénérée à la demande',
      'progression-builder : fiche HTML de progression par glisser-déposer, BO embarqué',
      'Treize fiches vierges prêtes, du CM1 à la Terminale',
      'Validateur de progression : codes inconnus, doublons, couverture',
    ],
    annexes: 'Aucun module Python à installer pour consulter et construire (PyMuPDF, facultatif, seulement pour régénérer les images de pages du BO ou reconstruire la base avec un nouveau BO)',
  },
]

/** Bundles et packs de skills réunis (résolution des téléchargements et des doublons du panier) */
export const ALL_PACKAGES: AIPackage<PackageId>[] = [...AI_PACKAGES, ...SKILL_PACKS]

/**
 * Returns true if pkgA fully includes pkgB.
 * Power User (tier 3) includes everything.
 * Tier 2 packages (latex, typst) include Généraliste (tier 1), mais pas l'un l'autre.
 * Un bundle inclut un pack de skill (tier 0) s'il contient tous ses skills.
 * Same package includes itself.
 */
export function packageIncludes(pkgAId: PackageId, pkgBId: PackageId): boolean {
  if (pkgAId === pkgBId) return true
  const a = ALL_PACKAGES.find(p => p.id === pkgAId)
  const b = ALL_PACKAGES.find(p => p.id === pkgBId)
  if (!a || !b) return false
  // Un pack de skill n'inclut aucun autre package
  if (a.tier === 0) return false
  // Power User includes everything
  if (a.tier === 3) return true
  // Pack de skill : inclus si le bundle en contient tous les skills
  if (b.tier === 0) return b.skills.every(s => a.skills.includes(s))
  // Tier 2 includes only tier 1
  if (a.tier === 2 && b.tier === 1) return true
  return false
}

/**
 * Find redundant packages in a list.
 * Returns packages that are already included by another package in the list.
 */
export function findRedundantPackages(packageIds: PackageId[]): {
  redundant: PackageId[]
  reason: Record<PackageId, PackageId> // redundant → included by
} {
  const redundant: PackageId[] = []
  const reason: Record<string, PackageId> = {}

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

  return { redundant, reason: reason as Record<PackageId, PackageId> }
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
