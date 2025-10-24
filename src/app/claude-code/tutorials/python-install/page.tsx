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
  ExternalLink,
  Sparkles
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation de Python x64 | Tutoriels",
  description:
    "Guide complet pour installer et configurer Python x64 sur votre ordinateur. Python est nécessaire pour les fonctionnalités graphiques et d'IA.",
}

export default function PythonInstallPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="python-install" title="Installation de Python x64" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Installation Python x64", href: "/claude-code/tutorials/python-install" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Code2 className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation de Python x64
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Python est un langage de programmation essentiel pour les fonctionnalités graphiques
          et d'intelligence artificielle
        </p>
      </section>

      {/* Qu'est-ce que Python */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Qu'est-ce que Python ?</h2>
        </div>

        <p className="text-muted-foreground">
          Python est un langage de programmation populaire et polyvalent. C'est l'un des compilateurs
          principaux utilisés par les outils d'IA modernes. Il permet d'exécuter de nombreux programmes
          liés à l'intelligence artificielle, au traitement d'images, à l'analyse de données et bien plus.
        </p>

        <div className="grid md:grid-cols-2 gap-4 mt-6">
          <div className="flex gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <CheckCircle className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">Fonctionnalités IA</h3>
              <p className="text-sm text-muted-foreground">
                Requis pour utiliser des bibliothèques d'IA comme TensorFlow, PyTorch, OpenCV
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <CheckCircle className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">Traitement graphique</h3>
              <p className="text-sm text-muted-foreground">
                Nécessaire pour la génération et le traitement d'images
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <CheckCircle className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">Écosystème riche</h3>
              <p className="text-sm text-muted-foreground">
                Accès à des milliers de bibliothèques scientifiques et éducatives
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <CheckCircle className="w-6 h-6 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-nebula-300">Version x64 importante</h3>
              <p className="text-sm text-muted-foreground">
                La version 64 bits offre de meilleures performances et plus de mémoire
              </p>
            </div>
          </div>
        </div>

        <div className="mt-4 p-4 bg-blue-950/30 border border-blue-800 rounded-lg">
          <p className="text-sm text-muted-foreground">
            <strong className="text-blue-300">Important :</strong> Installez la version <strong className="text-foreground">x64 (64 bits)</strong>
            de Python, et non la version 32 bits. La version 64 bits est nécessaire pour exploiter pleinement
            les capacités de votre ordinateur moderne.
          </p>
        </div>
      </section>

      {/* Installation */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Télécharger Python x64</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Download className="w-6 h-6 text-nebula-400" />
              <CardTitle>Téléchargement depuis le site officiel</CardTitle>
            </div>
            <CardDescription>
              Rendez-vous sur le site officiel de Python pour télécharger la dernière version x64
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                <div className="flex-1">
                  <p className="font-medium mb-2">Accéder au site officiel</p>
                  <p className="text-sm text-muted-foreground mb-3">
                    Ouvrez votre navigateur et allez sur :
                  </p>
                  <Button asChild variant="outline" size="sm">
                    <a href="https://www.python.org/downloads/" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2">
                      <ExternalLink className="w-4 h-4" />
                      https://www.python.org/downloads/
                    </a>
                  </Button>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium mb-1">Télécharger la version Windows x64</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    Cliquez sur le bouton de téléchargement de la dernière version stable.
                    Le site détecte automatiquement votre système d'exploitation.
                  </p>
                  <div className="p-3 bg-amber-950/30 border border-amber-800 rounded-lg">
                    <p className="text-sm text-amber-300">
                      <strong>Vérification importante :</strong> Assurez-vous que le fichier téléchargé contient
                      bien "amd64" ou "x86-64" dans son nom. Par exemple : <code className="px-2 py-1 bg-slate-900 rounded">python-3.12.0-amd64.exe</code>
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <CheckCircle className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="font-medium mb-1">Version recommandée</p>
                  <p className="text-sm text-muted-foreground">
                    <strong className="text-foreground">Minimum version 3.8</strong>, mais nous recommandons
                    la dernière version stable (3.12 ou supérieure) pour bénéficier des dernières améliorations.
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
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Installer Python x64</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Settings className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Procédure d'installation</CardTitle>
            </div>
            <CardDescription>
              Suivez attentivement ces étapes pour installer Python correctement
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-nebula-500 flex items-center justify-center text-white text-xs font-bold">
                  1
                </div>
                <div>
                  <p className="font-medium mb-1">Exécuter l'installateur</p>
                  <p className="text-sm text-muted-foreground">
                    Double-cliquez sur le fichier .exe téléchargé
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-500 flex items-center justify-center text-white text-xs font-bold">
                  2
                </div>
                <div>
                  <p className="font-medium mb-1 text-emerald-300">
                    Cocher "Add python.exe to PATH"
                  </p>
                  <p className="text-sm text-muted-foreground mb-2">
                    <strong className="text-foreground">TRÈS IMPORTANT :</strong> Avant de cliquer sur "Install Now",
                    cochez impérativement la case "Add python.exe to PATH" en bas de la fenêtre.
                    Cette option permet d'utiliser Python depuis n'importe quel terminal.
                  </p>
                  <div className="p-3 bg-red-950/30 border border-red-800 rounded-lg">
                    <p className="text-sm text-red-300">
                      <strong>⚠️ Attention :</strong> Si vous oubliez cette étape, Python ne sera pas accessible
                      depuis le terminal et vous devrez réinstaller.
                    </p>
                  </div>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-nebula-500 flex items-center justify-center text-white text-xs font-bold">
                  3
                </div>
                <div>
                  <p className="font-medium mb-1">Cliquer sur "Install Now"</p>
                  <p className="text-sm text-muted-foreground">
                    Une fois la case cochée, cliquez sur "Install Now" (installation recommandée)
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-nebula-500 flex items-center justify-center text-white text-xs font-bold">
                  4
                </div>
                <div>
                  <p className="font-medium mb-1">Autoriser les modifications</p>
                  <p className="text-sm text-muted-foreground">
                    Windows vous demandera l'autorisation. Cliquez sur "Oui"
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-nebula-500 flex items-center justify-center text-white text-xs font-bold">
                  5
                </div>
                <div>
                  <p className="font-medium mb-1">Attendre la fin de l'installation</p>
                  <p className="text-sm text-muted-foreground">
                    L'installation prend généralement 1 à 2 minutes
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-nebula-500 flex items-center justify-center text-white text-xs font-bold">
                  6
                </div>
                <div>
                  <p className="font-medium mb-1">Désactiver la limite de chemin (optionnel)</p>
                  <p className="text-sm text-muted-foreground">
                    À la fin de l'installation, si l'option "Disable path length limit" apparaît, cliquez dessus.
                    Cela évite des problèmes avec les chemins de fichiers trop longs.
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
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <h2 className="text-3xl font-bold">Vérifier l'installation</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-emerald-400" />
              <CardTitle>Tester que Python fonctionne</CardTitle>
            </div>
            <CardDescription>
              Vérifiez que Python x64 et pip sont correctement installés
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div>
                <p className="font-medium mb-3">Ouvrir un NOUVEAU terminal</p>
                <p className="text-sm text-muted-foreground mb-2">
                  <strong className="text-amber-300">Important :</strong> Si vous aviez un terminal ouvert,
                  fermez-le et ouvrez-en un nouveau pour que les changements du PATH soient pris en compte.
                </p>
                <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                  <li>Windows : Ouvrir "Invite de commandes" ou "PowerShell"</li>
                  <li>macOS : Ouvrir "Terminal"</li>
                  <li>Linux : Ouvrir votre terminal préféré</li>
                </ul>
              </div>

              <div>
                <p className="font-medium mb-3">Vérifier la version de Python</p>
                <CodeBlock code="python --version" language="bash" />
                <p className="text-sm text-muted-foreground mt-2">
                  Vous devriez voir s'afficher un numéro de version, par exemple : <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">Python 3.12.0</code>
                </p>
              </div>

              <div>
                <p className="font-medium mb-3">Vérifier que c'est bien la version x64</p>
                <CodeBlock code="python -c &quot;import platform; print(platform.architecture()[0])&quot;" language="bash" />
                <p className="text-sm text-muted-foreground mt-2">
                  Vous devriez voir s'afficher : <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">64bit</code>
                </p>
              </div>

              <div>
                <p className="font-medium mb-3">Vérifier la version de pip (gestionnaire de paquets)</p>
                <CodeBlock code="pip --version" language="bash" />
                <p className="text-sm text-muted-foreground mt-2">
                  Vous devriez voir s'afficher un numéro de version et le chemin d'installation
                </p>
              </div>
            </div>

            <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-4">
              <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-emerald-300 mb-1">Installation réussie !</p>
                <p className="text-sm text-muted-foreground">
                  Si toutes les commandes affichent des résultats corrects, Python x64 est correctement installé.
                  Vous pouvez maintenant profiter des fonctionnalités IA et graphiques !
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
              Commande "python" non reconnue
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Vous avez probablement oublié de cocher "Add python.exe to PATH"</li>
              <li>Fermez tous vos terminaux et ouvrez-en un nouveau</li>
              <li>Si le problème persiste, désinstallez Python et réinstallez-le en cochant la case PATH</li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Architecture 32 bits au lieu de 64 bits
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Vérifiez le nom du fichier d'installation : il doit contenir "amd64" ou "x86-64"</li>
              <li>Désinstallez la version 32 bits depuis le Panneau de configuration (Windows)</li>
              <li>Téléchargez et installez la version x64 correcte depuis python.org</li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Erreurs lors de l'installation de packages
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Mettez à jour pip : <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">python -m pip install --upgrade pip</code></li>
              <li>Exécutez le terminal en tant qu'administrateur (Windows)</li>
              <li>Certains packages nécessitent Visual Studio Build Tools (installés automatiquement avec Node.js)</li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Plusieurs versions de Python installées
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Utilisez <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">py --list</code> pour voir toutes les versions</li>
              <li>Utilisez <code className="px-2 py-1 bg-slate-900 rounded text-nebula-300">py -3.12</code> pour lancer une version spécifique</li>
              <li>Pour simplifier, désinstallez les anciennes versions depuis le Panneau de configuration</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-nebula-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        </div>

        <p className="text-muted-foreground">
          Maintenant que Python x64 est installé, vous pouvez :
        </p>

        <div className="flex flex-wrap gap-3">
          <Button asChild variant="nebula" size="lg">
            <Link href="/claude-code/tutorials/nodejs-install" prefetch={false}>
              Installer Node.js
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
