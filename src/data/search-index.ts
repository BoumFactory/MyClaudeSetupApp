import { PARCOURS, CAPSULES } from '@/data/parcours'
import { VOCABULARY } from '@/data/vocabulary'
import { AI_PACKAGES } from '@/data/ai-packages'
import categoriesData from '@/../public/render/Reveals/categories.json'

export type SearchCategory =
  | 'tutoriel'
  | 'presentation'
  | 'package'
  | 'application'
  | 'formation'
  | 'video'
  | 'vocabulaire'

export interface SearchableItem {
  id: string
  title: string
  description: string
  category: SearchCategory
  categoryLabel: string
  tags: string[]
  url: string
  /** Extended content for deep search (stripped HTML) */
  content?: string
  /** Icon emoji or name */
  icon?: string
  /** Additional metadata for display */
  meta?: Record<string, string>
}

function stripHtml(html: string): string {
  return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim()
}

export function buildSearchIndex(): SearchableItem[] {
  const items: SearchableItem[] = []

  // ============ 1. Tutorials from parcours ============
  for (const parcours of PARCOURS) {
    items.push({
      id: `parcours-${parcours.id}`,
      title: parcours.title,
      description: parcours.description,
      category: 'tutoriel',
      categoryLabel: 'Parcours tutoriel',
      tags: ['parcours', 'tutoriel'],
      url: `/claude-code/tutorials/parcours/${parcours.id}`,
      icon: parcours.icon,
      meta: {
        type: 'Parcours',
        capsules: `${parcours.capsules.length} capsules`,
      },
    })
  }

  // Capsules from CAPSULES object — each capsule has its own page
  for (const capsule of Object.values(CAPSULES)) {
    const contentParts: string[] = []
    if (capsule.sections?.info) contentParts.push(capsule.sections.info)
    if (capsule.sections?.exemple) contentParts.push(capsule.sections.exemple)
    if (capsule.sections?.pratique) contentParts.push(capsule.sections.pratique)

    // Find parent parcours title for display
    const parentParcours = PARCOURS.find(p => p.id === capsule.parcours)

    items.push({
      id: `capsule-${capsule.id}`,
      title: capsule.title,
      description: capsule.description,
      category: 'tutoriel',
      categoryLabel: `Capsule — ${parentParcours?.title || capsule.parcours}`,
      tags: [
        ...(capsule.tags || []),
        'capsule',
        capsule.parcours,
      ],
      url: `/claude-code/tutorials/parcours/${capsule.parcours}/${capsule.id}`,
      content: stripHtml(contentParts.join(' ')),
      meta: {
        parcours: parentParcours?.title || capsule.parcours,
        duration: capsule.duration || '',
      },
    })
  }

  // ============ 2. Installation guides (static) ============
  const installationGuides = [
    {
      id: 'python-install',
      title: 'Installation Python',
      description: 'Guide complet pour installer Python et configurer votre environnement',
      url: '/claude-code/tutorials/python-install',
      tags: ['python', 'installation', 'prérequis'],
    },
    {
      id: 'nodejs-install',
      title: 'Installation Node.js',
      description: 'Installer Node.js et npm pour Claude Code et les outils web',
      url: '/claude-code/tutorials/nodejs-install',
      tags: ['nodejs', 'installation', 'prérequis'],
    },
    {
      id: 'vscode-miktex',
      title: 'VS Code + MiKTeX',
      description: 'Configuration de VS Code et MiKTeX pour LaTeX',
      url: '/claude-code/tutorials/vscode-miktex',
      tags: ['vscode', 'miktex', 'latex', 'installation'],
    },
    {
      id: 'claude-desktop-install',
      title: 'Installation Claude Desktop',
      description: 'Installer et configurer l\'application Claude Desktop',
      url: '/claude-code/tutorials/claude-desktop-install',
      tags: ['claude desktop', 'installation', 'setup'],
    },
    {
      id: 'claude-code-install',
      title: 'Installation Claude Code',
      description: 'Installer Claude Code CLI et ses dépendances',
      url: '/claude-code/tutorials/claude-code-install',
      tags: ['claude code', 'cli', 'installation'],
    },
    {
      id: 'claude-code-config',
      title: 'Configuration Claude Code',
      description: 'Configurer Claude Code avec vos skills et agents',
      url: '/claude-code/tutorials/claude-code-config',
      tags: ['configuration', 'claude code', 'setup'],
    },
    {
      id: 'google-api-setup',
      title: 'Configuration API Google',
      description: 'Activer l\'API Google Imagen pour la génération d\'images',
      url: '/claude-code/tutorials/google-api-setup',
      tags: ['api', 'google', 'imagen', 'configuration'],
    },
    {
      id: 'bfcours-setup',
      title: 'Configuration bfcours',
      description: 'Installer et configurer le package LaTeX bfcours',
      url: '/claude-code/tutorials/bfcours-setup',
      tags: ['bfcours', 'latex', 'configuration'],
    },
    {
      id: 'utilisation-config',
      title: 'Utilisation et configuration avancée',
      description: 'Guide avancé pour optimiser votre configuration',
      url: '/claude-code/tutorials/utilisation-config',
      tags: ['configuration', 'utilisation', 'avancé'],
    },
  ]

  for (const guide of installationGuides) {
    items.push({
      id: guide.id,
      title: guide.title,
      description: guide.description,
      category: 'tutoriel',
      categoryLabel: 'Guide d\'installation',
      tags: guide.tags,
      url: guide.url,
    })
  }

  // ============ 3. Presentations ============
  // Human-readable titles for presentation slugs
  const presentationTitles: Record<string, string> = {
    'architecture-claude-code-reveals': 'Architecture Claude Code',
    'claude-code-interface': 'Interface Claude Code',
    'commandes-disponibles': 'Commandes disponibles',
    'tex-document-creator-system': 'Tex Document Creator',
    'agent-make-images': 'Agent Make Images',
    'skill-creator-system': 'Skill Creator',
    'beamer-presentation-system': 'Beamer Presentation',
    'reveals-presentation-system': 'Reveals Presentation',
    'programmes-officiels-system': 'Programmes Officiels',
    'bfcours-latex-system': 'Package bfcours LaTeX',
    'educational-app-builder-system': 'Educational App Builder',
    'jupyter-notebook-skill': 'Jupyter Notebook',
    'interactive-animation-skill': 'Interactive Animation',
    'qcm-creator-skill': 'QCM Creator',
    'infography-generator-skill': 'Infography Generator',
    'blueprint-eval-skill': 'Blueprint Eval',
  }

  const categories = categoriesData as any

  if (categories.categories) {
    for (const category of categories.categories) {
      for (const subcategory of category.subcategories || []) {
        for (const presentation of subcategory.presentations || []) {
          const title = presentationTitles[presentation.slug]
            || presentation.slug.replace(/-/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase())

          items.push({
            id: `pres-${presentation.slug}`,
            title,
            description: presentation.comment || '',
            category: 'presentation',
            categoryLabel: `Présentation — ${subcategory.name}`,
            tags: [
              ...(presentation.tags || []),
              presentation.level || '',
              category.name,
              'diaporama', 'présentation',
            ].filter(Boolean),
            url: `/claude-code/presentations/${presentation.slug}`,
            meta: {
              level: presentation.level || '',
              category: category.name,
              subcategory: subcategory.name,
            },
          })
        }
      }
    }
  }

  // ============ 4. AI Packages ============
  for (const pkg of AI_PACKAGES) {
    const highlights = pkg.highlights || []
    const tags = [
      ...highlights.slice(0, 5).map((h: string) => h.toLowerCase()),
      'package',
      'téléchargement',
      'setup',
      'claude code',
    ]

    items.push({
      id: `pkg-${pkg.id}`,
      title: `Package ${pkg.name}`,
      description: pkg.description,
      category: 'package',
      categoryLabel: 'Package IA',
      tags: tags.filter(Boolean),
      url: `/claude-code/download-ai-packages#package-${pkg.id}`,
      icon: pkg.icon,
      content: [
        ...highlights,
        ...pkg.skills,
      ].join(' '),
      meta: {
        tier: `Niveau ${pkg.tier}`,
        skills: `${pkg.skills.length} skills`,
      },
    })
  }

  // ============ 5. Applications ============
  const applications = [
    {
      id: 'app-second-degre',
      title: 'Second Degré - Partie 2',
      description: 'Application Flask interactive pour l\'apprentissage des équations du second degré (signe, tableau de variations, extremum)',
      url: '/claude-code/applications/educatives#second-degre',
      tags: ['app flask', 'maths', 'second degré', 'équations', 'python'],
      categoryLabel: 'Application éducative — Flask',
    },
    {
      id: 'app-produit-scalaire',
      title: 'Produit Scalaire',
      description: 'Animation interactive pour visualiser et comprendre le produit scalaire de deux vecteurs',
      url: '/claude-code/applications/educatives#produit-scalaire',
      tags: ['animation', 'géométrie', 'vecteurs', 'produit scalaire', 'html'],
      categoryLabel: 'Application éducative — Animation',
    },
    {
      id: 'app-trigonometrie',
      title: 'Trigonométrie',
      description: 'Animation du cercle trigonométrique avec visualisation des fonctions sin, cos et tan',
      url: '/claude-code/applications/educatives#trigo',
      tags: ['animation', 'cercle trigonométrique', 'trigonométrie', 'html'],
      categoryLabel: 'Application éducative — Animation',
    },
    {
      id: 'app-gestionnaire-prompts',
      title: 'Gestionnaire de Prompts',
      description: 'Application Tauri pour stocker, organiser et créer des prompts IA. Arbre décisionnel, fabricateur de prompts et générateur de résumés.',
      url: '/claude-code/applications/educatives#prompt-manager',
      tags: ['application', 'prompts', 'templates', 'productivité', 'tauri'],
      categoryLabel: 'Application éducative — Tauri',
    },
    {
      id: 'app-revisions',
      title: 'Application de Révisions',
      description: 'Application Tauri de révision multi-matières avec QCM et questions libres. Support LaTeX pour les maths.',
      url: '/claude-code/applications/educatives#global-revision',
      tags: ['qcm', 'révisions', 'multi-matières', 'évaluation', 'tauri', 'latex'],
      categoryLabel: 'Application éducative — Tauri',
    },
    {
      id: 'app-python-lycee',
      title: 'Python pour le Lycée',
      description: 'Notebook Jupyter pour enseigner Python aux mathématiques avec numpy et matplotlib',
      url: '/claude-code/applications/educatives#python-lycee',
      tags: ['jupyter', 'notebook', 'python', 'numpy', 'matplotlib'],
      categoryLabel: 'Application éducative — Jupyter',
    },
    {
      id: 'app-bftools',
      title: 'BFtools',
      description: 'Suite d\'outils de productivité et d\'automatisation pour enseignants sur GitHub',
      url: '/claude-code/applications/logiciels',
      tags: ['outils', 'enseignant', 'productivité', 'github', 'automatisation'],
      categoryLabel: 'Logiciel enseignant',
    },
  ]

  for (const app of applications) {
    items.push({
      id: app.id,
      title: app.title,
      description: app.description,
      category: 'application',
      categoryLabel: app.categoryLabel,
      tags: app.tags,
      url: app.url,
    })
  }

  // ============ 6. Formations ============
  const formations = [
    {
      id: 'formation-latex',
      title: 'Formation LaTeX',
      description: 'Formation complète pour maîtriser LaTeX et produire des documents mathématiques professionnels',
      url: '/formations/latex',
      tags: ['formation', 'latex', 'mathématiques', 'documents'],
    },
    {
      id: 'formation-ia-latex',
      title: 'Formation IA & LaTeX',
      description: 'Combinaison de l\'IA et de LaTeX pour automatiser la création de ressources pédagogiques',
      url: '/formations/ia-latex',
      tags: ['formation', 'ia', 'latex', 'claude code', 'automatisation'],
    },
  ]

  for (const formation of formations) {
    items.push({
      id: formation.id,
      title: formation.title,
      description: formation.description,
      category: 'formation',
      categoryLabel: 'Formation',
      tags: formation.tags,
      url: formation.url,
    })
  }

  // ============ 7. Videos ============
  items.push({
    id: 'videos-claude-code',
    title: 'Vidéos Claude Code',
    description: 'Tutoriels vidéo et démonstrations de Claude Code sur YouTube',
    category: 'video',
    categoryLabel: 'Vidéo',
    tags: ['vidéo', 'youtube', 'démonstration', 'tutoriel'],
    url: '/claude-code/videos',
  })

  // ============ 8. Vocabulary ============
  for (const term of VOCABULARY) {
    const vocabId = term.term.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')

    items.push({
      id: `vocab-${vocabId}`,
      title: term.term,
      description: stripHtml(term.definition),
      category: 'vocabulaire',
      categoryLabel: 'Vocabulaire',
      tags: [
        term.term.toLowerCase(),
        ...(term.aliases || []).map(a => a.toLowerCase()),
        'vocabulaire',
        'définition',
      ].filter(Boolean),
      url: term.docUrl || '/claude-code/tutorials/parcours/quick-view/qv-overview',
      meta: term.docUrl ? { lien: 'Documentation officielle' } : { lien: 'Voir dans le tutoriel Quick View' },
    })
  }

  return items
}

// Cache the index
let cachedIndex: SearchableItem[] | null = null

export function getSearchIndex(): SearchableItem[] {
  if (!cachedIndex) {
    cachedIndex = buildSearchIndex()
  }
  return cachedIndex
}

export function invalidateSearchCache(): void {
  cachedIndex = null
}
