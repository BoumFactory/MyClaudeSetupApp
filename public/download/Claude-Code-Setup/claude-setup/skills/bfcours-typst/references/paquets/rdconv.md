# rdconv

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-conv` puis `#import rd-conv: *`.
- Réglage : `setrdconv` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdconv.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdconv`).

## Sommaire

- `rdconv` — `rdconv` : tableau de conversion d'unités (longueur, masse, capacité, aire ou volume), dont les lignes sont décrites par `rdplace`, `rdconv…
- `rdplace` — `rdplace` : place une grandeur (valeur et unité) dans le tableau, sans conversion. À écrire dans `rdconv`.
- `rdconvert` — `rdconvert` : écrit la conversion d'une grandeur : chiffres, zéros ajoutés, virgule déplacée et zéros inutiles barrés. À écrire dans `rdcon…
- `rdconvemptyline` — `rdconvemptyline` : insère des lignes vides, numérotées si la numérotation est active. À écrire dans `rdconv`.
- `rdconvtext` — `rdconvtext` : valeur convertie d'une grandeur, écrite avec une virgule décimale, sans zéros inutiles (`"12500"`, `"0,721"`). Sert dans une…
- `setrdconv` — `setrdconv` : le réglage de `rdconv`, sous ses quatre formes (mêmes clés que `rdconv`).
- `rdtheme` — `rdtheme` : jeu de clés du style `rdtheme` pour trois couleurs (principale, multiples, fond des données), à passer à `rdconv` ou à `setrdco…
- `rdconvdingnum` — `rdconvdingnum` : numéro encerclé ➊ ➋ ➌… (de 1 à 10), à donner à `nb-info-macro` ou `nb-table-macro`.
- `rdconvbadge` — `rdconvbadge` : pastille ronde numérotée, à donner à `nb-table-macro` (par `"rdconvbadge"`, la couleur suit `rdtheme-main-color`).

## rdconv

```typ
rdconv(type: auto, title: auto, title-pos: auto, title-format: auto, title-border: auto, show-mult: auto, mult-format: auto, mult-border: auto, mult-text: auto, submult-text: auto, decimal-sep: auto, correction: auto, mass-tons: auto, show-ca: auto, sec-units: auto, width: auto, liter: auto, number-info: auto, number-table: auto, nb-info-col-type: auto, nb-table-col-type: auto, nb-info-macro: auto, nb-table-macro: auto, info-col: auto, info-col-type: auto, tblr-options: auto, grid-style: auto, grid-v-style: auto, grid-vminor-style: auto, grid-outer-style: auto, grid-h-style: auto, grid-hminor-style: auto, unit-format: auto, sec-unit-format: auto, data-format: auto, cell-base-style: auto, digit-style: auto, added-style: auto, comma-style: auto, cross-style: auto, cross-path: auto, rdtheme-main-color: auto, style: auto, ..lignes)
```

`rdconv` : tableau de conversion d'unités (longueur, masse, capacité, aire ou volume), dont les lignes sont décrites par `rdplace`, `rdconvert` et `rdconvemptyline`.

Les STYLES (clés `digit-style`, `added-style`, `comma-style`, `cross-style`, `cell-base-style`) sont des dictionnaires `(text: red, font: (weight: "bold"), fill: yellow, inset: 2pt, min-width: 1em…)` ; les FORMATS (clés `unit-format`, `sec-unit-format`, `data-format`, `title-format`, `mult-format`) sont des dictionnaires `(bg: couleur, fg: couleur, font: (…), align: right, border: false)`. Les traits de grille (clés `grid-…-style`) sont des traits Typst (`1.5pt + black`, `(paint: blue, dash: "dashed")`) ou `none` pour une ligne invisible.

- ..lignes (any): les lignes du tableau, dans l'ordre : `rdplace(…)`, `rdconvert(…)`, `rdconvemptyline(…)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `type` | `auto` | auto, str | grandeur : `"length"`, `"mass"`, `"capacity"`, `"area"` ou `"volume"`. Défaut : `"length"`. | type |
| `title` | `auto` | auto, none, str, content | titre fusionné sur toute la largeur ; `none` : aucun titre. Défaut : `none`. | title |
| `title-pos` | `auto` | auto, str | place du titre : `"top"` (au-dessus), `"bottom"` (sous le tableau) ou `"below-mult"` (sous la ligne des multiples). Défaut : `"top"`. | title-pos |
| `title-format` | `auto` | auto, none, dictionary | format de la cellule du titre ; sa clé `border` règle le cadre. Défaut : `none`. | title-format |
| `title-border` | `auto` | auto, bool | cadre autour du titre. Défaut : `true`. | title-border |
| `show-mult` | `auto` | auto, bool | affiche la ligne « Multiples » et « Sous-multiples ». Défaut : `false`. | show-mult |
| `mult-format` | `auto` | auto, none, dictionary | format de la ligne des multiples ; sa clé `border` règle le cadre. Défaut : `none`. | mult-format |
| `mult-border` | `auto` | auto, bool | cadre autour des cases « Multiples » et « Sous-multiples ». Défaut : `true`. | mult-border |
| `mult-text` | `auto` | auto, content | texte de la case des multiples (ajout). Défaut : `[Multiples]`. |  |
| `submult-text` | `auto` | auto, content | texte de la case des sous-multiples (ajout). Défaut : `[Sous-multiples]`. |  |
| `decimal-sep` | `auto` | auto, bool | `rdplace` dessine la virgule d'un nombre décimal. Défaut : `false`. | decimal sep |
| `correction` | `auto` | auto, bool | les éléments de `rdconvert` (chiffres, zéros, virgule, ratures) n'apparaissent qu'en version professeur, dans la couleur et la police des corrections ; en version élève les cases restent vides. Défaut : `false`. | correction |
| `mass-tons` | `auto` | auto, bool | tableau de masses avec les colonnes des tonnes, des quintaux et des dizaines de kilogrammes. Défaut : `false`. | mass-tons |
| `show-ca` | `auto` | auto, bool | tableau d'aires : affiche le centiare sous les mètres carrés. Défaut : `false`. | show-ca |
| `sec-units` | `auto` | auto, bool | aires et volumes : affiche la ligne des unités secondaires (ha, a ; capacités). Défaut : `true`. | sec-units |
| `width` | `auto` | auto, length, ratio | largeur totale du tableau. Défaut : `100%`. | width |
| `liter` | `auto` | auto, content | lettre du litre dans les en-têtes de capacité. Défaut : `$ell$`. | liter |
| `number-info` | `auto` | auto, bool | colonne de numéros tout à gauche. Défaut : `false`. | number-info |
| `number-table` | `auto` | auto, bool | colonne de numéros juste avant la grille. Défaut : `false`. | number-table |
| `nb-info-col-type` | `auto` | auto, str, dictionary | alignement et largeur de la colonne `number-info` (`"l"`, `"c"`, `"r"` ou `(align: left, width: 2cm)`). Défaut : `"c"`. | nb-info-col-type |
| `nb-table-col-type` | `auto` | auto, str, dictionary | alignement et largeur de la colonne `number-table`. Défaut : `"c"`. | nb-table-col-type |
| `nb-info-macro` | `auto` | auto, none, function, str | met en forme le numéro de `number-info` : fonction `numéro => contenu` ou `"rdconvbadge"`. Défaut : `none`. | nb-info-macro |
| `nb-table-macro` | `auto` | auto, none, function, str | met en forme le numéro de `number-table`. Défaut : `none`. | nb-table-macro |
| `info-col` | `auto` | auto, none, content, function | colonne de texte libre à gauche ; une fonction reçoit le dictionnaire `(rdValInit, rdUnitInit, rdValTarget, rdUnitTarget)` de la ligne. Défaut : `none`. | info-col (avec \\rdValInit…) |
| `info-col-type` | `auto` | auto, str, dictionary | alignement et largeur de la colonne `info-col` (`"l"`, `(align: left, width: 6fr)`…). Défaut : `"l"`. | info-col-type |
| `tblr-options` | `auto` | auto, none, dictionary | `(colsep: longueur, rowsep: longueur, cells: format)` : marges des cellules et format commun. Défaut : `none`. | tblr-options |
| `grid-style` | `auto` | auto, none, length, color, stroke, dictionary | même trait pour les cinq lignes de grille suivantes (celles qui sont données l'emportent). Défaut : `auto`. | grid-style |
| `grid-v-style` | `auto` | auto, none, length, color, stroke, dictionary | lignes verticales qui séparent les unités. Défaut : `1.5pt + black`. | grid-v-style |
| `grid-vminor-style` | `auto` | auto, none, length, color, stroke, dictionary | lignes verticales secondaires entre les colonnes d'une même unité (aires, volumes). Défaut : `0.6pt + black`, en pointillés. | grid-vminor-style |
| `grid-outer-style` | `auto` | auto, none, length, color, stroke, dictionary | cadre extérieur de la grille. Défaut : `1.5pt + black`. | grid-outer-style |
| `grid-h-style` | `auto` | auto, none, length, color, stroke, dictionary | lignes horizontales. Défaut : `1.5pt + black`. | grid-h-style |
| `grid-hminor-style` | `auto` | auto, none, length, color, stroke, dictionary | ligne entre les unités principales et secondaires. Défaut : `auto` (comme `grid-h-style`). | grid-hminor-style |
| `unit-format` | `auto` | auto, none, dictionary | format de la ligne des unités. Défaut : `none`. | unit-format |
| `sec-unit-format` | `auto` | auto, none, dictionary | format de la ligne des unités secondaires. Défaut : `none`. | sec-unit-format |
| `data-format` | `auto` | auto, none, dictionary | format du bloc des cellules de données. Défaut : `none`. | data-format |
| `cell-base-style` | `auto` | auto, none, dictionary, function, array | style de base de chaque case ; remplace le style d'origine. Défaut : `(inset: 2pt, min-width: 1em)`. | cell-base-style |
| `digit-style` | `auto` | auto, none, dictionary, function, array | style des chiffres saisis. Défaut : `none`. | digit-style |
| `added-style` | `auto` | auto, none, dictionary, function, array | style des zéros ajoutés par une conversion. Défaut : `(text: red, font: (weight: "bold"))`. |  |
| `comma-style` | `auto` | auto, none, dictionary, function, array | style de la virgule. Défaut : `(text: red, font: (weight: "bold", size: 1.6em), inset: 0pt)` (virgule agrandie, lisible sur le filet de colonne). | comma-style ; option de \\rdconvert[…] |
| `cross-style` | `auto` | auto, none, dictionary, function, array | style des ratures. Défaut : `(draw: red, line-width: 0.8pt)`. | cross-style |
| `cross-path` | `auto` | auto, none, function | fonction qui dessine la rature : elle reçoit `(w, h, asc, stroke)` (largeur, hauteur, hauteur de la ligne de base, trait) et rend un contenu posé avec `place`. Défaut : la diagonale de la case. | cross-path (code TikZ avec \\rdcell) |
| `rdtheme-main-color` | `auto` | auto, color | couleur des pastilles `"rdconvbadge"`. Défaut : `rgb("#5F8090")`. | rdtheme-main-color |
| `style` | `auto` | auto, str, array | style(s) nommé(s) : `"rdfiche"`, `"rdtheme"`, `"rdtheme-blue"`, `"rdtheme-dark"`, `"rdtheme-lightblue"`, `"rdtheme-teal"`, `"rdtheme-red"`, ou définis par `setrdconv(definir: …)`. Défaut : `auto`. | rdfiche, rdtheme, rdtheme-blue… (styles) |

Clés documentées dans le guide (`rdconv/docs/fiches-rdconv.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..lignes` | (positionnel) | any |  | les lignes du tableau, dans l'ordre : `rdplace(…)`, `rdconvert(…)`, `rdconvemptyline(…)`. |

Exemple :

```typ
#rdconv(
  rdplace(12, "m"),
  rdplace("3,45", "dam"),
  rdplace("45.6", "cm"),
)
```

## rdplace

```typ
rdplace(valeur, unite)
```

`rdplace` : place une grandeur (valeur et unité) dans le tableau, sans conversion. À écrire dans `rdconv`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | int, float, str | entier ou décimal ; la virgule et le point sont acceptés (`"3,45"`, `"45.6"`). |  |
| `unite` | (positionnel) | str | unité du tableau : `"km"`, `"m^2"`, `"ha"`, `"dL"`, `"kg"`… (l'exposant s'écrit `^2`, ou `²`). |  |

Exemple :

```typ
#rdconv(decimal-sep: true, rdplace("3,52", "m"), rdplace(45, "cm"))
```

## rdconvert

```typ
rdconvert(valeur, de, vers, comma-style: auto)
```

`rdconvert` : écrit la conversion d'une grandeur : chiffres, zéros ajoutés, virgule déplacée et zéros inutiles barrés. À écrire dans `rdconv`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | int, float, str | entier ou décimal. |  |
| `de` | (positionnel) | str | unité de départ. |  |
| `vers` | (positionnel) | str | unité d'arrivée. |  |
| `comma-style` | `auto` | auto, none, dictionary, function, array | style de la virgule pour cette seule ligne, ajouté au style global (`(yshift: -2pt)` la descend). Défaut : `auto`. | comma-style ; option de \\rdconvert[…] |

Exemple :

```typ
#rdconv(type: "mass", rdconvert(12, "g", "cg"), rdconvert("3,45", "hg", "g"), rdconvert(4500, "mg", "g"))
```

## rdconvemptyline

```typ
rdconvemptyline(nombre)
```

`rdconvemptyline` : insère des lignes vides, numérotées si la numérotation est active. À écrire dans `rdconv`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nombre` | (positionnel) | int | nombre de lignes vides. |  |

Exemple :

```typ
#rdconv(number-info: true, rdplace(12, "m"), rdconvemptyline(2), rdplace("3,45", "dam"))
```

## rdconvtext

```typ
rdconvtext(valeur, de, vers)
```

`rdconvtext` : valeur convertie d'une grandeur, écrite avec une virgule décimale, sans zéros inutiles (`"12500"`, `"0,721"`). Sert dans une phrase ou comme argument d'une autre fonction (`num`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | int, float, str | entier ou décimal. |  |
| `de` | (positionnel) | str | unité de départ. |  |
| `vers` | (positionnel) | str | unité d'arrivée. |  |

Exemple :

```typ
12,5 km $=$ #rdconvtext("12.5", "km", "m") m $=$ #rdconvtext("12.5", "km", "cm") cm.

Une aire de 0,35 m#super[2] vaut #rdconvtext("0.35", "m^2", "cm^2") cm#super[2].
```

## setrdconv

```typ
setrdconv(pour: none, reinitialiser: false, definir: none, ..cles)
```

`setrdconv` : le réglage de `rdconv`, sous ses quatre formes (mêmes clés que `rdconv`).

- `setrdconv(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdconv(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` sur `rdconv` ou `setrdconv`. Un style peut en appeler un autre (`style:`). - `setrdconv(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles définis.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (`rdconv` n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. | nom/.style={…} |

Clés documentées dans le guide (`rdconv/docs/fiches-rdconv.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdconv` (et `style:`). |

Exemple :

```typ
#setrdconv(decimal-sep: true, grid-style: (paint: gray, thickness: 1pt))
#rdconv(rdplace("3,52", "m"))
#setrdconv(definir: "bleu", unit-format: (bg: "blue!15", fg: blue))
#rdconv(style: "bleu", rdplace(12, "m"))
#setrdconv(reinitialiser: "tout")
```

## rdtheme

```typ
rdtheme(..couleurs)
```

`rdtheme` : jeu de clés du style `rdtheme` pour trois couleurs (principale, multiples, fond des données), à passer à `rdconv` ou à `setrdconv` avec `..`. Sans argument : les couleurs bleu-gris d'origine. Les cinq variantes prêtes à l'emploi sont les styles nommés `"rdtheme-blue"`, `"rdtheme-dark"`, `"rdtheme-lightblue"`, `"rdtheme-teal"` et `"rdtheme-red"`.

- ..couleurs (color): jusqu'à trois couleurs, dans l'ordre : principale (unités, pastilles, zéros ajoutés ; défaut `rgb("#5F8090")`), multiples (fond de la ligne des multiples ; défaut `rgb("#AABAC2")`), fond (cellules de données ; défaut `rgb("#EEF3F5")`).

Clés documentées dans le guide (`rdconv/docs/fiches-rdconv.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..couleurs` | (positionnel) | color |  | jusqu'à trois couleurs, dans l'ordre : principale (unités, pastilles, zéros ajoutés ; défaut `rgb("#5F8090")`), multiples (fond de la ligne des multiples ; défaut `rgb("#AABAC2")`), fond (cellules de données ; défaut `r… |

Exemple :

```typ
#rdconv(..rdtheme(purple, purple.lighten(50%), purple.lighten(88%)), rdconvert(12.3, "m", "mm"))
```

## rdconvdingnum

```typ
rdconvdingnum(numero)
```

`rdconvdingnum` : numéro encerclé ➊ ➋ ➌… (de 1 à 10), à donner à `nb-info-macro` ou `nb-table-macro`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `numero` | (positionnel) | int | entier de 1 à 10. |  |

Exemple :

```typ
#rdconvdingnum(1) #rdconvdingnum(2) #rdconvdingnum(3)
```

## rdconvbadge

```typ
rdconvbadge(numero, couleur: _m.rdconv-bleu-fonce)
```

`rdconvbadge` : pastille ronde numérotée, à donner à `nb-table-macro` (par `"rdconvbadge"`, la couleur suit `rdtheme-main-color`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `numero` | (positionnel) | int, content | numéro écrit dans la pastille. |  |
| `couleur` | `_m.rdconv-bleu-fonce` | color, str | couleur du fond. Défaut : `rgb("#5F8090")`. |  |

Exemple :

```typ
#rdconvbadge(1) #rdconvbadge(2, couleur: red)
```
