# Configuration reveal.js, transitions, raccourcis et espacement

À lire seulement pour comprendre ou vérifier la configuration d'un template (qu'on ne modifie jamais), ou pour régler l'espacement des slides.

## Gestion de l'espace : marges et règle « 2 par slide »

**Marges et espacements CSS** :

```css
/* Pour une meilleure lisibilité */
.reveal h2 {
  margin-bottom: 1em;
}

.reveal ul {
  margin-top: 1em;
}

.reveal li {
  margin-bottom: 0.5em;
}

.reveal .box-info {
  padding: 1em;
  margin: 1em 0;
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}
```

**Vérification de densité** :
- Tester dans le navigateur
- Si slide > 70% remplie → découper en 2 slides
- Préférer 2 slides aérées à 1 slide dense

**RÈGLE FONDAMENTALE : Maximum 2 éléments côte à côte par slide**

**Principe "2 par slide"** :
- **Maximum 2 images** côte à côte par slide (utiliser `.grid-2`)
- **Maximum 2 boxes/cartes** côte à côte par slide
- **Maximum 2 colonnes** de contenu
- Si plus de 2 éléments → créer des slides DOWN supplémentaires

**Application pratique** :
- 4 images à afficher → 2 slides DOWN (2 images par slide)
- 6 avantages à lister → 3 slides DOWN (2 avantages par slide)
- 5 étapes → 2 slides DOWN (2-3 par slide OU grille 2 colonnes)

**Exceptions acceptables** :
- Listes à puces textuelles : jusqu'à 5 points OK si courts
- Workflow steps : jusqu'à 5 OK si en grille 2 colonnes
- Tags/badges : nombreux OK car petits

**En cas de contenu abondant** :
1. **Priorité 1** : Navigation DOWN (slides verticales)
   - Slide principale : vue d'ensemble + hint `↓`
   - Slides DOWN : détails (2 éléments max par slide)
2. **Priorité 2** : Grille 2 colonnes (`.grid-2`)
3. **Priorité 3** : Nouvelle slide horizontale

**Exemple - 4 images d'escape game** :
```html
<section>
  <!-- Slide principale -->
  <section>
    <h2>Escape game - Images générées</h2>
    <p>4 images créées pour le scénario</p>
    <p class="smaller"><i class="fas fa-arrow-down"></i> Appuyez sur ↓</p>
  </section>

  <!-- Slide DOWN 1 : 2 premières images -->
  <section>
    <h3>Images (1/2)</h3>
    <div class="grid-2">
      <div><img src="img1.png"><p>Porte</p></div>
      <div><img src="img2.png"><p>Coffre</p></div>
    </div>
  </section>

  <!-- Slide DOWN 2 : 2 dernières images -->
  <section>
    <h3>Images (2/2)</h3>
    <div class="grid-2">
      <div><img src="img3.png"><p>Carte</p></div>
      <div><img src="img4.png"><p>Médaille</p></div>
    </div>
  </section>
</section>
```

## Intégration de MathJax

**Configuration MathJax** :

```javascript
Reveal.initialize({
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full',
  },
  plugins: [ RevealMath ]
});
```

**Délimiteurs** :
- Inline : `\(formule\)` ou `$formule$`
- Block : `\[formule\]` ou `$$formule$$`
- Environnements LaTeX : `\begin{align}...\end{align}`

## Configuration reveal.js

### Options essentielles

```javascript
Reveal.initialize({
  // Affichage
  width: 1280,
  height: 720,
  margin: 0.1,

  // Navigation
  controls: true,
  controlsLayout: 'bottom-right',
  progress: true,
  slideNumber: 'c/t', // current/total
  hash: true,
  navigationMode: 'default',

  // Comportement
  transition: 'slide', // none/fade/slide/convex/concave/zoom
  transitionSpeed: 'default', // default/fast/slow
  backgroundTransition: 'fade',

  // Math
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full'
  },

  // Plugins
  plugins: [
    RevealMath,
    RevealNotes,
    RevealHighlight,
    RevealZoom
  ]
});

// IMPORTANT : Forcer le retour au top lors de la navigation horizontale
// Évite de rester au niveau vertical lors du changement de slide
let lastHorizontalIndex = 0;

Reveal.on('slidechanged', event => {
  const currentH = event.indexh;
  const currentV = event.indexv;

  // Si on change de slide horizontale et qu'on n'est pas au top
  if (currentH !== lastHorizontalIndex && currentV !== 0) {
    // Revenir au top de la nouvelle slide
    Reveal.slide(currentH, 0);
  }

  // Mettre à jour l'index horizontal
  lastHorizontalIndex = currentH;
});
```

**Pourquoi ce code ?**
Lorsqu'on navigue verticalement (DOWN) dans une slide puis qu'on change de slide horizontalement (→), reveal.js garde par défaut le même niveau vertical. Ce code force le retour au niveau 0 (top) de la nouvelle slide pour une expérience plus logique.

## Transitions disponibles

- `none` : Pas de transition
- `fade` : Fondu enchaîné
- `slide` : Glissement horizontal
- `convex` : Perspective convexe
- `concave` : Perspective concave
- `zoom` : Zoom avant/arrière

## Navigation et raccourcis clavier

### Raccourcis essentiels

- **Flèches** : Navigation entre slides
- **Espace** : Slide suivante
- **S** : Mode présentation (speaker notes)
- **F** : Plein écran
- **Esc** : Vue d'ensemble (aperçu de toutes les slides)
- **O** : Identique à Esc
- **B** / **.** : Écran noir (pause)

### Speaker notes

```html
<section>
  <h2>Titre de la slide</h2>
  <p>Contenu visible</p>

  <aside class="notes">
    Notes pour le présentateur (visibles uniquement en mode S)
    - Point à mentionner
    - Anecdote à raconter
    - Timing : 2 minutes
  </aside>
</section>
```
