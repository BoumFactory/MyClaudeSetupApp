---
name: adaptTex
description: Skill spécialisé pour adapter n'importe quel document avec les conventions bfcours-latex ( de préférence source .tex ).
---

# /adaptTex - Adaptation conceptuelle de documents LaTeX vers bfcours

## Description

Adapte automatiquement un document existant au format LaTeX utilisant les environnements et conventions du package bfcours, en adoptant une **approche conceptuelle** : les environnements sont mappés selon leur **rôle pédagogique** plutôt que leur nom syntaxique.

## Cadre d'intervention

Le contenu adapté est écrit dans un document déjà construit (ou créé avec le skill `tex-document-creator`). Si le fichier est destiné à être inclus (`\input`) dans un document maître, il faut filtrer les éléments de préambule et de page de titre (auteur, chapitre, etc.), déjà gérés par le document maître.

## Skills

- `tex-document-creator` : initialisation du projet LaTeX.
- `bfcours-latex` : rédaction du contenu avec les environnements du package.
- `tex-compiling-skill` : compilation et diagnostic des erreurs.
- Lecture du PDF produit (skill ou outil de lecture de PDF disponible) pour vérifier la présentation.

## Philosophie de la commande

**PRINCIPE FONDAMENTAL** : Au lieu de transformer "nom d'environnement → nom d'environnement", on transforme "**concept pédagogique** → **environnement bfcours**".

Par exemple :

- Tous les environnements qui représentent une **définition** (peu importe leur nom : `definition`, `def`, `defi`, etc.) → `Definition` (bfcours)
- Tous les environnements qui représentent un **exercice** (peu importe leur nom : `exercise`, `exer1`, `exo`, etc.) → `EXO` (bfcours)
- Toutes les **listes énumérées** → `tcbenumerate`
- Toutes les **listes à puces** → `MultiColonnes{2}` pour compacter la mise en page.

**Principe fondamental des exercices** : Tous les exercices doivent avoir une correction.
La tâche te revient donc d'implémenter les solutions des exercices si elles ne sont pas présentes.

## Usage

```
/adaptTex <chemin_fichier_source> [--output <chemin_sortie>] [--backup]
```

## Paramètres

- `<chemin_fichier_source>` : Fichier .tex à adapter (obligatoire)
- `--output <chemin_sortie>` : Fichier de sortie (optionnel, défaut: `<source>_modified.tex`)
- `--backup` : Créer une sauvegarde du fichier original (optionnel, défaut: true)
- `--crep` : Insérer des espaces réponse après les questions. (optionnel, défaut: false)
  On utilisera \begin{crep} contenu \end{crep} pour les gros environnements de réponse ; \repsim[xcm]{contenu} pour les réponses inline de longueur fixe ( souvent pour les toutes petites réponse ) ; \tcfillcrep{contenu} pour les réponses inline de longueur autoadaptable ( occupe tout l'espace disponible ).

## Workflow

1. Lire la source que l'utilisateur veut adapter.
2. Initier un projet en utilisant le skill tex-document-creator.
3. Implémenter le contenu directement dans l'énoncé avec le skill bfcours-latex.
4. Implémenter les éventuels autres documents annexes nécessaires.
5. Utiliser le skill tex-compiling-skill pour compiler le fichier maître du projet créé.
6. Si le document ne compile pas, corriger les erreurs avec le skill bfcours-latex jusqu'à ce que le fichier compile.
7. Vérifier le PDF : le document est correct, les figures sont bien affichées et les informations données dessus sont correctes.
8. Si des erreurs ou des modifications sont à faire, corriger, recompiler, puis vérifier à nouveau.
9. Annoncer à l'utilisateur que la tâche est terminée et demander s'il faut produire un document d'explication pédagogique dédié (et sous quel format). Attendre jusqu'à ce que l'utilisateur réponde.
