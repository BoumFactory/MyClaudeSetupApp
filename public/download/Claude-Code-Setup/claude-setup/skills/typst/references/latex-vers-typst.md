# De LaTeX à Typst : constructions courantes

Chaque ligne Typst a été compilée avec Typst 0.15.0. Pour les commandes du paquet bfcours (`\Definition`, `\EXO`, `\crep`, `\tcbtab`…), ce n'est pas ici : skill `bfcours-typst`, `chercher.py --latex <commande>`.

## Sommaire

1. Document et préambule
2. Texte
3. Structure et listes
4. Mise en page
5. Tableaux et figures
6. Maths
7. Programmation (macros, conditions, compteurs)
8. TikZ → cetz

## 1. Document et préambule

| LaTeX | Typst |
|---|---|
| `\documentclass{article}` + `\begin{document}` | rien : le fichier est le document |
| `\usepackage{x}` | `#import "@preview/x:0.1.0": *` ou `@local/…` |
| `\geometry{a4paper, margin=2cm}` | `#set page(paper: "a4", margin: 2cm)` |
| `\geometry{landscape}` | `#set page(flipped: true)` |
| `\pagestyle{…}`, `fancyhdr` | `#set page(header: […], footer: […], numbering: "1")` |
| `\usepackage[french]{babel}` | `#set text(lang: "fr")` |
| `\setmainfont{X}`, `\fontsize` | `#set text(font: "X", size: 11pt)` |
| `\parindent`, `\parskip` | `#set par(first-line-indent: 1em, spacing: 0.8em)` |
| `\input{f}` | `#include "f.typ"` (contenu) ou `#import "f.typ": *` (définitions) |
| `\newif\ifprof` + deux fichiers maîtres | un fichier, `sys.inputs` : `--input correction=false` |

## 2. Texte

| LaTeX | Typst |
|---|---|
| `\textbf{x}`, `\textit{x}`, `\emph{x}` | `*x*`, `_x_`, `#emph[x]` |
| `\underline{x}`, `\sout{x}` | `#underline[x]`, `#strike[x]` |
| `\texttt{x}` | `` `x` `` |
| `\textsc{x}` | `#smallcaps[x]` |
| `\textcolor{red}{x}`, `{\color{red} x}` | `#text(fill: red)[x]` |
| `\definecolor{c}{HTML}{C2410C}` | `#let c = rgb("#c2410c")` |
| `red!30`, `red!30!black` | `red.lighten(70%)`, `color.mix((red, 30%), (black, 70%))` |
| `\small`, `\large` | `#text(size: 9pt)[…]`, `#text(size: 1.2em)[…]` |
| `\textsuperscript{e}` | `#super[e]` |
| `~`, `\,` | `~`, `#h(0.17em)` ou le caractère U+202F |
| `\og x \fg{}` | `"x"` avec `lang: "fr"` → « x » |
| `--`, `---` | `--`, `---` |
| `\\` | `\` en fin de ligne, ou `#linebreak()` |
| `\footnote{x}` | `#footnote[x]` |
| `\href{url}{texte}`, `\url{u}` | `#link("url")[texte]`, `#link("u")` |
| `\label{x}` … `\ref{x}` | `<x>` … `@x` |
| `%` commentaire | `//` ou `/* … */` |
| `\$`, `\#`, `\_`, `\&` | `\$`, `\#`, `\_`, `&` (pas besoin) |

## 3. Structure et listes

| LaTeX | Typst |
|---|---|
| `\section{X}`, `\subsection{X}` | `= X`, `== X` |
| `\section*{X}` | `#heading(numbering: none)[X]` |
| numérotation I.1. | `#set heading(numbering: "I.1.")` |
| `\tableofcontents` | `#outline()` |
| `itemize` | `- a` (indentation de 2 espaces pour une sous-liste) |
| `enumerate` | `+ a` ; style : `#set enum(numbering: "a)")` |
| `enumerate[label=\arabic*.]` sur une liste | `#enum(numbering: "1.", [a], [b])` |
| `\item[$\bullet$]` | `#list(marker: [•], [a])` |
| `description` | `/ Terme: définition` |
| `\newpage`, `\clearpage` | `#pagebreak()` |

## 4. Mise en page

| LaTeX | Typst |
|---|---|
| `\vspace{1cm}`, `\hspace{1cm}` | `#v(1cm)`, `#h(1cm)` |
| `\hfill`, `\vfill` | `#h(1fr)`, `#v(1fr)` |
| `\medskip`, `\bigskip` | `#v(0.5em)`, `#v(1em)` |
| `\centering`, `center` | `#align(center)[…]` |
| `flushright` | `#align(right)[…]` |
| `minipage{0.5\linewidth}` | `#box(width: 50%)[…]` ou `#grid(columns: (1fr, 1fr), …)` |
| `multicols{2}` | `#columns(2)[… #colbreak() …]` |
| `\fbox{x}`, `\framebox` | `#box(stroke: 0.5pt, inset: 3pt)[x]` |
| `tcolorbox` simple | `#block(fill: …, stroke: …, inset: 6pt, radius: 3pt, width: 100%)[…]` |
| `\rule{…}`, `\hrule` | `#line(length: 100%)` |
| `\phantom{x}` | `#hide[x]` |
| `\raisebox{2pt}{x}` | `#move(dy: -2pt)[x]` |
| `\rotatebox{90}{x}` | `#rotate(90deg, reflow: true)[x]` |
| `\needspace{3cm}` | `#block(breakable: false)[…]` autour de ce qui doit rester ensemble |
| `1ex` | `0.5em` (pas d'unité `ex`) |
| `\linewidth`, `\textwidth` | `100%` |

## 5. Tableaux et figures

| LaTeX | Typst |
|---|---|
| `tabular{|c|c|}` | `#table(columns: 2, [a], [b], …)` (cellules lues ligne par ligne) |
| colonne `p{3cm}`, `X` | `columns: (3cm, 1fr)` |
| `\hline` ponctuel | `table.hline()` |
| `\multicolumn{2}{c}{x}` | `table.cell(colspan: 2)[x]` |
| `\multirow{2}{*}{x}` | `table.cell(rowspan: 2)[x]` |
| `\cellcolor{gray!20}` | `table.cell(fill: luma(230))[x]` ou `fill: (x, y) => …` |
| `\rowcolor` sur l'en-tête | `fill: (x, y) => if y == 0 { luma(230) }` |
| sans filets | `stroke: none` |
| `\includegraphics[width=5cm]{f}` | `#image("f.png", width: 5cm)` (PNG, JPG, SVG, PDF) |
| `figure` + `\caption` | `#figure(…, caption: […]) <etiquette>` |
| `wrapfig` | pas d'équivalent natif : `#grid(columns: (1fr, auto), …)` |

## 6. Maths

| LaTeX | Typst |
|---|---|
| `$x$`, `\[ x \]` | `$x$`, `$ x $` |
| `\frac{a}{b}`, `\dfrac`, `\tfrac` | `$a/b$` ou `$frac(a, b)$`, `$display(a/b)$`, `$inline(a/b)$` |
| `\sqrt{x}`, `\sqrt[3]{x}` | `$sqrt(x)$`, `$root(3, x)$` |
| `x^{2n}`, `x_{n+1}` | `$x^(2n)$`, `$x_(n+1)$` |
| `\overrightarrow{AB}`, `\vec u` | `$arrow(A B)$`, `$arrow(u)$` |
| `\begin{pmatrix} x \\ y \end{pmatrix}` | `$vec(x, y)$` |
| `\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}` | `$mat(1, 2; 3, 4)$` |
| `\mathbb{R}`, `\mathbb{R}_+^*` | `$RR$`, `$RR_+^*$` |
| `\mathcal{C}`, `\mathbf{u}`, `\mathrm{d}` | `$cal(C)$`, `$bold(u)$`, `$upright(d)$` |
| `\text{si}` | `$"si"$` |
| `\operatorname{pgcd}` | `$op("pgcd")$` |
| `\left( … \right)` | automatique ; forcé : `$lr(( … ))$` |
| `]-\infty ; 3]` | `$lr(] -oo thin";" thin 3 ])$` (sans `lr`, le `-` qui suit `]` devient un moins binaire espacé : « ] − ∞ ») |
| `\lVert u \rVert`, `\lvert x \rvert` | `$norm(arrow(u))$`, `$abs(x)$` |
| `\leq`, `\geq`, `\neq`, `\approx` | `$<=$`, `$>=$`, `$!=$`, `$approx$` |
| `\times`, `\cdot`, `\div`, `\pm` | `$times$`, `$dot$`, `$div$`, `$plus.minus$` |
| `\infty` | `$oo$` |
| `\in`, `\notin`, `\subset`, `\cup`, `\cap`, `\emptyset` | `$in$`, `$in.not$`, `$subset$`, `$union$`, `$inter$`, `$emptyset$` |
| `\Rightarrow`, `\Leftrightarrow`, `\to` | `$=>$`, `$<=>$`, `$->$` |
| `\forall`, `\exists` | `$forall$`, `$exists$` |
| `\ldots`, `\cdots` | `$dots.h$`, `$dots.c$` |
| `\quad`, `\,`, `\;` | `$quad$`, `$thin$`, `$med$` |
| `\lim_{x\to+\infty}` | `$lim_(x -> +oo)$` |
| `\sum_{k=1}^{n}`, `\int_0^1 f(x)\,dx` | `$sum_(k=1)^n$`, `$integral_0^1 f(x) dif x$` |
| `\binom{n}{k}` | `$binom(n, k)$` |
| `cases` | `$cases(x^2 &"si" x >= 0, -x &"sinon")$` |
| `align*` | `$ a &= b \ &= c $` (`\` change de ligne, `&` aligne) |
| `\overline{z}`, `\hat{x}`, `\widehat{ABC}` | `$overline(z)$`, `$hat(x)$`, `$hat(A B C)$` |
| `3{,}14` | `$3","14$` |
| `\num{1234.5}` (siunitx) | fonction de paquet (`num` de farfadet-maths), ou écrire `1 234,5` à la main |

## 7. Programmation

| LaTeX | Typst |
|---|---|
| `\newcommand{\R}{\mathbb{R}}` | `#let R = $RR$` |
| `\newcommand{\f}[2]{#1 + #2}` | `#let f(a, b) = [#a + #b]` |
| argument optionnel `[opt]` | argument nommé `opt: défaut` |
| `\newenvironment{boite}{…}{…}` | `#let boite(corps) = block(…)[#corps]`, appel `#boite[…]` |
| `\ifthenelse{…}{a}{b}`, `\ifx` | `#if cond [a] else [b]` |
| `\foreach \i in {1,...,5}` | `#for i in range(1, 6) […]` |
| `\newcounter`, `\stepcounter`, `\thecounter` | `#let c = counter("c")`, `#c.step()`, `#context c.display()` |
| `\setcounter{c}{0}` | `#c.update(0)` |
| `\def\total{…}` modifié plus loin | `state("total", 0)` + `.update(x => …)` + `context s.final()` |
| `\pgfmathsetmacro`, `\fpeval` | `calc.round(x, digits: 2)`, `calc.sqrt`, opérateurs |
| `\renewcommand` d'un style global | `#set …` ou `#show …` |

## 8. TikZ → cetz

Détails et exemple complet : `cetz.md`.

| TikZ | cetz (`import cetz.draw: *` dans `cetz.canvas({ … })`) |
|---|---|
| `\begin{tikzpicture}[scale=0.8]` | `#cetz.canvas(length: 0.8cm, { … })` |
| `\draw (0,0) -- (3,2);` | `line((0, 0), (3, 2))` |
| `\draw[->]` | `line(…, mark: (end: ">"))` ; `"stealth"` pour une pointe fine |
| `\draw[thick, blue, dashed]` | `stroke: (paint: blue, thickness: 1pt, dash: "dashed")` |
| `\draw (0,0) grid (5,4);` | `grid((0, 0), (5, 4), step: 1, stroke: 0.3pt + luma(180))` |
| `\draw (1,1) circle (0.5);` | `circle((1, 1), radius: 0.5)` |
| `\fill (A) circle (2pt);` | `circle(A, radius: 0.06, fill: black)` |
| `\node[above] at (A) {$A$};` | `content(A, [$A$], anchor: "south", padding: 3pt)` |
| `\coordinate (A) at (1,1);` | `let A = (1, 1)` ou `name: "A"` sur un élément |
| `($(A)!0.5!(B)$)` | `"v.mid"` sur une ligne nommée `v`, ou `(A, 50%, B)` (pourcentage obligatoire : `0.5` serait une distance) |
| `\draw (A) -- (B) -- (C) -- cycle;` | `line(A, B, C, close: true)` |
| `\draw (0,0) arc (0:90:1);` | `arc((0, 0), start: 0deg, stop: 90deg, radius: 1)` |
| `\draw[domain=-1:4, samples=30] plot (\x, {\x*\x/4});` | `line(..range(0, 31).map(i => { let x = -1 + i / 6; (x, x * x / 4) }))` |
| `\clip` | pas de clip simple : borner les données |
