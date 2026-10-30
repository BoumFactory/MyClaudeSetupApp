import Link from "next/link"
import { Zap, Keyboard, FolderOpen, Braces, Bot, Check, PlayCircle, ArrowLeft } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Snippets LaTeX dans VS Code - Tutoriels",
  description:
    "Créer des snippets VS Code pour taper ses macros et environnements LaTeX en quelques touches, et les faire écrire par Claude Code à partir de ses besoins.",
}

const EXEMPLE_SNIPPET = `{
  "Fraction": {
    "scope": "latex",
    "prefix": "fr",
    "body": "\\\\dfrac{$1}{$2}$0",
    "description": "Fraction en grand format"
  },
  "Liste": {
    "scope": "latex",
    "prefix": "liste",
    "body": [
      "\\\\begin{\${1|itemize,enumerate|}}",
      "\\t\\\\item \${2:premier élément}",
      "\\\\end{$1}",
      "$0"
    ],
    "description": "Liste à puces ou numérotée"
  }
}`

const REGLAGE_TAB = `"[latex]": {
  "editor.tabCompletion": "on"
}`

const EXEMPLE_RACCOURCIS = `[
  {
    "key": "alt+f r",
    "command": "editor.action.insertSnippet",
    "args": { "langId": "latex", "name": "Fraction" },
    "when": "editorTextFocus && editorLangId == latex"
  }
]`

const PROMPT = `Je veux des snippets VS Code pour écrire mon LaTeX plus vite.
Mes besoins : [facultatif, décrivez-les ici : macros que vous tapez souvent,
environnements, paquets utilisés, préfixes souhaités. Sinon, laissez tel quel.]

Consignes :
1. Si je n'ai décrit aucun besoin, ne crée rien tout de suite. Pose-moi d'abord
   des questions, par petites séries, avec des propositions concrètes :
   - les commandes et environnements que je tape le plus souvent (appuie-toi sur
     mes fichiers .tex de ce dossier s'il y en a, et montre-moi ce que tu y vois) ;
   - les paquets que j'utilise ;
   - si les snippets doivent servir dans tous mes projets (snippets utilisateur,
     fichier latex.json) ou seulement dans ce dossier (.vscode/latex.code-snippets) ;
   - les préfixes qui les déclenchent (courts, en français ou en anglais) ;
   - si je veux aussi des raccourcis clavier pour les plus fréquents
     (par exemple Alt+F puis R pour une fraction).
   Récapitule ensuite en une ligne par snippet et attends ma confirmation.
2. N'invente aucune commande : vérifie la syntaxe exacte de chaque macro dans mes
   fichiers ou dans la documentation du paquet.
3. Format VS Code : "scope": "latex", "prefix", "body" (une chaîne par ligne),
   "description". Utilise les tabulations $1, \${2:texte par défaut}, les choix
   \${1|a,b,c|} et $0 pour la position finale. Double chaque antislash (\\\\begin).
4. Si un fichier de snippets existe déjà, complète-le sans rien écraser.
   Raccourcis clavier : ajoute-les à mon keybindings.json avec la commande
   editor.action.insertSnippet (args : langId "latex" et le nom du snippet),
   limités aux fichiers LaTeX ("when": "editorTextFocus && editorLangId == latex").
   Vérifie qu'ils n'écrasent pas un raccourci existant, et active
   "editor.tabCompletion": "on" pour LaTeX.
5. Vérifie que le JSON est valide, puis donne-moi un tableau
   « préfixe → ce que ça insère » et dis-moi comment les tester.`

function Etape({ n, titre, icone: Icone, children }: { n: number; titre: string; icone: typeof Zap; children: React.ReactNode }) {
  return (
    <section className="space-y-6">
      <div className="flex items-center gap-4">
        <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
          {n}
        </div>
        <h2 className="text-3xl font-bold flex items-center gap-3">
          {titre}
          <Icone className="w-6 h-6 text-cosmic-400" />
        </h2>
      </div>
      {children}
    </section>
  )
}

export default function VSCodeSnippetsPage() {
  return (
    <div className="space-y-12">
      <TutorialTracker slug="vscode-snippets" title="Snippets LaTeX dans VS Code" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Snippets VS Code", href: "/claude-code/tutorials/vscode-snippets" },
        ]}
      />

      {/* En-tête */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Keyboard className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">Snippets LaTeX dans VS Code</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Tapez trois lettres, appuyez sur Tab : l&apos;environnement complet s&apos;écrit, le curseur attend
          à la bonne place. Et Claude Code peut écrire ces raccourcis pour vous.
        </p>
      </section>

      <div className="glass-card rounded-xl p-5 border-l-4 border-cosmic-400 text-sm text-muted-foreground">
        Prérequis : VS Code et l&apos;extension LaTeX Workshop, installés avec le{" "}
        <Link href="/claude-code/tutorials/vscode-miktex" prefetch={false} className="text-cosmic-400 hover:underline">
          tutoriel VS Code + MiKTeX
        </Link>
        . LaTeX Workshop complète déjà les commandes LaTeX courantes ; les snippets ajoutent les vôtres.
      </div>

      <Etape n={1} titre="Ce qu'un snippet fait pour vous" icone={Zap}>
        <Card className="glass-card">
          <CardContent className="pt-6 space-y-4 text-muted-foreground">
            <p>
              Un snippet est un modèle de texte associé à un préfixe. Dans un fichier <code>.tex</code>, vous
              tapez le préfixe, VS Code le propose dans la liste de suggestions, et Tab (ou Entrée) le
              remplace par le modèle.
            </p>
            <ul className="space-y-2">
              <li className="flex gap-2"><Check className="w-5 h-5 text-cosmic-400 flex-shrink-0" />Des <strong className="text-foreground">cases à remplir</strong> : Tab passe de l&apos;une à la suivante.</li>
              <li className="flex gap-2"><Check className="w-5 h-5 text-cosmic-400 flex-shrink-0" />Des <strong className="text-foreground">choix</strong> : une petite liste s&apos;ouvre (nombre de colonnes, type de liste…).</li>
              <li className="flex gap-2"><Check className="w-5 h-5 text-cosmic-400 flex-shrink-0" />Un <strong className="text-foreground">texte modifié une fois</strong> se répète partout où il apparaît, par exemple le nom d&apos;un environnement dans <code>\begin</code> et <code>\end</code>.</li>
            </ul>
          </CardContent>
        </Card>
      </Etape>

      <Etape n={2} titre="Où les ranger" icone={FolderOpen}>
        <div className="grid md:grid-cols-2 gap-5">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-lg">Pour tous vos projets</CardTitle>
              <CardDescription>Snippets utilisateur</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-muted-foreground">
              <p>
                Ctrl+Maj+P, puis <code>Snippets: Configure Snippets</code> (« Extraits de code : configurer
                les extraits ») et choisissez <strong className="text-foreground">latex</strong>.
              </p>
              <p>
                VS Code ouvre le fichier <code>latex.json</code> de votre profil : ses snippets marchent dans
                tous vos dossiers.
              </p>
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-lg">Pour un dossier précis</CardTitle>
              <CardDescription>Snippets de projet</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2 text-sm text-muted-foreground">
              <p>
                Un fichier <code>.vscode/latex.code-snippets</code> à la racine du dossier ouvert dans VS Code.
              </p>
              <p>
                Ses snippets ne marchent que dans ce dossier, et voyagent avec lui : pratique pour les partager
                avec un collègue.
              </p>
            </CardContent>
          </Card>
        </div>
      </Etape>

      <Etape n={3} titre="À quoi ressemble un snippet" icone={Braces}>
        <Card className="glass-card">
          <CardContent className="pt-6 space-y-4">
            <CodeBlock filename="latex.code-snippets" language="json" code={EXEMPLE_SNIPPET} />
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li><code>prefix</code> : ce que vous tapez ; <code>body</code> : ce qui s&apos;écrit, une chaîne par ligne.</li>
              <li><code>$1</code>, <code>$2</code> : les cases, dans l&apos;ordre de Tab ; <code>{"${2:texte}"}</code> : une case préremplie.</li>
              <li><code>{"${1|itemize,enumerate|}"}</code> : un choix ; <code>$0</code> : où le curseur finit.</li>
              <li>
                <strong className="text-foreground">Piège :</strong> en JSON, l&apos;antislash se double.{" "}
                <code>\\begin</code> dans le fichier donne <code>\begin</code> dans votre document.
              </li>
            </ul>
          </CardContent>
        </Card>
      </Etape>

      <Etape n={4} titre="Les faire écrire par Claude Code" icone={Bot}>
        <Card className="glass-card">
          <CardContent className="pt-6 space-y-4">
            <p className="text-muted-foreground">
              Ouvrez Claude Code dans le dossier de vos fichiers LaTeX et collez ce prompt.
            </p>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li className="flex gap-2">
                <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0" />
                <span><strong className="text-foreground">Vous savez ce que vous voulez</strong> : décrivez-le à la ligne « Mes besoins », Claude écrit les snippets.</span>
              </li>
              <li className="flex gap-2">
                <Check className="w-5 h-5 text-cosmic-400 flex-shrink-0" />
                <span><strong className="text-foreground">Vous ne savez pas encore</strong> : laissez la ligne telle quelle. Claude regarde vos fichiers, vous pose des questions, puis attend votre accord avant d&apos;écrire.</span>
              </li>
            </ul>
            <CodeBlock filename="prompt à copier" language="text" code={PROMPT} />
          </CardContent>
        </Card>
      </Etape>

      <Etape n={5} titre="Aller plus vite : Tab et raccourcis clavier" icone={Keyboard}>
        <div className="grid md:grid-cols-2 gap-5">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-lg">Préfixe puis Tab</CardTitle>
              <CardDescription>Pour tous les snippets d&apos;un coup</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <p>
                Avec ce réglage, <code>mc</code> puis Tab insère le snippet directement, sans attendre la liste
                de suggestions. À mettre dans <code>settings.json</code> (utilisateur ou <code>.vscode/</code> du
                dossier).
              </p>
              <CodeBlock filename="settings.json" language="json" code={REGLAGE_TAB} />
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-lg">Un raccourci par snippet</CardTitle>
              <CardDescription>Alt+F puis R pour une fraction</CardDescription>
            </CardHeader>
            <CardContent className="space-y-3 text-sm text-muted-foreground">
              <p>
                Ctrl+Maj+P, puis <code>Preferences: Open Keyboard Shortcuts (JSON)</code>. Chaque ligne lie une
                touche, ou une suite de deux touches, au <strong className="text-foreground">nom</strong> d&apos;un
                snippet (la clé avant les deux-points dans le fichier de snippets).
              </p>
              <CodeBlock filename="keybindings.json" language="json" code={EXEMPLE_RACCOURCIS} />
            </CardContent>
          </Card>
        </div>
        <div className="glass-card rounded-xl p-5 border-l-4 border-amber-400 text-sm text-muted-foreground space-y-2">
          <p>
            <strong className="text-foreground">Alt et les menus :</strong> sous Windows, Alt+F ouvre aussi le menu
            Fichier. Si le menu s&apos;ouvre à la place du snippet, ajoutez{" "}
            <code>&quot;window.enableMenuBarMnemonics&quot;: false</code> à vos paramètres utilisateur.
          </p>
          <p>
            Les raccourcis valent pour tous vos dossiers, mais un snippet de projet n&apos;existe que dans son
            dossier : ailleurs, le raccourci ne fait rien. Claude Code peut écrire ces raccourcis avec les snippets :
            demandez-le-lui dans le prompt.
          </p>
        </div>
      </Etape>

      <Etape n={6} titre="Tester" icone={PlayCircle}>
        <Card className="glass-card">
          <CardContent className="pt-6 space-y-3 text-muted-foreground">
            <p>Ouvrez un fichier <code>.tex</code> et tapez un préfixe : le snippet apparaît dans la liste, Tab l&apos;insère.</p>
            <p>
              Rien ne s&apos;affiche ? Ctrl+Espace ouvre la liste des suggestions à la demande. Si un snippet
              manque toujours, le fichier contient sans doute une erreur de JSON : VS Code la souligne en rouge
              quand vous l&apos;ouvrez.
            </p>
          </CardContent>
        </Card>
      </Etape>

      {/* Suite */}
      <section className="glass-card rounded-xl p-8 space-y-6 text-center">
        <h2 className="text-2xl font-bold">Et ensuite ?</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Ajoutez un snippet chaque fois que vous vous surprenez à retaper la même structure. Il suffit de
          redonner le prompt à Claude Code avec le nouveau besoin : il complète le fichier existant.
        </p>
        <div className="flex flex-wrap gap-4 justify-center">
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/tutorials/vscode-miktex" prefetch={false}>
              <ArrowLeft className="w-4 h-4 mr-2" />
              VS Code + MiKTeX
            </Link>
          </Button>
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/tutorials" prefetch={false}>
              Voir d&apos;autres tutoriels
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
