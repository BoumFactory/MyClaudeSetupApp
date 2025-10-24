import { User, Code2, GraduationCap, Sparkles, Rocket, Brain } from "lucide-react"
import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Qui suis-je ? - IA & Enseignement",
  description:
    "Un prof de maths qui code des trucs... avec un peu d'aide artificielle à l'intelligence !",
}

export default function AboutPage() {
  return (
    <div className="space-y-12">
      <Breadcrumb
        items={[
          { label: "Accueil", href: "/" },
          { label: "Qui suis-je ?", href: "/about" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <User className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Qui suis-je ?
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Un prof de maths qui code des trucs... avec un peu d'aide artificielle à l'intelligence !
        </p>
      </section>

      {/* Histoire */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <GraduationCap className="w-6 h-6 text-cosmic-400" />
          <h2 className="text-2xl font-bold">De la craie au code</h2>
        </div>

        <div className="space-y-4 text-muted-foreground">
          <p>
            Je suis professeur de mathématiques, et comme beaucoup d'enseignants, je passe beaucoup de temps
            à chercher la meilleure façon de créer mes ressources pédagogiques. 
          </p>
          <p>
            LaTeX pour les documents, outils numériques pour simplifier... Le quotidien classique d'un
            prof organisé (ou qui essaie de l'être) !
          </p>

          <p>
            J'ai découvert les possibilités de l'intelligence artificielle comme beaucoup à la sortie de ChatGPT.
          </p>
          <p>            J'écrivais des macros pour autoformater des documents dans LibreOffice.
          </p>
          <p>            Rapidement, le langage LaTeX s'est avéré plus performant.
          </p>

          <p>
            Mes contacts avec la programmation ont été marqués par :
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Des documents LaTeX produits dans le cadre de mes études de mathématiques.</li>
            <li>Un été passé à l'apprentissage du C++. Cela s'est avéré salvateur des années plus tard.</li>
          </ul>
        </div>
      </section>

      {/* La méthode */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="w-6 h-6 text-nebula-400" />
          <h2 className="text-2xl font-bold">L'IA comme professeur de code</h2>
        </div>

        <div className="space-y-4 text-muted-foreground">
          <p>
            Grâce à <span className="font-semibold text-cosmic-400">outils IA</span> et d'autres
            , j'ai pu apprendre la programmation <span className="font-semibold text-cosmic-400">en contexte</span>.
            Pas besoin de passer des mois sur des tutoriels abstraits, j'ai déjà un projet clair : des outils pour faciliter mon quotidien.
          </p>
          <p>
            Il suffit de se concentrer sur des projets qui correspondent à mes compétences techniques. 
            On applique en fait un des principes de l'apprentissage du code : <span className="font-semibold text-cosmic-400">pratiquer</span>. 
          </p>
          <p>
            Je dois pouvoir comprendre les technologies sur lesquelles je travaille pour pouvoir guider les agents IA. 

            Je dois également prendre en compte leurs capacités.
          </p>
          <p>
            Protocole :
          </p>
          <ul className="list-disc list-inside space-y-2 ml-4">
            <li>Je choisis un projet qui me paraît réalisable. Cela évolue avec la qualité des modèles et de mes compétences.</li>
            <li>Je demande à un agent, et j'obtiens du code que je dois rendre fonctionnel.</li>
            <li>Je précise mes attentes si cela ne me convient pas.</li>
            <li>On itère jusqu'à obtenir un résultat satisfaisant.</li>
          </ul>
          <p>
            C'est un peu comme avoir un collègue développeur disponible 24h/24 qui ne se moque jamais
            de vos questions de débutant. Pratique, non ?

            Pendant qu'il écrit du code, je me documente pour mieux pouvoir le conseiller.

            Cela m'a permis de changer plusieurs fois de plateforme d'accès à l'IA pour m'adapter aux fonctionnalités les plus récentes.
          </p>

          <p>
            <span className="font-semibold text-cosmic-400">Le temps gagné</span> est précieux. Il permet d'organiser ses idées, de se détendre. 
            Mais surtout, ce temps gagné peut être consacré à quelque chose de fondamental : <span className="font-semibold text-cosmic-400">prendre soin de ses proches</span>.
          </p>
          <p>
            La <span className="font-semibold text-cosmic-400">charge mentale</span> occasionnée par la production de documents est également <span className="font-semibold text-cosmic-400">extrêmement réduite</span>, ce qui ne fait qu'améliorer le temps passé avec vos proches.
          </p>
          <Card className="glass-card border-cosmic-700/50">
            <CardContent className="p-6">
              <p className="text-base italic text-muted-foreground">
                "Ce site web a été créé avec l'aide de Claude Code.

                Pendant ce temps, je préparais de délicieux feuilletés au fromage de chèvre avec ma compagne."
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Ce que je partage */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <Sparkles className="w-6 h-6 text-cosmic-400" />
          <h2 className="text-2xl font-bold">Ce que je partage ici</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <Card className="glass-card border-cosmic-700/30">
            <CardContent className="p-5 space-y-3">
              <div className="flex items-center gap-2">
                <Code2 className="w-5 h-5 text-cosmic-400" />
                <h3 className="font-semibold">Configurations & Setup</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Toutes mes configurations Claude Code, agents personnalisés, skills,
                et serveurs MCP pour automatiser la création de ressources pédagogiques.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-nebula-700/30">
            <CardContent className="p-5 space-y-3">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-nebula-400" />
                <h3 className="font-semibold">Applications éducatives</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Des applications interactives créées pour mes cours de maths,
                que vous pouvez utiliser directement ou adapter à vos besoins.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-cosmic-700/30">
            <CardContent className="p-5 space-y-3">
              <div className="flex items-center gap-2">
                <GraduationCap className="w-5 h-5 text-cosmic-400" />
                <h3 className="font-semibold">Packages LaTeX</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Mes packages LaTeX personnalisés pour créer des documents
                pédagogiques professionnels et cohérents.
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-nebula-700/30">
            <CardContent className="p-5 space-y-3">
              <div className="flex items-center gap-2">
                <Rocket className="w-5 h-5 text-nebula-400" />
                <h3 className="font-semibold">Tutoriels & Découvertes</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Mes expériences, mes réussites, mes galères (oui, il y en a eu !),
                et comment j'ai résolu les problèmes.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Philosophie */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <Rocket className="w-6 h-6 text-nebula-400" />
          <h2 className="text-2xl font-bold">Ma philosophie</h2>
        </div>

        <div className="space-y-4">
          <Card className="glass-card border-l-4 border-cosmic-500 bg-cosmic-900/20">
            <CardContent className="p-5">
              <p className="text-lg font-semibold text-cosmic-300 mb-2">
                L'IA n'est pas là pour remplacer les profs...
              </p>
              <p className="text-sm text-muted-foreground">
                ...mais pour nous donner des super-pouvoirs ! On peut enfin créer les outils
                qu'on imagine sans attendre qu'un éditeur les développe (ou qu'ils soient payants).
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-l-4 border-nebula-500 bg-nebula-900/20">
            <CardContent className="p-5">
              <p className="text-lg font-semibold text-nebula-300 mb-2">
                Partager, c'est multiplier les idées
              </p>
              <p className="text-sm text-muted-foreground">
                Si mes configurations ou mes outils peuvent faire gagner du temps à d'autres
                enseignants, alors tout ce travail en vaut doublement la peine. Et qui sait,
                peut-être que vous allez les améliorer et me donner de nouvelles idées !
              </p>
            </CardContent>
          </Card>

          <Card className="glass-card border-l-4 border-cosmic-500 bg-cosmic-900/20">
            <CardContent className="p-5">
              <p className="text-lg font-semibold text-cosmic-300 mb-2">
                On apprend mieux en créant
              </p>
              <p className="text-sm text-muted-foreground">
                Que ce soit pour mes élèves ou pour moi : la meilleure façon de comprendre,
                c'est de faire. L'IA permet de passer moins de temps sur la syntaxe et
                plus de temps sur la logique et la créativité.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  )
}
