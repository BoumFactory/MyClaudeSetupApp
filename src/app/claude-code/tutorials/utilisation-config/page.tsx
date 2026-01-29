import Link from "next/link"
import {
  Terminal,
  Sparkles,
  FolderOpen,
  FileText,
  ArrowRight,
  CheckCircle,
  AlertCircle,
  Zap,
  Command,
  Search,
  Lightbulb,
  Play,
  Settings,
  BookOpen,
  ExternalLink
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Utiliser ma configuration | Tutoriels",
  description:
    "Guide pratique pour utiliser les commandes et skills de ma configuration Claude Code. Apprenez à déclencher les agents et automatiser vos tâches.",
}

export default function UtilisationConfigPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="utilisation-config" title="Utiliser ma configuration" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Utiliser ma configuration", href: "/claude-code/tutorials/utilisation-config" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Command className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Utiliser ma configuration
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Apprenez à déclencher les commandes et skills pour automatiser
          la création de vos ressources pédagogiques
        </p>
      </section>

      {/* Prérequis */}
      <section className="glass-card rounded-xl p-6 border-2 border-amber-500/40 bg-amber-950/20">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-amber-300">Prérequis</h2>
            <p className="text-muted-foreground">
              Avant de suivre ce tutoriel, assurez-vous d'avoir :
            </p>
            <ul className="space-y-2 mt-3">
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                <span>Installé <Link href="/claude-code/tutorials/claude-code-install" className="text-cosmic-400 hover:underline">Claude Code CLI</Link> ou <Link href="/claude-code/tutorials/claude-desktop-install" className="text-emerald-400 hover:underline">Claude Desktop</Link></span>
              </li>
              <li className="flex items-start gap-2 text-sm text-muted-foreground">
                <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                <span>Téléchargé et installé <Link href="/claude-code/tutorials/claude-code-config" className="text-cosmic-400 hover:underline">ma configuration</Link> (dossier .claude)</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Principe général */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Lightbulb className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Le principe</h2>
        </div>

        <p className="text-muted-foreground">
          Ma configuration ajoute des <strong className="text-cosmic-300">commandes</strong> et des <strong className="text-nebula-300">skills</strong> à Claude Code.
          Ces raccourcis déclenchent des agents spécialisés qui savent exactement quoi faire pour créer vos ressources.
        </p>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <div className="flex items-center gap-2 mb-3">
              <Terminal className="w-5 h-5 text-cosmic-400" />
              <h3 className="font-semibold text-cosmic-300">Commandes</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Syntaxe : <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">/chemin:vers:commande</code>
            </p>
            <p className="text-xs text-muted-foreground">
              Les commandes sont organisées par catégories (dossiers). Le chemin reflète l'arborescence.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-nebula-400" />
              <h3 className="font-semibold text-nebula-300">Skills</h3>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Syntaxe : <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">/nom-du-skill</code>
            </p>
            <p className="text-xs text-muted-foreground">
              Les skills sont accessibles directement par leur nom, sans chemin.
            </p>
          </div>
        </div>
      </section>

      {/* Autocomplétion */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-emerald-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
            <Search className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">L'autocomplétion</h2>
        </div>

        <div className="p-4 bg-emerald-950/30 border border-emerald-700 rounded-lg">
          <p className="text-emerald-300 font-semibold mb-2">Bonne nouvelle : pas besoin de tout retenir !</p>
          <p className="text-sm text-muted-foreground">
            Claude Code propose l'<strong className="text-foreground">autocomplétion</strong>. Tapez simplement <code className="px-2 py-1 bg-slate-900 rounded">/</code> et
            commencez à écrire : les suggestions apparaissent automatiquement.
          </p>
        </div>

        {/* Simulation visuelle */}
        <div className="space-y-4">
          <p className="text-sm font-medium text-muted-foreground">Exemple d'autocomplétion :</p>

          <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
            {/* Barre de titre terminal */}
            <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
              <span className="text-xs text-muted-foreground ml-2">Claude Code</span>
            </div>

            {/* Contenu terminal */}
            <div className="p-4 font-mono text-sm space-y-3">
              <div className="flex items-center gap-2">
                <span className="text-emerald-400">❯</span>
                <span className="text-foreground">/create</span>
                <span className="animate-pulse text-cosmic-400">|</span>
              </div>

              {/* Suggestions */}
              <div className="ml-4 space-y-1 border-l-2 border-cosmic-700 pl-3">
                <div className="flex items-center gap-2 px-2 py-1 rounded bg-cosmic-900/50 text-cosmic-300">
                  <Terminal className="w-4 h-4" />
                  <span>/createTex</span>
                  <span className="text-xs text-muted-foreground ml-auto">Créer document LaTeX</span>
                </div>
                <div className="flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-800 text-muted-foreground">
                  <Terminal className="w-4 h-4" />
                  <span>/createBeamer</span>
                  <span className="text-xs text-muted-foreground ml-auto">Créer diaporama Beamer</span>
                </div>
                <div className="flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-800 text-muted-foreground">
                  <Terminal className="w-4 h-4" />
                  <span>/createReveals</span>
                  <span className="text-xs text-muted-foreground ml-auto">Créer présentation Reveal.js</span>
                </div>
                <div className="flex items-center gap-2 px-2 py-1 rounded hover:bg-slate-800 text-muted-foreground">
                  <Terminal className="w-4 h-4" />
                  <span>/create-app</span>
                  <span className="text-xs text-muted-foreground ml-auto">Créer application éducative</span>
                </div>
              </div>
            </div>
          </div>

          <p className="text-xs text-muted-foreground">
            Utilisez les flèches <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">↑</kbd> <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">↓</kbd> pour naviguer et <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">Tab</kbd> ou <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">Entrée</kbd> pour sélectionner.
          </p>
        </div>
      </section>

      {/* Utiliser les Skills */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Utiliser les Skills</h2>
        </div>

        <Card className="glass-card border-2 border-nebula-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Sparkles className="w-6 h-6 text-nebula-400" />
              <CardTitle>Déclencher un skill</CardTitle>
            </div>
            <CardDescription>
              Les skills s'appellent directement par leur nom, sans chemin
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 bg-nebula-950/30 border border-nebula-700 rounded-lg">
              <p className="text-sm text-muted-foreground mb-3">
                <strong className="text-nebula-300">Syntaxe :</strong>
              </p>
              <code className="block px-4 py-3 bg-slate-950 rounded-lg text-nebula-300 font-mono">
                /nom-du-skill dans [chemin/vers/dossier] fais [description de la tâche]
              </code>
            </div>

            {/* Exemple concret */}
            <div className="space-y-3">
              <p className="text-sm font-medium">Exemple concret :</p>

              <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="text-xs text-muted-foreground ml-2">Claude Code</span>
                </div>

                <div className="p-4 font-mono text-sm">
                  <div className="flex items-start gap-2">
                    <span className="text-emerald-400">❯</span>
                    <div>
                      <span className="text-nebula-400">/bfcours-latex</span>
                      <span className="text-muted-foreground"> dans </span>
                      <span className="text-amber-400">./Cours/6eme/Fractions</span>
                      <span className="text-muted-foreground"> fais </span>
                      <span className="text-foreground">un cours sur les fractions avec des exercices progressifs</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2 p-3 bg-emerald-950/30 border border-emerald-800 rounded-lg">
                <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm text-muted-foreground">
                  L'agent <strong className="text-emerald-300">bfcours-latex</strong> va créer un document LaTeX complet
                  avec le package bfcours, adapté au niveau 6ème.
                </p>
              </div>
            </div>

            {/* Note importante pour LaTeX */}
            <div className="p-4 bg-amber-950/30 border border-amber-700 rounded-lg">
              <div className="flex items-start gap-3">
                <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-amber-300 font-semibold mb-1">Pour créer des documents LaTeX</p>
                  <p className="text-sm text-muted-foreground">
                    Commencez toujours par <code className="px-1.5 py-0.5 bg-slate-900 rounded text-nebula-300">/tex-document-creator</code> pour
                    générer vos documents avec les <strong className="text-foreground">bons modèles</strong> et la structure adaptée à votre niveau (collège, lycée, etc.).
                  </p>
                </div>
              </div>
            </div>

            {/* Liste des skills populaires */}
            <div className="space-y-3">
              <p className="text-sm font-medium">Skills populaires :</p>
              <div className="grid md:grid-cols-2 gap-2">
                {[
                  { name: "tex-document-creator", desc: "Créer un document LaTeX", highlight: true },
                  { name: "bfcours-latex", desc: "Éditer avec package bfcours" },
                  { name: "reveals-presentation", desc: "Présentations web Reveal.js" },
                  { name: "image-generator", desc: "Générer des images IA" },
                  { name: "tex-compiling-skill", desc: "Compiler du LaTeX" },
                  { name: "programmes-officiels", desc: "Citer les programmes BO" },
                ].map((skill) => (
                  <div key={skill.name} className={`flex items-center gap-2 p-2 rounded border ${(skill as any).highlight ? 'bg-amber-950/30 border-amber-700' : 'bg-slate-950/50 border-slate-800'}`}>
                    <Sparkles className={`w-4 h-4 flex-shrink-0 ${(skill as any).highlight ? 'text-amber-400' : 'text-nebula-400'}`} />
                    <code className={`text-sm ${(skill as any).highlight ? 'text-amber-300' : 'text-nebula-300'}`}>/{ skill.name }</code>
                    <span className="text-xs text-muted-foreground ml-auto">{ skill.desc }</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Utiliser les Commandes */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Utiliser les Commandes</h2>
        </div>

        <Card className="glass-card border-2 border-cosmic-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Terminal className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Déclencher une commande</CardTitle>
            </div>
            <CardDescription>
              Les commandes utilisent un chemin qui reflète leur organisation en dossiers
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 bg-cosmic-950/30 border border-cosmic-700 rounded-lg">
              <p className="text-sm text-muted-foreground mb-3">
                <strong className="text-cosmic-300">Syntaxe :</strong> Les commandes reflètent l'arborescence des dossiers
              </p>
              <code className="block px-4 py-3 bg-slate-950 rounded-lg text-cosmic-300 font-mono">
                /dossier:sous-dossier:commande [arguments]
              </code>
              <p className="text-xs text-muted-foreground mt-2">
                Exemple : <code className="text-cosmic-400">/creer:latex:createTex</code> = dossier creer → sous-dossier latex → commande createTex
              </p>
            </div>

            {/* Exemple concret avec /modifier:latex:adaptTex */}
            <div className="space-y-3">
              <p className="text-sm font-medium">Exemple concret avec /modifier:latex:adaptTex :</p>

              <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="text-xs text-muted-foreground ml-2">Claude Code</span>
                </div>

                <div className="p-4 font-mono text-sm">
                  <div className="flex items-start gap-2">
                    <span className="text-emerald-400">❯</span>
                    <div className="break-all">
                      <span className="text-cosmic-400">/modifier:latex:adaptTex</span>
                      <span className="text-foreground"> </span>
                      <span className="text-blue-400">"C:/Users/Prof/Documents/source.tex"</span>
                      <span className="text-foreground"> </span>
                      <span className="text-amber-400">"C:/Users/Prof/Cours/6eme/Fractions/"</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-2 p-3 bg-emerald-950/30 border border-emerald-800 rounded-lg">
                <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                <div className="text-sm text-muted-foreground">
                  <p>La commande <strong className="text-emerald-300">/modifier:latex:adaptTex</strong> prend :</p>
                  <ul className="mt-1 ml-4 space-y-1">
                    <li><span className="text-blue-400">1er argument</span> : chemin absolu du fichier source</li>
                    <li><span className="text-amber-400">2ème argument</span> : chemin absolu du dossier de destination</li>
                  </ul>
                  <p className="mt-2">L'agent sait exactement quoi adapter et où le mettre !</p>
                </div>
              </div>
            </div>

            {/* Liste des commandes populaires */}
            <div className="space-y-3">
              <p className="text-sm font-medium">Commandes populaires :</p>
              <div className="space-y-2">
                {[
                  { name: "/modifier:latex:adaptTex", desc: "Adapter un document existant", highlight: true },
                  { name: "/creer:latex:createTex", desc: "Créer un document LaTeX" },
                  { name: "/modifier:latex:modifyTex", desc: "Modifier un document LaTeX" },
                  { name: "/creer:latex:createBeamer", desc: "Créer un diaporama Beamer" },
                  { name: "/creer:html:createReveals", desc: "Créer une présentation Reveal.js" },
                  { name: "/creer:application:create-app", desc: "Créer une application éducative" },
                  { name: "/outillage:documentation:ficheTexnique", desc: "Générer une fiche technique" },
                  { name: "/do", desc: "Mode intelligent (choix auto)", highlight: true },
                ].map((cmd) => (
                  <div key={cmd.name} className={`flex items-center gap-2 p-2 rounded border ${(cmd as any).highlight ? 'bg-cosmic-950/40 border-cosmic-600' : 'bg-slate-950/50 border-slate-800'}`}>
                    <Terminal className={`w-4 h-4 flex-shrink-0 ${(cmd as any).highlight ? 'text-cosmic-300' : 'text-cosmic-400'}`} />
                    <code className={`text-xs ${(cmd as any).highlight ? 'text-cosmic-200 font-semibold' : 'text-cosmic-300'}`}>{ cmd.name }</code>
                    <span className="text-xs text-muted-foreground ml-auto">{ cmd.desc }</span>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* La commande /do */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <h2 className="text-3xl font-bold">La commande /do</h2>
        </div>

        <Card className="glass-card border-2 border-amber-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Zap className="w-6 h-6 text-amber-400" />
              <CardTitle>Le mode intelligent</CardTitle>
            </div>
            <CardDescription>
              Laissez Claude choisir les outils adaptés à votre demande
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 bg-amber-950/30 border border-amber-700 rounded-lg">
              <p className="text-sm text-muted-foreground mb-3">
                <strong className="text-amber-300">Principe :</strong> La commande <code className="px-2 py-1 bg-slate-900 rounded text-amber-300">/do</code> demande
                à Claude de <strong className="text-foreground">réfléchir</strong> et de <strong className="text-foreground">choisir automatiquement</strong> les
                skills et agents les plus adaptés pour répondre à votre demande.
              </p>
            </div>

            {/* Exemple */}
            <div className="space-y-3">
              <p className="text-sm font-medium">Exemple :</p>

              <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-2 bg-slate-900 border-b border-slate-800">
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <div className="w-3 h-3 rounded-full bg-yellow-500" />
                  <div className="w-3 h-3 rounded-full bg-green-500" />
                  <span className="text-xs text-muted-foreground ml-2">Claude Code</span>
                </div>

                <div className="p-4 font-mono text-sm">
                  <div className="flex items-start gap-2">
                    <span className="text-emerald-400">❯</span>
                    <div>
                      <span className="text-amber-400">/do</span>
                      <span className="text-foreground"> crée un cours sur les fonctions affines pour les 3ème avec des exercices, une présentation reveal.js et une évaluation</span>
                    </div>
                  </div>
                </div>
              </div>

              <div className="p-3 bg-slate-950/50 border border-slate-700 rounded-lg">
                <p className="text-sm text-muted-foreground mb-2">
                  <strong className="text-amber-300">Claude va analyser la demande et pourrait :</strong>
                </p>
                <ul className="space-y-1 text-sm text-muted-foreground ml-4">
                  <li className="flex items-start gap-2">
                    <span className="text-amber-400">1.</span>
                    <span>Utiliser <code className="text-nebula-300">/bfcours-latex</code> pour le cours</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-amber-400">2.</span>
                    <span>Utiliser <code className="text-nebula-300">/reveals-presentation</code> pour la présentation</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-amber-400">3.</span>
                    <span>Utiliser <code className="text-cosmic-300">/createTex</code> pour l'évaluation</span>
                  </li>
                </ul>
              </div>
            </div>

            {/* Avantages et limites */}
            <div className="grid md:grid-cols-2 gap-4">
              <div className="p-4 rounded-lg bg-emerald-950/30 border border-emerald-800">
                <h4 className="font-semibold text-emerald-300 mb-2 flex items-center gap-2">
                  <CheckCircle className="w-4 h-4" />
                  Avantages
                </h4>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li>• Pas besoin de connaître tous les skills</li>
                  <li>• Efficace pour les demandes complexes</li>
                  <li>• Combine plusieurs outils automatiquement</li>
                  <li>• Idéal pour les utilisateurs avancés</li>
                </ul>
              </div>

              <div className="p-4 rounded-lg bg-amber-950/30 border border-amber-800">
                <h4 className="font-semibold text-amber-300 mb-2 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4" />
                  Limites
                </h4>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li>• Peut parfois mal interpréter la demande</li>
                  <li>• Moins prévisible qu'un skill direct</li>
                  <li>• Consomme plus de tokens (réflexion)</li>
                  <li>• Pour les tâches simples, préférez le skill direct</li>
                </ul>
              </div>
            </div>

            <div className="flex items-start gap-2 p-3 bg-blue-950/30 border border-blue-800 rounded-lg">
              <Lightbulb className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-blue-300">Conseil :</strong> Utilisez <code className="text-amber-300">/do</code> pour les demandes
                multi-tâches ou quand vous ne savez pas quel skill utiliser. Pour une tâche précise,
                préférez appeler directement le skill concerné.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Insertion flexible */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center text-white font-bold text-xl">
            4
          </div>
          <h2 className="text-3xl font-bold">Insertion flexible</h2>
        </div>

        <Card className="glass-card border-2 border-blue-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Play className="w-6 h-6 text-blue-400" />
              <CardTitle>Commandes et skills : où vous voulez !</CardTitle>
            </div>
            <CardDescription>
              Vous pouvez insérer une commande ou un skill à n'importe quel endroit de votre prompt
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="p-4 bg-blue-950/30 border border-blue-700 rounded-lg">
              <p className="text-sm text-muted-foreground">
                <strong className="text-blue-300">Principe :</strong> Les commandes et skills ne doivent pas forcément être au début du prompt.
                Vous pouvez les <strong className="text-foreground">intercaler naturellement</strong> dans votre phrase.
              </p>
            </div>

            {/* Exemples variés */}
            <div className="space-y-4">
              <p className="text-sm font-medium">Différentes façons d'écrire :</p>

              {/* Exemple 1 : au début */}
              <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
                <div className="px-3 py-1.5 bg-slate-900 border-b border-slate-800 text-xs text-muted-foreground">
                  Au début (classique)
                </div>
                <div className="p-3 font-mono text-sm">
                  <span className="text-nebula-400">/bfcours-latex</span>
                  <span className="text-foreground"> fais un cours sur les fractions dans ./6eme/</span>
                </div>
              </div>

              {/* Exemple 2 : au milieu */}
              <div className="bg-slate-950 rounded-lg border border-emerald-800 overflow-hidden">
                <div className="px-3 py-1.5 bg-emerald-950/50 border-b border-emerald-800 text-xs text-emerald-400">
                  Au milieu (naturel)
                </div>
                <div className="p-3 font-mono text-sm">
                  <span className="text-foreground">Dans le dossier ./6eme/Fractions/ utilise </span>
                  <span className="text-nebula-400">/bfcours-latex</span>
                  <span className="text-foreground"> pour créer un cours complet</span>
                </div>
              </div>

              {/* Exemple 3 : à la fin */}
              <div className="bg-slate-950 rounded-lg border border-slate-800 overflow-hidden">
                <div className="px-3 py-1.5 bg-slate-900 border-b border-slate-800 text-xs text-muted-foreground">
                  À la fin
                </div>
                <div className="p-3 font-mono text-sm">
                  <span className="text-foreground">Je veux une évaluation sur Pythagore niveau 4ème avec </span>
                  <span className="text-cosmic-400">/creer:latex:createTex</span>
                </div>
              </div>

              {/* Exemple 4 : multiples */}
              <div className="bg-slate-950 rounded-lg border border-purple-800 overflow-hidden">
                <div className="px-3 py-1.5 bg-purple-950/50 border-b border-purple-800 text-xs text-purple-400">
                  Plusieurs commandes/skills (workflow complet)
                </div>
                <div className="p-3 font-mono text-sm leading-relaxed">
                  <span className="text-foreground">Utilise </span>
                  <span className="text-nebula-400">/tex-document-creator</span>
                  <span className="text-foreground"> pour créer le cours, puis </span>
                  <span className="text-nebula-400">/bfcours-latex</span>
                  <span className="text-foreground"> pour écrire le contenu et tout modifier. Enfin, </span>
                  <span className="text-cosmic-400">/creer:html:createReveals</span>
                  <span className="text-foreground"> pour la présentation associée</span>
                </div>
              </div>
            </div>

            <div className="flex items-start gap-2 p-3 bg-emerald-950/30 border border-emerald-800 rounded-lg">
              <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-emerald-300">L'essentiel :</strong> Écrivez naturellement ! Claude détecte les commandes et skills
                où qu'ils soient dans votre phrase. L'important est d'être clair sur ce que vous voulez.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Astuce importante : préciser le chemin */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-amber-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center">
            <Zap className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Astuce importante</h2>
        </div>

        <div className="p-4 bg-amber-950/30 border border-amber-700 rounded-lg">
          <p className="text-amber-300 font-semibold mb-2">Précisez toujours le chemin de travail !</p>
          <p className="text-sm text-muted-foreground">
            Pour éviter que l'agent ne perde du temps à chercher où travailler,
            <strong className="text-foreground"> indiquez toujours le dossier ou fichier cible</strong> dans votre demande.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {/* Mauvais exemple */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-red-400">
              <span className="text-lg">✗</span>
              <span className="font-medium">À éviter</span>
            </div>
            <div className="bg-slate-950 rounded-lg border border-red-900/50 p-3 font-mono text-sm">
              <span className="text-nebula-400">/bfcours-latex</span>
              <span className="text-foreground"> fais un cours sur les fractions</span>
            </div>
            <p className="text-xs text-muted-foreground">
              L'agent va devoir chercher où créer le fichier...
            </p>
          </div>

          {/* Bon exemple */}
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-emerald-400">
              <span className="text-lg">✓</span>
              <span className="font-medium">Recommandé</span>
            </div>
            <div className="bg-slate-950 rounded-lg border border-emerald-900/50 p-3 font-mono text-sm">
              <span className="text-nebula-400">/bfcours-latex</span>
              <span className="text-muted-foreground"> dans </span>
              <span className="text-amber-400">./6eme/Fractions/</span>
              <span className="text-foreground"> fais un cours</span>
            </div>
            <p className="text-xs text-muted-foreground">
              L'agent sait exactement où travailler !
            </p>
          </div>
        </div>

        <div className="space-y-3 pt-4">
          <p className="text-sm font-medium">Exemples de chemins :</p>
          <div className="grid md:grid-cols-2 gap-2 text-sm font-mono">
            <div className="flex items-center gap-2 p-2 rounded bg-slate-950/50">
              <FolderOpen className="w-4 h-4 text-amber-400" />
              <span className="text-amber-300">./Cours/6eme/Fractions/</span>
              <span className="text-xs text-muted-foreground ml-auto">Dossier</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded bg-slate-950/50">
              <FileText className="w-4 h-4 text-blue-400" />
              <span className="text-blue-300">./Eval/4eme/pythagore.tex</span>
              <span className="text-xs text-muted-foreground ml-auto">Fichier</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded bg-slate-950/50">
              <FolderOpen className="w-4 h-4 text-amber-400" />
              <span className="text-amber-300">C:/Users/.../MonProjet/</span>
              <span className="text-xs text-muted-foreground ml-auto">Absolu</span>
            </div>
            <div className="flex items-center gap-2 p-2 rounded bg-slate-950/50">
              <FileText className="w-4 h-4 text-blue-400" />
              <span className="text-blue-300">../Exercices/exo1.tex</span>
              <span className="text-xs text-muted-foreground ml-auto">Relatif</span>
            </div>
          </div>
        </div>
      </section>

      {/* Récapitulatif */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Récapitulatif</h2>
        </div>

        <div className="space-y-4">
          <div className="flex items-start gap-4 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <Sparkles className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-nebula-300 mb-1">Pour les Skills</h3>
              <code className="block px-3 py-2 bg-slate-950 rounded text-sm font-mono mt-2">
                <span className="text-nebula-400">/skill</span>
                <span className="text-muted-foreground"> dans </span>
                <span className="text-amber-400">[chemin]</span>
                <span className="text-muted-foreground"> fais </span>
                <span className="text-foreground">[description]</span>
              </code>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <Terminal className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-cosmic-300 mb-1">Pour les Commandes</h3>
              <code className="block px-3 py-2 bg-slate-950 rounded text-sm font-mono mt-2">
                <span className="text-cosmic-400">/dossier:sous-dossier:commande</span>
                <span className="text-muted-foreground"> </span>
                <span className="text-foreground">[arguments]</span>
              </code>
              <p className="text-xs text-muted-foreground mt-2">
                Ex: <code className="text-cosmic-300">/modifier:latex:adaptTex</code>, <code className="text-cosmic-300">/creer:html:createReveals</code>
              </p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 rounded-lg bg-emerald-950/30 border border-emerald-800">
            <Search className="w-6 h-6 text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-emerald-300 mb-1">Autocomplétion</h3>
              <p className="text-sm text-muted-foreground">
                Tapez <code className="px-1.5 py-0.5 bg-slate-900 rounded">/</code> et commencez à écrire pour voir les suggestions.
                Naviguez avec <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">↑↓</kbd> et validez avec <kbd className="px-1.5 py-0.5 bg-slate-800 rounded text-xs">Tab</kbd>.
              </p>
            </div>
          </div>
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
          Maintenant que vous savez utiliser les commandes et skills, explorez les présentations
          pour découvrir toutes les fonctionnalités disponibles.
        </p>

        <div className="flex flex-wrap gap-3">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/presentations" prefetch={false}>
              Explorer les présentations
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/downloads" prefetch={false}>
              Télécharger la configuration
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
