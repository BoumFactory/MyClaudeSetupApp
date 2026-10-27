# Figures avec cetz 0.5.3

cetz est l'équivalent Typst de TikZ. La version 0.5.3 se télécharge au premier usage, puis reste dans le cache local (`%LOCALAPPDATA%/typst/packages/preview/cetz/0.5.3` sous Windows) : elle compile ensuite hors ligne. Hors ligne, ne pas prendre une autre version sans vérifier qu’elle est en cache. Tout ce qui suit a été compilé avec cetz 0.5.3.

## Exemple complet : repère, quadrillage, points, vecteur, courbe

```typ
#import "@preview/cetz:0.5.3"

#cetz.canvas(length: 0.8cm, {          // length : taille de l'unité (TikZ : scale)
  import cetz.draw: *
  // Quadrillage et axes
  grid((-1, -1), (6, 4), step: 1, stroke: 0.3pt + luma(180))
  line((-1, 0), (6, 0), mark: (end: "stealth"), stroke: 0.6pt)
  line((0, -1), (0, 4), mark: (end: "stealth"), stroke: 0.6pt)
  content((0, 0), [$O$], anchor: "north-east", padding: 2pt)
  // Points : de simples couples de nombres
  let A = (1, 1)
  let B = (4, 3)
  circle(A, radius: 0.06, fill: black)
  content(A, [$A$], anchor: "north", padding: 3pt)
  content(B, [$B$], anchor: "south-west", padding: 2pt)
  // Vecteur nommé, étiquette au milieu
  line(A, B, mark: (end: ">", fill: blue), stroke: 1pt + blue, name: "v")
  content("v.mid", text(fill: blue)[$arrow(u)$], anchor: "south-east", padding: 3pt)
  // Pointillés, arc, polygone plein
  line((4, 0), B, stroke: (dash: "dashed"))
  arc((5, 1), start: 0deg, stop: 90deg, radius: 0.5)
  line((1, 3), (2, 3.5), (1.5, 2.5), close: true, fill: rgb("#fde68a"))
  // Un point marqué d'une croix (fonction locale)
  let croix(p, nom) = {
    line((rel: (-0.1, -0.1), to: p), (rel: (0.2, 0.2)))
    line((rel: (-0.1, 0.1), to: p), (rel: (0.2, -0.2)))
    content(p, nom, anchor: "west", padding: 4pt)
  }
  croix((5, 2), [$C$])
  // Courbe d'une fonction sans paquet de tracé
  line(..range(0, 31).map(i => { let x = -1 + i / 6; (x, 0.25 * x * x) }), stroke: red)
  // Graduations
  for x in range(1, 6) { content((x, 0), text(7pt)[#x], anchor: "north", padding: 2pt) }
})
```

## Correspondances utiles

| Besoin | cetz |
|---|---|
| unité, échelle | `cetz.canvas(length: 0.8cm, { … })` |
| segment, ligne brisée, polygone | `line(a, b)`, `line(a, b, c)`, `line(a, b, c, close: true, fill: …)` |
| flèche | `mark: (end: ">")`, `(end: "stealth")`, `(start: ">", end: ">")` ; pointe pleine : `mark: (end: ">", fill: blue)` |
| trait | `stroke: 1pt + blue`, `stroke: (paint: blue, thickness: 1pt, dash: "dashed")` (`"dotted"`, `"dash-dotted"`) |
| quadrillage | `grid(a, b, step: 1, stroke: …)` |
| cercle, disque | `circle(c, radius: r)`, `fill: …` |
| rectangle | `rect(a, b, fill: …)` |
| arc | `arc(départ, start: 0deg, stop: 90deg, radius: r)` (le premier point est le DÉBUT de l'arc, pas le centre) |
| texte, étiquette | `content(p, [$A$], anchor: "south", padding: 3pt)` ; ancres : `"north"`, `"south-west"`, `"east"`… |
| point au milieu, au tiers | `(a, 50%, b)`, `(a, 33.33%, b)` (interpolation, en POURCENTAGE : `(a, 1/3, b)` place le point à 0,33 unité de `a`, pas au tiers) ; sur un élément nommé : `"v.mid"`, `"v.start"`, `"v.end"` |
| texte incliné | `content(p, [6 cm], angle: 30deg)` (pas `rotate`, qui est celui de cetz dans le canevas) |
| coordonnée relative | `(rel: (dx, dy), to: p)` ; seule : `(rel: (dx, dy))` part du point précédent |
| boucle, calcul | du code Typst ordinaire : `for`, `let`, `calc.cos(30deg)` |
| style commun | `set-style(stroke: 0.6pt, mark: (fill: black))` en tête du canevas |

## Pièges propres à cetz

- **`import cetz.draw: *` masque des fonctions Typst** : dans le canevas, `rotate`, `scale`, `line`, `rect`, `circle`, `grid`, `content` sont ceux de cetz. `rotate(-30deg)[texte]` y échoue (« Rotate takes a single z-angle… ») : incliner un texte par `content(p, [texte], angle: 30deg)`, ou appeler la fonction Typst par `std.rotate(…)`.
- **`grid` part du premier coin** : `grid((-3.5, -2.5), (4.5, 3.5))` trace des lignes aux demi-unités, alors que `\draw (-3.5,-2.5) grid (4.5,3.5)` de TikZ les trace aux entiers. Pour un quadrillage TikZ à bords non entiers, tracer les lignes entières par deux boucles `for`.
- **Unités** : un nombre (coordonnée, `radius`, `padding` numérique) est en unités du canevas, donc multiplié par `length:`. Un `\fill (A) circle (2pt)` de TikZ dans un canevas `length: 0.8cm` devient `radius: 0.09` (2 pt ≈ 0,07 cm, divisé par 0,8) ; une longueur Typst (`radius: 2pt`, `padding: 3pt`) reste absolue.
- **Interpolation** : `(a, 50%, b)` ; un nombre seul (`(a, 0.5, b)`) est une distance, pas une fraction.
- **Une figure qui dépend de la version** (pointillés de correction) : `context { let prof = … ; cetz.canvas({ … if prof { … } }) }` — les fonctions qui lisent l'état du document exigent `context`.

## Traduire une figure TikZ

1. Relever le repère (unités, `scale`, `x=`, `y=`) → `length:` du canevas.
2. Les `\coordinate` deviennent des `let A = (x, y)` en tête : la figure reste lisible et se modifie à un seul endroit.
3. Les styles `\tikzset{…}` deviennent des fonctions locales (`let croix(p, nom) = { … }`) ou un `set-style`.
4. Les `\foreach` deviennent des `for`.
5. Compiler, regarder le PNG à côté de la figure LaTeX : l'ordre des ancres (`anchor: "south"` place le texte AU-DESSUS du point, comme `[above]`) est la source d'erreur la plus fréquente.
6. Une figure trop lourde à traduire (calques, `\clip`, décorations) : la simplifier en une figure équivalente pour l'élève et le dire.
