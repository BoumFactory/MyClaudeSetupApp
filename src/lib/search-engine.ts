import { SearchableItem, SearchCategory } from '@/data/search-index'

export interface SearchResult {
  item: SearchableItem
  score: number
  matchLevel: 'title' | 'tag' | 'description' | 'content'
  /** Highlighted snippet (for expanded view) */
  snippet?: string
}

export interface SearchOptions {
  /** Max results per category */
  maxPerCategory?: number
  /** Categories to search (all if empty) */
  categories?: SearchCategory[]
}

/**
 * Search the index with multi-level scoring.
 * Level 1: Title match (score 100)
 * Level 2: Tag match (score 70)
 * Level 3: Description match (score 40)
 * Level 4: Content match (score 20)
 */
export function search(
  query: string,
  index: SearchableItem[],
  options: SearchOptions = {}
): SearchResult[] {
  if (!query.trim()) return []

  const terms = query.toLowerCase().split(/\s+/).filter(Boolean)
  const { maxPerCategory = 10, categories } = options

  let filtered = index
  if (categories && categories.length > 0) {
    filtered = index.filter(item => categories.includes(item.category))
  }

  const results: SearchResult[] = []

  for (const item of filtered) {
    let bestScore = 0
    let matchLevel: SearchResult['matchLevel'] = 'content'
    let snippet: string | undefined

    const titleLower = item.title.toLowerCase()
    const descLower = item.description.toLowerCase()
    const tagsLower = item.tags.map(t => t.toLowerCase())
    const contentLower = item.content?.toLowerCase() || ''

    for (const term of terms) {
      // Title match (highest priority)
      if (titleLower.includes(term)) {
        const titleScore = titleLower === term ? 120 : titleLower.startsWith(term) ? 110 : 100
        if (titleScore > bestScore) {
          bestScore = titleScore
          matchLevel = 'title'
        }
      }

      // Tag match
      if (tagsLower.some(t => t.includes(term))) {
        const tagScore = tagsLower.some(t => t === term) ? 80 : 70
        if (tagScore > bestScore) {
          bestScore = tagScore
          matchLevel = 'tag'
        }
      }

      // Description match
      if (descLower.includes(term)) {
        const descScore = 40
        if (descScore > bestScore) {
          bestScore = descScore
          matchLevel = 'description'
          // Extract snippet around match
          const idx = descLower.indexOf(term)
          const start = Math.max(0, idx - 40)
          const end = Math.min(item.description.length, idx + term.length + 60)
          snippet =
            (start > 0 ? '...' : '') +
            item.description.slice(start, end) +
            (end < item.description.length ? '...' : '')
        }
      }

      // Content match (deep search)
      if (contentLower && contentLower.includes(term)) {
        const contentScore = 20
        if (contentScore > bestScore) {
          bestScore = contentScore
          matchLevel = 'content'
          const idx = contentLower.indexOf(term)
          const start = Math.max(0, idx - 50)
          const end = Math.min((item.content || '').length, idx + term.length + 80)
          snippet =
            (start > 0 ? '...' : '') +
            (item.content || '').slice(start, end) +
            (end < (item.content || '').length ? '...' : '')
        }
      }
    }

    // Multi-term bonus: increase score if multiple terms match
    if (terms.length > 1) {
      const matchedTerms = terms.filter(
        term =>
          titleLower.includes(term) ||
          tagsLower.some(t => t.includes(term)) ||
          descLower.includes(term) ||
          contentLower.includes(term)
      )
      if (matchedTerms.length > 1) {
        bestScore += matchedTerms.length * 15
      }
    }

    if (bestScore > 0) {
      results.push({ item, score: bestScore, matchLevel, snippet })
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score)

  // Apply per-category limit if specified
  if (maxPerCategory < Infinity) {
    const categoryCounts = new Map<SearchCategory, number>()
    return results.filter(r => {
      const count = categoryCounts.get(r.item.category) || 0
      if (count >= maxPerCategory) return false
      categoryCounts.set(r.item.category, count + 1)
      return true
    })
  }

  return results
}

/**
 * Group results by category for display
 */
export function groupByCategory(results: SearchResult[]): Map<SearchCategory, SearchResult[]> {
  const grouped = new Map<SearchCategory, SearchResult[]>()
  for (const result of results) {
    const cat = result.item.category
    if (!grouped.has(cat)) grouped.set(cat, [])
    grouped.get(cat)!.push(result)
  }
  return grouped
}

/** Category display info */
export const CATEGORY_INFO: Record<
  SearchCategory,
  { label: string; icon: string; color: string }
> = {
  tutoriel: { label: 'Tutoriels', icon: '📖', color: 'emerald' },
  presentation: { label: 'Présentations', icon: '📊', color: 'cosmic' },
  package: { label: 'Packages IA', icon: '📦', color: 'purple' },
  application: { label: 'Applications', icon: '🖥️', color: 'sky' },
  formation: { label: 'Formations', icon: '🎓', color: 'amber' },
  video: { label: 'Vidéos', icon: '🎬', color: 'red' },
  vocabulaire: { label: 'Vocabulaire', icon: '📚', color: 'slate' },
}
