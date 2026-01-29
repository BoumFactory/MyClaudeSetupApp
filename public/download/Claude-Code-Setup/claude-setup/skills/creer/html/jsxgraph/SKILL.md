---
name: jsxgraph-creator
description: Skill spécialisé pour créer des graphiques mathématiques interactifs avec JSXGraph. Génère des pages HTML autonomes avec visualisations de fonctions, constructions géométriques, sliders dynamiques et animations. Optimisé pour l'enseignement des mathématiques.
---

# JSXGraph Creator Skill

Skill pour la création de graphiques mathématiques interactifs en HTML avec la bibliothèque JSXGraph.

## Quand utiliser ce skill

- Graphiques de fonctions interactifs avec paramètres modifiables
- Constructions géométriques dynamiques
- Visualisations pour l'enseignement (calcul, géométrie, analyse)
- Démonstrations de théorèmes avec manipulation directe
- Animations mathématiques contrôlées par sliders

## Structure HTML de base

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Titre du graphique</title>
    <link rel="stylesheet" href="https://jsxgraph.org/distrib/jsxgraph.css">
    <script src="https://jsxgraph.org/distrib/jsxgraphcore.js"></script>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        #box { margin: 20px auto; border: 1px solid #ddd; }
    </style>
</head>
<body>
    <h1>Titre</h1>
    <div id="box" style="width: 600px; height: 400px;"></div>

    <script>
        // Code JSXGraph ici
    </script>
</body>
</html>
```

## Initialisation du Board

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-6, 10, 6, -4],  // [xmin, ymax, xmax, ymin]
    axis: true,
    grid: true,
    showNavigation: false,         // Cache boutons de navigation
    showCopyright: false,          // Cache copyright
    keepAspectRatio: true          // Ratio 1:1
});
```

### Options du boundingbox
- Format : `[xmin, ymax, xmax, ymin]`
- Exemple classique : `[-10, 10, 10, -10]` pour un repère centré
- Pour les fonctions : `[-6, 10, 6, -2]` (plus de place en hauteur)

## Types d'éléments

### Points

```javascript
// Point fixe
const A = board.create('point', [2, 3], {
    name: 'A',
    color: 'blue',
    size: 4,
    fixed: true              // Non déplaçable
});

// Point libre (déplaçable)
const B = board.create('point', [0, 0], {
    name: 'B',
    color: 'red',
    size: 5
});

// Point dépendant (glisseur sur élément)
const C = board.create('glider', [0, 0, line], {
    name: 'C',
    color: 'green'
});

// Point défini par fonction
const D = board.create('point', [
    () => A.X() + 1,
    () => A.Y() * 2
], {name: 'D'});
```

### Segments et Droites

```javascript
// Segment entre deux points
const segment = board.create('segment', [A, B], {
    strokeColor: 'blue',
    strokeWidth: 2
});

// Droite passant par deux points
const line = board.create('line', [A, B], {
    strokeColor: 'black',
    strokeWidth: 1
});

// Droite par équation ax + by + c = 0
const line2 = board.create('line', [1, 2, -3], {
    strokeColor: 'gray',
    dash: 2        // Tirets
});

// Demi-droite
const ray = board.create('line', [A, B], {
    straightFirst: false,  // S'arrête au premier point
    straightLast: true
});

// Perpendiculaire
const perp = board.create('perpendicular', [line, C], {
    strokeColor: 'purple'
});

// Parallèle
const para = board.create('parallel', [line, C], {
    strokeColor: 'orange'
});
```

### Cercles

```javascript
// Cercle par centre et point
const circle = board.create('circle', [A, B], {
    strokeColor: 'blue',
    fillColor: 'lightblue',
    fillOpacity: 0.3
});

// Cercle par centre et rayon
const circle2 = board.create('circle', [A, 3], {
    strokeColor: 'red'
});

// Cercle par rayon dynamique
const circle3 = board.create('circle', [A, () => slider.Value()], {
    strokeColor: 'green'
});

// Arc de cercle
const arc = board.create('arc', [center, pointStart, pointEnd], {
    strokeColor: 'blue',
    strokeWidth: 3
});

// Secteur
const sector = board.create('sector', [center, pointStart, pointEnd], {
    fillColor: 'yellow',
    fillOpacity: 0.5
});
```

### Polygones

```javascript
// Triangle
const triangle = board.create('polygon', [A, B, C], {
    fillColor: 'lightgreen',
    fillOpacity: 0.4,
    borders: {
        strokeColor: 'darkgreen',
        strokeWidth: 2
    }
});

// Polygone régulier
const hexagon = board.create('regularpolygon', [A, B, 6], {
    fillColor: 'lightblue'
});
```

### Fonctions

```javascript
// Fonction simple
const f = board.create('functiongraph', [
    x => Math.sin(x)
], {
    strokeColor: 'blue',
    strokeWidth: 2
});

// Fonction avec domaine limité
const g = board.create('functiongraph', [
    x => x * x,
    -3,    // xmin
    3      // xmax
], {strokeColor: 'red'});

// Fonction dépendant de paramètres (sliders)
const h = board.create('functiongraph', [
    x => a.Value() * x * x + b.Value() * x + c.Value()
], {strokeColor: 'purple'});

// Courbe paramétrique
const param = board.create('curve', [
    t => 2 * Math.cos(t),    // x(t)
    t => Math.sin(t),         // y(t)
    0,                        // tmin
    2 * Math.PI               // tmax
], {strokeColor: 'orange'});

// Courbe polaire
const polar = board.create('curve', [
    phi => 2 + Math.cos(3 * phi),  // r(phi)
    [0, 2 * Math.PI]                // domaine
], {
    curveType: 'polar',
    strokeColor: 'magenta'
});
```

### Vecteurs

```javascript
// Vecteur de A vers B
const vec = board.create('arrow', [A, B], {
    strokeColor: 'red',
    strokeWidth: 3
});

// Vecteur par coordonnées depuis un point
const vec2 = board.create('arrow', [
    [0, 0],
    [3, 2]
], {strokeColor: 'blue'});
```

## Sliders (Paramètres interactifs)

```javascript
// Slider horizontal
const a = board.create('slider', [
    [-5, 8],      // Position début
    [-1, 8],      // Position fin
    [-2, 1, 2]    // [min, valeur initiale, max]
], {
    name: 'a',
    snapWidth: 0.1,           // Pas de graduation
    precision: 1,             // Décimales affichées
    withTicks: true,          // Graduations visibles
    suffixLabel: ' unités'    // Suffixe après la valeur
});

// Récupérer la valeur
const valeur = a.Value();

// Slider vertical
const b = board.create('slider', [
    [5, -3],
    [5, 3],
    [0, 0, 10]
], {name: 'b', isVertical: true});
```

## Textes et Labels

```javascript
// Texte statique
board.create('text', [2, 5, 'Texte simple'], {
    fontSize: 16,
    color: 'blue'
});

// Texte dynamique (avec fonction)
board.create('text', [2, 4, () =>
    'a = ' + a.Value().toFixed(2)
], {fontSize: 14});

// Texte avec LaTeX (si MathJax chargé)
board.create('text', [0, -3,
    '\\(f(x) = x^2\\)'
], {useMathJax: true});

// Texte HTML (formules complexes)
board.create('text', [0, 6, () =>
    `f(x) = ${a.Value().toFixed(1)}x² + ${b.Value().toFixed(1)}x + ${c.Value().toFixed(1)}`
], {fontSize: 18});
```

## Transformations géométriques

```javascript
// Translation
const translation = board.create('transform', [2, 3], {type: 'translate'});
const A_prime = board.create('point', [A, translation], {name: "A'"});

// Rotation
const rotation = board.create('transform', [Math.PI/4, center], {type: 'rotate'});
const B_prime = board.create('point', [B, rotation], {name: "B'"});

// Symétrie axiale
const reflexion = board.create('reflection', [A, line], {name: "A'"});

// Homothétie
const homothetie = board.create('transform', [2, center], {type: 'scale'});
```

## Intersections

```javascript
// Intersection de deux droites
const I = board.create('intersection', [line1, line2, 0], {
    name: 'I',
    color: 'red'
});

// Intersections cercle/droite (deux points possibles)
const P1 = board.create('intersection', [circle, line, 0], {name: 'P1'});
const P2 = board.create('intersection', [circle, line, 1], {name: 'P2'});

// Intersections de deux cercles
const Q1 = board.create('intersection', [circle1, circle2, 0]);
const Q2 = board.create('intersection', [circle1, circle2, 1]);
```

## Mesures et Angles

```javascript
// Angle entre trois points
const angle = board.create('angle', [A, B, C], {
    radius: 0.8,
    name: 'α',
    withLabel: true
});

// Afficher mesure de l'angle
board.create('text', [3, 3, () =>
    'α = ' + (angle.Value() * 180 / Math.PI).toFixed(1) + '°'
]);

// Distance entre deux points
const dist = () => A.Dist(B);
board.create('text', [0, -2, () =>
    'AB = ' + dist().toFixed(2)
]);

// Milieu
const M = board.create('midpoint', [A, B], {name: 'M'});
```

## Animations

```javascript
// Animation automatique d'un point sur un cercle
const movingPoint = board.create('glider', [1, 0, circle]);

// Fonction d'animation
function animate() {
    const t = Date.now() / 1000;
    const x = 2 * Math.cos(t);
    const y = 2 * Math.sin(t);
    movingPoint.moveTo([x, y], 0);
    requestAnimationFrame(animate);
}
animate();

// Animation avec slider (contrôle manuel)
const t = board.create('slider', [[−5, −3], [5, −3], [0, 0, 2*Math.PI]], {name: 't'});
const P = board.create('point', [
    () => 2 * Math.cos(t.Value()),
    () => 2 * Math.sin(t.Value())
], {name: 'P', trace: true});  // trace: true laisse une trace
```

## Styles et Attributs communs

### Couleurs
```javascript
{
    strokeColor: 'blue',       // Contour
    fillColor: 'lightblue',    // Remplissage
    fillOpacity: 0.5,          // Opacité (0-1)
    highlightStrokeColor: 'red',  // Survol
    highlightFillColor: 'pink'
}
```

### Tailles et épaisseurs
```javascript
{
    strokeWidth: 2,            // Épaisseur trait
    size: 5,                   // Taille point
    dash: 2,                   // Type tirets (0=plein, 1,2,3,4=tirets)
}
```

### Visibilité et interaction
```javascript
{
    visible: true,
    fixed: true,               // Non déplaçable
    frozen: true,              // Invisible mais actif
    withLabel: true,           // Affiche le nom
    label: {
        offset: [10, 10],      // Décalage du label
        fontSize: 14
    }
}
```

## Exemples pédagogiques complets

### 1. Parabole avec paramètres

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-6, 10, 6, -4],
    axis: true, grid: true
});

// Sliders pour les coefficients
const a = board.create('slider', [[-5, 8], [-1, 8], [-2, 1, 2]], {name: 'a'});
const b = board.create('slider', [[-5, 7], [-1, 7], [-3, 0, 3]], {name: 'b'});
const c = board.create('slider', [[-5, 6], [-1, 6], [-3, 0, 3]], {name: 'c'});

// Parabole
const f = board.create('functiongraph', [
    x => a.Value() * x * x + b.Value() * x + c.Value()
], {strokeColor: 'blue', strokeWidth: 2});

// Sommet
const sommet = board.create('point', [
    () => -b.Value() / (2 * a.Value()),
    () => {
        const xS = -b.Value() / (2 * a.Value());
        return a.Value() * xS * xS + b.Value() * xS + c.Value();
    }
], {name: 'S', color: 'red', size: 5});

// Équation affichée
board.create('text', [1, 8, () =>
    `f(x) = ${a.Value().toFixed(1)}x² + ${b.Value().toFixed(1)}x + ${c.Value().toFixed(1)}`
], {fontSize: 16});
```

### 2. Théorème de Thalès

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-2, 8, 10, -2],
    axis: false, grid: false
});

// Points de base
const A = board.create('point', [0, 0], {name: 'A', fixed: true});
const B = board.create('point', [8, 0], {name: 'B'});
const C = board.create('point', [5, 6], {name: 'C'});

// Triangle ABC
board.create('polygon', [A, B, C], {
    fillColor: 'transparent',
    borders: {strokeColor: 'blue', strokeWidth: 2}
});

// Point M sur [AB]
const M = board.create('glider', [3, 0, board.create('line', [A, B], {visible: false})], {
    name: 'M', color: 'red'
});

// Parallèle à (BC) passant par M
const BC = board.create('line', [B, C], {visible: false});
const parallele = board.create('parallel', [BC, M], {strokeColor: 'green', dash: 2});

// Point N intersection avec (AC)
const AC = board.create('line', [A, C], {visible: false});
const N = board.create('intersection', [parallele, AC, 0], {name: 'N', color: 'red'});

// Affichage des rapports
board.create('text', [0, -1, () =>
    `AM/AB = ${(M.Dist(A) / B.Dist(A)).toFixed(3)}`
], {fontSize: 14});
board.create('text', [4, -1, () =>
    `AN/AC = ${(N.Dist(A) / C.Dist(A)).toFixed(3)}`
], {fontSize: 14});
```

### 3. Cercle trigonométrique

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-2.5, 2.5, 2.5, -2.5],
    axis: true, grid: true, keepAspectRatio: true
});

// Cercle unité
const circle = board.create('circle', [[0, 0], 1], {
    strokeColor: 'black', strokeWidth: 1
});

// Slider pour l'angle
const angle = board.create('slider', [[-2, -2], [2, -2], [0, 0, 2*Math.PI]], {
    name: 'θ', snapWidth: Math.PI/12
});

// Point sur le cercle
const M = board.create('point', [
    () => Math.cos(angle.Value()),
    () => Math.sin(angle.Value())
], {name: 'M', color: 'red', size: 4});

// Projections
const Mx = board.create('point', [() => M.X(), 0], {
    name: '', color: 'blue', size: 3
});
const My = board.create('point', [0, () => M.Y()], {
    name: '', color: 'green', size: 3
});

// Segments de projection
board.create('segment', [M, Mx], {strokeColor: 'blue', dash: 2});
board.create('segment', [M, My], {strokeColor: 'green', dash: 2});

// Affichage cos et sin
board.create('text', [1.5, 2, () =>
    `cos(θ) = ${Math.cos(angle.Value()).toFixed(3)}`
], {color: 'blue'});
board.create('text', [1.5, 1.7, () =>
    `sin(θ) = ${Math.sin(angle.Value()).toFixed(3)}`
], {color: 'green'});
```

## Intégration avec MathJax/KaTeX

Pour des formules LaTeX propres, ajouter MathJax :

```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async
    src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

Puis utiliser `useMathJax: true` :

```javascript
board.create('text', [0, 5, '\\(f(x) = \\frac{1}{x}\\)'], {
    useMathJax: true,
    fontSize: 20
});
```

## Bonnes pratiques

1. **Nommer les éléments** : Utiliser des noms explicites (`const sommet`, pas `const p1`)
2. **Fonctions pour les dépendances** : `() => slider.Value()` plutôt que `slider.Value()`
3. **Limiter les sliders** : Max 3-4 sliders pour éviter la surcharge
4. **Couleurs cohérentes** : Utiliser une palette limitée et significative
5. **Labels clairs** : Positionner les labels pour éviter les chevauchements
6. **Commentaires** : Séparer les sections par des commentaires (sur des lignes dédiées !)

## Erreurs courantes à éviter

### Commentaires sur la même ligne que le code
```javascript
// INCORRECT - tout après // est commenté !
// Créer le point        const A = board.create('point', [0, 0]);

// CORRECT
// Créer le point
const A = board.create('point', [0, 0]);
```

### Oublier les fonctions pour les valeurs dynamiques
```javascript
// INCORRECT - valeur figée à l'initialisation
const f = board.create('functiongraph', [x => a.Value() * x]);

// CORRECT - recalculé à chaque frame
const f = board.create('functiongraph', [
    function(x) { return a.Value() * x; }
]);
```

### boundingbox inversé
```javascript
// Format : [xmin, ymax, xmax, ymin]
// INCORRECT
boundingbox: [-10, -10, 10, 10]  // Y inversé !

// CORRECT
boundingbox: [-10, 10, 10, -10]
```

## Ressources

- [Documentation officielle](https://jsxgraph.org/docs/index.html)
- [Wiki avec exemples](https://jsxgraph.org/wiki/)
- [GitHub](https://github.com/jsxgraph/jsxgraph)
