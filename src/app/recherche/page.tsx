'use client'

import { useState, useMemo, useCallback } from 'react'
import { buildSearchIndex } from '@/data/search-index'
import type { SearchCategory } from '@/data/search-index'
import { search, groupByCategory, CATEGORY_INFO } from '@/lib/search-engine'
import type { SearchResult } from '@/lib/search-engine'
import { Search, ExternalLink, ChevronDown, ChevronRight, Filter, Expand, Shrink, Tag } from 'lucide-react'
import { cn } from '@/lib/utils'

// Color mapping for category badges
const colorMap: Record<string, string> = {
  emerald: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
  cosmic: 'bg-cosmic-500/20 text-cosmic-300 border-cosmic-500/30',
  purple: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
  sky: 'bg-sky-500/20 text-sky-300 border-sky-500/30',
  amber: 'bg-amber-500/20 text-amber-300 border-amber-500/30',
  red: 'bg-red-500/20 text-red-300 border-red-500/30',
  slate: 'bg-slate-500/20 text-slate-300 border-slate-500/30',
}

const matchLevelLabels: Record<string, { label: string; color: string }> = {
  title: { label: 'Titre', color: 'text-emerald-400' },
  tag: { label: 'Tag', color: 'text-cosmic-400' },
  description: { label: 'Description', color: 'text-amber-400' },
  content: { label: 'Contenu', color: 'text-white/40' },
}

function ResultCard({ result, expanded }: { result: SearchResult; expanded: boolean }) {
  const { item, matchLevel, snippet } = result
  const catInfo = CATEGORY_INFO[item.category]
  const catColor = colorMap[catInfo.color] || colorMap.slate

  return (
    <a
      href={item.url}
      target="_blank"
      rel="noopener noreferrer"
      className={cn(
        'block p-4 rounded-lg transition-all duration-200',
        'bg-white/5 border border-white/10',
        'hover:bg-white/10 hover:border-white/20',
        'group'
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          {/* Title row */}
          <div className="flex items-center gap-2 mb-1">
            {item.icon && <span className="text-lg">{item.icon}</span>}
            <h3 className="font-medium text-white truncate group-hover:text-cosmic-300 transition-colors">
              {item.title}
            </h3>
            <ExternalLink className="w-3.5 h-3.5 text-white/20 group-hover:text-white/50 flex-shrink-0 transition-colors" />
          </div>

          {/* Category + match level */}
          <div className="flex items-center gap-2 mb-2 flex-wrap">
            <span className={cn('text-xs px-2 py-0.5 rounded-full border', catColor)}>
              {catInfo.icon} {item.categoryLabel}
            </span>
            <span className={cn('text-xs', matchLevelLabels[matchLevel].color)}>
              via {matchLevelLabels[matchLevel].label}
            </span>
            {item.meta && Object.entries(item.meta).slice(0, 2).map(([key, val]) => (
              <span key={key} className="text-xs text-white/30">
                {val}
              </span>
            ))}
          </div>

          {/* Description (expanded mode) */}
          {expanded && (
            <p className="text-sm text-white/50 mb-2 line-clamp-2">
              {item.description}
            </p>
          )}

          {/* Snippet (expanded mode) */}
          {expanded && snippet && (
            <div className="text-xs text-white/30 bg-white/5 rounded px-2 py-1 mb-2 line-clamp-2 italic">
              {snippet}
            </div>
          )}

          {/* Tags */}
          {expanded && item.tags.length > 0 && (
            <div className="flex items-center gap-1 flex-wrap">
              <Tag className="w-3 h-3 text-white/20" />
              {item.tags.slice(0, 6).map((tag, i) => (
                <span key={i} className="text-xs text-white/30 bg-white/5 rounded px-1.5 py-0.5">
                  {tag}
                </span>
              ))}
              {item.tags.length > 6 && (
                <span className="text-xs text-white/20">+{item.tags.length - 6}</span>
              )}
            </div>
          )}
        </div>
      </div>
    </a>
  )
}

export default function RecherchePage() {
  const [query, setQuery] = useState('')
  const [expanded, setExpanded] = useState(false)
  const [activeCategories, setActiveCategories] = useState<Set<SearchCategory>>(new Set())
  const [collapsedGroups, setCollapsedGroups] = useState<Set<SearchCategory>>(new Set())

  // Build index once
  const index = useMemo(() => buildSearchIndex(), [])

  // Search results
  const results = useMemo(() => {
    if (!query.trim()) return []
    return search(query, index, {
      categories: activeCategories.size > 0 ? Array.from(activeCategories) : undefined,
      maxPerCategory: 20,
    })
  }, [query, index, activeCategories])

  const grouped = useMemo(() => groupByCategory(results), [results])

  const toggleCategory = useCallback((cat: SearchCategory) => {
    setActiveCategories(prev => {
      const next = new Set(prev)
      if (next.has(cat)) next.delete(cat)
      else next.add(cat)
      return next
    })
  }, [])

  const toggleGroupCollapse = useCallback((cat: SearchCategory) => {
    setCollapsedGroups(prev => {
      const next = new Set(prev)
      if (next.has(cat)) next.delete(cat)
      else next.add(cat)
      return next
    })
  }, [])

  const allCategories: SearchCategory[] = ['tutoriel', 'presentation', 'package', 'application', 'formation', 'video', 'vocabulaire']

  return (
    <div className="container mx-auto px-4 py-12 max-w-4xl">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Recherche</h1>
        <p className="text-white/50 text-sm">
          Tutoriels, présentations, packages, applications, vocabulaire...
        </p>
      </div>

      {/* Search input */}
      <div className="relative mb-6">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-white/30" />
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Rechercher par mot-clé, compétence, outil..."
          className={cn(
            'w-full pl-12 pr-4 py-3 rounded-xl',
            'bg-white/5 border border-white/10',
            'text-white placeholder:text-white/30',
            'focus:outline-none focus:ring-2 focus:ring-cosmic-500/50 focus:border-cosmic-500/30',
            'text-lg transition-all duration-200'
          )}
          autoFocus
        />
        {query && (
          <span className="absolute right-4 top-1/2 -translate-y-1/2 text-xs text-white/30">
            {results.length} résultat{results.length !== 1 ? 's' : ''}
          </span>
        )}
      </div>

      {/* Filters + View toggle */}
      <div className="flex items-center justify-between gap-4 mb-6 flex-wrap">
        <div className="flex items-center gap-2 flex-wrap">
          <Filter className="w-4 h-4 text-white/30 flex-shrink-0" />
          {allCategories.map(cat => {
            const info = CATEGORY_INFO[cat]
            const isActive = activeCategories.has(cat)
            return (
              <button
                key={cat}
                onClick={() => toggleCategory(cat)}
                className={cn(
                  'text-xs px-2.5 py-1 rounded-full border transition-all duration-200',
                  isActive
                    ? colorMap[info.color]
                    : 'border-white/10 text-white/30 hover:text-white/50 hover:border-white/20'
                )}
              >
                {info.icon} {info.label}
              </button>
            )
          })}
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center gap-1.5 text-xs text-white/40 hover:text-white/60 transition-colors"
        >
          {expanded ? <Shrink className="w-3.5 h-3.5" /> : <Expand className="w-3.5 h-3.5" />}
          {expanded ? 'Vue compacte' : 'Vue détaillée'}
        </button>
      </div>

      {/* Results */}
      {!query.trim() ? (
        <div className="text-center py-20 text-white/30">
          <Search className="w-12 h-12 mx-auto mb-4 opacity-30" />
          <p className="text-lg">Tapez votre recherche</p>
          <p className="text-sm mt-2">Mots-clés, noms d'outils, compétences, concepts...</p>
        </div>
      ) : results.length === 0 ? (
        <div className="text-center py-20 text-white/30">
          <p className="text-lg mb-2">Aucun résultat pour « {query} »</p>
          <p className="text-sm">Essayez des termes plus généraux ou vérifiez l'orthographe</p>
        </div>
      ) : (
        <div className="space-y-6">
          {Array.from(grouped.entries()).map(([category, categoryResults]) => {
            const info = CATEGORY_INFO[category]
            const isCollapsed = collapsedGroups.has(category)

            return (
              <div key={category} className="glass-card rounded-xl border border-white/10 overflow-hidden">
                {/* Category header */}
                <button
                  onClick={() => toggleGroupCollapse(category)}
                  className="w-full flex items-center justify-between px-4 py-3 hover:bg-white/5 transition-colors"
                >
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{info.icon}</span>
                    <h2 className="font-semibold text-white text-sm">{info.label}</h2>
                    <span className="text-xs text-white/30 bg-white/10 rounded-full px-2 py-0.5">
                      {categoryResults.length}
                    </span>
                  </div>
                  {isCollapsed
                    ? <ChevronRight className="w-4 h-4 text-white/30" />
                    : <ChevronDown className="w-4 h-4 text-white/30" />
                  }
                </button>

                {/* Results list */}
                {!isCollapsed && (
                  <div className="px-3 pb-3 space-y-2">
                    {categoryResults.map(result => (
                      <ResultCard
                        key={result.item.id}
                        result={result}
                        expanded={expanded}
                      />
                    ))}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
