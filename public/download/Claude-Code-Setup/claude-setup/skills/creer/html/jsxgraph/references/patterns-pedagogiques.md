# Patterns pédagogiques JSXGraph

Exemples réutilisables organisés par niveau et thème.

## Collège (6e-3e)

### Symétrie axiale

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-8, 8, 8, -8], axis: true, grid: true
});

// Axe de symétrie (droite verticale)
const d = board.create('line', [[0, 0], [0, 1]], {
    strokeColor: 'red', strokeWidth: 2, name: 'd'
});

// Point A déplaçable
const A = board.create('point', [-3, 2], {name: 'A', color: 'blue', size: 4});

// Symétrique A'
const A_sym = board.create('reflection', [A, d], {
    name: "A'", color: 'green', size: 4
});

// Segment [AA']
board.create('segment', [A, A_sym], {strokeColor: 'gray', dash: 2});

// Instruction
board.create('text', [-7, 7, 'Déplace le point A'], {fontSize: 14});
```

### Théorème de Pythagore (visualisation des aires)

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-2, 10, 12, -2], axis: false, grid: false
});

// Triangle rectangle
const A = board.create('point', [0, 0], {name: 'A', fixed: true});
const B = board.create('point', [4, 0], {name: 'B', fixed: true});
const C = board.create('point', [4, 3], {name: 'C', fixed: true});

board.create('polygon', [A, B, C], {
    fillColor: 'transparent',
    borders: {strokeColor: 'black', strokeWidth: 2}
});

// Carrés sur chaque côté
// Carré sur AB (côté a)
const carrAB = board.create('regularpolygon', [A, B, 4], {
    fillColor: 'lightblue', fillOpacity: 0.5,
    borders: {strokeColor: 'blue'}
});

// Carré sur BC (côté b)
const carrBC = board.create('regularpolygon', [B, C, 4], {
    fillColor: 'lightgreen', fillOpacity: 0.5,
    borders: {strokeColor: 'green'}
});

// Carré sur AC (hypoténuse c)
const carrAC = board.create('regularpolygon', [C, A, 4], {
    fillColor: 'lightyellow', fillOpacity: 0.5,
    borders: {strokeColor: 'orange'}
});

// Calcul des aires
const aireAB = () => Math.pow(A.Dist(B), 2);
const aireBC = () => Math.pow(B.Dist(C), 2);
const aireAC = () => Math.pow(A.Dist(C), 2);

board.create('text', [6, 8, () =>
    `a² = ${aireAB().toFixed(1)}`
], {color: 'blue', fontSize: 14});

board.create('text', [6, 7, () =>
    `b² = ${aireBC().toFixed(1)}`
], {color: 'green', fontSize: 14});

board.create('text', [6, 6, () =>
    `c² = ${aireAC().toFixed(1)}`
], {color: 'orange', fontSize: 14});

board.create('text', [6, 4.5, () =>
    `a² + b² = ${(aireAB() + aireBC()).toFixed(1)}`
], {fontSize: 14, color: 'purple'});
```

### Proportionnalité et graphique

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-1, 12, 12, -1], axis: true, grid: true
});

// Coefficient de proportionnalité
const k = board.create('slider', [[1, 11], [6, 11], [0.5, 2, 4]], {name: 'k'});

// Droite y = kx
const droite = board.create('functiongraph', [
    x => k.Value() * x
], {strokeColor: 'blue', strokeWidth: 2});

// Points exemples
const points = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D']];
points.forEach(([x, name]) => {
    board.create('point', [x, () => k.Value() * x], {
        name: name, color: 'red', size: 4
    });
});

// Affichage équation
board.create('text', [7, 10, () =>
    `y = ${k.Value().toFixed(1)}x`
], {fontSize: 18, color: 'blue'});
```

## Lycée (2nde)

### Fonction affine et variations

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-8, 8, 8, -8], axis: true, grid: true
});

// Paramètres m et p
const m = board.create('slider', [[-7, 7], [-3, 7], [-3, 1, 3]], {name: 'm'});
const p = board.create('slider', [[-7, 6], [-3, 6], [-5, 0, 5]], {name: 'p'});

// Droite f(x) = mx + p
const f = board.create('functiongraph', [
    x => m.Value() * x + p.Value()
], {strokeColor: 'blue', strokeWidth: 2});

// Point d'ordonnée à l'origine
const origine = board.create('point', [0, () => p.Value()], {
    name: '', color: 'green', size: 5, fixed: true
});

// Indication du sens de variation
board.create('text', [3, 7, () => {
    if (m.Value() > 0) return 'Fonction CROISSANTE ↗';
    if (m.Value() < 0) return 'Fonction DÉCROISSANTE ↘';
    return 'Fonction CONSTANTE →';
}], {fontSize: 14, color: 'darkblue'});

// Équation
board.create('text', [3, 5.5, () =>
    `f(x) = ${m.Value().toFixed(1)}x + ${p.Value().toFixed(1)}`
], {fontSize: 16});
```

### Vecteurs et coordonnées

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-6, 6, 6, -6], axis: true, grid: true
});

// Points A et B déplaçables
const A = board.create('point', [-2, -1], {name: 'A', color: 'blue', size: 4});
const B = board.create('point', [3, 2], {name: 'B', color: 'blue', size: 4});

// Vecteur AB
const vecAB = board.create('arrow', [A, B], {
    strokeColor: 'red', strokeWidth: 3
});

// Coordonnées du vecteur
board.create('text', [-5, 5, () =>
    `A(${A.X().toFixed(1)} ; ${A.Y().toFixed(1)})`
], {fontSize: 14});

board.create('text', [-5, 4.3, () =>
    `B(${B.X().toFixed(1)} ; ${B.Y().toFixed(1)})`
], {fontSize: 14});

board.create('text', [-5, 3.3, () =>
    `→AB (${(B.X() - A.X()).toFixed(1)} ; ${(B.Y() - A.Y()).toFixed(1)})`
], {fontSize: 16, color: 'red'});

board.create('text', [-5, 2.3, () =>
    `||→AB|| = ${A.Dist(B).toFixed(2)}`
], {fontSize: 14, color: 'purple'});
```

## Lycée (1ère)

### Dérivée et tangente

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-5, 10, 5, -3], axis: true, grid: true
});

// Fonction f(x) = x²
const f = x => x * x;
const fPrime = x => 2 * x;

// Courbe
board.create('functiongraph', [f], {
    strokeColor: 'blue', strokeWidth: 2, name: 'Cf'
});

// Point de tangence (abscisse mobile)
const a = board.create('slider', [[-4, 9], [0, 9], [-3, 1, 3]], {name: 'a'});

// Point sur la courbe
const M = board.create('point', [
    () => a.Value(),
    () => f(a.Value())
], {name: 'M', color: 'red', size: 5});

// Tangente en M : y = f'(a)(x - a) + f(a)
const tangente = board.create('functiongraph', [
    x => fPrime(a.Value()) * (x - a.Value()) + f(a.Value())
], {strokeColor: 'green', strokeWidth: 2, dash: 2});

// Affichages
board.create('text', [1.5, 9, () =>
    `a = ${a.Value().toFixed(2)}`
], {fontSize: 14});

board.create('text', [1.5, 8, () =>
    `f(a) = ${f(a.Value()).toFixed(2)}`
], {fontSize: 14, color: 'blue'});

board.create('text', [1.5, 7, () =>
    `f'(a) = ${fPrime(a.Value()).toFixed(2)}`
], {fontSize: 14, color: 'green'});

board.create('text', [1.5, 5.5, () =>
    `Tangente : y = ${fPrime(a.Value()).toFixed(1)}(x - ${a.Value().toFixed(1)}) + ${f(a.Value()).toFixed(1)}`
], {fontSize: 12, color: 'green'});
```

### Suites géométriques

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-1, 20, 12, -2], axis: true, grid: true
});

// Paramètres
const u0 = board.create('slider', [[1, 19], [5, 19], [0.5, 1, 3]], {name: 'u₀'});
const q = board.create('slider', [[1, 18], [5, 18], [0.5, 1.5, 2.5]], {name: 'q'});

// Calcul des termes
const termes = [];
for (let n = 0; n <= 10; n++) {
    const point = board.create('point', [
        n,
        () => u0.Value() * Math.pow(q.Value(), n)
    ], {
        name: n === 0 ? 'u₀' : '',
        color: 'red',
        size: 3
    });
    termes.push(point);

    // Segments verticaux
    if (n > 0) {
        board.create('segment', [
            [n, 0],
            termes[n]
        ], {strokeColor: 'gray', strokeWidth: 1, dash: 2});
    }
}

// Relier les points
for (let n = 0; n < 10; n++) {
    board.create('segment', [termes[n], termes[n + 1]], {
        strokeColor: 'blue', strokeWidth: 2
    });
}

// Formule
board.create('text', [6, 18, () =>
    `uₙ = ${u0.Value().toFixed(1)} × ${q.Value().toFixed(2)}ⁿ`
], {fontSize: 16, color: 'blue'});

// Indication comportement
board.create('text', [6, 16.5, () => {
    if (q.Value() > 1) return 'Suite croissante (q > 1)';
    if (q.Value() < 1) return 'Suite décroissante (q < 1)';
    return 'Suite constante (q = 1)';
}], {fontSize: 14, color: 'darkgreen'});
```

## Lycée (Terminale)

### Intégrale et aire sous la courbe

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-1, 5, 8, -1], axis: true, grid: true
});

// Fonction
const f = x => 0.5 * x * x - 2 * x + 3;

// Courbe
board.create('functiongraph', [f, 0, 7], {
    strokeColor: 'blue', strokeWidth: 2
});

// Bornes d'intégration
const a = board.create('slider', [[1, 4.5], [3, 4.5], [0, 1, 4]], {name: 'a'});
const b = board.create('slider', [[4, 4.5], [6, 4.5], [2, 5, 7]], {name: 'b'});

// Aire sous la courbe (rectangles de Riemann)
const n = 20;
for (let i = 0; i < n; i++) {
    board.create('polygon', [
        [() => a.Value() + i * (b.Value() - a.Value()) / n, 0],
        [() => a.Value() + i * (b.Value() - a.Value()) / n,
         () => f(a.Value() + i * (b.Value() - a.Value()) / n)],
        [() => a.Value() + (i + 1) * (b.Value() - a.Value()) / n,
         () => f(a.Value() + i * (b.Value() - a.Value()) / n)],
        [() => a.Value() + (i + 1) * (b.Value() - a.Value()) / n, 0]
    ], {
        fillColor: 'lightblue',
        fillOpacity: 0.5,
        borders: {strokeColor: 'blue', strokeWidth: 0.5}
    });
}

// Calcul approché de l'intégrale (méthode des rectangles)
const integrale = () => {
    let sum = 0;
    const dx = (b.Value() - a.Value()) / 100;
    for (let x = a.Value(); x < b.Value(); x += dx) {
        sum += f(x) * dx;
    }
    return sum;
};

board.create('text', [1, -0.5, () =>
    `∫ f(x)dx ≈ ${integrale().toFixed(3)}`
], {fontSize: 16, color: 'blue'});
```

### Probabilités - Loi normale

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-5, 0.5, 5, -0.1], axis: true, grid: false
});

// Paramètres
const mu = board.create('slider', [[-4, 0.45], [-1, 0.45], [-2, 0, 2]], {name: 'μ'});
const sigma = board.create('slider', [[0, 0.45], [3, 0.45], [0.3, 1, 2]], {name: 'σ'});

// Densité de la loi normale
const normale = x => {
    const s = sigma.Value();
    const m = mu.Value();
    return (1 / (s * Math.sqrt(2 * Math.PI))) *
           Math.exp(-0.5 * Math.pow((x - m) / s, 2));
};

// Courbe de Gauss
board.create('functiongraph', [normale, -5, 5], {
    strokeColor: 'blue', strokeWidth: 2
});

// Ligne verticale pour la moyenne
board.create('line', [
    [() => mu.Value(), 0],
    [() => mu.Value(), 1]
], {
    strokeColor: 'red', dash: 2, straightFirst: false, straightLast: false
});

// Annotation
board.create('text', [() => mu.Value(), 0.42, 'μ'], {
    color: 'red', fontSize: 16
});

board.create('text', [2.5, 0.35, () =>
    `N(${mu.Value().toFixed(1)} ; ${sigma.Value().toFixed(2)}²)`
], {fontSize: 14, color: 'blue'});
```

## Géométrie dans l'espace (représentation 2D)

### Perspective cavalière d'un cube

```javascript
const board = JXG.JSXGraph.initBoard('box', {
    boundingbox: [-2, 6, 8, -2], axis: false, grid: false
});

// Paramètre taille
const c = 3;
const angle = Math.PI / 6;
const ratio = 0.5;

// Sommets face avant
const A = board.create('point', [0, 0], {name: 'A', size: 2});
const B = board.create('point', [c, 0], {name: 'B', size: 2});
const C = board.create('point', [c, c], {name: 'C', size: 2});
const D = board.create('point', [0, c], {name: 'D', size: 2});

// Sommets face arrière (décalage en perspective)
const dx = c * ratio * Math.cos(angle);
const dy = c * ratio * Math.sin(angle);

const E = board.create('point', [dx, dy], {name: 'E', size: 2});
const F = board.create('point', [c + dx, dy], {name: 'F', size: 2});
const G = board.create('point', [c + dx, c + dy], {name: 'G', size: 2});
const H = board.create('point', [dx, c + dy], {name: 'H', size: 2});

// Arêtes visibles (trait plein)
board.create('segment', [A, B], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [B, C], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [C, D], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [D, A], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [B, F], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [C, G], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [D, H], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [F, G], {strokeColor: 'black', strokeWidth: 2});
board.create('segment', [G, H], {strokeColor: 'black', strokeWidth: 2});

// Arêtes cachées (pointillés)
board.create('segment', [A, E], {strokeColor: 'gray', dash: 2});
board.create('segment', [E, F], {strokeColor: 'gray', dash: 2});
board.create('segment', [E, H], {strokeColor: 'gray', dash: 2});
```

## Templates réutilisables

### Structure HTML complète avec style moderne

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Graphique interactif</title>
    <link rel="stylesheet" href="https://jsxgraph.org/distrib/jsxgraph.css">
    <script src="https://jsxgraph.org/distrib/jsxgraphcore.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        header {
            background: #2d3748;
            color: white;
            padding: 20px 30px;
        }
        header h1 { font-size: 1.5rem; font-weight: 600; }
        header p { opacity: 0.8; margin-top: 5px; font-size: 0.9rem; }
        #box {
            width: 100%;
            height: 500px;
            background: #f7fafc;
        }
        .instructions {
            padding: 20px 30px;
            background: #edf2f7;
            border-top: 1px solid #e2e8f0;
        }
        .instructions h3 {
            color: #2d3748;
            margin-bottom: 10px;
        }
        .instructions ul {
            color: #4a5568;
            padding-left: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Titre du graphique</h1>
            <p>Description courte</p>
        </header>
        <div id="box"></div>
        <div class="instructions">
            <h3>Comment utiliser</h3>
            <ul>
                <li>Déplacez les sliders pour modifier les paramètres</li>
                <li>Cliquez et glissez les points pour les déplacer</li>
            </ul>
        </div>
    </div>
    <script>
        // Code JSXGraph ici
    </script>
</body>
</html>
```
