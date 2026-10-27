import fs from 'node:fs'
import path from 'node:path'
import type { Metadata } from 'next'
import { Breadcrumb } from '@/components/layout/Breadcrumb'
import { CodeBlock } from '@/components/ui/code-block'
import {
  Video,
  Download,
  ExternalLink,
  Package,
  Terminal,
  Sparkles,
  Mic,
  Clapperboard,
  Cpu,
} from 'lucide-react'

export const metadata: Metadata = {
  title: 'Créer des vidéos avec Claude Code',
  description:
    "Fabriquer des capsules vidéo animées (corrections d'exercices, explications de cours) avec Claude Code : voix de synthèse ou clonée, gestes calés sur chaque mot, logiciels gratuits.",
}

/** Fichier autonome embarqué dans l'application (public/tutoriels). */
const TUTO_URL = '/tutoriels/capsules-animees-tuto.html'
const TUTO_NOM = 'capsules-animees-tuto.html'
const YOUTUBE_URL = 'https://youtu.be/okn0E7I2tE0'

/** Poids du fichier lu à la génération de la page. */
function lirePoids(): string {
  try {
    const stat = fs.statSync(path.join(process.cwd(), 'public', 'tutoriels', TUTO_NOM))
    return `${Math.round(stat.size / 1e6)} Mo`
  } catch {
    return '4 Mo'
  }
}

const OBTENU = [
  {
    icon: Clapperboard,
    title: 'Ce qu’on obtient',
    text: "Une vidéo MP4 où chaque geste suit la voix, mot à mot : les nombres quittent le tableau pour se poser dans la formule, les lignes s’allument, les résultats tombent en place. Formules, figures, tableaux et scènes 3D, en thème sombre ou clair.",
  },
  {
    icon: Mic,
    title: 'Deux points de départ',
    text: "Vous enregistrez votre correction (Claude la transcrit puis l’anime), ou Claude rédige le texte et une voix de synthèse française le lit : voix du catalogue ou clone de la vôtre, à partir de 15 à 20 secondes d’échantillon.",
  },
  {
    icon: Cpu,
    title: '100 % local et gratuit',
    text: "Tout tourne sur votre ordinateur, sans carte graphique obligatoire. Le rendu prend environ 10 à 20 secondes pour une capsule 2D de 2 à 4 minutes, en 540p léger (environ 2 Mo par minute).",
  },
]

const COMMANDES_LOGICIELS = `winget install Git.Git
winget install Python.Python.3.12
winget install Gyan.FFmpeg
irm https://claude.ai/install.ps1 | iex`

const COMMANDE_INSTALLEUR = `powershell -ExecutionPolicy Bypass -File .\\installer.ps1`

const COMMANDE_LANCEMENT = `cd D:\\Capsules
claude`

export default function CapsulesVideoPage() {
  const poids = lirePoids()

  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-5xl mx-auto">
        <Breadcrumb
          items={[
            { label: 'Claude Code', href: '/claude-code' },
            { label: 'Tutoriels', href: '/claude-code/tutorials' },
            { label: 'Créer des vidéos', href: '/claude-code/tutorials/capsules-video' },
          ]}
        />
      </div>

      {/* En-tête */}
      <div className="text-center mb-10 max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-amber-500/15 border border-amber-400/40 text-sm text-amber-300 mb-6">
          <Video className="w-4 h-4" />
          Tutoriel · Vidéo
        </div>
        <h1 className="text-4xl font-bold text-white mb-4">Créer des vidéos avec Claude Code</h1>
        <p className="text-lg text-white/60">
          Une correction d&apos;exercice ou une explication de cours devient une vidéo animée dont chaque geste suit la
          voix. Ce tutoriel tout-en-un explique quoi installer, quelles commandes lancer et comment demander votre
          première capsule à l&apos;agent grâce au skill{' '}
          <code className="text-cosmic-300 bg-cosmic-900/50 px-1.5 py-0.5 rounded text-sm">capsule-video</code>.
        </p>
        <p className="mt-3">
          <a
            href={YOUTUBE_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-amber-300 hover:text-amber-200 underline underline-offset-4"
          >
            <ExternalLink className="w-4 h-4" />
            Voir la vidéo de présentation sur YouTube (6 minutes)
          </a>
        </p>
        <p className="mt-2">
          <a
            href="/claude-code/presentations/capsule-video-skill"
            className="inline-flex items-center gap-2 text-cosmic-300 hover:text-cosmic-200 underline underline-offset-4"
          >
            <Package className="w-4 h-4" />
            Comment travaille l&apos;agent, et le skill seul en pack
          </a>
        </p>
      </div>

      {/* À quoi ça sert */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-5xl mx-auto mb-10">
        {OBTENU.map(({ icon: Icon, title, text }) => (
          <div key={title} className="glass-card rounded-xl p-5 border border-cosmic-500/20">
            <div className="w-10 h-10 rounded-lg bg-cosmic-500/20 flex items-center justify-center mb-3">
              <Icon className="w-5 h-5 text-cosmic-300" />
            </div>
            <h2 className="font-semibold text-white mb-1">{title}</h2>
            <p className="text-sm text-white/55">{text}</p>
          </div>
        ))}
      </div>

      {/* Résumé : quoi installer, commandes, tout-en-un */}
      <div className="max-w-5xl mx-auto glass-card rounded-xl border border-white/10 p-6 mb-10 space-y-6">
        <h2 className="text-2xl font-bold text-white flex items-center gap-3">
          <Terminal className="w-6 h-6 text-cosmic-300" />
          En résumé
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-3">
            <h3 className="font-semibold text-white">Quoi installer</h3>
            <ul className="list-disc list-inside space-y-1.5 text-sm text-white/65">
              <li>
                <strong className="text-white/85">Claude Code</strong> (ou un autre agent qui sait utiliser un skill),
                avec un compte Claude.
              </li>
              <li>
                <strong className="text-white/85">Git, Python 3.12 et ffmpeg</strong>, gratuits.
              </li>
              <li>
                Le reste (voix Pocket TTS, contrôle Parakeet, horodatage MFA, Chromium, Piper de secours) est posé par
                l&apos;installeur, environ 6 Go et 20 à 40 minutes, surtout du téléchargement.
              </li>
              <li>Whisper n&apos;est utile que pour transcrire vos propres enregistrements (facultatif).</li>
            </ul>
          </div>

          <div className="space-y-3">
            <h3 className="font-semibold text-white">Les logiciels, en PowerShell</h3>
            <CodeBlock code={COMMANDES_LOGICIELS} language="powershell" filename="PowerShell" />
            <p className="text-xs text-white/45">Fermez puis rouvrez PowerShell ensuite, puis connectez-vous au premier lancement de claude.</p>
          </div>
        </div>

        <div className="rounded-xl border border-amber-400/30 bg-amber-500/10 p-5 space-y-3">
          <h3 className="font-semibold text-amber-300 flex items-center gap-2">
            <Package className="w-5 h-5" />
            L&apos;option tout-en-un : le kit et son installeur
          </h3>
          <p className="text-sm text-white/65">
            Le tutoriel ci-dessous contient le <strong className="text-white/85">kit à télécharger</strong> (1,5 Mo :
            installeur Windows, installeur Linux et macOS, mode d&apos;emploi et skill{' '}
            <code className="text-cosmic-300">capsule-video</code>, sans aucune voix clonée). Après l&apos;avoir
            décompressé :
          </p>
          <CodeBlock code={COMMANDE_INSTALLEUR} language="powershell" filename="Installeur Windows" />
          <p className="text-sm text-white/65">
            Indiquez le dossier de base (par exemple <code className="text-cosmic-300">D:\Capsules</code>, sans espace
            ni accent) : tout s&apos;y installe et rien ailleurs. Puis ouvrez l&apos;agent dans ce dossier et demandez une
            capsule :
          </p>
          <CodeBlock code={COMMANDE_LANCEMENT} language="powershell" filename="Premier usage" />
          <p className="text-xs text-white/45">
            Sur Linux et macOS (non testés), l&apos;installeur est <code>bash installer.sh</code>.
          </p>
        </div>
      </div>

      {/* Boutons */}
      <div className="max-w-5xl mx-auto flex flex-wrap items-center gap-3 mb-4">
        <a
          href={TUTO_URL}
          download={TUTO_NOM}
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg bg-amber-400 text-slate-900 font-semibold hover:bg-amber-300 transition-colors"
        >
          <Download className="w-5 h-5" />
          Télécharger le tutoriel (HTML, {poids})
        </a>
        <a
          href={TUTO_URL}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-lg border border-cosmic-500/40 text-cosmic-300 font-medium hover:bg-cosmic-900/40 transition-colors"
        >
          <ExternalLink className="w-5 h-5" />
          Ouvrir dans un nouvel onglet
        </a>
        <span className="text-sm text-white/45 flex items-center gap-2">
          <Sparkles className="w-4 h-4" />
          Fichier léger, avec le kit inclus. La vidéo est lue depuis YouTube (connexion nécessaire).
        </span>
      </div>

      {/* Le tutoriel */}
      <div className="max-w-5xl mx-auto mb-6">
        <iframe
          src={TUTO_URL}
          title="Tutoriel : créer des vidéos avec Claude Code"
          loading="lazy"
          className="w-full rounded-xl border border-white/10 bg-white"
          style={{ height: '85vh', minHeight: '640px' }}
        />
        <p className="text-xs text-white/40 mt-2">
          Le tutoriel pèse {poids} (kit inclus ; la vidéo de présentation est lue depuis{' '}
          <a href={YOUTUBE_URL} target="_blank" rel="noopener noreferrer" className="underline hover:text-white/70">
            YouTube
          </a>
          ). Les polices viennent de Google Fonts ; sans connexion, des polices système les remplacent.
        </p>
      </div>
    </div>
  )
}
