'use client'

import Link from 'next/link'
import { Zap, Monitor, Terminal, Sparkles, MessageSquareText, ChevronRight, CheckCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { ProgressBar } from '@/components/tutorials/ProgressBar'
import { useTutorialProgress } from '@/contexts/TutorialProgressContext'
import type { Parcours, Capsule } from '@/types/tutorial'

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap,
  Monitor,
  Terminal,
  Sparkles,
  MessageSquareText,
}

const COLOR_MAP: Record<string, { border: string; hover: string; badge: string }> = {
  amber: {
    border: 'border-amber-500/30',
    hover: 'hover:border-amber-500/60',
    badge: 'bg-amber-500/10 text-amber-400',
  },
  emerald: {
    border: 'border-emerald-500/30',
    hover: 'hover:border-emerald-500/60',
    badge: 'bg-emerald-500/10 text-emerald-400',
  },
  cosmic: {
    border: 'border-cosmic-500/30',
    hover: 'hover:border-cosmic-500/60',
    badge: 'bg-cosmic-500/10 text-cosmic-400',
  },
  nebula: {
    border: 'border-nebula-500/30',
    hover: 'hover:border-nebula-500/60',
    badge: 'bg-nebula-500/10 text-nebula-400',
  },
  violet: {
    border: 'border-violet-500/30',
    hover: 'hover:border-violet-500/60',
    badge: 'bg-violet-500/10 text-violet-400',
  },
}

const DEFAULT_COLORS = {
  border: 'border-blue-500/30',
  hover: 'hover:border-blue-500/60',
  badge: 'bg-blue-500/10 text-blue-400',
}

interface ParcoursContentProps {
  parcours: Parcours
  capsules: Capsule[]
}

export function ParcoursContent({ parcours, capsules }: ParcoursContentProps) {
  const { isCompleted } = useTutorialProgress()
  const Icon = ICON_MAP[parcours.icon]
  const colors = COLOR_MAP[parcours.color] ?? DEFAULT_COLORS

  return (
    <div className="max-w-4xl mx-auto space-y-8 px-4 py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-400">
        <Link href="/claude-code/tutorials" className="hover:text-white transition-colors">
          Tutoriels
        </Link>
        <ChevronRight className="w-4 h-4" />
        <span className="text-white">{parcours.title}</span>
      </nav>

      {/* En-tete */}
      <div className="glass-card rounded-xl p-6 space-y-4">
        <div className="flex items-center gap-3">
          {Icon && <Icon className={cn('w-8 h-8', colors.badge.split(' ')[1])} />}
          <div>
            <h1 className="text-3xl font-bold text-white">{parcours.title}</h1>
            <p className="text-gray-400 mt-1">{parcours.description}</p>
          </div>
        </div>
        <ProgressBar parcoursId={parcours.id} />
      </div>

      {/* Grille des capsules */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {capsules.map((capsule, index) => {
          const completed = isCompleted(capsule.id)
          return (
            <Link
              key={capsule.id}
              href={`/claude-code/tutorials/parcours/${parcours.id}/${capsule.id}`}
              className="block group"
            >
              <Card
                className={cn(
                  'glass-card border transition-all duration-200 h-full',
                  colors.border,
                  colors.hover,
                  'hover:shadow-lg'
                )}
              >
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <span
                        className={cn(
                          'flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold',
                          colors.badge
                        )}
                      >
                        {index + 1}
                      </span>
                      <CardTitle className="text-lg text-white group-hover:text-white/90">
                        {capsule.title}
                      </CardTitle>
                    </div>
                    {completed && (
                      <CheckCircle className="w-5 h-5 text-green-400 shrink-0" />
                    )}
                  </div>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-gray-400">
                    {capsule.description}
                  </CardDescription>
                  {capsule.duration && (
                    <span className="inline-block mt-2 text-xs text-gray-500 bg-white/5 px-2 py-0.5 rounded">
                      {capsule.duration}
                    </span>
                  )}
                </CardContent>
              </Card>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
