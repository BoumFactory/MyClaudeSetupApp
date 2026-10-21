'use client'

import { useRef, useState } from 'react'
import { Play, Maximize2, ExternalLink, Loader2 } from 'lucide-react'

const URL_FORMATION = '/typst-formation/index.html'

/**
 * Bouton « Lancer la formation » : rien n'est téléchargé avant le clic. Le clic monte l'iframe de la Formation
 * (même origine), qui télécharge alors le compilateur Typst avec une barre de progression.
 */
export default function LanceurFormation({ poids }: { poids: string }) {
  const [lancee, setLancee] = useState(false)
  const cadre = useRef<HTMLIFrameElement>(null)

  const pleinEcran = () => {
    const iframe = cadre.current
    if (iframe?.requestFullscreen) iframe.requestFullscreen().catch(() => window.open(URL_FORMATION, '_blank'))
    else window.open(URL_FORMATION, '_blank')
  }

  if (!lancee) {
    return (
      <div className="glass-card rounded-xl border border-cosmic-500/30 bg-cosmic-950/20 p-8 text-center">
        <p className="text-white/70 mb-2">
          Le compilateur Typst tourne dans votre navigateur : rien n&apos;est installé, rien n&apos;est envoyé.
        </p>
        <p className="text-sm text-white/50 mb-6">
          Premier lancement : {poids} à télécharger (une fois, puis le cache du navigateur prend le relais). Prévoir un
          ordinateur et Chrome, Edge ou Firefox récent.
        </p>
        <div className="flex flex-wrap justify-center gap-3">
          <button
            type="button"
            onClick={() => setLancee(true)}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg cosmic-gradient text-base font-medium text-white hover:opacity-90 transition-opacity"
          >
            <Play className="w-5 h-5" />
            Lancer la formation
          </button>
          <a
            href={URL_FORMATION}
            target="_blank"
            rel="noopener"
            className="inline-flex items-center gap-2 px-4 py-3 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-white/70 hover:text-white transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            Ouvrir dans un onglet
          </a>
        </div>
      </div>
    )
  }

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-3 mb-3">
        <p className="text-sm text-white/55 inline-flex items-center gap-2">
          <Loader2 className="w-4 h-4 text-cosmic-400" />
          La formation se charge ci-dessous ; votre progression est gardée dans ce navigateur.
        </p>
        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={pleinEcran}
            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-white/70 hover:text-white transition-colors"
          >
            <Maximize2 className="w-4 h-4" />
            Plein écran
          </button>
          <a
            href={URL_FORMATION}
            target="_blank"
            rel="noopener"
            className="inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-white/5 hover:bg-white/10 border border-white/10 text-sm text-white/70 hover:text-white transition-colors"
          >
            <ExternalLink className="w-4 h-4" />
            Ouvrir dans un onglet
          </a>
        </div>
      </div>
      <iframe
        ref={cadre}
        src={URL_FORMATION}
        title="Formation Typst avec farfadet"
        allow="fullscreen"
        allowFullScreen
        className="w-full rounded-xl border border-white/10 bg-white"
        style={{ height: '85vh', minHeight: 560 }}
      />
    </div>
  )
}
