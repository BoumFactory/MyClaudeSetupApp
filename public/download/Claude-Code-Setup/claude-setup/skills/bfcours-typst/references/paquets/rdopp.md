# rdopp

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-opp` puis `#import rd-opp: *`.
- Réglage : `setrdopp` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdopp.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdopp`).

## Sommaire

- `rdopp` — `rdopp[options]{nombres}` : pose et effectue une opération « à la française » : addition (à plusieurs termes), soustraction, multiplication…
- `setrdopp` — `setrdopp{clés}` : le réglage de `rdopp`, sous ses quatre formes (mêmes clés que `rdopp`).

## rdopp

```typ
rdopp(operation: auto, add: auto, sub: auto, mul: auto, div: auto, divint: auto, precision: auto, add-symbol: auto, sub-symbol: auto, mul-symbol: auto, decimal-sep: auto, carry: auto, carry-font: auto, carry-style: auto, top-carry-style: auto, bot-carry-style: auto, zero: auto, zero-style: auto, intermediary: auto, mul-zero-lines: auto, offset-char: auto, bridge: auto, bridge-style: auto, hbar: auto, vbar: auto, vbar-leftsep: auto, vbar-rightsep: auto, vbar-sep: auto, correction: auto, seyes: auto, cell-width: auto, cell-height: auto, cell-depth: auto, lw: auto, bar-style: auto, subbar-style: auto, grid: auto, grid-width: auto, grid-color: auto, cell: auto, baseline: auto, matrix: auto, tikz: auto, matrix-name: auto, row-sep: auto, column-sep: auto, matrix-inset: auto, overlay: auto, style: auto, ..nombres)
```

`rdopp[options]{nombres}` : pose et effectue une opération « à la française » : addition (à plusieurs termes), soustraction, multiplication ou division, avec retenues, zéros ajoutés, grille, mise en page Séyès, et masquage de la solution en version élève.

Les nombres s'écrivent comme une seule chaîne `"12.5, 3.45"` (la virgule sépare les nombres), comme un tableau `(12.5, 3.45)` ou comme plusieurs arguments `12.5, 3.45` (chaînes, entiers, décimaux ; la chaîne `"12,5"` seule est lue comme deux nombres). Pour les décimaux, le point est recommandé ; une chaîne garde les zéros finals (`"2.50"`). La soustraction attend le plus grand nombre en premier ; la division, un diviseur entier. Les clés `add`, `sub`, `mul`, `div` et `divint` sont des raccourcis de `operation` ; si plusieurs sont vraies, `divint` l'emporte sur `div`, puis `mul`, `sub`, `add`.

Les STYLES (clés `carry-style`, `zero-style`, `bar-style`, `matrix`, `cell`…) sont un dictionnaire `(text: red, fill: "yellow!50", draw: blue, line-width: 1pt, font: (weight: "bold")…)`, une fonction `c => …` ou un tableau de styles.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `operation` | `auto` | auto, str | `"add"`, `"sub"`, `"mul"`, `"div"` (ou `"addition"`, `"soustraction"`, `"multiplication"`). Défaut : `"add"`. | operation |
| `add` | `auto` | auto, bool | raccourci de `operation: "add"` (style LaTeX `add`). Défaut : `false`. | add (style) |
| `sub` | `auto` | auto, bool | raccourci de `operation: "sub"` (style LaTeX `sub`). Défaut : `false`. | sub (style) |
| `mul` | `auto` | auto, bool | raccourci de `operation: "mul"` (style LaTeX `mul`). Défaut : `false`. | mul (style) |
| `div` | `auto` | auto, bool | raccourci de `operation: "div"` (style LaTeX `div`). Défaut : `false`. | div (style) |
| `divint` | `auto` | auto, bool | division euclidienne : `operation: "div"` et `precision: 0` (style LaTeX `divint`). Défaut : `false`. | divint (style) |
| `precision` | `auto` | auto, int | nombre maximal de décimales du quotient (la division s'arrête avant si le reste est nul). Défaut : `2`. | precision |
| `add-symbol` | `auto` | auto, content | signe de l'addition (et des lignes ajoutées de la multiplication). Défaut : `$+$`. |  |
| `sub-symbol` | `auto` | auto, content | signe de la soustraction. Défaut : `$-$`. | sub symbol |
| `mul-symbol` | `auto` | auto, content | signe de la multiplication. Défaut : `$times$`. | mul symbol |
| `decimal-sep` | `auto` | auto, content | séparateur décimal affiché. Défaut : `[,]`. | decimal sep |
| `carry` | `auto` | auto, bool | affiche les retenues (addition, soustraction, multiplication). Défaut : `false`. | carry |
| `carry-font` | `auto` | auto, dictionary, str, length, function, none | police des retenues : taille LaTeX (`"scriptsize"`), dictionnaire `(size: …, weight: …)`, longueur ou fonction. Défaut : `"tiny"`. | carry font |
| `carry-style` | `auto` | auto, dictionary, function, array, none | style de toutes les retenues. Défaut : `none`. | carry style |
| `top-carry-style` | `auto` | auto, dictionary, function, array, none | style des retenues du haut (emprunts de la soustraction), en plus de `carry-style`. Défaut : `none`. | top carry style |
| `bot-carry-style` | `auto` | auto, dictionary, function, array, none | style des retenues du bas (remboursements de la soustraction), en plus de `carry-style`. Défaut : `none`. | bot carry style |
| `zero` | `auto` | auto, bool | écrit les zéros ajoutés pour aligner les décimales (addition, soustraction). Défaut : `false`. |  |
| `zero-style` | `auto` | auto, dictionary, function, array, none | style des zéros ajoutés. Défaut : `none`. |  |
| `intermediary` | `auto` | auto, bool | affiche les calculs intermédiaires (multiplication : produits partiels ; division : soustractions). Défaut : `true`. | intermediary |
| `mul-zero-lines` | `auto` | auto, bool | garde les lignes de zéros quand un chiffre du multiplicateur est nul. Défaut : `false`. | mul zero lines |
| `offset-char` | `auto` | auto, content, none | caractère écrit dans le décalage vers la gauche des produits partiels. Défaut : `none`. | offset char |
| `bridge` | `auto` | auto, bool | dessine un pont (arc) au-dessus du premier dividende partiel de la division. Défaut : `false`. | bridge |
| `bridge-style` | `auto` | auto, dictionary, function, array, none | style du pont (`bend` : courbure en degrés, 30 par défaut). Défaut : `none`. | bridge style |
| `hbar` | `auto` | auto, int, str | longueur du trait de la division, en chiffres (`"auto"` : le diviseur ou le quotient, le plus long) ; pour les autres opérations, décalage du début du trait (`"auto"` : 0). Défaut : `"auto"`. | hbar |
| `vbar` | `auto` | auto, int, str | hauteur de la potence de la division, en lignes (`"auto"` : 4 lignes au plus ; `"max"` : toutes). Défaut : `"auto"`. | vbar |
| `vbar-leftsep` | `auto` | auto, length, none | espace entre le dernier chiffre du dividende et la potence. Défaut : `none` (1ex ou `vbar-sep`). | vbar leftsep |
| `vbar-rightsep` | `auto` | auto, length, none | espace entre la potence et le diviseur. Défaut : `none` (1ex ou `vbar-sep`). | vbar rightsep |
| `vbar-sep` | `auto` | auto, length, none | fixe en une fois `vbar-leftsep` et `vbar-rightsep` ; ces deux clés l'emportent si elles sont données. Défaut : `none`. | vbar sep |
| `correction` | `auto` | auto, bool | n'affiche que l'énoncé en version élève, et la résolution complète, colorée, en version professeur. Défaut : `false`. | correction |
| `seyes` | `auto` | auto, bool | dimensions des cellules pour une zone de réponse Séyès (2,4ex × 6mm + 2mm) ; les clés `cell-width`, `cell-height` et `cell-depth` écrites sur l'appel l'emportent. Défaut : `false`. | seyes (style) |
| `cell-width` | `auto` | auto, length | largeur minimale d'une cellule (2ex). Défaut : `0.8667em`. | cell width |
| `cell-height` | `auto` | auto, length | hauteur d'une cellule au-dessus de la ligne de base (2ex). Défaut : `0.8667em`. | cell height |
| `cell-depth` | `auto` | auto, length | profondeur d'une cellule sous la ligne de base (0,5ex). Défaut : `0.2167em`. | cell depth |
| `lw` | `auto` | auto, length | épaisseur par défaut des traits principaux (barres, potence, pont). Défaut : `0.8pt`. | lw |
| `bar-style` | `auto` | auto, dictionary, function, array, none | style des traits principaux (résultat, potence de la division). Défaut : `none`. | bar style |
| `subbar-style` | `auto` | auto, dictionary, function, array, none | style des petits traits des soustractions intermédiaires de la division. Défaut : `none`. | subbar style |
| `grid` | `auto` | auto, bool | trace une grille autour de chaque cellule. Défaut : `false`. | grid |
| `grid-width` | `auto` | auto, length | épaisseur des traits de la grille. Défaut : `0.4pt`. | grid width |
| `grid-color` | `auto` | auto, color, str | couleur de la grille. Défaut : `"gray"`. | grid color |
| `cell` | `auto` | auto, array, dictionary, none | styles de cellules : un tableau de triplets `(lignes, colonnes, style)` ou de dictionnaires `(rows: …, cols: …, style: …)` ; les lignes et colonnes sont un entier, une plage `"2-4"`, une liste `"1,3"` ou un tableau de c… | cell{lignes}{colonnes} |
| `baseline` | `auto` | auto, int, str | ligne de base de l'opération : `"t"` (haut), `"c"` (centre), `"b"` (bas) ou le numéro de la ligne qui s'aligne avec le texte. Défaut : `1`. | baseline |
| `matrix` | `auto` | auto, dictionary, function, array, none | style du cadre de l'opération (fill, draw, inset, radius) ; la sous-clé `nodes` règle toutes les cellules, `row-sep` et `column-sep` les espaces. Défaut : `none`. | matrix |
| `tikz` | `auto` | auto, dictionary, function, array, none | style de l'arrière-plan de l'image (fill, draw, radius, inset), sans effet sur sa taille. Défaut : `none`. | tikz |
| `matrix-name` | `auto` | auto, str, none | label Typst posé sur l'opération. Défaut : `none`. | matrix name |
| `row-sep` | `auto` | auto, length, none | espace entre les lignes (ajout ; `none` : cellules jointives, traits de grille confondus). Défaut : `none`. |  |
| `column-sep` | `auto` | auto, length, none | espace entre les colonnes (ajout). Défaut : `none`. |  |
| `matrix-inset` | `auto` | auto, length, dictionary | marge intérieure du cadre (ajout ; `inner sep` de la matrice). Défaut : `0.3333em`. |  |
| `overlay` | `auto` | auto, function, none | fonction `cellules => contenu` qui dessine par-dessus l'opération (ajout) ; `cellules.at("cell 5-4")` donne les ancres (`north`, `south-west`, `base-east`…) de la cellule ligne 5, colonne 4 (aussi `"M-5-4"` si `matrix-n… |  |
| `style` | `auto` | auto, str, array | style(s) nommé(s) défini(s) par `setrdopp(definir: …)`. Défaut : `auto`. | monstyle (nom d'un style) |

Clés documentées dans le guide (`rdopp/docs/fiches-rdopp.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..nombres` | (positionnel) | any |  | les nombres à poser (voir ci-dessus). |

Exemple :

```typ
#rdopp("12.5, 3.45", operation: "sub") #h(1cm)
#rdopp("234, 56", mul: true, carry: true) #h(1cm)
#rdopp("125, 5", div: true)
```

## setrdopp

```typ
setrdopp(pour: none, reinitialiser: false, definir: none, ..cles)
```

`setrdopp{clés}` : le réglage de `rdopp`, sous ses quatre formes (mêmes clés que `rdopp`).

- `setrdopp(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdopp(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` sur `rdopp` ou `setrdopp`. Un style peut en appeler un autre (`style:`). - `setrdopp(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (`rdopp` n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdopp/docs/fiches-rdopp.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdopp` (et `style:`). |

Exemple :

```typ
#setrdopp(carry: true, seyes: true)
#rdopp("37, 8", mul: true)
#setrdopp(definir: "gris", zero: true, zero-style: (text: gray))
#rdopp(style: "gris", "12, 3.4", sub: true)
#setrdopp(reinitialiser: "tout")
```
