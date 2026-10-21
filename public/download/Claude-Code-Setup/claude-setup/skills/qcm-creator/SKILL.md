---
name: qcm-creator
description: Rédige des QCM de mathématiques au format bfcours (environnement Mcq et commande McqQuest du paquet rdmcq, style BFCours chargé par bfcours) avec des distracteurs construits sur les erreurs réelles des élèves, notamment pour la partie « automatismes » de l'épreuve anticipée de mathématiques de première (12 questions, 4 propositions, une seule bonne réponse). Utiliser dès qu'il faut écrire, compléter, corriger ou mettre en page un QCM, un questionnaire à choix multiples, des « questions flash » ou des automatismes dans un fichier LaTeX bfcours, même si l'utilisateur ne prononce pas le mot « Mcq ».
---

# QCM Creator — QCM au format bfcours

Un QCM bfcours s'écrit avec l'environnement `Mcq` et la commande `\McqQuest` du paquet `rdmcq`, habillés par le format `BFCours`. Ce skill donne la syntaxe exacte de ce format (voie principale) puis le savoir-faire pour écrire de bonnes questions (énoncés, distracteurs, progression).

Charger aussi `bfcours-latex` pour le reste du document (EXO, `\acc`, `\encadrer`, `MultiColonnes`).

---

## 1. Ce que bfcours charge déjà

`bfcours.sty` charge `rdmcq` (ligne 168) puis le format `rdmcq.bfcours.format` (ligne 182). Dans un document bfcours :

- **rien à ajouter au préambule** ;
- **ne jamais recopier le format** dans le document ni créer de fichier de format dans le dossier : la version installée fait foi ;
- respecter la structure du document existant et insérer le QCM à sa place.

Le format `BFCours` (`rdmcq.bfcours.format.sty`) : pastille noire numérotée à gauche de chaque question, propositions dans des boîtes à case à cocher, **2 colonnes de propositions par défaut** (`answer columns=2`, ligne 120), case cochée en rouge et fond teinté `prop!10` en mode correction.

Hors bfcours : `\usepackage{rdmcq}` puis un format livré avec rdmcq, par exemple `\input{rdmcq.boston.format.tex}` et `\begin{Mcq}[Boston]`.

---

## 2. Syntaxe

### Environnement `Mcq`

```latex
\begin{Mcq}[BFCours]
  ... questions ...
\end{Mcq}
```

Options utiles (clés `/rdmcq`, à ajouter après `BFCours`, séparées par des virgules) :

| Option | Effet | Source `rdmcq.sty` |
|---|---|---|
| `resume` | Poursuit la numérotation du bloc `Mcq` précédent (sinon elle repart à 1) | l. 76-79, 1341 |
| `num start=n` | Commence la numérotation à `n` | l. 80 |
| `answer columns=n` | Nombre de colonnes de propositions (4 pour des réponses très courtes, 1 pour des phrases) | l. 111 |
| `orientation=vertical` | Propositions empilées sous la question (défaut : `horizontal`) | l. 71-74, 227 |
| `correction=true` | Force l'affichage des bonnes réponses (case cochée, fond teinté) | l. 135-137 |
| `width=…` | Largeur totale (défaut `\linewidth`) | l. 83, 231 |

Le mode correction s'active aussi tout seul quand la version corrigée bfcours est activée (booléen de `rdcrep`, l. 1318-1322).

### Question `\McqQuest`

```latex
\McqQuest[br=3]
{Énoncé de la question :}
{Proposition 1, Proposition 2, Proposition 3, Proposition 4}
```

- `br=n` : numéro de la bonne réponse. Plusieurs bonnes réponses : `br={1,3}` (liste, l. 1113-1115).
- Le deuxième argument est une **liste séparée par des virgules** (l. 1117-1119). Conséquences :
  - virgule décimale toujours protégée : `$0{,}5$`, jamais `$0,5$` (sinon la proposition est coupée en deux) ;
  - une proposition qui contient elle-même une virgule (texte, ensemble, couple) se met entre accolades : `{oui, car $f(2) = 0$}`, `{$\{1, 2\}$}` ;
  - les espaces autour des virgules sont ignorés.
- L'énoncé peut contenir plusieurs paragraphes (ligne vide), `\acc{…}`, `\encadrer[prop]{…}`, une figure.

### Message commun `\McqMessage`

Bandeau « Info » en pleine largeur entre deux questions, pour une donnée partagée : `\McqMessage{Les questions 5 à 7 portent sur la fonction $f$ définie par $f(x) = x^2 - 4$.}` (l. 1084).

---

## 3. Modèle complet dans un EXO

Usage type, relevé dans des évaluations bfcours réelles :

```latex
\def\rdifficulty{1}
\begin{EXO}{Automatismes}{}
\tcbitempoint{6}\textit{Pour chaque question, une seule réponse est correcte. Aucune justification n'est demandée.}

\begin{Mcq}[BFCours]
\McqQuest[br=4]
{L'\acc{opération} qui permet de calculer \acc{25~\% de 480} est :}
{$\dfrac{480}{25 \times 100}$, $25 \times 480 \times 0{,}1$, $\dfrac{480 \times 100}{25}$, $\dfrac{1}{4} \times 480$}

\McqQuest[br=2]
{Un appareil consomme \encadrer[defi]{$7{,}2 \times 10^6$} joules.

À combien de kWh cela correspond-il ? \hfill \encadrer[defi]{$1\,\text{kWh} = 3{,}6 \times 10^6\,\text{J}$}}
{$0{,}5\,\text{kWh}$, $2\,\text{kWh}$, $5\,\text{kWh}$, $20\,\text{kWh}$}
\end{Mcq}

\exocorrection
\begin{Mcq}[BFCours, correction=true]
... mêmes questions, recopiées à l'identique ...
\end{Mcq}

\begin{tcbenumerate}[1]
\tcbitem $25~\% = \dfrac{1}{4}$, donc on calcule $\dfrac{1}{4} \times 480$. \acc{Réponse 4.}
\tcbitem $\dfrac{7{,}2 \times 10^6}{3{,}6 \times 10^6} = 2$. \acc{Réponse 2.}
\end{tcbenumerate}
\end{EXO}
```

- Titre d'EXO : texte pur, jamais de virgule ni de mode math.
- Correction : le bloc recopié avec `correction=true`, suivi au besoin d'une justification courte par question.

### Question avec figure

La figure se place dans l'énoncé, en `MultiColonnes` (texte à gauche, figure centrée à droite) :

```latex
\McqQuest[br=1]
{\begin{MultiColonnes}{2}
\tcbitem On a représenté ci-contre une parabole $\mathcal{P}$.

\acc{Une seule} des quatre fonctions ci-dessous peut être représentée par $\mathcal{P}$. Laquelle ?
\tcbitem[halign=center,valign=center] \begin{tikzpicture}[scale=0.5] ... \end{tikzpicture}
\end{MultiColonnes}}
{$x \longmapsto 1{,}6(x+5)^2-4$, $x \longmapsto 1{,}6(x-5)^2-4$, $x \longmapsto -1{,}6(x+5)^2-4$, $x \longmapsto -1{,}6(x-5)^2-4$}
```

---

## 4. Découper le QCM en blocs (coupure de page)

Un bloc `Mcq` est **insécable** : s'il ne tient pas dans la place restante, il saute en entier à la page suivante ; s'il est trop grand pour la boîte d'un EXO, les dernières questions **disparaissent du PDF** (`Package tcolorbox Warning: The upper box part has become overfull`).

Règle : couper en plusieurs blocs, le suivant ouvert par `\begin{Mcq}[BFCours, resume]`, et **dimensionner le premier bloc sur la place libre** de la page 1, pas au milieu arbitraire des 12 questions.

```latex
\begin{Mcq}[BFCours]
... Q1 à Q5 (le dernier qui tient sous l'en-tête) ...
\end{Mcq}

\begin{Mcq}[BFCours, resume]
... Q6 à Q12 ...
\end{Mcq}
```

- Sous un en-tête d'évaluation complet (cartouche `chapEval` + encart « Première partie »), le premier bloc tient environ 5 questions ; sans en-tête lourd, davantage.
- Une question avec figure ou à propositions longues consomme plus de place : couper plus tôt.
- Après compilation : `grep -c "upper box part has become overfull"` sur le `.log` doit valoir 0 ; regarder la page 1 et avancer ou reculer la coupure d'une question (skill `latex-visual-review`, Recette M).
- Faire la même coupure dans le bloc de correction.

---

## 5. Savoir-faire : écrire de bonnes questions

Typologie détaillée des questions, formulations types et progression des deux sujets zéro de première : `references/SYNTHESE_QCM_SUJETS_0.md`. À lire avant de rédiger un QCM de type épreuve anticipée.

### Énoncés

- Une question = une compétence ; 1 à 3 lignes ; variables définies (« Soit $x$ un réel… »).
- Mots-clés en `\acc{…}` (toujours `\acc{$…$}`, jamais `$\acc{…}$`), données en `\encadrer[prop]{…}` ou `[defi]`.
- Notation française : `0{,}21`, `\dfrac` pour les fractions, espaces insécables avant `\%` et les unités.
- Calculatrice interdite à l'épreuve anticipée : des nombres qui se calculent de tête.

### Distracteurs

Chaque mauvaise réponse correspond à une erreur réelle et identifiable ; jamais de réponse absurde.

| Famille | Exemples |
|---|---|
| Erreur de calcul classique | $(a+b)^2 = a^2 + b^2$ ; $25~\%$ de 480 calculé $25 \times 480$ |
| Confusion de concepts | moyenne / médiane ; affine / carré ; +10 % puis +10 % = +20 % |
| Erreur de signe ou de lecture | $(x-3)^2 = x^2 - 9$ ; pente lue à la place de l'ordonnée à l'origine |
| Lecture littérale | « tiers d'un quart » lu $\dfrac{1}{3} \times 4$ au lieu de $\dfrac{1}{3} \times \dfrac{1}{4}$ |

Exemple commenté (le commentaire reste dans le source, pas dans le PDF) :

```latex
\McqQuest[br=4]
{Le \acc{tiers d'un quart} correspond à la fraction :}
{$\dfrac{1}{7}$, $\dfrac{3}{4}$, $\dfrac{1}{3} \times 4$, $\dfrac{1}{12}$}
% 1/7 : 1/3 + 1/4 additionnés terme à terme ; 3/4 : inversion ;
% 1/3 x 4 : lecture littérale ; 1/12 : correct
```

### Structure d'un QCM d'automatismes (épreuve anticipée de première)

- 12 questions, 4 propositions, une seule bonne réponse, 6 points (0,5 par question), 20 à 30 minutes.
- Répartition : 3-4 algèbre, 2-3 géométrie, 2-3 fonctions, 1-2 statistiques et probabilités, 2-3 autres (pourcentages, suites…) ; jamais trois questions du même domaine d'affilée.
- Progression : Q1-Q3 faciles, Q4-Q6 moyennes, Q7-Q9 moyennes à difficiles, Q10-Q12 difficiles.
- Voie générale sans spécialité : contextes concrets, calcul. Spécialité : abstraction, lecture graphique, raisonnement.

---

## 6. Déroulé

1. Lire la source et les consignes (niveau, nombre de questions, thème, barème).
2. Choisir les questions selon la structure ci-dessus et `references/SYNTHESE_QCM_SUJETS_0.md`.
3. Construire les distracteurs (une erreur identifiée par distracteur).
4. Écrire le QCM dans un EXO selon le modèle de la section 3, découpé en blocs (section 4).
5. Vérifier :
   - une seule bonne réponse par question (ou la liste `br={…}` voulue), résultat recalculé ;
   - bonnes réponses réparties sur les positions 1 à 4 (pas toujours la même) ;
   - aucune virgule décimale non protégée dans les propositions ;
   - bloc de correction identique à l'énoncé, avec `correction=true` ;
   - compilation sans `upper box part has become overfull`.

---

## Sources

- `rdmcq.sty` (paquet rdmcq de la collection « ProfDeleuze », qui fournit aussi `rdexo`, `rdcrep`, `rdcheckbox`), fourni avec les paquets LaTeX bfcours à télécharger sur le même site que ce paquet de skills (dossier `latex-packages/ProfDeleuze/`) ; les numéros de ligne cités correspondent à cette version. À installer dans le texmf local (MiKTeX ou TeX Live) avec les fichiers bfcours.
- `rdmcq.bfcours.format.sty` et `bfcours.sty` : dossier `latex-packages/BFcours/` du même téléchargement.
- Sujets zéro de l'épreuve anticipée de mathématiques (Éduscol) : https://eduscol.education.gouv.fr/5688/epreuve-anticipee-de-mathematiques-aux-baccalaureats-general-et-technologique
