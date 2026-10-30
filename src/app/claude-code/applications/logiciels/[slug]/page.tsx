import { notFound } from "next/navigation"
import Link from "next/link"
import { FileText, Puzzle, BarChart3, ExternalLink, Download } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AddToCartButton } from "@/components/cart/AddToCartButton"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { APPLICATIONS_BUREAU } from "@/data/applications-bureau"
import { OUTILS_HTML, type OutilHtml } from "@/data/outils-html"
import { ApplicationBureauCard, AvertissementExecutableNonSigne } from "@/components/logiciels/ApplicationBureauCard"
import type { Metadata } from "next"

/**
 * Page d'un logiciel enseignant : application de bureau (src/data/applications-bureau.ts)
 * ou outil web autonome (src/data/outils-html.ts). QF-Studio et les tuiles
 * algébriques ont leur propre dossier, prioritaire sur cette route.
 */
interface PageProps {
  params: Promise<{ slug: string }>
}

export const dynamicParams = false

export function generateStaticParams() {
  return [...APPLICATIONS_BUREAU, ...OUTILS_HTML].map((x) => ({ slug: x.slug }))
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { slug } = await params
  const app = APPLICATIONS_BUREAU.find((a) => a.slug === slug)
  const outil = OUTILS_HTML.find((o) => o.slug === slug)
  const nom = app?.nom ?? outil?.nom
  if (!nom) return {}
  return {
    title: `${nom} | Logiciels Enseignants`,
    description: app?.accroche ?? outil?.description,
  }
}

// Classes Tailwind écrites en entier (pas de concaténation) pour que la purge les garde.
const STYLES_OUTIL = {
  violet: { bordure: "border-violet-500/20", pastille: "bg-gradient-to-br from-violet-500 to-purple-600", badge: "bg-violet-500/15 text-violet-400", lien: "text-violet-400", icone: FileText },
  emerald: { bordure: "border-emerald-500/20", pastille: "bg-gradient-to-br from-emerald-500 to-teal-600", badge: "bg-emerald-500/15 text-emerald-400", lien: "text-emerald-400", icone: Puzzle },
  amber: { bordure: "border-amber-500/20", pastille: "bg-gradient-to-br from-amber-500 to-orange-600", badge: "bg-amber-500/15 text-amber-400", lien: "text-amber-400", icone: BarChart3 },
} as const

function CarteOutilHtml({ outil }: { outil: OutilHtml }) {
  const s = STYLES_OUTIL[outil.couleur]
  const Icone = s.icone
  return (
    <Card className={`glass-card border-2 ${s.bordure}`}>
      <CardHeader>
        <div className="flex items-start justify-between mb-2">
          <div className={`w-11 h-11 rounded-lg ${s.pastille} flex items-center justify-center`}>
            <Icone className="w-5 h-5 text-white" />
          </div>
          <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>{outil.badge}</span>
        </div>
        <CardTitle className="text-2xl">{outil.nom}</CardTitle>
        <CardDescription className="text-base">{outil.description}</CardDescription>
      </CardHeader>
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-1.5">
          {outil.tags.map((t) => (
            <span key={t} className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">{t}</span>
          ))}
        </div>
        <p className="text-sm text-muted-foreground">
          Application web autonome : utilisez-la directement en ligne, ou téléchargez le fichier HTML
          et ouvrez-le d&apos;un double-clic, sans installation.
        </p>
        <div className="flex flex-col sm:flex-row flex-wrap gap-3">
          <Button asChild variant="nebula">
            <a href={outil.fichier} target="_blank" rel="noopener noreferrer">
              <ExternalLink className="w-4 h-4 mr-2" />
              Ouvrir dans le navigateur
            </a>
          </Button>
          <Button asChild variant="outline">
            <a href={outil.fichier} download>
              <Download className="w-4 h-4 mr-2" />
              Télécharger (HTML)
            </a>
          </Button>
          <AddToCartButton item={outil.item} />
        </div>
        {outil.ficheTechnique && (
          <p className="text-xs text-muted-foreground">
            Inclut une <Link href={outil.ficheTechnique} className={`${s.lien} hover:underline`}>fiche technique PDF</Link>
          </p>
        )}
      </CardContent>
    </Card>
  )
}

export default async function LogicielPage({ params }: PageProps) {
  const { slug } = await params
  const app = APPLICATIONS_BUREAU.find((a) => a.slug === slug)
  const outil = OUTILS_HTML.find((o) => o.slug === slug)
  if (!app && !outil) notFound()
  const nom = (app?.nom ?? outil?.nom)!

  return (
    <div className="space-y-8 max-w-3xl mx-auto">
      <Breadcrumb
        items={[
          { label: "Applications", href: "/claude-code/applications" },
          { label: "Logiciels Enseignants", href: "/claude-code/applications/logiciels" },
          { label: nom, href: `/claude-code/applications/logiciels/${slug}` },
        ]}
      />
      {app && (
        <>
          <ApplicationBureauCard app={app} />
          <AvertissementExecutableNonSigne />
        </>
      )}
      {outil && <CarteOutilHtml outil={outil} />}
    </div>
  )
}
