import { Video, Youtube, ExternalLink } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Vidéos Claude Code | Chaîne YouTube",
  description: "Découvrez ma chaîne YouTube où j'explique mon fonctionnement avec Claude Code et partage des exemples d'utilisation concrets.",
}

const claudeCodeVideosUrl = "https://www.youtube.com/playlist?list=PLdhRy3n11XGD3kVAQGtgL9UhmvqBqaeh3"

/**
 * Page redirigeant vers la chaîne YouTube
 */
export default function VideosPage() {
  return (
    <div className="space-y-12">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Vidéos", href: "/claude-code/videos" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Youtube className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Vidéos YouTube
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Découvrez ma chaîne YouTube où je partage mon expérience avec Claude Code
        </p>
      </section>

      {/* Contenu principal */}
      <section className="glass-card rounded-xl p-8 max-w-3xl mx-auto space-y-6">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
            <Video className="w-6 h-6 text-white" />
          </div>
          <div className="space-y-4">
            <h2 className="text-2xl font-bold">Contenu de la chaîne</h2>
            <p className="text-muted-foreground">
              Sur ma chaîne YouTube, je partage :
            </p>
            <ul className="space-y-3 text-muted-foreground">
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-cosmic-400 mt-2 flex-shrink-0"></span>
                <span>
                  <strong className="text-foreground">Mon fonctionnement avec Claude Code :</strong> Comment j'utilise cet outil au quotidien pour l'enseignement des mathématiques
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-cosmic-400 mt-2 flex-shrink-0"></span>
                <span>
                  <strong className="text-foreground">Exemples d'utilisation concrets :</strong> Démonstrations pratiques de création de ressources pédagogiques
                </span>
              </li>
              <li className="flex items-start gap-3">
                <span className="w-1.5 h-1.5 rounded-full bg-cosmic-400 mt-2 flex-shrink-0"></span>
                <span>
                  <strong className="text-foreground">Astuces et workflows :</strong> Partage de mes techniques et méthodes de travail
                </span>
              </li>
            </ul>
          </div>
        </div>

        {/* CTA vers YouTube */}
        <div className="pt-4">
          <Button asChild variant="cosmic" size="lg" className="w-full gap-2">
            <a
              href={claudeCodeVideosUrl}
              target="_blank"
              rel="noopener noreferrer"
            >
              <Youtube className="w-5 h-5" />
              Voir la playlist YouTube
              <ExternalLink className="w-4 h-4" />
            </a>
          </Button>
          <p className="text-xs text-muted-foreground text-center mt-2">
            Ouvrira dans un nouvel onglet
          </p>
        </div>
      </section>

      {/* Note complémentaire */}
      <section className="glass-card rounded-xl p-6 max-w-3xl mx-auto border-cosmic-700/30">
        <p className="text-sm text-muted-foreground text-center">
          💡 <strong className="text-foreground">Astuce :</strong> N'hésitez pas à consulter les{" "}
          <Link href="/claude-code/tutorials" className="text-cosmic-400 hover:underline" prefetch={false}>
            tutoriels écrits
          </Link>{" "}
          et les{" "}
          <Link href="/claude-code/presentations" className="text-nebula-400 hover:underline" prefetch={false}>
            présentations interactives
          </Link>{" "}
        </p>
      </section>
    </div>
  )
}
