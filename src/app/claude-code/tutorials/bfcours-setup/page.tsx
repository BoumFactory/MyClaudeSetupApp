import {
  Package,
  FolderGit,
  Settings,
  CheckCircle,
  AlertCircle,
  Terminal,
  FileCode,
  RefreshCw,
  Lightbulb,
  ArrowRight,
  Copy
} from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"
import Image from "next/image"

export const metadata: Metadata = {
  title: "Installation du package bfcours | Tutoriels Claude Code",
  description:
    "Guide complet pour installer et configurer le package LaTeX bfcours pour l'enseignement des mathématiques avec MikTeX.",
}

/**
 * Page tutoriel : Installation du package bfcours
 *
 * Guide étape par étape pour configurer bfcours avec MikTeX
 */
export default function BfcoursSetupPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="bfcours-setup" title="Installation du package bfcours" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Installation bfcours", href: "/claude-code/tutorials/bfcours-setup" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Package className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation du package bfcours
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Guide complet pour installer et configurer votre environnement LaTeX
          avec le package bfcours personnalisé
        </p>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
            <Lightbulb className="w-6 h-6 text-white" />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-bold">Qu'est-ce que bfcours ?</h2>
            <p className="text-muted-foreground">
              <strong className="text-foreground">bfcours</strong> est un package LaTeX
              personnalisé créé spécialement pour l'enseignement des mathématiques.
              Il fournit des environnements et commandes pour créer rapidement des cours,
              exercices, activités et évaluations de qualité professionnelle.
            </p>
            <div className="bg-cosmic-900/20 border border-cosmic-700/30 rounded-lg p-4 space-y-2">
              <p className="text-sm font-semibold text-cosmic-300">Avantages :</p>
              <ul className="text-sm text-muted-foreground space-y-1 ml-4 list-disc">
                <li>Mise en page cohérente et professionnelle</li>
                <li>Environnements prédéfinis pour exercices et activités</li>
                <li>Commandes mathématiques simplifiées</li>
                <li>Gestion automatique des titres et numérotation</li>
                <li>Compatible avec Claude Code pour génération automatique</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Prérequis */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold flex items-center gap-3">
          <CheckCircle className="w-7 h-7 text-green-500" />
          Prérequis
        </h2>
        <p className="text-muted-foreground">
          Avant de commencer, assurez-vous d'avoir les éléments suivants :
        </p>

        <div className="grid md:grid-cols-3 gap-4">
          <Card className="glass-card border-cosmic-700/30">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <FileCode className="w-5 h-5 text-cosmic-400" />
                MikTeX
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Distribution LaTeX installée et configurée
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/claude-code/tutorials/vscode-miktex" prefetch={false}>
                  Guide d'installation
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="glass-card border-cosmic-700/30">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <FileCode className="w-5 h-5 text-cosmic-400" />
                VS Code + LaTeX Workshop
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Éditeur avec extension LaTeX Workshop installée
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <Link href="/claude-code/tutorials/vscode-miktex" prefetch={false}>
                  Configuration VS Code
                </Link>
              </Button>
            </CardContent>
          </Card>

          <Card className="glass-card border-cosmic-700/30">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <FolderGit className="w-5 h-5 text-cosmic-400" />
                Git
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Git installé pour cloner le repository
              </p>
              <Button asChild variant="outline" size="sm" className="w-full">
                <a href="https://git-scm.com/downloads" target="_blank" rel="noopener noreferrer">
                  Télécharger Git
                </a>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Installation - Étape 1 */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            1
          </div>
          <div className="flex-1 space-y-4">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-3 mb-2">
                <FolderGit className="w-7 h-7 text-cosmic-400" />
                Récupérer le package bfcours
              </h2>
              <p className="text-muted-foreground">
                Vous avez deux méthodes pour obtenir le package bfcours et ses dépendances.
              </p>
            </div>

            {/* Méthode 1 : Téléchargement direct */}
            <Card className="glass-card border-cosmic-700/30">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Package className="w-5 h-5 text-cosmic-400" />
                  Méthode 1 : Téléchargement direct (recommandé)
                </CardTitle>
                <CardDescription>
                  Téléchargez directement l'archive ZIP depuis ce site
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <ol className="text-sm text-muted-foreground space-y-2 list-decimal ml-4">
                  <li>
                    Rendez-vous sur la page de téléchargement :
                    <Button asChild variant="outline" size="sm" className="ml-2">
                      <Link href="/claude-code/downloads" prefetch={false}>
                        Téléchargements
                      </Link>
                    </Button>
                  </li>
                  <li>Dans la section "Packages LaTeX", téléchargez <strong className="text-foreground">bfcours - profDeleuze</strong></li>
                  <li>Extrayez l'archive ZIP dans un emplacement permanent (voir ci-dessous)</li>
                </ol>
              </CardContent>
            </Card>

            {/* Méthode 2 : GitHub */}
            <Card className="glass-card border-cosmic-700/30">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <FolderGit className="w-5 h-5 text-cosmic-400" />
                  Méthode 2 : Clone GitHub
                </CardTitle>
                <CardDescription>
                  Pour les utilisateurs avancés qui souhaitent accéder au code source
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="bg-cosmic-900/20 border border-cosmic-700/30 rounded-lg p-4 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-semibold text-cosmic-300">Commande Git</span>
                    <Copy className="w-4 h-4 text-muted-foreground cursor-pointer hover:text-cosmic-400" />
                  </div>
                  <pre className="bg-black/30 rounded p-3 overflow-x-auto">
                    <code className="text-sm text-green-400">
                      git clone https://github.com/Romain1099/BFCours.git localtexmf
                    </code>
                  </pre>
                </div>
                <Button asChild variant="outline" size="sm" className="w-full">
                  <a href="https://github.com/Romain1099/BFCours.git" target="_blank" rel="noopener noreferrer">
                    Voir le repository GitHub
                  </a>
                </Button>
              </CardContent>
            </Card>

            {/* Important : emplacement */}
            <div className="flex items-start gap-3 bg-amber-900/20 border border-amber-700/30 rounded-lg p-4">
              <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
              <div className="space-y-1">
                <p className="text-sm font-semibold text-amber-300">Important - Emplacement permanent</p>
                <p className="text-sm text-muted-foreground">
                  Quelle que soit la méthode choisie, placez le dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code> dans
                  un emplacement <strong>permanent</strong>, car MikTeX devra y accéder régulièrement.
                </p>
                <p className="text-sm text-muted-foreground">
                  Emplacement recommandé : <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">
                    C:\Users\VotreNom\Documents\LaTeX\localtexmf
                  </code>
                </p>
              </div>
            </div>

            {/* Structure attendue */}
            <div className="space-y-2">
              <p className="text-sm font-semibold">Structure attendue du dossier :</p>
              <pre className="bg-black/30 rounded p-4 overflow-x-auto text-sm">
                <code className="text-muted-foreground">
{`C:\\Users\\VotreNom\\Documents\\LaTeX\\
└── localtexmf/
    ├── tex/
    │   └── latex/
    │       └── bfcours/
    │           ├── bfcours.sty
    │           ├── bfcours-exos.sty
    │           ├── bfcours-activites.sty
    │           └── [autres fichiers .sty]
    └── README.md`}
                </code>
              </pre>
            </div>
          </div>
        </div>
      </section>

      {/* Installation - Étape 2 */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full nebula-gradient flex items-center justify-center text-white font-bold text-xl">
            2
          </div>
          <div className="flex-1 space-y-4">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-3 mb-2">
                <Settings className="w-7 h-7 text-nebula-400" />
                Configurer le localtexmf dans MikTeX
              </h2>
              <p className="text-muted-foreground">
                Le dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-sm">localtexmf</code> contient
                le package bfcours et doit être enregistré dans MikTeX pour être reconnu.
              </p>
            </div>

            <div className="space-y-4">
              {/* Sous-étape 2.1 */}
              <Card className="glass-card border-nebula-700/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <ArrowRight className="w-4 h-4 text-nebula-400" />
                    2.1 - Localiser le dossier localtexmf
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <p className="text-sm text-muted-foreground">
                    Après avoir cloné le repository, identifiez le chemin complet vers le dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code>.
                  </p>
                  <div className="bg-cosmic-900/20 border border-cosmic-700/30 rounded p-3">
                    <p className="text-xs font-semibold text-cosmic-300 mb-1">Exemple de chemin :</p>
                    <code className="text-sm text-green-400">
                      C:\Users\VotreNom\Documents\LaTeX\localtexmf
                    </code>
                  </div>
                </CardContent>
              </Card>

              {/* Sous-étape 2.2 */}
              <Card className="glass-card border-nebula-700/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <ArrowRight className="w-4 h-4 text-nebula-400" />
                    2.2 - Copier le chemin d'accès
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <ul className="text-sm text-muted-foreground space-y-1 list-disc ml-4">
                    <li>Faites un clic droit sur le dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code></li>
                    <li>Sélectionnez "Copier en tant que chemin d'accès"</li>
                    <li>Ou copiez-le manuellement en notant le chemin complet</li>
                  </ul>
                </CardContent>
              </Card>

              {/* Sous-étape 2.3 */}
              <Card className="glass-card border-nebula-700/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <ArrowRight className="w-4 h-4 text-nebula-400" />
                    2.3 - Ouvrir MikTeX Console
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                  <ul className="text-sm text-muted-foreground space-y-1 list-disc ml-4">
                    <li>Ouvrez le menu Démarrer de Windows</li>
                    <li>Recherchez "MikTeX Console"</li>
                    <li>Lancez l'application</li>
                  </ul>
                </CardContent>
              </Card>

              {/* Sous-étape 2.4 */}
              <Card className="glass-card border-nebula-700/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <ArrowRight className="w-4 h-4 text-nebula-400" />
                    2.4 - Ajouter le répertoire localtexmf
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <ol className="text-sm text-muted-foreground space-y-2 list-decimal ml-4">
                    <li>Dans MikTeX Console, cliquez sur l'onglet <strong className="text-foreground">Settings</strong></li>
                    <li>Allez dans l'onglet <strong className="text-foreground">Directories</strong></li>
                    <li>Cliquez sur le bouton <strong className="text-foreground">+</strong> (Ajouter)</li>
                    <li>Collez le chemin vers votre dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code></li>
                    <li>Cliquez sur <strong className="text-foreground">OK</strong> pour confirmer</li>
                  </ol>
                </CardContent>
              </Card>

              {/* Sous-étape 2.5 */}
              <Card className="glass-card border-nebula-700/30">
                <CardHeader>
                  <CardTitle className="text-base flex items-center gap-2">
                    <RefreshCw className="w-4 h-4 text-nebula-400" />
                    2.5 - Rafraîchir la base de données
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <p className="text-sm text-muted-foreground">
                    Cette étape est cruciale pour que MikTeX prenne en compte le nouveau package.
                  </p>
                  <ol className="text-sm text-muted-foreground space-y-2 list-decimal ml-4">
                    <li>Dans MikTeX Console, allez dans l'onglet <strong className="text-foreground">Tasks</strong></li>
                    <li>Cliquez sur <strong className="text-foreground">Refresh file name database</strong></li>
                    <li>Attendez la fin de l'opération (quelques secondes)</li>
                  </ol>

                  <div className="flex items-start gap-3 bg-green-900/20 border border-green-700/30 rounded-lg p-4">
                    <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                    <div>
                      <p className="text-sm font-semibold text-green-300">
                        Configuration terminée !
                      </p>
                      <p className="text-sm text-muted-foreground mt-1">
                        Le package bfcours est maintenant accessible depuis tous vos documents LaTeX.
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Installation - Étape 3 */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-start gap-4">
          <div className="flex-shrink-0 w-12 h-12 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-xl">
            3
          </div>
          <div className="flex-1 space-y-4">
            <div>
              <h2 className="text-2xl font-bold flex items-center gap-3 mb-2">
                <Terminal className="w-7 h-7 text-cosmic-400" />
                Tester l'installation
              </h2>
              <p className="text-muted-foreground">
                Vérifiez que le package bfcours est correctement installé en compilant un document de test.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-sm font-semibold mb-2">
                  Créez un fichier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">test-bfcours.tex</code> :
                </p>
                <div className="bg-black/30 rounded-lg overflow-hidden">
                  <div className="bg-cosmic-900/30 px-4 py-2 flex items-center justify-between border-b border-cosmic-700/30">
                    <span className="text-xs font-mono text-cosmic-300">test-bfcours.tex</span>
                    <Copy className="w-4 h-4 text-muted-foreground cursor-pointer hover:text-cosmic-400" />
                  </div>
                  <pre className="p-4 overflow-x-auto">
                    <code className="text-sm">
{`\\documentclass{article}
\\usepackage{bfcours}

\\begin{document}

\\section{Test du package bfcours}

Ceci est un test du package bfcours.

\\end{document}`}
                    </code>
                  </pre>
                </div>
              </div>

              <div className="space-y-2">
                <p className="text-sm font-semibold">Compilation :</p>
                <ol className="text-sm text-muted-foreground space-y-1 list-decimal ml-4">
                  <li>Ouvrez le fichier dans VS Code</li>
                  <li>Assurez-vous que LuaLaTeX est sélectionné comme compilateur</li>
                  <li>Compilez le document (Ctrl+Alt+B ou bouton "Build LaTeX project")</li>
                </ol>
              </div>

              <div className="flex items-start gap-3 bg-green-900/20 border border-green-700/30 rounded-lg p-4">
                <CheckCircle className="w-5 h-5 text-green-400 flex-shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-green-300">
                    Installation réussie !
                  </p>
                  <p className="text-sm text-muted-foreground mt-1">
                    Si la compilation réussit sans erreur, le package bfcours est correctement installé
                    et prêt à l'emploi. Vous pouvez maintenant créer vos documents pédagogiques !
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Dépannage */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold flex items-center gap-3">
          <AlertCircle className="w-7 h-7 text-amber-400" />
          Dépannage
        </h2>
        <p className="text-muted-foreground">
          Vous rencontrez des problèmes ? Voici les solutions aux erreurs les plus courantes.
        </p>

        <div className="space-y-4">
          {/* Problème 1 */}
          <Card className="glass-card border-amber-700/30">
            <CardHeader>
              <CardTitle className="text-base text-amber-300">
                Le package n'est pas trouvé
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Erreur : <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs text-red-400">
                  ! LaTeX Error: File `bfcours.sty' not found.
                </code>
              </p>
              <div className="space-y-2">
                <p className="text-sm font-semibold">Solutions :</p>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc ml-4">
                  <li>Vérifiez que le chemin dans MikTeX Console est correct et pointe vers le dossier <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code></li>
                  <li>Assurez-vous d'avoir rafraîchi la base de données MikTeX (Tasks → Refresh file name database)</li>
                  <li>Le dossier doit s'appeler exactement <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf</code></li>
                  <li>Vérifiez que la structure est : <code className="bg-black/30 px-1.5 py-0.5 rounded text-xs">localtexmf/tex/latex/bfcours/bfcours.sty</code></li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Problème 2 */}
          <Card className="glass-card border-amber-700/30">
            <CardHeader>
              <CardTitle className="text-base text-amber-300">
                Erreurs de compilation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Le document ne compile pas malgré le package trouvé.
              </p>
              <div className="space-y-2">
                <p className="text-sm font-semibold">Solutions :</p>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc ml-4">
                  <li>Vérifiez que vous compilez avec <strong className="text-foreground">LuaLaTeX</strong> (pas pdfLaTeX)</li>
                  <li>Assurez-vous que tous les fichiers .sty sont présents dans le dossier bfcours</li>
                  <li>Vérifiez les dépendances du package (polices, autres packages LaTeX)</li>
                  <li>Consultez le fichier de log pour identifier l'erreur précise</li>
                </ul>
              </div>
            </CardContent>
          </Card>

          {/* Problème 3 */}
          <Card className="glass-card border-amber-700/30">
            <CardHeader>
              <CardTitle className="text-base text-amber-300">
                Modifications du package non prises en compte
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Vous avez modifié des fichiers .sty mais les changements n'apparaissent pas.
              </p>
              <div className="space-y-2">
                <p className="text-sm font-semibold">Solution :</p>
                <ul className="text-sm text-muted-foreground space-y-1 list-disc ml-4">
                  <li>Rafraîchissez la base de données MikTeX après chaque modification</li>
                  <li>Dans MikTeX Console : Tasks → Refresh file name database</li>
                  <li>Recompilez complètement le document (supprimez les fichiers .aux, .log temporaires)</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        <p className="text-muted-foreground">
          Maintenant que bfcours est installé, vous pouvez commencer à créer des documents pédagogiques professionnels !
        </p>

        <div className="grid md:grid-cols-2 gap-4">
          <Card className="glass-card border-cosmic-700/30 hover:scale-105 transition-all duration-300">
            <CardHeader>
              <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center mb-2">
                <FileCode className="w-5 h-5 text-white" />
              </div>
              <CardTitle className="text-lg">Créer des cours structurés</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Utilisez les environnements dédiés de bfcours pour créer des cours
                avec sections, définitions, théorèmes et exemples.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-nebula-700/30 hover:scale-105 transition-all duration-300">
            <CardHeader>
              <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center mb-2">
                <FileCode className="w-5 h-5 text-white" />
              </div>
              <CardTitle className="text-lg">Générer des exercices</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Créez des fiches d'exercices avec corrections automatiques et
                numérotation gérée par le package.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-cosmic-700/30 hover:scale-105 transition-all duration-300">
            <CardHeader>
              <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center mb-2">
                <Terminal className="w-5 h-5 text-white" />
              </div>
              <CardTitle className="text-lg">Utiliser Claude Code</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Automatisez la création de documents avec Claude Code et les
                agents spécialisés pour LaTeX.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-nebula-700/30 hover:scale-105 transition-all duration-300">
            <CardHeader>
              <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center mb-2">
                <Settings className="w-5 h-5 text-white" />
              </div>
              <CardTitle className="text-lg">Personnaliser le package</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Modifiez les fichiers .sty pour adapter bfcours à vos besoins
                spécifiques d'enseignement.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 pt-4">
          <Button asChild variant="cosmic" size="lg" className="flex-1">
            <Link href="/claude-code/tutorials" prefetch={false}>
              Voir les autres tutoriels
            </Link>
          </Button>
          <Button asChild variant="nebula" size="lg" className="flex-1">
            <Link href="/claude-code/downloads" prefetch={false}>
              Télécharger les ressources
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
