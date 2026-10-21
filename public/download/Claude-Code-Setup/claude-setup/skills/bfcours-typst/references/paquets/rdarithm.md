# rdarithm

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-arithm` puis `#import rd-arithm: *`.
- Réglage : `setrdarithm` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdarithm.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdarithm`).

## Sommaire

- `setrdarithm` — `setrdarithm(clés)` : le réglage de rdarithm, sous ses quatre formes.
- `liste-fp` — `\ListeFP[options]{n}` : liste des facteurs premiers de n.
- `decomp-fp` — `\DecompFP[options]{n}` : décomposition de n en facteurs premiers, dans la mise en page choisie par la clé `mise-en-page`. Elle remplace `\…
- `liste-diviseurs` — `\ListeDiviseurs[options]{n}` : liste ordonnée des diviseurs de n.
- `tab-diviseurs` — `\TabDiviseurs[options]{n}` : diviseurs rangés par paires dans un tableau à deux colonnes. Mêmes clés que `decomp-fp(mise-en-page: "tableau…
- `pgcd` — `\pgcd{a}{b}` : écrit PGCD(a ; b) ; `\pgcd*{a}{b}` (`etoile: true`) : renvoie la valeur (entier). Sans argument, `pgcd()` écrit l'opérateur…
- `ppcm` — `\ppcm{a}{b}` : écrit PPCM(a ; b) ; `\ppcm*{a}{b}` (`etoile: true`) : renvoie la valeur (entier). Sans argument, `ppcm()` écrit l'opérateur…
- `tab-pgcd` — `\TabPGCD[options]{a}{b}` : tableau des facteurs premiers de a et b rangés en colonnes ; les facteurs communs (ceux du PGCD) reçoivent `gcd…
- `row-pgcd` — `\RowPGCD[options]{a}{b}` : décompositions de a et b alignées, facteurs communs reliés (`link` : `"bubble"`, `"line"` ou `"none"`). Dans `c…
- `decomp-frac` — `\DecompFrac[options]{a}{b}` : fraction a/b, numérateur et dénominateur décomposés, facteurs communs mis en valeur par `cf-style` (`"arithm…
- `fracirr` — `\fracirr{a}{b}` : fraction irréductible égale à a/b (taille du texte).
- `dfracirr` — `\dfracirr{a}{b}` : fraction irréductible égale à a/b, en taille « display ».

## setrdarithm

```typ
setrdarithm(pour: none, reinitialiser: false, definir: none, ..cles)
```

`setrdarithm(clés)` : le réglage de rdarithm, sous ses quatre formes.

- `setrdarithm(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdarithm(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` ; un style peut en appeler un autre, la clé locale l'emporte. - `setrdarithm(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

Clés (option LaTeX → clé Typst, espaces → tirets) :

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (rdarithm n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. | nom/.style={…} |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `colors` | `("arithmcol1", "arithmcol2")` | array \| str |  | couleurs des boîtes, traits et liens, en boucle. |
| `node-opacity` | `0.25` | float |  | opacité des boîtes de la mise en page `"etapes"`. |
| `node-style` | `none` | dictionary |  | style des restes encadrés de la mise en page `"etapes"` (text, font, inset…). |
| `decorate` | `true` | bool |  | boîtes et traits de la mise en page `"etapes"`. |
| `stop` | `0` | int |  | nombre d'étapes affichées (0 : toutes). |
| `powers` | `"none"` | str \| bool |  | `"none"`, `"right"`, `"bottom"` (`true` = `"bottom"`) : écriture avec exposants. |
| `crep` | `false` | bool |  | chaque valeur dans une boîte réponse \\tccrep (vide en version élève). |
| `crep-width` | `3em` | length |  | largeur des boîtes réponse. |
| `crep-style` | `(seyes: true, boxsep: 1pt, opacityback: 0.6, left: 2pt, right: 2pt)` | dictionary |  | clés de `tccrep`. |
| `prime-style` | `défaut du paquet` | dictionary |  | style des facteurs premiers. Défaut : fond arithmcol1 à 25 %, contour arithmcol1, gras. |
| `prime-append-style` | `défaut du paquet` | dictionary |  | style des facteurs premiers. Défaut : fond arithmcol1 à 25 %, contour arithmcol1, gras. |
| `cell-style` | `none` | dictionary |  | style de toutes les cellules. |
| `cell-append-style` | `none` | dictionary |  | style de toutes les cellules. |
| `cell` | `none` | dictionary |  | style d'une cellule (`cell 1`, `cell m-n`) : `("1": (fill: blue), "3-2": (fill: green))`. |
| `picture-style` | `none` | dictionary |  | `draw` (couleur des traits), `fill`, `radius`, `inset` (fond). |
| `level-distance` | `8mm` | length |  | distance entre niveaux (ou rangées) ; entre frères. |
| `sibling-distance` | `15mm` | length |  | distance entre niveaux (ou rangées) ; entre frères. |
| `label` | `"none"` | str \| bool |  | `"none"`, `"left"`, `"above"` (`true` = `"above"`). |
| `label-style` | `none` | dictionary |  | libellé. |
| `prefix-label` | `none` | content |  | libellé. |
| `suffix-label` | `none` | content |  | libellé. |
| `label-extrasep` | `0mm` | length |  | libellé. |
| `overlay` | `none` | function |  | `cellules => contenu` posé par-dessus (ancres `center`, `north-west`… des cellules `"cell 1"`, `"cell 2-1"`… ; aide `node`). |
| `column-sep` | `1mm` | length |  | espace entre colonnes ; épaisseur des traits. |
| `line-width` | `0.7pt` | length |  | espace entre colonnes ; épaisseur des traits. |
| `separator` | `[,~]` | content |  | séparateur de \\ListeFP et \\ListeDiviseurs. |
| `cf` | `0` | int |  | diviseurs communs avec `cf` mis en valeur. |
| `cf-style` | `(fill: "arithmcol3!50")` | dictionary |  | diviseurs communs avec `cf` mis en valeur. |
| `gcd-style` | `(fill: "arithmcol3")` | dictionary |  | diviseurs communs avec `cf` mis en valeur. |
| `tab-orientation` | `"horizontal"` | str |  | `"horizontal"` ou `"vertical"` (\\TabPGCD). |
| `header-style` | `défaut du paquet` | dictionary |  | entêtes de \\TabPGCD. Défaut : fond gris, gras ; `none` ; `[~:]`. |
| `prefix-header` | `défaut du paquet` | content |  | entêtes de \\TabPGCD. Défaut : fond gris, gras ; `none` ; `[~:]`. |
| `suffix-header` | `défaut du paquet` | content |  | entêtes de \\TabPGCD. Défaut : fond gris, gras ; `none` ; `[~:]`. |
| `rules` | `"all"` | str |  | `"none"`, `"all"`, `"horizontal"`, `"Horizontal"`, `"vertical"`, `"Vertical"`. |
| `rule-color` | `"black"` | color \| str |  | couleur des traits de \\TabPGCD. |
| `forced-width` | `0cm` | length |  | largeur imposée de \\TabPGCD. |
| `inner-xsep` | `3pt` | length |  | largeur imposée de \\TabPGCD. |
| `header-width` | `0cm` | length |  | largeur imposée de \\TabPGCD. |
| `frac-mode` | `"dfrac"` | str |  | `"frac"` ou `"dfrac"` (\\DecompFrac). |
| `link` | `"bubble"` | str |  | `"none"`, `"line"`, `"bubble"` (\\RowPGCD). |
| `line-style` | `none` | dictionary |  | style des liens `line` (shorten…). |
| `to` | `none` | dictionary |  | style du lien n° m (`to m`) : `("2": (out: -90, "in": 90))`. |
| `row-sep` | `1.24em + 3pt` | length |  | interligne des décompositions alignées (ajout ; \\baselineskip + \\jot). |
| `decoration-line-width` | `0.4pt` | length |  | trait des potences de la mise en page `"etapes"` (ajout). |
| `bubble-width` | `1.25mm` | length |  | épaisseur de la barre des bulles (ajout ; amplitude=1.25mm). |
| `bubble-line-width` | `0.7pt` | length |  | contour des bulles (ajout). |
| `cell-min-width` | `3em` | length |  | largeur minimale des cellules (ajout ; minimum width=3em). |
| `..cles` | (positionnel) | any |  | clés ci-dessus (et `style:`). |

Exemple :

```typ
#setrdarithm(colors: ("red", "green", "blue"))
#decomp-fp(mise-en-page: "etapes", 1260)
#setrdarithm(definir: "monstyle", cell-append-style: (radius: 2pt), prime-append-style: (fill-opacity: 1))
#decomp-fp(mise-en-page: "arbre", style: "monstyle", 126)
#setrdarithm(reinitialiser: "tout")
```

## liste-fp

```typ
liste-fp(separator: auto, style: auto, n)
```

`\ListeFP[options]{n}` : liste des facteurs premiers de n.

LaTeX : `\ListeFP`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `separator` | `auto` | auto, content | séparateur. Défaut : `[,~]`. | separator |
| `style` | `auto` | auto, str, array | style(s) nommé(s). Défaut : `auto`. |  |
| `n` | (positionnel) | int | entier à décomposer. |  |

Exemple :

```typ
Facteurs premiers de 210 : #liste-fp(210). Autre séparateur : #liste-fp(separator: [~-~], 210).
```

## decomp-fp

```typ
decomp-fp(mise-en-page: "produit", ..options, n)
```

`\DecompFP[options]{n}` : décomposition de n en facteurs premiers, dans la mise en page choisie par la clé `mise-en-page`. Elle remplace `\DecompFP` (produit), `\DecompFPA`, `\DecompFPB` et `\DecompFPC`.

`"produit"` (défaut, `\DecompFP`) : produit en ligne, `powers` écrit les facteurs égaux en puissances. `"etapes"` (`\DecompFPA`) : étapes alignées, restes encadrés et reliés (clés `decorate`, `colors`, `node-opacity`, `node-style`, `powers`, `stop`, `crep`, `row-sep`, `overlay`). `"arbre"` (`\DecompFPB`) : arbre, facteur premier à gauche et quotient à droite (`level-distance`, `sibling-distance`, `line-width`, `picture-style`, `cell-style`, `prime-style`, `cell`, `stop`, `crep`, `overlay`). `"tableau"` (`\DecompFPC`) : tableau à deux colonnes, quotients puis facteurs (`column-sep`, `label`, `prefix-label`, `suffix-label`, `cell-style`, `prime-style`, `cell`, `stop`, `crep`, `overlay`).

LaTeX : `\DecompFP`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mise-en-page` | `"produit"` | str | `"produit"`, `"etapes"`, `"arbre"` ou `"tableau"`. Défaut : `"produit"`. |  |
| `n` | (positionnel) | int | entier à décomposer. |  |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `setrdarithm` (celles qui n'ont pas de sens pour la mise en page choisie sont sans effet). |

Exemple :

```typ
$126 = #decomp-fp(126) = #decomp-fp(powers: true, 126)$

#decomp-fp(mise-en-page: "etapes", 1260) #h(5mm) #decomp-fp(mise-en-page: "arbre", 126)
#h(5mm) #decomp-fp(mise-en-page: "tableau", label: true, prefix-label: [Décomposition de~], 105)
```

## liste-diviseurs

```typ
liste-diviseurs(separator: auto, style: auto, n)
```

`\ListeDiviseurs[options]{n}` : liste ordonnée des diviseurs de n.

LaTeX : `\ListeDiviseurs`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `separator` | `auto` | auto, content | séparateur. Défaut : `[,~]`. | separator |
| `style` | `auto` | auto, str, array | style(s) nommé(s). Défaut : `auto`. |  |
| `n` | (positionnel) | int | entier. |  |

Exemple :

```typ
Les diviseurs de 40 : #liste-diviseurs(40).
```

## tab-diviseurs

```typ
tab-diviseurs(..options, n)
```

`\TabDiviseurs[options]{n}` : diviseurs rangés par paires dans un tableau à deux colonnes. Mêmes clés que `decomp-fp(mise-en-page: "tableau")`, plus `cf`, `cf-style` et `gcd-style` (diviseurs communs avec `cf`, PGCD).

LaTeX : `\TabDiviseurs`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int | entier. |  |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `setrdarithm`. |

Exemple :

```typ
#tab-diviseurs(label: true, prefix-label: [Diviseurs de ], level-distance: 5mm, cf: 75, 60)
```

## pgcd

```typ
pgcd(etoile: false, ..termes)
```

`\pgcd{a}{b}` : écrit PGCD(a ; b) ; `\pgcd*{a}{b}` (`etoile: true`) : renvoie la valeur (entier). Sans argument, `pgcd()` écrit l'opérateur « PGCD » seul.

- ..termes (int): les deux entiers a et b, ou aucun argument (opérateur « PGCD » seul).

LaTeX : `\pgcd`, `\pgcd*`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `etoile` | `false` | bool | renvoie le PGCD calculé. Défaut : `false`. | \\pgcd*, \\ppcm* |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..termes` | (positionnel) | int |  | les deux entiers a et b, ou aucun argument (opérateur « PGCD » seul). |

Exemple :

```typ
Le #pgcd() de 60 et 75. On a : $#pgcd(60, 75) = #pgcd(60, 75, etoile: true)$.
```

## ppcm

```typ
ppcm(etoile: false, ..termes)
```

`\ppcm{a}{b}` : écrit PPCM(a ; b) ; `\ppcm*{a}{b}` (`etoile: true`) : renvoie la valeur (entier). Sans argument, `ppcm()` écrit l'opérateur « PPCM » seul.

- ..termes (int): les deux entiers a et b, ou aucun argument (opérateur « PPCM » seul).

LaTeX : `\ppcm`, `\ppcm*`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `etoile` | `false` | bool | renvoie le PPCM calculé. Défaut : `false`. | \\pgcd*, \\ppcm* |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..termes` | (positionnel) | int |  | les deux entiers a et b, ou aucun argument (opérateur « PPCM » seul). |

Exemple :

```typ
Le #ppcm() de 60 et de 75 vaut #ppcm(60, 75, etoile: true).
```

## tab-pgcd

```typ
tab-pgcd(..options, a, b)
```

`\TabPGCD[options]{a}{b}` : tableau des facteurs premiers de a et b rangés en colonnes ; les facteurs communs (ceux du PGCD) reçoivent `gcd-style`. Clés utiles : `tab-orientation`, `header-style`, `prefix-header`, `suffix-header`, `rules`, `rule-color`, `forced-width`, `inner-xsep`, `header-width`, `line-width`, `level-distance`, `cell-style`, `gcd-style`, `cell`, `picture-style`, `overlay`, `crep`.

LaTeX : `\TabPGCD`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | int | premier entier. |  |
| `b` | (positionnel) | int | second entier. |  |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `setrdarithm`. |

Exemple :

```typ
#tab-pgcd(420, 126)

Ainsi $#pgcd(420, 126) = #decomp-fp(pgcd(420, 126, etoile: true)) = #pgcd(420, 126, etoile: true)$
```

## row-pgcd

```typ
row-pgcd(..options, a, b)
```

`\RowPGCD[options]{a}{b}` : décompositions de a et b alignées, facteurs communs reliés (`link` : `"bubble"`, `"line"` ou `"none"`). Dans `cf-style`, la couleur `"arithmcol"` désigne la couleur du couple courant (liste `colors`). Clés utiles : `colors`, `cf-style`, `link`, `line-width`, `line-style`, `to`, `cell` (`"1-k"`, `"2-k"`), `crep`.

LaTeX : `\RowPGCD`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | int | premier entier. |  |
| `b` | (positionnel) | int | second entier. |  |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `setrdarithm`. |

Exemple :

```typ
#row-pgcd(cf-style: (inset: 1.5pt), colors: ("arithmcol1!50", "arithmcol2!50", "arithmcol3!50"), 420, 126)
#h(1cm)
#row-pgcd(cf-style: (inset: 1.5pt, fill: "arithmcol"), link: "line", 420, 126)
```

## decomp-frac

```typ
decomp-frac(..options, a, b)
```

`\DecompFrac[options]{a}{b}` : fraction a/b, numérateur et dénominateur décomposés, facteurs communs mis en valeur par `cf-style` (`"arithmcol"` : couleur du couple). `frac-mode: "frac"` : fraction en ligne.

LaTeX : `\DecompFrac`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | int | numérateur. |  |
| `b` | (positionnel) | int | dénominateur. |  |

Clés documentées dans le guide (`rdarithm/docs/fiches-rdarithm.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | clés de `setrdarithm`. |

Exemple :

```typ
$105/273 = #decomp-frac(cf-style: (shape: "circle", inset: 1.5pt, fill: "arithmcol"),
  colors: ("arithmcol1!50", "arithmcol2!50"), 105, 273) = #dfracirr(105, 273)$
```

## fracirr

```typ
fracirr(a, b)
```

`\fracirr{a}{b}` : fraction irréductible égale à a/b (taille du texte).

LaTeX : `\fracirr`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | int | numérateur. |  |
| `b` | (positionnel) | int | dénominateur. |  |

Exemple :

```typ
On a $15/45 = #fracirr(15, 45)$.
```

## dfracirr

```typ
dfracirr(a, b)
```

`\dfracirr{a}{b}` : fraction irréductible égale à a/b, en taille « display ».

LaTeX : `\dfracirr`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | int | numérateur. |  |
| `b` | (positionnel) | int | dénominateur. |  |

Exemple :

```typ
On a $display(63/96) = #dfracirr(63, 96)$.
```
