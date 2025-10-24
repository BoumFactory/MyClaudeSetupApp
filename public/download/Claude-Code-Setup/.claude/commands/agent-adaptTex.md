# /adaptTex - Adaptation conceptuelle de documents LaTeX vers bfcours

## Description

Adapte automatiquement un document existant au format LaTeX utilisant les environnements et conventions du package bfcours, en adoptant une **approche conceptuelle** : les environnements sont mappés selon leur **rôle pédagogique** plutôt que leur nom syntaxique.

## Cadre d'intervention

Tu devra créer un document avec le skill approprié et le serveur mcp approprié.

L'écriture de code latex se passe seulement pour le code dans un document déjà construit.
Le fichier dans lequel tu écriras sera input dans un document maître possédant généralement le nom du dossier parent suivi de l'extension .tex

Il convient donc de filtrer les éléments de préambule ( déjà gérés ) et les éléments de présentation de page ( auteur, chapter etc qui sont déjà gérés par mes fichiers main )

## Skills

Tu utiliseras à fond le skill 'tex-document-creator' pour l'initialisation de projets latex.

Tu utiliseras à fond les agents latex-main-worker et latex-side-worker en les référent au skill bfcours-latex lorsque l'utilisateur demande une architecture atomique.

Tu utilises le skill 'bfcours-latex' pour la création de documents latex si l'utilisateur ne précise rien sur l'architecture atomique.

Tu utiliseras à fond le skill 'pdf' pour visualiser ta production et t'assurer que cela a bien la présentation escomptée.

## Philosophie de la commande

**PRINCIPE FONDAMENTAL** : Au lieu de transformer "nom d'environnement → nom d'environnement", on transforme "**concept pédagogique** → **environnement bfcours**".

Par exemple :

- Tous les environnements qui représentent une **définition** (peu importe leur nom : `definition`, `def`, `defi`, etc.) → `Definition` (bfcours)
- Tous les environnements qui représentent un **exercice** (peu importe leur nom : `exercise`, `exer1`, `exo`, etc.) → `EXO` (bfcours)
- Toutes les **listes énumérées** → `tcbenumerate`
- Toutes les **listes à puces** → `MultiColonnes{2}` pour compacter la mise en page.

**Principe fondamental des exercices** : Tous les exercices doivent avoir une correction.
La tâche te reviens donc d'implémenter les solutions des exercices si elles ne sont pas présentes.

## Principe de structure LaTeX atomique

Dans un projet LaTeX, créer dans le sous répertoire sections des dossiers destinés à contenir les différents fichiers atomiques.
Ces atomes de contenu LaTeX seront injectés dans le corps du contenu situé dans enonce.tex

Exemple :
Pour adapter un document qui va contenir 3 définitions, 2 propriétés et 5 exercices, créer 3 dossiers : 'Definition', 'Propriete' et 'Exercices' dans lesquels tu peupleras avec 3 fichier distincts pour les définitions ( un pour chaque définition ) et de même pour les propriétés ( 2 ) et les exercices ( 5 ).

Tu lancera un agent latex-side-worker par atome voulu.

Tu es responsable d'organiser les atomes produits dans le enonce.tex puisque tu les as commandé aux agents.

**critical** : Sois explicite avec les agents side qui seront des scripteurs sans réflexion. Tu leur donne soit les numéro de lignes à lire, soit la procédure exacte pour pouvoir accéder au contenu facilement, soit un prompt ultra détaillé de ce que tu lui demande de mettre en forme. Dans tous les cas tu les envoie sur une tâche précise.

## Principe d'auto-amélioration

Ajoute des informations à tes agents 'latex-side-worker' de sorte à prendre en compte les remarques de l'utilisateur sur ce qui ne va pas dans les documents.

**critical** Toujours demander à l'utilisateur de formuler des choses à modifier qui ne vont pas dans le rendu en explicitant que tu modifieras alors le document sur lequel tu travaillais et ensuite modifier les agents latex-side-worker pour que les itérations futures tiennes compte de ces contraintes.

## Usage

```
/adaptTex <chemin_fichier_source> [--output <chemin_sortie>] [--backup]
```

## Paramètres

- `<chemin_fichier_source>` : Fichier .tex à adapter (obligatoire)
- `--output <chemin_sortie>` : Fichier de sortie (optionnel, défaut: `<source>_modified.tex`)
- `--atomic` : Produire un contenu latex atomique (optionnel, défaut: false)
- `--backup` : Créer une sauvegarde du fichier original (optionnel, défaut: true)
- `--crep` : Insérer des espaces réponse après les questions. (optionnel, défaut: false)
  On utilisera \begin{crep} contenu \end{crep} pour les gros environnements de réponse ; \repsim[xcm]{contenu} pour les réponses inline de longueur fixe ( souvent pour les toutes petites réponse ) ; \tcfillcrep{contenu} pour les réponses inline de longueur autoadaptable ( occupe tout l'espace disponible ).

## Workflow

1. Lire la source que l'utilisateur veut adapter.
2. Initier un projet en utilisant ton skill tex-document-creator.
3. Utiliser des agents .claude\agents\latex-side-worker.md en leur disant d'utiliser le skill bfcours-latex pour implémenter le code latex de la ressource au format atomique. Chaque agent aura a charge une partie clairement identifiée à reproduire. **voir architecture latex atomique**
4. Implémenter les éventuels autres documents annexes nécessaires.
5. Utiliser ton skill tex-compiling-skill pour compiler le fichier maître du projet créé.
6. Si le document ne compile pas tu réutilise ton skill bfcours-latex en modifiant les erreurs jusqu'à ce que le fichier compile.
7. Utilise ton skill pdf pour vérifier que le document est correct, que les figures sont bien affichées et que les informations données dessus sont correctes.
8. Si tu repères des erreurs ou qu'il y a des modifications à faire, reviens à ton skill bfcours-latex pour corriger les erreurs, puis recompiler avec le skill tex-compiling-skill, puis vérification avec le skill pdf.
9. Si tu remarque des erreurs fréquentes à éviter dans les agents side-worker, corrige leur prompt situé : .claude\agents\latex-side-worker.md
10. Annoncer à l'utilisateur que la tache est terminée et demander s'il faut produire un document d'explication pédagogique dédié ( et sous quel format). Attendre jusqu'à ce que l'utilisateur réponde.
