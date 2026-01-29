import Image from "next/image"
import Link from "next/link"
import {
  Terminal,
  Download,
  CheckCircle,
  AlertCircle,
  Package,
  Settings,
  Code2,
  ExternalLink
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation de Node.js | Tutoriels",
  description:
    "Guide complet pour installer et configurer Node.js sur votre ordinateur. Node.js est un environnement d'exécution JavaScript nécessaire pour Claude Code.",
}

export default function NodeJSInstallPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="nodejs-install" title="Installation de Node.js" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Installation Node.js", href: "/claude-code/tutorials/nodejs-install" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Terminal className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation de Node.js
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Node.js est un environnement d'exécution JavaScript utile pour exploiter pleinement
          les fonctionnalités avancées de Claude Code
        </p>
      </section>

      {/* Bandeau : Plus obligatoire */}
      <section className="glass-card rounded-xl p-6 border-2 border-amber-500/40 bg-amber-950/20">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <div className="space-y-2">
            <h2 className="text-xl font-bold text-amber-300">Node.js n'est plus obligatoire pour Claude Code</h2>
            <p className="text-muted-foreground">
              Depuis les dernières mises à jour, Claude Code propose une <strong className="text-foreground">installation native</strong> qui
              ne nécessite plus Node.js. L'installation via npm est désormais <strong className="text-amber-300">dépréciée</strong>.
            </p>
            <div className="mt-3 p-3 bg-amber-950/40 border border-amber-800 rounded-lg">
              <p className="text-sm text-muted-foreground">
                <strong className="text-amber-300">Faut-il quand même installer Node.js ?</strong> Oui, si vous souhaitez :
              </p>
              <ul className="mt-2 space-y-1 text-sm text-muted-foreground ml-4">
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>Utiliser des serveurs MCP (Model Context Protocol)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>Exécuter des scripts Node.js personnalisés</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>Développer des applications web (React, Next.js, etc.)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span>Utiliser des packages npm tiers</span>
                </li>
              </ul>
              <p className="text-sm text-muted-foreground mt-3">
                Si vous débutez avec Claude Code, vous pouvez <strong className="text-foreground">sauter cette étape</strong> et
                revenir installer Node.js plus tard si nécessaire.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Qu'est-ce que Node.js */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Package className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Qu'est-ce que Node.js ?</h2>
        </div>

        <p className="text-muted-foreground">
          Node.js est un environnement d'exécution JavaScript côté serveur. C'est l'un des compilateurs
          principaux utilisés par les outils d'IA et de développement modernes. Il permet d'exécuter
          du code JavaScript en dehors d'un navigateur web.
        </p>

        <div className="grid md:grid-cols-2 gap-4 mt-6">
          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <CheckCircle className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">Serveurs MCP</h3>
              <p className="text-sm text-muted-foreground">
                Requis pour exécuter les serveurs MCP qui étendent les capacités de Claude Code
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <CheckCircle className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">NPM inclus</h3>
              <p className="text-sm text-muted-foreground">
                Node.js inclut npm, le gestionnaire de paquets pour installer des outils tiers
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <CheckCircle className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">Écosystème riche</h3>
              <p className="text-sm text-muted-foreground">
                Accès à des milliers d'outils et de bibliothèques utiles
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <CheckCircle className="w-6 h-6 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-cosmic-300">Compatible multi-plateformes</h3>
              <p className="text-sm text-muted-foreground">
                Fonctionne sur Windows, macOS et Linux
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Installation */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Télécharger Node.js</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Download className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Téléchargement depuis le site officiel</CardTitle>
            </div>
            <CardDescription>
              Rendez-vous sur le site officiel de Node.js pour télécharger la dernière version
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium mb-2">Accéder au site officiel</p>
                  <p className="text-sm text-muted-foreground mb-3">
                    Ouvrez votre navigateur et allez sur :
                  </p>
                  <Button asChild variant="outline" size="sm">
                    <a href="https://nodejs.org" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2">
                      <ExternalLink className="w-4 h-4" />
                      https://nodejs.org
                    </a>
                  </Button>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium mb-1">Choisir la version LTS (recommandée)</p>
                  <p className="text-sm text-muted-foreground">
                    Téléchargez la version <strong className="text-emerald-300">LTS (Long Term Support)</strong>,
                    qui est la version stable et recommandée pour la plupart des utilisateurs.
                    <strong className="text-foreground ml-1">Minimum version 18</strong> requise pour Claude Code.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Installation pas à pas */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Installer Node.js</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Settings className="w-6 h-6 text-nebula-400" />
              <CardTitle>Procédure d'installation</CardTitle>
            </div>
            <CardDescription>
              Suivez les étapes pour installer Node.js sur votre système
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium mb-1">Exécuter l'installateur</p>
                  <p className="text-sm text-muted-foreground">
                    Double-cliquez sur le fichier téléchargé (.msi pour Windows, .pkg pour macOS)
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium mb-1">Accepter les termes de licence</p>
                  <p className="text-sm text-muted-foreground">
                    Lisez et acceptez les conditions d'utilisation
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium mb-1">Choisir le dossier d'installation</p>
                  <p className="text-sm text-muted-foreground">
                    Le dossier par défaut convient généralement. Gardez l'emplacement proposé.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  4
                </div>
                <div>
                  <p className="font-medium mb-1 text-emerald-300">
                    Cocher "Automatically install necessary tools"
                  </p>
                  <p className="text-sm text-muted-foreground">
                    <strong className="text-foreground">Important :</strong> Cette option installe automatiquement
                    les outils de compilation nécessaires (Chocolatey, Python, Visual Studio Build Tools).
                    C'est essentiel pour le bon fonctionnement de nombreux packages npm.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                  5
                </div>
                <div>
                  <p className="font-medium mb-1">Lancer l'installation</p>
                  <p className="text-sm text-muted-foreground">
                    Cliquez sur "Install" et patientez quelques minutes
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500 flex items-center justify-center text-white text-xs font-bold">
                  6
                </div>
                <div>
                  <p className="font-medium mb-1">Finaliser l'installation</p>
                  <p className="text-sm text-muted-foreground">
                    Une fenêtre PowerShell peut s'ouvrir pour installer les outils supplémentaires.
                    Appuyez sur Entrée lorsque demandé et laissez le processus se terminer.
                  </p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Vérification */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <h2 className="text-3xl font-bold">Vérifier l'installation</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-emerald-400" />
              <CardTitle>Tester que Node.js fonctionne</CardTitle>
            </div>
            <CardDescription>
              Vérifiez que Node.js et npm sont correctement installés
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div>
                <p className="font-medium mb-3">Ouvrir un terminal</p>
                <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                  <li>Windows : Ouvrir "Invite de commandes" ou "PowerShell"</li>
                  <li>macOS : Ouvrir "Terminal"</li>
                  <li>Linux : Ouvrir votre terminal préféré</li>
                </ul>
              </div>

              <div>
                <p className="font-medium mb-3">Vérifier la version de Node.js</p>
                <CodeBlock code="node --version" language="bash" />
                <p className="text-sm text-muted-foreground mt-2">
                  Vous devriez voir s'afficher un numéro de version, par exemple : <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">v20.11.0</code>
                </p>
              </div>

              <div>
                <p className="font-medium mb-3">Vérifier la version de npm</p>
                <CodeBlock code="npm --version" language="bash" />
                <p className="text-sm text-muted-foreground mt-2">
                  Vous devriez voir s'afficher un numéro de version, par exemple : <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">10.2.4</code>
                </p>
              </div>
            </div>

            <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-4">
              <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-emerald-300 mb-1">Installation réussie !</p>
                <p className="text-sm text-muted-foreground">
                  Si les deux commandes affichent un numéro de version, Node.js est correctement installé.
                  Vous pouvez maintenant installer Claude Code !
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Dépannage */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Problèmes fréquents</h2>
        </div>

        <div className="space-y-4">
          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Commande "node" non reconnue
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Fermez et rouvrez votre terminal</li>
              <li>Redémarrez votre ordinateur</li>
              <li>Vérifiez que Node.js est bien installé dans le Panneau de configuration (Windows)</li>
              <li>Réinstallez Node.js si le problème persiste</li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Erreurs lors de l'installation de packages
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Assurez-vous d'avoir coché "Automatically install necessary tools" lors de l'installation</li>
              <li>Exécutez le terminal en tant qu'administrateur (Windows)</li>
              <li>Nettoyez le cache npm : <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">npm cache clean --force</code></li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Version trop ancienne
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Claude Code nécessite Node.js version 18 ou supérieure</li>
              <li>Désinstallez l'ancienne version depuis le Panneau de configuration</li>
              <li>Téléchargez et installez la dernière version LTS depuis nodejs.org</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-cosmic-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Code2 className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        </div>

        <p className="text-muted-foreground">
          Maintenant que Node.js est installé, vous pouvez :
        </p>

        <div className="flex flex-wrap gap-3">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/tutorials/python-install" prefetch={false}>
              Installer Python x64
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/tutorials/claude-code-install" prefetch={false}>
              Installer Claude Code
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
