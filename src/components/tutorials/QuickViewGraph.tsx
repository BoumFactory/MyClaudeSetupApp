'use client'

import { useState } from 'react'
import {
  Cpu,
  Wrench,
  FileText,
  BookOpen,
  Code2,
  FileOutput,
  ChevronRight,
  Sparkles,
  Lightbulb,
  ChevronDown,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'

/** Description d'un noeud du graphe */
interface GraphNode {
  id: string
  label: string
  description: string
  icon: React.ElementType
  colorClass: string
  borderClass: string
  bgClass: string
  glowClass: string
}

/** Les noeuds principaux du systeme agentique */
const NODES: GraphNode[] = [
  {
    id: 'agent',
    label: 'Agent IA',
    description:
      'Le cerveau qui planifie et decide. Il analyse votre demande, choisit les bons outils et orchestre le travail.',
    icon: Cpu,
    colorClass: 'text-cosmic-400',
    borderClass: 'border-cosmic-500/50',
    bgClass: 'bg-cosmic-500/20',
    glowClass: 'shadow-cosmic-500/30',
  },
  {
    id: 'skills',
    label: 'Skills',
    description:
      'Savoir-faire spécialisés : création LaTeX, génération d\'images, présentations... Chaque skill est un expert dans son domaine.',
    icon: Wrench,
    colorClass: 'text-nebula-400',
    borderClass: 'border-nebula-500/50',
    bgClass: 'bg-nebula-500/20',
    glowClass: 'shadow-nebula-500/30',
  },
  {
    id: 'instructions',
    label: 'Instructions',
    description:
      'CLAUDE.md, GEMINI.md... Ces fichiers définissent le comportement de l\'agent : ses règles, son style, ses préférences.',
    icon: FileText,
    colorClass: 'text-amber-400',
    borderClass: 'border-amber-500/50',
    bgClass: 'bg-amber-500/20',
    glowClass: 'shadow-amber-500/30',
  },
  {
    id: 'references',
    label: 'Références',
    description:
      'Documentation et exemples à disposition de l\'agent. Il peut s\'en inspirer pour produire un travail de qualité.',
    icon: BookOpen,
    colorClass: 'text-blue-400',
    borderClass: 'border-blue-500/50',
    bgClass: 'bg-blue-500/20',
    glowClass: 'shadow-blue-500/30',
  },
  {
    id: 'scripts',
    label: 'Scripts',
    description:
      'Programmes déterministes qui éliminent l\'aléatoire. Compilation LaTeX, traitement d\'images... Le résultat est reproductible à 100%.',
    icon: Code2,
    colorClass: 'text-emerald-400',
    borderClass: 'border-emerald-500/50',
    bgClass: 'bg-emerald-500/20',
    glowClass: 'shadow-emerald-500/30',
  },
  {
    id: 'result',
    label: 'Résultat',
    description:
      'Documents créés directement sur votre machine : PDF, images, présentations, code source...',
    icon: FileOutput,
    colorClass: 'text-green-400',
    borderClass: 'border-green-500/50',
    bgClass: 'bg-green-500/20',
    glowClass: 'shadow-green-500/30',
  },
]

/** Etapes du workflow LaTeX */
interface WorkflowStep {
  step: number
  skill: string
  description: string
  colorClass: string
  bgClass: string
  reflexion: string
  outils: string[]
  workflowInterne: string
}

const WORKFLOW_STEPS: WorkflowStep[] = [
  {
    step: 1,
    skill: 'tex-document-creator',
    description: 'Choisit le bon template LaTeX selon le type de document demandé (cours, exercice, évaluation...)',
    colorClass: 'text-nebula-400',
    bgClass: 'bg-nebula-500/10',
    reflexion: 'L\'agent analyse la demande (cours ? exercice ? évaluation ?) et choisit le template LaTeX adapté.',
    outils: ['Read', 'Glob', 'Write'],
    workflowInterne: 'Lire les templates disponibles → Matcher le type de document → Créer la structure de fichiers → Remplir les métadonnées',
  },
  {
    step: 2,
    skill: 'bfcours-latex',
    description: 'Écrit le contenu mathématique en LaTeX en respectant les conventions et la mise en page du template',
    colorClass: 'text-cosmic-400',
    bgClass: 'bg-cosmic-500/10',
    reflexion: 'L\'agent écrit le contenu mathématique structuré en LaTeX avec le package bfcours.',
    outils: ['Read', 'Write', 'Grep'],
    workflowInterne: 'Consulter les références du package → Écrire le contenu pédagogique → Structurer en sections → Vérifier la syntaxe LaTeX',
  },
  {
    step: 3,
    skill: 'tex-compiling-skill',
    description: 'Compile le fichier .tex en PDF de manière déterministe. Pas d\'aléatoire : même source = même PDF',
    colorClass: 'text-emerald-400',
    bgClass: 'bg-emerald-500/10',
    reflexion: 'L\'agent lance la compilation déterministe du fichier .tex en PDF.',
    outils: ['Bash', 'Read'],
    workflowInterne: 'Exécuter pdflatex → Analyser le log → Si erreur : diagnostiquer et corriger → Relancer → Confirmer le PDF',
  },
]

/**
 * Composant d'un noeud dans le graphe
 */
function GraphNodeCard({
  node,
  isSelected,
  onSelect,
}: {
  node: GraphNode
  isSelected: boolean
  onSelect: () => void
}) {
  const Icon = node.icon

  return (
    <button
      type="button"
      onClick={onSelect}
      className={cn(
        'glass-card rounded-xl p-4 transition-all duration-300 cursor-pointer text-left w-full',
        'border',
        node.borderClass,
        isSelected && [node.bgClass, 'shadow-lg', node.glowClass],
        !isSelected && 'hover:scale-[1.02]'
      )}
    >
      <div className="flex items-center gap-3">
        <div
          className={cn(
            'w-10 h-10 rounded-lg flex items-center justify-center shrink-0',
            node.bgClass
          )}
        >
          <Icon className={cn('w-5 h-5', node.colorClass)} />
        </div>
        <div className="min-w-0">
          <h4 className={cn('font-semibold text-sm', node.colorClass)}>
            {node.label}
          </h4>
        </div>
      </div>

      {/* Détail affiché quand sélectionné */}
      <div
        className={cn(
          'overflow-hidden transition-all duration-300',
          isSelected ? 'max-h-40 opacity-100 mt-3' : 'max-h-0 opacity-0'
        )}
      >
        <p className="text-sm text-white/90 leading-relaxed">
          {node.description}
        </p>
      </div>
    </button>
  )
}

/**
 * Badge pour un outil
 */
function ToolBadge({ tool }: { tool: string }) {
  const colorMap: Record<string, string> = {
    Read: 'bg-blue-500/20 text-blue-300 border-blue-500/30',
    Write: 'bg-green-500/20 text-green-300 border-green-500/30',
    Bash: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
    Glob: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
    Grep: 'bg-rose-500/20 text-rose-300 border-rose-500/30',
  }

  return (
    <span className={cn(
      'inline-block rounded-full px-2 py-0.5 text-xs font-medium border',
      colorMap[tool] || 'bg-gray-500/20 text-gray-300 border-gray-500/30'
    )}>
      {tool}
    </span>
  )
}

/**
 * Panneau de détails dépliable pour une étape du workflow
 */
function WorkflowStepDetails({
  isOpen,
  reflexion,
  outils,
  workflowInterne,
}: {
  isOpen: boolean
  reflexion: string
  outils: string[]
  workflowInterne: string
}) {
  return (
    <div
      className={cn(
        'overflow-hidden transition-all duration-300',
        isOpen ? 'max-h-96 opacity-100 mt-3' : 'max-h-0 opacity-0'
      )}
    >
      <div className="space-y-3 text-sm">
        {/* Réflexion */}
        <div className="flex gap-2">
          <Lightbulb className="w-4 h-4 text-yellow-400 shrink-0 mt-0.5" />
          <p className="text-white/80 italic">
            {reflexion}
          </p>
        </div>

        {/* Outils utilisés */}
        <div className="flex flex-wrap gap-2">
          {outils.map((tool) => (
            <ToolBadge key={tool} tool={tool} />
          ))}
        </div>

        {/* Workflow interne */}
        <div className="text-white/70 leading-relaxed">
          {workflowInterne}
        </div>
      </div>
    </div>
  )
}

/**
 * Ligne de connexion animée entre les nœuds (pulsation CSS)
 */
function ConnectionLine({ direction = 'horizontal' }: { direction?: 'horizontal' | 'vertical' }) {
  return (
    <div
      className={cn(
        'flex items-center justify-center',
        direction === 'horizontal' ? 'px-1' : 'py-1'
      )}
    >
      <div
        className={cn(
          'rounded-full animate-pulse-line',
          direction === 'horizontal'
            ? 'w-6 h-0.5 bg-gradient-to-r from-cosmic-500 to-nebula-500'
            : 'h-6 w-0.5 bg-gradient-to-b from-nebula-500 to-emerald-500'
        )}
      />
      <ChevronRight
        className={cn(
          'w-3 h-3 text-cosmic-400',
          direction === 'vertical' && 'rotate-90'
        )}
      />
    </div>
  )
}

/**
 * Graphe interactif montrant l'architecture d'un système d'agents IA
 *
 * Structure :
 * [Agent IA] --> [Skills] --> [Instructions]
 *                  |          [Références]
 *                  |          [Scripts]
 *                  v
 *              [Résultat]
 */
export function QuickViewGraph() {
  const [selectedNode, setSelectedNode] = useState<string | null>(null)
  const [showWorkflow, setShowWorkflow] = useState(false)
  const [activeStep, setActiveStep] = useState<number>(0)
  const [expandedStep, setExpandedStep] = useState<number | null>(null)

  const handleNodeSelect = (nodeId: string) => {
    setSelectedNode((prev) => (prev === nodeId ? null : nodeId))
  }

  const handleStepToggle = (step: number) => {
    setExpandedStep((prev) => (prev === step ? null : step))
  }

  const handleShowWorkflow = () => {
    setShowWorkflow(true)
    setActiveStep(0)
    // Animation séquentielle des étapes
    const timers = WORKFLOW_STEPS.map((_, i) =>
      setTimeout(() => setActiveStep(i + 1), (i + 1) * 800)
    )
    return () => timers.forEach(clearTimeout)
  }

  const getNode = (id: string) => NODES.find((n) => n.id === id)!

  return (
    <div className="space-y-8">
      {/* Titre du graphe */}
      <div className="text-center space-y-2">
        <h3 className="text-lg font-bold text-white flex items-center justify-center gap-2">
          <Sparkles className="w-5 h-5 text-amber-400" />
          Architecture d&apos;un système agentique
        </h3>
        <p className="text-sm text-gray-400">
          Cliquez sur les nœuds pour découvrir chaque composant
        </p>
      </div>

      {/* ====== GRAPHE PRINCIPAL ====== */}

      {/* Version desktop : disposition en grille */}
      <div className="hidden md:block">
        <div className="flex items-start justify-center gap-2">
          {/* Colonne 1 : Agent */}
          <div className="w-44 pt-12">
            <GraphNodeCard
              node={getNode('agent')}
              isSelected={selectedNode === 'agent'}
              onSelect={() => handleNodeSelect('agent')}
            />
          </div>

          {/* Connexion Agent -> Skills */}
          <div className="pt-16">
            <ConnectionLine direction="horizontal" />
          </div>

          {/* Colonne 2 : Skills */}
          <div className="w-44 pt-12">
            <GraphNodeCard
              node={getNode('skills')}
              isSelected={selectedNode === 'skills'}
              onSelect={() => handleNodeSelect('skills')}
            />
            {/* Connexion Skills -> Resultat */}
            <div className="flex justify-center">
              <ConnectionLine direction="vertical" />
            </div>
            <GraphNodeCard
              node={getNode('result')}
              isSelected={selectedNode === 'result'}
              onSelect={() => handleNodeSelect('result')}
            />
          </div>

          {/* Connexion Skills -> sous-composants */}
          <div className="pt-16">
            <ConnectionLine direction="horizontal" />
          </div>

          {/* Colonne 3 : Instructions, References, Scripts */}
          <div className="w-44 space-y-2">
            <GraphNodeCard
              node={getNode('instructions')}
              isSelected={selectedNode === 'instructions'}
              onSelect={() => handleNodeSelect('instructions')}
            />
            <GraphNodeCard
              node={getNode('references')}
              isSelected={selectedNode === 'references'}
              onSelect={() => handleNodeSelect('references')}
            />
            <GraphNodeCard
              node={getNode('scripts')}
              isSelected={selectedNode === 'scripts'}
              onSelect={() => handleNodeSelect('scripts')}
            />
          </div>
        </div>
      </div>

      {/* Version mobile : disposition en colonne */}
      <div className="md:hidden space-y-2">
        <GraphNodeCard
          node={getNode('agent')}
          isSelected={selectedNode === 'agent'}
          onSelect={() => handleNodeSelect('agent')}
        />
        <div className="flex justify-center">
          <ConnectionLine direction="vertical" />
        </div>
        <GraphNodeCard
          node={getNode('skills')}
          isSelected={selectedNode === 'skills'}
          onSelect={() => handleNodeSelect('skills')}
        />
        <div className="flex justify-center">
          <ConnectionLine direction="vertical" />
        </div>

        {/* Sous-composants en grille 2 colonnes sur mobile */}
        <div className="grid grid-cols-2 gap-2">
          <GraphNodeCard
            node={getNode('instructions')}
            isSelected={selectedNode === 'instructions'}
            onSelect={() => handleNodeSelect('instructions')}
          />
          <GraphNodeCard
            node={getNode('references')}
            isSelected={selectedNode === 'references'}
            onSelect={() => handleNodeSelect('references')}
          />
        </div>
        <div className="w-1/2 mx-auto">
          <GraphNodeCard
            node={getNode('scripts')}
            isSelected={selectedNode === 'scripts'}
            onSelect={() => handleNodeSelect('scripts')}
          />
        </div>

        <div className="flex justify-center">
          <ConnectionLine direction="vertical" />
        </div>
        <GraphNodeCard
          node={getNode('result')}
          isSelected={selectedNode === 'result'}
          onSelect={() => handleNodeSelect('result')}
        />
      </div>

      {/* ====== MESSAGE CLE ====== */}
      <div className="glass-card rounded-xl p-4 border border-emerald-500/30 bg-emerald-500/5">
        <p className="text-sm text-emerald-300 text-center leading-relaxed">
          <strong>Point clé :</strong> Les scripts déterministes (compilation LaTeX,
          génération d&apos;images...) éliminent l&apos;imprévisibilité de l&apos;IA.
          L&apos;agent décide <em>quoi</em> faire, les scripts garantissent <em>comment</em> c&apos;est fait.
        </p>
      </div>

      {/* ====== WORKFLOW CONCRET ====== */}
      <div className="glass-card rounded-xl p-5 border border-cosmic-500/30 space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-sm font-semibold text-white">
            Exemple concret : workflow /latex
          </h4>
          {!showWorkflow && (
            <Button
              variant="outline"
              size="sm"
              onClick={handleShowWorkflow}
              className="text-cosmic-400 border-cosmic-500/30 hover:bg-cosmic-500/10 hover:text-cosmic-300"
            >
              Voir le flux
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          )}
          {showWorkflow && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => { setShowWorkflow(false); setActiveStep(0) }}
              className="text-gray-400 hover:text-white"
            >
              Fermer
            </Button>
          )}
        </div>

        {showWorkflow && (
          <div className="space-y-3">
            {WORKFLOW_STEPS.map(({ step, skill, description, colorClass, bgClass, reflexion, outils, workflowInterne }) => {
              const isActive = activeStep >= step
              const isExpanded = expandedStep === step
              return (
                <div
                  key={step}
                  className={cn(
                    'rounded-lg border transition-all duration-500',
                    isActive
                      ? [bgClass, 'border-white/15', 'opacity-100 translate-x-0']
                      : 'border-transparent opacity-0 -translate-x-4'
                  )}
                >
                  <button
                    type="button"
                    onClick={() => isActive && handleStepToggle(step)}
                    disabled={!isActive}
                    className={cn(
                      'w-full text-left flex items-start gap-3 p-3 transition-all',
                      isActive && 'cursor-pointer hover:bg-white/5'
                    )}
                  >
                    {/* Numéro d'étape */}
                    <div
                      className={cn(
                        'w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold shrink-0',
                        bgClass,
                        colorClass
                      )}
                    >
                      {step}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={cn('text-sm font-semibold', colorClass)}>
                        {skill}
                      </p>
                      <p className="text-xs text-gray-300 mt-0.5 leading-relaxed">
                        {description}
                      </p>
                    </div>
                    {isActive && (
                      <ChevronDown
                        className={cn(
                          'w-5 h-5 text-gray-400 shrink-0 transition-transform duration-300 mt-0.5',
                          isExpanded && 'rotate-180'
                        )}
                      />
                    )}
                  </button>

                  {/* Panneau de détails */}
                  {isActive && (
                    <WorkflowStepDetails
                      isOpen={isExpanded}
                      reflexion={reflexion}
                      outils={outils}
                      workflowInterne={workflowInterne}
                    />
                  )}
                </div>
              )
            })}

            {/* Resultat final */}
            <div
              className={cn(
                'flex items-center justify-center gap-2 pt-2 transition-all duration-500',
                activeStep >= 3
                  ? 'opacity-100 translate-y-0'
                  : 'opacity-0 translate-y-4'
              )}
            >
              <FileOutput className="w-5 h-5 text-green-400" />
              <span className="text-sm font-semibold text-green-400">
                PDF généré sur votre machine
              </span>
            </div>
          </div>
        )}
      </div>

      {/* ====== STYLES D'ANIMATION ====== */}
      <style jsx>{`
        @keyframes pulse-line {
          0%, 100% { opacity: 0.4; }
          50% { opacity: 1; }
        }
        :global(.animate-pulse-line) {
          animation: pulse-line 2s ease-in-out infinite;
        }
      `}</style>
    </div>
  )
}
