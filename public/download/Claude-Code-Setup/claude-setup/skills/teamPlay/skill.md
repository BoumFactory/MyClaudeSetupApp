---
name: teamPlay
description: Orchestrate the QFStudio React agent team to port and build features collaboratively. This skill should be used when the user invokes /teamPlay followed by a task. Opus orchestrates, Sonnet agents code. No backend agent — Rust is untouched. Spawn multiple react-module agents in parallel for independent modules. Dispatch via module-specific skills (mod-*) for deep domain knowledge.
---

# TeamPlay — QFStudio Agent Team

Orchestrer l'equipe QFStudio pour auditer, corriger et ameliorer les features React.
Opus orchestre. Sonnet code. Zero agent backend — le Rust ne change pas.

## Skills specialises par module

Chaque module a un skill expert avec auto-memory. **Toujours injecter le skill dans le prompt de l'agent.**

| Module | Skill | Source QFgen | Commandes Rust | Fichiers React |
|--------|-------|-------------|----------------|----------------|
| Dashboard | `mod-dashboard` | dashboard.js (1289L) | 3 | 11 |
| Generator | `mod-generator` | generator.js (2457L) | 13 | 8 |
| Templates | `mod-templates` | templates.js (1969L) | 20 | 7 |
| Compilation | `mod-compilation` | compilation.js (1523L) | 7 | 6 |
| Evaluation | `mod-evaluation` | evaluation.js (2786L) | 24 | 10 |
| Planning | `mod-planning` | planning.js (2651L) | 25+ | 13 |
| Styles | `mod-styles` | style-designer.js (2174L) | 13 | 12 |
| Sharing | `mod-sharing` | sharing.js (821L) | 8 | 5 |
| Settings | `mod-settings` | settings.js (1426L) | 4 | 8 |

### Auto-Memory

Chaque skill a un dossier memoire : `.dev/module-memory/MODULE/STATUS.md`
L'agent lit STATUS.md en debut de tache et le met a jour en fin.
Cela permet de cumuler les connaissances entre sessions.

## L'equipe

### Agents de code (Sonnet)

| Nom | subagent_type | Domaine | Skill a injecter |
|-----|---------------|---------|------------------|
| `mod-dashboard` | `qfstudio-ui-coder` | Dashboard | `/mod-dashboard` |
| `mod-generator` | `qfstudio-ui-coder` | Generator | `/mod-generator` |
| `mod-templates` | `qfstudio-ui-coder` | Templates | `/mod-templates` |
| `mod-compilation` | `qfstudio-ui-coder` | Compilation | `/mod-compilation` |
| `mod-evaluation` | `qfstudio-ui-coder` | Evaluation | `/mod-evaluation` |
| `mod-planning` | `qfstudio-ui-coder` | Planning | `/mod-planning` |
| `mod-styles` | `qfstudio-ui-coder` | Style Designer | `/mod-styles` |
| `mod-sharing` | `qfstudio-ui-coder` | Sharing | `/mod-sharing` |
| `mod-settings` | `qfstudio-ui-coder` | Settings | `/mod-settings` |
| `shared-ui` | `qfstudio-ui-coder` | Composants partages | `/shadcn` |
| `tests` | `qfstudio-ui-coder` | Tests E2E Playwright | — |
| `reviewer` | `qfstudio-explorer` | Review lecture seule | — |

### Modules independants (parallelisables)

```
dashboard   styles   planning   sharing   settings
```

### Modules avec dependances (sequencer)

```
evaluation  compilation  templates  → dependent de questions (generator)
llm → transversal (hook partage)
```

## Workflow

### Phase 0 — Etat des lieux (coordinateur seul)

1. Lire `.dev/refacto-react/PROGRESS.md` pour l'etat global
2. Lire les STATUS.md de chaque module concerne dans `.dev/module-memory/*/STATUS.md`
3. Identifier les taches : audit parite / bugfix / amelioration UI

### Phase 1 — Dispatch (NOUVEAU — skill-aware)

Pour chaque tache, identifier le module concerne et spawner l'agent avec le bon skill.

#### Template de spawn agent module

```
Tu es l'agent expert du module MODULE pour QFStudio.

## Skill
Lire et appliquer : .claude/skills/mod-MODULE/SKILL.md

## Tache
[DESCRIPTION DE LA TACHE]

## Auto-Memory
1. Lire .dev/module-memory/MODULE/STATUS.md (creer si absent)
2. Executer la tache
3. Mettre a jour STATUS.md avec les resultats

## Regles
- Zero invoke() dans les composants
- Imports depuis @/api (jamais @/api/v1)
- Build doit passer : cd ui && npm run build
- Ne pas toucher au Rust
```

#### Exemples de dispatch

| Tache user | Module | Agent | Skill |
|------------|--------|-------|-------|
| "Les stats dashboard sont vides" | dashboard | mod-dashboard | `/mod-dashboard` |
| "Ajouter undo/redo au generateur" | generator | mod-generator | `/mod-generator` |
| "Les templates ne se chargent pas" | templates | mod-templates | `/mod-templates` |
| "Ameliorer le style designer" | styles | mod-styles | `/mod-styles` |
| "Auditer parite evaluation" | evaluation | mod-evaluation | `/mod-evaluation` |
| "Bug dans les settings LLM" | settings | mod-settings | `/mod-settings` |

### Phase 2 — Audit parite (mode special)

Quand le user demande un audit global :

1. Spawner les 9 agents en parallele (independants entre eux)
2. Chaque agent :
   a. Lit le JS source QFgen de son module
   b. Compare avec l'implementation React
   c. Remplit STATUS.md avec les resultats
3. Le coordinateur collecte les 9 STATUS.md et produit un rapport global

#### Template spawn audit

```
Tu es l'agent expert du module MODULE.

## Mission : Audit parite fonctionnelle

1. Lire .claude/skills/mod-MODULE/SKILL.md pour le contexte
2. Lire le fichier Vanilla JS source : D:\Applications\QFgen\ui\js\modules\SOURCE.js
3. Pour CHAQUE feature/fonction du JS, verifier sa presence dans les composants React
4. Lire les fichiers React dans ui/src/app/MODULE/
5. Remplir .dev/module-memory/MODULE/STATUS.md avec le resultat
6. Lister les features manquantes en fin de STATUS.md

NE PAS modifier le code. Lecture seule.
```

### Phase 3 — Fix / Improve (spawns cibles)

Apres l'audit, pour chaque feature manquante ou bug :

1. Spawner l'agent du module concerne
2. Lui donner le contexte depuis STATUS.md
3. L'agent corrige/ajoute la feature
4. Met a jour STATUS.md

### Phase 4 — Validation

```bash
cd D:/Applications/QFStudio/ui && npm run build
cd D:/Applications/QFStudio && npx playwright test
```

Si erreur → envoyer a l'agent concerne avec le message d'erreur.

### Phase 5 — Rapport

Generer un rapport depuis les 9 STATUS.md :

```markdown
# Rapport TeamPlay — [date]

## Parite globale
X features verifiees / Y totales

## Par module
| Module | Parite | Bugs fixes | Ameliorations |
|--------|--------|------------|---------------|
| Dashboard | 11/11 | 0 | 0 |
| Generator | 18/20 | 1 | 0 |
| ... | | | |
```

## Boundaries (regles absolues)

| Agent | Peut modifier | Ne touche JAMAIS |
|-------|--------------|-----------------|
| `mod-X` | `ui/src/app/X/` + `ui/src/api/v1/commands/X.ts` + `.dev/module-memory/X/` | Autres modules, shared/ui, src-tauri/ |
| `shared-ui` | `ui/src/shared/ui/` + `ui/src/components/ui/` | features/, api/, src-tauri/ |
| `tests` | `tests/e2e/` | ui/src/, src-tauri/ |
| `reviewer` | `.dev/reviews/` (lecture seule partout) | Tout code de prod |

`src-tauri/` : **intouchable par tous les agents.**

## Modes d'operation

### `/teamPlay audit`
Audit parite global → 9 agents paralleles → rapport

### `/teamPlay fix MODULE`
Fix bug dans un module specifique → 1 agent cible

### `/teamPlay improve MODULE`
Amelioration UI d'un module → 1 agent cible

### `/teamPlay audit+fix`
Audit puis correction automatique des features manquantes

### `/teamPlay all`
Audit global + fix + improve + tests + validation complete
