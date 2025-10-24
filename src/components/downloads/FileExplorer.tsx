"use client"

import { useState } from "react"
import { Download, CheckSquare, Square, AlertTriangle, Info } from "lucide-react"
import { DownloadableItem } from "@/types"
import { Button } from "@/components/ui/button"
import { FileTreeItem } from "./FileTreeItem"
import {
  toggleAllSelection,
  toggleItemSelection,
  countSelectedFiles,
} from "@/lib/zip-generator"
import { getTotalSize, formatSize } from "@/lib/file-scanner"

interface FileExplorerProps {
  files: DownloadableItem[]
  basePath: string
}

/**
 * Explorateur de fichiers pour téléchargement sélectif
 */
export function FileExplorer({ files: initialFiles, basePath }: FileExplorerProps) {
  const [files, setFiles] = useState<DownloadableItem[]>(initialFiles)
  const [isDownloading, setIsDownloading] = useState(false)
  const [rateLimitAlert, setRateLimitAlert] = useState<{
    show: boolean
    message: string
    remaining?: number
  }>({ show: false, message: "" })

  // Compter les fichiers sélectionnés
  const selectedCount = countSelectedFiles(files)
  const totalSize = getTotalSize(files, true)

  // Basculer la sélection de tous les fichiers
  const handleToggleAll = () => {
    const hasSelected = selectedCount > 0
    setFiles(toggleAllSelection(files, !hasSelected))
  }

  // Basculer la sélection d'un item
  const handleToggleItem = (itemPath: string) => {
    setFiles(toggleItemSelection(files, itemPath))
  }

  // Récupérer les chemins sélectionnés pour analytics
  const getSelectedPaths = (items: DownloadableItem[]): string[] => {
    const paths: string[] = []
    for (const item of items) {
      if (item.isSelected && item.type === 'file') {
        paths.push(item.path)
      }
      if (item.children) {
        paths.push(...getSelectedPaths(item.children))
      }
    }
    return paths
  }

  // Télécharger les fichiers sélectionnés
  const handleDownload = async () => {
    if (selectedCount === 0) {
      alert("Veuillez sélectionner au moins un fichier")
      return
    }

    // Vérifier le rate limiting AVANT de générer le ZIP
    try {
      const checkResponse = await fetch('/api/download/check')
      const checkData = await checkResponse.json()

      if (!checkData.allowed || checkResponse.status === 429) {
        setRateLimitAlert({
          show: true,
          message: checkData.message || "Limite de téléchargements atteinte",
          remaining: 0
        })
        return
      }

      // Afficher les téléchargements restants
      if (checkData.remaining !== undefined) {
        setRateLimitAlert({
          show: true,
          message: checkData.message,
          remaining: checkData.remaining
        })
      }
    } catch (error) {
      console.error('Erreur lors de la vérification du rate limit:', error)
      // Continuer quand même en cas d'erreur de vérification
    }

    console.log('[CLIENT] Préparation du téléchargement')
    console.log('[CLIENT] Nombre de fichiers sélectionnés:', selectedCount)
    console.log('[CLIENT] BasePath:', basePath)

    // Vérifier si les fichiers ont bien isSelected à true
    const checkSelection = (items: DownloadableItem[]): number => {
      let count = 0
      for (const item of items) {
        if (item.isSelected) count++
        if (item.children) count += checkSelection(item.children)
      }
      return count
    }
    console.log('[CLIENT] Items avec isSelected=true:', checkSelection(files))

    setIsDownloading(true)

    try {
      // Générer le ZIP via l'API
      const response = await fetch('/api/download', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          files,
          // basePath supprimé - sera recalculé côté serveur au runtime
        }),
      })

      if (!response.ok) {
        throw new Error('Erreur lors de la génération du ZIP')
      }

      // Télécharger le fichier
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `claude-code-${Date.now()}.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)

      // Enregistrer le téléchargement dans les analytics
      try {
        const selectedPaths = getSelectedPaths(files)
        const recordResponse = await fetch('/api/download/record', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            fileCount: selectedCount,
            totalSize: totalSize,
            selectedPaths: selectedPaths
          }),
        })

        const recordData = await recordResponse.json()

        if (recordResponse.ok && recordData.success) {
          // Mettre à jour le bandeau avec le nombre de téléchargements restants
          setRateLimitAlert({
            show: true,
            message: `Téléchargement réussi ! Il vous reste ${recordData.remaining} téléchargement(s) aujourd'hui.`,
            remaining: recordData.remaining
          })
        }
      } catch (error) {
        console.error('Erreur lors de l\'enregistrement du téléchargement:', error)
        // Ne pas bloquer l'utilisateur si l'enregistrement échoue
      }
    } catch (error) {
      console.error('Erreur lors du téléchargement :', error)
      alert('Une erreur est survenue lors du téléchargement')
    } finally {
      setIsDownloading(false)
    }
  }

  return (
    <div className="space-y-4">
      {/* Bandeau d'alerte rate limiting */}
      {rateLimitAlert.show && (
        <div
          className={`glass-card rounded-xl p-4 flex items-start gap-3 ${
            rateLimitAlert.remaining === 0
              ? "border-2 border-red-500/50 bg-red-500/10"
              : "border-2 border-cosmic-500/50 bg-cosmic-500/10"
          }`}
        >
          {rateLimitAlert.remaining === 0 ? (
            <AlertTriangle className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          ) : (
            <Info className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
          )}
          <div className="flex-1">
            <p className="text-sm font-medium">{rateLimitAlert.message}</p>
            {rateLimitAlert.remaining !== undefined && rateLimitAlert.remaining > 0 && (
              <p className="text-xs text-muted-foreground mt-1">
                Téléchargements restants aujourd'hui : {rateLimitAlert.remaining}
              </p>
            )}
          </div>
          <button
            onClick={() => setRateLimitAlert({ show: false, message: "" })}
            className="text-muted-foreground hover:text-foreground text-sm"
          >
            ✕
          </button>
        </div>
      )}

      {/* Barre d'outils */}
      <div className="glass-card rounded-xl p-4 flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
          <Button
            onClick={handleToggleAll}
            variant="outline"
            size="sm"
            className="gap-2 whitespace-nowrap"
          >
            {selectedCount > 0 ? (
              <CheckSquare className="w-4 h-4" />
            ) : (
              <Square className="w-4 h-4" />
            )}
            <span className="hidden sm:inline">
              {selectedCount > 0 ? "Tout désélectionner" : "Tout sélectionner"}
            </span>
            <span className="sm:hidden">
              {selectedCount > 0 ? "Désélect." : "Sélect."}
            </span>
          </Button>

          <div className="text-sm text-muted-foreground text-center sm:text-left">
            {selectedCount} fichier{selectedCount > 1 ? "s" : ""} sélectionné
            {selectedCount > 1 ? "s" : ""}
            {selectedCount > 0 && (
              <>
                <br className="sm:hidden" />
                <span className="hidden sm:inline"> </span>
                <span className="text-xs sm:text-sm">({formatSize(totalSize)})</span>
              </>
            )}
          </div>
        </div>

        <Button
          onClick={handleDownload}
          disabled={selectedCount === 0 || isDownloading}
          variant="cosmic"
          className="gap-2 w-full sm:w-auto"
        >
          <Download className="w-4 h-4" />
          <span className="hidden sm:inline">
            {isDownloading
              ? "Génération en cours..."
              : "Télécharger la sélection"}
          </span>
          <span className="sm:hidden">
            {isDownloading ? "Génération..." : "Télécharger"}
          </span>
        </Button>
      </div>

      {/* Arbre de fichiers */}
      <div className="glass-card rounded-xl p-6">
        {files.length > 0 ? (
          <div className="space-y-1">
            {files.map((item) => (
              <FileTreeItem
                key={item.path}
                item={item}
                onToggle={handleToggleItem}
                level={0}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-muted-foreground">
            <Download className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p>Aucun fichier disponible</p>
          </div>
        )}
      </div>
    </div>
  )
}
