# Forme

## Format et outils
- LaTeX avec le paquet bfcours, compilé en **LuaLaTeX** (D-06). Le `CLAUDE.md` du modèle Échantillonnage mentionne pdflatex : ne pas le suivre sur ce point, le script de compilation lance LuaLaTeX.
- Skills à charger avant d'écrire : `bfcours-latex` (forme), `latex-geometry` (figures TikZ : styles `quadrillage`, `point`, `vecteur`).
- Agent rédacteur conseillé : `latex-main-worker` (`.claude/agents/creer/latex/latex-main-worker.md`). Il ne charge pas de lui-même `latex-geometry` : le prompt doit les lui demander.
- Compilation, depuis la racine du projet :
  `PYTHONIOENCODING=utf-8 python ".claude/skills/tex-compiling-skill/scripts/quick_compile.py" --file "1. Cours/2nde/Sequence-Vecteur_par_coordonnees-P1/Activite_translations/Activite_translations.tex" --passes 2`
- Modèle à imiter : `1. Cours/2nde/Sequence-Statistiques/Activite_Echantillonnage/` (préambule, `\chapitre`, `\input{enonce}`, partie « Solution » avec `\rdexocorrection{0}`), sauf pour le style : le skin et les en-têtes colorés sont remplacés selon D-28. En-tête : D-29.
- Questions et réponses : D-27 (toutes les questions des fiches sont des EXO).
- Notations : `\input{../Cours/commands_def}` pour reprendre les macros du cours P1 (D-11), au lieu de les redéfinir.

## Mise en page
- Style sobre (D-10) : un seul accent de couleur, filets, aucun aplat ; tout reste lisible en photocopie noir et blanc. Les rôles se distinguent sans couleur.
- Chaque séance est une `\begin{Activite}[…]` contenant ses parties en `EXO` (titres d'EXO sans virgule ni mode math : « Partie A Construire l'image d'une figure »).
- Ordre dans la fiche S1 : partie A, encadré « Ce que l'on retient », partie B, « Pour aller plus loin ».
- Ordre dans la fiche S2 : rappel flash, partie C, encadré « Ce que l'on retient », partie D, « Pour aller plus loin ».
- Fiche élève de chaque séance : un recto-verso A4 au plus (D-18), en commençant sur une nouvelle page.
- Énoncés serrés possibles en colonnes (`MultiColonnes`, texte à gauche, figure à droite) ; les zones de réponse restent en une colonne et aérées.
- Zones de réponse : `crep`, `\repsim`, `\tcfillcrep`, réglure Seyès (D-09) ; trous de vecteurs selon D-26.
- Quadrillages : carreau de 0,5 cm sur la fiche élève, trait `gray!45` comme le préconise `latex-geometry`, sans axes ni graduations (D-05).
- Pas de point final après une expression mathématique seule dans un item.
- Encadrés « Ce que l'on retient » : un filet et deux lignes de texte (D-07), pas de boîte titrée colorée.

## Supports dérivés
- **Pages de scène** (D-15) : deux pages en paysage (scène S1, scène S2), regroupées après les fiches élèves pour ne pas être photocopiées par erreur.
- **Cartes coup de pouce** (D-13) : une page de six cartes à découper, soit les trois textes (parties A, C, D) imprimés chacun deux fois.
- **Billet de sortie** (D-14) : une demi-page A4, deux billets identiques par page pour la photocopie.
- **Version professeur** (D-27) : « Solution », puis « Notes pour le professeur ».

## Fichiers livrés

```
1. Cours/2nde/Sequence-Vecteur_par_coordonnees-P1/Activite_translations/
├── deroule.md                  déroulé minute par minute validé (lot 1)
├── Activite_translations.tex   maître : préambule, fiches, scènes, cartes, billet, Solution, notes
├── activite_translations.sty   réglages du style sobre (D-28)
├── enonce_seance1.tex          Activite de la séance 1
├── enonce_seance2.tex          Activite de la séance 2
├── scenes.tex                  pages projetables S1 et S2
├── annexes.tex                 cartes coup de pouce et billet de sortie
├── notes_prof.tex              minutage, erreurs prévisibles, réponses du rappel et du billet
├── enonce_figures.tex          toutes les figures TikZ, appelées par \tikzinclude{NOM} (noms en lettres seules)
├── planche_figures.tex         document de contrôle : toutes les figures, une par cadre, avec leur nom
├── planche_figures.pdf         sa compilation
├── CLAUDE.md                   compilation, plages de pages à imprimer, où modifier une figure
└── Activite_translations.pdf   PDF compilé
```

Les données des figures (points, déplacements) vivent seulement dans `enonce_figures.tex` : changer un jeu de données ne touche pas aux énoncés (01-usages, U6). Les réponses de la Solution qui en dépendent sont à reprendre en même temps, ce que le `CLAUDE.md` du dossier signale. `planche_figures.tex` reste dans le dossier comme outil de contrôle des figures.

Les impressions se font à partir du PDF unique, par plages de pages ; le `CLAUDE.md` du dossier donne les plages (fiche S1, fiche S2, scènes, cartes, billet, Solution et notes).
