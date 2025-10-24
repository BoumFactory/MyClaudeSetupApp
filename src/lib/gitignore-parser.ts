import fs from 'fs/promises'
import path from 'path'

/**
 * Parser pour fichiers .gitignore
 */
export class GitignoreParser {
  private patterns: string[] = []
  private negativePatterns: string[] = []

  /**
   * Charger et parser un fichier .gitignore
   * @param gitignorePath - Chemin vers le fichier .gitignore
   */
  async load(gitignorePath: string): Promise<void> {
    try {
      const content = await fs.readFile(gitignorePath, 'utf-8')
      this.parse(content)
    } catch (error) {
      // Fichier .gitignore non trouvé, ignorer
      console.warn(`Fichier .gitignore non trouvé : ${gitignorePath}`)
    }
  }

  /**
   * Parser le contenu d'un .gitignore
   * @param content - Contenu du fichier
   */
  private parse(content: string): void {
    const lines = content.split('\n')

    for (const line of lines) {
      const trimmed = line.trim()

      // Ignorer les lignes vides et les commentaires
      if (!trimmed || trimmed.startsWith('#')) {
        continue
      }

      // Pattern de négation (commence par !)
      if (trimmed.startsWith('!')) {
        this.negativePatterns.push(trimmed.slice(1))
      } else {
        this.patterns.push(trimmed)
      }
    }
  }

  /**
   * Vérifier si un chemin doit être ignoré
   * @param filePath - Chemin du fichier à vérifier
   * @param basePath - Chemin de base pour la comparaison
   * @returns true si le fichier doit être ignoré
   */
  shouldIgnore(filePath: string, basePath: string = ''): boolean {
    const relativePath = basePath
      ? path.relative(basePath, filePath).replace(/\\/g, '/')
      : filePath.replace(/\\/g, '/')

    // Vérifier d'abord les patterns de négation
    for (const negPattern of this.negativePatterns) {
      if (this.matchPattern(relativePath, negPattern)) {
        return false
      }
    }

    // Vérifier les patterns normaux
    for (const pattern of this.patterns) {
      if (this.matchPattern(relativePath, pattern)) {
        return true
      }
    }

    return false
  }

  /**
   * Vérifier si un chemin correspond à un pattern
   * @param filePath - Chemin du fichier
   * @param pattern - Pattern gitignore
   * @returns true si le pattern correspond
   */
  private matchPattern(filePath: string, pattern: string): boolean {
    // Pattern de dossier (se termine par /)
    if (pattern.endsWith('/')) {
      const dirPattern = pattern.slice(0, -1)

      // Si le pattern commence par /, match uniquement à la racine
      if (dirPattern.startsWith('/')) {
        const rootPattern = dirPattern.slice(1)
        return filePath === rootPattern || filePath.startsWith(rootPattern + '/')
      }

      // Sinon, match n'importe où dans le chemin
      const pathSegments = filePath.split('/')
      return pathSegments.some((segment, index) => {
        if (segment === dirPattern) {
          return true
        }
        // Match aussi les sous-dossiers
        const subPath = pathSegments.slice(index).join('/')
        return subPath.startsWith(dirPattern + '/')
      })
    }

    // Pattern avec wildcard
    if (pattern.includes('*')) {
      const regexPattern = pattern
        .replace(/\./g, '\\.')
        .replace(/\*\*/g, '§DOUBLESTAR§')  // Protéger les ** temporairement
        .replace(/\*/g, '[^/]*')  // * match tout sauf /
        .replace(/§DOUBLESTAR§/g, '.*')  // ** match tout y compris /
        .replace(/\?/g, '[^/]')

      // Si le pattern ne commence pas par /, il peut matcher n'importe où
      if (!pattern.startsWith('/')) {
        const regex = new RegExp(`(^|/)${regexPattern}(/|$)`)
        return regex.test(filePath)
      } else {
        const regex = new RegExp(`^${regexPattern.slice(1)}(/|$)`)
        return regex.test(filePath)
      }
    }

    // Pattern exact
    // Si le pattern commence par /, match uniquement à la racine
    if (pattern.startsWith('/')) {
      const rootPattern = pattern.slice(1)
      return filePath === rootPattern || filePath.startsWith(rootPattern + '/')
    }

    // Sinon, match n'importe où dans le chemin (nom de fichier ou dossier)
    const pathSegments = filePath.split('/')
    return pathSegments.some(segment => segment === pattern) ||
           filePath === pattern ||
           filePath.endsWith('/' + pattern)
  }

  /**
   * Obtenir tous les patterns chargés
   * @returns Liste des patterns
   */
  getPatterns(): string[] {
    return [...this.patterns]
  }
}

/**
 * Créer et charger un parser .gitignore
 * @param gitignorePath - Chemin vers le .gitignore
 * @returns Parser initialisé
 */
export async function createGitignoreParser(
  gitignorePath: string
): Promise<GitignoreParser> {
  const parser = new GitignoreParser()
  await parser.load(gitignorePath)
  return parser
}
