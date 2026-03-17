import { notFound } from 'next/navigation'
import { getParcoursById, CAPSULES } from '@/data/parcours'
import { ParcoursContent } from './ParcoursContent'

interface ParcoursPageProps {
  params: Promise<{ parcours: string }>
}

export async function generateMetadata({ params }: ParcoursPageProps) {
  const { parcours: parcoursId } = await params
  const parcours = getParcoursById(parcoursId)
  if (!parcours) return { title: 'Parcours introuvable' }
  return {
    title: `${parcours.title} - Tutoriels`,
    description: parcours.description,
  }
}

export default async function ParcoursPage({ params }: ParcoursPageProps) {
  const { parcours: parcoursId } = await params
  const parcours = getParcoursById(parcoursId)

  if (!parcours) {
    notFound()
  }

  // Charger les capsules du parcours
  const capsules = parcours.capsules
    .map((id) => CAPSULES[id])
    .filter(Boolean)

  return <ParcoursContent parcours={parcours} capsules={capsules} />
}
