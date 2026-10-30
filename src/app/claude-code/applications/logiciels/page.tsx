import { ExternalLink, Wrench, Github, Zap, ArrowRight, ListVideo, Users, Timer, BookOpenCheck, FileText, Puzzle, BarChart3, type LucideIcon } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { AddToCartButton } from "@/components/cart/AddToCartButton"
import type { Metadata } from "next"
import { APPLICATIONS_BUREAU } from "@/data/applications-bureau"
import { OUTILS_HTML } from "@/data/outils-html"

export const metadata: Metadata = {
  title: "Logiciels Enseignants",
  description: "Outils de productivité créés avec Claude Code pour les enseignants de mathématiques",
}

/**
 * Sommaire des logiciels enseignants : une carte par logiciel, chacune mène à
 * sa page (logiciels/<slug>). Les mêmes pages sont listées dans le menu
 * Applications (src/components/layout/MainNav.tsx) : garder les deux à jour.
 */

const BASE = "/claude-code/applications/logiciels"

interface Entree {
  slug: string
  nom: string
  accroche: string
  badge: string
  icone: LucideIcon
  pastille: string
}

const ICONES_BUREAU: Record<string, LucideIcon> = {
  "exos-lombards": BookOpenCheck,
  "gestion-classes": Users,
  "activite-timer": Timer,
}
const PASTILLES_BUREAU = {
  sky: "bg-gradient-to-br from-sky-500 to-blue-600",
  rose: "bg-gradient-to-br from-rose-500 to-pink-600",
  emerald: "bg-gradient-to-br from-emerald-500 to-teal-600",
} as const
const OUTILS = {
  violet: { icone: FileText, pastille: "bg-gradient-to-br from-violet-500 to-purple-600" },
  emerald: { icone: Puzzle, pastille: "bg-gradient-to-br from-emerald-500 to-teal-600" },
  amber: { icone: BarChart3, pastille: "bg-gradient-to-br from-amber-500 to-orange-600" },
} as const

// Toutes les entrées, par slug ; les rubriques ci-dessous les rangent par usage.
// Pastille : « Windows » = application à télécharger, « Navigateur » = fichier HTML.
const ENTREES: Record<string, Entree> = Object.fromEntries(
  [
    {
      slug: "qf-studio",
      nom: "QF-Studio",
      accroche: "Créer et projeter des questions flash en classe. Mise à jour automatique.",
      badge: "Windows",
      icone: Zap,
      pastille: "bg-gradient-to-br from-indigo-500 to-violet-600",
    },
    ...APPLICATIONS_BUREAU.map((a) => ({
      slug: a.slug,
      nom: a.nom,
      accroche: a.accroche,
      badge: "Windows",
      icone: ICONES_BUREAU[a.slug] ?? Wrench,
      pastille: PASTILLES_BUREAU[a.couleur],
    })),
    ...OUTILS_HTML.map((o) => ({
      slug: o.slug,
      nom: o.nom,
      accroche: o.description,
      badge: "Navigateur",
      icone: OUTILS[o.couleur].icone,
      pastille: OUTILS[o.couleur].pastille,
    })),
    {
      slug: "tuiles-algebriques",
      nom: "Tuiles algébriques",
      accroche: "Dix capsules et dix fiches : nombres relatifs, calcul littéral, équations et distributivité.",
      badge: "Vidéos et fiches",
      icone: ListVideo,
      pastille: "bg-gradient-to-br from-amber-500 to-rose-500",
    },
  ].map((e) => [e.slug, e])
)

const RUBRIQUES: { titre: string; texte: string; slugs: string[] }[] = [
  {
    titre: "Créer des documents",
    texte: "Questions flash, fiches d'exercices, devoirs, documents Word et activités Moodle.",
    slugs: ["qf-studio", "exos-lombards", "loiseau-generator", "stats-datagouv", "h5p-moodle"],
  },
  {
    titre: "Gérer la classe",
    texte: "Plan de classe, rôles des élèves et rythme de la séance.",
    slugs: ["gestion-classes", "activite-timer"],
  },
  {
    titre: "Ressources prêtes à l'emploi",
    texte: "Séries à projeter : capsules vidéo courtes et fiches élève et professeur, imprimables en A4.",
    slugs: ["tuiles-algebriques"],
  },
]

function CarteEntree({ e }: { e: Entree }) {
  const Icone = e.icone
  return (
    <Link
      href={`${BASE}/${e.slug}`}
      className="group glass-card rounded-xl p-5 border-2 border-white/5 hover:border-nebula-400/40 transition-all duration-300 flex flex-col gap-3"
    >
      <div className="flex items-start justify-between">
        <div className={`w-11 h-11 rounded-lg ${e.pastille} flex items-center justify-center`}>
          <Icone className="w-5 h-5 text-white" />
        </div>
        <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">{e.badge}</span>
      </div>
      <p className="text-lg font-semibold group-hover:text-nebula-300 transition-colors">{e.nom}</p>
      <p className="text-sm text-muted-foreground line-clamp-3 flex-1">{e.accroche}</p>
      <span className="text-sm text-nebula-400 inline-flex items-center gap-1">
        Voir la page
        <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
      </span>
    </Link>
  )
}

export default function LogicielsEnseignantsPage() {
  return (
    <div className="space-y-10">
      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Wrench className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Logiciels Enseignants
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Outils de productivité et ressources pour la classe, créés avec Claude Code pour les enseignants de mathématiques
        </p>
      </section>

      {RUBRIQUES.map((r) => (
        <section key={r.titre} className="space-y-4">
          <div>
            <h2 className="text-2xl font-bold">{r.titre}</h2>
            <p className="text-muted-foreground mt-1">{r.texte}</p>
          </div>
          <div className="grid sm:grid-cols-2 xl:grid-cols-3 gap-5">
            {r.slugs.map((slug) => (
              <CarteEntree key={slug} e={ENTREES[slug]} />
            ))}
          </div>
        </section>
      ))}

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
              Vous y trouverez des outils pour la préparation de cours, la gestion de classe et l&apos;automatisation
              de tâches pédagogiques.
            </p>
            <div className="flex flex-wrap gap-3">
              <AddToCartButton
                item={{ id: 'bftools-repo', name: 'BFtools (GitHub)', type: 'logiciel', path: 'logiciels-enseignant', description: 'Depot GitHub BFtools - outils enseignants' }}
                variant="nebula"
                className="w-full sm:w-auto"
              />
              <Button asChild variant="ghost" size="sm" className="w-full sm:w-auto">
                <a
                  href="https://github.com/Romain1099/BFtools.git"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Github className="w-4 h-4 mr-1" />
                  <span className="text-xs">Voir sur GitHub</span>
                  <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
