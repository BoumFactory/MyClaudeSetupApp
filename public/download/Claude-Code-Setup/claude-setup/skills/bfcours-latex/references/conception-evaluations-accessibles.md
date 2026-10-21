# Concevoir une évaluation accessible en bfcours

À charger **avant de rédiger ou de remanier une évaluation** (DS, contrôle, interro, sujet type bac). Ce fichier traduit en gestes d'écriture bfcours les principes Éduscol 2026 « Rendre les mathématiques accessibles pour tous ». L'analyse complète d'un sujet existant (grille, captures, rapport) relève du skill `audit-accessibilite-eval`, dont `references/referentiel-eduscol.md` contient la source détaillée et les codes d'obstacles cités ici (MF, AL, ST…).

Le fichier se termine par les **retours de l'enseignant**, qui priment sur les principes généraux : lis-les avant d'écrire.

## Le principe qui commande tout

Un obstacle est **ce qui peut faire échouer l'élève pour une raison étrangère à l'objectif évalué** : un mot inconnu, une mise en page coûteuse, une recopie, une question qui dépend d'un résultat raté plus haut, une compétence clandestine. La difficulté qui *est* l'objectif n'est pas un obstacle : on ne la retire pas.

D'où l'ordre de rédaction : écrire d'abord, en commentaire en tête d'exercice, l'**objectif** et les **critères de réussite** ; rédiger ensuite l'énoncé en se demandant, phrase par phrase, ce qu'elle exige qui n'est pas dans cette liste.

```latex
% EXERCICE 3 - Arbre pondéré (5 points)
%  Objectif : construire un arbre pondéré et appliquer la règle des chemins.
%  Critères : poids du 1er niveau ; poids conditionnels ; règle des noeuds ;
%             produit le long d'un chemin.
%  Hors objectif (donc fourni) : la traduction des phrases en événements.
```

## Énoncé : lisibilité

| Principe | En bfcours | Code |
|---|---|---|
| Une consigne = une action | Un `\tcbitem` par verbe d'action ; jamais « calculer … puis dire si … » dans un même item quand les deux sont notés | ST1 |
| Verbe de consigne exact | `\acc{Placer}` (approximatif) ≠ `\acc{Construire}` (instruments) ; `\acc{Calculer}` ≠ `\acc{Justifier}` ; accentuer le verbe **et** la forme de réponse attendue | AL3 |
| Pas de mot hors objectif | Un terme de vocabulaire non évalué se remplace par un mot courant ou se définit **avant** la question qui l'utilise, pas après | AL1 |
| Phrases courtes, une donnée par phrase | Un pourcentage par phrase dans un contexte ; les événements définis en liste (`\textbullet` ou `tcbenumerate`) plutôt que dans une phrase | AL2 |
| Texte aligné à gauche, sans césure dans les paragraphes d'énoncé longs | Les colonnes étroites de `MultiColonnes` multiplient les césures | MF5 |
| Supports à l'endroit où l'élève agit | Le tableau à compléter dans (ou juste au-dessus de) la question qui le fait compléter ; la figure dans la question qui la fait tracer | MF6 |
| Pas de décor | Pas d'image ni de pictogramme sans fonction ; les étoiles de difficulté et les badges de points sont utiles, les illustrations d'ambiance non | MF4 |

**Colonnes et densité.** Éduscol déconseille la lecture en colonnes (MF3), alors que la densification latérale (`MultiColonnes`, `tcbenumerate[2]`) tient un sujet dans son nombre de pages. Arbitrage par défaut :
- garder côte à côte un **texte court** et un **tableau de données** ;
- linéariser quand le bloc de gauche dépasse cinq ou six lignes, ou quand les deux colonnes portent chacune une tâche ;
- mettre côte à côte deux questions seulement si elles sont courtes et indépendantes.

Les retours de l'enseignant ci-dessous peuvent déplacer ce curseur.

## Énoncé : séquençage

| Principe | En bfcours | Code |
|---|---|---|
| Pas d'échec en cascade | Quand la question n+1 dépend d'un résultat : `\acc{Montrer que} … = …` plutôt que « Calculer », ou un total de contrôle dans le tableau, ou « on admet que … » en tête de la question suivante | ST2 |
| Une entrée réussissable par exercice | La question 1 de chaque `EXO` est faisable par un élève fragile ; le saut de difficulté vient ensuite | RS1 |
| Progressivité dans l'exercice | Les items d'une liste vont du plus simple au plus délicat (ex. traduire : intersection, puis conditionnelle) | ST3 |
| Pas de compétence clandestine | Une question n'exige pas, en plus, une compétence évaluée dans un autre exercice ou non annoncée : fournir l'élément non visé (la notation de l'événement, le résultat intermédiaire) | ST9 |
| Amorce pour une tâche complexe | Une case déjà remplie, un rayon tracé, un premier niveau d'arbre esquissé — seulement si construire ce départ n'est pas l'objectif | ST4 |
| Unités et totaux | L'unité dans l'en-tête de ligne du `tcbtab` (« Superficie en m² »), le total général donné | ST6 |

## Support de réponse

- **Compléter sur le sujet plutôt que recopier.** « Recopier et compléter le tableau » fait refaire un travail non évalué, coûteux pour un élève lent ou dyspraxique (MF8). Si la copie est séparée, prévoir que le sujet soit rendu avec la copie, ou fournir le tableau vide en annexe.
- **Un espace de recherche** pour les questions ouvertes quand le sujet sert de support (`\repline[n]`, ou les espaces de `tcfillcrep` / `repsim` selon le type de réponse). Éduscol encourage le brouillon visible : il renseigne sur la démarche.
- Les constructions (arbre, figure) restent réalisables à main levée quand la précision du tracé n'est pas évaluée (MA2), mais **le sujet commun ne le mentionne pas** : c'est un aménagement individuel (PAP), qui reste hors du sujet.
- Les cases d'un tableau à compléter sur le sujet sont des `\repsim[1cm]{<réponse du corrigé>}` (zone seyès, réponse affichée en mode correction), jamais des pointillés.

## En-tête et consignes générales

- Le cartouche « Compétences évaluées » est **généré à partir des titres des `EXO`** : le titre d'un exercice est donc son libellé de compétence. Il reste **court** et nomme la compétence du programme travaillée, pas l'habillage : « Tableau d'effectifs à partir de pourcentages » plutôt que « Test de dépistage et faux positifs » (ST5). Pas de phrase longue en « je sais… ». Les critères de réussite détaillés restent en commentaire dans la source et servent à la correction.
- Une seule consigne générale, juste pour **tous** les exercices : pas de « chaque résultat justifié par un calcul » si un exercice est sans calcul ; préciser l'arrondi attendu.
- Matériel autorisé écrit sur le sujet (calculatrice, instruments, fiche-outil) (MA1).
- Une phrase qui valorise les démarches : « Toute démarche, même non aboutie, est prise en compte » (RS2). Elle se place en pleine largeur sous l'en-tête (avec la consigne générale), pas dans le cadre étroit des Modalités.

## Étayage et échéance

L'étayage acceptable dépend du moment : cases à remplir, exemple travaillé, piste (« il est utile d'effectuer deux calculs ») conviennent à une évaluation proche de la découverte ; à l'approche de l'examen (épreuve anticipée de 1re, bac, brevet), l'élève doit identifier seul les étapes. Un étayage ajouté à un sujet sommatif de fin de cycle s'assume comme transitoire, et se dit en commentaire dans la source.

Accessibiliser pour tous ne remplace pas les adaptations individuelles (PAP, PPS, tiers temps, fiches-outils) : une version adaptée d'un sujet est un second maître, pas un affaiblissement du sujet commun.

## Contrôle avant compilation finale

1. Chaque `EXO` a son objectif et ses critères en commentaire.
2. Aucun item ne porte deux actions notées.
3. Aucune question ne dépend d'un résultat non fourni ; aucune n'exige une compétence d'un autre exercice.
4. Tout vocabulaire hors objectif est remplacé ou défini avant usage.
5. Aucun « Recopier » sans nécessité.
6. La consigne générale vaut pour tous les exercices.
7. Une première question accessible dans chaque exercice.

Pour un audit complet d'un sujet existant, avec captures et rapport : skill `audit-accessibilite-eval`.

## Retours de l'enseignant

Préférences durables tirées des audits (choix cochés ou refusés, remarques de portée générale). Elles priment sur les sections précédentes. Une ligne par préférence, datée, avec sa portée ; une préférence contredite plus tard est **remplacée**, pas empilée.

Format : `- AAAA-MM-JJ · <portée : tous sujets / niveau / type d'éval> · <préférence> — <raison donnée ou constatée>`

- 2026-10-06 · DS de lycée · L'énoncé d'un DS tient en deux pages, ce qui impose une densification latérale ; l'arbitrage colonnes / linéarité se fait exercice par exercice (voir « Colonnes et densité »). — exigence écrite dans le `CLAUDE.md` du DS de probabilités conditionnelles de 1re techno.
- 2026-10-07 · DS de lycée · Aucun exercice coupé entre deux pages : chaque `EXO` tient entier sur une page (`\needspace` avant l'exercice si besoin). — exigence de l'enseignant.
- 2026-10-07 · tous sujets · Jamais de linéarisation qui laisse du vide : chercher un agencement compact qui lève l'obstacle (texte pleine largeur, tableau à côté des questions qui l'utilisent). — remarque sur l'audit du DS de probabilités conditionnelles.
- 2026-10-07 · tous sujets · Cases de tableau à compléter sur le sujet : `\repsim[1cm]{<réponse>}`, jamais de pointillés. — remarque de l'enseignant.
- 2026-10-07 · tous sujets · Pas de mention d'un tracé à main levée (ni d'autre aménagement PAP) dans le sujet commun. — remarque de l'enseignant.
- 2026-10-07 · tous sujets · Titres d'EXO courts = libellés de compétences de l'en-tête, calés sur le programme (« Tableau d'effectifs à partir de pourcentages »). — remarque de l'enseignant.
- 2026-10-07 · tous sujets · Données numériques choisies pour que les calculs tombent juste (quotients décimaux simples), sans changer objectifs ni structure. — remarque de l'enseignant.
- 2026-10-07 · tous sujets · La phrase de valorisation des démarches va en pleine largeur sous l'en-tête, pas dans le cadre Modalités. — remarque de l'enseignant.
