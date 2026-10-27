'use client'

import { useEffect, useRef, useState, type ReactNode } from 'react'
import { Check, ChevronLeft, ChevronRight, Clock, ListChecks, Rows3, RotateCcw } from 'lucide-react'
import { cn } from '@/lib/utils'
import { ETAPES, type CouleurEtape, type EtapeTuto } from './etapes'

const CLE_FAITS = 'tuto-creer-un-skill:faits'
const CLE_ETAPE = 'tuto-creer-un-skill:etape'

/** Classes complètes par couleur (Tailwind ne génère pas de classes construites à la volée) */
const COULEURS: Record<CouleurEtape, { pastille: string; bord: string; texte: string; fond: string }> = {
  emerald: { pastille: 'bg-emerald-500', bord: 'border-emerald-500/40', texte: 'text-emerald-300', fond: 'bg-emerald-500/10' },
  sky: { pastille: 'bg-sky-500', bord: 'border-sky-500/40', texte: 'text-sky-300', fond: 'bg-sky-500/10' },
  amber: { pastille: 'bg-amber-500', bord: 'border-amber-500/40', texte: 'text-amber-300', fond: 'bg-amber-500/10' },
  violet: { pastille: 'bg-violet-500', bord: 'border-violet-500/40', texte: 'text-violet-300', fond: 'bg-violet-500/10' },
  teal: { pastille: 'bg-teal-500', bord: 'border-teal-500/40', texte: 'text-teal-300', fond: 'bg-teal-500/10' },
  slate: { pastille: 'bg-slate-500', bord: 'border-slate-400/40', texte: 'text-slate-300', fond: 'bg-slate-500/10' },
}

function lire<T>(cle: string, defaut: T): T {
  try {
    const brut = window.localStorage.getItem(cle)
    return brut === null ? defaut : (JSON.parse(brut) as T)
  } catch {
    return defaut
  }
}

function ecrire(cle: string, valeur: unknown) {
  try {
    window.localStorage.setItem(cle, JSON.stringify(valeur))
  } catch {
    // Stockage indisponible (navigation privée, quota) : la progression n'est simplement pas mémorisée
  }
}

/**
 * Parcours en étapes numérotées : une étape à la fois (Précédent / Suivant) ou toutes à la suite,
 * case « fait » par étape mémorisée dans le navigateur, lien direct #etape-N.
 */
export function CreerUnSkillStepper() {
  const [courante, setCourante] = useState(0)
  const [faits, setFaits] = useState<string[]>([])
  const [toutes, setToutes] = useState(false)
  const [charge, setCharge] = useState(false)
  const haut = useRef<HTMLDivElement>(null)

  // Lecture de la progression (après le premier rendu, pour éviter un écart d'hydratation)
  useEffect(() => {
    setFaits(lire<string[]>(CLE_FAITS, []).filter(id => ETAPES.some(e => e.id === id)))
    const depuisLien = /^#etape-(\d+)$/.exec(window.location.hash)
    const n = depuisLien ? Number(depuisLien[1]) - 1 : lire<number>(CLE_ETAPE, 0)
    if (Number.isInteger(n) && n >= 0 && n < ETAPES.length) setCourante(n)
    setCharge(true)
  }, [])

  useEffect(() => { if (charge) ecrire(CLE_FAITS, faits) }, [faits, charge])
  useEffect(() => { if (charge) ecrire(CLE_ETAPE, courante) }, [courante, charge])

  const aller = (i: number) => {
    setCourante(i)
    setToutes(false)
    haut.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  const basculerFait = (id: string) =>
    setFaits(f => (f.includes(id) ? f.filter(x => x !== id) : [...f, id]))

  const nbFaits = faits.length
  const pourcent = Math.round((nbFaits / ETAPES.length) * 100)

  return (
    <div ref={haut} className="scroll-mt-24 space-y-6">
      {/* Progression */}
      <div className="glass-card rounded-xl p-4 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="text-sm text-white/70 flex items-center gap-2">
            <ListChecks className="w-4 h-4 text-emerald-400" />
            <span><strong className="text-white">{nbFaits}</strong> étape{nbFaits > 1 ? 's' : ''} faite{nbFaits > 1 ? 's' : ''} sur {ETAPES.length}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => setToutes(t => !t)}
              className="inline-flex items-center gap-1.5 rounded-md border border-white/10 px-3 py-1.5 text-xs text-white/70 hover:text-white hover:bg-white/5"
            >
              <Rows3 className="w-3.5 h-3.5" /> {toutes ? 'Une étape à la fois' : 'Afficher toutes les étapes'}
            </button>
            {nbFaits > 0 && (
              <button
                type="button"
                onClick={() => setFaits([])}
                className="inline-flex items-center gap-1.5 rounded-md px-2 py-1.5 text-xs text-white/40 hover:text-white/70"
                title="Décocher toutes les étapes"
              >
                <RotateCcw className="w-3.5 h-3.5" /> Réinitialiser
              </button>
            )}
          </div>
        </div>
        <div className="h-1.5 rounded-full bg-white/10 overflow-hidden">
          <div className="h-full bg-gradient-to-r from-emerald-500 to-sky-500 transition-all" style={{ width: `${pourcent}%` }} />
        </div>

        {/* Les six étapes, cliquables */}
        <ol className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2">
          {ETAPES.map((e, i) => {
            const c = COULEURS[e.couleur]
            const fait = faits.includes(e.id)
            const actif = !toutes && i === courante
            return (
              <li key={e.id}>
                <button
                  type="button"
                  onClick={() => aller(i)}
                  aria-current={actif ? 'step' : undefined}
                  className={cn(
                    'w-full h-full text-left rounded-lg border px-3 py-2 transition-colors',
                    actif ? cn(c.bord, c.fond) : 'border-white/10 hover:bg-white/5'
                  )}
                >
                  <div className="flex items-center gap-2">
                    <span className={cn('w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0', fait ? 'bg-emerald-600' : c.pastille)}>
                      {fait ? <Check className="w-3.5 h-3.5" /> : i + 1}
                    </span>
                    <span className={cn('text-xs font-semibold leading-tight', actif ? 'text-white' : 'text-white/70')}>{e.titre}</span>
                  </div>
                </button>
              </li>
            )
          })}
        </ol>
      </div>

      {/* Contenu */}
      {toutes
        ? ETAPES.map((e, i) => (
            <CarteEtape key={e.id} etape={e} index={i} fait={faits.includes(e.id)} onFait={() => basculerFait(e.id)} />
          ))
        : (
          <CarteEtape
            etape={ETAPES[courante]}
            index={courante}
            fait={faits.includes(ETAPES[courante].id)}
            onFait={() => basculerFait(ETAPES[courante].id)}
            navigation={
              <div className="flex items-center justify-between gap-3 pt-6 mt-6 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => aller(courante - 1)}
                  disabled={courante === 0}
                  className="inline-flex items-center gap-1.5 rounded-lg border border-white/10 px-4 py-2 text-sm text-white/80 hover:bg-white/5 disabled:opacity-30 disabled:pointer-events-none"
                >
                  <ChevronLeft className="w-4 h-4" /> Précédent
                </button>
                <span className="text-xs text-white/40">Étape {courante + 1} sur {ETAPES.length}</span>
                {courante < ETAPES.length - 1 ? (
                  <button
                    type="button"
                    onClick={() => {
                      if (!faits.includes(ETAPES[courante].id)) basculerFait(ETAPES[courante].id)
                      aller(courante + 1)
                    }}
                    className="inline-flex items-center gap-1.5 rounded-lg bg-cosmic-500/30 border border-cosmic-400/40 px-4 py-2 text-sm font-semibold text-white hover:bg-cosmic-500/40"
                    title="Marque cette étape comme faite et passe à la suivante"
                  >
                    Suivant <ChevronRight className="w-4 h-4" />
                  </button>
                ) : (
                  <span className="w-[104px]" />
                )}
              </div>
            }
          />
        )}
    </div>
  )
}

function CarteEtape({
  etape,
  index,
  fait,
  onFait,
  navigation,
}: {
  etape: EtapeTuto
  index: number
  fait: boolean
  onFait: () => void
  navigation?: ReactNode
}) {
  const c = COULEURS[etape.couleur]
  return (
    <section id={`etape-${index + 1}`} className={cn('glass-card rounded-xl border-l-4 p-6 md:p-8 scroll-mt-24', c.bord)}>
      <header className="flex flex-wrap items-start justify-between gap-4 mb-6">
        <div className="flex items-start gap-4">
          <span className={cn('w-10 h-10 rounded-full flex items-center justify-center text-lg font-bold text-white shrink-0', c.pastille)}>
            {index + 1}
          </span>
          <div>
            <h2 className="text-2xl font-bold text-white">{etape.titre}</h2>
            <p className={cn('text-sm mt-1', c.texte)}>{etape.resume}</p>
            <p className="text-xs text-white/40 mt-1 flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {etape.duree}</p>
          </div>
        </div>
        <label className={cn(
          'inline-flex items-center gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer select-none transition-colors',
          fait ? 'border-emerald-500/40 bg-emerald-500/15 text-emerald-200' : 'border-white/15 text-white/70 hover:bg-white/5'
        )}>
          <input type="checkbox" checked={fait} onChange={onFait} className="w-4 h-4 accent-emerald-500" />
          {fait ? 'Fait' : 'Marquer comme fait'}
        </label>
      </header>

      <div>{etape.contenu}</div>

      {navigation}
    </section>
  )
}
