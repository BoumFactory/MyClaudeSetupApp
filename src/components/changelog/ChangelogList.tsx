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

interface ChangelogListProps {
  category?: string // Filtrer par catégorie (ex: "downloads", "general")
  limit?: number // Limiter le nombre d'entrées affichées
  compact?: boolean // Mode compact
}

/**
 * Composant pour afficher une liste de changelogs
 * Peut être filtré par catégorie et limité en nombre
 */
export function ChangelogList({ category, limit, compact = false }: ChangelogListProps) {
  // Filtrer les changelogs par catégorie si spécifiée
  let changelogs = changelogsData.changelogs as Changelog[]

  if (category) {
    changelogs = changelogs.filter(changelog =>
      changelog.categories.includes(category)
    )
  }

  // Limiter le nombre d'entrées si spécifié
  if (limit) {
    changelogs = changelogs.slice(0, limit)
  }

  // Trier par date décroissante
  changelogs = [...changelogs].sort((a, b) =>
    new Date(b.date).getTime() - new Date(a.date).getTime()
  )

  if (changelogs.length === 0) {
    return (
      <div className="glass-card rounded-xl p-6 text-center text-muted-foreground">
        Aucun changement à afficher pour le moment.
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {changelogs.map((changelog) => (
        <ChangelogEntry
          key={changelog.id}
          date={changelog.date}
          title={changelog.title}
          changes={changelog.changes}
          compact={compact}
        />
      ))}
    </div>
  )
}
