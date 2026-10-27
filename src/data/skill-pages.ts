import type { SkillPackId } from '@/data/ai-packages'

/**
 * Pages de présentation des skills : contenu affiché sous le diaporama
 * (/claude-code/presentations/<slug>) quand le slug figure ici.
 *
 * Discours orienté flux : la demande du prof, ce que fait l'agent à chaque étape,
 * ce que le prof obtient, puis le pack à télécharger et son installation.
 * Pour ajouter un skill : déclarer son pack dans SKILL_PACKS (src/data/ai-packages.ts),
 * puis une entrée ici, clée par le slug du diaporama.
 */

export interface SkillPageStep {
  /** Verbe court : Créer, Écrire… */
  nom: string
  /** Skill qui réalise l'étape (affiché discrètement) */
  skill: string
  /** Ce que fait l'agent, en une phrase */
  quoi: string
  /** Nom d'icône lucide-react, résolu par SkillPackPanel */
  icone: 'FolderPlus' | 'PenLine' | 'Cog' | 'Eye' | 'FileText' | 'Search' | 'Sparkles' | 'Mic' | 'Clapperboard'
    | 'BookOpen' | 'ListOrdered' | 'Calculator' | 'ChartColumn'
}

export interface SkillPageConfig {
  /** Titre de la page (remplace le titre déduit du nom de fichier) */
  titre: string
  /** Une phrase : où l'on veut en venir */
  accroche: string
  /** Pack à ajouter au panier */
  packId: SkillPackId
  /** Exemple de demande du professeur */
  demandeExemple: string
  /** Résultat obtenu, en une ligne */
  resultat: string
  etapes: SkillPageStep[]
  /** Ce que le prof obtient */
  obtient: string[]
  /** Prérequis, avec lien facultatif */
  prerequis: { texte: string; lien?: { href: string; label: string } }[]
  /** Pour lancer le skill */
  invocation: string
}

export const SKILL_PAGES: Record<string, SkillPageConfig> = {
  'bfcours-latex-system': {
    titre: 'Le skill latex : de votre demande au PDF relu',
    accroche:
      'Vous décrivez le document en français ; l\'agent le crée, l\'écrit avec bfcours, le compile puis relit le PDF page par page pour en améliorer la mise en page.',
    packId: 'skill-latex',
    demandeExemple: 'Fais-moi une fiche d\'exercices sur les vecteurs en seconde, avec le corrigé.',
    resultat: 'Un PDF compilé, à la mise en page vérifiée, et ses sources LaTeX.',
    etapes: [
      {
        nom: 'Créer',
        skill: 'tex-document-creator',
        quoi: 'Choisit le modèle (cours, devoir, DM, fiche…), remplit l\'en-tête et prépare le dossier.',
        icone: 'FolderPlus',
      },
      {
        nom: 'Écrire',
        skill: 'bfcours-latex',
        quoi: 'Rédige définitions, propriétés, exemples et exercices dans les encadrés bfcours, barème et corrigé compris.',
        icone: 'PenLine',
      },
      {
        nom: 'Compiler',
        skill: 'tex-compiling-skill',
        quoi: 'Produit le PDF, lit les erreurs, corrige et recompile jusqu\'à un PDF sans erreur.',
        icone: 'Cog',
      },
      {
        nom: 'Regarder et améliorer',
        skill: 'latex-visual-review',
        quoi: 'Photographie chaque page, repère blancs et débordements, resserre les énoncés en colonnes, revient en arrière si le rendu se dégrade.',
        icone: 'Eye',
      },
    ],
    obtient: [
      'Le PDF, prêt à imprimer ou à projeter.',
      'Un dossier LaTeX propre, que vous pouvez reprendre à la main.',
      'Des retouches en français : « passe l\'exercice 3 sur deux colonnes ».',
      'Si vous partez d\'un PDF, ses figures reprises à l\'identique (pdf2tikz).',
    ],
    prerequis: [
      {
        texte: 'Une distribution LaTeX avec LuaLaTeX (MiKTeX ou TeX Live).',
        lien: { href: '/claude-code/tutorials/vscode-miktex', label: 'Installer MiKTeX' },
      },
      {
        texte: 'Le paquet bfcours.',
        lien: { href: '/claude-code/download-latex-packages', label: 'Paquets LaTeX' },
      },
      {
        texte: 'Python 3, avec les modules de la partie « Modules Python ».',
        lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
      },
    ],
    invocation: 'Demandez simplement « une évaluation sur Pythagore en 4e », ou tapez /latex suivi de votre demande.',
  },
  'reveals-presentation-system': {
    titre: 'Le skill reveals : de votre demande au diaporama prêt à projeter',
    accroche:
      'Vous décrivez la séance en français, ou vous joignez votre fiche ; l\'agent choisit le gabarit adapté à votre public, construit la séance de gauche à droite avec les détails en dessous, reprend vos figures, puis contrôle chaque diapo avant de livrer.',
    packId: 'skill-reveals',
    demandeExemple: 'Fais-moi un diaporama pour corriger en classe les exercices de ma fiche sur les vecteurs, en seconde.',
    resultat: 'Un diaporama web : une question par diapo, la correction révélée pas à pas.',
    etapes: [
      {
        nom: 'Cadrer',
        skill: 'gabarits collège · lycée · académique',
        quoi: 'Repère le public et le type de séance (cours ou exercices), puis part du gabarit correspondant, dont il ne touche jamais le design.',
        icone: 'Search',
      },
      {
        nom: 'Construire',
        skill: 'reveals-presentation',
        quoi: 'Écrit le fil de la séance de gauche à droite et les détails en dessous : un cours en quatre niveaux, une diapo par question d\'exercice, la correction révélée au clic.',
        icone: 'PenLine',
      },
      {
        nom: 'Illustrer',
        skill: 'extract_tikz_figures.py',
        quoi: 'Si votre document contient des figures TikZ, les compile une à une et les place en images sur les bonnes diapos.',
        icone: 'Sparkles',
      },
      {
        nom: 'Contrôler',
        skill: 'liste de vérification du skill',
        quoi: 'Pas plus de 70 % de diapo remplie, deux éléments côte à côte au plus, formules et navigation vérifiées dans le navigateur.',
        icone: 'Eye',
      },
    ],
    obtient: [
      'Un fichier HTML qui s\'ouvre dans le navigateur, prêt à projeter en plein écran.',
      'Ses sources lisibles et ses images, que vous pouvez reprendre à la main.',
      'Des retouches en français : « coupe la question c) en deux diapos ».',
      'Sur demande, une version autonome (images incluses) à envoyer par mail ou à déposer sur l\'ENT.',
    ],
    prerequis: [
      {
        texte: 'Un navigateur récent et une connexion internet à l\'ouverture (reveal.js et les formules se chargent en ligne).',
      },
      {
        texte: 'Python 3, pour les scripts de figures et la version autonome (aucun module à installer).',
        lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
      },
      {
        texte: 'Facultatif, pour reprendre des figures TikZ : LuaLaTeX (MiKTeX ou TeX Live) et pdftoppm, Ghostscript ou ImageMagick.',
        lien: { href: '/claude-code/tutorials/vscode-miktex', label: 'Installer MiKTeX' },
      },
    ],
    invocation: 'Demandez simplement « un diaporama de cours sur Pythagore pour une 4e, 20 minutes », en joignant votre fiche si vous en avez une, ou tapez /reveals-presentation suivi de votre demande.',
  },
  'capsule-video-skill': {
    titre: 'Le skill capsules vidéo : de votre demande à la vidéo animée',
    accroche:
      'Vous demandez la correction d\'un exercice ou l\'explication d\'une notion ; l\'agent relit le document, écrit le texte comme une copie modèle, le fait lire par une voix française installée sur votre ordinateur (ou part de votre enregistrement), puis cale chaque geste sur le mot qui le dit et filme la vidéo.',
    packId: 'skill-capsule-video',
    demandeExemple: 'Fais-moi une capsule vidéo de correction de l\'exercice 5 de ma fiche sur les probabilités conditionnelles.',
    resultat: 'Une vidéo MP4 de quelques minutes, dont chaque geste suit la voix.',
    etapes: [
      {
        nom: 'Préparer',
        skill: 'revue critique · preferences.md',
        quoi: 'Relit l\'exercice en enseignant exigeant (démarche plus simple, vocabulaire, hypothèses), pose une seule salve de questions et retient vos goûts.',
        icone: 'Search',
      },
      {
        nom: 'Écrire',
        skill: 'script.md · relire_script.py',
        quoi: 'Rédige le texte en courts passages écrits pour l\'oreille, comme une copie modèle ; une relecture automatique bloque la voix tant qu\'une faute reste.',
        icone: 'PenLine',
      },
      {
        nom: 'Dire',
        skill: 'Pocket TTS · MFA',
        quoi: 'Une voix de synthèse française lit chaque passage, puis l\'instant de chaque mot est repéré. Ou bien votre enregistrement est transcrit, lapsus signalés.',
        icone: 'Mic',
      },
      {
        nom: 'Animer',
        skill: 'spec.js · moteur canvas',
        quoi: 'Décrit chaque écran, accroche chaque geste à un mot dit, puis filme la vidéo en quelques secondes, sans débordement possible.',
        icone: 'Clapperboard',
      },
    ],
    obtient: [
      'La vidéo MP4 (720p par défaut, 540p ou 1080p sur demande), prête pour l\'ENT ou Moodle.',
      'Une page d\'aperçu pour commenter à l\'instant voulu et copier vos remarques pour l\'agent.',
      'Des retouches en français : seuls les passages modifiés sont revoisés et réanimés.',
      'Sur demande, une fiche entière en série : voix en lot, animations en parallèle, rendus en file.',
    ],
    prerequis: [
      {
        texte: 'Après l\'archive, lancer l\'installeur du skill (.claude/skills/capsule-video/installation/installer.ps1, ou installer.sh sous Linux et macOS, non testés ; mode d\'emploi : installation/LISEZMOI.md). Il demande un dossier de base sans espace ni accent (le projet lui-même s\'il convient, sinon par exemple D:\\Capsules) : il y recopie le skill, y pose Chromium, FFmpeg, la voix Pocket TTS et les outils de calage (≈ 6 Go, 20 à 40 minutes) et y écrit CLAUDE.md et AGENTS.md. Travaillez ensuite dans ce dossier.',
        lien: { href: '/claude-code/tutorials/capsules-video', label: 'Tutoriel pas à pas' },
      },
      {
        texte: 'Python 3.10 à 3.13 et FFmpeg (l\'installeur propose de les installer s\'ils manquent).',
        lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
      },
      {
        texte: 'Un PC Windows 64 bits ; aucune carte graphique nécessaire (une carte NVIDIA n\'accélère que la transcription de vos enregistrements).',
      },
      {
        texte: 'Voir une capsule réalisée avec ce skill : vidéo de démonstration de 6 minutes (https://youtu.be/okn0E7I2tE0).',
        lien: { href: 'https://youtu.be/okn0E7I2tE0', label: 'YouTube' },
      },
    ],
    invocation: 'Demandez simplement « une capsule de correction de l\'exercice 2, en 2de », en joignant l\'énoncé, ou votre enregistrement (.m4a, .mp3, .wav) pour le mettre en images.',
  },
  'bareme-actions-eleves-skill': {
    titre: 'Le skill barème détaillé : du sujet corrigé au barème justifié',
    accroche:
      'Vous donnez un sujet et son corrigé ; l\'agent découpe chaque corrigé en actions d\'élève visibles sur la copie, en tire les points, la conversion sur 20 et la densité du sujet.',
    packId: 'skill-bareme',
    demandeExemple: 'Établis le barème de mon DS de seconde, calculs et géométrie, noté sur 20.',
    resultat: 'Un barème question par question, où 1 point = 1 action d\'élève, converti sur 20.',
    etapes: [
      {
        nom: 'Lire',
        skill: 'commande /bareme',
        quoi: 'Ouvre le sujet, repère chaque exercice, ses questions et son corrigé, et reconnaît le type d\'exercice (calcul, géométrie, QCM…).',
        icone: 'BookOpen',
      },
      {
        nom: 'Atomiser',
        skill: 'bareme-actions-eleves',
        quoi: 'Découpe chaque corrigé en actions que l\'élève doit écrire : un calcul intermédiaire, une formule posée, une conclusion, un point placé.',
        icone: 'ListOrdered',
      },
      {
        nom: 'Calculer',
        skill: 'bareme-actions-eleves',
        quoi: 'Additionne les actions, les pondère (une action de géométrie vaut 0,5 point) et calcule le coefficient qui ramène la note sur 20.',
        icone: 'Calculator',
      },
      {
        nom: 'Analyser',
        skill: 'bareme-actions-eleves',
        quoi: 'Mesure la densité du sujet (actions par point de la note) et recommande d\'alléger ou d\'étoffer.',
        icone: 'ChartColumn',
      },
    ],
    obtient: [
      'Le barème détaillé (bareme.json) : chaque point décrit par l\'action qu\'il récompense.',
      'Une interface (bareme.html) pour relire et ajuster le barème, avec synthèse et export CSV.',
      'La conversion sur 20 : total libre et coefficient de conversion (la notation des copies reste hors du skill).',
      'Un diagnostic du sujet : densité standard entre 3 et 4 actions par point, trop dense au-delà de 4.',
    ],
    prerequis: [
      { texte: 'Un sujet avec son corrigé rédigé, idéalement en bfcours (EXO, \\tcbitempoint, \\exocorrection).' },
      { texte: 'Un navigateur pour ouvrir l\'interface bareme.html. Ni Python, ni LaTeX nécessaires.' },
      {
        texte: 'Pour rédiger le sujet lui-même : le skill latex.',
        lien: { href: '/claude-code/presentations/bfcours-latex-system', label: 'Skill latex' },
      },
    ],
    invocation: 'Demandez « établis le barème de mon DS, sur 20 » en indiquant le fichier .tex, ou tapez /bareme suivi du chemin du sujet (Claude Code).',
  },
  'bfcours-typst-skill': {
    titre: 'Le skill Typst : de votre demande aux PDF professeur et élève',
    accroche:
      'Vous décrivez le document, ou vous donnez votre cours LaTeX bfcours ; l\'agent le passe en Typst avec la suite farfadet, compile d\'un coup les versions professeur et élève, puis regarde les pages des deux avant de vous les rendre.',
    packId: 'skill-typst',
    demandeExemple: 'Passe mon cours LaTeX sur les vecteurs en Typst, avec la version élève.',
    resultat: 'Un fichier Typst dans votre dossier et ses PDF professeur et élève, vérifiés.',
    etapes: [
      {
        nom: 'Partir',
        skill: 'bfcours-typst · convertir.py, recettes',
        quoi: 'Convertit votre cours LaTeX bfcours commande par commande, ou part d\'un document modèle du même type (cours, fiche, évaluation, QCM).',
        icone: 'FileText',
      },
      {
        nom: 'Écrire',
        skill: 'bfcours-typst · chercher.py',
        quoi: 'Rédige avec les encadrés farfadet (définitions, exercices, zones de réponse, corrigés) ; chaque fonction et chaque option sont cherchées, jamais devinées.',
        icone: 'PenLine',
      },
      {
        nom: 'Compiler',
        skill: 'bfcours-typst · compiler.py',
        quoi: 'Produit d\'un coup les versions professeur et élève, figures LaTeX comprises ; lit les erreurs et corrige.',
        icone: 'Cog',
      },
      {
        nom: 'Regarder',
        skill: 'bfcours-typst · compiler.py --png',
        quoi: 'Regarde chaque page des deux versions : aucune réponse chez l\'élève, rien qui manque ou déborde, comparaison au PDF LaTeX d\'origine.',
        icone: 'Eye',
      },
    ],
    obtient: [
      'Deux PDF, professeur et élève, tirés d\'un seul fichier.',
      'Le fichier .typ dans le dossier que vous indiquez : aperçu en direct dans VS Code, retouches à la main.',
      'Vos fichiers LaTeX intacts : ils ne sont jamais modifiés.',
      'Des retouches en français : « redessine la figure de l\'exercice 2 en Typst ».',
    ],
    prerequis: [
      {
        texte: 'La suite farfadet, installée en une commande depuis la page Packages Typst du site (paquets, polices, extension VS Code).',
        lien: { href: '/claude-code/download-typst-packages', label: 'Packages Typst' },
      },
      {
        texte: 'Python 3, avec le module typst (PyMuPDF pour les images de contrôle).',
        lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
      },
      {
        texte: 'Facultatif : une distribution LaTeX, seulement pour les figures gardées en LaTeX.',
      },
      {
        texte: 'Pour apprendre Typst vous-même : la formation interactive.',
        lien: { href: '/claude-code/tutorials/typst', label: 'Formation Typst' },
      },
    ],
    invocation: 'Demandez « passe ce cours en Typst, avec la version élève » en indiquant le fichier .tex et le dossier de travail, ou « fais-moi une fiche d\'exercices en Typst sur… ».',
  },
  'programmes-officiels-system': {
    titre: 'Les skills programmes et progression : du BO 2026 à la progression annuelle',
    accroche:
      'Vous posez une question sur le programme ou demandez une progression ; l\'agent cherche dans le BO de la rentrée 2026, le cite mot pour mot avec sa page, puis construit avec vous la progression du niveau et la vérifie.',
    packId: 'skill-programmes-progression',
    demandeExemple: 'Construis ma progression de 5e sur le nouveau programme : sept séquences, avec les vacances.',
    resultat: 'Une fiche de progression interactive, chaque compétence tirée du BO avec sa page.',
    etapes: [
      {
        nom: 'Chercher',
        skill: 'programmes-officiels',
        quoi: 'Trouve dans le programme du niveau les compétences, démonstrations exigibles et algorithmes qui vous concernent ; suit une notion d\'un niveau à l\'autre.',
        icone: 'Search',
      },
      {
        nom: 'Citer',
        skill: 'programmes-officiels',
        quoi: 'Donne la formulation du BO mot pour mot, extraite du PDF par un script, avec le PDF et la page d\'où elle vient.',
        icone: 'BookOpen',
      },
      {
        nom: 'Construire',
        skill: 'progression-builder',
        quoi: 'Prépare la fiche du niveau avec toutes les compétences du BO, puis répartit avec vous les compétences en séquences, bloc par bloc, vacances comprises.',
        icone: 'ListOrdered',
      },
      {
        nom: 'Vérifier',
        skill: 'progression-builder',
        quoi: 'Contrôle chaque code, signale les doublons et compte les compétences placées sur le total du programme.',
        icone: 'Eye',
      },
    ],
    obtient: [
      'Une fiche HTML de progression : glisser-déposer, séquences, vacances, commentaires, export HTML, PDF, JSON, Markdown et LaTeX.',
      'Des citations prouvées : formulation du BO, PDF et page de chaque compétence ; un double-clic dans la fiche ouvre le BO à la bonne page.',
      'Treize fiches vierges prêtes, du CM1 à la Terminale, à distribuer à vos collègues.',
      'Des retouches en français : « déplace les statistiques en séquence 6 », « qu\'est-ce qui n\'est pas encore placé ? ».',
    ],
    prerequis: [
      {
        texte: 'Python 3, sans module à installer (PyMuPDF seulement pour reconstruire la base avec un nouveau BO).',
        lien: { href: '/claude-code/tutorials/python-install', label: 'Installer Python' },
      },
      { texte: 'Un navigateur pour ouvrir la fiche de progression, sans installation.' },
      { texte: 'Les deux skills côte à côte dans skills/ : progression-builder lit la base de programmes-officiels.' },
    ],
    invocation: 'Demandez « construis ma progression de 5e en sept séquences », « une fiche vierge de 3e pour mes collègues » ou « quelles démonstrations sont exigibles en seconde ? Cite le BO ».',
  },
}
