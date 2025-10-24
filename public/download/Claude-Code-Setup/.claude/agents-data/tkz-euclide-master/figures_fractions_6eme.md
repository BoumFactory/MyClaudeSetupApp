# Figures TikZ pour Addition/Soustraction de Fractions - 6ème

## Nouvelles figures créées : FRAJ et FRAK

### FRAJ : Addition de fractions avec dénominateurs différents
**Objectif pédagogique** : Visualiser concrètement l'addition 1/2 + 1/3 = 5/6

**Éléments techniques** :
- Rectangles divisés pour représenter les fractions
- Transformation visuelle : 1/2 → 3/6 et 1/3 → 2/6
- Code couleur cohérent : defi!60 (bleu) pour 1/2, prop!60 (vert) pour 1/3
- Progression verticale : fractions originales → transformations → résultat
- Encadré récapitulatif orange avec la formule complète
- Annotations pédagogiques avec flèches explicatives

**Innovation technique** :
- Utilisation de `\foreach` pour divisions automatiques des rectangles
- Coordonnées calculées pour alignement parfait
- Combinaison de couleurs dans le résultat final (3 parts bleues + 2 parts vertes)

**Compétences ciblées** :
- Addition de fractions à dénominateurs différents (niveau CM2/6ème)
- Fractions équivalentes et dénominateur commun
- Représentation géométrique des fractions

### FRAK : Méthode en 4 étapes pour additionner des fractions
**Objectif pédagogique** : Schéma procédural clair pour la méthode générale

**Éléments techniques** :
- 4 cadres colorés distincts pour chaque étape
- Progression logique : Identifier → Dénominateur commun → Transformer → Additionner
- Code couleur pédagogique :
  - ÉTAPE 1 : defi (bleu) - Identification
  - ÉTAPE 2 : prop (vert) - Dénominateur commun  
  - ÉTAPE 3 : orange - Transformation
  - ÉTAPE 4 : red - Addition finale
- Formules génériques avec variables a, b, c, d
- Exemple concret en encadré jaune : 1/2 + 1/3
- Annotations avec flèches pour les dénominateurs

**Innovation technique** :
- Cadre global prop!5 pour unifier visuellement
- Rounded corners pour esthétique moderne
- Combinaison texte/formules mathématiques
- Mise en évidence de l'exemple concret

## Intégration au système d'indexation

**Codes utilisés** :
- **FRAJ** : Addition avec dénominateurs différents (illustration concrète)
- **FRAK** : Méthode générale en 4 étapes (diagramme procédural)

**Cohérence stylistique** :
- Respect des couleurs bfcours : defi, prop, orange, red
- Épaisseurs uniformes : thick pour contours principaux
- Tailles cohérentes avec les autres figures du cours
- Annotations pédagogiques systématiques

## Utilisation recommandée

### Dans la séquence pédagogique
1. **FRAJ** : Après introduction des fractions équivalentes, pour illustrer concrètement
2. **FRAK** : Comme mémo-méthodologie, à afficher en permanence

### Différenciation
- **FRAJ** : Élèves visuels, besoin de manipulation concrète
- **FRAK** : Élèves logiques, besoin de procédures structurées

### Compilation
- Figures testées et validées
- Compatible LuaLaTeX
- Rendu vectoriel haute qualité
- Temps de compilation optimisé

## Code source
- 140+ lignes ajoutées au fichier enonce_figures.tex
- Documentation interne complète
- Maintenabilité assurée par structure modulaire
- Intégration harmonieuse aux 9 figures existantes