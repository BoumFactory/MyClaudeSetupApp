import type JSZip from 'jszip'
import fs from 'fs/promises'
import path from 'path'

/**
 * Ajout d'un diaporama reveal.js (public/render/Reveals/<filename>) à une archive,
 * avec les assets locaux (assets/...) qu'il référence.
 * Partagé par /api/download-presentation (bouton « ZIP direct » du viewer) et par
 * package-zip.ts (le diaporama d'un skill voyage avec son pack).
 */

const REVEALS_PATH = path.join(process.cwd(), 'public', 'render', 'Reveals')

/** Nom de fichier accepté : un .html du dossier Reveals, sans remontée de dossier */
export function isValidPresentationFilename(filename: string): boolean {
  return filename.endsWith('.html') && !filename.includes('..') && !/[\\/]/.test(filename)
}

/**
 * Copie le HTML et ses assets dans `zip`, sous `prefix` (ex. '.claude/diaporama').
 * Retourne false si le diaporama n'existe pas.
 */
export async function addPresentationToZip(zip: JSZip, filename: string, prefix = ''): Promise<boolean> {
  if (!isValidPresentationFilename(filename)) return false
  const htmlPath = path.join(REVEALS_PATH, filename)
  let htmlContent: string
  try {
    htmlContent = await fs.readFile(htmlPath, 'utf-8')
  } catch {
    return false
  }

  const at = (rel: string) => (prefix ? `${prefix}/${rel}` : rel)
  zip.file(at(filename), htmlContent)

  const assetRegex = /(?:src|href)=["']assets\/([^"']+)["']/g
  const assets = new Set<string>()
  let match
  while ((match = assetRegex.exec(htmlContent)) !== null) {
    assets.add(match[1])
  }

  for (const assetPath of assets) {
    try {
      const content = await fs.readFile(path.join(REVEALS_PATH, 'assets', assetPath))
      zip.file(at(`assets/${assetPath}`), content)
    } catch (error) {
      console.warn(`[Download] Asset non trouvé: ${assetPath}`, error)
    }
  }
  return true
}
