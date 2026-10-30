import { ListVideo, ExternalLink, Download, Youtube, Wifi } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Tuiles algébriques | Logiciels Enseignants",
  description: "Dix capsules vidéo et dix fiches élève et professeur sur les tuiles algébriques, d'après MathBits.com",
}

// Page statique public/tuiles-algebriques/index.html, produite par
// outils/livraison.py --web (projet tuiles-videos) : vidéos lues depuis YouTube.
// Ouverte en fichier local, elle lit les vidéos via le relais
// public/tuiles-algebriques/lecteur.html (voir next.config.js).
const PAGE = "/tuiles-algebriques/index.html"
const PLAYLIST = "https://www.youtube.com/playlist?list=PLJTH_FcV6OCY"

const LIENS = [
  {
    titre: "Tuiles virtuelles (Mathsbot)",
    texte: "Manipuler et projeter les tuiles en ligne, sans matériel : pratique pour montrer les gestes à la classe.",
    url: "https://mathsbot.com/manipulatives/tiles",
  },
  {
    titre: "Working with Algebra Tiles (MathBits)",
    texte: "La ressource d'origine de la série, en anglais.",
    url: "https://mathbits.com/MathBits/AlgebraTiles/AlgebraTiles/AlgebraTiles.html",
  },
]

const CAPSULES = [
  "Fabriquer ses tuiles",
  "Les pièces et la paire nulle",
  "Facteurs et rectangles",
  "Ajouter des nombres relatifs",
  "Soustraire des nombres relatifs",
  "Multiplier des nombres relatifs",
  "Diviser des nombres relatifs",
  "Calculer une expression pour une valeur de x",
  "Résoudre une équation",
  "La distributivité",
]

export default function TuilesAlgebriquesPage() {
  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      <Breadcrumb
        items={[
          { label: "Applications", href: "/claude-code/applications" },
          { label: "Logiciels Enseignants", href: "/claude-code/applications/logiciels" },
          { label: "Tuiles algébriques", href: "/claude-code/applications/logiciels/tuiles-algebriques" },
        ]}
      />

      <section className="glass-card rounded-xl p-8 border-2 border-amber-500/20 space-y-5">
        <div className="flex items-start gap-4">
          <div className="w-14 h-14 rounded-xl bg-gradient-to-br from-amber-500 to-rose-500 flex items-center justify-center flex-shrink-0">
            <ListVideo className="w-7 h-7 text-white" />
          </div>
          <div className="space-y-2">
            <h1 className="text-3xl font-bold">Tuiles algébriques</h1>
            <p className="text-muted-foreground leading-relaxed">
              Dix capsules vidéo et dix fiches d&apos;activité, d&apos;après MathBits.com : fabriquer ses tuiles,
              opérations sur les nombres relatifs, calcul littéral, équations et distributivité. Chaque fiche
              existe en version élève et professeur, imprimable en A4, avec le gabarit des tuiles à imprimer.
            </p>
            <div className="flex flex-wrap gap-1.5">
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Vidéos</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Fiches élève et professeur</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Collège</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row flex-wrap gap-3">
          <Button asChild variant="nebula">
            <a href={PAGE} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="w-4 h-4 mr-2" />
              Ouvrir les capsules et les fiches
            </a>
          </Button>
          <Button asChild variant="outline">
            <a href={PAGE} download="tuiles-algebriques.html">
              <Download className="w-4 h-4 mr-2" />
              Télécharger la page (HTML, 1,3 Mo)
            </a>
          </Button>
          <Button asChild variant="ghost">
            <a href={PLAYLIST} target="_blank" rel="noopener noreferrer">
              <Youtube className="w-4 h-4 mr-2" />
              Playlist YouTube
            </a>
          </Button>
        </div>

        <p className="text-sm text-muted-foreground flex gap-2">
          <Wifi className="w-4 h-4 flex-shrink-0 mt-0.5 text-amber-400" />
          <span>
            La page téléchargée s&apos;ouvre d&apos;un double-clic, sans repasser par le site : les fiches
            fonctionnent hors ligne, les vidéos demandent une connexion internet.
          </span>
        </p>
      </section>

      <section className="glass-card rounded-xl p-6 space-y-3">
        <h2 className="text-xl font-semibold">Les dix capsules</h2>
        <ol className="space-y-1.5">
          {CAPSULES.map((titre, i) => {
            const n = String(i).padStart(2, "0")
            return (
              <li key={n}>
                <a
                  href={`${PAGE}#${n}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex items-baseline gap-3 text-muted-foreground hover:text-amber-300 transition-colors"
                >
                  <span className="font-mono text-sm text-amber-400">{n}</span>
                  <span className="group-hover:underline">{titre}</span>
                </a>
              </li>
            )
          })}
        </ol>
      </section>

      <section className="glass-card rounded-xl p-6 space-y-3">
        <h2 className="text-xl font-semibold">Pour aller plus loin</h2>
        <ul className="space-y-3">
          {LIENS.map((l) => (
            <li key={l.url}>
              <a
                href={l.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-start gap-3 text-muted-foreground hover:text-amber-300 transition-colors"
              >
                <ExternalLink className="w-4 h-4 mt-1 flex-shrink-0 text-amber-400" />
                <span>
                  <span className="font-medium text-foreground group-hover:underline">{l.titre}</span>
                  <span className="block text-sm">{l.texte}</span>
                </span>
              </a>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}
