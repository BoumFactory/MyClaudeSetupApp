# rdratio

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-ratio` puis `#import rd-ratio: *`.
- Réglage : `setrdratio` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdratio.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdratio`).

## Sommaire

- `rdratio` — `\ratio[options]{n1,n2,…}` : barre de proportion. Une case par unité, une couleur par part (dégradé de `leftcol` à `rightcol`, ou liste `co…
- `dratio` — `\dratio{2:3}` : écrit un rapport « 2 : 3 » avec des espaces fines autour des deux-points.
- `sumlist` — `\sumlist{a,b,…}` : somme des entiers d'une liste (nombre Typst).
- `setrdratio` — `\setrdratio{clés}` : le réglage de `rdratio`, sous ses quatre formes (mêmes clés que `rdratio`, plus `dratio-sep`).

## rdratio

```typ
rdratio(width: auto, height: auto, auto-width: auto, auto-height: auto, line-width: auto, rounded-corners: auto, brace-amplitude: auto, colframe: auto, leftcol: auto, rightcol: auto, colors: auto, align: auto, raise: auto, labels: auto, label-above: auto, label-above-font: auto, label-above-color: auto, label-above-sep: auto, label-above-node-sep: auto, label-above-line-width: auto, label-above-decoration: auto, label-below: auto, label-below-auto: auto, label-below-font: auto, label-below-color: auto, label-below-auto-colors: auto, label-below-sep: auto, label-below-node-sep: auto, label-below-line-width: auto, label-below-decoration: auto, label-below-n: auto, label-below-node-n: auto, ratiobox: auto, code-after: auto, remember: auto, label-inner-sep: auto, label-phantom: auto, style: auto, parts)
```

`\ratio[options]{n1,n2,…}` : barre de proportion. Une case par unité, une couleur par part (dégradé de `leftcol` à `rightcol`, ou liste `colors`), une accolade au-dessus (`label-above`) et une accolade sous chaque part (« 2 parts », ou la liste `label-below`).

Nommée `rdratio` et non `ratio` : `ratio` est un type natif de Typst (repli R18).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `width` | `auto` | auto, length | largeur totale. Défaut : `6cm`. | width |
| `height` | `auto` | auto, length | hauteur totale. Défaut : `0.8cm`. | height |
| `auto-width` | `auto` | auto, bool | cases carrées, largeur calculée d'après `height`. Défaut : `false`. | auto width |
| `auto-height` | `auto` | auto, bool | cases carrées, hauteur calculée d'après `width`. Défaut : `false`. | auto height |
| `line-width` | `auto` | auto, length | épaisseur du contour (et des séparations). Défaut : `1pt`. | line width |
| `rounded-corners` | `auto` | auto, length | arrondi des coins (`0pt` : coins vifs). Défaut : `3pt`. | rounded corners |
| `brace-amplitude` | `auto` | auto, length | amplitude des accolades. Défaut : `2.5pt`. | brace amplitude |
| `colframe` | `auto` | auto, color, str | couleur du contour. Défaut : `"black"`. | colframe |
| `leftcol` | `auto` | auto, color, str | couleur de la première part. Défaut : `"red"`. | leftcol |
| `rightcol` | `auto` | auto, color, str | couleur de la dernière part. Défaut : `"blue"`. | rightcol |
| `colors` | `auto` | auto, none, array, str | couleurs des parts, en boucle ; remplace le dégradé. Défaut : `none`. | colors |
| `align` | `auto` | auto, str | `"top"`, `"center"` ou `"bottom"` : point du cadre posé sur la ligne de base. Défaut : `"center"`. | align |
| `raise` | `auto` | auto, length | décalage vertical (positif : vers le haut). Défaut : `0pt`. | raise |
| `labels` | `auto` | auto, str | `"all"`, `"above"`, `"below"` ou `"none"`. Défaut : `"all"`. | labels |
| `label-above` | `auto` | auto, none, content | légende de l'accolade supérieure. Défaut : `none`. | label above |
| `label-above-font` | `auto` | auto, str, length, dictionary, function | police de la légende : taille LaTeX, longueur, dictionnaire de police ou fonction. Défaut : `"footnotesize"`. | label above font |
| `label-above-color` | `auto` | auto, color, str | couleur de la légende. Défaut : `"black"`. | label above color |
| `label-above-sep` | `auto` | auto, length | distance cadre–accolade. Défaut : `2mm`. | label above sep |
| `label-above-node-sep` | `auto` | auto, length | distance accolade–légende. Défaut : `2pt`. | label above node sep |
| `label-above-line-width` | `auto` | auto, length | épaisseur de l'accolade. Défaut : `0.7pt`. | label above line width |
| `label-above-decoration` | `auto` | auto, none, dictionary | style de l'accolade : `draw`, `line-width`, `amplitude`, `dash`. Défaut : `none`. | label above decoration |
| `label-below` | `auto` | auto, none, array, str | légendes des parts, une par part ; remplace `label-below-auto`. Défaut : `none`. | label below |
| `label-below-auto` | `auto` | auto, array, str | singulier et pluriel des légendes automatiques. Défaut : `("part", "parts")`. | label below auto |
| `label-below-font` | `auto` | auto, str, length, dictionary, function | police des légendes inférieures. Défaut : `"footnotesize"`. | label below font |
| `label-below-color` | `auto` | auto, color, str | couleur des légendes inférieures. Défaut : `"black"`. | label below color |
| `label-below-auto-colors` | `auto` | auto, bool | accolades et légendes de la couleur de leur part. Défaut : `false`. | label below auto colors |
| `label-below-sep` | `auto` | auto, length | distance cadre–accolades. Défaut : `2mm`. | label below sep |
| `label-below-node-sep` | `auto` | auto, length | distance accolades–légendes. Défaut : `2pt`. | label below node sep |
| `label-below-line-width` | `auto` | auto, length | épaisseur des accolades inférieures. Défaut : `0.7pt`. | label below line width |
| `label-below-decoration` | `auto` | auto, none, dictionary | style des accolades inférieures. Défaut : `none`. | label below decoration |
| `label-below-n` | `auto` | auto, none, dictionary | style de l'accolade n° n (`label below <n>`) : `("2": (draw: green, line-width: 2pt))`. Défaut : `none`. | label below <n> |
| `label-below-node-n` | `auto` | auto, none, dictionary | style de la légende n° n (`label below node <n>`) : `("2": (text: orange))`. Défaut : `none`. | label below node <n> |
| `ratiobox` | `auto` | auto, none, dictionary | style de la case n° n (`ratiobox <n>`) : `fill`, `pattern` (tiling), `draw`, `content`… Défaut : `none`. | ratiobox <n> |
| `code-after` | `auto` | auto, none, function | `points => contenu`, posé dans le repère du cadre ; `points` contient `rdframe`, `rdbox<n>` (ancres `center`, `north-west`…), `rdmid<n>`, et l'aide `node(point, contenu)`. Défaut : `none`. | code after |
| `remember` | `auto` | auto, bool | pose les points dans un `metadata` étiqueté `<rdratio-remember>` (équivalent de `remember picture`). Défaut : `false`. | remember |
| `label-inner-sep` | `auto` | auto, length | marge des légendes (ajout ; `inner sep` TikZ). Défaut : `0.3333em`. |  |
| `label-phantom` | `auto` | auto, none, content | fantôme qui égalise la hauteur des légendes (ajout ; `\vphantom{ÀÊÉpgjy}`). Défaut : `[ÀÊÉpgjy]`. |  |
| `style` | `auto` | auto, str, array | style(s) nommé(s) (`setrdratio(definir: …)`). Défaut : `auto`. | monstyle (nom d'un style) |
| `parts` | (positionnel) | array, str, int | parts du ratio : `(2, 3)` ou `"2,3"`. |  |

Exemple :

```typ
Le ratio #dratio("1:3") : #rdratio((1, 3))

#rdratio(width: 5cm, label-above: [150 €], label-below-auto-colors: true, "1,2,3")
```

## dratio

```typ
dratio(dratio-sep: auto, ratio)
```

`\dratio{2:3}` : écrit un rapport « 2 : 3 » avec des espaces fines autour des deux-points.

LaTeX : `\dratio`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `dratio-sep` | `auto` | auto, content | séparateur (ajout ; `\,:\,` en LaTeX). Défaut : espace fine, deux-points, espace fine. |  |
| `ratio` | (positionnel) | str, array | `"2:3"` ou `(2, 3)`. |  |

Exemple :

```typ
Ces quantités sont dans le ratio #dratio("2:3") ; celles-ci dans le ratio *#dratio("4:5:7")*.
```

## sumlist

```typ
sumlist(liste)
```

`\sumlist{a,b,…}` : somme des entiers d'une liste (nombre Typst).

LaTeX : `\sumlist`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `liste` | (positionnel) | str, array | `"2,3,4"` ou `(2, 3, 4)`. |  |

Exemple :

```typ
Il y a #sumlist("2,3,4") parts en tout.
```

## setrdratio

```typ
setrdratio(pour: none, reinitialiser: false, definir: none, ..cles)
```

`\setrdratio{clés}` : le réglage de `rdratio`, sous ses quatre formes (mêmes clés que `rdratio`, plus `dratio-sep`).

- `setrdratio(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdratio(definir: "nom", cle: v, …)` : définit le style nommé « nom » (`\setrdratio{nom/.style={…}}`), appelé ensuite par `style: "nom"`. Un style peut en appeler un autre ; la clé locale l'emporte. - `setrdratio(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

LaTeX : `\setrdratio`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (`rdratio` n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdratio/docs/fiches-rdratio.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdratio` (et `style:`). |

Exemple :

```typ
#setrdratio(leftcol: "yellow", rightcol: "brown", width: 4cm)
#rdratio((2, 3))
#setrdratio(definir: "sarcelle", colframe: "teal", leftcol: "white", rightcol: "teal")
#rdratio(style: "sarcelle", (1, 2, 3))
#setrdratio(reinitialiser: "tout")
```
