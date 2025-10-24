/**
 * Types de l'application
 */

/**
 * Représente une présentation reveal.js
 */
export interface Presentation {
  id: string
  title: string
  slug: string
  filename: string
  description?: string
  category: string
  path: string
  createdAt?: Date
  updatedAt?: Date
}

/**
 * Représente une vidéo YouTube
 */
export interface YouTubeVideo {
  id: string
  title: string
  url: string
  videoId: string
  thumbnail?: string
  description?: string
  category: string
}

/**
 * Représente un fichier ou dossier téléchargeable
 */
export interface DownloadableItem {
  name: string
  path: string
  type: 'file' | 'directory'
  size?: number
  children?: DownloadableItem[]
  isSelected?: boolean
  isIgnored?: boolean
}

/**
 * Représente un scope (section thématique)
 */
export interface Scope {
  id: string
  title: string
  slug: string
  description: string
  icon: string
  color: string
  gradient: string
  path: string
}

/**
 * Représente une ressource générique
 */
export interface Resource {
  id: string
  title: string
  type: 'presentation' | 'video' | 'download' | 'article'
  category: string
  scope: string
  path?: string
  url?: string
  description?: string
  thumbnail?: string
  tags?: string[]
  createdAt?: Date
}

/**
 * Configuration d'un scope
 */
export interface ScopeConfig {
  scope: Scope
  presentations: Presentation[]
  videos: YouTubeVideo[]
  downloadables: DownloadableItem[]
}
