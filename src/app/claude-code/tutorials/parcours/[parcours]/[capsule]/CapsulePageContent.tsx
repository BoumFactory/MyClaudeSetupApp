'use client'

import { useMemo } from 'react'
import Link from 'next/link'
import { ChevronRight, ChevronLeft, ArrowLeft } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Capsule } from '@/components/tutorials/Capsule'
import { QuickViewGraph } from '@/components/tutorials/QuickViewGraph'
import { SkillDecisionTree } from '@/components/tutorials/SkillDecisionTree'
import { PrePlanDemo } from '@/components/tutorials/PrePlanDemo'
import { IdeaChallengerCopy } from '@/components/tutorials/IdeaChallengerCopy'
import type { Parcours, Capsule as CapsuleType } from '@/types/tutorial'

interface CapsulePageContentProps {
  parcours: Parcours
  capsule: CapsuleType
  prevCapsule: CapsuleType | null
  nextCapsule: CapsuleType | null
}

export function CapsulePageContent({
  parcours,
  capsule,
  prevCapsule,
  nextCapsule,
}: CapsulePageContentProps) {
  /** Composants interactifs à injecter dans les sections de certaines capsules */
  const sectionComponents = useMemo(() => {
    if (capsule.id === 'qv-overview') {
      return {
        exemple: <QuickViewGraph />,
      }
    }
    if (capsule.id === 'pc-skills-agents') {
      return {
        pratique: <SkillDecisionTree />,
      }
    }
    if (capsule.id === 'pc-idea-challenger') {
      return {
        pratique: <IdeaChallengerCopy />,
      }
    }
    if (capsule.id === 'pc-preplan') {
      return {
        pratique: <PrePlanDemo />,
      }
    }
    return undefined
  }, [capsule.id])

  return (
    <div className="max-w-4xl mx-auto space-y-6 px-4 py-8">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-gray-400 flex-wrap">
        <Link href="/claude-code/tutorials" className="hover:text-white transition-colors">
          Tutoriels
        </Link>
        <ChevronRight className="w-4 h-4 shrink-0" />
        <Link
          href={`/claude-code/tutorials/parcours/${parcours.id}`}
          className="hover:text-white transition-colors"
        >
          {parcours.title}
        </Link>
        <ChevronRight className="w-4 h-4 shrink-0" />
        <span className="text-white">{capsule.title}</span>
      </nav>

      {/* Contenu de la capsule */}
      <Capsule capsule={capsule} sectionComponents={sectionComponents} />

      {/* Navigation prev/next */}
      <div className="flex items-center justify-between gap-4 pt-4">
        {prevCapsule ? (
          <Button asChild variant="ghost" className="text-gray-400 hover:text-white">
            <Link href={`/claude-code/tutorials/parcours/${parcours.id}/${prevCapsule.id}`}>
              <ChevronLeft className="w-4 h-4 mr-1" />
              {prevCapsule.title}
            </Link>
          </Button>
        ) : (
          <Button asChild variant="ghost" className="text-gray-400 hover:text-white">
            <Link href={`/claude-code/tutorials/parcours/${parcours.id}`}>
              <ArrowLeft className="w-4 h-4 mr-1" />
              Retour au parcours
            </Link>
          </Button>
        )}

        {nextCapsule ? (
          <Button asChild variant="ghost" className="text-gray-400 hover:text-white">
            <Link href={`/claude-code/tutorials/parcours/${parcours.id}/${nextCapsule.id}`}>
              {nextCapsule.title}
              <ChevronRight className="w-4 h-4 ml-1" />
            </Link>
          </Button>
        ) : (
          <Button asChild variant="ghost" className="text-gray-400 hover:text-white">
            <Link href={`/claude-code/tutorials/parcours/${parcours.id}`}>
              Terminer le parcours
              <ChevronRight className="w-4 h-4 ml-1" />
            </Link>
          </Button>
        )}
      </div>
    </div>
  )
}
