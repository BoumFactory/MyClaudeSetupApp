import Link from "next/link"
import {
  Monitor,
  Download,
  CheckCircle,
  AlertCircle,
  Settings,
  Code2,
  ExternalLink,
  Apple,
  Laptop,
  Play,
  FolderOpen,
  GitBranch,
  Zap,
  Layers,
  Terminal,
  MousePointer,
  ArrowRight,
  Sparkles,
  Cable,
  Eye
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation de Claude Desktop | Tutoriels",
  description:
    "Guide complet pour installer Claude Desktop et activer Claude Code. Découvrez comment utiliser l'interface graphique pour coder avec l'IA.",
}

export default function ClaudeDesktopInstallPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="claude-desktop-install" title="Installation de Claude Desktop" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Claude Desktop", href: "/claude-code/tutorials/claude-desktop-install" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Monitor className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation de Claude Desktop
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          L'application de bureau officielle d'Anthropic avec interface graphique
          et Claude Code intégré
        </p>
      </section>

      {/* Point d'entrée idéal pour débutants */}
      <section className="glass-card rounded-xl p-6 border-2 border-emerald-500/50 bg-emerald-950/20">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-600 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-6 h-6 text-white" />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-bold text-emerald-300">Le point d'entrée idéal pour débuter</h2>
            <p className="text-muted-foreground">
              Si vous découvrez Claude Code, <strong className="text-emerald-300">Claude Desktop est fait pour vous</strong>.
              Interface graphique intuitive, pas de terminal à apprendre, tout se fait en quelques clics.
            </p>
            <div className="grid md:grid-cols-2 gap-3 mt-4">
              <div className="p-3 rounded-lg bg-emerald-950/40 border border-emerald-800">
                <p className="text-sm font-semibold text-emerald-300 mb-1">Pas besoin de VS Code</p>
                <p className="text-xs text-muted-foreground">
                  Claude Desktop est autonome. Vous pouvez créer, modifier et gérer vos projets directement dedans.
                </p>
              </div>
              <div className="p-3 rounded-lg bg-amber-950/40 border border-amber-800">
                <p className="text-sm font-semibold text-amber-300 mb-1">MikTeX toujours requis pour LaTeX</p>
                <p className="text-xs text-muted-foreground">
                  Pour compiler des documents LaTeX, vous aurez toujours besoin de MikTeX installé sur votre machine.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Qu'est-ce que Claude Desktop */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Monitor className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Qu'est-ce que Claude Desktop ?</h2>
        </div>

        <p className="text-muted-foreground">
          Claude Desktop est l'application native d'Anthropic pour Windows et macOS. Elle offre
          une interface graphique complète pour interagir avec Claude, avec trois modes de travail :
        </p>

        <div className="grid md:grid-cols-3 gap-4 mt-6">
          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <MousePointer className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">Chat</h3>
              <p className="text-sm text-muted-foreground">
                Interface conversationnelle classique (comme claude.ai)
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <Zap className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">Cowork</h3>
              <p className="text-sm text-muted-foreground">
                Agent autonome qui travaille en arrière-plan
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-emerald-950/30 border border-emerald-800">
            <Code2 className="w-6 h-6 text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-emerald-300">Code</h3>
              <p className="text-sm text-muted-foreground">
                Claude Code avec interface graphique
              </p>
            </div>
          </div>
        </div>

        <div className="mt-4 p-4 bg-emerald-950/30 border border-emerald-500/50 rounded-lg">
          <div className="flex items-start gap-3">
            <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-emerald-300 mb-1">Alternative visuelle au terminal</p>
              <p className="text-sm text-muted-foreground">
                L'onglet <strong className="text-foreground">Code</strong> offre les mêmes fonctionnalités que Claude Code CLI,
                mais avec une interface graphique plus accessible pour ceux qui préfèrent éviter le terminal.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Prérequis */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prérequis</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-slate-950/30 border border-slate-700">
            <div className="flex items-center gap-2 mb-2">
              <Apple className="w-5 h-5 text-slate-400" />
              <h3 className="font-semibold">macOS</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Version <strong className="text-foreground">11 (Big Sur)</strong> ou supérieure
            </p>
          </div>

          <div className="p-4 rounded-lg bg-slate-950/30 border border-slate-700">
            <div className="flex items-center gap-2 mb-2">
              <Laptop className="w-5 h-5 text-blue-400" />
              <h3 className="font-semibold">Windows</h3>
            </div>
            <p className="text-sm text-muted-foreground">
              Version <strong className="text-foreground">10</strong> ou supérieure
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3 mt-4">
          <CheckCircle className="w-5 h-5 text-cosmic-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-semibold">Un compte Claude</p>
            <p className="text-sm text-muted-foreground">
              Gratuit ou payant (Pro/Max recommandé pour Claude Code)
            </p>
          </div>
        </div>

        <div className="flex items-start gap-3">
          <CheckCircle className="w-5 h-5 text-cosmic-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-semibold">Git (optionnel mais recommandé)</p>
            <p className="text-sm text-muted-foreground">
              Nécessaire pour l'isolation des sessions (worktrees)
            </p>
          </div>
        </div>
      </section>

      {/* Étape 1 : Téléchargement */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Télécharger Claude Desktop</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Download className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Téléchargement officiel</CardTitle>
            </div>
            <CardDescription>
              Téléchargez l'application depuis le site officiel d'Anthropic
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Lien vers la page officielle */}
            <div className="text-center">
              <a
                href="https://claude.ai/download"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-3 px-6 py-4 rounded-xl bg-gradient-to-r from-cosmic-600 to-nebula-600 hover:from-cosmic-500 hover:to-nebula-500 transition-all text-white font-semibold text-lg shadow-lg hover:shadow-xl hover:scale-105"
              >
                <Download className="w-6 h-6" />
                Télécharger sur claude.ai/download
                <ExternalLink className="w-5 h-5" />
              </a>
              <p className="text-sm text-muted-foreground mt-3">
                Page officielle de téléchargement Anthropic
              </p>
            </div>

            {/* Indications par OS */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="flex items-center gap-4 p-4 rounded-lg bg-slate-950/50 border border-slate-700">
                <div className="w-12 h-12 rounded-lg bg-slate-800 flex items-center justify-center">
                  <Apple className="w-7 h-7 text-slate-300" />
                </div>
                <div className="flex-1">
                  <p className="font-semibold">macOS</p>
                  <p className="text-sm text-muted-foreground">Intel & Apple Silicon (.dmg)</p>
                </div>
              </div>

              <div className="flex items-center gap-4 p-4 rounded-lg bg-slate-950/50 border border-slate-700">
                <div className="w-12 h-12 rounded-lg bg-blue-950 flex items-center justify-center">
                  <Laptop className="w-7 h-7 text-blue-400" />
                </div>
                <div className="flex-1">
                  <p className="font-semibold">Windows</p>
                  <p className="text-sm text-muted-foreground">x64 et ARM64 (.exe)</p>
                </div>
              </div>
            </div>

            <div className="p-3 bg-slate-950/50 border border-slate-700 rounded-lg text-sm text-muted-foreground">
              <strong className="text-foreground">Note Windows ARM64 :</strong> Les sessions locales ne sont pas disponibles sur ARM64, utilisez les sessions distantes à la place.
            </div>

            <div className="flex items-start gap-2 bg-amber-950/30 border border-amber-800 rounded-lg p-3">
              <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-amber-300">Linux non supporté :</strong> Claude Desktop n'est pas disponible sur Linux.
                Utilisez <Link href="/claude-code/tutorials/claude-code-install" className="text-cosmic-400 hover:underline">Claude Code CLI</Link> à la place.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 2 : Installation */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Installer l'application</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* macOS */}
          <Card className="glass-card">
            <CardHeader>
              <div className="flex items-center gap-3">
                <Apple className="w-6 h-6 text-slate-300" />
                <CardTitle>Installation macOS</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                    1
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Double-cliquez sur le fichier <code className="px-1 py-0.5 bg-slate-900 rounded">.dmg</code> téléchargé
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                    2
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Glissez l'icône Claude vers le dossier <strong className="text-foreground">Applications</strong>
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                    3
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Éjectez le disque virtuel et lancez Claude depuis Applications
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Windows */}
          <Card className="glass-card">
            <CardHeader>
              <div className="flex items-center gap-3">
                <Laptop className="w-6 h-6 text-blue-400" />
                <CardTitle>Installation Windows</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
                    1
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Double-cliquez sur le fichier <code className="px-1 py-0.5 bg-slate-900 rounded">.exe</code> téléchargé
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
                    2
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Suivez les instructions de l'installateur
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white text-xs font-bold">
                    3
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Lancez Claude depuis le menu <strong className="text-foreground">Démarrer</strong>
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Étape 3 : Connexion */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <h2 className="text-3xl font-bold">Se connecter</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Play className="w-6 h-6 text-emerald-400" />
              <CardTitle>Premier lancement</CardTitle>
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-3">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  1
                </div>
                <p className="text-sm text-muted-foreground">
                  Lancez Claude depuis le dossier Applications (macOS) ou le menu Démarrer (Windows)
                </p>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  2
                </div>
                <p className="text-sm text-muted-foreground">
                  Connectez-vous avec votre compte Claude (email + mot de passe ou SSO)
                </p>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  3
                </div>
                <p className="text-sm text-muted-foreground">
                  Vous arrivez sur l'interface principale avec les onglets <strong className="text-foreground">Chat</strong>, <strong className="text-foreground">Cowork</strong> et <strong className="text-foreground">Code</strong>
                </p>
              </div>
            </div>

            <div className="p-4 bg-cosmic-950/30 border border-cosmic-800 rounded-lg">
              <p className="text-sm text-muted-foreground">
                <strong className="text-cosmic-300">Note :</strong> L'application est gratuite à télécharger et utiliser.
                Les fonctionnalités disponibles dépendent de votre abonnement (Free, Pro, Max, Team, Enterprise).
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 4 : Activer Claude Code */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            4
          </div>
          <h2 className="text-3xl font-bold">Activer Claude Code</h2>
        </div>

        <Card className="glass-card border-2 border-emerald-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Code2 className="w-6 h-6 text-emerald-400" />
              <CardTitle>Utiliser l'onglet Code</CardTitle>
            </div>
            <CardDescription>
              Claude Code est intégré directement dans l'application desktop
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium mb-1">Cliquez sur l'onglet "Code"</p>
                  <p className="text-sm text-muted-foreground">
                    En haut à gauche de l'interface, cliquez sur <strong className="text-emerald-300">Code</strong>
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium mb-1">Choisissez le type de session</p>
                  <div className="grid md:grid-cols-2 gap-3 mt-2">
                    <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-800">
                      <p className="font-semibold text-emerald-300 text-sm mb-1">Local</p>
                      <p className="text-xs text-muted-foreground">
                        Exécute Claude sur votre machine avec accès direct à vos fichiers
                      </p>
                    </div>
                    <div className="p-3 rounded-lg bg-blue-950/30 border border-blue-800">
                      <p className="font-semibold text-blue-300 text-sm mb-1">Remote</p>
                      <p className="text-xs text-muted-foreground">
                        Exécute dans le cloud, continue même si vous fermez l'app
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium mb-1">Sélectionnez un dossier projet</p>
                  <p className="text-sm text-muted-foreground">
                    Cliquez sur <strong className="text-foreground">Select folder</strong> et choisissez le répertoire de votre projet
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  4
                </div>
                <div>
                  <p className="font-medium mb-1">Commencez à coder !</p>
                  <p className="text-sm text-muted-foreground">
                    Tapez ce que vous voulez faire, par exemple :
                  </p>
                  <div className="mt-2 space-y-1 text-sm font-mono text-cosmic-300">
                    <p>"Trouve les TODO et corrige-les"</p>
                    <p>"Ajoute des tests pour la fonction principale"</p>
                    <p>"Crée un CLAUDE.md pour ce projet"</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Modes de permission */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Eye className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Modes de permission</h2>
        </div>

        <p className="text-muted-foreground">
          Contrôlez comment Claude travaille avec le sélecteur de mode à côté du bouton d'envoi :
        </p>

        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 rounded-lg bg-amber-950/30 border border-amber-800">
            <h3 className="font-semibold text-amber-300 mb-2">Ask (recommandé)</h3>
            <p className="text-sm text-muted-foreground">
              Claude demande votre approbation avant chaque modification de fichier ou commande.
              Vous voyez un diff et pouvez accepter ou rejeter.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-emerald-950/30 border border-emerald-800">
            <h3 className="font-semibold text-emerald-300 mb-2">Code</h3>
            <p className="text-sm text-muted-foreground">
              Claude applique automatiquement les modifications de fichiers mais demande
              avant d'exécuter des commandes terminal.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-blue-950/30 border border-blue-800">
            <h3 className="font-semibold text-blue-300 mb-2">Plan</h3>
            <p className="text-sm text-muted-foreground">
              Claude crée un plan détaillé pour votre approbation avant de faire
              quoi que ce soit. Idéal pour les tâches complexes.
            </p>
          </div>
        </div>
      </section>

      {/* Sessions parallèles */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Layers className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Sessions parallèles</h2>
        </div>

        <div className="flex items-start gap-3">
          <GitBranch className="w-5 h-5 text-cosmic-400 mt-0.5 flex-shrink-0" />
          <div>
            <p className="text-muted-foreground">
              Cliquez sur <strong className="text-foreground">+ New session</strong> dans la barre latérale
              pour travailler sur plusieurs tâches en parallèle.
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              Pour les dépôts Git, chaque session obtient sa propre copie isolée du projet (worktrees).
              Les modifications d'une session n'affectent pas les autres jusqu'au commit.
            </p>
          </div>
        </div>

        <div className="p-4 bg-cosmic-950/30 border border-cosmic-800 rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong className="text-cosmic-300">Note :</strong> L'isolation des sessions nécessite Git.
            Sans Git, les sessions dans le même répertoire modifient les mêmes fichiers.
          </p>
        </div>
      </section>

      {/* Connecteurs */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Cable className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Connecteurs (extensions)</h2>
        </div>

        <p className="text-muted-foreground">
          Pour les sessions locales, cliquez sur <strong className="text-foreground">...</strong> avant de démarrer
          et sélectionnez <strong className="text-foreground">Connectors</strong> pour ajouter des intégrations :
        </p>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {["Google Calendar", "Slack", "GitHub", "Linear", "Notion", "Gmail", "Drive", "Et plus..."].map((connector) => (
            <div key={connector} className="p-3 rounded-lg bg-slate-950/50 border border-slate-700 text-center">
              <p className="text-sm font-medium">{connector}</p>
            </div>
          ))}
        </div>

        <div className="p-4 bg-nebula-950/30 border border-nebula-800 rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong className="text-nebula-300">MCP intégré :</strong> Les connecteurs sont des serveurs MCP
            pré-configurés. Vous pouvez aussi ajouter vos propres serveurs MCP via les fichiers de configuration.
          </p>
        </div>
      </section>

      {/* CLI vs Desktop */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Terminal className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Desktop vs CLI</h2>
        </div>

        <p className="text-muted-foreground">
          Desktop et CLI utilisent le même moteur. Vous pouvez utiliser les deux simultanément.
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h3 className="font-semibold text-emerald-300">Desktop ajoute :</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>Interface graphique avec gestion visuelle des sessions</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>Connecteurs intégrés pour les intégrations courantes</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-emerald-400 mt-0.5 flex-shrink-0" />
                <span>Isolation automatique des sessions (worktrees)</span>
              </li>
            </ul>
          </div>

          <div className="space-y-3">
            <h3 className="font-semibold text-cosmic-300">CLI ajoute :</h3>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
                <span>Fournisseurs API tiers (Bedrock, Vertex, Foundry)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
                <span>Flags CLI pour le scripting (--print, --resume)</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
                <span>Usage programmatique via l'Agent SDK</span>
              </li>
            </ul>
          </div>
        </div>

        <div className="p-4 bg-blue-950/30 border border-blue-800 rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong className="text-blue-300">Configuration partagée :</strong> Les fichiers CLAUDE.md, serveurs MCP,
            hooks et skills sont partagés entre Desktop et CLI.
          </p>
        </div>
      </section>

      {/* Documentation */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <ExternalLink className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Documentation officielle</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <a
            href="https://support.claude.com/en/articles/10065433-installing-claude-desktop"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 transition-colors group"
          >
            <Monitor className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                Installation Claude Desktop
                <ExternalLink className="w-3 h-3" />
              </h4>
              <p className="text-xs text-muted-foreground">
                Guide officiel d'installation
              </p>
            </div>
          </a>

          <a
            href="https://code.claude.com/docs/en/desktop"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 transition-colors group"
          >
            <Code2 className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                Claude Code on Desktop
                <ExternalLink className="w-3 h-3" />
              </h4>
              <p className="text-xs text-muted-foreground">
                Documentation complète de l'onglet Code
              </p>
            </div>
          </a>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-cosmic-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <ArrowRight className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        </div>

        <p className="text-muted-foreground">
          Maintenant que Claude Desktop est installé, vous pouvez :
        </p>

        <div className="flex flex-wrap gap-3">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/tutorials/claude-code-config" prefetch={false}>
              Configurer mes outils personnalisés
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/tutorials/claude-code-install" prefetch={false}>
              Installer Claude Code CLI
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
