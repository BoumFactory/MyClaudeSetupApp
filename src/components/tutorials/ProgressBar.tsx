'use client'

import { cn } from '@/lib/utils'
import { useTutorialProgress } from '@/contexts/TutorialProgressContext'
import { getParcoursById } from '@/data/parcours'

/** Mapping couleur parcours vers classes Tailwind */
const COLOR_MAP: Record<string, { bar: string; text: string }> = {
  amber: { bar: 'bg-amber-500', text: 'text-amber-400' },
  emerald: { bar: 'bg-emerald-500', text: 'text-emerald-400' },
  cosmic: { bar: 'bg-gradient-to-r from-cosmic-400 to-cosmic-600', text: 'text-cosmic-400' },
  nebula: { bar: 'bg-gradient-to-r from-nebula-400 to-nebula-600', text: 'text-nebula-400' },
  violet: { bar: 'bg-gradient-to-r from-violet-400 to-purple-600', text: 'text-violet-400' },
}

const DEFAULT_COLOR = { bar: 'bg-blue-500', text: 'text-blue-400' }

interface ProgressBarProps {
  parcoursId: string
  showLabel?: boolean
}

export function ProgressBar({ parcoursId, showLabel = true }: ProgressBarProps) {
  const { getParcoursProgress } = useTutorialProgress()
  const { completed, total, percent } = getParcoursProgress(parcoursId)
  const parcours = getParcoursById(parcoursId)
  const colors = COLOR_MAP[parcours?.color ?? ''] ?? DEFAULT_COLOR

  return (
    <div className="space-y-2">
      {showLabel && (
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-400">
            {completed} / {total} capsules
          </span>
          <span className={cn('font-semibold', colors.text)}>{percent}%</span>
        </div>
      )}
      <div className="h-3 rounded-full bg-white/10 overflow-hidden shadow-inner">
        <div
          className={cn('h-full rounded-full transition-all duration-700 ease-out shadow-lg', colors.bar)}
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  )
}
