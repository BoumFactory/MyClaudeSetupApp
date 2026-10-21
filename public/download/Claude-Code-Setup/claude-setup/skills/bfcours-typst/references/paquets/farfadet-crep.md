# farfadet-crep

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": zones-reponse` puis `#import zones-reponse: *`.
- Réglage : `setrdcrep` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-crep.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-crep`).

## Sommaire

- `setrdcrep` — Règle les zones de réponse, les cases à cocher et les boîtes du paquet à partir de cet endroit du document (`\setrdcrep{…}`) : c'est le seu…
- `crep` — Zone de réponse en bloc (`\begin{crep}[options] … \end{crep}`) : un cadre gris (ou des lignes Seyès) sous la question. Version professeur :…
- `tccrep` — Boîte réponse en ligne de largeur fixe (`\tccrep[options]{largeur}{réponse}`), contenu centré. Avec `auto` à la place de la largeur, la lar…
- `tcfillcrep` — Boîte réponse qui occupe le reste de la ligne (`\tcfillcrep[options]{réponse}`), contenu à gauche. Vide, c'est le trait pointillé de `\dotf…
- `repsim` — Petite boîte en ligne (`\repsim[largeur]{réponse}`) : une tccrep.
- `tcfraccrep` — Fraction à trous (`\tcfraccrep[options]{num}{den}`) : deux boîtes en ligne dans une fraction.
- `seyesrep` — Énoncé en haut, réponse sur lignes Seyès en bas, dans un cadre arrondi (`\begin{seyesrep}[options]{réponse} énoncé \end{seyesrep}`, style `…
- `assosbox` — Énoncé accompagné d'une case réponse accolée, à droite (défaut) ou à gauche (`\begin{assosbox}[options]{réponse} énoncé \end{assosbox}`).
- `seyesfig` — Figure encadrée aux couleurs Seyès (style `seyesfig` de rdcrep).
- `dembox` — Étiquette de démonstration (`\dembox[options]{titre}{contenu}`) : « Ce que je sais », « Propriété », « Conclusion »… à la couleur de correc…
- `crepbox` — Boîte réponse Seyès précédée d'une étiquette (`\crepbox[options]{largeur}{étiquette}{réponse}`) : une `tccrep` Seyès de la largeur donnée, …
- `correction-box` — Texte de correction (`\CorrectionBox{x}`) : en version professeur, `x` dans la couleur et la police de correction ; en version élève, la mê…
- `crepcorrectionfont` — La police de correction seule, sans sa couleur (`\crepcorrectionfont`), dans les deux versions : pour écrire un texte comme une réponse (gr…
- `seyestab` — Tableau dont chaque rangée occupe une ligne Seyès (`\begin{seyestab}{colonnes} … \end{seyestab}`) ; sa première rangée est sur la ligne de …
- `seyesarray` — Tableau mathématique Seyès (`\begin{seyesarray}{colonnes}`, NiceArray) : cellules en mode maths. Avec `delims:`, c'est le `seyesarraydelims…
- `checkbox` — Une case à cocher ou un bouton radio vectoriel (`\checkbox[options]`), posé sur la ligne de base. Défauts réglables : `setrdcrep(pour: "che…
- `tcbcheckbox` — Boîte avec une case dans son coin supérieur gauche (environnement `tcbcheckbox`). Défauts réglables : `setrdcrep(pour: "tcbcheckbox", …)` ;…
- `tccheckbox` — Boîte à cocher sensible au mode correctif (`\tccheckbox[options]{contenu}`) : une bande colorée à gauche reçoit la marque (en couleur de co…
- `tccheckboxlist` — Liste de boîtes à cocher en colonnes (`\tccheckboxlist[options]{Bleu, Rouge, …}`) : un contenu par élément (ou un tableau). Les clés de `tc…
- `cb` — Case vide de bfcours (`\cb` = `\checkbox[check mark=mark14, skin=squareshadow]`).
- `ccb` — Case cochée en version professeur (`\ccb` = `\cb` + `checked corr`).
- `mysquare` — Case carrée blanche à cadre noir épais (`\mysquare`).

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `colframe` | cadre. Défaut : `black`. |  | 3 : `crep`, `tcbcheckbox`, `tccheckbox` |
| `width` | largeur. Défaut : `100%`. | width | 5 : `crep`, `seyesfig`, `dembox`, `tcbcheckbox`, `tccheckbox` |
| `bottom` | marge basse. Défaut : `0pt`. |  | 3 : `tccrep`, `tcbcheckbox`, `tccheckbox` |
| `left` | marge gauche. Défaut : `0pt`. |  | 3 : `tccrep`, `tcbcheckbox`, `tccheckbox` |
| `right` | marge droite. Défaut : `0pt`. |  | 3 : `tccrep`, `tcbcheckbox`, `tccheckbox` |
| `arc` | coins. Défaut : `1mm`. |  | 3 : `seyesfig`, `crepbox`, `tccheckbox` |
| `valign` | alignement vertical. Défaut : `"center"`. |  | 3 : `seyesfig`, `tcbcheckbox`, `tccheckbox` |
| `style` | style(s) nommé(s) (`setrdcrep(definir: …)`). | crep/seyesrep style | 3 : `checkbox`, `tcbcheckbox`, `tccheckbox` |

## setrdcrep

```typ
setrdcrep(pour: none, reinitialiser: false, definir: none, correction: auto, correction-color: auto, correction-font: auto, show-crep: auto, seyes: auto, seyes-colors: auto, dotfill-command: auto, auto-factor: auto, seyes-unit: auto, seyes-thick: auto, seyes-thin: auto, seyes-shift: auto, seyes-subdivisions: auto, sans-font: auto, every-crep: none, every-tccrep: none, every-box: none, reset-crep-counter: false, reset-tccrep-counter: false, set-crep-counter: none, set-tccrep-counter: none, default: false, style: auto, ..cles)
```

Règle les zones de réponse, les cases à cocher et les boîtes du paquet à partir de cet endroit du document (`\setrdcrep{…}`) : c'est le seul réglage du paquet. Les clés absentes gardent leur valeur ; une clé inconnue ou une valeur invalide arrête la compilation avec la liste des possibilités.

LaTeX : `\setrdcrep`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type réglé : `"crep"`, `"tccrep"`, `"frac"`, `"dembox"`, `"seyesfig"`, `"seyestab"`, `"tccheckbox"`, `"tccheckboxlist"`, `"crepbox"`, `"checkbox"`, `"tcbcheckbox"`, ou un tableau de types. Défaut : `none` (réglage globa… |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages global et par type (les styles nommés restent) ; avec des clés, repart des défauts puis les applique ; `"tout"` : ramène aussi les styles aux styles prédéfinis. Défaut : `false`. |  |
| `definir` | `none` | str, none | définit le style nommé de ce nom (appelé ensuite par `style:` sur n'importe quelle boîte) avec les clés données ; `pour:` contrôle alors ces clés contre un type. Les styles prédéfinis de rdcrep se redéfinissent de la mê… |  |
| `correction` | `auto` | bool, auto | version professeur (`true`) ou élève (`false`) à partir d'ici ; `--input correction=…` l'emporte. Défaut : `auto` (inchangée). | correction |
| `correction-color` | `auto` | auto, color, str | couleur des réponses en version professeur ; la valeur donnée est aussi recopiée dans le socle (objets rd). Défaut : `auto`, la couleur réglée par `setbfsocle(correction-color: …)`, elle-même par défaut la couleur nommé… | correction color |
| `correction-font` | `auto` | auto, dictionary, str, function | police des réponses : `(size: "large", weight: "bold")`, ou commandes LaTeX `"\large\bfseries"`. Défaut : `auto`, la police réglée par `setbfsocle(correction-font: …)` (grand et gras). | correction font |
| `show-crep` | `auto` | bool | `false` supprime les boîtes crep et vide les boîtes en ligne (simple énoncé). Défaut : `true`. | show crep |
| `seyes` | `auto` | bool | lignes Seyès dans les boîtes. Défaut bfcours : `true` (rdcrep : `false`). | seyes |
| `seyes-colors` | `auto` | color, array | couleurs (lignes épaisses, lignes fines). Défaut : la couleur nommée `seyescol` pour les deux. | seyes colors |
| `dotfill-command` | `auto` | content, none | remplissage des boîtes `dotfill` côté élève ; `none` : pointillés. Défaut : `none`. | dotfill command |
| `auto-factor` | `auto` | int, float | largeur d'une `tccrep(auto)` = facteur × largeur de la réponse. Défaut : `2`. | auto factor |
| `seyes-unit` | `auto` | length | interligne Seyès (ajout). Défaut : `8mm`. |  |
| `seyes-thick` | `auto` | length | épaisseur des lignes épaisses (ajout). Défaut : `1.128pt` TeX. |  |
| `seyes-thin` | `auto` | length | épaisseur des lignes fines (ajout). Défaut : `0.564pt` TeX. |  |
| `seyes-shift` | `auto` | length | décalage des lignes sous la ligne de base (ajout). Défaut : `0.564pt` TeX. |  |
| `seyes-subdivisions` | `auto` | int | intervalles par ligne Seyès (ajout). Défaut : `4`. |  |
| `sans-font` | `auto` | str, array | police sans empattement des pastilles et des dembox (ajout). |  |
| `every-crep` | `none` | dictionary | clés appliquées à toutes les boîtes `crep` (`every crep`). | every crep |
| `every-tccrep` | `none` | dictionary | clés appliquées à toutes les boîtes en ligne (`every tccrep`). | every tccrep |
| `every-box` | `none` | dictionary | clés appliquées aux deux (`every box`). | every box |
| `reset-crep-counter` | `false` | bool | remet à zéro le compteur des crep. Défaut : `false`. | reset crep counter |
| `reset-tccrep-counter` | `false` | bool | remet à zéro le compteur des boîtes en ligne. Défaut : `false`. | reset tccrep counter |
| `set-crep-counter` | `none` | int, none | fixe le compteur des crep. Défaut : `none`. | set crep counter |
| `set-tccrep-counter` | `none` | int, none | fixe le compteur des boîtes en ligne. Défaut : `none`. | set tccrep counter |
| `default` | `false` | bool | `true` : défauts d'origine de rdcrep (préréglage « rd » : rouge, gras, sans Seyès, version élève). Défaut : `false`. | default |
| `style` | `auto` | str, array | style(s) nommé(s) appliqué(s) au niveau réglé. | crep/seyesrep style |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | les clés du type visé par `pour:` (celles de `checkbox`, `tcbcheckbox`, `crepbox`, `seyestab`… ; voir leurs fiches). |

Exemple :

```typ
#setrdcrep(seyes: false, correction-color: blue)
Réponse : #tccrep(2cm)[$42$]
```

## crep

```typ
crep(style: auto, lines: auto, extra-lines: auto, seyes: auto, seyes-colors: auto, dotfill: auto, normal-crep: auto, show-crep-num: auto, crep-mode: auto, forced-height: auto, crep-opaq: auto, bbox: auto, crep-box: auto, title: auto, tcblower: auto, colback: auto, colframe: auto, opacityback: auto, boxrule: auto, arc: auto, sharp-corners: auto, boxsep: auto, top: auto, bottom: auto, left: auto, right: auto, middle: auto, frame-hidden: auto, colbacklower: auto, opacitybacklower: auto, colbacktitle: auto, coltitle: auto, fonttitle: auto, width: auto, height: auto, halign: auto, halign-lower: auto, valign: auto, lefthand-width: auto, righthand-width: auto, sidebyside-gap: auto, bicolor: auto, before-skip: auto, after-skip: auto, crep-num-veil: auto, crep-num-fill: auto, crep-num-color: auto, crep-num-size: auto, seyes-unit: auto, seyes-thick: auto, seyes-thin: auto, seyes-shift: auto, seyes-subdivisions: auto, ..parties)
```

Zone de réponse en bloc (`\begin{crep}[options] … \end{crep}`) : un cadre gris (ou des lignes Seyès) sous la question. Version professeur : la réponse en couleur ; version élève : la même place, vide. Deux contenus (ou `tcblower:`) donnent deux parties : l'une visible, l'autre réponse (`crep-mode`).

LaTeX : `\crep`

Clés communes acceptées (voir en tête) : `colframe`, `width`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `style` | `auto` | str, array | style(s) nommé(s) (`setrdcrep(definir: …)`, `"crep opaq"`, `"seyes lower"`…). | crep/seyesrep style |
| `lines` | `auto` | int, float | nombre de lignes Seyès vides ajoutées sous la réponse (= `\repline[n]`) ; remplace `extra-lines`. Défaut : `auto` (`extra-lines`). |  |
| `extra-lines` | `auto` | int, float | lignes Seyès vides ajoutées sous la réponse. Défaut : `0`. | extra lines |
| `seyes` | `auto` | bool | lignes Seyès. Défaut : réglage de `setrdcrep` (vrai dans bfcours). | seyes |
| `seyes-colors` | `auto` | color, array | couleurs (épaisses, fines) des lignes Seyès. | seyes colors |
| `dotfill` | `auto` | bool | côté élève, affiche le contenu normalement (sans le masquer). Défaut : `false`. | dotfill |
| `normal-crep` | `auto` | bool | contenu affiché normalement, quelle que soit la version. Défaut : `false`. | normal crep |
| `show-crep-num` | `auto` | bool | voile et numéro de la boîte. Défaut : `false`. | show crep num |
| `crep-mode` | `auto` | str | `"regular"`, `"upper"`, `"lower"`, `"left"`, `"right"` : partie qui reçoit la réponse. Défaut : `"regular"`. | crep mode |
| `forced-height` | `auto` | bool | ancrage des lignes sur la première ligne (hauteur imposée). Défaut : `false`. | forced height |
| `crep-opaq` | `auto` | bool | boîte opaque grise, sans Seyès (`crep opaq`). Défaut : `false`. | crep opaq |
| `bbox` | `auto` | array, none | `(bas, haut)` : agrandit la boîte en bas et en haut. Défaut : `none`. | bbox |
| `crep-box` | `auto` | dictionary | style par numéro de boîte : `("11": (colback: yellow))`. Défaut : `(:)`. |  |
| `title` | `auto` | content, none | titre en bandeau. Défaut : `none`. |  |
| `tcblower` | `auto` | content, none | partie basse (`\tcblower`). Défaut : `none`. |  |
| `colback` | `auto` | color, str | fond. Défaut : `gray!10` (blanc transparent avec Seyès). |  |
| `opacityback` | `auto` | float | opacité du fond. Défaut : `1` (`0` avec Seyès). |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `0.6pt` (`0pt` avec Seyès). |  |
| `arc` | `auto` | length | rayon des coins. Défaut : `1mm`. |  |
| `sharp-corners` | `auto` | bool | coins vifs. |  |
| `boxsep` | `auto` | length | marge intérieure. Défaut : `7pt`. |  |
| `top` | `auto` | length | marge haute en plus. Défaut : `0pt` (`1mm` avec Seyès). |  |
| `bottom` | `auto` | length | marge basse en plus. Défaut : `0pt`. |  |
| `left` | `auto` | length | marge gauche en plus. Défaut : `0pt`. |  |
| `right` | `auto` | length | marge droite en plus. Défaut : `0pt`. |  |
| `middle` | `auto` | length | demi-écart entre les deux parties. Défaut : `0pt`. |  |
| `frame-hidden` | `auto` | bool | cadre caché. Défaut : `false` (`true` avec Seyès). |  |
| `colbacklower` | `auto` | color, str, none | fond de la partie basse. |  |
| `opacitybacklower` | `auto` | float | opacité du fond de la partie basse. |  |
| `colbacktitle` | `auto` | color, str | fond du titre. Défaut : `gray!30`. |  |
| `coltitle` | `auto` | color, str | couleur du titre. Défaut : `black`. |  |
| `fonttitle` | `auto` | dictionary, str, function | police du titre. Défaut : grand et gras. |  |
| `height` | `auto` | length | hauteur imposée. Défaut : `auto`. |  |
| `halign` | `auto` | str | `"justify"`, `"left"`, `"center"`, `"right"` (partie haute). Défaut : `"justify"`. |  |
| `halign-lower` | `auto` | str | alignement de la partie basse. Défaut : `"justify"`. |  |
| `valign` | `auto` | str | `"top"`, `"center"`, `"bottom"`. Défaut : `"top"`. |  |
| `lefthand-width` | `auto` | length | largeur de la partie gauche (modes left/right). |  |
| `righthand-width` | `auto` | length | largeur de la partie droite (modes left/right). |  |
| `sidebyside-gap` | `auto` | length | écart entre les parties côte à côte. Défaut : `0pt`. |  |
| `bicolor` | `auto` | bool | fond seulement sous la partie haute. |  |
| `before-skip` | `auto` | int, float, length | espace avant (nombre = fois l'interligne). Défaut : `0.25`. |  |
| `after-skip` | `auto` | int, float, length | espace après. Défaut : `0.5`. |  |
| `crep-num-veil` | `auto` | color | voile de `show-crep-num` (ajout). Défaut : blanc à 80 %. |  |
| `crep-num-fill` | `auto` | color | fond de la pastille (ajout). Défaut : `black!70`. |  |
| `crep-num-color` | `auto` | color | couleur du numéro (ajout). Défaut : `white`. |  |
| `crep-num-size` | `auto` | str, length | taille du numéro (ajout). Défaut : `"tiny"`. |  |
| `seyes-unit` | `auto` | length | interligne Seyès (ajout). Défaut : `8mm`. |  |
| `seyes-thick` | `auto` | length | épaisseur des lignes épaisses (ajout). |  |
| `seyes-thin` | `auto` | length | épaisseur des lignes fines (ajout). |  |
| `seyes-shift` | `auto` | length | décalage des lignes (ajout). |  |
| `seyes-subdivisions` | `auto` | int | intervalles par ligne (ajout). Défaut : `4`. |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..parties` | (positionnel) | content |  | la réponse ; avec deux contenus : partie haute puis partie basse. |

Exemple :

```typ
#crep(extra-lines: 1)[Le triangle est rectangle en $A$.]
#crep(seyes: false, crep-mode: "lower")[Énoncé visible.][Réponse.]
```

## tccrep

```typ
tccrep(style: auto, auto-factor: auto, seyes: auto, seyes-colors: auto, dotfill: auto, normal-crep: auto, show-crep-num: auto, crep-align: auto, crep-opaq: auto, bbox: auto, tccrep-box: auto, maths: auto, width: auto, colback: auto, colframe: auto, opacityback: auto, boxrule: auto, arc: auto, sharp-corners: auto, boxsep: auto, top: auto, bottom: auto, left: auto, right: auto, frame-hidden: auto, crep-num-veil: auto, crep-num-fill: auto, crep-num-color: auto, crep-num-size: auto, seyes-unit: auto, seyes-thick: auto, seyes-thin: auto, seyes-shift: auto, seyes-subdivisions: auto, largeur, corps)
```

Boîte réponse en ligne de largeur fixe (`\tccrep[options]{largeur}{réponse}`), contenu centré. Avec `auto` à la place de la largeur, la largeur est automatique (`\tcautocrep`) : `auto-factor` × largeur naturelle de la réponse (la même en version élève).

LaTeX : `\tccrep`

Clés communes acceptées (voir en tête) : `bottom`, `left`, `right`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `style` | `auto` | str, array | style(s) nommé(s). | crep/seyesrep style |
| `auto-factor` | `auto` | int, float | facteur de la largeur automatique (`largeur: auto`). Défaut : réglage de `setrdcrep` (`2`). | auto factor |
| `seyes` | `auto` | bool | lignes Seyès. Défaut : réglage de `setrdcrep`. | seyes |
| `seyes-colors` | `auto` | color, array | couleurs des lignes Seyès. | seyes colors |
| `dotfill` | `auto` | bool | côté élève, remplit la boîte avec `dotfill-command` (pointillés). Défaut : `false`. | dotfill |
| `normal-crep` | `auto` | bool | contenu affiché normalement. Défaut : `false`. | normal crep |
| `show-crep-num` | `auto` | bool | voile et numéro. Défaut : `false`. | show crep num |
| `crep-align` | `auto` | str | `"default"`, `"center"`, `"left"`, `"right"`. Défaut : `"default"` (centré). | crep align |
| `crep-opaq` | `auto` | bool | boîte opaque. Défaut : `false`. | crep opaq |
| `bbox` | `auto` | array, none | `(bas, haut)` : agrandit la boîte. | bbox |
| `tccrep-box` | `auto` | dictionary | style par numéro : `("42": (colback: yellow))`. |  |
| `maths` | `auto` | bool | la réponse est une formule (sans `$`). Défaut : `false`. |  |
| `width` | `auto` | length | remplace la largeur. | width |
| `colback` | `auto` | color, str | fond. Défaut : `gray!10`. |  |
| `colframe` | `auto` | color, str | couleur du cadre (si `frame-hidden: false`). |  |
| `opacityback` | `auto` | float | opacité du fond. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `0pt`. |  |
| `arc` | `auto` | length | coins. Défaut : `0pt`. |  |
| `sharp-corners` | `auto` | bool | coins vifs. |  |
| `boxsep` | `auto` | length | marge intérieure. Défaut : `5pt`. |  |
| `top` | `auto` | length | marge haute. Défaut : `0pt` (`1mm` avec Seyès). |  |
| `frame-hidden` | `auto` | bool | cadre caché. Défaut : `true`. |  |
| `crep-num-veil` | `auto` | color | voile du numéro (ajout). |  |
| `crep-num-fill` | `auto` | color | fond de la pastille (ajout). |  |
| `crep-num-color` | `auto` | color | couleur du numéro (ajout). |  |
| `crep-num-size` | `auto` | str, length | taille du numéro (ajout). |  |
| `seyes-unit` | `auto` | length | interligne Seyès (ajout). |  |
| `seyes-thick` | `auto` | length | lignes épaisses (ajout). |  |
| `seyes-thin` | `auto` | length | lignes fines (ajout). |  |
| `seyes-shift` | `auto` | length | décalage des lignes (ajout). |  |
| `seyes-subdivisions` | `auto` | int | intervalles par ligne (ajout). |  |
| `largeur` | (positionnel) | length, ratio, auto | largeur de la boîte (premier argument LaTeX) ; `auto` : largeur automatique. |  |
| `corps` | (positionnel) | content | la réponse. |  |

Exemple :

```typ
Le carré de $3$ vaut #tccrep(1.5cm)[$9$].
Des #tccrep(auto)[boîtes] dont la #tccrep(auto, auto-factor: 1)[largeur] est automatique.
```

## tcfillcrep

```typ
tcfillcrep(style: auto, seyes: auto, seyes-colors: auto, dotfill: auto, normal-crep: auto, show-crep-num: auto, crep-align: auto, crep-opaq: auto, bbox: auto, tccrep-box: auto, maths: auto, colback: auto, colframe: auto, opacityback: auto, boxrule: auto, arc: auto, boxsep: auto, top: auto, bottom: auto, left: auto, right: auto, frame-hidden: auto, corps)
```

Boîte réponse qui occupe le reste de la ligne (`\tcfillcrep[options]{réponse}`), contenu à gauche. Vide, c'est le trait pointillé de `\dotfills` : `#tcfillcrep[]`.

LaTeX : `\tcfillcrep`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `style` | `auto` | str, array | style(s) nommé(s). | crep/seyesrep style |
| `seyes` | `auto` | bool | lignes Seyès. | seyes |
| `seyes-colors` | `auto` | color, array | couleurs des lignes Seyès. | seyes colors |
| `dotfill` | `auto` | bool | pointillés côté élève. | dotfill |
| `normal-crep` | `auto` | bool | contenu affiché normalement. | normal crep |
| `show-crep-num` | `auto` | bool | voile et numéro. | show crep num |
| `crep-align` | `auto` | str | alignement (`"default"` = gauche). | crep align |
| `crep-opaq` | `auto` | bool | boîte opaque. | crep opaq |
| `bbox` | `auto` | array, none | `(bas, haut)`. | bbox |
| `tccrep-box` | `auto` | dictionary | style par numéro. |  |
| `maths` | `auto` | bool | la réponse est une formule. |  |
| `colback` | `auto` | color, str | fond. |  |
| `colframe` | `auto` | color, str | cadre. |  |
| `opacityback` | `auto` | float | opacité du fond. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. |  |
| `arc` | `auto` | length | coins. |  |
| `boxsep` | `auto` | length | marge intérieure. |  |
| `top` | `auto` | length | marge haute. |  |
| `bottom` | `auto` | length | marge basse. |  |
| `left` | `auto` | length | marge gauche. |  |
| `right` | `auto` | length | marge droite. |  |
| `frame-hidden` | `auto` | bool | cadre caché. |  |
| `corps` | (positionnel) | content | la réponse. |  |

Exemple :

```typ
Nom : #tcfillcrep[] \
Le périmètre vaut #tcfillcrep[12 cm].
```

## repsim

```typ
repsim(largeur: 1.5cm, ..options, corps)
```

Petite boîte en ligne (`\repsim[largeur]{réponse}`) : une tccrep.

LaTeX : `\repsim`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `largeur` | `1.5cm` | length | largeur. Défaut : `1.5cm`. |  |
| `corps` | (positionnel) | content | la réponse. |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `tccrep`. |

Exemple :

```typ
$x = #repsim[$3$]$
```

## tcfraccrep

```typ
tcfraccrep(width: auto, crep-for: auto, crep-style: auto, crep-num-style: auto, crep-den-style: auto, num, den)
```

Fraction à trous (`\tcfraccrep[options]{num}{den}`) : deux boîtes en ligne dans une fraction.

LaTeX : `\tcfraccrep`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `width` | `auto` | length | largeur de chaque boîte. Défaut : `0.7cm`. | width |
| `crep-for` | `auto` | str | `"both"`, `"num"` ou `"den"` : boîtes au numérateur, au dénominateur ou aux deux. Défaut : `"both"`. | frac/crep for |
| `crep-style` | `auto` | dictionary | clés de tccrep pour les deux boîtes. Défaut : `(:)`. | frac/crep style |
| `crep-num-style` | `auto` | dictionary | clés de tccrep pour la boîte du numérateur. |  |
| `crep-den-style` | `auto` | dictionary | clés de tccrep pour la boîte du dénominateur. |  |
| `num` | (positionnel) | content | numérateur. |  |
| `den` | (positionnel) | content | dénominateur. |  |

Exemple :

```typ
$1/2 = #tcfraccrep[2][4]$ et $3/4 = #tcfraccrep(crep-for: "den")[3][4]$
```

## seyesrep

```typ
seyesrep(..options, reponse, enonce)
```

Énoncé en haut, réponse sur lignes Seyès en bas, dans un cadre arrondi (`\begin{seyesrep}[options]{réponse} énoncé \end{seyesrep}`, style `"seyesrep style"`).

- ..options: toutes les clés de `crep` (elles l'emportent sur le style « seyesrep style »).

LaTeX : `\seyesrep`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `reponse` | (positionnel) | content | la réponse (premier argument LaTeX). |  |
| `enonce` | (positionnel) | content | l'énoncé (corps de l'environnement). |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | toutes les clés de `crep` (elles l'emportent sur le style « seyesrep style »). |

Exemple :

```typ
#seyesrep[$1/4$][Écrire $0,25$ sous forme de fraction.]
```

## assosbox

```typ
assosbox(box-right: auto, box-left: none, ..options, reponse, enonce)
```

Énoncé accompagné d'une case réponse accolée, à droite (défaut) ou à gauche (`\begin{assosbox}[options]{réponse} énoncé \end{assosbox}`).

LaTeX : `\assosbox`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `box-right` | `auto` | length, bool, auto | case à droite, de cette largeur. Défaut : `1.5cm`. | assosbox right |
| `box-left` | `none` | length, bool, none | case à gauche, de cette largeur (`true` : `1.5cm`). Défaut : `none`. | assosbox left |
| `reponse` | (positionnel) | content | la réponse (premier argument LaTeX). |  |
| `enonce` | (positionnel) | content | l'énoncé. |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | toutes les clés de `crep`. |

Exemple :

```typ
#assosbox[$25$][Quel est le carré de $5$ ?]
#assosbox(box-left: 2cm)[$14$][Quel est le double de $7$ ?]
```

## seyesfig

```typ
seyesfig(title: auto, boxrule: auto, colframe: auto, colback: auto, arc: auto, halign: auto, valign: auto, boxsep: auto, top: auto, bottom: auto, left: auto, right: auto, lefttitle: auto, fonttitle: auto, width: auto, height: auto, corps)
```

Figure encadrée aux couleurs Seyès (style `seyesfig` de rdcrep).

Clés communes acceptées (voir en tête) : `arc`, `valign`, `width`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `title` | `auto` | content, none | titre en gras. Défaut : `none`. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `1.128pt` TeX. |  |
| `colframe` | `auto` | color, str | cadre. Défaut : `seyescolA!90!black`. |  |
| `colback` | `auto` | color, str | fond. Défaut : `seyescolB!10`. |  |
| `halign` | `auto` | str | alignement horizontal. Défaut : `"center"`. |  |
| `boxsep` | `auto` | length | marge. Défaut : `2pt` TeX. |  |
| `top` | `auto` | length | marge haute en plus. Défaut : `4pt` TeX. |  |
| `bottom` | `auto` | length | marge basse en plus. Défaut : `4pt` TeX. |  |
| `left` | `auto` | length | marge gauche en plus. Défaut : `0pt`. |  |
| `right` | `auto` | length | marge droite en plus. Défaut : `0pt`. |  |
| `lefttitle` | `auto` | length | retrait du titre. Défaut : `0pt`. |  |
| `fonttitle` | `auto` | dictionary, str, function | police du titre. Défaut : gras. |  |
| `height` | `auto` | length, auto | hauteur. Défaut : `auto`. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#seyesfig(title: [Figure])[Un schéma à compléter.]
```

## dembox

```typ
dembox(demskin: auto, normal-dembox: auto, normal-crep: auto, width: auto, halign: auto, colback: auto, opacityback: auto, colframe: auto, coltext: auto, coltitle: auto, fonttitle: auto, boxrule: auto, top: auto, bottom: auto, left: auto, right: auto, title-boxsep: auto, tick-length: auto, corner-length: auto, titre, corps)
```

Étiquette de démonstration (`\dembox[options]{titre}{contenu}`) : « Ce que je sais », « Propriété », « Conclusion »… à la couleur de correction (noire avec `normal-crep` ou `normal-dembox`).

LaTeX : `\dembox`

Clés communes acceptées (voir en tête) : `width`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `demskin` | `auto` | str | `"regular"` (titre au-dessus), `"compact"` (titre à gauche) ou `"fiche"` (titre arrondi à cheval sur le bord haut, équerre en haut à gauche ). Défaut : `"regular"`. | dembox/demskin |
| `normal-dembox` | `auto` | bool | en noir, quelle que soit la version, sans dépendre de `normal-crep`. Défaut : `false`. | normal dembox |
| `normal-crep` | `auto` | bool | en noir, hors mode correctif. Défaut : `false`. | normal crep |
| `halign` | `auto` | str | alignement du contenu. Défaut : `"center"`. |  |
| `colback` | `auto` | color, str | fond (à `opacityback`). Défaut : `black`. |  |
| `opacityback` | `auto` | float | opacité du fond. Défaut : `0.05`. |  |
| `colframe` | `auto` | color, str | traits et étiquette. Défaut : couleur de correction. |  |
| `coltext` | `auto` | color, str | texte. Défaut : couleur de correction. |  |
| `coltitle` | `auto` | color, str | texte de l'étiquette. Défaut : `white`. |  |
| `fonttitle` | `auto` | dictionary, str, function | police de l'étiquette. Défaut : sans, `scriptsize`, gras (`tiny` avec `"fiche"`). |  |
| `boxrule` | `auto` | length | épaisseur des traits. Défaut : `1pt` TeX. |  |
| `top` | `auto` | length | marge haute. Défaut : `8pt` TeX. |  |
| `bottom` | `auto` | length | marge basse. Défaut : `4pt` TeX. |  |
| `left` | `auto` | length | marge gauche. Défaut : `6pt` TeX. |  |
| `right` | `auto` | length | marge droite. Défaut : `6pt` TeX. |  |
| `title-boxsep` | `auto` | length | marge de l'étiquette (ajout). Défaut : `2pt` TeX. |  |
| `tick-length` | `auto` | length | trait vertical en haut à gauche (ajout) ; avec `"fiche"`, aussi le trait horizontal et le décalage de l'étiquette. Défaut : `4mm` (`6mm` en compact). |  |
| `corner-length` | `auto` | length | équerre en bas à droite (ajout). Défaut : `4mm`. |  |
| `titre` | (positionnel) | content | titre de l'étiquette. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#dembox(width: 6cm)[Propriété :][Deux droites perpendiculaires à une même troisième sont parallèles.]
#dembox(demskin: "compact")[Conclusion :][$(A T) parallel (H S)$]
#dembox(demskin: "fiche", width: 8cm)[À retenir][Le carré d'un nombre est toujours positif.]
```

## crepbox

```typ
crepbox(lw: auto, inner-left-sep: auto, left-align: auto, crep-style: auto, colback: auto, colframe: auto, coltext: auto, fontupper: auto, boxrule: auto, boxsep: auto, arc: auto, opacityback: auto, opacityframe: auto, largeur, etiquette, corps)
```

Boîte réponse Seyès précédée d'une étiquette (`\crepbox[options]{largeur}{étiquette}{réponse}`) : une `tccrep` Seyès de la largeur donnée, dans un cadre dont la partie gauche porte l'étiquette (« Réponse : », « x = »…). Elle se pose sur la ligne de base de la réponse.

LaTeX : `\crepbox`

Clés communes acceptées (voir en tête) : `arc`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `lw` | `auto` | length | largeur de la zone d'étiquette ; `0pt` : celle de l'étiquette entourée de `inner-left-sep`. Défaut : `0pt`. |  |
| `inner-left-sep` | `auto` | length | marge de part et d'autre de l'étiquette. Défaut : `1em`. |  |
| `left-align` | `auto` | str | `"center"`, `"left"`, `"right"` : alignement de l'étiquette. Défaut : `"center"`. |  |
| `crep-style` | `auto` | dictionary | clés de `tccrep` pour la boîte réponse (la boîte est `seyes: true`). Défaut : `(:)`. | frac/crep style |
| `colback` | `auto` | color, str | fond de l'étiquette. Défaut : `white`. |  |
| `colframe` | `auto` | color, str | cadre. Défaut : `black!75`. |  |
| `coltext` | `auto` | color, str | couleur de l'étiquette. Défaut : `black`. |  |
| `fontupper` | `auto` | dictionary, str, function, none | police de l'étiquette. Défaut : `none`. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `0.7pt` TeX. |  |
| `boxsep` | `auto` | length | marge entre le cadre et la boîte réponse. Défaut : `2pt` TeX. |  |
| `opacityback` | `auto` | float | opacité du fond de l'étiquette. Défaut : `1`. |  |
| `opacityframe` | `auto` | float | opacité du cadre. Défaut : `1`. |  |
| `largeur` | (positionnel) | length | largeur de la boîte réponse (et non de la boîte finale). |  |
| `etiquette` | (positionnel) | content | texte de la zone gauche. |  |
| `corps` | (positionnel) | content | la réponse. |  |

Exemple :

```typ
Le périmètre : #crepbox(3cm)[Réponse][12 cm] et l'aire : #crepbox(2cm, colback: yellow.lighten(60%))[$A =$][$9$].
```

## correction-box

```typ
correction-box(corps)
```

Texte de correction (`\CorrectionBox{x}`) : en version professeur, `x` dans la couleur et la police de correction ; en version élève, la même place, invisible (`\phantom`). C'est la façon d'écrire une réponse « en rose » au milieu d'un énoncé sans zone de réponse.

LaTeX : `\CorrectionBox`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte (ou la formule) de correction. |  |

Exemple :

```typ
Le périmètre vaut #correction-box[12 cm] et l'aire #correction-box[$9 "cm"^2$].
```

## crepcorrectionfont

```typ
crepcorrectionfont(corps)
```

La police de correction seule, sans sa couleur (`\crepcorrectionfont`), dans les deux versions : pour écrire un texte comme une réponse (grand, gras par défaut) sans la colorer.

LaTeX : `\crepcorrectionfont`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte. |  |

Exemple :

```typ
Réponse attendue : #crepcorrectionfont[Pythagore].
```

## seyestab

```typ
seyestab(largeur: auto, skip: auto, vlines: auto, hlines: auto, rules-width: auto, rules-color: auto, tabcolsep: auto, strut-height: auto, strut-depth: auto, spec, ..cellules)
```

Tableau dont chaque rangée occupe une ligne Seyès (`\begin{seyestab}{colonnes} … \end{seyestab}`) ; sa première rangée est sur la ligne de base du texte. Avec `largeur:`, les colonnes `X` se partagent la largeur donnée. Dans une crep Seyès, le tableau ne prend pas de place verticale : sauter les lignes qu'il occupe avec `skip:`. Filets : clés `vlines` et `hlines`, ou `table.hline()` entre les rangées.

LaTeX : `\seyestab`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `largeur` | `auto` | length, ratio, none | largeur du tableau (colonnes `X`). Défaut : `none` (largeur naturelle). |  |
| `skip` | `auto` | int, float | lignes Seyès à sauter après le tableau, en zone Seyès. Défaut : `0`. |  |
| `vlines` | `auto` | bool, array | filets verticaux (tous, ou leurs positions). Défaut : `false`. |  |
| `hlines` | `auto` | bool, array | filets horizontaux (tous, ou leurs positions). Défaut : `false`. |  |
| `rules-width` | `auto` | length | épaisseur des filets (`rules/width`). Défaut : `0.4pt` TeX. |  |
| `rules-color` | `auto` | color, str | couleur des filets. Défaut : `black`. |  |
| `tabcolsep` | `auto` | length | demi-écart entre colonnes. Défaut : `6pt` TeX. |  |
| `strut-height` | `auto` | length | hauteur d'une rangée au-dessus de la ligne de base. Défaut : `5mm`. |  |
| `strut-depth` | `auto` | length | profondeur d'une rangée. Défaut : `3mm`. |  |
| `spec` | (positionnel) | str | colonnes à la LaTeX : `l`, `c`, `r`, `X`, `X[c]`, `p{3cm}`, `\|` (filet vertical). |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cellules` | (positionnel) | content |  | les cellules, rangée par rangée, et des filets `table.hline()`. |

Exemple :

```typ
#crep[Un tableau : #seyestab("lcc", vlines: true, table.hline(), [Ligne 1], [a], [b], table.hline(), [Ligne 2], [c], [d], table.hline(), skip: 2)
Après.]
#seyestab("XX[c]X[c]", largeur: 10cm, hlines: true, [Ligne 1], [a], [b], [Ligne 2], [c], [d])
```

## seyesarray

```typ
seyesarray(delims: auto, skip: auto, vlines: auto, hlines: auto, rules-width: auto, rules-color: auto, arraycolsep: auto, strut-height: auto, strut-depth: auto, spec, ..cellules)
```

Tableau mathématique Seyès (`\begin{seyesarray}{colonnes}`, NiceArray) : cellules en mode maths. Avec `delims:`, c'est le `seyesarraydelims` de rdcrep : le tableau est entouré de délimiteurs.

LaTeX : `\seyesarray`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `delims` | `auto` | array, none | délimiteurs `(gauche, droite)` parmi `"("`, `")"`, `"["`, `"]"`, `"{"`, `"}"`, `"\|"` ; `"."` : aucun. Défaut : `none`. |  |
| `skip` | `auto` | int, float | lignes Seyès à sauter après le tableau, en zone Seyès. Défaut : `0`. |  |
| `vlines` | `auto` | bool, array | filets verticaux. |  |
| `hlines` | `auto` | bool, array | filets horizontaux. |  |
| `rules-width` | `auto` | length | épaisseur des filets. |  |
| `rules-color` | `auto` | color, str | couleur des filets. |  |
| `arraycolsep` | `auto` | length | demi-écart entre colonnes. Défaut : `5pt` TeX. |  |
| `strut-height` | `auto` | length | hauteur d'une rangée. |  |
| `strut-depth` | `auto` | length | profondeur d'une rangée. |  |
| `spec` | (positionnel) | str | colonnes. |  |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cellules` | (positionnel) | content |  | les cellules. |

Exemple :

```typ
$ #seyesarray("rcl", $f(x)$, $=$, $2x - 1$, $g(x)$, $=$, $-3x + 5$) $
$ #seyesarray("l", delims: ("{", "."), $f(x) = 2x - 1$, $g(x) = -3x + 5$) $
```

## checkbox

```typ
checkbox(style: auto, width: auto, color: auto, opacity: auto, background-color: auto, background-opacity: auto, background-style: auto, checked: auto, checked-corr: auto, skin: auto, fill-style: auto, check-mark: auto, mark-color: auto, mark-overlay: auto, mark-scale: auto, mark-opacity: auto, mark-style: auto, mark-preaction: auto, raise: auto)
```

Une case à cocher ou un bouton radio vectoriel (`\checkbox[options]`), posé sur la ligne de base. Défauts réglables : `setrdcrep(pour: "checkbox", …)`, styles nommés : `setrdcrep(definir: "nom", pour: "checkbox", …)`.

LaTeX : `\checkbox`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `width` | `auto` | length | largeur. Défaut : `0.9em`. | width |
| `color` | `auto` | color, str, none | couleur de la case. Défaut : `black`. | color |
| `opacity` | `auto` | float | opacité de la case. Défaut : `1`. | opacity |
| `background-color` | `auto` | color, str, none | fond. Défaut : `none`. | background color |
| `background-opacity` | `auto` | float | opacité du fond. Défaut : `1`. | background opacity |
| `background-style` | `auto` | color, gradient, dictionary, none | peinture du fond (remplace `background-color`). Défaut : `none`. | background style |
| `checked` | `auto` | bool | case cochée. Défaut : `false`. | checked |
| `checked-corr` | `auto` | bool | cochée en version professeur seulement. Défaut : `false`. | checked corr |
| `skin` | `auto` | str | `"square"`, `"squareshadow"`, `"squarerounded"`, `"squareshadowrounded"`, `"circle"`, `"circleshadowA"`, `"circleshadowB"`. Défaut : `"squareshadow"`. | skin |
| `fill-style` | `auto` | color, gradient, dictionary, none | peinture de la case (remplace `color`). Défaut : `none`. | fill style |
| `check-mark` | `auto` | str, content | `"mark1"` … `"mark14"`, `"square"`, `"hollowsquare"`, `"squarerounded"`, `"hollowsquarerounded"`, `"disc"`, `"smalldisc"`, `"hollowdisc"`, ou un contenu. Défaut : `"mark1"`. | check mark |
| `mark-color` | `auto` | color, str, none | couleur de la marque. Défaut : `red`. | mark color |
| `mark-overlay` | `auto` | bool | la marque déborde sans prendre de place. Défaut : `true`. | mark overlay |
| `mark-scale` | `auto` | int, float | échelle de la marque. Défaut : `1`. | mark scale |
| `mark-opacity` | `auto` | float | opacité de la marque. Défaut : `1`. | mark opacity |
| `mark-style` | `auto` | color, gradient, dictionary, none | peinture de la marque. Défaut : `none`. | mark style |
| `mark-preaction` | `auto` | stroke, none | trait dessiné sous la marque (`3pt + white`). Défaut : `none`. | mark preaction |
| `raise` | `auto` | length | décalage vertical. Défaut : `0pt`. | /chkbox/raise |

Exemple :

```typ
Une case #checkbox() cochée #checkbox(checked: true) ronde #checkbox(skin: "circle", check-mark: "disc", checked: true).
#setrdcrep(pour: "checkbox", color: blue, skin: "squarerounded")
#setrdcrep(definir: "sbr", pour: "checkbox", width: 1.3em, skin: "circleshadowA", color: blue)
Réglée : #checkbox() #checkbox(checked: true) bouton radio : #checkbox(style: "sbr")
```

## tcbcheckbox

```typ
tcbcheckbox(style: auto, xsep: auto, ysep: auto, sep: auto, checked-corr: auto, checkbox-auto-color: auto, checkbox: auto, colframe: auto, colback: auto, opacityback: auto, opacityframe: auto, halign: auto, valign: auto, boxsep: auto, boxrule: auto, arc: auto, top: auto, bottom: auto, left: auto, right: auto, width: auto, height: auto, corps)
```

Boîte avec une case dans son coin supérieur gauche (environnement `tcbcheckbox`). Défauts réglables : `setrdcrep(pour: "tcbcheckbox", …)` ; la case suit `setrdcrep(pour: "checkbox", …)`.

LaTeX : `\tcbcheckbox`

Clés communes acceptées (voir en tête) : `style`, `colframe`, `valign`, `bottom`, `left`, `right`, `width`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `xsep` | `auto` | length | écart horizontal entre la case et le cadre. Défaut : `3pt` TeX. |  |
| `ysep` | `auto` | length | écart vertical. Défaut : `3pt` TeX. |  |
| `sep` | `auto` | length | les deux à la fois. |  |
| `checked-corr` | `auto` | bool | case cochée en version professeur. Défaut : `false`. | checked corr |
| `checkbox-auto-color` | `auto` | bool | la case prend la couleur du fond. Défaut : `false`. | tcbcheckbox/checkbox auto color |
| `checkbox` | `auto` | dictionary | clés de `checkbox` pour la case. Défaut : `(:)`. | tcbcheckbox/checkbox |
| `colback` | `auto` | color, str | fond. Défaut : `white`. |  |
| `opacityback` | `auto` | float | opacité du fond. Défaut : `0`. |  |
| `opacityframe` | `auto` | float | opacité du cadre. Défaut : `1`. |  |
| `halign` | `auto` | str | alignement du contenu. Défaut : `"center"`. |  |
| `boxsep` | `auto` | length | marge. Défaut : `3pt` TeX. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `0.7pt` TeX. |  |
| `arc` | `auto` | length | coins. Défaut : `0pt`. |  |
| `top` | `auto` | length | marge haute. Défaut : `0pt`. |  |
| `height` | `auto` | length, auto | hauteur minimale. Défaut : `auto`. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#tcbcheckbox(width: 6cm)[Une boîte \ avec une case à cocher]
#setrdcrep(pour: "tcbcheckbox", boxrule: 2pt, checkbox: (color: blue, check-mark: "mark8"))
#tcbcheckbox(checked-corr: true, width: 5cm)[Choix n° 2]
```

## tccheckbox

```typ
tccheckbox(style: auto, left-width: auto, background: auto, check-color: auto, check-mark: auto, mark-scale: auto, checked: auto, checked-corr: auto, on-line: auto, colback: auto, opacityback: auto, colframe: auto, boxrule: auto, arc: auto, boxsep: auto, top: auto, bottom: auto, left: auto, right: auto, width: auto, height: auto, halign: auto, valign: auto, corps)
```

Boîte à cocher sensible au mode correctif (`\tccheckbox[options]{contenu}`) : une bande colorée à gauche reçoit la marque (en couleur de correction) quand la boîte est cochée.

LaTeX : `\tccheckbox`

Clés communes acceptées (voir en tête) : `style`, `colframe`, `arc`, `bottom`, `left`, `right`, `width`, `valign`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `left-width` | `auto` | length | largeur de la bande de gauche. Défaut : `1.5em`. | crep/checkbox/left width |
| `background` | `auto` | color, str | couleur de la bande. Défaut : `seyescolA!20`. | crep/checkbox/background |
| `check-color` | `auto` | color, str | couleur de la marque. Défaut : couleur de correction. | crep/checkbox/check color |
| `check-mark` | `auto` | str, content | marque (nom de marque de checkbox, ou contenu). Défaut : `"mark2"` (✔). | check mark |
| `mark-scale` | `auto` | int, float | échelle de la marque (ajout). Défaut : `1`. | mark scale |
| `checked` | `auto` | bool | cochée. Défaut : `false`. | checked |
| `checked-corr` | `auto` | bool | cochée en version professeur. Défaut : `false`. | checked corr |
| `on-line` | `auto` | bool | boîte en ligne (posée sur la ligne de base). Défaut : `false`. |  |
| `colback` | `auto` | color, str | fond. Défaut : `white`. |  |
| `opacityback` | `auto` | float | opacité du fond. Défaut : `0`. |  |
| `boxrule` | `auto` | length | épaisseur du cadre. Défaut : `0.5pt` TeX. |  |
| `boxsep` | `auto` | length | marge. Défaut : `3pt` TeX. |  |
| `top` | `auto` | length | marge haute. Défaut : `0pt`. |  |
| `height` | `auto` | length, auto | hauteur minimale. Défaut : `auto`. |  |
| `halign` | `auto` | str | alignement du contenu. Défaut : `"left"`. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#tccheckbox(checked-corr: true)[Oui]
Une boîte isolée : #tccheckbox(checked: true, on-line: true, width: 4cm, halign: "center")[Toute seule]
```

## tccheckboxlist

```typ
tccheckboxlist(columns: auto, col-skip: auto, row-skip: auto, checked: auto, checked-corr: auto, raster: auto, checkbox-style: auto, checked-style: auto, checkbox: auto, ..elements)
```

Liste de boîtes à cocher en colonnes (`\tccheckboxlist[options]{Bleu, Rouge, …}`) : un contenu par élément (ou un tableau). Les clés de `tccheckbox` passées ici s'appliquent à toutes les boîtes.

LaTeX : `\tccheckboxlist`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `columns` | `auto` | int | nombre de colonnes ; `0` : une par élément. Défaut : `0`. |  |
| `col-skip` | `auto` | length | écart entre colonnes. Défaut : `2mm`. |  |
| `row-skip` | `auto` | length | écart entre rangées. Défaut : `2mm`. |  |
| `checked` | `auto` | int, array | numéro(s) des boîtes cochées. Défaut : `()`. | checked |
| `checked-corr` | `auto` | int, array | numéro(s) cochés en version professeur. Défaut : `()`. | checked corr |
| `raster` | `auto` | dictionary | clés de `tccheckbox` pour toutes les boîtes (options du tcbraster). Défaut : `(:)`. |  |
| `checkbox-style` | `auto` | dictionary | style commun des boîtes. Défaut : `(:)`. |  |
| `checked-style` | `auto` | dictionary | style des boîtes cochées. Défaut : `(:)`. |  |
| `checkbox` | `auto` | dictionary | style par numéro : `("2": (colframe: blue))` (`checkbox n`). Défaut : `(:)`. | tcbcheckbox/checkbox |

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..elements` | (positionnel) | content |  | les éléments (et, en clés nommées, des clés de `tccheckbox`). |

Exemple :

```typ
#tccheckboxlist(columns: 2, checked-corr: 3)[Bleu][Rouge][Jaune][Vert]
```

## cb

```typ
cb(..options)
```

Case vide de bfcours (`\cb` = `\checkbox[check mark=mark14, skin=squareshadow]`).

- ..options: clés de `checkbox`.

LaTeX : `\cb`

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `checkbox`. |

Exemple :

```typ
#cb() Option A #h(1em) #cb() Option B
```

## ccb

```typ
ccb(..options)
```

Case cochée en version professeur (`\ccb` = `\cb` + `checked corr`).

- ..options: clés de `checkbox`.

LaTeX : `\ccb`

Clés documentées dans le guide (`farfadet-crep/docs/fiches.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `checkbox`. |

Exemple :

```typ
#cb() Faux #h(1em) #ccb() Vrai
```

## mysquare

```typ
mysquare()
```

Case carrée blanche à cadre noir épais (`\mysquare`).

LaTeX : `\mysquare`

Exemple :

```typ
#mysquare() Vrai #h(1em) #mysquare() Faux
```
