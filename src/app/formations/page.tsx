import Link from "next/link"
import { BookOpen, Sparkles } from "lucide-react"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Formations",
  description: "Formations complètes sur LaTeX et l'IA pour l'enseignement des mathématiques",
}

/**
 * Page d'accueil des formations
 * Liste toutes les formations disponibles avec liens directs
 */
export default function FormationsPage() {
  const formations = [
    {
      title: "Formation LaTeX",
      description: "Formation complète sur l'utilisation de LaTeX pour l'enseignement des mathématiques. Découvrez comment créer des documents professionnels, des exercices et des cours structurés.",
      href: "/formations/latex",
      icon: BookOpen,
      color: "cosmic"
    },
    {
      title: "Formation IA & LaTeX",
      description: "Découvrez comment utiliser l'intelligence artificielle (Claude Code) pour automatiser et optimiser votre workflow de création de documents LaTeX pour l'enseignement.",
      href: "/formations/ia-latex",
      icon: Sparkles,
      color: "nebula"
    }
  ]

  return (
    <div className="space-y-6">
      <Breadcrumb
        items={[
          { label: "Accueil", href: "/" },
          { label: "Formations", href: "/formations" }
        ]}
      />

      {/* Header */}
      <div className="glass-card rounded-xl p-8 text-center">
        <h1 className="text-4xl font-bold mb-4 glow-text">Formations</h1>
        <p className="text-muted-foreground text-lg max-w-3xl mx-auto">
          Formations complètes pour maîtriser LaTeX et l'IA au service de l'enseignement
          des mathématiques. Documents PDF téléchargeables et consultables en ligne.
        </p>
      </div>

      {/* Liste des formations */}
      <div className="grid md:grid-cols-2 gap-6">
        {formations.map((formation) => {
          const Icon = formation.icon
          return (
            <Link
              key={formation.href}
              href={formation.href}
              className="group glass-card rounded-xl p-6 hover:border-cosmic-500/60 transition-all duration-300 hover:shadow-[0_0_20px_rgba(139,92,246,0.2)]"
            >
              <div className="flex items-start gap-4">
                <div className={`p-3 rounded-lg cosmic-gradient flex-shrink-0`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <div className="flex-1">
                  <h2 className="text-xl font-bold mb-2 group-hover:text-cosmic-300 transition-colors">
                    {formation.title}
                  </h2>
                  <p className="text-muted-foreground text-sm">
                    {formation.description}
                  </p>
                  <div className="mt-4 text-sm text-cosmic-400 font-medium">
                    Consulter la formation →
                  </div>
                </div>
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
