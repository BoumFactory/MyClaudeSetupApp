---
name: grill-me
description: Interview serrée pour affiner un plan, une idée, un design ou une décision, par manches de questions à choix (dans le terminal, ou sur une page HTML cliquable avec dictée vocale). Déclencheurs : « grill-me », « grille-moi », « cuisine-moi », « challenge mon plan », « pose-moi des questions avant de te lancer », « interroge-moi », et l'appel par wayfinder.
---

# Grill-me

Interroge l'utilisateur sans relâche jusqu'à atteindre une compréhension partagée. Le plan est un **arbre de décisions** : chaque décision se ramifie en décisions qui en dépendent.

## Étape 0 : choisir le mode

Quelle que soit la demande, la toute première action est un appel à `AskUserQuestion` qui demande le mode de questionnement :

- **Terminal** : questions à choix directement dans le terminal.
- **Page HTML** : la manche complète s'affiche dans une page cliquable, avec dictée vocale et copie des réponses.

Le mode choisi vaut pour toute la session. L'utilisateur peut en changer à tout moment.

## La méthode

Travaille l'arbre par **manches**.

- La **frontière** est l'ensemble des décisions dont les prérequis sont réglés, c'est-à-dire les questions posables *maintenant* sans deviner des réponses pas encore entendues.
- Pose **toute la frontière** à chaque manche. N'attends pas la réponse à une question pour poser les autres.
- Une question qui dépend d'une autre question encore ouverte va à la **manche suivante**, pas à celle-ci.
- Chaque question porte des **options concrètes** et une **recommandation argumentée**. Une question n'est ouverte (`libre`) que si aucune option sensée n'existe.
- Après chaque manche, les réponses règlent des décisions, poussent la frontière vers l'extérieur et débloquent les questions qui en dépendaient. Recalcule la frontière et pose la manche suivante.

**Les faits se cherchent soi-même.** Quand une question de la frontière demande un fait de l'environnement (fichiers, outils, état du projet), lance un sous-agent pour le trouver. Ne demande jamais à l'utilisateur ce que tu peux vérifier. N'attends pas le sous-agent : une exploration en cours est un prérequis non réglé, donc seules les questions qui en dépendent attendent son résultat. Pose le reste de la frontière tout de suite.

**Les décisions appartiennent à l'utilisateur.** Tu cherches les faits, il tranche les décisions. Chaque décision lui est posée explicitement, et tu attends sa réponse.

**Fin de session** : quand la frontière est vide, chaque branche de l'arbre a été visitée et rien n'est resté implicite.

## Mode Terminal

Chaque manche passe par `AskUserQuestion` :

- Au plus **4 questions par appel**. Si la frontière en compte davantage, enchaîne plusieurs appels dans la même manche.
- **2 à 4 options** par question.
- L'option recommandée vient **en premier**, avec « (Recommandé) » à la fin du libellé.
- `multiSelect: true` quand plusieurs choix peuvent se combiner.
- `header` de **12 caractères maximum**.
- Une description courte par option, qui dit la **conséquence** du choix.
- L'utilisateur dispose toujours de « Other » pour répondre librement.
- Pas de pavé de questions en texte brut dans le chat.

## Mode Page HTML

Pour chaque manche :

1. **Écrire la manche en Markdown** dans le scratchpad de la session, dans le fichier `manche-01.md`, puis `manche-02.md`, etc. Lis `.claude/skills/grill-me/references/format-manche.md` avant la première manche. Un exemple se trouve dans `.claude/skills/grill-me/assets/exemple-manche.md`. Rappel du format :
   - front-matter avec `titre:` et `contexte:` ;
   - une section `## Q1 — Titre` par question ;
   - une ligne `type: unique|multiple|libre` ;
   - le corps de la question en Markdown ;
   - une ligne `reco: …` ;
   - la liste des options, au format `- [reco] Libellé : description`.

2. **Lancer la page** :
   ```
   PYTHONIOENCODING=utf-8 python ".claude/skills/grill-me/scripts/manche_html.py" "<scratchpad>/manche-01.md"
   ```
   - La page s'ouvre en `http://127.0.0.1:47821/<nom>.html` via un petit serveur local (`scripts/serveur_pages.py`) qui démarre seul, ne sert que `%TEMP%/grill-me-pages/` et s'arrête après 3 h sans requête. L'origine étant stable, Chrome ne demande l'autorisation du micro qu'une seule fois. Port surchargeable par `GRILL_ME_PORT`.
   - `--fichier-local` : ancien mode, ouverture en `file://` (le micro est alors redemandé à chaque fois). C'est aussi le repli automatique si le serveur échoue.
   - `--pas-ouvrir` : génère (et copie dans `%TEMP%/grill-me-pages/`) sans ouvrir le navigateur.
   - `--sortie <fichier>` : choisit le fichier HTML produit.
   - Micro : bouton orange « démarrage… » puis rouge « à l'écoute, parlez ». Alternative sans autorisation : dictée Windows (Win + H).

3. **Annoncer en une ligne** que la page est ouverte, puis **attendre**. L'utilisateur répond au clic (mode focus, raccourcis 1 à 9, micro par question), clique sur « Copier les réponses » et colle le texte dans le chat.

4. **Lire les réponses.** Le format est `Q1 — titre : choix (recommandé)`, suivi de commentaires en `>`. Une réponse `NON RÉPONDU` signale une question à reposer, ou à trancher par défaut après confirmation de l'utilisateur.

5. **Recalculer la frontière** et préparer la manche suivante.

**Ne génère jamais de HTML à la main.** Seul le fichier `.md` change d'une manche à l'autre. Cela économise des tokens.

## Clôture

Quand la frontière est vide :

1. Présente un **récapitulatif compact** des décisions, une ligne par décision.
2. **Demande confirmation** de la compréhension partagée. Signale les points restés par défaut, s'il y en a.
3. Seulement après confirmation : agis, ou passe la main (par exemple à wayfinder).

Ne rien faire avant cette confirmation.
