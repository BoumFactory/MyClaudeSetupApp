import Link from "next/link"
import {
  Blocks,
  PanelRight,
  Bell,
  Terminal,
  ShieldAlert,
  Download,
  Lightbulb,
  MessageSquareText,
  FolderTree,
  Power,
  BookOpen,
  ExternalLink,
  CheckCircle,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Les mods de Claude Code | Tutoriels",
  description:
    "Personnaliser l'interface et le comportement de Claude Code avec des mods : panneau, bandeau, notification, commande. Les demander à Claude, les installer, un exemple à télécharger (notifications de bureau) et des idées pour enseignants.",
}

const CE_QUE_FAIT_UN_MOD = [
  { titre: "Un panneau", texte: "à côté de la conversation, qui se met à jour (avancement d'une fournée, liste de fichiers produits…)" },
  { titre: "Un bandeau", texte: "au-dessus de la zone de saisie (le projet en cours, un rappel)" },
  { titre: "Une notification", texte: "dans Claude Code, ou même sur le bureau Windows" },
  { titre: "Une commande", texte: "/quelque-chose qui exécute votre code tout de suite, sans faire travailler Claude" },
  { titre: "Une règle sur les actions", texte: "bloquer, modifier ou signaler un appel d'outil avant qu'il s'exécute" },
  { titre: "Un habillage", texte: "redessiner une partie de l'interface : le texte du spinner, une ligne d'outil…" },
]

const IDEES = [
  {
    titre: "Une jauge de contexte",
    pourquoi: "Savoir d'un coup d'œil quand la conversation devient trop longue et qu'il vaut mieux repartir d'une session neuve.",
    prompt:
      "Fais-moi un mod qui affiche au-dessus de la zone de saisie une petite jauge du contexte utilisé (en pourcentage), qui passe en orange au-delà de 60 % et en rouge au-delà de 80 %.",
  },
  {
    titre: "Un rappel de compilation",
    pourquoi: "Ne pas oublier de compiler et de relire le PDF après une série de modifications d'un fichier LaTeX ou Typst.",
    prompt:
      "Fais-moi un mod qui, à la fin d'une réponse où Claude a modifié des fichiers .tex ou .typ sans les compiler ensuite, affiche une notification « Pensez à compiler : » suivie des noms des fichiers concernés.",
  },
  {
    titre: "Le bandeau du projet en cours",
    pourquoi: "Avec plusieurs terminaux ouverts (une classe, une séquence chacun), savoir tout de suite dans lequel on tape.",
    prompt:
      "Fais-moi un mod qui affiche au-dessus de la zone de saisie le nom du dossier de travail en gras, et le niveau de classe s'il apparaît dans le chemin (2nde, 1re, Tle, 3e…), dans une couleur différente par niveau.",
  },
]

export default function ModsPage() {
  return (
    <div className="space-y-12">
      <TutorialTracker slug="mods" title="Les mods de Claude Code" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Les mods", href: "/claude-code/tutorials/mods" },
        ]}
      />

      {/* En-tête */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-fuchsia-500 to-violet-600 mb-4">
          <Blocks className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">Les mods de Claude Code</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Un mod modifie Claude Code lui-même : ce qu&apos;il affiche et la façon dont il se comporte.
          On ne l&apos;écrit pas : on le décrit, et Claude le fabrique.
        </p>
      </section>

      {/* Qu'est-ce qu'un mod */}
      <section className="glass-card rounded-xl p-8 space-y-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-fuchsia-500 to-violet-600 flex items-center justify-center">
            <PanelRight className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Ce qu&apos;un mod peut ajouter</h2>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {CE_QUE_FAIT_UN_MOD.map((c) => (
            <div key={c.titre} className="p-4 rounded-lg bg-fuchsia-950/20 border border-fuchsia-800/50">
              <p className="font-semibold text-fuchsia-300 mb-1">{c.titre}</p>
              <p className="text-sm text-muted-foreground">{c.texte}</p>
            </div>
          ))}
        </div>
        <p className="text-muted-foreground">
          Les mods fonctionnent dans Claude Code en terminal, dans l&apos;onglet Code de Claude Desktop et dans
          l&apos;extension VS Code, à partir de la version <strong className="text-foreground">2.1.287</strong>{" "}
          (vérifiez avec <code className="px-1 bg-slate-900 rounded">claude --version</code>).
        </p>

        <div className="overflow-x-auto rounded-lg border border-white/10">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-left">
                <th className="p-3"></th>
                <th className="p-3 text-fuchsia-300">Mod</th>
                <th className="p-3 text-violet-300">Skill</th>
                <th className="p-3 text-sky-300">Hook (settings.json)</th>
              </tr>
            </thead>
            <tbody className="text-muted-foreground">
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">Agit sur</td>
                <td className="p-3">l&apos;interface et les événements de Claude Code</td>
                <td className="p-3">ce que Claude sait faire</td>
                <td className="p-3">autoriser, bloquer ou journaliser une action, par un script</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">Peut dessiner</td>
                <td className="p-3">oui</td>
                <td className="p-3">non</td>
                <td className="p-3">non</td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-gray-300">Écrit en</td>
                <td className="p-3">TypeScript ou JavaScript (par Claude)</td>
                <td className="p-3">Markdown</td>
                <td className="p-3">un script et une ligne de réglage</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      {/* Où ils vivent */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-violet-600 flex items-center justify-center">
            <FolderTree className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Où ils vivent</h2>
        </div>
        <p className="text-muted-foreground">
          Un mod est un petit dossier de trois fichiers : une fiche d&apos;identité, un fichier qui pointe vers le
          code, et le code lui-même.
        </p>
        <CodeBlock
          language="text"
          code={`notif-bureau/\n├── .claude-plugin/\n│   └── plugin.json      ← nom, version, description\n└── hooks/\n    ├── hooks.json       ← « le code est dans register.ts »\n    └── register.ts      ← le code`}
        />
        <ul className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-violet-400 flex-shrink-0 mt-1" />
            <span>
              <strong className="text-foreground">Un mod que Claude vient d&apos;écrire</strong> est rangé dans{" "}
              <code className="px-1 bg-slate-900 rounded">~/.claude/dev-mods/</code>, dans un dossier propre à la
              session. Ce dossier est temporaire : pour garder le mod, demandez à Claude de le copier ailleurs (voir plus bas).
            </span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-violet-400 flex-shrink-0 mt-1" />
            <span>
              <strong className="text-foreground">Un mod installé</strong> vient d&apos;une « marketplace » : un dossier
              ou un dépôt GitHub qui en liste un ou plusieurs. La commande{" "}
              <code className="px-1 bg-slate-900 rounded">/plugin</code>, onglet Installed, montre les mods actifs.
            </span>
          </li>
        </ul>
      </section>

      {/* Demander un mod */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-fuchsia-500 to-violet-600 flex items-center justify-center">
            <MessageSquareText className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Demander un mod à Claude</h2>
        </div>

        <div className="glass-card rounded-xl p-8 space-y-5">
          <ol className="space-y-4 text-muted-foreground">
            <li>
              <p className="font-semibold text-foreground">1. Décrire ce que vous voulez, avec vos mots</p>
              <p className="text-sm mb-2">
                Commencez par « fais-moi un mod qui… ». Claude charge de lui-même le skill intégré{" "}
                <code className="px-1 bg-slate-900 rounded">plugin-authoring</code>, qui connaît tout le
                fonctionnement des mods de votre version.
              </p>
              <CodeBlock
                language="text"
                code="Fais-moi un mod qui affiche au-dessus de la zone de saisie le nom du dossier où je travaille."
              />
            </li>
            <li>
              <p className="font-semibold text-foreground">2. Accepter la question « activer les mods de cette session ? »</p>
              <p className="text-sm">
                Au premier fichier écrit, Claude Code vous demande s&apos;il peut charger les mods que Claude écrit.
                Répondez oui : le mod se charge à la fin de la réponse, et se recharge après chaque correction.
              </p>
            </li>
            <li>
              <p className="font-semibold text-foreground">3. Essayer, puis corriger en parlant</p>
              <p className="text-sm">
                « Mets-le en vert », « affiche-le seulement quand… » : chaque demande est appliquée dès que Claude a
                fini de répondre. Si une ligne grisée signale qu&apos;une modification n&apos;a pas pu se charger,
                copiez-la dans votre message suivant : Claude ne la voit pas.
              </p>
            </li>
            <li>
              <p className="font-semibold text-foreground">4. Le garder pour les prochaines sessions</p>
              <p className="text-sm mb-2">Un mod écrit en session ne se charge que dans cette session. Pour le conserver :</p>
              <CodeBlock
                language="text"
                code="Copie ce mod dans un dossier à moi (par exemple ~/.claude/mes-mods), fais de ce dossier une marketplace et installe le mod pour toutes mes sessions."
              />
            </li>
          </ol>
        </div>
      </section>

      {/* Installer un mod */}
      <section className="glass-card rounded-xl p-8 space-y-5">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center">
            <Terminal className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Installer un mod existant</h2>
        </div>
        <p className="text-muted-foreground">
          Un mod s&apos;installe comme un plugin, depuis une marketplace : on ajoute la marketplace une fois, puis
          on installe le mod par son nom.
        </p>
        <CodeBlock
          language="bash"
          code={`claude plugin marketplace add <dossier ou propriétaire/dépôt GitHub>\nclaude plugin install <nom-du-mod>@<nom-de-la-marketplace>`}
        />
        <p className="text-sm text-muted-foreground">
          Dans une session ouverte, <code className="px-1 bg-slate-900 rounded">/reload-plugins</code> charge le mod
          sans redémarrer. Anthropic partage aussi quelques{" "}
          <a
            href="https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods"
            target="_blank"
            rel="noopener noreferrer"
            className="text-fuchsia-400 hover:underline"
          >
            mods d&apos;exemple
          </a>{" "}
          (une météo du contexte, un garde-fou sur les commandes risquées…), en anglais.
        </p>
        <div className="p-4 rounded-lg bg-red-950/30 border border-red-800 flex items-start gap-3">
          <ShieldAlert className="w-5 h-5 text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-muted-foreground">
            <strong className="text-red-300">Un mod n&apos;est pas isolé.</strong> Il s&apos;exécute avec vos droits :
            il peut lire vos fichiers, voir vos messages, lancer des programmes. N&apos;installez que des mods de
            sources de confiance. Pour voir ce qu&apos;un mod fait avant de l&apos;installer :{" "}
            <code className="px-1 bg-slate-900 rounded">claude plugin validate &lt;dossier du mod&gt;</code> liste les
            événements qu&apos;il écoute et les actions qu&apos;il demande.
          </p>
        </div>
      </section>

      {/* Exemple : notif-bureau */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
            <Bell className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Un exemple à télécharger : notif-bureau</h2>
        </div>

        <div className="glass-card rounded-xl p-8 space-y-5 border-2 border-amber-500/30">
          <p className="text-muted-foreground">
            Pendant que Claude travaille, on part souvent faire autre chose dans une autre fenêtre. Ce mod affiche
            une notification en bas à droite de l&apos;écran Windows, <strong className="text-foreground">seulement si
            la fenêtre de Claude Code n&apos;est pas au premier plan</strong> :
          </p>
          <ul className="space-y-2 text-muted-foreground">
            <li className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
              <span><strong className="text-foreground">Tâche terminée</strong> : la durée et la première phrase de la réponse, puis la carte s&apos;efface après 5 secondes.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
              <span><strong className="text-foreground">Claude vous pose une question à choix</strong> : les choix sont dans la notification, on répond sans revenir au terminal.</span>
            </li>
            <li className="flex items-start gap-2">
              <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
              <span><strong className="text-foreground">La réponse se termine par une question</strong> : un champ de saisie dans la notification ; ce qu&apos;on tape part comme message.</span>
            </li>
          </ul>
          <p className="text-sm text-muted-foreground">
            Plusieurs sessions ouvertes partagent la même pile de cartes, et un bouton ramène au bon terminal.
            Windows 10 ou 11 uniquement ; rien à installer en plus (le mod compile au premier lancement son petit
            programme d&apos;affichage avec le compilateur présent dans Windows).
          </p>

          <div className="flex flex-wrap gap-3">
            <Button asChild variant="default" size="lg">
              <a href="/download/mods/notif-bureau.zip" download className="flex items-center gap-2">
                <Download className="w-4 h-4" />
                Télécharger notif-bureau (zip, 15 Ko)
              </a>
            </Button>
          </div>

          <div className="space-y-3">
            <h3 className="font-semibold text-amber-300">Installation</h3>
            <ol className="list-decimal list-inside space-y-2 text-sm text-muted-foreground">
              <li>
                Décompressez l&apos;archive et placez le dossier <code className="px-1 bg-slate-900 rounded">mods-enseignant</code>{" "}
                à un endroit stable, par exemple dans <code className="px-1 bg-slate-900 rounded">C:\Users\&lt;vous&gt;\.claude\</code>{" "}
                (le mod est lu depuis ce dossier : ne le déplacez plus ensuite).
              </li>
              <li>Dans un terminal, tapez les deux commandes suivantes (en adaptant le chemin) :</li>
            </ol>
            <CodeBlock
              language="powershell"
              code={`claude plugin marketplace add "$env:USERPROFILE\\.claude\\mods-enseignant"\nclaude plugin install notif-bureau@mods-enseignant`}
            />
            <p className="text-sm text-muted-foreground">
              Relancez Claude Code : <code className="px-1 bg-slate-900 rounded">/plugin</code> doit afficher{" "}
              <code className="px-1 bg-slate-900 rounded">notif-bureau</code> dans l&apos;onglet Installed. Le fichier
              README de l&apos;archive détaille la désinstallation et la modification.
            </p>
          </div>

          <div className="space-y-3">
            <h3 className="font-semibold text-amber-300">Ou le faire fabriquer par Claude</h3>
            <p className="text-sm text-muted-foreground">
              Sur macOS, ou pour une version à votre goût, donnez cette description à Claude :
            </p>
            <CodeBlock
              language="text"
              code={`Fais-moi un mod de notifications de bureau pour la session principale (pas les sous-agents), qui ne s'affichent que si la fenêtre de mon terminal n'a pas le focus :\n- à la fin d'une réponse ordinaire : « Tâche terminée » avec la durée et la première phrase, qui s'efface après 5 secondes ;\n- quand tu me poses une question à choix : les choix cliquables dans la notification, et ma réponse renvoyée directement ;\n- quand ta réponse se termine par une question : un champ de réponse dans la notification, envoyé comme message.\nLes notifications s'empilent en bas à droite et un bouton ramène au terminal.`}
            />
          </div>
        </div>
      </section>

      {/* Idées */}
      <section className="space-y-6">
        <div className="flex items-center gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
            <Lightbulb className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Des idées à demander</h2>
        </div>
        <p className="text-muted-foreground">
          Ces mods n&apos;existent pas tout faits : ce sont des pistes. Copiez le prompt, ajustez-le à votre goût, et
          laissez Claude le fabriquer.
        </p>
        <div className="grid lg:grid-cols-3 gap-4">
          {IDEES.map((idee) => (
            <div key={idee.titre} className="glass-card rounded-xl p-5 space-y-3 border border-emerald-500/20">
              <h3 className="font-semibold text-emerald-300">{idee.titre}</h3>
              <p className="text-sm text-muted-foreground">{idee.pourquoi}</p>
              <CodeBlock language="text" code={idee.prompt} />
            </div>
          ))}
        </div>
        <p className="text-sm text-muted-foreground">
          Pour une simple ligne d&apos;informations sous la zone de saisie (modèle, dossier, coût de la session), pas
          besoin de mod : la commande <code className="px-1 bg-slate-900 rounded">/statusline</code> configure la
          ligne de statut classique.
        </p>
      </section>

      {/* Désactiver */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-slate-600 flex items-center justify-center">
            <Power className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Couper un mod</h2>
        </div>
        <ul className="list-disc list-inside space-y-2 text-muted-foreground">
          <li>
            <strong className="text-foreground">Un seul mod</strong> : <code className="px-1 bg-slate-900 rounded">/plugin</code>,
            onglet Installed, puis le désactiver ou le désinstaller.
          </li>
          <li>
            <strong className="text-foreground">Tous, le temps d&apos;une session</strong> : lancer{" "}
            <code className="px-1 bg-slate-900 rounded">claude --safe-mode</code> (coupe aussi vos autres personnalisations).
          </li>
          <li>
            <strong className="text-foreground">Tous, durablement</strong> :{" "}
            <code className="px-1 bg-slate-900 rounded">&quot;disableAllHooks&quot;: true</code> dans{" "}
            <code className="px-1 bg-slate-900 rounded">~/.claude/settings.json</code> (coupe aussi vos hooks et votre ligne de statut).
          </li>
        </ul>
      </section>

      {/* Documentation */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-l-4 border-fuchsia-400">
        <div className="flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-fuchsia-400" />
          <h2 className="text-2xl font-bold">Documentation officielle d&apos;Anthropic</h2>
        </div>
        <div className="grid sm:grid-cols-2 gap-3">
          <a
            href="https://code.claude.com/docs/fr/plugins/mods/overview"
            target="_blank"
            rel="noopener noreferrer"
            className="glass-card rounded-lg p-4 border border-white/10 hover:border-fuchsia-400/40 transition-colors flex items-start gap-2"
          >
            <ExternalLink className="w-4 h-4 text-fuchsia-400 flex-shrink-0 mt-0.5" />
            <span className="text-sm text-gray-200">Aperçu des mods (en français) : ce qu&apos;ils font, les installer, leur faire confiance</span>
          </a>
          <a
            href="https://code.claude.com/docs/fr/plugins/mods/create"
            target="_blank"
            rel="noopener noreferrer"
            className="glass-card rounded-lg p-4 border border-white/10 hover:border-fuchsia-400/40 transition-colors flex items-start gap-2"
          >
            <ExternalLink className="w-4 h-4 text-fuchsia-400 flex-shrink-0 mt-0.5" />
            <span className="text-sm text-gray-200">Créer un mod (en français) : le demander à Claude, ou suivre le tutoriel pas à pas</span>
          </a>
        </div>
        <p className="text-sm text-muted-foreground">
          Voir aussi :{" "}
          <Link href="/claude-code/tutorials/creer-un-skill" className="text-fuchsia-400 hover:underline">
            créer son propre skill
          </Link>
          , l&apos;autre façon d&apos;adapter Claude Code à votre manière de travailler.
        </p>
      </section>
    </div>
  )
}
