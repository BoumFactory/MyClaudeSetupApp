# Reference : H5P Interactive Book

Livre numerique avec chapitres et exercices integres.

## Usage pedagogique

- **Cours complet** : remplacement du PDF avec interactivite
- **Sequence structuree** : chapitres progressifs
- **Auto-formation** : progression autonome avec validation
- **Revision** : resume interactif avec exercices

## Structure JSON

```json
{
  "bookCover": {
    "coverDescription": "<p><strong>Titre</strong></p><p>Sous-titre</p>",
    "coverMedium": {}
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
    "progressIndicators": true,
    "progressAuto": true,
    "displaySummary": true
  },
  "l10n": {
    "previousPage": "Page precedente",
    "nextPage": "Page suivante",
    "summaryHeader": "Resume"
  }
}
```

## Types de contenu par chapitre

### Texte (AdvancedText)
```json
{
  "content": {
    "library": "H5P.AdvancedText 1.1",
    "params": {
      "text": "<h2>Definition</h2><p>Une suite \\((u_n)\\) est...</p>"
    },
    "metadata": {"contentType": "Text", "license": "U"}
  }
}
```

### Quiz (QuestionSet)
```json
{
  "content": {
    "library": "H5P.QuestionSet 1.20",
    "params": {
      "introPage": {"showIntroPage": false},
      "questions": [
        {
          "params": {"question": "...", "answers": [...]},
          "library": "H5P.MultiChoice 1.16"
        }
      ],
      "endGame": {
        "showResultPage": true,
        "showSolutionButton": true
      }
    }
  }
}
```

### Texte a trous (Blanks)
```json
{
  "content": {
    "library": "H5P.Blanks 1.14",
    "params": {
      "text": "<p>Completer : *reponse*</p>",
      "behaviour": {"caseSensitive": false}
    }
  }
}
```

### Mots a glisser (DragText)
```json
{
  "content": {
    "library": "H5P.DragText 1.10",
    "params": {
      "taskDescription": "<p>Placez les mots</p>",
      "textField": "Une suite *arithmetique* a une *raison* constante."
    }
  }
}
```

## Dependances requises

```json
{
  "preloadedDependencies": [
    {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
    {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
    {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
    {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16},
    {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8},
    {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14},
    {"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10},
    {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5},
    {"machineName": "H5P.JoubelUI", "majorVersion": 1, "minorVersion": 3}
  ]
}
```

## Script Python

```python
from h5p_advanced_generator import H5PAdvancedGenerator

book = H5PAdvancedGenerator.create_interactive_book(
    title="Suites numeriques",
    chapters=[
        {
            "title": "1. Definition",
            "contents": [
                {"type": "text", "content": "<h2>Qu'est-ce qu'une suite ?</h2>..."},
                {"type": "quiz", "questions": [{"type": "multichoice", ...}]}
            ]
        },
        {
            "title": "2. Suites arithmetiques",
            "contents": [
                {"type": "text", "content": "..."},
                {"type": "blanks", "text": "La raison est *constante*."},
                {"type": "dragwords", "text": "Une suite *arithmetique*..."}
            ]
        }
    ],
    cover_title="Chapitre 5",
    cover_subtitle="Mathematiques 1ere"
)
```

## Bonnes pratiques

1. **Structure** : 3-5 chapitres maximum par livre
2. **Longueur** : chapitres courts (lecture 5-10 min)
3. **Exercices** : 1-2 exercices par section de cours
4. **Progression** : du simple au complexe
5. **Resume** : activer le resume final

## Sources

- [H5P Interactive Book](https://h5p.org/content-types-and-applications)
- [Documentation H5P](https://h5p.org/documentation)
