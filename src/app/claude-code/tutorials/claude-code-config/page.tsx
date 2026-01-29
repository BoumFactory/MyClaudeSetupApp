import Link from "next/link"
import {
  Settings,
  Download,
  FolderOpen,
  CheckCircle,
  AlertCircle,
  FileText,
  ArrowRight,
  Sparkles,
  Terminal,
  BookOpen,
  ExternalLink,
  Package,
  Zap
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Configuration de Claude Code | Tutoriels",
  description:
    "Guide complet pour configurer Claude Code avec mes outils personnalisés : agents, skills, commandes et serveurs MCP pour l'enseignement.",
}

export default function ClaudeCodeConfigPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="claude-code-config" title="Configuration de Claude Code" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Configuration", href: "/claude-code/tutorials/claude-code-config" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Settings className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Configuration de Claude Code
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Configurez Claude Code avec mes outils personnalisés pour automatiser la création de vos ressources pédagogiques
        </p>
      </section>

      {/* Prérequis */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-2 border-amber-500/30 bg-amber-950/10">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-bold text-amber-300">Prérequis</h2>
            <p className="text-muted-foreground">
              Avant de configurer Claude Code avec mes outils, assurez-vous d'avoir :
            </p>
            <ul className="space-y-2 text-sm text-muted-foreground ml-4">
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                <span><strong className="text-foreground">Claude Code installé</strong> - Suivez le tutoriel d'installation si ce n'est pas fait</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                <span><strong className="text-foreground">Un éditeur de code</strong> - VS Code recommandé</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                <span><strong className="text-foreground">Un répertoire de travail</strong> - Un dossier dédié à vos projets avec Claude</span>
              </li>
            </ul>
            <div className="mt-4">
              <Button asChild variant="outline" size="sm">
                <Link href="/claude-code/tutorials/claude-code-install" className="flex items-center gap-2" prefetch={false}>
                  <Terminal className="w-4 h-4" />
                  Tutoriel d'installation de Claude Code
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Étapes de configuration */}
      <section className="space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Download className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Étapes de configuration</h2>
        </div>

        {/* Étape 1 */}
        <div className="glass-card rounded-xl p-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg">
              1
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                  <Download className="w-5 h-5 text-nebula-400" />
                  Accéder à la page de téléchargement
                </h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Rendez-vous sur la page de téléchargement pour accéder aux fichiers de configuration :
                </p>
                <Button asChild variant="cosmic" size="sm">
                  <Link href="/claude-code/downloads" className="flex items-center gap-2" prefetch={false}>
                    <Download className="w-4 h-4" />
                    Accéder aux téléchargements
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Étape 2 */}
        <div className="glass-card rounded-xl p-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg">
              2
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                  <FolderOpen className="w-5 h-5 text-nebula-400" />
                  Sélectionner les fichiers dans Claude-Code-Setup
                </h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Dans l'arborescence des fichiers, naviguez vers le dossier <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">Claude-Code-Setup</code> et sélectionnez :
                </p>

                <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm border border-slate-800 space-y-2 mb-4">
                  <div className="text-muted-foreground">
                    <span className="text-nebula-300">Claude-Code-Setup/</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-emerald-400">├── claude-setup/</span> <span className="text-xs text-emerald-300">← Sélectionnez ce dossier entier</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">├── CLAUDE-autoAmelioration.md</span> <span className="text-xs text-muted-foreground">← Version avancée</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">├── CLAUDE-simple.md</span> <span className="text-xs text-muted-foreground">← Version simple (recommandé pour débuter)</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">├── README.md</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">└── settings.json</span>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-3">
                    <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm text-emerald-300 font-medium">Fichiers à sélectionner :</p>
                      <ul className="text-sm text-muted-foreground mt-1 space-y-1">
                        <li>• Le dossier <code className="px-1 bg-slate-900 rounded text-emerald-300">claude-setup</code> (contient agents, skills, commandes)</li>
                        <li>• Un fichier CLAUDE.md de votre choix (simple ou auto-amélioration)</li>
                      </ul>
                    </div>
                  </div>

                  <div className="flex items-start gap-2 bg-blue-950/30 border border-blue-800 rounded-lg p-3">
                    <AlertCircle className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm text-blue-300 font-medium">Quel fichier CLAUDE.md choisir ?</p>
                      <ul className="text-sm text-muted-foreground mt-1 space-y-1">
                        <li><strong className="text-blue-300">CLAUDE-simple.md</strong> : Pour débuter, instructions de base</li>
                        <li><strong className="text-blue-300">CLAUDE-autoAmelioration.md</strong> : Version avancée avec auto-amélioration</li>
                      </ul>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Étape 3 */}
        <div className="glass-card rounded-xl p-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg">
              3
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-nebula-400" />
                  Télécharger et extraire
                </h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Cliquez sur "Télécharger la sélection" pour obtenir un fichier ZIP, puis extrayez-le.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Étape 4 */}
        <div className="glass-card rounded-xl p-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg">
              4
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                  <FolderOpen className="w-5 h-5 text-nebula-400" />
                  Renommer et placer les fichiers
                </h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Placez les fichiers dans votre répertoire de travail en les renommant correctement :
                </p>

                <div className="space-y-4">
                  {/* Renommer claude-setup */}
                  <div className="bg-slate-950 rounded-lg p-4 border border-slate-800">
                    <p className="text-sm font-medium text-nebula-300 mb-2">1. Renommer le dossier de configuration :</p>
                    <div className="flex items-center gap-3 text-sm">
                      <code className="px-2 py-1 bg-slate-900 rounded text-muted-foreground">claude-setup</code>
                      <ArrowRight className="w-4 h-4 text-nebula-400" />
                      <code className="px-2 py-1 bg-emerald-950 rounded text-emerald-300 font-bold">.claude</code>
                    </div>
                  </div>

                  {/* Renommer CLAUDE.md */}
                  <div className="bg-slate-950 rounded-lg p-4 border border-slate-800">
                    <p className="text-sm font-medium text-nebula-300 mb-2">2. Renommer le fichier d'instructions :</p>
                    <div className="flex items-center gap-3 text-sm">
                      <code className="px-2 py-1 bg-slate-900 rounded text-muted-foreground">CLAUDE-simple.md</code>
                      <ArrowRight className="w-4 h-4 text-nebula-400" />
                      <code className="px-2 py-1 bg-emerald-950 rounded text-emerald-300 font-bold">CLAUDE.md</code>
                    </div>
                    <p className="text-xs text-muted-foreground mt-2">
                      (ou CLAUDE-autoAmelioration.md si vous avez choisi la version avancée)
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Étape 5 */}
        <div className="glass-card rounded-xl p-6">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg">
              5
            </div>
            <div className="flex-1 space-y-4">
              <div>
                <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-emerald-400" />
                  Structure finale
                </h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Votre répertoire de travail doit maintenant ressembler à ceci :
                </p>

                <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm border border-slate-800 space-y-1">
                  <div className="text-muted-foreground">
                    <span className="text-emerald-300">votre-repertoire-de-travail/</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">├── .claude/</span> <span className="text-xs text-emerald-400">← Dossier de configuration</span>
                  </div>
                  <div className="ml-8 text-muted-foreground">
                    <span className="text-slate-500">├── agents/</span> <span className="text-xs text-muted-foreground">← Agents personnalisés</span>
                  </div>
                  <div className="ml-8 text-muted-foreground">
                    <span className="text-slate-500">├── skills/</span> <span className="text-xs text-muted-foreground">← Skills spécialisés</span>
                  </div>
                  <div className="ml-8 text-muted-foreground">
                    <span className="text-slate-500">├── commands/</span> <span className="text-xs text-muted-foreground">← Commandes personnalisées</span>
                  </div>
                  <div className="ml-8 text-muted-foreground">
                    <span className="text-slate-500">├── mcp_servers/</span> <span className="text-xs text-muted-foreground">← Serveurs MCP</span>
                  </div>
                  <div className="ml-8 text-muted-foreground">
                    <span className="text-slate-500">└── settings.json</span>
                  </div>
                  <div className="ml-4 text-muted-foreground">
                    <span className="text-nebula-400">└── CLAUDE.md</span> <span className="text-xs text-emerald-400">← Instructions pour Claude</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Vérification */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Terminal className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Vérifier la configuration</h2>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Lancer Claude dans votre répertoire</h3>
            <p className="text-sm text-muted-foreground mb-3">
              Ouvrez un terminal "cmd prompt" dans votre répertoire de travail et lancez :
            </p>
            <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm border border-slate-800 space-y-2">
              <div>
                <span className="text-cosmic-300">claude</span>
              </div>
            </div>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-lg font-semibold mb-2">Tester les outils disponibles</h3>
            <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm border border-slate-800 space-y-2">
              <div className="text-muted-foreground">
                <span className="text-cosmic-300">Est-ce que tu peux me montrer rapidement ce dont tu es capable avec tes skills disponibles ?</span>
              </div>
              <div className="text-muted-foreground italic">
                [Claude se chargera de vous expliquer le fonctionnement de ses fonctionnalités.]
              </div>
            </div>
          </div>

          <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-3 mt-3">
            <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-emerald-300">
              Si Claude reconnaît les skills et peut les utiliser, la configuration est réussie !
            </p>
          </div>
        </div>
      </section>

      {/* Ce que vous pouvez faire maintenant */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Ce que vous pouvez faire maintenant</h2>
        </div>

        <p className="text-muted-foreground">
          Avec cette configuration, Claude Code dispose de nombreux outils spécialisés pour l'enseignement :
        </p>

        <div className="grid md:grid-cols-2 gap-4">
          <Link
            href="/claude-code/presentations/tex-document-creator-system"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <FileText className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors">Créer des documents LaTeX</h4>
              <p className="text-sm text-muted-foreground">
                Cours, exercices, évaluations avec le package bfcours
              </p>
            </div>
          </Link>

          <Link
            href="/claude-code/presentations/reveals-presentation-system"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <BookOpen className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors">Générer des présentations</h4>
              <p className="text-sm text-muted-foreground">
                Reveal.js interactives ou diaporamas Beamer
              </p>
            </div>
          </Link>

          <Link
            href="/claude-code/presentations/educational-app-builder-system"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <Package className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors">Créer des applications</h4>
              <p className="text-sm text-muted-foreground">
                Applications éducatives interactives Flask
              </p>
            </div>
          </Link>

          <Link
            href="/claude-code/presentations/skill-creator-system"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <Zap className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors">Automatiser vos tâches</h4>
              <p className="text-sm text-muted-foreground">
                Agents spécialisés et skills personnalisés
              </p>
            </div>
          </Link>
        </div>

        <div className="flex flex-wrap gap-3 pt-4">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/presentations" prefetch={false}>
              Explorer les présentations
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/tutorials/bfcours-setup" prefetch={false}>
              Installer le package bfcours
            </Link>
          </Button>
        </div>
      </section>

      {/* Documentation */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Pour aller plus loin</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <Link
            href="/claude-code/presentations/architecture-claude-code-reveals"
            className="flex items-start gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800 hover:border-nebula-600 hover:scale-105 transition-all group"
          >
            <Settings className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-nebula-400 transition-colors">
                Architecture Claude Code
              </h4>
              <p className="text-xs text-muted-foreground">
                Comprendre l'organisation de la configuration
              </p>
            </div>
          </Link>

          <Link
            href="/claude-code/presentations/commandes-disponibles"
            className="flex items-start gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800 hover:border-nebula-600 hover:scale-105 transition-all group"
          >
            <Terminal className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-nebula-400 transition-colors">
                Commandes disponibles
              </h4>
              <p className="text-xs text-muted-foreground">
                Catalogue des commandes et skills
              </p>
            </div>
          </Link>

          <a
            href="https://docs.claude.com/en/docs/claude-code/overview"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <BookOpen className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                Documentation officielle
                <ExternalLink className="w-3 h-3" />
              </h4>
              <p className="text-xs text-muted-foreground">
                Référence complète Claude Code
              </p>
            </div>
          </a>

          <Link
            href="/claude-code/tutorials/google-api-setup"
            className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
          >
            <Sparkles className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors">
                Configuration API Google
              </h4>
              <p className="text-xs text-muted-foreground">
                Pour la génération d'images IA
              </p>
            </div>
          </Link>
        </div>
      </section>
    </div>
  )
}
