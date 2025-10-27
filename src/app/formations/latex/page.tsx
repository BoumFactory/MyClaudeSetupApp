import { PdfViewer } from "@/components/formations/PdfViewer"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Formation LaTeX",
  description: "Formation complète sur l'utilisation de LaTeX pour l'enseignement des mathématiques",
}

/**
 * Page de formation LaTeX
 * Affiche le PDF de formation LaTeX avec visualisation et téléchargement
 */
export default function FormationLatexPage() {
  const pdfUrl = "/render/pdf/Formation_LaTeX.pdf"
  const title = "Formation LaTeX"
  const filename = "Formation_LaTeX.pdf"

  return (
    <div className="space-y-6">
      <Breadcrumb
        items={[
          { label: "Accueil", href: "/" },
          { label: "Formations", href: "/formations" },
          { label: "Formation LaTeX", href: "/formations/latex" }
        ]}
      />

      {/* Header */}
      <div className="glass-card rounded-xl p-6">
        <h1 className="text-3xl font-bold mb-2">Formation LaTeX</h1>
        <p className="text-muted-foreground">
          Formation complète sur l'utilisation de LaTeX pour l'enseignement des mathématiques.
          Découvrez comment créer des documents professionnels, des exercices et des cours structurés.
        </p>
      </div>

      {/* Viewer */}
      <PdfViewer
        pdfUrl={pdfUrl}
        title={title}
        filename={filename}
      />
    </div>
  )
}
