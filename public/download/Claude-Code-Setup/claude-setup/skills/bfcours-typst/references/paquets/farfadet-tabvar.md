# farfadet-tabvar

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": variations` puis `#import variations: *`.
- Réglage : `setbftabvar` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-tabvar.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-tabvar`).

## Sommaire

- `setbftabvar` — Setter unique du paquet (signature commune de la famille).
- `tkz-tab-line` — Ligne de signes (`\tkzTabLine`). `spec` : 2·N − 1 éléments pour N valeurs de x, séparés par des virgules : les valeurs de x aux rangs impai…
- `tkz-tab-var` — Ligne de variations (`\tkzTabVar`). Un élément par valeur de x : - `"R"` : rien (la flèche passe) ; `"+"`, `"-"` : un point haut ou bas san…
- `tabvar` — Vérifie les arguments publics de `tabvar` puis dessine le tableau.

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `a-completer` |  |  | 3 : `tkz-tab-line`, `tkz-tab-var`, `tabvar` |

## setbftabvar

```typ
setbftabvar(pour: none, reinitialiser: false, definir: none, ..cles)
```

Setter unique du paquet (signature commune de la famille).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` |  |  |  |
| `reinitialiser` | `false` |  |  |  |
| `definir` | `none` |  |  |  |

Clés documentées dans le guide (`farfadet-tabvar/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Les clés du tableau de @sec-perso. |

## tkz-tab-line

```typ
tkz-tab-line(nom, spec, h: 1, a-completer: auto)
```

Ligne de signes (`\tkzTabLine`). `spec` : 2·N − 1 éléments pour N valeurs de x, séparés par des virgules : les valeurs de x aux rangs impairs, les intervalles aux rangs pairs. Éléments : « » (vide), `+`, `-`, `z` (zéro), `t` (trait pointillé), `d` (double barre), `|` (trait plein), `h` (hachures, intervalle seulement), ou une formule.

LaTeX : `\tkzTabLine`

Clés communes acceptées (voir en tête) : `a-completer`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) |  |  |  |
| `spec` | (positionnel) |  |  |  |
| `h` | `1` |  |  |  |

Clés documentées dans le guide (`farfadet-tabvar/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `signes` | (positionnel) | str \| array |  | Les $2 N - 1$ éléments d'une ligne de signes pour $N$ valeurs de $x$ : une chaîne séparée par des virgules (`",-,z,+,"`) ou un tableau. Éléments : vide, `+`, `-`, `z`, `t`, `d`, `\|`, `h` ou une formule. |

## tkz-tab-var

```typ
tkz-tab-var(nom, ..items, h: 2, a-completer: auto)
```

Ligne de variations (`\tkzTabVar`). Un élément par valeur de x : - `"R"` : rien (la flèche passe) ; `"+"`, `"-"` : un point haut ou bas sans valeur ; - `("+", val)`, `("-", val)` : une valeur en haut ou en bas ; - `("+D-", gauche, droite)`, `("-D+", …)`, `("D-", droite)`, `("+D", gauche)`… : valeur interdite, double barre, limites de part et d'autre ; - `("im", val)` : image intermédiaire posée sur la flèche, à l'abscisse de cette colonne.

LaTeX : `\tkzTabVar`

Clés communes acceptées (voir en tête) : `a-completer`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) |  |  |  |
| `h` | `2` |  |  |  |

Clés documentées dans le guide (`farfadet-tabvar/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `elements` | (positionnel) | array \| str |  | Un élément par valeur de $x$ : `"R"`, `"+"`, `"-"`, `("+", v)`, `("-", v)`, `("+D-", g, d)` et ses variantes, `("D-", d)`, `("+D", g)`, `"D"`, `("im", v)`. |

## tabvar

```typ
tabvar(x, ..args, nom-x: auto, a-completer: false, version: auto)
```

Vérifie les arguments publics de `tabvar` puis dessine le tableau.

Clés communes acceptées (voir en tête) : `a-completer`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `x` | (positionnel) |  |  |  |
| `nom-x` | `auto` |  |  |  |
| `version` | `auto` |  |  |  |

Clés documentées dans le guide (`farfadet-tabvar/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `lignes` | (positionnel) | dictionary |  | Les lignes du tableau, dans l'ordre : résultats de `tkz-tab-line` et `tkz-tab-var`. |
| `style` | `none` | str \| array |  | Style nommé, défini par `setbftabvar(definir: …)`. |
| `..cles` | `(:)` | any |  | Toute clé de `setbftabvar` (voir @sec-perso) : `lgt`, `espcl`, `deltacl`, `lw`, `nocadre`, `unite`, `h-x`, `largeur`, `reduire`, `fractions`, `taille`, `alignement`, `pointilles`, `pointe`, `marge-fleches`, `ep-fleches`… |
