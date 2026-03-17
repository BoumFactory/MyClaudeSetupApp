'use client'

import Link from 'next/link'
import { Zap, Monitor, Terminal, Sparkles, MessageSquareText, CheckCircle } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { useTutorialProgress } from '@/contexts/TutorialProgressContext'
import { PARCOURS, CAPSULES } from '@/data/parcours'
import type { Parcours, Capsule } from '@/types/tutorial'

const ICON_MAP: Record<string, React.ComponentType<{ className?: string }>> = {
  Zap,
  Monitor,
  Terminal,
  Sparkles,
  MessageSquareText,
}

const COLOR_MAP: Record<string, { border: string; hover: string; badge: string; text: string }> = {
  amber: {
    border: 'border-amber-500/30',
    hover: 'hover:border-amber-500/60',
    badge: 'bg-amber-500/10 text-amber-400',
    text: 'text-amber-400',
  },
  emerald: {
    border: 'border-emerald-500/30',
    hover: 'hover:border-emerald-500/60',
    badge: 'bg-emerald-500/10 text-emerald-400',
    text: 'text-emerald-400',
  },
  cosmic: {
    border: 'border-cosmic-500/30',
    hover: 'hover:border-cosmic-500/60',
    badge: 'bg-cosmic-500/10 text-cosmic-400',
    text: 'text-cosmic-400',
  },
  nebula: {
    border: 'border-nebula-500/30',
    hover: 'hover:border-nebula-500/60',
    badge: 'bg-nebula-500/10 text-nebula-400',
    text: 'text-nebula-400',
  },
  violet: {
    border: 'border-violet-500/30',
    hover: 'hover:border-violet-500/60',
    badge: 'bg-violet-500/10 text-violet-400',
    text: 'text-violet-400',
  },
}

const DEFAULT_COLORS = {
  border: 'border-blue-500/30',
  hover: 'hover:border-blue-500/60',
  badge: 'bg-blue-500/10 text-blue-400',
  text: 'text-blue-400',
}

export function ParcoursLibreContent() {
  const { isCompleted } = useTutorialProgress()

  return (
    <div className="space-y-12">
      {PARCOURS.map((parcours) => {
        const Icon = ICON_MAP[parcours.icon]
        const colors = COLOR_MAP[parcours.color] ?? DEFAULT_COLORS

        // Récupérer toutes les capsules de ce parcours
        const capsules = parcours.capsules
          .map((id) => CAPSULES[id])
          .filter(Boolean) as Capsule[]

        return (
          <section key={parcours.id} className="space-y-6">
            {/* Titre de section avec icône */}
            <div className="flex items-center gap-3 border-b border-white/10 pb-4">
              {Icon && <Icon className={cn('w-6 h-6', colors.text)} />}
              <h2 className="text-2xl font-bold text-white">{parcours.title}</h2>
              <span className={cn('ml-auto text-sm font-medium px-3 py-1 rounded-full', colors.badge)}>
                {capsules.length} capsule{capsules.length > 1 ? 's' : ''}
              </span>
            </div>

            {/* Grille des capsules */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {capsules.map((capsule) => {
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
                      <CardHeader className="pb-3">
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex-1 min-w-0">
                            <CardTitle className="text-base text-white group-hover:text-white/90">
                              {capsule.title}
                            </CardTitle>
                          </div>
                          {completed && (
                            <CheckCircle className="w-5 h-5 text-green-400 shrink-0 mt-0.5" />
                          )}
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <CardDescription className="text-gray-400 text-sm">
                          {capsule.description}
                        </CardDescription>
                        <div className="flex items-center justify-between pt-2 border-t border-white/5">
                          {capsule.duration && (
                            <span className="text-xs text-gray-500">
                              {capsule.duration}
                            </span>
                          )}
                          {capsule.tags && capsule.tags.length > 0 && (
                            <div className="flex flex-wrap gap-1 justify-end">
                              {capsule.tags.slice(0, 2).map((tag) => (
                                <span
                                  key={tag}
                                  className={cn('text-xs px-2 py-0.5 rounded-full', colors.badge)}
                                >
                                  {tag}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </CardContent>
                    </Card>
                  </Link>
                )
              })}
            </div>
          </section>
        )
      })}
    </div>
  )
}
