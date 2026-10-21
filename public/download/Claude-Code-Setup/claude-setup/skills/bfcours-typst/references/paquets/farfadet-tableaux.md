# farfadet-tableaux

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": tableaux` puis `#import tableaux: *`.
- Réglage : `setbftableaux` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-tableaux.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-tableaux`).

## Sommaire

- `tcbtab` — Tableau encadré à la bfcours. Les cellules se donnent à la suite, rangée après rangée, comme dans la `table` de Typst : on garde tout ce qu…
- `hline` — Filet horizontal sur toute la largeur. À glisser entre les cellules de `tcbtab`.
- `cline` — Filet horizontal sous les colonnes `a` à `b` (numérotées à partir de 1).
- `multicolumn` — Une cellule sur `n` colonnes. L'alignement se lit dans la spécification (`l`, `c` ou `r`).
- `multirow` — Une cellule sur `n` rangées. La rangée suivante donne une cellule vide (`[]`) à la place couverte. (Une `table.cell(rowspan: n)` native sui…
- `cellcolor` — Cellule colorée.
- `tableaurecapsequence` — Tableau de bilan de séquence, une colonne large (0,68 de la largeur du texte) et quatre colonnes étroites (MI, MF, MS, TBM). Les rangées se…
- `entete-contenu` — Rangée d'en-tête « Contenu de la séquence » avec les quatre colonnes de maîtrise MI, MF, MS, TBM colorées, suivie d'un filet. Renvoie des c…
- `recap-heures` — Rangée « Nombre d'heures » suivie du total, sur quatre colonnes, puis d'un filet. Renvoie des cellules : à étaler avec `..`.
- `setbftableaux` — Règle les tableaux pour la suite du document. Sans `pour`, le réglage vaut pour tous les tableaux ; avec `pour`, pour un seul type : `"tcbt…

## tcbtab

```typ
tcbtab(colonnes, title: auto, style: auto, entete: auto, entete-colonne: auto, couleurs: auto, colframe: auto, colback: auto, colbacktitle: auto, coltitle: auto, colupper: auto, entete-fond: auto, entete-texte: auto, entete-colonne-fond: auto, rowcolors: auto, arrayrulecolor: auto, arrayrulewidth: auto, arraystretch: auto, tabcolsep: auto, marges: auto, alignement: auto, filets: auto, cadre: auto, boxrule: auto, arc: auto, toptitle: auto, bottomtitle: auto, fonttitle: auto, fontupper: auto, center-title: auto, drop-fuzzy-shadow: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, width: auto, align: auto, ..cellules)
```

Tableau encadré à la bfcours. Les cellules se donnent à la suite, rangée après rangée, comme dans la `table` de Typst : on garde tout ce que Typst sait faire (`table.cell(colspan: 2)[…]`, `table.hline()`, `table.vline()`), et on dispose aussi des aides du paquet (`hline()`, `cline("2-3")`, `multicolumn`, `multirow`, `cellcolor`).

Le premier argument (positionnel) décrit les colonnes de trois façons : la **spécification de colonnes** (`"|c|p{4cm}|c|"` : alignements, filets verticaux `|`, largeurs `p{…}`, colonnes `X`), un **nombre** de colonnes, ou un **tableau de largeurs** Typst `(auto, 1fr, 3cm)`. Avec une spécification de colonnes, les filets la suivent (verticaux aux `|`) et des filets horizontaux séparent toutes les rangées ; `filets: "verticaux"` les supprime, et `hline()` reste utile pour les bordures ou les filets partiels.

Sans réglage, le tableau a l'allure des tableaux bfcours : cadre bleu nuit à coins arrondis avec une ombre légère, filets fins, texte rouge sombre centré. Chaque détail se règle par une clé ; `cadre: false` donne une grille nue, sans cadre ni titre. Toutes les clés valent `auto` (« selon les réglages ») : on les fixe pour tout le document avec `setbftableaux`.

Les variantes sont des clés : tableau centré (`\tcbtabc`) = `align: center` (défaut : `left`, comme `\tcbtab`) ; tableau secondaire de largeur imposée = `couleurs: "secondaire"` avec `width:` ; tableau compact en ligne = `style: "CompTab"` avec `align: none`.

LaTeX : `\tcbtab`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `colonnes` | (positionnel) | str, int, array | spécification de colonnes, nombre de colonnes ou liste de largeurs. |  |
| `title` | `auto` | content, none | titre, dans un bandeau coloré au-dessus du tableau (défaut : aucun). |  |
| `style` | `auto` | str, array | nom (ou noms) de style défini par `setbftableaux(definir: …)`. |  |
| `entete` | `auto` | bool, int | colore la première rangée (les `n` premières si on donne un entier) : fond et texte du titre, texte gras (défaut : `false`). |  |
| `entete-colonne` | `auto` | bool | met la première colonne en valeur : gras, fond teinté (défaut : `false`). |  |
| `couleurs` | `auto` | str | jeu de couleurs courantes : `"primaire"` (`couleurs-tabular`) ou `"secondaire"` (`couleurs-secondary-tabular`, avec leurs réglages : filets de `0.5mm`, `arraystretch: 1.4`, titre agrandi) (défaut : `"primaire"`). |  |
| `colframe` | `auto` | color, str | couleur du cadre (défaut : `currentTableFrameColor`, bleu nuit). |  |
| `colback` | `auto` | color, str | fond du tableau (défaut : `currentTableColbackColor`, blanc ; sans cadre, aucun fond). |  |
| `colbacktitle` | `auto` | color, str | fond du bandeau de titre (défaut : `current-table-colback-title-color`, bleu nuit). |  |
| `coltitle` | `auto` | color, str | couleur du texte du titre (défaut : `current-table-col-title-color`, blanc). |  |
| `colupper` | `auto` | color, str, none | couleur du texte des cellules (défaut : `currentTableColupperColor`, rouge sombre) ; `none` garde la couleur du texte courant. |  |
| `entete-fond` | `auto` | color, str | fond de l'en-tête (défaut : celui du titre). |  |
| `entete-texte` | `auto` | color, str | texte de l'en-tête (défaut : celui du titre). |  |
| `entete-colonne-fond` | `auto` | color, str | fond de la première colonne mise en valeur (défaut : teinte pâle du cadre). |  |
| `rowcolors` | `auto` | bool, color, array | rangées alternées : `true` colore une rangée sur deux en teinte pâle du cadre ; une couleur colore une rangée sur deux ; `(c1, c2)` alterne `c1`, `c2` à partir de la première rangée du corps ; `(n, impaires, paires)` : … |  |
| `arrayrulecolor` | `auto` | color, str | couleur des filets (défaut : celle de `couleurs-tabular`, noire). |  |
| `arrayrulewidth` | `auto` | length | épaisseur des filets (défaut : `0.4pt`). |  |
| `arraystretch` | `auto` | float | interligne des rangées (défaut : `1.5`, valeur de bfcours). |  |
| `tabcolsep` | `auto` | length, auto | espace de part et d'autre du contenu d'une cellule (défaut : `6pt`, celui de `marges`). |  |
| `marges` | `auto` | length, dictionary | marges des cellules `(x: 6pt, y: 5.5pt)`, `y` valant pour `arraystretch: 1.5`. |  |
| `alignement` | `auto` | alignment, array | alignement du contenu ; un tableau en donne un par colonne. Avec une spécification de colonnes, les lettres `l`, `c`, `r` règlent l'horizontal, `alignement` règle le vertical (défaut : `center + horizon`). |  |
| `filets` | `auto` | str | `"tous"` (quadrillage), `"horizontaux"`, `"verticaux"`, `"aucun"` ; `auto` : avec une spécification de colonnes, filets verticaux aux `\|` et filets horizontaux entre toutes les rangées (comme un `\hline` après chaque r… |  |
| `cadre` | `auto` | bool | entoure le tableau du cadre bfcours. Sans cadre, le titre n'est pas affiché (défaut : `true`). |  |
| `boxrule` | `auto` | length | épaisseur du cadre (défaut : `0.5mm`). |  |
| `arc` | `auto` | length | rayon des coins du cadre (défaut : `1mm`). |  |
| `toptitle` | `auto` | length | marge au-dessus du titre (défaut : `0.5mm`). |  |
| `bottomtitle` | `auto` | length | marge au-dessous du titre (défaut : `0.5mm`). |  |
| `fonttitle` | `auto` | dictionary | police du titre : arguments de `text`, la taille pouvant être un nom (`"large"`) (défaut : `(weight: "bold")`). |  |
| `fontupper` | `auto` | dictionary | police du contenu : arguments de `text` (défaut : aucun). |  |
| `center-title` | `auto` | bool | centre le titre ; sinon à gauche (défaut : `true`). |  |
| `drop-fuzzy-shadow` | `auto` | bool | ombre floue sous le cadre (défaut : `true`). |  |
| `left` | `auto` | length | marge intérieure gauche de la boîte, entre le cadre et la grille (défaut : `0mm`, comme `TableauBox`). |  |
| `right` | `auto` | length | marge intérieure droite (défaut : `0mm`). |  |
| `top` | `auto` | length | marge intérieure haute (défaut : `0mm`). |  |
| `bottom` | `auto` | length | marge intérieure basse (défaut : `0mm`). |  |
| `boxsep` | `auto` | length | marge ajoutée des quatre côtés, en plus de `left`, `right`, `top`, `bottom` (défaut : `0mm`). |  |
| `width` | `auto` | length, ratio, str | largeur du tableau ; `auto` : celle du contenu. Avec des colonnes en `fr` ou `X`, donner une largeur. Une chaîne est acceptée : `"0.8\\textwidth"` (défaut : `auto`). |  |
| `align` | `auto` | alignment, none | placement sur la page : `center`, `left`, `right` ; `none` : boîte en ligne, sans saut de ligne (défaut : `left`, comme `\tcbtab` ; `center` = `\tcbtabc`). |  |

Exemple :

```typ
#tcbtab(3, title: [Valeurs], entete: true,
  [$x$], [$1$], [$2$],
  [$f(x)$], [$3$], [$5$],
)
```

## hline

```typ
hline()
```

Filet horizontal sur toute la largeur. À glisser entre les cellules de `tcbtab`.

LaTeX : `\hline`

Exemple :

```typ
#tcbtab("|c|c|", hline(), [a], [b], hline())
```

## cline

```typ
cline(plage)
```

Filet horizontal sous les colonnes `a` à `b` (numérotées à partir de 1).

LaTeX : `\cline`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `plage` | (positionnel) | str | « a-b », par exemple `"2-3"`. |  |

Exemple :

```typ
#tcbtab("|c|c|c|", hline(), [a], [b], [c], cline("2-3"), [d], [e], [f], hline())
```

## multicolumn

```typ
multicolumn(n, spec, corps)
```

Une cellule sur `n` colonnes. L'alignement se lit dans la spécification (`l`, `c` ou `r`).

LaTeX : `\multicolumn`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int | nombre de colonnes couvertes. |  |
| `spec` | (positionnel) | str | spécification de la cellule : `"c"`, `"l"`, `"r"`, avec ou sans `\|`. |  |
| `corps` | (positionnel) | content | contenu de la cellule. |  |

Exemple :

```typ
#tcbtab("|c|c|c|", hline(), multicolumn(3, "|c|")[Titre sur trois colonnes], hline(), [a], [b], [c], hline())
```

## multirow

```typ
multirow(n, corps, width: auto, align: auto)
```

Une cellule sur `n` rangées. La rangée suivante donne une cellule vide (`[]`) à la place couverte. (Une `table.cell(rowspan: n)` native suit au contraire la convention de Typst : pas de cellule de remplacement.)

LaTeX : `\multirow`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int | nombre de rangées couvertes. |  |
| `corps` | (positionnel) | content | contenu de la cellule. |  |
| `width` | `auto` | length, auto | largeur du texte ; `auto` : largeur naturelle (défaut : `auto`). |  |
| `align` | `auto` | alignment, auto | alignement horizontal de la cellule (défaut : celui de la colonne). |  |

Exemple :

```typ
#tcbtab("|c|c|", hline(), multirow(2)[Groupe], [a], cline("2-2"), [], [b], hline())
```

## cellcolor

```typ
cellcolor(couleur, corps)
```

Cellule colorée.

LaTeX : `\cellcolor`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | couleur Typst ou expression xcolor (`"red!30!white"`). |  |
| `corps` | (positionnel) | content | contenu de la cellule. |  |

Exemple :

```typ
#tcbtab(2, cellcolor("red!30!white")[Rouge pâle], [Normal])
```

## tableaurecapsequence

```typ
tableaurecapsequence(..cellules-brutes)
```

Tableau de bilan de séquence, une colonne large (0,68 de la largeur du texte) et quatre colonnes étroites (MI, MF, MS, TBM). Les rangées se donnent comme celles de `tcbtab` (utiliser `hline()`, `entete-contenu()`, `competence`…).

Syntaxe environnement : `#begin(tableaurecapsequence)` puis un contenu par item `-`, puis `#end(tableaurecapsequence)`. Le filet du haut, l'en-tête, les quatre cases vides de chaque rangée et les filets sont ajoutés. Les cellules écrites entre crochets dans `#begin(…)` sont ajoutées après l'en-tête.

LaTeX : `\tableaurecapsequence`

Clés documentées dans le guide (`farfadet-tableaux/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cellules` | (positionnel) | content |  | Les cellules, rangée après rangée (`hline()`, `entete-contenu()`…) ; les clés nommées sont celles de `tcbtab`. |

Exemple :

```typ
#tableaurecapsequence(hline(), ..entete-contenu(), [Calculer], [], [], [], [], hline())
```

## entete-contenu

```typ
entete-contenu()
```

Rangée d'en-tête « Contenu de la séquence » avec les quatre colonnes de maîtrise MI, MF, MS, TBM colorées, suivie d'un filet. Renvoie des cellules : à étaler avec `..`.

Exemple :

```typ
#tableaurecapsequence(hline(), ..entete-contenu(), [Fractions], [], [], [], [], hline())
```

## recap-heures

```typ
recap-heures(heures)
```

Rangée « Nombre d'heures » suivie du total, sur quatre colonnes, puis d'un filet. Renvoie des cellules : à étaler avec `..`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `heures` | (positionnel) | int, content | nombre d'heures de la séquence. |  |

Exemple :

```typ
#tableaurecapsequence(hline(), ..recap-heures(12))
```

## setbftableaux

```typ
setbftableaux(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les tableaux pour la suite du document. Sans `pour`, le réglage vaut pour tous les tableaux ; avec `pour`, pour un seul type : `"tcbtab"` (tableau principal) ou `"secondaire"` (tableau à `couleurs: "secondaire"`).

Priorité : clé locale, puis style nommé, puis réglage du type, puis réglage global, puis défaut. Les couleurs par défaut sont les couleurs nommées de bfcours : `setbfcolors` (ou `couleurs-tabular`) les change pour tout le document ; ce setter les remplace pour les seuls tableaux.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type visé : `"tcbtab"` ou `"secondaire"` ; `none` : tous. |  |
| `reinitialiser` | `false` | bool, str | `true` repart des réglages d'origine avant d'appliquer les clés (les styles nommés restent) ; `"tout"` ramène aussi les styles aux styles prédéfinis `TableauBox` et `CompTab`. |  |
| `definir` | `none` | str, none | nom d'un style à définir (ou à remplacer) avec les clés données ; on l'appelle ensuite par `style: "nom"`. Deux styles existent d'origine : `"TableauBox"` et `"CompTab"` (filets bleu nuit, `arraystretch: 0.2`, tableau c… |  |

Clés documentées dans le guide (`farfadet-tableaux/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | (positionnel) | any |  | Les clés de `tcbtab`, plus `style: "nom"`. |

Exemple :

```typ
#setbftableaux(arraystretch: 1.2, drop-fuzzy-shadow: false)         // global
#setbftableaux(pour: "secondaire", arrayrulewidth: 1pt)             // un type
#setbftableaux(definir: "compact", arraystretch: 0.8, entete: true) // style nommé
#setbftableaux(reinitialiser: true)                                 // retour aux défauts
```
