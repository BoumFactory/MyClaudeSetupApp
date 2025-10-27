import Link from "next/link"
import { ArrowRight, History } from "lucide-react"
import { ChangelogList } from "./ChangelogList"

interface ChangelogSectionProps {
  category?: string
  limit?: number
  compact?: boolean
  title?: string
  showViewAll?: boolean
}

/**
 * Section de changelog avec titre et lien vers la page complète
 * Encapsule ChangelogList avec un header et un footer
 */
export function ChangelogSection({
  category,
  limit = 1,
  compact = false,
  title = "Dernières modifications",
  showViewAll = true
}: ChangelogSectionProps) {
  return (
    <div className="space-y-4">
      {/* Header avec titre */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <History className="w-5 h-5 text-nebula-400" />
          <h2 className="text-lg font-semibold text-nebula-400">{title}</h2>
        </div>
        {showViewAll && (
          <Link
            href="/changelog"
            className="text-sm text-cosmic-400 hover:text-cosmic-300 transition-colors flex items-center gap-1 group"
          >
            <span>Voir l'historique complet</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>
        )}
      </div>

      {/* Liste des changelogs */}
      <ChangelogList category={category} limit={limit} compact={compact} />
    </div>
  )
}
