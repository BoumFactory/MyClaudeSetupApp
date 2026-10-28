/**
 * Applications de bureau (Tauri, Windows) distribuées sur la page
 * « Logiciels Enseignants ».
 *
 * Distribution : l'EXÉCUTABLE AUTONOME (src-tauri/target/release/<app>.exe),
 * jamais un installeur NSIS ou MSI, livré UNIQUEMENT dans un zip. Dans
 *   public/download/logiciels-enseignant/applications-bureau/<slug>/
 * on trouve :
 *   - <slug>-<version>.zip : dossier prêt à l'emploi (exe + mode d'emploi HTML,
 *     + kit .exoslombards pour Exos Lombards) — c'est ce que livre le panier ;
 *   - <slug>-mode-emploi.html (aussi copié dans le zip).
 * Ni exécutable seul ni kit seul dans le dossier public : construire_zips.py lit
 * l'exe dans D:/Applications/<App>/src-tauri/target/release/.
 * Les zips se reconstruisent par script, pas à la main : docs/applications-bureau/
 * (construire_kit.py produit le kit, construire_zips.py les zips ; essai_kit.mjs =
 * essai à vide d'Exos Lombards).
 *
 * Panier : item `direct: true` → le navigateur télécharge le zip statique
 * tel quel, sans passer par /api/download (réponse d'une fonction Vercel
 * limitée à quelques Mo).
 *
 * Règle : aucun dossier de données n'est distribué. Chaque application crée
 * le sien, vide, à côté de l'exécutable au premier lancement (Exos Lombards :
 * seulement le kit de départ, sans banque d'exercices).
 *
 * À chaque nouvelle version : recompiler l'application, reconstruire les zips,
 * mettre à jour version, date et taille du zip ci-dessous, et le mode d'emploi HTML.
 */
import type { CartItem } from '@/types/cart-theme'

export interface ApplicationBureau {
  /** Identifiant (sert aussi de nom de dossier) */
  slug: string
  nom: string
  /** Phrase d'accroche */
  accroche: string
  /** Ce que l'application fait en classe (3 ou 4 points) */
  points: string[]
  version: string
  /** Date de construction de l'exécutable */
  date: string
  /** Taille du zip, en Mo (arrondie au dixième) */
  tailleZipMo: number
  /** Nom du fichier exécutable contenu dans le zip */
  fichier: string
  /** Prérequis à installer soi-même */
  prerequis?: string[]
  /** Ce qu'il faut faire au premier lancement */
  premierLancement: string[]
  /** Où vivent les données de l'utilisateur */
  donnees: string
  /** Précision propre à l'application */
  remarque?: string
  /** Couleur Tailwind de la carte */
  couleur: 'sky' | 'rose' | 'emerald'
}

const BASE = '/download/logiciels-enseignant/applications-bureau'

export const APPLICATIONS_BUREAU: ApplicationBureau[] = [
  {
    slug: 'exos-lombards',
    nom: 'Exos Lombards',
    accroche: 'Composer fiches, devoirs et sujets au format bac à partir de vos propres exercices LaTeX.',
    points: [
      'Fiches d’exercices, devoirs avec barème et sujets au format bac, compilés en PDF, corrigés en fin de document ou dans un second fichier.',
      'Import de vos fichiers LaTeX (environnement EXO de bfcours, paires énoncé et corrigé…) pour constituer vos bases d’exercices par thèmes.',
      'Exercices libres écrits directement en LaTeX, avec aperçu compilé.',
      'Suivi des exercices déjà donnés à chaque classe et catalogues PDF de vos bases.',
    ],
    version: '0.1.0',
    date: '16 septembre 2026',
    tailleZipMo: 5.3,
    fichier: 'exos-lombards.exe',
    prerequis: [
      'LuaLaTeX, par MiKTeX (recommandé) ou TeX Live. MiKTeX installe à la volée les paquets manquants au premier document : gardez une connexion internet.',
      'bfcours : une copie est fournie dans le kit. S’il n’est pas déjà installé, ouvrez Réglages, rubrique « bfcours embarqué », puis « Installer bfcours dans MiKTeX ».',
      'En secours seulement, si LuaLaTeX est absent : tectonic.exe (site officiel de Tectonic), à placer à côté de l’exécutable.',
    ],
    premierLancement: [
      'Décompressez le zip dans un dossier dont le chemin ne contient aucune espace (par exemple C:\\Applis) : il crée un dossier « Exos-Lombards » avec l’exécutable et le kit de départ « .exoslombards », qui doivent rester côte à côte.',
      'L’application démarre avec « 0 exercice » : aucune banque d’exercices n’est fournie. Importez vos fichiers LaTeX, ou commencez par un « Exercice libre » dans le Composer.',
      'Dans le Composer, remplacez le nom d’établissement proposé par le vôtre.',
      'L’éditeur de code LaTeX se charge en ligne : connexion internet nécessaire pour l’utiliser.',
    ],
    donnees:
      'Vos données restent sur votre poste, dans le dossier « .exoslombards » à côté de l’exécutable : bases, fiches, classes et réglages. Aucun compte, aucun envoi. Pour sauvegarder ou changer de poste, copiez le dossier « Exos-Lombards » entier.',
    remarque:
      'L’écran Aide de l’application est vide dans cette distribution : le mode d’emploi fourni dans le zip le remplace.',
    couleur: 'emerald',
  },
  {
    slug: 'gestion-classes',
    nom: 'Gestion de classes',
    accroche: 'Plan de classe interactif et rôles des élèves, à piloter en direct pendant la séance.',
    points: [
      'Import des listes d’élèves par classe depuis un fichier CSV (enregistré depuis un tableur).',
      'Plan de classe sur grille : on place et on déplace les élèves, avec l’historique des plans.',
      'Rôles de classe (délégué, éco-délégué… ou rôles personnalisés) attribués et répartis équitablement au fil des séances.',
      'Mode « Je suis en séance » et emploi du temps sommaire pour retrouver la classe en cours.',
    ],
    version: '0.1.0',
    date: '28 octobre 2026',
    tailleZipMo: 3.6,
    fichier: 'gestion-classes.exe',
    premierLancement: [
      'Décompressez le zip dans un dossier où vous avez le droit d’écrire (par exemple vos Documents) : il crée un dossier « Gestion-de-classes » avec l’exécutable et son mode d’emploi. Double-cliquez sur l’exécutable.',
      'L’application démarre vide : aucune classe n’est fournie.',
      'Importez un fichier CSV par classe, avec une ligne d’en-tête contenant au moins « nom » et « prénom » (colonnes facultatives : « id », « sousGroupe » ; séparateur virgule ou point-virgule).',
      'Activez ensuite les rôles prédéfinis ou créez les vôtres.',
    ],
    donnees:
      'Vos données restent sur votre poste : de simples fichiers CSV et JSON, dans un dossier « data » créé à côté de l’exécutable. Aucun compte, aucune connexion. Pour changer de poste ou sauvegarder, copiez l’exécutable avec son dossier « data ». Seules les préférences d’affichage (dernière classe ouverte, taille de la grille) sont gardées par Windows dans votre profil.',
    couleur: 'sky',
  },
  {
    slug: 'activite-timer',
    nom: 'Activité-Timer',
    accroche: 'Un minuteur qui se superpose au document projeté pour rythmer recherche et correction.',
    points: [
      'Fenêtre flottante toujours au premier plan, posée sur votre PDF ou votre page projetée, sans lui voler le focus.',
      'Deux phases explicites, résolution puis correction, avec changement de couleur et jauge.',
      'Préréglages de 1, 3, 5, 10, 15 et 20 minutes, lancement au clavier (Espace, touches 1 à 6).',
      'Fenêtre de contrôle pour l’enseignant, avec un aperçu de ce que voit la classe.',
    ],
    version: '0.1.0',
    date: '28 octobre 2026',
    tailleZipMo: 2.3,
    fichier: 'activite-timer.exe',
    premierLancement: [
      'Décompressez le zip dans un dossier où vous avez le droit d’écrire : il crée un dossier « Activite-Timer » avec l’exécutable et son mode d’emploi. Double-cliquez sur l’exécutable.',
      'Rien d’autre à préparer : choisissez une durée et lancez. Aucun droit d’administrateur n’est nécessaire.',
    ],
    donnees:
      'Vos réglages restent sur votre poste, dans les dossiers « config » et « assets » créés à côté de l’exécutable. Aucune connexion.',
    couleur: 'rose',
  },
]

export function nomZip(app: ApplicationBureau): string {
  return `${app.slug}-${app.version}.zip`
}

export function urlZip(app: ApplicationBureau): string {
  return `${BASE}/${app.slug}/${nomZip(app)}`
}

export function urlModeEmploi(app: ApplicationBureau): string {
  return `${BASE}/${app.slug}/${app.slug}-mode-emploi.html`
}

/** Item du panier : le zip statique, téléchargé directement (sans /api/download). */
export function itemPanier(app: ApplicationBureau): CartItem {
  return {
    id: `app-bureau-${app.slug}`,
    name: `${app.nom} (Windows)`,
    type: 'logiciel',
    path: `logiciels-enseignant/applications-bureau/${app.slug}/${nomZip(app)}`,
    description: `Application prête à l'emploi (exécutable et mode d'emploi) — ${app.nom} v${app.version}`,
    direct: true,
  }
}
