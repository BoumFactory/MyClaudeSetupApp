# /do - Méta-commande intelligente d'orchestration

## Description

Point d'entrée unique et intelligent pour toutes les demandes pédagogiques. Cette méta-commande :
- Analyse la demande (souvent vague) de l'utilisateur
- Décompose en sous-tâches parallélisables
- **Orchestre les méta-agents (meta-low, meta-mid, meta-high)** pour exécution concurrente
- **Choisit la meilleure approche technique** (LaTeX vs HTML, TikZ vs cetz, etc.)
- **Détecte les demandes généralisables** en nouvelles commandes
- Masque toute la complexité à l'utilisateur

## Usage

```
/do <demande_en_langage_naturel>
```

## Exemples

```bash
/do je voudrais un truc sur les vecteurs
/do faire une éval avec un schéma sympa
/do cours sur pythagore avec une fiche d'exercices + animation
/do 10 exercices progressifs sur les fractions pour 4eme
/do adapter ce document externe vers mon style LaTeX
```

---

## ÉTAPE 0 : PRINCIPES FONDAMENTAUX

### Orchestration parallèle avec méta-agents

La force de /do est d'**orchestrer plusieurs agents en parallèle** quand les tâches sont indépendantes.

| Méta-agent | Modèle | Usage | Quand l'utiliser |
|------------|--------|-------|------------------|
| `meta-low` | haiku | Modification ciblée unique | Corriger une coquille, remplacer un terme |
| `meta-mid` | sonnet | Batch modifications / 1 skill | Renommer partout, appliquer un skill |
| `meta-high` | opus | Workflow multi-skills complexe | Créer contenu élaboré, enchaîner skills |

### Règle de parallélisation

```
SI tâches indépendantes ALORS
  → Lancer plusieurs Task() en PARALLÈLE (même message, plusieurs tool calls)
SINON
  → Séquentiel avec dépendances explicites
```

**Exemple** : "Cours + Exercices + Animation"
```python
# PARALLÈLE : 3 agents simultanés
Task(subagent_type="meta-high", prompt="Créer le cours LaTeX...")
Task(subagent_type="meta-mid", prompt="Créer la fiche d'exercices...")
Task(subagent_type="meta-mid", prompt="Créer l'animation...")
# SÉQUENTIEL ensuite : intégrer les résultats
```

### Fluidité de l'interaction

L'orchestration intelligente réduit naturellement la complexité pour l'utilisateur :
- Questions simples et ciblées (max 2 à la fois)
- Choix techniques automatiques
- Commandes combinées sans intervention
- Résultat livré sans friction

---

## ARBRE DE DÉCISION PRINCIPAL

Suivre cet arbre **dans l'ordre** pour déterminer la stratégie d'exécution.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        DEMANDE UTILISATEUR                                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  Q1 : L'ACTION PRINCIPALE EST...                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │   CRÉER     │  │  MODIFIER   │  │  RECHERCHER │  │   AUTRE     │        │
│  │  (nouveau)  │  │ (existant)  │  │  (explorer) │  │  (autre)    │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│         ▼                ▼                ▼                ▼               │
│    → Q2 Format     → Q3 Ampleur    outillage/        experimental/        │
│                                    recherche/                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────────────┐
│  Q2 : FORMAT ?    │   │  Q3 : AMPLEUR ?   │   │  COMMANDES DIRECTES       │
├───────────────────┤   ├───────────────────┤   ├───────────────────────────┤
│                   │   │                   │   │                           │
│ ○ LaTeX (PDF)     │   │ ○ 1 fichier,      │   │ /searchMathSource         │
│   → Q2a           │   │   modif locale    │   │ /search-report            │
│                   │   │   → meta-low      │   │                           │
│ ○ HTML (Web)      │   │                   │   │ /continueBO               │
│   → Q2b           │   │ ○ Plusieurs       │   │                           │
│                   │   │   modifs, 1 skill │   │ /vocal-correction         │
│ ○ Figure          │   │   → meta-mid      │   │                           │
│   → Q2c           │   │                   │   └───────────────────────────┘
│                   │   │ ○ Restructuration │
│ ○ Notebook        │   │   profonde        │
│   → Q2d           │   │   → meta-high     │
│                   │   │                   │
│ ○ Moodle          │   └───────────────────┘
│   → Q2e           │
│                   │
│ ○ Évaluation      │
│   → Q2f           │
└───────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2a : CRÉER LaTeX - QUEL TYPE ?                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ Cours/Exercices │  │      QCM        │  │   Optimisé/     │             │
│  │ Fiche/Activité  │  │ (automatismes)  │  │   Autonome      │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                      │
│           ▼                    ▼                    ▼                      │
│      /createTex           skill qcm-creator    /optiLatex                  │
│      → meta-high          → meta-mid           → meta-mid                  │
│                                                                             │
│  Skills requis : tex-document-creator + bfcours-latex                       │
│  + latex-geometry si figures géométriques                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2b : CRÉER HTML - QUEL TYPE ?                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ Cours interactif│  │  Présentation   │  │   Animation     │             │
│  │    KaTeX        │  │   Reveal.js     │  │  interactive    │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                      │
│           ▼                    ▼                    ▼                      │
│      /createHtml          /createReveals        /moodleise                 │
│      → meta-high          → meta-mid            → meta-mid                 │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2c : CRÉER UNE FIGURE                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Figure de géométrie, courbe, arbre, schéma  ──►  TikZ dans le document     │
│                                                  (skill latex-geometry)     │
│  Document Typst  ──►  figure cetz (skill bfcours-typst)                     │
│                                                                             │
│  Pas d'agent séparé : la figure est écrite avec le document.                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2d : CRÉER UN NOTEBOOK                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Notebook Jupyter pédagogique  ──►  jupyter-notebook-creator (agent)        │
│                                     → meta-high                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2e : CRÉER MOODLE                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐                                  │
│  │  Cours complet  │  │ Parcours gamifié│                                  │
│  │    (.mbz)       │  │      H5P        │                                  │
│  └────────┬────────┘  └────────┬────────┘                                  │
│           │                    │                                           │
│           ▼                    ▼                                           │
│      /moodleise          /createGameMap                                    │
│      → meta-high         → meta-high                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q2f : CRÉER ÉVALUATION                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐             │
│  │ Évaluation maths│  │ Évaluation      │  │  Barème seul    │             │
│  │   complète      │  │    Python       │  │                 │             │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘             │
│           │                    │                    │                      │
│           ▼                    ▼                    ▼                      │
│      /makeEval           /makePythonEval        /bareme                    │
│      → meta-high         → meta-high            → meta-mid                 │
│                                                                             │
│  Note : /makeEval + /bareme souvent combinés                                │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  Q3 : MODIFIER - QUEL FORMAT ?                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                          LaTeX                                    │      │
│  ├──────────────────────────────────────────────────────────────────┤      │
│  │                                                                   │      │
│  │  Fichier existant      Document externe      Reformatage          │      │
│  │  à modifier            à adapter             compacté             │      │
│  │       │                     │                    │                │      │
│  │       ▼                     ▼                    ▼                │      │
│  │  /modifyTex            /adaptTex           /formatTexBetter       │      │
│  │  → meta-mid            → meta-high          → meta-mid            │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                          HTML                                     │      │
│  ├──────────────────────────────────────────────────────────────────┤      │
│  │  Document → HTML/KaTeX                                            │      │
│  │       │                                                           │      │
│  │       ▼                                                           │      │
│  │  /adaptHtml → meta-mid                                            │      │
│  └──────────────────────────────────────────────────────────────────┘      │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────┐      │
│  │                        Notebook                                   │      │
│  ├──────────────────────────────────────────────────────────────────┤      │
│  │  Audit/Refactoring Jupyter                                        │      │
│  │       │                                                           │      │
│  │       ▼                                                           │      │
│  │  /notebook-audit → meta-mid                                       │      │
│  └──────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ARBRE DE DÉCISION : PARALLÉLISATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  DEMANDE MULTI-RESSOURCES DÉTECTÉE ?                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Mots-clés : "et", "avec", "plus", "+", virgule, liste                      │
│  Exemples : "cours ET exercices", "éval AVEC figure", "10 fiches"           │
│                                                                             │
│       OUI                                              NON                  │
│        │                                                │                   │
│        ▼                                                ▼                   │
│  ┌─────────────────────────────┐             ┌─────────────────────────┐   │
│  │  Q4 : DÉPENDANCES ?         │             │  Agent unique           │   │
│  │                             │             │  selon Q2/Q3            │   │
│  │  Les ressources dépendent-  │             └─────────────────────────┘   │
│  │  elles les unes des autres? │                                           │
│  └─────────────────────────────┘                                           │
│           │                                                                 │
│     ┌─────┴─────┐                                                           │
│     │           │                                                           │
│    NON         OUI                                                          │
│     │           │                                                           │
│     ▼           ▼                                                           │
│ ┌───────────┐ ┌───────────────────────────────────────────────────────┐    │
│ │ PARALLÈLE │ │ SÉQUENTIEL avec phases                                │    │
│ │           │ │                                                       │    │
│ │ Lancer    │ │ Phase 1 : Créations indépendantes (parallèle)         │    │
│ │ tous les  │ │ Phase 2 : Intégration (séquentiel, meta-low)          │    │
│ │ agents    │ │                                                       │    │
│ │ en même   │ │ Exemple : cours + figure intégrée dans le cours       │    │
│ │ temps     │ │ → P1: meta-high(cours) // meta-mid(figure)            │    │
│ │           │ │ → P2: meta-low(ajouter \includegraphics)              │    │
│ └───────────┘ └───────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ARBRE DE DÉCISION : CHOIX DU MÉTA-AGENT

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SÉLECTION DU MÉTA-AGENT                                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         meta-low (haiku)                            │   │
│  │                                                                     │   │
│  │  ✓ 1 fichier ciblé                                                  │   │
│  │  ✓ 1-3 modifications locales (Edit)                                 │   │
│  │  ✓ Correction coquille, remplacement terme                          │   │
│  │  ✓ Ajout d'une ligne (ex: \includegraphics)                         │   │
│  │  ✓ Tâche < 2 min estimée                                            │   │
│  │                                                                     │   │
│  │  Commandes typiques : intégration, corrections ponctuelles          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                          NON ──────┴────── OUI → meta-low                   │
│                           │                                                 │
│                           ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         meta-mid (sonnet)                           │   │
│  │                                                                     │   │
│  │  ✓ Plusieurs modifications dans 1+ fichiers                         │   │
│  │  ✓ 1 skill à appliquer                                              │   │
│  │  ✓ Renommage global (replace_all)                                   │   │
│  │  ✓ Figure TikZ isolée                                               │   │
│  │  ✓ Animation HTML simple                                            │   │
│  │  ✓ Présentation Reveal.js                                           │   │
│  │  ✓ Adaptation de document                                           │   │
│  │                                                                     │   │
│  │  Commandes : /createHtml, /createReveals, /adaptTex...              │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                          NON ──────┴────── OUI → meta-mid                   │
│                           │                                                 │
│                           ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         meta-high (opus)                            │   │
│  │                                                                     │   │
│  │  ✓ Création de contenu élaboré (cours, évaluation)                  │   │
│  │  ✓ Multi-skills enchaînés                                           │   │
│  │  ✓ Workflow complexe avec documentation                             │   │
│  │  ✓ Adaptation contextuelle intelligente                             │   │
│  │  ✓ Notebook Jupyter complet                                         │   │
│  │  ✓ Cours Moodle complet                                             │   │
│  │                                                                     │   │
│  │  Commandes : /createTex, /makeEval, /moodleise...                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## RÉSUMÉ DÉCISIONNEL RAPIDE

| Question | Réponse | Action |
|----------|---------|--------|
| Créer du neuf ? | LaTeX | Q2a → /createTex, skill qcm-creator, /optiLatex |
| | HTML | Q2b → /createHtml, /createReveals |
| | Figure | Q2c → TikZ (latex-geometry) ou cetz (bfcours-typst) |
| | Notebook | Q2d → jupyter-notebook-creator |
| | Moodle | Q2e → /moodleise, /createGameMap |
| | Évaluation | Q2f → /makeEval, /makePythonEval, /bareme |
| Modifier existant ? | LaTeX | /modifyTex, /adaptTex, /formatTexBetter |
| | HTML | /adaptHtml |
| | Notebook | /notebook-audit |
| Rechercher ? | - | /searchMathSource, /search-report |
| Multi-ressources ? | Indépendantes | PARALLÈLE |
| | Dépendantes | Phase 1 parallèle + Phase 2 séquentielle |
| Complexité ? | Simple (1 edit) | meta-low |
| | Moyenne (1 skill) | meta-mid |
| | Complexe (multi) | meta-high |

---

## ÉTAPE 1 : ANALYSE ET DÉCOMPOSITION

### 1.1 Classification de la demande

| Catégorie | Sous-catégories | Commandes associées |
|-----------|-----------------|---------------------|
| **creer/** | latex, html, moodle, evaluation | `/createTex`, `/createHtml`, `/createReveals`, `/makeEval`, `/makePythonEval`, `/bareme`, `/moodleise`, `/createGameMap` |
| **modifier/** | latex, html, notebook | `/modifyTex`, `/adaptTex`, `/formatTexBetter`, `/adaptHtml`, `/notebook-audit` |
| **outillage/** | recherche, chargement | `/searchMathSource`, `/search-report`, `/loadTexKnowledge` |
| **experimental/** | - | `/vocal-correction` |

### 1.2 Détection des besoins multiples

Identifier si la demande implique **plusieurs ressources** :

| Pattern détecté | Décomposition |
|-----------------|---------------|
| "cours + exercices" | meta-high(cours) // meta-mid(exercices) |
| "éval + barème" | meta-mid(éval) → meta-low(barème) |
| "document + figure" | meta-high(doc) // meta-mid(figure) |
| "document + animation" | meta-high(doc) // meta-mid(animation) |
| "batch N fichiers" | N × meta-low en parallèle |
| "adapter + compiler" | meta-mid(adapt) → meta-low(compile) |

### 1.3 Évaluation de la complexité

| Complexité | Critères | Agent recommandé |
|------------|----------|------------------|
| **Simple** | 1 fichier, 1 modification locale | meta-low |
| **Moyenne** | Plusieurs modifications, 1 skill | meta-mid |
| **Complexe** | Multi-fichiers, multi-skills, création élaborée | meta-high |

---

## ÉTAPE 2 : QUESTIONNEMENT INTELLIGENT

**Maximum 2 questions à la fois.** Inférer le reste.

### Les 5 dimensions à clarifier

#### 1. QUOI ? (Type de ressource)

| Type | Sous-types |
|------|------------|
| **Document LaTeX** | Cours, Exercices, Évaluation, Activité, DM, Fiche |
| **Document HTML** | Cours interactif, Support de projection |
| **Présentation** | Reveal.js (web) |
| **Figure/Visuel** | Figure TikZ ou cetz, Schéma, Animation |
| **Notebook** | Notebook Jupyter |
| **Moodle** | Cours complet, Parcours gamifié |
| **Autre** | Recherche, Barème, QCM |

#### 2. OÙ ? (Chemin de destination)

```
📁 Racine
├── 1. Cours/[niveau]/Sequence-[theme]/[type]/
├── 1. Devoirs_communs/[niveau]/
├── 1. DM/[niveau]/
├── 6. Cours_particuliers/
├── GT_IA_MATHS/
├── LABOMATHS/
├── 4. Images/
└── Applications_educatives/
```

#### 3. POUR QUI ? (Public)

| Public | Impact sur le contenu |
|--------|----------------------|
| **Élèves** | Langage accessible, progression |
| **Inspecteur** | Références programmes, compétences |
| **Collègues** | Documentation technique |
| **Personnel** | Format condensé |

#### 4. COMMENT ? (Méthode - déterminée automatiquement)

#### 5. CONTEXTE ? (Optionnel : durée, contraintes)

### Règles de questionnement

1. **Fichier ouvert** → Proposer de travailler dessus
2. **Niveau évident** → Ne pas redemander
3. **Action claire** → Ne pas redemander
4. **Toujours "Autre"** → Permettre les combinaisons

---

## ÉTAPE 3 : CHOIX TECHNIQUES AUTOMATIQUES

### Figures : TikZ ou cetz

**RÈGLE** : toute figure est écrite en code, donc modifiable et nette à l'impression.

| LaTeX : TikZ (skill `latex-geometry`) | Typst : cetz (skill `bfcours-typst`) |
|---------------------------------------|--------------------------------------|
| Figure géométrique | Figure géométrique |
| Graphique de fonction | Graphique de fonction |
| Arbre de probabilités | Arbre de probabilités |
| Diagramme simple | Diagramme simple |

Pour une carte mentale, utiliser le skill `mind-map-creator`.

### LaTeX vs HTML

| LaTeX (`/createTex`) | HTML (`/createHtml`) |
|---------------------|----------------------|
| Impression, documents officiels | Projection, consultation web |
| Évaluations, fiches élèves | Cours projetés, révisions |
| PDF statique | Interactif (dark mode, sélecteur) |

---

## ÉTAPE 4 : ORCHESTRATION DES AGENTS

### 4.1 Patterns d'orchestration

#### Pattern A : Tâche unique simple
```python
# 1 seul agent suffit
Task(subagent_type="meta-low", prompt="...")
```

#### Pattern B : Tâches indépendantes (PARALLÈLE)
```python
# MÊME MESSAGE, plusieurs Task() = exécution parallèle
Task(subagent_type="meta-high", prompt="Créer cours LaTeX sur [thème]...")
Task(subagent_type="meta-mid", prompt="Créer fiche d'exercices [thème]...")
Task(subagent_type="meta-mid", prompt="Créer animation interactive [thème]...")
```

#### Pattern C : Tâches dépendantes (SÉQUENTIEL)
```python
# Étape 1 : Création principale
result1 = Task(subagent_type="meta-high", prompt="Créer le document...")
# Étape 2 : Intégration (dépend de result1)
Task(subagent_type="meta-low", prompt=f"Ajouter \includegraphics dans {result1.file}...")
```

#### Pattern D : Batch parallèle
```python
# 10 exercices → 10 agents meta-low en parallèle
for i in range(10):
    Task(subagent_type="meta-low", prompt=f"Créer exercice {i+1} sur [thème]...", run_in_background=True)
```

### 4.2 Formulation des prompts pour méta-agents

**IMPORTANT** : Les prompts doivent être **autonomes et complets**.

```markdown
# Structure prompt méta-agent

## Contexte
[Niveau, thème, public cible]

## Objectif précis
[Ce qui doit être créé/modifié]

## Skills à utiliser
[Liste des skills nécessaires]

## Fichiers concernés
[Chemins absolus ou patterns glob]

## Format de sortie attendu
[JSON, rapport, fichier créé]

## Contraintes spécifiques
[Style, longueur, particularités]
```

### 4.3 Gestion des dépendances

```
┌─────────────────────────────────────────────────────────┐
│  Demande : "Cours + Infographie + Animation intégrés"   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 1 : Créations parallèles                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐     │
│  │ meta-high    │ │ meta-mid     │ │ meta-mid     │     │
│  │ → cours.tex  │ │ → infog.png  │ │ → anim.html  │     │
│  └──────────────┘ └──────────────┘ └──────────────┘     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  PHASE 2 : Intégration (séquentielle)                   │
│  ┌──────────────────────────────────────────────────┐   │
│  │ meta-low : Ajouter \includegraphics{infog.png}  │   │
│  │ meta-low : Ajouter lien vers anim.html          │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## ÉTAPE 5 : MATRICE DE DÉCISION COMMANDES

### Commandes par catégorie

#### creer/latex/
| Commande | Cas d'usage |
|----------|-------------|
| `/createTex` | Créer document LaTeX (cours, exercices, fiche) |
| `/optiLatex` | Création LaTeX autonome optimisée |

#### creer/html/
| Commande | Cas d'usage |
|----------|-------------|
| `/createHtml` | Cours HTML interactif KaTeX |
| `/createReveals` | Présentation Reveal.js |

#### creer/evaluation/
| Commande | Cas d'usage |
|----------|-------------|
| `/makeEval` | Générer évaluation complète |
| `/makePythonEval` | Évaluation Python lycée |
| `/bareme` | Générer barème actions élèves |

#### creer/moodle/
| Commande | Cas d'usage |
|----------|-------------|
| `/moodleise` | Créer cours Moodle complet |
| `/createGameMap` | Parcours gamifié H5P |

#### modifier/latex/
| Commande | Cas d'usage |
|----------|-------------|
| `/modifyTex` | Modifier document LaTeX existant |
| `/adaptTex` | Adapter document externe → bfcours |
| `/formatTexBetter` | Édition compacte optimisée |

#### modifier/html/
| Commande | Cas d'usage |
|----------|-------------|
| `/adaptHtml` | Adapter document → HTML/KaTeX |

#### modifier/notebook/
| Commande | Cas d'usage |
|----------|-------------|
| `/notebook-audit` | Audit et refactoring notebooks |

#### outillage/recherche/
| Commande | Cas d'usage |
|----------|-------------|
| `/searchMathSource` | Rechercher ressources maths |
| `/search-report` | Recherche web + rapport |
| `/continueBO` | Poursuite extraction BO |

---

## ÉTAPE 6 : RÈGLES LaTeX bfcours

**RÈGLE OBLIGATOIRE** : Pour toute création de document LaTeX utilisant bfcours :

1. **Utiliser le skill `tex-document-creator`** pour initialiser le projet
2. **Puis utiliser le skill `bfcours-latex`** pour éditer le contenu
3. **Si géométrie** : charger également `latex-geometry`

**Ne jamais créer un document bfcours manuellement** sans passer par `tex-document-creator`.

---

## ÉTAPE 7 : PROPOSITION DE CHEMIN

```
Je vais créer [ressource(s)] sur [thème] pour [niveau].

📁 Emplacement principal : `1. Cours/[niveau]/Sequence-[theme]/[type]/`
📁 Images associées : `4. Images/[theme]/`

Cela vous convient-il ?
```

---

## ÉTAPE 8 : EXÉCUTION

### Workflow standard

1. **Analyser** : Décomposer la demande
2. **Planifier** : Identifier les agents et leur ordonnancement
3. **Exécuter** : Lancer les agents (parallèle si possible)
4. **Intégrer** : Assembler les résultats si nécessaire
5. **Vérifier** : Compilation LaTeX, tests HTML

### Exemple complet

**Demande** : "Cours sur Pythagore avec fiche d'exercices et animation"

```python
# ANALYSE
# - Ressource principale : cours LaTeX
# - Annexes : fiche d'exercices (LaTeX), animation (HTML)
# - Intégration : liens dans le cours

# EXÉCUTION PARALLÈLE (même message)
Task(
    subagent_type="meta-high",
    prompt="""
    Contexte: Cours 4ème sur le théorème de Pythagore
    Objectif: Créer un cours complet avec le style bfcours
    Skills: tex-document-creator, bfcours-latex
    Destination: 1. Cours/4eme/Sequence-Pythagore/Cours/
    """
)
Task(
    subagent_type="meta-mid",
    prompt="""
    Contexte: Fiche d'exercices Pythagore
    Objectif: Exercices progressifs, énoncés et corrigés
    Skills: bfcours-latex
    Destination: 1. Cours/4eme/Sequence-Pythagore/Exercices/
    """
)
Task(
    subagent_type="meta-mid",
    prompt="""
    Contexte: Diaporama Pythagore
    Objectif: Présentation Reveal.js de la preuve visuelle, projetable en classe
    Skills: reveals-presentation
    Destination: 1. Cours/4eme/Sequence-Pythagore/Presentations/
    """
)

# INTÉGRATION SÉQUENTIELLE (après résultats)
Task(
    subagent_type="meta-low",
    prompt="Ajouter dans le cours créé un renvoi vers la fiche d'exercices"
)
```

---

## ÉTAPE 9 : DÉTECTION DE COMMANDE GÉNÉRALISABLE

### Quand proposer une nouvelle commande ?

Après avoir compris la demande, se demander :

> "Cette demande, une fois **généralisée** (avec des paramètres variables), serait-elle une commande utile et réutilisable ?"

### Critères de pertinence

| Critère | Exemple positif | Exemple négatif |
|---------|-----------------|-----------------|
| **Paramétrable** | "QCM de N questions sur [thème]" | "Ce QCM précis sur Pythagore" |
| **Réutilisable** | "Fiche de révision [niveau] [chapitre]" | Document unique très spécifique |
| **Pattern clair** | "Éval diagnostique de rentrée [niveau]" | Demande floue sans structure |
| **Gain de temps** | "Correction type exercice [type]" | Action simple déjà couverte |

### Format de proposition (en fin de tâche)

```markdown
## Proposition de nouvelle commande

J'ai remarqué que votre demande pourrait être généralisée en commande réutilisable :

**Commande proposée** : `/ficheRevision`
**Catégorie** : `creer/latex/`
**Usage** : `/ficheRevision [niveau] [theme] [--format court|long]`
**Description** : Génère une fiche de révision structurée pour un chapitre donné.

Voulez-vous que je crée cette commande ?
```

---

## ÉTAPE 10 : AUTO-AMÉLIORATION (OBLIGATOIRE)

En fin de tâche :

1. **Analyser** les difficultés rencontrées
2. **Logger** les erreurs dans `.claude/logs/frequent-errors.jsonl` si pertinent
3. **Détecter** si la demande était généralisable (voir ÉTAPE 9)
4. **Présenter** le résumé

```markdown
## Fin de tâche

✅ Ressources créées :
- `1. Cours/4eme/.../cours_pythagore.tex`
- `1. Cours/4eme/.../Exercices/exercices_pythagore.tex`
- `1. Cours/4eme/.../Animations/preuve_visuelle.html`

### Orchestration utilisée
- 3 agents parallèles (meta-high + 2 meta-mid)
- 1 agent séquentiel (meta-low pour intégration)

[Si demande généralisable :]
Cette demande pourrait devenir une commande `/coursComplet [niveau] [theme]`...

Souhaitez-vous que j'applique des améliorations ?
```

---

## Rappels essentiels

- **Paralléliser** : Lancer plusieurs Task() dans le même message si tâches indépendantes
- **Méta-agents** : low (ciblé), mid (batch/skill), high (complexe)
- **Figures** : TikZ en LaTeX, cetz en Typst (jamais d'image générée)
- **tex-document-creator + bfcours-latex** : Toujours pour création LaTeX
- **Auto-amélioration** : Toujours en fin de tâche
- **Détecter les patterns** : Proposer des commandes généralisables
