# Architecture des Commandes

> **Fichier généré** : 2026-01-27
>
> Ce fichier sert de base pour réorganiser les commandes en structure hiérarchique.

---

## Inventaire Automatique des Commandes (23 commandes)

| Commande | Description courte |
|----------|-------------------|
| `adaptHtml` | Adaptation de documents vers HTML/KaTeX |
| `adaptTex` | Adaptation conceptuelle vers bfcours |
| `agent-adaptTex` | Adaptation via agent dédié |
| `bareme` | Génération de barèmes actions élèves |
| `continueBO` | Poursuite extraction compétences BO |
| `createHtml` | Création cours HTML/KaTeX |
| `createReveals` | Création présentations reveal.js |
| `createTex` | Création documents LaTeX |
| `do` | Méta-commande d'orchestration |
| `formatTexBetter` | Édition LaTeX compacte |
| `loadSkillKnowledge` | Chargement connaissances skills |
| `loadTexKnowledge` | Chargement connaissances LaTeX |
| `makeEval` | Génération d'évaluations |
| `makePythonEval` | Génération évaluations Python |
| `modifyTex` | Modification documents LaTeX |
| `moodleise` | Création cours Moodle |
| `notebook-audit` | Audit notebooks Jupyter |
| `optiLatex` | Création LaTeX optimisée |
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
│   │   └── optiLatex.md               # → optiLatex
│   │
│   ├── html/                           # Documents Web
│   │   ├── createHtml.md              # → createHtml
│   │   └── createReveals.md           # → createReveals
│   │
│   ├── moodle/                         # Contenus Moodle
│   │   └── moodleise.md               # → moodleise
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
│   └── chargement/                     # Chargement de connaissances
│       ├── loadTexKnowledge.md        # → loadTexKnowledge
│       └── loadSkillKnowledge.md      # → loadSkillKnowledge
│
├── experimental/                       # COMMANDES EN DÉVELOPPEMENT
│   └── vocal-correction.md            # → vocal-correction
│
└── meta/                               # MÉTA-COMMANDES
    └── do.md                          # → do (orchestration)
```

---

## Mapping Détaillé

### Créer / LaTeX
- [ ] `createTex` → `creer/latex/createTex.md`
- [ ] `optiLatex` → `creer/latex/optiLatex.md`

### Créer / HTML
- [ ] `createHtml` → `creer/html/createHtml.md`
- [ ] `createReveals` → `creer/html/createReveals.md`

### Créer / Moodle
- [ ] `moodleise` → `creer/moodle/moodleise.md`

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

### Outillage / Chargement
- [ ] `loadTexKnowledge` → `outillage/chargement/loadTexKnowledge.md`
- [ ] `loadSkillKnowledge` → `outillage/chargement/loadSkillKnowledge.md`

### Experimental
- [ ] `vocal-correction` → `experimental/vocal-correction.md`

### Meta
- [ ] `do` → `meta/do.md`

---

## Résumé par catégorie

| Catégorie | Sous-catégories | Nb commandes |
|-----------|-----------------|--------------|
| `creer/` | latex, html, moodle, evaluation | 7 |
| `modifier/` | latex, html, notebook | 6 |
| `outillage/` | recherche, chargement | 5 |
| `experimental/` | - | 1 |
| `meta/` | - | 1 |
| **Total** | | **21** |

---

## Notes

- Les commandes restent des fichiers `.md` uniques (pas de dossiers comme les skills)
- La structure en sous-dossiers permet un accès `/creer/latex/createTex` ou `/createTex` (alias)
