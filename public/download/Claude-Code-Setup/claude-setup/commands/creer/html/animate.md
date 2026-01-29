# Commande /animate

Création d'une animation mathématique interactive à partir d'une demande utilisateur.

## Demande utilisateur

$ARGUMENTS

## Ton rôle

Tu es le **coordinateur** de la création d'animations. Tu dois :

1. **Analyser** la demande utilisateur
2. **Structurer** un prompt détaillé et complet pour l'agent
3. **Lancer** l'agent `interactive-animation-creator`

## Étape 1 : Analyse de la demande

Extraire de la demande utilisateur :

### Sujet mathématique
- Thème principal (géométrie, fonctions, suites, probabilités, algèbre...)
- Notions spécifiques à illustrer
- Niveau scolaire si mentionné (sinon, déduire du sujet)

### Besoins pédagogiques
- Objectif de l'animation (comprendre, visualiser, manipuler, démontrer...)
- Cas particuliers à montrer
- Erreurs courantes à prévenir
- Interactivité souhaitée

### Paramètres à contrôler
- Identifier les variables que l'utilisateur voudra ajuster
- Déterminer les plages de valeurs raisonnables
- Prévoir les options d'affichage utiles

### Scénarios à créer
- Scénario basique : introduction progressive du concept
- Scénario intermédiaire : exemples d'application
- Scénario avancé : cas limites, propriétés particulières

## Étape 2 : Structuration du prompt

Créer un prompt structuré selon ce template :

```markdown
## Animation demandée

**Titre** : [Titre clair et concis]
**Sujet** : [Thème mathématique]
**Niveau** : [Collège/Lycée/Supérieur]
**Destination** : [Chemin du dossier de sortie]

## Description détaillée

[Description complète de ce que l'animation doit montrer]

## Éléments graphiques requis

- [Liste des objets à dessiner : points, vecteurs, courbes, etc.]
- [Leurs propriétés visuelles : couleurs, épaisseurs, labels]

## Paramètres contrôlables

| Paramètre | Type | Plage | Défaut | Description |
|-----------|------|-------|--------|-------------|
| ... | range/number/checkbox/select | ... | ... | ... |

## Informations à afficher

- [Liste des valeurs calculées à montrer en temps réel]

## Scénarios pédagogiques

### Scénario 1 : Introduction (basique)
- Étape 1 : [Description]
- Étape 2 : [Description]
- ...

### Scénario 2 : Application (intermédiaire)
- Étape 1 : [Description]
- ...

### Scénario 3 : Approfondissement (avancé)
- Étape 1 : [Description]
- ...

## Contraintes techniques

- [Précisions sur les calculs mathématiques]
- [Cas limites à gérer]
- [Comportements spécifiques]

## Notes pédagogiques

- [Points d'attention pour l'enseignement]
- [Erreurs courantes des élèves à anticiper]
```

## Étape 3 : Demander le chemin de destination

Si l'utilisateur n'a pas précisé où créer l'animation, lui demander :

> Où souhaitez-vous créer l'animation ?
>
> Exemples de chemins :
> - `./animations/vecteurs/`
> - `C:\Users\...\animations\trigonometrie\`

## Étape 4 : Lancer l'agent

Une fois le prompt structuré et le chemin connu, lancer l'agent :

```
Lancer l'agent `interactive-animation-creator` avec le prompt structuré complet.
```

L'agent s'occupera de :
- Copier le template
- Implémenter `animation-logic.js`
- Définir les scénarios
- Tester et valider
- Générer le monolithe si demandé

## Exemple de transformation

### Demande utilisateur brute
> "fais moi une animation sur les vecteurs"

### Prompt structuré généré

```markdown
## Animation demandée

**Titre** : Manipulation de vecteurs dans le plan
**Sujet** : Géométrie - Vecteurs
**Niveau** : Lycée (Seconde/Première)
**Destination** : ./animations/vecteurs-plan/

## Description détaillée

Animation interactive permettant de visualiser et manipuler des vecteurs dans un repère orthonormé. L'utilisateur peut créer des vecteurs, les additionner, les soustraire, calculer leur produit scalaire et observer les propriétés géométriques associées.

## Éléments graphiques requis

- Repère orthonormé avec grille
- Vecteurs représentés par des flèches colorées
- Points origine et extrémité avec labels (A, B, etc.)
- Vecteur somme/différence en couleur distincte
- Projection orthogonale (optionnel)
- Angle entre vecteurs avec arc

## Paramètres contrôlables

| Paramètre | Type | Plage | Défaut | Description |
|-----------|------|-------|--------|-------------|
| vec1_x | range | -5 à 5 | 2 | Composante x du vecteur u |
| vec1_y | range | -5 à 5 | 1 | Composante y du vecteur u |
| vec2_x | range | -5 à 5 | 1 | Composante x du vecteur v |
| vec2_y | range | -5 à 5 | 2 | Composante y du vecteur v |
| operation | select | add/sub/scal | add | Opération à visualiser |
| showProjection | checkbox | - | false | Afficher la projection |
| showAngle | checkbox | - | true | Afficher l'angle |

## Informations à afficher

- Coordonnées de u et v
- Norme de chaque vecteur
- Produit scalaire u·v
- Angle entre u et v (en degrés)
- Coordonnées du vecteur résultat

## Scénarios pédagogiques

### Scénario 1 : Découverte (basique)
- Étape 1 : Présentation du repère et des axes
- Étape 2 : Création d'un premier vecteur u
- Étape 3 : Lecture des coordonnées
- Étape 4 : Calcul de la norme

### Scénario 2 : Addition (intermédiaire)
- Étape 1 : Deux vecteurs u et v
- Étape 2 : Construction de u + v par la règle du parallélogramme
- Étape 3 : Vérification par les coordonnées
- Étape 4 : Propriété de commutativité

### Scénario 3 : Produit scalaire (avancé)
- Étape 1 : Définition géométrique (projection)
- Étape 2 : Cas où u·v > 0 (angle aigu)
- Étape 3 : Cas où u·v < 0 (angle obtus)
- Étape 4 : Cas où u·v = 0 (orthogonalité)

## Contraintes techniques

- Utiliser MathUtils.vec2* pour tous les calculs vectoriels
- Gérer le cas des vecteurs nuls (éviter division par zéro pour norme)
- Arrondir les angles affichés à 1 décimale

## Notes pédagogiques

- Insister sur la différence entre vecteur et point
- Montrer que u + v = v + u visuellement
- L'orthogonalité (produit scalaire nul) est un cas important à mettre en évidence
```

## Important

- **Ne pas créer l'animation toi-même** : déléguer à l'agent
- **Être exhaustif** dans le prompt structuré
- **Anticiper les besoins pédagogiques** même non explicités
- **Proposer des scénarios pertinents** selon le niveau
