"use client"

import { useState } from "react"
import { ChangelogFilters } from "./ChangelogFilters"
import { ChangelogEntry } from "./ChangelogEntry"
import changelogsData from "@/data/changelogs.json"

interface Change {
  title: string
  details: string | null
  type: "fix" | "feature" | "improvement" | "wip"
  highlight?: boolean
}

interface Changelog {
  id: string
  date: string
  title: string
  categories: string[]
  changes: Change[]
}

/**
 * Liste de changelogs avec filtres interactifs
 * Composant client qui gère l'état des filtres
 */
export function ChangelogListFiltered() {
  const [selectedCategories, setSelectedCategories] = useState<string[]>([])

  // Filtrer les changelogs
  let changelogs = changelogsData.changelogs as Changelog[]

  if (selectedCategories.length > 0) {
    changelogs = changelogs.filter((changelog) =>
      changelog.categories.some((cat) => selectedCategories.includes(cat))
    )
  }

  // Trier par date décroissante
  changelogs = [...changelogs].sort(
    (a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
  )

  return (
    <div className="space-y-6">
      {/* Filtres */}
      <ChangelogFilters onFilterChange={setSelectedCategories} />

      {/* Liste des changelogs */}
      {changelogs.length === 0 ? (
        <div className="glass-card rounded-xl p-6 text-center text-muted-foreground">
          Aucun changement ne correspond aux filtres sélectionnés.
        </div>
      ) : (
        <div className="space-y-6">
          {changelogs.map((changelog) => (
            <ChangelogEntry
              key={changelog.id}
              date={changelog.date}
              title={changelog.title}
              changes={changelog.changes}
              compact={false}
            />
          ))}
        </div>
      )}
    </div>
  )
}
