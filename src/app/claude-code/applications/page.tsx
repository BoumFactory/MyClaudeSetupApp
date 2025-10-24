import { FileText, GraduationCap, Wrench, ArrowRight } from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Applications & Logiciels",
  description: "Découvrez les applications et logiciels créés avec Claude Code",
}

/**
 * Page principale des applications - Vue d'ensemble des différentes catégories
 */
export default function ApplicationsOverviewPage() {
  const categories = [
    {
      title: "Applications Éducatives",
      description: "Applications interactives destinées aux élèves pour l'apprentissage des mathématiques",
      icon: GraduationCap,
      href: "/claude-code/applications/educatives",
      features: [
        "Exercices interactifs avec correction automatique",
        "Visualisations graphiques et géométriques",
        "Suivi de progression et adaptation",
        "Interface intuitive pour les élèves"
      ],
      color: "cosmic"
    },
    {
      title: "Logiciels Enseignants",
      description: "Outils de productivité et d'automatisation pour les enseignants de mathématiques",
      icon: Wrench,
      href: "/claude-code/applications/logiciels",
      features: [
        "Génération automatique de documents",
        "Outils de planification et d'organisation",
        "Automatisation de tâches répétitives",
        "Intégration avec les programmes officiels"
      ],
      color: "nebula"
    }
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <FileText className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Applications & Logiciels
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Deux catégories d'outils créés avec Claude Code : applications pour les élèves et logiciels pour les enseignants
        </p>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-6">
        <p className="text-muted-foreground leading-relaxed">
          Cette section présente deux types d'outils distincts créés avec Claude Code. D'une part, les{" "}
          <span className="font-semibold text-cosmic-400">applications éducatives</span> sont conçues pour les élèves,
          offrant des expériences d'apprentissage interactives. D'autre part, les{" "}
          <span className="font-semibold text-nebula-400">logiciels enseignants</span> sont des outils de productivité
          pour automatiser et faciliter le travail quotidien des professeurs.
        </p>
      </section>

      {/* Catégories */}
      <section className="grid md:grid-cols-2 gap-6">
        {categories.map((category) => {
          const Icon = category.icon
          return (
            <Card
              key={category.href}
              className="glass-card hover:scale-105 transition-all duration-300 overflow-hidden"
            >
              <CardHeader>
                <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${category.color}-gradient mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="text-2xl">{category.title}</CardTitle>
                <CardDescription className="text-base">
                  {category.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Features */}
                <ul className="space-y-2">
                  {category.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start gap-2 text-sm text-muted-foreground">
                      <div className={`w-1.5 h-1.5 rounded-full ${category.color === 'cosmic' ? 'bg-cosmic-400' : 'bg-nebula-400'} mt-1.5 flex-shrink-0`} />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>

                {/* CTA */}
                <Button
                  asChild
                  variant={category.color as any}
                  className="w-full"
                  size="lg"
                >
                  <Link href={category.href}>
                    Découvrir
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Link>
                </Button>
              </CardContent>
            </Card>
          )
        })}
      </section>

      {/* Note technique */}
      <section className="glass-card rounded-xl p-6 border-l-4 border-cosmic-400">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg bg-cosmic-900/50 flex items-center justify-center flex-shrink-0">
            <FileText className="w-5 h-5 text-cosmic-400" />
          </div>
          <div className="space-y-2">
            <h3 className="font-semibold text-cosmic-400">Créées avec Claude Code</h3>
            <p className="text-sm text-muted-foreground">
              Toutes les applications et logiciels présentés dans cette section ont été créés avec l'aide de Claude Code.
              Vous pouvez apprendre à créer vos propres outils en consultant les tutoriels et présentations disponibles sur ce site.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
