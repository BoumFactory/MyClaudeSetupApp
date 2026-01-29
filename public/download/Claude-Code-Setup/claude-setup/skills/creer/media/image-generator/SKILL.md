---
name: image-generator
description: Skill polyvalent pour générer tout type d'image éducative via Gemini. Couvre les infographies, schémas annotés, photos, illustrations humoristiques, portraits, vues conceptuelles, et bien plus. Nécessite une phase THINKHARD pour construire un prompt parfait avant génération. Utiliser pour toute demande d'image qui n'est pas une simple icône.
---

# Image Generator Skill

Skill polyvalent pour générer des **images éducatives de haute qualité** via Gemini 3 Pro. Ce skill couvre une large palette de formats visuels, de l'infographie structurée à l'illustration humoristique.

## Philosophie : THINKHARD avant de générer

**La génération d'image coûte cher** (temps API, crédits). L'objectif est de réussir en **une seule génération**.

Avant TOUTE génération, le modèle doit :
1. **Analyser** la demande en profondeur
2. **Concevoir** mentalement l'image (composition, éléments, texte)
3. **Structurer** un prompt ultra-détaillé
4. **Vérifier** chaque élément du prompt (notations, accents, positions)

Ce processus THINKHARD garantit un résultat optimal du premier coup.

---

## Types d'images supportés

### 1. Infographie éducative
**Quand** : "Le cours en une image", synthèse visuelle, fiche récap
**Caractéristiques** :
- Plusieurs zones/sections distinctes
- Texte, titres, annotations
- Flèches, connecteurs, hiérarchie visuelle
- Organisation claire de l'information

### 2. Schéma annoté (style scientifique)
**Quand** : Schéma avec légendes et flèches, "comme en SVT"
**Caractéristiques** :
- Objet/concept central
- Flèches pointant vers des parties
- Légendes explicatives
- Numérotation ou lettrage des éléments

### 3. Photo réaliste
**Quand** : Illustration de contexte, mise en situation, photo de problème
**Caractéristiques** :
- Style photographique réaliste
- Contexte visuel pour un exercice
- Objets du quotidien pour ancrer les maths

### 4. Portrait / Vue conceptuelle
**Quand** : Représentation d'un concept mathématique, vue artistique
**Caractéristiques** :
- Abstraction visuelle d'une notion
- Style artistique possible
- Focus sur l'esthétique et la compréhension

### 5. Image humoristique
**Quand** : Illustration décalée, style "Plonk et Replonk", blague visuelle
**Caractéristiques** :
- Personnages expressifs
- Situations absurdes ou décalées
- Texte humoristique possible
- Style cartoon ou vintage

### 6. Illustration de cours
**Quand** : Image pour accompagner un énoncé, illustration de notion
**Caractéristiques** :
- Style propre et lisible
- Adapté à l'impression
- Peut contenir du texte minimal

### 7. Schéma géométrique
**Quand** : Figure géométrique précise, construction
**Caractéristiques** :
- Précision mathématique requise
- Notations correctes
- Codages (angles droits, longueurs égales)

### 8. Graphique / Courbe
**Quand** : Représentation de fonction, diagramme
**Caractéristiques** :
- Repère avec axes gradués
- Courbes ou points
- Annotations sur les axes

---

## Workflow obligatoire

### Étape 1 : Comprendre la demande

1. **Quel type d'image ?** (voir liste ci-dessus)
2. **Quel contexte éducatif ?** (niveau, chapitre, notion)
3. **Quel usage ?** (projection, impression, exercice, décoration)
4. **Quel style ?** (réaliste, schématique, humoristique, artistique)

### Étape 2 : Concevoir l'image mentalement (THINKHARD)

**C'est l'étape critique.** Avant d'écrire le prompt, visualiser :

- **Composition globale** : Que voit-on en premier ? En second ?
- **Éléments présents** : Lister TOUS les éléments visuels
- **Texte à afficher** : Quel texte exact ? Où ?
- **Couleurs** : Palette cohérente avec l'usage
- **Positions** : Où est chaque élément ?
- **Relations** : Quelles flèches, liens, hiérarchies ?

### Étape 3 : Construire le prompt ultra-détaillé

**Format recommandé** :

```
TYPE D'IMAGE : [infographie / schéma annoté / photo / etc.]

CONTEXTE :
- Niveau : [collège/lycée/classe précise]
- Notion : [concept mathématique]
- Usage : [projection/impression/exercice]

COMPOSITION GLOBALE :
- Format : [portrait/paysage/carré]
- Style visuel : [réaliste/schématique/cartoon/etc.]
- Fond : [couleur/texture/blanc]
- Disposition : [description du layout]

ÉLÉMENT PRINCIPAL :
- Description : [ce que c'est]
- Position : [centre/gauche/haut/etc.]
- Taille : [grande/moyenne/petite]
- Détails visuels : [couleurs, formes, textures]

ÉLÉMENTS SECONDAIRES :
- Élément 1 : [description, position, taille]
- Élément 2 : [description, position, taille]
- ...

TEXTE À AFFICHER :
- Texte 1 : "[contenu exact]" - position : [où], style : [police, taille, couleur]
- Texte 2 : "[contenu exact]" - position : [où], style : [police, taille, couleur]

ANNOTATIONS / FLÈCHES :
- Flèche de [A] vers [B] avec label "[texte]"
- Annotation pointant vers [élément] : "[texte]"

STYLE VISUEL :
- Palette de couleurs : [couleurs principales]
- Bordures/contours : [style]
- Ambiance : [sérieuse/ludique/professionnelle]

CONTRAINTES :
- [Lisible en projection / adapté à l'impression]
- [Fond blanc pour impression]
- [Pas de texte complexe avec accents]
```

### Étape 4 : Vérification THINKHARD

Avant génération, vérifier mentalement :

#### Notations mathématiques
| Contexte | Correct | Incorrect |
|----------|---------|-----------|
| Exposant simple | `2^-3` | `2^(-3)` |
| Exposant avec opération | `a^(m+n)` | `a^m+n` |
| Base négative | `(-3)^2` | `-3^2` |

#### Texte français
| Problème | Solution |
|----------|----------|
| Accents | Simplifier : "connaitre" au lieu de "connaître" |
| Caractères spéciaux | Éviter ≤ ≥, utiliser "<=" ou "inferieur ou egal" |
| Apostrophes | Espacer : "l exposant" au lieu de "l'exposant" |

#### Termes parasites
| À éviter | Alternative |
|----------|-------------|
| "BOX 1", "SECTION 2" | Descriptions naturelles |
| Termes anglais techniques | Français ou description |

#### Flèches et positions
```
❌ "Une flèche pointe vers l'exposant"
✅ "Arrow on the LEFT side, pointing RIGHT toward the 'n', with label below"
```

### Étape 5 : Générer l'image

Utiliser le script avec le prompt construit :

```bash
python ".claude/skills/image-generator/scripts/generate_image.py" \
  --prompt "DESCRIPTION COMPLÈTE ICI" \
  --context "Niveau: 3ème. Chapitre: Pythagore." \
  --style "Clean educational, white background" \
  --output "chemin/vers/image.png"
```

Ou via fichier JSON pour les prompts longs :

```bash
python ".claude/skills/image-generator/scripts/generate_image.py" \
  --prompt-file "prompt_image.json" \
  --output "chemin/vers/image.png"
```

---

## Exemples de prompts par type

### Exemple 1 : Schéma annoté (style scientifique)

```
TYPE D'IMAGE : Schéma annoté

CONTEXTE :
- Niveau : 3ème
- Notion : Triangle rectangle et ses éléments
- Usage : Projection en classe

COMPOSITION GLOBALE :
- Format : Paysage
- Style : Schéma épuré, lignes nettes
- Fond : Blanc
- Disposition : Triangle au centre, annotations autour

ÉLÉMENT PRINCIPAL :
- Triangle rectangle ABC, angle droit en C
- Position : Centre de l'image
- Taille : Grande (60% de l'image)
- Couleurs : Contour bleu foncé, épaisseur 3px

ANNOTATIONS AVEC FLÈCHES :
- Flèche depuis la gauche vers le côté [AB] : "Hypoténuse (côté le plus long)"
- Flèche depuis le haut vers l'angle C : "Angle droit (90°)"
- Flèche depuis le bas vers le côté [AC] : "Côté adjacent à A"
- Flèche depuis la droite vers le côté [BC] : "Côté adjacent à B"

CODAGES :
- Petit carré rouge dans l'angle C (angle droit)
- Lettres A, B, C aux sommets en bleu

STYLE :
- Palette : Bleu principal, rouge pour l'angle droit
- Flèches fines avec pointes
- Texte en noir, police sans-serif
```

### Exemple 2 : Image humoristique

```
TYPE D'IMAGE : Illustration humoristique style vintage

CONTEXTE :
- Pour détendre l'atmosphère en cours
- Notion : Difficultés avec les fractions

COMPOSITION GLOBALE :
- Format : Carré
- Style : Dessin vintage années 50, noir et blanc avec une touche de couleur
- Fond : Papier vieilli, légèrement jauni
- Ambiance : Humour décalé, absurde

SCÈNE :
- Un écolier des années 50 (costume, cartable ancien)
- Devant un tableau noir couvert de fractions
- Expression de panique exagérée
- Les fractions semblent "vivantes" et menaçantes

ÉLÉMENTS VISUELS :
- Tableau noir avec fractions griffonnées
- Fractions avec petits yeux et sourires malicieux
- Écolier qui recule, mains levées
- Craie au sol (tombée)

TEXTE :
- En bas, style légende vintage : "Quand les fractions attaquent..."
- Police : Typewriter / machine à écrire

STYLE :
- Trait fin, hachures pour les ombres
- Une seule couleur accent : rouge sur les fractions
- Aspect "gravure ancienne"
```

### Exemple 3 : Photo réaliste pour énoncé

```
TYPE D'IMAGE : Photo réaliste

CONTEXTE :
- Illustration d'un problème de proportionnalité
- Usage : Exercice imprimé

COMPOSITION GLOBALE :
- Format : Paysage
- Style : Photographie naturelle, lumière douce
- Fond : Contexte de marché/épicerie

SCÈNE :
- Étal de fruits avec pommes rouges
- Étiquette de prix visible : "2,50 € le kg"
- Balance de marché visible
- Quelques pommes dans un sac en papier

ÉLÉMENTS :
- Pommes : rouges, brillantes, appétissantes
- Étiquette : claire et lisible
- Balance : ancienne ou moderne
- Ambiance : marché du matin, lumière chaude

CONTRAINTES :
- Étiquette parfaitement lisible
- Prix en euros bien visible
- Pas de personnes dans le cadre
```

### Exemple 4 : Portrait conceptuel

```
TYPE D'IMAGE : Portrait conceptuel / Vue artistique

CONTEXTE :
- Représentation visuelle du concept de "fonction"
- Pour affichage ou introduction de chapitre

COMPOSITION GLOBALE :
- Format : Portrait
- Style : Illustration moderne, géométrique
- Fond : Dégradé bleu vers violet

CONCEPT VISUALISÉ :
- Machine abstraite avec entrée et sortie
- Entrée : Nombres qui "entrent" (1, 2, 3...)
- Sortie : Nombres transformés qui "sortent"
- La machine est stylisée, moderne, presque futuriste

ÉLÉMENTS VISUELS :
- Forme centrale : boîte ou engrenage stylisé avec "f"
- Flèches d'entrée à gauche avec nombres
- Flèches de sortie à droite avec résultats
- Effets de lumière/énergie autour de la transformation

PALETTE :
- Bleu électrique, violet, blanc
- Effets néon pour les transformations
- Contrastes forts

TEXTE :
- Aucun texte (image purement conceptuelle)
```

---

## Répertoires de destination

### Convention de nommage

| Type d'image | Préfixe | Exemple |
|--------------|---------|---------|
| Infographie | `infographie_` | `infographie_pythagore.png` |
| Schéma | `schema_` | `schema_triangle_rectangle.png` |
| Photo | `photo_` | `photo_marche_fruits.png` |
| Illustration | `illus_` | `illus_fonction.png` |
| Humoristique | `humor_` | `humor_fractions.png` |

### Emplacement

```
Projet/
├── images/              # Toutes les images générées
│   ├── infographie_*.png
│   ├── schema_*.png
│   └── ...
└── annexes/             # Alternative si images/ n'existe pas
```

---

## Mascottes mathématiques (optionnel)

Pour les infographies, des mascottes peuvent être ajoutées en bas-droite :

| Mascotte | Domaine | Description |
|----------|---------|-------------|
| **Gaia** | Géométrie | Fille noire, cheveux bouclés, signe OK |
| **Alex** | Analyse | Garçon asiatique, lunettes, pouce levé |
| **Priya** | Probabilités | Femme sud-asiatique, clin d'oeil |
| **Nabil** | Arithmétique | Garçon nord-africain, compte sur doigts |
| **Sofia** | Algèbre | Fille latina, signe victoire |
| **Sven** | Suites | Garçon scandinave, signe paix |

Descriptions complètes dans : `.claude/skills/image-generator/knowledge/mascots.json`

---

## Checklist THINKHARD avant génération

```
□ Type d'image clairement identifié
□ Tous les éléments visuels listés
□ Positions de chaque élément précisées
□ Texte exact à afficher (si applicable)
□ Notations mathématiques vérifiées (exposants, parenthèses)
□ Accents simplifiés dans le texte français
□ Pas de termes anglais/techniques qui pourraient fuiter
□ Flèches avec positions et directions explicites
□ Style et palette de couleurs définis
□ Format adapté à l'usage (projection/impression)
□ Prompt ordonné du plus important au moins important
```

---

## Paramètres du script

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `--prompt`, `-p` | Description détaillée | Oui* |
| `--context`, `-c` | Contexte éducatif | Non |
| `--style`, `-s` | Instructions de style | Non |
| `--output`, `-o` | Chemin de sortie | Oui |
| `--prompt-file`, `-f` | Fichier JSON | Non* |

*Soit `--prompt` soit `--prompt-file` requis.

## Dépendances

```bash
pip install requests python-dotenv
```

Clé API : `NANOBANANA_API_KEY` dans le fichier `.env`
