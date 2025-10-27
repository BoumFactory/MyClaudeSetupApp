import { AlertCircle, CheckCircle2, Hammer, Sparkles } from "lucide-react"

interface Change {
  title: string
  details: string | null
  type: "fix" | "feature" | "improvement" | "wip"
  highlight?: boolean
}

interface ChangelogEntryProps {
  date: string
  title: string
  changes: Change[]
  compact?: boolean // Mode compact pour affichage dans d'autres pages
}

/**
 * Composant pour afficher une entrée de changelog
 * Peut être utilisé en mode compact ou complet
 */
export function ChangelogEntry({ date, title, changes, compact = false }: ChangelogEntryProps) {
  const getTypeIcon = (type: Change["type"]) => {
    switch (type) {
      case "fix":
        return <CheckCircle2 className="w-4 h-4 text-green-400" />
      case "feature":
        return <Sparkles className="w-4 h-4 text-cosmic-400" />
      case "improvement":
        return <Hammer className="w-4 h-4 text-blue-400" />
      case "wip":
        return <AlertCircle className="w-4 h-4 text-amber-400" />
    }
  }

  const getTypeLabel = (type: Change["type"]) => {
    switch (type) {
      case "fix":
        return "Correction"
      case "feature":
        return "Nouveauté"
      case "improvement":
        return "Amélioration"
      case "wip":
        return "En cours"
    }
  }

  const formatDate = (dateStr: string) => {
    const [year, month, day] = dateStr.split('-')
    return `${day}/${month}/${year}`
  }

  return (
    <div className={`glass-card rounded-xl p-6 space-y-4 border-l-4 border-nebula-500 ${compact ? 'text-sm' : ''}`}>
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-baseline gap-3">
          <h3 className={`font-semibold text-nebula-400 ${compact ? 'text-base' : 'text-lg'}`}>
            {title}
          </h3>
          <span className="text-xs text-muted-foreground">
            {formatDate(date)}
          </span>
        </div>

        {/* Changes Grid - 2 colonnes sur grand écran, 1 colonne en mode compact */}
        <div className={`${
          compact
            ? 'space-y-2'
            : 'grid grid-cols-1 lg:grid-cols-2 gap-x-6 gap-y-3'
        } ${compact ? 'text-sm' : 'text-base'}`}>
          {changes.map((change, index) => (
            <div
              key={index}
              className="flex items-start gap-3 group"
            >
              <span className="mt-1 flex-shrink-0">
                {getTypeIcon(change.type)}
              </span>
              <div className="flex-1 min-w-0">
                {change.highlight && (
                  <span className="text-amber-400 font-medium mr-2">
                    ⚡ {getTypeLabel(change.type)} :
                  </span>
                )}
                <span className={change.highlight ? "text-foreground" : "text-muted-foreground"}>
                  {change.title}
                </span>
                {change.details && (
                  <span className="text-xs text-cosmic-400 block mt-1">
                    ({change.details})
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
