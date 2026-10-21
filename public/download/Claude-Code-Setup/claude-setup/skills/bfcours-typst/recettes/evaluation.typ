// RECETTE : évaluation (devoir de 2de, 55 min, 7 exercices sur 20 points, corrigé à la fin).
//
// Ce qu'elle montre :
//   - le bandeau d'évaluation `chap-eval` (cases Classe et Date) avec le cartouche `tableau-eval(55)` dessous ;
//   - la ligne de consignes et le « Bilan : … / total » calculé (`getsavedtotalpoints()`) ;
//   - les points EN TÊTE de chaque question : `#itempoint(2)[Énoncé…]`, boîtes visibles (`displayitempoints(true)`),
//     score de chaque exercice calculé dans son bandeau (`display-score: true`) ;
//   - un exercice d'évaluation `exo-eval` (grille MI / MF / MS / TBM, compétence dans `tags`) à côté des `exo` ;
//   - les réponses dans le sujet : `crep` (lignes Seyès, réponse en couleur chez le professeur) et `tcfillcrep`
//     (trou qui occupe la fin de la ligne) ; résultats et calculs intermédiaires colorés par deux fonctions `res`, `op` ;
//   - des fractions « display », des égalités alignées (`&=` et `\`), des puissances ;
//   - trois figures redessinées en cetz (parallélogramme, triangles accolés, rectangle et parallèle) ;
//   - la partie « Solutions » en version professeur seulement, avec son propre bandeau (`chapitre`).
// Pour un tableau des compétences évaluées en fin de sujet : `#printcompindex()` (il reprend les étiquettes des
// EXOEVAL et les titres des EXO) ; pour régler la grille : `setrdexo(pour: "competences", …)`.
//
// Source : 1. Cours/2nde/Sequence-Configuration_du_plan/Evaluation/ (Evaluation.tex, enonce_TOOLS.tex,
// enonce_TOOLS_figures.tex). Contenu mathématique repris tel quel, sauf deux corrections signalées en commentaire
// (exercice 6 : coquille `\times'` ; exercice 7 : réponse de la zone élève 3^4 au lieu de 3^3).
// Le maître élève (ELEVE_….tex) écrit « Calculatrice interdite » et le maître professeur « Calculatrice
// autorisée » : la recette garde le texte élève, celui que lisent les élèves.
//
// Compiler une copie placée dans le dossier de travail (pas dans le skill) ; PDF prof et élève, images :
//   python "<skill>/scripts/compiler.py" "dossier/evaluation.typ" --png

#import "@preview/farfadet:0.2.0": *
#import "@preview/cetz:0.5.3"

// Sans `niveau` ni `theme`, le modèle ne pose pas de bandeau : on pose `chap-eval` soi-même.
// Identité de l'auteur, réglée une fois pour les bandeaux et le pied de page (dans une façade,
// ces lignes disparaissent du document : voir references/facade.md).
#setbfmodele(pour: "identite", cycle: [Lycée], etablissement: [du Parc])

#show: modele("cours", marges: (right: 1cm))

#setrdexo(display-exotitle: true, exo-header: "tcolorbox", skin: "bouyachakka", display-score: true,
  display-level: true, display-tags: "correction")
#setrdcrep(seyes: true, correction-color: "prop", correction-font: "\large\bfseries")
#displayitempoints(true)

// Couleurs du corrigé d'origine : résultat en orange, opération ajoutée en bleu (utilisables en maths : res(37/4))
#let res(x) = text(fill: rgb("#f15929"), x)
#let op(x) = text(fill: rgb("#216D9A"), x)

// ---------------------------------------------------------------------------
// Figures (enonce_TOOLS_figures.tex) en cetz
// ---------------------------------------------------------------------------
#let fig-parallelogramme = cetz.canvas(length: 0.6cm, {
  import cetz.draw: *
  line((0, 0), (6, 0), (7, -3), (1, -3), close: true, stroke: 1pt)
  line((0, 0), (7, -3), stroke: (dash: "dashed")); line((6, 0), (1, -3), stroke: (dash: "dashed"))
  content((0, 0), $G$, anchor: "south-east", padding: 2pt); content((6, 0), $H$, anchor: "south-west", padding: 2pt)
  content((7, -3), $I$, anchor: "north-west", padding: 2pt); content((1, -3), $J$, anchor: "north-east", padding: 2pt)
  content((3.5, -1.5), $O$, anchor: "south", padding: 3pt)
})

#let fig-trigo = cetz.canvas(length: 0.4cm, {
  import cetz.draw: *
  let (M, N, O, P) = ((7, 0), (0, 0), (0, 5), (13, 8.4))
  line(M, N, O, close: true); line(O, M, P, close: true)
  line((0, 0), (0.4, 0), (0.4, 0.4), (0, 0.4), close: true, stroke: 0.5pt)              // angle droit en N
  line((7, 0), (6.67, 0.23), (6.9, 0.56), (7.23, 0.33), close: true, stroke: 0.5pt)    // angle droit en M
  content((7, -0.6), $M$); content((0, -0.6), $N$); content((0, 5.6), $O$); content((13.6, 8.4), $P$)
})

#let fig-thales = cetz.canvas(length: 0.6cm, {
  import cetz.draw: *
  line((0, 4), (7, 4), (7, 0), (0, 0), close: true)
  for (a, b, c, d) in (((0, 4), (0, 3.6), (0.4, 3.6), (0.4, 4)), ((7, 4), (6.6, 4), (6.6, 3.6), (7, 3.6)),
                       ((7, 0), (7, 0.4), (6.6, 0.4), (6.6, 0)), ((0, 0), (0.4, 0), (0.4, 0.4), (0, 0.4))) {
    line(a, b, c, d, close: true, stroke: 0.5pt)
  }
  line((2.33, 4), (0, 2.67)); line((7, 4), (0, 0))
  line((-1.3, 2.67), (-1.3, 0), mark: (start: "stealth", end: "stealth", fill: black))
  content((-1.5, 1.34), [?], anchor: "west")
  // dans le canevas, `rotate` est celui de cetz (il tourne le repère) : texte incliné par la clé `angle`
  content((3.75, 1.57), [6 cm], angle: 30deg); content((1.42, 2.9), [2,4 cm], angle: 30deg)
  content((7.5, 2), [3 cm], angle: 270deg)
  content((2.33, 4.5), $M$); content((-0.5, 2.67), $N$); content((0, 4.5), $T$)
  content((7, 4.5), $U$); content((7, -0.5), $V$); content((0, -0.5), $W$)
})

// ---------------------------------------------------------------------------
// En-tête (Evaluation.tex)
// ---------------------------------------------------------------------------
#chap-eval(niveau: "2nde", theme: [Configurations du plan - Techniques opératoires],
  apres: tableau-eval(55), type: [Devoir :])

#multi-colonnes(3)[
  #tcbitem(raster-multicolumn: 2)[
    #acc[Calculatrice interdite] #h(1fr) - #h(1fr) #acc[Brouillon conseillé]

    Les réponses sont à #acc[justifier] par un calcul ou un résultat de cours.
  ]
  #tcbitem(colback: white, colframe: black, boxrule: 1pt)[
    *Bilan : #tccrep(seyes: false, 1.5cm)[] / #getsavedtotalpoints() #tccrep(seyes: false, 2cm)[]*
  ]
]

// ---------------------------------------------------------------------------
// Exercices (enonce_TOOLS.tex)
// ---------------------------------------------------------------------------

// Exercice 1 : EXOEVAL au lieu d'EXO (seul changement : l'en-tête porte la grille de maîtrise, la compétence
// évaluée est l'étiquette `tags`). Le contenu est celui de l'original.
#rdifficulty(1)
#exo-eval(tags: "2G11-1")[Utiliser le théorème de Pythagore][
  #tcbenumerate(raster-columns: 2)[
    + #itempoint(2)[$G H I J$ est un parallélogramme de centre $O$ tel que $G O = 3","9$ cm, $G H = 6","7$ cm et $H O = 5","2$ cm. \ $G H I J$ est-il un losange ?]
      #crep[Dans le triangle $G O H$, le plus grand côté est $[G H]$. \ $G H^2 = 6","7^2 = 44","89$ \ $G O^2 + O H^2 = 3","9^2 + 5","2^2 = 42","25$ \ On constate que $G H^2 != G O^2 + O H^2$, l'égalité de Pythagore n'est pas vérifiée donc $G O H$ n'est pas un triangle rectangle. \ Finalement, $G H I J$ #res[n'est pas un losange].]
    + #itempoint(2)[$S T U V$ est un rectangle tel que $S T = 1$ cm et $S U = 2","6$ cm. \ #acc[Calculer] $T U$.]
      #crep[$S T U V$ est un rectangle donc il possède 4 angles droits. Le triangle $T U S$ est rectangle en $T$ donc d'après le théorème de Pythagore, on a : \ $U S^2 = T U^2 + T S^2$ \ D'où $T U^2 = U S^2 - T S^2$. \ $T U^2 = 2","6^2 - 1^2$ \ $T U^2 = 5","76$ \ $T U = sqrt(5","76)$ cm Donc $T U = res(2","4)$ #res[cm].]
  ]
  #exocorrection
  #tcbenumerate(raster-columns: 2)[
    + #fig-parallelogramme

      Dans le triangle $G O H$, le plus grand côté est $[G H]$. \ $G H^2 = 6","7^2 = 44","89$ \ $G O^2 + O H^2 = 3","9^2 + 5","2^2 = 42","25$ \ On constate que $G H^2 != G O^2 + O H^2$, l'égalité de Pythagore n'est pas vérifiée donc $G O H$ n'est pas un triangle rectangle. \ Si $G H I J$ était un losange alors ses diagonales devraient être perpendiculaires et $G O H$ devrait être un triangle rectangle. \ Finalement, comme $G O H$ n'est pas un triangle rectangle, alors $G H I J$ #res[*n'est pas un losange*].
    + $S T U V$ est un rectangle donc il possède 4 angles droits. Le triangle $T U S$ est rectangle en $T$ donc d'après le théorème de Pythagore, on a : \ $U S^2 = T U^2 + T S^2$ \ D'où $T U^2 = U S^2 - T S^2$. \ $T U^2 = 2","6^2 - 1^2$ \ $T U^2 = 6","76 - 1$ \ $T U^2 = 5","76$ \ $T U = sqrt(5","76)$ cm \ Donc $T U = res(2","4)$ #res[*cm*].
  ]
]

#rdifficulty(1)
#exo(tags: "2N20-5")[Décomposition en produit de facteurs premiers.][
  #itempoint(2)[#acc[Écrire] les nombres suivants sous la forme d'un produit de facteurs premiers.]

  #tcbenumerate(raster-columns: 2)[
    + $378 =$ #tcfillcrep[$2 times 3^3 times 7$]
    + $702 =$ #tcfillcrep[$2 times 3^3 times 13$]
  ]
  #exocorrection
  #tcbenumerate(raster-columns: 2)[
    + $378 = 2 times 189$ \ $378 = 2 times 3 times 63$ \ $378 = 2 times 3 times 3 times 21$ \ $378 = 2 times 3 times 3 times 3 times 7$ \ $378 = res(2 times 3^3 times 7)$
      #v(0.5em)
      Donc la décomposition en produit de facteurs premiers de $378$ est $res(2 times 3^3 times 7)$.
    + $702 = 2 times 351$ \ $702 = 2 times 3 times 117$ \ $702 = 2 times 3 times 3 times 39$ \ $702 = 2 times 3 times 3 times 3 times 13$ \ $702 = res(2 times 3^3 times 13)$
      #v(0.5em)
      Donc la décomposition en produit de facteurs premiers de $702$ est $res(2 times 3^3 times 13)$.
  ]
]

#needspace(7cm)   // le bandeau de l'exercice ne reste pas seul en bas de page
#rdifficulty(1)
#exo(tags: "2G11-3")[Trigonométrie][
  #multi-colonnes(3)[
    #tcbitem[
      #fig-trigo \
      On donne :
      #multi-colonnes(2)[
        - $bullet$ $N M = 7$ cm
        - $bullet$ $hat(N M O) = 36°$
        #tcbitem(raster-multicolumn: 2)[$bullet$ $M P = 10","3$ cm]
      ]
    ]
    #tcbitem(raster-multicolumn: 2)[
      #tcbenumerate(raster-columns: 2)[
        + #itempoint(2)[#acc[Calculer] $M O$.]
          #crep(extra-lines: 2)[$O N M$ est rectangle en $N$ \ Donc $cos(hat(N M O)) = display((N M)/(M O))$ \ Soit $cos(36°) = display(7/(M O))$ \ $M O = display(7/cos(36°)) approx 8","7$ cm.]
        + #itempoint(2)[#acc[Calculer] la mesure de l'angle $hat(M O P)$]
          #crep(extra-lines: 1)[$O M P$ est rectangle en $M$ \ donc $tan(hat(M O P)) = display((M P)/(M O))$ \ $approx display((10","3)/(8","7))$ \ $hat(M O P) approx "arctan"(display((10","3)/(8","7))) approx res(50)°$.]
      ]
    ]
  ]
  #exocorrection
  $O N M$ est rectangle en $N$. \ Donc $cos(hat(N M O)) = display((N M)/(M O))$ \ Soit $cos(36°) = display(7/(M O))$ \ $M O = display(7/cos(36°)) approx 8","7$ cm. \ $O M P$ est rectangle en $M$. \ Donc $tan(hat(M O P)) = display((M P)/(M O))$ \ Soit $tan(hat(M O P)) approx display((10","3)/(8","7))$ \ $hat(M O P) approx "arctan"(display((10","3)/(8","7))) approx res(50)°$. \ La somme des angles d'un triangle est égale à $180°$. \ Donc $hat(N O M) = 180° - 90° - 36° = res(54)°$. \ De même, $hat(O P M) approx 180° - 90° - 50°$ et donc $hat(O P M) approx res(40)°$.
]

// Le LaTeX passait à la page avant cet exercice ; ici les exercices 3 et 4 tiennent ensemble en page 2.
#rdifficulty(1)
#exo(tags: "2G11-2")[Utiliser le théorème de Thalès][
  #itempoint(2)[Sur la figure ci-dessous $T U V W$ est un rectangle et $(M N)$ est parallèle à la diagonale $(U W)$. \ #acc[Calculer] la longueur $W N$ au millimètre près.]

  #multi-colonnes(3)[
    #tcbitem(halign: "center", valign: "center")[
      #fig-thales
      #crep[Dans le triangle $T U W$, $M in [T U]$, $N in [T W]$ et $(M N) slash.double (U W)$]
    ]
    #tcbitem(raster-multicolumn: 2)[
      #crep(extra-lines: 2)[D'après le théorème de Thalès on a :

        $display((T M)/(T U)) = display((T N)/(T W)) = display((M N)/(U W)) -> display((T N)/3) = display((2","4)/6)$

        $T N = display((3 times 2","4)/6) = 1","2$ cm

        Les points $T$, $N$ et $W$ sont alignés dans cet ordre donc $N W = T W - T N = 3 - 1","2 = 1","8$ cm.]
    ]
  ]
  #exocorrection
  // #v(…) = \medskip du LaTeX ; indispensable ici : dans les solutions, deux lignes de fractions
  // « display » consécutives se chevauchent sans lui (défaut de rdexocorrection, 07/10/2026).
  Dans le triangle $T U W$, $M$ est un point de $[T U]$, $N$ est un point de $[T W]$ et $(M N)$ est parallèle à $(U W)$ donc d'après le théorème de Thalès on a :
  #v(0.5em)
  $display((T M)/(T U)) = display((T N)/(T W)) = display((M N)/(U W))$
  #v(0.5em)
  $display((T M)/(T U)) = display((T N)/3) = display((2","4)/6)$
  #v(0.5em)
  $T N = display((3 times 2","4)/6) = 1","2$ cm
  #v(0.5em)
  Les points $T$, $N$ et $W$ sont alignés dans cet ordre donc $N W = T W - T N = 3 - 1","2 = 1","8$ cm.
]

#rdifficulty(1)
#exo(tags: "2N30-2")[Opérations avec les fractions][
  #itempoint(2)[#acc[Calculer] et #acc[donner] le résultat sous la forme d'une fraction simplifiée au maximum.]

  #tcbenumerate(raster-columns: 2)[
    + $7 - display((-9)/4) =$ #tcfillcrep[$display((7 op(times 4))/op(4)) - display((-9)/4)$]
      #crep[$= display((28 - (-9))/4) = display((28 + 9)/4) = res(display(37/4))$]
    + $display((-1)/6) + display(1/21) =$ #tcfillcrep[$display((-1 op(times 7))/(6 op(times 7))) + display((1 op(times 2))/(21 op(times 2)))$]
      #crep[$= display((-7 + 2)/42) = display((-5)/42) = res(-display(5/42))$]
  ]
  #exocorrection
  #tcbenumerate(raster-columns: 2)[
    + $7 - display((-9)/4) = display((7 op(times 4))/op(4)) - display((-9)/4) = display((28 - (-9))/4) = res(display(37/4))$
    + $display((-1)/6) + display(1/21) = display((-1 op(times 7))/(6 op(times 7))) + display((1 op(times 2))/(21 op(times 2))) = display((-7 + 2)/42) = display((-5)/42) = res(-display(5/42))$
  ]
]

#rdifficulty(1)
#exo(tags: "2N30-3")[Opérations avec les fractions][
  #itempoint(2)[#acc[Calculer] et #acc[donner] le résultat sous forme irréductible.]
  #tcbenumerate(raster-columns: 2)[
    + $A = display((-4)/(-9)) times display(5/6) =$ #tcfillcrep[$display((10 times 2)/(27 times 2))$] \
      $=$ #tcfillcrep[$display(10/27)$]
    + $B = display(7/9) div display((-2)/(-1)) =$ #tcfillcrep[$display((7 times (-1))/(9 times (-2)))$] \
      $=$ #tcfillcrep[$display((-7)/(-18)) = display(7/18)$]
  ]
  #exocorrection
  // Original : `-9 \times' 6` (coquille, prime parasite), corrigé en `-9 times 6`.
  // Le LaTeX aligne les égalités (`aligned`). Dans les solutions, une équation centrée `$ … $` prend la
  // police de texte des corrections (défaut de rdexocorrection, 07/10/2026) : une étape par ligne, empilées.
  #tcbenumerate(raster-columns: 2)[
    + #stack(spacing: 0.8em,
      $A = display((-4)/(-9)) times display(5/6)$,
      $#h(0.8em) = display((-4 times 5)/(-9 times 6))$,
      $#h(0.8em) = display(((-2) times 2 times 5)/((-3) times 3 times 2 times 3))$,
      $#h(0.8em) = display((10 op(times 2))/(27 op(times 2)))$,
      $#h(0.8em) = res(display(10/27))$)
    + #stack(spacing: 0.8em,
      $B = display(display(7/9)/display((-2)/(-1)))$,
      $#h(0.8em) = display(7/9) times display((-1)/(-2))$,
      $#h(0.8em) = display((7 times (-1))/(9 times (-2)))$,
      $#h(0.8em) = res(display((-7)/(-18)))$,
      $#h(0.8em) = res(display(7/18))$)
  ]
]

#rdifficulty(1)
#exo(tags: "2N31-3")[Puissances et notation scientifique][
  #itempoint(2)[#acc[Écrire] sous la forme $a^n$.]
  #tcbenumerate(raster-columns: 2)[
    + $display(27^2/3) =$ #tcfillcrep[$display((3^3)^2/3) = display(3^(3 times 2)/3) = display(3^6/3) = 3^(6 - 1) = res(3^5)$] \
      $=$ #tcfillcrep[]
    + // Original : la zone élève donnait 3^4 ; 3^9 / 3^6 = 3^3, comme dans la correction de l'original.
      $display((3^5 times 3^4)/9^3) =$ #tcfillcrep[$display(3^(5 + 4)/(3^2)^3) = display(3^9/3^(2 times 3)) = display(3^9/3^6)$] \
      $=$ #tcfillcrep[$3^(9 - 6) = res(3^3)$]
  ]

  #itempoint(2)[#acc[Donner] la notation scientifique des nombres suivants.]
  #tcbenumerate(raster-columns: 2, depart: 3)[
    + $390 times 10^(-7) =$ #tcfillcrep[$3","9 times 10^(text(fill: #blue, 2 + (-7))) = res(3","9 times 10^(-5))$]
    + $210 times 10^(-6) =$ #tcfillcrep[$2","1 times 10^(text(fill: #blue, 2 + (-6))) = res(2","1 times 10^(-4))$]
  ]
  #exocorrection
  #tcbenumerate(raster-columns: 2)[
    + $display(27^2/3) = display((3^3)^2/3) = display(3^(3 times 2)/3) = display(3^6/3) = 3^(6 - 1) = res(3^5)$.
    + $display((3^5 times 3^4)/9^3) = display(3^(5 + 4)/(3^2)^3) = display(3^9/3^(2 times 3)) = display(3^9/3^6) = 3^(9 - 6) = res(3^3)$.
  ]
  #tcbenumerate(raster-columns: 2, depart: 3)[
    + $390 times 10^(-7) = text(fill: #blue, 3","9 times 10^2) times 10^(-7) = 3","9 times 10^(text(fill: #blue, 2 + (-7))) = res(3","9 times 10^(-5))$
    + $210 times 10^(-6) = text(fill: #blue, 2","1 times 10^2) times 10^(-6) = 2","1 times 10^(text(fill: #blue, 2 + (-6))) = res(2","1 times 10^(-4))$
  ]
]

// ---------------------------------------------------------------------------
// Solutions : version professeur seulement
// ---------------------------------------------------------------------------
#ifcorrection[
  #pagebreak()
  #counter(page).update(1)
  #chapitre(niveau: "2nde", theme: [Configurations du plan - Techniques opératoires],
    type: [Solutions :])
  #rdexocorrection(0)
]
