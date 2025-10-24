import { DownloadableItem } from '@/types'

/**
 * Utilitaires ZIP (côté client uniquement)
 * La fonction generateZip qui utilise fs est dans l'API route /api/download
 */

/**
 * Sélectionner/désélectionner récursivement tous les items
 * @param items - Items à modifier
 * @param selected - État de sélection
 * @returns Items modifiés
 */
export function toggleAllSelection(
  items: DownloadableItem[],
  selected: boolean
): DownloadableItem[] {
  return items.map((item) => {
    const updated = { ...item, isSelected: selected }

    if (updated.children) {
      updated.children = toggleAllSelection(updated.children, selected)
    }

    return updated
  })
}

/**
 * Basculer la sélection d'un item spécifique
 * @param items - Liste d'items
 * @param itemPath - Chemin de l'item à basculer
 * @returns Items mis à jour
 */
export function toggleItemSelection(
  items: DownloadableItem[],
  itemPath: string
): DownloadableItem[] {
  return items.map((item) => {
    if (item.path === itemPath) {
      const isSelected = !item.isSelected

      // Si c'est un dossier, appliquer récursivement
      if (item.type === 'directory' && item.children) {
        return {
          ...item,
          isSelected,
          children: toggleAllSelection(item.children, isSelected),
        }
      }

      return { ...item, isSelected }
    }

    // Chercher dans les enfants
    if (item.children) {
      return {
        ...item,
        children: toggleItemSelection(item.children, itemPath),
      }
    }

    return item
  })
}

/**
 * Compter le nombre de fichiers sélectionnés
 * @param items - Arbre de fichiers
 * @returns Nombre de fichiers sélectionnés
 */
export function countSelectedFiles(items: DownloadableItem[]): number {
  let count = 0

  for (const item of items) {
    if (item.isSelected && item.type === 'file') {
      count++
    }

    if (item.children) {
      count += countSelectedFiles(item.children)
    }
  }

  return count
}
