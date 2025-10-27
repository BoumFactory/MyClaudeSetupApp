"use client"

import { Maximize2, Download } from "lucide-react"
import { Button } from "@/components/ui/button"

interface PdfViewerProps {
  pdfUrl: string // URL du fichier PDF
  title: string
  filename: string // Nom du fichier pour le téléchargement
}

/**
 * Viewer pour les documents PDF
 * Affiche le PDF dans un iframe et permet le téléchargement
 */
export function PdfViewer({ pdfUrl, title, filename }: PdfViewerProps) {
  const handleDownload = () => {
    const link = document.createElement('a')
    link.href = pdfUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }

  const toggleFullscreen = () => {
    const iframeContainer = document.getElementById('pdf-container')
    if (iframeContainer) {
      if (document.fullscreenElement) {
        document.exitFullscreen()
      } else {
        iframeContainer.requestFullscreen()
      }
    }
  }

  return (
    <div className="space-y-4">
      {/* Contrôles principaux */}
      <div className="glass-card rounded-xl p-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="text-sm text-muted-foreground">
            Consultez et téléchargez le document PDF
          </div>
          <div className="flex gap-2 w-full sm:w-auto">
            <Button
              onClick={toggleFullscreen}
              variant="outline"
              size="sm"
              className="gap-2 flex-1 sm:flex-initial"
            >
              <Maximize2 className="w-4 h-4" />
              Plein écran
            </Button>
            <Button
              onClick={handleDownload}
              variant="outline"
              size="sm"
              className="gap-2 flex-1 sm:flex-initial"
              title={`Télécharger ${filename}`}
            >
              <Download className="w-4 h-4" />
              Télécharger
            </Button>
          </div>
        </div>
      </div>

      {/* Iframe PDF */}
      <div
        id="pdf-container"
        className="relative w-full overflow-hidden rounded-xl border border-cosmic-800/50 bg-black/20"
      >
        <iframe
          src={pdfUrl}
          title={title}
          className="w-full"
          style={{
            border: 'none',
            minHeight: '800px',
            height: '80vh',
          }}
        />
      </div>

      {/* Instructions */}
      <div className="glass-card rounded-xl p-6">
        <h3 className="font-semibold mb-3">Navigation dans le PDF</h3>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <div className="font-medium mb-1">Contrôles</div>
            <ul className="text-muted-foreground space-y-1">
              <li>• Molette : Faire défiler les pages</li>
              <li>• Ctrl + Molette : Zoomer/Dézoomer</li>
              <li>• Utiliser les contrôles natifs du lecteur PDF</li>
            </ul>
          </div>
          <div>
            <div className="font-medium mb-1">Options</div>
            <ul className="text-muted-foreground space-y-1">
              <li>• Mode plein écran disponible</li>
              <li>• Téléchargement direct du PDF</li>
              <li>• Navigation native du lecteur PDF</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
