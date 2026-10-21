# farfadet-qcm

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": qcm` puis `#import qcm: *`.
- Réglage : `setrdmcq` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-qcm.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-qcm`).

## Sommaire

- `mcq` — Questionnaire à choix multiples (`\begin{Mcq}[…] … \end{Mcq}`) : contient des `mcq-quest`. Version professeur : les bonnes réponses (`br`) …
- `mcq-quest` — Une question et ses réponses (`\McqQuest[…]{question}{rép1, rép2, …}`). Le premier contenu est la question, les suivants sont les réponses …
- `setrdmcq` — Setter unique du paquet (`\setrdmcq{…}`, `\setrdmcqcb{…}`, `\setrdmcqrb{…}` de rdmcq, plus le réglage de `vrai-faux`). `pour:` choisit ce q…
- `affirmation` — Une affirmation d'un exercice « vrai ou faux ». Le booléen `vrai` donne la bonne réponse.
- `vrai-faux` — Exercice « vrai ou faux » (ajout) : un tableau où chaque affirmation se coche dans la colonne « Vrai » ou « Faux ». La version professeur c…

## mcq

```typ
mcq(..args)
```

Questionnaire à choix multiples (`\begin{Mcq}[…] … \end{Mcq}`) : contient des `mcq-quest`. Version professeur : les bonnes réponses (`br`) sont mises en valeur selon le format. La teinte des bonnes réponses du format `"BFCours"` est une couleur nommée de bfcours (`prop`) : `setbfcolors` la change.

LaTeX : `\Mcq`

Clés documentées dans le guide (`farfadet-qcm/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `orientation` | `"horizontal"` | str | `horizontal`, `vertical` | Disposition des réponses. |
| `resume` | `false` | bool |  | Poursuit la numérotation du `mcq` précédent. |
| `num-start` | `1` | int |  | Numéro de la première question. |
| `width` | `auto` | length \| auto |  | Largeur totale (`auto` : la ligne). |
| `question-width` | `8.5cm` | length |  | Largeur de la zone des questions. |
| `same-width` | `false` | bool |  | Les réponses passent sous la question, sur toute la largeur. |
| `boxrule` | `0.6pt` | length |  | Épaisseur des cadres. |
| `column-sep` | `0pt` | length |  | Écart entre question et réponses. |
| `row-sep` | `0pt` | length |  | Écart entre deux rangées. |
| `question-answer-sep` | `auto` | length \| auto |  | Écart question/réponses avec `same-width` (`auto` : `row-sep`). |
| `answer-column-sep` | `auto` | length \| auto |  | Écart entre réponses voisines (`auto` : `column-sep`). |
| `answer-row-sep` | `0pt` | length |  | Écart vertical entre réponses. |
| `answer-columns` | `0` | int |  | Colonnes de réponses en orientation verticale (`0` : automatique). |
| `format` | `none` | str |  | Les deux formats partiels (questions, réponses) d'un coup. |
| `question-format, answer-format` | `"default"` | str |  | Format des questions, des réponses. |
| `boxstyle` | `(:)` | dictionary |  | Boîte englobante : `before-skip`, `after-skip`, `colback`, `colframe`, `boxrule`, `boxsep`… |
| `correction` | `auto` | bool \| auto |  | Mode correction (`auto` : version professeur ou élève du document). |
| `colback, colframe, opacityback` | `none` | color \| str \| float |  | Raccourcis : fond, cadre, opacité des zones question et réponses. |
| `question-colback, answer-colback` | `none` | color \| str |  | Fond d'une seule zone ; idem avec `-colframe` et `-opacityback`. |
| `every-question-zone, every-question, every-answer-zone, every-answer` | `(:)` | dictionary |  | Style ajouté à toutes les zones ou boîtes de ce type. |
| `every-odd-…, every-even-…` | `(:)` | dictionary |  | Mêmes styles, rangées impaires ou paires ; `every-odd-row` et `every-even-row` règlent les trois d'un coup. |
| `answer` | `(:)` | dictionary |  | Style par numéro de réponse : `("3": (colback: gray))`. |
| `counter-format` | `pastille noire` | function |  | Présentation du numéro de question. |
| `corps` | (positionnel) | content |  | Les `mcq-quest`. |

Exemple :

```typ
#mcq(question-width: 6cm)[
  #mcq-quest(br: 2)[Combien font $2 + 2$ ?][3][4][5]
]
```

## mcq-quest

```typ
mcq-quest(..args)
```

Une question et ses réponses (`\McqQuest[…]{question}{rép1, rép2, …}`). Le premier contenu est la question, les suivants sont les réponses (ou un tableau de réponses). Les clés inconnues de rdmcq sont des clés tcb de la zone externe de la question.

LaTeX : `\McqQuest`

Clés documentées dans le guide (`farfadet-qcm/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `br` | `0` | int \| array |  | Numéro(s) des bonnes réponses, à partir de 1. |
| `answer-zone` | `(:)` | dictionary |  | Style local de la zone des réponses. |
| `answer` | `(:)` | dictionary |  | Style par numéro de réponse : `("2": (colback: gray))`. |
| `points` | `none` | int \| float \| none |  | Barème de la question, ajouté au total des points (ajout bfcours). |
| `boite` | `auto` | bool \| auto |  | Boîte « n pts » à droite de l'énoncé (`auto` : suit `displayitempoints`) (ajout). |
| `question` | (positionnel) | content |  | La question. |
| `reponses` | (positionnel) | content \| array |  | Les réponses. |

Exemple :

```typ
#mcq(same-width: true)[
  #mcq-quest(br: (1, 3), answer: ("2": (colback: luma(220))))[Quels nombres sont pairs ?][2][3][4]
]
```

## setrdmcq

```typ
setrdmcq(pour: none, reinitialiser: false, definir: none, ..cles)
```

Setter unique du paquet (`\setrdmcq{…}`, `\setrdmcqcb{…}`, `\setrdmcqrb{…}` de rdmcq, plus le réglage de `vrai-faux`). `pour:` choisit ce qu'on règle : `"Mcq"` (défaut : les clés /rdmcq/ de `mcq`), `"rdmcqcb"` (cases à cocher des formats), `"rdmcqrb"` (boutons radio des formats) ou `"vrai-faux"`. Les appels s'ajoutent clé par clé. Un format se choisit par `style: "Boston"` (ou `format: "Boston"`, qui pose les deux formats partiels d'un coup) : formats `"default"`, `"Troyes"`, `"Tokyo"`, `"Boston"`, `"Miami"`, `"Reims"`, `"Millau"`, `"Melun"`, `"Paris"` et `"BFCours"`.

LaTeX : `\setrdmcq`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, none | `"Mcq"`, `"rdmcqcb"`, `"rdmcqrb"` ou `"vrai-faux"` ; `none` : `"Mcq"` (et, pour `reinitialiser`, les quatre). Défaut `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : repart des défauts de rdmcq avant d'appliquer les clés (styles nommés gardés) ; `"tout"` : ramène aussi les styles nommés aux formats prédéfinis. Défaut `false`. |  |
| `definir` | `none` | str, none | nom d'un style à définir avec les clés données (`pour: "Mcq"` ou `"vrai-faux"`) ; on l'appelle ensuite par `style: "nom"` (dans `mcq`, `setrdmcq`, `vrai-faux`). Défaut `none`. |  |

Clés documentées dans le guide (`farfadet-qcm/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `clés` | `—` | any |  | Pour `mcq` : toutes les clés de `mcq` sauf `resume` ; `style` y choisit un format. Pour les cases : `size`, `color`, `raise`, `check-symbol`, `check-color`, `checked`, `background-color`. Pour `vrai-faux` : voir `vrai-f… |

Exemple :

```typ
#setrdmcq(orientation: "vertical", question-width: 6cm)                // réglage global de Mcq
#setrdmcq(pour: "rdmcqcb", color: blue)                                // cases à cocher des formats
#setrdmcq(pour: "vrai-faux", cases: "rond")                            // vrai-faux
#setrdmcq(definir: "serre", row-sep: 2pt, column-sep: 2pt, style: "Reims") // style nommé
#setrdmcq(reinitialiser: true)                                         // retour aux défauts
```

## affirmation

```typ
affirmation(enonce, vrai: true, justification: none, points: none, boite: auto)
```

Une affirmation d'un exercice « vrai ou faux ». Le booléen `vrai` donne la bonne réponse.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `enonce` | (positionnel) | content | l'affirmation. |  |
| `vrai` | `true` | bool | `true` si l'affirmation est vraie, `false` si elle est fausse. Défaut `true`. |  |
| `justification` | `none` | content, none | justification attendue, affichée en version professeur seulement. Défaut `none`. |  |
| `points` | `none` | int, float, none | barème de l'affirmation. Défaut `none`. |  |
| `boite` | `auto` | bool, auto | boîte « n pts » à droite de l'affirmation. Défaut `auto`. |  |

Clés documentées dans le guide (`farfadet-qcm/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `corps` | (positionnel) | content |  | L'affirmation. |

Exemple :

```typ
#vrai-faux(affirmation(vrai: true)[Un carré est un rectangle.])
```

## vrai-faux

```typ
vrai-faux(..args)
```

Exercice « vrai ou faux » (ajout) : un tableau où chaque affirmation se coche dans la colonne « Vrai » ou « Faux ». La version professeur coche la bonne colonne ; la version élève laisse les cases vides. Réglage global : `setrdmcq(pour: "vrai-faux", …)`, mêmes clés.

L'ancienne écriture (`vrai-faux(affirmation(…)[…], affirmation(…)[…])`) reste acceptée.

Clés documentées dans le guide (`farfadet-qcm/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `colonnes` | `1` | int |  | Nombre de tableaux côte à côte. |
| `numerotation, num-start` | `"1.", 1` | str \| none, int |  | Numérotation des affirmations. |
| `cases` | `"carre"` | str | `carre`, `rond` | Forme des cases. |
| `libelles` | `([Vrai], [Faux])` | array |  | Intitulés des deux colonnes. |
| `lignes-justification` | `0` | int |  | Lignes pour justifier, dans la version élève. |
| `melanger, graine` | `false, 1` | bool, int |  | Mélange reproductible : même ordre dans les deux versions. |
| `correction` | `auto` | bool \| auto |  | Version professeur. |
| `correction-color` | `monrose` | color \| str |  | Couleur des corrections. |
| `row-sep, column-sep, largeur-colonne` | `0.9em, 1em, 1.7cm` | length |  | Écarts, largeur des colonnes Vrai/Faux. |
| `filet, filet-color` | `0.5pt, rem` | length \| stroke \| none, color |  | Filets du tableau : épaisseur et couleur (ou trait complet). |
| `fond-entete` | `rem!15` | color \| str \| none |  | Fond de la ligne d'en-tête. |
| `marge-cellule, taille-justification` | `(x: 0.5em, y: 0.45em), 0.9em` | length \| dictionary |  | Marges des cellules, taille des justifications. |
| `taille-case, filet-case, couleur-case, epaisseur-coche` | `0.85em, 0.7pt, black, 1.2pt` | length \| color |  | Dessin des cases. |
| `affirmations` | (positionnel) | dictionary |  | Créées par `affirmation`. |

Exemple :

```typ
#vrai-faux[
  #affirmation(vrai: true)[Un carré est un rectangle.]
  #affirmation(vrai: false, justification: [Le nombre $2$ est pair et premier.])[Aucun nombre premier n'est pair.]
]
```
