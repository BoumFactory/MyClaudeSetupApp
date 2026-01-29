# Reference : H5P Image Hotspots

Points interactifs cliquables sur une image de fond.

## Usage pedagogique

- **Mini-jeux mathematiques** : defis places sur un schema
- **Exploration de concepts** : points d'information sur une carte mentale
- **Schemas annotes interactifs** : labels cliquables sur un diagramme
- **Parcours decouverte** : progression guidee sur une image

## Structure JSON

```json
{
  "image": {
    "path": "images/background.png",
    "mime": "image/png",
    "width": 1920,
    "height": 1080,
    "copyright": {"license": "U"}
  },
  "backgroundImageAltText": "Description de l'image",
  "iconType": "icon",
  "icon": "plus",
  "color": "#1e73be",
  "hotspots": [
    {
      "position": {"x": 25.5, "y": 30.2},
      "alwaysFullscreen": false,
      "header": "Titre du point",
      "content": [
        {
          "library": "H5P.Text 1.1",
          "params": {"text": "<p>Contenu avec \\(LaTeX\\)</p>"},
          "subContentId": "unique-id",
          "metadata": {"contentType": "Text", "license": "U"}
        }
      ]
    }
  ],
  "l10n": {
    "hotspotNumberLabel": "Point #num",
    "closeButtonLabel": "Fermer"
  }
}
```

## Position des hotspots

Coordonnees en **pourcentage** (0-100) depuis le coin superieur gauche :
- `x: 0` = bord gauche
- `x: 100` = bord droit
- `y: 0` = bord superieur
- `y: 100` = bord inferieur

## Icones disponibles

| Icone | Code | Usage suggere |
|-------|------|---------------|
| + | `plus` | Ajout d'info, point neutre |
| - | `minus` | Exclusion, soustraction |
| x | `times` | Erreur, attention |
| v | `check` | Validation, reponse correcte |
| ? | `question` | Defi, question |
| i | `info` | Information, definition |
| ! | `exclamation` | Important, alerte |

## Couleurs predefinies

```python
COLORS = {
    'blue': '#1e73be',
    'green': '#2ecc71',
    'red': '#e74c3c',
    'orange': '#f39c12',
    'purple': '#9b59b6',
    'teal': '#1abc9c',
    'pink': '#e91e63'
}
```

## Types de contenu popup

### Texte (H5P.Text 1.1)
```json
{
  "library": "H5P.Text 1.1",
  "params": {
    "text": "<h3>Titre</h3><p>Contenu avec \\(formule\\)</p>"
  }
}
```

### Image (H5P.Image 1.1)
```json
{
  "library": "H5P.Image 1.1",
  "params": {
    "contentName": "Image",
    "file": {
      "path": "images/detail.png",
      "mime": "image/png"
    },
    "alt": "Description"
  }
}
```

### Video YouTube (H5P.Video 1.6)
```json
{
  "library": "H5P.Video 1.6",
  "params": {
    "sources": [{"path": "https://youtube.com/watch?v=xxx", "mime": "video/YouTube"}],
    "visuals": {"fit": true, "controls": true}
  }
}
```

### Audio (H5P.Audio 1.5)
```json
{
  "library": "H5P.Audio 1.5",
  "params": {
    "files": [{"path": "audio/explication.mp3"}],
    "playerMode": "full"
  }
}
```

## Dependances requises

```json
{
  "preloadedDependencies": [
    {"machineName": "H5P.ImageHotspots", "majorVersion": 1, "minorVersion": 10},
    {"machineName": "H5P.Text", "majorVersion": 1, "minorVersion": 1},
    {"machineName": "H5P.Image", "majorVersion": 1, "minorVersion": 1},
    {"machineName": "H5P.Video", "majorVersion": 1, "minorVersion": 6},
    {"machineName": "H5P.Audio", "majorVersion": 1, "minorVersion": 5},
    {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
  ]
}
```

## Script Python

```python
from h5p_image_hotspots import H5PImageHotspotsGenerator

# Exploration mathematique
h5p = H5PImageHotspotsGenerator.create_math_exploration(
    title="Exploration",
    image_path="/chemin/image.png",
    challenges=[
        {"x": 25, "y": 30, "title": "Defi 1", "question": "...", "answer": "..."}
    ]
)

# Schema annote
h5p = H5PImageHotspotsGenerator.create_labeled_diagram(
    title="Schema",
    image_path="/chemin/schema.png",
    labels=[
        {"x": 50, "y": 20, "term": "Terme", "definition": "Definition"}
    ]
)
```

## Integration avec image-generator

Pour creer l'image de fond avant de generer le H5P :

```bash
# 1. Generer l'image avec le skill image-generator
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \
  --prompt "Schema conceptuel des suites numeriques..." \
  --type "infographic" \
  --output "images/suites_exploration.png"

# 2. Utiliser l'image dans le H5P
# Voir h5p_image_hotspots.py
```

## Bonnes pratiques

1. **Image de fond** : resolution 1920x1080 ou 1280x720 recommandee
2. **Espacement** : minimum 10% entre les hotspots pour eviter chevauchement
3. **Contenu** : court et precis (popup, pas page complete)
4. **Icones** : coherentes (meme couleur/type pour meme fonction)
5. **LaTeX** : fonctionne dans le texte avec `\\(formule\\)`

## Sources

- [H5P Image Hotspots](https://h5p.org/image-hotspots)
- [Tutorial officiel](https://h5p.org/tutorial-image-hotspots)
- [GitHub h5p-image-hotspots](https://github.com/h5p/h5p-image-hotspots)
