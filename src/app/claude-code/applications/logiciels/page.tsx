import { FileText, ExternalLink, Wrench, Settings, Sparkles, Github } from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Logiciels Enseignants",
  description: "Outils de productivité créés avec Claude Code pour les enseignants de mathématiques",
}

/**
 * Page des logiciels enseignants créés avec Claude Code
 */
export default function LogicielsEnseignantsPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Wrench className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Logiciels Enseignants
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Outils de productivité et d'automatisation créés avec Claude Code pour les enseignants de mathématiques
        </p>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-6">
        <p className="text-muted-foreground leading-relaxed">
          Ces logiciels sont conçus pour faciliter le travail quotidien des enseignants :
          génération automatique de documents, organisation des cours, automatisation de tâches répétitives,
          et bien plus encore. Chaque outil a été pensé pour gagner du temps et améliorer votre productivité.
        </p>
      </section>

      {/* CTA GitHub */}
      <section className="glass-card rounded-xl p-8 border-l-4 border-nebula-400 space-y-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-nebula-900/50 flex items-center justify-center flex-shrink-0">
            <Github className="w-6 h-6 text-nebula-400" />
          </div>
          <div className="flex-1 space-y-3">
            <h3 className="text-xl font-semibold text-nebula-400">Disponible sur GitHub</h3>
            <p className="text-muted-foreground">
              Tous les logiciels enseignants sont disponibles en open source sur le dépôt GitHub <strong>BFtools</strong>.
              Vous y trouverez des outils pour la préparation de cours, la gestion de classe et l'automatisation
              de tâches pédagogiques.
            </p>
            <Button asChild variant="nebula" size="lg" className="w-full sm:w-auto">
              <a
                href="https://github.com/Romain1099/BFtools.git"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="w-4 h-4 mr-2" />
                Accéder au dépôt BFtools
                <ExternalLink className="w-4 h-4 ml-2" />
              </a>
            </Button>
          </div>
        </div>
      </section>

      {/* Catégories de logiciels */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Catégories de logiciels disponibles</h2>
        <p className="text-muted-foreground">
          Le dépôt BFtools contient plusieurs catégories d'outils pour répondre à vos besoins quotidiens :
        </p>
        <div className="grid md:grid-cols-2 gap-4">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-nebula-400" />
                Outils de préparation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Générateurs de fiches, création automatique de documents, modèles personnalisables
                pour vos cours et évaluations.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-nebula-400" />
                Outils d'automatisation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Scripts pour automatiser les tâches répétitives, conversion de formats,
                traitement par lots de documents.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Wrench className="w-5 h-5 text-nebula-400" />
                Outils de gestion
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Organisation des progressions, planification de séquences, gestion
                des ressources pédagogiques.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-nebula-400" />
                Outils spécialisés
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Intégration avec les programmes officiels, génération d'exercices,
                outils spécifiques aux mathématiques.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
