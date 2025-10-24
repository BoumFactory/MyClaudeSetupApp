import JSZip from 'jszip'
import fs from 'fs/promises'
import path from 'path'
import { DownloadableItem } from '@/types'

/**
 * Générateur de fichiers ZIP (côté serveur uniquement)
 * Ces fonctions utilisent fs/promises et ne peuvent pas être importées côté client
 */

/**
 * Générer un fichier ZIP à partir d'un arbre de fichiers
 * @param items - Arbre de fichiers à zipper
 * @param basePath - Chemin de base des fichiers
 * @param onlySelected - Inclure seulement les fichiers sélectionnés
 * @returns Buffer du fichier ZIP
 */
export async function generateZip(
  items: DownloadableItem[],
  basePath: string,
  onlySelected: boolean = true
): Promise<Buffer> {
  const zip = new JSZip()

  console.log('[ZIP] Génération du ZIP avec basePath:', basePath)
  console.log('[ZIP] Nombre d\'items racine:', items.length)
  console.log('[ZIP] Mode onlySelected:', onlySelected)

  // Compter les fichiers sélectionnés
  const countSelected = (items: DownloadableItem[]): number => {
    let count = 0
    for (const item of items) {
      if (item.isSelected && !item.isIgnored) count++
      if (item.children) count += countSelected(item.children)
    }
    return count
  }
  console.log('[ZIP] Fichiers sélectionnés:', countSelected(items))

  await addItemsToZip(zip, items, basePath, '', onlySelected)

  return await zip.generateAsync({
    type: 'nodebuffer',
    compression: 'DEFLATE',
    compressionOptions: {
      level: 9,
    },
  })
}

/**
 * Ajouter récursivement des items à un ZIP
 * @param zip - Instance JSZip
 * @param items - Items à ajouter
 * @param basePath - Chemin de base
 * @param currentPath - Chemin courant dans le ZIP
 * @param onlySelected - Inclure seulement les sélectionnés
 */
async function addItemsToZip(
  zip: JSZip,
  items: DownloadableItem[],
  basePath: string,
  currentPath: string,
  onlySelected: boolean
): Promise<void> {
  for (const item of items) {
    // Ignorer les fichiers marqués comme ignorés
    if (item.isIgnored) {
      console.log(`[ZIP] Ignoré (isIgnored): ${item.path}`)
      continue
    }

    const zipPath = currentPath ? `${currentPath}/${item.name}` : item.name
    const fullPath = path.join(basePath, item.path)

    if (item.type === 'directory') {
      // Pour un dossier, on explore toujours ses enfants
      // même s'il n'est pas sélectionné (il peut contenir des fichiers sélectionnés)
      if (item.children && item.children.length > 0) {
        // Créer le dossier seulement s'il contient des fichiers sélectionnés
        const hasSelectedChildren = onlySelected
          ? hasAnySelectedDescendant(item.children)
          : true

        if (hasSelectedChildren) {
          console.log(`[ZIP] Création dossier: ${zipPath}`)
          zip.folder(zipPath)

          await addItemsToZip(
            zip,
            item.children,
            basePath,
            zipPath,
            onlySelected
          )
        } else {
          console.log(`[ZIP] Ignoré (aucun enfant sélectionné): ${item.path}`)
        }
      }
    } else {
      // Pour un fichier, vérifier la sélection
      if (onlySelected && !item.isSelected) {
        console.log(`[ZIP] Ignoré (non sélectionné): ${item.path}`)
        continue
      }

      // Ajouter le fichier au ZIP
      try {
        console.log(`[ZIP] Ajout fichier: ${zipPath} (${fullPath})`)
        const fileContent = await fs.readFile(fullPath)
        zip.file(zipPath, fileContent)
        console.log(`[ZIP] ✓ Fichier ajouté avec succès: ${zipPath}`)
      } catch (error) {
        console.error(`[ZIP] ✗ Erreur lors de l'ajout du fichier ${fullPath} :`, error)
      }
    }
  }
}

/**
 * Vérifier si un item ou ses descendants sont sélectionnés
 */
function hasAnySelectedDescendant(items: DownloadableItem[]): boolean {
  for (const item of items) {
    if (item.isIgnored) continue

    if (item.isSelected && item.type === 'file') {
      return true
    }

    if (item.children && hasAnySelectedDescendant(item.children)) {
      return true
    }
  }

  return false
}
