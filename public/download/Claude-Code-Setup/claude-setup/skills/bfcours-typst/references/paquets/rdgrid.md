# rdgrid

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-grid` puis `#import rd-grid: *`.
- Réglage : `setrdgrid` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdgrid.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdgrid`).

## Sommaire

- `rdgrid` — `rdgrid(xmax, ymax)` : grille de `xmax` × `ymax` polygones, dont la forme se choisit par la clé `type` : triangles équilatéraux (`"equi"`, …
- `setrdgrid` — `setrdgrid(clés)` : le réglage de `rdgrid`, sous ses quatre formes (mêmes clés que `rdgrid`).

## rdgrid

```typ
rdgrid(type: "equi", width: auto, radius: auto, grid: auto, orientation: auto, dot: auto, dot-style: auto, dot-style-app: auto, show-grid: auto, show-num: auto, num-style: auto, only-dot: auto, scope-style: auto, scope-style-app: auto, frame: auto, lines: auto, polygon-style: auto, code-after: auto, line-join: auto, style: auto, xmax, ymax)
```

`rdgrid(xmax, ymax)` : grille de `xmax` × `ymax` polygones, dont la forme se choisit par la clé `type` : triangles équilatéraux (`"equi"`, défaut), hexagones (`"hexa"`), hexagones tournés (`"rhexa"`) ou grille isométrique (`"iso"`).

Chaque polygone porte un nom (`trg-<i>-<j>` pour equi et iso, `hexa-<i>-<j>` pour les hexagones), et ses sommets un point nommé (`trg-1-3-north east`, `hexa-0-2-center`…), à la manière des ancres de TikZ. Pour dessiner par-dessus (polygones copiés depuis le livret GeoGebra), on passe une fonction à `code-after` : elle reçoit `pt(nom)`, `path(chemin-tikz, stroke:, fill:)`, `node(point, contenu)`, `xy(x, y)` (unités TikZ) et le dictionnaire `points`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `type` | `"equi"` | str | `"equi"`, `"hexa"`, `"rhexa"` ou `"iso"`. Défaut : `"equi"`. | argument {type} |
| `width` | `auto` | auto, int, float, length | taille d'un polygone (côté, ou rayon des hexagones), en cm si sans unité. Défaut : `1` (`0.7` pour hexa et rhexa). | width |
| `radius` | `auto` | auto, int, float, length | autre nom de `width`. Défaut : `auto`. | radius |
| `grid` | `auto` | auto, int | disposition : equi et iso : `1` ou `-1` (premier triangle vers le haut / la droite, ou l'inverse) ; rhexa : `1`, `-1`, `2`, `-2` (décalage des lignes impaires) ; hexa : signe = décalage des colonnes impaires. Défaut : `… | grid |
| `orientation` | `auto` | auto, bool | orientation d'un polygone isolé (pics TikZ) ; sans effet sur une grille, où le type la fixe. Défaut : `true`. | orientation |
| `dot` | `auto` | auto, bool | un point à chaque sommet. Défaut : `false`. | dot |
| `dot-style` | `auto` | auto, dictionary | style des points. Défaut : `(shape: "circle", min-width: 1.5pt, fill: "gray")`. | dot style |
| `dot-style-app` | `auto` | auto, none, dictionary | style ajouté à `dot-style`. Défaut : `none`. |  |
| `show-grid` | `auto` | auto, bool | trace les polygones. Défaut : `true`. | show grid |
| `show-num` | `auto` | auto, bool | numéro `i-j` au centre de chaque polygone. Défaut : `false`. | show num |
| `num-style` | `auto` | auto, dictionary | style des numéros. Défaut : sans empattement, gras, `footnotesize`. | num style |
| `only-dot` | `auto` | auto, bool | papier pointé (`show-grid: false, dot: true`). Défaut : `false`. | only dot |
| `scope-style` | `auto` | auto, dictionary | style des traits de la grille. Défaut : `(draw: "gray", line-width: 0.5pt)`. | scope style |
| `scope-style-app` | `auto` | auto, none, dictionary | style ajouté à `scope-style`. Défaut : `none`. |  |
| `frame` | `auto` | auto, bool | cadre autour de la grille (iso seulement). Défaut : `true`. | frame |
| `lines` | `auto` | auto, bool | lignes verticales (iso seulement). Défaut : `true`. | lines |
| `polygon-style` | `auto` | auto, none, dictionary | style de polygones nommés (ajout, comme `tikzset` en LaTeX) : `("hexa-0-0": (fill: red))`. Défaut : `none`. |  |
| `code-after` | `auto` | auto, none, function | dessin ajouté par-dessus la grille (ajout ; le `tikzpicture` de l'utilisateur). Défaut : `none`. |  |
| `line-join` | `auto` | auto, str | jointure des traits (ajout ; `line join=bevel`). Défaut : `"bevel"`. |  |
| `style` | `auto` | auto, str, array | style(s) nommé(s) (`setrdgrid(definir: …)`). Défaut : `auto`. | monstyle (nom d'un style) |
| `xmax` | (positionnel) | int | nombre de polygones en largeur. |  |
| `ymax` | (positionnel) | int | nombre de polygones en hauteur. |  |

Exemple :

```typ
#rdgrid(grid: -1, 10, 7, code-after: g => (g.path)(
  "[color = red, line width=1.5pt] (trg-8-4-north east)--(trg-3-0-south east)--(trg-1-0-south east)--(trg-0-2-north west)--(trg-0-2-north east)--(trg-2-0-north east)--(trg-7-5-north east)--cycle"))
```

## setrdgrid

```typ
setrdgrid(pour: none, reinitialiser: false, definir: none, ..cles)
```

`setrdgrid(clés)` : le réglage de `rdgrid`, sous ses quatre formes (mêmes clés que `rdgrid`).

- `setrdgrid(cle: v, …)` : réglage global, pour la suite du document ; les appels s'ajoutent clé par clé. - `setrdgrid(pour: "hexa", cle: v, …)` : réglage d'un seul type de grille (`"equi"`, `"hexa"`, `"rhexa"`, `"iso"`, ou un tableau de types). - `setrdgrid(definir: "nom", cle: v, …)` : définit le style nommé « nom », appelé ensuite par `style: "nom"` ; `pour:` contrôle alors les clés contre un type. - `setrdgrid(reinitialiser: true)` : oublie les réglages global et par type (styles gardés) ; avec des clés, repart des défauts puis les applique. `reinitialiser: "tout"` oublie aussi les styles.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str, array | type visé (`"equi"`, `"hexa"`, `"rhexa"`, `"iso"`) ou `none` (tous). Défaut : `none`. |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages ; `"tout"` : oublie aussi les styles. Défaut : `false`. |  |
| `definir` | `none` | none, str | nom du style à définir avec les clés données. Défaut : `none`. |  |

Clés documentées dans le guide (`rdgrid/docs/fiches-rdgrid.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | (positionnel) | any |  | clés de `rdgrid` (et `style:`), hors `type`. |

Exemple :

```typ
#setrdgrid(scope-style: (draw: "blue!50", line-width: 0.3pt))
#setrdgrid(pour: "iso", frame: false)
#setrdgrid(definir: "pointe", only-dot: true, dot-style-app: (fill: "red"))
#rdgrid(type: "iso", 6, 4, width: 0.5) #rdgrid(style: "pointe", 5, 3, width: 0.5)
```
