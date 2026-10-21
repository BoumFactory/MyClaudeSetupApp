# rdsheet

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-sheet` puis `#import rd-sheet: *`.
- Réglage : `setrdsheet` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdsheet.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdsheet`).

## Sommaire

- `rdsheet` — `rdsheet` : compose une capture de feuille de calcul (style LibreOffice Calc ou Excel) : en-têtes de colonnes (A, B, C…) et de lignes (1, 2…
- `setrdsheet` — `\setrdsheet{clés}` : le réglage de `rdsheet`, sous ses quatre formes (mêmes clés que `rdsheet`).
- `rdsheetsetup` — `\rdsheetsetup{clés}` : alias de `setrdsheet`.

## rdsheet

```typ
rdsheet(..options)
```

`rdsheet` : compose une capture de feuille de calcul (style LibreOffice Calc ou Excel) : en-têtes de colonnes (A, B, C…) et de lignes (1, 2, 3…) générés et protégés, sélection active avec cadre et poignée de recopie, barre de formule facultative.

Les lignes de données sont les arguments positionnels : chacune est un tableau de cellules (`("Janvier", "1250", "1420")`) ou une chaîne « a & b & c ». Une cellule est un contenu ou une chaîne ; un nombre est écrit avec ses chiffres exacts en chaîne (`"1.20"`). Aucune cellule d'en-tête n'est à fournir : le nombre de colonnes est le plus grand nombre de cellules d'une ligne.

Les coordonnées sont celles du tableur : `"B2"` désigne la deuxième cellule de la deuxième ligne, avec l'origine réglée par `row-start`, `col-start` ou `range`. Les styles de cellules sont des dictionnaires aux clés de tabularray : `bg` (fond), `fg` (texte), `font`, `halign` (`"l"`, `"c"`, `"r"`), `valign` (`"t"`, `"m"`, `"b"`), `ht`, `wd`, `mode` (`"math"`), `r` et `c` (fusions), `cmd`, `preto`, `appto`. Les clés des options externes (`theme`, `bw`, `contrast`, `row-start`, `col-start`, `range`, `head-width`) et des spécifications se donnent dans le même appel. Les alias LaTeX (`print`, `rowstart`, `head_width`…) sont acceptés.

- ..lignes (array, str): lignes de données.

Clés documentées dans le guide (`rdsheet/docs/fiches-rdsheet.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..lignes` | (positionnel) | array \| str |  | lignes de données. |
| `theme` | `"default"` | auto \| str |  | `"default"` (LibreOffice Calc ; alias `"calc"`, `"libreoffice"`, `"classic"`, `"blue"`) ou `"excel"` (alias `"green"`, `"office"`) ; `"print"` et `"bw"` activent le mode noir et blanc. |
| `bw` | `false` | auto \| bool |  | mode noir et blanc, indépendant du thème (alias `print`, `monochrome`, `blackandwhite`, `gray`, `grey`). |
| `contrast` | `0.5` | auto \| float |  | contraste du mode noir et blanc, de 0 (doux) à 1 (franc). |
| `row-start` | `1` | auto \| int |  | numéro de la première ligne de données visible (alias `rowstart`, `start-row`, `startrow`). |
| `col-start` | `1` | auto \| int \| str |  | première colonne de données visible, lettre ou entier (alias `colstart`, `start-col`, `startcol`). |
| `range` | `none` | auto \| none \| str |  | plage de tableur `"C12:E15"` : règle l'origine et impose des dimensions minimales à la grille ; les cellules manquantes sont créées vides. |
| `head-width` | `auto` | auto \| length |  | largeur de l'en-tête de ligne, `auto` : 2em (2.5em dès la ligne 100, 3.2em dès la ligne 1000) (alias `headwidth`). |
| `width` | `100%` | auto \| length \| ratio \| str |  | largeur totale de la grille. |
| `colspec` | `auto` | auto \| str \| array |  | colonnes de données, chaîne tabularray (`"Q[l,m,wd=2cm] Q[c,m,wd=2cm]"`) ou tableau de largeurs (`(2cm, 1fr)`) ; la colonne des numéros de ligne est ajoutée automatiquement. |
| `select` | `none` | auto \| none \| str |  | cellule ou plage active `"B2"` ou `"B2:C3"` : cadre de sélection, poignée de recopie, en-têtes en surbrillance. |
| `bar` | `false` | auto \| bool |  | barre de formule au-dessus de la grille ; `auto` : affichée seulement si `name` ou `formula` est donné. |
| `name` | `none` | auto \| none \| str \| content |  | texte de la zone de nom ; par défaut, la cellule ou plage sélectionnée. |
| `name-width` | `60pt` | auto \| length |  | largeur de la zone de nom (alias `namewidth`). |
| `formula` | `none` | auto \| none \| str \| content |  | texte du champ de formule ; par défaut, avec une cellule unique sélectionnée, le contenu de cette cellule. |
| `cell` | `none` | auto \| none \| dictionary \| array |  | styles de cellules : `("B2": style, "A1:C1": style)`, ou tableau d'éléments `("B2", style)` et `(lignes, colonnes, style)` avec des sélecteurs comme `("2-3", "B-C", style)`. |
| `row` | `none` | auto \| none \| dictionary \| array |  | styles de lignes : `("1": style, "odd": style, "Z": style)` ; sélecteurs : numéro, plage `"2-3"`, liste `"1, 3"`, `"odd"`, `"even"`, ancres `"Z"` (dernière), `"Y"` (avant-dernière)… |
| `column` | `none` | auto \| none \| dictionary \| array |  | styles de colonnes : `("A": style, "B-C": style)`, par lettre ou numéro. |
| `cells` | `none` | auto \| none \| dictionary |  | style de toutes les cellules de données, sans toucher aux en-têtes. |
| `rows` | `none` | auto \| none \| dictionary |  | style de toutes les lignes de données. |
| `columns` | `none` | auto \| none \| dictionary |  | style de toutes les colonnes de données. |
| `hline` | `none` | auto \| none \| dictionary \| array |  | filets horizontaux : `("2": "1.2pt, red")` trace le filet au sommet de la ligne de données 2 ; `("3": ("B-C", "1pt, dashed, blue"))` le restreint aux colonnes B à C. |
| `vline` | `none` | auto \| none \| dictionary \| array |  | filets verticaux, même syntaxe que `hline` (`("2": ("1-3", filet))` restreint aux lignes). |
| `hlines` | `0.5pt, gris du thème` | auto \| none \| str \| length \| color \| stroke \| dictionary |  | filet de tous les filets horizontaux de la zone de données. |
| `vlines` | `0.5pt, gris du thème` | auto \| none \| str \| length \| color \| stroke \| dictionary |  | filet de tous les filets verticaux de la zone de données. |
| `long` | `false` | auto \| bool |  | autorise la coupure de la grille entre deux pages (options `long` et `tall` de tabularray). |
| `baseline` | `none` | auto \| none \| str \| length \| ratio |  | ligne de base de la feuille dans le texte (option `baseline` de tabularray) : `"t"`, `"c"`, `"b"` ou longueur ; `none` : feuille isolée. |
| `colsep` | `6pt` | auto \| length |  | marge gauche et droite des cellules (ajout ; `colsep` de tabularray). |
| `rowsep` | `2pt` | auto \| length |  | marge haute et basse des cellules (ajout ; `rowsep` de tabularray). |
| `row-height` | `1.4em` | auto \| length |  | hauteur minimale des lignes (ajout ; `rows = {ht=1.4em}` du `.sty`). |
| `grid-width` | `0.5pt` | auto \| length |  | épaisseur des filets de la grille (ajout). |
| `border-width` | `0.8pt` | auto \| length |  | épaisseur des bordures extérieures et du filet d'en-tête (ajout). |
| `select-width` | `1.5pt` | auto \| length |  | épaisseur du cadre de sélection (ajout). |
| `handle-size` | `4.5pt` | auto \| length |  | côté de la poignée de recopie (ajout). |
| `sans-font` | `("Latin Modern Sans", "TeX Gyre Heros", "Liberation Sans", "Arial")` | auto \| str \| array |  | police sans empattement de la feuille (ajout ; `\sffamily`). |
| `colors` | `none` | auto \| none \| dictionary |  | couleurs du thème à remplacer, par nom (ajout) : `(headerbg: …, selectborder: …)`. Noms : `headerbg`, `headerfg`, `grid`, `headerborder`, `border`, `selectborder`, `selecthandle`, `selectheadbg`, `selectheadfg`, `toolba… |
| `style` | `auto` | auto \| str \| array |  | style(s) nommé(s) défini(s) par `setrdsheet(definir: …)`. |

Exemple :

```typ
#rdsheet(
  select: "B2",
  ("Article", "Prix"), ("Bureau", "249"), ("Chaise", "89"),
)
```

## setrdsheet

```typ
setrdsheet(pour: none, reinitialiser: false, definir: none, ..cles)
```

`\setrdsheet{clés}` : le réglage de `rdsheet`, sous ses quatre formes (mêmes clés que `rdsheet`).

- `setrdsheet(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdsheet(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` sur `rdsheet` ou `setrdsheet`. Un style peut en appeler un autre (`style:`). - `setrdsheet(reinitialiser: true)` : oublie les réglages (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

LaTeX : `\setrdsheet`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | sans effet ici (`rdsheet` n'a pas de types) ; gardé pour la signature commune des setters. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdsheet/docs/fiches-rdsheet.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdsheet` (et `style:`). |

Exemple :

```typ
#setrdsheet(theme: "excel", contrast: 0.8)
#rdsheet(select: "B1", ("42", "84"), ("10", "20"))
#setrdsheet(reinitialiser: "tout")
#rdsheet(select: "B1", ("42", "84"), ("10", "20"))
```

## rdsheetsetup

```typ
rdsheetsetup(pour: none, reinitialiser: false, definir: none, ..cles)
```

`\rdsheetsetup{clés}` : alias de `setrdsheet`.

LaTeX : `\rdsheetsetup`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | voir `setrdsheet`. Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | voir `setrdsheet`. Défaut : `false`. |  |
| `definir` | `none` | none, str | voir `setrdsheet`. Défaut : `none`. |  |

Clés documentées dans le guide (`rdsheet/docs/fiches-rdsheet.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdsheet`. |

Exemple :

```typ
#rdsheetsetup(bw: true)
#rdsheet(select: "A1", ("1", "2"))
```
