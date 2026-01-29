# Architecture des Skills

> **Fichier généré automatiquement** par `generate_skills_architecture.py`
> Dernière génération : 2026-01-27 17:22
> **Complété manuellement** : 2026-01-27
>
> Ce fichier sert de base pour réorganiser les skills en structure hiérarchique.

---

## Inventaire Automatique des Skills (36 skills)

| Skill | Description courte |
|-------|-------------|
| `agent-generator` | Création d'agents autonomes |
| `bareme-actions-eleves` | Barèmes basés sur actions élèves |
| `beamer-presentation` | Diaporamas Beamer (LaTeX) |
| `bfcours-latex` | Édition documents LaTeX bfcours |
| `cahier-de-textes` | Gestion cahier de textes Electron |
| `canvas-design` | Création visuelle (posters, art) |
| `docx` | Documents Word |
| `educational-app-builder` | Applications Flask éducatives |
| `html-katex-compiler` | Cours HTML interactifs KaTeX |
| `icons-generator` | Génération d'icônes (Imagen) |
| `image-generator` | Génération d'images (Gemini) |
| `infography-generator` | Infographies éducatives |
| `interactive-animation` | Animations HTML/JS interactives |
| `jupyter-notebook` | Notebooks Jupyter pédagogiques |
| `latex-geometry` | Figures géométriques TikZ |
| `latex-package-search` | Recherche définitions LaTeX |
| `make-blueprint-eval` | Blueprints d'évaluations HTML |
| `mind-map-creator` | Cartes mentales Markdown |
| `moodle-cloze` | Questions Cloze Moodle |
| `moodle-course-creator` | Cours Moodle complets (.mbz) |
| `odt` | Documents OpenDocument |
| `pdf` | Manipulation PDF |
| `pisa-resource` | Recherche ressources PISA |
| `pptx` | Présentations PowerPoint |
| `problematheque-search` | Recherche problèmes maths |
| `programmes-officiels` | Programmes Éducation Nationale |
| `qcm-creator` | QCM LaTeX bfcours |
| `reveals-presentation` | Présentations Reveal.js |
| `routine-matin` | Journal d'actualités quotidien |
| `self-improve` | Auto-amélioration proactive |
| `skill-creator` | Création de skills |
| `tex-compiling-skill` | Compilation LaTeX |
| `tex-document-creator` | Création documents LaTeX |
| `tex-fiche-technique` | Fiches techniques pédagogiques |
| `vocal-correction` | Corrections depuis transcriptions |
| `xlsx` | Feuilles de calcul Excel |

---

## Architecture Proposée

```
.claude/skills/
│
├── creer/                              # CRÉATION DE CONTENU
│   │
│   ├── latex/                          # Documents LaTeX
│   │   ├── bfcours/                   # → bfcours-latex (édition générale)
│   │   ├── diaporama/                 # → beamer-presentation
│   │   ├── qcm/                       # → qcm-creator
│   │   ├── geometrie/                 # → latex-geometry (TikZ)
│   │   ├── fiche-technique/           # → tex-fiche-technique
│   │   └── nouveau/                   # → tex-document-creator (templates)
│   │
│   ├── html/                           # Documents Web
│   │   ├── diaporama/                 # → reveals-presentation
│   │   ├── animation/                 # → interactive-animation
│   │   ├── cours/                     # → html-katex-compiler
│   │   ├── blueprint/                 # → make-blueprint-eval
│   │   └── carte-mentale/             # → mind-map-creator
│   │
│   ├── moodle/                         # Contenus Moodle
│   │   ├── qcm/                       # → moodle-cloze
│   │   └── cours/                     # → moodle-course-creator
│   │
│   ├── office/                         # Documents Office
│   │   ├── word/                      # → docx
│   │   ├── excel/                     # → xlsx
│   │   ├── powerpoint/                # → pptx
│   │   ├── libreoffice/               # → odt
│   │   └── pdf/                       # → pdf
│   │
│   ├── media/                          # Contenus visuels
│   │   ├── image/                     # → image-generator (Gemini)
│   │   ├── icone/                     # → icons-generator (Imagen)
│   │   └── infographie/               # → infography-generator
│   │
│   ├── application/                    # Applications
│   │   └── flask/                     # → educational-app-builder
│   │
│   └── jupyter/                        # Notebooks Jupyter
│       └── python/                    # → jupyter-notebook
│
├── outillage/                          # OUTILS TECHNIQUES
│   │
│   ├── latex/                          # Outils LaTeX
│   │   └── compilation/               # → tex-compiling-skill
│   │
│   ├── ressources/                     # Recherche de ressources
│   │   └── programmes-bo/             # → programmes-officiels
│   │
│   └── evaluation/                     # Outils d'évaluation
│       └── bareme/                    # → bareme-actions-eleves
│
├── modifier/                           # MODIFICATION DE CONTENU (à venir)
│   └── (vide pour le moment)
│
├── experimental/                       # SKILLS EN DÉVELOPPEMENT
│   ├── vocal-correction/              # → vocal-correction
│   ├── cahier-de-textes/              # → cahier-de-textes
│   ├── latex-package-search/          # → latex-package-search
│   ├── canvas-design/                 # → canvas-design
│   ├── problematheque-search/         # → problematheque-search
│   └── pisa-resource/                 # → pisa-resource
│
├── perso/                              # SKILLS PERSONNELS
│   └── routine-matin/                 # → routine-matin
│
└── meta/                               # MÉTA-SKILLS
    ├── skill-creator/                 # → skill-creator
    ├── agent-generator/               # → agent-generator
    └── self-improve/                  # → self-improve
```

---

## Mapping Détaillé

### Créer / LaTeX
- [x] `bfcours-latex` → `creer/latex/bfcours/`
- [x] `beamer-presentation` → `creer/latex/diaporama/`
- [x] `qcm-creator` → `creer/latex/qcm/`
- [x] `latex-geometry` → `creer/latex/geometrie/`
- [x] `tex-fiche-technique` → `creer/latex/fiche-technique/`
- [x] `tex-document-creator` → `creer/latex/nouveau/`

### Créer / HTML
- [x] `reveals-presentation` → `creer/html/diaporama/`
- [x] `interactive-animation` → `creer/html/animation/`
- [x] `html-katex-compiler` → `creer/html/cours/`
- [x] `make-blueprint-eval` → `creer/html/blueprint/`
- [x] `mind-map-creator` → `creer/html/carte-mentale/`

### Créer / Moodle
- [x] `moodle-cloze` → `creer/moodle/qcm/`
- [x] `moodle-course-creator` → `creer/moodle/cours/`

### Créer / Office
- [x] `docx` → `creer/office/word/`
- [x] `xlsx` → `creer/office/excel/`
- [x] `pptx` → `creer/office/powerpoint/`
- [x] `odt` → `creer/office/libreoffice/`
- [x] `pdf` → `creer/office/pdf/`

### Créer / Media
- [x] `image-generator` → `creer/media/image/`
- [x] `icons-generator` → `creer/media/icone/`
- [x] `infography-generator` → `creer/media/infographie/`

### Créer / Application
- [x] `educational-app-builder` → `creer/application/flask/`

### Créer / Jupyter
- [x] `jupyter-notebook` → `creer/jupyter/python/`

### Outillage / LaTeX
- [x] `tex-compiling-skill` → `outillage/latex/compilation/`

### Outillage / Ressources
- [x] `programmes-officiels` → `outillage/ressources/programmes-bo/`

### Outillage / Evaluation
- [x] `bareme-actions-eleves` → `outillage/evaluation/bareme/`

### Experimental
- [x] `vocal-correction` → `experimental/vocal-correction/`
- [x] `cahier-de-textes` → `experimental/cahier-de-textes/`
- [x] `latex-package-search` → `experimental/latex-package-search/`
- [x] `canvas-design` → `experimental/canvas-design/`
- [x] `problematheque-search` → `experimental/problematheque-search/`
- [x] `pisa-resource` → `experimental/pisa-resource/`

### Perso
- [x] `routine-matin` → `perso/routine-matin/`

### Meta
- [x] `skill-creator` → `meta/skill-creator/`
- [x] `agent-generator` → `meta/agent-generator/`
- [x] `self-improve` → `meta/self-improve/`

---

## Résumé par catégorie

| Catégorie | Sous-catégories | Nb skills |
|-----------|-----------------|-----------|
| `creer/` | latex, html, moodle, office, media, application, jupyter | 24 |
| `outillage/` | latex, ressources, evaluation | 3 |
| `experimental/` | - | 6 |
| `perso/` | - | 1 |
| `meta/` | - | 3 |
| **Total** | | **37** |

---

## Notes

- **Noms de dossiers** : français sans accents
- **Structure** : 3 niveaux max (action / type / variante)
- **Un skill = un dossier terminal** contenant `SKILL.md` + scripts éventuels
- **Rétrocompatibilité** : les anciens chemins peuvent être redirigés via symlinks ou aliases

## Prochaines étapes

1. [ ] Valider cette architecture
2. [ ] Créer le script de migration
3. [ ] Mettre à jour les références dans les commandes/agents
4. [ ] Tester que tout fonctionne
