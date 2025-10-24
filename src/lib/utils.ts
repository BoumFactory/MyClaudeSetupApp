import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

/**
 * Utilitaire pour fusionner les classes Tailwind CSS
 * @param inputs - Classes CSS à fusionner
 * @returns Classes fusionnées
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

/**
 * Formater une date en français
 * @param date - Date à formater
 * @returns Date formatée
 */
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(date)
}

/**
 * Obtenir l'ID d'une vidéo YouTube depuis une URL
 * @param url - URL de la vidéo YouTube
 * @returns ID de la vidéo ou null
 */
export function getYouTubeVideoId(url: string): string | null {
  const regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/
  const match = url.match(regExp)
  return match && match[7].length === 11 ? match[7] : null
}

/**
 * Générer un slug à partir d'un titre
 * @param title - Titre à transformer
 * @returns Slug
 */
export function slugify(title: string): string {
  return title
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
}
