---
name: typst
description: Le langage Typst pour quelqu'un qui vient de LaTeX — syntaxe des trois modes (markup, code, maths), règles set/show, context, états et compteurs, imports de paquets @local et @preview, unités, figures cetz, table de correspondance LaTeX → Typst, pièges courants, compilation (module pip typst, CLI tinymist, --font-path, --input, --root) et lecture des erreurs. Utiliser dès qu'on écrit, corrige, compile ou relit un fichier .typ, qu'une compilation Typst échoue, qu'on traduit une construction LaTeX ou TikZ en Typst, ou que l'utilisateur parle de Typst, de Tinymist ou de cetz — même pour une petite question de syntaxe. Pour un document de cours avec la suite farfadet, charger AUSSI le skill bfcours-typst.
---

# Typst

Typst est un langage de composition à la place de LaTeX : une seule passe de compilation (quelques dixièmes de seconde), des messages d'erreur localisés, un vrai langage de programmation intégré. Ce skill a été écrit et vérifié avec **Typst 0.15.0** (module pip `typst`, et Tinymist 0.15 dans VS Code) : c'est la version installée qui fait foi, pas un souvenir d'une version antérieure (`python -c "import typst; print(typst.__version__)"`).

Ce skill couvre le **langage**. Il ne dit rien des paquets de cours : pour un document farfadet (cours, fiche, évaluation), charger aussi `bfcours-typst`.

## Compiler

```bash
# <skill> = dossier de ce skill ; python = le Python qui a le module typst (pip install typst)
python "<skill>/scripts/compiler.py" doc.typ
python "<skill>/scripts/compiler.py" doc.typ --png "<dossier>" --input correction=false
```

**Où écrire** : un document se compile dans son propre dossier ; tout fichier d'essai (`.typ` de test, PDF, PNG) va dans un dossier temporaire de session, écrit avec son chemin **complet**. Jamais à la racine d'un disque, dans le dossier personnel, `Documents`, le Bureau ou les Téléchargements, et jamais de chemin raccourci tapé à la main (`C:/NOMCOU~1/…`) : le script refuse ces destinations.

Le script affiche l'erreur **avec fichier, ligne, colonne et indices** (le message brut du module pip n'a ni position ni indice), ajoute les polices de la suite farfadet quand il les trouve, prend la racine dans le dossier du fichier, et produit en option une image PNG par page. Après toute compilation d'un document destiné à quelqu'un, **regarder les PNG** : une compilation réussie ne dit rien de la mise en page. Détails (CLI, polices, racine, entrées, lecture d'une erreur) : `references/compilation.md`.

## Les trois modes en dix lignes

```typ
= Titre de section                      // markup : le texte est du texte
Du texte *gras*, _italique_, `code`, un lien @etiquette, une formule $x^2$.
#let aire(r) = calc.pi * r * r          // `#` fait entrer en mode code pour UNE expression
#aire(2)                                // appel : le résultat s'insère dans le texte
#set text(lang: "fr", size: 11pt)       // règle `set` : valeur par défaut d'un élément
#show heading: set text(fill: blue)     // règle `show` : transformer un élément
$ f(x) = (x + 1)/(2 x) $                // maths centrées (espaces après/avant `$`)
#context counter(page).get()            // ce qui dépend de la position s'écrit sous `context`
```

- **Markup** : texte, `*gras*`, `_ital_`, `- puce`, `+ numéro`, `/ Terme: déf`, `= titres`, `\` fin de ligne, `~` insécable, `--` et `---` tirets.
- **Code** : après `#` ou dans `{ … }` ; `[ … ]` revient au markup (bloc de contenu). Types : `none`, `auto`, booléens, entiers, flottants, longueurs, chaînes, contenu, tableaux `(1, 2)`, dictionnaires `(a: 1)`, fonctions.
- **Maths** : entre `$`. Les lettres isolées sont des variables (`$A B$`), un mot de plusieurs lettres est un NOM de symbole ou de fonction (`$pi$`, `$sin$`) : `$ABC$` est une erreur, écrire `$A B C$`.

Syntaxe complète (fonctions, arguments nommés, contenu en dernier argument, set/show, context, états, compteurs, imports, unités) : `references/syntaxe.md`.

## Venir de LaTeX

| LaTeX | Typst |
|---|---|
| `\section{X}` | `= X` |
| `\textbf{x}`, `\emph{x}` | `*x*`, `_x_` |
| `\begin{itemize}\item a` | `- a` |
| `\frac{a}{b}`, `\sqrt{x}` | `$a/b$` ou `$frac(a, b)$`, `$sqrt(x)$` |
| `\dfrac{a}{b}` (grande fraction en ligne) | `$display(a/b)$` — `$f(1/2)$` seul donne une fraction minuscule |
| `\overrightarrow{AB}` | `$arrow(A B)$` |
| `\mathbb{R}` | `$RR$` |
| `\newcommand{\f}[1]{…}` | `#let f(x) = […]` |
| `\vspace{1em}`, `\hfill` | `#v(1em)`, `#h(1fr)` |
| `1ex` | pas d'unité `ex` : `0.5em` |

Table complète (texte, mise en page, tableaux, maths, programmation, TikZ → cetz) : `references/latex-vers-typst.md`.

## Les pièges qui coûtent le plus

1. **`$ABC$`** → « unknown variable » : écrire `$A B C$`. Un nom de point à plusieurs lettres se sépare toujours.
2. **`;` dans un appel en maths** sépare des lignes de matrice : `$lr(] -oo ; 3])$` → « expected content, found array ». Protéger le point-virgule : `$lr(] -oo thin";" thin 3 ])$`.
3. **La virgule décimale** : `$3,14$` donne « 3, 14 ». Écrire `$3","14$` (ou une fonction de nombres d'un paquet).
4. **Le point-virgule français** est collé en maths : `$[0 ; 1]$` → « [0; 1] » ; écrire `$[0 thin; thin 1]$`. Après un `]` ouvrant, le `-` devient binaire (« ] − ∞ ») : entourer de `lr(…)`.
5. **Fin d'expression en markup** : `#str(3) + "a"` n'additionne rien (le `+ "a"` est du texte) : `#(str(3) + "a")`.
6. **Tirets dans les noms** : `#a-b` lit la variable `a-b` ; une soustraction s'écrit `#(a - b)`.
7. **`_` au milieu d'un mot** ouvre l'italique : `x_1` en texte → `x\_1` ou `$x_1$`.
8. **`sys.inputs` ne contient que des chaînes** : `sys.inputs.at("correction", default: "true") == "true"`.
9. **Racine du projet** : une image hors du dossier racine est refusée (« would escape the project root ») : passer `--racine`.
10. **Une équation centrée ne se coupe pas** : une formule trop longue déborde de la marge sans erreur.

Liste complète, avec le message d'erreur exact et la correction : `references/pieges.md`.

## Figures

Les figures TikZ se traduisent avec **cetz** (`#import "@preview/cetz:0.5.3"`), téléchargé au premier usage puis gardé dans le cache local (`%LOCALAPPDATA%/typst/packages/preview/cetz/` sous Windows) : il compile ensuite hors ligne. Repère, quadrillage, vecteurs, points nommés, courbes, codages : `references/cetz.md`.

## Méthode de travail

1. Écrire par petits morceaux et compiler souvent : une compilation coûte moins d'une seconde.
2. Sur une erreur, lire la **ligne et la colonne** données, puis les `hint:` : ils proposent souvent la correction exacte.
3. Une erreur inconnue de `references/pieges.md` et résolue : l'y ajouter en une ligne (message → cause → correction).
4. Regarder les PNG avant de livrer.
