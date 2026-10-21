'use client'

import { useState } from 'react'
import { Copy, Check } from 'lucide-react'

const PLACEHOLDER_IDEA = '[décrivez ici votre idée, en une ou deux phrases]'

function buildPrompt(idea: string): string {
  const subject = idea.trim() || PLACEHOLDER_IDEA
  return `/grill-me ${subject}

Avant de te lancer, interroge-moi pour affiner cette idée.
- Pose toutes les questions utiles par manches, avec des options concrètes et ta recommandation pour chacune.
- Cherche toi-même les faits que tu peux vérifier (fichiers, outils disponibles) au lieu de me les demander.
- Quand tout est clair, fais un récapitulatif d'une ligne par décision et attends ma confirmation avant d'agir.`
}

export function GrillMeCopy() {
  const [idea, setIdea] = useState('')
  const [copied, setCopied] = useState(false)

  const prompt = buildPrompt(idea)

  const handleCopy = () => {
    navigator.clipboard.writeText(prompt).then(() => {
      setCopied(true)
      setTimeout(() => setCopied(false), 2500)
    })
  }

  return (
    <div className="space-y-3 py-4">
      <div className="text-xs font-semibold text-violet-400">
        LANCER UNE INTERVIEW GRILL-ME
      </div>

      <div className="bg-black/30 border border-violet-500/30 rounded-lg p-3 space-y-2">
        <div className="text-xs text-gray-500">Votre idée (elle sera insérée dans la commande) :</div>
        <textarea
          value={idea}
          onChange={(e) => setIdea(e.target.value)}
          placeholder="Ex : une fiche de révision sur les fonctions affines pour mes élèves de seconde..."
          className="w-full min-h-[60px] bg-black/30 border border-white/10 rounded-md p-3 text-gray-200 text-sm placeholder-gray-600 resize-y focus:outline-none focus:ring-2 focus:ring-violet-500/50"
        />
      </div>

      <pre className="bg-black/40 border border-violet-500/30 rounded-lg p-4 text-[0.78rem] leading-relaxed whitespace-pre-wrap text-gray-300 font-mono">
        {prompt}
      </pre>

      <button
        onClick={handleCopy}
        className={`w-full flex items-center justify-center gap-2 py-3 rounded-lg font-semibold transition-all text-sm ${
          copied
            ? 'bg-gradient-to-r from-green-600/40 to-emerald-600/40 border border-green-500/50 text-green-200'
            : 'bg-gradient-to-r from-violet-600/40 to-indigo-600/40 border border-violet-500/50 text-violet-100 hover:from-violet-600/50 hover:to-indigo-600/50'
        }`}
      >
        {copied ? (
          <>
            <Check className="w-4 h-4" />
            Copié ! Collez-le dans Claude Code
          </>
        ) : (
          <>
            <Copy className="w-4 h-4" />
            Copier la commande
          </>
        )}
      </button>

      <p className="text-xs text-gray-500 leading-relaxed">
        <strong className="text-emerald-400">Comment ça marche :</strong> collez le texte dans Claude Code.
        Le skill <code>grill-me</code> (fourni dans le pack de skills) vous demande d&apos;abord où poser les questions
        (dans le terminal ou sur une page cliquable), puis vous interroge manche par manche jusqu&apos;à ce que
        l&apos;idée soit claire.
      </p>
    </div>
  )
}
