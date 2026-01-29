import Link from "next/link"
import {
  Terminal,
  Zap,
  BookOpen,
  CheckCircle,
  AlertCircle,
  Download,
  Play,
  CreditCard,
  Settings,
  Code2,
  ArrowRight,
  ExternalLink,
  Package,
  KeyRound,
  HelpCircle,
  Sparkles,
  DollarSign,
  CheckCircle2,
  XCircle
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { CodeBlock } from "@/components/ui/code-block"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Installation de Claude Code | Tutoriels",
  description:
    "Guide complet pour installer et configurer Claude Code. Découvrez comment choisir votre abonnement, installer le CLI et commencer à utiliser Claude Code pour l'enseignement.",
}

export default function ClaudeCodeInstallPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="claude-code-install" title="Installation de Claude Code" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Installation", href: "/claude-code/tutorials/claude-code-install" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Terminal className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Installation de Claude Code
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Tout ce qu'il faut savoir pour installer et configurer Claude Code en quelques minutes
        </p>
      </section>

      {/* Qu'est-ce que Claude Code ? */}
      <section className="glass-card rounded-xl p-8 space-y-4">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Qu'est-ce que Claude Code ?</h2>
        </div>

        <p className="text-muted-foreground">
          Claude Code est l'assistant IA développé par Anthropic, accessible via une interface en ligne de commande (CLI)
          ou via l'application Claude Desktop. C'est un outil puissant pour automatiser la création de code, documents LaTeX,
          applications éducatives et bien plus.
        </p>
      </section>

      {/* Disclaimer - Alternative Gemini CLI */}
      <section className="glass-card rounded-xl p-8 space-y-4 border-2 border-blue-500/30 bg-blue-950/20">
        <div className="flex items-start gap-4">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0">
            <AlertCircle className="w-5 h-5 text-white" />
          </div>
          <div className="space-y-3">
            <h2 className="text-2xl font-bold text-blue-300">Alternative : Gemini CLI</h2>
            <p className="text-muted-foreground">
              <strong className="text-foreground">Important :</strong> Claude Code n'est pas la seule option disponible.
              Vous pouvez remplacer l'ensemble de cette configuration par un setup avec <strong className="text-blue-300">Gemini CLI</strong>
              de Google, qui offre des fonctionnalités similaires avec quelques différences mineures.
            </p>

            <div className="space-y-2 mt-4">
              <h3 className="font-semibold text-blue-300">Pourquoi Gemini CLI ?</h3>
              <ul className="space-y-2 text-sm text-muted-foreground ml-4">
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                  <span>Fonctionnalités équivalentes à Claude Code pour la génération de documents</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                  <span>Intégration native avec l'écosystème Google (Drive, Docs, etc.)</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                  <span>Tarification potentiellement différente (à vérifier selon vos besoins)</span>
                </li>
                <li className="flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <span className="text-amber-300">Quelques retards possibles sur les toutes dernières fonctionnalités par rapport à Claude</span>
                </li>
              </ul>
            </div>

            <div className="mt-6 p-4 bg-blue-950/40 border border-blue-800 rounded-lg">
              <p className="text-sm text-muted-foreground">
                <strong className="text-blue-300">Note :</strong> Ce tutoriel se concentre sur Claude Code car c'est l'outil que j'utilise
                personnellement pour éviter de changer d'outil régulièrement. Cependant, vous êtes libre de choisir l'alternative
                qui correspond le mieux à vos besoins et à votre budget. Les concepts et méthodes présentés ici sont
                transposables à d'autres CLI d'IA.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Comparatif Tarifs */}
      <section className="space-y-6">
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
              <CreditCard className="w-5 h-5 text-white" />
            </div>
            <h2 className="text-3xl font-bold">Comparatif des tarifs</h2>
          </div>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Claude (Anthropic) vs Gemini (Google)
          </p>
          <p className="text-muted-foreground max-w-3xl mx-auto">
            Comparaison des plans d'abonnement pour utiliser les CLI d'IA dans votre terminal
          </p>
        </div>

        {/* Tableau comparatif */}
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Claude (Anthropic) */}
          <div className="glass-card rounded-xl p-6 border-2 border-cosmic-500/30">
            <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Sparkles className="w-6 h-6 text-cosmic-400" />
              Claude (Anthropic)
            </h3>

            <div className="space-y-3">
              {/* Plan Free */}
              <div className="p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
                <h4 className="font-semibold mb-2">Plan Free</h4>
                <p className="text-xl font-bold text-foreground mb-2">Gratuit</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-cosmic-400 flex-shrink-0 mt-0.5" />
                    <span>Accès limité aux modèles</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-cosmic-400 flex-shrink-0 mt-0.5" />
                    <span>Pour tester le CLI</span>
                  </li>
                </ul>
              </div>

              {/* Plan Pro - RECOMMANDÉ */}
              <div className="p-4 rounded-lg bg-emerald-950/30 border-2 border-emerald-500 relative">
                <div className="absolute -top-2 -right-2 bg-emerald-500 text-white px-2 py-0.5 text-xs font-bold rounded">
                  RECOMMANDÉ
                </div>
                <h4 className="font-semibold mb-2 text-emerald-300">Plan Pro</h4>
                <p className="text-xl font-bold text-foreground mb-2">~20€/mois</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>5× les usages du plan Free</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span>Accès prioritaire aux modèles</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <span className="font-semibold text-emerald-300">Parfait pour l'enseignement</span>
                  </li>
                </ul>
              </div>

              {/* Note */}
              <div className="p-3 bg-cosmic-950/50 border border-cosmic-800 rounded text-xs text-muted-foreground">
                <strong className="text-foreground">Note :</strong> Pas besoin de l'API pour utiliser Claude Code.
                Le plan Pro suffit pour créer vos ressources pédagogiques.
              </div>
            </div>
          </div>

          {/* Gemini (Google) */}
          <div className="glass-card rounded-xl p-6 border-2 border-blue-500/30">
            <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Code2 className="w-6 h-6 text-blue-400" />
              Gemini (Google)
            </h3>

            <div className="space-y-3">
              {/* Plan Gratuit */}
              <div className="p-4 rounded-lg bg-blue-950/30 border border-blue-800">
                <h4 className="font-semibold mb-2">Plan Gratuit</h4>
                <p className="text-xl font-bold text-foreground mb-2">Gratuit</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Accès limité à certains modèles</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Jetons d'entrée/sortie sans frais</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Accès à Google AI Studio</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <AlertCircle className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                    <span className="text-amber-300">Données utilisées pour améliorer les produits</span>
                  </li>
                </ul>
              </div>

              {/* Plan Payant */}
              <div className="p-4 rounded-lg bg-blue-950/30 border border-blue-800">
                <h4 className="font-semibold mb-2 text-blue-300">Plan Payant (API)</h4>
                <p className="text-xl font-bold text-foreground mb-2">À l'usage</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Limites de débit plus élevées</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>API Batch (réduction -50%)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Modèles avancés (Gemini 2.5 Pro, 2.0 Flash)</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-blue-400 flex-shrink-0 mt-0.5" />
                    <span>Données NON utilisées pour améliorer</span>
                  </li>
                </ul>
                <div className="mt-3 p-2 bg-blue-950/50 rounded text-xs">
                  <p className="font-semibold text-blue-300 mb-1">Exemples de tarifs :</p>
                  <p className="text-muted-foreground">• Gemini 2.0 Flash : $0.30 entrée / $2.50 sortie par 1M tokens</p>
                  <p className="text-muted-foreground">• Gemini 2.5 Pro : $1.25-$2.50 entrée / $10-$15 sortie par 1M tokens</p>
                </div>
              </div>

              {/* Note */}
              <div className="p-3 bg-blue-950/50 border border-blue-800 rounded text-xs text-muted-foreground">
                <strong className="text-foreground">Note :</strong> Le plan gratuit peut suffire pour débuter.
                Tarification au paiement à l'utilisation pour la production.
              </div>
            </div>
          </div>

          {/* OpenAI Codex */}
          <div className="glass-card rounded-xl p-6 border-2 border-purple-500/30">
            <h3 className="text-2xl font-bold mb-4 flex items-center gap-2">
              <Terminal className="w-6 h-6 text-purple-400" />
              OpenAI Codex
            </h3>

            <div className="space-y-3">
              {/* Plan Plus */}
              <div className="p-4 rounded-lg bg-purple-950/30 border border-purple-800">
                <h4 className="font-semibold mb-2">ChatGPT Plus</h4>
                <p className="text-xl font-bold text-foreground mb-2">~20$/mois</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>Codex inclus dans l'abonnement</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>30-150 messages locaux / 5h</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>5-40 tâches cloud / 5h</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>Limite hebdomadaire partagée</span>
                  </li>
                </ul>
              </div>

              {/* Plan Pro */}
              <div className="p-4 rounded-lg bg-purple-950/30 border border-purple-800">
                <h4 className="font-semibold mb-2 text-purple-300">ChatGPT Pro</h4>
                <p className="text-xl font-bold text-foreground mb-2">Prix supérieur</p>
                <ul className="space-y-1 text-sm text-muted-foreground">
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>300-1500 messages locaux / 5h</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>50-400 tâches cloud / 5h</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <CheckCircle className="w-4 h-4 text-purple-400 flex-shrink-0 mt-0.5" />
                    <span>Pour usage intensif toute la journée</span>
                  </li>
                </ul>
              </div>

              {/* Option API */}
              <div className="p-4 rounded-lg bg-purple-950/30 border border-purple-800">
                <h4 className="font-semibold mb-2 text-purple-300">Extension via API</h4>
                <p className="text-sm text-muted-foreground mb-2">
                  Possibilité d'utiliser une clé API OpenAI pour étendre l'usage local (CLI et IDE).
                  Tarification aux tarifs standards de l'API OpenAI.
                </p>
              </div>

              {/* Note */}
              <div className="p-3 bg-purple-950/50 border border-purple-800 rounded text-xs text-muted-foreground">
                <strong className="text-foreground">Note :</strong> Codex spécialisé pour le code.
                Business/Enterprise : plans avec crédits flexibles disponibles.
              </div>
            </div>
          </div>
        </div>

        {/* Disclaimer Codex */}
        <div className="glass-card rounded-xl p-4 border border-purple-500/30 bg-purple-950/10">
          <p className="text-sm text-muted-foreground">
            <strong className="text-purple-300">Note sur OpenAI Codex :</strong> Ajouté ici uniquement pour comparatif.
            Je ne l'utilise pas personnellement, mais il peut être une alternative intéressante pour certains utilisateurs,
            notamment ceux déjà abonnés à ChatGPT Plus.
          </p>
        </div>

        {/* Recommandation finale */}
        <div className="glass-card rounded-xl p-6 border border-emerald-500/30 bg-emerald-950/20">
          <div className="flex gap-3">
            <AlertCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
            <div className="space-y-3">
              <div>
                <h3 className="font-semibold text-emerald-300 mb-1">Recommandation pour l'enseignement</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  <strong className="text-emerald-300">Claude Pro (~20€/mois)</strong> : Simple, fixe, parfait pour créer des ressources pédagogiques sans se soucier de la consommation.
                </p>
                <p className="text-sm text-muted-foreground mb-2">
                  <strong className="text-blue-300">Gemini Gratuit/Payant</strong> : Alternative intéressante avec plan gratuit généreux.
                  Le plan payant à l'usage peut être économique selon votre utilisation.
                </p>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-purple-300">OpenAI Codex (ChatGPT Plus ~20$/mois)</strong> : Bonne option si vous êtes déjà abonné à ChatGPT Plus.
                  Spécialisé pour le code avec limites de messages par période.
                </p>
              </div>

              <div>
                <h3 className="font-semibold text-emerald-300 mb-1">Pourquoi je partage Claude Code</h3>
                <p className="text-sm text-muted-foreground mb-2">
                  <strong className="text-foreground">Aucune solution n'est parfaite.</strong> Je partage simplement ma façon de faire
                  avec Claude Code car je suis personnellement plus à l'aise avec cet outil :
                </p>
                <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-4">
                  <li>Plus transparent dans son fonctionnement</li>
                  <li>Plus pragmatique pour mes besoins d'enseignement</li>
                  <li>Documentation claire et accessible</li>
                </ul>
                <p className="text-sm text-muted-foreground mt-2">
                  Mais vous êtes libre de choisir Gemini CLI ou d'autres alternatives selon vos préférences.
                  Les concepts et méthodes présentés dans ce tutoriel sont transposables à d'autres outils CLI d'IA.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Installation */}
      <section className="space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Download className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-3xl font-bold">Installation</h2>
        </div>

        {/* Prérequis */}
        <div className="glass-card rounded-xl p-6">
          <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
            <Package className="w-5 h-5 text-cosmic-400" />
            Prérequis
          </h3>

          {/* Note importante : Node.js plus obligatoire */}
          <div className="mb-4 p-4 bg-emerald-950/30 border-2 border-emerald-500/50 rounded-lg">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-semibold text-emerald-300 mb-1">Bonne nouvelle ! Node.js n'est plus obligatoire</p>
                <p className="text-sm text-muted-foreground">
                  Depuis les dernières mises à jour, Claude Code propose une <strong className="text-foreground">installation native</strong> qui
                  ne nécessite plus Node.js. L'installation via npm est désormais <strong className="text-amber-300">dépréciée</strong>.
                </p>
              </div>
            </div>
          </div>

          <div className="mb-4 p-4 bg-blue-950/30 border border-blue-800 rounded-lg">
            <p className="text-sm text-muted-foreground">
              <strong className="text-blue-300">Pourquoi installer Node.js et Python quand même ?</strong> Ces environnements
              restent très utiles pour exploiter pleinement les fonctionnalités avancées (serveurs MCP, scripts personnalisés,
              fonctionnalités graphiques et d'IA). Si vous débutez, vous pouvez les installer plus tard.
            </p>
          </div>

          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-semibold">Un compte Anthropic/Claude</p>
                <p className="text-sm text-muted-foreground">Avec un abonnement actif (Pro recommandé à ~20€/mois)</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-950/30 border border-slate-700/50">
              <CheckCircle className="w-5 h-5 text-slate-400 mt-0.5 flex-shrink-0" />
              <div className="flex-1">
                <p className="font-semibold text-slate-300">Node.js (version 18+) — <span className="text-amber-400 text-sm">Optionnel</span></p>
                <p className="text-sm text-muted-foreground mb-2">
                  Plus requis pour l'installation native. Utile pour les serveurs MCP et certains outils avancés.
                </p>
                <Button asChild variant="outline" size="sm">
                  <Link href="/claude-code/tutorials/nodejs-install" className="flex items-center gap-2" prefetch={false}>
                    <Download className="w-4 h-4" />
                    Tutoriel d'installation de Node.js
                  </Link>
                </Button>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 rounded-lg bg-slate-950/30 border border-slate-700/50">
              <CheckCircle className="w-5 h-5 text-slate-400 mt-0.5 flex-shrink-0" />
              <div className="flex-1">
                <p className="font-semibold text-slate-300">Python x64 (version 3.8+) — <span className="text-amber-400 text-sm">Optionnel</span></p>
                <p className="text-sm text-muted-foreground mb-2">
                  Utile pour les fonctionnalités graphiques, IA et certains scripts avancés.
                </p>
                <Button asChild variant="outline" size="sm">
                  <Link href="/claude-code/tutorials/python-install" className="flex items-center gap-2" prefetch={false}>
                    <Download className="w-4 h-4" />
                    Tutoriel d'installation de Python x64
                  </Link>
                </Button>
              </div>
            </div>

            <div className="flex items-start gap-3">
              <CheckCircle className="w-5 h-5 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <div>
                <p className="font-semibold">Un terminal</p>
                <p className="text-sm text-muted-foreground">PowerShell, cmd, bash, etc.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Étapes d'installation */}
        <div className="space-y-4">
          <h3 className="text-xl font-bold">Étapes d'installation</h3>

          {/* Étape 1 */}
          <div className="glass-card rounded-xl p-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg">
                1
              </div>
              <div className="flex-1 space-y-4">
                <div>
                  <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                    <KeyRound className="w-5 h-5 text-cosmic-400" />
                    Créer un compte Claude
                  </h4>
                  <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-4">
                    <li>Allez sur <a href="https://claude.ai" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline inline-flex items-center gap-1">
                      https://claude.ai <ExternalLink className="w-3 h-3" />
                    </a></li>
                    <li>Créez un compte ou connectez-vous</li>
                    <li>Souscrivez à l'abonnement Mini (20€/mois)</li>
                  </ol>
                </div>
              </div>
            </div>
          </div>

          {/* Étape 2 */}
          <div className="glass-card rounded-xl p-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg">
                2
              </div>
              <div className="flex-1 space-y-4">
                <div>
                  <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                    <Terminal className="w-5 h-5 text-cosmic-400" />
                    Installer Claude Code
                  </h4>
                  <p className="text-sm text-muted-foreground mb-3">
                    Choisissez la méthode d'installation adaptée à votre système :
                  </p>

                  <div className="space-y-4">
                    {/* macOS / Linux / WSL */}
                    <div className="p-4 bg-slate-950/50 rounded-lg border border-slate-800">
                      <p className="text-sm font-semibold text-cosmic-300 mb-2">macOS / Linux / WSL :</p>
                      <CodeBlock code="curl -fsSL https://claude.ai/install.sh | bash" language="bash" />
                    </div>

                    {/* Windows PowerShell */}
                    <div className="p-4 bg-slate-950/50 rounded-lg border border-slate-800">
                      <p className="text-sm font-semibold text-cosmic-300 mb-2">Windows PowerShell :</p>
                      <CodeBlock code="irm https://claude.ai/install.ps1 | iex" language="powershell" />
                    </div>

                    {/* Windows CMD */}
                    <div className="p-4 bg-slate-950/50 rounded-lg border border-slate-800">
                      <p className="text-sm font-semibold text-cosmic-300 mb-2">Windows CMD :</p>
                      <CodeBlock code="curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd" language="batch" />
                    </div>
                  </div>

                  <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-3 mt-4">
                    <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-emerald-300">
                      Les installations natives se mettent à jour automatiquement en arrière-plan.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Étape 3 */}
          <div className="glass-card rounded-xl p-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg">
                3
              </div>
              <div className="flex-1 space-y-4">
                <div>
                  <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                    <KeyRound className="w-5 h-5 text-cosmic-400" />
                    Authentification
                  </h4>
                  <p className="text-sm text-muted-foreground mb-3">
                    Lors du premier appel de claude, vous devrez vous identifier et choisir votre mode de facturation :
                  </p>

                  <CodeBlock code="claude" language="bash" />
                  <p className="text-sm text-muted-foreground mt-3">
                    Choisir le mode de facturation qui utilise votre abonnement.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Étape 4 */}
          <div className="glass-card rounded-xl p-6">
            <div className="flex gap-4">
              <div className="flex-shrink-0 w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold text-lg">
                4
              </div>
              <div className="flex-1 space-y-4">
                <div>
                  <h4 className="text-lg font-semibold mb-2 flex items-center gap-2">
                    <CheckCircle className="w-5 h-5 text-emerald-400" />
                    Vérifier l'installation
                  </h4>
                  <p className="text-sm text-muted-foreground mb-3">
                    Testez que tout fonctionne :
                  </p>

                  <CodeBlock code="claude --version" language="bash" />

                  <div className="flex items-start gap-2 bg-emerald-950/30 border border-emerald-800 rounded-lg p-3 mt-3">
                    <CheckCircle className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
                    <p className="text-sm text-emerald-300">
                      Si vous voyez le numéro de version, c'est bon !
                    </p>
                  </div>

                  <div className="mt-4 p-3 bg-cosmic-950/30 border border-cosmic-800 rounded-lg">
                    <p className="text-sm text-muted-foreground">
                      <strong className="text-cosmic-300">Documentation officielle :</strong>{" "}
                      <a href="https://code.claude.com/docs/" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline inline-flex items-center gap-1">
                        code.claude.com/docs <ExternalLink className="w-3 h-3" />
                      </a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Première utilisation */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Play className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Première utilisation</h2>
        </div>

        <div className="space-y-4">
          <div>
            <h3 className="text-lg font-semibold mb-2">Lancer Claude Code</h3>
            <p className="text-sm text-muted-foreground mb-3">
              Dans votre terminal, naviguez vers votre dossier de travail et lancez :
            </p>
            <CodeBlock code="claude" language="bash" />
            <p className="text-sm text-muted-foreground mt-3">
              Vous pouvez maintenant dialoguer avec Claude directement dans votre terminal !
            </p>
          </div>

          <div className="border-t border-border pt-4">
            <h3 className="text-lg font-semibold mb-2">Exemple d'utilisation</h3>
            <div className="bg-slate-950 rounded-lg p-4 font-mono text-sm border border-slate-800 space-y-2">
              <div>
                <span className="text-cosmic-300">claude</span> # Ouvre une instance claude dans le terminal du dossier.
              </div>
              <div className="text-muted-foreground">
                <span className="text-cosmic-300">/init</span> # Commande d'initialisation.
              </div>
              <div className="text-muted-foreground italic">
                [Claude analyse vos sources présentes dans le répertoire d'appel et prépare un fichier CLAUDE.md]
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Personnaliser */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-nebula-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Personnalisation avec mes outils</h2>
        </div>

        <div className="space-y-4">
          <p className="text-muted-foreground">
            Une fois Claude Code installé, vous pouvez le configurer avec mes outils personnalisés
            (agents, skills, commandes) pour automatiser la création de vos ressources pédagogiques.
          </p>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-nebula-950/30 border border-nebula-800">
            <Settings className="w-5 h-5 text-nebula-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1">Configuration de Claude Code</h4>
              <p className="text-sm text-muted-foreground mb-3">
                Téléchargez et installez mes configurations personnalisées pour profiter des agents,
                skills et commandes spécialisés pour l'enseignement.
              </p>
              <Button asChild variant="nebula" size="sm">
                <Link href="/claude-code/tutorials/claude-code-config" className="flex items-center gap-2" prefetch={false}>
                  <ArrowRight className="w-4 h-4" />
                  Voir le tutoriel de configuration
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Documentation</h2>
        </div>

        <div className="space-y-4">
          <h3 className="text-lg font-semibold">Ressources officielles</h3>

          <div className="grid md:grid-cols-3 gap-4">
            <a
              href="https://code.claude.com/docs/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
            >
              <BookOpen className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                  Documentation Claude Code
                  <ExternalLink className="w-3 h-3" />
                </h4>
                <p className="text-xs text-muted-foreground">
                  Référence officielle
                </p>
              </div>
            </a>

            <a
              href="https://docs.anthropic.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
            >
              <Code2 className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                  Documentation Anthropic
                  <ExternalLink className="w-3 h-3" />
                </h4>
                <p className="text-xs text-muted-foreground">
                  API et ressources
                </p>
              </div>
            </a>

            <a
              href="https://www.anthropic.com/learn"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800 hover:border-cosmic-600 hover:scale-105 transition-all group"
            >
              <Sparkles className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-semibold mb-1 group-hover:text-cosmic-400 transition-colors flex items-center gap-1">
                  Tutoriels Anthropic
                  <ExternalLink className="w-3 h-3" />
                </h4>
                <p className="text-xs text-muted-foreground">
                  Guides d'apprentissage
                </p>
              </div>
            </a>
          </div>
        </div>

        <div className="border-t border-border pt-4">
          <h3 className="text-lg font-semibold mb-3">Bonnes pratiques</h3>
          <div className="space-y-2">
            <div className="flex items-start gap-2">
              <ArrowRight className="w-4 h-4 text-cosmic-400 mt-1 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Soyez précis</strong> : Plus votre demande est détaillée, meilleur sera le résultat
              </p>
            </div>
            <div className="flex items-start gap-2">
              <ArrowRight className="w-4 h-4 text-cosmic-400 mt-1 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Itérez</strong> : N'hésitez pas à demander des modifications
              </p>
            </div>
            <div className="flex items-start gap-2">
              <ArrowRight className="w-4 h-4 text-cosmic-400 mt-1 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Utilisez les agents</strong> : Profitez du système d'agents pour des tâches complexes
              </p>
            </div>
            <div className="flex items-start gap-2">
              <ArrowRight className="w-4 h-4 text-cosmic-400 mt-1 flex-shrink-0" />
              <p className="text-sm text-muted-foreground">
                <strong className="text-foreground">Consultez la doc</strong> : La documentation officielle est excellente
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Commandes utiles */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <Terminal className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Commandes utiles</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Lancer Claude Code</p>
            <CodeBlock code="claude" language="bash" />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Voir l'aide</p>
            <CodeBlock code="claude --help" language="bash" />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Vérifier la version</p>
            <CodeBlock code="claude --version" language="bash" />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Vérifier l'installation</p>
            <CodeBlock code="claude doctor" language="bash" />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Se déconnecter</p>
            <CodeBlock code="claude logout" language="bash" />
          </div>

          <div className="space-y-2">
            <p className="text-sm font-semibold text-cosmic-300">Mettre à jour (si installé via npm)</p>
            <CodeBlock code="npm update -g @anthropic-ai/claude-code" language="bash" />
          </div>
        </div>
      </section>

      {/* Configuration avancée */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Configuration avancée</h2>
        </div>

        <div>
          <h3 className="text-lg font-semibold mb-3">Fichier .claude</h3>
          <p className="text-muted-foreground mb-4">
            Dans votre dossier de travail, vous pouvez créer un dossier <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">.claude/</code> pour :
          </p>

          <div className="grid md:grid-cols-2 gap-3">
            <div className="flex items-start gap-2 text-sm">
              <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <span className="text-muted-foreground">Configurer des agents personnalisés</span>
            </div>
            <div className="flex items-start gap-2 text-sm">
              <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <span className="text-muted-foreground">Définir des skills spécialisés</span>
            </div>
            <div className="flex items-start gap-2 text-sm">
              <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <span className="text-muted-foreground">Ajouter des commandes custom</span>
            </div>
            <div className="flex items-start gap-2 text-sm">
              <CheckCircle className="w-4 h-4 text-cosmic-400 mt-0.5 flex-shrink-0" />
              <span className="text-muted-foreground">Configurer des serveurs MCP</span>
            </div>
          </div>

          <div className="mt-4 p-4 bg-nebula-950/30 border border-nebula-800 rounded-lg">
            <p className="text-sm text-muted-foreground">
              Nous verrons cela dans les tutoriels avancés !
            </p>
          </div>
        </div>
      </section>

      {/* Dépannage */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-amber-600 flex items-center justify-center">
            <HelpCircle className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Dépannage</h2>
        </div>

        <div className="space-y-4">
          {/* Problème 1 */}
          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <XCircle className="w-5 h-5 text-amber-400" />
              Problèmes d'authentification
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Vérifiez que votre abonnement est actif</li>
              <li>Essayez de vous déconnecter puis reconnecter :
                <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300 ml-1">claude logout</code> puis relancez
                <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300 ml-1">claude</code>
              </li>
            </ul>
          </div>

          {/* Problème 2 */}
          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <XCircle className="w-5 h-5 text-amber-400" />
              Commande non trouvée
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Redémarrez votre terminal après l'installation</li>
              <li>Vérifiez l'installation : <code className="px-2 py-1 bg-slate-900 rounded text-cosmic-300">claude doctor</code></li>
              <li>Réinstallez avec la méthode native (voir étape 2 ci-dessus)</li>
            </ul>
          </div>

          {/* Problème 3 */}
          <div className="border border-border rounded-lg p-4">
            <h3 className="font-semibold mb-2 flex items-center gap-2">
              <XCircle className="w-5 h-5 text-amber-400" />
              Erreurs de génération
            </h3>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground ml-6">
              <li>Soyez plus précis dans vos demandes</li>
              <li>Vérifiez que vous avez des tokens disponibles</li>
              <li>Consultez la documentation : <a href="https://code.claude.com/docs/" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline">code.claude.com/docs</a></li>
            </ul>
          </div>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-cosmic-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        </div>

        <p className="text-muted-foreground">
          Une fois Claude Code installé, vous pouvez :
        </p>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <Code2 className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1">Générer des documents LaTeX</h4>
              <p className="text-sm text-muted-foreground">
                Avec le package bfcours pour vos cours
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <BookOpen className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1">Créer des présentations</h4>
              <p className="text-sm text-muted-foreground">
                Reveal.js interactives pour vos élèves
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <Settings className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1">Configurer vos agents</h4>
              <p className="text-sm text-muted-foreground">
                Personnalisés pour vos besoins
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-cosmic-950/30 border border-cosmic-800">
            <KeyRound className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="font-semibold mb-1">Ajouter une clé API Google</h4>
              <p className="text-sm text-muted-foreground">
                Pour la génération d'images
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-3 pt-4">
          <Button asChild variant="cosmic" size="lg">
            <Link href="/claude-code/presentations" prefetch={false}>
              Explorer les présentations
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/claude-code/downloads" prefetch={false}>
              Télécharger les configurations
            </Link>
          </Button>
        </div>
      </section>
    </div>
  )
}
