# Architecture des Agents

> **Fichier généré** : 2026-01-27
>
> Ce fichier sert de base pour réorganiser les agents en structure hiérarchique.

---

## Inventaire Automatique des Agents (28 agents)

| Agent | Description courte |
|-------|-------------------|
| `app-creator-agent` | Création d'applications Flask éducatives |
| `beamer-worker` | Création diaporamas Beamer |
| `bo-competence-extractor` | Extraction compétences depuis BO |
| `bo-search-agent` | Recherche dans les programmes BO |
| `competence-presentation-generator` | Présentations reveal.js par compétence |
| `debug-tex-log` | Débogage fichiers LaTeX |
| `document-creator-worker` | Création documents LaTeX (templates) |
| `error-investigator` | Analyse logs d'erreurs |
| `eval-builder` | Génération d'évaluations complètes |
| `fiche-technique-agent` | Génération fiches techniques |
| `image-user` | Génération d'images (Imagen) |
| `interactive-animation-creator` | Création animations interactives |
| `jupyter-notebook-creator` | Création notebooks Jupyter |
| `latex-main-worker` | Édition LaTeX principale (bfcours) |
| `latex-side-worker` | Édition LaTeX secondaire |
| `mathalea-scraper` | Récupération exercices mathAlea |
| `prevision-seances-completer` | Complétion prévisions séances |
| `programme-officiel-extractor` | Extraction programmes officiels |
| `program-updater` | Mise à jour programmes |
| `python-competences-extractor` | Extraction compétences Python |
| `qcm-builder` | Création QCM LaTeX |
| `reveals-creator` | Création présentations reveal.js |
| `seance-sequence-matcher` | Association séances/séquences |
| `self-improvement-agent` | Auto-amélioration du système |
| `student-prompt-builder` | Construction prompts étudiants |

---

## Architecture Proposée

```
.claude/agents/
│
├── creer/                              # CRÉATION DE CONTENU
│   │
│   ├── latex/                          # Documents LaTeX
│   │   ├── latex-main-worker.md       # → Édition principale bfcours
│   │   ├── latex-side-worker.md       # → Édition secondaire
│   │   ├── document-creator-worker.md # → Création depuis templates
│   │   ├── beamer-worker.md           # → Diaporamas Beamer
│   │   └── qcm-builder.md             # → QCM LaTeX
│   │
│   ├── html/                           # Documents Web
│   │   ├── reveals-creator.md         # → Présentations reveal.js
│   │   ├── interactive-animation-creator.md # → Animations
│   │   └── competence-presentation-generator.md # → Présent. compétences
│   │
│   ├── media/                          # Contenus visuels
│   │   └── image-user.md              # → Génération images
│   │
│   ├── application/                    # Applications
│   │   └── app-creator-agent.md       # → Applications Flask
│   │
│   ├── notebook/                       # Notebooks
│   │   └── jupyter-notebook-creator.md # → Notebooks Jupyter
│   │
│   ├── evaluation/                     # Évaluations
│   │   └── eval-builder.md            # → Construction évaluations
│   │
│   └── documentation/                  # Documentation
│       ├── fiche-technique-agent.md   # → Fiches techniques
│       └── student-prompt-builder.md  # → Prompts étudiants
│
├── outillage/                          # OUTILS TECHNIQUES
│   │
│   ├── latex/                          # Outils LaTeX
│   │   └── debug-tex-log.md           # → Débogage compilation
│   │
│   ├── extraction/                     # Extraction de données
│   │   ├── bo-competence-extractor.md # → Compétences BO
│   │   ├── bo-search-agent.md         # → Recherche BO
│   │   ├── programme-officiel-extractor.md # → Programmes officiels
│   │   ├── python-competences-extractor.md # → Compétences Python
│   │   └── mathalea-scraper.md        # → Exercices mathAlea
│   │
│   └── gestion/                        # Gestion planning
│       ├── prevision-seances-completer.md # → Prévisions séances
│       ├── seance-sequence-matcher.md # → Association séances
│       └── program-updater.md         # → Mise à jour programmes
│
├── experimental/                       # AGENTS EN DÉVELOPPEMENT
│   └── (vide pour le moment)
│
├── perso/                              # AGENTS PERSONNELS
│   └── (vide pour le moment)
│
└── meta/                               # MÉTA-AGENTS
    ├── error-investigator.md          # → Analyse erreurs
    ├── self-improvement-agent.md      # → Auto-amélioration
    ├── meta-low.md                    # → Modifications ciblées (haiku)
    ├── meta-mid.md                    # → Batch modifications simples (sonnet)
    └── meta-high.md                   # → Batch créations complexes (opus)
```

---

## Mapping Détaillé

### Créer / LaTeX
- [ ] `latex-main-worker` → `creer/latex/latex-main-worker.md`
- [ ] `latex-side-worker` → `creer/latex/latex-side-worker.md`
- [ ] `document-creator-worker` → `creer/latex/document-creator-worker.md`
- [ ] `beamer-worker` → `creer/latex/beamer-worker.md`
- [ ] `qcm-builder` → `creer/latex/qcm-builder.md`

### Créer / HTML
- [ ] `reveals-creator` → `creer/html/reveals-creator.md`
- [ ] `interactive-animation-creator` → `creer/html/interactive-animation-creator.md`
- [ ] `competence-presentation-generator` → `creer/html/competence-presentation-generator.md`

### Créer / Media
- [ ] `image-user` → `creer/media/image-user.md`

### Créer / Application
- [ ] `app-creator-agent` → `creer/application/app-creator-agent.md`

### Créer / Notebook
- [ ] `jupyter-notebook-creator` → `creer/notebook/jupyter-notebook-creator.md`

### Créer / Evaluation
- [ ] `eval-builder` → `creer/evaluation/eval-builder.md`

### Créer / Documentation
- [ ] `fiche-technique-agent` → `creer/documentation/fiche-technique-agent.md`
- [ ] `student-prompt-builder` → `creer/documentation/student-prompt-builder.md`

### Outillage / LaTeX
- [ ] `debug-tex-log` → `outillage/latex/debug-tex-log.md`

### Outillage / Extraction
- [ ] `bo-competence-extractor` → `outillage/extraction/bo-competence-extractor.md`
- [ ] `bo-search-agent` → `outillage/extraction/bo-search-agent.md`
- [ ] `programme-officiel-extractor` → `outillage/extraction/programme-officiel-extractor.md`
- [ ] `python-competences-extractor` → `outillage/extraction/python-competences-extractor.md`
- [ ] `mathalea-scraper` → `outillage/extraction/mathalea-scraper.md`

### Outillage / Gestion
- [ ] `prevision-seances-completer` → `outillage/gestion/prevision-seances-completer.md`
- [ ] `seance-sequence-matcher` → `outillage/gestion/seance-sequence-matcher.md`
- [ ] `program-updater` → `outillage/gestion/program-updater.md`

### Meta
- [ ] `error-investigator` → `meta/error-investigator.md`
- [ ] `self-improvement-agent` → `meta/self-improvement-agent.md`
- [x] `meta-low` → `meta/meta-low.md` (haiku - modifications ciblées)
- [x] `meta-mid` → `meta/meta-mid.md` (sonnet - batch modifications simples)
- [x] `meta-high` → `meta/meta-high.md` (opus - batch créations complexes)

---

## Résumé par catégorie

| Catégorie | Sous-catégories | Nb agents |
|-----------|-----------------|-----------|
| `creer/` | latex, html, media, application, notebook, evaluation, documentation | 14 |
| `outillage/` | latex, extraction, gestion | 9 |
| `experimental/` | - | 0 |
| `perso/` | - | 0 |
| `meta/` | error-investigator, self-improvement, meta-low, meta-mid, meta-high | 5 |
| **Total** | | **28** |

---

## Notes

- Les agents restent des fichiers `.md` uniques
- La structure miroir skills/commands/agents facilite la navigation
- `experimental/` et `perso/` sont prêts pour de futurs agents
