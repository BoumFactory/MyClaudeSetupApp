# Reference : H5P Course Presentation

Diaporama interactif avec quiz integres.

## Usage pedagogique

- **Cours interactif** : slides avec questions de verification
- **Capsule autonome** : mini-lecon complete
- **Revision active** : resume avec exercices integres
- **Presentation guidee** : navigation controlee

## Structure JSON

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
              "params": {"text": "<h1>Titre</h1>"}
            }
          }
        ],
        "keywords": [{"main": "mot-cle"}]
      }
    ],
    "keywordListEnabled": true
  },
  "l10n": {
    "slide": "Diapositive",
    "score": "Score",
    "prevSlide": "Precedent",
    "nextSlide": "Suivant"
  }
}
```

## Positionnement des elements

Toutes les coordonnees en **pourcentage** (0-100) :
- `x`, `y` : position du coin superieur gauche
- `width`, `height` : dimensions de l'element

Exemple de layout typique :
```
+----------------------------------+
|  Titre (x:5, y:5, w:90, h:15)   |
+----------------------------------+
|                                  |
|  Contenu (x:5, y:25, w:90, h:50)|
|                                  |
+----------------------------------+
|  Quiz (x:10, y:80, w:80, h:15)  |
+----------------------------------+
```

## Types d'elements supportes

### Texte (AdvancedText)
```json
{
  "action": {
    "library": "H5P.AdvancedText 1.1",
    "params": {
      "text": "<h2>Titre</h2><p>Texte avec \\(formule\\)</p>"
    }
  }
}
```

### Image
```json
{
  "action": {
    "library": "H5P.Image 1.1",
    "params": {
      "file": {"path": "images/figure.png", "mime": "image/png"},
      "alt": "Description"
    }
  }
}
```

### QCM (MultiChoice)
```json
{
  "action": {
    "library": "H5P.MultiChoice 1.16",
    "params": {
      "question": "<p>Question avec \\(formule\\) ?</p>",
      "answers": [
        {"text": "<p>\\(reponse1\\)</p>", "correct": true},
        {"text": "<p>\\(reponse2\\)</p>", "correct": false}
      ],
      "behaviour": {
        "enableRetry": true,
        "enableSolutionsButton": true
      }
    }
  }
}
```

### Vrai/Faux (TrueFalse)
```json
{
  "action": {
    "library": "H5P.TrueFalse 1.8",
    "params": {
      "question": "<p>Affirmation</p>",
      "correct": "true",
      "l10n": {"trueText": "Vrai", "falseText": "Faux"}
    }
  }
}
```

### Texte a trous (Blanks)
```json
{
  "action": {
    "library": "H5P.Blanks 1.14",
    "params": {
      "questions": ["<p>Completer avec *reponse*.</p>"],
      "behaviour": {"caseSensitive": false}
    }
  }
}
```

### Video
```json
{
  "action": {
    "library": "H5P.Video 1.6",
    "params": {
      "sources": [{"path": "https://youtube.com/watch?v=xxx", "mime": "video/YouTube"}]
    }
  }
}
```

## Dependances requises

```json
{
  "preloadedDependencies": [
    {"machineName": "H5P.CoursePresentation", "majorVersion": 1, "minorVersion": 25},
    {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
    {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
    {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
    {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
    {"machineName": "H5P.Image", "majorVersion": 1, "minorVersion": 1},
    {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6},
    {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
    {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3}
  ]
}
```

## Script Python

```python
from h5p_advanced_generator import H5PAdvancedGenerator

presentation = H5PAdvancedGenerator.create_course_presentation(
    title="Titre",
    slides=[
        {
            "elements": [
                {"type": "text", "content": "<h1>Slide 1</h1>", "x": 5, "y": 5, "width": 90, "height": 15},
                {"type": "quiz", "question": "Q?", "options": ["A", "B"], "correct": 0, "x": 10, "y": 50, "width": 80, "height": 30}
            ],
            "keywords": ["intro"]
        }
    ]
)
```

## Bonnes pratiques

1. **Structure** : 1 notion principale par slide
2. **Quiz** : question apres chaque notion importante
3. **Texte** : concis, utiliser les slides suivantes si besoin
4. **Navigation** : permettre retour arriere (sauf evaluation)
5. **Keywords** : activer pour revision rapide

## Sources

- [H5P Course Presentation](https://h5p.org/presentation)
- [Tutorial officiel](https://h5p.org/tutorial-course-presentation)
- [GitHub h5p-course-presentation](https://github.com/h5p/h5p-course-presentation)
