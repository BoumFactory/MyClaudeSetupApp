'use client'

import { useState, useEffect, useRef, useCallback, type ReactNode } from 'react'
import { BookOpen, Eye, Play, CheckCircle, ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { processVocabulary } from '@/lib/vocabulary-processor'
import { useTutorialProgress } from '@/contexts/TutorialProgressContext'
import type { Capsule as CapsuleType } from '@/types/tutorial'

/** Configuration des sections d'une capsule */
const SECTION_CONFIG = [
  {
    key: 'info' as const,
    label: 'À savoir',
    icon: BookOpen,
    color: 'text-blue-400',
    bgColor: 'bg-blue-500/10',
    borderColor: 'border-blue-500/30',
    borderLeftColor: 'border-l-blue-500',
    activeBgColor: 'bg-white/[0.03]',
  },
  {
    key: 'exemple' as const,
    label: 'Exemple',
    icon: Eye,
    color: 'text-amber-400',
    bgColor: 'bg-amber-500/10',
    borderColor: 'border-amber-500/30',
    borderLeftColor: 'border-l-amber-500',
    activeBgColor: 'bg-white/[0.03]',
  },
  {
    key: 'pratique' as const,
    label: 'À vous de jouer',
    icon: Play,
    color: 'text-green-400',
    bgColor: 'bg-green-500/10',
    borderColor: 'border-green-500/30',
    borderLeftColor: 'border-l-emerald-500',
    activeBgColor: 'bg-white/[0.03]',
  },
] as const

interface CapsuleProps {
  capsule: CapsuleType
  /** Composants React a injecter apres le contenu HTML d'une section */
  sectionComponents?: Partial<Record<'info' | 'exemple' | 'pratique', ReactNode>>
}

export function Capsule({ capsule, sectionComponents }: CapsuleProps) {
  const { isCompleted, markComplete, setLastVisited } = useTutorialProgress()
  const completed = isCompleted(capsule.id)
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({})
  const containerRef = useRef<HTMLDivElement>(null)

  // Marquer comme dernière capsule visitée
  useEffect(() => {
    setLastVisited(capsule.id)
  }, [capsule.id, setLastVisited])

  // Gestion clic-to-pin des tooltips vocabulaire
  const setupVocabListeners = useCallback(() => {
    const container = containerRef.current
    if (!container) return

    const handleTermClick = (e: Event) => {
      const term = (e.currentTarget as HTMLElement)
      // Fermer les autres tooltips pinnés
      container.querySelectorAll('.vocab-term.vocab-pinned').forEach((el) => {
        if (el !== term) el.classList.remove('vocab-pinned')
      })
      // Toggle pin sur ce terme
      term.classList.toggle('vocab-pinned')
      e.stopPropagation()
    }

    const handleCloseClick = (e: Event) => {
      const btn = e.currentTarget as HTMLElement
      btn.closest('.vocab-term')?.classList.remove('vocab-pinned')
      e.stopPropagation()
    }

    // Fermer au clic ailleurs
    const handleDocClick = () => {
      container.querySelectorAll('.vocab-term.vocab-pinned').forEach((el) => {
        el.classList.remove('vocab-pinned')
      })
    }

    container.querySelectorAll('.vocab-term').forEach((el) => {
      el.addEventListener('click', handleTermClick)
    })
    container.querySelectorAll('.vocab-tooltip-close').forEach((el) => {
      el.addEventListener('click', handleCloseClick)
    })
    document.addEventListener('click', handleDocClick)

    return () => {
      container.querySelectorAll('.vocab-term').forEach((el) => {
        el.removeEventListener('click', handleTermClick)
      })
      container.querySelectorAll('.vocab-tooltip-close').forEach((el) => {
        el.removeEventListener('click', handleCloseClick)
      })
      document.removeEventListener('click', handleDocClick)
    }
  }, [])

  // Gestion des onglets CLI injectés via dangerouslySetInnerHTML
  useEffect(() => {
    const container = containerRef.current
    if (!container) return

    const handleTabClick = (e: Event) => {
      const btn = e.currentTarget as HTMLElement
      const targetId = btn.getAttribute('data-tab-target')
      const tabsContainer = btn.closest('[data-cli-tabs]')
      if (!targetId || !tabsContainer) return

      tabsContainer.querySelectorAll('.cli-tab-btn').forEach((b) => b.classList.remove('active'))
      tabsContainer.querySelectorAll('.cli-tab-panel').forEach((p) => p.classList.remove('active'))
      btn.classList.add('active')
      tabsContainer.querySelector(`#${targetId}`)?.classList.add('active')
    }

    container.querySelectorAll('.cli-tab-btn').forEach((btn) => {
      btn.addEventListener('click', handleTabClick)
    })

    return () => {
      container.querySelectorAll('.cli-tab-btn').forEach((btn) => {
        btn.removeEventListener('click', handleTabClick)
      })
    }
  }, [openSections])

  // Ré-attacher les listeners quand les sections s'ouvrent
  useEffect(() => {
    const cleanup = setupVocabListeners()
    return cleanup
  }, [openSections, setupVocabListeners])

  const toggleSection = (key: string) => {
    setOpenSections((prev) => ({ ...prev, [key]: !prev[key] }))
  }

  return (
    <div ref={containerRef} className="glass-card rounded-xl p-6 space-y-4">
      {/* En-tete */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold text-white">{capsule.title}</h2>
          <p className="text-gray-400 mt-1">{capsule.description}</p>
          {capsule.duration && (
            <span className="inline-block mt-2 text-xs text-gray-500 bg-white/5 px-2 py-1 rounded">
              {capsule.duration}
            </span>
          )}
        </div>
        {completed && (
          <span className="flex items-center gap-1.5 text-sm font-medium text-green-400 bg-green-500/10 px-3 py-1.5 rounded-full shrink-0">
            <CheckCircle className="w-4 h-4" />
            Terminé
          </span>
        )}
      </div>

      {/* Sections accordeon */}
      <div className="space-y-3">
        {SECTION_CONFIG.map(({ key, label, icon: Icon, color, bgColor, borderColor, borderLeftColor, activeBgColor }) => {
          const isOpen = openSections[key] ?? false
          return (
            <div
              key={key}
              className={cn(
                'rounded-lg border-l-4 border transition-all duration-300',
                borderColor,
                borderLeftColor,
                isOpen ? [activeBgColor, 'shadow-md'] : 'bg-transparent'
              )}
            >
              <button
                type="button"
                onClick={() => toggleSection(key)}
                aria-expanded={isOpen}
                aria-controls={`section-panel-${key}`}
                className={cn(
                  'w-full flex items-center justify-between px-4 py-3 text-left transition-colors duration-200',
                  isOpen ? 'hover:opacity-90' : 'hover:bg-white/5'
                )}
              >
                <span className={cn('flex items-center gap-2 font-semibold', color)}>
                  <Icon className="w-5 h-5" />
                  {label}
                </span>
                <ChevronDown
                  className={cn(
                    'w-4 h-4 transition-transform duration-300',
                    color,
                    isOpen && 'rotate-180'
                  )}
                />
              </button>
              {isOpen && (
                <div
                  id={`section-panel-${key}`}
                  role="region"
                  className="px-4 pb-4 pt-2 border-t border-white/10 capsule-content"
                >
                  <div
                    className="prose prose-invert prose-sm max-w-none"
                    dangerouslySetInnerHTML={{ __html: processVocabulary(capsule.sections[key]) }}
                  />
                  {/* Composant React custom injecte apres le HTML */}
                  {sectionComponents?.[key] && (
                    <div className="mt-4">
                      {sectionComponents[key]}
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      {/* Bouton marquer comme fait */}
      {!completed && (
        <div className="pt-4 border-t border-white/10">
          <Button
            onClick={() => markComplete(capsule.id)}
            className="w-full bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-600 text-white font-semibold transition-all duration-200"
          >
            <CheckCircle className="w-4 h-4 mr-2" />
            Marquer comme fait
          </Button>
        </div>
      )}
    </div>
  )
}
