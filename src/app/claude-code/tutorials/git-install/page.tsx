import Link from "next/link"
import {
  GitBranch,
  Download,
  CheckCircle,
  AlertCircle,
  Settings,
  Terminal,
  ExternalLink,
  Sparkles,
  Package,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation de Git pour Windows | Tutoriels",
  description:
    "Installer Git pour Windows et Git Bash, le terminal que Claude Code utilise sous Windows pour exécuter ses commandes. Méthode winget en une ligne ou installateur classique.",
}

function Etape({ n, titre, children, accent = false }: { n: number; titre: string; children: React.ReactNode; accent?: boolean }) {
  return (
    <div className="flex items-start gap-3">
      <div
        className={`flex-shrink-0 w-6 h-6 rounded-full ${accent ? "bg-emerald-500" : "bg-orange-500"} flex items-center justify-center text-white text-xs font-bold`}
      >
        {n}
      </div>
      <div>
        <p className={`font-medium mb-1 ${accent ? "text-emerald-300" : ""}`}>{titre}</p>
        <div className="text-sm text-muted-foreground space-y-2">{children}</div>
      </div>
    </div>
  )
}

export default function GitInstallPage() {
  return (
    <div className="space-y-12">
      <TutorialTracker slug="git-install" title="Installation de Git pour Windows" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Installation Git", href: "/claude-code/tutorials/git-install" },
        ]}
      />

      {/* En-tête */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-orange-500 to-red-600 mb-4">
          <GitBranch className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">Installation de Git pour Windows</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Git garde l&apos;historique de vos fichiers. Sous Windows, il apporte surtout Git Bash, le terminal
          dans lequel Claude Code préfère exécuter ses commandes.
        </p>
      </section>

      {/* Pourquoi */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Pourquoi l&apos;installer ?</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="flex gap-3 p-4 rounded-lg bg-orange-950/20 border border-orange-800/60">
            <Terminal className="w-6 h-6 text-orange-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-orange-300">Git Bash pour Claude Code</h3>
              <p className="text-sm text-muted-foreground">
                La documentation d&apos;Anthropic recommande Git pour Windows : Claude Code s&apos;en sert pour son
                outil Bash. Sans lui, il se rabat sur PowerShell, et une partie des skills et scripts partagés
                (écrits pour Bash) fonctionne moins bien.
              </p>
            </div>
          </div>
          <div className="flex gap-3 p-4 rounded-lg bg-orange-950/20 border border-orange-800/60">
            <GitBranch className="w-6 h-6 text-orange-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1 text-orange-300">Un filet de sécurité</h3>
              <p className="text-sm text-muted-foreground">
                Un dossier suivi par Git garde chaque version enregistrée : si Claude abîme un fichier,
                on revient en arrière. Claude Code sait faire ces enregistrements à votre demande.
              </p>
            </div>
          </div>
        </div>

        <p className="text-sm text-muted-foreground">
          Sur macOS, Git est déjà présent (ou proposé à la première utilisation de la commande{" "}
          <code className="px-2 py-1 bg-slate-900 rounded">git</code>) : ce tutoriel concerne Windows.
        </p>
      </section>

      {/* Étape 1 : winget */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Installer Git</h2>
        </div>

        <Card className="glass-card border-2 border-emerald-500/30">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Terminal className="w-6 h-6 text-emerald-400" />
              <CardTitle>Voie rapide : une commande</CardTitle>
            </div>
            <CardDescription>
              Ouvrez PowerShell (menu Démarrer, tapez « PowerShell ») et collez :
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <CodeBlock code="winget install --id Git.Git -e" language="powershell" />
            <p className="text-sm text-muted-foreground">
              winget installe Git avec les réglages par défaut, qui conviennent. Acceptez la demande
              d&apos;autorisation de Windows, puis passez à l&apos;étape 2.
            </p>
          </CardContent>
        </Card>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Download className="w-6 h-6 text-orange-400" />
              <CardTitle>Ou méthode classique : l&apos;installateur</CardTitle>
            </div>
            <CardDescription>
              L&apos;installateur pose une douzaine de questions : gardez les choix proposés, sauf un.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Etape n={1} titre="Télécharger l'installateur">
              <Button asChild variant="outline" size="sm">
                <a
                  href="https://git-scm.com/downloads/win"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2"
                >
                  <ExternalLink className="w-4 h-4" />
                  https://git-scm.com/downloads/win
                </a>
              </Button>
              <p>Choisissez « Click here to download » (version 64 bits).</p>
            </Etape>
            <Etape n={2} titre="Éditeur par défaut : choisir autre chose que Vim" accent>
              <p>
                À l&apos;écran « Choosing the default editor used by Git », remplacez Vim (réputé difficile à
                quitter) par <strong className="text-foreground">Visual Studio Code</strong> s&apos;il est installé,
                ou par <strong className="text-foreground">Notepad</strong>.
              </p>
            </Etape>
            <Etape n={3} titre="Laisser l'option PATH recommandée">
              <p>
                À l&apos;écran « Adjusting your PATH environment », gardez{" "}
                <em>Git from the command line and also from 3rd-party software</em> : c&apos;est ce qui permet à
                Claude Code de trouver Git Bash.
              </p>
            </Etape>
            <Etape n={4} titre="Cliquer sur Next jusqu'à Install">
              <p>Les autres écrans (fins de ligne, terminal, gestionnaire d&apos;identifiants) se valident tels quels.</p>
            </Etape>
          </CardContent>
        </Card>
      </section>

      {/* Étape 2 : vérification */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Vérifier et se présenter</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <CheckCircle className="w-6 h-6 text-emerald-400" />
              <CardTitle>Dans un NOUVEAU terminal</CardTitle>
            </div>
            <CardDescription>
              Fermez PowerShell et rouvrez-le, pour qu&apos;il voie le nouveau PATH.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-5">
            <div>
              <p className="font-medium mb-2">Vérifier la version</p>
              <CodeBlock code="git --version" language="bash" />
              <p className="text-sm text-muted-foreground mt-2">
                Réponse attendue, par exemple :{" "}
                <code className="px-2 py-1 bg-slate-900 rounded text-orange-300">git version 2.56.0.windows.3</code>
              </p>
            </div>
            <div>
              <p className="font-medium mb-2">Indiquer votre nom et votre adresse (une seule fois)</p>
              <p className="text-sm text-muted-foreground mb-2">
                Git signe chaque enregistrement. Remplacez les valeurs entre guillemets par les vôtres :
              </p>
              <CodeBlock
                code={`git config --global user.name "Prénom Nom"\ngit config --global user.email "prenom.nom@exemple.fr"`}
                language="bash"
              />
            </div>
            <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-4">
              <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-emerald-300">C&apos;est tout.</strong> Au prochain lancement, Claude Code
                détecte Git Bash seul : rien à configurer de son côté.
              </p>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* winget pour le reste */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-600 flex items-center justify-center">
            <Package className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">winget pour les autres outils</h2>
        </div>
        <p className="text-muted-foreground">
          La même commande installe la plupart des logiciels utiles avec Claude Code. Quelques exemples :
        </p>
        <CodeBlock
          code={`winget install Python.Python.3.13          # Python\nwinget install OpenJS.NodeJS.LTS           # Node.js (version LTS)\nwinget install MiKTeX.MiKTeX               # LaTeX\nwinget install Microsoft.VisualStudioCode  # VS Code\nwinget install Gyan.FFmpeg                 # FFmpeg (audio et vidéo)\nwinget install Anthropic.ClaudeCode        # Claude Code`}
          language="powershell"
        />
        <p className="text-sm text-muted-foreground">
          Pour tout mettre à jour d&apos;un coup :{" "}
          <code className="px-2 py-1 bg-slate-900 rounded text-emerald-300">winget upgrade --all</code>. Un nom
          introuvable ? <code className="px-2 py-1 bg-slate-900 rounded text-emerald-300">winget search ffmpeg</code>{" "}
          liste les identifiants disponibles.
        </p>
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
              « winget » n&apos;est pas reconnu
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Mettez à jour « Programme d&apos;installation d&apos;application » depuis le Microsoft Store</li>
              <li>Sur un poste géré par l&apos;établissement, winget peut être bloqué : utilisez l&apos;installateur classique</li>
            </ul>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-amber-400" />
              Claude Code ne trouve pas Git Bash
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Fermez tous les terminaux et relancez Claude Code</li>
              <li>
                Si Git est installé ailleurs que dans le dossier par défaut, indiquez le chemin de{" "}
                <code className="px-1 bg-slate-900 rounded">bash.exe</code> dans{" "}
                <code className="px-1 bg-slate-900 rounded">~/.claude/settings.json</code> :
              </li>
            </ul>
            <div className="mt-3">
              <CodeBlock
                filename="settings.json"
                language="json"
                code={`{\n  "env": {\n    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\\\Program Files\\\\Git\\\\bin\\\\bash.exe"\n  }\n}`}
              />
            </div>
          </div>
        </div>
      </section>

      {/* Suite */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-orange-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500 to-red-600 flex items-center justify-center">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/tutorials/claude-code-install" prefetch={false}>
              Installer Claude Code
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/tutorials/python-install" prefetch={false}>
              Installer Python
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
