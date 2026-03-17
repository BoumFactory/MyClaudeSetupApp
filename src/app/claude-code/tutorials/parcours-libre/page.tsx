import { Metadata } from 'next'
import { BookOpen } from 'lucide-react'
import { Breadcrumb } from '@/components/layout/Breadcrumb'
import { ProgressDashboard } from '@/components/tutorials/ProgressDashboard'
import { ParcoursLibreContent } from './ParcoursLibreContent'

export const metadata: Metadata = {
  title: 'Parcours libre - Tutoriels',
  description: 'Explorez librement toutes les capsules tutoriels sans suivre un parcours particulier',
}

export default function ParcoursLibrePage() {
  return (
    <div className="space-y-12">
      {/* Breadcrumb */}
      <Breadcrumb
        items={[
          { label: 'Claude Code', href: '/claude-code' },
          { label: 'Tutoriels', href: '/claude-code/tutorials' },
          { label: 'Parcours libre', href: '/claude-code/tutorials/parcours-libre' },
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <BookOpen className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Parcours libre
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Explorez toutes les capsules sans suivre un parcours particulier.
          Progressez librement dans vos domaines d&apos;intérêt.
        </p>
      </section>

      {/* Dashboard de progression */}
      <ProgressDashboard />

      {/* Capsules organisées par parcours */}
      <section className="space-y-8">
        <ParcoursLibreContent />
      </section>
    </div>
  )
}
