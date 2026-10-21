# rdtime

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-time` puis `#import rd-time: *`.
- Réglage : `setrdtime` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdtime.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdtime`).

## Sommaire

- `rdtime` — `\rdtime[options]{durée 1}{durée 2}` : pose et effectue une addition (ou une soustraction) de durées en colonnes, avec les retenues et les …
- `setrdtime` — `\setrdtime{clés}` : le réglage de `rdtime`, sous ses quatre formes (mêmes clés que `rdtime`).

## rdtime

```typ
rdtime(operation: auto, add: auto, sub: auto, digit-width: auto, column-sep: auto, hour-label: auto, min-label: auto, sec-label: auto, minus-sign: auto, plus-sign: auto, name: auto, baseline: auto, display-intermediary: auto, visible: auto, mode-correctif: auto, correction: auto, matrix: auto, nodes: auto, sign: auto, rule: auto, special-cell: auto, result: auto, result-h: auto, result-min: auto, result-sec: auto, first-number: auto, first-number-h: auto, first-number-min: auto, first-number-sec: auto, second-number: auto, second-number-h: auto, second-number-min: auto, second-number-sec: auto, intermediary: auto, labels: auto, hours-label: auto, minutes-label: auto, seconds-label: auto, text-height: auto, text-depth: auto, rule-width: auto, matrix-inset: auto, style: auto, duree-1, duree-2)
```

`\rdtime[options]{durée 1}{durée 2}` : pose et effectue une addition (ou une soustraction) de durées en colonnes, avec les retenues et les cellules barrées.

Les durées s'écrivent `"HH h MM min SS s"` : nombres entiers avec ou sans zéros inutiles, les unités dans cet ordre, espaces facultatifs (`"2h37min"`, `"29 min 17 s"`). En soustraction, la première durée doit être la plus grande.

Les STYLES (clés `result`, `sign`, `rule`, `matrix`, `nodes`…) remplacent les styles TikZ : un dictionnaire `(text: red, font: (weight: "bold"), fill: "red!5", draw: blue, line-width: 1pt…)`, une fonction `c => …` ou un tableau de styles.

LaTeX : `\rdtime`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `operation` | `auto` | auto, str | `"add"` (addition) ou `"sub"` (soustraction). Défaut : `"add"`. | operation/add, operation/sub |
| `add` | `auto` | auto, bool | raccourci de `operation: "add"` (style LaTeX `add`). Défaut : `false`. | add (style) |
| `sub` | `auto` | auto, bool | raccourci de `operation: "sub"` (style LaTeX `sub`). Défaut : `false`. | sub (style) |
| `digit-width` | `auto` | auto, length | largeur occupée par chaque chiffre. Défaut : `0.65em` (1.5ex). | digit width |
| `column-sep` | `auto` | auto, length | espace entre les colonnes. Défaut : `0.5em`. | column sep |
| `hour-label` | `auto` | auto, content | libellé des heures. Défaut : `[h]`. | hour label |
| `min-label` | `auto` | auto, content | libellé des minutes. Défaut : `[min]`. | min label |
| `sec-label` | `auto` | auto, content | libellé des secondes. Défaut : `[s]`. | sec label |
| `minus-sign` | `auto` | auto, content | signe de la soustraction. Défaut : `$-$`. | minus sign |
| `plus-sign` | `auto` | auto, content | signe de l'addition. Défaut : `$+$`. | plus sign |
| `name` | `auto` | auto, str, none | label Typst posé sur l'opération (nom de la matrice TikZ). Défaut : `"timematrix"`. | name |
| `baseline` | `auto` | auto, str, int | ligne de base : `"t"`, `"c"`, `"b"`, `"sign"` (second terme), `"result"` ou numéro de ligne (0 ou 1 : premier terme). Défaut : `0`. | baseline |
| `display-intermediary` | `auto` | auto, bool | affiche les calculs intermédiaires. Défaut : `true`. | display intermediary |
| `visible` | `auto` | auto, bool | `false` n'affiche que l'opération (résultats et retenues masqués, place gardée). Défaut : `true`. | visible |
| `mode-correctif` | `auto` | auto, bool | `visible` suit la version du document (professeur : visible). Défaut : `false`. | mode correctif |
| `correction` | `auto` | auto, bool | style LaTeX `correction` : mode correctif, résultat et retenues dans la couleur des corrections. Défaut : `false`. | correction (style) |
| `matrix` | `auto` | auto, dictionary, function, array, none | style du cadre de l'opération (fill, draw, line-width, inset, radius). Défaut : `none`. | matrix |
| `nodes` | `auto` | auto, dictionary, function, array, none | style de toutes les cellules (text-height, text-depth, min-width…). Défaut : `none`. | nodes |
| `sign` | `auto` | auto, dictionary, function, array, none | style de la cellule du signe. Défaut : `none`. | sign |
| `rule` | `auto` | auto, dictionary, function, array, none | style du trait horizontal (draw, line-width, dash). Défaut : `none`. | rule |
| `special-cell` | `auto` | auto, dictionary, function, array, none | style des cellules barrées. Défaut : `(stroke-out: (line-width: 0.8pt, color: "red", shadowed: "black"))`. | special cell |
| `result` | `auto` | auto, dictionary, function, array, none | style de la ligne du résultat. Défaut : `none`. | result |
| `result-h` | `auto` | auto, dictionary, function, array, none | style des heures du résultat. Défaut : `none`. | result H |
| `result-min` | `auto` | auto, dictionary, function, array, none | style des minutes du résultat. Défaut : `none`. | result Min |
| `result-sec` | `auto` | auto, dictionary, function, array, none | style des secondes du résultat. Défaut : `none`. | result Sec |
| `first-number` | `auto` | auto, dictionary, function, array, none | style de la ligne du premier terme. Défaut : `none`. | first number |
| `first-number-h` | `auto` | auto, dictionary, function, array, none | style des heures du premier terme. Défaut : `none`. | first number H |
| `first-number-min` | `auto` | auto, dictionary, function, array, none | style des minutes du premier terme. Défaut : `none`. | first number Min |
| `first-number-sec` | `auto` | auto, dictionary, function, array, none | style des secondes du premier terme. Défaut : `none`. | first number Sec |
| `second-number` | `auto` | auto, dictionary, function, array, none | style de la ligne du second terme. Défaut : `none`. | second number |
| `second-number-h` | `auto` | auto, dictionary, function, array, none | style des heures du second terme. Défaut : `none`. | second number H |
| `second-number-min` | `auto` | auto, dictionary, function, array, none | style des minutes du second terme. Défaut : `none`. | second number Min |
| `second-number-sec` | `auto` | auto, dictionary, function, array, none | style des secondes du second terme. Défaut : `none`. | second number Sec |
| `intermediary` | `auto` | auto, dictionary, function, array, none | style des calculs intermédiaires. Défaut : `none`. | intermediary |
| `labels` | `auto` | auto, dictionary, function, array, none | style des trois libellés d'unités. Défaut : `none`. | labels |
| `hours-label` | `auto` | auto, dictionary, function, array, none | style du libellé des heures. Défaut : `none`. | hours label |
| `minutes-label` | `auto` | auto, dictionary, function, array, none | style du libellé des minutes. Défaut : `none`. | minutes label |
| `seconds-label` | `auto` | auto, dictionary, function, array, none | style du libellé des secondes. Défaut : `none`. | seconds label |
| `text-height` | `auto` | auto, length | hauteur des cellules au-dessus de la ligne de base (ajout ; `text height` du style de matrice). Défaut : `6mm`. |  |
| `text-depth` | `auto` | auto, length | profondeur des cellules (ajout ; `text depth`). Défaut : `2mm`. |  |
| `rule-width` | `auto` | auto, length | épaisseur du trait horizontal (ajout). Défaut : `0.8pt`. |  |
| `matrix-inset` | `auto` | auto, length, dictionary | marge intérieure du cadre (ajout ; `inner sep` de `\matrix`). Défaut : `0.3333em`. |  |
| `style` | `auto` | auto, str, array | style(s) nommé(s) défini(s) par `setrdtime(definir: …)`. Défaut : `auto`. | monstyle (nom d'un style) |
| `duree-1` | (positionnel) | str | première durée (premier terme). |  |
| `duree-2` | (positionnel) | str | seconde durée (second terme). |  |

Exemple :

```typ
#rdtime("2h37min", "3h49min") #h(1cm)
#rdtime(sub: true, "5h27min38s", "2h19min46s")
```

## setrdtime

```typ
setrdtime(pour: none, reinitialiser: false, definir: none, ..cles)
```

`\setrdtime{clés}` : le réglage de `rdtime`, sous ses quatre formes (mêmes clés que `rdtime`).

- `setrdtime(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdtime(definir: "nom", cle: v, …)` : définit le style nommé « nom » (`\setrdtime{nom/.style={…}}`), appelé ensuite par `style: "nom"` sur `rdtime` ou `setrdtime`. Un style peut en appeler un autre (`style:`). - `setrdtime(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

LaTeX : `\setrdtime`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (`rdtime` n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdtime/docs/fiches-rdtime.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdtime` (et `style:`). |

Exemple :

```typ
#setrdtime(matrix: (fill: "blue!8"), result: (text: red))
#rdtime("3min4s", "5min6s")
#setrdtime(definir: "bleu", result: (text: blue))
#rdtime(style: "bleu", "3min4s", "5min6s")
#setrdtime(reinitialiser: "tout")
#rdtime("3min4s", "5min6s")
```
