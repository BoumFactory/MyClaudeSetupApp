import Link from "next/link"
import { BookOpen, Code2, Download, Settings, FileCode2, Package, Image, Sparkles, GraduationCap } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Tutoriels d'installation - Claude Code",
  description:
    "Guides pas à pas pour configurer votre environnement de développement complet et utiliser les outils IA pour l'enseignement. Installation de VS Code, MikTeX, bfcours, Claude Code et API Google.",
}

export default function TutorialsPage() {
  return (
    <div className="space-y-12">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <GraduationCap className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Tutoriels d'installation
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Suivez ces guides dans l'ordre recommandé pour configurer votre environnement complet
          et profiter pleinement de Claude Code pour l'enseignement.
        </p>
      </section>

      {/* Tutoriels disponibles */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold text-center">
          Parcours d'installation recommandé
        </h2>

        <div className="grid md:grid-cols-2 gap-6">
          {/* 1. VS Code & MikTeX */}
          <Link href="/claude-code/tutorials/vscode-miktex" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full border-2 border-cosmic-500/30">
              <CardHeader>
                <div className="flex items-start justify-between mb-3">
                  <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
                    <Code2 className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    1
                  </div>
                </div>
                <CardTitle className="group-hover:text-cosmic-400 transition-colors">
                  Installation VS Code & MikTeX
                </CardTitle>
                <CardDescription>
                  <strong className="text-cosmic-400">La fondation</strong> : configurez un environnement de qualité pour LaTeX.
                  Installation complète avec extensions et compilation automatique.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium">
                      <Download className="w-3 h-3" />
                      Installation
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium">
                      <Settings className="w-3 h-3" />
                      Configuration
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium">
                      <FileCode2 className="w-3 h-3" />
                      LaTeX
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                      <Sparkles className="w-3 h-3" />
                      Essentiel
                    </span>
                  </div>
                  <div className="text-cosmic-400 font-semibold group-hover:underline">
                    Commencer le tutoriel →
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>

          {/* 2. bfcours */}
          <Link href="/claude-code/tutorials/bfcours-setup" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full border-2 border-nebula-500/30">
              <CardHeader>
                <div className="flex items-start justify-between mb-3">
                  <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center">
                    <Package className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    2
                  </div>
                </div>
                <CardTitle className="group-hover:text-nebula-400 transition-colors">
                  Installation du package bfcours
                </CardTitle>
                <CardDescription>
                  <strong className="text-nebula-400">Package LaTeX personnalisé</strong> pour l'enseignement des mathématiques.
                  Environnements prédéfinis pour cours, exercices et activités.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-nebula-500/20 text-nebula-400 text-xs font-medium">
                      <Package className="w-3 h-3" />
                      Package
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-nebula-500/20 text-nebula-400 text-xs font-medium">
                      <Settings className="w-3 h-3" />
                      MikTeX
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-nebula-500/20 text-nebula-400 text-xs font-medium">
                      <FileCode2 className="w-3 h-3" />
                      LaTeX
                    </span>
                  </div>
                  <div className="text-nebula-400 font-semibold group-hover:underline">
                    Installer le package →
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>

          {/* 3. Claude Code */}
          <Link href="/claude-code/tutorials/claude-code-install" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full border-2 border-cosmic-500/30">
              <CardHeader>
                <div className="flex items-start justify-between mb-3">
                  <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
                    <Sparkles className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg shadow-lg">
                    3
                  </div>
                </div>
                <CardTitle className="group-hover:text-cosmic-400 transition-colors">
                  Installation de Claude Code
                </CardTitle>
                <CardDescription>
                  <strong className="text-cosmic-400">L'outil IA principal</strong> : installez Claude Code CLI et configurez votre abonnement.
                  Automatisez la création de code et de documents pédagogiques.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium">
                      <Download className="w-3 h-3" />
                      CLI
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-cosmic-500/20 text-cosmic-400 text-xs font-medium">
                      <Settings className="w-3 h-3" />
                      Configuration
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                      20€/mois
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-medium">
                      <Sparkles className="w-3 h-3" />
                      Essentiel
                    </span>
                  </div>
                  <div className="text-cosmic-400 font-semibold group-hover:underline">
                    Installer Claude Code →
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>

          {/* 4. Google API (optionnel) */}
          <Link href="/claude-code/tutorials/google-api-setup" className="block">
            <Card className="glass-card hover:scale-105 transition-all duration-300 group cursor-pointer h-full border-2 border-nebula-500/30 opacity-95">
              <CardHeader>
                <div className="flex items-start justify-between mb-3">
                  <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center">
                    <Image className="w-6 h-6 text-white" />
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-nebula-400 px-2.5 py-1 rounded-full bg-nebula-500/30 border border-nebula-500/50">
                      Optionnel
                    </span>
                    <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-lg shadow-lg">
                      4
                    </div>
                  </div>
                </div>
                <CardTitle className="group-hover:text-nebula-400 transition-colors">
                  Configuration de l'API Google (Imagen)
                </CardTitle>
                <CardDescription>
                  <strong className="text-nebula-400">Fonctionnalité avancée</strong> : générez des images avec l'IA pour illustrer vos cours.
                  Nécessite une carte bancaire (facturation à l'usage).
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex flex-wrap gap-2">
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-nebula-500/20 text-nebula-400 text-xs font-medium">
                      <Image className="w-3 h-3" />
                      Images IA
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-nebula-500/20 text-nebula-400 text-xs font-medium">
                      <Settings className="w-3 h-3" />
                      API
                    </span>
                    <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-yellow-500/20 text-yellow-400 text-xs font-medium">
                      Facturation
                    </span>
                  </div>
                  <div className="text-nebula-400 font-semibold group-hover:underline">
                    Configurer l'API →
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        </div>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <h2 className="text-2xl font-bold">Pourquoi ces tutoriels ?</h2>
        <div className="space-y-3 text-muted-foreground">
          <p>
            Ces tutoriels ont été créés pour vous accompagner dans la mise en place
            d'un environnement de travail professionnel et moderne, affranchi des
            limitations des plateformes propriétaires comme Overleaf.
          </p>
          <p>
            En suivant ces guides dans l'ordre recommandé, vous apprendrez à :
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Configurer des outils open source puissants (VS Code, MikTeX)</li>
            <li>Installer et utiliser des packages LaTeX personnalisés</li>
            <li>Automatiser vos workflows avec Claude Code et l'IA</li>
            <li>Générer du contenu pédagogique de qualité professionnelle</li>
            <li>Collaborer efficacement avec vos collègues (Live Share)</li>
            <li>Enrichir vos documents avec des images générées par IA</li>
            <li>Maintenir le contrôle total sur vos données et outils</li>
          </ul>
        </div>
      </section>

      {/* Ordre d'installation */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-l-4 border-cosmic-400">
        <h2 className="text-2xl font-bold">Pourquoi cet ordre ?</h2>
        <div className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              1
            </div>
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">
                VS Code & MikTeX (Essentiel)
              </h3>
              <p className="text-muted-foreground text-sm">
                La fondation : vous ne pouvez rien faire sans un éditeur et une distribution LaTeX.
                C'est la base indispensable pour compiler vos documents.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold">
              2
            </div>
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">
                Package bfcours (Recommandé)
              </h3>
              <p className="text-muted-foreground text-sm">
                Package personnalisé pour l'enseignement des mathématiques. Facilite grandement
                la création de cours, exercices et activités avec des environnements prédéfinis.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
              3
            </div>
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">
                Claude Code (Essentiel pour l'IA)
              </h3>
              <p className="text-muted-foreground text-sm">
                L'outil principal pour automatiser la création de contenu avec l'IA. Génère du code,
                des documents LaTeX, des présentations et bien plus encore.
              </p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="flex-shrink-0 w-10 h-10 rounded-full nebula-gradient flex items-center justify-center text-white font-bold">
              4
            </div>
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">
                API Google Imagen (Optionnel)
              </h3>
              <p className="text-muted-foreground text-sm">
                Pour aller plus loin : générez des images avec l'IA pour illustrer vos documents.
                Nécessite une carte bancaire avec facturation à l'usage (très abordable).
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Besoin d'aide */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-l-4 border-cosmic-400">
        <h2 className="text-2xl font-bold">Besoin d'aide ?</h2>
        <p className="text-muted-foreground">
          Si vous rencontrez des difficultés lors de l'installation ou de la configuration,
          n'hésitez pas à consulter les ressources supplémentaires disponibles dans la
          section téléchargements ou à explorer les présentations pour mieux comprendre
          les concepts.
        </p>
        <div className="flex flex-wrap gap-3 pt-2">
          <Link href="/claude-code/downloads" prefetch={false}>
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cosmic-500/20 text-cosmic-400 hover:bg-cosmic-500/30 transition-colors text-sm font-medium cursor-pointer">
              <Download className="w-4 h-4" />
              Téléchargements
            </span>
          </Link>
          <Link href="/claude-code/presentations" prefetch={false}>
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-nebula-500/20 text-nebula-400 hover:bg-nebula-500/30 transition-colors text-sm font-medium cursor-pointer">
              <BookOpen className="w-4 h-4" />
              Présentations
            </span>
          </Link>
        </div>
      </section>
    </div>
  )
}
