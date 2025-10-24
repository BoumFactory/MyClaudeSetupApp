import { BookOpen, Calendar, ArrowRight, Code2, Cpu, FileCode, Palette, Layers, Package, Settings, FolderOpen } from "lucide-react"
import Link from "next/link"
import path from "path"
import { scanPresentations, readCategoriesConfig, organizePresentationsByCategory } from "@/lib/file-scanner-server"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { formatDate } from "@/lib/utils"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Présentations Claude Code",
  description: "Parcourez nos présentations reveal.js sur les systèmes, agents et skills Claude Code",
}

/**
 * Map des icônes disponibles
 */
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

/**
 * Fonction pour obtenir l'icône depuis son nom
 */
function getIconComponent(iconName: string) {
  return iconMap[iconName] || BookOpen
}

/**
 * Génère un style de fond unique pour chaque catégorie
 */
function getCategoryBackgroundStyle(categoryId: string) {
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

/**
 * Page listant toutes les présentations reveal.js disponibles organisées par catégories
 */
export default async function PresentationsPage() {
  // Scanner les présentations dans le dossier src/public/render/Reveals
  const revealsPath = path.join(process.cwd(), 'src', 'public', 'render', 'Reveals')
  const presentations = await scanPresentations(revealsPath, 'claude-code')

  // Lire la configuration des catégories
  const categoriesPath = path.join(revealsPath, 'categories.json')
  const categoriesConfig = await readCategoriesConfig(categoriesPath)

  // Organiser les présentations par catégories
  const organizedPresentations = organizePresentationsByCategory(presentations, categoriesConfig)

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

      {/* Statistiques */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass-card rounded-xl p-6 text-center">
          <div className="text-3xl font-bold text-cosmic-400">
            {presentations.length}
          </div>
          <div className="text-sm text-muted-foreground mt-1">
            Présentations disponibles
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

      {/* Liste des présentations par catégories et sous-catégories */}
      {organizedPresentations.size > 0 ? (
        <div className="space-y-16">
          {Array.from(organizedPresentations.entries()).map(([category, subcategoriesMap]) => {
            const Icon = getIconComponent(category.icon)

            // Compter le nombre total de présentations dans cette catégorie
            let totalPresentations = 0
            subcategoriesMap.forEach((presentations) => {
              totalPresentations += presentations.length
            })

            return (
              <section key={category.id} className="space-y-8">
                {/* En-tête de catégorie principale */}
                <div className="flex items-start gap-4">
                  <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${category.gradient} border-2 ${(category as any).borderColor} flex items-center justify-center flex-shrink-0 shadow-xl`}>
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
                        {subcategoriesMap.size} sous-catégorie{subcategoriesMap.size > 1 ? 's' : ''}
                      </span>
                      <span className="px-2 py-1 rounded-full bg-cosmic-900/30">
                        {totalPresentations} présentation{totalPresentations > 1 ? 's' : ''}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Sous-catégories */}
                <div className="space-y-10 ml-8">
                  {Array.from(subcategoriesMap.entries()).map(([subcategory, subcategoryPresentations]) => (
                    <div key={subcategory.id} className="space-y-4">
                      {/* En-tête de sous-catégorie */}
                      <div className="border-l-4 pl-4" style={{ borderColor: `rgb(var(--${category.color}-500) / 0.5)` }}>
                        <h3 className={`text-xl font-semibold text-${category.color}-300`}>
                          {subcategory.name}
                        </h3>
                        <p className="text-muted-foreground text-sm mt-1">
                          {subcategory.description}
                        </p>
                        <div className="text-xs text-muted-foreground mt-2">
                          {subcategoryPresentations.length} présentation{subcategoryPresentations.length > 1 ? 's' : ''}
                        </div>
                      </div>

                      {/* Cartes des présentations de cette sous-catégorie */}
                      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        {subcategoryPresentations.map((presentation) => (
                    <Card
                      key={presentation.id}
                      className={`glass-card hover:scale-[1.02] transition-all duration-300 group cursor-pointer relative overflow-hidden border-2 ${(category as any).borderColor || 'border-cosmic-700/30'}`}
                      style={getCategoryBackgroundStyle(category.id)}
                    >
                      <Link href={`/claude-code/presentations/${presentation.slug}`} className="relative z-10 block">
                        <CardHeader>
                          <div className="flex items-start justify-between gap-2">
                            <div
                              className={`w-14 h-14 rounded-xl bg-gradient-to-br ${category.gradient} border-2 ${(category as any).borderColor || 'border-cosmic-700/50'} flex items-center justify-center flex-shrink-0 shadow-lg group-hover:shadow-xl transition-shadow`}
                            >
                              <Icon className={`w-7 h-7 text-${category.color}-400 group-hover:scale-110 transition-transform`} />
                            </div>
                            {presentation.updatedAt && (
                              <div className="flex items-center gap-1 text-xs text-muted-foreground bg-black/20 rounded-full px-2 py-1">
                                <Calendar className="w-3 h-3" />
                                {formatDate(presentation.updatedAt)}
                              </div>
                            )}
                          </div>
                          <CardTitle className={`line-clamp-2 group-hover:text-${category.color}-400 transition-colors font-bold text-lg mt-3`}>
                            {presentation.title}
                          </CardTitle>
                          {presentation.comment && (
                            <CardDescription className="line-clamp-3 text-sm">
                              {presentation.comment}
                            </CardDescription>
                          )}
                        </CardHeader>
                        <CardContent>
                          <div className={`flex items-center justify-between text-muted-foreground group-hover:text-${category.color}-400 transition-colors font-medium text-sm`}>
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
            Aucune présentation disponible
          </h3>
          <p className="text-muted-foreground">
            Les présentations seront ajoutées prochainement.
          </p>
        </section>
      )}

      {/* Vue d'ensemble des catégories */}
      {categoriesConfig.categories.length > 0 && (
        <section className="glass-card rounded-xl p-6 space-y-4">
          <h3 className="font-semibold">Catégories disponibles</h3>
          <div className="grid md:grid-cols-2 gap-3 text-sm">
            {categoriesConfig.categories.map((category) => {
              const Icon = getIconComponent(category.icon)
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
