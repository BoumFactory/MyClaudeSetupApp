# Animation Produit Scalaire - Guide pour agents

## Structure du projet

```
Animation_Produit_scalaire/
├── index.html              # Point d'entrée (charger via serveur local)
├── CLAUDE.md               # Ce fichier
├── build_monolith.py       # Script de génération fichier unique
├── css/
│   ├── main.css            # Styles principaux + MathJax overlay
│   ├── timeline.css        # Styles timeline
│   └── interactive.css     # Styles mode interactif
└── js/
    ├── math-utils.js       # NE PAS MODIFIER - Utilitaires math
    ├── canvas-renderer.js  # NE PAS MODIFIER - Rendu canvas
    ├── animation-core.js   # NE PAS MODIFIER - Boucle animation
    ├── timeline.js         # NE PAS MODIFIER - Gestion timeline
    ├── controls.js         # NE PAS MODIFIER - Contrôles UI
    ├── render-helpers.js   # RÉFÉRENCE - Fonctions de rendu (drawTextBox, drawMathBox)
    ├── animation-logic.js  # Mode interactif (modifiable)
    ├── scenes.js           # Chargement des scènes
    ├── main.js             # Point d'entrée JS
    └── scenarios/          # ⭐ SCÈNES À MODIFIER
        ├── index.js        # Registre des scènes
        ├── 01-intro.js
        ├── 02-norme.js
        ├── 03-deux-vecteurs.js
        ├── 04-angle.js
        ├── 05-calcul-geometrique.js
        ├── 06-projection.js
        ├── 07-analytique.js
        ├── 08-orthogonalite.js
        ├── 09-signe.js
        └── 10-recap.js
```

## Fichiers monolithes (NE PAS MODIFIER)

Les fichiers `.html` à la racine (sauf `index.html`) sont des **monolithes générés** :
- `produit_scalaire.html`
- `produit_scalaire_v2.html`
- `produit_scalaire_final.html`
- `produit_scalaire_latex.html`

**IMPORTANT** : Ne jamais modifier ces fichiers directement. Modifier les sources JS/CSS puis régénérer avec :
```bash
python build_monolith.py -o nom_fichier.html
```

## Système de rendu des formules

### Deux options disponibles

#### 1. drawTextBox (Canvas natif - recommandé pour texte simple)

```javascript
drawTextBox(renderer, 'u · v = ||u|| × ||v|| × cos(θ)', -9, 2, {
    font: 'bold 20px Arial',
    color: '#1e3a8a',
    align: 'left'
});
```

Utilise des caractères Unicode directement. Rapide et efficace.

#### 2. drawMathBox (MathJax - pour LaTeX complexe)

```javascript
drawMathBox('id-formule', '\\vec{u} \\cdot \\vec{v} = \\|\\vec{u}\\| \\times \\|\\vec{v}\\| \\times \\cos(\\theta)', -9, 2, {
    align: 'left',
    fontSize: '1.4em'
});
```

Rendu LaTeX complet via overlay HTML. Pour fractions, racines complexes, vecteurs avec flèches.

### Caractères Unicode utiles

| Symbole | Description |
|---------|-------------|
| √ | Racine carrée |
| × | Multiplication |
| · | Produit scalaire |
| θ | Theta |
| ² | Exposant 2 |
| ⊥ | Perpendiculaire |
| ⟺ | Équivalence |
| → | Flèche |

## Positionnement des éléments

### RÈGLE FONDAMENTALE

Le repère s'étend de **-15 à +15** sur chaque axe. Les textes doivent être positionnés loin du centre.

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

**Coordonnées recommandées** :
- Formules/explications à gauche : **x = -9**
- Animation graphique au centre : x ∈ [-4, 6]
- Remarques en bas : y = -4

### Exemple de bon positionnement

```javascript
// Formules empilées à gauche
drawTextBox(renderer, '||u|| = √25 = 5', -9, 3, { align: 'left' });
drawTextBox(renderer, '||v|| = √18 ≈ 4.24', -9, 2, { align: 'left' });
drawTextBox(renderer, 'θ = 45°', -9, 1, { align: 'left' });

// Animation centrée
renderer.drawVector(0, 0, 4, 3, { color: '#ef4444' });

// Remarque en bas
drawResultBox(renderer, 'Même résultat !', 0, -4, {});
```

## Bonnes pratiques

1. **Toujours utiliser `align: 'left'`** pour les formules à gauche
2. **Empiler verticalement** avec y décroissant (3, 2, 1, 0, -1...)
3. **Utiliser drawResultBox** pour les résultats finaux (vert avec bordure)
4. **Prévoir 30% de temps de lecture** avec `getProgressWithDelay(progress, 0.70)`

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

## Régénérer le monolithe

Après modifications :
```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\1ere_spe\Sequence-Produit_scalaire\Animation_Produit_scalaire"
python build_monolith.py -o produit_scalaire.html
```

## Test local

```bash
python -m http.server 8000
# Ouvrir http://localhost:8000
```
