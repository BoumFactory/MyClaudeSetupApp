'use client'

import { useState, useCallback } from 'react'
import { X, SlidersHorizontal } from 'lucide-react'
import { Button } from '@/components/ui/button'
import type { CategoriesConfig } from '@/lib/file-scanner-server'

export interface FilterState {
  level: string | null
  tags: string[]
}

interface PresentationFiltersProps {
  categories: CategoriesConfig
  onFilter: (filters: FilterState) => void
}

const LEVEL_LABELS: Record<string, string> = {
  'débutant': 'Débutant',
  'intermédiaire': 'Intermédiaire',
  'avancé': 'Avancé',
}

const LEVEL_COLORS: Record<string, string> = {
  'débutant': 'text-emerald-400 border-emerald-500/40 bg-emerald-500/10 hover:bg-emerald-500/20',
  'intermédiaire': 'text-amber-400 border-amber-500/40 bg-amber-500/10 hover:bg-amber-500/20',
  'avancé': 'text-rose-400 border-rose-500/40 bg-rose-500/10 hover:bg-rose-500/20',
}

const LEVEL_COLORS_ACTIVE: Record<string, string> = {
  'débutant': 'text-emerald-300 border-emerald-400 bg-emerald-500/30',
  'intermédiaire': 'text-amber-300 border-amber-400 bg-amber-500/30',
  'avancé': 'text-rose-300 border-rose-400 bg-rose-500/30',
}

export function PresentationFilters({ categories, onFilter }: PresentationFiltersProps) {
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null)
  const [selectedTags, setSelectedTags] = useState<string[]>([])

  const availableLevels = categories.settings.availableLevels ?? ['débutant', 'intermédiaire', 'avancé']
  const availableTags = categories.settings.availableTags ?? []

  const handleLevelToggle = useCallback((level: string) => {
    const newLevel = selectedLevel === level ? null : level
    setSelectedLevel(newLevel)
    onFilter({ level: newLevel, tags: selectedTags })
  }, [selectedLevel, selectedTags, onFilter])

  const handleTagToggle = useCallback((tag: string) => {
    const newTags = selectedTags.includes(tag)
      ? selectedTags.filter((t) => t !== tag)
      : [...selectedTags, tag]
    setSelectedTags(newTags)
    onFilter({ level: selectedLevel, tags: newTags })
  }, [selectedTags, selectedLevel, onFilter])

  const handleReset = useCallback(() => {
    setSelectedLevel(null)
    setSelectedTags([])
    onFilter({ level: null, tags: [] })
  }, [onFilter])

  const hasActiveFilters = selectedLevel !== null || selectedTags.length > 0

  return (
    <div className="glass-card rounded-xl p-5 space-y-5">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="w-4 h-4 text-cosmic-400" />
          <span className="font-semibold text-sm">Filtrer les présentations</span>
          {hasActiveFilters && (
            <span className="px-2 py-0.5 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium border border-cosmic-500/30">
              {(selectedLevel ? 1 : 0) + selectedTags.length} actif{(selectedLevel ? 1 : 0) + selectedTags.length > 1 ? 's' : ''}
            </span>
          )}
        </div>
        {hasActiveFilters && (
          <button
            onClick={handleReset}
            className="flex items-center gap-1.5 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <X className="w-3.5 h-3.5" />
            Réinitialiser
          </button>
        )}
      </div>

      {/* Sélecteur de niveau */}
      <div className="space-y-2">
        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Niveau</p>
        <div className="flex flex-wrap gap-2">
          {availableLevels.map((level) => {
            const isActive = selectedLevel === level
            const colorClass = isActive ? LEVEL_COLORS_ACTIVE[level] : LEVEL_COLORS[level]
            return (
              <button
                key={level}
                onClick={() => handleLevelToggle(level)}
                className={`px-3.5 py-1.5 rounded-full border text-sm font-medium transition-all duration-200 ${colorClass ?? 'text-muted-foreground border-border hover:border-cosmic-500/40'}`}
              >
                {LEVEL_LABELS[level] ?? level}
              </button>
            )
          })}
        </div>
      </div>

      {/* Tags */}
      {availableTags.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider">Tags</p>
          <div className="flex flex-wrap gap-2">
            {availableTags.map((tag) => {
              const isActive = selectedTags.includes(tag)
              return (
                <button
                  key={tag}
                  onClick={() => handleTagToggle(tag)}
                  className={`px-2.5 py-1 rounded-md border text-xs font-medium transition-all duration-200 ${
                    isActive
                      ? 'text-nebula-300 border-nebula-400/60 bg-nebula-500/25'
                      : 'text-muted-foreground border-border hover:border-nebula-500/40 hover:text-nebula-400 hover:bg-nebula-500/10'
                  }`}
                >
                  {tag}
                </button>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
