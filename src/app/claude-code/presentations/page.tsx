import { BookOpen, Layers, Cpu, FileCode, Code2, Palette, Package, Settings, FolderOpen } from "lucide-react"
import path from "path"
import { scanPresentations, readCategoriesConfig, organizePresentationsByCategory } from "@/lib/file-scanner-server"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { PresentationsClient } from "@/components/presentations/PresentationsClient"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Présentations Claude Code",
  description: "Parcourez nos présentations reveal.js sur les systèmes, agents et skills Claude Code",
}

/**
 * Page listant toutes les présentations reveal.js disponibles organisées par catégories
 */
export default async function PresentationsPage() {
  // Scanner les présentations dans le dossier public/render/Reveals
  const revealsPath = path.join(process.cwd(), 'public', 'render', 'Reveals')
  const presentations = await scanPresentations(revealsPath, 'claude-code')

  // Lire la configuration des catégories
  const categoriesPath = path.join(revealsPath, 'categories.json')
  const categoriesConfig = await readCategoriesConfig(categoriesPath)

  // Organiser les présentations par catégories
  const organizedMap = organizePresentationsByCategory(presentations, categoriesConfig)

  // Convertir la Map en tableau sérialisable pour le client
  const organizedData = Array.from(organizedMap.entries()).map(([category, subcategoriesMap]) => ({
    category,
    subcategories: Array.from(subcategoriesMap.entries()).map(([subcategory, subPresentations]) => ({
      subcategory,
      presentations: subPresentations,
    })),
  }))

  return (
    <div className="space-y-8">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Présentations", href: "/claude-code/presentations" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <BookOpen className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Présentations Reveal.js
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Découvrez nos présentations interactives sur l'architecture, les
          systèmes, les agents et les skills utilisés avec Claude Code.
        </p>
      </section>

      {/* Contenu interactif (filtrage côté client) */}
      <PresentationsClient
        presentations={presentations}
        organizedData={organizedData}
        categoriesConfig={categoriesConfig}
        totalCount={presentations.length}
      />

      {/* Vue d'ensemble des catégories */}
      {categoriesConfig.categories.length > 0 && (
        <section className="glass-card rounded-xl p-6 space-y-4">
          <h3 className="font-semibold">Catégories disponibles</h3>
          <div className="grid md:grid-cols-2 gap-3 text-sm">
            {categoriesConfig.categories.map((category) => {
              const iconMap: Record<string, any> = { Layers, Cpu, Code2, Palette, FileCode, Package, Settings, BookOpen, FolderOpen }
              const Icon = iconMap[category.icon] || BookOpen
              return (
                <div key={category.id} className="flex items-start gap-2">
                  <Icon className={`w-5 h-5 text-${category.color}-400 mt-0.5 flex-shrink-0`} />
                  <div>
                    <span className={`font-medium text-${category.color}-400`}>
                      {category.name}
                    </span>
                    <p className="text-muted-foreground text-xs">{category.description}</p>
                  </div>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {/* Info */}
      <section className="glass-card rounded-xl p-6 space-y-3">
        <h3 className="font-semibold">À propos de Reveal.js</h3>
        <p className="text-sm text-muted-foreground">
          Reveal.js est un framework open-source pour créer des présentations
          HTML interactives et réactives. Toutes nos présentations sont
          navigables au clavier (flèches directionnelles) et tactiles, et offrent une expérience
          immersive pour découvrir nos contenus.
        </p>
        <div className="flex items-start gap-2 pt-2">
          <BookOpen className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
          <p className="text-xs text-muted-foreground">
            <span className="font-medium">Navigation :</span> Utilisez les flèches ← → pour naviguer horizontalement
            entre les sections principales, et ↑ ↓ pour explorer les sous-sections verticales.
          </p>
        </div>
      </section>
    </div>
  )
}
