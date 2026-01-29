# Moodle

> Contenus Moodle : cours interactifs, H5P, parcours pedagogiques

## Skills disponibles

### moodle-course-creator
- **Commande** : `/moodleise`
- **Usage** : Creer des cours Moodle complets (.mbz)
- **Capacites** :
  - Quiz H5P (QCM, Vrai/Faux, textes a trous, drag&drop)
  - Interactive Book (livres numeriques)
  - Course Presentation (diaporamas)
  - **Image Hotspots** (mini-jeux, explorations)
  - **Game Map** (parcours gamifies via delegation agent)
- [Documentation](./moodle-course-creator/skill.md)

### h5p-gamemap ★ NOUVEAU
- **Commande** : `/createGameMap`
- **Usage** : Creer des parcours gamifies H5P Game Map
- **Capacites** :
  - Analyse de ressources (LaTeX, PDF, HTML, Markdown)
  - Arbre de decision intelligent pour extraction de contenu
  - Types varies (QCM, Vrai/Faux, DragText, Blanks, etc.)
  - Validation visuelle des positions (hotspot_preview.py)
  - Image de fond thematique (integration image-generator)
- **Integration** : Utilise par `/moodleise` en modes Enrichi/Complet
- [Documentation](./h5p-gamemap/SKILL.md)
- [Reference technique](./h5p-gamemap/references/ETAT_DES_LIEUX.md)

### moodle-cloze
- **Usage** : Syntaxe CLOZE pour questions Moodle
- [Documentation](./moodle-cloze/SKILL.md)

## Nouveautes

### Parcours interactifs (Image Hotspots)
Creer des mini-jeux mathematiques sur des images :
- Points cliquables revelant des defis
- Ideal pour le college
- Support LaTeX complet

### Correction LaTeX
Le LaTeX s'affiche maintenant correctement dans :
- Les questions
- Les options/reponses
- Les feedbacks

## Scripts

### moodle-course-creator

| Script | Description |
|--------|-------------|
| `h5p_generator.py` | H5P basique |
| `h5p_generator_v2.py` | H5P avec metadonnees |
| `h5p_advanced_generator.py` | Tous types H5P |
| `h5p_image_hotspots.py` | Image Hotspots |
| `generate_course_mbz.py` | Package Moodle |

### h5p-gamemap

| Script | Description |
|--------|-------------|
| `generate_gamemap.py` | Generation complete Game Map depuis preplan |
| `parse_preplan.py` | Parse le Markdown en structure JSON |
| `hotspot_preview.py` | Previsualisation et repositionnement des hotspots |

## References

- [Types H5P](./moodle-course-creator/references/h5p-types-reference.md)
- [Guide LaTeX H5P](./moodle-course-creator/references/latex-h5p-guide.md)
- [Game Map - Etat des lieux](./h5p-gamemap/references/ETAT_DES_LIEUX.md)
- [Exemple preplan](./h5p-gamemap/examples/preplan_gamemap.md)

## Integration inter-skills

### /moodleise → /createGameMap

En modes **Enrichi** ou **Parcours complet**, `/moodleise` delegue automatiquement a un agent `meta-high` qui utilise `/createGameMap` :

```
/moodleise "sequence/"
     │
     ├─► Mode Enrichi/Complet detecte
     │
     └─► Lance agent meta-high :
           "Utilise /createGameMap pour creer un parcours gamifie
            base sur le contenu de sequence/Cours/enonce.tex"
                 │
                 └─► Retourne le fichier .h5p genere
                       │
                       └─► Integre dans la section "Parcours de revision"
```
