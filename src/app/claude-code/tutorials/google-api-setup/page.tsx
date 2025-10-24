import Link from "next/link"
import {
  Image,
  Cloud,
  CreditCard,
  Key,
  Shield,
  AlertCircle,
  CheckCircle,
  DollarSign,
  FileText,
  Settings,
  Lock,
  CheckCircle2,
  XCircle,
  Bell,
  BarChart3,
  Sparkles,
  Zap,
  Palette,
} from "lucide-react"
import { Breadcrumb } from "@/components/layout/Breadcrumb"
import { TutorialTracker } from "@/components/analytics/PageTracker"
import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Configuration de l'API Google Imagen (Nanobanana) - Claude Code",
  description:
    "Guide complet pour configurer l'API Google Imagen avec Claude Code. Générez des images pour vos cours de mathématiques et documents pédagogiques.",
}

export default function GoogleApiSetupPage() {
  return (
    <div className="space-y-12">
      {/* Tracker analytics */}
      <TutorialTracker slug="google-api-setup" title="Configuration de l'API Google" />

      <Breadcrumb
        items={[
          { label: "Claude Code", href: "/claude-code" },
          { label: "Tutoriels", href: "/claude-code/tutorials" },
          { label: "Configuration API Google Imagen", href: "/claude-code/tutorials/google-api-setup" }
        ]}
      />

      {/* Header */}
      <section className="text-center space-y-4">
        <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl cosmic-gradient mb-4">
          <Image className="w-8 h-8 text-white" />
        </div>
        <h1 className="text-4xl md:text-5xl font-bold glow-text">
          Configuration de l'API Google Imagen
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Générez des images professionnelles pour vos cours avec l'API Imagen (nanobanana)
        </p>
      </section>

      {/* Qu'est-ce que l'API Imagen */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Qu'est-ce que l'API Imagen ?</h2>
        </div>

        <p className="text-muted-foreground leading-relaxed">
          L'API Google Imagen (code <code className="px-2 py-1 bg-muted rounded text-sm font-mono">nanobanana</code>)
          permet de générer des images à partir de descriptions textuelles. C'est un outil puissant pour créer des
          illustrations pour vos cours, fiches d'exercices, présentations, etc.
        </p>

        <div className="grid md:grid-cols-2 gap-4 mt-6">
          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-500/10 border border-cosmic-500/20">
            <Palette className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Illustrations pédagogiques</h3>
              <p className="text-sm text-muted-foreground">
                Générez des schémas, diagrammes, illustrations pour vos documents
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-500/10 border border-cosmic-500/20">
            <Zap className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Intégration parfaite</h3>
              <p className="text-sm text-muted-foreground">
                Claude Code peut automatiquement générer des images via l'API
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-500/10 border border-cosmic-500/20">
            <DollarSign className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Tarification flexible</h3>
              <p className="text-sm text-muted-foreground">
                Payez uniquement ce que vous utilisez
              </p>
            </div>
          </div>

          <div className="flex gap-3 p-4 rounded-lg bg-cosmic-500/10 border border-cosmic-500/20">
            <CheckCircle className="w-5 h-5 text-cosmic-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Qualité professionnelle</h3>
              <p className="text-sm text-muted-foreground">
                Images haute résolution adaptées à l'impression
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Prérequis */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold">Prérequis</h2>

        <div className="space-y-3">
          <div className="flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span className="text-muted-foreground">Un compte Google</span>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span className="text-muted-foreground">Une carte bancaire (pour activer la facturation Google Cloud)</span>
          </div>
          <div className="flex items-start gap-3">
            <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
            <span className="text-muted-foreground">Claude Code installé et configuré</span>
          </div>
        </div>
      </section>

      {/* Étape 1 : Créer un compte Google Cloud */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            1
          </div>
          <h2 className="text-2xl font-bold">Créer un compte Google Cloud</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Cloud className="w-5 h-5 text-cosmic-400" />
              1.1 Accéder à Google Cloud Console
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Allez sur <a href="https://console.cloud.google.com" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline">https://console.cloud.google.com</a></li>
              <li>Connectez-vous avec votre compte Google</li>
              <li>Acceptez les conditions d'utilisation</li>
            </ol>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <FileText className="w-5 h-5 text-cosmic-400" />
              1.2 Créer un nouveau projet
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Cliquez sur le sélecteur de projet en haut de la page</li>
              <li>Cliquez sur <strong className="text-foreground">"Nouveau projet"</strong></li>
              <li>Donnez un nom à votre projet (ex: "Claude-Images-Education")</li>
              <li>Cliquez sur <strong className="text-foreground">"Créer"</strong></li>
              <li>Attendez que le projet soit créé et sélectionnez-le</li>
            </ol>
          </div>
        </div>
      </section>

      {/* Étape 2 : Activer l'API */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            2
          </div>
          <h2 className="text-2xl font-bold">Activer l'API Google AI Studio</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Settings className="w-5 h-5 text-cosmic-400" />
              2.1 Accéder à Google AI Studio
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Allez sur <a href="https://aistudio.google.com" target="_blank" rel="noopener noreferrer" className="text-cosmic-400 hover:underline">https://aistudio.google.com</a></li>
              <li>Connectez-vous avec le même compte Google</li>
              <li>Sélectionnez le projet que vous venez de créer</li>
            </ol>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Image className="w-5 h-5 text-cosmic-400" />
              2.2 Activer l'API Imagen
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Dans Google AI Studio, cherchez <strong className="text-foreground">"Imagen"</strong></li>
              <li>Cliquez sur <strong className="text-foreground">"Activer"</strong> ou <strong className="text-foreground">"Enable"</strong></li>
              <li>Suivez les instructions pour activer l'API</li>
            </ol>
          </div>
        </div>
      </section>

      {/* Étape 3 : Configurer la facturation */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-yellow-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            3
          </div>
          <h2 className="text-2xl font-bold">Configurer la facturation</h2>
        </div>

        {/* Warning important */}
        <div className="bg-yellow-500/10 border-2 border-yellow-500/50 rounded-lg p-4 flex gap-3">
          <AlertCircle className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-yellow-500 mb-1">Important</h4>
            <p className="text-sm text-muted-foreground">
              Vous devez associer une carte bancaire pour utiliser l'API, mais vous ne serez facturé
              que pour ce que vous utilisez. Pour un usage éducatif raisonnable, le coût est très faible.
            </p>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <CreditCard className="w-5 h-5 text-cosmic-400" />
              3.1 Associer un moyen de paiement
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Dans Google Cloud Console, allez dans <strong className="text-foreground">"Facturation"</strong> (Billing)</li>
              <li>Cliquez sur <strong className="text-foreground">"Associer un compte de facturation"</strong></li>
              <li>Si vous n'avez pas de compte de facturation :
                <ul className="list-disc list-inside ml-6 mt-2 space-y-1">
                  <li>Cliquez sur <strong className="text-foreground">"Créer un compte de facturation"</strong></li>
                  <li>Entrez vos informations de carte bancaire</li>
                  <li>Validez</li>
                </ul>
              </li>
              <li>Associez ce compte de facturation à votre projet</li>
            </ol>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <DollarSign className="w-5 h-5 text-cosmic-400" />
              3.2 Tarification
            </h3>

            <div className="bg-muted/50 rounded-lg p-4 space-y-3">
              <p className="text-sm text-muted-foreground mb-3">
                <strong className="text-foreground">Tarifs indicatifs</strong> (vérifiez les tarifs actuels sur Google Cloud) :
              </p>

              <div className="grid md:grid-cols-2 gap-3">
                <div className="bg-background/50 rounded-lg p-3 border border-border">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">Standard</span>
                    <span className="text-lg font-bold text-cosmic-400">~0.02€</span>
                  </div>
                  <p className="text-xs text-muted-foreground">par image</p>
                </div>

                <div className="bg-background/50 rounded-lg p-3 border border-border">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm font-medium">Haute qualité</span>
                    <span className="text-lg font-bold text-nebula-400">~0.04€</span>
                  </div>
                  <p className="text-xs text-muted-foreground">par image</p>
                </div>
              </div>

              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 mt-3">
                <p className="text-sm text-muted-foreground">
                  <strong className="text-green-500">Note :</strong> Pour un usage éducatif raisonnable
                  (quelques dizaines d'images par mois), le coût est très faible (quelques euros).
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Étape 4 : Générer une clé API */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-red-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            4
          </div>
          <h2 className="text-2xl font-bold">Générer une clé API</h2>
        </div>

        {/* Security warning */}
        <div className="bg-red-500/10 border-2 border-red-500/50 rounded-lg p-4 flex gap-3">
          <Shield className="w-6 h-6 text-red-500 flex-shrink-0 mt-0.5" />
          <div>
            <h4 className="font-semibold text-red-500 mb-1">Sécurité</h4>
            <p className="text-sm text-muted-foreground">
              Ne partagez JAMAIS votre clé API publiquement ! Conservez-la en lieu sûr.
            </p>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Key className="w-5 h-5 text-cosmic-400" />
              4.1 Créer la clé
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Dans Google AI Studio ou Google Cloud Console</li>
              <li>Allez dans <strong className="text-foreground">"Identifiants"</strong> (Credentials)</li>
              <li>Cliquez sur <strong className="text-foreground">"Créer des identifiants"</strong> → <strong className="text-foreground">"Clé API"</strong></li>
              <li>Une clé API sera générée (format : <code className="px-2 py-1 bg-muted rounded text-sm font-mono">AIza...</code>)</li>
              <li><strong className="text-foreground">Copiez cette clé</strong> et conservez-la en lieu sûr</li>
            </ol>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Lock className="w-5 h-5 text-cosmic-400" />
              4.2 Associer la clé au projet
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Assurez-vous que la clé est bien associée à votre projet</li>
              <li>Dans les paramètres de la clé, vous pouvez restreindre son utilisation à certaines APIs (recommandé)</li>
              <li>Limitez l'utilisation à l'API Imagen uniquement</li>
            </ol>
          </div>
        </div>
      </section>

      {/* Étape 5 : Configurer Claude Code */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            5
          </div>
          <h2 className="text-2xl font-bold">Configurer Claude Code</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <FileText className="w-5 h-5 text-cosmic-400" />
              5.1 Localiser le dossier .claude
            </h3>
            <p className="text-muted-foreground mb-3">
              Dans votre dossier de travail (là où vous utilisez Claude Code), vous devez avoir un dossier <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.claude/</code>.
            </p>
            <p className="text-muted-foreground mb-3">Si ce dossier n'existe pas encore, créez-le :</p>

            <div className="space-y-3">
              <div className="bg-muted/50 rounded-lg p-4">
                <p className="text-xs text-muted-foreground mb-2">Windows PowerShell</p>
                <pre className="text-sm font-mono overflow-x-auto">
                  <code>mkdir .claude</code>
                </pre>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <p className="text-xs text-muted-foreground mb-2">Linux/Mac</p>
                <pre className="text-sm font-mono overflow-x-auto">
                  <code>mkdir .claude</code>
                </pre>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <FileText className="w-5 h-5 text-cosmic-400" />
              5.2 Créer le fichier .env
            </h3>
            <p className="text-muted-foreground mb-3">
              Dans le dossier <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.claude/</code>, créez un fichier <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.env</code> :
            </p>

            <div className="space-y-3">
              <div className="bg-muted/50 rounded-lg p-4">
                <p className="text-xs text-muted-foreground mb-2">Windows PowerShell</p>
                <pre className="text-sm font-mono overflow-x-auto">
                  <code>{`cd .claude
New-Item -ItemType File -Name ".env"`}</code>
                </pre>
              </div>

              <div className="bg-muted/50 rounded-lg p-4">
                <p className="text-xs text-muted-foreground mb-2">Linux/Mac</p>
                <pre className="text-sm font-mono overflow-x-auto">
                  <code>touch .claude/.env</code>
                </pre>
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Key className="w-5 h-5 text-cosmic-400" />
              5.3 Ajouter la clé API
            </h3>
            <p className="text-muted-foreground mb-3">
              Ouvrez le fichier <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.env</code> avec votre éditeur (VS Code, Notepad++, etc.) et ajoutez :
            </p>

            <div className="bg-muted/50 rounded-lg p-4">
              <pre className="text-sm font-mono overflow-x-auto">
                <code>GOOGLE_API_KEY=AIza_votre_cle_api_ici</code>
              </pre>
            </div>

            <p className="text-muted-foreground mt-3">
              Remplacez <code className="px-2 py-1 bg-muted rounded text-sm font-mono">AIza_votre_cle_api_ici</code> par votre vraie clé API.
            </p>

            <div className="bg-muted/50 rounded-lg p-4 mt-4">
              <p className="text-sm font-semibold mb-2">Structure finale :</p>
              <pre className="text-xs font-mono text-muted-foreground">
{`votre-projet/
├── .claude/
│   ├── .env          ← Votre clé API ici
│   ├── agents/       ← (optionnel)
│   └── skills/       ← (optionnel)
└── [vos fichiers]`}
              </pre>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Shield className="w-5 h-5 text-cosmic-400" />
              5.4 Protéger votre clé API
            </h3>
            <p className="text-muted-foreground mb-3">
              Si vous utilisez Git, ajoutez le fichier <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.env</code> au <code className="px-2 py-1 bg-muted rounded text-sm font-mono">.gitignore</code> :
            </p>

            <div className="bg-muted/50 rounded-lg p-4">
              <p className="text-xs text-muted-foreground mb-2">Ajouter à .gitignore</p>
              <pre className="text-sm font-mono overflow-x-auto">
                <code>echo ".claude/.env" &gt;&gt; .gitignore</code>
              </pre>
            </div>

            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 mt-3">
              <p className="text-sm text-muted-foreground">
                <strong className="text-green-500">Protection :</strong> Cela empêche votre clé d'être envoyée sur GitHub !
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Étape 6 : Tester */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full cosmic-gradient flex items-center justify-center text-white font-bold">
            6
          </div>
          <h2 className="text-2xl font-bold">Tester la configuration</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-cosmic-400" />
              6.1 Vérifier dans Claude Code
            </h3>
            <p className="text-muted-foreground mb-3">Lancez Claude Code et demandez :</p>

            <div className="bg-muted/50 rounded-lg p-4">
              <pre className="text-sm font-mono overflow-x-auto whitespace-pre-wrap">
                <code>Génère une image d'un graphique de fonction affine pour illustrer un cours de mathématiques</code>
              </pre>
            </div>

            <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 mt-3">
              <p className="text-sm text-muted-foreground">
                <strong className="text-green-500">Succès :</strong> Claude devrait utiliser l'API Imagen pour créer l'image !
              </p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-yellow-500" />
              6.2 Dépannage
            </h3>
            <p className="text-muted-foreground mb-3">Si ça ne fonctionne pas :</p>

            <div className="space-y-2">
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">1</div>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-foreground">Vérifiez que la clé API est correcte</strong> (pas d'espaces, pas de guillemets)
                </p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">2</div>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-foreground">Vérifiez que l'API Imagen est activée</strong> dans Google Cloud
                </p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">3</div>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-foreground">Vérifiez que la facturation est activée</strong> sur votre projet
                </p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">4</div>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-foreground">Vérifiez que le fichier .env est dans .claude/</strong> (pas ailleurs)
                </p>
              </div>
              <div className="flex items-start gap-2">
                <div className="w-6 h-6 rounded-full bg-muted flex items-center justify-center text-xs font-bold flex-shrink-0 mt-0.5">5</div>
                <p className="text-sm text-muted-foreground">
                  <strong className="text-foreground">Redémarrez Claude Code</strong> après avoir ajouté la clé
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Sécurité et bonnes pratiques */}
      <section className="glass-card rounded-xl p-8 space-y-6 border-2 border-cosmic-500/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg cosmic-gradient flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Sécurité et bonnes pratiques</h2>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* À faire */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-green-500" />
              À faire
            </h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3 p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Conserver la clé API dans le fichier .env uniquement</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Ajouter .env au .gitignore</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Définir des alertes de facturation dans Google Cloud</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-green-500/10 border border-green-500/20">
                <CheckCircle2 className="w-4 h-4 text-green-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Révoquer et recréer la clé si elle est compromise</span>
              </div>
            </div>
          </div>

          {/* À ne pas faire */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold flex items-center gap-2">
              <XCircle className="w-5 h-5 text-red-500" />
              À ne pas faire
            </h3>
            <div className="space-y-3">
              <div className="flex items-start gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Ne jamais commiter la clé dans Git</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Ne jamais partager la clé publiquement</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Ne pas inclure la clé directement dans le code</span>
              </div>
              <div className="flex items-start gap-3 p-3 rounded-lg bg-red-500/10 border border-red-500/20">
                <XCircle className="w-4 h-4 text-red-500 flex-shrink-0 mt-0.5" />
                <span className="text-sm text-muted-foreground">Ne pas utiliser la même clé pour plusieurs projets</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Gérer les coûts */}
      <section className="glass-card rounded-xl p-8 space-y-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg nebula-gradient flex items-center justify-center">
            <BarChart3 className="w-6 h-6 text-white" />
          </div>
          <h2 className="text-2xl font-bold">Gérer les coûts</h2>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <Bell className="w-5 h-5 text-nebula-400" />
              Définir des alertes de budget
            </h3>
            <ol className="list-decimal list-inside space-y-2 text-muted-foreground ml-6">
              <li>Dans Google Cloud Console → <strong className="text-foreground">"Facturation"</strong></li>
              <li>Créez un <strong className="text-foreground">budget</strong> (ex: 10€/mois)</li>
              <li>Configurez des <strong className="text-foreground">alertes</strong> à 50%, 90%, 100%</li>
              <li>Vous recevrez des emails si vous dépassez ces seuils</li>
            </ol>
          </div>

          <div>
            <h3 className="text-lg font-semibold mb-3 flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-nebula-400" />
              Surveiller l'utilisation
            </h3>
            <ul className="space-y-2 text-muted-foreground ml-6">
              <li className="flex items-start gap-2">
                <span className="text-nebula-400 mt-1">•</span>
                <span>Consultez régulièrement l'onglet <strong className="text-foreground">"Facturation"</strong> pour voir votre consommation</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-nebula-400 mt-1">•</span>
                <span>Utilisez l'API avec parcimonie pour les tests</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-nebula-400 mt-1">•</span>
                <span>Désactivez l'API si vous ne l'utilisez plus</span>
              </li>
            </ul>
          </div>
        </div>
      </section>

      {/* Prochaines étapes */}
      <section className="glass-card rounded-xl p-8 space-y-6 cosmic-gradient text-white">
        <h2 className="text-2xl font-bold">Prochaines étapes</h2>
        <p className="text-white/90">
          Une fois l'API configurée, vous pouvez :
        </p>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="flex items-start gap-3 p-4 rounded-lg bg-white/10 backdrop-blur-sm">
            <Palette className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Illustrations pour vos cours</h3>
              <p className="text-sm text-white/80">Générez des images pédagogiques sur mesure</p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-white/10 backdrop-blur-sm">
            <BarChart3 className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Diagrammes mathématiques</h3>
              <p className="text-sm text-white/80">Créez des graphiques et schémas complexes</p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-white/10 backdrop-blur-sm">
            <Image className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Présentations reveal.js</h3>
              <p className="text-sm text-white/80">Illustrez vos slides avec des images IA</p>
            </div>
          </div>

          <div className="flex items-start gap-3 p-4 rounded-lg bg-white/10 backdrop-blur-sm">
            <FileText className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold mb-1">Documents LaTeX</h3>
              <p className="text-sm text-white/80">Enrichissez vos documents avec des illustrations</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
