import Link from "next/link"
import {
  Plug,
  Cloud,
  Server,
  KeyRound,
  ShieldAlert,
  CheckCircle,
  ExternalLink,
  BookOpen,
  Info,
} from "lucide-react"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Connecteurs, serveurs MCP et clés API | Tutoriels",
  description:
    "Relier Claude à d'autres services : connecteurs claude.ai (Google Drive, Gmail, Agenda, Canva…), serveurs MCP ajoutés à Claude Code, clés API. Différences, mise en place et précautions pour un enseignant.",
}

const LIENS_OFFICIELS = [
  {
    titre: "Utiliser les connecteurs (aide Claude, en français)",
    href: "https://support.claude.com/fr/articles/11176164-utiliser-les-connecteurs-pour-etendre-les-capacites-de-claude",
  },
  {
    titre: "Répertoire des connecteurs",
    href: "https://claude.com/connectors",
  },
  {
    titre: "Claude Code et MCP (documentation, en français)",
    href: "https://code.claude.com/docs/fr/mcp",
  },
]

export default function ConnecteursPage() {
  return (
    <div className="space-y-12">
      <TutorialTracker slug="connecteurs" title="Connecteurs, serveurs MCP et clés API" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Connecteurs et API", href: "/claude-code/tutorials/connecteurs" },
        ]}
      />

      {/* En-tête */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-sky-500 to-indigo-600 mb-4">
          <Plug className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">Connecteurs, serveurs MCP et clés API</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Trois façons de relier Claude à d&apos;autres services. Aucune n&apos;est indispensable pour préparer
          ses cours : voyez-les comme des options.
        </p>
      </section>

      {/* Avertissement de ton */}
      <section className="glass-card rounded-xl p-6 border-l-4 border-sky-400">
        <div className="flex items-start gap-3">
          <Info className="w-5 h-5 text-sky-400 flex-shrink-0 mt-0.5" />
          <p className="text-muted-foreground">
            L&apos;essentiel du travail avec Claude Code se fait sur des fichiers de votre ordinateur, sans aucun
            service extérieur. Les connecteurs servent quand vos documents vivent ailleurs (un Drive, un agenda) ;
            les clés API, quand un outil précis en réclame une. Si vous n&apos;en voyez pas l&apos;usage, passez votre chemin.
          </p>
        </div>
      </section>

      {/* Comparatif */}
      <section className="space-y-6">
        <h2 className="text-3xl font-bold">Trois mécanismes, trois usages</h2>
        <div className="overflow-x-auto glass-card rounded-xl">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-left">
                <th className="p-4"></th>
                <th className="p-4 text-sky-300">Connecteur claude.ai</th>
                <th className="p-4 text-indigo-300">Serveur MCP dans Claude Code</th>
                <th className="p-4 text-amber-300">Clé API</th>
              </tr>
            </thead>
            <tbody className="text-muted-foreground">
              <tr className="border-b border-white/5">
                <td className="p-4 font-semibold text-gray-300">Ce que c&apos;est</td>
                <td className="p-4">Un accès à un service (Drive, Gmail…) que vous autorisez une fois dans votre compte Claude</td>
                <td className="p-4">Un petit programme ou une adresse web qui donne des outils à Claude Code, déclaré sur votre ordinateur</td>
                <td className="p-4">Un mot de passe technique qui permet à un script d&apos;utiliser un service payant à l&apos;usage</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-4 font-semibold text-gray-300">Où on l&apos;ajoute</td>
                <td className="p-4">claude.ai ou Claude Desktop : Personnaliser → Connecteurs</td>
                <td className="p-4">Dans le terminal : <code className="px-1 bg-slate-900 rounded">claude mcp add</code></td>
                <td className="p-4">Sur le site du service, puis dans une variable d&apos;environnement</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-4 font-semibold text-gray-300">Où ça marche</td>
                <td className="p-4">claude.ai, Desktop, application mobile et Claude Code (même compte)</td>
                <td className="p-4">Claude Code, sur cet ordinateur</td>
                <td className="p-4">Le script ou le skill qui la lit</td>
              </tr>
              <tr>
                <td className="p-4 font-semibold text-gray-300">Exemple</td>
                <td className="p-4">« Résume le compte rendu du conseil pédagogique rangé dans mon Drive »</td>
                <td className="p-4">Le serveur de data.gouv.fr pour chercher des jeux de données réels</td>
                <td className="p-4">Une clé Google Gemini pour un skill qui génère des images</td>
              </tr>
            </tbody>
          </table>
        </div>
        <p className="text-sm text-muted-foreground">
          Connecteurs et serveurs reposent sur le même protocole, <strong className="text-foreground">MCP</strong>{" "}
          (Model Context Protocol) : un connecteur est un serveur MCP qu&apos;Anthropic ou l&apos;éditeur du service
          héberge pour vous.
        </p>
      </section>

      {/* Connecteurs */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-sky-500 to-indigo-600 flex items-center justify-center">
            <Cloud className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Les connecteurs claude.ai</h2>
        </div>

        <p className="text-muted-foreground">
          Google Drive, Gmail, Google Agenda, Canva, Notion, Slack… : le{" "}
          <a href="https://claude.com/connectors" target="_blank" rel="noopener noreferrer" className="text-sky-400 hover:underline">
            répertoire des connecteurs
          </a>{" "}
          en compte des dizaines, et la liste évolue souvent. Un connecteur s&apos;ajoute une fois, dans votre compte,
          et suit ce compte partout.
        </p>

        <div className="space-y-3">
          <h3 className="font-semibold text-sky-300">Ajouter un connecteur</h3>
          <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-2">
            <li>Sur claude.ai ou dans Claude Desktop : <strong className="text-foreground">Personnaliser → Connecteurs</strong>, puis le bouton <strong className="text-foreground">+</strong>. Depuis une conversation : bouton <strong className="text-foreground">+</strong> près de la zone de saisie → Connecteurs → Gérer les connecteurs.</li>
            <li>Choisissez le service, cliquez sur <strong className="text-foreground">Connecter</strong> et suivez l&apos;authentification (fenêtre de connexion Google, Canva…).</li>
            <li>Ouvrez le connecteur et réglez ses <strong className="text-foreground">Autorisations d&apos;outils</strong> : pour chaque action, « Toujours autoriser », « Approbation requise » ou « Bloqué ». Mettez au moins les actions d&apos;écriture (envoyer un mail, créer un événement) en « Approbation requise ».</li>
          </ol>
          <p className="text-sm text-muted-foreground">
            Sur les comptes Team ou Enterprise, un administrateur doit d&apos;abord autoriser le connecteur pour l&apos;organisation.
          </p>
        </div>

        <div className="space-y-3">
          <h3 className="font-semibold text-sky-300">Les retrouver dans Claude Code</h3>
          <p className="text-muted-foreground">
            Si vous vous êtes connecté à Claude Code avec votre compte claude.ai (et non avec une clé API), vos
            connecteurs y sont disponibles automatiquement. Pour les voir, les activer ou les couper pour le projet en cours :
          </p>
          <CodeBlock code="/mcp" language="text" />
          <p className="text-sm text-muted-foreground">
            Ils apparaissent avec la mention « claude.ai ». Ils n&apos;apparaissent pas si Claude Code utilise une clé
            API (<code className="px-1 bg-slate-900 rounded">ANTHROPIC_API_KEY</code>) au lieu de votre abonnement :{" "}
            <code className="px-1 bg-slate-900 rounded">/status</code> indique le mode de connexion actif.
          </p>
          <p className="text-sm text-muted-foreground">
            Pour qu&apos;aucun connecteur claude.ai ne soit chargé dans Claude Code, ajoutez dans{" "}
            <code className="px-1 bg-slate-900 rounded">~/.claude/settings.json</code> :
          </p>
          <CodeBlock filename="settings.json" language="json" code={`{\n  "disableClaudeAiConnectors": true\n}`} />
        </div>
      </section>

      {/* Serveurs MCP */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-indigo-600 flex items-center justify-center">
            <Server className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Les serveurs MCP ajoutés à Claude Code</h2>
        </div>

        <p className="text-muted-foreground">
          Quand un service n&apos;a pas de connecteur, ou quand l&apos;outil tourne sur votre propre ordinateur, on le
          déclare directement à Claude Code. Exemple : data.gouv.fr publie un serveur MCP officiel qui permet à
          Claude de chercher et lire des jeux de données publics (utile pour des exercices de statistiques sur
          données réelles).
        </p>
        <CodeBlock code="claude mcp add --transport http datagouv https://mcp.data.gouv.fr/mcp" language="bash" />
        <p className="text-sm text-muted-foreground">
          Le serveur est alors disponible dans le dossier où vous avez lancé la commande. Ajoutez{" "}
          <code className="px-1 bg-slate-900 rounded">--scope user</code> pour l&apos;avoir dans tous vos projets.{" "}
          <code className="px-1 bg-slate-900 rounded">/mcp</code> liste les serveurs et leur état ;{" "}
          <code className="px-1 bg-slate-900 rounded">claude mcp remove datagouv</code> le retire.
        </p>
        <p className="text-sm text-muted-foreground">
          Le plus simple reste souvent de demander à Claude : « ajoute le serveur MCP de data.gouv.fr à ma
          configuration ». Un serveur qui tourne en local (lancé par <code className="px-1 bg-slate-900 rounded">npx</code>{" "}
          ou <code className="px-1 bg-slate-900 rounded">uvx</code>) demande Node.js ou Python sur le poste.
        </p>
      </section>

      {/* Clés API */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center">
            <KeyRound className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Les clés API</h2>
        </div>

        <p className="text-muted-foreground">
          Une clé API est un mot de passe technique qui ouvre un service facturé à l&apos;usage (génération
          d&apos;images, synthèse vocale…). Certains skills en ont besoin ; votre abonnement Claude, lui, n&apos;en
          demande aucune.
        </p>
        <ul className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span>Rangez-la dans une variable d&apos;environnement ou un fichier <code className="px-1 bg-slate-900 rounded">.env</code> qui ne quitte pas votre poste, jamais dans un fichier partagé, un CLAUDE.md ou un skill.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span>Ne la collez pas dans la conversation : indiquez à Claude le nom de la variable qui la contient.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span>Fixez un plafond de dépense mensuel sur le site du fournisseur, et supprimez la clé si vous pensez qu&apos;elle a fuité.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span>
              Cas particulier : une variable <code className="px-1 bg-slate-900 rounded">ANTHROPIC_API_KEY</code> présente
              sur le poste peut faire facturer Claude Code à l&apos;usage au lieu de votre abonnement. Ne la définissez que si c&apos;est voulu.
            </span>
          </li>
        </ul>
      </section>

      {/* Précautions */}
      <section className="glass-card rounded-xl p-8 space-y-5 border-2 border-red-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-red-600 flex items-center justify-center">
            <ShieldAlert className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Précautions</h2>
        </div>
        <ul className="space-y-3 text-muted-foreground">
          <li>
            <strong className="text-red-300">Pas de données d&apos;élèves.</strong> Ne connectez pas un compte qui
            contient des données personnelles d&apos;élèves (messagerie de l&apos;ENT, dossier de notes, copies
            nominatives, adresse professionnelle qui reçoit des messages de familles). Ce que Claude lit par un
            connecteur part chez Anthropic et, selon le service, chez des tiers : le RGPD s&apos;applique.
          </li>
          <li>
            <strong className="text-red-300">Le moindre privilège.</strong> Connectez seulement ce dont vous avez
            besoin, plutôt un compte ou un dossier dédié aux ressources de cours, et laissez les actions d&apos;écriture
            en « Approbation requise ».
          </li>
          <li>
            <strong className="text-red-300">Méfiance envers le contenu lu.</strong> Un mail ou un document peut
            contenir des instructions cachées destinées à l&apos;IA (« injection de prompt »). Relisez ce que Claude
            propose d&apos;envoyer ou de modifier.
          </li>
          <li>
            <strong className="text-red-300">Des sources de confiance.</strong> Les connecteurs personnalisés et les
            serveurs MCP tiers ne sont pas vérifiés par Anthropic : n&apos;ajoutez que ceux d&apos;éditeurs connus.
          </li>
          <li>
            <strong className="text-red-300">Faire le ménage.</strong> Déconnectez ce que vous n&apos;utilisez plus
            (Personnaliser → Connecteurs, ou <code className="px-1 bg-slate-900 rounded">claude mcp remove</code>).
          </li>
        </ul>
      </section>

      {/* Liens */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-sky-400" />
          <h2 className="text-2xl font-bold">Documentation officielle</h2>
        </div>
        <div className="grid sm:grid-cols-3 gap-3">
          {LIENS_OFFICIELS.map((l) => (
            <a
              key={l.href}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="glass-card rounded-lg p-4 border border-white/10 hover:border-sky-400/40 transition-colors flex items-start gap-2"
            >
              <ExternalLink className="w-4 h-4 text-sky-400 flex-shrink-0 mt-0.5" />
              <span className="text-sm text-gray-200">{l.titre}</span>
            </a>
          ))}
        </div>
        <p className="text-sm text-muted-foreground">
          Pour aller plus loin côté Claude Desktop, la capsule{" "}
          <Link
            href="/claude-code/tutorials/parcours/claude-desktop/cd-extensions"
            className="text-sky-400 hover:underline"
          >
            Extensions MCP
          </Link>{" "}
          montre les extensions et connecteurs de l&apos;application.
        </p>
      </section>
    </div>
  )
}
