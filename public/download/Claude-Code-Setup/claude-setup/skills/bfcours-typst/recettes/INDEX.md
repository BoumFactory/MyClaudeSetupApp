# Recettes : documents complets à imiter

Chaque recette compile en version professeur et élève (vérifié le 11/10/2026 par `scripts/compiler.py --png`) ; son en-tête de commentaire dit ce qu'elle montre et comment la compiler. Avant d'écrire un document d'un de ces types, ouvrir la recette correspondante et en reprendre la structure. Les quatre premières sont des conversions fidèles de documents LaTeX réels (source indiquée dans l'en-tête, fichier LaTeX d'origine rappelé en commentaire devant chaque bloc).

| Recette | Type | Ce qu'elle montre | Pages (prof / élève) |
|---|---|---|---|
| [cours.typ](cours.typ) | Cours (2de, vecteurs, sections 1 à 4.3) | sommaire, compétences, index du vocabulaire ; Definition, Propriete, Remarque, Notation, Demonstration, Methode, Exemple ; `voc` ; texte et figure par `multi-colonnes` + `tcbitem` ; `crep` dans le cours ; EXO au fil du cours et corrigés en fin ; 15 figures cetz dont une qui dépend de la version | 8 / 7 |
| [fiche-exercices.typ](fiche-exercices.typ) | Fiche d'exercices (revue de chapitre) | 8 `exo` avec niveau, étiquette et correction ; `tcbenumerate` en colonnes, imbriqué, numérotation reprise ; points en tête de question (boîtes masquées) ; `coordonnees`, `encadrer` ; partie « Solutions » avec second bandeau ; 4 figures cetz | 6 / 3 |
| [evaluation.typ](evaluation.typ) | Évaluation (devoir sur 20) | `chap-eval` + `tableau-eval` ; bilan `getsavedtotalpoints()` ; `itempoint` en tête, boîtes visibles, score par exercice ; un `exo-eval` (grille de maîtrise) ; `crep` et `tcfillcrep` ; couleurs de corrigé ; égalités alignées ; 3 figures cetz | 5 / 3 |
| [qcm.typ](qcm.typ) | QCM et vrai/faux | `mcq` + `mcq-quest(br: …)` en formats `Troyes` et `BFCours`, numérotation poursuivie ; `vrai-faux` + `affirmation` avec justification et points | 1 / 1 |
| [paquets-rd.typ](paquets-rd.typ) | Fiche de calcul (collège) | `rdopp`, `rdconv`, `rdtabnum`, `rdtime`, `rdratio`, `decomp-fp`, `pgcd`, `rd.methode`, `rd.tache` ; prof/élève par `ifcorrection` | 2 / 2 |

Pour une fiche d'exercices avec zones de réponse (`crep`) et barème visible, partir de `evaluation.typ` (la fiche de revue n'a ni `crep` ni boîtes de points) en remplaçant `chap-eval` par le modèle `type-document: [Fiche d'exercices :]`. Les libellés prédéfinis (`"cours"`, `"exercices"`…) s'affichent suivis de « : » (« Exercices : Thème ») ; un libellé libre qui finit déjà par « : » (`[Fiche 1 :]`) garde une simple espace ; `separateur-type: [ ]` redonne l'ancien rendu sans deux-points.

Défauts de paquets contournés dans les recettes (chacun commenté sur place) : bandeau d'EXO ou titre de solution seul en bas de page (`needspace` ou `pagebreak`) ; lignes de fractions qui se chevauchent dans les solutions (`v(0.5em)`).
