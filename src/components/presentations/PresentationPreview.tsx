"use client"

import { useState } from "react"
import { Play, Eye } from "lucide-react"

interface PresentationPreviewProps {
  /** Chemin vers le fichier HTML de la présentation */
  src: string
  /** Titre de la présentation (pour l'accessibilité) */
  title: string
  /** Classe CSS additionnelle */
  className?: string
  /** Hauteur de l'aperçu (défaut: 120px) */
  height?: number
}

/**
 * Composant affichant un aperçu miniature d'une présentation reveal.js
 * L'iframe est non-interactive et sert uniquement de preview visuel
 */
export function PresentationPreview({
  src,
  title,
  className = "",
  height = 120
}: PresentationPreviewProps) {
  const [isLoaded, setIsLoaded] = useState(false)
  const [hasError, setHasError] = useState(false)

  // Calcul du ratio pour l'iframe (16:9)
  const iframeWidth = Math.round(height * (16 / 9))
  const scale = height / 540 // 540px est une hauteur typique pour reveal.js

  return (
    <div
      className={`relative overflow-hidden rounded-lg bg-slate-900/50 ${className}`}
      style={{ height: `${height}px` }}
    >
      {/* Loader */}
      {!isLoaded && !hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-10">
          <div className="flex flex-col items-center gap-2">
            <div className="w-6 h-6 border-2 border-cosmic-400 border-t-transparent rounded-full animate-spin" />
            <span className="text-xs text-muted-foreground">Chargement...</span>
          </div>
        </div>
      )}

      {/* Fallback en cas d'erreur */}
      {hasError && (
        <div className="absolute inset-0 flex items-center justify-center bg-slate-900/80 z-10">
          <div className="flex flex-col items-center gap-2 text-muted-foreground">
            <Eye className="w-8 h-8 opacity-50" />
            <span className="text-xs">Aperçu non disponible</span>
          </div>
        </div>
      )}

      {/* Container de l'iframe avec scaling */}
      <div
        className="absolute top-0 left-1/2 origin-top"
        style={{
          width: `${960}px`, // Largeur standard reveal.js
          height: `${540}px`, // Hauteur standard reveal.js
          transform: `translateX(-50%) scale(${scale})`,
        }}
      >
        <iframe
          src={src}
          title={`Aperçu: ${title}`}
          className="w-full h-full border-0"
          style={{
            pointerEvents: "none", // Désactive toute interaction
          }}
          loading="lazy"
          onLoad={() => setIsLoaded(true)}
          onError={() => setHasError(true)}
          sandbox="allow-same-origin allow-scripts"
        />
      </div>

      {/* Overlay avec icône play au hover */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-end justify-center pb-2 z-20">
        <div className="flex items-center gap-1 text-white/90 text-xs font-medium">
          <Play className="w-3 h-3" />
          <span>Voir</span>
        </div>
      </div>

      {/* Bordure subtile */}
      <div className="absolute inset-0 rounded-lg border border-white/10 pointer-events-none z-30" />
    </div>
  )
}
