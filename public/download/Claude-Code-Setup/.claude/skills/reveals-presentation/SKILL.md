---
name: reveals-presentation
description: Skill spécialisé pour la création de présentations reveal.js interactives et stylées pour l'enseignement. Gère la mise en page, l'espacement, les animations, les exercices avec estimation de temps. Trois styles disponibles - collège, lycée, académique. Utiliser pour créer des présentations web professionnelles adaptées au contexte éducatif.
---

# Reveal.js Presentation Expert

Système expert pour la création de présentations reveal.js interactives et stylées de haute qualité avec gestion précise de l'espacement, animations progressives et styles contextuels.

## Objectif

Créer des présentations web professionnelles et interactives, parfaitement adaptées au contexte (classe collège, classe lycée, présentation académique) avec une attention particulière à la densité d'information par slide et à la progressivité pédagogique.

## 📖 Guides de référence

**LIRE IMPÉRATIVEMENT** les guides suivants avant de créer une présentation :

- `.claude/skills/reveals-presentation/references/fragments-reveals.md` : **PRIORITÉ ABSOLUE** - Fragments pour révélation progressive
- `.claude/skills/reveals-presentation/references/navigation-2d.md` : **TRÈS IMPORTANT** - Navigation multidirectionnelle 2D (haut/bas/gauche/droite)
- `.claude/skills/reveals-presentation/references/animations-transitions.md` : **IMPORTANT** - Transitions et effets visuels
- `.claude/skills/reveals-presentation/references/mathjax-integration.md` : **ESSENTIEL** - Intégration des formules mathématiques
- `.claude/skills/reveals-presentation/references/reveals-best-practices.md` : Bonnes pratiques et règles d'espacement
- `.claude/skills/reveals-presentation/references/reveals-styles-guide.md` : Guide des trois styles disponibles
- `.claude/skills/reveals-presentation/references/exercices-reveals.md` : Création d'exercices avec estimation de temps

## Principes Fondamentaux

### 1. Règle d'or : L'espace est votre allié

**JAMAIS plus de 70% de la slide remplie**

Une slide surchargée = une slide illisible. L'espace vide permet :
- La respiration visuelle
- La focalisation de l'attention
- La mémorisation efficace
- La lisibilité depuis le fond de la classe

### 2. Progressivité pédagogique avec fragments

**RÈGLE ABSOLUE** : Utiliser les fragments pour révélation progressive

Classes de fragments à utiliser :
- `class="fragment"` : Apparition au clic
- `class="fragment fade-in"` : Apparition en fondu
- `class="fragment fade-out"` : Disparition en fondu
- `class="fragment highlight-red"` : Mise en évidence rouge
- `data-fragment-index="1"` : Contrôle de l'ordre d'apparition

**Contrôle précis** : Savoir exactement ce qui s'affiche à chaque clic

### 2bis. Navigation 2D (multidirectionnelle)

**NOUVELLE POSSIBILITÉ** : Structurer la présentation en 2 dimensions !

- **Axe horizontal (← →)** : Progression principale du cours
- **Axe vertical (↑ ↓)** : Détails, approfondissements, explications complémentaires

**Quand utiliser la navigation 2D ?**
- Pour offrir des niveaux de détail optionnels
- Pour permettre différents parcours de lecture
- Pour ajouter des démonstrations étape par étape sans alourdir le flux principal
- Pour créer des exercices avec indices progressifs

**Lire impérativement** : `.claude/skills/reveals-presentation/references/navigation-2d.md`

### 3. Adaptation au contexte

Chaque style (collège, lycée, académique) a ses propres contraintes :
- **Collège** : Police grande, couleurs vives, animations fréquentes
- **Lycée** : Équilibre entre rigueur et accessibilité
- **Académique** : Sobriété, densité maîtrisée, références

## Structure type d'une présentation reveal.js

### Structure HTML de base

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Titre de la présentation</title>
  <meta name="author" content="Votre nom">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/white.css">

  <!-- Custom styles -->
  <style>
    /* Styles personnalisés selon le template */
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slides ici -->
    </div>
  </div>

  <!-- Reveal.js JS -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/math/math.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/notes/notes.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/highlight/highlight.js"></script>

  <script>
    Reveal.initialize({
      // Configuration
    });
  </script>
</body>
</html>
```

### Slide de titre

```html
<section>
  <h1>Titre de la présentation</h1>
  <h3>Sous-titre</h3>
  <p>
    <small>Par <strong>Nom de l'auteur</strong></small><br>
    <small>Établissement</small><br>
    <small>Date</small>
  </p>
</section>
```

### Slide de contenu avec fragments

```html
<section>
  <h2>Titre de la slide</h2>

  <ul>
    <li class="fragment">Premier point</li>
    <li class="fragment">Deuxième point</li>
    <li class="fragment">Troisième point</li>
  </ul>

  <div class="fragment">
    <div class="box-info">
      <strong>Point important :</strong> Une information clé à retenir
    </div>
  </div>
</section>
```

### Slide avec exercice et formules mathématiques

```html
<section class="exercise">
  <h2>Exercice : Application directe</h2>

  <div class="exercise-header">
    <span class="difficulty">★☆☆</span>
    <span class="estimated-time">5 minutes</span>
  </div>

  <!-- Énoncé -->
  <div class="statement">
    <p><strong>Énoncé :</strong> Résoudre l'équation suivante :</p>
    <p>\[2x + 3 = 7\]</p>
  </div>

  <!-- Solution progressive -->
  <div class="fragment">
    <p><strong>Solution :</strong></p>
    <p>\begin{align}
      2x + 3 &= 7 \\
      2x &= 4 \\
      x &= 2
    \end{align}</p>
  </div>

  <!-- Résultat encadré -->
  <div class="fragment">
    <div class="result-box">
      \(x = 2\)
    </div>
  </div>
</section>
```

## Workflow de création d'une présentation

### Étape 1 : Analyse du contexte

Identifier :
1. **Public cible** : Collège (6e-3e), Lycée (2nde-Tale), Académique (conférence)
2. **Durée prévue** : Adapter le nombre de slides (1 slide ≈ 2-3 minutes)
3. **Niveau de détail** : Introduction, approfondissement, synthèse
4. **Interactivité** : Exercices, questions, activités

### Étape 2 : Choix du template

Utiliser le template approprié dans `.claude/datas/reveal-templates/` :
- `template-college.html` : Police 22px, couleurs vives, animations nombreuses
- `template-lycee.html` : Police 20px, style équilibré, rigueur mathématique
- `template-academique.html` : Police 18px, sobriété, références bibliographiques

### Étape 3 : Structure du contenu

**Règle des 5-7 slides par section** :
- 1 slide de titre de section
- 5-6 slides de contenu
- Éviter les sections de 1 seule slide

**Règle du 6-6-6** (pour lycée/académique) :
- Maximum 6 bullets par slide
- Maximum 6 mots par bullet
- Maximum 6 slides de suite sans pause interactive

### Étape 4 : Gestion de l'espace

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

### Étape 5 : Animations et fragments

**Révélation progressive des items** :

```html
<ul>
  <li class="fragment">Premier</li>
  <li class="fragment">Deuxième</li>
  <li class="fragment">Troisième</li>
</ul>
```

**Mise en évidence** :

```html
<ul>
  <li>Point normal</li>
  <li class="fragment highlight-red">Point important révélé et surligné</li>
  <li>Point normal</li>
</ul>
```

**Ordre explicite** :

```html
<div class="fragment" data-fragment-index="2">Apparaît en deuxième</div>
<div class="fragment" data-fragment-index="1">Apparaît en premier</div>
```

### Étape 6 : Intégration de MathJax

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

### Étape 7 : Test et vérification

**Lancer un serveur local** :

```bash
# Python
python -m http.server 8000

# Node.js (si http-server installé)
npx http-server -p 8000

# Puis ouvrir http://localhost:8000/presentation.html
```

**Vérifier** :
- Navigation (flèches, espace)
- Fragments (animations progressives)
- MathJax (formules affichées)
- Responsive (mobile, tablette)
- Mode présentation (touche S)

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

### Transitions disponibles

- `none` : Pas de transition
- `fade` : Fondu enchaîné
- `slide` : Glissement horizontal
- `convex` : Perspective convexe
- `concave` : Perspective concave
- `zoom` : Zoom avant/arrière

## Styles par défaut selon le contexte

### Collège

```css
.reveal {
  font-size: 22px;
  font-family: 'Comic Neue', 'Comic Sans MS', sans-serif;
}

.reveal h1 { font-size: 2.5em; color: #ff6b6b; }
.reveal h2 { font-size: 2em; color: #4ecdc4; }

.reveal .box-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5em;
  border-radius: 15px;
  font-size: 1.2em;
}
```

### Lycée

```css
.reveal {
  font-size: 20px;
  font-family: 'Roboto', 'Arial', sans-serif;
}

.reveal h1 { font-size: 2.2em; color: #2c3e50; }
.reveal h2 { font-size: 1.8em; color: #34495e; }

.reveal .box-info {
  background-color: #ecf0f1;
  border-left: 5px solid #3498db;
  padding: 1em;
}
```

### Académique

```css
.reveal {
  font-size: 18px;
  font-family: 'Lato', 'Georgia', serif;
}

.reveal h1 { font-size: 2em; color: #000; }
.reveal h2 { font-size: 1.6em; color: #333; }

.reveal .box-info {
  border: 1px solid #ccc;
  padding: 1em;
  background-color: #fafafa;
}
```

## Classes CSS utiles

### Mise en page

```css
.two-columns {
  display: flex;
  gap: 2em;
}

.two-columns > div {
  flex: 1;
}

.center-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}
```

### Boxes et alertes

```css
.box-info {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
  padding: 1em;
  margin: 1em 0;
}

.box-warning {
  background-color: #fff3cd;
  border-left: 4px solid #ffc107;
  padding: 1em;
  margin: 1em 0;
}

.box-success {
  background-color: #d4edda;
  border-left: 4px solid #28a745;
  padding: 1em;
  margin: 1em 0;
}

.result-box {
  background-color: #f0f0f0;
  border: 2px solid #333;
  padding: 1em;
  text-align: center;
  font-size: 1.3em;
  font-weight: bold;
}
```

### Exercices

```css
.exercise {
  background-color: #fff9e6;
}

.exercise-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1em;
  font-size: 0.9em;
}

.difficulty {
  color: #ff9800;
  font-weight: bold;
}

.estimated-time {
  color: #666;
  font-style: italic;
}

.statement {
  background-color: white;
  padding: 1em;
  border-radius: 8px;
  margin-bottom: 1em;
}
```

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

## Vérifications finales

**Checklist avant finalisation** :

- [ ] Chaque slide < 70% remplie
- [ ] Fragments testés et fonctionnels
- [ ] MathJax affiche correctement toutes les formules
- [ ] Police lisible (≥ 18px)
- [ ] Cohérence des couleurs (thème respecté)
- [ ] Orthographe et mathématiques vérifiées
- [ ] Navigation fluide (pas de slides vides ou cassées)
- [ ] Exercices avec estimations de temps
- [ ] Responsive (testé sur mobile/tablette)
- [ ] Mode présentation fonctionne

## Bonnes pratiques

1. **Une idée = une slide** : Ne pas surcharger
2. **Couleurs cohérentes** : Respecter le thème choisi
3. **Taille de police** : Minimum 18px pour le texte principal
4. **Formules mathématiques** : Utiliser MathJax systématiquement
5. **Images** : Haute résolution, avec alt text
6. **Transitions** : Simples et discrètes
7. **Navigation** : Inclure sommaire pour présentations > 20 slides
8. **Accessibilité** : Contraste suffisant, texte alternatif

## Erreurs fréquentes à éviter

❌ **Slide surchargée** : > 10 lignes de texte
✅ **Slide aérée** : 5-7 points clés maximum

❌ **Police trop petite** : < 18px
✅ **Police adaptée** : 18-22px selon le contexte

❌ **Fragments désordonnés** : Animations illogiques
✅ **Ordre explicite** : `data-fragment-index` pour contrôle précis

❌ **MathJax oublié** : Formules mal affichées
✅ **MathJax intégré** : Toutes les formules avec délimiteurs corrects

❌ **Pas d'estimation** : Exercice sans indication de temps
✅ **Temps estimé** : Permet au professeur de gérer la séance

## Rappels critiques

- **PRIORITÉ ABSOLUE** : Utiliser les fragments pour révélation progressive
- **RÈGLE FONDAMENTALE** : Maximum 2 éléments côte à côte par slide (images, boxes, colonnes)
- **OBLIGATOIRE** : Intégrer MathJax pour toutes les formules mathématiques
- **TOUJOURS** tester dans un navigateur avant finalisation
- **TOUJOURS** vérifier la densité visuelle (< 70% rempli)
- **TOUJOURS** utiliser navigation DOWN si plus de 2 éléments à afficher
- **TOUJOURS** estimer le temps des exercices
- **TOUJOURS** adapter le style au public (collège/lycée/académique)
- **NE JAMAIS** oublier les balises de fermeture HTML
- **NE JAMAIS** mettre plus de 2 images côte à côte sur une même slide
- **NE JAMAIS** mettre plus de 7 items dans une liste
- **NE JAMAIS** utiliser des polices < 18px

## Référence rapide des classes de fragments

### Classes de base

```html
<div class="fragment">Apparition simple</div>
<div class="fragment fade-in">Apparition en fondu</div>
<div class="fragment fade-out">Disparition en fondu</div>
<div class="fragment fade-up">Apparition depuis le bas</div>
```

### Classes de mise en évidence

```html
<span class="fragment highlight-red">Surligné en rouge</span>
<span class="fragment highlight-green">Surligné en vert</span>
<span class="fragment highlight-blue">Surligné en bleu</span>
```

### Classes avancées

```html
<div class="fragment grow">Agrandissement</div>
<div class="fragment shrink">Rétrécissement</div>
<div class="fragment strike">Barré</div>
```

### Ordre explicite

```html
<div class="fragment" data-fragment-index="3">Troisième</div>
<div class="fragment" data-fragment-index="1">Premier</div>
<div class="fragment" data-fragment-index="2">Deuxième</div>
```

---

**Ce skill fait de vous un expert reveal.js** capable de créer des présentations web interactives, élégantes et pédagogiques pour tous les publics éducatifs.
