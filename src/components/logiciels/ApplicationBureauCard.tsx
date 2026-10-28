import { MonitorDown, ShieldAlert, HardDrive, PlayCircle, Info, Users, Timer, BookOpenCheck, Wrench, FileText } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { AddToCartButton } from "@/components/cart/AddToCartButton"
import {
  type ApplicationBureau,
  urlZip,
  urlModeEmploi,
  itemPanier,
} from "@/data/applications-bureau"

// Classes Tailwind écrites en entier (pas de concaténation) pour que la purge les garde.
const STYLES = {
  sky: {
    bordure: "border-sky-500/20 hover:border-sky-500/40",
    pastille: "bg-gradient-to-br from-sky-500 to-blue-600",
    titre: "group-hover:text-sky-400",
    badge: "bg-sky-500/15 text-sky-300",
    puce: "text-sky-400",
    lien: "text-sky-400",
  },
  rose: {
    bordure: "border-rose-500/20 hover:border-rose-500/40",
    pastille: "bg-gradient-to-br from-rose-500 to-pink-600",
    titre: "group-hover:text-rose-400",
    badge: "bg-rose-500/15 text-rose-300",
    puce: "text-rose-400",
    lien: "text-rose-400",
  },
  emerald: {
    bordure: "border-emerald-500/20 hover:border-emerald-500/40",
    pastille: "bg-gradient-to-br from-emerald-500 to-teal-600",
    titre: "group-hover:text-emerald-400",
    badge: "bg-emerald-500/15 text-emerald-300",
    puce: "text-emerald-400",
    lien: "text-emerald-400",
  },
} as const

const ICONES = {
  "gestion-classes": Users,
  "activite-timer": Timer,
  "exos-lombards": BookOpenCheck,
} as const

function formatTaille(mo: number): string {
  return `${mo.toLocaleString("fr-FR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} Mo`
}

/**
 * Carte d'une application de bureau Windows : description, prérequis, premier
 * lancement, données ; bouton Télécharger (zip prêt à l'emploi), ajout au
 * panier (même zip, téléchargement direct) et lien vers le mode d'emploi.
 */
export function ApplicationBureauCard({ app }: { app: ApplicationBureau }) {
  const s = STYLES[app.couleur]
  const Icone = ICONES[app.slug as keyof typeof ICONES] ?? MonitorDown

  return (
    <Card className={`glass-card border-2 ${s.bordure} transition-all duration-300 group flex flex-col`}>
      <CardHeader>
        <div className="flex items-start justify-between mb-2">
          <div className={`w-11 h-11 rounded-lg ${s.pastille} flex items-center justify-center`}>
            <Icone className="w-5 h-5 text-white" />
          </div>
          <div className="flex flex-wrap justify-end gap-1.5">
            <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>Windows</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-white/5 text-gray-400 font-mono">v{app.version}</span>
          </div>
        </div>
        <CardTitle className={`text-lg transition-colors ${s.titre}`}>{app.nom}</CardTitle>
        <CardDescription>{app.accroche}</CardDescription>
      </CardHeader>

      <CardContent className="space-y-4 flex-1 flex flex-col">
        <ul className="space-y-1.5 text-sm text-muted-foreground">
          {app.points.map((point, i) => (
            <li key={i} className="flex gap-2">
              <span className={`${s.puce} flex-shrink-0`}>•</span>
              <span>{point}</span>
            </li>
          ))}
        </ul>

        <p className="text-xs text-muted-foreground">
          Le zip contient {app.fichier}, à lancer directement, sans installation — Windows 10 ou 11, 64 bits
          (x64) — construit le {app.date}.
        </p>

        {app.prerequis && (
          <div className="rounded-lg bg-white/5 p-3 space-y-1.5">
            <p className="text-sm font-semibold text-foreground inline-flex items-center gap-1.5">
              <Wrench className="w-4 h-4" />
              Prérequis
            </p>
            <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
              {app.prerequis.map((p, i) => (
                <li key={i}>{p}</li>
              ))}
            </ul>
          </div>
        )}

        <div className="rounded-lg bg-white/5 p-3 space-y-1.5">
          <p className="text-sm font-semibold text-foreground inline-flex items-center gap-1.5">
            <PlayCircle className="w-4 h-4" />
            Au premier lancement
          </p>
          <ul className="list-disc list-inside space-y-1 text-sm text-muted-foreground">
            {app.premierLancement.map((etape, i) => (
              <li key={i}>{etape}</li>
            ))}
          </ul>
        </div>

        <p className="text-sm text-muted-foreground flex gap-2">
          <HardDrive className="w-4 h-4 flex-shrink-0 mt-0.5 text-emerald-400" />
          <span>{app.donnees}</span>
        </p>

        {app.remarque && (
          <p className="text-sm text-amber-200/90 flex gap-2">
            <Info className="w-4 h-4 flex-shrink-0 mt-0.5 text-amber-400" />
            <span>{app.remarque}</span>
          </p>
        )}

        <div className="mt-auto space-y-2">
          <div className="flex flex-col sm:flex-row gap-2">
            <Button asChild variant="nebula" className="flex-1">
              <a href={urlZip(app)} download>
                <MonitorDown className="w-4 h-4 mr-2" />
                Télécharger (zip, {formatTaille(app.tailleZipMo)})
              </a>
            </Button>
            <AddToCartButton item={itemPanier(app)} className="flex-1" />
          </div>
          <p className="text-xs text-muted-foreground flex flex-wrap gap-x-3 gap-y-1">
            <a
              href={urlModeEmploi(app)}
              target="_blank"
              rel="noopener noreferrer"
              className={`${s.lien} hover:underline inline-flex items-center gap-1`}
            >
              <FileText className="w-3 h-3" />
              Mode d&apos;emploi
            </a>
          </p>
        </div>
      </CardContent>
    </Card>
  )
}

/**
 * Avertissement commun aux exécutables non signés (formulation reprise du
 * tutoriel « Première app Tauri »).
 */
export function AvertissementExecutableNonSigne() {
  return (
    <div className="glass-card rounded-xl p-5 space-y-2 border-l-4 border-amber-400">
      <p className="font-semibold text-amber-300 inline-flex items-center gap-2">
        <ShieldAlert className="w-5 h-5" />
        Avant le premier lancement : l&apos;avertissement de Windows
      </p>
      <ul className="list-disc list-inside space-y-1.5 text-sm text-muted-foreground">
        <li>
          Ces exécutables ne sont pas <strong className="text-foreground">signés</strong> (une signature
          s&apos;achète auprès d&apos;une autorité de certification). Windows SmartScreen affichera donc
          « Windows a protégé votre ordinateur ». Cliquez sur{" "}
          <strong className="text-foreground">Informations complémentaires</strong>, puis{" "}
          <strong className="text-foreground">Exécuter quand même</strong>.
        </li>
        <li>
          Sous Windows 11, si le <strong className="text-foreground">contrôle intelligent des applications</strong>{" "}
          (Smart App Control) est activé, une application non signée est bloquée, sans possibilité de
          l&apos;autoriser au cas par cas.
        </li>
        <li>
          Les applications ont besoin du composant <strong className="text-foreground">WebView2</strong> de
          Microsoft, déjà présent sur Windows 10 et 11 à jour. S&apos;il manque, la fenêtre ne s&apos;ouvre pas :
          installez le « runtime WebView2 » depuis le site de Microsoft.
        </li>
        <li>
          L&apos;antivirus peut analyser l&apos;exécutable quelques secondes avant de le laisser démarrer.
        </li>
        <li>
          Chaque zip contient un dossier prêt à l&apos;emploi : l&apos;exécutable et son mode d&apos;emploi
          (et, pour Exos Lombards, le kit de départ). Le panier livre ces mêmes zips.
        </li>
      </ul>
    </div>
  )
}
