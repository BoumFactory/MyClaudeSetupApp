# Fichiers de configuration

Ce dossier contient des configurations pr\u00e9-d\u00e9finies pour diff\u00e9rents types de g\u00e9n\u00e9ration d'images.

## Utilisation

Pour utiliser une configuration :

```bash
python .claude/skills/image-generator/scripts/generate_prompt.py \
  --config .claude/skills/image-generator/config/escape_game_medieval.json \
  --output "prompts/mon_projet.json" \
  --num_images 5 \
  --contexts "porte,coffre,carte,enigme,recompense"
```

La configuration remplacera les param\u00e8tres par d\u00e9faut pour le style, le th\u00e8me, et les modificateurs personnalis\u00e9s.

## Configurations disponibles

### escape_game_medieval.json
- **Usage :** Escape games th\u00e8me m\u00e9di\u00e9val
- **Style :** minimal_color_print
- **Co\u00fbt :** Tr\u00e8s bas
- **Id\u00e9al pour :** Fiches d'exercices th\u00e9matis\u00e9es quotidiennes

### mathematics_diagrams.json
- **Usage :** Sch\u00e9mas et diagrammes math\u00e9matiques
- **Style :** educational_illustration
- **Co\u00fbt :** Tr\u00e8s bas
- **Id\u00e9al pour :** Cours et fiches de synth\u00e8se

### classroom_activities.json
- **Usage :** Activit\u00e9s sp\u00e9ciales en classe
- **Style :** moderate_color_classroom
- **Co\u00fbt :** Moyen
- **Id\u00e9al pour :** Projets, affichage en classe

### science_illustrations.json
- **Usage :** Illustrations scientifiques
- **Style :** flat_design
- **Co\u00fbt :** Bas
- **Id\u00e9al pour :** Cours de sciences, ressources num\u00e9riques

## Cr\u00e9er sa propre configuration

Pour cr\u00e9er une configuration personnalis\u00e9e, dupliquez l'un des fichiers existants et modifiez les param\u00e8tres :

```json
{
  "name": "Mon Config",
  "description": "Description de l'usage",
  "style": "minimal_color_print",
  "theme": "mathematics",
  "custom_modifiers": "vos modificateurs",
  "num_variations": 2,
  "output_format": "png",
  "resolution": {
    "width": 1024,
    "height": 1024
  },
  "print_settings": {
    "target": "economical_printing",
    "max_colors": 3,
    "background": "white",
    "style_keywords": ["keyword1", "keyword2"]
  },
  "suggested_contexts": [
    "Contexte 1",
    "Contexte 2"
  ],
  "notes": "Notes personnelles"
}
```

## Param\u00e8tres

### style
Voir `knowledge/styles.md` pour la liste compl\u00e8te des styles disponibles.

### theme
- escape_game_medieval
- escape_game_scifi
- escape_game_detective
- mathematics
- science_physics
- science_biology
- history
- geography
- literature
- adventure
- neutral_educational

### print_settings.target
- economical_printing : Co\u00fbt minimal
- educational_clarity : Focus clart\u00e9
- balanced_color_cost : \u00c9quilibre
- modern_educational : Style moderne

## Conseils

1. **Pour usage quotidien :** Choisir `minimal_color_print` avec max_colors ≤ 3
2. **Pour activit\u00e9s sp\u00e9ciales :** Utiliser `moderate_color_classroom` avec max_colors ≤ 6
3. **Pour num\u00e9rique :** `flat_design` ou `educational_illustration`
4. **Toujours :** Sp\u00e9cifier `"background": "white"` pour \u00e9conomiser l'encre
