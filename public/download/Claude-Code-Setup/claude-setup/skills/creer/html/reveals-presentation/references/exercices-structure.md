# Structure spécifique pour les présentations d'exercices

## Principe fondamental

Les présentations d'exercices suivent une logique **DIFFÉRENTE** des présentations de cours.

**COURS** : Navigation 2D en 4 niveaux (Question → Réponse → Remarques → FAQ)
**EXERCICES** : Navigation verticale par question avec résolution progressive

## Détection du contexte

Une présentation est considérée comme "session d'exercices" si :
- Le fichier source contient "Exo", "exercice", "Exercices" dans le nom
- Le fichier source contient principalement des environnements `\begin{EXO}`
- L'utilisateur spécifie explicitement qu'il s'agit d'exercices

## Différences clés : Cours vs Exercices

| Aspect | COURS | EXERCICES |
|--------|-------|-----------|
| Rappels théoriques | ✅ Présents (rappels, définitions) | ❌ Absents (direct aux exercices) |
| Structure verticale | 4 niveaux (Q→R→Remarques→FAQ) | N niveaux (1 par question) |
| Slide principale | Concept + Question | Énoncé global de l'exercice |
| Slides DOWN | Réponse, remarques, FAQ | 1 slide par question |
| Timer | Par exercice | Global + par question |
| Format header | - | ligne / durée .. titre .. difficulté |

## Structure pour une présentation d'exercices

### Slide de titre

```html
<section>
  <h1>Session d'exercices</h1>
  <h2>Développements et factorisations</h2>
  <p>
    <small>Classe de <strong>2nde</strong></small><br>
    <small>Lycée Camille Claudel</small>
  </p>
</section>
```

**IMPORTANT** : Pas de slides de rappel théorique après le titre.

### Structure d'un exercice (navigation verticale)

```html
<section>
  <!-- Niveau 0 : Énoncé global -->
  <section class="exercise">
    <div class="exercise-title-bar">
      <!-- Nouvelle structure : ligne / durée .. titre .. difficulté -->
      <hr style="margin: 0 0 0.5em 0; border: 1px solid #ccc;">
      <div class="exercise-meta">
        <span class="estimated-time">⏱️ 8 minutes</span>
        <span class="exercise-name">Exercice 1 : Développements simples</span>
        <span class="difficulty">★★☆</span>
      </div>
    </div>

    <!-- Énoncé global (ou partie 1 si trop long) -->
    <div class="statement">
      <p><strong>Développer et réduire les expressions suivantes :</strong></p>
      <div class="questions-overview">
        <p>a) \(S = -4(-5x+2)\)</p>
        <p>b) \(A = -3(2x-3)+4(-22x+5)\)</p>
        <p>c) \(M = -x(15x+7)-2(12x+5)\)</p>
        <p>d) \(U = 3x(11x+8)-3x(12x+4)\)</p>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la question a)
    </div>
  </section>

  <!-- Niveau 1 : Question a) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question a)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <!-- Rappel de la question -->
    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(S = -4(-5x+2)\)</p>
    </div>

    <!-- Résolution progressive avec fragments -->
    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p><em>On applique la distributivité :</em></p>
        <p>\[S = -4 \times (-5x) + (-4) \times 2\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <p><em>On calcule :</em></p>
        <p>\[S = 20x - 8\]</p>
      </div>

      <div class="fragment" data-fragment-index="3">
        <div class="result-box">
          \(S = 20x - 8\)
        </div>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la question b)
    </div>
  </section>

  <!-- Niveau 2 : Question b) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question b)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(A = -3(2x-3)+4(-22x+5)\)</p>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p><em>On développe chaque terme :</em></p>
        <p>\[\begin{align}
          A &= -3(2x-3)+4(-22x+5) \\
            &= -6x + 9 - 88x + 20
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <p><em>On regroupe les termes semblables :</em></p>
        <p>\[A = -94x + 29\]</p>
      </div>

      <div class="fragment" data-fragment-index="3">
        <div class="result-box">
          \(A = -94x + 29\)
        </div>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la question c)
    </div>
  </section>

  <!-- Niveaux suivants : questions c), d), etc. -->
  <!-- ... -->

</section>
```

### CSS pour le nouveau format

```css
/* Barre de titre de l'exercice */
.exercise-title-bar {
  margin-bottom: 1.5em;
}

.exercise-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5em 0;
  font-size: 0.9em;
}

.exercise-name {
  flex: 1;
  text-align: center;
  font-weight: bold;
  font-size: 1.3em;
  color: #2c3e50;
}

.estimated-time {
  color: #e74c3c;
  font-weight: bold;
  font-size: 1.1em;
}

.difficulty {
  color: #f39c12;
  font-weight: bold;
  font-size: 1.2em;
}

/* Header de question individuelle */
.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.5em 1em;
  border-radius: 8px;
  margin-bottom: 1em;
}

.question-number {
  font-weight: bold;
  font-size: 1.2em;
}

.question-time {
  font-size: 1em;
  font-style: italic;
}

/* Rappel de la question */
.question-recall {
  background-color: #fff9e6;
  border-left: 4px solid #f39c12;
  padding: 1em;
  margin-bottom: 1.5em;
  border-radius: 4px;
}

/* Zone de résolution */
.resolution {
  text-align: left;
}

.resolution p {
  margin: 0.5em 0;
}

/* Overview des questions (slide niveau 0) */
.questions-overview {
  background-color: #f8f9fa;
  padding: 1em;
  border-radius: 8px;
  margin-top: 1em;
}

.questions-overview p {
  margin: 0.5em 0;
  font-size: 1.1em;
}
```

## Gestion des timers

### Timer global (niveau 0)

Le timer global est la **somme des timers individuels** de toutes les questions de l'exercice.

Exemple :
- Question a) : 2 min
- Question b) : 2 min
- Question c) : 2 min
- Question d) : 2 min
- **Timer global** : 8 min

### Timer par question (niveaux 1+)

Chaque slide de question affiche son propre timer dans le header :

```html
<div class="question-header">
  <span class="question-number">Question a)</span>
  <span class="question-time">⏱️ 2 min</span>
</div>
```

## Cas particuliers

### Énoncé trop long (slide niveau 0)

Si l'énoncé global contient trop de questions (> 6 questions), le découper en 2 parties :

```html
<section>
  <!-- Niveau 0a : Énoncé partie 1 -->
  <section class="exercise">
    <div class="exercise-title-bar">
      <hr>
      <div class="exercise-meta">
        <span class="estimated-time">⏱️ 12 minutes</span>
        <span class="exercise-name">Exercice 2 : Factorisations complexes</span>
        <span class="difficulty">★★★</span>
      </div>
    </div>

    <div class="statement">
      <p><strong>Factoriser les expressions suivantes (partie 1/2) :</strong></p>
      <div class="questions-overview">
        <p>a) \(M = (23x+1)(-17x+1)+(23x+1)^2\)</p>
        <p>b) \(A = (13x-14)(25x-11)-(13x-14)^2\)</p>
        <p>c) \(N = (8-18x)^2-(16x-3)(8-18x)\)</p>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-right"></i> Suite de l'énoncé →
    </div>
  </section>

  <!-- Niveau 0b : Énoncé partie 2 (même niveau horizontal) -->
  <!-- Placé après pour navigation → -->
</section>

<section>
  <section class="exercise">
    <div class="statement">
      <p><strong>Factoriser les expressions suivantes (partie 2/2) :</strong></p>
      <div class="questions-overview">
        <p>d) \(U = (11-2x)(9-7x)+(2x-11)(11x+2)\)</p>
        <p>e) \(E = (6x+23)(6x-5)-(19x-6)(5-6x)\)</p>
        <p>f) \(L = (16x+13)(21x-3)+(16x+13)\)</p>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la question a)
    </div>
  </section>

  <!-- Niveaux 1+ : Questions a), b), c), d), e), f) -->
  <!-- ... -->
</section>
```

**IMPORTANT** : Le découpage se fait en **navigation horizontale** (→), pas verticale (↓).

### Exercice sans sous-questions

Si l'exercice est une question unique (par exemple, un problème de Pythagore), la structure est simplifiée :

```html
<section>
  <!-- Niveau 0 : Énoncé global -->
  <section class="exercise">
    <div class="exercise-title-bar">
      <hr>
      <div class="exercise-meta">
        <span class="estimated-time">⏱️ 5 minutes</span>
        <span class="exercise-name">Exercice 10 : Application de Pythagore</span>
        <span class="difficulty">★★☆</span>
      </div>
    </div>

    <div class="statement">
      <p>ABC est un triangle rectangle en A tel que \(BC = x+7\) et \(AC = 5\) où \(x\) désigne un nombre positif.</p>
      <p><strong>Exprimer \(AB^2\) en fonction de \(x\) sous forme factorisée.</strong></p>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la résolution
    </div>
  </section>

  <!-- Niveau 1 : Résolution complète -->
  <section>
    <div class="question-header">
      <span class="question-number">Résolution</span>
      <span class="question-time">⏱️ 5 min</span>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p><em>D'après le théorème de Pythagore dans le triangle ABC rectangle en A :</em></p>
        <p>\[BC^2 = AB^2 + AC^2\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <p><em>Donc :</em></p>
        <p>\[\begin{align}
          AB^2 &= BC^2 - AC^2 \\
               &= (x+7)^2 - 5^2
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="3">
        <p><em>On reconnaît une différence de deux carrés :</em></p>
        <p>\[\begin{align}
          AB^2 &= (x+7-5)(x+7+5) \\
               &= (x+2)(x+12)
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="4">
        <div class="result-box">
          \(AB^2 = (x+2)(x+12)\)
        </div>
      </div>
    </div>
  </section>
</section>
```

## Règles strictes pour les exercices

### ✅ À FAIRE

1. **Détecter le contexte** : Vérifier si c'est une session d'exercices
2. **Pas de rappel de cours** : Aller directement aux exercices après le titre
3. **Format header** : ligne / durée .. titre .. difficulté
4. **Navigation verticale** : 1 slide par question
5. **Rappel de question** : Toujours rappeler la question en haut de sa slide
6. **Timer double** : Global (niveau 0) + par question (niveaux 1+)
7. **Résolution progressive** : Utiliser les fragments pour les étapes
8. **Densité** : Respecter la règle des 70% maximum
9. **Découpage si nécessaire** : Si > 6 questions, découper l'énoncé en 2 parties (navigation →)

### ❌ À NE JAMAIS FAIRE

1. ❌ **Ajouter des rappels théoriques** dans une session d'exercices
2. ❌ **Utiliser la structure 4 niveaux** (Question → Réponse → Remarques → FAQ)
3. ❌ **Oublier le timer par question**
4. ❌ **Ne pas rappeler la question** en haut de la slide de résolution
5. ❌ **Mettre plusieurs questions sur une même slide** verticale
6. ❌ **Oublier la ligne de séparation** dans le header de l'exercice
7. ❌ **Mettre le format ancien** (titre exo / ligne / difficulté ... durée)

## Exemple complet : Exercice à 4 questions

```html
<section>
  <!-- NIVEAU 0 : Énoncé global -->
  <section class="exercise">
    <div class="exercise-title-bar">
      <hr style="margin: 0 0 0.5em 0; border: 1px solid #ccc;">
      <div class="exercise-meta">
        <span class="estimated-time">⏱️ 8 minutes</span>
        <span class="exercise-name">Exercice 1 : Développements simples</span>
        <span class="difficulty">★☆☆</span>
      </div>
    </div>

    <div class="statement">
      <p><strong>Développer et réduire les expressions suivantes :</strong></p>
      <div class="questions-overview">
        <p>a) \(S = -4(-5x+2)\)</p>
        <p>b) \(A = -3(2x-3)+4(-22x+5)\)</p>
        <p>c) \(M = -x(15x+7)-2(12x+5)\)</p>
        <p>d) \(U = 3x(11x+8)-3x(12x+4)\)</p>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Appuyez sur ↓ pour la question a)
    </div>
  </section>

  <!-- NIVEAU 1 : Question a) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question a)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(S = -4(-5x+2)\)</p>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p>\[S = -4 \times (-5x) + (-4) \times 2\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <div class="result-box">\(S = 20x - 8\)</div>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Question b) ↓
    </div>
  </section>

  <!-- NIVEAU 2 : Question b) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question b)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(A = -3(2x-3)+4(-22x+5)\)</p>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p>\[\begin{align}
          A &= -6x + 9 - 88x + 20 \\
            &= -94x + 29
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <div class="result-box">\(A = -94x + 29\)</div>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Question c) ↓
    </div>
  </section>

  <!-- NIVEAU 3 : Question c) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question c)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(M = -x(15x+7)-2(12x+5)\)</p>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p>\[\begin{align}
          M &= -15x^2 - 7x - 24x - 10 \\
            &= -15x^2 - 31x - 10
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <div class="result-box">\(M = -15x^2 - 31x - 10\)</div>
      </div>
    </div>

    <div class="nav-hint fragment">
      <i class="fas fa-arrow-down"></i> Question d) ↓
    </div>
  </section>

  <!-- NIVEAU 4 : Question d) -->
  <section>
    <div class="question-header">
      <span class="question-number">Question d)</span>
      <span class="question-time">⏱️ 2 min</span>
    </div>

    <div class="question-recall">
      <p><strong>Développer et réduire :</strong> \(U = 3x(11x+8)-3x(12x+4)\)</p>
    </div>

    <div class="resolution">
      <div class="fragment" data-fragment-index="1">
        <p>\[\begin{align}
          U &= 33x^2 + 24x - 36x^2 - 12x \\
            &= -3x^2 + 12x
        \end{align}\]</p>
      </div>

      <div class="fragment" data-fragment-index="2">
        <div class="result-box">\(U = -3x^2 + 12x\)</div>
      </div>
    </div>
  </section>
</section>
```

## Checklist de validation pour exercices

Avant de livrer une présentation d'exercices, vérifier :

- [ ] Détection du contexte réussie (exercices vs cours)
- [ ] Aucun rappel théorique présent (sauf si explicitement demandé)
- [ ] Format header correct : ligne / durée .. titre .. difficulté
- [ ] Timer global = somme des timers locaux
- [ ] Chaque question a sa propre slide verticale
- [ ] Question rappelée en haut de chaque slide de résolution
- [ ] Timer par question affiché dans le header de la question
- [ ] Résolution progressive avec fragments
- [ ] Navigation hints présents (↓)
- [ ] Densité < 70% sur chaque slide
- [ ] MathJax correctement intégré
- [ ] Si > 6 questions : énoncé découpé en 2 parties (→)

---

**Ce guide garantit des présentations d'exercices optimales, focalisées sur la résolution progressive et la gestion du temps.**
