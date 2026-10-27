import type { Metadata } from 'next'
import Link from 'next/link'
import { ArrowDown, MessageSquare, Presentation, Wand2 } from 'lucide-react'
import { Breadcrumb } from '@/components/layout/Breadcrumb'
import { PresentationViewer } from '@/components/presentations/PresentationViewer'
import { CreerUnSkillStepper } from '@/components/tutorials/creer-un-skill/CreerUnSkillStepper'

export const metadata: Metadata = {
  title: 'Créer son propre skill avec skill-creator',
  description:
    "Tutoriel pas à pas : faire écrire à l'agent un skill qui rédige vos cours comme vous, à partir d'un cours déjà fait. Interview grill-me, écriture par skill-creator, test sur un cas connu, amélioration continue.",
}

const DIAPORAMA = '/render/Reveals/creer-un-skill.html'

export default function CreerUnSkillPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-5xl mx-auto">
        <Breadcrumb
          items={[
            { label: 'Claude Code', href: '/claude-code' },
            { label: 'Tutoriels', href: '/claude-code/tutorials' },
            { label: 'Créer son propre skill', href: '/claude-code/tutorials/creer-un-skill' },
          ]}
        />
      </div>

      {/* En-tête */}
      <div className="text-center mb-10 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-violet-500/15 border border-violet-400/40 text-sm text-violet-300 mb-6">
          <Wand2 className="w-4 h-4" />
          Tutoriel · 6 étapes
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">Créer son propre skill avec skill-creator</h1>
        <p className="text-lg text-white/60">
          Un skill est une fiche de consignes que l&apos;agent relit à chaque fois qu&apos;il en a besoin. Dans ce
          tutoriel, vous en faites écrire un qui rédige vos cours <em>comme vous</em>, à partir d&apos;un cours que vous
          avez déjà fait.
        </p>

        <div className="mt-6 flex flex-col items-center gap-2">
          <div className="max-w-xl rounded-2xl rounded-bl-sm border border-sky-500/40 bg-sky-950/30 px-4 py-3 text-left">
            <div className="text-xs font-semibold text-sky-300 mb-1 flex items-center gap-1">
              <MessageSquare className="w-3.5 h-3.5" /> Vous, à la fin du tutoriel
            </div>
            <p className="text-sm text-white/85">« /mes-cours Le cours sur les fractions pour une 5e. »</p>
          </div>
          <ArrowDown className="w-5 h-5 text-white/40" />
          <div className="rounded-lg bg-gradient-to-r from-red-500 to-rose-600 px-4 py-2 text-sm font-semibold text-white">
            Un cours dans votre format, avec votre structure et votre ton, à relire.
          </div>
        </div>

        <p className="mt-6 text-sm text-white/50">
          Votre rôle : décrire votre façon de faire, répondre aux questions, relire et signaler.{' '}
          <a href="#diaporama" className="inline-flex items-center gap-1 text-cosmic-300 hover:text-cosmic-200 underline underline-offset-4">
            <Presentation className="w-4 h-4" /> La démarche en diaporama
          </a>
        </p>
      </div>

      {/* Les étapes */}
      <div className="max-w-5xl mx-auto">
        <CreerUnSkillStepper />
      </div>

      {/* Le diaporama */}
      <section id="diaporama" className="max-w-5xl mx-auto mt-16 space-y-4 scroll-mt-24">
        <div className="glass-card rounded-xl p-6">
          <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
            <Presentation className="w-6 h-6 text-cosmic-300" /> La démarche en diaporama
          </h2>
          <p className="text-sm text-white/60">
            Pour la présenter à des collègues : <kbd className="px-1 rounded border border-white/20">→</kbd> suit les six
            étapes, <kbd className="px-1 rounded border border-white/20">↓</kbd> descend dans les détails (exemple
            d&apos;interview, anatomie d&apos;un skill, critères de test…).{' '}
            <Link href="/claude-code/presentations/creer-un-skill" className="underline text-cosmic-300 hover:text-cosmic-200">
              Ouvrir sur sa propre page
            </Link>
          </p>
        </div>
        <PresentationViewer presentationUrl={DIAPORAMA} title="Créer son propre skill" />
      </section>

      <p className="max-w-5xl mx-auto mt-8 text-sm text-white/50 text-center">
        Version courte, et autre méthode (transformer une ressource en skill) : capsule{' '}
        <Link href="/claude-code/tutorials/parcours/avance/av-creer-skill" className="underline hover:text-white/80">
          Créer un skill
        </Link>{' '}
        du parcours Avancé.
      </p>
    </div>
  )
}
