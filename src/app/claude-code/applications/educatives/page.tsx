import { FileText, ExternalLink, Code2, GraduationCap, Play, BookOpen, Download } from "lucide-react"
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
  // Applications Flask
  const applications = [
    {
      id: "second-degre",
      title: "Second Degré - Partie 2",
      description:
        "Application interactive pour l'apprentissage des équations du second degré (signe, tableau de variations, extremum)",
      technologies: ["Python", "Flask", "HTML/CSS", "JavaScript"],
      path: "/download/Applications_educatives/app_second_degre_partie2",
    },
  ]

  // Animations interactives
  const animations = [
    {
      id: "produit-scalaire",
      title: "Produit Scalaire",
      description: "Animation interactive pour visualiser et comprendre le produit scalaire de deux vecteurs",
      technologies: ["HTML", "CSS", "JavaScript"],
      viewPath: "/download/Applications_educatives/animations/produit_scalaire.html",
      downloadPath: "/download/Applications_educatives/animations/produit_scalaire.html",
    },
    {
      id: "trigo",
      title: "Trigonométrie",
      description: "Animation du cercle trigonométrique avec visualisation des fonctions sin, cos et tan",
      technologies: ["HTML", "CSS", "JavaScript"],
      viewPath: "/download/Applications_educatives/animations/animation_trigo.html",
      downloadPath: "/download/Applications_educatives/animations/animation_trigo.html",
    },
  ]

  // Notebooks Jupyter
  const notebooks = [
    {
      id: "python-lycee",
      title: "Python pour le Lycée",
      description: "Notebook Jupyter pour apprendre Python dans le contexte des mathématiques au lycée",
      technologies: ["Python", "Jupyter", "NumPy", "Matplotlib"],
      viewPath: "/download/Applications_educatives/notebooks/python-lycee.html",
      downloadPath: "/download/Applications_educatives/notebooks/python-lycee.html",
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

      {/* Liste des applications Flask */}
      {applications.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold">Applications Flask</h2>
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
      )}

      {/* Animations interactives */}
      {animations.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Play className="w-6 h-6 text-cosmic-400" />
            Animations Interactives
          </h2>
          <p className="text-muted-foreground">
            Animations HTML/CSS/JS autonomes pour visualiser des concepts mathématiques.
            <span className="block mt-1 text-cosmic-400">
              Produites par les agents disponibles dans la configuration Claude Code de ce site.
            </span>
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {animations.map((anim) => (
              <Card key={anim.id} className="glass-card hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center flex-shrink-0 mb-2">
                    <Play className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-lg">{anim.title}</CardTitle>
                  <CardDescription className="text-sm">{anim.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {anim.technologies.map((tech) => (
                      <span
                        key={tech}
                        className="px-2 py-1 text-xs rounded-md bg-green-900/30 border border-green-700 text-green-300"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <Button asChild variant="outline" size="sm" className="flex-1">
                      <a href={anim.viewPath} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="w-4 h-4 mr-1" />
                        Voir
                      </a>
                    </Button>
                    <Button asChild variant="ghost" size="sm">
                      <a href={anim.downloadPath} download>
                        <Download className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      )}

      {/* Notebooks Jupyter */}
      {notebooks.length > 0 && (
        <section className="space-y-4">
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-orange-400" />
            Notebooks Jupyter
          </h2>
          <p className="text-muted-foreground">
            Notebooks interactifs pour apprendre Python et les mathématiques.
            <span className="block mt-1 text-orange-400">
              Produits par les agents disponibles dans la configuration Claude Code de ce site.
            </span>
          </p>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {notebooks.map((nb) => (
              <Card key={nb.id} className="glass-card hover:scale-105 transition-all duration-300">
                <CardHeader>
                  <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-orange-500 to-amber-600 flex items-center justify-center flex-shrink-0 mb-2">
                    <BookOpen className="w-6 h-6 text-white" />
                  </div>
                  <CardTitle className="text-lg">{nb.title}</CardTitle>
                  <CardDescription className="text-sm">{nb.description}</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-wrap gap-2">
                    {nb.technologies.map((tech) => (
                      <span
                        key={tech}
                        className="px-2 py-1 text-xs rounded-md bg-orange-900/30 border border-orange-700 text-orange-300"
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <Button asChild variant="outline" size="sm" className="flex-1">
                      <a href={nb.viewPath} target="_blank" rel="noopener noreferrer">
                        <ExternalLink className="w-4 h-4 mr-1" />
                        Voir
                      </a>
                    </Button>
                    <Button asChild variant="ghost" size="sm">
                      <a href={nb.downloadPath} download>
                        <Download className="w-4 h-4" />
                      </a>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
