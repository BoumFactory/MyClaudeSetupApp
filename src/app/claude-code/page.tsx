import Link from "next/link"
import { Code2, BookOpen, Download, Video, FileText, GraduationCap } from "lucide-react"
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
