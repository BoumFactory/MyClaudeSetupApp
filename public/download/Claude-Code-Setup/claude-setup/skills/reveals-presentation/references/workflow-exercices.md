# Workflow exercices (géométrie et autres)

### Pattern exercices géométrie (avec figures)

**RÈGLE ABSOLUE** pour les exercices de géométrie avec figures graphiques :

**Structure recommandée** :

1. **Slide 1 : Énoncé + toutes les questions (PAS d'image)**
   - Titre de l'exercice + difficulté + temps total
   - Énoncé complet
   - Liste de toutes les questions (a, b, c, d...)
   - **Pas d'image sur cette slide** (elle viendra à la fin)
   - Nav-hint `↓ Question a)` SANS classe `fragment`

2. **1 slide par question avec résolution progressive**
   - Header : numéro de question + temps estimé
   - Fragment 1 : Rappel de la question + méthode/formule à appliquer
   - Fragment 2 : Calculs détaillés
   - Fragment 3 : Résultat encadré (utiliser `\boxed{}` en LaTeX ou `.result-box` en HTML)
   - Nav-hint `↓ Question b)` SANS classe `fragment` (navigation directe)

3. **Slide finale : Figure complète uniquement**
   - Header : "Figure complète" ou "Représentation graphique"
   - Image du graphique final avec toutes les constructions
   - Éventuellement légende descriptive

**Exemple de structure HTML** :

```html
<!-- Slide 1 : Énoncé -->
<section class="exercise">
  <div class="exercise-title-bar">
    <div class="exercise-meta">
      <span class="estimated-time">⏱️ 10 minutes</span>
      <span class="exercise-name">Exercice X : Titre</span>
      <span class="difficulty">★★☆</span>
    </div>
  </div>

  <div class="statement">
    <p>Énoncé complet...</p>
    <div class="questions-overview">
      <p>a) Première question</p>
      <p>b) Deuxième question</p>
      <p>c) Troisième question</p>
    </div>
  </div>

  <div class="nav-hint">
    <i class="fas fa-arrow-down"></i> Question a) ↓
  </div>
</section>

<!-- Slide 2 : Question a -->
<section>
  <div class="question-header">
    <span class="question-number">Question a)</span>
    <span class="question-time">⏱️ 3 min</span>
  </div>

  <div class="question-recall">
    <p><strong>Calculer :</strong> Les coordonnées de...</p>
  </div>

  <div class="resolution">
    <div class="fragment" data-fragment-index="1">
      <p><em>Utilisons la formule du milieu...</em></p>
    </div>

    <div class="fragment" data-fragment-index="2">
      <p>\[\begin{align}
        x_M &= \frac{x_A + x_B}{2} \\
        &= \frac{2 + 6}{2} = 4
      \end{align}\]</p>
    </div>

    <div class="fragment" data-fragment-index="3">
      <div class="result-box">
        \(M(4~;~3)\)
      </div>
    </div>
  </div>

  <div class="nav-hint">
    <i class="fas fa-arrow-down"></i> Question b) ↓
  </div>
</section>

<!-- Slides suivantes : une par question -->
<!-- ... -->

<!-- Slide finale : Figure -->
<section>
  <div class="question-header">
    <span class="question-number">Figure complète</span>
  </div>

  <div style="text-align: center; margin-top: 2em;">
    <img src="images_graphiques/graph_XX.png"
         alt="Représentation graphique complète"
         style="max-width: 90%; max-height: 500px; border: 2px solid #ddd; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <p style="margin-top: 1em; font-style: italic;">Représentation graphique complète</p>
  </div>
</section>
```

**Points clés** :

- ✅ **Nav-hints sans `fragment`** : Permet navigation directe sans clic supplémentaire
- ✅ **Maximum 3 fragments par question** : Méthode → Calculs → Résultat
- ✅ **Image uniquement à la fin** : Évite distraction pendant résolution
- ✅ **Résultats encadrés** : Utiliser `\boxed{}` ou `.result-box` pour visibilité
- ✅ **Temps estimés** : Aide à planifier la séance

### Pattern exercices non-géométriques

Pour les exercices sans figures graphiques, conserver le même workflow SAUF :
- Pas de slide finale avec figure
- Dernière question termine directement l'exercice
- Possibilité d'ajouter une slide de synthèse (optionnel)

### Optimisation de l'espace : Layout deux colonnes

**Principe** : Utiliser un layout 2 colonnes pour contenus peu larges mais occupant de l'espace vertical, en opposition ou complétion.

**Quand l'utiliser** :
- Deux méthodes de résolution différentes (calcul vs observation graphique)
- Comparaison de deux approches
- Contenu principal + exemple/contre-exemple
- Données + graphique côte à côte
- Avantages + inconvénients

**Exemple : Deux méthodes de résolution**

```html
<div class="fragment" data-fragment-index="2">
  <div class="two-columns" style="display: flex; gap: 2em;">
    <!-- Méthode 1 : Calcul -->
    <div style="flex: 1; background-color: #f0f8ff; padding: 1em; border-radius: 5px;">
      <p><strong>Méthode 1 : Par le calcul</strong></p>
      <p>\[\begin{align}
        AB &= \sqrt{(x_B-x_A)^2+(y_B-y_A)^2} \\
        &= \sqrt{5^2 + 3^2} = \sqrt{34}
      \end{align}\]</p>
    </div>

    <!-- Méthode 2 : Observation graphique -->
    <div style="flex: 1; background-color: #f0fff0; padding: 1em; border-radius: 5px;">
      <p><strong>Méthode 2 : Observation graphique</strong></p>
      <p>Sur le graphique, on observe que la médiatrice est horizontale d'ordonnée 0,5.</p>
      <p>Le point B a pour ordonnée 1 ≠ 0,5, donc B n'appartient pas à la médiatrice.</p>
    </div>
  </div>
</div>
```

**Avantages** :
- Gain d'espace vertical
- Comparaison visuelle immédiate
- Évite multiplication des slides
- Meilleure pédagogie (voir les liens entre approches)

**Limitation** : Maximum 2 colonnes (règle "2 par slide")

### Cas particulier : Simplification avec `\boxed{}`

Pour gagner de l'espace dans les slides de calculs, possibilité de :
- Réduire de 3 à 1 fragment
- Encadrer directement les résultats finaux avec `\boxed{}` dans les formules LaTeX
- Supprimer le `.result-box` séparé

**Exemple** :

```html
<div class="fragment" data-fragment-index="1">
  <p><em>Utilisons la formule de la distance...</em></p>
  <p>\[\begin{align}
    TA &= \sqrt{(-1{,}2-(-2{,}2))^2+(3{,}6-1{,}2)^2} \\
    &= \sqrt{1+5{,}76} = \boxed{\dfrac{13}{5}} \\[0.4cm]
    AC &= \sqrt{(6-(-1{,}2))^2+(0{,}6-3{,}6)^2} \\
    &= \sqrt{60{,}84} = \boxed{\dfrac{39}{5}}
  \end{align}\]</p>
</div>
```

**Avantages** :
- Gain d'une ligne verticale
- Résultats clairement identifiés
- Moins de clics pour l'utilisateur

**Utiliser si** : Les calculs tiennent sur une slide sans saturation
