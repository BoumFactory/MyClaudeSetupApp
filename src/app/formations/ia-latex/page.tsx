import { PdfViewer } from "@/components/formations/PdfViewer"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Formation IA & LaTeX",
  description: "Formation sur l'utilisation de l'intelligence artificielle (Claude Code) pour automatiser la création de documents LaTeX",
}

/**
 * Page de formation IA & LaTeX
 * Affiche le PDF de formation IA & LaTeX avec visualisation et téléchargement
 */
export default function FormationIALatexPage() {
  const pdfUrl = "/render/pdf/Formation_IA_LaTeX.pdf"
  const title = "Formation IA & LaTeX"
  const filename = "Formation_IA_LaTeX.pdf"

  return (
    <div className="space-y-6">
      <Breadcrumb
        items={[
          { label: "Accueil", href: "/" },
          { label: "Formations", href: "/formations" },
          { label: "Formation IA & LaTeX", href: "/formations/ia-latex" }
        ]}
      />

      {/* Header */}
      <div className="glass-card rounded-xl p-6">
        <h1 className="text-3xl font-bold mb-2">Formation IA & LaTeX</h1>
        <p className="text-muted-foreground">
          Découvrez comment utiliser l'intelligence artificielle (Claude Code) pour automatiser
          et optimiser votre workflow de création de documents LaTeX pour l'enseignement.
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
