---
name: image-generator
description: Skill pour générer des images avec l'API Google Imagen. Utiliser ce skill pour créer des images à partir de descriptions textuelles, avec choix de modèles (rapide/standard/ultra), formats, et emplacements de sauvegarde (projet local ou dossier global). Support de la génération photoréaliste, artistique, éducative avec contrôle des paramètres.
---

# Image Generator Skill

Skill spécialisé pour générer des images de haute qualité avec l'API Google Imagen. Permet de créer des images photoréalistes, artistiques, éducatives ou techniques à partir de descriptions textuelles.

## Quand utiliser ce skill

Utiliser ce skill lorsque:
- Création d'images pour des documents éducatifs (fiches, exercices)
- Génération de personnages ou d'assets pour des applications/escape games
- Création d'illustrations pour des présentations ou du matériel pédagogique
- Besoin d'images spécifiques qui ne sont pas disponibles dans les ressources existantes
- Prototypage rapide de concepts visuels

## Script principal

Le script `scripts/generate_images.py` est l'outil principal pour générer des images.

### Installation des dépendances

Avant la première utilisation, installer les dépendances Python nécessaires:

```bash
pip install google-genai python-dotenv pillow
```

### Utilisation de base

```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Description de l'image en anglais" \
  -o "chemin/vers/dossier/sortie" \
  -m standard \
  -n 4
```

### Paramètres disponibles

- `prompt` (requis): Description textuelle en anglais pour générer l'image
- `-o, --output-dir` (requis): Répertoire de sortie pour les images
- `-m, --model`: Modèle à utiliser
  - `fast`: Rapide et économique (défaut pour itérations rapides)
  - `standard`: Équilibre qualité/coût (défaut recommandé)
  - `ultra`: Meilleure qualité, plus coûteux
  - `imagen3`: Version précédente de l'API
- `-n, --num-images`: Nombre d'images (1-4, défaut: 4)
- `-a, --aspect-ratio`: Format d'image
  - `square`: 1:1 (défaut)
  - `fullscreen`: 4:3
  - `fullscreen_portrait`: 3:4
  - `widescreen`: 16:9
  - `portrait`: 9:16
- `-s, --image-size`: Taille (1K ou 2K, défaut: 1K)
- `-p, --person-generation`: Autorisation de personnes
  - `dont_allow`: Bloquer
  - `allow_adult`: Adultes uniquement (défaut)
  - `allow_all`: Adultes et enfants
- `-f, --filename`: Nom de base des fichiers (défaut: generated_image)

## Stratégie de sauvegarde des images

Choisir l'emplacement de sauvegarde selon le contexte:

### Images locales au projet LaTeX

Pour des images spécifiques à un document (fiche d'exercices, cours):
- Sauvegarder dans le sous-répertoire `images/` du projet LaTeX
- Exemple: `projet-latex/images/`

```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Geometric shapes for math exercises" \
  -o "chemin/vers/projet/images" \
  -m fast \
  -n 2
```

### Images globales réutilisables

Pour des assets partagés (personnages, éléments d'escape game):
- Utiliser le dossier global `4. Images/` à la racine
- Structure recommandée:
  - `4. Images/escape-game/`: Images pour escape games
  - `4. Images/personnages/`: Personnages récurrents
  - `4. Images/assets/`: Éléments génériques réutilisables
  - `4. Images/educatif/`: Illustrations éducatives générales

Pour chaque nouveau lot d'images, créer un sous-répertoire dédié avec un nom descriptif:

```bash
# Exemple: Personnages pour un escape game
python .claude/skills/image-generator/scripts/generate_images.py \
  "Friendly robot character, cartoon style, colorful" \
  -o "4. Images/escape-game/robot-detective" \
  -m standard \
  -n 4
```

## Workflow de génération

1. **Analyser le besoin**:
   - Type d'image nécessaire (photo, illustration, schéma)
   - Contexte d'utilisation (fiche, app, présentation)
   - Qualité requise vs budget

2. **Choisir le modèle**:
   - `fast`: Pour tests rapides ou images simples
   - `standard`: Usage général, bon compromis
   - `ultra`: Pour publications finales de haute qualité

3. **Rédiger le prompt en anglais**:
   - Consulter `references/imagen_api_guide.md` pour les conseils
   - Structure: Objet + Contexte + Style
   - Ajouter des modificateurs de qualité si nécessaire

4. **Sélectionner les paramètres**:
   - Format adapté au contexte (portrait, paysage, carré)
   - Nombre d'images (4 pour avoir du choix, 1-2 pour économiser)
   - Taille appropriée (1K suffit généralement, 2K pour impression)

5. **Déterminer l'emplacement**:
   - Local: Si spécifique au document actuel
   - Global: Si réutilisable dans plusieurs projets

6. **Générer et vérifier**:
   - Exécuter le script
   - Vérifier la qualité des images générées
   - Itérer si nécessaire en affinant le prompt

## Exemples d'utilisation

### Image pour exercice de mathématiques
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Simple geometric diagram showing a right triangle with labeled sides, educational style, clean lines, white background" \
  -o "cours-geometrie/images" \
  -m fast \
  -n 2 \
  -a square \
  -f triangle_diagram
```

### Personnage pour escape game
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Detective character in cartoon style, friendly appearance, magnifying glass, colorful illustration for children" \
  -o "4. Images/escape-game/detective-set" \
  -m standard \
  -n 4 \
  -a portrait \
  -f detective_character
```

### Illustration scientifique
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Detailed scientific illustration of the solar system, planets in orbit, educational diagram style, labels, high quality" \
  -o "4. Images/educatif/astronomie" \
  -m ultra \
  -n 1 \
  -a widescreen \
  -s 2K \
  -f solar_system
```

### Photo réaliste pour présentation
```bash
python .claude/skills/image-generator/scripts/generate_images.py \
  "Professional photo of modern classroom with students using tablets, natural lighting, 4K quality, bright and welcoming atmosphere" \
  -o "presentation-numerique/images" \
  -m standard \
  -n 4 \
  -a fullscreen \
  -f classroom_photo
```

## Conseils pour l'écriture de prompts

### Prompts courts efficaces
Pour génération rapide:
```
"Math geometric shapes diagram, simple, clean"
"Friendly robot character, cartoon"
"Science lab equipment photo, professional"
```

### Prompts détaillés
Pour contrôle précis:
```
"Professional studio photograph of scientific laboratory equipment including beakers and test tubes, clean white background, natural lighting, high quality 4K, perfect for educational materials"
```

### Styles courants

**Photographie réaliste**:
- "Professional photo", "studio photograph", "4K", "HDR"
- Ajouter détails d'éclairage: "natural light", "golden hour", "dramatic lighting"

**Illustration pour enfants**:
- "Cartoon style", "colorful illustration", "friendly", "cute"
- "Suitable for children", "playful", "bright colors"

**Éducatif/Technique**:
- "Educational diagram", "technical illustration", "scientific drawing"
- "Clean lines", "labeled", "schematic", "isometric"

**Artistique**:
- Styles: "watercolor", "oil painting", "sketch", "digital art"
- Mouvements: "impressionist", "art deco", "minimalist"

## Référence complète

Pour plus de détails sur l'API, les modificateurs avancés et les techniques d'optimisation, consulter `references/imagen_api_guide.md`.

## Gestion des erreurs courantes

### API Key manquante
Vérifier que `NANOBANANA_API_KEY` est définie dans `.env` à la racine du projet.

### Prompt en français
L'API Imagen n'accepte que l'anglais. Traduire le prompt avant de générer.

### Erreur de format
Vérifier que le modèle et les paramètres sont compatibles (ex: image_size uniquement pour standard/ultra).

### Résultats non satisfaisants
- Affiner le prompt avec plus de détails
- Ajouter des modificateurs de style ou qualité
- Essayer de générer plusieurs fois
- Consulter les exemples dans la référence
