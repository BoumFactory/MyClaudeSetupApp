# Fragments Reveal.js - Guide Complet

## Introduction

Les **fragments** sont le mécanisme principal de révélation progressive dans reveal.js. Ils permettent de contrôler précisément ce qui apparaît à chaque clic de navigation.

## Principe fondamental

**RÈGLE D'OR** : Utiliser `class="fragment"` pour tout contenu qui doit apparaître progressivement.

```html
<section>
  <h2>Titre visible immédiatement</h2>

  <p class="fragment">Apparaît au premier clic</p>
  <p class="fragment">Apparaît au deuxième clic</p>
  <p class="fragment">Apparaît au troisième clic</p>
</section>
```

**Résultat** : 4 étapes (slide initiale + 3 clics)

## Classes de fragments disponibles

### Apparition simple

```html
<div class="fragment">Apparition instantanée</div>
```

### Apparition avec fondu

```html
<div class="fragment fade-in">Apparition en fondu</div>
<div class="fragment fade-out">Disparition en fondu</div>
<div class="fragment fade-in-then-out">Apparaît puis disparaît</div>
```

### Apparition directionnelle

```html
<div class="fragment fade-up">Vient du bas</div>
<div class="fragment fade-down">Vient du haut</div>
<div class="fragment fade-left">Vient de la droite</div>
<div class="fragment fade-right">Vient de la gauche</div>
```

### Mise en évidence (highlight)

```html
<span class="fragment highlight-red">Surligné en rouge</span>
<span class="fragment highlight-green">Surligné en vert</span>
<span class="fragment highlight-blue">Surligné en bleu</span>
<span class="fragment highlight-current-red">Rouge temporaire</span>
```

### Effets spéciaux

```html
<div class="fragment grow">Agrandissement</div>
<div class="fragment shrink">Rétrécissement</div>
<div class="fragment strike">Texte barré</div>
<div class="fragment semi-fade-out">Semi-transparent</div>
```

## Contrôle de l'ordre avec data-fragment-index

Par défaut, les fragments apparaissent dans l'ordre du DOM. Pour contrôler explicitement :

```html
<div class="fragment" data-fragment-index="3">Troisième</div>
<div class="fragment" data-fragment-index="1">Premier</div>
<div class="fragment" data-fragment-index="2">Deuxième</div>
```

**Utilisation** : Utile pour faire apparaître plusieurs éléments en même temps :

```html
<div class="fragment" data-fragment-index="1">Élément A</div>
<div class="fragment" data-fragment-index="1">Élément B (en même temps que A)</div>
<div class="fragment" data-fragment-index="2">Élément C</div>
```

## Pattern pédagogique : Question → Réponse

### Exercice simple (2 étapes)

```html
<section>
  <h2>Exercice : Calcul mental</h2>

  <!-- Étape 1 : Question visible immédiatement -->
  <div class="question">
    <p><strong>Question :</strong> Combien font \(7 \times 8\) ?</p>
  </div>

  <!-- Étape 2 : Réponse apparaît au clic -->
  <div class="fragment">
    <div class="result-box">
      \(7 \times 8 = 56\)
    </div>
  </div>
</section>
```

### Exercice avec étapes intermédiaires

```html
<section>
  <h2>Exercice : Résolution d'équation</h2>

  <!-- Énoncé : toujours visible -->
  <p><strong>Résoudre :</strong> \(2x + 3 = 7\)</p>

  <!-- Étape 1 : Soustraction -->
  <div class="fragment" data-fragment-index="1">
    <p><em>On soustrait 3 de chaque côté :</em></p>
    <p>\(2x = 4\)</p>
  </div>

  <!-- Étape 2 : Division -->
  <div class="fragment" data-fragment-index="2">
    <p><em>On divise par 2 :</em></p>
    <p>\(x = 2\)</p>
  </div>

  <!-- Étape 3 : Résultat final encadré -->
  <div class="fragment" data-fragment-index="3">
    <div class="result-box">
      \(x = 2\)
    </div>
  </div>
</section>
```

**Pages générées** : 4 étapes (énoncé + 3 clics)

## Pattern : Révélation progressive de liste

### Liste simple

```html
<section>
  <h2>Propriétés du produit scalaire</h2>

  <ul>
    <li class="fragment">Commutativité : \(\vec{u} \cdot \vec{v} = \vec{v} \cdot \vec{u}\)</li>
    <li class="fragment">Bilinéarité : \((k\vec{u}) \cdot \vec{v} = k(\vec{u} \cdot \vec{v})\)</li>
    <li class="fragment">Symétrie : \(\vec{u} \cdot \vec{u} = \|\vec{u}\|^2\)</li>
  </ul>
</section>
```

### Liste avec mise en évidence

```html
<section>
  <h2>Étapes de résolution</h2>

  <ol>
    <li class="fragment fade-in-then-semi-out">Lire l'énoncé</li>
    <li class="fragment fade-in-then-semi-out">Identifier les données</li>
    <li class="fragment fade-in-then-semi-out">Choisir la méthode</li>
    <li class="fragment highlight-red">Appliquer et calculer (étape actuelle)</li>
  </ol>
</section>
```

## Pattern : Transformation progressive

### Développement algébrique

```html
<section>
  <h2>Développement de \((x+2)^2\)</h2>

  <!-- Expression initiale -->
  <p>\[(x+2)^2\]</p>

  <!-- Formule -->
  <div class="fragment">
    <p><em>On applique : \((a+b)^2 = a^2 + 2ab + b^2\)</em></p>
  </div>

  <!-- Application -->
  <div class="fragment">
    <p>\[= x^2 + 2 \cdot x \cdot 2 + 2^2\]</p>
  </div>

  <!-- Simplification -->
  <div class="fragment">
    <p>\[= x^2 + 4x + 4\]</p>
  </div>

  <!-- Résultat final mis en évidence -->
  <div class="fragment">
    <div class="highlight-box">
      \[(x+2)^2 = x^2 + 4x + 4\]
    </div>
  </div>
</section>
```

## Pattern : Comparaison côte à côte

```html
<section>
  <h2>Méthode 1 vs Méthode 2</h2>

  <div class="two-columns">
    <!-- Colonne gauche -->
    <div>
      <h3>Méthode analytique</h3>
      <div class="fragment" data-fragment-index="1">
        <p>Calcul exact</p>
        <p>Complexe mais précis</p>
      </div>
    </div>

    <!-- Colonne droite -->
    <div>
      <h3>Méthode graphique</h3>
      <div class="fragment" data-fragment-index="2">
        <p>Visualisation intuitive</p>
        <p>Approximatif mais rapide</p>
      </div>
    </div>
  </div>

  <!-- Conclusion -->
  <div class="fragment" data-fragment-index="3">
    <p><strong>Choix :</strong> Dépend du contexte</p>
  </div>
</section>
```

## Limites et bonnes pratiques

### ✅ À FAIRE

1. **Limiter à 3-4 fragments par slide** :
   - Trop de fragments = audience perdue
   - Maximum 5 fragments pour exercices complexes

2. **Utiliser data-fragment-index pour synchroniser** :
   ```html
   <p class="fragment" data-fragment-index="1">Partie A</p>
   <p class="fragment" data-fragment-index="1">Partie B (en même temps)</p>
   ```

3. **Combiner avec des commentaires pédagogiques** :
   ```html
   <div class="fragment">
     <p><em>On remarque que...</em></p>
     <p>Formule résultante</p>
   </div>
   ```

### ❌ À ÉVITER

1. **Trop de fragments** :
   ```html
   <!-- MAUVAIS : 10 fragments = 10 clics -->
   <ul>
     <li class="fragment">Item 1</li>
     <li class="fragment">Item 2</li>
     <!-- ... 8 autres items -->
   </ul>
   ```

   **Solution** : Grouper par thème
   ```html
   <!-- BON : 3 groupes -->
   <ul>
     <li class="fragment" data-fragment-index="1">Items 1-3 : Définitions</li>
     <li class="fragment" data-fragment-index="2">Items 4-6 : Propriétés</li>
     <li class="fragment" data-fragment-index="3">Items 7-10 : Applications</li>
   </ul>
   ```

2. **Fragments sans logique pédagogique** :
   - Chaque fragment doit avoir une **raison** d'apparaître séparément
   - Question : "Pourquoi ce contenu n'apparaît-il pas immédiatement ?"

3. **Oublier l'ordre** :
   ```html
   <!-- PROBLÈME : ordre peut être imprévisible selon le DOM -->
   <span class="fragment">B</span>
   <span class="fragment">A</span>
   ```

   **Solution** : Toujours spécifier l'index si l'ordre importe
   ```html
   <span class="fragment" data-fragment-index="1">A</span>
   <span class="fragment" data-fragment-index="2">B</span>
   ```

## Fragments et CSS personnalisés

### Définir des effets personnalisés

```css
/* Apparition depuis la gauche avec rotation */
.fragment.custom-effect {
  opacity: 0;
  transform: translateX(-100%) rotate(-45deg);
  transition: all 0.5s ease;
}

.fragment.custom-effect.visible {
  opacity: 1;
  transform: translateX(0) rotate(0);
}
```

```html
<div class="fragment custom-effect">
  Contenu avec effet personnalisé
</div>
```

## Événements JavaScript (avancé)

```javascript
Reveal.on('fragmentshown', event => {
  console.log('Fragment affiché :', event.fragment);
  // Actions personnalisées
});

Reveal.on('fragmenthidden', event => {
  console.log('Fragment caché :', event.fragment);
});
```

## Récapitulatif

| Classe | Effet | Usage |
|--------|-------|-------|
| `fragment` | Apparition instantanée | Par défaut |
| `fragment fade-in` | Fondu entrant | Douceur |
| `fragment fade-up` | Depuis le bas | Dynamisme |
| `fragment highlight-red` | Surlignage rouge | Attention |
| `fragment grow` | Agrandissement | Emphase |
| `fragment strike` | Barré | Correction |

**Attribut** : `data-fragment-index="N"` pour contrôle de l'ordre

---

**Maîtrisez les fragments pour des présentations pédagogiques dynamiques et engageantes !**
