# Image Generator Skill - Documentation

## Vue d'ensemble

Le skill **image-generator** permet de générer des images de haute qualité avec l'API Google Imagen. Il est conçu pour créer des images éducatives, des personnages, des illustrations et des photos réalistes.

## Installation

### 1. Dépendances Python

```bash
pip install google-genai python-dotenv pillow
```

### 2. Configuration de l'API Key

Créer ou modifier le fichier `.env` à la racine du projet:

```env
NANOBANANA_API_KEY=votre_clé_api_google
```

## Structure du skill

```
image-generator/
├── SKILL.md                          # Documentation principale du skill
├── README.md                         # Ce fichier
├── scripts/
│   └── generate_images.py            # Script principal de génération
└── references/
    └── imagen_api_guide.md           # Guide détaillé de l'API
```

## Utilisation rapide

### Commande de base

```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Description en anglais de l'image" \
  -o "chemin/vers/dossier/sortie" \
  -m standard \
  -n 4
```

### Exemples concrets

#### 1. Schéma pour exercice de maths
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Simple geometric diagram showing a right triangle with labeled sides, educational style, clean lines, white background" \
  -o "exercices-geometrie/images" \
  -m fast \
  -n 2 \
  -a square
```

#### 2. Personnage pour escape game
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Friendly detective character in cartoon style, magnifying glass, colorful illustration for children" \
  -o "4. Images/escape-game/detective" \
  -m standard \
  -n 4 \
  -a portrait
```

#### 3. Photo pour présentation
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Professional photo of modern classroom with students using tablets, natural lighting, 4K quality" \
  -o "presentation/images" \
  -m ultra \
  -n 4 \
  -a widescreen \
  -s 2K
```

## Paramètres disponibles

| Paramètre | Valeurs | Description |
|-----------|---------|-------------|
| `prompt` | Texte | Description en anglais (requis) |
| `-o, --output-dir` | Chemin | Dossier de sortie (requis) |
| `-m, --model` | fast, standard, ultra, imagen3 | Modèle à utiliser (défaut: standard) |
| `-n, --num-images` | 1-4 | Nombre d'images (défaut: 4) |
| `-a, --aspect-ratio` | square, fullscreen, fullscreen_portrait, widescreen, portrait | Format (défaut: square) |
| `-s, --image-size` | 1K, 2K | Taille (défaut: 1K, standard/ultra seulement) |
| `-p, --person-generation` | dont_allow, allow_adult, allow_all | Génération de personnes (défaut: allow_adult) |
| `-f, --filename` | Texte | Nom de base des fichiers (défaut: generated_image) |

## Choix du modèle

- **fast**: Rapide et économique, parfait pour tests et itérations
- **standard**: Équilibre qualité/coût, recommandé pour la plupart des usages
- **ultra**: Meilleure qualité, pour publications finales importantes
- **imagen3**: Version précédente, pour compatibilité

## Organisation des images

### Images locales (spécifiques à un projet)
Placer dans le sous-dossier `images/` du projet LaTeX:
```
projet-latex/
└── images/
    ├── schema1.png
    └── photo1.png
```

### Images globales (réutilisables)
Placer dans `4. Images/` avec organisation par catégorie:
```
4. Images/
├── escape-game/
│   ├── detective-scientifique/
│   └── chateau-mystere/
├── personnages/
│   └── professeur-einstein/
├── assets/
│   └── icones-matieres/
└── educatif/
    ├── astronomie/
    └── geometrie/
```

## Conseils pour les prompts

### Structure recommandée
```
[Objet] + [Contexte] + [Style] + [Modificateurs de qualité]
```

### Exemples de templates

**Schéma éducatif**:
```
"[Description], educational diagram style, clean lines, labeled, white background, high quality"
```

**Personnage**:
```
"[Description], cartoon style, colorful illustration, friendly, suitable for children, professional quality"
```

**Photo réaliste**:
```
"Professional photograph of [sujet], [éclairage], 4K quality, [ambiance]"
```

### Modificateurs utiles

- **Qualité**: professional, high quality, 4K, HDR, detailed
- **Éclairage**: natural lighting, golden hour, dramatic lighting
- **Style**: cartoon, watercolor, digital art, minimalist, photorealistic
- **Contexte éducatif**: educational, suitable for children, textbook style

## Agent image-user

Un agent autonome est disponible pour utiliser ce skill automatiquement.

### Utilisation de l'agent

```markdown
Lancer l'agent image-user en lui demandant de générer des images.
L'agent va:
1. Charger le skill image-generator
2. Analyser les besoins
3. Traduire en anglais
4. Choisir les paramètres optimaux
5. Générer les images
6. Rapporter les résultats
```

### Exemple de demande à l'agent

```
"J'ai besoin d'un personnage de robot détective pour mon escape game sur les enquêtes scientifiques.
Il doit être amical et coloré, adapté pour des collégiens."
```

L'agent va automatiquement:
- Traduire en anglais
- Choisir le modèle standard
- Sélectionner le format portrait
- Créer le dossier `4. Images/escape-game/robot-detective/`
- Générer 4 variantes
- Rapporter les résultats

## Résolution de problèmes

### Erreur: API Key manquante
Vérifier que `NANOBANANA_API_KEY` est définie dans `.env`

### Erreur: Module non trouvé
Installer les dépendances:
```bash
pip install google-genai python-dotenv pillow
```

### Résultats non satisfaisants
- Affiner le prompt avec plus de détails
- Ajouter des modificateurs de qualité
- Essayer un modèle différent
- Générer plusieurs fois pour avoir plus d'options

### Prompt trop long
Maximum 480 jetons. Réduire la description ou simplifier.

## Ressources

- **SKILL.md**: Documentation complète du skill
- **referencias/imagen_api_guide.md**: Guide détaillé de l'API avec exemples
- **Agent image-user**: `.claude/agents/image-user.md`

## Support

Pour plus d'informations, consulter:
1. La documentation dans `SKILL.md`
2. Le guide de l'API dans `references/imagen_api_guide.md`
3. Les exemples dans l'agent `image-user.md`
