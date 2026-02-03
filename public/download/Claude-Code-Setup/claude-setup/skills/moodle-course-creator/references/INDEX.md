# Index des References H5P

Documentation technique pour la creation de contenus H5P Moodle.

## Types H5P

| Reference | Description | Usage principal |
|-----------|-------------|-----------------|
| [h5p-image-hotspots.md](./h5p-image-hotspots.md) | Points interactifs sur image | Mini-jeux, explorations |
| [h5p-course-presentation.md](./h5p-course-presentation.md) | Diaporama interactif | Cours avec quiz integres |
| [h5p-interactive-book.md](./h5p-interactive-book.md) | Livre numerique | Cours complets |
| [h5p-types-reference.md](./h5p-types-reference.md) | Vue d'ensemble tous types | Reference generale |

## Guides techniques

| Reference | Description |
|-----------|-------------|
| [latex-h5p-guide.md](./latex-h5p-guide.md) | Gestion LaTeX/MathJax dans H5P |
| [integration-image-generator.md](./integration-image-generator.md) | Creer des images pour H5P |

## Workflow recommande

### Capsule interactive (mini-jeu)

```
1. Concevoir le contenu pedagogique
2. [Optionnel] Generer image de fond avec image-generator
3. Creer Image Hotspots avec h5p_image_hotspots.py
4. Tester dans Moodle
```

### Quiz de revision

```
1. Extraire les notions cles du cours
2. Rediger questions variees (QCM, V/F, trous)
3. Creer Question Set avec h5p_generator_v2.py
4. Tester le rendu LaTeX
```

### Cours interactif complet

```
1. Structurer en chapitres/slides
2. Alterner contenu et quiz
3. Creer Interactive Book ou Course Presentation
4. Integrer dans Moodle
```

## Scripts disponibles

| Script | Usage |
|--------|-------|
| `h5p_generator.py` | H5P basique |
| `h5p_generator_v2.py` | H5P avec metadonnees |
| `h5p_advanced_generator.py` | Tous types avances |
| `h5p_image_hotspots.py` | Image Hotspots |
| `generate_course_mbz.py` | Package Moodle complet |

## Skill image-generator

Pour creer des images de fond :

```bash
python ".claude/skills/creer/media/image-generator/scripts/generate_image.py" \
  --prompt "Description detaillee..." \
  --type "infographic" \
  --output "chemin/image.png"
```

Chemin : `.claude/skills/creer/media/image-generator/`

Types disponibles : `infographic`, `schema`, `photo`, `illustration`, `geometry`, `graph`
