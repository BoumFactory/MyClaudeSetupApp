'use client'

import Link from "next/link"
import {
  BookOpen,
  Download,
  GraduationCap,
  Zap,
  Monitor,
  Terminal,
  Sparkles,
  MessageSquareText,
  Settings,
  Wrench,
  RotateCcw,
  CheckCircle,
  Code2,
  FileText,
  Globe,
  Image,
  Key,
  Layers,
  PenTool,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { ProgressBar } from "@/components/tutorials/ProgressBar"
import { useTutorialProgress } from "@/contexts/TutorialProgressContext"
import { PARCOURS, CAPSULES } from "@/data/parcours"
import { cn } from "@/lib/utils"

/** Mapping noms d'icônes vers composants Lucide */
const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap,
  Monitor,
  Terminal,
  Sparkles,
  MessageSquareText,
}

/** Mapping couleurs vers classes Tailwind complètes pour chaque card */
const COLOR_CLASSES: Record<string, {
  border: string
  text: string
  badgeBg: string
  gradient: string
  hoverTitle: string
  arrow: string
}> = {
  amber: {
    border: 'border-amber-500/30',
    text: 'text-amber-400',
    badgeBg: 'bg-amber-500/20',
    gradient: 'bg-gradient-to-br from-amber-500 to-orange-600',
    hoverTitle: 'group-hover:text-amber-400',
    arrow: '#f59e0b',
  },
  emerald: {
    border: 'border-emerald-500/30',
    text: 'text-emerald-400',
    badgeBg: 'bg-emerald-500/20',
    gradient: 'bg-gradient-to-br from-emerald-500 to-teal-600',
    hoverTitle: 'group-hover:text-emerald-400',
    arrow: '#10b981',
  },
  cosmic: {
    border: 'border-cosmic-500/30',
    text: 'text-cosmic-400',
    badgeBg: 'bg-cosmic-500/20',
    gradient: 'cosmic-gradient',
    hoverTitle: 'group-hover:text-cosmic-400',
    arrow: '#818cf8',
  },
  nebula: {
    border: 'border-nebula-500/30',
    text: 'text-nebula-400',
    badgeBg: 'bg-nebula-500/20',
    gradient: 'nebula-gradient',
    hoverTitle: 'group-hover:text-nebula-400',
    arrow: '#c084fc',
  },
  violet: {
    border: 'border-violet-500/30',
    text: 'text-violet-400',
    badgeBg: 'bg-violet-500/20',
    gradient: 'bg-gradient-to-br from-violet-500 to-purple-600',
    hoverTitle: 'group-hover:text-violet-400',
    arrow: '#8b5cf6',
  },
}

const DEFAULT_COLORS = {
  border: 'border-blue-500/30',
  text: 'text-blue-400',
  badgeBg: 'bg-blue-500/20',
  gradient: 'cosmic-gradient',
  hoverTitle: 'group-hover:text-blue-400',
  arrow: '#60a5fa',
}

/** Guides d'installation enrichis */
const INSTALL_GUIDES = [
  {
    category: 'Prérequis logiciels',
    icon: Download,
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    borderColor: 'border-emerald-500/20',
    guides: [
      { title: 'Python', href: '/claude-code/tutorials/python-install', icon: Code2, color: 'text-yellow-400', description: 'Langage requis pour les scripts et skills avancés' },
      { title: 'Node.js', href: '/claude-code/tutorials/nodejs-install', icon: Globe, color: 'text-green-400', description: 'Environnement JavaScript pour Claude Code et les outils web' },
      { title: 'VS Code + MiKTeX', href: '/claude-code/tutorials/vscode-miktex', icon: FileText, color: 'text-sky-400', description: 'Éditeur de code et compilateur LaTeX pour les documents' },
    ],
  },
  {
    category: 'Installation des IA',
    icon: Sparkles,
    color: 'text-cosmic-400',
    bg: 'bg-cosmic-500/10',
    borderColor: 'border-cosmic-500/20',
    guides: [
      { title: 'Claude Desktop', href: '/claude-code/tutorials/claude-desktop-install', icon: Monitor, color: 'text-emerald-400', description: 'Application graphique — idéal pour débuter sans terminal' },
      { title: 'Claude Code CLI', href: '/claude-code/tutorials/claude-code-install', icon: Terminal, color: 'text-cosmic-400', description: 'Interface ligne de commande — puissance maximale' },
      { title: 'Configuration initiale', href: '/claude-code/tutorials/claude-code-config', icon: Settings, color: 'text-amber-400', description: 'Permissions, modèle, et premiers réglages' },
    ],
  },
  {
    category: 'Configuration avancée',
    icon: Wrench,
    color: 'text-nebula-400',
    bg: 'bg-nebula-500/10',
    borderColor: 'border-nebula-500/20',
    guides: [
      { title: 'Utilisation et config', href: '/claude-code/tutorials/utilisation-config', icon: Layers, color: 'text-violet-400', description: 'Commandes, skills, agents et fichiers de configuration' },
      { title: 'Setup BFCours', href: '/claude-code/tutorials/bfcours-setup', icon: PenTool, color: 'text-rose-400', description: 'Installer le package LaTeX pédagogique complet' },
      { title: 'API Google (Imagen)', href: '/claude-code/tutorials/google-api-setup', icon: Key, color: 'text-amber-400', description: 'Clé API pour la génération d\'images IA' },
    ],
  },
]

/** Référentiel de compétences IA pour l'enseignant de maths */
const COMPETENCES = [
  {
    domaine: 'Structurer sa communication',
    icon: '🧱',
    color: 'text-amber-400',
    bg: 'bg-amber-500/10',
    items: [
      { label: 'Organiser un prompt en sections (Rôle, Contexte, Tâche, Format)', parcours: 'prompt-craft', capsule: 'pc-structure' },
      { label: 'Utiliser la hiérarchie Markdown (#, ##, ###)', parcours: 'prompt-craft', capsule: 'pc-structure' },
      { label: 'Spécifier le format de sortie attendu (fichier, structure)', parcours: 'prompt-craft', capsule: 'pc-structure' },
      { label: 'Varier les rôles pour changer le prisme de lecture', parcours: 'prompt-craft', capsule: 'pc-structure' },
    ],
  },
  {
    domaine: 'S\'appuyer sur ses sources',
    icon: '📄',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    items: [
      { label: 'Fournir ses fichiers pour limiter les hallucinations', parcours: 'prompt-craft', capsule: 'pc-sources' },
      { label: 'Distinguer transformation (sûr) et création (risqué)', parcours: 'prompt-craft', capsule: 'pc-sources' },
      { label: 'Produire des dérivés d\'un document source (blueprint, slides, variantes)', parcours: 'prompt-craft', capsule: 'pc-sources' },
    ],
  },
  {
    domaine: 'Choisir le bon modèle',
    icon: '⚡',
    color: 'text-green-400',
    bg: 'bg-green-500/10',
    items: [
      { label: 'Connaître les niveaux de modèle (Haiku, Sonnet, Opus)', parcours: 'prompt-craft', capsule: 'pc-models' },
      { label: 'Adapter la puissance à la complexité de la tâche', parcours: 'prompt-craft', capsule: 'pc-models' },
      { label: 'Optimiser le coût en tokens par choix de modèle', parcours: 'prompt-craft', capsule: 'pc-models' },
      { label: 'Identifier les cas de sur-traitement', parcours: 'prompt-craft', capsule: 'pc-models' },
    ],
  },
  {
    domaine: 'Mobiliser les bons outils',
    icon: '🎯',
    color: 'text-violet-400',
    bg: 'bg-violet-500/10',
    items: [
      { label: 'Invoquer un skill par commande slash ou mention', parcours: 'prompt-craft', capsule: 'pc-skills-agents' },
      { label: 'Cibler des fichiers avec @ pour guider l\'agent', parcours: 'prompt-craft', capsule: 'pc-skills-agents' },
      { label: 'Construire un workflow multi-étapes avec ##', parcours: 'prompt-craft', capsule: 'pc-skills-agents' },
      { label: 'Choisir entre déclenchement explicite et implicite', parcours: 'prompt-craft', capsule: 'pc-skills-agents' },
    ],
  },
  {
    domaine: 'Planifier avant de produire',
    icon: '🤝',
    color: 'text-cyan-400',
    bg: 'bg-cyan-500/10',
    items: [
      { label: 'Demander un pré-plan avant toute production complexe', parcours: 'prompt-craft', capsule: 'pc-preplan' },
      { label: 'Annoter et itérer sur un pré-plan', parcours: 'prompt-craft', capsule: 'pc-preplan' },
      { label: 'Distinguer vibe coding et prompt engineering', parcours: 'prompt-craft', capsule: 'pc-preplan' },
      { label: 'Évaluer quand un pré-plan est nécessaire ou non', parcours: 'prompt-craft', capsule: 'pc-preplan' },
    ],
  },
  {
    domaine: 'Clarifier sa demande',
    icon: '💡',
    color: 'text-orange-400',
    bg: 'bg-orange-500/10',
    items: [
      { label: 'Identifier les dimensions manquantes d\'une demande', parcours: 'prompt-craft', capsule: 'pc-idea-challenger' },
      { label: 'Se faire challenger par l\'IA pour préciser sa pensée', parcours: 'prompt-craft', capsule: 'pc-idea-challenger' },
      { label: 'Obtenir un prompt .md structuré à partir d\'une idée vague', parcours: 'prompt-craft', capsule: 'pc-idea-challenger' },
    ],
  },
  {
    domaine: 'Faire critiquer pour améliorer',
    icon: '🔍',
    color: 'text-rose-400',
    bg: 'bg-rose-500/10',
    items: [
      { label: 'Demander une adversarial review avec des rôles ciblés', parcours: 'prompt-craft', capsule: 'pc-adversarial' },
      { label: 'Choisir les bons reviewers selon la tâche', parcours: 'prompt-craft', capsule: 'pc-adversarial' },
      { label: 'Comprendre le workflow plan → critique → arbitrage', parcours: 'prompt-craft', capsule: 'pc-adversarial' },
    ],
  },
  {
    domaine: 'Combiner les briques',
    icon: '🧩',
    color: 'text-indigo-400',
    bg: 'bg-indigo-500/10',
    items: [
      { label: 'Doser la complexité selon la tâche (pas tout utiliser à chaque fois)', parcours: 'prompt-craft', capsule: 'pc-synthesis' },
      { label: 'Combiner structure + skills + pré-plan + review dans un seul prompt', parcours: 'prompt-craft', capsule: 'pc-synthesis' },
      { label: 'Construire un workflow multi-étapes avec montée en puissance progressive', parcours: 'prompt-craft', capsule: 'pc-synthesis' },
    ],
  },
  {
    domaine: 'Installer et configurer',
    icon: '⚙️',
    color: 'text-emerald-400',
    bg: 'bg-emerald-500/10',
    items: [
      { label: 'Installer Claude Desktop ou Claude Code', parcours: 'claude-desktop', capsule: 'cd-install' },
      { label: 'Configurer les permissions et le modèle', parcours: 'claude-code', capsule: 'cc-config' },
      { label: 'Comprendre l\'architecture agents + skills', parcours: 'quick-view', capsule: 'qv-overview' },
    ],
  },
  {
    domaine: 'Maîtriser l\'architecture',
    icon: '🏗️',
    color: 'text-nebula-400',
    bg: 'bg-nebula-500/10',
    items: [
      { label: 'Configurer le CLAUDE.md et les hooks', parcours: 'avance', capsule: 'av-hooks' },
      { label: 'Créer ses propres skills', parcours: 'avance', capsule: 'av-skill-creator' },
      { label: 'Partager sa configuration entre collègues', parcours: 'avance', capsule: 'av-share' },
      { label: 'Orchestrer des sous-agents spécialisés en parallèle', parcours: 'avance', capsule: 'av-subagents' },
      { label: 'Organiser une équipe d\'agents persistante (TeamPlay)', parcours: 'avance', capsule: 'av-teamplay' },
    ],
  },
]

function ParcoursCard({ parcours }: { parcours: typeof PARCOURS[0] }) {
  const Icon = ICON_MAP[parcours.icon]
  const colors = COLOR_CLASSES[parcours.color] ?? DEFAULT_COLORS
  return (
    <Link
      href={`/claude-code/tutorials/parcours/${parcours.id}`}
      className="block"
    >
      <Card className={`glass-card hover:scale-[1.03] transition-all duration-300 group cursor-pointer h-full border-2 ${colors.border}`}>
        <CardHeader>
          <div className="flex items-start justify-between mb-3">
            <div className={`w-12 h-12 rounded-lg ${colors.gradient} flex items-center justify-center`}>
              {Icon && <Icon className="w-6 h-6 text-white" />}
            </div>
            <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-full ${colors.badgeBg} ${colors.text} text-xs font-medium`}>
              {parcours.capsules.length} capsule{parcours.capsules.length > 1 ? 's' : ''}
            </span>
          </div>
          <CardTitle className={`${colors.hoverTitle} transition-colors`}>
            {parcours.title}
          </CardTitle>
          <CardDescription>
            {parcours.description}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ProgressBar parcoursId={parcours.id} showLabel={true} />
          <div className={`${colors.text} font-semibold group-hover:underline`}>
            Commencer le parcours &rarr;
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}

/** Flèche SVG animée entre les étapes */
function FlowArrow({ label, fromColor = '#8b5cf6', toColor = '#8b5cf6' }: { label: string; fromColor?: string; toColor?: string }) {
  return (
    <div className="flex flex-col items-center py-2 relative">
      <svg width="40" height="64" viewBox="0 0 40 64" fill="none" className="drop-shadow-lg">
        <defs>
          <linearGradient id={`arrow-${label.replace(/\s/g, '')}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor={fromColor} stopOpacity="0.6" />
            <stop offset="100%" stopColor={toColor} stopOpacity="0.8" />
          </linearGradient>
        </defs>
        {/* Ligne */}
        <rect x="18" y="0" width="4" height="44" rx="2" fill={`url(#arrow-${label.replace(/\s/g, '')})`} />
        {/* Pointe */}
        <path d="M20 64L8 44h24L20 64z" fill={toColor} fillOpacity="0.7" />
        {/* Cercle lumineux */}
        <circle cx="20" cy="4" r="4" fill={fromColor} fillOpacity="0.4">
          <animate attributeName="fillOpacity" values="0.4;0.8;0.4" dur="2s" repeatCount="indefinite" />
        </circle>
      </svg>
      <span className="absolute top-1/2 -translate-y-1/2 left-full ml-3 text-xs text-muted-foreground whitespace-nowrap bg-background/90 backdrop-blur-sm px-2.5 py-1 rounded-md border border-white/10">
        {label}
      </span>
    </div>
  )
}

/** Connecteur Y (split vers 2 branches) */
function FlowSplit() {
  return (
    <div className="flex justify-center py-2">
      <svg width="300" height="48" viewBox="0 0 300 48" fill="none" className="drop-shadow-lg">
        <defs>
          <linearGradient id="split-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#f59e0b" stopOpacity="0.5" />
            <stop offset="100%" stopColor="#10b981" stopOpacity="0.5" />
          </linearGradient>
        </defs>
        {/* Ligne verticale du tronc */}
        <rect x="148" y="0" width="4" height="16" rx="2" fill="url(#split-grad)" />
        {/* Branche gauche */}
        <path d="M150 16 Q150 32 75 40" stroke="#10b981" strokeWidth="3" strokeOpacity="0.5" fill="none" strokeLinecap="round" />
        {/* Branche droite */}
        <path d="M150 16 Q150 32 225 40" stroke="#818cf8" strokeWidth="3" strokeOpacity="0.5" fill="none" strokeLinecap="round" />
        {/* Pointe gauche */}
        <polygon points="75,34 69,44 81,44" fill="#10b981" fillOpacity="0.6" />
        {/* Pointe droite */}
        <polygon points="225,34 219,44 231,44" fill="#818cf8" fillOpacity="0.6" />
      </svg>
    </div>
  )
}

/** Connecteur merge (2 branches vers 1) */
function FlowMerge() {
  return (
    <div className="flex justify-center py-2">
      <svg width="300" height="48" viewBox="0 0 300 48" fill="none" className="drop-shadow-lg">
        <defs>
          <linearGradient id="merge-grad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
            <stop offset="100%" stopColor="#8b5cf6" stopOpacity="0.6" />
          </linearGradient>
        </defs>
        {/* Branche gauche */}
        <path d="M75 8 Q75 24 150 32" stroke="#10b981" strokeWidth="3" strokeOpacity="0.5" fill="none" strokeLinecap="round" />
        {/* Branche droite */}
        <path d="M225 8 Q225 24 150 32" stroke="#818cf8" strokeWidth="3" strokeOpacity="0.5" fill="none" strokeLinecap="round" />
        {/* Ligne verticale du tronc */}
        <rect x="148" y="32" width="4" height="8" rx="2" fill="url(#merge-grad)" />
        {/* Pointe */}
        <polygon points="150,48 142,40 158,40" fill="#8b5cf6" fillOpacity="0.6" />
      </svg>
    </div>
  )
}

export default function TutorialsPage() {
  const { resetProgress, isCompleted } = useTutorialProgress()

  const quickView = PARCOURS.find(p => p.id === 'quick-view')
  const desktop = PARCOURS.find(p => p.id === 'claude-desktop')
  const cli = PARCOURS.find(p => p.id === 'claude-code')
  const promptCraft = PARCOURS.find(p => p.id === 'prompt-craft')
  const avance = PARCOURS.find(p => p.id === 'avance')

  return (
    <div className="space-y-16">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <GraduationCap className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Tutoriels
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Choisissez votre parcours de formation et progressez à votre rythme.
          Chaque parcours est composé de capsules interactives avec suivi de progression.
        </p>
      </section>

      {/* ===== PARCOURS EN FLUX ===== */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">
          Parcours de formation
        </h2>

        <div className="max-w-5xl mx-auto">
          {/* 1. Quick View */}
          {quickView && (
            <div className="max-w-lg mx-auto">
              <ParcoursCard parcours={quickView} />
            </div>
          )}

          {/* Flèche split */}
          <FlowSplit />

          {/* 2. Desktop OU CLI */}
          <div className="relative">
            <div className="absolute -top-1 left-1/2 -translate-x-1/2 z-10">
              <span className="text-xs font-medium text-muted-foreground bg-background/90 backdrop-blur-sm px-3 py-1 rounded-full border border-dashed border-white/20">
                Choisissez votre interface
              </span>
            </div>
            <div className="grid md:grid-cols-2 gap-6 pt-4 px-2 pb-2 rounded-xl border border-dashed border-white/10 bg-white/[0.015]">
              {desktop && <ParcoursCard parcours={desktop} />}
              {cli && <ParcoursCard parcours={cli} />}
              <div className="md:col-span-2 text-center text-xs text-muted-foreground -mt-2 pb-1">
                Interface graphique ou ligne de commande — les deux mènent au même résultat
              </div>
            </div>
          </div>

          {/* Flèche merge */}
          <FlowMerge />

          {/* 3. Parler à une IA */}
          {promptCraft && (
            <div className="max-w-lg mx-auto">
              <ParcoursCard parcours={promptCraft} />
            </div>
          )}

          {/* Flèche simple */}
          <FlowArrow label="Allez plus loin" fromColor="#8b5cf6" toColor="#c084fc" />

          {/* 4. Avancé */}
          {avance && (
            <div className="max-w-lg mx-auto">
              <ParcoursCard parcours={avance} />
            </div>
          )}
        </div>

        {/* Lien parcours libre */}
        <p className="text-center text-sm text-muted-foreground pt-4">
          Ou{' '}
          <Link
            href="/claude-code/tutorials/parcours"
            className="underline hover:text-white transition-colors"
          >
            explorez librement toutes les capsules
          </Link>
        </p>
      </section>

      {/* ===== RÉFÉRENTIEL DE COMPÉTENCES ===== */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold">
            Référentiel de compétences IA
          </h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Les compétences travaillées dans les parcours, organisées par domaine.
            Un référentiel pour l&apos;enseignant de mathématiques qui utilise l&apos;IA.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4 max-w-5xl mx-auto">
          {COMPETENCES.map((domaine) => (
            <div
              key={domaine.domaine}
              className={cn(
                'glass-card rounded-xl p-5 border space-y-3',
                domaine.bg,
                'border-white/10',
              )}
            >
              <div className="flex items-center gap-2.5">
                <span className="text-xl">{domaine.icon}</span>
                <h3 className={cn('font-bold text-sm', domaine.color)}>{domaine.domaine}</h3>
              </div>
              <ul className="space-y-2">
                {domaine.items.map((item, i) => {
                  const done = isCompleted(item.capsule)
                  return (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      {done ? (
                        <CheckCircle className="w-4 h-4 mt-0.5 text-green-400 shrink-0" />
                      ) : (
                        <div className="w-4 h-4 mt-0.5 rounded-full border border-white/20 shrink-0" />
                      )}
                      <Link
                        href={`/claude-code/tutorials/parcours/${item.parcours}/${item.capsule}`}
                        className={cn(
                          'hover:underline transition-colors',
                          done ? 'text-gray-400' : 'text-gray-300 hover:text-white',
                        )}
                      >
                        {item.label}
                      </Link>
                    </li>
                  )
                })}
              </ul>
            </div>
          ))}
        </div>
      </section>

      {/* ===== GUIDES D'INSTALLATION ===== */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold">
            Guides d&apos;installation
          </h2>
          <p className="text-muted-foreground">
            Tutoriels pas-à-pas pour installer et configurer les outils nécessaires
          </p>
        </div>

        <div className="max-w-5xl mx-auto space-y-6">
          {INSTALL_GUIDES.map((group) => {
            const GroupIcon = group.icon
            return (
              <div key={group.category} className={cn('rounded-xl border p-5 space-y-4', group.borderColor, group.bg)}>
                <div className="flex items-center gap-2.5">
                  <GroupIcon className={cn('w-5 h-5', group.color)} />
                  <h3 className={cn('font-bold text-sm uppercase tracking-wider', group.color)}>
                    {group.category}
                  </h3>
                </div>
                <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
                  {group.guides.map((guide) => {
                    const GuideIcon = guide.icon
                    return (
                      <Link key={guide.href} href={guide.href}>
                        <div className="glass-card rounded-lg p-4 flex items-start gap-3 hover:bg-white/10 transition-all duration-200 group cursor-pointer border border-white/10 hover:border-white/25 h-full">
                          <div className={cn(
                            'w-10 h-10 rounded-lg flex items-center justify-center shrink-0 transition-colors',
                            'bg-white/5 group-hover:bg-white/10',
                          )}>
                            <GuideIcon className={cn('w-5 h-5 transition-colors', guide.color)} />
                          </div>
                          <div className="min-w-0">
                            <div className="text-sm font-semibold text-gray-200 group-hover:text-white transition-colors">
                              {guide.title}
                            </div>
                            <div className="text-xs text-muted-foreground mt-0.5 line-clamp-2">
                              {guide.description}
                            </div>
                          </div>
                        </div>
                      </Link>
                    )
                  })}
                </div>
              </div>
            )
          })}
        </div>
      </section>

      {/* Pourquoi ces tutoriels */}
      <section className="glass-card rounded-xl p-8 space-y-4 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold">Pourquoi ces tutoriels ?</h2>
        <div className="space-y-3 text-muted-foreground">
          <p>
            Ces tutoriels ont été créés pour vous accompagner dans la découverte
            et la maîtrise des agents IA au service de l&apos;enseignement des mathématiques.
          </p>
          <p>
            En suivant les parcours proposés, vous apprendrez à :
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Installer et configurer Claude Desktop ou Claude Code CLI</li>
            <li>Structurer vos demandes pour des résultats précis</li>
            <li>Invoquer les bons skills et agents au bon moment</li>
            <li>Planifier avec des pré-plans avant de produire</li>
            <li>Faire critiquer vos productions par des agents spécialisés</li>
            <li>Maîtriser l&apos;architecture agentique (agents, skills, hooks)</li>
          </ul>
        </div>
      </section>

      {/* Besoin d'aide */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-l-4 border-cosmic-400 max-w-5xl mx-auto">
        <h2 className="text-2xl font-bold">Besoin d&apos;aide ?</h2>
        <p className="text-muted-foreground">
          Si vous rencontrez des difficultés lors de l&apos;installation ou de la configuration,
          n&apos;hésitez pas à consulter les ressources supplémentaires disponibles dans la
          section téléchargements ou à explorer les présentations pour mieux comprendre
          les concepts.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link href="/claude-code/downloads" prefetch={false}>
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cosmic-500/20 text-cosmic-400 hover:bg-cosmic-500/30 transition-colors text-sm font-medium cursor-pointer">
              <Download className="w-4 h-4" />
              Téléchargements
            </span>
          </Link>
          <Link href="/claude-code/presentations" prefetch={false}>
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-nebula-500/20 text-nebula-400 hover:bg-nebula-500/30 transition-colors text-sm font-medium cursor-pointer">
              <BookOpen className="w-4 h-4" />
              Présentations
            </span>
          </Link>
        </div>
      </section>

      {/* Bouton reset progression */}
      <div className="flex justify-center">
        <Button
          variant="ghost"
          size="sm"
          onClick={resetProgress}
          className="text-gray-500 hover:text-gray-300 hover:bg-white/5 text-xs"
        >
          <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
          Réinitialiser la progression
        </Button>
      </div>
    </div>
  )
}
