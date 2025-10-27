import { ChangelogListFiltered } from "@/components/changelog/ChangelogListFiltered"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { History, Info } from "lucide-react"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Changelog",
  description: "Historique des modifications et améliorations de la configuration Claude Code",
}

/**
 * Page du changelog
 * Affiche l'historique complet des modifications
 */
export default function ChangelogPage() {
  return (
    <div className="space-y-6">
      <Breadcrumb
        items={[
          { label: "Accueil", href: "/" },
          { label: "Changelog", href: "/changelog" }
        ]}
      />

      {/* Header */}
      <div className="glass-card rounded-xl p-8 text-center">
        <div className="flex items-center justify-center gap-3 mb-4">
          <History className="w-8 h-8 text-cosmic-400" />
          <h1 className="text-4xl font-bold glow-text">Changelog</h1>
        </div>
        <p className="text-muted-foreground text-lg max-w-3xl mx-auto">
          Historique complet des modifications, nouvelles fonctionnalités et améliorations
          apportées à la configuration Claude Code et au site.
        </p>
      </div>

      {/* Info box */}
      <div className="glass-card rounded-xl p-4 border-l-4 border-cosmic-500">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-muted-foreground">
            <p>
              Cette page recense toutes les modifications importantes apportées à la configuration.
              Les entrées sont organisées par date et incluent les corrections de bugs, les nouvelles
              fonctionnalités, et les améliorations du workflow.
            </p>
          </div>
        </div>
      </div>

      {/* Liste des changelogs avec filtres */}
      <ChangelogListFiltered />

    </div>
  )
}
