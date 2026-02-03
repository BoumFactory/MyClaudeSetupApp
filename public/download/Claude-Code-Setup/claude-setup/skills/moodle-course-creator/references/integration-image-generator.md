# Integration : Skill image-generator pour H5P

Ce document explique comment utiliser le skill **image-generator** pour creer des images de fond pour les contenus H5P (Image Hotspots, Course Presentation, etc.)

## Localisation du skill

```
.claude/skills/creer/media/image-generator/
├── SKILL.md                    # Documentation complete
├── scripts/
│   └── generate_image.py       # Script de generation
├── assets/
│   └── mascots/                # Mascottes disponibles
├── knowledge/
│   └── mascots.json            # Descriptions des mascottes
└── examples/
    └── *.json                  # Exemples de prompts
```

## Usage basique

```bash
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \
  --prompt "DESCRIPTION DETAILLEE" \
  --type "infographic" \
  --context "Niveau: 1ere. Chapitre: Suites." \
  --style "Clean educational, white background" \
  --output "chemin/vers/image.png"
```

## Types d'images disponibles

| Type | Usage pour H5P |
|------|----------------|
| `infographic` | Image Hotspots - carte conceptuelle |
| `schema` | Image Hotspots - schema annote |
| `photo` | Course Presentation - illustration realiste |
| `illustration` | Tout H5P - image educative |
| `geometry` | Image Hotspots - figure geometrique |
| `graph` | Course Presentation - courbe/graphique |

## Workflow complet : Image Hotspots

### Etape 1 : Concevoir l'image

Avant de generer, planifier :
- Quels points d'interet ?
- Ou seront-ils places (coordonnees %) ?
- Quel contenu pour chaque point ?

### Etape 2 : Generer l'image

```bash
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \
  --prompt "Educational infographic about numerical sequences (suites numeriques).
Central concept: a machine/function that transforms numbers.
Layout: 3 zones arranged horizontally.
Zone 1 (left, 30%): Arithmetic sequences - show u(n) = u(0) + n*r with visual of constant steps
Zone 2 (center, 40%): General definition - function from N to R, notation u_n
Zone 3 (right, 30%): Geometric sequences - show u(n) = u(0) * q^n with visual of multiplication
Background: light blue gradient
Style: modern educational, clean vectors, sans-serif labels
No complex mathematical notation - keep labels simple" \
  --type "infographic" \
  --context "Level: 1ere (Grade 11). Chapter: Numerical sequences. For Moodle H5P." \
  --output "capsule_suites/images/suites_overview.png"
```

### Etape 3 : Creer le H5P

```python
from h5p_image_hotspots import H5PImageHotspotsGenerator

h5p = H5PImageHotspotsGenerator.create_image_hotspots(
    title="Exploration des suites",
    image_path="capsule_suites/images/suites_overview.png",
    hotspots=[
        {"x": 15, "y": 50, "header": "Suites arithmetiques", "content": [...]},
        {"x": 50, "y": 30, "header": "Definition generale", "content": [...]},
        {"x": 85, "y": 50, "header": "Suites geometriques", "content": [...]}
    ],
    icon="question",
    color="blue"
)
```

## Prompts recommandes par type H5P

### Pour Image Hotspots - Exploration

```
Educational map/diagram of [CONCEPT].
Multiple distinct zones for different aspects.
Clear separation between zones.
Light background for visibility of hotspot icons.
Zones should be spaced for hotspot placement.
Style: infographic, modern, educational.
```

### Pour Image Hotspots - Schema annote

```
Technical diagram of [CONCEPT].
Central element with surrounding components.
Clear areas for label placement.
White background.
Style: scientific illustration, clean lines.
```

### Pour Course Presentation - Slide de titre

```
Title slide visual for [TOPIC].
Central title area.
Decorative mathematical elements around edges.
Style: modern presentation, professional.
```

## Mascottes disponibles

Pour ajouter une mascotte a l'image :

| Mascotte | Domaine | Fichier |
|----------|---------|---------|
| Gaia | Geometrie | `gaia_geometrie.png` |
| Alex | Analyse | `alex_analyse.png` |
| Priya | Probabilites | `priya_probabilites.png` |
| Nabil | Arithmetique | `nabil_arithmetique.png` |
| Sofia | Algebre | `sofia_algebre.png` |
| Sven | Suites | `sven_suites.png` |

Chemin : `.claude/skills/creer/media/image-generator/assets/mascots/`

## Checklist avant generation

```
□ Prompt suffisamment detaille (>200 caracteres)
□ Type d'image specifie
□ Contexte educatif indique
□ Zones claires pour placement des hotspots
□ Fond adapte (clair pour visibilite des icones)
□ Pas de texte complexe avec accents
□ Resolution adaptee (1920x1080 recommande)
```

## Exemple complet JSON

Pour un prompt complexe, utiliser un fichier JSON :

```json
{
  "prompt": "Educational infographic showing the relationship between arithmetic and geometric sequences...",
  "type": "infographic",
  "context": "Level: 1ere. Chapter: Suites numeriques. For H5P Image Hotspots.",
  "style": "Clean modern educational style. White/light background. Clear zones. No complex math notation."
}
```

```bash
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \
  --prompt-file "prompt_suites.json" \
  --output "images/suites_infographic.png"
```

## Dependances

```bash
# Dans le venv du projet
pip install requests python-dotenv
```

Variable d'environnement requise : `NANOBANANA_API_KEY`
