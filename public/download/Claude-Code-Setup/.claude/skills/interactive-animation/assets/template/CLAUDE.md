# Animation Interactive - Guide de structure

Ce document aide les agents à se repérer dans la structure du template d'animation.

## Structure des fichiers

```
animation/
├── index.html              # Structure HTML principale (MathJax inclus)
├── CLAUDE.md               # Ce fichier (guide pour agents)
├── build_monolith.py       # Script de génération du fichier unique
├── css/
│   ├── main.css            # Styles de base + overlay MathJax + transitions
│   ├── timeline.css        # Styles de la timeline
│   └── interactive.css     # Styles du mode interactif
└── js/
    ├── math-utils.js       # NE PAS MODIFIER - Utilitaires math + easings
    ├── canvas-renderer.js  # NE PAS MODIFIER - Rendu canvas avec repère
    ├── animation-core.js   # NE PAS MODIFIER - Boucle d'animation
    ├── timeline.js         # NE PAS MODIFIER - Gestion timeline et lecture
    ├── controls.js         # NE PAS MODIFIER - Contrôles UI
    ├── render-helpers.js   # IMPORTANT: drawTextBox, drawMathBox, MathOverlay
    ├── animation-logic.js  # Mode interactif (à éditer)
    ├── scenes.js           # Charge les scènes depuis scenarios/
    ├── main.js             # Point d'entrée
    └── scenarios/          # ⭐ SCÈNES À MODIFIER
        ├── index.js        # Registre des scènes
        └── 01-intro.js     # Scène 1 (template)
```

## Monolithes générés

Les fichiers `.html` générés par `build_monolith.py` sont des monolithes autonomes.

**IMPORTANT** : Ne jamais modifier les monolithes directement. Modifier les sources JS/CSS puis régénérer.

## Système de rendu des formules (LaTeX)

### 1. drawTextBox - Texte simple avec Unicode

Pour du texte simple ou des formules courtes avec caractères Unicode :

```javascript
drawTextBox(renderer, 'u · v = ||u|| × ||v|| × cos(θ)', -9, 2, {
    font: 'bold 20px Arial',
    color: '#1e3a8a',
    align: 'left'
});
```

**Caractères Unicode utiles** : √ × · θ ² ⊥ ⟺ →

### 2. drawMathBox - LaTeX complet avec MathJax

Pour des formules complexes (fractions, racines, vecteurs avec flèches) :

```javascript
drawMathBox('id-formule', '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\cos(\\theta)', -9, 2, {
    align: 'left',
    fontSize: '1.4em'
});

// Résultat mis en valeur
drawMathResult('result', '\\vec{u} \\cdot \\vec{v} = 12', 0, -3);
```

### 3. Cycle de vie MathOverlay

Pour les scènes avec formules dynamiques :

```javascript
animate(localTime, progress, renderer, state) {
    MathOverlay.beginFrame();  // Marquer éléments comme inactifs

    // Afficher les formules
    if (progress > 0.3) {
        drawMathBox('formule', 'LaTeX...', x, y, { opacity: fadeIn(progress, 0.3, 0.5) });
    }

    MathOverlay.endFrame();    // Supprimer les éléments non utilisés
}
```

## Positionnement des éléments

### RÈGLE FONDAMENTALE

Le repère s'étend de **-15 à +15** sur chaque axe. Les textes doivent être positionnés **loin du centre** pour éviter les chevauchements.

### Zones recommandées

```
┌───────────────────────────────────────────────────────────────┐
│    ZONE GAUCHE     │      ZONE CENTRE       │   ZONE DROITE   │
│  (infos/formules)  │      (animation)       │   (infos opt.)  │
│    x = -9          │     x ∈ [-4, 6]        │   x ∈ [8, 12]   │
├────────────────────┴────────────────────────┴─────────────────┤
│                    ZONE BAS (remarques) y ∈ [-4, -5]          │
└───────────────────────────────────────────────────────────────┘
```

**Coordonnées clés** :
- Formules à gauche : **x = -9** avec `align: 'left'`
- Animation au centre : x ∈ [-4, 6]
- Remarques en bas : y = -4

### Exemple de bon positionnement

```javascript
// Formules empilées à gauche
drawTextBox(renderer, '||u|| = 5', -9, 3, { align: 'left' });
drawTextBox(renderer, '||v|| = 4.24', -9, 2, { align: 'left' });
drawTextBox(renderer, 'θ = 45°', -9, 1, { align: 'left' });

// Animation centrée
renderer.drawVector(0, 0, 4, 3, { color: '#ef4444' });

// Remarque en bas
drawResultBox(renderer, 'Même résultat !', 0, -4);
```

## API principales

### drawTextBox(renderer, text, x, y, options)

Options : font, color, bgColor, padding, borderRadius, align, opacity, borderColor, borderWidth, shadow

### drawMathBox(id, latex, x, y, options)

Options : color, fontSize, bgColor, padding, borderRadius, opacity, align, borderColor, borderWidth, shadow

### drawMathResult(id, latex, x, y, options)

Comme drawMathBox mais avec style "résultat" (vert avec bordure).

### drawResultBox(renderer, text, x, y, options)

Version canvas de la boîte résultat.

### getProgressWithDelay(progress, contentEnd = 0.85)

Retourne : { contentProgress, isInDelay, delayProgress }

## Bonnes pratiques

1. **Délai de fin** : `getProgressWithDelay(progress, 0.70)` pour 30% de temps de lecture
2. **Durées généreuses** : 8000-15000ms par scène
3. **Alignement gauche** : Toujours `align: 'left'` pour les formules à gauche
4. **Empiler verticalement** : y décroissant (3, 2, 1, 0, -1...)
5. **Transitions fluides** : fadeIn(), slideIn() pour les apparitions

## RÈGLE CRITIQUE : LaTeX statique vs valeurs dynamiques

**PROBLÈME** : Si le contenu LaTeX change à chaque frame, MathJax recompile en boucle → freeze/bug.

**SOLUTION** : Séparer en deux éléments adjacents :

```javascript
// ❌ MAUVAIS - recompile MathJax à chaque frame
drawMathBox('result', `\\vec{u} \\cdot \\vec{v} = ${dotProduct}`, -9, 3, {...});

// ✅ BON - LaTeX statique + valeur canvas séparée
drawMathBox('label', '\\vec{u} \\cdot \\vec{v} =', -9, 3, { align: 'left' });
drawTextBox(renderer, MathUtils.format(dotProduct, 1), -5.5, 3, {
    font: 'bold 26px Arial', color: color
});
```

**Appliquer cette règle quand** :
- Une valeur change en continu (animation de rotation, slider)
- Mode interactif avec paramètres modifiables

## Génération du monolithe

```bash
python build_monolith.py -o animation.html
```
