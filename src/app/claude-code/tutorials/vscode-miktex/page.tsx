import Image from "next/image"
import Link from "next/link"
import {
  Code2,
  Settings,
  Check,
  FileCode2,
  Package,
  Users,
  Puzzle,
  Terminal,
  Copy
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation VS Code et MikTeX - Tutoriels",
  description:
    "Guide complet pour installer et configurer VS Code avec MikTeX pour travailler avec LaTeX de manière professionnelle, sans Overleaf.",
}

export default function VSCodeMikTeXPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="vscode-miktex" title="Installation VS Code & MikTeX" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "VS Code & MikTeX", href: "/claude-code/tutorials/vscode-miktex" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Code2 className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation de VS Code et MikTeX
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Configurez un environnement de qualité pour LaTeX avec VS Code et MikTeX.
          Vous pouvez également utiliser TeX Live ou TeXStudio.
        </p>
      </section>

      {/* Étape 1 : MikTeX */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <h2 className="text-3xl font-bold">Installer MikTeX</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Package className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Installation de la distribution LaTeX</CardTitle>
            </div>
            <CardDescription>
              MikTeX est une distribution LaTeX moderne et complète pour Windows, macOS et Linux
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid lg:grid-cols-2 gap-6 items-start">
              {/* Colonne gauche : Texte */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-cosmic-400" />
                  Étapes d'installation :
                </h3>

                <div className="space-y-3 ml-7">
                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Télécharger l'installateur</p>
                      <p className="text-sm text-muted-foreground">
                        Aller sur <a href="https://miktex.org/download" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline">https://miktex.org/download</a> et choisir la version adaptée à votre système d'exploitation
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Activer l'installation automatique des packages</p>
                      <p className="text-sm text-muted-foreground">
                        Cocher l'option "installer les packages à la volée" (on-the-fly) pour plus de souplesse
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Installation utilisateur unique</p>
                      <p className="text-sm text-muted-foreground">
                        Décocher l'option d'installation pour tous les utilisateurs (simplifie l'utilisation de la console MikTeX)
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Colonne droite : Image */}
              <div className="rounded-lg overflow-hidden border border-border">
                <Image
                  src="/images/miktex/set_localtexmf_path.png"
                  alt="Console MikTeX - Configuration du chemin LocalTexMF"
                  width={520}
                  height={285}
                  className="w-full h-auto"
                />
                <div className="p-3 bg-muted/50 text-sm text-muted-foreground">
                  Exemple de la console MikTeX pour la configuration
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 2 : VS Code */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <h2 className="text-3xl font-bold">Installer VS Code</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Code2 className="w-6 h-6 text-nebula-400" />
              <CardTitle>Environnement de développement</CardTitle>
            </div>
            <CardDescription>
              Visual Studio Code est un IDE puissant et gratuit, parfait pour LaTeX
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid lg:grid-cols-2 gap-6 items-start">
              {/* Colonne gauche : Instructions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-nebula-400" />
                  Étapes d'installation :
                </h3>

                <div className="space-y-3 ml-7">
                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Télécharger VS Code</p>
                      <p className="text-sm text-muted-foreground">
                        Aller sur <a href="https://code.visualstudio.com/download" target="_blank" rel="noopener noreferrer" className="text-nebula-400 hover:underline">https://code.visualstudio.com/download</a> et choisir la version adaptée
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium text-emerald-300">Cocher "Ajouter au PATH"</p>
                      <p className="text-sm text-muted-foreground">
                        <strong className="text-foreground">Important :</strong> Pendant l'installation,
                        cochez l'option "Ajouter au PATH". Cela permettra à VS Code d'accéder automatiquement
                        aux exécutables TeX installés précédemment (MikTeX/LuaLaTeX), ainsi qu'à d'autres
                        outils de développement présents sur votre système.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Autres options recommandées</p>
                      <p className="text-sm text-muted-foreground">
                        Vous pouvez aussi cocher les options pour ajouter VS Code au menu contextuel
                        (clic droit sur un fichier ou dossier)
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-3">
                    <Check className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="font-medium">Personnalisation (optionnel)</p>
                      <p className="text-sm text-muted-foreground">
                        Après installation, vous pouvez personnaliser le style de l'IDE selon vos préférences
                      </p>
                    </div>
                  </div>
                </div>

                <div className="glass-card p-4 bg-muted/30 mt-4">
                  <p className="text-sm text-muted-foreground">
                    <span className="font-semibold text-foreground">Note :</span> VS Code peut être remplacé par d'autres IDE comme Windsurf ou Cursor, qui offrent des fonctionnalités similaires.
                  </p>
                </div>
              </div>

              {/* Colonne droite : Image */}
              <div className="rounded-lg overflow-hidden border border-border">
                <Image
                  src="/images/ide/set-additional-tasks.png"
                  alt="Options d'installation VS Code"
                  width={503}
                  height={392}
                  className="w-full h-auto"
                />
                <div className="p-3 bg-muted/50 text-sm text-muted-foreground">
                  Options d'installation VS Code avec PATH cochée
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 3 : Extensions */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <h2 className="text-3xl font-bold">Installer les extensions VS Code</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Puzzle className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Extensions essentielles</CardTitle>
            </div>
            <CardDescription>
              VS Code dispose d'une marketplace d'extensions. Limitez-vous aux extensions téléchargées de nombreuses fois et ayant plusieurs étoiles.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Colonne gauche : Image 1, puis images 3 et 4 */}
              <div className="space-y-6">
                {/* Image 1 : Marketplace */}
                <div className="rounded-lg overflow-hidden border border-border max-w-xs">
                  <Image
                    src="/images/ide/extension_marketplace.png"
                    alt="Marketplace des extensions VS Code"
                    width={560}
                    height={440}
                    className="w-full h-auto"
                  />
                  <div className="p-3 bg-muted/50 text-sm text-muted-foreground">
                    La marketplace des extensions VS Code
                  </div>
                </div>

                {/* Image 3 : Git Extension Pack */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Package className="w-5 h-5 text-nebula-400" />
                    <h3 className="font-semibold">Git Extension Pack</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Pour la gestion de version de vos documents.
                  </p>
                  <div className="rounded-lg overflow-hidden border border-border max-w-md">
                    <Image
                      src="/images/ide/git_extension_pack.png"
                      alt="Extension Git Extension Pack"
                      width={630}
                      height={90}
                      className="w-full h-auto"
                    />
                  </div>
                </div>

                {/* Image 4 : Live Share */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <Users className="w-5 h-5 text-cosmic-400" />
                    <h3 className="font-semibold">Live Share (optionnel)</h3>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    Pour le travail collaboratif en temps réel. Meilleur qu'Overleaf et gratuit !
                  </p>
                  <div className="rounded-lg overflow-hidden border border-border w-64">
                    <Image
                      src="/images/ide/live_share_snippet.png"
                      alt="Extension Live Share"
                      width={400}
                      height={320}
                      className="w-full h-auto"
                    />
                  </div>
                </div>
              </div>

              {/* Colonne droite : Image 2 haute (LaTeX Workshop) */}
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <FileCode2 className="w-5 h-5 text-cosmic-400" />
                  <h3 className="font-semibold">LaTeX Workshop</h3>
                </div>
                <p className="text-sm text-muted-foreground">
                  L'extension principale pour compiler et prévisualiser vos documents LaTeX.
                </p>
                <div className="rounded-lg overflow-hidden border border-border max-w-sm">
                  <Image
                    src="/images/ide/latex_workshop.png"
                    alt="Extension LaTeX Workshop"
                    width={400}
                    height={570}
                    className="w-full h-auto"
                  />
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 4 : Configuration */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            4
          </div>
          <h2 className="text-3xl font-bold">Configuration de LaTeX Workshop</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Settings className="w-6 h-6 text-cosmic-400" />
              <CardTitle>Compilation automatique</CardTitle>
            </div>
            <CardDescription>
              Configurez LaTeX Workshop pour compiler automatiquement à chaque sauvegarde
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold">Étapes de configuration :</h3>

              <div className="space-y-3">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500/20 flex items-center justify-center text-cosmic-400 font-semibold text-sm">
                    1
                  </div>
                  <p className="text-muted-foreground">
                    Ouvrir les settings de l'extension LaTeX Workshop
                  </p>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500/20 flex items-center justify-center text-cosmic-400 font-semibold text-sm">
                    2
                  </div>
                  <div className="space-y-1">
                    <p className="text-muted-foreground">
                      Utiliser la barre de recherche et taper :
                    </p>
                    <code className="block px-3 py-2 rounded-md bg-muted text-sm">
                      &gt;latex workshop settings → &gt;settings Sync: Open User Settings(JSON)
                    </code>
                  </div>
                </div>

                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-cosmic-500/20 flex items-center justify-center text-cosmic-400 font-semibold text-sm">
                    3
                  </div>
                  <p className="text-muted-foreground">
                    Coller cette configuration JSON dans <code className="px-2 py-1 rounded bg-muted text-sm">settings.json</code> :
                  </p>
                </div>
              </div>
            </div>

            <CodeBlock
              filename="settings.json"
              language="json"
              code={`{
  "latex-workshop.latex.tools": [
    {
      "name": "lualatex",
      "command": "lualatex",
      "args": [
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-shell-escape",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "Compile with LuaLaTeX",
      "tools": ["lualatex"]
    }
  ],
  "latex-workshop.latex.autoBuild.run": "onSave",
  "editor.wordWrap": "on"
}`}
            />

            <div className="glass-card p-4 bg-cosmic-500/10 border-l-4 border-cosmic-400">
              <div className="flex items-start gap-3">
                <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
                <p className="text-sm">
                  <span className="font-semibold text-foreground">Résultat :</span> Désormais, à chaque sauvegarde, le fichier se compile automatiquement et le PDF est actualisé !
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Étape 5 : Travail collaboratif */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            5
          </div>
          <h2 className="text-3xl font-bold">Interface configurée de VS Code</h2>
        </div>

        <Card className="glass-card">
          <CardHeader>
            <div className="flex items-center gap-3">
              <Users className="w-6 h-6 text-nebula-400" />
              <CardTitle>Configuration type</CardTitle>
            </div>
            <CardDescription>
              Une fois configuré, votre environnement VSCode ressemblera à ceci - module les options choisies pour les styles.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className = "grid lg:grid-cols-2 gap-6 items-start">
              <p className="text-muted-foreground">
              De nombreuses fonctionnalités de styles sont disponibles pour VS Code.
              Une petite recherche sur Youtube permet de se faire une idée des possibilités de personnalisation de VS Code.
            </p>

            <div className="rounded-lg overflow-hidden border border-border">
              <Image
                src="/images/ide/VSCode_use.png"
                alt="Exemple d'environnement VS Code configuré"
                width={500}
                height={220}
                className="w-full h-auto"
              />
              <div className="p-3 bg-muted/50 text-sm text-muted-foreground">
                Exemple d'environnement VS Code parfaitement configuré pour LaTeX
              </div>
            </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Conclusion */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold text-center">Vous êtes prêt !</h2>
        <div className="space-y-4 text-center">
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Vous disposez maintenant d'un environnement professionnel pour travailler avec LaTeX,
            sans les limitations d'Overleaf. Vous pouvez utiliser des scripts, des packages personnels,
            et même intégrer vos outils IA préférés !
          </p>

          <div className="flex flex-wrap gap-4 justify-center pt-4">
            <Button asChild variant="cosmic" size="lg">
              <Link href="/claude-code/tutorials" prefetch={false}>
                Voir d'autres tutoriels
              </Link>
            </Button>
            <Button asChild variant="outline" size="lg">
              <Link href="/claude-code" prefetch={false}>
                Retour à Claude Code
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  )
}
