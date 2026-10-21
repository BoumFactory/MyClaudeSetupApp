# farfadet-extras

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": extras` puis `#import extras: *`.
- Réglage : `setbfextras` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-extras.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-extras`).

## Sommaire

- `setbfextras` — Règle les commandes du paquet pour toute la suite du document. Les clés valables dépendent de la commande visée (`pour:`) ; une clé inconnu…
- `clip-image` — L'image est mise à l'échelle pour couvrir la zone `largeur × hauteur`, puis rognée à droite ou en bas (le coin haut gauche est conservé).
- `colored-small-box` — Une perforation de la couleur de la clé `colored-small-box` (blanche par défaut ; se règle par `setbfextras(pour: "film", ColoredSmallBox: …
- `filmbox` — Pellicule de film : un cadre noir percé de perforations en haut et en bas autour de chaque contenu. Une seule commande pour une vignette is…
- `filmt` — Vignette bicolore dans un cadre de film : partie haute blanche (`haut`), partie basse grise (`bas`), cadre noir, hauteur totale `hauteur`.
- `whitebox` — Une perforation, centrée entre deux ressorts `h(1fr)`, à placer dans une `box` de largeur fixée pour composer une bande à la main.
- `bf-code-python` — Code Python mis en forme dans une boîte : coloration, numéros de ligne facultatifs, titre.
- `habiller` — Place une figure sur un côté et fait couler le texte autour d'elle, sur la hauteur de la figure ; en dessous, le texte reprend toute la lar…
- `icone` — Icône Feather à insérer dans le texte (environ 280 pictogrammes : `"book"`, `"check"`, `"alert-triangle"`, `"clock"`, `"edit-2"`, `"help-ci…

## setbfextras

```typ
setbfextras(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les commandes du paquet pour toute la suite du document. Les clés valables dépendent de la commande visée (`pour:`) ; une clé inconnue ou une valeur invalide arrête la compilation en listant les possibilités.

Priorité : clé locale > style nommé > réglage du type (`pour:`) > réglage global > défaut.

Types : `"filmbox"` (mode `"image"`), `"filmbox-rogne"` (mode `"rogne"`), `"filmbox-texte"` (mode `"texte"`), `"filmt"`, `"BFCodePython"`, `"habiller"`, `"icone"`. Le groupe `"film"` vise les quatre types de film d'un coup : chacun reçoit celles des clés qu'il connaît. Styles prédéfinis de `bf-code-python` : `"classique"`, `"sobre"`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str, array | type, tableau de types ou groupe visé ; `none` : réglage global (chaque commande qui a la clé la reçoit). |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages global et par type (les styles nommés restent) ; avec des clés, repart des défauts puis les applique ; `"tout"` : oublie aussi les styles de l'utilisateur et remet les styles prédéfinis à le… |  |
| `definir` | `none` | none, str | définit le style nommé de ce nom, appelé ensuite par la clé `style:` d'une commande ; `pour` contrôle alors les clés contre un type. |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | Les clés à régler. |

Exemple :

```typ
#setbfextras(pour: "film", fond: "blue!50!black", perforation-couleur: "yellow")
#setbfextras(pour: "BFCodePython", title: "Python")
#setbfextras(definir: "rouge", pour: "film", fond: "red!60!black", perforation-couleur: "orange")
#filmbox(style: "rouge", rect(width: 3cm, height: 2cm, fill: luma(200)))
#setbfextras(reinitialiser: true)
```

## clip-image

```typ
clip-image(largeur, hauteur, image)
```

L'image est mise à l'échelle pour couvrir la zone `largeur × hauteur`, puis rognée à droite ou en bas (le coin haut gauche est conservé).

La syntaxe environnement donne le même résultat : `#begin(clip-image, 2cm, 3cm)`, l'image, puis `#end(clip-image)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `largeur` | (positionnel) | length | largeur de la zone. |  |
| `hauteur` | (positionnel) | length | hauteur de la zone. |  |
| `image` | (positionnel) | content | l'image, en contenu (`image("a.png")`). |  |

Exemple :

```typ
#clip-image(2cm, 3cm, rect(width: 4cm, height: 3cm, fill: gradient.linear(red, blue))[A])
```

## colored-small-box

```typ
colored-small-box(..options)
```

Une perforation de la couleur de la clé `colored-small-box` (blanche par défaut ; se règle par `setbfextras(pour: "film", ColoredSmallBox: …)`), entre deux ressorts `h(1fr)`.

- ..options (any): clés du type `filmbox` : `colored-small-box`, `perforation-largeur`, `perforation-hauteur`, `style`.

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | Clés `colored-small-box`, `perforation-largeur`, `perforation-hauteur`, `style`. |

Exemple :

```typ
#setbfextras(pour: "film", ColoredSmallBox: "orange")
#box(width: 4cm, fill: black, height: 6mm)[#colored-small-box()#whitebox()#colored-small-box()]
#setbfextras(reinitialiser: true)
```

## filmbox

```typ
filmbox(..contenus, n: auto, mode: "image")
```

Pellicule de film : un cadre noir percé de perforations en haut et en bas autour de chaque contenu. Une seule commande pour une vignette isolée comme pour une rangée : `n` vignettes par ligne, les suivantes passent à la ligne.

Trois modes : - `"image"` (défaut) : cadre de 3,2 cm, image à 3 cm de large (proportions conservées) ; - `"rogne"` : l'image est rognée à 3 × 3 cm (`clip-image`) et la bande haute alterne perforations colorées (`colored-small-box`) et blanches ; - `"texte"` : cadre de 4,5 cm autour d'un contenu quelconque, centré. Le texte noir sur le fond noir est invisible : posez-le sur un fond clair (`box(fill: white)[…]`) ou réglez `couleur-texte: white`.

Le corps est UN SEUL bloc `[…]` : une vignette par `-`. La syntaxe environnement donne le même résultat : `#begin(filmbox, mode: "rogne")`, les `-`, puis `#end(filmbox)`. L'ancienne écriture `filmbox(a, b, c)` (une vignette par argument) arrête la compilation avec cet exemple.

- ..contenus (content): le corps : une vignette par `-` (images en contenu, `image("a.png")`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | `auto` | auto, int | nombre de vignettes par rangée ; `auto` : toutes sur une seule rangée. |  |
| `mode` | `"image"` | str | `"image"`, `"rogne"` ou `"texte"`. `image-hauteur` (3 cm, mode rogne), `fond` (noir), `perforations` (9), `perforation-largeur` (1,8 mm), `perforation-hauteur` (2,8 mm), `perforation-couleur` (blanc), `colored-small-box… |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..contenus` | (positionnel) | content |  | Les vignettes, une par argument (images en contenu). |

Exemple :

```typ
#let im(t) = rect(width: 4cm, height: 3cm, fill: luma(200))[#t]
#filmbox[- #im[A]]
#filmbox(mode: "rogne")[
  - #im[A]
  - #im[B]
  - #im[C]
]
#filmbox(mode: "rogne", n: 3, largeur: 2.8cm, image-largeur: 2.6cm, image-hauteur: 2.6cm)[
  - #im[1]
  - #im[2]
  - #im[3]
  - #im[4]
  - #im[5]
]
```

## filmt

```typ
filmt(haut, bas, ..options)
```

Vignette bicolore dans un cadre de film : partie haute blanche (`haut`), partie basse grise (`bas`), cadre noir, hauteur totale `hauteur`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `haut` | (positionnel) | content | contenu de la partie haute. |  |
| `bas` | (positionnel) | content | contenu de la partie basse. `colframe` (noir), `boxrule` (0,5 mm), `arc` (1 mm), `boxsep` (1 mm), `left`, `right`, `top`, `bottom` (4 pt) ; et celles du cadre de film : `fond`, `perforations`, `perforation-largeur`, `pe… |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `largeur` | `4.7cm` | length |  | Largeur du cadre. |
| `hauteur` | `6cm` | length |  | Hauteur totale. |
| `colback` | `"white"` | color \| str |  | Fond de la partie haute. |
| `colbacklower` | `"gray!50"` | color \| str |  | Fond de la partie basse. |
| `colframe` | `"black"` | color \| str |  | Cadre intérieur. |
| `boxrule` | `0.5mm` | length |  | Épaisseur du cadre intérieur. |
| `arc` | `1mm` | length |  | Coins arrondis. |
| `left, right, top, bottom` | `4pt` | length |  | Marges intérieures. |
| `..cles-film` | (positionnel) | any |  | Les clés du cadre de `filmbox` (fond, perforations, marges, `couleur-texte`, `style`…). |

Exemple :

```typ
#filmt[Question][Réponse]
#filmt(largeur: 3.5cm, hauteur: 4cm, colbacklower: "yellow!40")[Énoncé][Solution]
```

## whitebox

```typ
whitebox(..options)
```

Une perforation, centrée entre deux ressorts `h(1fr)`, à placer dans une `box` de largeur fixée pour composer une bande à la main.

- ..options (any): clés du type `filmbox` : `perforation-largeur`, `perforation-hauteur`, `perforation-couleur`, `style`.

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | (positionnel) | any |  | Clés `perforation-largeur`, `perforation-hauteur`, `perforation-couleur`, `style`. |

Exemple :

```typ
#box(width: 4cm, fill: black, height: 6mm)[#whitebox()#whitebox()#whitebox()]
```

## bf-code-python

```typ
bf-code-python(code, numeros: auto, ..options)
```

Code Python mis en forme dans une boîte : coloration, numéros de ligne facultatifs, titre.

Le style par défaut, `"classique"`, reprend le rendu de `bfcodepython` : fond vert très pâle, cadre vert forêt, coins arrondis en diagonale, titre « Code Python » dans un onglet en haut à droite. Le style `"sobre"` donne un cadre fin gris foncé, un fond blanc, un bandeau de titre sur toute la largeur et une bande grisée derrière les numéros.

La syntaxe environnement donne le même résultat : `#begin(bf-code-python, numeros: 3)`, le bloc `raw`, puis `#end(bf-code-python)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `code` | (positionnel) | str, content | le code, en bloc `raw` (```` ```python … ``` ````) ou en chaîne. |  |
| `numeros` | `auto` | auto, bool, int | `false` : sans numéros ; `true` : numérotées à partir de 1 ; un entier : numéro de la première ligne. Défaut : `auto` (selon les réglages ; `false` au départ). |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `style` | `auto` | str \| array |  | `"classique"` (défaut), `"sobre"`, ou un style défini par `setbfextras(definir: …)`. |
| `title` | `"Code Python"` | content \| none |  | Titre de la boîte ; `none` le supprime. |
| `titre-position` | `"onglet"` | str | `onglet`, `bandeau` | Place du titre. |
| `colframe` | `"CouleurVertForet"` | color \| str |  | Cadre. |
| `colback` | `"CouleurVertForet!5"` | color \| str |  | Fond. |
| `colbacktitle` | `"CouleurVertForet!25"` | color \| str |  | Fond du titre. |
| `boxrule` | `1.25pt` | length |  | Épaisseur du cadre. |
| `arc` | `12pt` | length |  | Coins arrondis. |
| `sharp-corners` | `"downhill"` | str | `none`, `all`, `downhill`, `uphill`, `north`, `south`, `east`, `west` | Coins carrés. |
| `left, right, top, bottom` | `0.6em + 1mm, 6mm, auto, 2mm` | length |  | Marges intérieures. |
| `before-skip, after-skip` | `auto` | length \| auto |  | Espaces avant et après la boîte. |
| `fonttitle` | `(:)` | dictionary |  | Police du titre : `size`, `style`, `weight`, `family`, `fill`. |
| `onglet` | `(:)` | dictionary |  | Onglet : `colframe`, `boxrule`, `arc`, `sharp-corners`, `left`, `hauteur`. |
| `basicstyle` | `"footnotesize"` | str \| length |  | Taille du code (nom de taille ou longueur). |
| `numberstyle` | `"scriptsize"` | str \| length |  | Taille des numéros. |
| `tabsize` | `4` | int |  | Largeur d'une tabulation, en espaces. |
| `police` | `auto` | auto \| str \| array |  | Police du code. |
| `pythonkeyword` | `"pythonkeyword"` | color \| str |  | Mots-clés (`def`, `for`…). |
| `pythonstring` | `"pythonstring"` | color \| str |  | Chaînes. |
| `pythoncomment` | `"pythoncomment"` | color \| str |  | Commentaires. |
| `pythonnumber` | `"pythonnumber"` | color \| str |  | Numéros de ligne. |
| `keywordstyle2` | `"magenta"` | color \| str |  | Fonctions et types prédéfinis (`print`, `range`…). |
| `numeros-fond` | `none` | color \| str \| none |  | Bande derrière les numéros (`"lightgray!25"` en style sobre). |
| `numeros-fond-largeur` | `1.6em` | length |  | Largeur de cette bande. |
| `surligner` | `()` | array |  | Numéros des lignes à surligner. |
| `couleur-surlignage` | `"yellow!40"` | color \| str |  | Couleur du surlignage. |

Exemple :

```typ
#bf-code-python(```python
def carre(x):
    # le carré de x
    return x * x
```)
#bf-code-python(numeros: 3, title: "Boucle", style: "sobre", ```python
for i in range(3):
    print(i)
```)
```

## habiller

```typ
habiller(figure, texte, ..options)
```

Place une figure sur un côté et fait couler le texte autour d'elle, sur la hauteur de la figure ; en dessous, le texte reprend toute la largeur. À mettre dans un paragraphe assez long : si le texte est plus court que la figure, la figure déborde en dessous.

La syntaxe environnement donne le même résultat : la figure et les options vont dans `#begin`, le texte entre `#begin` et `#end` : `#begin(habiller, fig, cote: "gauche")` … `#end(habiller)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `figure` | (positionnel) | content | ce qui est posé sur le côté : une image, une `figure`, un dessin. |  |
| `texte` | (positionnel) | content | le texte qui l'habille. `false` : en bas), `ecart` (1 em : distance figure-texte), `largeur` (`auto` : largeur réservée à la colonne de la figure), `debord` (0 pt : la figure déborde de cette longueur dans la marge), `s… |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cote` | `"droite"` | str | `droite`, `gauche` | Côté. |
| `haut` | `true` | bool |  | Figure en haut du texte (`false` : en bas). |
| `ecart` | `1em` | length |  | Distance figure - texte. |
| `largeur` | `auto` | length \| auto |  | Largeur de la colonne de la figure. |
| `debord` | `0pt` | length |  | La figure déborde de cette longueur dans la marge. |

Exemple :

```typ
#let fig = rect(width: 3.2cm, height: 2.4cm, fill: rgb("#dbe8f5"), stroke: 0.6pt + rgb("#2f5d8a"))[
  #align(center + horizon)[Figure]
]
#habiller(fig)[
  Dans un triangle rectangle, le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.
  Cette égalité permet de calculer une longueur manquante dès que les deux autres sont connues, et sa
  réciproque permet de prouver qu'un triangle est rectangle. On l'applique en trois temps : repérer
  l'hypoténuse, écrire l'égalité, puis résoudre l'équation obtenue.
]
```

## icone

```typ
icone(nom, ..options)
```

Icône Feather à insérer dans le texte (environ 280 pictogrammes : `"book"`, `"check"`, `"alert-triangle"`, `"clock"`, `"edit-2"`, `"help-circle"`…).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | le nom de l'icône (liste sur feathericons.com). de l'icône), `epaisseur` (2 ; 1 pour un trait fin), `decalage` (0,2 : descente sous la ligne de base, en fraction de la taille), `style`. |  |

Clés documentées dans le guide (`farfadet-extras/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleur` | `none` | color \| str \| none |  | Couleur (`none` : noir). |
| `taille` | `1em` | length |  | Hauteur de l'icône. |
| `epaisseur` | `2` | float |  | Épaisseur du trait (1 : fin). |
| `decalage` | `0.2` | float |  | Descente sous la ligne de base, en fraction de la taille. |

Exemple :

```typ
#icone("book") Lire le cours, #icone("edit-2") faire l'exercice, #icone("check", couleur: green) vérifier.
```
