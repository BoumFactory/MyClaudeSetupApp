---
name: programmes-officiels
description: Rechercher et citer précisément les éléments des programmes officiels de l'Éducation Nationale française (collège et lycée). Utiliser pour sourcer les compétences, capacités et contenus du programme dans les fiches pédagogiques et documents administratifs.
---

# Skill Programmes Officiels

Ce skill permet de rechercher et citer précisément les éléments des programmes officiels de l'Éducation Nationale française pour les mathématiques au collège et au lycée.

## Objectif

Fournir des références exactes et sourcées aux programmes officiels lors de la création de documents pédagogiques, notamment :
- Fiches techniques pour inspecteurs
- Documents de préparation de séquence
- Progressions annuelles
- Évaluations et leur justification

## Quand utiliser ce skill

Utiliser ce skill lorsqu'il faut :
- Identifier les compétences du programme liées à une notion mathématique
- Citer précisément un extrait du Bulletin Officiel (BO)
- Justifier les choix pédagogiques par référence aux textes officiels
- Vérifier qu'un contenu est conforme aux programmes en vigueur

## Comment utiliser ce skill

### 1. Recherche par niveau et thème

Pour trouver les éléments du programme :

1. Identifier le niveau concerné (6ème, 5ème, 4ème, 3ème, 2nde, 1ère spécialité, 1ère enseignement scientifique, Terminale spécialité, Terminale enseignement scientifique)
2. Consulter le fichier de référence correspondant dans `references/`
3. Localiser le thème mathématique (Nombres et calculs, Géométrie, Grandeurs et mesures, etc.)

### 2. Structure des programmes

Les programmes sont organisés selon :
- **Thèmes** : grandes catégories mathématiques
- **Attendus de fin d'année** : ce que l'élève doit savoir faire
- **Connaissances et compétences associées** : détail des notions
- **Exemples de situations, d'activités et de ressources** : suggestions pédagogiques

### 3. Citation dans les documents

Lors de la rédaction de fiches techniques ou documents administratifs :

```latex
% Format recommandé pour citer le BO
\textit{Programme officiel de [niveau] (BO n°[numéro] du [date]) :}

« [Citation exacte] »
```

### 4. Compétences du socle commun

Pour le collège, relier systématiquement aux compétences du socle commun de connaissances, de compétences et de culture :
- Domaine 1 : Les langages pour penser et communiquer
- Domaine 2 : Les méthodes et outils pour apprendre
- Domaine 4 : Les systèmes naturels et les systèmes techniques

## Fichiers de référence disponibles

Les programmes sont stockés dans le dossier `references/` :

- `college_cycle3.md` : Programmes de 6ème (cycle 3)
- `college_cycle4.md` : Programmes de 5ème, 4ème, 3ème (cycle 4)
- `seconde_generale.md` : Programme de 2nde générale et technologique
- `premiere_specialite.md` : Programme de 1ère spécialité mathématiques
- `premiere_enseignement_scientifique.md` : Programme de 1ère enseignement scientifique
- `terminale_specialite.md` : Programme de Terminale spécialité mathématiques
- `terminale_enseignement_scientifique.md` : Programme de Terminale enseignement scientifique
- `competences_socle_commun.md` : Compétences du socle commun (collège)

## Workflow type

1. **Identifier** le niveau et le thème de la ressource pédagogique
2. **Lire** le fichier de référence correspondant
3. **Extraire** les attendus et compétences pertinents
4. **Citer** précisément avec la référence du BO
5. **Relier** aux compétences du socle (si collège)

## Notes importantes

- Les programmes évoluent : vérifier la date du BO cité
- Pour les documents officiels (inspecteurs), privilégier les citations exactes entre guillemets
- Pour les documents entre collègues, reformulation possible mais garder la référence
- Les exemples d'activités dans les programmes sont indicatifs, pas obligatoires

## TODO : Compléter les références

Actuellement, les fichiers de référence doivent être complétés avec :
- Les textes officiels extraits des BO
- Les références précises (numéro de BO, date de publication)
- Les repères de progressivité entre niveaux
