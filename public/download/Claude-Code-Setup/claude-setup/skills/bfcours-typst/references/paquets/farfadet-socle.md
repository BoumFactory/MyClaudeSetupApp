# farfadet-socle

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": socle` puis `#import socle: *`.
- Réglage : `setbfcolors`, `setbfsocle` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-socle.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-socle`).

## Sommaire

- `ifcorrection` — `\ifcorrection … \else … \fi` : la conditionnelle professeur / élève, en trois formes.
- `begin` — Ouvre un environnement : `#begin(f, ..options)` ; ferme-le par `#end(f)`. `f` est la fonction elle-même (`tcbenumerate`, `exo`…), pas son n…
- `end` — Ferme l'environnement ouvert par `#begin(f, …)`. Une étiquette peut suivre : `#end(f) <ex1>`.
- `environnements` — Passe de regroupement des environnements `begin … end`. À utiliser en tête de document (`#show: environnements`, déjà fait par `#show: mode…
- `alias` — Crée un ALIAS d'une commande : un nom court, des clés renommées et des valeurs par défaut. On le nomme par `#let`, puis on l'emploie comme …
- `oe` — Ligatures du français œ et Œ (`\oe` et `\OE` de LaTeX). Au milieu d'un mot, terminer l'appel par `;` (ou l'écrire entre parenthèses), sinon…
- `oe-maj` — 
- `euro` — Symbole euro € (`\euro`, `\texteuro` de LaTeX). Dans une formule, il s'écrit sans `#` : `$12 euro$`.
- `definir-style` — Définit (ou remplace) un STYLE NOMMÉ commun à tous les paquets farfadet-* (ajout ; équivalent de `\tcbset{mon style/.style={…}}`). On l'app…
- `setbfcolors` — Change la valeur de base des COULEURS NOMMÉES de bfcours (`\colorlet{thm}{…}` de bfcours-colors) et des macros d'état (`\renewcommand{\curr…
- `setbfsocle` — Réglage du socle (convention commune des setters `setbf…`). Les appels s'ajoutent clé par clé ; une clé inconnue ou une valeur invalide arr…
- `couleur-texte-accent` — `\CouleurTexteAccent{couleur}` : couleur d'accent du texte (`\currentAccentColor`, lue par `acc`, `voc`…) ET couleur des boîtes `boite`/`bf…
- `couleurs-secondary-tabular` — `\CouleursSecondaryTabular{cadre}{fond titre}{texte titre}{fond}{texte}` : couleurs des tableaux SECONDAIRES (`tcbtabx`) pour la suite du d…
- `couleurs-tabular` — `\CouleursTabular{cadre}{fond titre}{texte titre}{fond}{texte}` : couleurs des tableaux PRIMAIRES (`tcbtab`, `TableauBox`, `CompTab`) pour …
- `reset-couleur-texte-accent` — `\ResetCouleurTexteAccent` : accent noir et `\boitecouleur` = `gray!75!black`.
- `reset-couleurs-secondary-tabular` — `\ResetCouleursSecondaryTabular` : couleurs des tableaux secondaires par défaut (`red!50!black`, `Salmon!30!white`, `black`, `yellow!10!whi…
- `reset-couleurs-tabular` — `\ResetCouleursTabular` : couleurs des tableaux primaires par défaut (`blue!50!black`, `blue!50!black`, `white`, `white`, `red!50!black`) e…
- `colorlet` — `\colorlet{nom}{expression}` (xcolor) : nomme une couleur obtenue par une expression xcolor, évaluée immédiatement. Redéfinir un nom de bfc…
- `couleur-item` — `\couleurItem{couleur}` : couleur des pastilles numérotées (`\itemBaseColor`) de `tcbenumerate` et des énumérations, pour la suite du docum…
- `definecolor` — `\definecolor{nom}{modèle}{valeur}` (xcolor) : définit une couleur nommée, utilisable ensuite dans toute expression xcolor (`"macouleur!30!…
- `reset-item-base-color` — `\resetItemBaseColor` : pastilles en `gray!80!black`.
- `textcolor` — `\textcolor{couleur}{texte}` (xcolor) : écrit le texte dans une couleur nommée ou une expression xcolor.
- `xcolor` — Expression xcolor → couleur Typst (ajout : en LaTeX, l'expression s'écrit directement dans les options). Erreur explicite sur un nom inconn…
- `current-accent-color` — `\currentAccentColor` : couleur d'accent courante (noir hors environnement didactique). Dans un `context`.
- `current-table-col-title-color` — `\currentTableColTitleColor` : texte du titre des tableaux primaires (`white`). Dans un `context`.
- `current-table-colback-title-color` — `\currentTableColbackTitleColor` : fond du titre des tableaux primaires (`blue!50!black`). Dans un `context`.
- `item-base-color` — `\itemBaseColor` : couleur des pastilles numérotées (`gray!80!black`). Dans un `context`.

## ifcorrection

```typ
ifcorrection(..branches)
```

`\ifcorrection … \else … \fi` : la conditionnelle professeur / élève, en trois formes.

- `ifcorrection[prof][élève]` : deux branches ; - `ifcorrection[prof]` : rien en version élève ; `ifcorrection[][élève]` : rien en version professeur ; - `ifcorrection()` sans argument : renvoie le booléen (vrai en version professeur), dans un `context`.

La version se choisit par la clé `correction` du modèle ou de `setbfsocle` ; `--input correction=true|false` à la compilation l'emporte toujours.

- ..branches (content): zéro, un ou deux contenus (professeur, élève).

LaTeX : `\ifcorrection`

Clés documentées dans le guide (`farfadet-socle/docs/guide-avant-pilote.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..branches` | (positionnel) | content |  | Zéro, un ou deux contenus : `[professeur]`, `[professeur][élève]`, `[][élève]`. |

Exemple :

```typ
#ifcorrection[Corrigé : $x = 3$.][Cadre à compléter.]
#ifcorrection[][Complète la phrase ci-dessous.]
#context if ifcorrection() [Version professeur.] else [Version élève.]
```

## begin

```typ
begin(f, ..args)
```

Ouvre un environnement : `#begin(f, ..options)` ; ferme-le par `#end(f)`. `f` est la fonction elle-même (`tcbenumerate`, `exo`…), pas son nom.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `f` | (positionnel) | function | la fonction de l'environnement. |  |

Clés documentées dans le guide (`farfadet-socle/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `options` | (positionnel) | arguments |  | Les options et les blocs fixes, passés à `f` avant le corps. |

## end

```typ
end(f)
```

Ferme l'environnement ouvert par `#begin(f, …)`. Une étiquette peut suivre : `#end(f) <ex1>`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `f` | (positionnel) | function | la même fonction que celle de `begin`. |  |

## environnements

```typ
environnements(doc)
```

Passe de regroupement des environnements `begin … end`. À utiliser en tête de document (`#show: environnements`, déjà fait par `#show: modele(…)`) ou sur un corps : `environnements(corps)`. Un `begin` sans `end` (ou l'inverse), ou mal imbriqué, arrête la compilation avec un message qui indique où chercher.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `doc` | (positionnel) | content | le contenu à traiter ; une autre valeur (chaîne, nombre, none…) est rendue telle quelle. |  |

## alias

```typ
alias(pour, nom: none, cles: (:), ..defauts)
```

Crée un ALIAS d'une commande : un nom court, des clés renommées et des valeurs par défaut. On le nomme par `#let`, puis on l'emploie comme la commande d'origine (syntaxe commande ou begin/end).

Les clés d'origine restent acceptées à côté des nouveaux noms ; donner les deux à la fois arrête la compilation. Une clé donnée à l'appel l'emporte sur le défaut de l'alias. Les arguments positionnels (titre, corps, nombre de colonnes…) passent tels quels.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | (positionnel) | function | la commande d'origine (`multi-colonnes`, `exo`, `crep`…), la fonction elle-même, pas son nom. |  |
| `nom` | `none` | none, str | nom de l'alias, repris dans les messages d'erreur. Défaut : `none` (« alias »). |  |
| `cles` | `(:)` | dictionary | renommage des clés, `(clé d'origine: "nouveau nom", …)`. Défaut : `(:)`. |  |

Clés documentées dans le guide (`farfadet-socle/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..defauts` | `aucune` | any |  | Valeurs par défaut, en arguments nommés, sous le nouveau nom ou le nom d'origine. |

Exemple :

```typ
#let mc = alias(multi-colonnes, nom: "mc", cles: (columns: "nb"), nb: 3)
#mc[
  - un
  - deux
  - trois
]
#begin(mc, nb: 2)
- quatre
- cinq
#end(mc)
```

## oe

```typ
oe
```

Ligatures du français œ et Œ (`\oe` et `\OE` de LaTeX). Au milieu d'un mot, terminer l'appel par `;` (ou l'écrire entre parenthèses), sinon Typst lit `#oeur` comme un seul nom.

LaTeX : `\oe`, `\OE`

Exemple :

```typ
Le c#oe;ur du n#oe;ud, une #oe-maj;uvre, un b#(oe)uf.
```

## oe-maj

```typ
oe-maj
```

## euro

```typ
euro
```

Symbole euro € (`\euro`, `\texteuro` de LaTeX). Dans une formule, il s'écrit sans `#` : `$12 euro$`.

LaTeX : `\euro`

Exemple :

```typ
Le livre coûte 12~#euro, soit $3 times 4 euro$.
```

## definir-style

```typ
definir-style(nom, ..cles)
```

Définit (ou remplace) un STYLE NOMMÉ commun à tous les paquets farfadet-* (ajout ; équivalent de `\tcbset{mon style/.style={…}}`). On l'appelle ensuite par la clé `style:` de n'importe quelle commande réglable, ou dans un réglage global (`setbfsocle(style: …)`, `setrdcrep(style: …)`…).

Les clés sont contrôlées à l'emploi, contre celles de la commande qui appelle le style. Un style peut en appeler un autre (`style:` à l'intérieur : héritage). Priorité : clé locale > style nommé > réglage du type > réglage global > défaut.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom du style (les espaces sont permises : `"bfd theoreme"`). |  |

Clés documentées dans le guide (`farfadet-socle/docs/guide-avant-pilote.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` |  | any |  | Les clés du style, celles de la commande qui l'appellera ; `style:` à l'intérieur pour hériter d'un autre style. |

Exemple :

```typ
#definir-style("discret", correction-color: "gray", correction-font: (size: "small"))
#definir-style("discret-vert", style: "discret", correction-color: "defi")
#setbfsocle(style: "discret-vert")
#setbfsocle(reinitialiser: true)
Style défini ; à appeler par `style: "discret"` (par exemple `crep(style: "discret")[…]`).
```

## setbfcolors

```typ
setbfcolors(reinitialiser: false, ..couleurs)
```

Change la valeur de base des COULEURS NOMMÉES de bfcours (`\colorlet{thm}{…}` de bfcours-colors) et des macros d'état (`\renewcommand{\currentAccentColor}{…}`), pour la suite du document.

Ces couleurs sont les couleurs par défaut de TOUS les paquets farfadet-* (environnements, tableaux, zones de réponse, exercices, QCM, listes…) : elles sont lues au moment du rendu, donc `setbfcolors(thm: …)` recolore partout ce qui suit. Le setter d'un paquet peut ensuite les remplacer pour lui seul (`setrdcrep(correction-color: red)`).

Comme en LaTeX, `defi` colore à la fois `definition` et `notation`, `nota` `vocabulaire` et `aide`, `act` `activite`, `BaseColor` les bandeaux de section. Les valeurs sont évaluées tout de suite (comme `\colorlet`) : `setbfcolors(defi: "thm")` copie la valeur actuelle de `thm`. `boitecouleur: auto` rend à `boite` la couleur d'accent.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `reinitialiser` | `false` | bool | ramène d'abord toutes les couleurs nommées et toutes les macros d'état à leur valeur d'origine, puis applique les autres clés. Défaut : `false`. |  |

Clés documentées dans le guide (`farfadet-socle/docs/guide-avant-pilote.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..couleurs` |  | color \| str |  | Un argument nommé par couleur nommée (`defi`, `thm`, `prop`, `ex`, `nota`, `rem`, `demo`, `act`, `meth`, `monrose`, les couleurs de thèmes, les couleurs des autres modules) ou par macro d'état (`current-accent-color`, `… |

Exemple :

```typ
#setbfcolors(thm: "teal", currentAccentColor: "red!60!black")
#textcolor("thm")[Théorème], #context text(fill: current-accent-color())[accent].
#setbfcolors(reinitialiser: true)
#textcolor("thm")[Théorème d'origine.]
```

## setbfsocle

```typ
setbfsocle(pour: none, reinitialiser: false, definir: none, correction: auto, ..cles)
```

Réglage du socle (convention commune des setters `setbf…`). Les appels s'ajoutent clé par clé ; une clé inconnue ou une valeur invalide arrête la compilation avec la liste des possibilités.

Clés : - `correction` : version du document (`true` professeur, `false` élève ; équivaut à `\setrdcrep{correction=…}`), sans effet si `--input correction=…` est donné ; - `correction-color`, `correction-font`, `style` : couleur et police des corrections, lues par les zones de réponse de farfadet-crep et par les objets rd (`\setrdcrep{correction color=…, correction font=…}`) ; `setrdcrep(correction-color: …)` les remplace pour les zones de réponse et recopie sa valeur ici.

Les couleurs (macros d'état `current-accent-color`…, couleurs nommées `thm`…) se règlent par `setbfcolors`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none | sans objet pour le socle, qui n'a pas de types d'objets (gardé pour la signature commune des setters). Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` repart des défauts avant d'appliquer les clés (styles gardés) ; `"tout"` ramène aussi les styles du socle à ceux d'origine. Défaut : `false`. |  |
| `definir` | `none` | none, str | définit le style nommé du socle de ce nom avec les clés données, au lieu de régler. Défaut : `none`. |  |
| `correction` | `auto` | auto, bool | version du document. Défaut : `auto` (inchangée). |  |

Clés documentées dans le guide (`farfadet-socle/docs/guide-avant-pilote.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `correction-color` | `monrose` | color \| str |  | Couleur des corrections, lue par les zones de réponse de farfadet-crep. Défaut : la couleur nommée `monrose` (suit `setbfcolors`). |
| `correction-font` | `(size: "large", weight: "bold")` | dictionary \| function |  | Police des corrections : clés `size`, `weight`, `style`, `font`, ou fonction `c => …`. |
| `style` | `aucun` | str \| array |  | Style(s) nommé(s) appliqué(s) au réglage global. |

Exemple :

```typ
#setbfsocle(correction-color: "prop", correction-font: (size: "normalsize", style: "italic"))
#setbfsocle(definir: "discret", correction-color: "gray", correction-font: (size: "small"))
#setbfsocle(style: "discret")
#setbfsocle(reinitialiser: true)
#ifcorrection[Version professeur.][Version élève.]
```

## couleur-texte-accent

```typ
couleur-texte-accent(couleur)
```

`\CouleurTexteAccent{couleur}` : couleur d'accent du texte (`\currentAccentColor`, lue par `acc`, `voc`…) ET couleur des boîtes `boite`/`bfbox` (`\boitecouleur`), pour la suite du document.

LaTeX : `\CouleurTexteAccent`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | couleur Typst ou expression xcolor. |  |

Exemple :

```typ
#couleur-texte-accent("meth")
#context text(fill: current-accent-color())[Mot accentué.]
#reset-couleur-texte-accent()
```

## couleurs-secondary-tabular

```typ
couleurs-secondary-tabular(cadre, fond-titre, texte-titre, fond, texte)
```

`\CouleursSecondaryTabular{cadre}{fond titre}{texte titre}{fond}{texte}` : couleurs des tableaux SECONDAIRES (`tcbtabx`) pour la suite du document.

LaTeX : `\CouleursSecondaryTabular`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `cadre` | (positionnel) | color, str | `\currentSecondaryTableFrameColor`. Défaut : `"red!50!black"`. |  |
| `fond-titre` | (positionnel) | color, str | `\currentSecondaryTableColbackTitleColor`. Défaut : `"Salmon!30!white"`. |  |
| `texte-titre` | (positionnel) | color, str | `\currentSecondaryTableColTitleColor`. Défaut : `"black"`. |  |
| `fond` | (positionnel) | color, str | `\currentSecondaryTableColbackColor`. Défaut : `"yellow!10!white"`. |  |
| `texte` | (positionnel) | color, str | `\currentSecondaryTableColupperColor`. Défaut : `"red!50!black"`. |  |

Exemple :

```typ
#couleurs-secondary-tabular("prop", "prop!30!white", "black", "prop!5", "prop")
#context box(fill: xcolor("currentSecondaryTableColbackTitleColor"), inset: 4pt,
  stroke: xcolor("currentSecondaryTableFrameColor"))[Titre secondaire]
#reset-couleurs-secondary-tabular()
```

## couleurs-tabular

```typ
couleurs-tabular(cadre, fond-titre, texte-titre, fond, texte)
```

`\CouleursTabular{cadre}{fond titre}{texte titre}{fond}{texte}` : couleurs des tableaux PRIMAIRES (`tcbtab`, `TableauBox`, `CompTab`) pour la suite du document ; les filets (`\arrayrulecolor`) prennent la couleur du cadre. Les environnements didactiques les règlent eux-mêmes à leur ouverture.

LaTeX : `\CouleursTabular`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `cadre` | (positionnel) | color, str | `\currentTableFrameColor` et filets. Défaut LaTeX : `"blue!50!black"`. |  |
| `fond-titre` | (positionnel) | color, str | `\currentTableColbackTitleColor`. Défaut : `"blue!50!black"`. |  |
| `texte-titre` | (positionnel) | color, str | `\currentTableColTitleColor`. Défaut : `"white"`. |  |
| `fond` | (positionnel) | color, str | `\currentTableColbackColor`. Défaut : `"white"`. |  |
| `texte` | (positionnel) | color, str | `\currentTableColupperColor`. Défaut : `"red!50!black"`. |  |

Exemple :

```typ
#couleurs-tabular("defi", "defi", "white", "defi!5", "black")
#context {
  let (titre, fond) = (current-table-colback-title-color(), xcolor("currentTableColbackColor"))
  table(columns: 2, stroke: xcolor("currentTableFrameColor"), fill: (x, y) => if y == 0 { titre } else { fond },
    text(fill: current-table-col-title-color())[$x$], text(fill: current-table-col-title-color())[$f(x)$],
    [1], [3])
}
#reset-couleurs-tabular()
```

## reset-couleur-texte-accent

```typ
reset-couleur-texte-accent()
```

`\ResetCouleurTexteAccent` : accent noir et `\boitecouleur` = `gray!75!black`.

LaTeX : `\ResetCouleurTexteAccent`

Exemple :

```typ
#reset-couleur-texte-accent()
#textcolor("boitecouleur")[Couleur des boîtes par défaut.]
```

## reset-couleurs-secondary-tabular

```typ
reset-couleurs-secondary-tabular()
```

`\ResetCouleursSecondaryTabular` : couleurs des tableaux secondaires par défaut (`red!50!black`, `Salmon!30!white`, `black`, `yellow!10!white`, `red!50!black`).

LaTeX : `\ResetCouleursSecondaryTabular`

Exemple :

```typ
#reset-couleurs-secondary-tabular()
#context box(fill: xcolor("currentSecondaryTableColbackColor"), inset: 4pt)[Fond secondaire par défaut.]
```

## reset-couleurs-tabular

```typ
reset-couleurs-tabular()
```

`\ResetCouleursTabular` : couleurs des tableaux primaires par défaut (`blue!50!black`, `blue!50!black`, `white`, `white`, `red!50!black`) et filets noirs (`couleur_theme`).

LaTeX : `\ResetCouleursTabular`

Exemple :

```typ
#couleurs-tabular("thm", "thm", "white", "white", "thm")
#reset-couleurs-tabular()
#textcolor("currentTableFrameColor")[Cadre par défaut.]
```

## colorlet

```typ
colorlet(nom, expression)
```

`\colorlet{nom}{expression}` (xcolor) : nomme une couleur obtenue par une expression xcolor, évaluée immédiatement. Redéfinir un nom de bfcours (`"thm"`, `"defi"`…) le change dans toutes les expressions xcolor qui suivent, donc aussi dans les défauts de tous les paquets (même effet que `setbfcolors`).

LaTeX : `\colorlet`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom de la couleur. |  |
| `expression` | (positionnel) | color, str | couleur Typst ou expression xcolor. |  |

Exemple :

```typ
#colorlet("fondclair", "prop!10!white")
#box(fill: rgb("#ffffff"), inset: 3pt)[#textcolor("fondclair!50!black")[Bleu assombri.]]
```

## couleur-item

```typ
couleur-item(couleur)
```

`\couleurItem{couleur}` : couleur des pastilles numérotées (`\itemBaseColor`) de `tcbenumerate` et des énumérations, pour la suite du document.

LaTeX : `\couleurItem`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | couleur Typst ou expression xcolor. |  |

Exemple :

```typ
#couleur-item("geo")
#context circle(radius: 6pt, fill: item-base-color())
#reset-item-base-color()
```

## definecolor

```typ
definecolor(nom, modele, valeur)
```

`\definecolor{nom}{modèle}{valeur}` (xcolor) : définit une couleur nommée, utilisable ensuite dans toute expression xcolor (`"macouleur!30!white"`) de tous les paquets farfadet-*.

Modèles : `"RGB"` (0-255), `"rgb"` (0-1), `"HTML"` (`"FF1493"`), `"cmyk"`, `"cmy"`, `"gray"` (0-1), `"Gray"` (0-15), `"hsb"` (0-1), `"HSB"` (0-240), `"Hsb"` (teinte en degrés). La valeur s'écrit comme en LaTeX (`"56,128,77"`) ou en tableau (`(56, 128, 77)`).

LaTeX : `\definecolor`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom de la couleur (sans espace ni `!`). |  |
| `modele` | (positionnel) | str | modèle de couleur xcolor. |  |
| `valeur` | (positionnel) | str, array | composantes. |  |

Exemple :

```typ
#definecolor("vertlycee", "RGB", "34,139,34")
#definecolor("orangevif", "HTML", "FF6600")
#textcolor("vertlycee")[Vert lycée] et #textcolor("orangevif!60!black")[orange assombri].
```

## reset-item-base-color

```typ
reset-item-base-color()
```

`\resetItemBaseColor` : pastilles en `gray!80!black`.

LaTeX : `\resetItemBaseColor`

Exemple :

```typ
#reset-item-base-color()
#context circle(radius: 6pt, fill: item-base-color())
```

## textcolor

```typ
textcolor(couleur, corps)
```

`\textcolor{couleur}{texte}` (xcolor) : écrit le texte dans une couleur nommée ou une expression xcolor.

LaTeX : `\textcolor`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | couleur Typst ou expression xcolor (couleurs de bfcours, xcolor, svgnames, definecolor, macros d'état). |  |
| `corps` | (positionnel) | content | texte. |  |

Exemple :

```typ
#textcolor("thm")[Théorème], #textcolor("defi!80!black")[définition],
#textcolor("currentAccentColor")[accent courant], #textcolor(blue)[couleur Typst].
```

## xcolor

```typ
xcolor(expression)
```

Expression xcolor → couleur Typst (ajout : en LaTeX, l'expression s'écrit directement dans les options). Erreur explicite sur un nom inconnu. À appeler dans un `context`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `expression` | (positionnel) | color, str | `"thm"`, `"red!50!black"`, `"currentAccentColor!30"`, `"-thm"` (complémentaire)… |  |

Exemple :

```typ
#context rect(width: 2cm, height: 0.5cm, fill: xcolor("thm!20!white"), stroke: xcolor("thm"))
```

## current-accent-color

```typ
current-accent-color()
```

`\currentAccentColor` : couleur d'accent courante (noir hors environnement didactique). Dans un `context`.

LaTeX : `\currentAccentColor`

Exemple :

```typ
#context text(fill: current-accent-color())[Accent courant.]
```

## current-table-col-title-color

```typ
current-table-col-title-color()
```

`\currentTableColTitleColor` : texte du titre des tableaux primaires (`white`). Dans un `context`.

LaTeX : `\currentTableColTitleColor`

Exemple :

```typ
#context box(fill: black, inset: 3pt, text(fill: current-table-col-title-color())[Titre])
```

## current-table-colback-title-color

```typ
current-table-colback-title-color()
```

`\currentTableColbackTitleColor` : fond du titre des tableaux primaires (`blue!50!black`). Dans un `context`.

LaTeX : `\currentTableColbackTitleColor`

Exemple :

```typ
#context box(fill: current-table-colback-title-color(), inset: 3pt, text(fill: white)[Titre])
```

## item-base-color

```typ
item-base-color()
```

`\itemBaseColor` : couleur des pastilles numérotées (`gray!80!black`). Dans un `context`.

LaTeX : `\itemBaseColor`

Exemple :

```typ
#context circle(radius: 6pt, fill: item-base-color())
```
