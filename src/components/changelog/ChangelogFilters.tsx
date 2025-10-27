"use client"

import { useState } from "react"
import { Filter, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import changelogsData from "@/data/changelogs.json"

interface ChangelogFiltersProps {
  onFilterChange: (categories: string[]) => void
}

/**
 * Composant de filtres pour le changelog
 * Permet de filtrer par catégorie
 */
export function ChangelogFilters({ onFilterChange }: ChangelogFiltersProps) {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])

  // Extraire toutes les catégories uniques
  const allCategories = Array.from(
    new Set(
      changelogsData.changelogs.flatMap((log) => log.categories)
    )
  ).sort()

  const toggleCategory = (category: string) => {
    const newCategories = selectedCategories.includes(category)
      ? selectedCategories.filter((c) => c !== category)
      : [...selectedCategories, category]

    setSelectedCategories(newCategories)
    onFilterChange(newCategories)
  }

  const clearFilters = () => {
    setSelectedCategories([])
    onFilterChange([])
  }

  const getCategoryLabel = (category: string) => {
    const labels: Record<string, string> = {
      downloads: "Téléchargements",
      formations: "Formations",
      general: "Général",
    }
    return labels[category] || category
  }

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      downloads: "border-nebula-500 bg-nebula-900/20 text-nebula-300 hover:bg-nebula-900/40",
      formations: "border-cosmic-500 bg-cosmic-900/20 text-cosmic-300 hover:bg-cosmic-900/40",
      general: "border-green-500 bg-green-900/20 text-green-300 hover:bg-green-900/40",
    }
    return colors[category] || "border-gray-500 bg-gray-900/20 text-gray-300 hover:bg-gray-900/40"
  }

  return (
    <div className="glass-card rounded-xl p-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-cosmic-400" />
          <span className="text-sm font-medium">Filtrer par catégorie :</span>
        </div>

        <div className="flex flex-wrap items-center gap-2 flex-1">
          {allCategories.map((category) => {
            const isSelected = selectedCategories.includes(category)
            return (
              <button
                key={category}
                onClick={() => toggleCategory(category)}
                className={`
                  px-3 py-1.5 rounded-md text-sm font-medium transition-all
                  border-2
                  ${
                    isSelected
                      ? getCategoryColor(category) + " border-opacity-100"
                      : "border-cosmic-700/30 text-muted-foreground hover:border-cosmic-700/50"
                  }
                `}
              >
                {getCategoryLabel(category)}
              </button>
            )
          })}

          {selectedCategories.length > 0 && (
            <Button
              onClick={clearFilters}
              variant="outline"
              size="sm"
              className="gap-2 ml-2"
            >
              <X className="w-3 h-3" />
              Tout afficher
            </Button>
          )}
        </div>

        {selectedCategories.length > 0 && (
          <span className="text-xs text-muted-foreground whitespace-nowrap">
            {selectedCategories.length} filtre{selectedCategories.length > 1 ? "s" : ""} actif{selectedCategories.length > 1 ? "s" : ""}
          </span>
        )}
      </div>
    </div>
  )
}
