# Exemples d'Utilisation Professionnels BFCours

Ce fichier pointe vers les exemples réels d'utilisation de bfcours situés dans `.claude\agents-data\usecase\`.

## Organisation des Exemples

Les exemples sont organisés en dossiers représentant chacun une partie de la séquence sur les polynômes :

- **Cours** : Exemples complexes et atomiques
- **Cours Partie 2** : Exemples moins complexes et non atomiques
- **Exercices** : Exercices pour chaque partie
- **Évaluation** : Exemples d'évaluations
- **Devoir Maison** : Exemples de DM
- **TD Spécifique** : Travaux dirigés

## Comment Utiliser ces Exemples

**IMPORTANT** : Ne pas lire les fichiers complets. Utiliser Grep pour chercher des patterns spécifiques.

### Recherche par Environnement

Pour trouver des exemples d'utilisation d'un environnement spécifique :

```
Grep: pattern="\\begin{Definition}" path=".claude/agents-data/usecase" output_mode="content"
Grep: pattern="\\begin{EXO}" path=".claude/agents-data/usecase" output_mode="content"
Grep: pattern="\\begin{MultiColonnes}" path=".claude/agents-data/usecase" output_mode="content"
```

### Recherche par Type de Contenu

Pour trouver des exemples de contenu spécifique :

```
# Exemples de tableaux
Grep: pattern="\\begin{tcbtab}" path=".claude/agents-data/usecase" output_mode="content" -A=10

# Exemples d'énumérations
Grep: pattern="\\begin{tcbenumerate}" path=".claude/agents-data/usecase" output_mode="content" -A=10

# Exemples d'espaces réponses
Grep: pattern="\\begin{crep}" path=".claude/agents-data/usecase" output_mode="content" -A=5

# Exemples de figures TikZ
Grep: pattern="\\tikzfig" path=".claude/agents-data/usecase" output_mode="content"

# Exemples d'exercices avec points
Grep: pattern="\\tcbitempoint" path=".claude/agents-data/usecase" output_mode="content" -A=3
```

### Recherche par Niveau de Complexité

```
# Cours complexe et atomique
Read: ".claude/agents-data/usecase/[dossier_cours]/*.tex"

# Cours simple et non atomique
Read: ".claude/agents-data/usecase/[dossier_cours_partie2]/*.tex"

# Exercices avec corrections détaillées
Grep: pattern="\\exocorrection" path=".claude/agents-data/usecase" output_mode="content" -A=20
```

## Bonnes Pratiques

1. **Sélectionner ce qui vous concerne** : Ne lire que les parties pertinentes pour votre tâche actuelle

2. **Utiliser Grep en priorité** : Pour des recherches ciblées et efficaces

3. **Lire des fichiers spécifiques** : Seulement après avoir identifié le bon fichier via Grep

4. **Analyser la structure** : Observer comment les professionnels organisent le contenu

5. **Reproduire les patterns** : Adapter les structures trouvées à votre contexte

## Chemin Complet

Tous les exemples se trouvent dans :
```
C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\.claude\skills\assets\usecase\
```

Utiliser ce chemin pour les recherches Grep et les lectures Read.
