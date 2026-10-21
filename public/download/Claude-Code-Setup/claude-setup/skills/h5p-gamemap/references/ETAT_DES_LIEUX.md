# État des lieux - H5P Game Map

## Types de contenus supportés

### Contenus actuellement implémentés

| Type | Library H5P | Version | Usage | Syntaxe spéciale |
|------|-------------|---------|-------|------------------|
| **MultiChoice** | `H5P.MultiChoice` | 1.16 | QCM classique | LaTeX via `\(formule\)` |
| **TrueFalse** | `H5P.TrueFalse` | 1.8 | Vrai/Faux | - |
| **DragText** | `H5P.DragText` | 1.10 | Glisser-déposer mots | `*mot*` pour drag |
| **Blanks** | `H5P.Blanks` | 1.14 | Textes à trous | `*mot*` pour trou |

### Contenus prioritaires à implémenter

| Type | Library H5P | Version | Usage | Priorité |
|------|-------------|---------|-------|----------|
| **AdvancedText** | `H5P.AdvancedText` | 1.1 | Étapes "respiration" (rappel, checkpoint) | ★★★ CRITIQUE |
| **SingleChoiceSet** | `H5P.SingleChoiceSet` | 1.11 | Quiz rapide multi-questions | ★★★ HAUTE |
| **QuestionSet** | `H5P.QuestionSet` | 1.20 | Boss final, mix de types | ★★★ HAUTE |
| **MarkTheWords** | `H5P.MarkTheWords` | 1.11 | Sélectionner les bons mots | ★★ MOYENNE |
| **SortParagraphs** | `H5P.SortParagraphs` | 0.11 | Ordonner étapes démonstration | ★★ MOYENNE |

### Contenus optionnels

| Type | Library H5P | Version | Usage | Notes |
|------|-------------|---------|-------|-------|
| **MemoryGame** | `H5P.MemoryGame` | 1.3 | Jeu de mémoire | Nécessite images |
| **DialogCards** | `H5P.Dialogcards` | 1.9 | Flashcards | Vocabulaire |

### AdvancedText - Étapes "respiration" (ESSENTIEL)

**Objectif** : Éviter l'effet "exercices en batterie" en insérant des pauses informatives.

```json
{
  "library": "H5P.AdvancedText 1.1",
  "params": {
    "text": "<h3>🏕️ Checkpoint !</h3><p>Tu as parcouru la moitié du chemin.</p><p><strong>Rappelle-toi :</strong></p><ul><li>Une suite est une fonction de \\(\\mathbb{N}\\) vers \\(\\mathbb{R}\\)</li><li>La notation \\((u_n)\\) désigne la suite entière</li></ul><p><em>Continue, le sommet est proche !</em></p>"
  }
}
```

**Caractéristiques** :
- **Pas de score** : l'élève clique "Continuer" sans pression
- **HTML complet** : titres, listes, images, LaTeX
- **Quand l'utiliser** :
  - Après 3-4 étapes de quiz (respiration)
  - Avant un boss final (récapitulatif)
  - Pour introduire une nouvelle zone

---

## Paramètres comportementaux (behaviour)

### Configuration globale du jeu

```json
"behaviour": {
  "enableRetry": true,              // Permettre de réessayer
  "enableSolutionsButton": true,    // Afficher bouton solutions
  "lives": 4,                       // Nombre de vies (null = illimité)
  "globalTimeLimit": null,          // Limite temps globale en secondes
  "finishScore": null,              // Score minimum pour terminer
  "map": {
    "showLabels": true,             // Afficher noms des étapes
    "roaming": "complete",          // Mode de progression
    "fog": "visited"                // Mode de brouillard
  }
}
```

### Modes de roaming (progression)

| Mode | Description | Usage recommandé |
|------|-------------|------------------|
| `free` | Navigation libre, toutes les étapes accessibles | Découverte, exploration |
| `complete` | Doit réussir une étape pour débloquer les voisines | Apprentissage progressif |
| `strict` | Doit réussir avec score parfait pour avancer | Évaluation formative |

### Modes de brouillard (fog)

| Mode | Description | Usage recommandé |
|------|-------------|------------------|
| `none` | Tout visible dès le départ | Parcours court, vue d'ensemble |
| `visited` | Seules les étapes visitées sont visibles | Standard, suspense modéré |
| `all` | Brouillard total au début | Aventure, découverte |

### Paramètres par stage

```json
{
  "time": {
    "timeLimit": 60,                // Limite temps en secondes (optionnel)
    "showTimeLimit": true           // Afficher le temps restant
  },
  "accessRestrictions": {
    "allOrAnyRestrictionSet": "all",
    "restrictionSetList": [{
      "allOrAnyRestriction": "any",
      "restrictionList": [{"restrictionType": "totalScore"}]
    }]
  },
  "specialStageExtraLives": 0,      // Vies bonus gagnées
  "specialStageExtraTime": 0        // Temps bonus gagné
}
```

---

## Paramètres visuels (visual)

### Couleurs des stages

```json
"visual": {
  "stages": {
    "colorStage": "rgba(52, 152, 219, 0.85)",      // Non visité (bleu)
    "colorStageLocked": "rgba(127, 140, 141, 0.7)", // Verrouillé (gris)
    "colorStageCleared": "rgba(46, 204, 113, 0.85)", // Réussi (vert)
    "showScoreStars": "always"                      // never|visited|always
  }
}
```

### Styles de chemins

```json
"paths": {
  "displayPaths": true,
  "style": {
    "colorPath": "rgba(44, 62, 80, 0.6)",          // Couleur normale
    "colorPathCleared": "rgba(46, 204, 113, 0.7)", // Couleur après réussite
    "pathWidth": "0.25",                            // Épaisseur (0.1 à 0.5)
    "pathStyle": "dotted"                           // solid|dotted|dashed
  }
}
```

### Animations et effets

```json
"misc": {
  "useAnimation": true    // Activer les animations
}
```

---

## Écrans de titre et de fin

### Écran de titre

```json
"showTitleScreen": true,
"titleScreen": {
  "titleScreenIntroduction": "<p>Contenu HTML avec mise en forme...</p>"
}
```

### Écran de fin - Succès

```json
"endScreen": {
  "success": {
    "endScreenTextSuccess": "<p><strong>Bravo !</strong></p><p>Message de victoire</p>",
    "endScreenMedia": {
      "path": "images/success.png",
      "mime": "image/png"
    }
  }
}
```

### Écran de fin - Échec

```json
"noSuccess": {
  "endScreenTextNoSuccess": "<p><strong>Dommage !</strong></p><p>Message d'encouragement</p>",
  "endScreenMedia": {
    "path": "images/failure.png",
    "mime": "image/png"
  }
}
```

### Feedbacks globaux par score

```json
"overallFeedback": [
  {"from": 0, "to": 40, "feedback": "Continue tes efforts !"},
  {"from": 41, "to": 70, "feedback": "Bon travail, tu progresses !"},
  {"from": 71, "to": 99, "feedback": "Excellent ! Tu maîtrises presque tout."},
  {"from": 100, "to": 100, "feedback": "Parfait ! Tu es un expert !"}
]
```

---

## Audio

```json
"audio": {
  "backgroundMusic": {
    "params": {
      "files": [{
        "path": "audios/music.mp3",
        "mime": "audio/mpeg"
      }]
    },
    "muteDuringExercise": true    // Couper pendant les exercices
  },
  "ambient": {}                    // Sons d'ambiance (optionnel)
}
```

---

## Feedbacks par type de question

### MultiChoice - Feedback par réponse

```json
{
  "answers": [
    {
      "text": "<div>\\(u_5 = 11\\)</div>",
      "correct": true,
      "tipsAndFeedback": {
        "tip": "Remplace n par 5",
        "chosenFeedback": "<div>Bravo ! \\(u_5 = 2 \\times 5 + 1 = 11\\)</div>",
        "notChosenFeedback": ""
      }
    }
  ],
  "overallFeedback": [
    {"from": 0, "to": 0, "feedback": "Incorrect. Relis la question."},
    {"from": 100, "to": 100, "feedback": "Parfait !"}
  ]
}
```

### DragText - Syntaxe

```
Le *premier* terme est noté *u_0* ou *u_1* selon les conventions.
```

- Les mots entre `*...*` deviennent des zones de drag
- Le texte environnant supporte LaTeX `\(formule\)`
- **Limitation** : Les mots à glisser NE supportent PAS le LaTeX

### Blanks - Syntaxe

```
Une suite est une *fonction:fonction mathématique* de \\(\\mathbb{N}\\) vers \\(\\mathbb{R}\\).
```

- Format : `*réponse:indice*` ou simplement `*réponse*`
- Le texte environnant supporte LaTeX
- Possibilité d'accepter plusieurs réponses : `*réponse1/réponse2*`

### TrueFalse - Structure

```json
{
  "correct": "true",  // ou "false" (string, pas boolean !)
  "l10n": {
    "wrongAnswerMessage": "Incorrect, car...",
    "correctAnswerMessage": "Exact ! C'est bien..."
  }
}
```

---

## Structure technique d'un stage

```json
{
  "id": "uuid-généré",
  "label": "Nom affiché de l'étape",
  "telemetry": {
    "x": "50",        // Position X en % (0-100)
    "y": "30",        // Position Y en % (0-100)
    "width": "6",     // Largeur du hotspot
    "height": "10"    // Hauteur du hotspot
  },
  "neighbors": ["0", "2"],  // INDICES string des stages adjacents
  "type": "stage",
  "canBeStartStage": false, // true seulement pour le premier
  "contentsList": [{
    "contentType": {
      "params": {...},      // Paramètres du type H5P
      "library": "H5P.MultiChoice 1.16",
      "metadata": {...},
      "subContentId": "uuid"
    }
  }]
}
```

**IMPORTANT** : Les `neighbors` sont des **indices string** ("0", "1", "2"...), PAS des UUIDs !

---

## Dépendances h5p.json

```json
{
  "title": "Titre du parcours",
  "language": "fr",
  "mainLibrary": "H5P.GameMap",
  "embedTypes": ["iframe"],
  "license": "CC BY-SA",
  "preloadedDependencies": [
    {"machineName": "H5P.GameMap", "majorVersion": "1", "minorVersion": "5"},
    {"machineName": "H5P.MultiChoice", "majorVersion": "1", "minorVersion": "16"},
    {"machineName": "H5P.DragText", "majorVersion": "1", "minorVersion": "10"},
    {"machineName": "H5P.Blanks", "majorVersion": "1", "minorVersion": "14"},
    {"machineName": "H5P.TrueFalse", "majorVersion": "1", "minorVersion": "8"},
    {"machineName": "H5P.SingleChoiceSet", "majorVersion": "1", "minorVersion": "11"},
    {"machineName": "H5P.QuestionSet", "majorVersion": "1", "minorVersion": "20"},
    {"machineName": "H5P.Question", "majorVersion": "1", "minorVersion": "5"},
    {"machineName": "H5P.JoubelUI", "majorVersion": "1", "minorVersion": "3"},
    {"machineName": "FontAwesome", "majorVersion": "4", "minorVersion": "5"}
  ]
}
```

---

## Styles de parcours recommandés

| Style | Vies | Roaming | Fog | Ambiance | Usage |
|-------|------|---------|-----|----------|-------|
| **Aventure** | 4 | complete | visited | Image thématique | Révision ludique |
| **Révision** | illimité | free | none | Minimaliste | Entraînement libre |
| **Évaluation** | 1 | strict | visited | Sobre | Test noté |
| **Découverte** | illimité | free | all | Illustré | Introduction |

---

## Structure de parcours ambitieux (RECOMMANDÉ)

### Principe : PAS des exercices en batterie

Un bon Game Map raconte une histoire, pas une succession de quiz.

### Architecture type (12-15 étapes)

```
┌─────────────────────────────────────────────────────────────────────┐
│  🚢 ZONE DÉCOUVERTE (3-4 étapes)                                    │
│     dragtext → blanks → truefalse                                   │
│     Vocabulaire, définitions, premières notions                     │
│     Feedbacks très encourageants, indices généreux                  │
├─────────────────────────────────────────────────────────────────────┤
│  🏕️ [RESPIRATION] AdvancedText : Rappel illustré                    │
├─────────────────────────────────────────────────────────────────────┤
│  🌉 ZONE EXPLORATION (4-5 étapes)                                   │
│     multichoice → [★ bonus optionnel] → singlechoiceset → truefalse │
│     Premiers calculs, propriétés                                    │
│     Introduction d'un défi bonus sur le côté                        │
├─────────────────────────────────────────────────────────────────────┤
│  ⛺ [CHECKPOINT] AdvancedText : Encouragement                        │
├─────────────────────────────────────────────────────────────────────┤
│  🏔️ ZONE MAÎTRISE (3-4 étapes)                                      │
│     multichoice → questionset → BOSS FINAL                          │
│     Applications, synthèse                                          │
│     Challenge mais atteignable                                      │
├─────────────────────────────────────────────────────────────────────┤
│  🏆 VICTOIRE : Message narratif de félicitations                    │
└─────────────────────────────────────────────────────────────────────┘
```

### Règles anti-batterie

1. **JAMAIS 2 types identiques consécutifs**
2. **1 respiration toutes les 3-4 étapes de quiz**
3. **Noms d'étapes narratifs** (pas "Question 1, 2, 3")
4. **1-2 embranchements optionnels** (défis bonus)
5. **Progression de difficulté visible** (couleurs, noms)

### Exemple de nommage

| ✗ Éviter | ✓ Préférer |
|----------|------------|
| Question 1 | 🚢 Le Départ |
| Exercice 2 | 📜 Le Parchemin des Définitions |
| QCM 3 | 🌉 Le Pont des Calculs |
| Synthèse | 🏆 Le Trésor du Mathématicien |

### Défis bonus (★)

```json
{
  "label": "🗝️ La Grotte Secrète",
  "neighbors": ["4"],  // Accessible depuis étape 4 uniquement
  "specialStageExtraLives": 1  // Récompense : +1 vie
}
```

- Positionnés **sur le côté** de la carte (pas sur le chemin principal)
- Plus difficiles mais optionnels
- Récompensent par des vies supplémentaires

---

## Limites connues

1. **LaTeX dans DragText** : Les mots à glisser ne supportent pas le LaTeX, seulement le texte environnant
2. **Images par stage** : Possibles mais alourdissent le fichier
3. **Audio par stage** : Supporté mais rarement utile en maths
4. **Vies négatives** : Non supporté (minimum 0)
5. **Parcours non linéaire** : Les `neighbors` permettent des bifurcations, mais attention à la lisibilité

---

## Références

- **Exemple officiel** : `gamemap_example/content/content.json`
- **Générateur** : `scripts/generate_gamemap.py`
- **Documentation H5P** : https://h5p.org/documentation/developers/
