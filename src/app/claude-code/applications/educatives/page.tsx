import { FileText, ExternalLink, Code2, GraduationCap } from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Applications Éducatives",
  description: "Découvrez les applications éducatives créées avec Claude Code pour l'enseignement",
}

/**
 * Page des applications éducatives créées avec Claude Code
 */
export default function ApplicationsEducativesPage() {
  // Exemple d'application - À remplacer par un scan automatique
  const applications = [
    {
      id: "second-degre",
      title: "Second Degré - Partie 2",
      description:
        "Application interactive pour l'apprentissage des équations du second degré (signe, tableau de variations, extremum)",
      technologies: ["Python", "Flask", "HTML/CSS", "JavaScript"],
      path: "/download/ClaudeCode/Applications_educatives/app_second_degre_partie2",
    },
  ]

  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <GraduationCap className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Applications Éducatives
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Applications interactives créées avec Claude Code pour l'apprentissage
          des mathématiques
        </p>
      </section>

      {/* Disclaimer */}
      <section className="glass-card rounded-xl p-6 border-l-4 border-cosmic-400">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg bg-cosmic-900/50 flex items-center justify-center flex-shrink-0">
            <FileText className="w-5 h-5 text-cosmic-400" />
          </div>
          <div className="space-y-2">
            <h3 className="font-semibold text-cosmic-400">Note importante</h3>
            <p className="text-sm text-muted-foreground">
              Cette section est en cours de développement. La fonctionnalité permettant de créer
              des applications éducatives avec Claude Code est sortie récemment.
              De nouvelles applications seront progressivement ajoutées à l'avenir.
            </p>
          </div>
        </div>
      </section>

      {/* Liste des applications */}
      {applications.length > 0 ? (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Applications disponibles</h2>
          <div className="grid md:grid-cols-2 gap-6">
            {applications.map((app) => (
              <Card key={app.id} className="glass-card hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <div className="flex items-start justify-between gap-2">
                    <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center flex-shrink-0">
                      <Code2 className="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <CardTitle>{app.title}</CardTitle>
                  <CardDescription>{app.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Technologies */}
                  <div className="flex flex-wrap gap-2">
                    {app.technologies.map((tech) => (
                      <span
                        key={tech}
                        className="px-2 py-1 text-xs rounded-md bg-cosmic-900/50 border border-cosmic-700 text-cosmic-300"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button asChild variant="cosmic" className="flex-1">
                      <Link href="/claude-code/downloads">
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Télécharger
                      </Link>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      ) : (
        <section className="text-center py-12 glass-card rounded-xl">
          <FileText className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-xl font-semibold mb-2">
            Applications à venir
          </h3>
          <p className="text-muted-foreground">
            De nouvelles applications seront ajoutées prochainement
          </p>
        </section>
      )}
    </div>
  )
}
