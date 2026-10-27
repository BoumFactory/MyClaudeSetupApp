'use client'

import { useState } from 'react'
import { Check, Copy, MessageSquare } from 'lucide-react'
import { cn } from '@/lib/utils'

/**
 * Prompt prêt à copier : texte retour à la ligne compris, les [crochets] (à remplacer
 * par le professeur) surlignés, bouton Copier.
 */
export function PromptACopier({ titre, texte, className }: { titre: string; texte: string; className?: string }) {
  const [copie, setCopie] = useState(false)

  const copier = async () => {
    try {
      await navigator.clipboard.writeText(texte)
    } catch {
      // Repli : navigateurs sans API presse-papier (page non sécurisée, ancien navigateur)
      try {
        const zone = document.createElement('textarea')
        zone.value = texte
        zone.style.position = 'fixed'
        zone.style.opacity = '0'
        document.body.appendChild(zone)
        zone.select()
        document.execCommand('copy')
        document.body.removeChild(zone)
      } catch {
        return
      }
    }
    setCopie(true)
    setTimeout(() => setCopie(false), 2000)
  }

  // Découpage pour surligner les passages entre crochets
  const morceaux = texte.split(/(\[[^\]\n]+\])/g)

  return (
    <div className={cn('rounded-lg overflow-hidden border border-sky-500/30', className)}>
      <div className="flex items-center justify-between gap-3 bg-sky-950/40 px-4 py-2">
        <span className="text-sm font-medium text-sky-200 flex items-center gap-2">
          <MessageSquare className="w-4 h-4" /> {titre}
        </span>
        <button
          type="button"
          onClick={copier}
          className={cn(
            'inline-flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs font-semibold transition-colors',
            copie ? 'bg-emerald-500/20 text-emerald-300' : 'bg-white/10 text-white/80 hover:bg-white/20'
          )}
        >
          {copie ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
          {copie ? 'Copié !' : 'Copier'}
        </button>
      </div>
      <pre className="p-4 text-sm leading-relaxed whitespace-pre-wrap break-words bg-slate-950/50 text-slate-200 font-sans">
        {morceaux.map((m, i) =>
          /^\[[^\]]+\]$/.test(m)
            ? <mark key={i} className="bg-amber-400/20 text-amber-200 rounded px-0.5">{m}</mark>
            : <span key={i}>{m}</span>
        )}
      </pre>
    </div>
  )
}
