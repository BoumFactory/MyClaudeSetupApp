import Link from "next/link"
import {
  AppWindow,
  Laptop,
  Gauge,
  ShieldCheck,
  Download,
  HardDrive,
  Rocket,
  Package,
  ShieldAlert,
  AlertCircle,
  CheckCircle,
  MessageSquareText,
  BookOpen,
  ExternalLink,
  Lightbulb,
} from "lucide-react"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import { CodeBlock } from "@/components/ui/code-block"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Première application React + Tauri | Tutoriels",
  description:
    "Créer sa première application locale avec React et Tauri en demandant tout à Claude Code : installation des logiciels, workspace avec cache Rust partagé, création de l'application, installeur à partager.",
}

/* ------------------------------------------------------------------ */
/* Prompts                                                             */
/* ------------------------------------------------------------------ */

const PROMPT_INSTALLATION = `Installe sur mon ordinateur tout ce qu'il faut pour créer des applications Tauri 2 avec React, en suivant la page officielle https://v2.tauri.app/start/prerequisites/ :
- Microsoft C++ Build Tools avec la charge de travail « Développement Desktop en C++ » ;
- Rust par rustup, avec la chaîne MSVC par défaut ;
- vérifie que WebView2 est présent.
Vérifie aussi Node.js, pnpm et Git, et installe ce qui manque.
Utilise winget. Avant chaque installation, dis-moi ce que tu installes.
À la fin, montre-moi les versions installées.`

const PROMPT_WORKSPACE = `Prépare un workspace d'applications dans D:\\Applications avec un cache Rust partagé :
- crée le dossier s'il n'existe pas ;
- ajoute un fichier .cargo/config.toml qui envoie toutes les compilations Rust dans D:/Applications/.cargo-target et qui réduit les infos de débogage en développement (debug = "line-tables-only") ;
- écris à la racine un CLAUDE.md qui rappelle ces conventions.
Si j'ai déjà des applications Tauri dans ce dossier, liste-les avec la taille de leur dossier src-tauri/target, sans rien supprimer.`

const PROMPT_CREATION = `Dans D:\\Applications, crée une application Tauri 2 + React + TypeScript nommée tirage-au-sort, avec pnpm create tauri-app (modèle react-ts, gestionnaire pnpm).
Ce qu'elle fait :
- je colle la liste de ma classe, un prénom par ligne ;
- je clique sur « Tirer au sort » et un prénom s'affiche en grand ;
- le même élève ne sort pas deux fois tant que toute la liste n'est pas passée ;
- la liste reste enregistrée sur l'ordinateur pour la prochaine fois.
Interface en français, gros caractères lisibles au vidéoprojecteur.
Installe les dépendances, mais ne lance pas l'application : je lancerai pnpm tauri dev moi-même.`

const PROMPT_VERIF_CIBLE = `Dans tirage-au-sort, vérifie avec cargo metadata que le dossier de compilation Rust est bien D:/Applications/.cargo-target.`

const PROMPT_INSTALLEUR = `Produis l'installeur Windows de tirage-au-sort avec pnpm tauri build, puis donne-moi le chemin exact du fichier -setup.exe et sa taille.`

const ITERATIONS = [
  "Ajoute un bouton « Remettre tout le monde » qui recommence le tirage depuis le début.",
  "Affiche en petit, sous le prénom, combien d'élèves restent à passer.",
  "Je veux pouvoir garder plusieurs listes (une par classe) et choisir la classe dans un menu.",
  "Le prénom est trop petit au fond de la salle : double sa taille et mets un fond sombre.",
]

const CONFIG_TOML = `[build]
target-dir = "D:/Applications/.cargo-target"

[profile.dev]
debug = "line-tables-only"`

const ARBORESCENCE = `D:\\Applications\\
├── .cargo\\
│   └── config.toml        ← « compile tout dans .cargo-target »
├── .cargo-target\\         ← LE cache partagé (créé à la 1re compilation)
│   ├── debug\\             ← pnpm tauri dev
│   └── release\\
│       └── bundle\\        ← les installeurs (pnpm tauri build)
├── CLAUDE.md              ← les conventions, pour l'agent
├── tirage-au-sort\\        ← application 1
│   ├── src\\               ← l'interface (React)
│   └── src-tauri\\         ← le moteur (Rust), sans dossier target
└── minuteur-de-classe\\    ← application 2, qui réutilise le cache`

const CLAUDE_MD = `# Workspace d'applications

Une application par sous-dossier. Stack : Tauri 2 + React + TypeScript, pnpm.

## Cache Rust partagé
- .cargo/config.toml envoie toutes les compilations Rust dans .cargo-target/.
  Ne pas le modifier ; ne pas définir de target-dir propre à une application.
- Les installeurs sont dans .cargo-target/release/bundle/ (nsis = -setup.exe, msi = .msi),
  pas dans src-tauri/target.
- Ne jamais lancer cargo clean sans me demander : il vide le cache de toutes les applications.
- Une compilation à la fois : si cargo attend un verrou, patienter.

## Conventions
- Nouvelle application : pnpm create tauri-app <nom> --template react-ts --manager pnpm.
  Nom en minuscules, sans accents ni espaces, différent des applications existantes.
- pnpm uniquement (pas npm, pas yarn).
- Je lance moi-même pnpm tauri dev : tu ne le lances pas.`

const RECAPITULATIF = [
  { etape: "Installer les logiciels", prompt: PROMPT_INSTALLATION },
  { etape: "Préparer le workspace", prompt: PROMPT_WORKSPACE },
  { etape: "Créer l'application", prompt: PROMPT_CREATION },
  { etape: "Lancer l'application (vous, dans le terminal)", prompt: "cd D:\\Applications\\tirage-au-sort\npnpm tauri dev" },
  { etape: "Vérifier le cache partagé", prompt: PROMPT_VERIF_CIBLE },
  { etape: "Produire l'installeur", prompt: PROMPT_INSTALLEUR },
]

/* ------------------------------------------------------------------ */
/* Petits composants de mise en page                                   */
/* ------------------------------------------------------------------ */

function TitreEtape({ numero, titre }: { numero: number; titre: string }) {
  return (
    <div className="flex items-center gap-4">
      <div className="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center text-white font-bold text-xl">
        {numero}
      </div>
      <h2 className="text-3xl font-bold">{titre}</h2>
    </div>
  )
}

function Bloc({ titre, couleur, children }: { titre: string; couleur: string; children: React.ReactNode }) {
  return (
    <div className="space-y-2">
      <p className={`font-semibold ${couleur}`}>{titre}</p>
      {children}
    </div>
  )
}

function Code({ children }: { children: React.ReactNode }) {
  return <code className="px-1 bg-slate-900 rounded">{children}</code>
}

/* ------------------------------------------------------------------ */
/* Page                                                                */
/* ------------------------------------------------------------------ */

export default function PremiereAppTauriPage() {
  return (
    <div className="space-y-12">
      <TutorialTracker slug="premiere-app-tauri" title="Première application React + Tauri" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Première application Tauri", href: "/claude-code/tutorials/premiere-app-tauri" },
        ]}
      />

      {/* En-tête */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-amber-500 to-orange-600 mb-4">
          <AppWindow className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">Ma première application React + Tauri</h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Une vraie application de bureau, installée sur votre ordinateur, faite pour votre classe.
          Vous ne tapez presque rien : vous savez quoi demander à l&apos;agent.
        </p>
      </section>

      {/* Le principe */}
      <section className="glass-card rounded-xl p-6 border-2 border-amber-500/30 space-y-3">
        <div className="flex items-center gap-3">
          <MessageSquareText className="w-6 h-6 text-amber-400" />
          <h2 className="text-xl font-bold">Le principe de ce tutoriel</h2>
        </div>
        <p className="text-muted-foreground">Chaque étape tient en trois temps :</p>
        <ul className="space-y-2 text-muted-foreground">
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span><strong className="text-foreground">Ce que vous demandez</strong> : un prompt à copier dans Claude Code.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span><strong className="text-foreground">Ce que l&apos;agent fait</strong> : pour savoir à quoi vous attendre.</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-1" />
            <span><strong className="text-foreground">Comment vérifier</strong> : le signe que tout s&apos;est bien passé.</span>
          </li>
        </ul>
        <p className="text-sm text-muted-foreground">
          Il vous faut Claude Code déjà installé (
          <Link href="/claude-code/tutorials/claude-code-install" className="text-amber-400 hover:underline">
            voir le tutoriel
          </Link>
          ). Les exemples sont pour Windows ; un encart traite macOS et Linux.
        </p>
      </section>

      {/* 1. Pourquoi */}
      <section className="space-y-6">
        <TitreEtape numero={1} titre="Pourquoi React + Tauri ?" />

        <div className="grid md:grid-cols-3 gap-4">
          <div className="glass-card rounded-xl p-5 space-y-2 border border-amber-500/20">
            <Laptop className="w-6 h-6 text-amber-400" />
            <h3 className="font-semibold text-amber-300">Locale</h3>
            <p className="text-sm text-muted-foreground">
              Pas de serveur, pas de compte, pas d&apos;abonnement. Les données (vos listes d&apos;élèves, par exemple)
              restent sur votre ordinateur.
            </p>
          </div>
          <div className="glass-card rounded-xl p-5 space-y-2 border border-amber-500/20">
            <Gauge className="w-6 h-6 text-amber-400" />
            <h3 className="font-semibold text-amber-300">Légère et rapide</h3>
            <p className="text-sm text-muted-foreground">
              Tauri utilise le moteur web déjà présent dans Windows (WebView2) au lieu d&apos;embarquer un navigateur
              complet. Selon sa documentation, une application minimale peut peser moins de 600 Ko.
            </p>
          </div>
          <div className="glass-card rounded-xl p-5 space-y-2 border border-amber-500/20">
            <ShieldCheck className="w-6 h-6 text-amber-400" />
            <h3 className="font-semibold text-amber-300">Fiable</h3>
            <p className="text-sm text-muted-foreground">
              Le cœur est écrit en Rust, un langage qui écarte toute une famille d&apos;erreurs de mémoire.
              Tauri fait auditer sa sécurité à chaque version majeure ou mineure.
            </p>
          </div>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-3">
          <p className="text-muted-foreground">Une application Tauri a deux parties :</p>
          <ul className="space-y-2 text-muted-foreground">
            <li>
              <strong className="text-sky-300">L&apos;interface, en React</strong> : les boutons, les textes, les couleurs.
              C&apos;est une page web, celle que vous voyez.
            </li>
            <li>
              <strong className="text-orange-300">Le moteur, en Rust</strong> : la fenêtre, l&apos;accès aux fichiers,
              la fabrication de l&apos;installeur.
            </li>
          </ul>
          <p className="text-sm text-muted-foreground">
            Et Electron, qu&apos;utilisent beaucoup d&apos;applications connues ? Il embarque Chromium et Node.js dans
            chaque application. C&apos;est confortable pour le développeur, mais chaque installeur transporte un
            navigateur entier. Avec Tauri, les installeurs que l&apos;auteur de ce site a produits pour ses
            applications de classe font entre 1,6 et 7 Mo.
          </p>
        </div>
      </section>

      {/* 2. Logiciels */}
      <section className="space-y-6">
        <TitreEtape numero={2} titre="Installer les logiciels" />

        <div className="overflow-x-auto rounded-lg border border-white/10">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-white/10 text-left">
                <th className="p-3 text-amber-300">Logiciel</th>
                <th className="p-3 text-amber-300">À quoi il sert</th>
              </tr>
            </thead>
            <tbody className="text-muted-foreground">
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">Node.js + pnpm</td>
                <td className="p-3">
                  Construire l&apos;interface React (
                  <Link href="/claude-code/tutorials/nodejs-install" className="text-amber-400 hover:underline">
                    tutoriel Node.js
                  </Link>
                  ).
                </td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">Rust (rustup, chaîne MSVC)</td>
                <td className="p-3">Compiler le moteur de l&apos;application.</td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">Microsoft C++ Build Tools</td>
                <td className="p-3">
                  Les outils de Microsoft dont Rust a besoin sous Windows. Charge de travail
                  « Développement Desktop en C++ » (en anglais : <em>Desktop development with C++</em>).
                </td>
              </tr>
              <tr className="border-b border-white/5">
                <td className="p-3 font-semibold text-gray-300">WebView2</td>
                <td className="p-3">
                  Le moteur web qui affiche l&apos;interface. Déjà présent sous Windows 10 (version 1803 et suivantes)
                  et Windows 11.
                </td>
              </tr>
              <tr>
                <td className="p-3 font-semibold text-gray-300">Git</td>
                <td className="p-3">
                  Garder l&apos;historique de vos versions ; Claude Code s&apos;en sert sous Windows (
                  <Link href="/claude-code/tutorials/git-install" className="text-amber-400 hover:underline">
                    tutoriel Git
                  </Link>
                  ).
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div className="glass-card rounded-xl p-8 space-y-6">
          <Bloc titre="Ce que vous demandez" couleur="text-amber-300">
            <CodeBlock language="text" code={PROMPT_INSTALLATION} />
          </Bloc>

          <Bloc titre="Ce que l'agent fait" couleur="text-sky-300">
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              <li>Il regarde ce qui est déjà installé, puis installe le reste avec winget, l&apos;outil d&apos;installation de Windows.</li>
              <li>Pour les Build Tools, il ajoute la charge de travail C++ (sinon seul le noyau s&apos;installe).</li>
              <li>Il règle Rust sur la chaîne MSVC (<Code>rustup default stable-msvc</Code> si Rust était déjà là).</li>
            </ul>
          </Bloc>

          <div className="p-4 rounded-lg bg-amber-950/30 border border-amber-800 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
            <div className="text-sm text-muted-foreground space-y-1">
              <p>
                <strong className="text-amber-300">Restez devant l&apos;écran.</strong> Windows affiche des fenêtres
                « Voulez-vous autoriser cette application à apporter des modifications ? » : c&apos;est à vous de cliquer sur Oui.
              </p>
              <p>
                Les Build Tools pèsent plusieurs gigaoctets : comptez un bon moment. Ensuite, fermez et rouvrez le
                terminal ; parfois, il faut redémarrer l&apos;ordinateur.
              </p>
            </div>
          </div>

          <Bloc titre="Comment vérifier" couleur="text-emerald-300">
            <p className="text-sm text-muted-foreground">
              Dans un nouveau terminal, chaque commande doit afficher un numéro de version :
            </p>
            <CodeBlock language="powershell" code={`node --version\npnpm --version\nrustc --version\ncargo --version\ngit --version`} />
            <p className="text-sm text-muted-foreground">
              Et <Code>rustup default</Code> doit afficher une ligne qui se termine par <Code>windows-msvc</Code>.
            </p>
          </Bloc>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-3 border-l-4 border-slate-400">
          <h3 className="font-semibold text-gray-200">Sur macOS ou Linux</h3>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>
              <strong className="text-foreground">macOS</strong> : pas de Build Tools ni de WebView2. Il faut les outils
              en ligne de commande d&apos;Apple (<Code>xcode-select --install</Code>), ou Xcode complet si vous visez aussi l&apos;iPhone.
              Rust s&apos;installe avec rustup.
            </li>
            <li>
              <strong className="text-foreground">Linux</strong> : une liste de paquets système (WebKitGTK, outils de
              compilation…), différente selon la distribution.
            </li>
          </ul>
          <p className="text-sm text-muted-foreground">
            Le même prompt fonctionne : l&apos;agent lit la page des prérequis et suit la partie qui correspond à
            votre système.
          </p>
        </div>
      </section>

      {/* 3. Workspace */}
      <section className="space-y-6">
        <TitreEtape numero={3} titre="Le point central : un workspace d'applications" />

        <div className="glass-card rounded-xl p-8 space-y-5 border-2 border-orange-500/50 bg-orange-950/10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-orange-600 flex items-center justify-center">
              <HardDrive className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-2xl font-bold text-orange-300">À faire avant la première application</h3>
          </div>

          <p className="text-muted-foreground">
            Rust compile tout depuis le code source : Tauri et ses centaines de dépendances. Par défaut, chaque
            application garde ce travail dans son propre dossier <Code>src-tauri/target</Code>.
          </p>

          <div className="p-4 rounded-lg bg-red-950/30 border border-red-800 space-y-1">
            <p className="font-semibold text-red-300">Ce qui se passe sans workspace</p>
            <p className="text-sm text-muted-foreground">
              Chez l&apos;auteur de ce site, ce dossier pesait entre <strong className="text-foreground">2,3 Go et 4,9 Go
              par application</strong>. Et les mêmes dépendances étaient recompilées pour chacune, avec à chaque fois
              une longue première compilation.
            </p>
          </div>

          <div className="p-4 rounded-lg bg-emerald-950/30 border border-emerald-800 space-y-1">
            <p className="font-semibold text-emerald-300">La solution : un dossier parent unique, un cache partagé</p>
            <p className="text-sm text-muted-foreground">
              Toutes vos applications vivent dans un même dossier, sur un disque qui a de la place
              (par exemple <Code>D:\Applications\</Code>, ou <Code>Documents\Applications\</Code> si vous n&apos;avez
              qu&apos;un disque). Un petit fichier à sa racine dit à Rust : « compile tout au même endroit ».
              Les dépendances identiques (même version, mêmes options) sont compilées une fois, puis réutilisées :
              la première compilation de la deuxième application est bien plus rapide.
            </p>
          </div>

          <div className="space-y-2">
            <p className="font-semibold text-gray-200">L&apos;arborescence visée</p>
            <CodeBlock language="text" code={ARBORESCENCE} />
          </div>

          <div className="space-y-2">
            <p className="font-semibold text-gray-200">Pourquoi ça marche</p>
            <p className="text-sm text-muted-foreground">
              Cargo (l&apos;outil de compilation de Rust) cherche un fichier <Code>.cargo/config.toml</Code> dans
              le dossier courant, puis dans chaque dossier parent. Un seul fichier à la racine du workspace vaut donc
              pour toutes les applications rangées dessous. Le réglage <Code>build.target-dir</Code> y fixe le dossier
              où va toute la compilation.
            </p>
            <CodeBlock language="toml" filename=".cargo/config.toml" code={CONFIG_TOML} />
            <p className="text-sm text-muted-foreground">
              La seconde partie est facultative. En développement, Rust ajoute par défaut toutes les informations de
              débogage ; <Code>&quot;line-tables-only&quot;</Code> ne garde que les numéros de ligne, utiles en cas
              d&apos;erreur. Le dossier de compilation s&apos;en trouve allégé.
            </p>
          </div>
        </div>

        <div className="glass-card rounded-xl p-8 space-y-6">
          <Bloc titre="Ce que vous demandez" couleur="text-amber-300">
            <CodeBlock language="text" code={PROMPT_WORKSPACE} />
            <p className="text-sm text-muted-foreground">
              Adaptez le chemin s&apos;il le faut. Évitez les accents et les espaces dans le nom du dossier.
            </p>
          </Bloc>

          <Bloc titre="Ce que l'agent fait" couleur="text-sky-300">
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              <li>Il crée le dossier, le fichier <Code>.cargo/config.toml</Code> ci-dessus et un <Code>CLAUDE.md</Code>.</li>
              <li>
                Le <Code>CLAUDE.md</Code> est lu par Claude Code chaque fois que vous travaillez dans ce dossier : les
                conventions n&apos;ont plus à être répétées.
              </li>
            </ul>
          </Bloc>

          <Bloc titre="Le CLAUDE.md du workspace (exemple)" couleur="text-gray-200">
            <CodeBlock language="markdown" filename="CLAUDE.md" code={CLAUDE_MD} />
          </Bloc>

          <Bloc titre="Comment vérifier" couleur="text-emerald-300">
            <p className="text-sm text-muted-foreground">
              Les deux fichiers sont là. La vraie preuve viendra à l&apos;étape 4, après la première compilation :
              un dossier <Code>.cargo-target</Code> apparaît à la racine, et aucun dossier <Code>target</Code> dans{" "}
              <Code>src-tauri</Code>.
            </p>
          </Bloc>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-3 border-l-4 border-amber-400">
          <h3 className="font-semibold text-amber-300">Les contreparties, à connaître</h3>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>
              <strong className="text-foreground">Une compilation à la fois.</strong> Deux applications compilées en
              même temps se partagent le même dossier : la seconde attend que la première ait fini
              (cargo affiche « Blocking waiting for file lock »). Rien n&apos;est cassé, il suffit d&apos;attendre.
            </li>
            <li>
              <strong className="text-foreground">L&apos;installeur change de place.</strong> Il n&apos;est plus dans{" "}
              <Code>src-tauri/target/release/bundle/</Code> mais dans <Code>.cargo-target/release/bundle/</Code>.
            </li>
            <li>
              <strong className="text-foreground"><Code>cargo clean</Code> vide tout.</strong> Il efface le cache de
              toutes les applications d&apos;un coup : la suivante repartira de zéro.
            </li>
            <li>
              <strong className="text-foreground">Des noms différents.</strong> Deux applications qui porteraient le
              même nom écriraient leur programme au même endroit du cache. Donnez à chacune un nom unique.
            </li>
          </ul>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-3 border-l-4 border-sky-400">
          <h3 className="font-semibold text-sky-300">Bon à savoir</h3>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>
              <strong className="text-foreground">Côté interface, pnpm partage déjà.</strong> Il garde chaque paquet
              une seule fois dans un magasin commun et le relie à vos projets au lieu de le copier. Ce partage ne
              joue que sur un même disque : avec des projets sur D:, pnpm crée un magasin sur D:.
            </li>
            <li>
              <strong className="text-foreground">Disque C: plein ?</strong> Rust lui-même (compilateur et sources
              téléchargées) vit dans <Code>.rustup</Code> et <Code>.cargo</Code>, dans votre dossier personnel. On
              peut l&apos;installer ailleurs en définissant les variables <Code>RUSTUP_HOME</Code> et{" "}
              <Code>CARGO_HOME</Code> avant l&apos;installation ; elles doivent ensuite rester définies. Demandez-le
              à l&apos;agent dès l&apos;étape 2 si votre disque C: est petit.
            </li>
          </ul>
        </div>
      </section>

      {/* 4. Première application */}
      <section className="space-y-6">
        <TitreEtape numero={4} titre="Créer la première application" />

        <div className="glass-card rounded-xl p-8 space-y-6">
          <Bloc titre="Ce que vous demandez" couleur="text-amber-300">
            <p className="text-sm text-muted-foreground">
              Ouvrez Claude Code dans votre workspace (<Code>D:\Applications</Code>), puis :
            </p>
            <CodeBlock language="text" code={PROMPT_CREATION} />
            <p className="text-sm text-muted-foreground">
              Autre idée pour commencer : un minuteur de classe, avec de gros chiffres et une alarme douce.
            </p>
          </Bloc>

          <Bloc titre="Ce que l'agent fait" couleur="text-sky-300">
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              <li>
                Il crée le squelette avec la commande officielle, sans questions grâce à ses options :{" "}
                <Code>pnpm create tauri-app tirage-au-sort --template react-ts --manager pnpm</Code>.
              </li>
              <li>Il installe les dépendances (<Code>pnpm install</Code>) et écrit l&apos;interface demandée.</li>
              <li>Il s&apos;arrête là : c&apos;est vous qui lancez l&apos;application.</li>
            </ul>
          </Bloc>

          <Bloc titre="Lancer l'application (vous)" couleur="text-gray-200">
            <p className="text-sm text-muted-foreground">
              Dans un terminal, depuis le dossier de l&apos;application :
            </p>
            <CodeBlock language="powershell" code={"cd D:\\Applications\\tirage-au-sort\npnpm tauri dev"} />
            <div className="p-4 rounded-lg bg-amber-950/30 border border-amber-800 flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-amber-300">La toute première fois, c&apos;est long.</strong> Rust compile
                Tauri et toutes ses dépendances : comptez plusieurs minutes, davantage sur un ordinateur modeste.
                Les fois suivantes, et pour vos applications suivantes grâce au workspace, c&apos;est bien plus court.
              </p>
            </div>
            <p className="text-sm text-muted-foreground">
              Une fenêtre s&apos;ouvre avec votre application. Laissez ce terminal ouvert : tant qu&apos;il tourne,
              chaque modification faite par l&apos;agent apparaît dans la fenêtre.
            </p>
          </Bloc>

          <Bloc titre="Comment vérifier" couleur="text-emerald-300">
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              <li>La fenêtre affiche votre application, et le tirage fonctionne.</li>
              <li>
                Le dossier <Code>D:\Applications\.cargo-target</Code> existe, et{" "}
                <Code>tirage-au-sort\src-tauri</Code> ne contient pas de dossier <Code>target</Code>. Pour en
                avoir le cœur net :
              </li>
            </ul>
            <CodeBlock language="text" code={PROMPT_VERIF_CIBLE} />
          </Bloc>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-4 border border-emerald-500/20">
          <div className="flex items-center gap-3">
            <Lightbulb className="w-6 h-6 text-emerald-400" />
            <h3 className="text-xl font-bold">Ensuite, améliorer en français</h3>
          </div>
          <p className="text-sm text-muted-foreground">
            L&apos;application tourne, la fenêtre est ouverte : décrivez ce que vous voulez changer, une chose à la
            fois, et regardez le résultat.
          </p>
          <div className="grid md:grid-cols-2 gap-3">
            {ITERATIONS.map((p) => (
              <CodeBlock key={p} language="text" code={p} />
            ))}
          </div>
          <p className="text-sm text-muted-foreground">
            Si quelque chose ne marche pas, copiez le message d&apos;erreur du terminal dans votre message à
            l&apos;agent : il ne voit pas ce terminal.
          </p>
        </div>
      </section>

      {/* 5. Installeur */}
      <section className="space-y-6">
        <TitreEtape numero={5} titre="Produire l'installeur et le partager" />

        <div className="glass-card rounded-xl p-8 space-y-6">
          <Bloc titre="Ce que vous demandez" couleur="text-amber-300">
            <p className="text-sm text-muted-foreground">Fermez d&apos;abord la fenêtre de développement, puis :</p>
            <CodeBlock language="text" code={PROMPT_INSTALLEUR} />
          </Bloc>

          <Bloc titre="Ce que l'agent fait" couleur="text-sky-300">
            <p className="text-sm text-muted-foreground">
              Il lance <Code>pnpm tauri build</Code> : une compilation optimisée (de nouveau un peu longue la première
              fois), puis la fabrication des installeurs.
            </p>
          </Bloc>

          <Bloc titre="Où le trouver" couleur="text-emerald-300">
            <p className="text-sm text-muted-foreground">Avec le workspace, dans le cache partagé :</p>
            <CodeBlock
              language="text"
              code={`D:\\Applications\\.cargo-target\\release\\bundle\\\n├── nsis\\   ← tirage-au-sort_0.1.0_x64-setup.exe  (celui à partager)\n└── msi\\    ← tirage-au-sort_0.1.0_x64_en-US.msi`}
            />
            <p className="text-sm text-muted-foreground">
              Le fichier <Code>-setup.exe</Code> suffit pour un collègue. Le <Code>.msi</Code> sert surtout aux
              déploiements par un service informatique ; s&apos;il manque, la documentation de Tauri indique qu&apos;il
              demande la fonctionnalité facultative VBSCRIPT de Windows.
            </p>
          </Bloc>
        </div>

        <div className="glass-card rounded-xl p-6 space-y-3 border-l-4 border-red-400">
          <div className="flex items-center gap-3">
            <ShieldAlert className="w-5 h-5 text-red-400" />
            <h3 className="font-semibold text-red-300">Partager avec un collègue : l&apos;avertissement de Windows</h3>
          </div>
          <ul className="list-disc list-inside space-y-2 text-sm text-muted-foreground">
            <li>
              Votre installeur n&apos;est pas <strong className="text-foreground">signé</strong> (une signature
              s&apos;achète auprès d&apos;une autorité de certification). Windows SmartScreen affichera donc
              « Windows a protégé votre ordinateur ». Le collègue clique sur{" "}
              <strong className="text-foreground">Informations complémentaires</strong>, puis{" "}
              <strong className="text-foreground">Exécuter quand même</strong>.
            </li>
            <li>
              Sous Windows 11, si le <strong className="text-foreground">contrôle intelligent des applications</strong>{" "}
              (Smart App Control) est activé, une application non signée est bloquée, sans possibilité de
              l&apos;autoriser au cas par cas.
            </li>
            <li>
              Si WebView2 manque sur le poste du collègue, l&apos;installeur le télécharge par défaut : il faut alors
              une connexion internet pendant l&apos;installation.
            </li>
            <li>
              Ne partagez que ce que vous avez fait vous-même, et dites au collègue d&apos;où vient le fichier.
            </li>
          </ul>
        </div>
      </section>

      {/* 6. Récapitulatif */}
      <section className="space-y-6">
        <TitreEtape numero={6} titre="Récapitulatif : les prompts dans l'ordre" />

        <div className="space-y-4">
          {RECAPITULATIF.map((r, i) => (
            <div key={r.etape} className="glass-card rounded-xl p-5 space-y-2">
              <p className="font-semibold text-amber-300">
                {i + 1}. {r.etape}
              </p>
              <CodeBlock language="text" code={r.prompt} />
            </div>
          ))}
        </div>

        <p className="text-sm text-muted-foreground">
          Pour la deuxième application, seules les étapes 3 à 6 se répètent, dans le même workspace.
        </p>
      </section>

      {/* Documentation */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-l-4 border-amber-400">
        <div className="flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-amber-400" />
          <h2 className="text-2xl font-bold">Pour aller plus loin</h2>
        </div>
        <div className="grid sm:grid-cols-2 gap-3">
          {[
            { href: "https://v2.tauri.app/start/prerequisites/", texte: "Tauri 2 : les prérequis, système par système" },
            { href: "https://v2.tauri.app/start/create-project/", texte: "Tauri 2 : créer un projet" },
            { href: "https://v2.tauri.app/distribute/windows-installer/", texte: "Tauri 2 : l'installeur Windows" },
            { href: "https://doc.rust-lang.org/cargo/reference/config.html", texte: "Cargo : les fichiers de configuration (hiérarchie, build.target-dir)" },
          ].map((l) => (
            <a
              key={l.href}
              href={l.href}
              target="_blank"
              rel="noopener noreferrer"
              className="glass-card rounded-lg p-4 border border-white/10 hover:border-amber-400/40 transition-colors flex items-start gap-2"
            >
              <ExternalLink className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
              <span className="text-sm text-gray-200">{l.texte} (en anglais)</span>
            </a>
          ))}
        </div>
        <div className="flex flex-wrap gap-3 pt-2 text-sm">
          <Link href="/claude-code/tutorials/nodejs-install" className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500/15 text-green-400 hover:bg-green-500/25 transition-colors">
            <Package className="w-4 h-4" /> Tutoriel Node.js
          </Link>
          <Link href="/claude-code/tutorials/git-install" className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-orange-500/15 text-orange-400 hover:bg-orange-500/25 transition-colors">
            <Download className="w-4 h-4" /> Tutoriel Git
          </Link>
          <Link href="/claude-code/tutorials/claude-code-install" className="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-cosmic-500/15 text-cosmic-400 hover:bg-cosmic-500/25 transition-colors">
            <Rocket className="w-4 h-4" /> Installer Claude Code
          </Link>
        </div>
      </section>
    </div>
  )
}
