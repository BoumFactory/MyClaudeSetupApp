# Syntaxe de Typst 0.15

Tout ce qui suit a été compilé avec Typst 0.15.0 (module pip `typst`).

## Sommaire

1. Les trois modes et le passage de l'un à l'autre
2. Fonctions : appel, arguments nommés, contenu en dernier argument, `.with`
3. Règles `set` et `show`, portée
4. `context`, états, compteurs, requêtes
5. Imports, `include`, paquets `@local` et `@preview`
6. Unités et longueurs
7. Types et méthodes utiles
8. Mise en page de base
9. Maths

## 1. Les trois modes

| Mode | Où | On y écrit |
|---|---|---|
| Markup | le fichier, l'intérieur de `[ … ]` | du texte et des balises légères |
| Code | après `#`, dans `{ … }`, dans les arguments d'un appel | des expressions |
| Maths | entre `$ … $` | des formules |

Markup :

```typ
= Titre   == Sous-titre   === Niveau 3
*gras*  _italique_  `code`  \ (fin de ligne)  ~ (espace insécable)  -- (demi-cadratin)  --- (cadratin)
- puce          + liste numérotée          / Terme: définition
<etiquette>  et  @etiquette (référence)    // commentaire    /* bloc */
\#  \$  \*  \_  \\  \@  \<   (caractères littéraux)
```

Un paragraphe se termine par une ligne vide. Les crochets `[ … ]` écrits en markup sont du **texte** : `[a]` affiche « [a] ». Pour un bloc de contenu qui borne la portée d'un `set`, écrire `#[ … ]`.

Code : `#` fait entrer en mode code pour **une seule expression**, qui s'arrête au premier caractère qui ne peut pas la prolonger (espace, ponctuation…). Les appels, les accès de champ (`#d.nom`) et les méthodes (`#x.len()`) se prolongent ; un opérateur (`+`, `*`, `-` entouré d'espaces) ne prolonge pas : `#(a + b)`. Un point final après `#d.nom.` est bien du texte.

Plusieurs instructions : `#{ let x = 2; x * 3 }` ou `#let`, `#set`, `#show`, `#if`, `#for`, `#while`, `#import`, `#include`, `#context`, `#return` en tête de ligne. Un bloc `{ … }` renvoie la **concaténation** de ses valeurs non `none`.

```typ
#let x = 3
#if x > 2 [grand] else if x > 1 [moyen] else [petit]
#for i in range(1, 4) [Question #i. ]
#{
  let total = 0
  for i in range(1, 5) { total += i }
  [Total : #total]
}
```

## 2. Fonctions

```typ
#let carre(x) = x * x                         // fonction d'une expression
#let boite(titre: none, couleur: blue, corps) = block(stroke: couleur, inset: 4pt)[
  #if titre != none [*#titre* : ] #corps
]
#boite[Simple]                                 // contenu en dernier argument positionnel
#boite(titre: [T], couleur: red)[Avec titre]   // arguments nommés entre parenthèses
#let deux(a, b) = [#a / #b]
#deux[x][y]                                    // plusieurs blocs de contenu à la suite
#let rouge = boite.with(couleur: red)          // fonction partiellement appliquée
#let f(a, b: 2, ..reste) = a + b + reste.pos().sum(default: 0)   // variadique : reste.pos(), reste.named()
```

Les blocs `[…]` collés après la parenthèse sont des arguments positionnels ajoutés à la fin. **Pas d'espace** entre `)` et `[` : `#f(x) [y]` appelle `f(x)` puis affiche « [y] » comme du texte. Les parenthèses viennent avant les crochets : `#f[z](b: 2)` est une erreur (« expected function, found content »).

## 3. `set` et `show`

`set` fixe la valeur par défaut d'un paramètre d'un élément, jusqu'à la fin du bloc qui le contient (fichier, `#[…]`, `{…}`, corps de fonction).

```typ
#set page(paper: "a4", margin: (x: 2cm, y: 2.5cm), numbering: "1 / 1")
#set text(font: "New Computer Modern", size: 11pt, lang: "fr")
#set par(justify: true, first-line-indent: 0pt, spacing: 0.8em)
#set heading(numbering: "I.1.")
#set enum(numbering: "a)")
#set math.equation(numbering: "(1)")
#[#set text(fill: red); seulement ici] puis le texte normal
```

`show` transforme un élément choisi par un sélecteur :

```typ
#show heading.where(level: 1): set text(fill: blue)                  // show-set
#show heading.where(level: 2): it => block(fill: luma(230), inset: 3pt, it.body)  // fonction
#show "bfcours": strong                                              // un texte
#show regex("\d+"): it => text(fill: green, it)                      // une expression régulière
#show <special>: set text(weight: "bold")                            // une étiquette : #[mot] <special>
#show link: underline
```

Modèle de document : une fonction qui reçoit tout le reste du document.

```typ
#let modele(titre: none, corps) = {
  set heading(numbering: "I.1.")
  align(center, text(14pt, weight: "bold", titre))
  corps
}
#show: modele.with(titre: [Mon document])
```

Un `import` ne transporte que des noms : les `set`/`show` d'un fichier importé ne s'appliquent pas chez l'importateur. C'est la raison d'être de `#show: modele`.

## 4. `context`, états, compteurs, requêtes

Tout ce qui dépend de l'endroit du document (numéro de page, valeur d'un compteur, d'un état, mesure d'un contenu) se lit sous `context`. Sans lui : « can only be used when context is known ».

```typ
#context counter(page).get()                  // tableau : (3,)
#context counter(page).display()              // « 3 » selon la numérotation
#context counter(page).final().first()        // nombre total de pages
#context here().position().y                  // position verticale
#context measure([Bonjour]).width             // mesure d'un contenu
#layout(taille => [largeur : #taille.width])  // place disponible

#let q = counter("question")
#let question() = { q.step(); context [Q#q.display()] }     // step AVANT la lecture
#let s = state("pts", 0)
#let pts(n) = { s.update(x => x + n); [(#n pts)] }
Total : #context s.final()                    // valeur à la fin du document

#metadata("x") <meta>
#context query(<meta>).len()                  // éléments étiquetés
```

`context` fige la valeur au point où il est écrit. Une fonction qui lit un état doit retourner `context …`, pas lire hors contexte et retourner un nombre.

## 5. Imports et paquets

```typ
#import "outils.typ": aire, perimetre       // noms choisis (chemin relatif au fichier)
#import "outils.typ": aire as a             // renommage
#import "outils.typ"                         // module : outils.aire(…)
#import "outils.typ": *                      // tout
#include "chapitre1.typ"                     // insère le CONTENU du fichier (ses set/show y restent confinés)
#import "@local/monpaquet:0.1.0": *     // paquet local
#import "@preview/cetz:0.5.3"                // paquet de l'univers Typst (cache local)
```

- `@local/<nom>:<version>` : dossier `%APPDATA%/typst/packages/local/<nom>/<version>/` (Windows), qui contient `typst.toml` et le point d'entrée (`lib.typ`).
- `@preview/<nom>:<version>` : téléchargé au premier usage dans `%LOCALAPPDATA%/typst/packages/preview/`. Hors ligne, seul ce qui est déjà en cache compile ; regarder ce dossier avant de choisir une version.
- Un chemin commençant par `/` part de la racine du projet ; aucun fichier hors de la racine n'est lisible.

## 6. Unités

| Unité | Sens |
|---|---|
| `pt`, `mm`, `cm`, `in` | absolues |
| `em` | taille de la police courante (`0.5em` remplace le `1ex` de LaTeX : il n'y a **pas d'unité `ex`**, `2ex` est une erreur de syntaxe) |
| `%` | fraction de la place disponible (`width: 100%`) |
| `fr` | part de l'espace restant (`#h(1fr)`, `columns: (1fr, 2fr)`) |
| `deg`, `rad` | angles |

Les longueurs se combinent : `1cm + 2mm`, `2 * 1em`, `50% + 1cm` (longueur relative). `2cm / 1mm` donne le nombre `20`.

## 7. Types et méthodes utiles

```typ
none  auto  true  false  3  3.14  "chaîne"  [contenu]  (1, 2, 3)  (a: 1, b: 2)  1cm  45deg  50%  1fr
(1, 2, 3).map(x => x * 2)   .filter(x => x > 1)   .sum()   .len()   .at(0)   .first()   .last()   .sorted()
("a", "b").join(", ")   ("a", "b").enumerate()   range(1, 5)
d.at("c", default: 0)   d.keys()   d.values()   d.pairs()   for (k, v) in d [ … ]
"abc".len()  "a,b".split(",")  "abc".contains("b")  upper("é")  str(3)  int(3.7)  float("2.5")  repr(x)  type(x)
calc.round(2.567, digits: 2)  calc.sqrt(2)  calc.pow(2, 10)  calc.rem(7, 3)  calc.floor(2.5)  calc.max(1, 5)  calc.pi
rgb("#c2410c")  rgb(255, 0, 0)  luma(50%)  blue.lighten(50%)  red.darken(20%)  color.mix(red, blue)
```

`().join()` renvoie `none` (pas `""`). Un champ de dictionnaire qui contient une fonction s'appelle entre parenthèses : `(d.f)(x)`.

## 8. Mise en page de base

```typ
#v(3mm)  #h(2cm)  #h(1fr)  #pagebreak()  #colbreak()
#align(center)[centré]   #align(right + horizon, …)
#block(fill: luma(235), inset: 6pt, radius: 3pt, width: 100%, breakable: true)[bloc]   // se coupe entre pages
#box(stroke: 0.5pt, inset: 2pt)[en ligne]                                              // ne se coupe jamais
#grid(columns: (1fr, 2fr), gutter: 5pt, [A], [B])
#columns(2)[Colonne 1 #colbreak() Colonne 2]
#stack(dir: ltr, spacing: 4pt, [A], [B])
#place(top + right, dx: -2mm, rect(width: 5mm, height: 5mm))    // hors flux
#rect(width: 2cm, height: 1cm, stroke: (paint: blue, dash: "dashed"), radius: 2pt)
#circle(radius: 3mm, fill: luma(200))   #line(length: 100%, stroke: 0.5pt + gray)
#image("figure.png", width: 6cm)
#figure(image("f.png"), caption: [Légende]) <fig>   puis @fig
#table(
  columns: (auto, 1fr, 1fr), align: center + horizon, stroke: 0.5pt,
  fill: (x, y) => if y == 0 { luma(230) },
  table.header([$x$], [$-1$], [$2$]),
  table.cell(colspan: 2)[fusion], [c],
  table.hline(stroke: 1.5pt),
  [d], [e], [f],
)
#footnote[Note]  #link("https://typst.app")[lien]  #link(<fig>)[vers la figure]
#rotate(10deg)[…]  #move(dx: 3pt)[…]  #scale(150%)[…]  #lorem(30)
```

## 9. Maths

```typ
$x^2$  $x_(n+1)$  $e^(-x)$  $a/b$  $(a+b)/c$  $frac(a, b)$  $sqrt(2)$  $root(3, x)$  $binom(n, k)$
$arrow(A B)$  $vec(x, y)$  $mat(1, 2; 3, 4)$  $abs(x)$  $norm(arrow(u))$  $overline(z)$  $hat(x)$  $x'$
$RR$ $NN$ $ZZ$ $QQ$ $CC$  $RR_+^*$  $bb(N)$  $cal(C)$  $bold(u)$  $"texte"$  $op("pgcd")(a, b)$
$!=$ $<=$ $>=$ $approx$ $times$ $dot$ $div$ $plus.minus$ $oo$ $emptyset$ $in$ $subset$ $union$ $inter$
$forall$ $exists$ $=>$ $<=>$ $arrow.r$ $dots.h$ $quad$ $thin$ $med$
$lim_(x -> +oo) f(x)$  $sum_(k=1)^n k$  $integral_0^1 x dif x$
$f(x) = cases(x^2 &"si" x >= 0, -x &"sinon")$
$display(1/2)$  $inline(1/2)$  $lr(] -oo thin";" thin 3 ])$
```

- `$x$` en ligne ; `$ x $` (espace après et avant les dollars) centré, numéroté si `math.equation(numbering: …)`.
- Lettres isolées = variables ; mots = symboles ou fonctions ; texte entre guillemets.
- Parenthèses autour d'un indice ou d'un exposant de plusieurs caractères : `x^(2n)`.
- Dans un appel en maths, `,` sépare des arguments et `;` des lignes (matrice) : protéger par `";"`.
- La virgule décimale : `$3","14$`. Le point-virgule d'un intervalle français : `$[0 thin; thin 1]$`.
