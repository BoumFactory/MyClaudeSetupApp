import { Download, FolderTree } from "lucide-react"
import path from "path"
import { scanDirectory } from "@/lib/file-scanner-server"
import { createGitignoreParser } from "@/lib/gitignore-parser"
import { FileExplorer } from "@/components/downloads/FileExplorer"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { ChangelogSection } from "@/components/changelog/ChangelogSection"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Téléchargements Claude Code",
  description:
    "Téléchargez les configurations Claude, agents, skills et applications prêtes à l'emploi",
}

// Revalider le cache toutes les 24 heures (86400 secondes)
export const revalidate = 86400

/**
 * Page de téléchargement avec explorateur de fichiers
 */
export default async function DownloadsPage() {
  // Scanner le dossier public/download avec toutes les catégories
  const projectRoot = process.cwd()
  const downloadPath = path.join(
    projectRoot,
    'public',
    'download'
  )

  // Charger le parser .gitignore depuis la racine du projet
  const gitignorePath = path.join(projectRoot, '.gitignore')
  const gitignoreParser = await createGitignoreParser(gitignorePath)

  // Scanner les fichiers en respectant le .gitignore
  // projectRoot est passé pour que les patterns commençant par / soient correctement interprétés
  const files = await scanDirectory(downloadPath, downloadPath, gitignoreParser, Infinity, 0, projectRoot)

  return (
    <div className="space-y-8">
      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Téléchargements", href: "/claude-code/downloads" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Download className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Téléchargements
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Accédez aux configurations Claude, agents, skills et applications.
          Sélectionnez les fichiers que vous souhaitez télécharger.
        </p>
      </section>

      {/* Dernières modifications - Changelog */}
      <ChangelogSection category="downloads" limit={1} compact={false} />

      {/* Catégories disponibles */}
      <div className="glass-card rounded-xl p-6 space-y-4">
        <div className="flex items-start gap-3">
          <FolderTree className="w-5 h-5 text-cosmic-400 mt-0.5" />
          <div className="space-y-3 flex-1">
            <h3 className="font-semibold">Catégories de téléchargement</h3>
            <div className="grid md:grid-cols-2 gap-3">
              <div className="bg-cosmic-900/20 rounded-lg p-3 border border-cosmic-700/30">
                <h4 className="font-medium text-cosmic-400 mb-1">Claude-Code-Setup</h4>
                <p className="text-xs text-muted-foreground">
                  Configuration complète de Claude Code : agents, skills, commandes et serveurs MCP
                </p>
              </div>
              <div className="bg-nebula-900/20 rounded-lg p-3 border border-nebula-700/30">
                <h4 className="font-medium text-nebula-400 mb-1">latex-packages</h4>
                <p className="text-xs text-muted-foreground">
                  Packages LaTeX personnalisés pour l'enseignement des mathématiques
                </p>
              </div>
              <div className="bg-cosmic-900/20 rounded-lg p-3 border border-cosmic-700/30">
                <h4 className="font-medium text-cosmic-400 mb-1">logiciels-enseignant</h4>
                <p className="text-xs text-muted-foreground">
                  Logiciels et outils utiles pour l'enseignement
                </p>
              </div>
              <div className="bg-nebula-900/20 rounded-lg p-3 border border-nebula-700/30">
                <h4 className="font-medium text-nebula-400 mb-1">Applications éducatives</h4>
                <p className="text-xs text-muted-foreground">
                  Applications interactives créées avec Claude Code
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Info */}
      <div className="glass-card rounded-xl p-6 space-y-3">
        <h3 className="font-semibold">Comment utiliser ?</h3>
        <ol className="text-sm text-muted-foreground space-y-2 list-decimal list-inside">
          <li>
            Parcourez l'arborescence des fichiers ci-dessous et explorez les différentes catégories
          </li>
          <li>
            Sélectionnez les fichiers et dossiers que vous souhaitez télécharger
          </li>
          <li>
            Cliquez sur "Télécharger la sélection" pour générer un fichier ZIP
          </li>
          <li>
            Extrayez le ZIP dans votre répertoire de projet approprié
          </li>
          <li>
            Consultez les présentations pour comprendre l'utilisation de chaque composant
          </li>
        </ol>
      </div>

      {/* Explorateur de fichiers */}
      <FileExplorer files={files} basePath={downloadPath} />

      {/* Avertissement */}
      <div className="glass-card rounded-xl p-6 border-l-4 border-cosmic-500">
        <h3 className="font-semibold mb-2 text-cosmic-400">
          Note importante
        </h3>
        <p className="text-sm text-muted-foreground">
          Les fichiers téléchargés sont des exemples et des configurations de
          base. Assurez-vous de les adapter à vos besoins spécifiques et de
          comprendre leur fonctionnement avant de les utiliser en production.
          Les fichiers listés dans le .gitignore sont automatiquement exclus du
          téléchargement.
        </p>
      </div>
    </div>
  )
}
