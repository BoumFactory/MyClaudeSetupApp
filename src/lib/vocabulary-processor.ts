import { VOCABULARY } from '@/data/vocabulary'

/**
 * Remplace la première occurrence de chaque terme du vocabulaire dans un HTML
 * par un <span> contenant un vrai tooltip HTML (pas un pseudo-element CSS).
 * Ne remplace PAS dans les balises <code>, <pre>, <h1>-<h4>, <a>, <span>.
 */
export function processVocabulary(html: string): string {
  if (!html) return html

  let result = html

  for (const vocab of VOCABULARY) {
    const allVariants = [vocab.term, ...(vocab.aliases ?? [])]

    for (const variant of allVariants) {
      const escapedVariant = variant.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
      const wordRegex = new RegExp(`(?<![\\w\\-])${escapedVariant}(?![\\w\\-])`, 'i')

      const replaced = replaceOutsideProtectedTags(result, wordRegex, (match) => {
        // La définition contient du HTML intentionnel (<b>) — on ne l'escape pas
        const defHtml = vocab.definition
        // Valider docUrl: doit commencer par https:// ou http://
        const isValidUrl = vocab.docUrl && (vocab.docUrl.startsWith('https://') || vocab.docUrl.startsWith('http://'))
        const linkHtml = isValidUrl
          ? `<a href="${escapeHtml(vocab.docUrl!)}" target="_blank" rel="noopener noreferrer" class="vocab-tooltip-link">Voir la documentation →</a>`
          : ''
        const closeBtn = `<button type="button" class="vocab-tooltip-close" aria-label="Fermer">×</button>`
        const escapedMatch = escapeHtml(match)

        return `<span class="vocab-term">${escapedMatch}<span class="vocab-tooltip">${closeBtn}<span class="vocab-tooltip-def">${defHtml}</span>${linkHtml}</span></span>`
      })

      if (replaced !== result) {
        result = replaced
        break
      }
    }
  }

  return result
}

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/**
 * Remplace la première occurrence du pattern dans le HTML,
 * en ignorant le contenu des balises protégées.
 */
function replaceOutsideProtectedTags(
  html: string,
  pattern: RegExp,
  replacer: (match: string) => string
): string {
  const protectedTags = ['code', 'pre', 'h1', 'h2', 'h3', 'h4', 'a', 'span']

  const segments: Array<{ type: 'tag' | 'text'; value: string }> = []
  const tagRegex = /<[^>]*>/g
  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = tagRegex.exec(html)) !== null) {
    if (match.index > lastIndex) {
      segments.push({ type: 'text', value: html.slice(lastIndex, match.index) })
    }
    segments.push({ type: 'tag', value: match[0] })
    lastIndex = match.index + match[0].length
  }
  if (lastIndex < html.length) {
    segments.push({ type: 'text', value: html.slice(lastIndex) })
  }

  let protectedDepth = 0
  let replaced = false
  const result: string[] = []

  for (const seg of segments) {
    if (seg.type === 'tag') {
      const tagName = seg.value.match(/^<\/?([a-zA-Z][a-zA-Z0-9]*)/)?.[1]?.toLowerCase() ?? ''
      if (protectedTags.includes(tagName)) {
        if (seg.value.startsWith('</')) {
          protectedDepth = Math.max(0, protectedDepth - 1)
        } else if (!seg.value.endsWith('/>')) {
          protectedDepth++
        }
      }
      result.push(seg.value)
    } else {
      if (!replaced && protectedDepth === 0) {
        const newText = seg.value.replace(pattern, (m) => {
          replaced = true
          return replacer(m)
        })
        result.push(newText)
      } else {
        result.push(seg.value)
      }
    }
  }

  return result.join('')
}
