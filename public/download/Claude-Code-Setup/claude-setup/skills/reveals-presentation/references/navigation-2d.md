# Navigation 2D (Multidirectionnelle) dans reveal.js

## Concept fondamental

La navigation 2D de reveal.js permet de créer des présentations avec **deux dimensions** :
- **Axe horizontal** (gauche ↔ droite) : Progression principale de la présentation
- **Axe vertical** (haut ↕ bas) : Détails, approfondissements, notes complémentaires

Cette architecture est idéale pour :
- Présenter un concept principal avec des détails optionnels
- Offrir différents niveaux de profondeur
- Permettre à l'audience de choisir le niveau de détail souhaité
- Créer des parcours de navigation flexibles

## Structure HTML de base

### Slide horizontale simple

```html
<section>
  <h2>Slide horizontale</h2>
  <p>Contenu principal</p>
</section>
```

### Slide horizontale avec détails verticaux

```html
<section>
  <section>
    <h2>Slide principale</h2>
    <p>Vue d'ensemble</p>
    <p><small>↓ Appuyez sur la flèche bas pour plus de détails</small></p>
  </section>

  <section>
    <h3>Détail 1</h3>
    <p>Premier niveau d'approfondissement</p>
  </section>

  <section>
    <h3>Détail 2</h3>
    <p>Deuxième niveau d'approfondissement</p>
  </section>

  <section>
    <h3>Détail 3</h3>
    <p>Dernier détail</p>
    <p><small>↑ Flèche haut pour remonter</small></p>
  </section>
</section>
```

### Exemple complet d'une présentation 2D

```html
<div class="reveal">
  <div class="slides">

    <!-- Colonne 1 : Introduction -->
    <section>
      <section>
        <h1>Introduction</h1>
        <p>Vue générale du sujet</p>
      </section>
      <section>
        <h3>Contexte historique</h3>
        <p>Détails sur l'histoire</p>
      </section>
      <section>
        <h3>Motivations</h3>
        <p>Pourquoi ce sujet est important</p>
      </section>
    </section>

    <!-- Colonne 2 : Concept 1 -->
    <section>
      <section>
        <h2>Concept 1</h2>
        <p>Vue d'ensemble</p>
      </section>
      <section>
        <h3>Définition</h3>
        <p>Définition précise</p>
      </section>
      <section>
        <h3>Exemple</h3>
        <p>Illustration concrète</p>
      </section>
    </section>

    <!-- Colonne 3 : Concept 2 -->
    <section>
      <section>
        <h2>Concept 2</h2>
        <p>Vue d'ensemble</p>
      </section>
      <section>
        <h3>Formule</h3>
        <p>\[E = mc^2\]</p>
      </section>
      <section>
        <h3>Application</h3>
        <p>Cas pratique</p>
      </section>
    </section>

    <!-- Colonne 4 : Conclusion -->
    <section>
      <h1>Conclusion</h1>
      <p>Récapitulatif</p>
    </section>

  </div>
</div>
```

## Règles importantes

### ⚠️ Règle n°1 : Imbrication immédiate

**Ne jamais mélanger** contenu et sections imbriquées :

❌ **Mauvais** (ne fonctionne pas correctement) :
```html
<section>
  <h2>Titre</h2>
  <p>Contenu</p>
  <section>Slide imbriquée</section>
</section>
```

✅ **Bon** :
```html
<section>
  <section>
    <h2>Titre</h2>
    <p>Contenu</p>
  </section>
  <section>
    <h2>Slide imbriquée</h2>
  </section>
</section>
```

### Règle n°2 : Premier enfant = vue d'ensemble

La première slide d'une stack verticale devrait toujours être une **vue d'ensemble** qui peut se suffire à elle-même si l'audience ne descend pas dans les détails.

✅ **Bon exemple** :
```html
<section>
  <!-- Vue d'ensemble autonome -->
  <section>
    <h2>Les fonctions</h2>
    <p>Une fonction associe à chaque élément d'un ensemble de départ
       un unique élément d'un ensemble d'arrivée.</p>
    <p><small>↓ Détails sur les types de fonctions</small></p>
  </section>

  <!-- Détails optionnels -->
  <section>
    <h3>Fonctions affines</h3>
    <p>\[f(x) = ax + b\]</p>
  </section>

  <section>
    <h3>Fonctions polynomiales</h3>
    <p>\[f(x) = a_nx^n + ... + a_1x + a_0\]</p>
  </section>
</section>
```

### Règle n°3 : Profondeur maximale de 4-5 slides

Ne pas créer de stacks verticales trop longues :
- **Optimal** : 2-3 slides verticales
- **Maximum** : 4-5 slides verticales
- Au-delà : Créer une nouvelle colonne horizontale

## Navigation

### Contrôles clavier

- **Flèche droite (→)** : Slide suivante (horizontal)
- **Flèche gauche (←)** : Slide précédente (horizontal)
- **Flèche bas (↓)** : Descendre dans la stack verticale
- **Flèche haut (↑)** : Remonter dans la stack verticale
- **Espace** : Avancer (horizontal puis vertical si présent)
- **Shift + Espace** : Reculer

### Modes de navigation

#### Mode par défaut (`navigationMode: 'default'`)

Comportement classique :
- Gauche/Droite : Navigue entre les colonnes horizontales
- Haut/Bas : Navigue dans la stack verticale courante
- Passer d'une colonne à l'autre : arrive toujours sur la première slide de la stack

#### Mode grille (`navigationMode: 'grid'`)

**Recommandé pour les présentations 2D !**

```javascript
Reveal.initialize({
  navigationMode: 'grid',
  // ...
});
```

Avantage : Conserve l'index vertical lors des déplacements horizontaux.

Exemple : Si vous êtes en slide 1.3 (colonne 1, ligne 3) et que vous allez à droite, vous arrivez en 2.3 (colonne 2, ligne 3) au lieu de 2.0.

#### Mode linéaire (`navigationMode: 'linear'`)

Toutes les slides (horizontales et verticales) sont traitées comme une séquence linéaire. Les flèches gauche/droite parcourent toutes les slides.

## Configuration complète pour navigation 2D

```javascript
Reveal.initialize({
  // Dimensions
  width: 1280,
  height: 720,

  // Navigation 2D
  navigationMode: 'grid', // Recommandé !

  // Contrôles visuels
  controls: true,
  controlsLayout: 'edges', // Affiche les 4 flèches aux bords
  controlsBackArrows: 'visible', // Flèches retour toujours visibles
  controlsTutorial: true, // Animation des flèches pour guider l'utilisateur

  // Barre de progression
  progress: true,

  // Numérotation des slides
  slideNumber: 'h.v', // Format : horizontal.vertical (ex: 2.3)

  // Historique
  hash: true,

  // Transitions
  transition: 'slide',

  // Plugins
  plugins: [ RevealMath, RevealNotes, RevealHighlight ]
});
```

## Indicateurs visuels de navigation

### Indicateur de direction dans les slides

Ajouter des hints visuels pour guider l'audience :

```html
<section>
  <section>
    <h2>Titre principal</h2>
    <p>Contenu</p>

    <!-- Indicateur de contenu vertical -->
    <div class="nav-hint">
      <p><small>⬇️ Appuyez sur ↓ pour plus de détails</small></p>
    </div>
  </section>

  <section>
    <h3>Détail</h3>
    <p>Contenu détaillé</p>

    <!-- Indicateur de retour -->
    <div class="nav-hint">
      <p><small>⬆️ Appuyez sur ↑ pour revenir</small></p>
    </div>
  </section>
</section>
```

### Style CSS pour les indicateurs

```css
.nav-hint {
  position: absolute;
  bottom: 20px;
  right: 20px;
  padding: 0.5em 1em;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 5px;
  font-size: 0.8em;
  color: #666;
}

/* Animation pour attirer l'attention */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.nav-hint {
  animation: bounce 2s infinite;
}
```

## Plugin CustomControls (Contrôles visuels améliorés)

### Installation

Inclure le plugin depuis CDN :

```html
<!-- CustomControls CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/customcontrols/style.css">

<!-- CustomControls JS -->
<script src="https://cdn.jsdelivr.net/npm/reveal.js-plugins@latest/customcontrols/plugin.js"></script>
```

### Configuration de base

```javascript
Reveal.initialize({
  // ... autres options ...

  customcontrols: {
    controls: [
      {
        icon: '<i class="fa fa-arrow-up"></i>',
        title: 'Haut',
        action: 'Reveal.up();'
      },
      {
        icon: '<i class="fa fa-arrow-down"></i>',
        title: 'Bas',
        action: 'Reveal.down();'
      },
      {
        icon: '<i class="fa fa-arrow-left"></i>',
        title: 'Gauche',
        action: 'Reveal.left();'
      },
      {
        icon: '<i class="fa fa-arrow-right"></i>',
        title: 'Droite',
        action: 'Reveal.right();'
      }
    ]
  },

  plugins: [
    RevealMath,
    RevealNotes,
    RevealHighlight,
    RevealCustomControls // Ajouter le plugin
  ]
});
```

### Pad de navigation stylé

Créer un pad visuel avec les 4 directions :

```html
<!-- Dans le <head> : Font Awesome pour les icônes -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>
  /* Pad de navigation personnalisé */
  .navigation-pad {
    position: fixed;
    bottom: 80px;
    right: 30px;
    display: grid;
    grid-template-areas:
      ". up ."
      "left center right"
      ". down .";
    gap: 5px;
    z-index: 1000;
  }

  .nav-button {
    width: 40px;
    height: 40px;
    background: rgba(0, 0, 0, 0.3);
    border: 2px solid rgba(255, 255, 255, 0.5);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.3s ease;
    color: white;
    font-size: 18px;
  }

  .nav-button:hover {
    background: rgba(0, 0, 0, 0.6);
    border-color: rgba(255, 255, 255, 0.9);
    transform: scale(1.1);
  }

  .nav-button.disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .nav-button.active {
    background: rgba(41, 128, 185, 0.7);
    border-color: rgba(52, 152, 219, 1);
    box-shadow: 0 0 15px rgba(52, 152, 219, 0.8);
  }

  .nav-up { grid-area: up; }
  .nav-down { grid-area: down; }
  .nav-left { grid-area: left; }
  .nav-right { grid-area: right; }
  .nav-center {
    grid-area: center;
    background: rgba(0, 0, 0, 0.2);
    border: none;
    cursor: default;
  }
</style>
```

```html
<!-- Ajout du pad dans le body -->
<div class="navigation-pad">
  <button class="nav-button nav-up" onclick="Reveal.up();">
    <i class="fas fa-chevron-up"></i>
  </button>
  <button class="nav-button nav-left" onclick="Reveal.left();">
    <i class="fas fa-chevron-left"></i>
  </button>
  <div class="nav-button nav-center"></div>
  <button class="nav-button nav-right" onclick="Reveal.right();">
    <i class="fas fa-chevron-right"></i>
  </button>
  <button class="nav-button nav-down" onclick="Reveal.down();">
    <i class="fas fa-chevron-down"></i>
  </button>
</div>
```

### Script pour mettre à jour les états actifs/désactivés

```javascript
// Mettre à jour l'état des boutons de navigation
function updateNavigationPad() {
  const indices = Reveal.getIndices();
  const slides = Reveal.getSlides();

  // Vérifier les directions disponibles
  const hasLeft = indices.h > 0;
  const hasRight = indices.h < slides.length - 1;
  const hasUp = indices.v > 0;
  const hasDown = Reveal.availableRoutes().down;

  // Mettre à jour les classes
  document.querySelector('.nav-left').classList.toggle('disabled', !hasLeft);
  document.querySelector('.nav-right').classList.toggle('disabled', !hasRight);
  document.querySelector('.nav-up').classList.toggle('disabled', !hasUp);
  document.querySelector('.nav-down').classList.toggle('disabled', !hasDown);

  // Surligner la direction avec du contenu vertical
  if (hasDown) {
    document.querySelector('.nav-down').classList.add('active');
  } else {
    document.querySelector('.nav-down').classList.remove('active');
  }
}

// Mettre à jour à chaque changement de slide
Reveal.on('slidechanged', updateNavigationPad);
Reveal.on('ready', updateNavigationPad);
```

## Cas d'usage pédagogiques

### 1. Cours avec niveaux de difficulté

```
Introduction (H)
├─ Vue simple (V1)
├─ Niveau intermédiaire (V2)
└─ Niveau avancé (V3)

Exercice 1 (H)
├─ Énoncé (V1)
├─ Indice 1 (V2)
├─ Indice 2 (V3)
└─ Solution (V4)

Exercice 2 (H)
...
```

### 2. Présentation avec démonstrations

```
Théorème (H)
├─ Énoncé (V1)
├─ Démonstration étape 1 (V2)
├─ Démonstration étape 2 (V3)
└─ Conclusion (V4)

Application (H)
...
```

### 3. Cours avec approfondissements optionnels

```
Concept principal (H)
└─ Résumé (V1)

Détails techniques (H)
├─ Aspect 1 (V1)
├─ Aspect 2 (V2)
└─ Aspect 3 (V3)

Exemples pratiques (H)
├─ Exemple 1 (V1)
└─ Exemple 2 (V2)
```

## Bonnes pratiques

### ✅ À faire

1. **Toujours** avoir une slide d'ensemble autonome en première position verticale
2. **Indiquer visuellement** la présence de contenu vertical (icônes, texte)
3. **Limiter** la profondeur verticale à 4-5 slides maximum
4. **Utiliser** le mode `navigationMode: 'grid'` pour une navigation cohérente
5. **Tester** la navigation avant la présentation
6. **Afficher** le format de numérotation h.v pour montrer la position 2D

### ❌ À éviter

1. **Ne pas** mélanger contenu et sections imbriquées
2. **Ne pas** créer de stacks verticales trop profondes (> 5 slides)
3. **Ne pas** cacher l'existence du contenu vertical
4. **Ne pas** oublier de configurer `navigationMode: 'grid'`
5. **Ne pas** utiliser la navigation verticale pour la progression principale

## Résumé

La navigation 2D de reveal.js permet de créer des présentations riches et flexibles avec :
- Une progression horizontale principale
- Des approfondissements verticaux optionnels
- Une navigation intuitive avec les flèches du clavier
- Des indicateurs visuels pour guider l'audience
- Un contrôle total sur le parcours de présentation

**Configuration minimale recommandée** :

```javascript
Reveal.initialize({
  navigationMode: 'grid',
  controls: true,
  controlsLayout: 'edges',
  slideNumber: 'h.v',
  // ... autres options
});
```

Cette architecture est **particulièrement adaptée** aux présentations pédagogiques où l'on souhaite offrir différents niveaux de profondeur selon les besoins de l'audience !
