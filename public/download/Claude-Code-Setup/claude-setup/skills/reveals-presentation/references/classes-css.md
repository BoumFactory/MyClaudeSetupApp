# Classes CSS prédéfinies, styles par contexte et fragments

À lire quand on remplit un template : liste exhaustive des classes disponibles (à utiliser telles quelles, sans en créer), rappel des styles de chaque contexte et classes de fragments.

Les classes suivantes sont **prédéfinies** et doivent être utilisées telles quelles :

**Boxes et conteneurs** :
- `.box-info`, `.box-warning`, `.box-success`, `.box-error` : Boîtes colorées
- `.result-box` : Boîte de résultat encadré
- `.formula-box` : Boîte pour formules importantes

**Exercices** :
- `.exercise` : Container principal pour un exercice
- `.exercise-header` : En-tête avec difficulté et temps
- `.difficulty` : Étoiles de difficulté (★★☆)
- `.estimated-time` : Temps estimé (⏱ X minutes)
- `.statement` : Énoncé de l'exercice
- `.questions-overview` : Liste des questions d'un exercice
- `.question-header` : En-tête d'une question individuelle
- `.question-number` : Numéro de la question (ex: "Question a)")
- `.question-time` : Temps pour une question spécifique
- `.question-recall` : Rappel de la question sur une slide de résolution
- `.resolution` : Zone de résolution d'une question

**Questions et réponses** :
- `.question` : Boîte question (fond bleu clair)
- `.answer` : Boîte réponse (fond vert clair)

**Plan** :
- `.plan-slide` : Classe pour la slide de plan

**Mise en forme** :
- `.highlight` : Texte en rouge accentué
- `.two-columns` : Layout 2 colonnes
- `.nav-hint` : Indication de navigation (↓ →). Ce bloc est positionné en `absolute` en bas de la diapositive ; le CSS des templates réserve automatiquement un `padding-bottom` sous tout `<section>` qui en contient un, pour ne jamais recouvrir le contenu d'une diapositive dense (tableau, deux colonnes). Ne pas ajouter de `<p>&nbsp;</p>` ou d'espaceur manuel avant un `.nav-hint` : ce n'est plus nécessaire.

Ces classes sont disponibles dans **les trois gabarits** (`template-college.html`, `template-lycee.html`, `template-academique.html`). Le style académique dispose en plus de classes propres à l'argumentation scientifique (voir plus bas).

**Classes spécifiques au style académique** (`template-academique.html` uniquement, en plus des boîtes et de la mise en forme communes) :
- `.theorem` / `.theorem-title` : Énoncé de théorème et son titre
- `.definition` / `.definition-title` : Définition et son titre
- `.proof` / `.proof-title` : Démonstration et son titre
- `.reference` : Bloc de référence bibliographique
- `.citation` : Citation mise en exergue
- `.emphasis` : Emphase sobre (alternative à `.highlight` pour ce style)
- `.bibliography` : Liste de références en fin de présentation

Ce style n'a pas vocation à contenir des `.exercise`/`.question`/`.question-header` (destinés aux styles collège et lycée) : une conférence académique s'appuie sur théorèmes, définitions et démonstrations plutôt que sur des exercices chronométrés.

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

## Classes CSS utiles (rappel des définitions)

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
