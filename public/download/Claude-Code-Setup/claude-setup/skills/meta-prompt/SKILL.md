---
name: meta-prompt
description: "Skill de creation, refactoring et optimisation de prompts. Ce skill devrait etre utilise quand l'utilisateur veut creer un nouveau prompt optimise, ameliorer un prompt existant, diagnostiquer la qualite d'un prompt, ou transformer une idee en prompt structure. Embarque 23 techniques de prompt engineering 2025-2026 (Anthropic, OpenAI, Google, Meta). Trois workflows : creation (6 phases avec idea-challenger + skill-creator), refactoring (diagnostic + amelioration), diagnostic (scoring 8 axes)."
---

# Meta-Prompt - Fabrique de Prompts Optimises

Skill central pour creer, refactorer et optimiser des prompts selon les techniques de pointe 2025-2026. Chaque prompt produit est transforme en livrable reutilisable (skill, agent ou commande).

## Declenchement

- Creer un nouveau prompt pour une tache specifique
- Ameliorer/refactorer un prompt existant
- Diagnostiquer la qualite d'un prompt
- Comprendre quelle technique appliquer selon un contexte
- Preparer un prompt avant de creer un skill ou un agent

## Trois workflows

### Workflow 1 : Creation (`/meta-prompt create`)

Pipeline complet en 6 phases obligatoires : clarification → techniques → specification → generation → diagnostic → livrable.

**Phases** :
1. **Challenger la demande** — Invoquer `idea-challenger` pour clarifier sur 7 dimensions
2. **Selectionner les techniques** — Choisir dans le catalogue selon la matrice de decision
3. **Specifier** — Formulaire HTML interactif ou AskUserQuestion structuree
4. **Generer** — Appliquer les techniques, produire le prompt structure
5. **Diagnostiquer** — Scoring automatique 8 axes, corriger les faiblesses
6. **Rendre utile** — Transformer en skill/agent/commande via `skill-creator` ou `agent-generator`

Consulter **`references/workflow-creation.md`** pour le detail complet de chaque phase.

### Workflow 2 : Refactoring (`/meta-prompt refactor`)

Amelioration d'un prompt existant en 4 phases : charger → diagnostiquer → appliquer techniques → presenter diff.

Consulter **`references/workflow-refactoring.md`** pour le detail complet.

### Workflow 3 : Diagnostic (`/meta-prompt diagnose`)

Evaluation et scoring d'un prompt sur 8 axes de qualite (1-5 par axe).

Consulter **`references/workflow-diagnostic.md`** pour le detail complet.

---

## Matrice de decision rapide

| Contexte | Techniques prioritaires |
|----------|------------------------|
| **Logiciel/Code** | Role expert + XML tags + CoT structure + Structured Output + ReAct |
| **Education/Cours** | Role pedagogique + Few-shot + CoT + Constitutional (verification) |
| **Analyse de donnees** | RAG + Structured Output + Self-Consistency + CoT |
| **Generation creative** | Role + Temperature guidance + Few-shot style + Constitutional |
| **Agent autonome** | System prompt architecture + ReAct + State management + Agentic 3-reminders |
| **Classification/Tri** | Structured Output + Few-shot + Zero-shot CoT |

## Structure obligatoire d'un prompt genere

Tout prompt produit par ce skill respecte cette structure :

```markdown
# [Titre descriptif]

## Role
[Role specifique, contextualise, oriente tache]

## Contexte
[Situation, public cible, cadre d'utilisation]

## Instructions
[Forme imperative, etape par etape, XML tags pour donnees variables]

## Contraintes
- [Positives : ce qui DOIT etre fait]
- [Negatives : ce qui NE DOIT PAS etre fait]

## Format de sortie
[Type, structure, longueur, schema]

## Exemples
[Minimum 2 paires entree/sortie si format precis]

## Variables
| Variable | Description | Defaut |
|----------|-------------|--------|
| `{{VAR}}` | Description | Valeur |

## Criteres de qualite (auto-verification)
- [ ] [Critere 1]
```

## Regles de generation

1. **XML tags** pour toute donnee variable : `<input>`, `<context>`, `<examples>`
2. **Forme imperative** : "Generer X", pas "Vous devez generer X"
3. **Variables** en `{{SCREAMING_SNAKE_CASE}}`
4. **Few-shot** : minimum 2 exemples si format de sortie precis
5. **CoT** : integrer "raisonner etape par etape" pour taches complexes
6. **Structured Output** : toujours specifier le format exact de sortie
7. **Constitutional** : criteres d'auto-verification en fin de prompt
8. **Primacy/Recency** : instructions critiques en debut ET en fin de prompt

## Scripts disponibles

### `scripts/diagnose_prompt.py`

Diagnostic automatique sur 8 axes de qualite.

```bash
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file prompt.md
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --text "Prompt inline..."
```

### `scripts/generate_form.py`

Formulaire HTML interactif pour specifier un prompt.

```bash
python .claude/skills/meta-prompt/scripts/generate_form.py --context "education-math" --output /tmp/prompt-workshop.html
```

Contextes : `education-math`, `software`, `agent`, `analysis`, `creative`, `custom`

## Integration avec autres skills

| Etape | Skill invoque | Quand |
|-------|---------------|-------|
| Clarification | `idea-challenger` | Creation, toujours (Phase 1) |
| Encapsulation skill | `skill-creator` | Phase 6, par defaut |
| Creation agent | `agent-generator` | Phase 6, si agent autonome |
| Contenu pedagogique | `bfcours-latex` | Si prompt genere du LaTeX educatif |

## Fichiers de reference

- **`references/workflow-creation.md`** — Workflow creation detaille (6 phases)
- **`references/workflow-refactoring.md`** — Workflow refactoring detaille (4 phases)
- **`references/workflow-diagnostic.md`** — Workflow diagnostic detaille (8 axes)
- **`references/techniques-catalogue.md`** — Catalogue complet des 23 techniques
- **`references/context-patterns.md`** — Templates et patterns par contexte (5 contextes)
