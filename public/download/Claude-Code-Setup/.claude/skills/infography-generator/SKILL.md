---
name: infography-generator
description: Skill pour générer des infographies éducatives riches (images avec texte, zones, schémas annotés) à partir de contenu mathématique. Analyse le contenu source (fichier/dossier), synthétise les concepts clés, et génère une infographie détaillée via Gemini 3 Pro. Utiliser pour créer "le cours en une image" ou des schémas explicatifs annotés.
---

# Infography Generator Skill

Skill spécialisé pour générer des **infographies éducatives** de haute qualité. Une infographie n'est PAS une simple image : c'est une composition visuelle structurée avec :
- Plusieurs zones/sections distinctes
- Du texte, des titres, des annotations
- Des flèches, connecteurs, hiérarchie visuelle
- Des schémas, diagrammes ou flowcharts
- Une organisation claire de l'information

## Différence avec image-generator

| Aspect | image-generator | infography-generator |
|--------|----------------|---------------------|
| **Modèle** | gemini-2.5-flash-image-preview | **gemini-3-pro-image-preview** |
| **Prompts** | Courts et descriptifs | Longs et très détaillés |
| **Contenu** | Images simples | Images avec texte et structure |
| **Contexte** | Minimal | Analyse complète du contenu source |
| **Usage** | Illustrations, assets | Synthèse visuelle de cours |

## Workflow obligatoire

### Étape 1 : Analyser le contenu source

Quand l'utilisateur donne un chemin vers un fichier ou dossier :

1. **Lire le contenu intégralement**
   - Si fichier `.tex` : extraire le contenu mathématique
   - Si dossier : lire tous les fichiers pertinents
   - Identifier : titre, notions, définitions, théorèmes, exemples, exercices

2. **Identifier les concepts clés**
   - Quelles sont les notions principales ?
   - Quelles sont les relations entre les concepts ?
   - Quels sont les points importants à retenir ?
   - Y a-t-il des formules essentielles ?
   - Y a-t-il un raisonnement/processus à visualiser ?

3. **Déterminer le type d'infographie**
   - **Synthèse de cours** : "Le chapitre X en une image"
   - **Schéma explicatif** : Visualiser un concept/processus
   - **Carte mentale** : Relations entre notions
   - **Fiche mémo** : Formules et points clés
   - **Processus/Méthode** : Étapes d'une résolution

### Étape 2 : Construire une description ULTRA-DÉTAILLÉE

**C'EST L'ÉTAPE CRITIQUE.** Le modèle Gemini 3 Pro accepte des prompts très longs. Tu dois décrire TOUT ce que tu veux voir dans l'infographie :

#### Structure à suivre

```
TITRE : [Titre de l'infographie]

LAYOUT GÉNÉRAL :
- Description de la disposition globale (vertical, horizontal, zones)
- Nombre de sections principales
- Hiérarchie visuelle (ce qui doit ressortir en premier)

SECTION 1 : [Nom de la section]
- Position : [haut gauche, centre, etc.]
- Contenu textuel exact : "[Le texte à afficher]"
- Éléments visuels : [icône, schéma, diagramme]
- Couleur de fond : [couleur]
- Taille relative : [grande, moyenne, petite]

SECTION 2 : [Nom de la section]
...

ÉLÉMENTS DE LIAISON :
- Flèches de X vers Y avec label "[texte]"
- Connecteurs entre sections A et B
- Numérotation des étapes

FORMULES MATHÉMATIQUES :
- Formule 1 : "[LaTeX ou texte]" - position et mise en évidence
- Formule 2 : ...

ANNOTATIONS ET LÉGENDES :
- Annotation 1 : "[texte]" pointant vers [élément]
- Légende des couleurs si nécessaire

STYLE VISUEL :
- Palette de couleurs
- Style des bordures et ombres
- Police (sans-serif pour lisibilité)
- Niveau de détail
```

### Étape 3 : Générer l'infographie

Utiliser le script avec le prompt ultra-détaillé :

```bash
python ".claude/skills/infography-generator/scripts/generate_infography.py" \
  --prompt "DESCRIPTION COMPLÈTE ICI" \
  --context "Niveau: 3ème. Chapitre: Théorème de Pythagore." \
  --style "Educational infographic, clean, white background, blue and orange accents" \
  --output "chemin/vers/infographie.png"
```

Ou via fichier JSON pour les prompts très longs :

```bash
python ".claude/skills/infography-generator/scripts/generate_infography.py" \
  --prompt-file "prompt_infographie.json" \
  --output "chemin/vers/infographie.png"
```

## Exemples de descriptions détaillées

### Exemple 1 : Synthèse du théorème de Pythagore

```
TITRE : "LE THÉORÈME DE PYTHAGORE - Tout comprendre en une image"

LAYOUT GÉNÉRAL :
- Format paysage, divisé en 4 zones principales
- Zone centrale dominante avec le triangle et la formule
- Zones latérales pour conditions et applications
- Zone inférieure pour exemples

ZONE CENTRALE (50% de l'image) :
- Triangle rectangle ABC clairement dessiné
- Angle droit en C marqué avec un petit carré rouge
- Côtés labellés : "a" (côté opposé à A), "b" (côté opposé à B), "c" (hypoténuse)
- Formule encadrée en grand : "a² + b² = c²"
- Annotation : "L'hypoténuse est le côté le plus long, face à l'angle droit"

ZONE GAUCHE - CONDITIONS :
- Titre : "Quand l'utiliser ?"
- Icône : triangle avec point d'interrogation
- Liste à puces :
  • "Triangle RECTANGLE uniquement"
  • "Pour calculer un côté"
  • "Pour vérifier si un triangle est rectangle"
- Couleur de fond : bleu clair

ZONE DROITE - FORMULES DÉRIVÉES :
- Titre : "Les 3 formules"
- Formule 1 : "c = √(a² + b²)" avec flèche "trouver l'hypoténuse"
- Formule 2 : "a = √(c² - b²)" avec flèche "trouver un côté de l'angle droit"
- Formule 3 : "b = √(c² - a²)" avec flèche "trouver l'autre côté"
- Couleur de fond : orange clair

ZONE INFÉRIEURE - EXEMPLE :
- Titre : "Exemple concret"
- Triangle avec valeurs : a=3, b=4, c=?
- Calcul montré étape par étape : "c² = 3² + 4² = 9 + 16 = 25, donc c = 5"
- Résultat encadré : "c = 5"

ÉLÉMENTS VISUELS :
- Carrés construits sur chaque côté du triangle (visualisation géométrique)
- Flèches reliant les zones entre elles
- Icônes : calculatrice, règle, équerre

STYLE :
- Fond blanc
- Palette : bleu principal, orange accent, gris pour le texte
- Bordures arrondies sur les zones
- Police sans-serif, grande taille pour la formule principale
```

### Exemple 2 : Processus de résolution d'équation

```
TITRE : "RÉSOUDRE UNE ÉQUATION DU PREMIER DEGRÉ - La méthode pas à pas"

LAYOUT :
- Format vertical (portrait)
- 5 étapes numérotées de haut en bas
- Flèches descendantes entre chaque étape
- Exemple fil rouge à droite de chaque étape

ÉTAPE 1 - IDENTIFIER :
- Numéro : cercle bleu avec "1"
- Titre : "Identifier l'équation"
- Description : "Repérer l'inconnue x et les nombres"
- Exemple à droite : "3x + 5 = 17" avec x entouré

ÉTAPE 2 - ISOLER LES X :
- Numéro : cercle bleu avec "2"
- Titre : "Regrouper les x d'un côté"
- Description : "Déplacer les termes avec x à gauche"
- Exemple : "3x = 17 - 5"
- Annotation : "Ce qui passe de l'autre côté change de signe"

ÉTAPE 3 - ISOLER LES NOMBRES :
- Numéro : cercle bleu avec "3"
- Titre : "Calculer le membre de droite"
- Exemple : "3x = 12"

ÉTAPE 4 - DIVISER :
- Numéro : cercle bleu avec "4"
- Titre : "Diviser par le coefficient de x"
- Description : "Diviser des deux côtés par le nombre devant x"
- Exemple : "x = 12 ÷ 3"

ÉTAPE 5 - CONCLURE :
- Numéro : cercle vert avec "✓"
- Titre : "Solution"
- Exemple encadré en vert : "x = 4"
- Annotation : "Toujours vérifier : 3×4 + 5 = 17 ✓"

STYLE :
- Fond blanc cassé
- Flèches bleues descendantes entre les étapes
- Encadrés avec coins arrondis
- Zone exemple sur fond jaune pâle
```

## Conseils pour des infographies efficaces

### DO (À faire)

- ✅ Décrire chaque zone avec son contenu textuel exact
- ✅ Préciser la position de chaque élément
- ✅ Indiquer les couleurs et le style
- ✅ Mentionner les flèches et connecteurs
- ✅ Spécifier la hiérarchie visuelle (ce qui doit ressortir)
- ✅ Inclure des exemples concrets
- ✅ Demander un fond blanc/clair pour impression

### DON'T (À éviter)

- ❌ Description vague : "une infographie sur Pythagore"
- ❌ Oublier de préciser le texte à afficher
- ❌ Trop de sections (max 4-6)
- ❌ Texte trop long dans chaque zone
- ❌ Palette de couleurs non spécifiée
- ❌ Oublier les annotations et légendes

## Types d'infographies par contexte

### Synthèse de chapitre ("Le cours en une image")
- Layout avec zone centrale pour le concept principal
- Zones satellites pour propriétés, exemples, contre-exemples
- Formules mises en évidence
- Idéal pour : révisions, affichage classe

### Schéma de processus (résolution, méthode)
- Layout vertical avec étapes numérotées
- Flèches de progression
- Exemple fil rouge
- Idéal pour : méthodes de calcul, démonstrations

### Carte conceptuelle
- Concept central avec branches
- Relations nommées entre concepts
- Hiérarchie visuelle par taille
- Idéal pour : relations entre notions

### Fiche mémo/formulaire
- Grille de formules
- Couleurs par catégorie
- Exemples d'application
- Idéal pour : aide-mémoire, révisions exam

### Comparaison (vs, différences)
- Deux colonnes côte à côte
- Critères de comparaison listés
- Similitudes au centre, différences sur les côtés
- Idéal pour : distinguer deux notions proches

## Paramètres du script

| Paramètre | Description | Obligatoire |
|-----------|-------------|-------------|
| `--prompt`, `-p` | Description détaillée | Oui* |
| `--context`, `-c` | Contexte éducatif (niveau, chapitre) | Non |
| `--style`, `-s` | Instructions de style visuel | Non |
| `--output`, `-o` | Chemin du fichier de sortie | Oui |
| `--prompt-file`, `-f` | Fichier JSON avec le prompt | Non* |

*Soit `--prompt` soit `--prompt-file` est requis.

## Format du fichier JSON de prompt

```json
{
  "prompt": "Description complète de l'infographie...",
  "context": "Niveau 3ème, chapitre Géométrie",
  "style": "Clean educational infographic, white background, blue accents"
}
```

## Dépendances

Mêmes dépendances que image-generator :

```bash
pip install requests python-dotenv
```

Clé API : `NANOBANANA_API_KEY` dans le fichier `.env`

## Mascottes mathématiques (zone bas-droite)

### Pourquoi utiliser une mascotte ?

**PROBLÈME CONNU** : Le modèle Gemini fait souvent des erreurs dans la zone bas-droite des infographies (texte illisible, formules incorrectes, mise en page cassée).

**SOLUTION** : Remplacer cette zone problématique par une **mascotte simple** qui fait un geste positif. C'est plus fiable et ça ajoute une touche sympathique !

### Mascottes disponibles

Chaque mascotte représente un domaine mathématique. Choisir selon le chapitre :

| Mascotte | Domaine | Couleur | Description |
|----------|---------|---------|-------------|
| **Gaia** | Géométrie | Bleu | Fille noire, cheveux bouclés, compas, signe OK |
| **Alex** | Analyse/Calcul | Vert | Garçon asiatique, lunettes, sweat intégrale, pouce levé |
| **Priya** | Probabilités | Violet | Femme sud-asiatique, tresses, dés, clin d'oeil malicieux |
| **Nabil** | Arithmétique | Orange | Garçon nord-africain, spirale nombres, compte sur doigts |
| **Sofia** | Algèbre | Rouge | Fille latina, queue de cheval, X/Y, signe victoire |
| **Sven** | Suites | Turquoise | Garçon scandinave, spirale Fibonacci, signe paix |

### Comment intégrer une mascotte dans le prompt

Ajouter dans la description de l'infographie, section **ZONE BAS-DROITE** :

```
ZONE BAS-DROITE - MASCOTTE :
- Petit personnage manga/chibi style kawaii
- [NOM DE LA MASCOTTE] : [description courte]
- Geste positif (pouce leve, clin d'oeil, signe OK, victoire)
- Petite taille (coin de l'image)
- Peut avoir une bulle de dialogue courte : "Bravo !" ou "Tu as compris !"
```

### Exemple concret

Pour une infographie sur le produit scalaire (géométrie) :

```
ZONE BAS-DROITE - MASCOTTE :
- Petit personnage chibi kawaii en bas a droite
- Gaia : jeune fille noire avec cheveux boucles, t-shirt bleu triangles
- Elle fait le signe OK avec un clin d'oeil joyeux
- Petite bulle : "Le produit scalaire, c'est geometrique !"
- Style mignon et encourageant
```

### Infographies de présentation des mascottes

Des infographies complètes de présentation existent dans :
```
.claude/skills/infography-generator/assets/mascots/
```

Chaque mascotte a sa propre infographie avec tour d'horizon de son domaine :
- `gaia_geometrie.png` - Géométrie : formes, mesures, outils, applications
- `alex_analyse.png` - Analyse : méthodologie de résolution
- `priya_probabilites.png` - Probas/Stats : distributions, formules, applications
- `nabil_arithmetique.png` - Arithmétique : opérations, nombres, méthode
- `sofia_algebre.png` - Algèbre : variables, équations, résolution
- `sven_suites.png` - Suites : récurrence, arithmétiques, géométriques

Ces infographies peuvent servir d'introduction à un chapitre ou d'affichage en classe.

### Fichier de référence

Toutes les descriptions détaillées des mascottes sont dans :
```
.claude/skills/infography-generator/knowledge/mascots.json
```

## Workflow complet résumé

1. **Utilisateur** donne un chemin vers contenu mathématique
2. **Agent** lit et analyse le contenu intégralement
3. **Agent** identifie type d'infographie adapté
4. **Agent** choisit la mascotte appropriée au domaine
5. **Agent** construit une description ULTRA-DÉTAILLÉE avec mascotte en bas-droite
6. **Agent** génère via le script avec Gemini 3 Pro
7. **Agent** vérifie le résultat et propose ajustements si nécessaire
