# L'essentiel de Typst pour qui vient de LaTeX

Ce fichier suffit pour écrire, lire et corriger un document Typst. Il vaut pour Typst 0.13 à 0.15 (la version du module Python `typst` installé fait foi : `localiser.py` l'affiche). Pour les fonctions des paquets bfcours (`definition`, `exo`, `crep`, `tcbtab`…), ce n'est pas ici : `SKILL.md` et `chercher.py`.

## Sommaire

1. Les trois modes
2. Fonctions et arguments
3. Règles `set` et `show`
4. `context`, états, compteurs
5. Imports et fichiers
6. Unités
7. Mode maths
8. Correspondance LaTeX → Typst
9. Pièges : le message, la cause, la correction
10. Lire une erreur

## 1. Les trois modes

| Mode | Où | On y écrit |
|---|---|---|
| Markup | le fichier, l'intérieur de `[ … ]` | du texte et des balises légères |
| Code | après `#`, dans `{ … }`, dans les arguments d'un appel | des expressions |
| Maths | entre `$ … $` | des formules |

```typ
= Titre de section                      // == sous-section, === niveau 3
Du texte *gras*, _italique_, `code`, une formule $x^2$.
- une puce        + une liste numérotée        / Terme: définition
Fin de ligne forcée \
Espace insécable~: ici. Tirets -- et ---.  Caractères littéraux : \# \$ \* \_ \@ \<
#let aire(r) = calc.pi * r * r          // `#` : UNE expression en mode code
#aire(2)                                // le résultat s'insère dans le texte
#set text(lang: "fr")                   // règle set
$ f(x) = (x + 1) / (2 x) $              // formule centrée (espaces après et avant `$`)
```

**Où s'arrête une expression `#`.** Elle s'arrête au premier caractère qui ne peut pas la prolonger : espace, ponctuation, opérateur entouré d'espaces. Les appels `#f(x)`, les champs `#d.nom` et les méthodes `#x.len()` la prolongent. Conséquences :

- `#str(3) + "a"` n'additionne rien : seul `#str(3)` est du code. Écrire `#(str(3) + "a")`.
- `#a-b` lit la variable `a-b` (le tiret fait partie des noms). Une soustraction : `#(a - b)`.
- **Une expression collée à une lettre** continue en lisant la lettre comme un nom : `c#oeur` cherche la variable `oeur`. Le point-virgule ferme l'expression sans rien afficher : `c#oe;ur` donne « cœur ». Même règle pour `n#oe;ud`, `#oe-maj;uvre`, `12 #euro;HT`.

Un paragraphe se termine par une ligne vide. Les crochets `[a]` écrits en markup s'affichent tels quels ; un bloc de contenu qui borne la portée d'un `set` s'écrit `#[ … ]`.

Plusieurs instructions : `#{ let x = 2; x * 3 }`, ou une ligne qui commence par `#let`, `#set`, `#show`, `#if`, `#for`, `#import`, `#include`, `#context`.

```typ
#if x > 2 [grand] else [petit]
#for i in range(1, 4) [Question #i. ]
#{
  let total = 0
  for i in range(1, 5) { total += i }
  [Total : #total]
}
```

## 2. Fonctions et arguments

```typ
#let carre(x) = x * x
#let boite(titre: none, couleur: blue, corps) = block(stroke: couleur, inset: 4pt)[
  #if titre != none [*#titre* : ] #corps
]
#boite[Simple]                                 // contenu = dernier argument positionnel
#boite(titre: [T], couleur: red)[Avec titre]   // arguments nommés entre parenthèses
#let deux(a, b) = [#a / #b]
#deux[x][y]                                    // plusieurs blocs de contenu à la suite
#let rouge = boite.with(couleur: red)          // fonction partiellement appliquée
#let f(a, ..reste) = reste.pos()               // variadique : reste.pos(), reste.named()
```

- Les blocs `[…]` collés après `)` sont des arguments positionnels ajoutés à la fin. **Aucun espace** entre le nom, `(` et `[` : `#f(x) [y]` appelle `f(x)` puis affiche « [y] ».
- Les parenthèses avant les crochets : `#f[z](b: 2)` est une erreur.
- Une fonction sans argument s'appelle avec `()` : `#pagebreak()`. Écrite sans parenthèses, elle s'affiche comme un nom, sans erreur.
- Une fonction ne voit que les `#let` écrits **avant** elle.

## 3. Règles `set` et `show`

`set` fixe la valeur par défaut d'un paramètre jusqu'à la fin du bloc qui le contient (fichier, `#[…]`, corps de fonction).

```typ
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm), numbering: "1")
#set text(size: 11pt, lang: "fr")
#set par(justify: true, spacing: 0.8em)
#set heading(numbering: "I.1.")
#set enum(numbering: "a)")
#[#set text(fill: red); seulement ici] puis le texte normal
```

`show` transforme un élément :

```typ
#show heading.where(level: 1): set text(fill: blue)
#show heading.where(level: 2): it => block(fill: luma(230), inset: 3pt, it.body)
#show "bfcours": strong
#show link: underline
```

Un modèle de document est une fonction qui reçoit tout le reste : `#show: modele.with(titre: […])`. Un `import` ne transporte que des noms : les `set` et `show` d'un fichier importé ne s'appliquent pas chez l'importateur, d'où le `#show: modele(…)` en tête des documents bfcours.

## 4. `context`, états, compteurs

Tout ce qui dépend de la position dans le document se lit sous `context` : numéro de page, valeur d'un compteur ou d'un état, mesure d'un contenu. Sans lui : « can only be used when context is known ».

```typ
#context counter(page).get()            // (3,)
#context counter(page).final().first()  // nombre total de pages
#context measure([Bonjour]).width
#let s = state("pts", 0)
#let pts(n) = { s.update(x => x + n); [(#n pts)] }
Total : #context s.final()
```

Une fonction qui lit un état renvoie `context …`, elle ne lit pas l'état pour renvoyer un nombre. Les entrées de compilation (`--input correction=false`) se lisent par `sys.inputs.at("correction", default: "true")` et sont **des chaînes** : comparer à `"true"`, pas à `true`. Dans un document bfcours, on ne lit pas `sys.inputs` soi-même : `ifcorrection` le fait.

## 5. Imports et fichiers

```typ
#import "outils.typ": aire, perimetre    // noms choisis, chemin relatif au fichier
#import "outils.typ": *                   // tout
#include "chapitre1.typ"                  // insère le CONTENU du fichier
#import "@preview/farfadet:0.2.0": *  // la suite (Typst Universe, ou sa copie du dépôt)
#import "@preview/cetz:0.5.3"             // paquet public (téléchargé une fois, puis en cache)
```

- `@local/<nom>:<version>` est cherché dans le dossier des paquets locaux de Typst (`localiser.py` l'affiche).
- **Racine du projet** : aucun fichier hors de la racine n'est lisible (« would escape the project root ») ; un chemin qui commence par `/` part de la racine, pas du disque. Une image se range donc dans le dossier du document ou en dessous.
- Hors ligne, seul un paquet `@preview` déjà en cache compile.

## 6. Unités

| Unité | Sens |
|---|---|
| `pt`, `mm`, `cm`, `in` | absolues |
| `em` | taille de la police courante ; **pas d'unité `ex`** : `1ex` de LaTeX devient `0.5em` |
| `%` | fraction de la place disponible (`width: 100%` = `\linewidth`) |
| `fr` | part de l'espace restant (`#h(1fr)` = `\hfill`) |
| `deg`, `rad` | angles |

Les longueurs se combinent : `1cm + 2mm`, `2 * 1em`, `50% + 1cm`.

## 7. Mode maths

```typ
$x^2$  $x_(n+1)$  $e^(-x)$  $a/b$  $(a+b)/c$  $frac(a, b)$  $sqrt(2)$  $root(3, x)$  $binom(n, k)$
$arrow(A B)$  $vec(x, y)$  $mat(1, 2; 3, 4)$  $abs(x)$  $norm(arrow(u))$  $overline(z)$  $hat(x)$
$RR$ $NN$ $ZZ$ $QQ$ $CC$  $RR_+^*$  $cal(C)$  $bold(u)$  $upright(d)$  $"texte"$  $op("pgcd")(a, b)$
$!=$ $<=$ $>=$ $approx$ $times$ $dot$ $div$ $plus.minus$ $oo$ $emptyset$ $in$ $subset$ $union$ $inter$
$forall$ $exists$ $=>$ $<=>$ $->$ $dots.h$ $quad$ $thin$ $med$
$lim_(x -> +oo) f(x)$  $sum_(k=1)^n k$  $integral_0^1 x dif x$
$f(x) = cases(x^2 &"si" x >= 0, -x &"sinon")$
$ a &= b \ &= c $                         // lignes alignées : `\` change de ligne, `&` aligne
```

Les règles qui changent tout :

- **Lettres séparées.** Une lettre seule est une variable ; plusieurs lettres collées forment un NOM (`pi`, `sin`, `RR`). `$AB$` → erreur « unknown variable: AB » : écrire `$A B$`, `$A B C$`, `$(A B)$`. Un mot en texte : `$"aire"$`.
- **Un espace avant la parenthèse d'une variable appliquée.** `$P_A(B)$` est lu comme l'indice `A(B)` ; écrire `$P_A (B)$`. De même `$f_1 (x)$`.
- **Indices et exposants de plusieurs caractères** entre parenthèses : `$x^(2n)$`, `$u_(n+1)$`. Les parenthèses ne s'affichent pas.
- **Fractions.** `$a/b$` forme une fraction de ce qui touche la barre ; grouper par des parenthèses (`$(a+b)/(c+d)$`, parenthèses retirées à l'affichage). En ligne, une fraction est petite : `$display(a/b)$` pour la taille de `\dfrac`, `$inline(a/b)$` pour celle de `\tfrac`. Une barre oblique littérale : `$a slash b$`.
- **Virgule décimale** : `$3,14$` donne « 3, 14 ». Écrire `$3","14$` (ou `#num(3.14)` de farfadet-maths).
- **Point-virgule.** Dans un appel de fonction en maths, `;` sépare des lignes de matrice : `$lr(] -oo ; 3])$` → « expected content, found array ». Écrire `$lr(] -oo thin";" thin 3 ])$`. Entre crochets simples, `$[0 thin; thin 1]$` pour l'espacement français.
- **Intervalle ouvert à gauche.** Après un `]` ouvrant, `-` devient un moins binaire (« ] − ∞ ») : entourer de `lr(…)`.
- **Formule centrée** : `$ … $` avec des espaces intérieurs. Elle ne se coupe jamais : trop longue, elle déborde de la marge sans erreur. Couper avec `\` et `&`.
- Une fonction de paquet utilisée en maths s'écrit sans `#` : `$vect(A B)$`. Un contenu de texte au milieu d'une formule : `$x = #h(1em) "ou" #h(1em) y$`.

## 8. Correspondance LaTeX → Typst

### Document et texte

| LaTeX | Typst |
|---|---|
| `\documentclass`, `\begin{document}` | rien : le fichier est le document |
| `\usepackage{x}` | `#import "@preview/x:…": *` ou `@local/…` |
| `\geometry{margin=2cm}`, `landscape` | `#set page(margin: 2cm)`, `#set page(flipped: true)` |
| `\usepackage[french]{babel}` | `#set text(lang: "fr")` |
| `\input{f}` | `#include "f.typ"` (contenu) ou `#import "f.typ": *` (définitions) |
| `\textbf{x}`, `\emph{x}`, `\underline{x}` | `*x*`, `_x_`, `#underline[x]` |
| `\texttt{x}`, `\textsc{x}` | `` `x` ``, `#smallcaps[x]` |
| `\textcolor{red}{x}` | `#text(fill: red)[x]` |
| `\definecolor{c}{HTML}{C2410C}` | `#let c = rgb("#c2410c")` |
| `red!30` | `red.lighten(70%)` |
| `\small`, `\large` | `#text(size: 0.9em)[…]`, `#text(size: 1.2em)[…]` |
| `\textsuperscript{e}` | `#super[e]` |
| `\og x \fg{}` | `"x"` avec `lang: "fr"` → « x » |
| `\oe`, `\OE`, `\euro` | `œ`, `Œ`, `€` directement ; en ASCII avec bfcours : `c#oe;ur`, `#oe-maj;uvre`, `#euro` |
| `\\` | `\` en fin de ligne |
| `\footnote{x}`, `\href{u}{t}` | `#footnote[x]`, `#link("u")[t]` |
| `\label{x}` … `\ref{x}` | `<x>` … `@x` |
| `%` commentaire | `//` ou `/* … */` |

### Structure et mise en page

| LaTeX | Typst |
|---|---|
| `\section{X}`, `\section*{X}` | `= X`, `#heading(numbering: none)[X]` |
| `\tableofcontents` | `#outline()` (bfcours : `#tableofcontents()`) |
| `itemize`, `enumerate`, `description` | `- a`, `+ a`, `/ Terme: déf` (sous-liste : 2 espaces de retrait) |
| `\newpage` | `#pagebreak()` |
| `\vspace{1cm}`, `\hspace{1cm}`, `\hfill` | `#v(1cm)`, `#h(1cm)`, `#h(1fr)` |
| `\medskip`, `\bigskip` | `#v(0.5em)`, `#v(1em)` |
| `center`, `flushright` | `#align(center)[…]`, `#align(right)[…]` |
| `minipage{0.5\linewidth}` | `#box(width: 50%)[…]` ou `#grid(columns: (1fr, 1fr), …)` (bfcours : `multi-colonnes`) |
| `\fbox{x}` | `#box(stroke: 0.5pt, inset: 3pt)[x]` |
| `\phantom{x}`, `\raisebox{2pt}{x}` | `#hide[x]`, `#move(dy: -2pt)[x]` |
| `\includegraphics[width=5cm]{f}` | `#image("f.png", width: 5cm)` (PNG, JPG, SVG, PDF) |
| `tabular{|c|c|}` | `#table(columns: 2, [a], [b], …)` (bfcours : `tcbtab`) |
| `\multicolumn{2}{c}{x}`, `\multirow` | `table.cell(colspan: 2)[x]`, `table.cell(rowspan: 2)[x]` |

### Maths

| LaTeX | Typst |
|---|---|
| `\frac{a}{b}`, `\dfrac`, `\tfrac` | `$a/b$`, `$display(a/b)$`, `$inline(a/b)$` |
| `\overrightarrow{AB}`, `\vec u` | `$arrow(A B)$`, `$arrow(u)$` (bfcours : `$vect(A B)$`) |
| `\begin{pmatrix} x \\ y \end{pmatrix}` | `$vec(x, y)$` ; matrice : `$mat(1, 2; 3, 4)$` |
| `\mathbb{R}`, `\mathcal{C}`, `\mathrm{d}` | `$RR$`, `$cal(C)$`, `$upright(d)$` |
| `\text{si}`, `\operatorname{pgcd}` | `$"si"$`, `$op("pgcd")$` |
| `\left( … \right)` | automatique ; forcé : `$lr(( … ))$` |
| `\lVert u \rVert`, `\lvert x \rvert` | `$norm(arrow(u))$`, `$abs(x)$` |
| `\leq`, `\neq`, `\times`, `\cdot`, `\pm`, `\infty` | `$<=$`, `$!=$`, `$times$`, `$dot$`, `$plus.minus$`, `$oo$` |
| `\Rightarrow`, `\Leftrightarrow`, `\to` | `$=>$`, `$<=>$`, `$->$` |
| `\ldots`, `\quad`, `\,` | `$dots.h$`, `$quad$`, `$thin$` |
| `\widehat{ABC}` | `$hat(A B C)$` |
| `align*` | `$ a &= b \ &= c $` |
| `3{,}14`, `\num{1234.5}` | `$3","14$`, `#num(1234.5)` (farfadet-maths) |

### Programmation

| LaTeX | Typst |
|---|---|
| `\newcommand{\R}{\mathbb{R}}` | `#let R = $RR$` |
| `\newcommand{\f}[2]{#1 + #2}` | `#let f(a, b) = [#a + #b]` |
| argument optionnel `[opt]` | argument nommé `opt: défaut` |
| `\newenvironment{boite}{…}{…}` | `#let boite(corps) = block(…)[#corps]` |
| `\ifthenelse{…}{a}{b}` | `#if cond [a] else [b]` |
| `\foreach \i in {1,...,5}` | `#for i in range(1, 6) […]` |
| `\newcounter`, `\stepcounter`, `\thec` | `#let c = counter("c")`, `#c.step()`, `#context c.display()` |
| deux fichiers maîtres prof et élève | un seul fichier, `--input correction=false` |

### TikZ → cetz (figures hors de farfadet-geom)

| TikZ | cetz (`#cetz.canvas(length: 1cm, { import cetz.draw: *; … })`) |
|---|---|
| `scale=0.8` | `length: 0.8cm` |
| `\draw (0,0) -- (3,2);`, `[->]` | `line((0, 0), (3, 2))`, `mark: (end: ">")` |
| `[thick, blue, dashed]` | `stroke: (paint: blue, thickness: 1pt, dash: "dashed")` |
| `\draw (1,1) circle (0.5);` | `circle((1, 1), radius: 0.5)` |
| `\node[above] at (A) {$A$};` | `content(A, [$A$], anchor: "south", padding: 3pt)` (`"south"` place AU-DESSUS) |
| `\coordinate (A) at (1,1);` | `let A = (1, 1)` |
| `($(A)!0.5!(B)$)` | `(A, 50%, B)` (pourcentage obligatoire) |
| `-- cycle` | `line(A, B, C, close: true)` |

Dans un canevas, `import cetz.draw: *` masque `line`, `rect`, `circle`, `grid`, `rotate`, `content` de Typst ; un nombre y est en unités du canevas, une longueur (`2pt`) reste absolue.

## 9. Pièges : le message, la cause, la correction

| On écrit | Message ou effet | Correction |
|---|---|---|
| `$ABC$` | `unknown variable: ABC` | `$A B C$` |
| `c#oeur` | `unknown variable: oeur` | `c#oe;ur` |
| un nom défini plus bas | `unknown variable` | déplacer le `#let` avant son usage |
| un nom importé masqué | comportement étrange, sans erreur | ne pas redéfinir par `#let` un nom du paquet (`point`, `distance`…) |
| `$lr(] -oo ; 3])$` | `expected content, found array` | `";"` |
| `#box(width: 2ex)` | `invalid floating point number` | `1em` |
| `counter(page).get()` hors contexte | `can only be used when context is known` | `#context …` |
| `x_1` en texte | `unclosed delimiter` (italique ouvert) | `$x_1$` ou `x\_1` |
| `#a * b` | `unclosed delimiter` (l'étoile ouvre le gras) | `#(a * b)` |
| `#f[z](b: 2)` | `expected function, found content` | `#f(b: 2)[z]` |
| `#image("../img.png")` | `would escape the project root` | ranger l'image sous le dossier du document |
| clé mal écrite dans un appel | `unexpected argument: …` | lire la signature (`chercher.py --fiche`) |
| `$3,14$` | « 3, 14 » | `$3","14$` |
| `#f (x)`, `#f(x) [y]` | texte affiché, fonction non appelée ou bloc perdu | aucun espace avant `(` ou `[` |
| `#pagebreak` | le nom s'affiche | `#pagebreak()` |
| formules minuscules | aucune erreur : polices des paquets non passées | compiler par `compiler.py`, qui les passe |
| `$1/2$` en ligne | fraction réduite | `$display(1/2)$` |
| `\vspace` négatif reporté | chevauchements | ne pas le reporter : Typst ne crée pas le blanc qu'il compensait |

Habitudes LaTeX à perdre : pas de seconde passe (références et totaux justes du premier coup) ; pas de `%` en fin de ligne (un saut de ligne simple est une espace en markup, rien en mode code) ; pas de macro qui « avale » la suite (une fonction reçoit ses arguments entre `()` et `[]`) ; une ligne vide dans un `[…]` crée un vrai paragraphe.

## 10. Lire une erreur

```text
error: unknown variable: ABC
   ┌─ chemin/doc.typ:35:12
   │
35 │ $A B C$ et $ABC$
   │             ^^^
   = hint: if you meant to display multiple letters as is, try adding spaces between each letter: `A B C`
```

1. `error:` donne la cause ; `warning:` signale un doute, la compilation a réussi.
2. `fichier:ligne:colonne` et le soulignement `^^^` montrent l'expression fautive.
3. Si le fichier cité est celui d'un **paquet** (`@local/…`), l'erreur vient presque toujours d'un argument mal formé dans l'appel du document : remonter la trace (« error occurred in this call of function … ») jusqu'à la ligne du document.
4. `hint:` propose souvent la correction exacte.
5. Une erreur à la fois : corriger, recompiler. Une compilation coûte une à trois secondes.

Une compilation réussie ne dit rien de la mise en page (débordements, formules trop petites, pages blanches) : regarder les images.
