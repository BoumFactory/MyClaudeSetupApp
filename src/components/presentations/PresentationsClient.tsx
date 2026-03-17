'use client'

import { useState, useCallback } from 'react'
import Link from 'next/link'
import { BookOpen, Calendar, ArrowRight, Code2, Cpu, FileCode, Palette, Layers, Package, Settings, FolderOpen } from 'lucide-react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { PresentationPreview } from '@/components/presentations/PresentationPreview'
import { PresentationFilters, FilterState } from '@/components/presentations/PresentationFilters'
import { formatDate } from '@/lib/utils'
import type { CategoriesConfig, PresentationCategory, PresentationSubcategory } from '@/lib/file-scanner-server'
import type { Presentation } from '@/types'

const iconMap: Record<string, any> = {
  Layers,
  Cpu,
  Code2,
  Palette,
  FileCode,
  Package,
  Settings,
  BookOpen,
  FolderOpen,
}

function getIconComponent(iconName: string) {
  return iconMap[iconName] || BookOpen
}

function getCategoryBackgroundStyle(categoryId: string): React.CSSProperties {
  const styles: Record<string, React.CSSProperties> = {
    architecture: {
      backgroundImage: `
        linear-gradient(135deg, rgba(59, 130, 246, 0.05) 25%, transparent 25%),
        linear-gradient(225deg, rgba(147, 51, 234, 0.05) 25%, transparent 25%),
        linear-gradient(45deg, rgba(59, 130, 246, 0.03) 25%, transparent 25%),
        linear-gradient(315deg, rgba(147, 51, 234, 0.03) 25%, transparent 25%)
      `,
      backgroundSize: '40px 40px',
      backgroundPosition: '0 0, 20px 0, 20px -20px, 0px 20px',
    },
    interface: {
      backgroundImage: `
        repeating-linear-gradient(0deg, rgba(34, 197, 94, 0.03) 0px, transparent 1px, transparent 2px, rgba(34, 197, 94, 0.03) 3px),
        repeating-linear-gradient(90deg, rgba(20, 184, 166, 0.03) 0px, transparent 1px, transparent 2px, rgba(20, 184, 166, 0.03) 3px)
      `,
      backgroundSize: '20px 20px',
    },
    skills: {
      backgroundImage: `radial-gradient(circle at 20% 50%, rgba(6, 182, 212, 0.08) 0%, transparent 50%),
                       radial-gradient(circle at 80% 80%, rgba(99, 102, 241, 0.08) 0%, transparent 50%),
                       radial-gradient(circle at 40% 20%, rgba(6, 182, 212, 0.05) 0%, transparent 50%)`,
    },
    agents: {
      backgroundImage: `
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.1) 0%, transparent 25%),
        radial-gradient(circle at 20% 80%, rgba(168, 85, 247, 0.08) 0%, transparent 30%),
        radial-gradient(circle at 80% 20%, rgba(217, 70, 239, 0.08) 0%, transparent 30%)
      `,
    },
    presentations: {
      backgroundImage: `
        linear-gradient(90deg, rgba(249, 115, 22, 0.05) 1px, transparent 1px),
        linear-gradient(180deg, rgba(236, 72, 153, 0.05) 1px, transparent 1px)
      `,
      backgroundSize: '30px 30px',
    },
    latex: {
      backgroundImage: `
        linear-gradient(45deg, rgba(100, 116, 139, 0.03) 25%, transparent 25%),
        linear-gradient(-45deg, rgba(100, 116, 139, 0.03) 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, rgba(100, 116, 139, 0.03) 75%),
        linear-gradient(-45deg, transparent 75%, rgba(100, 116, 139, 0.03) 75%)
      `,
      backgroundSize: '20px 20px',
      backgroundPosition: '0 0, 0 10px, 10px -10px, -10px 0px',
    },
    educational: {
      backgroundImage: `
        radial-gradient(circle at 30% 30%, rgba(245, 158, 11, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 70% 70%, rgba(251, 146, 60, 0.08) 0%, transparent 40%),
        linear-gradient(135deg, rgba(245, 158, 11, 0.02) 25%, transparent 25%)
      `,
      backgroundSize: '60px 60px, 60px 60px, 20px 20px',
    },
  }

  return styles[categoryId] || {}
}

export type EnrichedPresentation = Presentation & {
  comment: string
  tags?: string[]
  level?: string
  configUpdatedAt?: string
}

interface OrganizedData {
  category: PresentationCategory
  subcategories: Array<{
    subcategory: PresentationSubcategory
    presentations: EnrichedPresentation[]
  }>
}

interface PresentationsClientProps {
  presentations: Presentation[]
  organizedData: OrganizedData[]
  categoriesConfig: CategoriesConfig
  totalCount: number
}

function matchesFilters(presentation: EnrichedPresentation, filters: FilterState): boolean {
  if (filters.level && presentation.level !== filters.level) {
    return false
  }
  if (filters.tags.length > 0) {
    const presentationTags = presentation.tags ?? []
    const hasAllTags = filters.tags.every((tag) => presentationTags.includes(tag))
    if (!hasAllTags) return false
  }
  return true
}

export function PresentationsClient({
  presentations,
  organizedData,
  categoriesConfig,
  totalCount,
}: PresentationsClientProps) {
  const [filters, setFilters] = useState<FilterState>({ level: null, tags: [] })

  const handleFilter = useCallback((newFilters: FilterState) => {
    setFilters(newFilters)
  }, [])

  const hasActiveFilters = filters.level !== null || filters.tags.length > 0

  // Filtrer les données organisées
  const filteredData = organizedData
    .map(({ category, subcategories }) => ({
      category,
      subcategories: subcategories
        .map(({ subcategory, presentations: subPresentations }) => ({
          subcategory,
          presentations: hasActiveFilters
            ? subPresentations.filter((p) => matchesFilters(p, filters))
            : subPresentations,
        }))
        .filter(({ presentations: subPresentations }) => subPresentations.length > 0),
    }))
    .filter(({ subcategories }) => subcategories.length > 0)

  const filteredCount = filteredData.reduce(
    (total, { subcategories }) =>
      total + subcategories.reduce((s, { presentations: p }) => s + p.length, 0),
    0
  )

  return (
    <div className="space-y-8">
      {/* Statistiques */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-6 text-center">
          <div className="text-3xl font-bold text-cosmic-400">
            {hasActiveFilters ? filteredCount : totalCount}
          </div>
          <div className="text-sm text-muted-foreground mt-1">
            {hasActiveFilters ? 'Présentations filtrées' : 'Présentations disponibles'}
          </div>
        </div>
        <div className="glass-card rounded-xl p-6 text-center">
          <div className="text-3xl font-bold text-nebula-400">
            100%
          </div>
          <div className="text-sm text-muted-foreground mt-1">
            Interactives
          </div>
        </div>
        <div className="glass-card rounded-xl p-6 text-center">
          <div className="text-3xl font-bold text-cosmic-400">
            Reveal.js
          </div>
          <div className="text-sm text-muted-foreground mt-1">
            Technologie utilisée
          </div>
        </div>
      </div>

      {/* Filtres */}
      <PresentationFilters categories={categoriesConfig} onFilter={handleFilter} />

      {/* Liste des présentations par catégories */}
      {filteredData.length > 0 ? (
        <div className="space-y-16">
          {filteredData.map(({ category, subcategories }) => {
            const Icon = getIconComponent(category.icon)
            const totalPresentations = subcategories.reduce(
              (sum, { presentations: p }) => sum + p.length,
              0
            )

            return (
              <section key={category.id} className="space-y-8">
                {/* En-tête de catégorie principale */}
                <div className="flex items-start gap-4">
                  <div
                    className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${category.gradient} border-2 ${(category as any).borderColor} flex items-center justify-center flex-shrink-0 shadow-xl`}
                  >
                    <Icon className={`w-9 h-9 text-${category.color}-400`} />
                  </div>
                  <div className="flex-1">
                    <h2 className={`text-3xl font-bold text-${category.color}-400`}>
                      {category.name}
                    </h2>
                    <p className="text-muted-foreground mt-2 text-lg">
                      {category.description}
                    </p>
                    <div className="text-sm text-muted-foreground mt-2 flex items-center gap-2">
                      <span className="px-2 py-1 rounded-full bg-cosmic-900/30">
                        {subcategories.length} sous-catégorie{subcategories.length > 1 ? 's' : ''}
                      </span>
                      <span className="px-2 py-1 rounded-full bg-cosmic-900/30">
                        {totalPresentations} présentation{totalPresentations > 1 ? 's' : ''}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Sous-catégories */}
                <div className="space-y-10 ml-8">
                  {subcategories.map(({ subcategory, presentations: subPresentations }) => (
                    <div key={subcategory.id} className="space-y-4">
                      {/* En-tête de sous-catégorie */}
                      <div
                        className="border-l-4 pl-4"
                        style={{ borderColor: `rgb(var(--${category.color}-500) / 0.5)` }}
                      >
                        <h3 className={`text-xl font-semibold text-${category.color}-300`}>
                          {subcategory.name}
                        </h3>
                        <p className="text-muted-foreground text-sm mt-1">
                          {subcategory.description}
                        </p>
                        <div className="text-xs text-muted-foreground mt-2">
                          {subPresentations.length} présentation{subPresentations.length > 1 ? 's' : ''}
                        </div>
                      </div>

                      {/* Cartes des présentations */}
                      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {subPresentations.map((presentation) => (
                          <Card
                            key={presentation.id}
                            className={`glass-card hover:scale-[1.02] transition-all duration-300 group cursor-pointer relative overflow-hidden border-2 ${(category as any).borderColor || 'border-cosmic-700/30'}`}
                            style={getCategoryBackgroundStyle(category.id)}
                          >
                            <Link
                              href={`/claude-code/presentations/${presentation.slug}`}
                              className="relative z-10 block"
                            >
                              {/* Aperçu de la présentation */}
                              <div className="relative">
                                <PresentationPreview
                                  src={`/render/Reveals/${presentation.filename}`}
                                  title={presentation.title}
                                  height={140}
                                  className="w-full"
                                />
                                {/* Badge de date sur l'aperçu */}
                                {presentation.updatedAt && (
                                  <div className="absolute top-2 right-2 flex items-center gap-1 text-xs text-white/90 bg-black/50 backdrop-blur-sm rounded-full px-2 py-1 z-30">
                                    <Calendar className="w-3 h-3" />
                                    {formatDate(presentation.updatedAt)}
                                  </div>
                                )}
                                {/* Badge de niveau */}
                                {presentation.level && (
                                  <div
                                    className={`absolute top-2 left-2 px-2 py-0.5 rounded-full text-xs font-medium z-30 border backdrop-blur-sm ${
                                      presentation.level === 'débutant'
                                        ? 'text-emerald-300 bg-emerald-900/70 border-emerald-500/40'
                                        : presentation.level === 'intermédiaire'
                                        ? 'text-amber-300 bg-amber-900/70 border-amber-500/40'
                                        : 'text-rose-300 bg-rose-900/70 border-rose-500/40'
                                    }`}
                                  >
                                    {presentation.level === 'débutant'
                                      ? 'Débutant'
                                      : presentation.level === 'intermédiaire'
                                      ? 'Intermédiaire'
                                      : 'Avancé'}
                                  </div>
                                )}
                              </div>

                              <CardHeader className="pt-4">
                                <div className="flex items-start gap-3">
                                  <div
                                    className={`w-10 h-10 rounded-lg bg-gradient-to-br ${category.gradient} border ${(category as any).borderColor || 'border-cosmic-700/50'} flex items-center justify-center flex-shrink-0 shadow-md group-hover:shadow-lg transition-shadow`}
                                  >
                                    <Icon
                                      className={`w-5 h-5 text-${category.color}-400 group-hover:scale-110 transition-transform`}
                                    />
                                  </div>
                                  <div className="flex-1 min-w-0">
                                    <CardTitle
                                      className={`line-clamp-2 group-hover:text-${category.color}-400 transition-colors font-bold text-base`}
                                    >
                                      {presentation.title}
                                    </CardTitle>
                                  </div>
                                </div>
                                {presentation.comment && (
                                  <CardDescription className="line-clamp-2 text-sm mt-2">
                                    {presentation.comment}
                                  </CardDescription>
                                )}
                              </CardHeader>

                              <CardContent className="pt-0">
                                {/* Tags */}
                                {presentation.tags && presentation.tags.length > 0 && (
                                  <div className="flex flex-wrap gap-1 mb-3">
                                    {presentation.tags.slice(0, 3).map((tag) => (
                                      <span
                                        key={tag}
                                        className="px-1.5 py-0.5 rounded text-xs text-nebula-400/80 border border-nebula-500/20 bg-nebula-500/5"
                                      >
                                        {tag}
                                      </span>
                                    ))}
                                  </div>
                                )}
                                <div
                                  className={`flex items-center justify-between text-muted-foreground group-hover:text-${category.color}-400 transition-colors font-medium text-sm`}
                                >
                                  <span>Ouvrir la présentation</span>
                                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                                </div>
                              </CardContent>
                            </Link>

                            {/* Effet de brillance au hover */}
                            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000" />
                          </Card>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )
          })}
        </div>
      ) : (
        <section className="text-center py-12 glass-card rounded-xl">
          <BookOpen className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-xl font-semibold mb-2">
            {hasActiveFilters ? 'Aucune présentation ne correspond aux filtres' : 'Aucune présentation disponible'}
          </h3>
          <p className="text-muted-foreground">
            {hasActiveFilters
              ? 'Essayez de modifier ou réinitialiser les filtres.'
              : 'Les présentations seront ajoutées prochainement.'}
          </p>
        </section>
      )}
    </div>
  )
}
