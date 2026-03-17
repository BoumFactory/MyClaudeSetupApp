'use client'

import { useState } from 'react'
import { useCart } from '@/contexts/CartContext'
import { useCartTheme } from '@/contexts/CartThemeContext'
import { Button } from '@/components/ui/button'
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetDescription,
  SheetFooter,
} from '@/components/ui/sheet'
import { cn } from '@/lib/utils'
import { HelpCircle, X } from 'lucide-react'
import { AI_PACKAGES, findRedundantPackages } from '@/data/ai-packages'
import type { PackageTier } from '@/data/ai-packages'

interface CartDrawerProps {
  /** Contrôle l'ouverture du drawer */
  open: boolean
  /** Callback de fermeture */
  onOpenChange: (open: boolean) => void
}

/**
 * Drawer latéral (Sheet) affichant le contenu du panier
 * Utilise le thème allégorique pour les textes et le style glass-card
 */
export function CartDrawer({ open, onOpenChange }: CartDrawerProps) {
  const { items, removeItem, clearCart, count } = useCart()
  const { theme } = useCartTheme()

  const [isDownloading, setIsDownloading] = useState(false)
  const [showHelp, setShowHelp] = useState(false)

  // Detect package conflicts in cart (non-linear hierarchy)
  const packageConflicts = (() => {
    const packageItems = items.filter(i => i.id.startsWith('package-'))
    if (packageItems.length <= 1) return null

    const packageIds = packageItems.map(i => i.id.replace('package-', '') as PackageTier)
    const { redundant, reason } = findRedundantPackages(packageIds)

    if (redundant.length === 0) return null

    return redundant.map(id => {
      const item = packageItems.find(i => i.id === `package-${id}`)!
      const includedBy = AI_PACKAGES.find(p => p.id === reason[id])!
      return { item, includedByName: includedBy.name }
    })
  })()

  const handleDownload = async () => {
    if (items.length === 0) return
    setIsDownloading(true)
    try {
      const packageItems = items.filter(i => i.id.startsWith('package-'))
      const regularItems = items.filter(i => !i.id.startsWith('package-'))

      // Download packages: deduplicate then download each non-redundant one
      if (packageItems.length > 0) {
        const pkgIds = packageItems
          .map(i => i.id.replace('package-', '') as PackageTier)

        // Remove redundant packages (already included by others)
        const { redundant } = findRedundantPackages(pkgIds)
        const toDownload = pkgIds.filter(id => !redundant.includes(id))

        for (const pkgId of toDownload) {
          const response = await fetch('/api/download-package', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ packageId: pkgId }),
          })
          if (!response.ok) {
            const errBody = await response.text().catch(() => 'no body')
            throw new Error(`Erreur ZIP package ${pkgId}: ${response.status} — ${errBody}`)
          }
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = `claude-setup-${pkgId}.zip`
          document.body.appendChild(a)
          a.click()
          // Laisser le temps au navigateur d'initier le téléchargement
          await new Promise(resolve => setTimeout(resolve, 500))
          window.URL.revokeObjectURL(url)
          document.body.removeChild(a)
        }
      }

      // Download regular items (if any)
      if (regularItems.length > 0) {
        const response = await fetch('/api/download', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            cartItems: regularItems,
            themeName: theme.name,
          }),
        })
        if (!response.ok) {
            const errBody = await response.text().catch(() => 'no body')
            throw new Error(`Erreur ZIP regular: ${response.status} — ${errBody}`)
          }
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `bfcours-${Date.now()}.zip`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }

      clearCart()
    } catch (err: any) {
      console.error('Erreur téléchargement panier:', err?.message || err)
    } finally {
      setIsDownloading(false)
    }
  }

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className={cn(
          'glass-card border-white/10',
          'bg-gray-900/95 backdrop-blur-xl',
          'flex flex-col'
        )}
      >
        <SheetHeader>
          <div className="flex items-center justify-between">
            <SheetTitle className="text-white flex items-center gap-2">
              <span className="text-2xl">{theme.icon}</span>
              <span>{theme.name}</span>
            </SheetTitle>
            <Button
              variant="ghost"
              size="sm"
              className="text-white/40 hover:text-white/80 hover:bg-white/10 h-8 w-8 p-0"
              onClick={() => setShowHelp(v => !v)}
            >
              {showHelp ? <X className="w-4 h-4" /> : <HelpCircle className="w-4 h-4" />}
            </Button>
          </div>
          <SheetDescription className="text-white/60">
            {count === 0
              ? theme.emptyMessage
              : `${count} élément${count > 1 ? 's' : ''}`}
          </SheetDescription>
        </SheetHeader>

        {/* Widget aide */}
        {showHelp && (
          <div className="mx-1 p-3 rounded-lg bg-white/5 border border-white/10 space-y-2 text-xs text-white/60">
            <p className="text-white/80 font-medium text-sm">Comment fonctionne le panier ?</p>
            <p>
              Le panier change d'apparence selon l'animation de fond active.
              Chaque animation a son propre univers : le filet de Fibonacci, la besace du Dragon, la partition de Fourier...
            </p>
            <p>
              Les boutons utilisent le vocabulaire de cet univers, mais les actions restent les mêmes :
            </p>
            <ul className="space-y-1 pl-3">
              <li><span className="text-white/80">Bouton principal</span> = t&eacute;l&eacute;charger vos ressources en ZIP</li>
              <li><span className="text-white/80">Bouton secondaire</span> = vider le panier sans t&eacute;l&eacute;charger</li>
              <li><span className="text-white/80">Bouton par item</span> = retirer cet item du panier</li>
            </ul>
            <p className="text-white/40 italic">
              Changez l'animation de fond pour d&eacute;couvrir les diff&eacute;rentes all&eacute;gories !
            </p>
          </div>
        )}

        {/* Package conflict warning */}
        {packageConflicts && packageConflicts.length > 0 && (
          <div className="mx-1 p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 space-y-2">
            <p className="text-sm font-medium text-amber-300 flex items-center gap-2">
              <span>⚠️</span>
              Bundles redondants détectés
            </p>
            <ul className="space-y-1">
              {packageConflicts.map(({ item, includedByName }) => (
                <li key={item.id} className="flex items-center justify-between text-xs">
                  <span className="text-white/60">
                    <span className="text-amber-200">{item.name}</span>
                    {' '}déjà inclus dans <strong className="text-white/80">{includedByName}</strong>
                  </span>
                  <button
                    onClick={() => removeItem(item.id)}
                    className="text-amber-400 hover:text-amber-300 underline ml-2 flex-shrink-0"
                  >
                    Retirer
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Liste des items */}
        <div className="flex-1 overflow-y-auto py-4 space-y-2">
          {items.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-white/40 space-y-3">
              <span className="text-5xl">{theme.icon}</span>
              <p className="text-sm text-center">{theme.emptyMessage}</p>
            </div>
          ) : (
            items.map(item => (
              <div
                key={item.id}
                className={cn(
                  'flex items-center justify-between',
                  'p-3 rounded-lg',
                  'bg-white/5 border border-white/10',
                  'hover:bg-white/10 transition-colors'
                )}
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">
                    {item.name}
                  </p>
                  {item.description && (
                    <p className="text-xs text-white/50 truncate">
                      {item.description}
                    </p>
                  )}
                  <span className="text-xs text-white/30 capitalize">
                    {item.type}
                  </span>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-red-400 hover:text-red-300 hover:bg-red-500/10 ml-2 shrink-0"
                  onClick={() => removeItem(item.id)}
                >
                  {theme.verbRemove}
                </Button>
              </div>
            ))
          )}
        </div>

        {/* Footer avec actions */}
        {items.length > 0 && (
          <SheetFooter className="flex-col gap-2 sm:flex-col">
            <Button
              variant="cosmic"
              className="w-full"
              onClick={handleDownload}
              disabled={isDownloading}
            >
              {theme.icon} {isDownloading ? 'Génération du ZIP...' : theme.verbDownload}
            </Button>
            <Button
              variant="ghost"
              className="w-full text-white/50 hover:text-white/80"
              onClick={clearCart}
            >
              {theme.verbClear}
            </Button>
          </SheetFooter>
        )}
      </SheetContent>
    </Sheet>
  )
}
