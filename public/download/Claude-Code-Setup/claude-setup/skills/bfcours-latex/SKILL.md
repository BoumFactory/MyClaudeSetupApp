---
name: bfcours-latex
description: Utiliser ce skill pour éditer des documents LaTeX éducatifs avec le package bfcours. Expertise spécialisée pour l'écriture de contenu pédagogique français (6ème à Terminale) incluant cours, exercices, évaluations, fiches et activités. Utiliser de manière proactive pour l'édition de contenu LaTeX bfcours.
---

# Expert Édition LaTeX BFCours

Système expert LaTeX pour éditer et enrichir des documents éducatifs de mathématiques avec le package bfcours. Ce skill se concentre sur l'écriture de contenu pédagogique de haute qualité en respectant les conventions bfcours.

## Objectif

Éditer du contenu LaTeX en respectant les conventions strictes du package bfcours pour l'enseignement des mathématiques. Produire du matériel pédagogique professionnel pour l'enseignement français de la 6ème à la Terminale.

## ⚠️ Séparation des Responsabilités

Ce skill se concentre **uniquement sur l'édition de contenu**. Pour les autres tâches :

- **Créer un nouveau projet** → Utiliser le skill `tex-document-creator`
- **Compiler un document** → Utiliser le skill `tex-compiling-skill`
- **Éditer le contenu** → Ce skill (bfcours-latex)

## Workflows Principaux

### Workflow 1 : Éditer un Document Complet avec Validation

Lors de l'édition de documents existants nécessitant une validation par compilation.

**Étapes :**

1. **Lire le document** et la structure du projet (fichier principal, enonce.tex, sections/, etc.)

2. **Charger les connaissances bfcours** depuis `references/bfcours-conventions.md` dans ce skill

3. **Lire les ressources fournies** par l'utilisateur si présentes pour référence

4. **Écrire/éditer le contenu** en utilisant les environnements didactiques bfcours (voir conventions ci-dessous)

5. **Compiler pour valider** : Déléguer au skill `tex-compiling-skill` :

   ```
   Utiliser tex-compiling-skill pour quick_compile()

   ```

6. **Corriger les erreurs de compilation de manière itérative** si nécessaire :
   - Analyser les messages d'erreur (via tex-compiling-skill)
   - Corriger les problèmes dans le contenu
   - Re-compiler

7. **Vérifier les erreurs mathématiques** dans le PDF qui peuvent ne pas être visibles dans le code LaTeX (lire le PDF généré pour validation)

8. **Effectuer les corrections finales** si nécessaire

9. **Finaliser le fichier principal** (pour les documents de type Cours uniquement) :
   - Lire le fichier principal du projet (généralement `Nom_projet.tex`)
   - **Compléter le tableau des compétences travaillées** juste après `\tableofcontents` avec les vraies compétences identifiées dans le contenu
   - **Supprimer les placeholders** : retirer `\voc{nobug}` et `\competence{nobug}` qui ne sont que des marqueurs temporaires
   - Sauvegarder le fichier principal modifié

### Workflow 2 : Éditer un Fichier Unique (Sans Compilation)

Lors de l'édition d'un fichier de contenu LaTeX autonome sans besoin de compilation immédiate.

**Étapes :**

1. **Se documenter** sur les exigences de la tâche ou du matériel source

2. **Charger les connaissances bfcours** depuis `references/bfcours-conventions.md`

3. **Vérifier si le fichier existe** et le lire s'il est présent

4. **Écrire le contenu** en suivant les standards bfcours

5. **NE PAS compiler** (focus uniquement sur la création de contenu)

## Architecture de Projet

Les documents suivent cette structure standard :

```
Nom_projet/
├── Nom_projet.tex          # Fichier principal à compiler (nommé d'après le répertoire)
│                           # Contient les en-têtes et les inputs globaux
├── VERSION_Nom_projet.tex  # Variantes de version (ex : ELEVE_Nom_projet.tex) [optionnel]
├── enonce.tex              # Contenu principal (importé dans le fichier principal)
├── enonce_TOOLS.tex        # Si présent, remplace enonce.tex [optionnel]
├── enonce_figures.tex      # Figures TikZ indexées par \tikzfig{CODE}
├── images/                 # Répertoire d'images [optionnel]
│   └── *.png
├── sections/               # Pour les gros documents [optionnel]
│   └── fichiers.tex        # Contenu réparti en plusieurs fichiers
└── annexes/                # Scripts et fichiers secondaires [optionnels]
    └── scripts.py
```

**Note** : Cette structure est créée par le skill `tex-document-creator`. Ce skill se concentre sur l'édition des fichiers de contenu (enonce.tex, sections/, etc.)

### Workflow d'édition selon la taille du `enonce.tex`

Le `enonce.tex` se rédige par défaut en un seul fichier monolithique. C'est l'écriture la plus simple et la plus directe. **Mais au-delà d'environ 1000 lignes**, le fichier devient un point de friction sérieux pour l'IA (lecture intégrale à chaque Read/Edit, contexte saturé, modifications ciblées coûteuses). À ce seuil, déclencher l'atomisation : extraire chaque environnement didactique top-level dans son propre fichier `sections/<Type>/<nom>.tex`, et remplacer par un `\input{...}`.

**Types atomisés par défaut** : `Definition`, `Propriete`, `Theoreme`, `Lemme`, `Corollaire`, `Demonstration`, `Exemple`, `Methode`, `Remarque`, `Notation`, `Activite`, `Histoire`, `Graphique`, `Conjecture`, `Algorithme`, **et `EXO`** (les exercices sont atomisés au même titre, énoncé et correction extraits ensemble dans un seul fichier).

Le `enonce.tex` ne garde alors que l'**orchestration pure** : `\section{}`, `\subsection{}`, les commentaires de section, le texte de transition éventuel, et les `\input{...}`. Le PDF compilé est **strictement identique** : LaTeX inline les `\input` au préprocesseur. Sur un cours de 1070 lignes, le `enonce.tex` typique passe à ~120 lignes (-89%).

**Quand atomiser** :

| Situation | Action |
|----------|--------|
| `enonce.tex` < 1000 lignes | Ne rien faire. Édition directe au fichier unique. |
| `enonce.tex` ≥ 1000 lignes | Lancer `atomize_didactic.py`. |
| Document à partager en archive autonome | Lancer `monolithize_didactic.py` pour reconstituer un fichier unique. |
| Refactor structurel d'un cours atomisé | Monolithiser → refondre → re-atomiser. |

**Scripts disponibles** :

```bash
# Atomisation : dry-run d'abord, toujours.
python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" \
    --enonce <chemin/enonce.tex> --dry-run

# Si le plan affiché est cohérent, lancer sans --dry-run :
python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" \
    --enonce <chemin/enonce.tex>

# Monolithisation : produit <enonce>.monolith.tex à côté.
python ".claude/skills/bfcours-latex/scripts/monolithize_didactic.py" \
    --enonce <chemin/enonce.tex>

# Monolithisation in-place + suppression des fichiers atomisés (avec backup) :
python ".claude/skills/bfcours-latex/scripts/monolithize_didactic.py" \
    --enonce <chemin/enonce.tex> --inplace --cleanup
```

**Garanties** :

- Backup horodaté automatique avant toute modification.
- Le parseur suit `\begin`/`\end` avec une pile : un environnement imbriqué (ex. une `Definition` à l'intérieur d'un `EXO`, ou une `MultiColonnes` dans une `Propriete`) **n'est pas extrait séparément** — il reste avec son contenant car il en fait sémantiquement partie.
- Pour chaque `EXO` atomisé, la ligne `\def\rdifficulty{N}` qui le précède immédiatement est **absorbée automatiquement** dans le fichier extrait (elle fait sémantiquement partie de l'exercice : elle pilote la coche de difficulté affichée).
- Les commentaires `% \begin{...}` sont ignorés par le parseur.
- Le round-trip `atomize → monolithize` est **strictement identique octet pour octet**.
- Idempotent : ré-exécuter le script sur un fichier déjà atomisé n'a aucun effet.
- Pour ne pas atomiser les `EXO` (comportement opt-out, rare), passer `--exclude-exo`.

**Convention de nommage des fichiers atomisés** :

- Pour les environnements didactiques classiques : `<prefix><NN>_<slug>.tex` où `NN` est un compteur cumulatif par type (`def01`, `def02`, ..., `prop01`, ...) et `slug` une version ASCII normalisée du titre (max 40 caractères). Pour un bloc sans titre, le nom se réduit à `<prefix><NN>.tex`.
- Pour les `EXO` : `exo<NN>_d<difficulty>_<code_competence>_<slug>.tex`, intégrant trois informations clés :
  - **difficulty** : valeur de `\def\rdifficulty{X}` qui précède l'EXO, normalisée pour le système de fichiers (`1` → `d1`, `1.5` → `d1-5`, `2.5` → `d2-5`).
  - **code compétence** : 2e argument obligatoire de `\begin{EXO}{titre}{code}`, transcrit en minuscules.
  - **slug du titre** : version ASCII normalisée du 1er argument.

  Exemples : `exo01_d1_1sp22_tirage_d_une_boule_numerotee.tex`, `exo15_d2-5_1sl19_duree_avant_la_premiere_panne.tex`. Cet ordre (difficulté avant compétence) permet le filtrage `ls sections/EXO/exo*_d1_*` (tous les exos faciles), `ls sections/EXO/exo*_*_1sp22_*` (tous les exos de la compétence 1SP22), ou `ls sections/EXO/exo*_d2-5_*` (tous les exos les plus difficiles).

  Si l'EXO n'a pas de `\def\rdifficulty` au-dessus, le token `d<difficulty>` est simplement omis : `exo03_exo_sans_rdifficulty.tex`.

Préfixes courants : `def`, `prop`, `theo`, `demo`, `exemple`, `rem`, `not`, `act`, `meth`, `hist`, `graph`, `exo`.

**Détails complets** : voir `references/atomize_workflow.md` (charger en cas de cas particulier, doute sur le périmètre, ou personnalisation des types).

## Résumé des Conventions BFCours

**Conventions critiques** à toujours suivre (voir `references/bfcours-conventions.md` pour tous les détails) :

### Environnements Structurels

1. **MultiColonnes** : Système de mise en page en grille

   ```latex
   \begin{MultiColonnes}{nbCol}[options]
       \tcbitem[raster multicolumn=2] Contenu large
       \tcbitem Contenu colonne 1
       \tcbitem Contenu colonne 2
   \end{MultiColonnes}

   ```

2. **tcbenumerate** : Énumération OBLIGATOIRE (remplace enumerate)

   ```latex
   \begin{tcbenumerate}[nbCol][nbStart][style]
       \tcbitem Premier item
       \tcbitem Deuxième item
   \end{tcbenumerate}

   ```

3. **tcbtab** : Tableaux OBLIGATOIRES (remplace tabular)

   ```latex
   \begin{tcbtab}[Titre]{l|c|r}
   Entête1 & Entête2 & Entête3\\
   \hline
   contenu & contenu & contenu\\
   \end{tcbtab}

   ```

### Commandes de Formatage de Texte

- **\acc{mot}** : Accentuation (REMPLACE \textbf) - couleur adaptative
- **\voc{mot}** : OBLIGATOIRE pour la première occurrence de vocabulaire dans les cours
- **\frquote{expr}** : Citations
- **a$^{\circ}$** : Notation des degrés (format OBLIGATOIRE)
- **\encadrer[couleur]{contenu}** : Encadrer les formules/résultats importants
- **Logique** : \Si, \Alors, \Donc, \Mais, \SSI, \Et
- **Ligatures** : TOUJOURS utiliser `\oe` au lieu du caractère Unicode œ (exemples : n\oe ud, c\oe ur, \oe il, s\oe ur, b\oe uf)

### Environnements Didactiques

Tout le contenu doit utiliser les environnements didactiques appropriés :

- **Definition** : Pour les définitions (met à jour les couleurs et la table des matières)
- **Propriete** : Pour les propriétés
- **Theoreme** : Pour les théorèmes
- **Demonstration** : Pour les démonstrations
- **Exemple** : Pour les exemples
- **Remarque** : Pour les remarques
- **Notation** : Pour les conventions de notation
- **Activite** : Pour les activités de découverte

**Syntaxe** :
```latex
\begin{Definition}[Titre Court]
contenu avec \acc{emphase} et \voc{vocabulaire}
\end{Definition}
```

### Environnement Exercice (EXO)

**⚠️ RÈGLE ABSOLUE : Environnement EXO OBLIGATOIRE**

L'environnement `EXO` est OBLIGATOIRE pour **TOUS les exercices**, y compris :
- Les exercices dans les feuilles d'exercices
- Les exercices dans les activités (environnement Activite)
- Les exercices dans les évaluations
- Les devoirs maison

**Principe fondamental** : Les corrections sont **toujours** intégrées après `\exocorrection` dans le même environnement EXO, **jamais dans un fichier séparé**.

**⚠️ RÈGLE CRITIQUE : Pas de virgule dans les titres d'EXO**

Le titre passé en premier argument de `\begin{EXO}{...}` ne doit **JAMAIS** contenir de virgule. Les virgules cassent le parsing interne de tcolorbox/bfcours et provoquent des erreurs `\iffalse` fatales. Utiliser des tirets `-` ou des points-virgules `;` à la place.

```
% CORRECT :
\begin{EXO}{Additionner - soustraire et comparer des fractions}{}
\begin{EXO}{QCM -- Fractions et Probabilités}{}

% INCORRECT (provoque des erreurs de compilation) :
\begin{EXO}{Additionner, soustraire et comparer des fractions}{}
\begin{EXO}{Multiplier, trouver l'inverse et diviser}{}
```

**⚠️ RÈGLE CRITIQUE : Pas de mode math dans les titres d'EXO**

Le titre d'un EXO ne doit **JAMAIS** contenir de commandes en mode math (`$...$`, `\R`, `\N`, `\Z`, `\C`, `\dfrac`, `\mathrm`, `\mathcal`, etc.). tcolorbox sauvegarde le titre dans le fichier `.aux` (pour la table des corrections via `\rdexocorrection`), et lors du rechargement ces commandes sont exécutées hors mode math, ce qui provoque des erreurs fatales du type :

- `\math@bb allowed only in math mode`
- `Missing $ inserted`
- `Extra alignment tab has been changed to \cr` (en cascade)

Utiliser du texte à la place (« réels », « entiers », « fraction », etc.), ou à la rigueur `\protect\ensuremath{...}` si un symbole math est indispensable.

```
% CORRECT :
\begin{EXO}{Résoudre dans les réels}{}
\begin{EXO}{Quotient avec exponentielle}{}
\begin{EXO}{Étude de la fonction f}{}

% INCORRECT (crash de l'aux au rechargement) :
\begin{EXO}{Résoudre dans $\R$}{}
\begin{EXO}{Étude de $f(x) = \dfrac{1}{x}$}{}
\begin{EXO}{Calcul de $\mathrm{e}^x$}{}
```

**Critique pour tous les exercices** :

```latex
\def\rdifficulty{1.5}  % Échelle de 1 à 3
\begin{EXO}{Titre de Compétence -- sans virgule}{code_competence}

Énoncé avec instructions claires.
\tcbitempoint{2}\acc{Calculer} la valeur...

\exocorrection

Contenu de la solution suivant la structure de l'énoncé.
\end{EXO}
```

**Attribution des points** avec \tcbitempoint :
- 1 point : Action basique (calcul, rappel, tâche simple)
- 2 points : Figure, tableau, production complexe
- Cumulatif : Plusieurs actions dans une question
- 5 points : Tâches de recherche (pas de cumul)

### Espaces Réponses pour les Élèves

**⚠️ RÈGLE CRITIQUE : Différence Collège / Lycée**

| Niveau | Espaces réponses | Comportement par défaut |
|--------|------------------|------------------------|
| **Collège** (6ème-3ème) | **SYSTÉMATIQUES** | Toujours inclure les espaces réponses dans les énoncés |
| **Lycée** (2nde-Terminale) | **Optionnels** | Ne pas inclure sauf demande explicite |

**Au collège**, les élèves travaillent sur le document imprimé. Les espaces réponses contiennent la correction qui s'affiche en mode professeur.

**Au lycée**, les élèves rédigent généralement sur copie. Les espaces réponses sont ajoutés uniquement si l'utilisateur le demande ou utilise l'option `--crep`.

**Commandes disponibles :**

1. **Ligne courte** : `\repsim[1.5cm]{contenu}` - pour les petites réponses (un nombre, un mot)
2. **Ligne adaptative** : `\tcfillcrep{texte}` - occupe tout l'espace disponible sur la ligne
3. **Multiligne** :

   ```latex
   \begin{crep}[extra lines=4]
   Contenu de réponse
   \end{crep}
   ```

**Bonnes pratiques pour les espaces réponses :**

- Utiliser `\repsim` pour les réponses courtes (résultats numériques, comparaisons)
- Utiliser `\tcfillcrep` pour les réponses à compléter en fin de ligne (textes à trous)
- Utiliser `\begin{crep}...\end{crep}` pour les calculs détaillés, raisonnements
- L'option `[extra lines=N]` permet d'ajuster la hauteur de l'espace multiligne

**Exemple collège (avec espaces réponses) :**
```latex
\tcbitem \tcbitempoint{2}$\dfrac{3}{4} + \dfrac{1}{2} = $ \tcfillcrep{$\dfrac{3}{4} + \dfrac{2}{4} = \dfrac{5}{4}$}
```

**Exemple lycée (sans espaces réponses) :**
```latex
\tcbitem \tcbitempoint{2}\acc{Calculer} $\dfrac{3}{4} + \dfrac{1}{2}$.
```

## Scripts Embarqués

Ce skill embarque des scripts Python regroupés en deux familles. Voir `references/scripts_to_use.md` pour le guide complet de recherche.

### Recherche dans la documentation bfcours

- **search_command.py** : Chercher une commande ou un environnement bfcours par nom ou mot-cle
  ```bash
  python ".claude/skills/bfcours-latex/scripts/search_command.py" --exact "\\encadrer"
  python ".claude/skills/bfcours-latex/scripts/search_command.py" --query "tableau"
  ```

- **search_examples.py** : Chercher des patterns dans les exemples reels (assets/usecase/)
  ```bash
  python ".claude/skills/bfcours-latex/scripts/search_examples.py" --pattern "\\begin{EXO}" --context 10
  python ".claude/skills/bfcours-latex/scripts/search_examples.py" --list-envs
  ```

- **search_package.py** : Chercher dans n'importe quel package LaTeX installe (via kpsewhich)
  ```bash
  python ".claude/skills/bfcours-latex/scripts/search_package.py" --package tcolorbox --query "raster"
  python ".claude/skills/bfcours-latex/scripts/search_package.py" --package siunitx --list-commands
  ```

### Atomisation / monolithisation d'un `enonce.tex`

Voir la section « Workflow d'édition selon la taille du `enonce.tex` » et `references/atomize_workflow.md` pour le détail. À utiliser dès que `enonce.tex` ≥ ~1000 lignes (gain massif de contexte pour les éditions ultérieures).

- **atomize_didactic.py** : Extrait les environnements didactiques top-level vers `sections/<Type>/<nom>.tex` et insère des `\input` à leur place.
  ```bash
  # Toujours dry-run d'abord pour visualiser le plan
  python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" --enonce <chemin> --dry-run
  python ".claude/skills/bfcours-latex/scripts/atomize_didactic.py" --enonce <chemin>
  ```

- **monolithize_didactic.py** : Reconstitue un `enonce.tex` monolithique en résolvant récursivement les `\input{sections/...}`. Utile pour partager une archive autonome ou re-monolithiser avant gros refactor.
  ```bash
  python ".claude/skills/bfcours-latex/scripts/monolithize_didactic.py" --enonce <chemin>
  python ".claude/skills/bfcours-latex/scripts/monolithize_didactic.py" --enonce <chemin> --inplace --cleanup
  ```

## Délégation aux Skills Compagnons

Ce skill ne travaille **jamais seul** pour certaines tâches. Il délègue systématiquement :

- **Créer un nouveau projet LaTeX** → Skill `tex-document-creator` (scripts Python pour la structure de dossiers, templates, fichiers)
- **Compiler un document** → Skill `tex-compiling-skill` (quick_compile.py, analyse d'erreurs)
- **Optimiser la disposition visuelle après compilation** → Skill `latex-visual-review` (capture PNG du PDF rendu, densification latérale des énoncés via colonnage `tcbenumerate`/`MultiColonnes` avec paramètres graphiques de clarté ; les corrections `\exocorrection` sont laissées aérées car projetées item par item)

Si l'utilisateur demande de créer un document complet depuis zéro (nouveau cours, nouvelle évaluation, etc.), la première étape est **toujours** de déléguer la création de la structure au skill `tex-document-creator`, puis de revenir à ce skill pour éditer le contenu.

## Auto-review visuelle (latex-visual-review)

Après la compilation réussie d'un document complet, déléguer au skill `latex-visual-review` pour **regarder** la sortie PDF et l'optimiser automatiquement (réduire les pages quasi vides, équilibrer la densité, ajuster les colonnes, retirer les sauts de page indésirables).

**Quand invoquer** :

- Systématiquement après la première compilation d'un document complet (cours, évaluation, fiche d'exercices ≥ 2 pages).
- Sur demande utilisateur explicite : « optimise l'espace », « fais tenir sur N pages », « la dernière page est presque vide », « améliore la disposition ».
- Quand le `.log` signale des `Overfull \hbox` non triviaux, ou que le document est notablement plus long qu'attendu.

**Ne pas invoquer** sur des éditions ciblées (ajout d'une remarque, correction d'un exercice) ou sur un brouillon intermédiaire d'une seule page.

Le skill `latex-visual-review` effectue une boucle adversariale plafonnée à 4 itérations, avec **rollback automatique** si une modification dégrade le rendu visuel ou casse la compilation. Il ne touche **jamais au contenu pédagogique**. Voir `.claude/skills/latex-visual-review/SKILL.md` pour le détail du workflow.

## Niveaux Scolaires

Niveaux du système éducatif français :

**Collège** :
- 6eme (Sixième) - `$\mathbf{6^{\text{ème}}}$`
- 5eme (Cinquième) - `$\mathbf{5^{\text{ème}}}$`
- 4eme (Quatrième) - `$\mathbf{4^{\text{ème}}}$`
- 3eme (Troisième) - `$\mathbf{3^{\text{ème}}}$`

**Lycée** :
- 2nde (Seconde) - `$\mathbf{2^{\text{nde}}}$`
- 1ere_spe (Première spécialité) - `$\mathbf{1^{\text{ère}}}$`
- Terminale - `$\mathbf{T^{\text{Le}}}$`

## Meilleures Pratiques

1. **Toujours utiliser les environnements bfcours** : Ne jamais utiliser les environnements LaTeX standard enumerate, itemize ou tabular. Utiliser tcbenumerate, MultiColonnes et tcbtab.

2. **Chargement progressif** :
   - Lire `references/bfcours-conventions.md` pour les conventions essentielles
   - Lire `references/exemples-usecases.md` pour des exemples professionnels si nécessaire
   - Utiliser Grep pour chercher des patterns spécifiques dans les exemples

3. **Validation par compilation** : Pour les documents complets, utiliser le skill `tex-compiling-skill` pour compiler et valider la sortie PDF.

5. **Emphase du vocabulaire** : Dans les cours (documents Cours), TOUJOURS utiliser `\voc{mot}` pour la première occurrence des termes de vocabulaire.

6. **Accentuation du texte** : Remplacer tous les `\textbf{}` par `\acc{}` pour une emphase colorée adaptative.

7. **Accentuation dans les énoncés d'exercices** : L'accentuation `\acc{}` est OBLIGATOIRE pour **DEUX éléments** :
   - **Les verbes d'action** : `\acc{Calculer}`, `\acc{Déterminer}`, `\acc{Résoudre}`, etc.
   - **La forme de réponse attendue** : `\acc{résultat simplifié}`, `\acc{sous forme d'intervalle(s)}`, `\acc{justifier le signe}`, etc.

   **Exemples corrects** :
   ```latex
   \tcbitempoint{2}\acc{Calculer} les valeurs suivantes en donnant un \acc{résultat simplifié} :
   \tcbitempoint{3}\acc{Résoudre} et donner l'ensemble des solutions \acc{sous forme d'intervalle(s)} :
   \tcbitempoint{2}\acc{Simplifier} les expressions suivantes (\acc{justifier le signe}) :
   ```

8. **Première ligne des tableaux** : Dans `tcbtab`, la première ligne EST l'en-tête (pas de `\hline` initial nécessaire, contrairement à tabular).

9. **Attribution des points** : Être réfléchi avec `\tcbitempoint{}` pour refléter avec précision la complexité de la tâche.

## Références de la Base de Connaissances

Ce skill inclut des références groupées dans le répertoire `references/` :

- **bfcours-conventions.md** : Conventions complètes du package bfcours (charger pour tous les workflows)
- **exemples-usecases.md** : Exemples professionnels réels de la séquence polynômes (utiliser Grep pour chercher des patterns spécifiques)
- **atomize_workflow.md** : Détail complet du pipeline d'atomisation / monolithisation d'un `enonce.tex` (algorithme de détection, convention de nommage, garanties d'invariance, cas particuliers). À charger quand on touche à un cours volumineux ou quand on veut comprendre / personnaliser le comportement des scripts `atomize_didactic.py` et `monolithize_didactic.py`.
- **tkz-tab-tableaux-variations.md** : Syntaxe complète de `tkz-tab` pour les tableaux de variations + **astuces critiques** : `\tkzTabIma` pour les valeurs intermédiaires non critiques (cas $f'$ s'annule sans changer de signe), structure de TV vide à compléter par l'élève via `\ifcorrection`, récapitulatif des symboles `+/-/z/d/t/R`. **À charger dès qu'on écrit un tableau de variations**, en particulier quand $f'$ a une racine double / multiple ou qu'on veut afficher une valeur de $f$ qui n'est pas un extremum.

- **conception-evaluations-accessibles.md** : principes Éduscol 2026 d'accessibilité des évaluations traduits en gestes bfcours (une action par item, pas d'échec en cascade, pas de compétence clandestine, compléter sur le sujet plutôt que recopier, arbitrage colonnes / linéarité, en-tête et consignes générales), liste de contrôle, et **retours de l'enseignant** issus des audits, qui priment. **À charger avant de rédiger ou de remanier toute évaluation** (DS, contrôle, interro, sujet type bac).

Charger ces références selon les besoins pendant les workflows en utilisant l'outil Read. Pour les documents volumineux, utiliser Grep avec des patterns de recherche spécifiques plutôt que de lire les fichiers entiers.

## Exemples d'Utilisation

### Exemple 1 : Éditer un cours existant

```
Utilisateur : "Ajoute une section sur les équations du second degré"

Workflow : Éditer un Document Complet avec Validation
1. Lire la structure actuelle du cours
2. Charger bfcours-conventions.md
3. Écrire une nouvelle section avec environnements Definition, Propriete, Exemple
4. Utiliser \voc{} pour le vocabulaire, \acc{} pour l'emphase
5. Déléguer compilation au skill tex-compiling-skill
6. Vérifier les erreurs mathématiques dans le PDF via pdf-analyzer
7. Effectuer corrections finales si nécessaire
```

### Exemple 2 : Édition rapide de fichier

```
Utilisateur : "Écris 3 exercices dans enonce.tex"

Workflow : Éditer un Fichier Unique (Sans Compilation)
1. Charger bfcours-conventions.md
2. Lire enonce.tex s'il existe
3. Écrire les exercices en utilisant l'environnement EXO avec \tcbitempoint
4. Terminé (pas de compilation)
```

### Exemple 3 : Enrichir un document avec compétences

```
Utilisateur : "Ajoute les codes de compétences aux exercices sur les vecteurs en 1ère"

1. Lire le document
2. Identifier les compétences pertinentes pour le sujet et le niveau
3. Éditer chaque environnement EXO pour ajouter le code compétence
4. Valider avec compilation (déléguer à tex-compiling-skill)
```

## Intégration du Barème (Évaluations)

Après la rédaction d'une évaluation, utiliser le skill `bareme-actions-eleves` pour :

1. **Atomiser la correction** en actions élèves distinctes
2. **Appliquer les coefficients** selon le type d'exercice (1 pour calcul, 0.5 pour géométrie)
3. **Générer le fichier `bareme.json`** pour la correction interactive
4. **Analyser la densité** de l'évaluation (actions / note cible)

### Correspondance avec \tcbitempoint

| Ce que vous écrivez | Ce que ça signifie |
|---------------------|-------------------|
| `\tcbitempoint{3}` | 3 actions élèves attendues pour cette question |

**Recommandation** : Toujours rédiger la correction (`\exocorrection`) **avant** d'attribuer les points. L'atomisation de la correction donne le nombre exact d'actions.

### Workflow Évaluation Complet

0. Lire `references/conception-evaluations-accessibles.md` (principes et retours de l'enseignant) ; écrire en commentaire l'objectif et les critères de réussite de chaque exercice
1. Rédiger l'évaluation avec `bfcours-latex`, puis passer la liste de contrôle de cette référence
2. Rédiger les corrections dans chaque `EXO` après `\exocorrection`
3. Utiliser `/bareme` ou le skill `bareme-actions-eleves` pour générer le barème
4. Corriger avec l'interface `bareme.html`
5. Pour un audit complet du sujet (grille Éduscol, captures, rapport à cocher) : skill `audit-accessibilite-eval`

## Rappels Critiques

- JAMAIS utiliser les environnements LaTeX standard `enumerate`, `itemize` ou `tabular`
- TOUJOURS utiliser `\acc{}` au lieu de `\textbf{}`
- TOUJOURS accentuer les **verbes d'action** ET la **forme de réponse attendue** dans les énoncés
- TOUJOURS utiliser `\voc{}` pour la première occurrence de vocabulaire dans les cours
- TOUJOURS déléguer la compilation au skill `tex-compiling-skill`
- TOUJOURS vérifier les exemples usecases en cas de doute sur l'utilisation bfcours
- TOUJOURS utiliser `bareme-actions-eleves` après rédaction d'une évaluation
- TOUJOURS lire `references/conception-evaluations-accessibles.md` avant d'écrire une évaluation : un élève ne doit pas échouer pour une raison étrangère à l'objectif évalué
- NE JAMAIS créer de nouveau projet manuellement (déléguer au skill `tex-document-creator`)
