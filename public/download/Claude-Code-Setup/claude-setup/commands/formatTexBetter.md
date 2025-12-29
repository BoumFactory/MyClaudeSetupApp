# /formatTexBetter.md - Edition de documents LaTeX avec présentation compacte

## Description

Adapte automatiquement un document latex existant en optimisant l'espace et en adoptant une prsentation la plus rigoureuse possible.

## Cadre d'intervention

Tu devra créer un document avec les skills appropriés.

L'écriture de code latex se passe seulement pour le code dans un document déjà construit.

Ton travail consiste à optimiser l'espace dédié au contenu sur chaque page.

Le workflow itératif que je te demande d'adopter te permettra de livrer un produit fini directement utilisable en classe.

## Skills

Tu utiliseras à fond le skill 'bfcours-latex' pour l'implémentation de documents latex.

Tu utiliseras à fond le skill 'pdf' pour analyser l'output et voir les points d'amélioration.

Tu utiliseras le skill 'tex-compiling-skill' pour compiler le document modifié et en corriger les erreurs, ou en optimisant davantage l'espace.

## Exemples contextualisés disponibles

Dans le dossier ".claude\skills\bfcours-latex\assets\usecase" se trouvent des dossier contenant des projets latex complets qui sont entrés en production.

Selon le type de tâche d'optimisation, tu dois pouvoir lire les 'enonce.tex' de ces projets de sorte à repérer comment l'espace a été optimisé ( attention ce sont parfois des fichiers atomiques. )

## Workflow

Déjà, sache que tu as accès à un certain nombre d'exemples d'utilisation complets dans les sous répertoires de ."claude\skills\bfcours-latex\assets\usecase" et qu'il faut en lire certains quand tu as besoin de voir comment optimiser l'utilisation de l'espace.

1. Lire la source que l'utilisateur veut adapter.
2. Utiliser le skill 'pdf' pour extraire les images de chaque page.
3. Faire une todolist pour chaque page de l'optimisation que l'on peut gagner sans changer le contenu.
4. Utiliser le skill bfcours-latex pour modifier le code latex du fichier enonce.tex de sorte à optimiser l'espace tout en étant très facile à lire. Ceci consistera sans doute à réorganiser avec des MultiColonnes ou tcbenumerate bien placés avec le bon nombre de colonnes. C'est un peu fastidieux mais très satisfaisant.
5. Utiliser ton skill tex-compiling-skill pour compiler le fichier maître du projet créé. Attention, tes modifications avec vont inclure des tcbraster qui nécessitent 2 passes avant de se stabiliser donc lance deux compilations.

Ce procédé doit être itératif et tu dois pouvoir améliorer pour que le document soit impeccable.

**critical** : A la fin de ton intervention, nettoie les fichier intermédiaires non nécessaires pour ne pas créer de bazar dans les dossiers de l'utilisateur.
