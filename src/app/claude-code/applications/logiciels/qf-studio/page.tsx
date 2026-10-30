import { Download, Zap, RefreshCw, MonitorDown, Package, ArrowRight } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "QF-Studio | Logiciels Enseignants",
  description: "Application de bureau pour créer et projeter des questions flash, avec mise à jour automatique",
}

// ────────────────────────────────────────────────────────────────────
// QF-Studio — application desktop de questions flash (Tauri v2, Windows)
// Distribuee depuis la zone d'auto-update gelee. A CHAQUE release, mettre
// a jour QFSTUDIO_VERSION et remplacer QFSTUDIO_LATEST_NOTES par les notes
// de la NOUVELLE version uniquement. L'historique complet des versions est
// desormais consultable directement dans l'application (tableau de bord).
// (Le binaire est depose dans public/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio/)
// La mise a jour automatique ne depend PAS de cette page : l'application
// lit seulement latest.json et les fichiers voisins de la zone gelee.
// ────────────────────────────────────────────────────────────────────
const QFSTUDIO_VERSION = "0.1.5"
const QFSTUDIO_BASE = "https://bfcours.dev/7gOdepBMu5OY2QBKBcd7mGyA/qfstudio"
const QFSTUDIO_INSTALLER = `${QFSTUDIO_BASE}/QF-Studio_${QFSTUDIO_VERSION}_x64-setup.exe`
const QFSTUDIO_LATEST_NOTES: { version: string; date: string; items: string[] } = {
  version: "0.1.5",
  date: "1er juillet 2026",
  items: [
    "Correctif majeur : les modèles de mise en page sont bien installés, la génération de PDF fonctionne dès l'installation.",
    "Calendrier scolaire 2026-2027 ajouté (vacances des zones A, B et C).",
    "Compilation par lot : plus de faux délai d'attente sur les gros lots de modèles.",
  ],
}

export default function QFStudioPage() {
  return (
    <div className="space-y-8">
      <Breadcrumb
        items={[
          { label: "Applications", href: "/claude-code/applications" },
          { label: "Logiciels Enseignants", href: "/claude-code/applications/logiciels" },
          { label: "QF-Studio", href: "/claude-code/applications/logiciels/qf-studio" },
        ]}
      />

      <section className="glass-card rounded-xl p-8 border-2 border-indigo-500/30 space-y-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-40 h-40 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="flex flex-col md:flex-row items-start gap-6">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center flex-shrink-0 shadow-lg shadow-indigo-500/30">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <div className="flex-1 space-y-4">
            <div className="flex flex-wrap items-center gap-3">
              <h1 className="text-3xl font-bold text-indigo-300">QF-Studio</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-indigo-500/15 text-indigo-300 font-medium">
                Windows
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400 font-mono">
                v{QFSTUDIO_VERSION}
              </span>
              <span className="inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-300 font-medium">
                <RefreshCw className="w-3 h-3" />
                Mise à jour automatique
              </span>
            </div>
            <p className="text-muted-foreground leading-relaxed">
              Application de bureau pour créer et projeter des <strong>questions flash</strong> en classe.
              Une fois installée, elle se met à jour <strong>toute seule</strong> : vous bénéficiez
              automatiquement des dernières versions et du contenu officiel, sans réinstaller quoi que ce soit.
            </p>
            <div className="flex flex-wrap gap-1.5">
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Application desktop</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Questions flash</span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Auto-update</span>
            </div>
            <div className="flex flex-wrap items-center gap-3 pt-1">
              <Button asChild variant="nebula" className="w-full sm:w-auto">
                <a href={QFSTUDIO_INSTALLER} download>
                  <MonitorDown className="w-4 h-4 mr-2" />
                  Télécharger pour Windows (v{QFSTUDIO_VERSION})
                </a>
              </Button>
              <p className="text-xs text-muted-foreground inline-flex items-center gap-1">
                <Download className="w-3 h-3" />
                Installeur .exe — installez une fois, les mises à jour suivent toutes seules.
              </p>
            </div>

            {/* Prérequis LaTeX — packages bfcours pour compiler les documents générés */}
            <Link
              href="/claude-code/download-latex-packages"
              prefetch={false}
              className="group flex items-center gap-3 rounded-lg border border-cosmic-500/30 bg-cosmic-950/20 p-4 hover:border-cosmic-400/50 transition-all duration-300"
            >
              <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
                <Package className="w-5 h-5 text-white" />
              </div>
              <div className="flex-1">
                <p className="text-sm font-semibold text-cosmic-300 group-hover:text-cosmic-200 transition-colors">
                  Prérequis : packages LaTeX bfcours
                </p>
                <p className="text-xs text-muted-foreground">
                  QF-Studio génère des documents LaTeX. Installez le package <strong>bfcours</strong> pour les compiler.
                </p>
              </div>
              <ArrowRight className="w-5 h-5 text-cosmic-400 flex-shrink-0 group-hover:translate-x-1 transition-transform" />
            </Link>

            {/* Notes de la derniere version — l'historique complet est dans l'app */}
            <div className="pt-2 space-y-3">
              <div className="flex items-baseline justify-between gap-2 flex-wrap">
                <h2 className="text-sm font-semibold text-indigo-300/90">Nouveautés de cette version</h2>
                <span className="text-xs text-muted-foreground">
                  Historique complet des versions dans l&apos;application.
                </span>
              </div>
              <div className="rounded-lg bg-white/5 p-3">
                <div className="flex items-baseline gap-2">
                  <span className="font-mono text-sm text-indigo-300">v{QFSTUDIO_LATEST_NOTES.version}</span>
                  <span className="text-xs text-muted-foreground">— {QFSTUDIO_LATEST_NOTES.date}</span>
                </div>
                <ul className="mt-1.5 space-y-1 text-sm text-muted-foreground list-disc list-inside">
                  {QFSTUDIO_LATEST_NOTES.items.map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
