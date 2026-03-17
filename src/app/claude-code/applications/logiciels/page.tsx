import { FileText, ExternalLink, Wrench, Settings, Sparkles, Github, Download, BarChart3, BookOpen, Puzzle, Globe } from "lucide-react"
import Link from "next/link"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AddToCartButton } from "@/components/cart/AddToCartButton"
import type { Metadata } from "next"
import type { CartItem } from "@/types/cart-theme"

export const metadata: Metadata = {
  title: "Logiciels Enseignants",
  description: "Outils de productivité créés avec Claude Code pour les enseignants de mathématiques",
}

/**
 * Page des logiciels enseignants créés avec Claude Code
 */
export default function LogicielsEnseignantsPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl nebula-gradient mb-4">
          <Wrench className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Logiciels Enseignants
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Outils de productivité et d'automatisation créés avec Claude Code pour les enseignants de mathématiques
        </p>
      </section>

      {/* Introduction */}
      <section className="glass-card rounded-xl p-6">
        <p className="text-muted-foreground leading-relaxed">
          Ces logiciels sont conçus pour faciliter le travail quotidien des enseignants :
          génération automatique de documents, organisation des cours, automatisation de tâches répétitives,
          et bien plus encore. Chaque outil a été pensé pour gagner du temps et améliorer votre productivité.
        </p>
      </section>

      {/* CTA GitHub */}
      <section className="glass-card rounded-xl p-8 border-l-4 border-nebula-400 space-y-4">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-lg bg-nebula-900/50 flex items-center justify-center flex-shrink-0">
            <Github className="w-6 h-6 text-nebula-400" />
          </div>
          <div className="flex-1 space-y-3">
            <h3 className="text-xl font-semibold text-nebula-400">Disponible sur GitHub</h3>
            <p className="text-muted-foreground">
              Tous les logiciels enseignants sont disponibles en open source sur le dépôt GitHub <strong>BFtools</strong>.
              Vous y trouverez des outils pour la préparation de cours, la gestion de classe et l'automatisation
              de tâches pédagogiques.
            </p>
            <div className="flex flex-wrap gap-3">
              <AddToCartButton
                item={{ id: 'bftools-repo', name: 'BFtools (GitHub)', type: 'logiciel', path: 'logiciels-enseignant', description: 'Depot GitHub BFtools - outils enseignants' }}
                variant="nebula"
                className="w-full sm:w-auto"
              />
              <Button asChild variant="ghost" size="sm" className="w-full sm:w-auto">
                <a
                  href="https://github.com/Romain1099/BFtools.git"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Github className="w-4 h-4 mr-1" />
                  <span className="text-xs">Voir sur GitHub</span>
                  <ExternalLink className="w-3 h-3 ml-1" />
                </a>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Outils prêts à l'emploi */}
      <section className="space-y-6">
        <div>
          <h2 className="text-2xl font-bold">Outils prêts à l&apos;emploi</h2>
          <p className="text-muted-foreground mt-1">
            Applications web autonomes — ouvrez le fichier HTML dans votre navigateur, aucune installation requise.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5">
          {/* Loiseau Generator */}
          <Card className="glass-card border-2 border-violet-500/20 hover:border-violet-500/40 transition-all duration-300 group">
            <CardHeader>
              <div className="flex items-start justify-between mb-2">
                <div className="w-11 h-11 rounded-lg bg-gradient-to-br from-violet-500 to-purple-600 flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <span className="text-xs px-2 py-0.5 rounded-full bg-violet-500/15 text-violet-400 font-medium">Word</span>
              </div>
              <CardTitle className="text-lg group-hover:text-violet-400 transition-colors">
                Loiseau Generator
              </CardTitle>
              <CardDescription>
                Générateur de documents Word avec mise en page professionnelle style &quot;Loiseau&quot;.
                Créez des cours, exercices et évaluations avec un rendu imprimable soigné —
                directement depuis votre navigateur.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex flex-wrap gap-1.5">
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Word .docx</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Mise en page pro</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Hors ligne</span>
              </div>
              <div className="flex gap-2">
                <AddToCartButton
                  item={{ id: 'loiseau-generator', name: 'Loiseau Generator', type: 'logiciel', path: 'logiciels-enseignant/debutant/loiseau-generator', description: 'Generateur Word mise en page pro' }}
                  className="flex-1"
                />
              </div>
              <p className="text-xs text-muted-foreground">
                Inclut une <Link href="/download/logiciels-enseignant/debutant/loiseau-generator/fiche_technique_ia_word.pdf" className="text-violet-400 hover:underline">fiche technique PDF</Link>
              </p>
            </CardContent>
          </Card>

          {/* H5P / Moodle Generator */}
          <Card className="glass-card border-2 border-emerald-500/20 hover:border-emerald-500/40 transition-all duration-300 group">
            <CardHeader>
              <div className="flex items-start justify-between mb-2">
                <div className="w-11 h-11 rounded-lg bg-gradient-to-br from-emerald-500 to-teal-600 flex items-center justify-center">
                  <Puzzle className="w-5 h-5 text-white" />
                </div>
                <span className="text-xs px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-medium">H5P</span>
              </div>
              <CardTitle className="text-lg group-hover:text-emerald-400 transition-colors">
                Générateur H5P / Moodle
              </CardTitle>
              <CardDescription>
                Créez des contenus interactifs H5P (QCM, glisser-déposer, textes à trous...)
                exportables directement dans Moodle ou tout LMS compatible.
                Interface visuelle, aucune connaissance technique requise.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex flex-wrap gap-1.5">
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">H5P interactif</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Export Moodle</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Hors ligne</span>
              </div>
              <AddToCartButton
                item={{ id: 'h5p-generator', name: 'Générateur H5P/Moodle', type: 'logiciel', path: 'logiciels-enseignant/debutant/h5p-moodle', description: 'Contenus interactifs H5P exportables Moodle' }}
                className="w-full"
              />
            </CardContent>
          </Card>

          {/* Stats DataGouv */}
          <Card className="glass-card border-2 border-amber-500/20 hover:border-amber-500/40 transition-all duration-300 group">
            <CardHeader>
              <div className="flex items-start justify-between mb-2">
                <div className="w-11 h-11 rounded-lg bg-gradient-to-br from-amber-500 to-orange-600 flex items-center justify-center">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <span className="text-xs px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 font-medium">Stats</span>
              </div>
              <CardTitle className="text-lg group-hover:text-amber-400 transition-colors">
                Stats DataGouv
              </CardTitle>
              <CardDescription>
                Générateur d&apos;exercices de statistiques à partir de données réelles
                issues de data.gouv.fr. Donnez du sens aux maths avec des données
                authentiques (démographie, environnement, économie...).
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex flex-wrap gap-1.5">
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Données réelles</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">data.gouv.fr</span>
                <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400">Hors ligne</span>
              </div>
              <AddToCartButton
                item={{ id: 'stats-datagouv', name: 'Stats DataGouv', type: 'logiciel', path: 'logiciels-enseignant/debutant/stats-datagouv', description: 'Exercices stats avec donnees reelles data.gouv.fr' }}
                className="w-full"
              />
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Catégories de logiciels */}
      <section className="space-y-4">
        <h2 className="text-2xl font-bold">Catégories de logiciels disponibles</h2>
        <p className="text-muted-foreground">
          Le dépôt BFtools contient plusieurs catégories d'outils pour répondre à vos besoins quotidiens :
        </p>
        <div className="grid md:grid-cols-2 gap-4">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-nebula-400" />
                Outils de préparation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Générateurs de fiches, création automatique de documents, modèles personnalisables
                pour vos cours et évaluations.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5 text-nebula-400" />
                Outils d'automatisation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Scripts pour automatiser les tâches répétitives, conversion de formats,
                traitement par lots de documents.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Wrench className="w-5 h-5 text-nebula-400" />
                Outils de gestion
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Organisation des progressions, planification de séquences, gestion
                des ressources pédagogiques.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-nebula-400" />
                Outils spécialisés
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Intégration avec les programmes officiels, génération d'exercices,
                outils spécifiques aux mathématiques.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
