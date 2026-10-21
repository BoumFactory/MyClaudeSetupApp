# Plan de construction

Le lot 1 s'arrête par construction sur la validation de l'utilisateur (D-12) : la construction ne se fait donc pas d'une traite.

## Lot 1 — Déroulé minute par minute à valider
- **Livre** : `Activite_translations/deroule.md`, qui transforme les tableaux et contenus de 02-contenu en déroulé minute par minute (ce que dit et fait le professeur, ce que font les élèves, ce qui est au tableau), puis la validation de l'utilisateur.
- **Lire** : `00-vision.md`, `01-usages.md` (U2, U3, U4), `02-contenu.md`, D-03, D-04, D-12.
- **Outils** : aucune rédaction LaTeX.
- **Terminé quand** : CA-01, CA-02.
- **Dépend de** : rien.

## Lot 2 — Squelette, style et figures de la séance 1
- **Livre** : le dossier `Activite_translations/` avec le maître, `activite_translations.sty`, et des fichiers `enonce_seance1.tex`, `enonce_seance2.tex`, `scenes.tex`, `annexes.tex`, `notes_prof.tex` vides mais compilables ; dans `enonce_figures.tex`, les figures de la séance 1 (scène S1, parties A et B) ; `planche_figures.tex` et son PDF.
- **Lire** : `03-forme.md`, `02-contenu.md` (blocs « Figure » de la séance 1), D-06, D-10, D-11, D-15, D-17, D-25, D-28, D-29.
- **Outils** : skills `bfcours-latex`, `latex-geometry`, `tex-compiling-skill` ; modèle `1. Cours/2nde/Sequence-Statistiques/Activite_Echantillonnage/`.
- **Terminé quand** : CA-05 pour les parties A et B, CA-06, CA-15, et le maître compile.
- **Dépend de** : lot 1.

## Lot 3 — Fiche de la séance 1
- **Livre** : `enonce_seance1.tex` rédigé (parties A et B, encadré, « Pour aller plus loin ») et ses réponses dans la Solution ; la scène S1 dans `scenes.tex`.
- **Lire** : `02-contenu.md` (séance 1), `03-forme.md`, le `deroule.md` validé, D-07, D-09, D-19, D-26, D-27.
- **Outils** : agent `latex-main-worker` avec les skills `bfcours-latex`, `latex-geometry`.
- **Terminé quand** : CA-03 (questions de la séance 1 et leurs réponses dans la Solution), CA-04, CA-08, CA-09 et CA-12 pour la séance 1.
- **Dépend de** : lot 2.

## Lot 4 — Figures de la séance 2
- **Livre** : dans `enonce_figures.tex`, les figures de la scène S2, du rappel flash, des parties C et D et du « Pour aller plus loin » S2 ; la planche recompilée.
- **Lire** : `02-contenu.md` (blocs « Figure » de la séance 2), D-17, D-20, D-25.
- **Outils** : skills `latex-geometry`, `tex-compiling-skill`.
- **Terminé quand** : CA-05 pour la partie C, et la planche montre toutes les figures de la séance 2.
- **Dépend de** : lot 2.

## Lot 5 — Fiche de la séance 2
- **Livre** : `enonce_seance2.tex` rédigé (rappel flash, parties C et D, encadré, « Pour aller plus loin ») et ses réponses dans la Solution ; la scène S2 dans `scenes.tex`.
- **Lire** : `02-contenu.md` (séance 2), `03-forme.md`, le `deroule.md` validé, D-05, D-08, D-20, D-21, D-23, D-26, D-27.
- **Outils** : agent `latex-main-worker` avec les mêmes skills.
- **Terminé quand** : CA-03 (questions de la séance 2 et leurs réponses dans la Solution), CA-04, CA-07, CA-08, CA-09 et CA-12 pour la séance 2.
- **Dépend de** : lots 3 et 4.

## Lot 6 — Annexes et notes pour le professeur
- **Livre** : `annexes.tex` (cartes coup de pouce, billet de sortie et sa figure), `notes_prof.tex` (minutage, erreurs prévisibles, réponses du billet).
- **Lire** : `02-contenu.md` (coups de pouce, erreurs prévisibles, billet, tableaux de déroulé), `03-forme.md` (supports dérivés), D-13, D-14, D-27.
- **Outils** : skills `bfcours-latex`, `latex-geometry`.
- **Terminé quand** : CA-10, CA-14, et CA-03 pour le billet.
- **Dépend de** : lot 5.

## Lot 7 — Finition et vérification
- **Livre** : document compilé, revu visuellement, et le `CLAUDE.md` du dossier.
- **Lire** : `04-criteres-acceptation.md`, `03-forme.md`, D-30.
- **Outils** : skills `tex-compiling-skill`, `latex-visual-review` ; agent `debug-tex-log` si la compilation échoue.
- **Terminé quand** : CA-11, CA-13, CA-16, CA-17, et une relecture de tous les autres critères.
- **Dépend de** : lot 6.
