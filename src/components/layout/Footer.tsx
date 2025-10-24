import Link from "next/link"
import { Code2, Github, Mail, FolderOpen, Package, Settings, Wrench } from "lucide-react"

/**
 * Footer de l'application
 */
export function Footer() {
  const currentYear = new Date().getFullYear()

  const githubRepos = [
    {
      title: "Claude Code Setup",
      url: "https://github.com/BoumFactory/BFTOOLS_code_setup.git",
      icon: Settings,
      description: "Configuration Claude Code pour VSCode"
    },
    {
      title: "Logiciels & Applications",
      url: "https://github.com/Romain1099/BFtools.git",
      icon: Wrench,
      description: "Outils pour préparations et classe"
    },
    {
      title: "Packages LaTeX",
      url: "https://github.com/Romain1099/BFCours.git",
      icon: Package,
      description: "Packages LaTeX personnalisés"
    },
  ]

  return (
    <footer className="border-t border-cosmic-800/50 mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-4 gap-8">
          {/* À propos */}
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg cosmic-gradient flex items-center justify-center">
                <Code2 className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg">IA & Enseignement</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Plateforme de partage de connaissances sur l'intelligence
              artificielle au service des enseignants de mathématiques.
            </p>
          </div>

          {/* Liens rapides */}
          <div className="space-y-3">
            <h3 className="font-semibold">Liens Rapides</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link
                  href="/about"
                  className="text-muted-foreground hover:text-cosmic-400 transition-colors"
                >
                  Qui suis-je ?
                </Link>
              </li>
              <li>
                <Link
                  href="/claude-code"
                  className="text-muted-foreground hover:text-cosmic-400 transition-colors"
                >
                  Claude Code
                </Link>
              </li>
              <li>
                <Link
                  href="/claude-code/tutorials"
                  className="text-muted-foreground hover:text-cosmic-400 transition-colors"
                >
                  Tutoriels
                </Link>
              </li>
              <li>
                <Link
                  href="/claude-code/presentations"
                  className="text-muted-foreground hover:text-cosmic-400 transition-colors"
                >
                  Présentations
                </Link>
              </li>
              <li>
                <Link
                  href="/claude-code/downloads"
                  className="text-muted-foreground hover:text-cosmic-400 transition-colors"
                >
                  Téléchargements
                </Link>
              </li>
            </ul>
          </div>

          {/* Dépôts GitHub */}
          <div className="space-y-3">
            <h3 className="font-semibold">Ressources GitHub</h3>
            <ul className="space-y-2">
              {githubRepos.map((repo) => {
                const Icon = repo.icon
                return (
                  <li key={repo.url}>
                    <a
                      href={repo.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group inline-flex items-start gap-2 text-sm text-muted-foreground hover:text-cosmic-400 transition-colors"
                      title={repo.description}
                    >
                      <Icon className="w-4 h-4 mt-0.5 flex-shrink-0" />
                      <span className="group-hover:underline">{repo.title}</span>
                    </a>
                  </li>
                )
              })}
              <li>
                <a
                  href="https://drive.google.com/drive/folders/1PjL52VJvCB9W3XmCDSZ3oMgidRZHw6Ql?usp=sharing"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group inline-flex items-start gap-2 text-sm text-muted-foreground hover:text-cosmic-400 transition-colors"
                  title="Formation LaTeX complète"
                >
                  <FolderOpen className="w-4 h-4 mt-0.5 flex-shrink-0" />
                  <span className="group-hover:underline">Formation LaTeX</span>
                </a>
              </li>
            </ul>
          </div>

          {/* Contact */}
          <div className="space-y-3">
            <h3 className="font-semibold">Contact</h3>
            <div className="flex flex-col gap-2">
              <a
                href="mailto:contact.bfcours.ai@gmail.com"
                className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-cosmic-400 transition-colors"
              >
                <Mail className="w-4 h-4" />
                contact.bfcours.ai@gmail.com
              </a>
              <a
                href="https://github.com/Romain1099"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-cosmic-400 transition-colors"
              >
                <Github className="w-4 h-4" />
                Profil GitHub
              </a>
            </div>
          </div>
        </div>

        <div className="border-t border-cosmic-800/50 mt-8 pt-6 text-center text-sm text-muted-foreground">
          <p>
            © {currentYear} IA & Enseignement des Mathématiques. Tous droits
            réservés.
          </p>
        </div>
      </div>
    </footer>
  )
}
