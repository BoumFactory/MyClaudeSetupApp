# Figures et défauts visuels résiduels

À lire à l'**Étape 4** quand le document contient des figures (TikZ, images raster) ou quand le diagnostic visuel relève un défaut qu'aucun colonnage n'explique. Couvre les Recettes K et L et les défauts D1 à D5 et D7 (D6, le `\Needspace`, est dans `pagination-et-bandeaux.md`).

---

## Recette L — Latéraliser une figure seule centrée dans une question

**Déclencheur** : un `\tcbitem` d'énoncé contient une consigne courte puis une figure isolée en `\begin{center}…\end{center}` (arbre, schéma, capture, petit repère). Toute la largeur sous la consigne est perdue et le rendu fait amateur. Règle : une figure attachée à une question ne reste pas seule centrée en pleine largeur ; elle passe à côté de sa consigne, en colonnes inégales adaptées au contenu, centrée dans sa colonne.

Outil : `MultiColonnes`, **jamais `minipage`**.

```latex
\tcbitem \tcbitempoint{N}\mbox{}\par\nointerlineskip
    \begin{MultiColonnes}{5}
    \tcbitem[raster multicolumn=2,valign=center]\acc{Recopier et compléter} l'arbre pondéré ci-contre :
    \tcbitem[raster multicolumn=3,halign=center,valign=center]\includegraphics[width=0.62\linewidth]{images/arbre.png}
    \end{MultiColonnes}
```

Points critiques :

1. **`\mbox{}\par\nointerlineskip` est obligatoire** avant un `MultiColonnes` qui ouvre le contenu d'un `\tcbitem` : sans cette ancre, le numéro de l'item se détache **sous** le bloc. Un `~` ne suffit pas.
2. Colonnes inégales : grille `{5}` en 2/3 ou 3/2 selon la largeur de la figure ; `{2}` symétrique pour un texte long et une figure étroite.
3. `halign=center,valign=center` sur la cellule figure ; `valign=center` sur la cellule texte.
4. Largeur relative à la colonne : `width=…\linewidth` (pas `\textwidth`), entre 0,55 et 0,95 pour garder une hauteur raisonnable.
5. Reformuler « ci-dessous » en « ci-contre ».

Même recette pour un algorithme ou une capture de tableau : `{2}` symétrique, seconde cellule avec un `tcolorbox` (`width=\linewidth, nobeforeafter`) ou une `\includegraphics`.

Garde-fou : une figure de **référence partagée** par tout l'exercice (courbe lue par trois questions) peut rester centrée en pleine largeur.

---

## Recette K — Distinguer une courbe de sa tangente

Hors mise en page stricte, mais recevable dès que l'utilisateur signale qu'« on distingue mal la courbe de la tangente » (défaut visible sur le PNG).

Deux causes à traiter ensemble : même style (deux traits pleins de même épaisseur) et tangente trop longue (elle épouse la courbe sur presque tout le domaine).

- Courbe : `ultra thick, blue!75!black` (ou la couleur principale du document).
- Tangente, asymptote, sécante : `thick, orange!90!black, densely dash dot`.
- Tangente raccourcie : `domain` de 1,2 à 1,8 unité centré sur le point de contact, pour que le décollage soit visible aux deux bouts.
- Tangente horizontale à un extremum : raccourcir encore (1 à 1,5 unité) et décaler l'étiquette du point pour qu'elle ne touche ni la courbe ni la tangente.

Vérifier la lisibilité en niveaux de gris (impression noir et blanc fréquente). Pour une nouvelle figure de géométrie, utiliser le skill `latex-geometry`.

---

## D7 — Image raster imprimée sous 150 dpi

Une `\includegraphics` PNG ou JPG paraît correcte à l'écran mais floue à l'impression : son dpi effectif, après mise à l'échelle, est trop bas.

`page_metrics.py` le calcule depuis le PDF (pixels natifs ÷ taille de placement) et liste les cas sous le seuil dans `low_dpi_images` (`--dpi-threshold`, 150 par défaut). Seul le raster est vu : TikZ, PDF et EPS ne sont jamais signalés.

```bash
python "scripts/page_metrics.py" --pdf "<pdf_path>" --dpi 80 --dpi-threshold 150 > metrics.json
```

Lecture : sous 100 dpi, flou net ; entre 100 et 150, flou perceptible sur le texte et les traits fins.

Correctif :

- schéma, graphique, arbre, capture reconstructible → proposer une reconstruction en TikZ (skill `latex-geometry`, ou `pdf2tikz` si une source vectorielle existe) ;
- photo ou capture authentique → réduire la largeur d'affichage jusqu'à repasser au-dessus de 150 dpi, ou demander une meilleure source.

---

## Défauts D1 à D5

| Défaut | Correctif |
|---|---|
| **D1** Veuve ou orpheline (ligne isolée en haut ou en bas de page) | Préambule : `\widowpenalty=10000` et `\clubpenalty=10000` |
| **D2** Figure surdimensionnée | `width=0.9\linewidth` → `0.6\linewidth`, ou `scale` TikZ |
| **D3** Débordement horizontal (`Overfull \hbox`) | Reformuler, césure manuelle `mathéma\-tiques`, en dernier recours `\sloppy` local ; dans un `MultiColonnes`, tester d'abord une largeur asymétrique |
| **D4** Marges trop larges | `\usepackage[margin=Xcm]{geometry}` du fichier principal |
| **D5** Page trop dense (`fill_ratio` > 0,55) | Aérer par des sauts de paragraphe (lignes vides), pas par `\medskip` ; `\baselinestretch=1.1` en dernier recours |
