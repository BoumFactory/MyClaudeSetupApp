'use client'

import { Zap, Monitor, Terminal, Sparkles, MessageSquareText, RotateCcw } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { ProgressBar } from '@/components/tutorials/ProgressBar'
import { useTutorialProgress } from '@/contexts/TutorialProgressContext'
import { PARCOURS } from '@/data/parcours'

/** Mapping noms d'icones vers composants Lucide */
const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap,
  Monitor,
  Terminal,
  Sparkles,
  MessageSquareText,
}

/** Mapping couleurs vers classes pour les icones */
const ICON_COLOR_MAP: Record<string, string> = {
  amber: 'text-amber-400',
  emerald: 'text-emerald-400',
  cosmic: 'text-cosmic-400',
  nebula: 'text-nebula-400',
  violet: 'text-violet-400',
}

export function ProgressDashboard() {
  const { resetProgress } = useTutorialProgress()

  return (
    <div className="glass-card rounded-xl p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-2xl font-bold text-white">Votre progression</h3>
        <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cosmic-500 to-nebula-500 flex items-center justify-center">
          <Sparkles className="w-5 h-5 text-white" />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {PARCOURS.map((parcours) => {
          const Icon = ICON_MAP[parcours.icon]
          const iconColor = ICON_COLOR_MAP[parcours.color] ?? 'text-blue-400'

          return (
            <div
              key={parcours.id}
              className={cn(
                'space-y-3 p-5 rounded-lg border transition-all duration-300',
                'bg-white/5 border-white/15 hover:bg-white/8 hover:border-white/25'
              )}
            >
              <div className="flex items-center gap-3">
                {Icon && (
                  <div className={cn('w-10 h-10 rounded-lg flex items-center justify-center', `bg-${parcours.color}-500/20`)}>
                    <Icon className={cn('w-5 h-5', iconColor)} />
                  </div>
                )}
                <span className="font-semibold text-white text-base">{parcours.title}</span>
              </div>
              <ProgressBar parcoursId={parcours.id} />
            </div>
          )
        })}
      </div>

      <div className="flex justify-end pt-2 border-t border-white/10">
        <Button
          variant="ghost"
          size="sm"
          onClick={resetProgress}
          className="text-gray-400 hover:text-gray-200 hover:bg-white/5 text-xs"
        >
          <RotateCcw className="w-3.5 h-3.5 mr-1.5" />
          Réinitialiser la progression
        </Button>
      </div>
    </div>
  )
}
