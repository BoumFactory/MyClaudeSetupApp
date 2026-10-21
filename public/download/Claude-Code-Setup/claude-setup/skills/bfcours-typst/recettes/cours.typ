// RECETTE : cours complet (2de, « Vecteurs du plan (1) »), sections 1 à 4.3 du cours d'origine.
//
// Ce qu'elle montre :
//   - le modèle de cours : bandeau (niveau, thème, zone de droite), sommaire, page des compétences
//     (`tableaucompetence` + `competence`) et index du vocabulaire (`printvocindex`) ;
//   - tous les environnements du cours : `definition`, `propriete`, `remarque`, `notation`, `demonstration`,
//     `methode`, `exemple`, avec leur titre entre les premiers crochets ;
//   - le vocabulaire en marge de l'index : `voc` ; la mise en valeur : `acc`, `encadrer`, `frquote` ;
//   - texte et figure côte à côte DANS l'environnement : `multi-colonnes(n)[ #tcbitem(raster-multicolumn: …)[…] … ]` ;
//   - les zones de réponse du cours à trous : `crep` (réponse en couleur `prop` chez le professeur, lignes Seyès
//     vides chez l'élève), y compris dans une `demonstration` et un `exemple` ;
//   - deux exercices `exo` au fil du cours et leurs corrigés regroupés à la fin (`ifcorrection` + `rdexocorrection`) ;
//   - des macros locales du cours (`\vrep`, `\baseij`) en `#let` ;
//   - quinze figures TikZ redessinées en cetz, dont une qui change selon la version (`context` + `ifcorrection()`).
//
// Source : 1. Cours/2nde/Sequence-Vecteur_par_coordonnees-P1/Cours/ (Cours.tex, enonce.tex, commands_def.tex,
// enonce_figures.tex et les fichiers des dossiers Definition/, Propriete/…). Raccourci : le cours d'origine
// continue (4.2 fin, 4.4 et section 5 : norme, distance, milieu) ; ces parties n'apportent aucun environnement
// de plus. Les blocs repris sont convertis fidèlement ; chaque bloc commence par le nom de son fichier LaTeX.
//
// Compiler une copie placée dans le dossier de travail (pas dans le skill) ; PDF prof et élève, images :
//   python "<skill>/scripts/compiler.py" "dossier/cours.typ" --png
//
// Écarts avec le LaTeX : un seul `\newpage` de calage est repris (avant 3.3), les `\Needspace*` non ;
// deux `crep` sont en cadre gris au lieu de lignes Seyès et une `multi-colonnes` de démonstration devient
// des paragraphes (défauts de farfadet-crep, commentés sur place) ; la `demonstration`
// est en cadre net (`craie: false`) comme dans le PDF LaTeX ; le point marqué (style TikZ `point`) est
// une croix ×.

#import "@preview/farfadet:0.2.0": *
#import "@preview/cetz:0.5.3"

// Identité de l'auteur, réglée une fois pour les bandeaux et le pied de page (dans une façade,
// ces lignes disparaissent du document : voir references/facade.md).
#setbfmodele(pour: "identite", cycle: [Lycée], etablissement: [du Parc])

#show: modele(
  "cours",
  niveau: "2nde",
  theme: [Vecteurs du plan (1)],
  type-document: "cours",
  zone-droite: [2026-2027],
  marges: (right: 1cm),
)

#setrdexo(display-exotitle: true, exo-header: "tcolorbox", skin: "bouyachakka", display-score: false,
  display-level: true, display-tags: "correction")
#setrdcrep(seyes: true, correction-color: "prop", correction-font: "\large")
#setbfenvironments(pour: "Demonstration", craie: false)

// Macros de commands_def.tex
#let vrep = $(O thin; vect(i) thin; vect(j))$
#let baseij = $(vect(i) thin; vect(j))$

// ---------------------------------------------------------------------------
// Figures (enonce_figures.tex) en cetz. Styles TikZ → fonctions.
// ---------------------------------------------------------------------------
#let c1 = blue                        // couleur1
#let c2 = red                         // couleur2
#let c3 = rgb(0, 140, 0)              // couleur3
#let gris-q = 0.5pt + luma(198)       // quadrillage : gray!45

// Quadrillage aux abscisses et ordonnées ENTIÈRES comprises dans le cadre, comme `grid` de TikZ
// (le `grid` de cetz part du premier coin, qui peut être une demi-unité).
#let quad(x0, x1, y0, y1) = {
  import cetz.draw: *
  for x in range(int(calc.ceil(x0)), int(calc.floor(x1)) + 1) { line((x, y0), (x, y1), stroke: gris-q) }
  for y in range(int(calc.ceil(y0)), int(calc.floor(y1)) + 1) { line((x0, y), (x1, y), stroke: gris-q) }
}
#let axe(a, b) = cetz.draw.line(a, b, stroke: 0.8pt, mark: (end: "stealth", fill: black))
#let pt(p, couleur: black) = cetz.draw.content(p, text(9pt, fill: couleur)[$times$])   // style `point`
#let lbl(p, corps, ancre, pad: 2.5pt) = cetz.draw.content(p, corps, anchor: ancre, padding: pad)
#let trace-vect(a, b, couleur, ep: 1.4pt) = cetz.draw.line(a, b, stroke: ep + couleur, mark: (end: "stealth", fill: couleur))
#let angle-droit(t) = cetz.draw.line((t, 0), (t, t), (0, t), stroke: 0.5pt)
// Ancres TikZ → cetz : above = "south", below = "north", left = "east", right = "west",
// above left = "south-east", above right = "south-west", below left = "north-east", below right = "north-west".

#let fig-repa = cetz.canvas(length: 0.75cm, {
  import cetz.draw: *
  quad(-1, 5, -1, 4)
  axe((-1, 0), (5.4, 0)); axe((0, -1), (0, 4.4))
  angle-droit(0.25)
  line((3, 0), (3, 2), (0, 2), stroke: (paint: c1, thickness: 0.8pt, dash: "dashed"))
  lbl((3, 0), text(fill: c1)[$x$], "north"); lbl((0, 2), text(fill: c1)[$y$], "east")
  pt((1, 0)); pt((0, 1))
  lbl((0, 0), $O$, "north-east"); lbl((1, 0), $I$, "north"); lbl((0, 1), $J$, "east")
  pt((3, 2), couleur: c1); lbl((3, 2), text(fill: c1)[$M(x thin; y)$], "south-west")
})

#let fig-transb = cetz.canvas(length: 0.6cm, {
  import cetz.draw: *
  let fond = blue.lighten(92%)
  line((0, 0), (2, 0), (0, 3), close: true, fill: fond, stroke: 0.8pt)
  line((4, 2), (6, 2), (4, 5), close: true, fill: fond, stroke: 0.8pt)
  for p in ((0, 0), (2, 0), (0, 3)) {
    line(p, (p.at(0) + 4, p.at(1) + 2), stroke: (paint: c2, dash: "dashed"), mark: (end: "stealth", fill: c2))
  }
  lbl((0, 0), $A$, "north-east"); lbl((2, 0), $B$, "north-west"); lbl((0, 3), $C$, "east")
  lbl((4, 2), $A'$, "south-east"); lbl((6, 2), $B'$, "west"); lbl((4, 5), $C'$, "south")
})

#let fig-veca = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  line((-1, -0.5), (5, 2.5), stroke: (paint: gray, dash: "dashed"))
  lbl((5, 2.5), text(size: 9pt, fill: gray.darken(30%))[direction : la droite $(A B)$], "south-east")
  trace-vect((0, 0), (4, 2), c1)
  lbl((2, 1), text(fill: c1)[$vect(A B)$], "north-west")
  pt((0, 0)); pt((4, 2))
  lbl((0, 0), [$A$ #text(7pt)[(origine)]], "south-east")
  lbl((4, 2), [$B$ #text(7pt)[(extrémité)]], "north-west")
})

#let fig-posa = cetz.canvas(length: 0.7cm, {
  import cetz.draw: *
  axe((-0.5, 0), (6.5, 0)); axe((0, -0.5), (0, 4))
  lbl((0, 0), $O$, "north-east")
  trace-vect((0, 0), (2, 3), c1, ep: 1.3pt); pt((2, 3)); lbl((2, 3), $M$, "south")
  lbl((0.9, 1.9), align(right, text(9pt, fill: c1)[position \ de $M$]), "east")
  trace-vect((3, 0.8), (5.8, 2.6), c2, ep: 1.3pt)
  pt((3, 0.8)); lbl((3, 0.8), $A$, "north"); pt((5.8, 2.6)); lbl((5.8, 2.6), $B$, "south")
  lbl((4.6, 1.1), text(9pt, fill: c2)[déplacement \ de $A$ à $B$], "west")
})

#let fig-repra = cetz.canvas(length: 0.6cm, {
  import cetz.draw: *
  quad(0.5, 8.5, 2.5, 6.5)
  for (a, b, n, m) in (((1, 3), (4, 4), $A$, $B$), ((2, 5), (5, 6), $C$, $D$), ((5, 3), (8, 4), $E$, $F$)) {
    trace-vect(a, b, c2, ep: 1.3pt); pt(a); pt(b)
    lbl(a, n, "north-east"); lbl(b, m, "south-west")
  }
  for p in ((2.3, 4), (3.3, 6), (6.3, 4)) { lbl(p, text(fill: c2)[$vect(u)$], "center", pad: 0pt) }
})

#let fig-oppa = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  trace-vect((0, 0), (4, 0), c1, ep: 1.3pt)
  trace-vect((4, 0.4), (0, 0.4), c2, ep: 1.3pt)
  pt((0, 0)); lbl((0, 0.2), $A$, "east"); pt((4, 0)); lbl((4, 0.2), $B$, "west")
  lbl((2, 0), text(fill: c1)[$vect(A B) = vect(u)$], "north")
  lbl((2, 0.4), text(fill: c2)[$vect(B A) = -vect(u)$], "south")
})

// Parallélogramme : sommets, côtés pleins, deux vecteurs rouges
#let parallelogramme(s1, s2, s3, s4, n1, n2, v1, v2, ancres, diagonales: false) = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  line(s1, s2, s3, s4, close: true, fill: blue.lighten(94%), stroke: none)
  line(s2, s3, stroke: 1pt); line(s4, s1, stroke: 1pt)
  if diagonales {
    line(s1, s3, stroke: (paint: gray, dash: "dashed")); line(s2, s4, stroke: (paint: gray, dash: "dashed"))
  }
  trace-vect(s1, s2, c2); trace-vect(s4, s3, c2)
  lbl((s1, 50%, s2), text(fill: c2)[#v1], "south-east"); lbl((s4, 50%, s3), text(fill: c2)[#v2], "north-west")
  for (s, n, a) in ((s1, n1.at(0), ancres.at(0)), (s2, n1.at(1), ancres.at(1)), (s3, n2.at(0), ancres.at(2)), (s4, n2.at(1), ancres.at(3))) {
    lbl(s, n, a)
  }
})
// PARAC : ABDC, vecteurs AB et CD
#let fig-parac = parallelogramme((0, 0), (3, 1), (4, -0.5), (1, -1.5), ($A$, $B$), ($D$, $C$),
  $vect(A B)$, $vect(C D)$, ("east", "south-west", "west", "north-east"))
// PARAA : écrite en entier (diagonales et point I en plus)
#let fig-paraa = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  let (A, B, C, D) = ((0, 0), (4, 1), (5.5, -0.8), (1.5, -1.8))
  line(A, B, C, D, close: true, fill: blue.lighten(94%), stroke: none)
  line(B, C, stroke: 1pt); line(D, A, stroke: 1pt)
  line(A, C, stroke: (paint: gray, dash: "dashed")); line(B, D, stroke: (paint: gray, dash: "dashed"))
  trace-vect(A, B, c2); trace-vect(D, C, c2)
  lbl((A, 50%, B), text(fill: c2)[$vect(A B)$], "south-east")
  lbl((D, 50%, C), text(fill: c2)[$vect(D C)$], "north-west")
  pt((2.75, -0.4)); lbl((2.75, -0.3), $I$, "south")
  lbl(A, $A$, "east"); lbl(B, $B$, "south-west"); lbl(C, $C$, "west"); lbl(D, $D$, "north-east")
})

#let fig-parab = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  line((-0.5, 0), (5.5, 0), stroke: gray)
  trace-vect((0, 0.25), (2, 0.25), c2); lbl((1, 0.25), text(fill: c2)[$vect(A B)$], "south")
  trace-vect((3, 0.25), (5, 0.25), c2); lbl((4, 0.25), text(fill: c2)[$vect(D C)$], "south")
  for (x, n) in ((0, $A$), (2, $B$), (3, $D$), (5, $C$)) { pt((x, 0)); lbl((x, 0), n, "north") }
})

#let fig-mila = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  line((0, 0), (5, 0), stroke: gray)
  for x in (1.25, 3.75) {   // codage : deux petits traits sur chaque moitié
    for d in (-0.06, 0.06) { line((x + d - 0.05, -0.12), (x + d + 0.05, 0.12), stroke: 0.6pt + gray) }
  }
  trace-vect((0, 0.3), (2.4, 0.3), c2); lbl((1.2, 0.3), text(fill: c2)[$vect(A I)$], "south")
  trace-vect((2.6, 0.3), (5, 0.3), c2); lbl((3.8, 0.3), text(fill: c2)[$vect(I B)$], "south")
  for (x, n) in ((0, $A$), (2.5, $I$), (5, $B$)) { pt((x, 0)); lbl((x, 0), n, "north") }
})

#let fig-hexa = cetz.canvas(length: 0.85cm, {
  import cetz.draw: *
  let noms = ($A$, $B$, $C$, $D$, $E$, $F$)
  let s = range(6).map(k => (2 * calc.cos(k * 60deg), 2 * calc.sin(k * 60deg)))
  for k in range(6) {
    line((0, 0), s.at(k), stroke: gray)
    content((2.45 * calc.cos(k * 60deg), 2.45 * calc.sin(k * 60deg)), noms.at(k))
  }
  line(..s, close: true, stroke: 1pt)
  for p in s { pt(p) }
  pt((0, 0)); lbl((0, 0), $O$, "north", pad: 5pt)
})

#let fig-paralla = cetz.canvas(length: 0.9cm, {
  import cetz.draw: *
  line((0, 0), (1, 2), (4, 3), (3, 1), close: true, fill: rgb(0, 153, 0).lighten(88%), stroke: none)
  line((0, 0), (1, 2), (5, 1), (4, -1), close: true, fill: blue.lighten(90%), stroke: none)
  line((1, 2), (4, 3), (3, 1), (0, 0), stroke: 1pt + c3)
  line((1, 2), (5, 1), (4, -1), (0, 0), stroke: 1pt + c1)
  trace-vect((0, 0), (1, 2), c2, ep: 1.5pt); trace-vect((4, -1), (5, 1), c2, ep: 1.5pt); trace-vect((3, 1), (4, 3), c2, ep: 1.5pt)
  for (p, n, a) in (((0, 0), $A$, "east"), ((1, 2), $B$, "south"), ((5, 1), $C$, "west"),
                    ((4, -1), $D$, "north"), ((4, 3), $E$, "south"), ((3, 1), $F$, "north-west")) { pt(p); lbl(p, n, a) }
})

#let fig-basea = cetz.canvas(length: 0.8cm, {
  import cetz.draw: *
  quad(-1, 4, -1, 3)
  axe((-1, 0), (4.3, 0)); axe((0, -1), (0, 3.3))
  angle-droit(0.22)
  trace-vect((0, 0), (1, 0), c2, ep: 1.6pt); trace-vect((0, 0), (0, 1), c2, ep: 1.6pt)
  lbl((0.5, 0), text(fill: c2)[$vect(i)$], "north"); lbl((0, 0.5), text(fill: c2)[$vect(j)$], "east")
  lbl((0, 0), $O$, "north-east"); lbl((1, 0), $I$, "south-west"); lbl((0, 1.1), $J$, "west")
})

// Graduations d'un repère sur quadrillage (LECTA, ABCOA)
#let graduations(xs, ys) = {
  import cetz.draw: *
  for x in xs { line((x, 0.08), (x, -0.08)); lbl((x, -0.08), text(7pt)[$#x$], "north", pad: 1pt) }
  for y in ys { line((0.08, y), (-0.08, y)); lbl((-0.08, y), text(7pt)[$#y$], "east", pad: 1pt) }
  lbl((0, 0), text(7pt)[$0$], "north-east", pad: 1pt)
}

// LECTA : les déplacements en pointillés n'apparaissent que dans la version professeur
#let fig-lecta = context {
  let prof = ifcorrection()
  let prop = xcolor("prop")
  cetz.canvas(length: 0.62cm, {
    import cetz.draw: *
    quad(-3.5, 4.5, -2.5, 3.5)
    axe((-3.5, 0), (4.7, 0)); axe((0, -2.5), (0, 3.7))
    graduations((-3, -2, -1, 1, 2, 3, 4), (-2, -1, 1, 2, 3))
    if prof {
      let pointilles = (paint: prop, thickness: 0.8pt, dash: "dashed")
      line((1, 1), (4, 1), (4, 3), stroke: pointilles)
      line((0, 0.1), (-2, 0.1), (-2, 3), stroke: pointilles)
      line((1, -1), (3, -1), (3, -2), stroke: pointilles)
    }
    trace-vect((1, 1), (4, 3), c1, ep: 1.5pt); lbl((2.5, 2), text(fill: c1)[$vect(u)$], "south-east")
    trace-vect((0, 0), (-2, 3), c2, ep: 1.5pt); lbl((-1, 1.5), text(fill: c2)[$vect(v)$], "east")
    trace-vect((1, -1), (3, -2), c3, ep: 1.5pt); lbl((2, -1.5), text(fill: c3)[$vect(w)$], "north-east")
  })
}

#let fig-abcoa = cetz.canvas(length: 0.62cm, {
  import cetz.draw: *
  quad(-1, 7, -1, 4)
  axe((-1, 0), (7.3, 0)); axe((0, -1), (0, 4.3))
  lbl((0, 0), text(7pt)[$0$], "north-east", pad: 1pt)
  let pointille = (thickness: 0.8pt, dash: "dotted")
  line((1, 3), (1, 0), stroke: pointille); lbl((1, 0), $x_A$, "north")
  line((6, 1), (6, 0), stroke: pointille); lbl((6, 0), $x_B$, "north")
  line((1, 3), (0, 3), stroke: pointille); lbl((0, 3), $y_A$, "east")
  line((6, 1), (0, 1), stroke: pointille); lbl((0, 1), $y_B$, "east")
  let tirets = (paint: c3, thickness: 0.8pt, dash: "dashed")
  line((1, 3), (6, 3), stroke: tirets); lbl((3.5, 3), text(fill: c3)[$x_B - x_A$], "south")
  line((6, 3), (6, 1), stroke: tirets); lbl((6, 2), text(fill: c3)[$y_B - y_A$], "west")
  trace-vect((1, 3), (6, 1), c1, ep: 1.5pt); lbl((3.5, 2), text(fill: c1)[$vect(A B)$], "north-east")
  pt((1, 3)); lbl((1, 3), $A$, "south-east"); pt((6, 1)); lbl((6, 1), $B$, "north-west")
})

// ---------------------------------------------------------------------------
// Première page : sommaire ; deuxième : compétences et vocabulaire (Cours.tex)
// ---------------------------------------------------------------------------
#tableofcontents()
#pagebreak()

#tableaucompetence(
  competence[Utiliser le vocabulaire et les notations des vecteurs : direction, sens, norme, vecteur nul, vecteur opposé],
  competence[Reconnaître des vecteurs égaux et utiliser la propriété du parallélogramme],
  competence[Caractériser le milieu d'un segment par une égalité de vecteurs],
  competence[Construire l'image d'un point par une translation],
  competence[Lire les coordonnées d'un vecteur et représenter un vecteur de coordonnées données],
  competence[Calculer les coordonnées d'un vecteur à partir de celles de ses extrémités],
  competence[Calculer la norme d'un vecteur et la distance entre deux points],
  competence[Calculer les coordonnées du milieu d'un segment],
  competence[Déterminer la nature d'un triangle ou d'un quadrilatère à l'aide des coordonnées],
)
#v(1fr)
#printvocindex()
#v(1fr)
#pagebreak()

// ---------------------------------------------------------------------------
// Section 1 (enonce.tex)
// ---------------------------------------------------------------------------
= Repérage dans le plan : rappels

// LaTeX : Definition/repere_orthonorme.tex
#definition[Repère du plan][
  Trois points $O$, $I$ et $J$ non alignés forment un #voc[repère] du plan, noté $rep$ :

  #multi-colonnes(6)[
    #tcbitem(raster-multicolumn: 4, valign: "center")[
      #tcbenumerate[
        + le point $O$ est appelé #voc[origine] du repère ;
        + la droite $(O I)$ est appelée #voc[axe des abscisses], d'unité $O I$ ;
        + la droite $(O J)$ est appelée #voc[axe des ordonnées], d'unité $O J$.
      ]

      Si les axes sont perpendiculaires, le repère est dit #voc[orthogonal].
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-repa]
  ]

  Si de plus $O I = O J$, c'est-à-dire si le triangle $O I J$ est rectangle isocèle en $O$, le repère est dit #voc[orthonormé].
]

// LaTeX : Propriete/coordonnees_point.tex
#propriete[Coordonnées d'un point][
  Dans un repère $rep$, chaque point $M$ du plan est repéré par un unique couple de nombres réels $(x thin; y)$ appelé #voc[coordonnées] du point $M$ : le nombre $x$ est appelé #voc[abscisse] de $M$ et le nombre $y$ son #voc[ordonnée]. On note $coordonnees(x, y, nom: M)$.
]

// ---------------------------------------------------------------------------
// Section 2
// ---------------------------------------------------------------------------
= Vecteurs : aspect géométrique

== De la translation au vecteur

// LaTeX : Definition/translation.tex
#definition[Translation et vecteur][
  #multi-colonnes(5)[
    #tcbitem(raster-multicolumn: 3, valign: "center")[
      Soient $A$ et $B$ deux points du plan.

      La #voc[translation] qui transforme $A$ en $A'$ fait glisser #acc[tous les points] du plan dans la même direction que $(A A')$, dans le sens de $A$ vers $A'$ et d'une longueur égale à $A A'$.

      On l'appelle la #acc[translation de vecteur $vect(A A')$]. Sur la figure, elle transforme le triangle $A B C$ en $A'B'C'$.
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-transb]
  ]
]

// LaTeX : Definition/vecteur.tex
#definition[Vecteur][
  Soient $A$ et $B$ deux points distincts. Le #voc[vecteur] $vect(A B)$ associé à la translation qui transforme $A$ en $B$ est caractérisé par :

  #multi-colonnes(5)[
    #tcbitem(raster-multicolumn: 3, valign: "center")[
      #tcbenumerate[
        + sa #acc[direction] : celle de la droite $(A B)$ ;
        + son #acc[sens] : de $A$ vers $B$ ;
        + sa #acc[longueur] : la longueur $A B$.
      ]
      On le représente par une flèche : $A$ est l'#acc[origine] du vecteur et $B$ son #voc[extrémité].
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-veca]
  ]
]

// LaTeX : Remarque/vecteur_deplacement_position.tex
#remarque[Vecteur déplacement et vecteur position][
  En physique et en mathématiques, on distingue deux cas d'utilisation du mot vecteur :

  #multi-colonnes(6)[
    #tcbitem(raster-multicolumn: 4, valign: "center")[
      #tcbenumerate[
        + le vecteur $vect(A B)$ est le #voc[vecteur déplacement] de $A$ à $B$ : il décrit le mouvement d'un objet qui passe de la position $A$ à la position $B$ ;
        + si le point $O$ est choisi comme origine, le vecteur $vect(O M)$ est le #voc[vecteur position] du point $M$ (relativement à $O$).
      ]
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-posa]
  ]
]

== Égalité de deux vecteurs et représentants

// LaTeX : Definition/egalite_vecteurs.tex
#definition[Égalité de deux vecteurs][
  Deux vecteurs $vect(A B)$ et $vect(C D)$ sont #voc[égaux] lorsqu'ils définissent la #acc[même translation] : la translation de vecteur $vect(A B)$ transforme $C$ en $D$. Cela signifie qu'ils ont :

  #tcbenumerate(raster-columns: 3)[
    + la même #acc[direction] : $(A B)$ et $(C D)$ sont parallèles ;
    + le même #acc[sens] : de $A$ vers $B$ comme de $C$ vers $D$ ;
    + la même #acc[longueur] : $A B = C D$.
  ]

  On écrit alors $vect(A B) = vect(C D)$.
]

// LaTeX : Definition/representants_notation.tex
#definition[Représentants et notation d'un vecteur][
  #multi-colonnes(6)[
    #tcbitem(raster-multicolumn: 4, valign: "center")[
      La translation qui transforme $A$ en $B$ transforme aussi $C$ en $D$ et $E$ en $F$ : on a donc $vect(A B) = vect(C D) = vect(E F)$.

      Ces flèches sont des #voc[représentants] d'un même vecteur, que l'on peut nommer par une seule lettre : on note $vect(u) = vect(A B)$.

      $vect(A B)$ est le représentant d'#acc[origine $A$] du vecteur $vect(u)$.
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-repra]
  ]
]

// LaTeX : Propriete/proprietes_egalite.tex
#propriete[Représentant d'origine donnée][
  #tcbenumerate(raster-columns: 2)[
    + Pour tout point $A$ et tout vecteur $vect(u)$, il existe un #acc[unique] point $B$ tel que $vect(A B) = vect(u)$.
    + Pour tous points $A$, $B$ et $C$ : $vect(A B) = vect(A C)$ si, et seulement si, $B = C$.
  ]
]

== Vecteur nul et vecteur opposé

// LaTeX : Notation/vecteur_nul_oppose.tex
#notation[Vecteur nul et vecteur opposé][
  #multi-colonnes(6)[
    #tcbitem(raster-multicolumn: 4, valign: "center")[
      #tcbenumerate[
        + La translation qui transforme $A$ en $A$ laisse tous les points immobiles. Son vecteur est le #voc[vecteur nul], noté $vect(0)$ :
          #align(center)[$vect(A A) = vect(B B) = vect(0)$ #h(1em) et #h(1em) $vect(A B) = vect(0)$ si, et seulement si, $A = B$.]
        + Le #voc[vecteur opposé] au vecteur $vect(A B)$ est le vecteur $vect(B A)$ : même direction, même longueur, mais #acc[sens contraire].

          On note $vect(B A) = -vect(A B)$ et, si $vect(u) = vect(A B)$, on note $-vect(u)$ ce vecteur.
      ]
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-oppa]
  ]
]

// ---------------------------------------------------------------------------
// Section 3
// ---------------------------------------------------------------------------
= Parallélogramme, milieu et translation

== Propriété du parallélogramme

// LaTeX : Propriete/parallelogramme_vecteurs.tex
#propriete[Parallélogramme et égalité de vecteurs][
  #multi-colonnes(2)[
    #tcbitem(valign: "center")[
      Soient $A$, $B$, $C$ et $D$ quatre points du plan.

      #tcbenumerate[
        + $vect(A B) = vect(D C)$ si, et seulement si, $A B C D$ est un #acc[parallélogramme] (éventuellement aplati).
        + $vect(A B) = vect(D C)$ si, et seulement si, les diagonales $[A C]$ et $[B D]$ ont le #acc[même milieu].
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-paraa]
  ]
]

// LaTeX : Remarque/ordre_sommets.tex
#remarque[Attention à l'ordre des sommets][
  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[#acc[Parallélogramme aplati] : si $vect(A B) = vect(D C)$ avec les quatre points alignés, $A B C D$ est un parallélogramme aplati.]
    #tcbitem(halign: "center", valign: "center")[#fig-parab]
    #tcbitem(raster-multicolumn: 2, valign: "center")[#acc[Ordre des lettres] : $vect(A B) = vect(C D)$ signifie que $A B D C$ (et non $A B C D$) est un parallélogramme. On lit les sommets en suivant $A -> B$, puis l'extrémité $D$ du second vecteur, puis son origine $C$.]
    #tcbitem(halign: "center", valign: "center")[#fig-parac]
  ]
]

== Caractérisation vectorielle du milieu

// LaTeX : Propriete/milieu_vecteurs.tex
#propriete[Caractérisation vectorielle du milieu][
  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[
      Soient $A$ et $B$ deux points distincts et $I$ un point du plan.

      $I$ est le #voc[milieu] du segment $[A B]$ si, et seulement si : #h(1fr) #encadrer(couleur: "prop")[$vect(A I) = vect(I B)$] #h(1fr)
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-mila]
  ]
]

// LaTeX : Demonstration/milieu_vecteurs.tex — la démonstration est un texte à trous (crep)
#demonstration[Caractérisation vectorielle du milieu][
  Soit $I$ le milieu de $[A B]$

  #crep[
    $<==>$ $I$ appartient au segment $[A B]$ et $A I = I B$ ;

    $<==>$ les points $A$, $I$ et $B$ sont alignés dans cet ordre et $A I = I B$ ;

    $<==>$ les droites $(A I)$ et $(I B)$ sont parallèles, le sens de $A$ vers $I$ est celui de $I$ vers $B$, et $A I = I B$ ;

    $<==>$ $vect(A I) = vect(I B)$ (même direction, même sens, même longueur).
  ]
]

#pagebreak()   // \newpage du LaTeX : sans lui, le bandeau de l'exercice 1 reste seul en bas de page
== Exercices d'application

// LaTeX : Exercice/hexagone_regulier.tex
#rdifficulty(1.5)
#exo(tags: "2GT-GEO-009")[Vecteurs dans un hexagone régulier][
  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[
      $A B C D E F$ est un hexagone régulier de centre $O$. On n'utilise que les points nommés sur la figure.
      #tcbenumerate[
        + #itempoint(2)[#acc[Citer] tous les vecteurs égaux au vecteur $vect(A B)$.]
        + #itempoint(2)[#acc[Citer] tous les vecteurs opposés au vecteur $vect(A B)$.]
        + #itempoint(2)[#acc[Déterminer] l'image du point $F$, puis celle du point $O$, par la translation de vecteur $vect(A B)$.]
        + #itempoint(1)[#acc[En déduire] la nature du quadrilatère $A B O F$.]
        + #itempoint(2)[#acc[Démontrer] que $O$ est le milieu de $[A D]$ #acc[à l'aide d'une égalité de vecteurs].]
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-hexa]
  ]
  #exocorrection
  #tcbenumerate[
    + Les côtés et les rayons de l'hexagone régulier ont tous la même longueur. Les segments $[A B]$, $[F O]$, $[O C]$ et $[E D]$ sont parallèles et se parcourent dans le même sens.

      Donc #encadrer(couleur: "prop")[$vect(A B) = vect(F O) = vect(O C) = vect(E D)$]
    + Les vecteurs opposés à $vect(A B)$ ont la même direction et la même longueur, mais le sens contraire :

      #encadrer(couleur: "prop")[$vect(B A)$, $vect(O F)$, $vect(C O)$ et $vect(D E)$]
    + $vect(F O) = vect(A B)$ donc la translation de vecteur $vect(A B)$ transforme $F$ en $O$.

      $vect(O C) = vect(A B)$ donc la translation de vecteur $vect(A B)$ transforme $O$ en $C$.
    + $vect(A B) = vect(F O)$ donc, d'après la propriété du parallélogramme, $A B O F$ est un parallélogramme.

      Comme de plus $A B = A F$, c'est même un losange.
    + Les points $A$, $O$ et $D$ sont alignés (diagonale de l'hexagone), le sens de $A$ vers $O$ est celui de $O$ vers $D$ et $A O = O D$ (rayons).

      Donc $vect(A O) = vect(O D)$ : #encadrer(couleur: "prop")[$O$ est le milieu de $[A D]$]
  ]
]

// LaTeX : Exercice/parallelogrammes.tex
#rdifficulty(1.5)
#exo(tags: "2GT-GEO-009")[Parallélogrammes et vecteurs][
  Soient $A B C D$ et $A B E F$ deux parallélogrammes.
  #tcbenumerate(raster-columns: 3)[
    + #itempoint(2)[#acc[Faire] une figure.]
    + #itempoint(2)[#acc[Citer] dans chaque parallélogramme un vecteur égal à $vect(A B)$.]
    + #itempoint(2)[#acc[En déduire] la nature du quadrilatère $D C E F$.]
  ]
  #exocorrection
  #tcbenumerate[
    + Une figure possible :
      #align(center, fig-paralla)
    + $A B C D$ est un parallélogramme donc $vect(A B) = vect(D C)$.

      $A B E F$ est un parallélogramme donc $vect(A B) = vect(F E)$.
    + Les vecteurs $vect(D C)$ et $vect(F E)$ sont tous les deux égaux à $vect(A B)$, donc $vect(D C) = vect(F E)$.

      D'après la propriété du parallélogramme, #encadrer(couleur: "prop")[$D C E F$ est un parallélogramme (éventuellement aplati)]

      On a démontré une égalité de vecteurs par l'intermédiaire d'un troisième vecteur.
  ]
]

// ---------------------------------------------------------------------------
// Section 4 (jusqu'à 4.3)
// ---------------------------------------------------------------------------
= Coordonnées d'un vecteur

== Base orthonormée

// LaTeX : Definition/base_orthonormee.tex
#definition[Base orthonormée][
  #multi-colonnes(5)[
    #tcbitem(raster-multicolumn: 3, valign: "center")[
      Soit $rep$ un repère orthonormé. On pose $vect(i) = vect(O I)$ et $vect(j) = vect(O J)$.

      Les vecteurs $vect(i)$ et $vect(j)$ ont des directions #acc[perpendiculaires] et une longueur égale à l'#acc[unité] : on dit que $baseij$ est une #voc[base orthonormée].

      Le repère $rep$ se note alors $vrep$.
    ]
    #tcbitem(raster-multicolumn: 2, halign: "center", valign: "center")[#fig-basea]
  ]
]

== Lire et représenter un vecteur

// LaTeX : Definition/coordonnees_vecteur.tex
#definition[Coordonnées d'un vecteur][
  Le plan est muni d'un repère $vrep$ et $vect(u)$ est un vecteur. Il existe un unique point $M$ tel que $vect(O M) = vect(u)$ ($vect(O M)$ est le vecteur position de $M$).

  Les #voc[coordonnées du vecteur] $vect(u)$ sont les coordonnées de ce point $M$. Si $coordonnees(x, y, nom: M)$, on note $vect(u) coordonnees(x, y)$ ou, en colonne, $vect(u) vec(x, y)$.

  En particulier, $vect(i) coordonnees(1, 0)$, $vect(j) coordonnees(0, 1)$ et $vect(0) coordonnees(0, 0)$.
]

// LaTeX : Methode/lire_coordonnees_vecteur.tex
#methode[Lire les coordonnées d'un vecteur sur un quadrillage][
  Dans une base orthonormée, on part de l'#acc[origine] d'un représentant et on compte le déplacement jusqu'à son #acc[extrémité] :
  #tcbenumerate(raster-columns: 2)[
    + l'#acc[abscisse] $x$ est le déplacement horizontal : positif vers la droite, négatif vers la gauche ;
    + l'#acc[ordonnée] $y$ est le déplacement vertical : positif vers le haut, négatif vers le bas.
  ]
  Tous les représentants d'un même vecteur donnent les mêmes coordonnées.
]

// LaTeX : Exemple/lire_coordonnees_vecteur.tex
#exemple[Lire des coordonnées][
  Dans la base orthonormée $baseij$, #acc[lire] les coordonnées des vecteurs $vect(u)$, $vect(v)$ et $vect(w)$.

  #multi-colonnes(2)[
    #tcbitem(valign: "center")[
      #crep[
        $vect(u)$ : 3 vers la droite, 2 vers le haut, donc $vect(u) coordonnees(3, 2)$.

        $vect(v) coordonnees(-2, 3)$.

        $vect(w) coordonnees(2, -1)$.
      ]
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-lecta]
  ]
]

== Coordonnées du vecteur $vect(A B)$

// LaTeX : Propriete/coordonnees_AB.tex
#propriete[Coordonnées du vecteur AB][
  Dans un repère $vrep$, on considère les points $coordonnees(x_A, y_A, nom: A)$ et $coordonnees(x_B, y_B, nom: B)$.

  #multi-colonnes(3)[
    #tcbitem(raster-multicolumn: 2, valign: "center")[
      Les coordonnées du vecteur $vect(A B)$ sont données par :
      #align(center)[#encadrer(couleur: "prop")[$vect(A B) coordonnees(x_B - x_A, y_B - y_A)$]]

      On fait #frquote[extrémité moins origine] : c'est le déplacement horizontal puis vertical pour aller de $A$ à $B$.
    ]
    #tcbitem(halign: "center", valign: "center")[#fig-abcoa]
  ]
]

// LaTeX : Exemple/coordonnees_AB.tex
#exemple[Calculer les coordonnées d'un vecteur][
  On donne $coordonnees(2, -5, nom: A)$ et $coordonnees(-7, 1, nom: B)$. #acc[Calculer] les coordonnées de $vect(A B)$ et de $vect(B A)$.

  #crep[
    $vect(A B) coordonnees(x_B - x_A, y_B - y_A)$, soit $vect(A B) coordonnees(-7 - 2, 1 - (-5))$, donc $vect(A B) coordonnees(-9, 6)$.

    De même $vect(B A) coordonnees(2 - (-7), -5 - 1)$, donc $vect(B A) coordonnees(9, -6)$ : les coordonnées du vecteur opposé sont opposées.
  ]
]

// ---------------------------------------------------------------------------
// Correction des exercices : version professeur seulement (\ifcorrection … \fi de Cours.tex)
// ---------------------------------------------------------------------------
#ifcorrection[
  #pagebreak()
  = Correction des exercices
  #rdexocorrection(0)
]
