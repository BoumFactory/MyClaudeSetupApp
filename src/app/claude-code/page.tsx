import Link from "next/link"
import { Code2, BookOpen, Download, Video, FileText, GraduationCap, Cpu, Terminal, FolderOpen, ArrowRight, Sparkles, Cog, FileOutput, Zap } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Claude Code",
  description:
    "Ou n'importe quel système d'agents CLI.",
}

export default function ClaudeCodePage() {
  return (
    <div className="space-y-12">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Code2 className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Claude Code
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          ... Ou n'importe quel système d'agents CLI intégrant les fonctionnalités récentes.
        </p>
        <p className="text-xl text-muted-foreground max-w-2l mx-auto">
          Parce qu'on s'adapte aux meilleurs outils.
        </p>
        <p className="text-xl text-muted-foreground max-w-2l mx-auto">
          Demain, j'utiliserai peut être un autre système.
        </p>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <h2 className="text-2xl font-bold">Qu'est-ce que Claude Code ?</h2>
        <div className="space-y-3 text-muted-foreground">
          <p>
            Claude Code est un assistant IA avancé développé par Anthropic,
            spécialement conçu pour aider les développeurs.
          </p>
          <p>
            C'est un système CLI : l'agent IA évolue dans un terminal. Cela lui donne accès à tout le système de commandes de votre ordinateur.
          </p>
          <p>
            Dans le contexte de l'enseignement des mathématiques, Claude Code
            devient un outil puissant pour :
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Créer des applications éducatives interactives</li>
            <li>Générer des présentations reveal.js personnalisées</li>
            <li>Développer des exercices dynamiques</li>
            <li>Automatiser la création de documents LaTeX</li>
            <li>Concevoir des systèmes d'agents intelligents</li>
          </ul>
        </div>
      </section>

      {/* Schéma explicatif : Système autonome */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-3xl font-bold">Un système complet et autonome</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Claude Code combine l'intelligence artificielle et des scripts pour créer
            des documents directement sur votre ordinateur, avec une efficacité remarquable.
          </p>
        </div>

        {/* Schéma visuel */}
        <div className="glass-card rounded-xl p-6 lg:p-8">
          {/* Flux principal */}
          <div className="flex flex-col lg:flex-row items-center justify-center gap-4 lg:gap-6">

            {/* Entrée : Votre demande */}
            <div className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center mb-3 shadow-lg shadow-blue-500/20">
                <Terminal className="w-8 h-8 text-white" />
              </div>
              <span className="font-semibold text-sm">Votre demande</span>
              <span className="text-xs text-muted-foreground">en langage naturel</span>
            </div>

            <ArrowRight className="w-6 h-6 text-muted-foreground rotate-90 lg:rotate-0 flex-shrink-0" />

            {/* Centre : Système IA + Scripts */}
            <div className="relative">
              <div className="glass-card rounded-2xl p-6 border-2 border-cosmic-500/50 bg-cosmic-950/30">
                <div className="flex flex-col items-center text-center space-y-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-xl cosmic-gradient flex items-center justify-center shadow-lg shadow-cosmic-500/20">
                      <Cpu className="w-6 h-6 text-white" />
                    </div>
                    <span className="text-2xl font-bold">+</span>
                    <div className="w-12 h-12 rounded-xl nebula-gradient flex items-center justify-center shadow-lg shadow-nebula-500/20">
                      <Cog className="w-6 h-6 text-white" />
                    </div>
                  </div>
                  <div>
                    <span className="font-bold text-lg">IA + Scripts</span>
                    <p className="text-xs text-muted-foreground mt-1">Agents & Skills spécialisés</p>
                  </div>
                </div>
              </div>
              {/* Badge autonome */}
              <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-3 py-1 bg-emerald-500 text-white text-xs font-bold rounded-full shadow-lg">
                Autonome
              </div>
            </div>

            <ArrowRight className="w-6 h-6 text-muted-foreground rotate-90 lg:rotate-0 flex-shrink-0" />

            {/* Sortie : Documents créés */}
            <div className="flex flex-col items-center text-center">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-emerald-500 to-emerald-600 flex items-center justify-center mb-3 shadow-lg shadow-emerald-500/20">
                <FileOutput className="w-8 h-8 text-white" />
              </div>
              <span className="font-semibold text-sm">Documents créés</span>
              <span className="text-xs text-muted-foreground">sur votre ordinateur</span>
            </div>
          </div>

          {/* Exemples de sorties */}
          <div className="mt-8 pt-6 border-t border-cosmic-800/50">
            <p className="text-center text-sm text-muted-foreground mb-4">Exemples de créations automatisées :</p>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-950/50 border border-slate-800">
                <FileText className="w-4 h-4 text-cosmic-400 flex-shrink-0" />
                <span className="text-xs">Documents LaTeX</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-950/50 border border-slate-800">
                <BookOpen className="w-4 h-4 text-nebula-400 flex-shrink-0" />
                <span className="text-xs">Présentations</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-950/50 border border-slate-800">
                <Code2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                <span className="text-xs">Applications</span>
              </div>
              <div className="flex items-center gap-2 p-3 rounded-lg bg-slate-950/50 border border-slate-800">
                <Sparkles className="w-4 h-4 text-amber-400 flex-shrink-0" />
                <span className="text-xs">Images IA</span>
              </div>
            </div>
          </div>
        </div>

        {/* Avantages clés */}
        <div className="grid md:grid-cols-3 gap-4">
          <div className="glass-card rounded-xl p-5 border-l-4 border-cosmic-500">
            <div className="flex items-start gap-3">
              <Zap className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-sm mb-1">Efficacité maximale</h3>
                <p className="text-xs text-muted-foreground">
                  L'IA comprend votre besoin et exécute les scripts nécessaires sans intervention
                </p>
              </div>
            </div>
          </div>
          <div className="glass-card rounded-xl p-5 border-l-4 border-nebula-500">
            <div className="flex items-start gap-3">
              <FolderOpen className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-sm mb-1">Fichiers locaux</h3>
                <p className="text-xs text-muted-foreground">
                  Tout est créé directement dans vos dossiers, prêt à l'emploi
                </p>
              </div>
            </div>
          </div>
          <div className="glass-card rounded-xl p-5 border-l-4 border-emerald-500">
            <div className="flex items-start gap-3">
              <Cog className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="font-semibold text-sm mb-1">Personnalisable</h3>
                <p className="text-xs text-muted-foreground">
                  Agents et skills adaptés à vos besoins d'enseignement
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tutoriels d'installation */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">
          Commencer avec Claude Code
        </h2>

        <div className="grid md:grid-cols-1 gap-6">
          {/* Tutoriels */}
          <Link href="/claude-code/tutorials" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full border-2 border-cosmic-500/50">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center mb-3">
                  <GraduationCap className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="group-hover:text-cosmic-400 transition-colors">
                  Tutoriels d'installation
                </CardTitle>
                <CardDescription>
                  Guides pas à pas pour installer et configurer votre environnement complet :
                  VS Code & MikTeX, package bfcours, Claude Code CLI et API Google (optionnel).
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                    <div className="flex items-center gap-2 text-sm">
                      <div className="w-6 h-6 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xs">1</div>
                      <span className="text-muted-foreground">VS Code & MikTeX</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <div className="w-6 h-6 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xs">2</div>
                      <span className="text-muted-foreground">Package bfcours</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <div className="w-6 h-6 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xs">3</div>
                      <span className="text-muted-foreground">Claude Code</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm">
                      <div className="w-6 h-6 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xs">4</div>
                      <span className="text-muted-foreground">API Google</span>
                    </div>
                  </div>
                  <div className="text-cosmic-400 font-semibold group-hover:underline">
                    Voir les tutoriels →
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      </section>

      {/* Getting Started */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold">Commencer avec Claude Code</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              1
            </div>
            <div>
              <h3 className="font-semibold mb-1">
                Suivre les tutoriels d'installation
              </h3>
              <p className="text-muted-foreground text-sm">
                Configurez votre environnement complet en suivant nos guides pas à pas :
                VS Code, MikTeX, bfcours et Claude Code.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              2
            </div>
            <div>
              <h3 className="font-semibold mb-1">
                Télécharger les configurations
              </h3>
              <p className="text-muted-foreground text-sm">
                Récupérez les fichiers de configuration, agents et skills depuis
                notre section téléchargements.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              3
            </div>
            <div>
              <h3 className="font-semibold mb-1">
                Explorer les présentations
              </h3>
              <p className="text-muted-foreground text-sm">
                Parcourez nos présentations pour comprendre l'architecture et
                les bonnes pratiques.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              4
            </div>
            <div>
              <h3 className="font-semibold mb-1">Créer vos projets</h3>
              <p className="text-muted-foreground text-sm">
                Utilisez les templates et exemples pour créer vos propres
                applications éducatives.
              </p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Ressources */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">
          Accès aux ressources
        </h2>

        <div className="grid md:grid-cols-2 gap-6">
          {/* Téléchargements */}
          <Link href="/claude-code/downloads" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center mb-3">
                  <Download className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="group-hover:text-nebula-400 transition-colors">Configurations & Agents</CardTitle>
                <CardDescription>
                  Téléchargez les configurations Claude, agents, skills et
                  applications prêtes à l'emploi
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-nebula-400 font-semibold group-hover:underline">
                  Accéder aux téléchargements →
                </div>
              </CardContent>
            </Card>
          </Link>

          {/* Applications */}
          <Link href="/claude-code/applications" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full">
              <CardHeader>
                <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center mb-3">
                  <FileText className="w-6 h-6 text-white" />
                </div>
                <CardTitle className="group-hover:text-nebula-400 transition-colors">Applications Éducatives</CardTitle>
                <CardDescription>
                  Découvrez les applications créées avec Claude Code pour
                  l'enseignement
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-muted-foreground font-semibold group-hover:text-nebula-400 group-hover:underline transition-colors">
                  Explorer les applications →
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      </section>

    </div>
  )
}
