import Link from 'next/link'
import type { Metadata } from 'next'
import {
  Package,
  BookOpen,
  FileText,
  ExternalLink,
  Download,
  Terminal,
  Video,
  Sparkles,
  AlertTriangle,
  Zap,
  Eye,
  PenLine,
  ArrowRight,
  Github,
} from 'lucide-react'

export const metadata: Metadata = {
  title: 'Packages Typst farfadet',
  description:
    "farfadet : la suite de 25 paquets Typst pour écrire cours, exercices et évaluations de mathématiques, en version professeur et élève. Installation en une commande, documentation et application Écriture Typst.",
}

const FORGE = 'https://forge.apps.education.fr/romaindeschamps/farfadet'
const FORGE_RAW = `${FORGE}/-/raw/main`

const REPO_URL = FORGE
const DOC_URL = `${FORGE}/-/blob/main/farfadet-documentation.pdf`
const README_URL = `${FORGE}/-/blob/main/README.md`
const APP_URL = `${FORGE_RAW}/application/ecriture-typst.html`
const APP_PAGE_URL = `${FORGE}/-/blob/main/application/ecriture-typst.html`
// Hébergée sur le site : la Forge ne gère pas les requêtes partielles, la balise <video> n'y lit pas le fichier
const VIDEO_URL = '/videos/ecriture-typst-prise-en-main.mp4'

const INSTALL_COMMANDS: { os: string; shell: string; command: string }[] = [
  {
    os: 'Windows',
    shell: 'PowerShell',
    command: `irm ${FORGE_RAW}/install/windows.ps1 | iex`,
  },
  {
    os: 'macOS',
    shell: 'Terminal',
    command: `curl -fsSL ${FORGE_RAW}/install/macos.sh | bash`,
  },
  {
    os: 'Linux',
    shell: 'Terminal',
    command: `curl -fsSL ${FORGE_RAW}/install/linux.sh | bash`,
  },
]

const WHY_TYPST: { icon: typeof Zap; title: string; text: string }[] = [
  {
    icon: Zap,
    title: 'Compilation instantanée',
    text: "Le PDF se met à jour en une fraction de seconde, là où LaTeX demande plusieurs secondes.",
  },
  {
    icon: PenLine,
    title: 'Syntaxe plus lisible',
    text: "Un titre s'écrit = Titre, une liste commence par un tiret. Moins de barres obliques, moins d'erreurs obscures.",
  },
  {
    icon: Eye,
    title: 'Aperçu en direct dans VS Code',
    text: "Le document s'affiche à côté du texte et change pendant la frappe. Ctrl+S ouvre l'aperçu, Ctrl+Maj+B écrit les PDF professeur et élève.",
  },
]

interface PackageEntry {
  name: string
  role: string
}

const PACKAGE_GROUPS: { title: string; subtitle: string; items: PackageEntry[] }[] = [
  {
    title: 'Cœur farfadet',
    subtitle: 'Les 15 paquets de la suite, à importer un par un ou d\'un coup avec le méta-paquet.',
    items: [
      { name: 'farfadet', role: "Méta-paquet : la porte d'entrée, il réexporte tous les autres." },
      { name: 'farfadet-socle', role: 'Version professeur ou élève, couleurs et réglages communs.' },
      { name: 'farfadet-modele', role: 'Gabarit de document, chapitres, variante dys.' },
      { name: 'farfadet-didactique', role: 'Définition, Propriété, Théorème, Exemple, Méthode, sommaire.' },
      { name: 'farfadet-enum', role: 'Énumérations tcbenumerate et colonnes.' },
      { name: 'farfadet-maths', role: 'Ensembles, intervalles, coordonnées, nombres et unités.' },
      { name: 'farfadet-exo', role: 'Exercices, corrigés différés, barème, compétences.' },
      { name: 'farfadet-crep', role: 'Zones de réponse, lignes et tableaux Seyès, cases à cocher.' },
      { name: 'farfadet-qcm', role: 'QCM et vrai/faux.' },
      { name: 'farfadet-tableaux', role: 'Tableaux tcbtab et bilans.' },
      { name: 'farfadet-tabvar', role: 'Tableaux de signes et de variations.' },
      { name: 'farfadet-geom', role: 'Figures de géométrie plane, en couche légère sur cetz.' },
      { name: 'farfadet-extras', role: 'Pellicule, code Python, habillage de figures, icônes.' },
      { name: 'farfadet-latex', role: 'Extraits LaTeX compilés dans un document Typst.' },
      { name: 'farfadet-docs', role: 'Aides de documentation (usage interne de la suite).' },
    ],
  },
  {
    title: 'Ressources collège rd*',
    subtitle: 'Neuf paquets thématiques, utilisables seuls.',
    items: [
      { name: 'rdarithm', role: 'Facteurs premiers, diviseurs, PGCD, PPCM, fractions irréductibles.' },
      { name: 'rdboites', role: "Boîtes de cours et d'activités : définitions, méthodes, encarts." },
      { name: 'rdconv', role: "Tableaux de conversion d'unités (longueur, masse, aire, volume…)." },
      { name: 'rdgrid', role: "Grilles de triangles, d'hexagones et isométriques." },
      { name: 'rdopp', role: 'Opérations posées à la française, avec retenues et corrections.' },
      { name: 'rdratio', role: 'Barres de proportion : parts colorées, accolades, légendes.' },
      { name: 'rdsheet', role: 'Captures de feuilles de calcul (style Calc ou Excel).' },
      { name: 'rdtabnum', role: "Tableaux de numération : puissances de dix, virgule, flèches." },
      { name: 'rdtime', role: 'Durées posées : heures, minutes et secondes en colonnes.' },
    ],
  },
  {
    title: 'Documentation',
    subtitle: 'Pour écrire un guide dans le même style.',
    items: [
      { name: 'bfdoc', role: 'Documentations stylées : exemples Typst et LaTeX avec rendu, fiches de fonction, de skill et d\'agent.' },
    ],
  },
]

function Code({ children }: { children: React.ReactNode }) {
  return (
    <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">{children}</code>
  )
}

export default function DownloadTypstPackagesPage() {
  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      {/* En-tête */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cosmic-900/50 border border-cosmic-700/50 text-sm text-cosmic-300 mb-6">
          <Package className="w-4 h-4" />
          Packages Typst
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">farfadet, la suite Typst pour les maths</h1>
        <p className="text-lg text-white/60 max-w-3xl mx-auto">
          <Code>farfadet</Code> réunit 25 paquets Typst pour écrire des{' '}
          <strong className="text-white/80">cours, fiches d&apos;exercices et évaluations de mathématiques</strong>,
          avec une version professeur et une version élève du même fichier. C&apos;est le successeur de{' '}
          <Code>bfcours</Code>, écrit pour Typst. Licence EUPL 1.2.
        </p>
      </div>

      {/* Pourquoi Typst */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-5xl mx-auto mb-12">
        {WHY_TYPST.map(({ icon: Icon, title, text }) => (
          <div key={title} className="glass-card rounded-xl p-5 border border-cosmic-500/20">
            <div className="w-10 h-10 rounded-lg bg-cosmic-500/20 flex items-center justify-center mb-3">
              <Icon className="w-5 h-5 text-cosmic-300" />
            </div>
            <h2 className="font-semibold text-white mb-1">{title}</h2>
            <p className="text-sm text-white/55">{text}</p>
          </div>
        ))}
      </div>

      {/* Liens Forge */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-5xl mx-auto mb-12">
        <a href={REPO_URL} target="_blank" rel="noopener noreferrer" className="group block">
          <div className="glass-card h-full rounded-xl p-5 border border-cosmic-500/30 hover:border-cosmic-400/50 transition-all duration-300 flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
              <Github className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="font-semibold text-white group-hover:text-cosmic-300 transition-colors">
                Dépôt sur la Forge
              </h2>
              <p className="text-sm text-white/55">Le code, le README et les mises à jour.</p>
            </div>
            <ExternalLink className="w-5 h-5 text-cosmic-400 flex-shrink-0" />
          </div>
        </a>

        <a href={DOC_URL} target="_blank" rel="noopener noreferrer" className="group block">
          <div className="glass-card h-full rounded-xl p-5 border border-nebula-500/30 hover:border-nebula-400/50 transition-all duration-300 flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center flex-shrink-0">
              <FileText className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="font-semibold text-white group-hover:text-nebula-300 transition-colors">
                Documentation (PDF)
              </h2>
              <p className="text-sm text-white/55">Le guide de chaque paquet, avec exemples compilés.</p>
            </div>
            <ExternalLink className="w-5 h-5 text-nebula-400 flex-shrink-0" />
          </div>
        </a>

        <a href={README_URL} target="_blank" rel="noopener noreferrer" className="group block">
          <div className="glass-card h-full rounded-xl p-5 border border-cosmic-500/30 hover:border-cosmic-400/50 transition-all duration-300 flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="font-semibold text-white group-hover:text-cosmic-300 transition-colors">
                Installation (README)
              </h2>
              <p className="text-sm text-white/55">Options, dépannage et premier document.</p>
            </div>
            <ExternalLink className="w-5 h-5 text-cosmic-400 flex-shrink-0" />
          </div>
        </a>
      </div>

      {/* Installation */}
      <div className="max-w-5xl mx-auto glass-card rounded-xl border border-white/10 p-6 mb-12">
        <div className="flex items-center gap-3 mb-2">
          <Terminal className="w-5 h-5 text-cosmic-400" />
          <h2 className="text-xl font-bold text-white">Installer en une commande</h2>
        </div>
        <p className="text-sm text-white/55 mb-5">
          Sans droits d&apos;administrateur, sans Python obligatoire, relançable sans risque. Ouvrez un terminal,
          collez la ligne de votre système, puis fermez et rouvrez VS Code. La commande prépare les paquets Typst, la
          police facultative Erewhon et, si VS Code est présent, l&apos;extension Tinymist et les réglages.
        </p>
        <div className="space-y-4">
          {INSTALL_COMMANDS.map(({ os, shell, command }) => (
            <div key={os}>
              <p className="text-sm font-medium text-cosmic-300 mb-1.5">
                {os} <span className="text-white/40 font-normal">({shell})</span>
              </p>
              <pre className="overflow-x-auto rounded-lg bg-black/40 border border-white/10 px-4 py-3 text-xs sm:text-sm text-white/80">
                <code>{command}</code>
              </pre>
            </div>
          ))}
        </div>
        <p className="text-xs text-white/45 mt-5">
          Premier essai : dans VS Code, créez <Code>cours.typ</Code>, puis Ctrl+S pour l&apos;aperçu en direct. Les
          options (sans polices, désinstallation, hors ligne) sont dans le{' '}
          <a href={README_URL} target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:text-cosmic-300 underline">
            README de la Forge
          </a>
          .
        </p>
      </div>

      {/* Application Écriture Typst */}
      <div className="max-w-5xl mx-auto glass-card rounded-xl border border-cosmic-500/30 bg-cosmic-950/20 p-6 mb-12">
        <div className="flex items-center gap-3 mb-2">
          <Sparkles className="w-5 h-5 text-cosmic-400" />
          <h2 className="text-xl font-bold text-white">Application Écriture Typst</h2>
        </div>
        <p className="text-sm text-white/60 mb-5">
          Un éditeur Typst complet, avec farfadet déjà dedans. Rien à installer : un seul fichier HTML d&apos;environ
          29 Mo, à ouvrir dans Chrome, Edge ou Firefox. Il fonctionne hors ligne, et vos documents restent sur votre
          poste.
        </p>
        <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-2 text-sm text-white/65 mb-6">
          <li><strong className="text-white/85">Aperçu en direct</strong>, en version professeur ou élève.</li>
          <li><strong className="text-white/85">Modèles</strong> : cours, fiche d&apos;exercices, évaluation, activité, fiche de révision.</li>
          <li><strong className="text-white/85">Personnalisation</strong> des environnements, de l&apos;en-tête et des titres.</li>
          <li><strong className="text-white/85">Prompt IA</strong> à coller dans l&apos;assistant de votre choix pour rédiger avec la suite.</li>
          <li><strong className="text-white/85">Formation</strong> : 13 leçons courtes, corrigées automatiquement.</li>
          <li><strong className="text-white/85">Export</strong> des fichiers .typ et des PDF professeur et élève.</li>
        </ul>

        <div className="flex flex-wrap gap-3 mb-6">
          <a
            href={APP_URL}
            download="ecriture-typst.html"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg cosmic-gradient text-sm font-medium text-white hover:opacity-90 transition-opacity"
          >
            <Download className="w-4 h-4" />
            Télécharger l&apos;application (29 Mo)
          </a>
          <a
            href={APP_PAGE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-white/70 hover:text-white transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            Page du fichier sur la Forge
          </a>
        </div>

        <div className="flex items-center gap-2 mb-3">
          <Video className="w-4 h-4 text-cosmic-400" />
          <h3 className="font-semibold text-white">Prise en main en vidéo</h3>
          <span className="text-xs text-white/40">3 min 49</span>
        </div>
        <video
          controls
          preload="metadata"
          playsInline
          className="w-full rounded-lg border border-white/10 bg-black"
        >
          <source src={VIDEO_URL} type="video/mp4" />
          Votre navigateur ne sait pas lire cette vidéo.
        </video>
        <p className="text-xs text-white/45 mt-2">
          La vidéo ne démarre pas ?{' '}
          <a href={VIDEO_URL} target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:text-cosmic-300 underline">
            Ouvrir la vidéo
          </a>{' '}
          dans un nouvel onglet.
        </p>
      </div>

      {/* Les 25 paquets */}
      <div className="max-w-5xl mx-auto mb-12">
        <h2 className="text-2xl font-bold text-white mb-1">Les 25 paquets</h2>
        <p className="text-sm text-white/55 mb-6">
          On importe le méta-paquet <Code>farfadet</Code> pour tout avoir, ou un paquet seul pour un besoin précis.
        </p>
        <div className="space-y-6">
          {PACKAGE_GROUPS.map((group) => (
            <div key={group.title} className="glass-card rounded-xl border border-cosmic-500/20 p-5">
              <h3 className="font-semibold text-cosmic-300">
                {group.title} <span className="text-white/35 font-normal text-sm">({group.items.length})</span>
              </h3>
              <p className="text-xs text-white/45 mb-3">{group.subtitle}</p>
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-1.5">
                {group.items.map((item) => (
                  <li key={item.name} className="text-sm text-white/65 flex gap-2">
                    <code className="text-cosmic-300 flex-shrink-0">{item.name}</code>
                    <span className="text-white/50">{item.role}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Avec Claude Code */}
      <div className="max-w-5xl mx-auto glass-card rounded-xl border border-nebula-500/30 p-6 mb-6">
        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <div className="flex-1">
            <h2 className="text-lg font-bold text-white mb-1">Avec Claude Code</h2>
            <p className="text-sm text-white/60">
              Le skill <Code>bfcours-typst</Code> apprend à Claude à écrire, compiler et corriger des documents
              farfadet, versions professeur et élève comprises. Sa présentation montre ce que fait l&apos;agent et
              propose un pack dédié à ajouter au panier ; il est aussi fourni dans les bundles{' '}
              <strong className="text-white/80">LaTeX Enseignant</strong> et{' '}
              <strong className="text-white/80">Power User</strong>.
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/claude-code/presentations/bfcours-typst-skill"
              prefetch={false}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-white/70 hover:text-white transition-colors"
            >
              <Package className="w-4 h-4" />
              Le skill et son pack
            </Link>
            <Link
              href="/claude-code/tutorials/typst"
              prefetch={false}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-lg cosmic-gradient text-sm font-medium text-white hover:opacity-90 transition-opacity"
            >
              Formation Typst interactive
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </div>

      {/* Note honnête */}
      <div className="max-w-5xl mx-auto glass-card p-4 rounded-xl border border-amber-500/20 bg-amber-950/10">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-white/50">
            <strong className="text-amber-300">Préversion 0.2.0.</strong> Le paquet est en cours de relecture pour
            Typst Universe, le dépôt officiel des paquets Typst. En attendant, l&apos;installateur de la Forge suffit :
            il prépare tout, y compris VS Code. L&apos;interface peut encore évoluer ; les changements sont listés dans
            le CHANGELOG du dépôt.
          </p>
        </div>
      </div>
    </div>
  )
}
