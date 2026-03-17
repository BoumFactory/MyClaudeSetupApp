'use client'

import { VOCABULARY } from '@/data/vocabulary'

interface VocabTooltipProps {
  term: string
}

export function VocabTooltip({ term }: VocabTooltipProps) {
  const vocab = VOCABULARY.find(
    (v) =>
      v.term.toLowerCase() === term.toLowerCase() ||
      v.aliases?.some((a) => a.toLowerCase() === term.toLowerCase())
  )

  if (!vocab) {
    return <>{term}</>
  }

  return (
    <span className="vocab-term-react" role="definition" aria-label={vocab.definition}>
      <span className="vocab-term-word">{term}</span>
      <span className="vocab-term-bubble" aria-hidden="true">
        <span className="vocab-term-bubble-definition">{vocab.definition}</span>
        {vocab.docUrl && (
          <a
            href={vocab.docUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="vocab-term-bubble-link"
            onClick={(e) => e.stopPropagation()}
          >
            Voir la doc →
          </a>
        )}
      </span>
    </span>
  )
}
