'use client'

import { useState } from 'react'
import Link from 'next/link'
import {
  ArrowDown, Check, Cog, Eye, FileText, FolderPlus, MessageSquare, Package,
  PenLine, Search, Sparkles, AlertTriangle, Terminal, Mic, Clapperboard,
  BookOpen, ListOrdered, Calculator, ChartColumn,
} from 'lucide-react'
import { AddToCartButton } from '@/components/cart/AddToCartButton'
import { CodeBlock } from '@/components/ui/code-block'
import { AI_PACKAGES, SKILL_PACKS, packageIncludes } from '@/data/ai-packages'
import type { AIPackage, SkillPackId } from '@/data/ai-packages'
import type { SkillPageConfig, SkillPageStep } from '@/data/skill-pages'
import { archiveName, pythonDepsCommands, skillPackInstallVariants } from '@/lib/skill-install'
import { cn } from '@/lib/utils'
import type { CartItem } from '@/types/cart-theme'

const ICONES: Record<SkillPageStep['icone'], typeof Cog> = {
  FolderPlus, PenLine, Cog, Eye, FileText, Search, Sparkles, Mic, Clapperboard,
  BookOpen, ListOrdered, Calculator, ChartColumn,
}

const COULEURS_ETAPES = [
  'border-emerald-500/40 text-emerald-300',
  'border-sky-500/40 text-sky-300',
  'border-amber-500/40 text-amber-300',
  'border-violet-500/40 text-violet-300',
]

type Systeme = 'windows' | 'unix'

/**
 * Bloc affiché sous le diaporama d'un skill :
 * le flux de l'agent, le pack à ajouter au panier et les commandes d'installation.
 */
export function SkillPackPanel({ config }: { config: SkillPageConfig }) {
  const pack = SKILL_PACKS.find(p => p.id === config.packId)
  if (!pack) return null

  return (
    <div className="space-y-6">
      {/* 1. Le flux : la demande, les quatre étapes, le résultat */}
      <section className="glass-card rounded-xl p-6">
        <h2 className="text-xl font-bold mb-4">Ce que fait l'agent</h2>

        <div className="flex justify-center">
          <div className="max-w-xl rounded-2xl rounded-bl-sm border border-sky-500/40 bg-sky-950/30 px-4 py-3">
            <div className="text-xs font-semibold text-sky-300 mb-1 flex items-center gap-1">
              <MessageSquare className="w-3.5 h-3.5" /> Vous
            </div>
            <p className="text-sm">« {config.demandeExemple} »</p>
          </div>
        </div>

        <div className="flex justify-center my-3 text-muted-foreground"><ArrowDown className="w-5 h-5" /></div>

        <ol className="grid gap-3 md:grid-cols-4">
          {config.etapes.map((etape, i) => {
            const Icone = ICONES[etape.icone]
            return (
              <li
                key={etape.nom}
                className={cn('rounded-lg border bg-white/5 p-4', COULEURS_ETAPES[i % COULEURS_ETAPES.length])}
              >
                <div className="flex items-center gap-2 font-semibold">
                  <Icone className="w-5 h-5" />
                  <span>{i + 1}. {etape.nom}</span>
                </div>
                <p className="mt-2 text-sm text-white/80">{etape.quoi}</p>
                <p className="mt-2 text-xs text-white/40 font-mono">{etape.skill}</p>
              </li>
            )
          })}
        </ol>

        <div className="flex justify-center my-3 text-muted-foreground"><ArrowDown className="w-5 h-5" /></div>

        <div className="flex justify-center">
          <div className="rounded-lg bg-gradient-to-r from-red-500 to-rose-600 px-4 py-2 text-sm font-semibold text-white flex items-center gap-2">
            <FileText className="w-4 h-4" /> {config.resultat}
          </div>
        </div>

        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div>
            <h3 className="font-semibold mb-2">Ce que vous obtenez</h3>
            <ul className="space-y-1.5 text-sm text-muted-foreground">
              {config.obtient.map(o => (
                <li key={o} className="flex gap-2"><Check className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />{o}</li>
              ))}
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-2">Pour le lancer</h3>
            <p className="text-sm text-muted-foreground">{config.invocation}</p>
          </div>
        </div>
      </section>

      {/* 2. Le pack */}
      <SkillPackCard pack={pack} diaporama />

      {/* 3. Installation */}
      <SkillPackInstall pack={pack} prerequis={config.prerequis} />
    </div>
  )
}

/**
 * Le pack : contenu, bouton « Ajouter au panier », bundles qui l'incluent déjà.
 * Réutilisable hors d'une page de skill (tutoriels).
 */
export function SkillPackCard({ pack, diaporama = false }: { pack: AIPackage<SkillPackId>; diaporama?: boolean }) {
  const cartItem: CartItem = {
    id: `package-${pack.id}`,
    name: `Pack ${pack.name}`,
    type: 'package',
    path: '',
    description: pack.subtitle,
  }

  return (
    <section className="glass-card rounded-xl p-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
        <div>
          <h2 className="text-xl font-bold flex items-center gap-2">
            <Package className="w-5 h-5 text-cosmic-300" /> Le pack « {pack.name} »
          </h2>
          <p className="text-sm text-muted-foreground mt-1">
            Tout ce qu'il faut pour ce flux, et rien d'autre : une archive <code className="text-cosmic-300">{archiveName(pack.id)}</code> qui
            contient un dossier <code className="text-cosmic-300">.claude/</code>.
          </p>
          <ul className="mt-3 space-y-1 text-sm text-white/70">
            {pack.highlights.map(h => (
              <li key={h} className="flex gap-2"><Check className="w-4 h-4 mt-0.5 shrink-0 text-cosmic-300" />{h}</li>
            ))}
            {diaporama && (
              <li className="flex gap-2"><Check className="w-4 h-4 mt-0.5 shrink-0 text-cosmic-300" />Le diaporama de cette page, dans <code className="text-cosmic-300">.claude/diaporama/</code></li>
            )}
            {pack.annexes !== null && (
              <li className="flex gap-2"><Check className="w-4 h-4 mt-0.5 shrink-0 text-cosmic-300" />{pack.annexes ?? 'Les modèles, guides et scripts Python dont ces skills ont besoin'}</li>
            )}
          </ul>
          {(() => {
            // Bundles qui contiennent déjà tous les skills du pack (calculé, pas écrit en dur)
            const bundles = AI_PACKAGES.filter(b => packageIncludes(b.id, pack.id)).map(b => b.name)
            if (bundles.length === 0) return null
            return (
              <p className="mt-3 text-xs text-white/40">
                Déjà inclus dans {bundles.length > 1 ? 'les bundles' : 'le bundle'}{' '}
                <Link href="/claude-code/download-ai-packages" className="underline hover:text-white/70">
                  {bundles.length > 1 ? `${bundles.slice(0, -1).join(', ')} et ${bundles[bundles.length - 1]}` : bundles[0]}
                </Link>.
              </p>
            )
          })()}
        </div>
        <div className="md:w-60 shrink-0">
          <AddToCartButton item={cartItem} className="w-full" variant="cosmic" />
          <p className="mt-2 text-xs text-white/40 text-center">Puis téléchargez depuis le panier.</p>
        </div>
      </div>
    </section>
  )
}

/**
 * Installation d'un pack : bascule Windows / macOS-Linux, quatre variantes
 * (Claude Code et Codex, projet et global), modules Python, prérequis, encart Codex.
 */
export function SkillPackInstall({
  pack,
  prerequis,
}: {
  pack: AIPackage<SkillPackId>
  prerequis: SkillPageConfig['prerequis']
}) {
  const [systeme, setSysteme] = useState<Systeme>('windows')
  const variantes = skillPackInstallVariants(pack.id)
  const deps = pack.pythonDeps ? pythonDepsCommands(pack.pythonDeps) : null

  return (
    <section className="glass-card rounded-xl p-6">
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <h2 className="text-xl font-bold flex items-center gap-2"><Terminal className="w-5 h-5" /> Installer le pack</h2>
        <div className="inline-flex rounded-lg border border-white/10 p-1 text-sm">
          {(['windows', 'unix'] as Systeme[]).map(s => (
            <button
              key={s}
              onClick={() => setSysteme(s)}
              className={cn(
                'px-3 py-1 rounded-md transition-colors',
                systeme === s ? 'bg-cosmic-500/30 text-white' : 'text-white/50 hover:text-white/80'
              )}
            >
              {s === 'windows' ? 'Windows (PowerShell)' : 'macOS / Linux'}
            </button>
          ))}
        </div>
      </div>

      <p className="text-sm text-muted-foreground mb-4">
        Les commandes partent de l'archive dans le dossier Téléchargements (adaptez le chemin sinon).
        Pour une installation dans un projet, ouvrez le terminal dans le dossier du projet.
      </p>

      <div className="grid gap-4 lg:grid-cols-2">
        {variantes.map(v => (
          <div
            key={v.id}
            className={cn(
              'rounded-lg border p-4',
              v.recommande ? 'border-emerald-500/30 bg-emerald-950/10' : 'border-amber-500/30 bg-amber-950/10'
            )}
          >
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="font-semibold">{v.outil}, {v.portee === 'projet' ? 'dans le projet' : 'global'}</span>
              <span
                className={cn(
                  'text-xs font-semibold px-2 py-0.5 rounded-full',
                  v.recommande ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                )}
              >
                {v.recommande ? 'recommandé' : 'déconseillé'}
              </span>
            </div>
            <p className="text-xs text-white/60 mb-3">
              Skills dans <code className="text-cosmic-300">{v.dossier}</code>. {v.explication}
            </p>
            <CodeBlock
              code={systeme === 'windows' ? v.windows : v.unix}
              language={systeme === 'windows' ? 'powershell' : 'bash'}
              filename={systeme === 'windows' ? 'PowerShell' : 'Terminal'}
            />
          </div>
        ))}
      </div>

      {deps && (
        <div className="mt-4">
          <h3 className="font-semibold mb-2">Modules Python (une fois pour toutes)</h3>
          <CodeBlock
            code={systeme === 'windows' ? deps.windows : deps.unix}
            language={systeme === 'windows' ? 'powershell' : 'bash'}
            filename={systeme === 'windows' ? 'PowerShell' : 'Terminal'}
          />
        </div>
      )}

      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <div>
          <h3 className="font-semibold mb-2">Prérequis</h3>
          <ul className="space-y-1.5 text-sm text-muted-foreground">
            {prerequis.map(p => (
              <li key={p.texte} className="flex gap-2">
                <Check className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />
                <span>
                  {p.texte}{' '}
                  {p.lien && <Link href={p.lien.href} className="underline text-cosmic-300 hover:text-cosmic-200">{p.lien.label}</Link>}
                </span>
              </li>
            ))}
          </ul>
        </div>
        <div className="rounded-lg border border-amber-500/20 bg-amber-950/10 p-3 text-xs text-white/60 flex gap-2">
          <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400 mt-0.5" />
          <p>
            <strong className="text-amber-300">Avec Codex</strong> : les fiches des skills citent leurs scripts
            sous <code>.claude/skills/</code>. Dites à Codex, ou écrivez dans votre <code>AGENTS.md</code>, que
            les skills sont installés dans <code>.agents/skills/</code>.
          </p>
        </div>
      </div>
    </section>
  )
}
