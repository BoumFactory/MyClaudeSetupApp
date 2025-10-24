import fs from 'fs/promises'
import path from 'path'
import { Presentation, DownloadableItem } from '@/types'
import { slugify } from './utils'
import { GitignoreParser } from './gitignore-parser'

/**
 * Scanner de fichiers pour les ressources publiques (côté serveur uniquement)
 * Ces fonctions utilisent fs/promises et ne peuvent pas être importées côté client
 */

/**
 * Type pour une entrée de présentation dans une sous-catégorie
 */
export interface PresentationEntry {
  slug: string
  comment: string
}

/**
 * Type pour une sous-catégorie de présentations
 */
export interface PresentationSubcategory {
  id: string
  name: string
  description: string
  presentations: PresentationEntry[]
}

/**
 * Type pour une catégorie de présentations
 */
export interface PresentationCategory {
  id: string
  name: string
  description: string
  icon: string
  gradient: string
  color: string
  subcategories: PresentationSubcategory[]
}

/**
 * Type pour la configuration des catégories
 */
export interface CategoriesConfig {
  categories: PresentationCategory[]
  settings: {
    defaultIcon: string
    defaultGradient: string
    defaultColor: string
  }
}

/**
 * Scanner les présentations reveal.js dans un dossier
 * @param baseDir - Dossier de base à scanner
 * @param category - Catégorie des présentations
 * @returns Liste des présentations trouvées
 */
export async function scanPresentations(
  baseDir: string,
  category: string = 'general'
): Promise<Presentation[]> {
  const presentations: Presentation[] = []

  try {
    const files = await fs.readdir(baseDir)

    for (const file of files) {
      if (file.endsWith('.html')) {
        const filePath = path.join(baseDir, file)
        const stats = await fs.stat(filePath)

        // Extraire le titre du nom de fichier
        const title = file
          .replace('.html', '')
          .replace(/-/g, ' ')
          .replace(/\b\w/g, (l) => l.toUpperCase())

        presentations.push({
          id: slugify(file),
          title,
          slug: slugify(title),
          filename: file,
          category,
          path: filePath,
          createdAt: stats.birthtime,
          updatedAt: stats.mtime,
        })
      }
    }
  } catch (error) {
    console.error(`Erreur lors du scan des présentations : ${error}`)
  }

  return presentations.sort((a, b) => a.title.localeCompare(b.title))
}

/**
 * Scanner récursivement un dossier et construire un arbre de fichiers (version optimisée)
 * @param dirPath - Chemin du dossier à scanner
 * @param basePath - Chemin de base pour les chemins relatifs
 * @param gitignoreParser - Parser .gitignore (optionnel)
 * @param maxDepth - Profondeur maximale de scan (optionnel, par défaut illimitée)
 * @param currentDepth - Profondeur actuelle (pour usage interne)
 * @returns Arbre de fichiers
 */
export async function scanDirectory(
  dirPath: string,
  basePath: string = dirPath,
  gitignoreParser?: GitignoreParser,
  maxDepth: number = Infinity,
  currentDepth: number = 0
): Promise<DownloadableItem[]> {
  const items: DownloadableItem[] = []

  try {
    // Si on atteint la profondeur max, ne pas scanner plus loin
    if (currentDepth >= maxDepth) {
      return items
    }

    const entries = await fs.readdir(dirPath, { withFileTypes: true })

    // Traiter tous les fichiers/dossiers en parallèle avec Promise.all
    const processedItems = await Promise.all(
      entries.map(async (entry) => {
        const fullPath = path.join(dirPath, entry.name)
        const relativePath = path.relative(basePath, fullPath)

        // Vérifier si le fichier doit être ignoré AVANT de traiter
        const isIgnored = gitignoreParser
          ? gitignoreParser.shouldIgnore(fullPath, basePath)
          : false

        // Court-circuiter les dossiers ignorés pour éviter de descendre dedans
        if (isIgnored && entry.isDirectory()) {
          return {
            name: entry.name,
            path: relativePath,
            type: 'directory' as const,
            children: [],
            isSelected: false,
            isIgnored: true,
          }
        }

        if (entry.isDirectory()) {
          // Scanner récursivement les sous-dossiers (sauf si ignoré)
          const children = isIgnored ? [] : await scanDirectory(
            fullPath,
            basePath,
            gitignoreParser,
            maxDepth,
            currentDepth + 1
          )

          return {
            name: entry.name,
            path: relativePath,
            type: 'directory' as const,
            children,
            isSelected: false,
            isIgnored,
          }
        } else {
          // Fichier - utiliser stat seulement si nécessaire
          const stats = isIgnored ? null : await fs.stat(fullPath)

          return {
            name: entry.name,
            path: relativePath,
            type: 'file' as const,
            size: stats?.size || 0,
            isSelected: false,
            isIgnored,
          }
        }
      })
    )

    items.push(...processedItems)
  } catch (error) {
    console.error(`Erreur lors du scan du dossier ${dirPath} : ${error}`)
  }

  return items.sort((a, b) => {
    // Dossiers d'abord, puis fichiers
    if (a.type !== b.type) {
      return a.type === 'directory' ? -1 : 1
    }
    return a.name.localeCompare(b.name)
  })
}

/**
 * Lire le contenu d'un fichier HTML de présentation
 * @param filePath - Chemin du fichier
 * @returns Contenu HTML
 */
export async function readPresentationContent(
  filePath: string
): Promise<string> {
  try {
    return await fs.readFile(filePath, 'utf-8')
  } catch (error) {
    console.error(`Erreur lors de la lecture du fichier ${filePath} : ${error}`)
    throw new Error(`Impossible de lire le fichier de présentation`)
  }
}

/**
 * Lire la configuration des catégories depuis le fichier JSON
 * @param categoriesPath - Chemin du fichier categories.json
 * @returns Configuration des catégories
 */
export async function readCategoriesConfig(
  categoriesPath: string
): Promise<CategoriesConfig> {
  try {
    const content = await fs.readFile(categoriesPath, 'utf-8')
    return JSON.parse(content) as CategoriesConfig
  } catch (error) {
    console.error(`Erreur lors de la lecture des catégories : ${error}`)
    // Retourner une configuration par défaut en cas d'erreur
    return {
      categories: [],
      settings: {
        defaultIcon: 'BookOpen',
        defaultGradient: 'cosmic-gradient',
        defaultColor: 'cosmic',
      },
    }
  }
}

/**
 * Organiser les présentations par catégories et sous-catégories
 * @param presentations - Liste des présentations
 * @param config - Configuration des catégories
 * @returns Map des présentations organisées par catégorie et sous-catégorie avec leurs commentaires
 */
export function organizePresentationsByCategory(
  presentations: Presentation[],
  config: CategoriesConfig
): Map<PresentationCategory, Map<PresentationSubcategory, Array<Presentation & { comment: string }>>> {
  const organized = new Map<PresentationCategory, Map<PresentationSubcategory, Array<Presentation & { comment: string }>>>()

  // Créer une map slug -> présentation pour un accès rapide
  const presentationMap = new Map<string, Presentation>()
  presentations.forEach((p) => {
    presentationMap.set(p.slug, p)
  })

  // Organiser par catégorie et sous-catégorie
  config.categories.forEach((category) => {
    const subcategoriesMap = new Map<PresentationSubcategory, Array<Presentation & { comment: string }>>()

    category.subcategories.forEach((subcategory) => {
      const subcategoryPresentations: Array<Presentation & { comment: string }> = []

      subcategory.presentations.forEach((entry) => {
        const presentation = presentationMap.get(entry.slug)
        if (presentation) {
          subcategoryPresentations.push({
            ...presentation,
            comment: entry.comment
          })
        }
      })

      if (subcategoryPresentations.length > 0) {
        subcategoriesMap.set(subcategory, subcategoryPresentations)
      }
    })

    if (subcategoriesMap.size > 0) {
      organized.set(category, subcategoriesMap)
    }
  })

  return organized
}
