# Guide de l'API Google Imagen

## Modèles disponibles

### Imagen 4 (Recommandé)
- **Fast** (`imagen-4.0-fast-generate-001`): Génération rapide et économique
- **Standard** (`imagen-4.0-generate-001`): Équilibre qualité/coût
- **Ultra** (`imagen-4.0-ultra-generate-001`): Meilleure qualité, plus coûteux

### Imagen 3
- **Standard** (`imagen-3.0-generate-002`): Version précédente, compatible

## Paramètres de configuration

### Nombre d'images
- `number_of_images`: 1 à 4 images par requête
- Défaut: 4

### Taille d'image (Standard/Ultra uniquement)
- `image_size`: "1K" ou "2K"
- Défaut: "1K"
- Non disponible pour le modèle Fast

### Format d'image
- `aspect_ratio`:
  - "1:1" - Carré (par défaut)
  - "4:3" - Plein écran
  - "3:4" - Portrait plein écran
  - "16:9" - Écran large
  - "9:16" - Portrait

### Génération de personnes
- `person_generation`:
  - "dont_allow" - Bloquer la génération de personnes
  - "allow_adult" - Générer des adultes uniquement (défaut)
  - "allow_all" - Générer adultes et enfants (non disponible dans UE/UK)

## Conseils pour l'écriture de prompts

### Structure de base
Un bon prompt contient:
1. **Objet**: Ce qui doit être représenté
2. **Contexte**: L'arrière-plan ou l'environnement
3. **Style**: Le style artistique ou photographique

Exemple: "Un croquis (style) d'un appartement moderne (objet) entouré de gratte-ciel (contexte)"

### Longueur
- Maximum: 480 jetons
- Prompts courts: génération rapide, résultats généraux
- Prompts longs: plus de détails, contrôle précis

### Modificateurs utiles

#### Pour la photographie
- Type de prise: "gros plan", "plan large", "vue aérienne", "vue de dessous"
- Éclairage: "naturel", "spectaculaire", "chaud", "froid", "heure dorée"
- Objectif: "35mm", "50mm", "fisheye", "grand angle", "macro"
- Effets: "flou de mouvement", "flou artistique", "bokeh"
- Film: "noir et blanc", "polaroid", "film"

#### Pour l'illustration et l'art
- Techniques: "peinture", "esquisse", "croquis", "dessin au fusain", "pastel"
- Styles: "impressionniste", "renaissance", "pop art", "art déco"
- Numérique: "rendu 3D", "art numérique", "isométrique"

#### Modificateurs de qualité
- Général: "haute qualité", "professionnel", "détaillé"
- Photo: "4K", "HDR", "photo studio"
- Art: "stylisé", "raffiné"

### Exemples de prompts efficaces

#### Photographie réaliste
```
Photo professionnelle en studio d'un produit, éclairage naturel,
haute qualité, 4K, fond blanc minimaliste
```

#### Portrait
```
Portrait en 35mm d'une personne souriante, éclairage de l'heure dorée,
bokeh d'arrière-plan, style photographique professionnel
```

#### Illustration éducative
```
Illustration scientifique détaillée d'un système solaire,
style technique, couleurs vives, fond noir étoilé,
haute résolution
```

#### Image pour enfants
```
Illustration colorée d'un robot amical dans un jardin fleuri,
style cartoon mignon, couleurs pastel, adapté aux enfants
```

#### Image technique/schéma
```
Schéma technique isométrique d'un bâtiment moderne,
lignes nettes, style architectural, rendu 3D propre
```

## Génération de texte dans les images

Imagen peut ajouter du texte dans les images. Conseils:
- Limiter à 25 caractères maximum par texte
- Spécifier le texte entre guillemets dans le prompt
- Itérer si nécessaire (le texte peut nécessiter plusieurs tentatives)
- Exemple: `Affiche avec le texte "Summerland" en gros titre`

## Contraintes importantes

1. **Langue**: Les prompts doivent être en anglais
2. **Localisation**: Certaines fonctionnalités (comme allow_all) sont restreintes dans certaines régions
3. **Limite de tokens**: Maximum 480 jetons par prompt
4. **Itération**: Parfois plusieurs générations sont nécessaires pour obtenir le résultat souhaité

## Stratégies d'optimisation

### Pour des coûts réduits
1. Utiliser le modèle "fast"
2. Générer moins d'images (1-2 au lieu de 4)
3. Utiliser la taille "1K"

### Pour la meilleure qualité
1. Utiliser le modèle "ultra"
2. Générer 4 images et sélectionner la meilleure
3. Utiliser la taille "2K"
4. Ajouter des modificateurs de qualité au prompt

### Pour des itérations rapides
1. Commencer avec le modèle "fast" pour tester des prompts
2. Une fois satisfait, régénérer avec "standard" ou "ultra"
3. Affiner progressivement les prompts entre les itérations
