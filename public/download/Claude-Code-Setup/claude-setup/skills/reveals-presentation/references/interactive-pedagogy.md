# Navigation 2D Interactive - Approche Pédagogique

## Principe fondamental

La navigation 2D de reveal.js doit être utilisée de manière **systématique et obligatoire** pour créer une **interactivité pédagogique** basée sur la progression Question → Réponse → Analyse → Approfondissement.

## Pourquoi cette approche ?

### Avantages pédagogiques

1. **Temps de réflexion** : Les élèves ont le temps de réfléchir à la question avant de voir la réponse
2. **Engagement actif** : L'interactivité maintient l'attention et favorise la participation
3. **Progression maîtrisée** : L'enseignant contrôle le rythme de révélation de l'information
4. **Différenciation** : Possibilité de s'arrêter au niveau adapté selon le public
5. **Anticipation des difficultés** : Les erreurs courantes et FAQ sont intégrées

### Structure cognitive optimale

La structure en 4 niveaux suit le processus d'apprentissage :

```
Niveau 0 : Questionnement   → Active la réflexion
Niveau 1 : Compréhension    → Apporte la connaissance
Niveau 2 : Consolidation    → Évite les erreurs
Niveau 3 : Approfondissement → Va plus loin
```

## Structure en 4 niveaux OBLIGATOIRE

### Niveau 0 : Question / Concept principal

**Objectif** : Poser une question ou présenter un concept de manière claire

**Contenu** :
- Question directe OU présentation du concept
- Formulation simple et compréhensible
- Éventuellement un contexte minimal

**Guidage visuel** :
```html
<div class="nav-hint fragment">
  <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la réponse
</div>
```

**Exemple** :
```html
<section>
  <h2>Qu'est-ce qu'un monôme ?</h2>
  <p>Un monôme est une expression algébrique particulière.</p>
  <p><strong>Question :</strong> Quelle est sa forme générale ?</p>
  <div class="nav-hint fragment">
    <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la définition
  </div>
</section>
```

### Niveau 1 : Réponse / Définition

**Objectif** : Apporter la réponse ou la définition avec exemples concrets

**Contenu** :
- Réponse claire et précise
- Définition formelle si applicable
- 2-3 exemples concrets
- Formule mathématique si nécessaire (MathJax)

**Guidage visuel** :
```html
<div class="nav-hint fragment">
  <i class="fas fa-arrow-down"></i> Remarques importantes ↓
</div>
```

**Exemple** :
```html
<section>
  <h3>Définition d'un monôme</h3>
  <p>Un monôme est le produit d'un coefficient réel par une puissance entière d'une indéterminée :</p>
  <p class="highlight">\(aX^n\)</p>
  <div class="fragment">
    <p><strong>Exemples :</strong></p>
    <ul>
      <li>\(3X^2\) est un monôme</li>
      <li>\(-5X\) est un monôme</li>
      <li>\(7\) est un monôme (degré 0)</li>
    </ul>
  </div>
  <div class="nav-hint fragment">
    <i class="fas fa-arrow-down"></i> Points d'attention ↓
  </div>
</section>
```

### Niveau 2 : Remarques / Erreurs courantes

**Objectif** : Anticiper les difficultés et erreurs fréquentes

**Contenu** :
- 2-3 remarques importantes
- Erreurs courantes à éviter
- Astuces mnémotechniques
- Pièges à connaître
- Points de vigilance

**Guidage visuel** :
```html
<div class="nav-hint fragment">
  <i class="fas fa-arrow-down"></i> Questions fréquentes ↓
</div>
```

**Exemple** :
```html
<section>
  <h3>⚠️ Points d'attention</h3>
  <ul class="fragment">
    <li><strong>Erreur courante :</strong> Oublier que \(7 = 7X^0\) est aussi un monôme</li>
    <li><strong>Astuce :</strong> Le degré est l'exposant de X (0 pour une constante)</li>
    <li><strong>Attention :</strong> \(X + 2\) n'est PAS un monôme (c'est une somme)</li>
  </ul>
  <div class="nav-hint fragment">
    <i class="fas fa-arrow-down"></i> Questions fréquentes ↓
  </div>
</section>
```

### Niveau 3 : FAQ / Approfondissement

**Objectif** : Répondre aux questions fréquentes et approfondir

**Contenu** :
- 1-2 questions fréquentes avec réponses
- Approfondissement théorique (optionnel)
- Lien avec d'autres notions
- Applications concrètes

**Format recommandé** :
```html
<div class="fragment">
  <p><strong>Q :</strong> [Question]</p>
  <p class="fragment"><strong>R :</strong> [Réponse]</p>
</div>
```

**Exemple** :
```html
<section>
  <h3>💡 Questions fréquentes</h3>

  <div class="fragment">
    <p><strong>Q :</strong> Pourquoi utilise-t-on X majuscule ?</p>
    <p class="fragment"><strong>R :</strong> X majuscule représente une indéterminée abstraite. On utilise x minuscule pour les variables concrètes (nombres).</p>
  </div>

  <div class="fragment">
    <p><strong>Q :</strong> Est-ce que \(0\) est un monôme ?</p>
    <p class="fragment"><strong>R :</strong> Oui ! C'est le monôme \(0X^n\) pour n'importe quel degré. Par convention, son degré est \(-\infty\).</p>
  </div>
</section>
```

## Cas d'usage spécifiques

### Cas 1 : Définition mathématique

**Structure type** :
```
Niveau 0 : "Qu'est-ce que [concept] ?"
Niveau 1 : Définition formelle + exemples
Niveau 2 : Erreurs de compréhension courantes
Niveau 3 : FAQ "Pourquoi cette définition ?" "Différence avec [autre concept]"
```

### Cas 2 : Formule / Propriété

**Structure type** :
```
Niveau 0 : Énoncé de la formule
Niveau 1 : Exemple d'application concrète
Niveau 2 : Erreurs de calcul courantes
Niveau 3 : FAQ "Pourquoi ça marche ?" "Quand l'utiliser ?"
```

### Cas 3 : Exercice

**Structure type** :
```
Niveau 0 : Énoncé de l'exercice
Niveau 1 : Méthode de résolution (stratégie)
Niveau 2 : Solution détaillée étape par étape
Niveau 3 : Vérification du résultat / autre méthode
```

### Cas 4 : Théorème / Démonstration

**Structure type** :
```
Niveau 0 : Énoncé du théorème
Niveau 1 : Démonstration (étapes principales)
Niveau 2 : Cas particuliers / contre-exemples
Niveau 3 : FAQ "Pourquoi ce théorème est important ?" "Applications"
```

### Cas 5 : Méthode / Procédure

**Structure type** :
```
Niveau 0 : Principe de la méthode
Niveau 1 : Exemple guidé d'application
Niveau 2 : Pièges à éviter dans l'application
Niveau 3 : Variantes de la méthode / cas limites
```

## Configuration technique OBLIGATOIRE

### Dans Reveal.initialize()

```javascript
Reveal.initialize({
  // Navigation 2D OBLIGATOIRE
  navigationMode: 'grid', // Conserve l'index vertical lors navigation horizontale
  controls: true,
  controlsLayout: 'edges', // Affiche les 4 flèches
  controlsBackArrows: 'visible',
  slideNumber: 'h.v', // Format horizontal.vertical (ex: 3.2)

  // Progression et historique
  hash: true,
  progress: true,

  // Transitions
  transition: 'slide',
  transitionSpeed: 'default',

  // Math
  math: {
    mathjax: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js',
    config: 'TeX-AMS_HTML-full'
  },

  // Plugins
  plugins: [ RevealMath, RevealNotes, RevealHighlight, RevealZoom ]
});
```

### Code de retour au top OBLIGATOIRE

**À placer IMMÉDIATEMENT après Reveal.initialize()** :

```javascript
// Retour automatique au niveau 0 lors changement horizontal
let lastHorizontalIndex = 0;

Reveal.on('slidechanged', event => {
  const currentH = event.indexh;
  const currentV = event.indexv;

  // Si on change de section horizontale ET qu'on n'est pas au niveau 0
  if (currentH !== lastHorizontalIndex && currentV !== 0) {
    // Forcer le retour au niveau 0 de la nouvelle section
    Reveal.slide(currentH, 0);
  }

  lastHorizontalIndex = currentH;
});
```

**Pourquoi ce code ?** : Sans ce code, lors du passage à la section suivante (→), l'utilisateur reste au même niveau vertical (ex: niveau 3), ce qui est désynchronisé et confusant.

## Guidage visuel de l'utilisateur

### Navigation hints

**OBLIGATOIRE sur chaque niveau** (sauf le dernier) :

```html
<div class="nav-hint fragment">
  <i class="fas fa-arrow-down"></i> [Texte contextuel] ↓
</div>
```

**Variantes de texte contextuel** :
- "Appuyez sur ↓ pour la réponse"
- "Remarques importantes ↓"
- "Questions fréquentes ↓"
- "Solution détaillée ↓"
- "Approfondissement ↓"

### Pad de navigation visuel (optionnel mais recommandé)

Un pad de navigation visuel peut être ajouté en bas à droite de l'écran avec des boutons directionnels actifs/inactifs selon le contenu disponible.

Voir template : `assets/templates/template-navigation-2d-demo.html`

## Exemples complets

### Exemple 1 : Définition simple

```html
<section>
  <!-- Niveau 0 : Question -->
  <section>
    <h2>Qu'est-ce qu'une fonction affine ?</h2>
    <p>Une fonction affine est un type particulier de fonction.</p>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Définition ↓
    </div>
  </section>

  <!-- Niveau 1 : Définition -->
  <section>
    <h3>Définition</h3>
    <p>Une fonction affine est une fonction de la forme :</p>
    <p class="highlight">\(f(x) = ax + b\)</p>
    <p>où \(a\) et \(b\) sont des nombres réels.</p>
    <div class="fragment">
      <p><strong>Exemples :</strong></p>
      <ul>
        <li>\(f(x) = 2x + 3\) (a=2, b=3)</li>
        <li>\(g(x) = -x + 1\) (a=-1, b=1)</li>
      </ul>
    </div>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Points d'attention ↓
    </div>
  </section>

  <!-- Niveau 2 : Remarques -->
  <section>
    <h3>⚠️ Points d'attention</h3>
    <ul class="fragment">
      <li><strong>Cas particulier :</strong> Si \(a=0\), la fonction est constante</li>
      <li><strong>Coefficient directeur :</strong> \(a\) représente la pente de la droite</li>
      <li><strong>Ordonnée à l'origine :</strong> \(b\) est la valeur de \(f(0)\)</li>
    </ul>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Questions fréquentes ↓
    </div>
  </section>

  <!-- Niveau 3 : FAQ -->
  <section>
    <h3>💡 Questions fréquentes</h3>
    <div class="fragment">
      <p><strong>Q :</strong> Quelle est la différence entre fonction affine et fonction linéaire ?</p>
      <p class="fragment"><strong>R :</strong> Une fonction linéaire est un cas particulier de fonction affine avec \(b=0\) (la droite passe par l'origine).</p>
    </div>
  </section>
</section>
```

### Exemple 2 : Exercice

```html
<section>
  <!-- Niveau 0 : Énoncé -->
  <section>
    <h2>Exercice : Développement</h2>
    <div class="exercise-header">
      <span class="difficulty">★★☆</span>
      <span class="estimated-time">4 minutes</span>
    </div>
    <p><strong>Énoncé :</strong> Développer et réduire l'expression suivante :</p>
    <p class="highlight">\((2x+3)(x-1)\)</p>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Méthode ↓
    </div>
  </section>

  <!-- Niveau 1 : Méthode -->
  <section>
    <h3>Méthode de résolution</h3>
    <p>On va utiliser la <strong>double distributivité</strong> :</p>
    <p class="highlight">\((a+b)(c+d) = ac + ad + bc + bd\)</p>
    <p class="fragment">Avec ici : \(a=2x\), \(b=3\), \(c=x\), \(d=-1\)</p>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Solution détaillée ↓
    </div>
  </section>

  <!-- Niveau 2 : Solution -->
  <section>
    <h3>Solution étape par étape</h3>
    <div class="fragment" data-fragment-index="1">
      <p><strong>Étape 1 :</strong> Appliquer la formule</p>
      <p>\((2x+3)(x-1) = 2x \cdot x + 2x \cdot (-1) + 3 \cdot x + 3 \cdot (-1)\)</p>
    </div>
    <div class="fragment" data-fragment-index="2">
      <p><strong>Étape 2 :</strong> Calculer les produits</p>
      <p>\(= 2x^2 - 2x + 3x - 3\)</p>
    </div>
    <div class="fragment" data-fragment-index="3">
      <p><strong>Étape 3 :</strong> Réduire</p>
      <p class="result-box">\(= 2x^2 + x - 3\)</p>
    </div>
    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Vérification ↓
    </div>
  </section>

  <!-- Niveau 3 : Vérification -->
  <section>
    <h3>Vérification</h3>
    <p>On peut vérifier avec \(x=0\) :</p>
    <div class="fragment">
      <p>Forme factorisée : \((2 \cdot 0 + 3)(0-1) = 3 \cdot (-1) = -3\)</p>
      <p>Forme développée : \(2 \cdot 0^2 + 0 - 3 = -3\)</p>
      <p class="highlight">✓ Les deux formes donnent le même résultat !</p>
    </div>
  </section>
</section>
```

## Checklist de validation

Avant de livrer une présentation, vérifier :

- [ ] Chaque section de contenu (définition, formule, exercice, théorème) a une structure verticale
- [ ] Chaque structure verticale a au minimum 3 niveaux (Question → Réponse → Remarques)
- [ ] Les navigation hints sont présents et contextuels sur chaque niveau (sauf le dernier)
- [ ] La configuration `navigationMode: 'grid'` est activée
- [ ] Le format de numérotation est `'h.v'`
- [ ] Le code de retour au top est présent après `Reveal.initialize()`
- [ ] Les fragments sont utilisés pour révélation progressive au sein de chaque niveau
- [ ] Les formules mathématiques utilisent MathJax
- [ ] La densité de chaque slide est < 70% (lycée/académique) ou < 60% (collège)
- [ ] La navigation ↓ ↑ → ← fonctionne correctement dans un navigateur

## Résumé

La navigation 2D interactive en 4 niveaux est **OBLIGATOIRE** pour toutes les présentations reveal.js éducatives. Elle transforme une présentation statique en expérience pédagogique interactive où :

1. L'enseignant **pose la question** (niveau 0)
2. Les élèves **réfléchissent** (temps de latence)
3. La **réponse est révélée** progressivement (niveau 1)
4. Les **points importants** sont soulignés (niveau 2)
5. Les **questions anticipées** sont traitées (niveau 3)

Cette approche maximise l'engagement, la compréhension et la rétention des connaissances.
