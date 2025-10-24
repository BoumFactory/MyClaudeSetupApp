import { notFound } from "next/navigation"
import path from "path"
import { scanPresentations } from "@/lib/file-scanner-server"
import { PresentationViewer } from "@/components/presentations/PresentationViewer"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { PresentationTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"

interface PresentationPageProps {
  params: Promise<{ slug: string }>
}

/**
 * Génération des metadata dynamiques pour le SEO
 */
export async function generateMetadata(
  { params }: PresentationPageProps
): Promise<Metadata> {
  const { slug } = await params
  const revealsPath = path.join(process.cwd(), 'public', 'render', 'Reveals')
  const presentations = await scanPresentations(revealsPath, 'claude-code')
  const presentation = presentations.find((p) => p.slug === slug)

  if (!presentation) {
    return {
      title: "Présentation non trouvée",
    }
  }

  return {
    title: presentation.title,
    description: presentation.description || `Présentation ${presentation.title}`,
  }
}

/**
 * Génération statique des routes pour toutes les présentations
 */
export async function generateStaticParams() {
  const revealsPath = path.join(process.cwd(), 'public', 'render', 'Reveals')
  const presentations = await scanPresentations(revealsPath, 'claude-code')

  return presentations.map((presentation) => ({
    slug: presentation.slug,
  }))
}

/**
 * Page d'affichage d'une présentation reveal.js
 * La navigation se fait via le hash d'URL (#/slide/subslide) géré par le composant client
 */
export default async function PresentationPage({ params }: PresentationPageProps) {
  const { slug } = await params
  const revealsPath = path.join(process.cwd(), 'public', 'render', 'Reveals')
  const presentations = await scanPresentations(revealsPath, 'claude-code')
  const presentation = presentations.find((p) => p.slug === slug)

  if (!presentation) {
    notFound()
  }

  // Construire l'URL de la présentation
  // Les fichiers sont servis depuis le dossier public/ standard de Next.js
  const presentationUrl = `/render/Reveals/${presentation.filename}`

  return (
    <div className="space-y-6">
      {/* Tracker analytics */}
      <PresentationTracker slug={slug} title={presentation.title} />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Présentations", href: "/claude-code/presentations" },
          { label: presentation.title, href: `/claude-code/presentations/${slug}` }
        ]}
      />

      {/* Header */}
      <div className="glass-card rounded-xl p-6">
        <h1 className="text-3xl font-bold mb-2">{presentation.title}</h1>
        {presentation.description && (
          <p className="text-muted-foreground">{presentation.description}</p>
        )}
      </div>

      {/* Viewer */}
      <PresentationViewer
        presentationUrl={presentationUrl}
        title={presentation.title}
      />

      {/* Instructions */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="font-semibold mb-3">Navigation</h3>
        <div className="grid md:grid-cols-3 gap-4 text-sm">
          <div>
            <div className="font-medium mb-1">Clavier</div>
            <ul className="text-muted-foreground space-y-1">
              <li>← → : Slide précédent/suivant</li>
              <li>↑ ↓ : Slide vertical</li>
              <li>Espace : Suivant</li>
              <li>F : Plein écran</li>
              <li>Esc : Vue d'ensemble</li>
            </ul>
          </div>
          <div>
            <div className="font-medium mb-1">Souris/Tactile</div>
            <ul className="text-muted-foreground space-y-1">
              <li>Clic : Avancer</li>
              <li>Glisser : Naviguer</li>
              <li>Pincer : Zoom</li>
            </ul>
          </div>
          <div>
            <div className="font-medium mb-1">Fonctionnalités</div>
            <ul className="text-muted-foreground space-y-1">
              <li>Mode speaker</li>
              <li>Notes privées</li>
              <li>Transitions animées</li>
              <li>Fragments progressifs</li>
            </ul>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-cosmic-800/50">
          <div className="font-medium mb-2 text-cosmic-400">Partager une slide spécifique</div>
          <p className="text-sm text-muted-foreground mb-2">
            Vous pouvez partager un lien direct vers une slide en ajoutant un hash à l'URL :
          </p>
          <ul className="text-sm text-muted-foreground space-y-1 ml-4">
            <li><code className="px-1.5 py-0.5 rounded bg-cosmic-900/50 text-cosmic-300">#/3</code> - Va à la slide 3</li>
            <li><code className="px-1.5 py-0.5 rounded bg-cosmic-900/50 text-cosmic-300">#/3/2</code> - Va à la slide 3, sous-slide 2 (vertical)</li>
          </ul>
          <p className="text-xs text-muted-foreground mt-2">
            Exemple : <code className="px-1.5 py-0.5 rounded bg-cosmic-900/50 text-cosmic-300">/claude-code/presentations/architecture-claude-code-reveals#/2/1</code>
          </p>
        </div>
        <div className="mt-4 pt-4 border-t border-cosmic-800/50">
          <div className="font-medium mb-2 text-nebula-400">Télécharger la présentation</div>
          <p className="text-sm text-muted-foreground mb-2">
            Le bouton de téléchargement génère un fichier ZIP contenant :
          </p>
          <ul className="text-sm text-muted-foreground space-y-1 ml-4">
            <li>✓ Le fichier HTML de la présentation</li>
            <li>✓ Tous les assets (images, fichiers) utilisés</li>
            <li>✓ Prêt à être utilisé hors ligne</li>
          </ul>
          <p className="text-sm text-muted-foreground mt-2">
            <strong>Note :</strong> Les bibliothèques Reveal.js sont chargées depuis des CDN et nécessitent une connexion internet.
          </p>
        </div>
      </div>
    </div>
  )
}
