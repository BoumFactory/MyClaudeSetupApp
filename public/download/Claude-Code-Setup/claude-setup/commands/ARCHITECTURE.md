# Architecture des Commandes

> **Fichier généré** : 2026-01-27
>
> Ce fichier sert de base pour réorganiser les commandes en structure hiérarchique.

---

## Inventaire Automatique des Commandes (27 commandes)

| Commande | Description courte |
|----------|-------------------|
| `adaptHtml` | Adaptation de documents vers HTML/KaTeX |
| `adaptTex` | Adaptation conceptuelle vers bfcours |
| `agent-adaptTex` | Adaptation via agent dédié |
| `animate` | Création d'animations interactives |
| `bareme` | Génération de barèmes actions élèves |
| `continueBO` | Poursuite extraction compétences BO |
| `create-app` | Création d'applications éducatives |
| `createBeamer` | Création diaporamas Beamer |
| `createHtml` | Création cours HTML/KaTeX |
| `createImage` | Création d'images et visuels |
| `createReveals` | Création présentations reveal.js |
| `createTex` | Création documents LaTeX |
| `do` | Méta-commande d'orchestration |
| `ficheTexnique` | Production fiches techniques |
| `formatTexBetter` | Édition LaTeX compacte |
| `loadSkillKnowledge` | Chargement connaissances skills |
| `loadTexKnowledge` | Chargement connaissances LaTeX |
| `makeEval` | Génération d'évaluations |
| `makePythonEval` | Génération évaluations Python |
| `modifyTex` | Modification documents LaTeX |
| `moodleise` | Création cours Moodle |
| `notebook-audit` | Audit notebooks Jupyter |
| `optiLatex` | Création LaTeX optimisée |
| `routine-matin` | Journal d'actualités quotidien |
| `search-report` | Recherche web et rapport |
| `searchMathSource` | Recherche ressources maths |
| `vocal-correction` | Corrections depuis transcriptions |

---

## Architecture Proposée

```
.claude/commands/
│
├── creer/                              # CRÉATION DE CONTENU
│   │
│   ├── latex/                          # Documents LaTeX
│   │   ├── createTex.md               # → createTex
│   │   ├── createBeamer.md            # → createBeamer
│   │   └── optiLatex.md               # → optiLatex
│   │
│   ├── html/                           # Documents Web
│   │   ├── createHtml.md              # → createHtml
│   │   ├── createReveals.md           # → createReveals
│   │   └── animate.md                 # → animate
│   │
│   ├── moodle/                         # Contenus Moodle
│   │   └── moodleise.md               # → moodleise
│   │
│   ├── media/                          # Contenus visuels
│   │   └── createImage.md             # → createImage
│   │
│   ├── application/                    # Applications
│   │   └── create-app.md              # → create-app
│   │
│   └── evaluation/                     # Évaluations
│       ├── makeEval.md                # → makeEval
│       ├── makePythonEval.md          # → makePythonEval
│       └── bareme.md                  # → bareme
│
├── modifier/                           # MODIFICATION DE CONTENU
│   │
│   ├── latex/                          # Documents LaTeX
│   │   ├── modifyTex.md               # → modifyTex
│   │   ├── formatTexBetter.md         # → formatTexBetter
│   │   ├── adaptTex.md                # → adaptTex
│   │   └── agent-adaptTex.md          # → agent-adaptTex
│   │
│   ├── html/                           # Documents Web
│   │   └── adaptHtml.md               # → adaptHtml
│   │
│   └── notebook/                       # Notebooks
│       └── notebook-audit.md          # → notebook-audit
│
├── outillage/                          # OUTILS ET RESSOURCES
│   │
│   ├── recherche/                      # Recherche de ressources
│   │   ├── searchMathSource.md        # → searchMathSource
│   │   ├── search-report.md           # → search-report
│   │   └── continueBO.md              # → continueBO
│   │
│   ├── documentation/                  # Production de documentation
│   │   └── ficheTexnique.md           # → ficheTexnique
│   │
│   └── chargement/                     # Chargement de connaissances
│       ├── loadTexKnowledge.md        # → loadTexKnowledge
│       └── loadSkillKnowledge.md      # → loadSkillKnowledge
│
├── experimental/                       # COMMANDES EN DÉVELOPPEMENT
│   └── vocal-correction.md            # → vocal-correction
│
├── perso/                              # COMMANDES PERSONNELLES
│   └── routine-matin.md               # → routine-matin
│
└── meta/                               # MÉTA-COMMANDES
    └── do.md                          # → do (orchestration)
```

---

## Mapping Détaillé

### Créer / LaTeX
- [ ] `createTex` → `creer/latex/createTex.md`
- [ ] `createBeamer` → `creer/latex/createBeamer.md`
- [ ] `optiLatex` → `creer/latex/optiLatex.md`

### Créer / HTML
- [ ] `createHtml` → `creer/html/createHtml.md`
- [ ] `createReveals` → `creer/html/createReveals.md`
- [ ] `animate` → `creer/html/animate.md`

### Créer / Moodle
- [ ] `moodleise` → `creer/moodle/moodleise.md`

### Créer / Media
- [ ] `createImage` → `creer/media/createImage.md`

### Créer / Application
- [ ] `create-app` → `creer/application/create-app.md`

### Créer / Evaluation
- [ ] `makeEval` → `creer/evaluation/makeEval.md`
- [ ] `makePythonEval` → `creer/evaluation/makePythonEval.md`
- [ ] `bareme` → `creer/evaluation/bareme.md`

### Modifier / LaTeX
- [ ] `modifyTex` → `modifier/latex/modifyTex.md`
- [ ] `formatTexBetter` → `modifier/latex/formatTexBetter.md`
- [ ] `adaptTex` → `modifier/latex/adaptTex.md`
- [ ] `agent-adaptTex` → `modifier/latex/agent-adaptTex.md`

### Modifier / HTML
- [ ] `adaptHtml` → `modifier/html/adaptHtml.md`

### Modifier / Notebook
- [ ] `notebook-audit` → `modifier/notebook/notebook-audit.md`

### Outillage / Recherche
- [ ] `searchMathSource` → `outillage/recherche/searchMathSource.md`
- [ ] `search-report` → `outillage/recherche/search-report.md`
- [ ] `continueBO` → `outillage/recherche/continueBO.md`

### Outillage / Documentation
- [ ] `ficheTexnique` → `outillage/documentation/ficheTexnique.md`

### Outillage / Chargement
- [ ] `loadTexKnowledge` → `outillage/chargement/loadTexKnowledge.md`
- [ ] `loadSkillKnowledge` → `outillage/chargement/loadSkillKnowledge.md`

### Experimental
- [ ] `vocal-correction` → `experimental/vocal-correction.md`

### Perso
- [ ] `routine-matin` → `perso/routine-matin.md`

### Meta
- [ ] `do` → `meta/do.md`

---

## Résumé par catégorie

| Catégorie | Sous-catégories | Nb commandes |
|-----------|-----------------|--------------|
| `creer/` | latex, html, moodle, media, application, evaluation | 11 |
| `modifier/` | latex, html, notebook | 6 |
| `outillage/` | recherche, documentation, chargement | 6 |
| `experimental/` | - | 1 |
| `perso/` | - | 1 |
| `meta/` | - | 1 |
| **Total** | | **27** |

---

## Notes

- Les commandes restent des fichiers `.md` uniques (pas de dossiers comme les skills)
- La structure en sous-dossiers permet un accès `/creer/latex/createTex` ou `/createTex` (alias)
