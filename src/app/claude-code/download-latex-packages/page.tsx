'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useCart } from '@/contexts/CartContext'
import { useCartTheme } from '@/contexts/CartThemeContext'
import { triggerCartToast } from '@/components/cart/CartToast'
import { Download, Check, Package, ArrowRight, BookOpen, FolderTree, Sparkles, AlertTriangle } from 'lucide-react'
import { cn } from '@/lib/utils'
import type { CartItem } from '@/types/cart-theme'

// ────────────────────────────────────────────────────────────────────
// Bundles LaTeX téléchargeables — bfcours seul OU bfcours + ProfDeleuze.
// Chaque bundle expose deux payloads :
//  - cartItems    : noms lisibles, pour le panier allégorique
//  - installItems : structure `localtexmf/tex/latex/...` prête à brancher
//                   sur MikTeX, pour le téléchargement direct optimisé
// (Le mode `cartItems` de /api/download zippe un dossier sous `item.name`,
//  donc un nom avec des `/` reconstitue l'arborescence localtexmf.)
// ────────────────────────────────────────────────────────────────────
type LatexBundleId = 'bfcours' | 'bfcours-profdeleuze'

interface LatexBundle {
  id: LatexBundleId
  name: string
  subtitle: string
  icon: string
  description: string
  highlights: string[]
  badge: string | null
  cartItems: CartItem[]
  installItems: { name: string; path: string }[]
}

const BFCOURS_CART_ITEM: CartItem = {
  id: 'latex-bfcours',
  name: 'Package bfcours',
  type: 'package',
  path: 'download/latex-packages/BFcours',
  description: 'Package LaTeX bfcours (localtexmf)',
}

const PROFDELEUZE_CART_ITEM: CartItem = {
  id: 'latex-profdeleuze',
  name: 'Modules ProfDeleuze',
  type: 'package',
  path: 'download/latex-packages/ProfDeleuze',
  description: 'Modules rd* (exercices, MCQ, grilles…) de ProfDeleuze',
}

const BFCOURS_INSTALL = { name: 'localtexmf/tex/latex/bfcours', path: 'download/latex-packages/BFcours' }
const PROFDELEUZE_INSTALL = { name: 'localtexmf/tex/latex/ProfDeleuze', path: 'download/latex-packages/ProfDeleuze' }

const LATEX_BUNDLES: LatexBundle[] = [
  {
    id: 'bfcours',
    name: 'bfcours',
    subtitle: 'Le package essentiel',
    icon: '📐',
    description:
      "Le package LaTeX maison pour l'enseignement des mathématiques : environnements de cours, exercices, activités, évaluations, couleurs et commandes prêtes à l'emploi.",
    highlights: [
      'Environnements de cours, exercices et activités',
      'Commandes mathématiques simplifiées',
      'Couleurs et mise en page cohérentes',
      'Compatible Claude Code et QF-Studio',
    ],
    badge: 'Recommandé',
    cartItems: [BFCOURS_CART_ITEM],
    installItems: [BFCOURS_INSTALL],
  },
  {
    id: 'bfcours-profdeleuze',
    name: 'bfcours + ProfDeleuze',
    subtitle: "L'arsenal complet",
    icon: '🎯',
    description:
      "bfcours accompagné des modules ProfDeleuze (rdexo, rdcrep, rdmcq…) pour les fiches d'exercices avancées, les QCM multi-formats et les grilles de correction.",
    highlights: [
      'Tout le package bfcours inclus',
      'Modules rdexo / rdcrep (exercices & corrections)',
      'QCM multi-formats (rdmcq : Paris, Reims, Tokyo…)',
      'Grilles, ratios, arithmétique et gestion du temps',
    ],
    badge: 'Complet',
    cartItems: [BFCOURS_CART_ITEM, PROFDELEUZE_CART_ITEM],
    installItems: [BFCOURS_INSTALL, PROFDELEUZE_INSTALL],
  },
]

function LatexPackageCard({
  bundle,
  downloading,
  onDownload,
}: {
  bundle: LatexBundle
  downloading: LatexBundleId | null
  onDownload: (bundle: LatexBundle) => void
}) {
  const { addItem, isInCart } = useCart()
  const { theme } = useCartTheme()

  const allInCart = bundle.cartItems.every((i) => isInCart(i.id))

  const handleAddToCart = () => {
    if (allInCart) return
    bundle.cartItems.forEach(addItem)
    triggerCartToast(`${theme.notification} ${bundle.name}`)
  }

  return (
    <div
      className={cn(
        'relative flex flex-col rounded-xl border backdrop-blur-sm transition-all duration-300',
        'border-cosmic-500/30 hover:border-cosmic-400/50 bg-cosmic-950/20',
        'hover:shadow-[0_0_30px_rgba(139,92,246,0.15)]',
      )}
    >
      <div className="p-6 flex-1 flex flex-col">
        {/* Icon + Name */}
        <div className="text-center mb-4">
          <span className="text-4xl mb-2 block">{bundle.icon}</span>
          <h2 className="text-xl font-bold text-white">{bundle.name}</h2>
          <p className="text-sm font-medium text-cosmic-400">{bundle.subtitle}</p>
        </div>

        {/* Badge */}
        {bundle.badge && (
          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border text-xs font-medium mb-4 mx-auto bg-cosmic-500/20 text-cosmic-300 border-cosmic-500/30">
            <Sparkles className="w-3 h-3" />
            {bundle.badge}
          </div>
        )}

        {/* Description */}
        <p className="text-sm text-white/60 mb-4">{bundle.description}</p>

        {/* Highlights */}
        <ul className="space-y-2 mb-6 flex-1">
          {bundle.highlights.map((highlight, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <Check className="w-4 h-4 mt-0.5 flex-shrink-0 text-cosmic-400" />
              <span className="text-white/70">{highlight}</span>
            </li>
          ))}
        </ul>

        {/* Actions */}
        <div className="space-y-2">
          <button
            onClick={handleAddToCart}
            disabled={allInCart}
            className={cn(
              'w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg',
              'text-sm font-medium text-white transition-all duration-200',
              allInCart
                ? 'bg-white/10 cursor-not-allowed'
                : 'cosmic-gradient hover:opacity-90',
            )}
          >
            {allInCart ? 'Déjà ajouté ✓' : `${theme.icon} ${theme.verbAdd}`}
          </button>
          <button
            onClick={() => onDownload(bundle)}
            disabled={downloading === bundle.id}
            className={cn(
              'w-full flex items-center justify-center gap-2 px-4 py-2 rounded-lg',
              'text-sm font-medium transition-all duration-200',
              'bg-white/5 hover:bg-white/10 text-white/60 hover:text-white/80',
              'border border-white/10 hover:border-white/20',
              downloading === bundle.id && 'opacity-50 cursor-not-allowed',
            )}
          >
            <Download className="w-4 h-4" />
            {downloading === bundle.id ? 'Génération…' : 'Télécharger directement'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default function DownloadLatexPackagesPage() {
  const [downloading, setDownloading] = useState<LatexBundleId | null>(null)

  const handleDirectDownload = async (bundle: LatexBundle) => {
    setDownloading(bundle.id)
    try {
      const cartItems: CartItem[] = bundle.installItems.map((item, i) => ({
        id: `${bundle.id}-${i}`,
        name: item.name,
        type: 'package',
        path: item.path,
      }))

      const response = await fetch('/api/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cartItems, themeName: 'Pack LaTeX' }),
      })
      if (!response.ok) {
        const errBody = await response.text().catch(() => 'no body')
        throw new Error(`Erreur ZIP: ${response.status} — ${errBody}`)
      }
      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `bfcours-latex-${bundle.id}.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      console.error('Erreur telechargement package LaTeX:', err)
    } finally {
      setDownloading(null)
    }
  }

  return (
    <div className="container mx-auto px-4 py-12 max-w-6xl">
      {/* Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cosmic-900/50 border border-cosmic-700/50 text-sm text-cosmic-300 mb-6">
          <Package className="w-4 h-4" />
          Packages LaTeX
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">Packages LaTeX bfcours</h1>
        <p className="text-lg text-white/60 max-w-2xl mx-auto">
          Téléchargez le package{' '}
          <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">bfcours</code>{' '}
          déjà structuré en <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">localtexmf</code>,
          prêt à brancher sur MikTeX. Nécessaire pour compiler les documents générés par Claude Code et par l'application QF-Studio.
        </p>
      </div>

      {/* Lien direct vers le tutoriel d'installation */}
      <Link
        href="/claude-code/tutorials/bfcours-setup"
        prefetch={false}
        className="group block max-w-4xl mx-auto mb-12"
      >
        <div className="glass-card rounded-xl p-5 border border-nebula-500/30 hover:border-nebula-400/50 transition-all duration-300 flex items-center gap-4">
          <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center flex-shrink-0">
            <BookOpen className="w-6 h-6 text-white" />
          </div>
          <div className="flex-1">
            <h2 className="font-semibold text-white group-hover:text-nebula-300 transition-colors">
              Tutoriel : installer bfcours dans MikTeX
            </h2>
            <p className="text-sm text-white/55">
              Guide pas à pas pour enregistrer le dossier <code className="text-nebula-300">localtexmf</code> dans MikTeX et tester la compilation.
            </p>
          </div>
          <ArrowRight className="w-5 h-5 text-nebula-400 flex-shrink-0 group-hover:translate-x-1 transition-transform" />
        </div>
      </Link>

      {/* Bundles */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-4xl mx-auto mb-12">
        {LATEX_BUNDLES.map((bundle) => (
          <LatexPackageCard
            key={bundle.id}
            bundle={bundle}
            downloading={downloading}
            onDownload={handleDirectDownload}
          />
        ))}
      </div>

      {/* Note structure */}
      <div className="max-w-4xl mx-auto glass-card p-4 rounded-xl border border-cosmic-500/20 bg-cosmic-950/10 mb-12">
        <div className="flex items-start gap-3">
          <FolderTree className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
          <div>
            <h3 className="font-medium text-cosmic-300 text-sm mb-1">Archive prête à l'emploi</h3>
            <p className="text-xs text-white/50">
              Le téléchargement direct contient déjà l'arborescence{' '}
              <code className="text-cosmic-300">localtexmf/tex/latex/…</code>. Il vous suffit de décompresser
              le dossier <code className="text-cosmic-300">localtexmf</code> dans un emplacement permanent et de
              l'ajouter dans MikTeX Console (Settings → Directories), puis de rafraîchir la base de données.
            </p>
          </div>
        </div>
      </div>

      {/* Installation rapide */}
      <div className="max-w-4xl mx-auto glass-card p-6 rounded-xl border border-white/10">
        <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
          <h2 className="text-lg font-bold text-white">Installation rapide</h2>
          <Link
            href="/claude-code/tutorials/bfcours-setup"
            prefetch={false}
            className="inline-flex items-center gap-1.5 text-sm text-cosmic-400 hover:text-cosmic-300 transition-colors"
          >
            Guide détaillé
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">1</div>
            <div>
              <p className="text-sm font-medium text-white">Décompressez l'archive</p>
              <p className="text-xs text-white/50">
                Placez le dossier <code className="text-cosmic-300">localtexmf</code> dans un emplacement permanent.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">2</div>
            <div>
              <p className="text-sm font-medium text-white">Déclarez-le dans MikTeX</p>
              <p className="text-xs text-white/50">
                MikTeX Console → Settings → Directories → ajoutez le chemin du dossier.
              </p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 rounded-lg bg-cosmic-500/20 flex items-center justify-center text-cosmic-300 font-bold text-sm flex-shrink-0">3</div>
            <div>
              <p className="text-sm font-medium text-white">Rafraîchissez la base</p>
              <p className="text-xs text-white/50">
                Tasks → Refresh file name database, puis compilez en LuaLaTeX.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Avertissement compilateur */}
      <div className="max-w-4xl mx-auto glass-card p-4 rounded-xl border border-amber-500/20 bg-amber-950/10 mt-6">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-white/50">
            bfcours se compile avec <strong className="text-amber-300">LuaLaTeX</strong> (et non pdfLaTeX).
            Pensez à sélectionner ce moteur dans votre éditeur.
          </p>
        </div>
      </div>
    </div>
  )
}
