# /createImage - Création intelligente d'images et visuels

## Description

Commande d'orchestration pour la création de tous types d'images et visuels pédagogiques. Analyse la demande de l'utilisateur et redirige vers le skill approprié : génération IA, infographie éducative, ou animation interactive.

## Usage

```
/createImage <description_du_visuel>
```

## Exemples d'utilisation

```bash
# Infographie récapitulative
/createImage infographie sur le théorème de Pythagore
/createImage le cours en une image sur les fonctions affines
/createImage schéma récapitulatif des identités remarquables

# Animation interactive
/createImage animation interactive du cercle trigonométrique
/createImage manipulation des vecteurs dans un repère
/createImage construction de la médiatrice pas à pas

# Image générée (IA)
/createImage illustration pour un problème de géométrie
/createImage photo réaliste d'un échiquier pour un exercice
/createImage dessin stylisé d'une pyramide pour le cours
```

## Protocole d'exécution

### ÉTAPE 1 : ANALYSE DE LA DEMANDE

Identifier le type de visuel demandé :

| Type | Déclencheurs | Skill à utiliser |
|------|--------------|------------------|
| **Infographie** | "infographie", "schéma", "récapitulatif", "cours en une image", "synthèse visuelle" | `infography-generator` |
| **Animation** | "animation", "interactif", "manipulation", "dynamique", "construction" | `interactive-animation` |
| **Image IA** | "illustration", "photo", "dessin", "image", "visuel" (générique) | `image-generator` |

### ÉTAPE 2 : CLARIFICATION SI NÉCESSAIRE

Si le type n'est pas clair, poser la question via `AskUserQuestion` :

```
Quel type de visuel souhaitez-vous créer ?

1. Infographie éducative (Recommandé) - Schéma récapitulatif du cours avec zones, texte et annotations
2. Animation interactive - Visualisation HTML manipulable (curseurs, clics, animations)
3. Image générée par IA - Illustration, photo réaliste ou dessin artistique
4. Autre - Préciser le type de visuel
```

### ÉTAPE 3 : COLLECTE DES INFORMATIONS

Selon le type identifié, collecter les informations nécessaires :

#### Pour Infographie (`infography-generator`)

| Information | Question si manquante |
|-------------|----------------------|
| **Source** | "Quel contenu analyser ? (fichier, dossier, notion)" |
| **Thème** | "Quelle notion mathématique ?" |
| **Style** | "Quel style ? (synthétique, détaillé, visuel)" |

#### Pour Animation (`interactive-animation`)

| Information | Question si manquante |
|-------------|----------------------|
| **Concept** | "Quelle notion illustrer ?" |
| **Interactions** | "Quels contrôles ? (curseurs, clics, saisie)" |
| **Scénario** | "Y a-t-il un scénario guidé ?" |

#### Pour Image IA (`image-generator`)

| Information | Question si manquante |
|-------------|----------------------|
| **Type** | "Quel type ? (infographic, schema, photo, humor, portrait, illustration, geometry, graph)" |
| **Description** | "Décrivez l'image souhaitée en détail" |
| **Style** | "Quel style ? (réaliste, cartoon, vintage, moderne...)" |
| **Usage** | "Pour quel usage ? (projection, impression, exercice)" |

### ÉTAPE 4 : DÉTERMINATION DU CHEMIN

Proposer l'emplacement selon le contexte :

```
📁 Emplacement proposé pour l'image :

1. Dans le dossier du projet actuel (Recommandé) - [chemin du projet ouvert]
2. Dans 4. Images/[niveau]/ - Dossier images centralisé
3. Autre emplacement - Préciser le chemin
```

**Logique de destination** :

- Si **projet ouvert** → `[projet]/annexes/` ou `[projet]/images/`
- Si **pas de projet** → `4. Images/[niveau]/[theme]/`
- Si **animation** → `[destination]/animations/`

### ÉTAPE 5 : EXÉCUTION DU SKILL

Invoquer le skill approprié avec tous les paramètres :

#### Infographie

```
Skill("infography-generator")
```

Le skill va :
1. Analyser le contenu source
2. Extraire les concepts clés
3. Générer une infographie détaillée via Gemini

#### Animation interactive

```
Skill("interactive-animation")
```

Le skill va :
1. Créer un fichier HTML autonome
2. Implémenter les contrôles interactifs
3. Garantir la précision mathématique
4. Optimiser pour la projection

#### Image IA

```
Skill("image-generator")
```

Le skill va :
1. Traduire la demande en prompt anglais optimisé
2. Choisir le modèle approprié (rapide/standard/ultra)
3. Générer l'image via Google Imagen
4. Sauvegarder au bon emplacement

### ÉTAPE 6 : AUTO-AMÉLIORATION (OBLIGATOIRE)

En fin de tâche, activer le skill `self-improve` pour analyser les difficultés et proposer des améliorations.

## Types d'images disponibles (image-generator)

Le skill `image-generator` supporte 8 types d'images avec des instructions optimisées :

| Type | Déclencheurs | Description |
|------|--------------|-------------|
| `infographic` | "infographie", "synthèse", "cours en une image" | Composition structurée avec zones, texte, flèches |
| `schema` | "schéma annoté", "légendes", "comme en SVT" | Objet central avec flèches et annotations |
| `photo` | "photo", "réaliste", "mise en situation" | Photographie naturelle pour contexte |
| `humor` | "humoristique", "Plonk et Replonk", "blague" | Illustration décalée, absurde, vintage |
| `portrait` | "portrait", "vue conceptuelle", "artistique" | Représentation abstraite d'un concept |
| `illustration` | "illustration", "pour exercice" | Image propre pour documents imprimés |
| `geometry` | "figure géométrique", "construction" | Précision mathématique, codages |
| `graph` | "graphique", "courbe", "repère" | Axes, courbes, points annotés |

**Usage dans le script** :
```bash
python ".claude\skills\creer\media\image-generator\scripts\generate_image.py" \
  --type humor \
  --prompt "DESCRIPTION DÉTAILLÉE" \
  --output "chemin/image.png"
```

## Combinaisons possibles

Certaines demandes peuvent nécessiter plusieurs skills :

| Demande | Skills combinés |
|---------|-----------------|
| "Infographie animée" | `infography-generator` + `interactive-animation` |
| "Animation avec illustrations IA" | `interactive-animation` + `image-generator` |
| "Schéma interactif" | Préférer `interactive-animation` seul |

## Styles disponibles par skill

### Infography-generator

- **Synthétique** : Concepts clés, peu de texte
- **Détaillé** : Explications complètes, exemples
- **Visuel** : Maximum d'illustrations, minimum de texte

### Interactive-animation

- **Géométrie** : Repère orthonormé, figures, transformations
- **Algèbre** : Graphiques de fonctions, courbes
- **Probabilités** : Simulations, lancers, tirages

### Image-generator

- **Réaliste** : Photos réalistes (photographie)
- **Éducatif** : Style manuel scolaire, clair
- **Artistique** : Illustrations stylisées
- **Schématique** : Diagrammes, schémas techniques

## Notes importantes

- **Qualité** : Toujours vérifier le rendu avant validation
- **Accessibilité** : Les animations doivent être lisibles projetées
- **Mathématiques** : Précision obligatoire pour les contenus mathématiques
- **Fichiers** : Format PNG pour images, HTML autonome pour animations

## Skills utilisés

- `infography-generator` : Génération d'infographies via Gemini
- `interactive-animation` : Création d'animations HTML/JS interactives
- `image-generator` : Génération d'images via Google Imagen
- `self-improve` : Auto-amélioration en fin de tâche
