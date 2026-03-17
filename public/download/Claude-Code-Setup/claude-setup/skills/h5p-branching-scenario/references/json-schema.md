# Schéma JSON du préplan Branching Scenario

## Structure racine

```json
{
  "title": "Titre du parcours",
  "startScreen": {
    "title": "Titre ecran d'accueil",
    "subtitle": "Description du parcours",
    "image": {},
    "altText": "Description de l'image"
  },
  "scoring": "static-end-score",
  "enableBackwardsNavigation": true,
  "forceContentFinished": false,
  "randomizeBranchingQuestions": false,
  "includeInteractionsScores": true,
  "nodes": [...],
  "endScreens": [...],
  "_meta": {
    "pattern": "diagnostic_differentiation",
    "level": "5eme",
    "theme": "fractions",
    "generated_by": "create_template.py",
    "version": "1.0"
  }
}
```

## Champs racine

| Champ | Type | Requis | Defaut | Description |
|-------|------|--------|--------|-------------|
| `title` | string | oui | - | Titre du parcours |
| `startScreen` | object | non | auto | Écran d'accueil |
| `scoring` | string | non | `no-score` | Mode de scoring |
| `enableBackwardsNavigation` | bool | non | `true` | Bouton retour |
| `forceContentFinished` | bool | non | `false` | Obliger à finir chaque contenu |
| `randomizeBranchingQuestions` | bool | non | `false` | Mélanger les alternatives |
| `includeInteractionsScores` | bool | non | `true` | Compter les scores des interactions (dynamic-score) |
| `nodes` | array | oui | - | Liste des nœuds du parcours |
| `endScreens` | array | non | auto | Écrans de fin |
| `_meta` | object | non | - | Métadonnées (pattern, level, theme) |

## Convention `__TODO__`

Les marqueurs `__TODO__` identifient les champs à remplir dans un template généré par `create_template.py`.

### Nommage

```
__TODO_[CONTEXTE]_[ELEMENT]__
```

Exemples :
- `__TODO_INTRO__` : contenu de l'introduction
- `__TODO_DIAGNOSTIC_QUESTION__` : question du test diagnostique
- `__TODO_SLIDE_EXPERT_1__` : premiere slide du parcours expert
- `__TODO_QUIZ_DEBUTANT__` : question de quiz pour debutants
- `__TODO_BILAN_INTERMEDIAIRE__` : bilan du parcours intermédiaire
- `__TODO_ALT_FB_TITLE_EXPERT__` : titre du feedback de l'alternative expert

### Cycle de vie

1. `create_template.py` génère les `__TODO__`
2. `scan_template.py` les détecte et génère un rapport
3. Le modèle pose des questions challenge
4. Les `__TODO__` sont remplacés par du contenu réel
5. `generate_branching.py --validate` vérifie qu'il n'en reste aucun

## Champ `meta` (metadonnees par noeud)

Chaque noeud peut contenir un champ `meta` (ignore par le generateur H5P mais utilise par le scanner et le workflow) :

```json
{
  "meta": {
    "purpose": "diagnostic",
    "difficulty": "medium",
    "branch": "common",
    "estimated_time_seconds": 60
  }
}
```

| Champ | Valeurs | Description |
|-------|---------|-------------|
| `purpose` | `introduction`, `diagnostic`, `content`, `assessment`, `remediation`, `conclusion`, `dilemma`, `consequence`, `menu` | Rôle pédagogique du nœud |
| `difficulty` | `none`, `easy`, `medium`, `hard` | Niveau de difficulté |
| `branch` | `common`, `expert`, `intermédiaire`, `débutant`, ... | Branche d'appartenance |
| `estimated_time_seconds` | entier | Temps estimé en secondes |

## Scoring

### Options

- `no-score` : pas de score envoye au LMS
- `static-end-score` : score fixe par écran de fin (défini dans endScreens et feedback.score)
- `dynamic-score` : score basé sur les interactions dans le parcours

### Limitation xAPI (IMPORTANT)

**Les scores des quiz embarques dans CoursePresentation ne remontent PAS au carnet Moodle.**

Seul `endScreenScore` (configuré manuellement par nœud terminal via `feedback.score`) est envoyé via xAPI au LMS. Cela signifie :

- Les quiz dans les slides CoursePresentation sont utiles pour l'apprentissage mais pas pour la notation
- Pour un scoring fiable dans Moodle, utiliser `static-end-score`
- Chaque noeud terminal (`nextContentId: -1`) doit avoir un `feedback.score`
- Les endScreens définissent les paliers de score visibles

### Recommandation

Utiliser **`static-end-score`** pour tous les parcours destines a Moodle :

```json
{
  "scoring": "static-end-score",
  "nodes": [
    {
      "title": "Fin expert",
      "type": "text",
      "content": "<p>Bravo !</p>",
      "nextContentId": -1,
      "feedback": { "title": "Excellent", "subtitle": "...", "score": 100 }
    }
  ],
  "endScreens": [
    { "title": "Excellent", "subtitle": "...", "score": 100 },
    { "title": "Bien", "subtitle": "...", "score": 70 },
    { "title": "A retravailler", "subtitle": "...", "score": 30 }
  ]
}
```

## Nodes (liste des noeuds)

Chaque nœud est un objet dans le tableau `nodes`. Son **index** (0, 1, 2...) est utilisé par `nextContentId` pour le branchement.

### Types de noeuds

| Type | Description | Champs specifiques |
|------|-------------|-------------------|
| `text` | Texte riche (HTML) | `content` |
| `branching_question` | Question d'embranchement | `question`, `alternatives` |
| `course_presentation` | Diaporama H5P avec quiz embarqués | `slides` (avec `interactions`) |
| `interactive_video` | Vidéo avec questions aux timestamps | `videoUrl`, `interactions` |
| `video` | Vidéo YouTube ou fichier | `videoUrl` |
| `image` | Image simple | `image`, `alt` |

### Noeud commun

```json
{
  "title": "Titre du noeud",
  "type": "text",
  "showTitle": true,
  "proceedText": "Continuer",
  "nextContentId": 1,
  "feedback": {
    "title": "Feedback titre",
    "subtitle": "Feedback detail",
    "score": 50
  },
  "meta": {
    "purpose": "content",
    "difficulty": "medium",
    "branch": "common",
    "estimated_time_seconds": 60
  }
}
```

**nextContentId** : index du noeud suivant, ou `-1` pour fin de scenario.

### Noeud text

```json
{
  "title": "Introduction",
  "type": "text",
  "content": "<p>Bienvenue dans ce <strong>parcours adaptatif</strong>.</p>",
  "nextContentId": 1
}
```

Le contenu est du HTML. Balises supportées : `<p>`, `<strong>`, `<em>`, `<ul>`, `<ol>`, `<li>`, `<h2>`, `<h3>`, `<sub>`, `<sup>`, `<pre>`, `<code>`, `<a>`.

Pour les maths, syntaxe MathJax : `\(formule\)` inline, `\[formule\]` display.

### Noeud branching_question

```json
{
  "title": "As-tu compris les fractions ?",
  "type": "branching_question",
  "question": "<p>Que vaut \\(\\frac{1}{2} + \\frac{1}{3}\\) ?</p>",
  "alternatives": [
    {
      "text": "5/6",
      "nextContentId": 3,
      "feedback": { "title": "Bravo !", "subtitle": "Bonne réponse.", "score": 100 }
    },
    {
      "text": "2/5",
      "nextContentId": 5,
      "feedback": { "title": "Pas tout à fait...", "subtitle": "Revoyons la méthode.", "score": 0 }
    }
  ]
}
```

**Règles alternatives** :
- Minimum 2 alternatives
- Chaque alternative a un `text` (requis) et un `nextContentId` (requis)
- `feedback` optionnel mais fortement recommande
- `nextContentId: -1` mène vers un écran de fin

### Noeud course_presentation (avec quiz embarques)

```json
{
  "title": "Rappel de cours avec quiz",
  "type": "course_presentation",
  "slides": [
    {
      "content": "<h2>Les fractions</h2><p>Une fraction représente...</p>",
      "interactions": []
    },
    {
      "content": "<h2>Quiz</h2>",
      "interactions": [
        {
          "type": "multichoice",
          "x": 5, "y": 40, "width": 90, "height": 55,
          "question": "Que vaut 1/2 + 1/4 ?",
          "answers": [
            {"text": "3/4", "correct": true, "feedback": "Correct !"},
            {"text": "2/6", "correct": false, "feedback": "Non, il faut un dénominateur commun."},
            {"text": "1/6", "correct": false, "feedback": "Non."}
          ]
        }
      ]
    }
  ],
  "nextContentId": 2
}
```

#### Types d'interactions dans les slides

| Type | Description | Champs |
|------|-------------|--------|
| `multichoice` | QCM | `question`, `answers` [{text, correct, feedback}] |
| `truefalse` | Vrai/Faux | `question`, `correct` (bool), `feedback_correct`, `feedback_incorrect` |
| `dragtext` | Glisser-déposer | `description`, `text` (avec *mots* à placer) |
| `blanks` | Texte à trous | `description`, `text` (avec *réponses* dans les trous) |
| `singlechoiceset` | Serie de choix uniques | `questions` [{question, answers}] (1ere reponse = correcte) |
| `markthewords` | Marquer les mots | `description`, `text` (mots corrects entoures de *asterisques*) |

#### Position des interactions

| Champ | Type | Description |
|-------|------|-------------|
| `x` | number (0-100) | Position horizontale (% du canvas) |
| `y` | number (0-100) | Position verticale (% du canvas) |
| `width` | number (0-100) | Largeur (% du canvas) |
| `height` | number (0-100) | Hauteur (% du canvas) |

**IMPORTANT** : Les scores des quiz dans CoursePresentation ne remontent PAS au carnet Moodle. Ils sont uniquement utiles pour l'apprentissage.

### Noeud interactive_video

```json
{
  "title": "Video explicative",
  "type": "interactive_video",
  "videoUrl": "https://www.youtube.com/watch?v=XXXXX",
  "interactions": [
    {
      "type": "multichoice",
      "time": 30,
      "duration": 10,
      "pause": true,
      "question": "Qu'avez-vous retenu ?",
      "answers": [
        {"text": "Reponse A", "correct": true},
        {"text": "Reponse B", "correct": false}
      ],
      "x": 10, "y": 10, "width": 80, "height": 60
    },
    {
      "type": "truefalse",
      "time": 60,
      "pause": true,
      "question": "La fraction 1/2 est égale à 0,5",
      "correct": true
    }
  ],
  "nextContentId": 3
}
```

| Champ interaction | Type | Description |
|-------------------|------|-------------|
| `time` | number | Timestamp en secondes ou la question apparait |
| `duration` | number | Durée d'affichage en secondes (défaut: 10) |
| `pause` | bool | Mettre la video en pause (defaut: true) |
| `label` | string | Etiquette de l'interaction |

### Noeud video

```json
{
  "title": "Video explicative",
  "type": "video",
  "videoUrl": "https://www.youtube.com/watch?v=XXXXX",
  "nextContentId": 2
}
```

### Noeud image

```json
{
  "title": "Schema recapitulatif",
  "type": "image",
  "alt": "Schema des fractions",
  "nextContentId": 2
}
```

## EndScreens (ecrans de fin)

```json
{
  "endScreens": [
    { "title": "Excellent !", "subtitle": "Tu maitrises les fractions.", "score": 100 },
    { "title": "Bien !", "subtitle": "Continue a t'entrainer.", "score": 70 },
    { "title": "A retravailler", "subtitle": "Revois le cours.", "score": 30 }
  ]
}
```

| Champ | Type | Description |
|-------|------|-------------|
| `title` | string | Titre de l'écran de fin |
| `subtitle` | string | Message detaille |
| `score` | number | Score envoye au LMS (0-100) |
| `image` | object | Image optionnelle |

## Logique de branchement

Le branchement fonctionne par **references d'index** :

```
nodes[0] -> nextContentId: 1
nodes[1] -> type: branching_question
             alt[0].nextContentId: 2  (branche A)
             alt[1].nextContentId: 4  (branche B)
nodes[2] -> nextContentId: 3
nodes[3] -> nextContentId: -1         (fin scenario -> endScreens[0])
nodes[4] -> nextContentId: 5
nodes[5] -> nextContentId: -1         (fin scenario -> endScreens[1])
```

**Convention** : `nextContentId = -1` signifie "fin de scenario".

## Interactions singlechoiceset

```json
{
  "type": "singlechoiceset",
  "x": 5, "y": 40, "width": 90, "height": 55,
  "questions": [
    {
      "question": "Quel est le denominateur de 3/4 ?",
      "answers": ["4", "3", "7"]
    },
    {
      "question": "Que vaut 1/2 + 1/2 ?",
      "answers": ["1", "2/4", "1/4"]
    }
  ]
}
```

**Convention** : la premiere reponse de `answers` est toujours la correcte. Les reponses sont melangees automatiquement par H5P.

## Interactions markthewords

```json
{
  "type": "markthewords",
  "x": 5, "y": 40, "width": 90, "height": 55,
  "description": "Marque les mots qui designent des fractions.",
  "text": "Le *denominateur* est en bas de la *fraction* et le numerateur est en haut."
}
```

**Convention** : les mots corrects a marquer sont entoures de `*asterisques*`. Le texte non marque est un distracteur.

**ATTENTION** : pas de LaTeX/MathJax dans le texte markthewords.

## forceContentFinished (par noeud)

Chaque noeud peut definir `forceContentFinished` pour controler le bouton "Continuer" :

| Valeur | Effet | Quand l'utiliser |
|--------|-------|------------------|
| `"disabled"` (DÉFAUT) | Bouton Continuer toujours actif | **Texte, Image, Vidéo** — ces types ne signalent PAS "finished" |
| `"enabled"` | BLOQUE le bouton tant que le contenu n'a pas signalé "finished" | CoursePresentation avec quiz obligatoires, InteractiveVideo |
| `"useBehavioural"` | Suit le setting global `behaviour.forceContentFinished` | Quand on veut un comportement uniforme |

**BUG CONNU** : `"enabled"` sur un nœud `text` ou `image` = bouton Continuer bloqué à jamais (AdvancedText ne signale jamais "finished"). Toujours utiliser `"disabled"` pour ces types.

```json
{
  "title": "Slide de cours",
  "type": "course_presentation",
  "forceContentFinished": "enabled",
  "slides": [...]
}
```

## LaTeX / MathJax dans H5P

### Delimiteurs

| Type | Syntaxe | Exemple |
|------|---------|---------|
| Inline | `\(` ... `\)` | `\(\frac{1}{2}\)` |
| Display | `\[` ... `\]` | `\[\sum_{i=1}^{n} i\]` |

**NE PAS utiliser** `$` ou `$$` (non supportes par H5P/MathJax).

### Extensions MathJax

Certaines commandes necessitent `\require{extension}` une seule fois dans le document :

| Commande | Extension | Usage |
|----------|-----------|-------|
| `\cancel`, `\bcancel`, `\xcancel` | `\require{cancel}` | Barrer un terme |
| `\color`, `\colorbox` | `\require{color}` | Colorer du texte math |
| `\enclose` | `\require{enclose}` | Entourer du texte |

Exemple : `\(\require{cancel}\frac{\cancel{3}}{7}\)`

### Commandes non supportees

| Commande | Alternative |
|----------|-------------|
| `\newcommand` | Ecrire la formule en entier |
| `\usepackage` | Utiliser `\require{...}` |
| `\begin{align*}` | Utiliser `\[` ... `\]` avec `\\` pour les sauts de ligne |

### Zones sans LaTeX

Le LaTeX/MathJax est **interdit** dans :
- Les trous `*...*` des interactions `dragtext` et `blanks`
- Le texte des interactions `markthewords`
- Les zones de glisser-deposer

Le validateur detecte automatiquement ces cas.

## Points de convergence

Pour faire converger des branches vers un meme noeud :

```
nodes[0] -> branching_question
             alt[0].nextContentId: 1  (branche facile)
             alt[1].nextContentId: 3  (branche difficile)
nodes[1] -> nextContentId: 2          (facile etape 1)
nodes[2] -> nextContentId: 5          (CONVERGENCE -> noeud commun)
nodes[3] -> nextContentId: 4          (difficile etape 1)
nodes[4] -> nextContentId: 5          (CONVERGENCE -> noeud commun)
nodes[5] -> contenu commun -> -1      (fin)
```

## Patterns predefinis

4 patterns sont disponibles via `create_template.py` :

### 1. `diagnostic_differentiation`

Q diagnostic > branches par niveau > fins differenciees.

```
[Intro] > [Q diagnostic]
  Expert       > [Contenu avance + quiz] > [Bilan 100%]
  Intermediaire > [Contenu moyen + quiz] > [Bilan 70%]
  Debutant     > [Contenu base + quiz]   > [Bilan 40%]
```

### 2. `remediation_loop`

Contenu > test > reussi/echoue > remediation > retest.

```
[Cours] > [Test]
  Reussi  > [Fin 100%]
  Echoue  > [Remediation + quiz] > [Retest]
    Reussi  > [Fin 70%]
    Echoue  > [Fin 30%]
```

### 3. `scenario_dilemmes`

Situation > choix > consequences > nouveaux choix.

```
[Situation] > [Choix 1/2/3]
  Choix A > [Consequence A] > [2nd choix]
  Choix B > [Consequence B] > [2nd choix]
  Choix C > [Consequence C] > [Fin 30%]
  2nd choix > [Fin A 100%] / [Fin B 70%]
```

### 4. `student_choice`

Menu > parcours paralleles > fins individuelles.

```
[Accueil] > [Choix parcours]
  Decouverte    > [3 etapes] > [Fin 60%]
  Entrainement  > [4 etapes] > [Fin 80%]
  Expert        > [2 etapes] > [Fin 100%]
```
