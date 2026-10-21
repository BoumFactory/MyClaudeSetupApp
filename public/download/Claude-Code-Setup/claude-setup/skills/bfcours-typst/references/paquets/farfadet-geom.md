# farfadet-geom

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": geom` puis `#import geom: *`.
- Réglage : `setbfgeom` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-geom.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-geom`).

## Sommaire

- `figure-geo` — Figure légendée (`figure`) contenant un `geo`. Même arguments que `geo`, plus la légende.
- `geo` — Canevas cetz aux couleurs de bfcours. Le corps appelle les macros du paquet (`repere`, `point`, `segment`…) ; une instruction cetz (`d.line…
- `setbfgeom` — Réglage du style des figures (convention commune des setters `setbf…`). Les appels s'ajoutent clé par clé ; une clé inconnue ou une valeur …
- `courbe` — Courbe d'une fonction, par échantillonnage : une ligne brisée de `n` points (sans bibliothèque de tracé). Les points hors de la fenêtre en …
- `repere` — Repère orthonormé : grille facultative, axes fléchés, graduations, origine et noms des axes. Il enregistre aussi la fenêtre de la figure, d…
- `arc` — Arc de cercle de centre `c`, de `debut` à `fin` (sens direct).
- `cercle` — Cercle de centre `c` et de rayon `r`.
- `demi-droite` — Demi-droite `[a b)` d'origine `a`, prolongée jusqu'au bord de la fenêtre.
- `droite` — Droite `(a b)` prolongée jusqu'aux bords de la fenêtre de la figure.
- `point` — Point marqué d'une croix (ou d'un disque), avec son nom placé autour. Le nom est le second argument (positionnel) ou la clé `nom`. Une chaî…
- `polygone` — Polygone fermé, avec noms des sommets placés vers l'extérieur et codages par côté ou par sommet.
- `segment` — Segment `[a b]`, avec codages facultatifs (traits de longueur égale, chevrons de parallélisme).
- `triangle` — Triangle `a b c` : cas particulier de `polygone` à trois sommets (mêmes clés).
- `fleche` — Vecteur de `a` vers `b` : flèche pleine et nom surmonté d'une flèche, placé au milieu.
- `fleche-de` — Vecteur de coordonnées `v` tracé à partir du point `a` (extrémité `a + v`).
- `axe` — Axe : trait fléché de `a` vers `b`, à l'épaisseur et à la flèche des repères (droite graduée, axe oblique…).
- `axes` — Deux axes fléchés qui se coupent en (0, 0), sans graduations ni quadrillage (voir `repere`).
- `etiquette` — Texte libre placé sur un point ou autour de lui.
- `ligne-brisee` — Ligne brisée par les points `pts`, ouverte ou fermée, éventuellement remplie.
- `quadrillage` — Quadrillage (sans axes) du rectangle `x` × `y`, aux multiples de `pas`.
- `angle-droit` — Marque d'angle droit (petit carré) au sommet, entre les deux côtés `sommet→a` et `sommet→b`.
- `angle-marque` — Angle marqué par un arc (simple, double ou triple), avec une valeur facultative.
- `codage-parallele` — Chevrons de parallélisme sur un segment : un segment par famille de parallèles (1, 2 ou 3 chevrons).
- `codage-segment` — Traits de codage au milieu d'un segment : 1, 2 ou 3 traits pour distinguer des longueurs égales.
- `bissectrice` — Bissectrice de l'angle `a sommet b`, tracée depuis le sommet, avec les deux angles marqués.
- `hauteur` — Hauteur issue de `a` dans le triangle `a b c` : segment de `a` à son projeté sur `(b c)`, avec l'angle droit et, si le pied sort du segment…
- `mediatrice` — Médiatrice de `[a b]`, avec son codage (deux moitiés égales et angle droit au milieu).
- `distance` — Distance entre deux points.
- `intersection` — Point d'intersection des droites `(a b)` et `(c d)` ; erreur si elles sont parallèles.
- `milieu` — Milieu de `[a b]`.
- `projete` — Projeté orthogonal de `p` sur la droite `(a b)`.

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `style` | style du trait. Défaut : `"plein"`. |  | 5 : `courbe`, `arc`, `cercle`, `polygone`, `fleche-de` |
| `couleur` | couleur du trait. Défaut : `auto`. |  | 3 : `arc`, `cercle`, `polygone` |
| `epaisseur` | épaisseur du trait. Défaut : `auto`. |  | 10 : `arc`, `cercle`, `demi-droite`, `droite`, `polygone`, `fleche-de`, `ligne-brisee`, `bissectrice` … |
| `couleur` | couleur. Défaut : `auto`. |  | 7 : `demi-droite`, `droite`, `segment`, `fleche`, `fleche-de`, `axe`, `axes` |
| `style` | `"plein"`, `"tirets"`, `"pointilles"` ou `"mixte"`. Défaut : `"plein"`. |  | 5 : `demi-droite`, `droite`, `segment`, `fleche`, `ligne-brisee` |
| `style` | style du trait. Défaut : `"tirets"`. |  | 3 : `bissectrice`, `hauteur`, `mediatrice` |

## figure-geo

```typ
figure-geo(corps, legende: none, unite: 1cm, fenetre: none)
```

Figure légendée (`figure`) contenant un `geo`. Même arguments que `geo`, plus la légende.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | suite de macros de dessin. |  |
| `legende` | `none` | none, content | légende de la figure. Défaut : `none`. |  |
| `unite` | `1cm` | length | longueur d'une unité du repère. Défaut : `1cm`. |  |
| `fenetre` | `none` | none, array | fenêtre de la figure. Défaut : `none`. |  |

## geo

```typ
geo(corps, unite: 1cm, fenetre: none)
```

Canevas cetz aux couleurs de bfcours. Le corps appelle les macros du paquet (`repere`, `point`, `segment`…) ; une instruction cetz (`d.line`, `d.content`…) y reste possible, avec `import cetz.draw`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | suite de macros de dessin, dans un bloc de code `{ … }`. |  |
| `unite` | `1cm` | length | longueur d'une unité du repère. Défaut : `1cm`. |  |
| `fenetre` | `none` | none, array | `((xmin, ymin), (xmax, ymax))`, utilisée par `droite`, `demi-droite`, `courbe` si aucun repère n'est tracé. Défaut : `none`. |  |

Exemple :

```typ
#geo({
  repere(x: (-1, 4), y: (-1, 3))
  segment((0, 0), (3, 2))
  point((3, 2), "A", pos: "ne")
})
```

## setbfgeom

```typ
setbfgeom(pour: none, reinitialiser: false, definir: none, ..cles)
```

Réglage du style des figures (convention commune des setters `setbf…`). Les appels s'ajoutent clé par clé ; une clé inconnue ou une valeur invalide arrête la compilation avec la liste des possibilités.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none | sans objet (pas de types d'objets) ; gardé pour la signature commune. |  |
| `reinitialiser` | `false` | bool, str | `true` repart des défauts avant d'appliquer les clés ; `"tout"` ramène aussi les styles prédéfinis. |  |
| `definir` | `none` | none, str | définit le style nommé de ce nom au lieu de régler (appelé ensuite par `style:`). |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleur` | `black` | color |  | Couleur des traits et des noms. |
| `couleur-bleu, couleur-rouge, couleur-vert, couleur-orange, couleur-rose, couleur-gris` | `couleurs nommées de bfcours` | color |  | Couleurs appelées par `couleur: "bleu"` et les autres noms. Défauts : `prop`, `thm`, `defi`, `demo`, `monrose`, `rem`. |
| `couleur-grille` | `rem à 40 %` | color |  | Couleur du quadrillage. |
| `epaisseur` | `0.9pt` | length |  | Trait ordinaire, axes, codages. |
| `epaisseur-fine` | `0.5pt` | length |  | Quadrillage, prolongements. |
| `epaisseur-forte` | `1.4pt` | length |  | Courbes et vecteurs. |
| `forme-point` | `"croix"` | str | `croix`, `disque` | Forme des points. |
| `taille-point` | `3pt` | length |  | Demi-diagonale de la croix, rayon du disque. |
| `taille-codage` | `3pt` | length |  | Demi-longueur des traits de codage. |
| `taille-angle-droit` | `0.3cm` | length |  | Côté du carré d'angle droit. |
| `rayon-angle` | `0.65cm` | length |  | Rayon de l'arc d'angle marqué. |
| `taille-texte` | `auto` | length \| auto |  | Taille des noms ; `auto` : celle du document. |
| `espace-etiquette` | `4pt` | length |  | Écart entre un point et son nom. |
| `fleche` | `"stealth"` | str | `stealth`, `>`, `triangle`, `straight` | Pointe des vecteurs et des axes. |

## courbe

```typ
courbe(f, x: auto, n: 150, coupures: (), couleur: "bleu", epaisseur: auto, style: "plein")
```

Courbe d'une fonction, par échantillonnage : une ligne brisée de `n` points (sans bibliothèque de tracé). Les points hors de la fenêtre en ordonnée sont coupés au bord ; `coupures` interrompt la courbe aux abscisses où la fonction n'est pas définie (par exemple `0` pour `1/x`).

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `f` | (positionnel) | function | fonction `x => …` qui renvoie un nombre. |  |
| `x` | `auto` | auto, array | intervalle `(min, max)` du tracé. Défaut : `auto` (l'intervalle des abscisses du repère). |  |
| `n` | `150` | int | nombre d'intervalles de l'échantillonnage. Défaut : `150`. |  |
| `coupures` | `()` | array | abscisses où interrompre la courbe. Défaut : `()`. |  |
| `couleur` | `"bleu"` | auto, str, color | couleur. Défaut : `"bleu"`. |  |
| `epaisseur` | `auto` | auto, length | épaisseur du trait. Défaut : `auto` (clé `epaisseur-forte`). |  |

## repere

```typ
repere(x: (-1, 5), y: (-1, 4), grille: true, pas: 1, graduations: true, pas-graduation: auto, origine: true, nom-origine: $O$, noms: ($x$, $y$), couleur: auto)
```

Repère orthonormé : grille facultative, axes fléchés, graduations, origine et noms des axes. Il enregistre aussi la fenêtre de la figure, dont se servent `droite`, `demi-droite`, `courbe` et `mediatrice`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `x` | `(-1, 5)` | array | intervalle des abscisses `(min, max)`. Défaut : `(-1, 5)`. |  |
| `y` | `(-1, 4)` | array | intervalle des ordonnées `(min, max)`. Défaut : `(-1, 4)`. |  |
| `grille` | `true` | bool | quadrillage au pas `pas`. Défaut : `true`. |  |
| `pas` | `1` | int, float, array | pas du quadrillage, ou `(pas-x, pas-y)`. Défaut : `1`. |  |
| `graduations` | `true` | bool | nombres sous l'axe des abscisses et à gauche de l'axe des ordonnées. Défaut : `true`. |  |
| `pas-graduation` | `auto` | auto, int, float, array | pas des graduations, ou `(pas-x, pas-y)`. Défaut : `auto` (le pas du quadrillage). |  |
| `origine` | `true` | bool | écrit le nom de l'origine. Défaut : `true`. |  |
| `nom-origine` | `$O$` | content | nom de l'origine. Défaut : `$O$`. |  |
| `noms` | `($x$, $y$)` | array | noms des axes `(nom-x, nom-y)`, ou `(none, none)`. Défaut : `($x$, $y$)`. |  |
| `couleur` | `auto` | auto, str, color | couleur des axes et des nombres. Défaut : `auto`. |  |

## arc

```typ
arc(c, r, debut, fin, couleur: auto, epaisseur: auto, style: "plein")
```

Arc de cercle de centre `c`, de `debut` à `fin` (sens direct).

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `c` | (positionnel) | array | centre `(x, y)`. |  |
| `r` | (positionnel) | int, float, length, array | rayon, ou point du cercle. |  |
| `debut` | (positionnel) | angle | angle de départ (`20deg`). |  |
| `fin` | (positionnel) | angle | angle d'arrivée (`110deg`). |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleur, epaisseur, style` | `comme cercle` | — |  | Mêmes clés que `cercle`. |

## cercle

```typ
cercle(c, r, remplissage: none, couleur: auto, epaisseur: auto, style: "plein")
```

Cercle de centre `c` et de rayon `r`.

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `c` | (positionnel) | array | centre `(x, y)`. |  |
| `r` | (positionnel) | int, float, length, array | rayon (en unités de la figure), ou point du cercle. |  |
| `remplissage` | `none` | none, str, color | fond (un nom de couleur donne sa version claire). Défaut : `none`. |  |

## demi-droite

```typ
demi-droite(a, b, couleur: auto, epaisseur: auto, style: "plein", fenetre: auto)
```

Demi-droite `[a b)` d'origine `a`, prolongée jusqu'au bord de la fenêtre.

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | origine. |  |
| `b` | (positionnel) | array | un autre point de la demi-droite. |  |
| `fenetre` | `auto` | auto, array | fenêtre `((xmin, ymin), (xmax, ymax))`. Défaut : `auto`. |  |

## droite

```typ
droite(a, b, couleur: auto, epaisseur: auto, style: "plein", fenetre: auto)
```

Droite `(a b)` prolongée jusqu'aux bords de la fenêtre de la figure.

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | un point de la droite. |  |
| `b` | (positionnel) | array | un autre point de la droite. |  |
| `fenetre` | `auto` | auto, array | `((xmin, ymin), (xmax, ymax))` ; `auto` prend celle de `geo` ou de `repere`. Défaut : `auto`. |  |

## point

```typ
point(p, ..autres, nom: none, pos: "ne", forme: auto, taille: auto, couleur: auto)
```

Point marqué d'une croix (ou d'un disque), avec son nom placé autour. Le nom est le second argument (positionnel) ou la clé `nom`. Une chaîne `"A"` est écrite en maths (`$A$`).

LaTeX : `\point`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `p` | (positionnel) | array | coordonnées `(x, y)`. |  |
| `nom` | `none` | none, str, content | nom du point, comme second argument positionnel. |  |
| `pos` | `"ne"` | str, angle | où se place le nom autour du point : `"n"`, `"s"`, `"e"`, `"o"`, `"ne"`, `"no"`, `"se"`, `"so"` ou un angle. Défaut : `"ne"`. |  |
| `forme` | `auto` | auto, str | `"croix"` ou `"disque"`. Défaut : `auto` (clé `forme-point`). |  |
| `taille` | `auto` | auto, length | demi-diagonale de la croix, ou rayon du disque. Défaut : `auto` (clé `taille-point`). |  |
| `couleur` | `auto` | auto, str, color | couleur du point et de son nom (`"rouge"`, `"rose"`…). Défaut : `auto`. |  |

## polygone

```typ
polygone(sommets, noms: none, pos-noms: auto, codages: none, paralleles: none, angles-droits: (), remplissage: none, couleur: auto, epaisseur: auto, style: "plein")
```

Polygone fermé, avec noms des sommets placés vers l'extérieur et codages par côté ou par sommet.

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sommets` | (positionnel) | array | au moins trois points `(x, y)`, dans l'ordre. |  |
| `noms` | `none` | none, array | noms des sommets (`("A", "B", "C")`), placés à l'opposé du centre. Défaut : `none`. |  |
| `pos-noms` | `auto` | auto, array | positions des noms (comme pour `point`), un par sommet ; `auto` les place vers l'extérieur. Défaut : `auto`. |  |
| `codages` | `none` | none, array | par côté `[Si Si+1]`, 1, 2, 3 traits ou `none` (`(1, 2, 1, 2)` pour un parallélogramme). Défaut : `none`. |  |
| `paralleles` | `none` | none, array | par côté, 1, 2, 3 chevrons ou `none`. Défaut : `none`. |  |
| `angles-droits` | `()` | array | indices (à partir de 0) des sommets où figure un angle droit. Défaut : `()`. |  |
| `remplissage` | `none` | none, str, color | fond. Défaut : `none`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleur, epaisseur, style` | `comme segment` | — |  | Trait du contour. |

## segment

```typ
segment(a, b, couleur: auto, epaisseur: auto, style: "plein", codage: none, parallele: none)
```

Segment `[a b]`, avec codages facultatifs (traits de longueur égale, chevrons de parallélisme).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | première extrémité `(x, y)`. |  |
| `b` | (positionnel) | array | seconde extrémité `(x, y)`. |  |
| `epaisseur` | `auto` | auto, length | épaisseur du trait. Défaut : `auto` (clé `epaisseur`). |  |
| `codage` | `none` | none, int | 1, 2 ou 3 traits au milieu. Défaut : `none`. |  |
| `parallele` | `none` | none, int | 1, 2 ou 3 chevrons au milieu. Défaut : `none`. |  |

## triangle

```typ
triangle(a, b, c, ..options)
```

Triangle `a b c` : cas particulier de `polygone` à trois sommets (mêmes clés).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | premier sommet. |  |
| `b` | (positionnel) | array | deuxième sommet. |  |
| `c` | (positionnel) | array | troisième sommet. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b, c` | (positionnel) | array |  | Les trois sommets. |
| `..options` | `—` | — |  | Toutes les clés de `polygone`. |

## fleche

```typ
fleche(a, b, nom: none, pos: auto, couleur: auto, epaisseur: auto, style: "plein")
```

Vecteur de `a` vers `b` : flèche pleine et nom surmonté d'une flèche, placé au milieu.

LaTeX : `\Vecteur`

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | origine. |  |
| `b` | (positionnel) | array | extrémité. |  |
| `nom` | `none` | none, str, content | nom du vecteur (`"u"`, `"A B"`) ; la flèche au-dessus est ajoutée. Défaut : `none`. |  |
| `pos` | `auto` | auto, str, angle | position du nom (comme pour `point`). Défaut : `auto` (à gauche du sens de la flèche). |  |
| `epaisseur` | `auto` | auto, length | épaisseur du trait. Défaut : `auto` (clé `epaisseur-forte`). |  |

## fleche-de

```typ
fleche-de(a, v, nom: none, pos: auto, couleur: auto, epaisseur: auto, style: "plein")
```

Vecteur de coordonnées `v` tracé à partir du point `a` (extrémité `a + v`).

Clés communes acceptées (voir en tête) : `couleur`, `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | origine. |  |
| `v` | (positionnel) | array | coordonnées `(dx, dy)` du vecteur. |  |
| `nom` | `none` | none, str, content | nom du vecteur. Défaut : `none`. |  |
| `pos` | `auto` | auto, str, angle | position du nom. Défaut : `auto`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `nom, pos, couleur, epaisseur, style` | `comme vecteur` | — |  | Mêmes clés que `fleche`. |

## axe

```typ
axe(a, b, couleur: auto)
```

Axe : trait fléché de `a` vers `b`, à l'épaisseur et à la flèche des repères (droite graduée, axe oblique…).

Clés communes acceptées (voir en tête) : `couleur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | origine. |  |
| `b` | (positionnel) | array | extrémité (côté flèche). |  |

## axes

```typ
axes(x: (-1, 5), y: (-1, 4), couleur: auto)
```

Deux axes fléchés qui se coupent en (0, 0), sans graduations ni quadrillage (voir `repere`).

Clés communes acceptées (voir en tête) : `couleur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `x` | `(-1, 5)` | array | intervalle `(x0, x1)` de l'axe horizontal. |  |
| `y` | `(-1, 4)` | array | intervalle `(y0, y1)` de l'axe vertical. |  |

## etiquette

```typ
etiquette(p, corps, pos: auto, couleur: auto, taille: auto)
```

Texte libre placé sur un point ou autour de lui.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `p` | (positionnel) | array | coordonnées `(x, y)`. |  |
| `corps` | (positionnel) | content, str | texte de l'étiquette, écrit tel quel (pas de passage en maths). |  |
| `pos` | `auto` | auto, str, angle | où se place le texte autour du point : `"n"`, `"s"`, `"e"`, `"o"`, `"ne"`, `"no"`, `"se"`, `"so"` ou un angle. Défaut : `auto` (centré sur le point). |  |
| `couleur` | `auto` | auto, str, color | couleur du texte. Défaut : `auto`. |  |
| `taille` | `auto` | auto, length | taille du texte. Défaut : `auto` (clé `taille-texte`). |  |

## ligne-brisee

```typ
ligne-brisee(pts, ferme: false, remplissage: none, couleur: auto, epaisseur: auto, style: "plein")
```

Ligne brisée par les points `pts`, ouverte ou fermée, éventuellement remplie.

Clés communes acceptées (voir en tête) : `epaisseur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pts` | (positionnel) | array | au moins deux points `(x, y)`. |  |
| `ferme` | `false` | bool | relie le dernier point au premier. Défaut : `false`. |  |
| `remplissage` | `none` | none, str, color | fond (un nom de couleur donne sa version claire). Défaut : `none`. |  |
| `couleur` | `auto` | auto, none, str, color | couleur du trait ; `none` : pas de trait (fond seul). Défaut : `auto`. |  |

## quadrillage

```typ
quadrillage(x: (-1, 5), y: (-1, 4), pas: 1)
```

Quadrillage (sans axes) du rectangle `x` × `y`, aux multiples de `pas`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `x` | `(-1, 5)` | array | intervalle `(x0, x1)`. |  |
| `y` | `(-1, 4)` | array | intervalle `(y0, y1)`. |  |
| `pas` | `1` | int, float, array | écart entre deux traits, ou `(pas-x, pas-y)`. Défaut : `1`. |  |

## angle-droit

```typ
angle-droit(sommet, a, b, taille: auto, couleur: auto)
```

Marque d'angle droit (petit carré) au sommet, entre les deux côtés `sommet→a` et `sommet→b`.

LaTeX : `\angleDroit`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sommet` | (positionnel) | array | sommet de l'angle. |  |
| `a` | (positionnel) | array | un point du premier côté. |  |
| `b` | (positionnel) | array | un point du second côté. |  |
| `taille` | `auto` | auto, length | côté du carré. Défaut : `auto` (clé `taille-angle-droit`). |  |
| `couleur` | `auto` | auto, str, color | couleur du codage. |  |

## angle-marque

```typ
angle-marque(sommet, a, b, n: 1, valeur: none, rayon: auto, couleur: auto)
```

Angle marqué par un arc (simple, double ou triple), avec une valeur facultative.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sommet` | (positionnel) | array | sommet de l'angle. |  |
| `a` | (positionnel) | array | un point du premier côté. |  |
| `b` | (positionnel) | array | un point du second côté. |  |
| `n` | `1` | int | nombre d'arcs (1, 2 ou 3). Défaut : `1`. |  |
| `valeur` | `none` | none, content | texte écrit à côté de l'arc, par exemple `$60°$`. Défaut : `none`. |  |
| `rayon` | `auto` | auto, length, int, float | rayon de l'arc intérieur. Défaut : `auto` (clé `rayon-angle`). |  |
| `couleur` | `auto` | auto, str, color | couleur de l'arc. |  |

## codage-parallele

```typ
codage-parallele(a, b, n: 1, couleur: auto)
```

Chevrons de parallélisme sur un segment : un segment par famille de parallèles (1, 2 ou 3 chevrons).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | première extrémité, qui donne le sens des chevrons. |  |
| `b` | (positionnel) | array | seconde extrémité. |  |
| `n` | `1` | int | nombre de chevrons (1, 2 ou 3). Défaut : `1`. |  |
| `couleur` | `auto` | auto, str, color | couleur du codage. |  |

## codage-segment

```typ
codage-segment(a, b, n: 1, couleur: auto)
```

Traits de codage au milieu d'un segment : 1, 2 ou 3 traits pour distinguer des longueurs égales.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | première extrémité `(x, y)`. |  |
| `b` | (positionnel) | array | seconde extrémité `(x, y)`. |  |
| `n` | `1` | int | nombre de traits (1, 2 ou 3). Défaut : `1`. |  |
| `couleur` | `auto` | auto, str, color | couleur du codage. Défaut : `auto` (couleur principale). |  |

## bissectrice

```typ
bissectrice(sommet, a, b, longueur: auto, codage: true, couleur: "bleu", style: "tirets", epaisseur: auto)
```

Bissectrice de l'angle `a sommet b`, tracée depuis le sommet, avec les deux angles marqués.

Clés communes acceptées (voir en tête) : `style`, `epaisseur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sommet` | (positionnel) | array | sommet de l'angle. |  |
| `a` | (positionnel) | array | un point du premier côté. |  |
| `b` | (positionnel) | array | un point du second côté. |  |
| `longueur` | `auto` | auto, int, float, length | longueur de la demi-droite tracée. Défaut : `auto` (moyenne des deux côtés). |  |
| `codage` | `true` | bool | marque les deux angles égaux par un arc. Défaut : `true`. |  |
| `couleur` | `"bleu"` | auto, str, color | couleur. Défaut : `"bleu"`. |  |

## hauteur

```typ
hauteur(a, b, c, codage: true, couleur: "rouge", style: "tirets", epaisseur: auto)
```

Hauteur issue de `a` dans le triangle `a b c` : segment de `a` à son projeté sur `(b c)`, avec l'angle droit et, si le pied sort du segment `[b c]`, le prolongement de `(b c)` en pointillés.

Clés communes acceptées (voir en tête) : `style`, `epaisseur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | sommet d'où part la hauteur. |  |
| `b` | (positionnel) | array | première extrémité du côté opposé. |  |
| `c` | (positionnel) | array | seconde extrémité du côté opposé. |  |
| `codage` | `true` | bool | trace l'angle droit au pied. Défaut : `true`. |  |
| `couleur` | `"rouge"` | auto, str, color | couleur. Défaut : `"rouge"`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `b, c` | (positionnel) | array |  | Extrémités du côté opposé. |

## mediatrice

```typ
mediatrice(a, b, longueur: auto, codage: true, couleur: "vert", style: "tirets", epaisseur: auto)
```

Médiatrice de `[a b]`, avec son codage (deux moitiés égales et angle droit au milieu).

Clés communes acceptées (voir en tête) : `style`, `epaisseur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | première extrémité. |  |
| `b` | (positionnel) | array | seconde extrémité. |  |
| `longueur` | `auto` | auto, int, float, length, str | demi-longueur du tracé de chaque côté du milieu ; `"fenetre"` prolonge jusqu'aux bords de la fenêtre. Défaut : `auto` (80 % de `[a b]`). |  |
| `codage` | `true` | bool | trace les traits d'égalité et l'angle droit. Défaut : `true`. |  |
| `couleur` | `"vert"` | auto, str, color | couleur. Défaut : `"vert"`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b` | (positionnel) | array |  | Les extrémités du segment. |

## distance

```typ
distance(a, b)
```

Distance entre deux points.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | point `(x, y)`. |  |
| `b` | (positionnel) | array | point `(x, y)`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b` | (positionnel) | array |  | Deux points. |

## intersection

```typ
intersection(a, b, c, d)
```

Point d'intersection des droites `(a b)` et `(c d)` ; erreur si elles sont parallèles.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | point de la première droite. |  |
| `b` | (positionnel) | array | second point de la première droite. |  |
| `c` | (positionnel) | array | point de la seconde droite. |  |
| `d` | (positionnel) | array | second point de la seconde droite. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b` | (positionnel) | array |  | Deux points de la première droite. |
| `c, d` | (positionnel) | array |  | Deux points de la seconde droite. |

## milieu

```typ
milieu(a, b)
```

Milieu de `[a b]`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | array | point `(x, y)`. |  |
| `b` | (positionnel) | array | point `(x, y)`. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b` | (positionnel) | array |  | Les extrémités. |

## projete

```typ
projete(p, a, b)
```

Projeté orthogonal de `p` sur la droite `(a b)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `p` | (positionnel) | array | point à projeter. |  |
| `a` | (positionnel) | array | premier point de la droite. |  |
| `b` | (positionnel) | array | second point de la droite. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `a, b` | (positionnel) | array |  | Deux points de la droite $(A B)$. |
