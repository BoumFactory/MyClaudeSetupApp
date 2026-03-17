import { notFound } from 'next/navigation'
import { getParcoursById, getCapsuleById } from '@/data/parcours'
import { CapsulePageContent } from './CapsulePageContent'

interface CapsulePageProps {
  params: Promise<{ parcours: string; capsule: string }>
}

export async function generateMetadata({ params }: CapsulePageProps) {
  const { capsule: capsuleId } = await params
  const capsule = getCapsuleById(capsuleId)
  if (!capsule) return { title: 'Capsule introuvable' }
  return {
    title: `${capsule.title} - Tutoriels`,
    description: capsule.description,
  }
}

export default async function CapsulePage({ params }: CapsulePageProps) {
  const { parcours: parcoursId, capsule: capsuleId } = await params
  const parcours = getParcoursById(parcoursId)
  const capsule = getCapsuleById(capsuleId)

  if (!parcours || !capsule) {
    notFound()
  }

  // Verifier que la capsule appartient bien au parcours
  if (!parcours.capsules.includes(capsuleId)) {
    notFound()
  }

  // Calculer prev/next
  const currentIndex = parcours.capsules.indexOf(capsuleId)
  const prevId = currentIndex > 0 ? parcours.capsules[currentIndex - 1] : null
  const nextId =
    currentIndex < parcours.capsules.length - 1
      ? parcours.capsules[currentIndex + 1]
      : null

  const prevCapsule = prevId ? getCapsuleById(prevId) : null
  const nextCapsule = nextId ? getCapsuleById(nextId) : null

  return (
    <CapsulePageContent
      parcours={parcours}
      capsule={capsule}
      prevCapsule={prevCapsule ?? null}
      nextCapsule={nextCapsule ?? null}
    />
  )
}
