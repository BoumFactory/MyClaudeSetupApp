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
| `randomizeBranchingQuestions` | bool | non | `true` | Mélanger les alternatives à chaque tentative (OBLIGATOIRE pour éviter le pattern « toujours la première bonne réponse ») |
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

### Recommandation — choix du mode

**Pour un parcours d'évaluation avec QCM (le cas standard) : utiliser `dynamic-score`.**

Avantages :
- H5P **comptabilise automatiquement** les bonnes réponses (somme des `feedback.endScreenScore` des alternatives choisies)
- L'élève voit son score réel à la fin, sans avoir à s'auto-évaluer (l'auto-évaluation honnête est INTERDITE — voir SKILL.md)
- Le score remonte au LMS via xAPI si `includeInteractionsScores: true`

Configuration type :

```json
{
  "scoring": "dynamic-score",
  "includeInteractionsScores": true,
  "randomizeBranchingQuestions": true,
  "nodes": [
    {
      "type": "branching_question",
      "question": "...",
      "alternatives": [
        {"text": "Bonne réponse", "nextContentId": 5, "feedback": {"title": "Bravo", "subtitle": "...", "score": 1}},
        {"text": "Mauvaise réponse", "nextContentId": 4, "feedback": {"title": "Faux", "subtitle": "...", "score": 0}}
      ]
    }
  ]
}
```

**Pour un parcours linéaire à embranchements narratifs (sans QCM scorés) : `static-end-score`** avec un `feedback.score` sur chaque nœud terminal et des `endScreens` paliers :

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
| `image` | Image simple | `image` (chemin local ou objet H5P), `alt` |
| `image_hotspots` | Image à zones cliquables (H5P.ImageHotspots 1.10) | `image`, `hotspots` — voir « Activités variées » |

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
| `blanks` | Texte à trous | `description`, `text` (avec *réponses* dans les trous), `numeric` (bool), `acceptSpellingErrors` (bool) — voir « Réponses saisies » |
| `singlechoiceset` | Serie de choix uniques | `questions` [{question, answers}] (1ere reponse = correcte) |
| `markthewords` | Marquer les mots | `description`, `text` (mots corrects entoures de *asterisques*) |
| `summary` | Affirmation juste à choisir, étape par étape (H5P.Summary 1.10) | `intro`, `statements` [{correct, wrong[], tip}] |
| `dragquestion` | Glisser-déposer sur une image (H5P.DragQuestion 1.14) | `image`, `zones` [{label, x, y, width, height, correct[]}], `draggables` [{text}] |
| `dialogcards` | Cartes recto-verso (H5P.Dialogcards 1.9) | `cards` [{front, back}], `description`, `mode` |

`imagehotspots` n'existe PAS comme interaction : H5P.ImageHotspots n'est pas autorisée dans une
diapositive par CoursePresentation 1.25 (le validateur le refuse). Utiliser le nœud `image_hotspots`.

#### Position des interactions

| Champ | Type | Description |
|-------|------|-------------|
| `x` | number (0-100) | Position horizontale (% du canvas) |
| `y` | number (0-100) | Position verticale (% du canvas) |
| `width` | number (0-100) | Largeur (% du canvas) |
| `height` | number (0-100) | Hauteur (% du canvas) |

#### Disposition de la diapositive : champ `layout` (30/09/2026)

Sans champ `layout`, le texte d'une diapositive occupe **tout le cadre** (0, 0, 100, 100) : une activité
placée par-dessus le recouvre. Le champ `layout`, porté par la **diapositive**, règle la répartition.

| Champ de la diapositive | Valeurs | Effet |
|-------------------------|---------|-------|
| `layout` | `"full"` (défaut) | Texte plein cadre, activité à ses coordonnées par défaut (x 5, y 40, largeur 90, hauteur 55) : **comportement historique, archive identique**. |
| | `"text-left"` | Texte dans la colonne de gauche (x 0, largeur 45 %) ; activité à droite (x 47, y 3, largeur 53 %, hauteur 94 %). |
| | `"text-top"` | Texte en haut (hauteur 25 %, pleine largeur) ; activité dessous (x 3, y 27, largeur 94 %, hauteur 71 %). |
| `text_width` | nombre 10 à 90 | Facultatif, avec `text-left` : largeur du texte, en % (défaut 45). |
| `text_height` | nombre 10 à 90 | Facultatif, avec `text-top` : hauteur du texte, en % (défaut 25). |

Une interaction qui porte ses propres `x`, `y`, `width`, `height` **les garde** : seuls les champs absents
reçoivent la valeur de la disposition.

```json
{
  "layout": "text-left",
  "content": "<h3>Le tableau</h3><p>Énoncé long, données chiffrées…</p>",
  "interactions": [
    {"type": "multichoice", "question": "Calculer …", "answers": [ … ]}
  ]
}
```

Le validateur refuse une valeur de `layout` inconnue et avertit quand le rectangle du texte et celui d'une
interaction se recouvrent (rectangles calculés, coordonnées propres comprises), quand l'activité sort du
cadre, ou quand un texte de plus de 250 caractères reste en `full` avec une activité.

Choisir `text-left` pour un énoncé long (tableau, arbre décrit, données) et `text-top` pour un texte
de quelques lignes. Un QCM qui affiche ses retours défile dans son cadre s'il est trop bas : ne pas
descendre `text_height` au-delà de 35 avec un QCM à trois propositions ou plus.

**Un outil amont qui produit le preplan doit émettre `layout`** (une valeur par diapositive)
plutôt que d'écrire « texte à gauche, activité à droite » dans le texte du prompt : le générateur applique
alors la répartition, sans que le rédacteur calcule de coordonnées. Exemple jouable, avec captures à
1366 × 768 : `examples/dispositions_diapo/`.

**Scores** : en `dynamic-score` avec `includeInteractionsScores: true` (défaut), les scores des quiz de CoursePresentation remontent au carnet Moodle ; en `static-end-score`, non. Détail : SKILL.md, « REGLES CRITIQUES > 1 » (correction du 26/07/2026).

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
  "image": "figures/schema.png",
  "alt": "Schema des fractions",
  "nextContentId": 2
}
```

`image` : chemin local (relatif au dossier du preplan), copié dans l'archive — voir « Images
locales ». Un objet H5P déjà formé (`{path, mime, width, height}`) reste accepté tel quel.

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

## Activités variées (ajout du 30/09/2026)

Quatre types ajoutés le 30/09/2026, que des outils amont peuvent
reprendre tels quels (ne pas les modifier à la légère). Exemple complet et jouable :
`examples/activites_variees/` (preplan, figures, archive, captures du lecteur réel).

| Type | Où | Librairie | Autorisation vérifiée |
|------|----|-----------|-----------------------|
| `summary` | interaction de diapositive | H5P.Summary 1.10 | `semantics.json` de CoursePresentation 1.25 |
| `dragquestion` | interaction de diapositive | H5P.DragQuestion 1.14 | idem |
| `dialogcards` | interaction de diapositive | H5P.Dialogcards 1.9 | idem |
| `image_hotspots` | **nœud** | H5P.ImageHotspots 1.10 | `semantics.json` de BranchingScenario 1.8 (absente de la liste de CoursePresentation 1.25) |

Libellés d'interface en français écrits par le générateur. Scores : `summary` et `dragquestion`
comptent dans la note de la présentation ; `dialogcards` et `image_hotspots` n'exposent aucun
score (pas de `getMaxScore` dans leur code) : activités de mémorisation et de découverte.

### Images locales

Tout champ `image` de ces types (et du nœud `image`) accepte un **chemin local** : relatif au
dossier du preplan, ou absolu. Formats : PNG, JPEG, GIF. Le générateur copie le fichier dans
`content/images/<nom>-<empreinte>.<ext>` et lit ses dimensions dans l'en-tête. Le validateur
signale une image introuvable ou d'un autre format.

### Positions en pourcentages du cadre de l'image

Toutes les positions (zones de dépôt, étiquettes, points cliquables) s'expriment en **% du cadre
de l'image** : `x`, `y` = coin haut gauche, `width`, `height` = taille, de 0 à 100, axe vertical
vers le bas. Astuce : dessiner la figure dans un repère `[0, 100] x [0, 100]` qui couvre
exactement l'image (voir `examples/activites_variees/make_images.py`) ; les coordonnées de dessin
sont alors directement les pourcentages.

### Interaction summary

```json
{
  "type": "summary",
  "x": 4, "y": 14, "width": 92, "height": 84,
  "intro": "À chaque étape, choisis l'affirmation juste.",
  "statements": [
    {"correct": "La probabilité d'un chemin est le produit des probabilités de ses branches.",
     "wrong": ["La probabilité d'un chemin est la somme des probabilités de ses branches."],
     "tip": "Pense à P(A ∩ B)."}
  ]
}
```

- Chaque étape : une affirmation juste (`correct`), au moins une fausse (`wrong`), un indice
  facultatif (`tip`). H5P mélange l'affichage ; l'élève avance quand il a trouvé la juste. Note :
  1 point par étape réussie **du premier coup** (`summary.js` l. 106-115).
- MathJax **accepté** (rendu vérifié dans le lecteur).

### Interaction dragquestion

```json
{
  "type": "dragquestion",
  "x": 42, "y": 2, "width": 56, "height": 96,
  "image": "arbre_a_completer.png",
  "zones": [
    {"label": "Branche vers A", "x": 17.5, "y": 25, "width": 11, "height": 8, "correct": [0]},
    {"label": "Branche vers Ā", "x": 17.5, "y": 47, "width": 11, "height": 8, "correct": [1]}
  ],
  "draggables": [
    {"text": "0,3", "width": 10, "height": 7},
    {"text": "0,7", "width": 10, "height": 7},
    {"text": "0,5", "width": 10, "height": 7}
  ]
}
```

| Champ | Requis | Description |
|-------|--------|-------------|
| `image` | oui | chemin local de la figure (fond de l'exercice) |
| `zones[].x/y/width/height` | oui | zone de dépôt, en % du cadre de l'image |
| `zones[].correct` | oui | indices (dans `draggables`) des étiquettes justes pour cette zone |
| `zones[].label` | non | nom lu par les lecteurs d'écran (`Zone n` par défaut) ; texte brut |
| `zones[].showLabel` / `tip` / `feedbackCorrect` / `feedbackIncorrect` / `single` / `autoAlign` | non | options H5P (défauts : `false`, `""`, `""`, `""`, `false`, `true`) |
| `draggables[].text` | oui | texte de l'étiquette, **texte brut sans MathJax** |
| `draggables[].x/y` | non | position de départ en % ; **absents : rangement automatique en rangées centrées dans la bande du bas** (10,5 % de hauteur par rangée, 12 x 9 % par défaut) |
| `draggables[].width/height` | non | taille en % (défaut 12 x 9) |
| `draggables[].allowedZones` | non | indices des zones où l'étiquette peut être posée (défaut : toutes) |
| `penalties` | non | `true` : une étiquette mal placée retire 1 point (défaut `false`) |
| `zoneOpacity` | non | opacité du fond gris des zones, 0-100 (défaut 40 : la figure reste lisible dessous) |
| `zoneHighlight` | non | `dragging` (défaut), `always`, `never` |

- Une étiquette qui n'est juste nulle part est un **distracteur** (ici `0,5`).
- **Réserver une bande libre en bas de l'image** pour les étiquettes rangées automatiquement ;
  le validateur signale une zone qui y empiète.
- **Hauteur de l'élément** : l'image prend toute la largeur de l'élément et garde ses
  proportions ; il faut en plus environ 25 % de la hauteur de la diapositive pour le retour, la
  barre de score et « Réessayer » après vérification (mesuré : sinon l'élément défile et coupe le
  haut de l'image). Règle : `height ≥ width x 1,98 x (hauteur/largeur de l'image) + 25`. Le
  validateur calcule la largeur maximale. Mise en page conseillée : consigne à gauche en lignes
  courtes (`<br>`), image à droite sur presque toute la hauteur.
- Conversion (pour mémoire) : `x`, `y` restent en % ; `width`/`height` passent en em avec
  `size.width = 640` (référence d'échelle, police des étiquettes environ 15 px).

### Interaction dialogcards

```json
{
  "type": "dialogcards",
  "x": 15, "y": 12, "width": 70, "height": 86,
  "description": "Lis le recto, réponds dans ta tête, puis retourne la carte.",
  "cards": [
    {"front": "Probabilité de \\(\\overline{A}\\) ?", "back": "\\(P(\\overline{A}) = 1 - P(A)\\)"},
    {"front": "Probabilité d'un chemin ?", "back": "Le produit des probabilités de ses branches.",
     "tipFront": "Suis le chemin de gauche à droite.", "image": "figure.png"}
  ],
  "mode": "normal",
  "random": false
}
```

- `front` / `back` requis ; `tipFront`, `tipBack`, `image`, `imageAlt` facultatifs ; `title`
  facultatif. `mode` : `normal` (défaut, on feuillette) ou `repetition` (l'élève dit s'il savait,
  les cartes ratées reviennent).
- MathJax **accepté** (rendu vérifié au recto comme au verso).

### Nœud image_hotspots

```json
{
  "type": "image_hotspots",
  "title": "Explorer l'arbre complet",
  "image": "arbre_complet.png",
  "alt": "Arbre pondéré complet.",
  "icon": "plus",
  "color": "#1f6feb",
  "hotspots": [
    {"x": 88, "y": 5, "header": "Chemin A puis B",
     "text": "<p>\\(P(A\\cap B)=0{,}3\\times 0{,}6=0{,}18\\)</p>"},
    {"x": 37, "y": 23, "width": 6, "height": 8, "header": "Nœud A",
     "text": "<p>Somme 1 : \\(0{,}6+0{,}4=1\\).</p>"}
  ],
  "nextContentId": 3
}
```

- Un point cliquable est un **point** : sans `width`/`height`, (`x`, `y`) est le **centre** de
  l'icône ; avec, c'est le coin haut gauche d'un rectangle et l'icône va en son centre. Centres
  mesurés dans le lecteur égaux au preplan.
- `header` et/ou `text` (HTML, MathJax accepté) requis ; `icon` parmi `plus`, `minus`, `times`,
  `check`, `question`, `info`, `exclamation` ; `color` de l'icône ; `fullscreen: true` pour
  ouvrir la bulle en plein écran.
- Placer le point **à côté** de ce qu'il commente : l'icône masque ce qu'elle recouvre.
- Nœud de contenu ordinaire : `nextContentId`, `feedback`, `forceContentFinished` forcé à
  `disabled` (aucun signal « terminé »).

## Réponses saisies (textes à trous)

Syntaxe H5P.Blanks 1.14 (`js/blanks.js` l. 735-760) : `*réponse1/réponse2/réponse3:indice*`.

- `/` sépare les réponses acceptées : **une fraction ne peut pas s'écrire `2/5`** dans un trou
  (lu « 2 OU 5 »). Demander la fraction en deux trous (numérateur, dénominateur) ou l'écriture
  décimale, et le dire dans la consigne.
- `:` introduit un **indice** : `*12:30*` attend « 12 » (et affiche l'indice « 30 »).
- Nombres : donner la virgule ET le point (`*0,4/0.4*`), les zéros non significatifs si le
  contexte le permet (`*0,40*`), jamais de MathJax.

### Tolérance aux fautes (mesure M4)

| Champ d'interaction | `acceptSpellingErrors` écrit |
|---------------------|------------------------------|
| aucun (défaut, mots) | `true` |
| `"numeric": true` | `false` |
| `"acceptSpellingErrors": true/false` | la valeur donnée (prioritaire) |

Lecture de `js/cloze.js` l. 43-60 : la tolérance ne distingue pas les nombres des mots. Elle ne
dépend que de la **longueur** de la réponse attendue : plus de 3 caractères, une erreur tolérée
(distance de Damerau-Levenshtein, qui compte aussi une inversion de deux caractères) ; plus de
9, deux. Mesure dans le lecteur réel (`examples/activites_variees/mesure_m4/`), réponses
attendues `0,4`, `0,25`, `1500`, `12,75`, `0,18/0.18`, `parallèle` :

| Saisi | Défaut (tolérance) | `numeric: true` |
|-------|--------------------|-----------------|
| `0,1` (attendu `0,4`) | faux (3 caractères : aucune tolérance) | faux |
| `0,26` (attendu `0,25`) | **juste** | faux |
| `1600` (attendu `1500`) | **juste** | faux |
| `12,57` (attendu `12,75`) | **juste** (inversion) | faux |
| `0,19` (attendu `0,18`) | **juste** | faux |
| `paralèle` (attendu `parallèle`) | juste | faux |

Donc : **toujours `numeric: true` pour une réponse chiffrée**. Avertissements du validateur :
`ANSWER_SINGLE_FORM` (décimal sans son autre écriture), `ANSWER_SLASH_FRACTION` (`*5/3*`),
`ANSWER_TIP_COLON` (`*12:30*`), `ANSWER_NUMERIC_TOLERANCE` (nombre de plus de 3 caractères avec
la tolérance active).

## forceContentFinished (par noeud)

⚠️ **Deux champs homonymes, de types DIFFERENTS** (`h5p_libs/H5P.BranchingScenario-1.8/semantics.json`) :

| Champ | Type | Défaut |
|-------|------|--------|
| `branchingScenario.content[].forceContentFinished` (par nœud) | `select` → **CHAINE** | `"useBehavioural"` |
| `branchingScenario.behaviour.forceContentFinished` (global) | `boolean` | `false` |

Le champ **par nœud** admet **TROIS** valeurs, toutes valides :

| Valeur | Effet | Quand l'utiliser |
|--------|-------|------------------|
| `"useBehavioural"` (DÉFAUT du schema) | Suit le réglage global `behaviour.forceContentFinished` | `course_presentation` / `interactive_video` que le réglage global doit piloter |
| `"enabled"` | BLOQUE le bouton tant que le contenu n'a pas signalé "finished" via xAPI | UNIQUEMENT `course_presentation` ou `interactive_video` avec quiz obligatoires |
| `"disabled"` | Ne bloque JAMAIS, même si le réglage global vaut `true` | `text`, `image`, `video`, `branching_question` : ces types ne signalent jamais "finished" |

⛔ **Le vrai piège n'est pas `"disabled"`, c'est le BOOLEEN.** Le lecteur compare en `===` **strict** sur des chaines (`src/scripts/libraryScreen.js` l. 524-527) :

```js
params.content[id].forceContentFinished === 'enabled'
|| params.content[id].forceContentFinished === 'useBehavioural' && params.behaviour.forceContentFinished === true
```

Un `true`/`false` ne satisfait aucune branche : le verrou est **désactivé en silence, nœud par nœud**, y compris quand le réglage global le demande. Mesuré dans le vrai lecteur (h5p-standalone), paquets identiques à un champ près :

| Champ par nœud | Global | Bouton « Continuer » |
|----------------|--------|----------------------|
| `false` (booléen) | `true` | **actif** — aucun verrou |
| `"useBehavioural"` | `true` | **verrouillé** — « Terminez le contenu pour continuer » |
| `"disabled"` | `true` | **actif** — c'est exactement le sens du mot |
| `true` (booléen) | `false` | **actif** — aucun verrou |
| `"enabled"` | `false` | **verrouillé** |

**Ce que fait le générateur** (`_resolve_force_content_finished`, corrigé le 25/07/2026) : il écrit **toujours l'une des trois chaines**. Absent → `"useBehavioural"` ; ancien booléen `true` → `"enabled"`, `false` → `"useBehavioural"` ; valeur hors schéma → refusée par `validators.py` (erreur bloquante). Sur un nœud `text` / `image` / `video` / `branching_question`, il écrit `"disabled"` : un verrou y serait définitif, et hériter d'un global à `true` bloquerait l'élève pour toujours.

**BUG CONNU** : `"enabled"` sur un nœud `text`, `image` ou `video` = bouton Continuer bloqué à jamais (ces types ne signalent jamais "finished" via xAPI). Le générateur y écrit `"disabled"` automatiquement, avec un message.

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
