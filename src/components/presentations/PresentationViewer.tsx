"use client"

import { useEffect, useRef, useState } from "react"
import { Maximize2, Navigation, Download } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

interface PresentationViewerProps {
  presentationUrl: string // URL du fichier HTML de la présentation
  title: string
  initialSlide?: string
}

/**
 * Viewer pour les présentations reveal.js
 * Charge la présentation dans un iframe et permet la navigation
 * Utilise le hash natif de Reveal.js pour la navigation (#/slide/subslide)
 */
export function PresentationViewer({ presentationUrl, title, initialSlide }: PresentationViewerProps) {
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const [currentSlide, setCurrentSlide] = useState(initialSlide || "0/0")
  const [manualSlideInput, setManualSlideInput] = useState("")
  const [isRevealReady, setIsRevealReady] = useState(false)
  const setupAttempts = useRef(0)
  const maxSetupAttempts = 50 // 50 * 100ms = 5 secondes max

  // Fonction pour mettre à jour l'URL sans recharger la page
  // Utilise le hash natif de Reveal.js via l'API History
  const updateURL = (slideIndex: string) => {
    if (typeof window === 'undefined') return

    const newHash = `#/${slideIndex}`
    // Utiliser l'API History native au lieu de Next.js router pour mieux gérer les hash
    if (window.location.hash !== newHash) {
      window.history.replaceState(null, '', newHash)
    }
  }

  // Fonction pour naviguer vers une slide spécifique
  const navigateToSlide = (slideIndex: string) => {
    const iframe = iframeRef.current
    if (!iframe) return

    const iframeWindow = iframe.contentWindow
    if (iframeWindow && (iframeWindow as any).Reveal) {
      const Reveal = (iframeWindow as any).Reveal
      const slideParts = slideIndex.split('/')
      const h = parseInt(slideParts[0], 10) || 0
      const v = slideParts[1] ? parseInt(slideParts[1], 10) : 0

      // Vérifier que Reveal est bien initialisé et utiliser la bonne méthode
      if (typeof Reveal.slide === 'function') {
        Reveal.slide(h, v)
      } else if (typeof Reveal.navigateTo === 'function') {
        Reveal.navigateTo(h, v)
      } else if (Reveal.configure && typeof Reveal.sync === 'function') {
        // Forcer la navigation via l'état interne
        Reveal.setState({ indexh: h, indexv: v })
      }

      setCurrentSlide(`${h}/${v}`)
      updateURL(`${h}/${v}`)
      console.log(`[Reveal] Navigation manuelle vers ${h}/${v}`)
    }
  }

  // Gérer la navigation manuelle
  const handleManualNavigation = () => {
    if (manualSlideInput) {
      navigateToSlide(manualSlideInput)
      setManualSlideInput("")
    }
  }

  // Détecter la slide depuis le hash de l'URL au chargement
  const getInitialSlideFromHash = () => {
    if (typeof window === 'undefined') return initialSlide

    const hash = window.location.hash
    if (hash && hash.startsWith('#/')) {
      // Extraire la slide depuis le hash (ex: #/2/3 -> "2/3")
      const slideFromHash = hash.substring(2) // Retire "#/"
      console.log('[PresentationViewer] Slide détectée depuis le hash:', slideFromHash)
      return slideFromHash
    }

    return initialSlide
  }

  useEffect(() => {
    const iframe = iframeRef.current
    if (!iframe) return

    setupAttempts.current = 0
    setIsRevealReady(false)

    // Écouter le chargement de l'iframe
    const handleIframeLoad = () => {
      console.log('[PresentationViewer] Iframe loaded')

      // Attendre que Reveal.js soit initialisé dans l'iframe
      const setupRevealListeners = () => {
        setupAttempts.current++

        if (setupAttempts.current > maxSetupAttempts) {
          console.error('[PresentationViewer] Max setup attempts reached')
          setIsRevealReady(true) // Afficher quand même l'iframe
          return
        }

        const iframeWindow = iframe.contentWindow
        if (!iframeWindow) {
          console.error('[PresentationViewer] No iframe window')
          return
        }

        const Reveal = (iframeWindow as any).Reveal
        if (!Reveal) {
          console.log(`[PresentationViewer] Reveal not ready (attempt ${setupAttempts.current}/${maxSetupAttempts}), retrying...`)
          setTimeout(setupRevealListeners, 100)
          return
        }

        console.log('[PresentationViewer] Reveal found')

        // Vérifier si Reveal est déjà initialisé
        const checkReady = () => {
          if (Reveal.isReady && Reveal.isReady()) {
            console.log('[PresentationViewer] Reveal is already ready')
            setupNavigation()
          } else {
            console.log('[PresentationViewer] Waiting for Reveal ready event')
            // Écouter l'événement ready
            Reveal.on('ready', () => {
              console.log('[PresentationViewer] Reveal ready event fired')
              setupNavigation()
            })

            // Fallback: réessayer après un délai au cas où l'événement ne se déclenche pas
            setTimeout(() => {
              if (!isRevealReady && Reveal.isReady && Reveal.isReady()) {
                console.log('[PresentationViewer] Reveal ready via fallback')
                setupNavigation()
              }
            }, 1000)
          }
        }

        const setupNavigation = () => {
          setIsRevealReady(true)

          // Reconfigurer Reveal pour le mode embedded
          try {
            Reveal.configure({
              embedded: true,
              keyboard: true,
              touch: true,
              hash: false, // Désactiver la gestion native du hash pour éviter les conflits
            })
          } catch (e) {
            console.warn('[PresentationViewer] Could not configure Reveal:', e)
          }

          // Déterminer la slide initiale (depuis le hash ou le prop)
          const targetSlide = getInitialSlideFromHash()

          // Naviguer vers la slide initiale si spécifiée
          if (targetSlide) {
            const slideParts = targetSlide.split('/')
            const h = parseInt(slideParts[0], 10) || 0
            const v = slideParts[1] ? parseInt(slideParts[1], 10) : 0

            console.log(`[PresentationViewer] Navigation vers la slide initiale ${h}/${v}`)

            // Attendre un peu que Reveal soit complètement prêt
            setTimeout(() => {
              try {
                // Utiliser la méthode de navigation appropriée
                if (typeof Reveal.slide === 'function') {
                  Reveal.slide(h, v)
                  console.log('[PresentationViewer] Navigation via Reveal.slide')
                } else if (typeof Reveal.navigateTo === 'function') {
                  Reveal.navigateTo(h, v)
                  console.log('[PresentationViewer] Navigation via Reveal.navigateTo')
                }
                setCurrentSlide(`${h}/${v}`)
              } catch (e) {
                console.error('[PresentationViewer] Error navigating to initial slide:', e)
              }
            }, 200)
          } else {
            // Obtenir la slide courante
            try {
              const indices = Reveal.getIndices()
              setCurrentSlide(`${indices.h}/${indices.v}`)
            } catch (e) {
              console.warn('[PresentationViewer] Could not get indices:', e)
              setCurrentSlide('0/0')
            }
          }

          // Écouter les changements de slide
          Reveal.on('slidechanged', (event: any) => {
            const { indexh, indexv } = event
            const newSlideIndex = `${indexh}/${indexv}`
            console.log(`[PresentationViewer] Slide changée vers ${newSlideIndex}`)
            setCurrentSlide(newSlideIndex)
            updateURL(newSlideIndex)
          })
        }

        checkReady()
      }

      // Démarrer la configuration après un délai pour laisser le temps aux scripts de se charger
      setTimeout(setupRevealListeners, 300)
    }

    iframe.addEventListener('load', handleIframeLoad)

    return () => {
      iframe.removeEventListener('load', handleIframeLoad)
      setupAttempts.current = 0
    }
  }, [presentationUrl, initialSlide])

  // Écouter les changements de hash dans l'URL pour naviguer
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash
      if (hash && hash.startsWith('#/')) {
        const slideFromHash = hash.substring(2)
        console.log('[PresentationViewer] Hash changed, navigating to:', slideFromHash)
        navigateToSlide(slideFromHash)
      }
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => {
      window.removeEventListener('hashchange', handleHashChange)
    }
  }, [])

  const toggleFullscreen = () => {
    if (iframeRef.current) {
      if (document.fullscreenElement) {
        document.exitFullscreen()
      } else {
        iframeRef.current.requestFullscreen()
      }
    }
  }

  const handleDownload = async () => {
    try {
      // Extraire le nom du fichier depuis l'URL
      const filename = presentationUrl.split('/').pop() || 'presentation.html'

      // Appeler l'API pour obtenir le package ZIP complet avec les assets
      const response = await fetch(`/api/download-presentation?filename=${encodeURIComponent(filename)}`)

      if (!response.ok) {
        throw new Error('Erreur lors du téléchargement')
      }

      const blob = await response.blob()

      // Créer un lien de téléchargement
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename.replace('.html', '.zip')

      // Déclencher le téléchargement
      document.body.appendChild(link)
      link.click()

      // Nettoyer
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error)
      alert('Une erreur est survenue lors du téléchargement. Veuillez réessayer.')
    }
  }

  return (
    <div className="space-y-4">
      {/* Contrôles principaux */}
      <div className="grid md:grid-cols-2 gap-4">
        {/* Informations et navigation */}
        <div className="glass-card rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
              Slide actuelle: <span className="font-mono text-cosmic-400">{currentSlide}</span>
            </div>
          </div>

          {/* Navigation manuelle */}
          <div className="space-y-2">
            <Label htmlFor="slide-navigation" className="text-sm">
              Aller à la slide
            </Label>
            <div className="flex gap-2">
              <Input
                id="slide-navigation"
                type="text"
                placeholder="Ex: 3 ou 3/2"
                value={manualSlideInput}
                onChange={(e) => setManualSlideInput(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    handleManualNavigation()
                  }
                }}
                className="flex-1"
              />
              <Button
                onClick={handleManualNavigation}
                variant="outline"
                size="sm"
                className="gap-2"
              >
                <Navigation className="w-4 h-4" />
                Aller
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">
              Format: <code className="px-1 py-0.5 rounded bg-cosmic-900/50">numéro</code> ou <code className="px-1 py-0.5 rounded bg-cosmic-900/50">numéro/sous-numéro</code>
            </p>
          </div>
        </div>

        {/* Actions */}
        <div className="glass-card rounded-xl p-4 flex flex-col justify-between">
          <div className="text-sm text-muted-foreground mb-3">
            Utilisez les flèches du clavier pour naviguer
          </div>
          <div className="space-y-2">
            <Button
              onClick={toggleFullscreen}
              variant="outline"
              size="sm"
              className="gap-2 w-full"
            >
              <Maximize2 className="w-4 h-4" />
              Plein écran
            </Button>
            <Button
              onClick={handleDownload}
              variant="outline"
              size="sm"
              className="gap-2 w-full"
              title="Télécharge un fichier ZIP contenant le HTML et tous les assets"
            >
              <Download className="w-4 h-4" />
              Télécharger (ZIP)
            </Button>
          </div>
        </div>
      </div>

      {/* Iframe de présentation */}
      <div className="relative w-3/4 mx-auto overflow-hidden rounded-xl border border-cosmic-800/50 bg-black/20">
        {!isRevealReady && (
          <div className="absolute inset-0 flex items-center justify-center bg-black/50 z-10">
            <div className="text-white text-center">
              <div className="animate-spin w-12 h-12 border-4 border-cosmic-400 border-t-transparent rounded-full mx-auto mb-4"></div>
              <p>Chargement de la présentation...</p>
            </div>
          </div>
        )}
        <iframe
          ref={iframeRef}
          src={presentationUrl}
          title={title}
          className="w-full aspect-video"
          sandbox="allow-scripts allow-same-origin"
          style={{
            border: 'none',
            minHeight: '600px',
          }}
        />
      </div>
    </div>
  )
}
