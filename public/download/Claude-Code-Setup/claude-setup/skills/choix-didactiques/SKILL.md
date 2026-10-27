---
name: choix-didactiques
description: Choix didactiques par défaut pour tout document destiné aux élèves (cours, fiche d'exercices, évaluation, questionnaire de réactivation, interrogation, activité). À charger systématiquement pendant la rédaction ou la relecture d'un document élève, en complément du skill bfcours-latex (LaTeX) ou bfcours-typst (Typst). Ce skill ne traite jamais de mise en forme (environnements, couleurs, colonnage) : uniquement des choix de fond pédagogique (échéances, construction des exemples et jeux de données, symétrie énoncé/correction, format de fiche, notation). Utiliser dès que l'utilisateur demande un cours, une fiche d'exercices, une évaluation, un questionnaire ou une interro pour ses élèves, ou dès qu'on relit un document élève déjà rédigé.
---

# Choix didactiques par défaut

Ce skill rassemble les choix didactiques par défaut de l'enseignant, à appliquer sans qu'il ait besoin de les repréciser à chaque document. Il complète `bfcours-latex` et `bfcours-typst` (qui régissent la forme) en couvrant le fond pédagogique : ce que le document demande à l'élève de faire, comment un exemple ou une donnée est construit, comment une fiche est pensée pour l'usage réel en classe.

**Ne contient aucune règle de mise en forme pure** (environnements, couleurs, colonnage, espacement...) : celles-ci restent dans `bfcours-latex` et `bfcours-typst`.

## Quand l'invoquer

Systématiquement pendant la rédaction ou la relecture de tout document destiné aux élèves : cours, fiche d'exercices, évaluation, questionnaire de réactivation, interrogation, activité. Dans le workflow `/latex`, ce skill s'invoque à l'étape 2 (rédaction du contenu), en complément de `bfcours-latex` : avant d'écrire l'énoncé, l'exemple ou la correction d'un exercice, pas après.

## Règles par défaut

### Échéance de matériel : « dès que possible », jamais une date lointaine

Quand un document demande à l'élève d'apporter un matériel (calculatrice, équerre, ordinateur, clé USB...), fixer l'échéance à **dès que possible**, jamais une date future précise.

**Pourquoi** : une échéance lointaine donne à l'élève la permission implicite de repousser, sans aucune pression douce à s'organiser tout de suite. « Dès que possible » ne fixe pas de sanction mais élimine l'excuse du délai.

### Conclusions et interprétations d'un exemple de cours : à écrire par l'élève

Dans un environnement `Exemple` de cours, ne jamais imprimer la conclusion ou l'interprétation finale (ce que le résultat signifie, ce qu'on en déduit). Laisser une zone seyes vierge (`crep`) que l'élève complète pendant le cours.

**Pourquoi** : rédiger soi-même la conclusion d'un exemple est l'exercice minimal de synthèse ; l'imprimer prive l'élève d'un des seuls moments actifs du cours magistral. Une zone à compléter transforme la lecture passive en vérification active.

### Jeu de données d'exemple : éviter les coïncidences numériques trompeuses

Choisir les valeurs numériques d'un exemple ou d'un exercice de façon à ce qu'aucune coïncidence n'oriente l'élève vers une fausse explication. Exemple : dans un exercice sur l'indépendance en probabilités, ne pas donner des effectifs de filles et de garçons égaux : un élève pourrait conclure à l'indépendance par symétrie apparente des effectifs, sans avoir vérifié $P(A \cap B) = P(A) \times P(B)$.

**Pourquoi** : une coïncidence numérique donne une explication fausse mais plausible, qui contourne l'outil mathématique visé. L'élève doit être forcé de passer par le calcul, jamais par un raccourci visuel.

### Fiche courte à photocopier : deux exemplaires par A4

Quand un document est une fiche courte (une demi-page ou moins de contenu réel : mémo, aide-mémoire, carte de références), la composer en **deux exemplaires identiques sur une même page A4**, séparés par une ligne de découpe.

**Pourquoi** : une fiche courte imprimée seule sur une page A4 gaspille du papier et incite à la jeter ; deux exemplaires par feuille permettent de distribuer aux binômes ou de garder une réserve, sans surcoût de tirage.

## Préférences didactiques générales

Les règles suivantes s'appliquent par défaut à tout document élève et ne doivent pas être contredites sans demande explicite de l'utilisateur.

### Probabilités conditionnelles : donner au moins une intersection dans l'énoncé

Ne jamais fournir toutes les données déjà au format conditionnel dans un arbre pondéré ou un tableau croisé. Donner au moins une probabilité sous forme d'**intersection** (« $y~\%$ des pièces proviennent de $M_2$ **et** sont défectueuses ») pour que l'élève retrouve lui-même $P_{M_2}(D) = P(M_2 \cap D)/P(M_2)$ avant de compléter l'arbre : c'est l'automatisme visé par le programme, pas le report mécanique d'un poids de branche déjà donné.

### Justifier une consigne par ce qu'elle permet, pas par ce qu'elle évite

Formuler une règle ou une consigne dans un document élève par son bénéfice (ce qu'elle rend possible), jamais par le risque qu'elle prévient : un cadrage défensif installe une image de suspicion là où il faudrait un service rendu. Trancher aussi une convention plutôt que de la présenter en option (« si vous dépassez neuf chapitres... ») : un document prescriptif choisit, il ne laisse pas l'élève arbitrer.

### Point final dans un item de liste : seulement si c'est une phrase

Un item de liste (exercice, correction) prend un point final seulement s'il est rédigé comme une phrase (consigne, explication). Une expression mathématique nue (`$2^{12}$`, un unique groupe `$...$` sans texte autour) n'en prend jamais : le point s'y lit comme un symbole parasite.

### Corrections d'exercices : toujours projetées item par item, jamais compactées

Les corrections d'EXO (entre `\exocorrection` et la fin) sont projetées en classe item par item : les garder ultra aérées, mono-colonne, sans densification, pour ne jamais révéler à l'écran la réponse suivante avant que l'enseignant ne l'aborde. À l'inverse, densifier librement les énoncés (colonnage, `tcbenumerate`) : c'est là qu'on gagne de la place.

### Exercices d'une séquence : deux fiches distinctes, application et approfondissement

Une séquence produit systématiquement deux fiches d'exercices autonomes : une fiche d'**application** (une seule propriété/méthode par exercice, proche des exemples du cours, faisable en autonomie) et une fiche d'**approfondissement** (plusieurs notions enchaînées, démonstration, initiative), jamais une fiche unique où la difficulté progresse par section.

### Questionnaires de réactivation : propriétés utiles, jamais de définitions ni d'anecdotes

Un questionnaire de réactivation (post-vacances, courte durée) exclut les définitions formelles des objets et les anecdotes/valeurs approchées. Il muscle les automatismes algébriques nécessaires aux chapitres suivants : un calcul direct simple en ouverture, un panorama des propriétés/relations à compléter, des questions d'application, une clôture en calcul mental.

### Interrogations d'informatique : notées sur 10, jamais les scripts du carnet

Les interros et tests de connaissances d'informatique (Python, lycée) sont notés sur 10 même si la fiche source était notée sur 5 ; un item difficile est compté dans le total, jamais en bonus hors barème. Les scripts et valeurs de l'interro ne reprennent jamais ceux du carnet Jupyter de la même séance : on évalue le transfert, pas la mémoire d'un exemple.

### Supports d'activité : sobriété éditoriale assumée

Pour un paquet de supports liés à une activité (fiches élèves, badges, cartes, fiche prof), choisir la sobriété : un seul accent chromatique pour tout le paquet, structure portée par la typographie et des filets plutôt que par des aplats de couleur ou des boîtes titrées, à l'inverse du goût pour le coloré dans les environnements didactiques d'un cours. Un paquet d'activité doit se tenir ensemble et rester lisible une fois photocopié en noir et blanc ; distinguer les catégories par un marqueur segmenté (carrés pleins) plutôt que par la couleur.

## Rappel

Ce skill ne dicte jamais la mise en forme (environnements, couleurs, colonnage, espacement) : pour cela, se référer à `bfcours-latex` ou `bfcours-typst`. Il dicte uniquement des choix de fond : ce que le document demande à l'élève, comment les données ou exemples sont construits, comment un ensemble de documents est pensé pour l'usage réel en classe.
