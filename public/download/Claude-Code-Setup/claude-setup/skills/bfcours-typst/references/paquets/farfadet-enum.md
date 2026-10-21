# farfadet-enum

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": enumerations` puis `#import enumerations: *`.
- Réglage : `setbfenum` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-enum.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-enum`).

## Sommaire

- `setbfenum` — Règle les énumérations et le colonnage de bfcours : UN setter, comme tous les paquets farfadet-*. Sans `pour` : réglage global (chaque type…
- `multi-colonnes` — Dispose des contenus côte à côte, en colonnes : un énoncé et sa figure, trois remarques alignées, des exercices en grille… Le premier argum…
- `tcbitem` — Une case d'un `multi-colonnes`, d'un `tcbenumerate` ou d'un `tcbraster`, avec ses réglages propres : elle peut occuper plusieurs colonnes (…
- `tcbraster` — Place des boîtes en grille, comme `tcbraster` de tcolorbox (et `tcbitemize`, qui n'en est que le nom quand chaque argument est un `tcbitem`…
- `enumerate` — Liste numérotée de bfcours (`\begin{enumerate}[options]`) : numéros dans une pastille de la couleur des items, « 1. », « a. », « i. » selon…
- `itemize` — Liste à puces de bfcours (`\begin{itemize}[options]`, puces `•` à tous les niveaux) : le corps est un seul bloc `[…]` où chaque item s'écri…
- `tcbenumerate` — Énumération à pastilles, qui peut se répartir en colonnes : la liste des questions d'un exercice, en une colonne ou en plusieurs quand les …
- `bfd-enum-label` — Étiquette de la question courante (`\bfdEnumLabel`), au format du niveau, sans le point : « b » pour la deuxième sous-question. La clé `niv…
- `bfd-enum-level` — Profondeur d'imbrication courante des `tcbenumerate` (`\bfdEnumLevel`) : 1, 2, 3… (0 hors liste).
- `bfd-enum-num` — Numéro de la question courante d'un `tcbenumerate` (`\bfdEnumNum`), à placer dans le texte d'une question : « (réponse à la question #bfd-e…

## setbfenum

```typ
setbfenum(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les énumérations et le colonnage de bfcours : UN setter, comme tous les paquets farfadet-*. Sans `pour` : réglage global (chaque type qui connaît la clé la reçoit) ; avec `pour: "<type>"` (ou un tableau de types) : réglage d'un seul type : `"tcbenumerate"`, `"MultiColonnes"`, `"tcbraster"`, `"itemize"`, `"enumerate"`. La clé locale d'un appel l'emporte sur un style nommé, qui l'emporte sur le réglage du type, qui l'emporte sur le réglage global.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type (ou types) à régler ; `none` : réglage global. |  |
| `reinitialiser` | `false` | bool, str | `true` oublie les réglages global et par type (les styles nommés restent) ; avec des clés, repart des défauts puis les applique ; `"tout"` oublie aussi les styles nommés. |  |
| `definir` | `none` | str, none | définit le style nommé de ce nom (appelé ensuite par `style: "nom"`) ; `pour` contrôle alors les clés contre un type. |  |

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | (positionnel) | any |  | Les clés du type ou du style, nommées. |

Exemple :

```typ
#setbfenum(pour: "enumerate", couleur-etiquette: "red!70!black", labelsep: 8pt)
#setbfenum(pour: "MultiColonnes", colframe: gray, colback: luma(248))
#setbfenum(definir: "cartes", colframe: gray, arc: 4pt)
#setbfenum(reinitialiser: true)
```

## multi-colonnes

```typ
multi-colonnes(..args)
```

Dispose des contenus côte à côte, en colonnes : un énoncé et sa figure, trois remarques alignées, des exercices en grille… Le premier argument est le nombre de colonnes (`{n}` de LaTeX) ; chaque contenu `[…]` qui suit devient une case, et quand une rangée est pleine la suivante commence dessous. Les cases d'une même rangée ont la même hauteur (`raster-equal-height`).

Sans réglage, les colonnes sont invisibles : du texte côte à côte. Avec `colframe` ou `colback`, chaque case devient une boîte. Avec `filets`, un trait sépare les colonnes. Une case qui a besoin d'un réglage propre (largeur de plusieurs colonnes, fond, titre…) se fabrique par `tcbitem(…)`.

Les réglages se posent trois façons : sur l'appel (clés ci-dessous), par un style nommé (`style: "mon-style"`, défini par `setbfenum(definir: "mon-style", …)`) ou pour tout le document (`setbfenum(pour: "MultiColonnes", …)`, qui remplace le `\setColonnesBaseStyle` de LaTeX). La clé locale l'emporte sur le style nommé, qui l'emporte sur le réglage du type, qui l'emporte sur le réglage global.

Le corps est UN SEUL bloc `[…]` : une case par `-` (ou `#tcbitem(…)[…]`). Du texte écrit après une case lui est rattaché.

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `n` | (positionnel) | int |  | Nombre de colonnes (sinon : celui de `largeurs`, sinon 2). |
| `largeurs` | `auto` | array \| auto |  | Largeurs : longueurs, parts (`2fr`) ou nombres qui valent des parts. |
| `raster-column-skip` | `6pt` | length |  | Espace entre colonnes. |
| `raster-row-skip` | `6pt` | length |  | Espace entre rangées. |
| `raster-equal-height` | `"rows"` | str |  | `"rows"` (même hauteur par rangée) ou `"none"`. |
| `filets` | `none` | stroke \| none |  | Trait entre les colonnes. |
| `filets-lignes` | `none` | stroke \| none |  | Trait entre les rangées. |
| `colframe` | `none` | color \| str \| none |  | Cadre des cases. |
| `boxrule` | `0.4pt` | length |  | Épaisseur du cadre. |
| `colback` | `none` | color \| str \| none |  | Fond des cases. |
| `arc` | `3pt` | length |  | Rayon des coins. |
| `boxsep` | `auto` | length \| auto |  | Marge intérieure (`auto` : 5 pt si boîte, 0 sinon). |
| `halign` | `"left"` | str |  | `"left"`, `"justify"`, `"center"`, `"right"`. |
| `valign` | `"top"` | str |  | `"top"`, `"center"`, `"bottom"`. |
| `colbacktitle` | `rem!24` | color \| str \| none |  | Fond du bandeau de titre : couleur nommée `rem` à 24 %. |
| `coltitle` | `currentTitleColor` | color \| str \| none |  | Couleur du titre : couleur nommée `currentTitleColor` (noir). |
| `before-skip` | `0.9em` | length |  | Espace avant. |
| `after-skip` | `0.9em` | length |  | Espace après. |
| `cases` | (positionnel) | content |  | Les cases. |

Exemple :

```typ
#multi-colonnes(2)[
  - Un énoncé.
  - Sa figure.
]
#multi-colonnes(largeurs: (3, 2), filets: 0.5pt + gray)[
  - Énoncé
  - Figure
]
```

## tcbitem

```typ
tcbitem(tcb: none, ..args)
```

Une case d'un `multi-colonnes`, d'un `tcbenumerate` ou d'un `tcbraster`, avec ses réglages propres : elle peut occuper plusieurs colonnes (`raster-multicolumn`), avoir son fond (`colback`), son cadre (`colframe` et `boxrule`), son alignement, un titre. Une clé absente reprend le réglage de la disposition qui contient la case. Sans réglage propre, un simple contenu `[…]` suffit.

Un `tcbitem` s'écrit dans le corps de la disposition, à la place du `-` ou du `+` (jamais `+ #tcbitem`). Il renvoie un marqueur de contenu, lu par la disposition qui le contient : hors d'une disposition, la compilation s'arrête.

Dans un `tcbenumerate`, `numerote: false` (alias `count`) fait une case de transition : pas de pastille, et le compteur n'avance pas. Elle se combine avec `raster-multicolumn` (case sur toute la largeur).

LaTeX : `\tcbitem`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `tcb` | `none` | str, none | clés tcolorbox en syntaxe LaTeX, comme dans `\tcbitem[…]` : `"raster multicolumn=2, halign=center"`. Les clés nommées ci-dessous s'y ajoutent et l'emportent. |  |

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `numerote` | `true` | bool |  | `false` : case de transition, sans pastille, le compteur n'avance pas (`tcbenumerate`). Alias : `count`. |
| `raster-multicolumn` | `1` | int |  | Colonnes occupées. |
| `colback` | `auto` | color \| str \| none |  | Fond de la case. |
| `colframe` | `auto` | color \| str \| none |  | Cadre de la case. |
| `boxrule` | `0.4pt` | length |  | Épaisseur du cadre. |
| `halign` | `auto` | str |  | `"justify"`, `"left"`, `"center"`, `"right"`. |
| `valign` | `auto` | str |  | `"top"`, `"center"`, `"bottom"`. |
| `title` | `none` | content |  | Titre en bandeau. |
| `corps` | (positionnel) | content |  | Le contenu. |

Exemple :

```typ
#multi-colonnes(3)[
  #tcbitem(raster-multicolumn: 2)[Énoncé, sur deux colonnes]
  #tcbitem(colback: yellow.lighten(80%))[Remarque]
]
```

## tcbraster

```typ
tcbraster(tcb: none, every-box: none, ..args)
```

Place des boîtes en grille, comme `tcbraster` de tcolorbox (et `tcbitemize`, qui n'en est que le nom quand chaque argument est un `tcbitem`) : les clés `raster-*` règlent la grille, les autres clés tcolorbox (`colback`, `colframe`, `boxrule`, `arc`…) s'appliquent à toutes les cases. Les cases ont l'aspect d'une `tcolorbox` bfcours (fond gris clair, cadre noir).

Le corps est UN SEUL bloc `[…]` : une case par `-` (ou `#tcbitem(…)[…]`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `tcb` | `none` | str, none | clés en syntaxe LaTeX (`"raster columns=3, raster equal height"`). |  |
| `every-box` | `none` | str, dictionary, none | clés appliquées à chaque case (`raster every box`). |  |

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `raster-columns` | `2` | int |  | Nombre de colonnes. Alias : `columns`. |
| `raster-width` | `100%` | length \| ratio |  | Largeur de la grille. |
| `raster-column-skip` | `2mm` | length |  | Espace entre colonnes. |
| `raster-row-skip` | `2mm` | length |  | Espace entre rangées. |
| `raster-before-skip` | `2mm` | length |  | Espace avant. |
| `raster-after-skip` | `2mm` | length |  | Espace après. |
| `raster-left-skip` | `0pt` | length |  | Retrait à gauche. |
| `raster-equal-height` | `"none"` | str |  | `"rows"` pour une hauteur commune. |
| `raster-valign` | `"center"` | str |  | Place d'une case dans sa cellule. |
| `cases` | (positionnel) | content |  | Les cases. |

Exemple :

```typ
#tcbraster(raster-columns: 2, raster-equal-height: "rows")[
  - Case A
  - Case B, plus longue
]
#tcbraster(columns: 3)[
  #tcbitem(title: [A])[un]
  #tcbitem(title: [B])[deux]
  #tcbitem(title: [C])[trois]
]
```

## enumerate

```typ
enumerate(..args)
```

Liste numérotée de bfcours (`\begin{enumerate}[options]`) : numéros dans une pastille de la couleur des items, « 1. », « a. », « i. » selon le niveau. Le corps est un seul bloc `[…]` où chaque item s'écrit `+`. Les options enumitem sont des clés. Un numéro écrit sur le premier item (`3. Texte`) vaut `start` si cette clé est absente ; les suivants sont ignorés.

LaTeX : `\enumerate`

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `label` | `auto` | str \| function \| array \| auto |  | Motif (`"a)"`), fonction `n => contenu` ou tableau par niveau ; `auto` : pastille. |
| `start` | `auto` | int \| auto |  | Numéro du premier item. |
| `couleur-etiquette` | `itemBaseColor` | color \| str \| auto |  | Couleur des pastilles : couleur nommée `item-base-color`. |
| `motifs` | `auto` | array \| auto |  | Motifs des pastilles par niveau (`("1", "a", "i", "A")`). |
| `leftmargin` | `auto` | length \| auto |  | Comme `itemize` (avec `labelsep`, `itemsep`, `topsep`, `nosep`, `leftmargini`…). |
| `items` | (positionnel) | content |  | Les items. |

Exemple :

```typ
#enumerate[
  + Premier
  + Deuxième #enumerate[
      + a
      + b
    ]
]
#enumerate(start: 3, couleur-etiquette: "red!70!black")[
  + Troisième
  + Quatrième
]
```

## itemize

```typ
itemize(..args)
```

Liste à puces de bfcours (`\begin{itemize}[options]`, puces `•` à tous les niveaux) : le corps est un seul bloc `[…]` où chaque item s'écrit `-`. Les options enumitem sont des clés. La syntaxe `- item` de Typst donne la même mise en page dans un document bfcours ; cette fonction sert quand on veut des options propres à une liste.

LaTeX : `\itemize`

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `leftmargin` | `auto` | length \| auto |  | Retrait des items (`auto` : valeur du niveau). |
| `labelsep` | `auto` | length \| auto |  | Espace puce / texte (5,475 pt). |
| `itemsep` | `auto` | length \| auto |  | Espace entre items. |
| `topsep` | `auto` | length \| auto |  | Espace avant la liste. |
| `nosep` | `false` | bool |  | Aucun espace vertical. |
| `label` | `auto` | content \| array \| auto |  | La puce ; un tableau donne une puce par niveau. |
| `leftmargini` | `auto` | length \| auto |  | Retrait au niveau 1 (idem `leftmarginii` à `leftmarginvi`). |
| `couleur-puce` | `auto` | color \| str \| auto |  | Couleur des puces. |
| `items` | (positionnel) | content |  | Les items. |

Exemple :

```typ
#itemize[
  - Premier item
  - Deuxième item #itemize[
      - Imbriqué
      - Autre
    ]
]
#itemize(label: [--], itemsep: 4pt)[
  - Tiret
  - Autre tiret
]
```

## tcbenumerate

```typ
tcbenumerate(..args)
```

Énumération à pastilles, qui peut se répartir en colonnes : la liste des questions d'un exercice, en une colonne ou en plusieurs quand les questions sont courtes. Le corps est UN SEUL bloc `[…]` où chaque question s'écrit `+` (ou `#tcbitem(…)[…]` quand elle a des options) ; elle est numérotée par une pastille. Une question peut contenir un autre `tcbenumerate`, qui prend alors le niveau suivant (1., 2. puis a., b. puis i., ii.). Du texte écrit après une question lui est rattaché ; du texte avant la première question est une erreur.

Les trois arguments optionnels de `\begin{tcbenumerate}[colonnes][début][format]` deviennent des clés : `raster-columns` (alias `columns`), `depart`, `format`. Les clés de cadre sont celles de tcolorbox : avec `colframe` ou `colback`, chaque question devient une boîte, toutes de même hauteur dans une rangée.

Un numéro écrit à la main sur la première question (`5. Texte`) vaut `depart` si cette clé est absente ; les numéros des questions suivantes sont ignorés (la pastille compte seule).

La syntaxe environnement donne le même résultat : `#begin(tcbenumerate, columns: 2)` … `#end(tcbenumerate)`.

LaTeX : `\tcbenumerate`

Clés documentées dans le guide (`farfadet-enum/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `raster-columns` | `1` | int |  | Nombre de colonnes. Alias : `columns`. |
| `depart` | `1` | int |  | Numéro de la première question. |
| `title` | `none` | content \| str \| none |  | Titre par défaut des questions qui n'ont pas le leur. |
| `format` | `"auto"` | str |  | `"auto"` ou `"num"`, `"arabic"`, `"alph"`, `"Alph"`, `"roman"`, `"Roman"` ; les motifs Typst `"1"`, `"a"`, `"A"`, `"i"`, `"I"` sont aussi permis. |
| `raster-column-skip` | `auto` | length \| auto |  | Espace entre colonnes (`auto` : un demi-quad). |
| `raster-row-skip` | `auto` | length \| auto |  | Espace entre questions (`auto` : 5 pt). |
| `colframe` | `none` | color \| str \| none |  | Cadre de chaque question. |
| `boxrule` | `0.4pt` | length |  | Épaisseur du cadre. |
| `colback` | `none` | color \| str \| none |  | Fond de chaque question. |
| `arc` | `3pt` | length |  | Rayon des coins. |
| `boxsep` | `3pt` | length |  | Marge intérieure des boîtes. |
| `couleur-badge` | `itemBaseColor` | color \| str \| auto |  | Couleur des pastilles : par défaut la couleur nommée `item-base-color` (`couleur-item`, `setbfcolors`). |
| `ecart-badge` | `auto` | length \| auto |  | Espace pastille / texte. |
| `rayon-badge` | `auto` | length \| auto |  | Rayon des coins des pastilles. |
| `format-auto` | `auto` | array \| auto |  | Motifs du format `auto` aux niveaux 1, 2, 3. |
| `bfdEnumIndentI` | `auto` | length \| auto |  | Retrait au niveau 1 (0 em). |
| `bfdEnumIndentII` | `auto` | length \| auto |  | Retrait au niveau 2 (1,5 em). |
| `bfdEnumIndentIII` | `auto` | length \| auto |  | Retrait au niveau 3 (3 em). |
| `raster-equal-height` | `"rows"` | str |  | `"rows"` : boîtes d'une rangée à la même hauteur ; `"none"` : hauteur naturelle. |
| `halign` | `"left"` | str |  | Alignement du texte des questions : `"left"`, `"justify"`, `"center"`, `"right"`. |
| `questions` | (positionnel) | content |  | Le corps : une question par `+`, ou un `#tcbitem(…)[…]`. |

Exemple :

```typ
#tcbenumerate(columns: 2)[
  + $x^2 = 4$
  + $x^2 = -1$
  + $x^2 = 0$
  + $x^2 = 9$
]
#tcbenumerate(format: "alph", depart: 3)[
  + Première question
  + Seconde question
]
```

## bfd-enum-label

```typ
bfd-enum-label(niveau: auto, format: auto)
```

Étiquette de la question courante (`\bfdEnumLabel`), au format du niveau, sans le point : « b » pour la deuxième sous-question. La clé `niveau` choisit le niveau ; la clé `format` impose un motif (`"1"`, `"a"`, `"i"`, ou `"alph"`, `"roman"`…) : `bfd-enum-label(niveau: 2, format: "a")` est le `\bfdEnumLabelII` de LaTeX, qui garde son format quel que soit celui de la liste.

LaTeX : `\bfdEnumLabel`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `niveau` | `auto` | int, auto | niveau de la liste ; `auto` : le niveau courant. |  |
| `format` | `auto` | str, auto | motif de numérotation ; `auto` : celui de la liste. |  |

Exemple :

```typ
#tcbenumerate(format: "Alph")[Voir la question #bfd-enum-label().]
```

## bfd-enum-level

```typ
bfd-enum-level()
```

Profondeur d'imbrication courante des `tcbenumerate` (`\bfdEnumLevel`) : 1, 2, 3… (0 hors liste).

LaTeX : `\bfdEnumLevel`

Exemple :

```typ
#tcbenumerate[Niveau #bfd-enum-level() #tcbenumerate[Niveau #bfd-enum-level()]]
```

## bfd-enum-num

```typ
bfd-enum-num(niveau: auto)
```

Numéro de la question courante d'un `tcbenumerate` (`\bfdEnumNum`), à placer dans le texte d'une question : « (réponse à la question #bfd-enum-num()) ». La clé `niveau` donne le numéro d'un niveau précis (`niveau: 1`, `2`, `3` : les `\bfdEnumNumI`, `II`, `III` de LaTeX) ; 0 hors liste.

LaTeX : `\bfdEnumNum`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `niveau` | `auto` | int, auto | niveau de la liste (1, 2, 3…) ; `auto` : le niveau courant. |  |

Exemple :

```typ
#tcbenumerate[Question #bfd-enum-num() #tcbenumerate[Sous-question #bfd-enum-num(niveau: 1).#bfd-enum-num(niveau: 2)]]
```
