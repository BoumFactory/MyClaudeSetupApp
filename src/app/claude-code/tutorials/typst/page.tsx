import fs from 'node:fs'
import path from 'node:path'
import Link from 'next/link'
import type { Metadata } from 'next'
import { GraduationCap, ListChecks, PenLine, Eye, Package, Download, ArrowRight, AlertTriangle } from 'lucide-react'
import LanceurFormation from './LanceurFormation'

export const metadata: Metadata = {
  title: 'Formation Typst avec farfadet',
  description:
    "Apprendre Typst et la suite farfadet en écrivant : des leçons courtes avec un éditeur, la compilation dans le navigateur et un cahier des charges qui se coche tout seul.",
}

// Application complète (éditeur de documents, modèles, Prompt IA) : un fichier HTML hébergé sur la Forge
const APP_URL = 'https://forge.apps.education.fr/romaindeschamps/farfadet/-/raw/main/application/ecriture-typst.html'

interface InfosFormation {
  totalGzip: number
  chapitres: { titre: string; lecons: number }[]
}

/** Poids et sommaire écrits par le build de la Formation (public/typst-formation/poids.json), lus à la génération de la page. */
function lireInfos(): InfosFormation | null {
  try {
    const brut = fs.readFileSync(path.join(process.cwd(), 'public', 'typst-formation', 'poids.json'), 'utf8')
    const infos = JSON.parse(brut) as Partial<InfosFormation>
    if (typeof infos.totalGzip !== 'number' || !Array.isArray(infos.chapitres)) return null
    return { totalGzip: infos.totalGzip, chapitres: infos.chapitres }
  } catch {
    return null
  }
}

const ETAPES: { icon: typeof Eye; title: string; text: string }[] = [
  {
    icon: Eye,
    title: 'Une notion, un exemple',
    text: "Chaque leçon explique une notion en quelques lignes et montre un exemple compilé, sur un autre contenu que l'exercice.",
  },
  {
    icon: PenLine,
    title: 'Vous écrivez',
    text: "L'exercice se fait dans un éditeur Typst, avec l'aperçu du document à côté, en version professeur ou élève.",
  },
  {
    icon: ListChecks,
    title: 'Le cahier des charges se coche',
    text: 'Les critères se vérifient à chaque frappe sur le document compilé. Une solution reste disponible après un premier essai.',
  },
]

export default function FormationTypstPage() {
  const infos = lireInfos()
  const poids = infos ? `environ ${Math.round(infos.totalGzip / 1e6)} Mo` : 'environ 15 Mo'
  const nbLecons = infos?.chapitres.reduce((s, c) => s + c.lecons, 0)

  return (
    <div className="container mx-auto px-4 py-12">
      {/* En-tête */}
      <div className="text-center mb-10 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cosmic-900/50 border border-cosmic-700/50 text-sm text-cosmic-300 mb-6">
          <GraduationCap className="w-4 h-4" />
          Formation interactive
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">Typst avec farfadet, en écrivant</h1>
        <p className="text-lg text-white/60">
          {nbLecons ? `${nbLecons} leçons courtes` : 'Des leçons courtes'} pour passer de LaTeX à Typst et prendre en
          main la suite <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">farfadet</code> :
          cours, exercices, zones de réponse, QCM, tableaux, figures, outils du collège. Tout se passe dans cette page.
        </p>
      </div>

      {/* Comment ça marche */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-5xl mx-auto mb-10">
        {ETAPES.map(({ icon: Icon, title, text }) => (
          <div key={title} className="glass-card rounded-xl p-5 border border-cosmic-500/20">
            <div className="w-10 h-10 rounded-lg bg-cosmic-500/20 flex items-center justify-center mb-3">
              <Icon className="w-5 h-5 text-cosmic-300" />
            </div>
            <h2 className="font-semibold text-white mb-1">{title}</h2>
            <p className="text-sm text-white/55">{text}</p>
          </div>
        ))}
      </div>

      {/* Sommaire */}
      {infos && (
        <div className="max-w-5xl mx-auto glass-card rounded-xl border border-white/10 p-6 mb-10">
          <h2 className="text-xl font-bold text-white mb-4">Les chapitres</h2>
          <ol className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-6 gap-y-2 text-sm">
            {infos.chapitres.map((c, i) => (
              <li key={c.titre} className="flex gap-2 text-white/65">
                <span className="text-cosmic-300 font-medium w-6 flex-shrink-0">{i + 1}.</span>
                <span className="flex-1">{c.titre}</span>
                <span className="text-white/40">
                  {c.lecons} leçon{c.lecons > 1 ? 's' : ''}
                </span>
              </li>
            ))}
          </ol>
        </div>
      )}

      {/* La formation */}
      <div className="max-w-[1600px] mx-auto mb-10">
        <LanceurFormation poids={poids} />
      </div>

      {/* Pour aller plus loin */}
      <div className="max-w-5xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <Link href="/claude-code/download-typst-packages" prefetch={false} className="group block">
          <div className="glass-card h-full rounded-xl p-5 border border-cosmic-500/30 hover:border-cosmic-400/50 transition-all duration-300 flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center flex-shrink-0">
              <Package className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="font-semibold text-white group-hover:text-cosmic-300 transition-colors">Packages Typst</h2>
              <p className="text-sm text-white/55">Installer farfadet sur votre poste en une commande, avec VS Code.</p>
            </div>
            <ArrowRight className="w-5 h-5 text-cosmic-400 flex-shrink-0" />
          </div>
        </Link>
        <a href={APP_URL} download="ecriture-typst.html" className="group block">
          <div className="glass-card h-full rounded-xl p-5 border border-nebula-500/30 hover:border-nebula-400/50 transition-all duration-300 flex items-center gap-4">
            <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center flex-shrink-0">
              <Download className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1">
              <h2 className="font-semibold text-white group-hover:text-nebula-300 transition-colors">
                Application Écriture Typst
              </h2>
              <p className="text-sm text-white/55">
                L&apos;éditeur complet hors ligne : documents, modèles, Prompt IA, export PDF (un fichier HTML de 29 Mo).
              </p>
            </div>
            <Download className="w-5 h-5 text-nebula-400 flex-shrink-0" />
          </div>
        </a>
      </div>

      {/* Note */}
      <div className="max-w-5xl mx-auto glass-card p-4 rounded-xl border border-amber-500/20 bg-amber-950/10">
        <div className="flex items-start gap-3">
          <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-white/50">
            La formation embarque la suite farfadet et ses polices ; elle ne télécharge pas d&apos;autre paquet Typst.
            Le bouton « Télécharger le .typ » de chaque leçon donne un fichier complet, à compiler avec Typst et
            farfadet installés. Sur un téléphone, l&apos;écran est trop étroit pour l&apos;éditeur et l&apos;aperçu côte à côte.
          </p>
        </div>
      </div>
    </div>
  )
}
