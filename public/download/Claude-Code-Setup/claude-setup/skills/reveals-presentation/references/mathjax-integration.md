# MathJax dans Reveal.js - Guide Complet

## Introduction

**MathJax** est la bibliothèque standard pour afficher des formules mathématiques dans les pages web. Son intégration avec reveal.js permet d'avoir des présentations avec des mathématiques de qualité typographique LaTeX.

## Configuration de base

### 1. Charger le plugin Math de reveal.js

```html
<!DOCTYPE html>
<html>
<head>
  <title>Ma présentation</title>
  <!-- Reveal.js CSS -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <!-- Slides ici -->
    </div>
  </div>

  <!-- Reveal.js core -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>

  <!-- Plugin Math -->
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/plugin/math/math.js"></script>

  <script>
    Reveal.initialize({
      math: {
        mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
        config: 'TeX-AMS_HTML-full',
      },
      plugins: [ RevealMath ]
    });
  </script>
</body>
</html>
```

### 2. Délimiteurs MathJax

**Formules inline** (dans le texte) :
- `\(formule\)` : Recommandé
- `$formule$` : Alternative (peut causer des conflits)

**Formules block** (centrées) :
- `\[formule\]` : Recommandé
- `$$formule$$` : Alternative

**Exemples** :

```html
<section>
  <h2>Formules mathématiques</h2>

  <p>La formule d'Euler : \(e^{i\pi} + 1 = 0\)</p>

  <p>Équation du second degré :</p>
  \[ax^2 + bx + c = 0\]

  <p>Avec discriminant : \(\Delta = b^2 - 4ac\)</p>
</section>
```

## Environnements LaTeX supportés

### align et align*

Pour aligner des équations :

```html
<section>
  <h2>Résolution étape par étape</h2>

  \begin{align}
    2x + 3 &= 7 \\
    2x &= 4 \\
    x &= 2
  \end{align}
</section>
```

**Note** : Le `&` permet l'alignement, `\\` crée une nouvelle ligne.

### cases

Pour des définitions par cas :

```html
<section>
  <h2>Fonction valeur absolue</h2>

  \[
    |x| = \begin{cases}
      x & \text{si } x \geq 0 \\
      -x & \text{si } x < 0
    \end{cases}
  \]
</section>
```

### matrix, pmatrix, bmatrix

Pour les matrices :

```html
<section>
  <h2>Matrices</h2>

  <p>Matrice sans délimiteurs :</p>
  \[
    \begin{matrix}
      a & b \\
      c & d
    \end{matrix}
  \]

  <p>Avec parenthèses :</p>
  \[
    \begin{pmatrix}
      1 & 2 \\
      3 & 4
    \end{pmatrix}
  \]

  <p>Avec crochets :</p>
  \[
    \begin{bmatrix}
      x & y \\
      z & w
    \end{bmatrix}
  \]
</section>
```

## Commandes LaTeX courantes

### Symboles mathématiques

```html
<section>
  <h2>Symboles</h2>

  <ul>
    <li>Ensembles : \(\mathbb{N}, \mathbb{Z}, \mathbb{Q}, \mathbb{R}, \mathbb{C}\)</li>
    <li>Infini : \(\infty\)</li>
    <li>Vecteurs : \(\vec{u}, \vec{v}\)</li>
    <li>Angles : \(\widehat{ABC}\)</li>
    <li>Fraction : \(\frac{a}{b}\)</li>
    <li>Racine : \(\sqrt{x}\), \(\sqrt[n]{x}\)</li>
    <li>Somme : \(\sum_{i=1}^{n} i\)</li>
    <li>Intégrale : \(\int_a^b f(x) \, dx\)</li>
    <li>Limite : \(\lim_{x \to +\infty} f(x)\)</li>
  </ul>
</section>
```

### Opérateurs

```html
<section>
  <h2>Opérateurs</h2>

  <ul>
    <li>Multiplication : \(\times\) ou \(\cdot\)</li>
    <li>Division : \(\div\)</li>
    <li>Plus ou moins : \(\pm\)</li>
    <li>Approximation : \(\approx\)</li>
    <li>Équivalence : \(\equiv\)</li>
    <li>Inférieur/supérieur : \(\leq\), \(\geq\)</li>
    <li>Appartenance : \(\in\), \(\notin\)</li>
    <li>Inclusion : \(\subset\), \(\subseteq\)</li>
  </ul>
</section>
```

### Fonctions

```html
<section>
  <h2>Fonctions usuelles</h2>

  <ul>
    <li>Sinus : \(\sin(x)\)</li>
    <li>Cosinus : \(\cos(x)\)</li>
    <li>Tangente : \(\tan(x)\)</li>
    <li>Logarithme : \(\ln(x)\), \(\log(x)\)</li>
    <li>Exponentielle : \(\exp(x)\) ou \(e^x\)</li>
  </ul>
</section>
```

## Pattern pédagogique : Formules progressives

### Révélation d'une démonstration

```html
<section>
  <h2>Démonstration : Formule du discriminant</h2>

  <!-- Équation initiale -->
  <p>Soit l'équation : \(ax^2 + bx + c = 0\)</p>

  <!-- Étape 1 -->
  <div class="fragment">
    <p><em>On divise par \(a\) :</em></p>
    \[x^2 + \frac{b}{a}x + \frac{c}{a} = 0\]
  </div>

  <!-- Étape 2 -->
  <div class="fragment">
    <p><em>On complète le carré :</em></p>
    \[x^2 + \frac{b}{a}x + \left(\frac{b}{2a}\right)^2 = \left(\frac{b}{2a}\right)^2 - \frac{c}{a}\]
  </div>

  <!-- Étape 3 -->
  <div class="fragment">
    <p><em>On factorise :</em></p>
    \[\left(x + \frac{b}{2a}\right)^2 = \frac{b^2 - 4ac}{4a^2}\]
  </div>

  <!-- Résultat final -->
  <div class="fragment">
    <div class="result-box">
      \[x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}\]
    </div>
  </div>
</section>
```

### Exercice avec solution progressive

```html
<section class="exercise">
  <h2>Exercice : Dérivée de produit</h2>

  <!-- Énoncé -->
  <p><strong>Calculer :</strong> \((x^2 \sin(x))'\)</p>

  <!-- Formule -->
  <div class="fragment">
    <p><em>On utilise : \((uv)' = u'v + uv'\)</em></p>
  </div>

  <!-- Identification -->
  <div class="fragment">
    <p><em>Avec \(u = x^2\) et \(v = \sin(x)\) :</em></p>
    <ul>
      <li>\(u' = 2x\)</li>
      <li>\(v' = \cos(x)\)</li>
    </ul>
  </div>

  <!-- Application -->
  <div class="fragment">
    <p><em>Application :</em></p>
    \[(x^2 \sin(x))' = 2x \cdot \sin(x) + x^2 \cdot \cos(x)\]
  </div>

  <!-- Résultat final -->
  <div class="fragment">
    <div class="result-box">
      \[(x^2 \sin(x))' = 2x\sin(x) + x^2\cos(x)\]
    </div>
  </div>
</section>
```

## Mise en forme et couleurs

### Couleurs dans les formules

```html
<section>
  <h2>Mise en évidence avec couleurs</h2>

  <p>Identité remarquable :</p>
  \[
    (\textcolor{red}{a} + \textcolor{blue}{b})^2 =
    \textcolor{red}{a}^2 + 2\textcolor{red}{a}\textcolor{blue}{b} + \textcolor{blue}{b}^2
  \]

  <div class="fragment">
    <p>Application avec \(a = x\) et \(b = 3\) :</p>
    \[
      (x + 3)^2 = \textcolor{orange}{x^2} + \textcolor{green}{6x} + \textcolor{purple}{9}
    \]
  </div>
</section>
```

### Taille des formules

```html
<section>
  <h2>Ajuster la taille</h2>

  <p>Formule normale : \(\frac{a}{b}\)</p>

  <p>Formule plus grande :</p>
  \[\Large \frac{a}{b}\]

  <p>Formule énorme (pour emphase) :</p>
  \[\Huge E = mc^2\]
</section>
```

## Configuration avancée de MathJax

### Options complètes

```javascript
Reveal.initialize({
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full',
    // Options MathJax supplémentaires
    tex: {
      inlineMath: [ ['$','$'], ['\\(','\\)'] ],
      displayMath: [ ['$$','$$'], ['\\[','\\]'] ],
      processEscapes: true,
      processEnvironments: true
    },
    options: {
      skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre']
    }
  },
  plugins: [ RevealMath ]
});
```

### Macros personnalisées

```javascript
Reveal.initialize({
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full',
    tex: {
      macros: {
        RR: "\\mathbb{R}",
        NN: "\\mathbb{N}",
        ZZ: "\\mathbb{Z}",
        vec: ["\\overrightarrow{#1}", 1]
      }
    }
  },
  plugins: [ RevealMath ]
});
```

**Usage** :

```html
<p>Soit \(x \in \RR\) et \(\vec{u}\) un vecteur.</p>
```

## Problèmes courants et solutions

### Problème : MathJax ne charge pas

**Symptômes** : Formules affichées brutes (ex: `\(x^2\)`)

**Solution 1** : Vérifier le CDN
```html
<!-- Utiliser le CDN officiel -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

**Solution 2** : Vérifier le plugin
```javascript
Reveal.initialize({
  plugins: [ RevealMath ] // S'assurer qu'il est bien inclus
});
```

### Problème : Délimiteurs $ causent des conflits

**Solution** : Utiliser exclusivement `\(...\)` et `\[...\]`

```html
<!-- ÉVITER -->
<p>$x^2 + 1$</p>

<!-- PRÉFÉRER -->
<p>\(x^2 + 1\)</p>
```

### Problème : Formules tronquées ou qui débordent

**Solution** : Réduire la taille ou découper

```html
<!-- Si formule trop longue -->
\begin{align}
  f(x) &= a_0 + a_1 x + a_2 x^2 \\
       &\quad + a_3 x^3 + \ldots
\end{align}
```

### Problème : Erreur de syntaxe LaTeX

**Erreur courante** : Accolades non fermées

```html
<!-- MAUVAIS -->
\frac{x^2{y}

<!-- CORRECT -->
\frac{x^2}{y}
```

## Bonnes pratiques

### ✅ À FAIRE

1. **Toujours tester les formules** dans la présentation
2. **Utiliser des fragments** pour révélation progressive
3. **Ajouter des commentaires** en italique pour expliquer les étapes
4. **Mettre en couleur** les transformations importantes
5. **Encadrer les résultats finaux** avec des boxes CSS

### ❌ À ÉVITER

1. **Formules trop longues** : Découper en plusieurs lignes
2. **Trop de symboles complexes** : Simplifier pour la lisibilité
3. **Oublier l'espacement** : Utiliser `\,` ou `\quad` si nécessaire
4. **Mélanger notations** : Être cohérent (ex: toujours `\cdot` pour le produit)

## Récapitulatif

| Délimiteur | Usage | Exemple |
|------------|-------|---------|
| `\(...\)` | Inline | `\(x^2\)` |
| `\[...\]` | Block | `\[x^2 + 1 = 0\]` |
| `\begin{align}...\end{align}` | Alignement multi-lignes | Voir exemples |
| `\begin{cases}...\end{cases}` | Définitions par cas | Voir exemples |

**Configuration** : Inclure `RevealMath` dans les plugins

---

**Maîtrisez MathJax pour des présentations mathématiques de qualité professionnelle !**
