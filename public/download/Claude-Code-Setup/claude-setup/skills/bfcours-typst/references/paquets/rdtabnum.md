# rdtabnum

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-tabnum` puis `#import rd-tabnum: *`.
- Réglage : `setrdtabnum` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdtabnum.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdtabnum`).

## Sommaire

- `rdtabnum` — Compose un tableau de numération (classes, rangs décimaux) et y place les nombres décrits par ses éléments.
- `rdtnplace` — Place un nombre entier ou décimal dans une nouvelle ligne de données.
- `rdtnconvert` — Montre la conversion d'un nombre d'une unité à une autre dans une nouvelle ligne.
- `rdtnemptyline` — Insère `n` lignes de données vides (une par défaut), prêtes à recevoir l'écriture de l'élève ; elles comptent dans la numérotation des lign…
- `rdtn-arrow` — Flèche d'opération en baïonnette sur un bord du tableau (× 10, ÷ 1000…), de la ligne de départ à la ligne d'arrivée (numéros de lignes de d…
- `rdtnsurcouche` — Tracé libre superposé au tableau (accolade, courbe, encadrés), à placer parmi les éléments de `rdtabnum`.
- `setrdtabnum` — Le réglage de `rdtabnum`, sous ses quatre formes (mêmes clés que `rdtabnum`).
- `rdtabnumarrowcol` — Couleur par défaut des flèches latérales (rdtabnumarrowcol).
- `rdtnpurple` — Synonyme de `rdtabnumarrowcol`.

## rdtabnum

```typ
rdtabnum(start: auto, stop: auto, width: auto, show-parts: auto, show-initial-comma: auto, correction: auto, tblr-options: auto, classes-style: auto, cdu-style: auto, decimals-style: auto, data-style: auto, int-part-style: auto, dec-part-style: auto, part-style: auto, header-tikz: auto, int-part-tikz: auto, dec-part-tikz: auto, part-tikz: auto, classes-tikz: auto, cdu-tikz: auto, decimals-tikz: auto, grid-outer-style: auto, grid-h-style: auto, grid-v-style: auto, grid-style: auto, digit-style: auto, added-style: auto, cross-style: auto, cross-path: auto, comma-style: auto, initial-comma-style: auto, cell-base-style: auto, row-cell-style: auto, style: auto, ..elements)
```

Compose un tableau de numération (classes, rangs décimaux) et y place les nombres décrits par ses éléments.

Les ÉLÉMENTS sont les arguments positionnels : `rdtnplace` (un nombre), `rdtnconvert` (une conversion d'unité), `rdtnemptyline` (lignes vides), `rdtn-arrow` (une flèche latérale) et `rdtnsurcouche` (un tracé libre). Les lignes de données se numérotent à partir de 1, dans l'ordre d'écriture. Les options sont les clés nommées ; chacune se règle aussi globalement par `setrdtabnum`.

Les STYLES (clés `*-style` et `*-tikz`) sont des dictionnaires `(text: red, font: (weight: "bold"), fill: "red!5", draw: blue, line-width: 1pt…)`, une fonction `c => …` ou un tableau de styles. Un dégradé s'écrit `(top-color: …, bottom-color: …)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `start` | `auto` | auto, int, str | borne de gauche : puissance de dix de la colonne des centaines de la classe visée (2, 5, 8, 11) ou nom (`"milliards"`, `"millions"`, `"milliers"`, `"unites"`). Défaut : `"milliers"`. | rdtabnum |
| `stop` | `auto` | auto, int, str | borne de droite : puissance de dix de la dernière colonne (0 à -11) ou nom (`"unites"`, `"dixiemes"`, `"centiemes"`, `"milliemes"`, `"dix-milliemes"`…). `"unites"` désigne ici la colonne des unités simples. Défaut : `"m… | rdtabnum |
| `width` | `auto` | auto, length, ratio | largeur du tableau ; les colonnes ont la même largeur, sauf si une cellule fusionnée (libellé de classe, « Partie décimale ») est plus large que les colonnes qu'elle recouvre : celles-ci s'élargissent alors. Défaut : `1… | rdtabnum |
| `show-parts` | `auto` | auto, bool | ajoute en haut la rangée « Partie entière » et « Partie décimale ». Défaut : `false`. | rdtabnum |
| `show-initial-comma` | `auto` | auto, bool | une conversion garde la virgule de départ, barrée. Défaut : `false`. | rdtabnum |
| `correction` | `auto` | auto, bool | le tableau suit la version du document : `rdtnplace(etoile: true)`, `rdtnconvert` et `rdtn-arrow(etoile: true)` n'apparaissent qu'en version professeur (la place reste réservée) et, dans ce cas, prennent la couleur et l… | rdtabnum |
| `tblr-options` | `auto` | auto, dictionary, none | réglages de la grille : `rowsep` (marge verticale des cellules), `cells` (style de toutes les cellules) ; `colsep` (marge horizontale, 6pt) fixe la largeur minimale des cellules fusionnées. Défaut : `none`. | rdtabnum |
| `classes-style` | `auto` | auto, dictionary, function, array, none | style des cellules « Classe des … ». Défaut : `none`. | rdtabnum |
| `cdu-style` | `auto` | auto, dictionary, function, array, none | style des cellules « c », « d », « u ». Défaut : `none`. | rdtabnum |
| `decimals-style` | `auto` | auto, dictionary, function, array, none | style des en-têtes décimaux pivotés (« dixièmes »…). Défaut : `none`. | rdtabnum |
| `data-style` | `auto` | auto, dictionary, function, array, none | style de toutes les lignes de données (`fill`, `font`, `text`, `row-sep`). Défaut : `none`. | rdtabnum |
| `int-part-style` | `auto` | auto, dictionary, function, array, none | style de la cellule « Partie entière » ; `border: false` retire la bordure extérieure autour de cette cellule. Défaut : `none`. | rdtabnum |
| `dec-part-style` | `auto` | auto, dictionary, function, array, none | style de la cellule « Partie décimale » (`border` aussi). Défaut : `none`. | rdtabnum |
| `part-style` | `auto` | auto, dictionary, function, array, none | raccourci : le même style pour `int-part-style` et `dec-part-style`. Défaut : `none`. | rdtabnum |
| `header-tikz` | `auto` | auto, dictionary, function, array, none | fond de tout l'en-tête (dégradé, couleur, opacité, contour). Défaut : `none`. | rdtabnum |
| `int-part-tikz` | `auto` | auto, dictionary, function, array, none | fond de la cellule « Partie entière ». Défaut : `none`. | rdtabnum |
| `dec-part-tikz` | `auto` | auto, dictionary, function, array, none | fond de la cellule « Partie décimale ». Défaut : `none`. | rdtabnum |
| `part-tikz` | `auto` | auto, dictionary, function, array, none | raccourci : le même fond pour `int-part-tikz` et `dec-part-tikz`. Défaut : `none`. | rdtabnum |
| `classes-tikz` | `auto` | auto, dictionary, function, array, none | fond de chaque cellule de classe. Défaut : `none`. | rdtabnum |
| `cdu-tikz` | `auto` | auto, dictionary, function, array, none | fond de chaque cellule « c », « d », « u ». Défaut : `none`. | rdtabnum |
| `decimals-tikz` | `auto` | auto, dictionary, function, array, none | fond de chaque colonne décimale de l'en-tête. Défaut : `none`. | rdtabnum |
| `grid-outer-style` | `auto` | auto, none, str, length, color, stroke, dictionary | trait du cadre extérieur. Défaut : `1pt + black`. | rdtabnum |
| `grid-h-style` | `auto` | auto, none, str, length, color, stroke, dictionary | traits horizontaux intérieurs. Défaut : `1pt + black`. | rdtabnum |
| `grid-v-style` | `auto` | auto, none, str, length, color, stroke, dictionary | traits verticaux intérieurs. Défaut : `1pt + black`. | rdtabnum |
| `grid-style` | `auto` | auto, none, str, length, color, stroke, dictionary | raccourci : le même trait pour les trois clés précédentes ; `none` supprime la grille. Défaut : `none`. | rdtabnum |
| `digit-style` | `auto` | auto, dictionary, function, array, none | style des chiffres placés. Défaut : `none`. | rdtabnum |
| `added-style` | `auto` | auto, dictionary, function, array, none | style des zéros ajoutés par une conversion (en plus du rouge, ou de la couleur des corrections). Défaut : `none`. | rdtabnum |
| `cross-style` | `auto` | auto, dictionary, function, array, none | style du trait qui barre les zéros inutiles (en plus de `draw: red, line-width: 1pt`). Défaut : `none`. | rdtabnum |
| `cross-path` | `auto` | auto, function, none | tracé d'un zéro inutile : une fonction qui reçoit `(w:, h:, asc:, trait:)` (taille de la cellule, distance du haut à la ligne de base, trait résolu) et renvoie du contenu placé dans la cellule ; `none` : la diagonale. D… | rdtabnum |
| `comma-style` | `auto` | auto, dictionary, function, array, none | style de la virgule (cercle, fond, police…). Défaut : `none`. | rdtabnum |
| `initial-comma-style` | `auto` | auto, dictionary, function, array, none | style de la virgule de départ barrée (en plus de `shape: "strike-out", draw: red`). Défaut : `none`. | rdtabnum |
| `cell-base-style` | `auto` | auto, dictionary, function, array, none | style de base de chaque cellule de données (`text-height`, `text-depth`, `min-width`, `seyes`…), appliqué après `inset: 0pt, min-width: 1em`. Défaut : `none`. | rdtabnum |
| `row-cell-style` | `auto` | auto, dictionary, array, none | styles ciblés par ligne de données : un dictionnaire dont les clés sont des sélecteurs (`"1"`, `"1-3"`, `"2-"`, `"-2"`, `"1, 3"`, `"odd"`, `"even"`) et les valeurs des styles, appliqués dans l'ordre après `cell-base-sty… | rdtabnum |
| `style` | `auto` | auto, str, array | style(s) nommé(s) défini(s) par `setrdtabnum(definir: …)`. Défaut : `auto`. |  |

Clés documentées dans le guide (`rdtabnum/docs/fiches-rdtabnum.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..elements` | (positionnel) | any |  | les éléments du tableau, dans l'ordre : `rdtnplace`, `rdtnconvert`, `rdtnemptyline`, `rdtn-arrow`, `rdtnsurcouche` (ou des tableaux de ces éléments). |

Exemple :

```typ
#rdtabnum(width: 7.5cm, rdtnplace(1500), rdtnplace(42), rdtnplace("3,14"))
```

## rdtnplace

```typ
rdtnplace(nombre, etoile: false, unite: 0)
```

Place un nombre entier ou décimal dans une nouvelle ligne de données.

Chaque chiffre est rangé dans la colonne de son ordre de grandeur ; la virgule est tracée sur le filet qui sépare les colonnes des unités et des dixièmes, à hauteur de la ligne de base. Le nombre s'écrit avec une virgule ou un point, de préférence en chaîne (`"3,14"`, `"0,75"`).

La variante étoilée (`etoile: true`) est la réponse de l'élève : dans un tableau `correction: true`, elle reste vide en version élève (la place est gardée) et s'écrit dans la couleur et la police des corrections en version professeur. Sans `correction: true`, elle se comporte comme `rdtnplace`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nombre` | (positionnel) | str, int, float | le nombre à placer. |  |
| `etoile` | `false` | bool | variante étoilée : réponse de l'élève, visible en version professeur seulement. Défaut : `false`. |  |
| `unite` | `0` | int | puissance de dix du chiffre des unités du nombre donné (`3` : le nombre est en milliers, `-1` : en dixièmes). Défaut : `0`. | rdtnplace |

Exemple :

```typ
#rdtabnum(width: 8cm, stop: "centiemes",
  rdtnplace(42), rdtnplace(1500), rdtnplace("3,14"), rdtnplace("0.75"))
```

## rdtnconvert

```typ
rdtnconvert(nombre, depart, cible)
```

Montre la conversion d'un nombre d'une unité à une autre dans une nouvelle ligne.

Les chiffres du nombre sont rangés selon l'unité source, les zéros nécessaires sont ajoutés (en rouge, clé `added-style`), la virgule est posée sur l'unité cible, et les zéros devenus inutiles sont barrés. Dans un tableau `correction: true`, la ligne est vide en version élève et prend la couleur des corrections en version professeur.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nombre` | (positionnel) | str, int, float | le nombre à convertir. |  |
| `depart` | (positionnel) | int | puissance de dix de l'unité de départ (0 : unités, 1 : dizaines, 3 : milliers, -1 : dixièmes). |  |
| `cible` | (positionnel) | int | puissance de dix de l'unité visée. |  |

Exemple :

```typ
#rdtabnum(width: 8cm,
  rdtnconvert("7,2", 1, -2),
  rdtnconvert(480, -3, 0),
  rdtnconvert("0,57", 0, -3))
```

## rdtnemptyline

```typ
rdtnemptyline(..args)
```

Insère `n` lignes de données vides (une par défaut), prêtes à recevoir l'écriture de l'élève ; elles comptent dans la numérotation des lignes.

Clés documentées dans le guide (`rdtabnum/docs/fiches-rdtabnum.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `n` | (positionnel) | int |  | nombre de lignes. |

Exemple :

```typ
#rdtabnum(width: 8cm, stop: "centiemes",
  rdtnplace(425), rdtnemptyline(2), rdtnplace("18,3"))
```

## rdtn-arrow

```typ
rdtn-arrow(depart, arrivee, libelle, etoile: false, pos: auto, left: auto, right: auto, shift-start: auto, shift-end: auto, shift: auto, arm: auto, arrow-style: auto, color: auto, tip: auto, node-sep: auto, node-pos: auto, node-style: auto, correction: auto, style: auto, ..autres)
```

Flèche d'opération en baïonnette sur un bord du tableau (× 10, ÷ 1000…), de la ligne de départ à la ligne d'arrivée (numéros de lignes de données, à partir de 1), avec son libellé. À placer parmi les éléments de `rdtabnum`.

La variante étoilée (`etoile: true`) n'apparaît qu'en version professeur quand le tableau est `correction: true` ; la clé `correction` règle ce comportement flèche par flèche (`true` : comme une correction, `false` : toujours visible, `"auto"` : selon l'étoile).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `depart` | (positionnel) | int | ligne de départ. |  |
| `arrivee` | (positionnel) | int | ligne d'arrivée (la pointe est de ce côté ; la flèche monte si elle précède le départ). |  |
| `libelle` | (positionnel) | content | texte ou formule posé le long du segment vertical. |  |
| `etoile` | `false` | bool | variante étoilée : visible en version professeur seulement (si le tableau est `correction: true`). Défaut : `false`. |  |
| `pos` | `auto` | auto, str | côté du tableau : `"right"` ou `"left"`. Défaut : `"right"`. | rdtn-arrow |
| `left` | `auto` | auto, bool | raccourci de `pos: "left"`. Défaut : `false`. | rdtn-arrow |
| `right` | `auto` | auto, bool | raccourci de `pos: "right"`. Défaut : `false`. | rdtn-arrow |
| `shift-start` | `auto` | auto, length | décalage vertical du point de départ (positif : vers le haut). Défaut : `0pt`. |  |
| `shift-end` | `auto` | auto, length | décalage vertical du point d'arrivée. Défaut : `0pt`. |  |
| `shift` | `auto` | auto, length | raccourci : `shift-start` à cette valeur et `shift-end` à son opposé. Défaut : `0pt`. | rdtn-arrow |
| `arm` | `auto` | auto, length | longueur du bras horizontal ; des bras de longueurs différentes permettent d'imbriquer plusieurs flèches. Défaut : `0.3cm`. | rdtn-arrow |
| `arrow-style` | `auto` | auto, dictionary, function, array, none | style du tracé (`draw`, `line-width`, `dash`…), ajouté à `draw: rdtabnumarrowcol, line-width: 1pt`. Défaut : `none`. |  |
| `color` | `auto` | auto, color, str, none | raccourci : couleur du tracé. Défaut : `none`. | rdtn-arrow |
| `tip` | `auto` | auto, str, dictionary, none | pointe : `"Stealth"`, `"Latex"`, `"Triangle"`, avec options (`"Latex[length=3mm]"`) ou dictionnaire `(type: "Latex", length: 3mm)` ; `none` : sans pointe. Défaut : `"Stealth[length=2mm, inset=1pt]"`. | rdtn-arrow |
| `node-sep` | `auto` | auto, length | écart horizontal entre le segment vertical et le libellé. Défaut : `2mm`. |  |
| `node-pos` | `auto` | auto, float | position du libellé le long du segment vertical, de 0 (coude de départ) à 1 (coude d'arrivée). Défaut : `0.5`. |  |
| `node-style` | `auto` | auto, dictionary, function, array, none | style du libellé (fond, cadre, couleur, police). Défaut : `none`. |  |
| `correction` | `auto` | auto, bool, str | `"auto"`, `true` ou `false` (voir ci-dessus). Défaut : `"auto"`. | rdtabnum |
| `style` | `auto` | auto, str, array | style(s) nommé(s) défini(s) par `setrdtabnum(pour: "rdtnArrow", definir: …)`. Défaut : `auto`. |  |

Exemple :

```typ
#rdtabnum(width: 6.5cm, stop: "dixiemes",
  rdtnplace("3,5"), rdtnplace(350), rdtnplace(3500),
  rdtn-arrow(1, 2, $times 100$),
  rdtn-arrow(3, 2, $div 10$, left: true))
```

## rdtnsurcouche

```typ
rdtnsurcouche(f, dessous: false)
```

Tracé libre superposé au tableau (accolade, courbe, encadrés), à placer parmi les éléments de `rdtabnum`.

`f` reçoit un dictionnaire `g` de coordonnées et renvoie du contenu, posé avec l'origine au coin supérieur gauche du tableau. `g.largeur` et `g.hauteur` sont les dimensions du tableau, `g.lignes` et `g.colonnes` le nombre de lignes de données et de colonnes. `(g.gauche)(k)` et `(g.droite)(k)` donnent le point `(x:, y:)` du bord gauche, ou droit, au centre de la ligne de données `k` ; les parenthèses sont nécessaires, `g` étant un dictionnaire. `(g.cellule)(k, c)` donne `(x:, y:, w:, h:, base:)` pour la cellule de la ligne `k` et de la colonne `c` (à partir de 1), `(g.colonne)(c)` donne `(x:, w:)`, `g.separation` est l'abscisse de la frontière entre parties entière et décimale, `g.entete` donne `(y:, h:)` pour les rangées `parties` (ou `none`), `classes` et `cdu`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `f` | (positionnel) | function | fonction `g => contenu`. |  |
| `dessous` | `false` | bool | trace sous le tableau (sous les fonds et le texte) au lieu de dessus. Défaut : `false`. |  |

Exemple :

```typ
#rdtabnum(width: 5.5cm, stop: "unites",
  rdtnplace("5,4"), rdtnplace(5400),
  rdtnsurcouche(g => {
    let a = (g.droite)(1)
    let b = (g.droite)(2)
    place(top + left, dx: a.x, dy: a.y,
      curve(stroke: teal + 1pt,
        curve.move((0pt, 0pt)),
        curve.cubic((1.4cm, 0pt), (1.4cm, b.y - a.y), (0pt, b.y - a.y))))
  }))
```

## setrdtabnum

```typ
setrdtabnum(pour: none, reinitialiser: false, definir: none, ..cles)
```

Le réglage de `rdtabnum`, sous ses quatre formes (mêmes clés que `rdtabnum`).

- `setrdtabnum(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdtabnum(pour: "rdtnArrow", cle: v, …)` : réglage des flèches (clés de `rdtn-arrow`). - `setrdtabnum(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` (avec `pour: "rdtnArrow"` : style de flèche). - `setrdtabnum(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | `none` (le tableau) ou `"rdtnArrow"` (les flèches). Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdtabnum/docs/fiches-rdtabnum.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdtabnum` (ou de `rdtn-arrow`) et `style:`. |

Exemple :

```typ
#setrdtabnum(width: 7cm, stop: "dixiemes", grid-style: (thickness: 0.8pt, paint: teal))
#rdtabnum(rdtnplace("4250,7"), rdtnplace(18))
#setrdtabnum(reinitialiser: "tout")
```

## rdtabnumarrowcol

```typ
rdtabnumarrowcol
```

Couleur par défaut des flèches latérales (rdtabnumarrowcol).

## rdtnpurple

```typ
rdtnpurple
```

Synonyme de `rdtabnumarrowcol`.
