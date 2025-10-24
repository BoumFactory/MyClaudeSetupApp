import { DownloadableItem } from '@/types'

/**
 * Utilitaires pour le scanner de fichiers (côté client uniquement)
 * Les fonctions qui utilisent fs sont dans file-scanner-server.ts
 */

/**
 * Obtenir la taille totale d'un arbre de fichiers
 * @param items - Arbre de fichiers
 * @param onlySelected - Compter seulement les fichiers sélectionnés
 * @returns Taille totale en octets
 */
export function getTotalSize(
  items: DownloadableItem[],
  onlySelected: boolean = false
): number {
  let total = 0

  for (const item of items) {
    if (item.type === 'file') {
      // Pour un fichier, vérifier la sélection
      if (onlySelected && !item.isSelected) {
        continue
      }
      total += item.size || 0
    } else if (item.children) {
      // Pour un dossier, toujours explorer les enfants
      // même s'il n'est pas sélectionné (il peut contenir des fichiers sélectionnés)
      total += getTotalSize(item.children, onlySelected)
    }
  }

  return total
}

/**
 * Formater une taille en octets en format lisible
 * @param bytes - Taille en octets
 * @returns Taille formatée
 */
export function formatSize(bytes: number): string {
  const units = ['o', 'Ko', 'Mo', 'Go']
  let size = bytes
  let unitIndex = 0

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }

  return `${size.toFixed(2)} ${units[unitIndex]}`
}

