import Link from "next/link";
import { Code2, Sparkles, BookOpen, Download, AlertCircle } from "lucide-react";
import { scopes } from "@/lib/data/scopes";
import { ScopeCard } from "@/components/ScopeCard";

export default function HomePage() {
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
              sera modifié régulièrement jusqu'à sa stabilisation. Merci de votre compréhension.
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
          Découvrez comment j'utilise l'intelligence artificielle, et comment vous pouvez l'utiliser de la même manière, simplement.
        </p>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Ici, on utilise Claude Code majoritairement. Parce que c'est pragmatique.
        </p>
        <div className="flex flex-wrap gap-4 justify-center pt-4">
          <Link
            href="/claude-code"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-lg cosmic-gradient text-white font-semibold hover:shadow-lg hover:shadow-cosmic-500/50 transition-all duration-300"
          >
            <Code2 className="w-5 h-5" />
            Découvrir Claude Code
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

      {/* Features Section */}
      <section className="grid md:grid-cols-4 gap-6">
        <Link href="/claude-code" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-cosmic-400 transition-colors">Tutos Claude Code</h3>
            <p className="text-muted-foreground">
              Des tutoriels pour configurer votre environnement de travail.
            </p>
          </div>
        </Link>

        <Link href="/claude-code/videos" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
              <Code2 className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-cosmic-400 transition-colors">Vidéos Claude Code</h3>
            <p className="text-muted-foreground">
              Des vidéos pour observer le fonctionnement de ma configuration.
            </p>
          </div>
        </Link>
        <Link href="/claude-code/presentations" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg nebula-gradient flex items-center justify-center">
              <BookOpen className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-nebula-400 transition-colors">Présentations Interactives</h3>
            <p className="text-muted-foreground">
              Pour comprendre ce qui se trouve dans ma configuration Claude Code.
            </p>
            <p className="text-muted-foreground">
              Pour en apprendre plus sur le fonctionnement des agents modernes.
            </p>
          </div>
        </Link>

        <Link href="/claude-code/downloads" className="block group">
          <div className="glass-card rounded-xl p-6 space-y-3 hover:scale-105 transition-all duration-300 cursor-pointer h-full">
            <div className="w-12 h-12 rounded-lg cosmic-gradient flex items-center justify-center">
              <Download className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-xl font-bold group-hover:text-cosmic-400 transition-colors">Ressources Téléchargeables</h3>
            <p className="text-muted-foreground">
              Pour télécharger facilement ce que je partage ici.
            </p>
          </div>
        </Link>
      </section>
    </div>
  );
}
