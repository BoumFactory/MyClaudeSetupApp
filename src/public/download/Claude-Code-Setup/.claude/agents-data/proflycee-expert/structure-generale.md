# Structure générale du package ProfLycee

## Architecture des fichiers

Le package ProfLycee est organisé en plusieurs fichiers modulaires :

### Fichiers principaux
- `ProfLycee.sty` : fichier principal du package
- `ProfLycee-Light.sty` : version allégée
- `ProfLycee-Pictosbac.sty` : pictogrammes pour le bac

### Modules spécialisés (fichiers .tex)
- `proflycee-tools-aleatoire.tex` : outils pour l'aléatoire
- `proflycee-tools-analyse.tex` : outils d'analyse mathématique
- `proflycee-tools-arithm.tex` : arithmétique
- `proflycee-tools-cliparts.tex` : cliparts et images
- `proflycee-tools-competences.tex` : compétences mathématiques
- `proflycee-tools-complexes.tex` : nombres complexes
- `proflycee-tools-ecritures.tex` : écritures mathématiques
- `proflycee-tools-espace.tex` : géométrie dans l'espace
- `proflycee-tools-exams.tex` : outils pour examens
- `proflycee-tools-geom.tex` : géométrie plane
- `proflycee-tools-graphiques.tex` : graphiques et repères
- `proflycee-tools-listings.tex` : intégration listings
- `proflycee-tools-minted.tex` : intégration minted
- `proflycee-tools-piton.tex` : intégration piton
- `proflycee-tools-probas.tex` : probabilités et statistiques
- `proflycee-tools-pythontex.tex` : intégration PythonTeX
- `proflycee-tools-recreat.tex` : mathématiques récréatives
- `proflycee-tools-stats.tex` : statistiques
- `proflycee-tools-suites.tex` : suites numériques
- `proflycee-tools-trigo.tex` : trigonométrie

## Philosophie du package

ProfLycee vise à fournir des outils LaTeX spécifiquement conçus pour l'enseignement des mathématiques au lycée français, en respectant :

1. **Conformité aux programmes** : adaptation au référentiel officiel
2. **Facilité d'usage** : syntaxe simple et intuitive
3. **Qualité typographique** : rendu professionnel
4. **Modularité** : chargement sélectif des modules selon les besoins
5. **Compatibilité** : intégration avec les packages existants

## Conventions de nommage

- Préfixe `PL` pour les commandes internes
- Préfixe `Prof` pour les commandes utilisateur principales
- Majuscules pour les environnements
- CamelCase pour les commandes composées

## Dépendances principales

Le package s'appuie sur :
- TikZ/PGF pour les graphiques
- xcolor pour les couleurs
- amsmath/amssymb pour les mathématiques
- tcolorbox pour les boîtes colorées
- listofitems pour les listes
- xstring pour la manipulation de chaînes