// RECETTE : fiche d'exercices (revue d'un chapitre de 2de, 8 exercices, corrigés à la fin).
//
// Ce qu'elle montre :
//   - le modèle `modele("cours", type-document: […])` avec un libellé libre dans le bandeau ;
//   - les réglages d'exercices repris du LaTeX (`setrdexo`, `setrdcrep`, `rdifficulty`) ;
//   - `exo` avec titre, étiquette (`tags`), niveau et correction (`exocorrection`) ;
//   - les questions `tcbenumerate` : en colonnes (`raster-columns`), imbriquées, numérotation reprise (`depart`) ;
//   - les points en tête de question : `#itempoint(n)[Énoncé]` (boîtes masquées, comme dans le LaTeX) ;
//   - `multi-colonnes` avec des cases réglées par `tcbitem(…)` (largeur, alignement) ;
//   - `vect`, `coordonnees`, `acc`, `encadrer` ; la virgule décimale `-1","5` ;
//   - quatre figures TikZ redessinées en cetz, avec leurs styles en fonctions ;
//   - la partie « Solutions » en version professeur seulement (`ifcorrection` + `rdexocorrection`).
//
// Source : 1. Cours/2nde/Sequence-Vecteur_par_coordonnees-P1/Fiche_1_Revue/ (Fiche_1_Revue.tex, enonce.tex,
// Exercice/*.tex, enonce_figures.tex), convertie fidèlement, sans rien retirer.
//
// Compiler une copie placée dans le dossier de travail (pas dans le skill) ; PDF prof et élève, images :
//   python "<skill>/scripts/compiler.py" "dossier/fiche-exercices.typ" --png
//
// Écarts avec le LaTeX : les étiquettes (codes de compétence) s'affichent tournées dans la marge comme
// avec l'`overlay` TikZ du LaTeX, en version professeur seulement (`display-tags: "correction"`) ; le
// préfixe « Exercice n : » ajouté aux solutions par `correction style` n'est pas repris.
// Deux réglages de mise en page faits après lecture du PNG : `needspace` avant un exercice dont le bandeau
// restait seul en bas de page, et `box(…)` autour des coordonnées qu'une colonne étroite coupait en deux.

#import "@preview/farfadet:0.2.0": *
#import "@preview/cetz:0.5.3"

// Identité de l'auteur, réglée une fois pour les bandeaux et le pied de page (dans une façade,
// ces lignes disparaissent du document : voir references/facade.md).
#setbfmodele(pour: "identite", cycle: [Lycée], etablissement: [du Parc])

#show: modele(
  "cours",
  niveau: "2nde",
  theme: [Vecteurs du plan (1)],
  type-document: [Fiche 1 -- Revue du chapitre :],   // libellé libre devant le thème
  marges: (right: 1cm),                              // geometry : left = right = 1 cm
)

// \setrdexo{display exotitle, exo header=tcolorbox, skin=bouyachakka, display score=false, display level, …}
#setrdexo(display-exotitle: true, exo-header: "tcolorbox", skin: "bouyachakka", display-score: false,
  display-level: true, display-tags: "correction")
// \setrdcrep{seyes, correction color=defi, correction font=\large\bfseries} (correction=… : par --input)
#setrdcrep(seyes: true, correction-color: "defi", correction-font: "\large\bfseries")
// \displayitempointsfalse : les points comptent, leurs boîtes ne s'affichent pas
#displayitempoints(false)

// ---------------------------------------------------------------------------
// Figures (enonce_figures.tex), redessinées en cetz
// ---------------------------------------------------------------------------
#let quadrillage = 0.5pt + luma(198)     // gray!45
#let bleu = rgb(0, 0, 179)               // blue!70!black

// \placerpoint : une croix et le nom du point
#let croix(p, nom, ancre) = {
  import cetz.draw: *
  line((rel: (-0.13, -0.13), to: p), (rel: (0.26, 0.26)), stroke: 0.7pt)
  line((rel: (-0.13, 0.13), to: p), (rel: (0.26, -0.26)), stroke: 0.7pt)
  content(p, nom, anchor: ancre, padding: 3pt)
}
// vecteurfig : flèche épaisse, nom au milieu
#let fleche(a, b, nom, ancre: "south-east", couleur: bleu) = {
  import cetz.draw: *
  line(a, b, stroke: 1.2pt + couleur, mark: (end: "stealth", fill: couleur), name: "v")
  content("v.mid", nom, anchor: ancre, padding: 2pt)
}
// Axes, graduations 1 et origine
#let axes(xmin, xmax, ymin, ymax, couleur: black) = {
  import cetz.draw: *
  line((xmin - 0.2, 0), (xmax + 0.4, 0), mark: (end: "stealth", fill: couleur), stroke: 0.8pt + couleur)
  line((0, ymin - 0.2), (0, ymax + 0.4), mark: (end: "stealth", fill: couleur), stroke: 0.8pt + couleur)
  content((0, 0), text(7pt)[$O$], anchor: "north-east", padding: 1.5pt)
}

// Lecture de coordonnées : trois repères ; `pas` : pas du quadrillage (x, y)
#let fig-lecture(numero, pas, points, place-numero) = cetz.canvas(length: 0.48cm, {
  import cetz.draw: *
  grid((-3, -3), (3, 3), step: pas, stroke: quadrillage)
  axes(-3, 3, -3, 3)
  line((1, 0.12), (1, -0.12))
  content((1, -0.12), text(7pt)[$1$], anchor: "north", padding: 1pt)
  line((0.12, 1), (-0.12, 1))
  content((-0.12, 1), text(7pt)[$1$], anchor: "east", padding: 1pt)
  for (p, nom, ancre) in points { croix(p, nom, ancre) }
  circle(place-numero, radius: 0.33, stroke: 0.5pt + blue)
  content(place-numero, text(8pt, fill: blue)[#numero])
})

#let fig-vocabulaire = cetz.canvas(length: 0.55cm, {
  import cetz.draw: *
  grid((0, 0), (14, 7), step: 1, stroke: quadrillage)
  fleche((1, 4), (3, 5), $vect(u)$)
  fleche((4, 1), (6, 2), $vect(v)$)
  fleche((7, 6), (5, 5), $vect(w)$)
  fleche((1, 1), (1, 3), $vect(a)$, ancre: "east")
  fleche((11, 3), (11, 1), $vect(b)$, ancre: "west")
  fleche((9, 4), (13, 6), $vect(s)$)
  fleche((7, 1), (8, 3), $vect(r)$, ancre: "west")
})

#let fig-parallelogramme = cetz.canvas(length: 0.85cm, {
  import cetz.draw: *
  let (A, B, C, D, O) = ((0, 0), (4, 0), (5.2, 2.2), (1.2, 2.2), (2.6, 1.1))
  line(A, B, C, D, close: true, stroke: (paint: blue, thickness: 0.8pt, join: "round"))
  line(A, C, stroke: (dash: "dashed", thickness: 0.4pt))
  line(B, D, stroke: (dash: "dashed", thickness: 0.4pt))
  circle(O, radius: 0.06, fill: black)
  content(A, $A$, anchor: "north-east", padding: 2pt)
  content(B, $B$, anchor: "north-west", padding: 2pt)
  content(C, $C$, anchor: "south-west", padding: 2pt)
  content(D, $D$, anchor: "south-east", padding: 2pt)
  content(O, $O$, anchor: "north", padding: 5pt)
})

#let fig-vecteurs-repere = cetz.canvas(length: 0.5cm, {
  import cetz.draw: *
  let axe = luma(40%)                              // gray!60!black
  grid((-5, -4), (6, 5), step: 1, stroke: quadrillage)
  axes(-5, 6, -4, 5, couleur: axe)
  // \baseij : vecteurs i et j en rouge
  line((0, 0), (1, 0), stroke: 1.4pt + red, mark: (end: "stealth", fill: red))
  content((0.55, 0), text(fill: red)[$vect(i)$], anchor: "north", padding: 2pt)
  line((0, 0), (0, 1), stroke: 1.4pt + red, mark: (end: "stealth", fill: red))
  content((0, 0.55), text(fill: red)[$vect(j)$], anchor: "east", padding: 2pt)
  fleche((1, 1), (4, 3), $vect(u)$)
  fleche((0, 0), (-2, 3), $vect(v)$, ancre: "east")
  content((-2, 3), $V$, anchor: "south-east", padding: 1pt)
  fleche((1, -1), (3, -2), $vect(w)$, ancre: "north-east")
  fleche((-4, -1), (-4, -3), $vect(a)$, ancre: "east")
  fleche((-4, 4), (-1, 4), $vect(b)$, ancre: "south")
  fleche((-3, -2), (-1, -3), $vect(c)$, ancre: "north-east")
  fleche((6, -1), (3, -3), $vect(d)$, ancre: "south-west")
})

// ---------------------------------------------------------------------------
// Exercices (enonce.tex)
// ---------------------------------------------------------------------------

// LaTeX : Exercice/lire_coordonnees_points.tex
#rdifficulty(1)
#exo(tags: "2GT-GEO-002")[Lire les coordonnées de points][
  #itempoint(9)[Dans chacun des repères orthonormés ci-dessous, #acc[lire] les coordonnées des points $A$, $B$ et $C$.]

  #multi-colonnes(3)[
    #tcbitem(halign: "center")[#fig-lecture(1, 1, (((-2, 1), $A$, "south-west"), ((1, 2), $B$, "south-west"), ((0, -2), $C$, "south-west")), (-2.5, 2.5))]
    #tcbitem(halign: "center")[#fig-lecture(2, (0.5, 1), (((-1.5, 2), $A$, "south-west"), ((0.5, -2), $B$, "south-west"), ((2, 1), $C$, "south-west")), (-2.5, 2.5))]
    #tcbitem(halign: "center")[#fig-lecture(3, 0.5, (((-2.5, 1.5), $A$, "south-west"), ((1.5, -1), $B$, "south-west"), ((-0.5, -2.5), $C$, "south-east")), (2.5, 2.5))]
  ]
  #exocorrection
  #multi-colonnes(3)[
    - #acc[Figure 1] (un carreau par unité)
      #tcbenumerate[
        + $coordonnees(-2, 1, nom: A)$
        + $coordonnees(1, 2, nom: B)$
        + $coordonnees(0, -2, nom: C)$
      ]
    - #acc[Figure 2] (deux carreaux par unité en abscisse)
      #tcbenumerate[
        + $coordonnees(-1","5, 2, nom: A)$
        + $coordonnees(0","5, -2, nom: B)$
        + $coordonnees(2, 1, nom: C)$
      ]
    - #acc[Figure 3] (deux carreaux par unité sur les deux axes)
      #tcbenumerate[
        + $coordonnees(-2","5, 1","5, nom: A)$
        + $coordonnees(1","5, -1, nom: B)$
        + $coordonnees(-0","5, -2","5, nom: C)$
      ]
  ]
]

// LaTeX : Exercice/vocabulaire_quadrillage.tex
#rdifficulty(1)
#exo(tags: "2GT-GEO-009")[Vocabulaire des vecteurs sur un quadrillage][
  #multi-colonnes(2)[
    #tcbitem(valign: "center")[
      À l'aide du quadrillage ci-contre :
      #tcbenumerate[
        + #itempoint(1)[#acc[citer] deux vecteurs égaux ;]
        + #itempoint(1)[#acc[citer] un vecteur opposé au vecteur $vect(u)$ ;]
        + #itempoint(1)[#acc[citer] un vecteur de même direction et de même sens que $vect(u)$, mais de longueur différente ;]
        + #itempoint(1)[#acc[citer] un vecteur de même longueur que $vect(u)$, mais de direction différente.]
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-vocabulaire]
  ]
  #exocorrection
  #tcbenumerate[
    + $vect(u) = vect(v)$ : ces deux vecteurs ont la même direction, le même sens et la même longueur (2 carreaux vers la droite et 1 carreau vers le haut).
    + $vect(w)$ : même direction et même longueur que $vect(u)$, mais sens contraire. On écrit $vect(w) = -vect(u)$.
    + $vect(s)$ : même direction et même sens que $vect(u)$, mais il est deux fois plus long (4 carreaux vers la droite et 2 vers le haut).
    + $vect(r)$ : 1 carreau vers la droite et 2 vers le haut. D'après le théorème de Pythagore, sa longueur vaut $sqrt(1^2 + 2^2) = sqrt(5)$, comme celle de $vect(u)$ qui vaut $sqrt(2^2 + 1^2) = sqrt(5)$ ; mais les directions sont différentes.
  ]
]

// LaTeX : Exercice/parallelogramme_egalites.tex
#rdifficulty(1)
#exo(tags: "2GT-GEO-009")[Parallélogramme et égalités de vecteurs][
  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[
      $A B C D$ est un parallélogramme de centre $O$. #acc[Compléter] avec des points de la figure.
      #tcbenumerate(raster-columns: 2)[
        + #itempoint(1)[$vect(A B) = vect(D ...)$]
        + #itempoint(1)[$vect(A D) = vect(... C)$]
        + #itempoint(1)[$vect(A O) = vect(O ...)$]
        + #itempoint(1)[$vect(O D) = vect(... O)$]
        + #itempoint(1)[$vect(C B) = vect(... ...)$]
        + #itempoint(1)[$vect(B A) = -vect(D ...)$]
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-parallelogramme]
  ]

  #acc[Vrai ou faux] ? #acc[Justifier].
  #tcbenumerate(raster-columns: 2, depart: 7)[
    + #itempoint(1)[Si $vect(M N) = vect(P Q)$, alors $M N P Q$ est un parallélogramme.]
    + #itempoint(1)[Si $vect(E F) = vect(H G)$, alors $E F G H$ est un parallélogramme, éventuellement aplati.]
  ]
  #exocorrection
  #tcbenumerate(raster-columns: 3)[
    + $vect(A B) = vect(D C)$
    + $vect(A D) = vect(B C)$
    + $vect(A O) = vect(O C)$
    + $vect(O D) = vect(B O)$
    + $vect(C B) = vect(D A)$
    + $vect(B A) = -vect(D C)$
  ]

  Les diagonales d'un parallélogramme se coupent en leur milieu : $O$ est le milieu de $[A C]$ et de $[B D]$, d'où les égalités 3 et 4.

  #tcbenumerate(depart: 7)[
    + #acc[Faux] : $vect(M N) = vect(P Q)$ signifie que $M N Q P$ est un parallélogramme. Attention à l'ordre des sommets !
    + #acc[Vrai] : c'est la propriété du parallélogramme, $vect(E F) = vect(H G)$ équivaut à $E F G H$ parallélogramme (éventuellement aplati).
  ]
]

// LaTeX : Exercice/lire_coordonnees_vecteurs.tex
#needspace(8cm)   // \Needspace* du LaTeX : le bandeau ne reste pas seul en bas de page
#rdifficulty(1)
#exo(tags: "2GT-GEO-018")[Lire les coordonnées de vecteurs][
  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[
      Le plan est muni du repère orthonormé $(O thin; vect(i), vect(j))$ ci-contre.
      #tcbenumerate[
        + #itempoint(7)[#acc[Lire] les coordonnées des vecteurs $vect(u)$, $vect(v)$, $vect(w)$, $vect(a)$, $vect(b)$, $vect(c)$ et $vect(d)$.]
        + #itempoint(2)[#acc[Citer] deux vecteurs égaux, puis deux vecteurs opposés.]
        + #itempoint(1)[Le représentant de $vect(v)$ tracé a pour origine $O$ et pour extrémité $V$ : c'est le #acc[vecteur position] du point $V$. #acc[Donner] les coordonnées de $V$.]
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-vecteurs-repere]
  ]
  #exocorrection
  #tcbenumerate[
    + On compte le déplacement horizontal (abscisse) puis vertical (ordonnée) de l'origine vers l'extrémité :
      #multi-colonnes(4)[
        - $vect(u) coordonnees(3, 2)$
        - $vect(v) coordonnees(-2, 3)$
        - $vect(w) coordonnees(2, -1)$
        - $vect(a) coordonnees(0, -2)$
        - $vect(b) coordonnees(3, 0)$
        - $vect(c) coordonnees(2, -1)$
        - $vect(d) coordonnees(-3, -2)$
      ]
    + $vect(w) = vect(c)$ (mêmes coordonnées) ; $vect(u)$ et $vect(d)$ sont opposés (coordonnées opposées) : $vect(d) = -vect(u)$.
    + Le vecteur position $vect(O V)$ a les mêmes coordonnées que le point $V$ : #encadrer(couleur: "defi")[$coordonnees(-2, 3, nom: V)$]
  ]
]

// LaTeX : Exercice/parallelogramme_coordonnees.tex
#rdifficulty(1.5)
#exo(tags: "2GT-GEO-014")[Reconnaître un parallélogramme][
  Le plan est muni d'un repère orthonormé.

  #tcbenumerate[
    + On considère les points $coordonnees(-2, 1, nom: A)$, $coordonnees(2, 3, nom: B)$, $coordonnees(3, -1, nom: C)$ et $coordonnees(7, 1, nom: D)$.
      #tcbenumerate(raster-columns: 2)[
        + #itempoint(2)[#acc[Calculer] les coordonnées de $vect(A B)$ et de $vect(C D)$.]
        + #itempoint(1)[#acc[En déduire] la nature du quadrilatère $A B D C$.]
      ]
  ]
  #tcbenumerate(depart: 2)[
    + #itempoint(3)[#acc[Prouver] que $R S T U$ est un parallélogramme, avec $coordonnees(3, 5, nom: R)$, $coordonnees(2, -1, nom: S)$, $coordonnees(-2, -4, nom: T)$ et $coordonnees(-1, 2, nom: U)$.]
  ]
  #tcbenumerate(depart: 3)[
    + #itempoint(3)[Dans chaque cas, #acc[indiquer] si $E F G H$ est un parallélogramme.]
      #tcbenumerate[
        + $coordonnees(2, -1, nom: E)$, $coordonnees(8, -1, nom: F)$, $coordonnees(10, 3, nom: G)$ et $coordonnees(4, 3, nom: H)$
        + $coordonnees(1, -1, nom: E)$, $coordonnees(0, 2, nom: F)$, $coordonnees(8, -3, nom: G)$ et $coordonnees(7, 0, nom: H)$
        + $coordonnees(3, -4, nom: E)$, $coordonnees(14, -4, nom: F)$, $coordonnees(10, 4, nom: G)$ et $coordonnees(-1, 4, nom: H)$
      ]
  ]
  #exocorrection
  #tcbenumerate[
    + Premier quadrilatère :
      #tcbenumerate[
        + $vect(A B) coordonnees(2 - (-2), 3 - 1)$ donc $vect(A B) coordonnees(4, 2)$ ; $vect(C D) coordonnees(7 - 3, 1 - (-1))$ donc $vect(C D) coordonnees(4, 2)$.
        + $vect(A B) = vect(C D)$ donc #acc[$A B D C$ est un parallélogramme]. Attention : c'est $A B D C$ et non $A B C D$.
      ]
  ]
  #tcbenumerate(depart: 2)[
    + $R S T U$ est un parallélogramme si et seulement si $vect(R S) = vect(U T)$.

      $vect(R S) coordonnees(2 - 3, -1 - 5)$ donc $vect(R S) coordonnees(-1, -6)$ ; $vect(U T) coordonnees(-2 - (-1), -4 - 2)$ donc $vect(U T) coordonnees(-1, -6)$.

      $vect(R S) = vect(U T)$ donc #encadrer(couleur: "defi")[$R S T U$ est un parallélogramme]
  ]
  #tcbenumerate(depart: 3)[
    + On compare $vect(E F)$ et $vect(H G)$ :
      #tcbenumerate[
        + $vect(E F) coordonnees(6, 0)$ et $vect(H G) coordonnees(6, 0)$ : #acc[oui], $E F G H$ est un parallélogramme.
        + $vect(E F) coordonnees(-1, 3)$ et $vect(H G) coordonnees(1, -3)$ : ces vecteurs sont opposés, #acc[non]. En revanche $vect(E F) = vect(G H)$, donc $E F H G$ est un parallélogramme.
        + $vect(E F) coordonnees(11, 0)$ et $vect(H G) coordonnees(11, 0)$ : #acc[oui], $E F G H$ est un parallélogramme.
      ]
  ]
]

// LaTeX : Exercice/quatrieme_sommet.tex
#rdifficulty(2)
#exo(tags: "2GT-GEO-014")[Quatrième sommet d'un parallélogramme][
  Dans un repère orthonormé, on considère les points $coordonnees(2, 5, nom: A)$, $coordonnees(-3, 8, nom: B)$ et $coordonnees(1, -3, nom: C)$. On veut calculer les coordonnées du point $D$ tel que $A B C D$ soit un parallélogramme.

  #tcbenumerate[
    + #itempoint(1)[#acc[Compléter] : $A B C D$ est un parallélogramme si et seulement si $vect(A B) = vect(... ...)$.]
    + #itempoint(1)[#acc[Calculer] les coordonnées de $vect(A B)$.]
    + #itempoint(1)[En notant $x_D$ et $y_D$ les coordonnées de $D$, #acc[exprimer] les coordonnées de $vect(D C)$.]
    + #itempoint(2)[#acc[En déduire] les coordonnées de $D$.]
  ]
  #exocorrection
  #tcbenumerate[
    + $A B C D$ est un parallélogramme si et seulement si #acc[$vect(A B) = vect(D C)$] (attention à l'ordre des points).
    + $vect(A B) coordonnees(-3 - 2, 8 - 5)$ donc #acc[$vect(A B) coordonnees(-5, 3)$].
    + #acc[$vect(D C) coordonnees(1 - x_D, -3 - y_D)$]
  ]
  #tcbenumerate(depart: 4)[
    + Ces deux vecteurs sont égaux, donc ils ont les mêmes coordonnées :

      $1 - x_D = -5$ donc $x_D = 6$ ; $-3 - y_D = 3$ donc $y_D = -6$.

      #encadrer(couleur: "defi")[$coordonnees(6, -6, nom: D)$]
  ]
]

// LaTeX : Exercice/coordonnees_inconnues.tex
#rdifficulty(1.5)
#exo(tags: "2GT-GEO-014")[Égalité de vecteurs et coordonnées inconnues][
  #tcbenumerate[
    + #itempoint(5)[Dans chaque cas, $vect(u)$ et $vect(v)$ sont deux représentants d'un même vecteur. #acc[Calculer] les valeurs de $x$ et de $y$.]
      #tcbenumerate(raster-columns: 3)[
        + $vect(u) coordonnees(-3, 5)$ et $vect(v) coordonnees(x - 6, y + 9)$
        + $vect(u) coordonnees(11, -13)$ et $vect(v) coordonnees(2 x + 5, 3 - 2 y)$
        + $vect(u) coordonnees(-3 x - 2, 5)$ et $vect(v) coordonnees(5 x - 10, 5)$
      ]
  ]
  #exocorrection
  Deux vecteurs sont égaux #acc[si et seulement si] ils ont les mêmes coordonnées.

  #tcbenumerate[
    + Résolutions :
      #tcbenumerate[
        + $x - 6 = -3$ donc $x = 3$ ; $y + 9 = 5$ donc $y = -4$.
        + $2 x + 5 = 11$ donc $2 x = 6$ et $x = 3$ ; $3 - 2 y = -13$ donc $-2 y = -16$ et $y = 8$.
        + $-3 x - 2 = 5 x - 10$ donc $-8 x = -8$ et $x = 1$. Les ordonnées sont égales à $5$ quel que soit le cas : aucune inconnue $y$ à déterminer.
      ]
  ]
]

// LaTeX : Exercice/norme_distance_milieu.tex
#rdifficulty(1)
#exo(tags: "2GT-GEO-020")[Norme - distance et milieu][
  Le plan est muni d'un repère orthonormé d'unité 1~cm.

  #tcbenumerate[
    + #itempoint(3)[#acc[Calculer] la norme de chacun des vecteurs suivants.]
      #tcbenumerate(raster-columns: 3)[
        + $vect(u) coordonnees(3, 4)$
        + $vect(v) coordonnees(-5, 12)$
        + $vect(w) coordonnees(1, -2)$
      ]
    + #itempoint(2)[Parmi les vecteurs $vect(a) coordonnees(4, -3)$, $vect(b) coordonnees(-3, -4)$ et $vect(c) coordonnees(1, 6)$, #acc[lesquels] ont la même norme que $vect(u)$ ? Sont-ils égaux à $vect(u)$ ?]
    + #itempoint(2)[On donne $coordonnees(-2, 5, nom: A)$ et $coordonnees(3, 4, nom: B)$. #acc[Calculer] la distance $A B$ : valeur exacte, puis #acc[arrondi au millimètre].]
    + #itempoint(1)[On donne $coordonnees(-2","6, 4","7, nom: E)$ et $coordonnees(6","3, -5","9, nom: F)$. #acc[Calculer] les coordonnées du milieu $K$ du segment $[E F]$.]
  ]
  #exocorrection
  #tcbenumerate[
    + Pour $vect(u) coordonnees(x, y)$ dans un repère orthonormé : $norm(vect(u)) = sqrt(x^2 + y^2)$.
      #multi-colonnes(3)[
        - $norm(vect(u)) = sqrt(9 + 16) = sqrt(25) = 5$
        - $norm(vect(v)) = sqrt(25 + 144) = sqrt(169) = 13$
        - $norm(vect(w)) = sqrt(1 + 4) = sqrt(5)$
      ]
  ]
  #tcbenumerate(depart: 2)[
    + $norm(vect(a)) = sqrt(16 + 9) = 5$, $norm(vect(b)) = sqrt(9 + 16) = 5$ et $norm(vect(c)) = sqrt(1 + 36) = sqrt(37)$.

      $vect(a)$ et $vect(b)$ ont la même norme que $vect(u)$, mais #acc[aucun n'est égal à $vect(u)$] : leurs coordonnées sont différentes (et $vect(b) = -vect(u)$).
  ]
  #tcbenumerate(depart: 3)[
    + $A B = sqrt((x_B - x_A)^2 + (y_B - y_A)^2) = sqrt((3 - (-2))^2 + (4 - 5)^2) = sqrt(25 + 1) = sqrt(26)$.

      #encadrer(couleur: "defi")[$A B = sqrt(26) approx 5","1$~cm]
  ]
  #tcbenumerate(depart: 4)[
    + $x_K = display((x_E + x_F)/2) = display((-2","6 + 6","3)/2) = 1","85$ et $y_K = display((y_E + y_F)/2) = display((4","7 + (-5","9))/2) = -0","6$.

      #encadrer(couleur: "defi")[$coordonnees(1","85, -0","6, nom: K)$]
  ]
]

// ---------------------------------------------------------------------------
// Solutions : version professeur seulement (Fiche_1_Revue_ELEVE.tex n'a pas cette partie)
// ---------------------------------------------------------------------------
#ifcorrection[
  #pagebreak()
  #counter(page).update(1)
  #chapitre(niveau: "2nde", theme: [Vecteurs du plan (1)], type: [Solutions :])
  #setrdcrep(correction-color: blue, correction-font: "\large")
  #rdexocorrection(0)
]
