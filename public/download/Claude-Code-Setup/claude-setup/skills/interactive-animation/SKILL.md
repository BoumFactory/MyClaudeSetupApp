---
name: interactive-animation
description: Skill spécialisé pour créer des animations mathématiques interactives de haute qualité pour l'enseignement. Utiliser ce skill pour générer des animations HTML/JS avec repère orthonormé, contrôles personnalisables, scénarios guidés et export monolithique. Garantit une précision mathématique parfaite et un affichage optimisé pour la projection en classe.
---

# Interactive Animation Skill

Skill pour la création d'animations mathématiques pour l'enseignement.

## Mode Animation (Capsule vidéo)

- **Animations séquentielles** comme Manim ou une capsule vidéo
- **Timeline** avec lecture, pause, navigation
- **Scènes** : chapitres de l'animation
- Les informations apparaissent **au bon moment** dans l'animation
- L'utilisateur **regarde** et contrôle le flux

## IMPORTANT : Exemples de référence

**AVANT de créer une animation**, lire les exemples dans :
```
SKILL_BASE/assets/examples/
```

Ces scénarios du "Produit Scalaire" sont la **référence à suivre** pour :
- Structure des fichiers de scènes
- Utilisation de `drawMathBox` et `drawMathResult` pour le LaTeX
- Positionnement des textes (zone gauche x=-9)
- Gestion des phases dans les animations
- Transitions fluides avec easings
- Durées appropriées par type de scène

## Architecture du template

```
animation-name/
├── index.html              # Structure HTML
├── css/
│   ├── main.css           # Base, variables, layout
│   └── timeline.css       # Timeline, chapitres
├── js/
│   ├── math-utils.js      # Utilitaires mathématiques + easings
│   ├── canvas-renderer.js # Rendu canvas avec repère mathématique
│   ├── animation-core.js  # Boucle d'animation
│   ├── timeline.js        # Gestion timeline et lecture
│   ├── controls.js        # Contrôles UI
│   ├── render-helpers.js  # drawTextBox, drawMathBox, drawMathResult
│   ├── scenes.js          # Charge les scènes depuis scenarios/
│   ├── scenarios/         # ⭐ UN FICHIER PAR SCÈNE
│   │   ├── index.js       # Registre des scènes
│   │   ├── 01-intro.js    # Scène 1
│   │   ├── 02-xxx.js      # Scène 2
│   │   └── ...
│   └── main.js            # Point d'entrée
└── build_monolith.py      # Génération fichier unique
```

## Protocole de création

### Étape 1 : Copier le template

```bash
cp -r "SKILL_BASE/assets/template/*" "[DESTINATION]/"
```

### Étape 2 : Personnaliser index.html

- `<title>` et `.app-title` : Titre de l'animation

### Étape 3 : Implémenter les scènes (Mode Animation)

Éditer `scenes.js` :

```javascript
const SCENES = [
    {
        id: 'intro',
        title: 'Introduction',
        duration: 5000, // 5 secondes

        // Fonction appelée à chaque frame
        animate(localTime, progress, renderer, state) {
            // localTime : temps depuis début de la scène (ms)
            // progress : ratio 0 à 1

            // Exemple : apparition progressive
            const opacity = MathUtils.ease(progress, 'easeOutQuad');

            renderer.drawText('Titre', 0, 2, {
                color: `rgba(37, 99, 235, ${opacity})`,
                font: 'bold 32px Arial'
            });

            // Exemple : point qui se déplace
            const x = MathUtils.lerpEase(-3, 3, progress, 'easeInOutCubic');
            renderer.drawPoint(x, 0, { radius: 8, color: '#ef4444' });
        }
    },

    {
        id: 'definition',
        title: 'Définition',
        duration: 8000,

        animate(localTime, progress, renderer, state) {
            // Animation de la définition...
        }
    }
];
```

### Étape 4 : Générer le monolithe

```bash
python build_monolith.py -o animation.html
```

## API des Scènes

### Paramètres de la fonction animate()

| Paramètre | Type | Description |
|-----------|------|-------------|
| localTime | number | Temps en ms depuis le début de la scène |
| progress | number | Ratio d'avancement (0 à 1) |
| renderer | CanvasRenderer | Instance pour dessiner |
| state | object | État partagé entre les scènes |

### Helpers d'animation (AnimationHelpers)

```javascript
// Morphing entre deux valeurs
AnimationHelpers.morph(from, to, progress, 'easeOutQuad')

// Animation séquencée (plusieurs étapes)
AnimationHelpers.sequence(progress, [
    { duration: 1, fn: (p) => ... },
    { duration: 2, fn: (p) => ... }
])

// Délai avant de commencer
AnimationHelpers.delay(progress, 0.2) // démarre à 20%

// Animation en boucle
AnimationHelpers.loop(progress, 3) // 3 tours

// Aller-retour
AnimationHelpers.pingPong(progress)

// Fade in/out
AnimationHelpers.fadeIn(progress, 0, 0.3)   // 0% à 30%
AnimationHelpers.fadeOut(progress, 0.7, 1)  // 70% à 100%

// Écriture progressive
AnimationHelpers.typewriter('Texte à afficher', progress)

// Tracé progressif de fonction
AnimationHelpers.drawProgressively(x => Math.sin(x), progress, renderer)
```

### Fonctions d'easing disponibles

```
linear
easeInQuad, easeOutQuad, easeInOutQuad
easeInCubic, easeOutCubic, easeInOutCubic
easeInQuart, easeOutQuart, easeInOutQuart
easeInSine, easeOutSine, easeInOutSine
easeInExpo, easeOutExpo, easeInOutExpo
easeInCirc, easeOutCirc, easeInOutCirc
easeInElastic, easeOutElastic, easeInOutElastic
easeInBounce, easeOutBounce, easeInOutBounce
easeInBack, easeOutBack, easeInOutBack
```

## API du CanvasRenderer

### Dessin

```javascript
renderer.drawPoint(x, y, { radius, color, label })
renderer.drawSegment(x1, y1, x2, y2, { color, width, dashed })
renderer.drawVector(x1, y1, x2, y2, { color, width, arrowSize })
renderer.drawCircle(cx, cy, radius, { strokeColor, fillColor })
renderer.drawArc(cx, cy, radius, startAngle, endAngle, options)
renderer.drawAngle(cx, cy, startAngle, endAngle, { radius, showValue })
renderer.drawFunction(fn, { color, minX, maxX })
renderer.drawText(text, x, y, { color, font, align })
renderer.drawPolygon(points, { strokeColor, fillColor })
```

### Viewport

```javascript
renderer.clear()
renderer.drawGrid()
renderer.drawAxes()
renderer.zoom(factor, cx, cy)
renderer.pan(dx, dy)
renderer.resetViewport()
```

## API MathUtils

### Mathématiques

```javascript
MathUtils.sin(angle), MathUtils.cos(angle), MathUtils.tan(angle)
MathUtils.degToRad(deg), MathUtils.radToDeg(rad)
MathUtils.vec2(x, y), MathUtils.vec2Add(v1, v2), MathUtils.vec2Sub(v1, v2)
MathUtils.vec2Dot(v1, v2), MathUtils.vec2Length(v)
MathUtils.distance(p1, p2)
MathUtils.pointOnCircle(cx, cy, r, angle)
```

### Animation

```javascript
MathUtils.lerp(a, b, t)           // Interpolation linéaire
MathUtils.ease(t, 'easeOutQuad')  // Appliquer easing
MathUtils.lerpEase(a, b, t, 'easeInOutCubic')  // Combo lerp + ease
MathUtils.clamp(value, min, max)
```

### Formatage

```javascript
MathUtils.format(value, decimals)
MathUtils.formatAngle(radians)
MathUtils.formatPoint(x, y)
```

## Exemple complet de scène

```javascript
{
    id: 'produit-scalaire',
    title: 'Produit scalaire',
    duration: 12000,

    animate(localTime, progress, renderer, state) {
        // Phase 1 (0-30%) : Apparition des vecteurs
        if (progress < 0.3) {
            const p = progress / 0.3;
            const len = MathUtils.lerpEase(0, 4, p, 'easeOutQuad');

            renderer.drawVector(0, 0, len, 0, { color: '#ef4444', label: 'u' });

        // Phase 2 (30-60%) : Apparition du second vecteur
        } else if (progress < 0.6) {
            const p = (progress - 0.3) / 0.3;

            // Vecteur u (complet)
            renderer.drawVector(0, 0, 4, 0, { color: '#ef4444', label: 'u' });

            // Vecteur v (en cours)
            const angle = MathUtils.lerpEase(0, Math.PI/4, p, 'easeOutQuad');
            const vx = 3 * MathUtils.cos(angle);
            const vy = 3 * MathUtils.sin(angle);
            renderer.drawVector(0, 0, vx, vy, { color: '#3b82f6', label: 'v' });

        // Phase 3 (60-100%) : Affichage du produit scalaire
        } else {
            const p = (progress - 0.6) / 0.4;

            // Vecteurs complets
            renderer.drawVector(0, 0, 4, 0, { color: '#ef4444', label: 'u' });
            renderer.drawVector(0, 0, 3 * Math.cos(Math.PI/4), 3 * Math.sin(Math.PI/4),
                { color: '#3b82f6', label: 'v' });

            // Arc de l'angle
            const arcOpacity = MathUtils.ease(p, 'easeOutQuad');
            renderer.drawArc(0, 0, 1, 0, Math.PI/4, {
                color: `rgba(16, 185, 129, ${arcOpacity})`
            });

            // Formule
            const textOpacity = AnimationHelpers.fadeIn(p, 0.3, 0.7);
            renderer.drawText('u · v = ||u|| × ||v|| × cos(θ)', 0, -2, {
                color: `rgba(37, 99, 235, ${textOpacity})`,
                font: 'bold 24px Arial'
            });
        }
    }
}
```

## Règles d'affichage des textes

### RÈGLE FONDAMENTALE : Pas de chevauchement

Les informations textuelles (formules, explications, calculs) doivent :
1. **Occuper l'espace disponible** sans chevaucher l'animation graphique
2. **Être dans des boîtes avec fond blanc** semi-transparent pour la lisibilité

### Positionnement intelligent

| Animation centrée/à droite | → Texte à GAUCHE |
| Animation centrée/à gauche | → Texte à DROITE |
| Texte déjà à gauche ET droite | → Texte en BAS centré |
| Remarques ponctuelles | → En bas centré |

### Zones de positionnement

**IMPORTANT** : Le repère mathématique s'étend généralement de -15 à +15 sur chaque axe.
Les zones de texte doivent être suffisamment éloignées du centre pour éviter tout chevauchement.

```
┌───────────────────────────────────────────────────────────────┐
│    ZONE GAUCHE     │      ZONE CENTRE       │   ZONE DROITE   │
│  (infos/formules)  │      (animation)       │   (infos opt.)  │
│    x ∈ [-12, -8]   │     x ∈ [-4, 6]        │   x ∈ [8, 12]   │
├────────────────────┴────────────────────────┴─────────────────┤
│                    ZONE BAS (remarques) y ∈ [-4, -5]          │
└───────────────────────────────────────────────────────────────┘
```

**Coordonnées recommandées** :
- Zone gauche : **x = -9** (ou x ∈ [-12, -8])
- Zone droite : x ∈ [8, 12]
- Zone bas : y ∈ [-4, -5]

### Helper drawTextBox

```javascript
// À ajouter dans chaque animation pour les boîtes de texte
function drawTextBox(renderer, text, x, y, options = {}) {
    const {
        font = '20px Arial',
        color = '#1e3a8a',
        bgColor = 'rgba(255, 255, 255, 0.9)',
        padding = 10,
        borderRadius = 5,
        align = 'center'
    } = options;

    const ctx = renderer.ctx;
    ctx.font = font;
    const metrics = ctx.measureText(text);
    const textWidth = metrics.width;
    const textHeight = parseInt(font) * 1.2;

    const canvasPos = renderer.toCanvas(x, y);

    ctx.fillStyle = bgColor;
    ctx.beginPath();
    const boxX = canvasPos.x - textWidth/2 - padding;
    const boxY = canvasPos.y - textHeight/2 - padding;
    ctx.roundRect(boxX, boxY, textWidth + 2*padding, textHeight + 2*padding, borderRadius);
    ctx.fill();

    renderer.drawText(text, x, y, { font, color, align });
}
```

## Organisation des scènes en fichiers séparés

**OBLIGATION** : Chaque scène dans un fichier JS séparé dans `js/scenarios/`.

```javascript
// js/scenarios/01-intro.js
export const scene01 = {
    id: 'intro',
    title: 'Introduction',
    duration: 4000,
    animate(localTime, progress, renderer, state) { ... }
};

// js/scenarios/index.js
import { scene01 } from './01-intro.js';
import { scene02 } from './02-definition.js';
export const SCENES = [scene01, scene02, ...];
```

## Bonnes pratiques

### Pour les animations (Mode Animation)

1. **Découper en phases** : Utiliser des conditions sur `progress`
2. **Transitions fluides** : Toujours utiliser des easings
3. **Informations au bon moment** : Afficher textes/formules quand c'est pertinent
4. **Durées appropriées** : 3-5s pour une notion simple, 8-15s pour complexe
5. **Réutiliser l'état** : Stocker les valeurs calculées dans `state`
6. **Textes dans des boîtes** : Utiliser `drawTextBox()` pour la lisibilité
7. **Pas de chevauchement** : Placer les textes dans les zones libres

### Performance

1. **Éviter les allocations** dans animate() : Réutiliser les objets
2. **Limiter les dessins** : Ne pas redessiner ce qui n'a pas changé
3. **Utiliser les helpers** : Ils sont optimisés

## Template de référence

```
SKILL_BASE/assets/template/
```

Copier ce dossier entier pour chaque nouvelle animation.
