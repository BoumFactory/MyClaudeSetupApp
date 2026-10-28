"use client"

/**
 * Section « Tout installer en une commande » du tutoriel de configuration.
 *
 * Les commandes appellent les scripts statiques de public/installer/ :
 * claude.ps1, codex.ps1 (Windows) et claude.sh, codex.sh (macOS / Linux).
 * Ces scripts récupèrent public/download/Claude-Code-Setup/ du dépôt GitHub public
 * par un clone Git partiel, puis le copient dans ./.claude ou ./.agents.
 */

import { useState } from "react"
import Link from "next/link"
import { CheckCircle, GitBranch, RefreshCw, ShieldCheck, Terminal, Zap } from "lucide-react"
import { CodeBlock } from "@/components/ui/code-block"
import { cn } from "@/lib/utils"

type Systeme = "windows" | "unix"

const SITE = "https://bfcours.dev/installer"

const OUTILS = [
  {
    id: "claude",
    nom: "Claude Code",
    dossier: ".claude/",
    instructions: "CLAUDE.md",
    windows: `irm ${SITE}/claude.ps1 | iex`,
    unix: `curl -fsSL ${SITE}/claude.sh | bash`,
    legerWindows: `$env:BFCOURS_LEGER = "1"; irm ${SITE}/claude.ps1 | iex`,
    legerUnix: `curl -fsSL ${SITE}/claude.sh | BFCOURS_LEGER=1 bash`,
  },
  {
    id: "codex",
    nom: "Codex et autres agents",
    dossier: ".agents/",
    instructions: "AGENTS.md",
    windows: `irm ${SITE}/codex.ps1 | iex`,
    unix: `curl -fsSL ${SITE}/codex.sh | bash`,
    legerWindows: `$env:BFCOURS_LEGER = "1"; irm ${SITE}/codex.ps1 | iex`,
    legerUnix: `curl -fsSL ${SITE}/codex.sh | BFCOURS_LEGER=1 bash`,
  },
] as const

export function InstallerConfigCommande() {
  const [systeme, setSysteme] = useState<Systeme>("windows")
  const shell = systeme === "windows" ? "PowerShell" : "Terminal"
  const langage = systeme === "windows" ? "powershell" : "bash"

  return (
    <section id="une-commande" className="glass-card rounded-xl p-8 space-y-6 border-2 border-emerald-500/30 scroll-mt-24">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Tout installer en une commande</h2>
        </div>
        <div className="inline-flex rounded-lg border border-white/10 p-1 text-sm">
          {(["windows", "unix"] as Systeme[]).map(s => (
            <button
              key={s}
              onClick={() => setSysteme(s)}
              className={cn(
                "px-3 py-1 rounded-md transition-colors",
                systeme === s ? "bg-cosmic-500/30 text-white" : "text-white/50 hover:text-white/80"
              )}
            >
              {s === "windows" ? "Windows (PowerShell)" : "macOS / Linux"}
            </button>
          ))}
        </div>
      </div>

      <p className="text-muted-foreground">
        Ouvrez un terminal <strong className="text-foreground">dans le dossier de votre projet</strong>,
        collez la commande de votre outil et validez. Toute la configuration arrive dans le projet.
      </p>

      <div className="grid gap-4 lg:grid-cols-2">
        {OUTILS.map(o => (
          <div key={o.id} className="rounded-lg border border-emerald-500/30 bg-emerald-950/10 p-4 space-y-3">
            <div>
              <h3 className="font-semibold text-lg">{o.nom}</h3>
              <p className="text-xs text-white/60">
                Configuration dans <code className="text-cosmic-300">{o.dossier}</code>, instructions
                dans <code className="text-cosmic-300">{o.instructions}</code>.
              </p>
            </div>
            <CodeBlock code={systeme === "windows" ? o.windows : o.unix} language={langage} filename={shell} />
          </div>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg bg-slate-950/50 border border-slate-800 p-4 space-y-2">
          <h3 className="font-semibold flex items-center gap-2">
            <Terminal className="w-4 h-4 text-nebula-400" />
            Ce que fait la commande
          </h3>
          <ul className="text-sm text-muted-foreground space-y-1.5">
            <li className="flex gap-2"><CheckCircle className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />Elle télécharge la configuration seule, sans le reste du site (environ 30 Mo).</li>
            <li className="flex gap-2"><CheckCircle className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />Elle copie agents, skills, commandes et serveurs MCP dans le dossier de l'outil.</li>
            <li className="flex gap-2"><CheckCircle className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />Elle crée le fichier d'instructions s'il n'existe pas encore. Un fichier existant n'est pas touché.</li>
            <li className="flex gap-2"><CheckCircle className="w-4 h-4 mt-0.5 shrink-0 text-emerald-400" />Elle affiche à la fin les modules Python à installer pour certains skills.</li>
          </ul>
        </div>

        <div className="space-y-3">
          <div className="rounded-lg bg-blue-950/30 border border-blue-800 p-4">
            <h3 className="font-semibold flex items-center gap-2 text-blue-300">
              <ShieldCheck className="w-4 h-4" />
              Dossier déjà présent ?
            </h3>
            <p className="text-sm text-muted-foreground mt-1">
              La commande le sauvegarde d'abord, par exemple dans <code className="text-blue-300">.claude.sauvegarde-20261028-1430</code>.
              Ensuite, elle ajoute la configuration : vos propres fichiers restent en place.
            </p>
          </div>
          <div className="rounded-lg bg-emerald-950/30 border border-emerald-800 p-4">
            <h3 className="font-semibold flex items-center gap-2 text-emerald-300">
              <RefreshCw className="w-4 h-4" />
              Mettre à jour
            </h3>
            <p className="text-sm text-muted-foreground mt-1">
              Relancez la même commande. Vous récupérez la dernière version publiée.
            </p>
          </div>
        </div>
      </div>

      <div className="flex items-start gap-3 bg-amber-950/20 border border-amber-700/50 rounded-lg p-4">
        <GitBranch className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
        <div className="text-sm text-muted-foreground space-y-1">
          <p>
            <strong className="text-amber-300">Git est nécessaire.</strong> Sans lui, la commande s'arrête
            et ne modifie rien.{" "}
            <Link href="/claude-code/tutorials/git-install" className="underline text-amber-300 hover:text-amber-200" prefetch={false}>
              Installer Git
            </Link>
          </p>
        </div>
      </div>

      <details className="rounded-lg border border-white/10 p-4">
        <summary className="cursor-pointer font-semibold">Version allégée (sans les deux skills les plus lourds)</summary>
        <div className="mt-3 space-y-3 text-sm text-muted-foreground">
          <p>
            Les skills <code className="text-cosmic-300">h5p-branching-scenario</code> et{" "}
            <code className="text-cosmic-300">programmes-officiels</code> pèsent à eux deux près de 80 Mo sur le disque.
            Cette variante les laisse de côté : le téléchargement passe d'environ 30 Mo à 15 Mo.
          </p>
          {systeme === "windows" && (
            <p>Sous Windows, le réglage reste actif jusqu'à la fermeture du terminal.</p>
          )}
          {OUTILS.map(o => (
            <div key={o.id} className="space-y-1">
              <p className="font-medium text-foreground">{o.nom}</p>
              <CodeBlock code={systeme === "windows" ? o.legerWindows : o.legerUnix} language={langage} filename={shell} />
            </div>
          ))}
        </div>
      </details>
    </section>
  )
}
