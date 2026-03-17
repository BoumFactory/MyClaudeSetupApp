'use client'

import { useState } from 'react'
import { AI_PACKAGES } from '@/data/ai-packages'
import type { AIPackage, PackageTier } from '@/data/ai-packages'
import { AddToCartButton } from '@/components/cart/AddToCartButton'
import { Download, Check, AlertTriangle, ArrowUp, Package, ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { CartItem } from '@/types/cart-theme'

const tierColors: Record<PackageTier, { border: string; bg: string; badge: string; text: string; glow: string }> = {
  generaliste: {
    border: 'border-emerald-500/30 hover:border-emerald-400/50',
    bg: 'bg-emerald-950/20',
    badge: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
    text: 'text-emerald-400',
    glow: 'hover:shadow-[0_0_30px_rgba(16,185,129,0.1)]',
  },
  latex: {
    border: 'border-cosmic-500/30 hover:border-cosmic-400/50',
    bg: 'bg-cosmic-950/20',
    badge: 'bg-cosmic-500/20 text-cosmic-300 border-cosmic-500/30',
    text: 'text-cosmic-400',
    glow: 'hover:shadow-[0_0_30px_rgba(139,92,246,0.15)]',
  },
  word: {
    border: 'border-sky-500/30 hover:border-sky-400/50',
    bg: 'bg-sky-950/20',
    badge: 'bg-sky-500/20 text-sky-300 border-sky-500/30',
    text: 'text-sky-400',
    glow: 'hover:shadow-[0_0_30px_rgba(56,189,248,0.1)]',
  },
  avance: {
    border: 'border-purple-500/30 hover:border-purple-400/50',
    bg: 'bg-purple-950/20',
    badge: 'bg-purple-500/20 text-purple-300 border-purple-500/30',
    text: 'text-purple-400',
    glow: 'hover:shadow-[0_0_30px_rgba(168,85,247,0.15)]',
  },
}

function PackageCard({ pkg, downloading, onDownload }: {
  pkg: AIPackage
  downloading: PackageTier | null
  onDownload: (id: PackageTier) => void
}) {
  const colors = tierColors[pkg.id]

  const cartItem: CartItem = {
    id: `package-${pkg.id}`,
    name: `Package ${pkg.name}`,
    type: 'package',
    path: '',
    description: pkg.subtitle,
  }

  const inclusionLabel = pkg.tier === 2
    ? 'Inclut le bundle Généraliste'
    : pkg.tier === 3
    ? 'Inclut tous les bundles'
    : null

  return (
    <div
      id={`package-${pkg.id}`}
      className={cn(
        'relative flex flex-col rounded-xl border backdrop-blur-sm transition-all duration-300',
        colors.border,
        colors.bg,
        colors.glow,
      )}
    >
      <div className="p-6 flex-1 flex flex-col">
        {/* Icon + Name */}
        <div className="text-center mb-4">
          <span className="text-4xl mb-2 block">{pkg.icon}</span>
          <h2 className="text-xl font-bold text-white">{pkg.name}</h2>
          <p className={cn('text-sm font-medium', colors.text)}>{pkg.subtitle}</p>
        </div>

        {/* Inclusion badge */}
        {inclusionLabel && (
          <div className={cn(
            'inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium mb-4 mx-auto',
            colors.badge
          )}>
            <ArrowUp className="w-3 h-3" />
            {inclusionLabel}
          </div>
        )}

        {/* Description */}
        <p className="text-sm text-white/60 mb-4">
          {pkg.description}
        </p>

        {/* Highlights */}
        <ul className="space-y-2 mb-6 flex-1">
          {pkg.highlights.map((highlight, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <Check className={cn('w-4 h-4 mt-0.5 flex-shrink-0', colors.text)} />
              <span className="text-white/70">{highlight}</span>
            </li>
          ))}
        </ul>

        {/* Stats */}
        <div className="flex items-center justify-center gap-4 py-3 mb-4 border-t border-b border-white/5 text-xs text-white/40">
          <span>{pkg.skills.length} skills</span>
          <span>·</span>
          <span>{pkg.agentPaths.includes('*') ? 'Tous les' : pkg.agentPaths.length} agents</span>
          <span>·</span>
          <span>{pkg.commandPaths.includes('*') ? 'Toutes les' : pkg.commandPaths.length} commandes</span>
        </div>

        {/* Actions */}
        <div className="space-y-2">
          <AddToCartButton item={cartItem} className="w-full" />
          <button
            onClick={() => onDownload(pkg.id)}
            disabled={downloading === pkg.id}
            className={cn(
              'w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg',
              'text-sm font-medium transition-all duration-200',
              'bg-white/5 hover:bg-white/10 text-white/60 hover:text-white/80',
              'border border-white/10 hover:border-white/20',
              downloading === pkg.id && 'opacity-50 cursor-not-allowed'
            )}
          >
            <Download className="w-4 h-4" />
            {downloading === pkg.id ? 'Génération...' : 'Télécharger directement'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function DownloadAIPackagesPage() {
  const [downloading, setDownloading] = useState<PackageTier | null>(null)

  const handleDirectDownload = async (packageId: PackageTier) => {
    setDownloading(packageId)
    try {
      const response = await fetch('/api/download-package', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ packageId }),
      })
      if (!response.ok) {
        const errBody = await response.text().catch(() => 'no body')
        throw new Error(`Erreur ZIP: ${response.status} — ${errBody}`)
      }
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `claude-setup-${packageId}.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Erreur telechargement package:', err)
    } finally {
      setDownloading(null)
    }
  }

  const generaliste = AI_PACKAGES.find(p => p.id === 'generaliste')!
  const latex = AI_PACKAGES.find(p => p.id === 'latex')!
  const word = AI_PACKAGES.find(p => p.id === 'word')!
  const avance = AI_PACKAGES.find(p => p.id === 'avance')!

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cosmic-900/50 border border-cosmic-700/50 text-sm text-cosmic-300 mb-6">
          <Package className="w-4 h-4" />
          Packages IA
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">
          Configurations Claude Code
        </h1>
        <p className="text-lg text-white/60 max-w-2xl mx-auto">
          Des setups <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">.claude</code> prêts à l'emploi,
          adaptés à votre profil. Chaque package contient les skills, agents et commandes nécessaires.
        </p>
      </div>

      {/* Tier 1 — Généraliste (centré, seul) */}
      <div className="max-w-md mx-auto mb-6">
        <PackageCard pkg={generaliste} downloading={downloading} onDownload={handleDirectDownload} />
      </div>

      {/* Connector */}
      <div className="flex justify-center mb-6">
        <div className="flex flex-col items-center text-white/20">
          <div className="w-px h-4 bg-white/20" />
          <ChevronDown className="w-4 h-4 -mt-1" />
        </div>
      </div>

      {/* Tier 2 — LaTeX + Word (côte à côte) */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto mb-6">
        <PackageCard pkg={latex} downloading={downloading} onDownload={handleDirectDownload} />
        <PackageCard pkg={word} downloading={downloading} onDownload={handleDirectDownload} />
      </div>

      {/* Connector */}
      <div className="flex justify-center mb-6">
        <div className="flex flex-col items-center text-white/20">
          <div className="w-px h-4 bg-white/20" />
          <ChevronDown className="w-4 h-4 -mt-1" />
        </div>
      </div>

      {/* Tier 3 — Power User (pleine largeur) */}
      <div className="max-w-4xl mx-auto mb-12">
        <PackageCard pkg={avance} downloading={downloading} onDownload={handleDirectDownload} />
      </div>

      {/* Warning about cart conflicts */}
      <div className="max-w-4xl mx-auto glass-card p-4 rounded-xl border border-amber-500/20 bg-amber-950/10">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-amber-300 text-sm mb-1">Bundles inclusifs</h3>
            <p className="text-xs text-white/50">
              Les bundles spécialisés (LaTeX et Word Enseignant) incluent le Généraliste.
              Le Power User inclut tout. Il est inutile d'ajouter un bundle déjà couvert par un autre.
              Le panier vous préviendra en cas de doublons.
            </p>
          </div>
        </div>
      </div>

      {/* Installation guide */}
      <div className="mt-12 max-w-4xl mx-auto glass-card p-6 rounded-xl border border-white/10">
        <h2 className="text-lg font-bold text-white mb-4">Installation</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">1</div>
            <div>
              <p className="text-sm font-medium text-white">Téléchargez et décompressez</p>
              <p className="text-xs text-white/50">Le ZIP contient un dossier <code className="text-cosmic-300">.claude</code>, un <code className="text-cosmic-300">CLAUDE.md</code> et un <code className="text-cosmic-300">settings.json</code></p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">2</div>
            <div>
              <p className="text-sm font-medium text-white">Copiez à la racine</p>
              <p className="text-xs text-white/50">Placez <code className="text-cosmic-300">.claude/</code> et <code className="text-cosmic-300">CLAUDE.md</code> à la racine de votre projet</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">3</div>
            <div>
              <p className="text-sm font-medium text-white">Lancez Claude Code</p>
              <p className="text-xs text-white/50">Les skills et agents seront automatiquement disponibles via les commandes slash</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
