# farfadet-latex

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": extraits-latex` puis `#import extraits-latex: *`.
- Réglage : `setbflatex` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-latex.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-latex`).

## Sommaire

- `latex` — Insère un extrait de code LaTeX, compilé à l'enregistrement et inséré comme image PDF. C'est la fonction à utiliser : l'import du paquet (o…
- `latex-avec` — Construit la fonction `latex` d'un document à partir de ses rendus. Forme « historique » : le document lit lui-même `rendus-tex/index.json`…
- `setbflatex` — Règle les extraits LaTeX de la suite du document : seul réglage du paquet (réglage global, style nommé, remise à zéro). Les appels s'ajoute…

## latex

```typ
latex
```

Insère un extrait de code LaTeX, compilé à l'enregistrement et inséré comme image PDF. C'est la fonction à utiliser : l'import du paquet (ou du méta-paquet) suffit, sans aucune ligne de mise en place. Les clés sont celles de `setbflatex` (`paquets`, `preambule`, `moteur`, `largeur`, `echelle`, `align`, `montrer-code`, `style`…).

Les rendus viennent de bfwatch (extension VS Code `bfcours-typst`, Ctrl+Maj+B) : il repère les extraits, les compile avec LaTeX (seulement ceux qui ont changé) et les range dans `rendus-tex/`. Les PDF du Ctrl+Maj+B les reçoivent directement ; l'aperçu Tinymist les lit si le document a écrit une fois `#setbflatex(lire: p => read(p, encoding: none))`. Sans cela, l'extrait est remplacé par un encadré « extrait LaTeX non rendu ».

Clés documentées dans le guide (`farfadet-latex/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `code` | (positionnel) | str \| raw |  | Le code LaTeX, dans un bloc brut ```` ```latex ```` placé entre crochets. |
| `paquets` | `()` | auto \| str \| array |  | Paquets chargés par `\usepackage`. Un paquet à options s'écrit `("babel", "french")`. |
| `preambule` | `none` | auto \| none \| str \| raw |  | Lignes de préambule propres à l'extrait. |
| `moteur` | `auto` | auto \| str | `auto`, `lualatex`, `pdflatex`, `xelatex` | Moteur LaTeX de cet extrait. |
| `largeur` | `auto` | auto \| length \| ratio |  | Largeur du rendu ; `auto` garde la taille naturelle. |
| `echelle` | `100%` | auto \| ratio |  | Facteur appliqué à la taille naturelle (sans effet si `largeur` est fixée). |
| `align` | `center` | auto \| alignment |  | Position horizontale du rendu. |
| `montrer-code` | `false` | auto \| bool |  | Affiche aussi le code LaTeX sous le rendu. |
| `style` | `auto` | auto \| str \| array |  | Nom d'un style défini par `setbflatex(definir: …)`, ou tableau de noms. |
| `..options` | `(:)` | any |  | Toute autre clé de `setbflatex` (`bordure`, `code-fond`, `couleur-erreur`…). |

Exemple :

```typ
#latex[```latex
$\dfrac{3}{4} + \dfrac{1}{4} = 1$
```]
```

## latex-avec

```typ
latex-avec(index, lire, dossier: "rendus-tex")
```

Construit la fonction `latex` d'un document à partir de ses rendus. Forme « historique » : le document lit lui-même `rendus-tex/index.json`, produit par le démon `rendus_tex`. Pour un cours enregistré avec l'extension VS Code (bfwatch), inutile : `latex` est déjà exporté par le paquet.

Typst interdit à une fonction de paquet de lire un fichier du document : l'index et la lecture des PDF sont donc fournis par le document lui-même.

Dans un document découpé en chapitres, le script écrit aussi `rendus-tex/latex.typ`, qui contient ces deux lignes : un chapitre n'a qu'à écrire `#import "rendus-tex/latex.typ": latex`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `index` | (positionnel) | dictionary | contenu de `rendus-tex/index.json`, lu avec `json(…)`. |  |
| `lire` | (positionnel) | function | fonction `chemin => read(chemin, encoding: none)` écrite dans le document. |  |
| `dossier` | `"rendus-tex"` | str | dossier des rendus, vu depuis le fichier qui écrit `lire`. |  |

Exemple :

```typ
#import "@preview/farfadet:0.2.0": latex-avec
#let latex = latex-avec(json("rendus-tex/index.json"), p => read(p, encoding: none))
```

## setbflatex

```typ
setbflatex(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les extraits LaTeX de la suite du document : seul réglage du paquet (réglage global, style nommé, remise à zéro). Les appels s'ajoutent clé par clé ; une clé locale de `latex(…)` l'emporte toujours. Une clé inconnue ou une valeur invalide arrête la compilation avec la liste des possibilités.

Clés (aucune n'a d'équivalent LaTeX : les noms sont ceux de Typst) :

*Le contenu LaTeX*

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none | sans objet (le paquet n'a qu'un type d'objet) ; gardé pour la signature commune des setters. |  |
| `reinitialiser` | `false` | bool, str | `true` repart des défauts avant d'appliquer les clés (styles gardés) ; `"tout"` oublie aussi les styles nommés (défaut `false`). |  |
| `definir` | `none` | none, str | définit le style nommé de ce nom avec les clés données, au lieu de régler ; on l'appelle ensuite par `style: "nom"` sur `latex(…)` ou dans `setbflatex(…)`. Un style peut en appeler un autre (`style:`) ; un style défini … |  |

Clés documentées dans le guide (`farfadet-latex/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Les clés du tableau du chapitre suivant (et `style:`) ; une clé inconnue ou une valeur invalide arrête la compilation avec la liste des possibilités. |

Exemple :

```typ
#setbflatex(paquets: ("tikz",), echelle: 80%, moteur: "pdflatex")
#setbflatex(couleur-erreur: purple, code-fond: luma(230))
#setbflatex(definir: "figure", paquets: ("tikz",), echelle: 85%)
#setbflatex(reinitialiser: true)
```
