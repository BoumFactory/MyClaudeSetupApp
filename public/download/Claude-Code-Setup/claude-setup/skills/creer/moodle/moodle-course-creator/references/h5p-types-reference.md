# Reference des Types H5P pour Parcours Interactifs

Ce document reference tous les types H5P disponibles pour creer des parcours pedagogiques interactifs.

## Types pour Parcours Interactifs (Jeux/Exploration)

### Image Hotspots

**Usage** : Image avec points cliquables revelant du contenu

**Structure JSON** :
```json
{
  "image": {
    "path": "images/background.png",
    "mime": "image/png",
    "width": 1920,
    "height": 1080
  },
  "iconType": "icon",
  "icon": "plus",
  "color": "#981d99",
  "hotspots": [
    {
      "position": {"x": 25.5, "y": 30.2},
      "alwaysFullscreen": false,
      "header": "Point 1",
      "content": [
        {
          "library": "H5P.Text 1.1",
          "params": {
            "text": "<p>Contenu avec \\(formule LaTeX\\)</p>"
          }
        }
      ]
    }
  ]
}
```

**Icones disponibles** : plus, minus, times, check, question, info, exclamation

**Types de contenu popup** :
- `H5P.Text 1.1` - Texte HTML avec MathJax
- `H5P.Video 1.6` - Video YouTube/locale
- `H5P.Image 1.1` - Image avec zoom
- `H5P.Audio 1.5` - Audio

**Dependances** :
```json
[
  {"machineName": "H5P.ImageHotspots", "majorVersion": 1, "minorVersion": 10},
  {"machineName": "H5P.Text", "majorVersion": 1, "minorVersion": 1},
  {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6},
  {"machineName": "H5P.Image", "majorVersion": 1, "minorVersion": 1}
]
```

---

### Course Presentation

**Usage** : Diaporama interactif avec quiz integres

**Structure JSON** :
```json
{
  "presentation": {
    "slides": [
      {
        "elements": [
          {
            "x": 5,
            "y": 10,
            "width": 90,
            "height": 20,
            "action": {
              "library": "H5P.AdvancedText 1.1",
              "params": {
                "text": "<h2>Titre</h2><p>Contenu avec \\(x^2\\)</p>"
              }
            }
          },
          {
            "x": 10,
            "y": 50,
            "width": 80,
            "height": 30,
            "action": {
              "library": "H5P.MultiChoice 1.16",
              "params": {
                "question": "<p>Question ?</p>",
                "answers": [
                  {"text": "<p>Option A</p>", "correct": true},
                  {"text": "<p>Option B</p>", "correct": false}
                ]
              }
            }
          }
        ],
        "keywords": [{"main": "mot-cle"}]
      }
    ]
  }
}
```

**Types d'elements** :
- Texte : AdvancedText, ContinuousText, ExportableTextArea
- Media : Image, Video, Audio
- Quiz : MultiChoice, TrueFalse, DragQuestion, DragText, Blanks
- Avance : InteractiveVideo, Summary, Dialogcards

**Positionnement** : x, y en pourcentage (0-100), width/height en pourcentage

---

### Interactive Book

**Usage** : Livre numerique avec chapitres et exercices

**Structure JSON** :
```json
{
  "bookCover": {
    "coverDescription": "<p><strong>Titre</strong></p><p>Sous-titre</p>"
  },
  "chapters": [
    {
      "title": "Chapitre 1",
      "content": [
        {
          "content": {
            "library": "H5P.AdvancedText 1.1",
            "params": {"text": "<h2>Section</h2><p>Contenu...</p>"}
          }
        },
        {
          "content": {
            "library": "H5P.QuestionSet 1.20",
            "params": {...}
          }
        }
      ]
    }
  ],
  "behaviour": {
    "defaultTableOfContents": true,
    "progressIndicators": true
  }
}
```

---

### Branching Scenario

**Usage** : Scenario a embranchements (type escape game, simulation)

**Structure conceptuelle** :
```
Start -> Choix A -> Resultat A1
              -> Resultat A2
      -> Choix B -> Resultat B1
              -> Sous-choix -> ...
```

**Elements de branchement** :
- Chaque noeud peut contenir du contenu H5P
- Les choix menent a differentes branches
- Feedback adaptatif selon le parcours

---

## Types de Questions

### MultiChoice
```json
{
  "type": "multichoice",
  "text": "Question avec \\(formule\\) ?",
  "options": ["\\(x=1\\)", "\\(x=2\\)", "\\(x=3\\)"],
  "correct_index": 0,
  "feedback": "Explication avec \\(calcul\\)"
}
```

### TrueFalse
```json
{
  "type": "truefalse",
  "text": "Affirmation a juger",
  "correct": true,
  "feedback_correct": "Bravo !",
  "feedback_incorrect": "Explication..."
}
```

### Fill in the Blanks
```json
{
  "type": "blanks",
  "text": "Le resultat de \\(2+2\\) est *4*."
}
```
Syntaxe : `*reponse*` ou `*rep1/rep2*` pour alternatives

### Drag the Words
```json
{
  "type": "dragwords",
  "text": "Une *fonction* est une relation qui associe..."
}
```
Syntaxe : `*mot*` pour les mots a deplacer

### Mark the Words
```json
{
  "type": "markwords",
  "text": "Selectionnez les nombres *pairs* : 1, *2*, 3, *4*, 5"
}
```

---

## Support LaTeX/MathJax

### Syntaxe
- **Inline** : `\(formule\)` ou `$formule$`
- **Block** : `\[formule\]` ou `$$formule$$`

### Echappement JSON
Dans le JSON, doubler les backslashes :
```json
"text": "La formule \\(x^2 + y^2 = z^2\\) est..."
```

### IMPORTANT : Gestion dans le code Python
```python
# CORRECT : Proteger le LaTeX AVANT d'echapper le HTML
def process_text(text):
    # 1. Proteger les formules
    protected = protect_latex(text)
    # 2. Echapper le HTML
    escaped = html.escape(protected)
    # 3. Restaurer les formules
    return restore_latex(escaped)

# INCORRECT : Echapper puis convertir
def bad_process(text):
    escaped = html.escape(text)  # Casse les \
    return wrap_math(escaped)     # Trop tard !
```

---

## Idees de Parcours Interactifs

### Mini-jeu Exploration Mathematique
1. Image de fond (carte, scene, schema)
2. Hotspots revelant des defis mathematiques
3. Chaque defi = sous-contenu H5P (quiz, texte a trous)
4. Progression visible (points, badges)

### Parcours Decouverte
1. Course Presentation avec slides
2. Chaque slide = notion + exercice
3. Resume interactif en fin

### Livre de Cours Interactif
1. Interactive Book structure par chapitres
2. Texte cours + exercices apres chaque notion
3. Quiz de validation par chapitre

---

## Sources

- [H5P Content Types](https://h5p.org/content-types-and-applications)
- [Image Hotspots](https://h5p.org/image-hotspots)
- [Course Presentation](https://h5p.org/presentation)
- [H5P File Structure](https://h5p.org/specification)
- [GitHub h5p-image-hotspots](https://github.com/h5p/h5p-image-hotspots)
