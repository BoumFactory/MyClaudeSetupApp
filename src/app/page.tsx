import Link from "next/link";
import { Code2, BookOpen, Download, AlertCircle, ChevronRight, Zap, GraduationCap, Video, Presentation } from "lucide-react";
import changelogs from "@/data/changelogs.json";

const TYPE_STYLES: Record<string, { label: string; color: string; bg: string }> = {
  feature: { label: 'Nouveau', color: 'text-emerald-400', bg: 'bg-emerald-500/15' },
  improvement: { label: 'Amélioré', color: 'text-blue-400', bg: 'bg-blue-500/15' },
  fix: { label: 'Corrigé', color: 'text-amber-400', bg: 'bg-amber-500/15' },
}

export default function HomePage() {
  const latest = changelogs.changelogs[0];

  return (
    <div className="space-y-16">
      {/* Disclaimer - Site en construction */}
      <section className="glass-card rounded-xl p-4 md:p-6 border-l-4 border-nebula-400">
        <div className="flex items-start gap-3">
          <div className="w-10 h-10 rounded-lg bg-nebula-900/50 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-nebula-400" />
          </div>
          <div className="space-y-1">
            <h3 className="font-semibold text-nebula-400">Site en construction</h3>
            <p className="text-sm text-muted-foreground">
              Ce site est actuellement en développement. Il peut contenir des erreurs et
              sera modifié régulièrement jusqu&apos;à sa stabilisation. Merci de votre compréhension.
            </p>
          </div>
        </div>
      </section>

      {/* Hero Section */}
      <section className="text-center space-y-6 py-12">
        <h1 className="text-5xl md:text-7xl font-bold glow-text">
          IA & Enseignement
          <br />
          <span className="bg-gradient-to-r from-cosmic-400 to-cosmic-600 bg-clip-text text-transparent">
            des Mathématiques
          </span>
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Découvrez comment j&apos;utilise l&apos;intelligence artificielle, et comment vous pouvez l&apos;utiliser de la même manière, simplement.
        </p>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Ici, on utilise Claude Code majoritairement. Parce que c&apos;est pragmatique.
        </p>
        <div className="flex flex-wrap gap-4 justify-center pt-4">
          <Link
            href="/claude-code/tutorials"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg cosmic-gradient text-white font-semibold hover:shadow-lg hover:shadow-cosmic-500/50 transition-all duration-300"
          >
            <GraduationCap className="w-5 h-5" />
            Commencer les tutoriels
          </Link>
          <Link
            href="/claude-code/presentations"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg glass-card hover:glow-border transition-all duration-300"
          >
            <BookOpen className="w-5 h-5" />
            Voir les présentations
          </Link>
        </div>
      </section>

      {/* Nouveautés — dernier changelog */}
      {latest && (
        <section className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <Zap className="w-6 h-6 text-amber-400" />
              Nouveautés
            </h2>
            <Link
              href="/changelog"
              className="text-sm text-muted-foreground hover:text-white transition-colors flex items-center gap-1"
            >
              Tout l&apos;historique
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="glass-card rounded-xl overflow-hidden border border-white/10">
            <div className="p-6 md:p-8 space-y-5">
              {/* Titre + date */}
              <div>
                <h3 className="text-lg font-semibold text-white">{latest.title}</h3>
                <p className="text-sm text-muted-foreground">{latest.date}</p>
              </div>

              {/* Changes highlights */}
              <div className="space-y-2.5">
                {latest.changes.filter((c: any) => c.highlight).map((change: any, i: number) => {
                  const style = TYPE_STYLES[change.type] || TYPE_STYLES.feature
                  return (
                    <div key={i} className="flex items-start gap-3 p-3 rounded-lg bg-white/[0.03] border border-white/5 hover:bg-white/[0.05] transition-colors">
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${style.bg} ${style.color} shrink-0 mt-0.5`}>
                        {style.label}
                      </span>
                      <div className="min-w-0">
                        <p className="text-sm font-medium text-gray-200">{change.title}</p>
                        <p className="text-xs text-muted-foreground mt-0.5 line-clamp-2">{change.details}</p>
                      </div>
                    </div>
                  )
                })}
              </div>

              {/* Footer */}
              {latest.changes.filter((c: any) => !c.highlight).length > 0 && (
                <p className="text-xs text-muted-foreground pt-2 border-t border-white/5">
                  + {latest.changes.filter((c: any) => !c.highlight).length} autres changements &middot;{' '}
                  <Link href="/changelog" className="text-cosmic-400 hover:underline">
                    voir le détail
                  </Link>
                </p>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="grid md:grid-cols-4 gap-6">
        <Link href="/claude-code/tutorials" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
              <GraduationCap className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-emerald-400 transition-colors">Tutoriels</h3>
            <p className="text-muted-foreground">
              Parcours interactifs pour apprendre à configurer et utiliser les agents IA pas à pas.
            </p>
          </div>
        </Link>

        <Link href="/claude-code/videos" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-rose-500 to-pink-600 flex items-center justify-center">
              <Video className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-rose-400 transition-colors">Vidéos</h3>
            <p className="text-muted-foreground">
              Démonstrations en vidéo de workflows complets avec Claude Code en situation réelle.
            </p>
          </div>
        </Link>

        <Link href="/claude-code/presentations" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center">
              <Presentation className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-nebula-400 transition-colors">Diaporamas</h3>
            <p className="text-muted-foreground">
              Présentations interactives pour comprendre l&apos;architecture et les skills disponibles.
            </p>
          </div>
        </Link>

        <Link href="/claude-code/downloads" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
              <Download className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-cosmic-400 transition-colors">Ressources téléchargeables</h3>
            <p className="text-muted-foreground">
              Bundles IA, packages LaTeX, logiciels et outils prêts à l&apos;emploi.
            </p>
          </div>
        </Link>
      </section>
    </div>
  );
}
