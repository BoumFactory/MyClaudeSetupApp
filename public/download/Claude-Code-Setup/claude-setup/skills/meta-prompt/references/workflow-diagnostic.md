# Workflow de Diagnostic — Les 8 Axes de Qualite

Evaluation et scoring d'un prompt sur 8 axes. Score total /40. Chaque axe note de 1 a 5.

---

## Utilisation

### Via script automatique

```bash
# Depuis un fichier
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file prompt.md

# Depuis du texte inline
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --text "Le prompt a evaluer..."

# Format JSON (pour integration pipeline)
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file prompt.md --format json
```

### Via analyse manuelle

Evaluer chaque axe selon la grille ci-dessous, noter de 1 a 5, totaliser.

---

## Grille d'evaluation detaillee

### Axe 1 : Clarte

| Score | Critere |
|-------|---------|
| 1 | Instructions vagues, ambigues, interpretables de plusieurs facons |
| 2 | Quelques instructions claires mais beaucoup d'implicite |
| 3 | Majorite des instructions explicites, quelques ambiguites |
| 4 | Instructions claires et explicites, tres peu d'ambiguite |
| 5 | Instructions explicites, non-ambigues, chaque phrase a un sens unique |

Indicateurs positifs : forme imperative, verbes d'action precis, pas de "si possible" / "eventuellement"

### Axe 2 : Specificite

| Score | Critere |
|-------|---------|
| 1 | Generique, applicable a tout, aucun exemple |
| 2 | Quelques details specifiques mais pas d'exemples |
| 3 | Details specifiques OU exemples (pas les deux) |
| 4 | Details specifiques ET exemples, format de sortie precis |
| 5 | Exemples diversifies, format detaille, cas limites couverts |

Indicateurs positifs : exemples entree/sortie, format de sortie avec schema, variables typees

### Axe 3 : Structure

| Score | Critere |
|-------|---------|
| 1 | Bloc de texte monolithique, pas de sections |
| 2 | Quelques paragraphes mais pas de structure claire |
| 3 | Sections identifiables, mais pas de separation donnees/instructions |
| 4 | Sections claires avec headings, donnees separees |
| 5 | Sections claires, XML tags, headings hierarchiques, separation complete |

Indicateurs positifs : headings Markdown, XML tags, sections Role/Contexte/Instructions/Format

### Axe 4 : Raisonnement

| Score | Critere |
|-------|---------|
| 1 | Pas de guidance de reflexion, instruction directe sans decomposition |
| 2 | Mention vague de "bien reflechir" sans structure |
| 3 | Etapes numerotees OU mention CoT |
| 4 | Etapes numerotees ET CoT integre |
| 5 | CoT structure avec `<thinking>`, decomposition logique, guidance de reflexion |

Indicateurs positifs : "raisonner etape par etape", etapes numerotees, balises thinking/answer

### Axe 5 : Robustesse

| Score | Critere |
|-------|---------|
| 1 | Aucune gestion d'erreurs ou cas limites |
| 2 | Mention d'un fallback isole |
| 3 | Quelques cas limites couverts |
| 4 | Cas limites principaux couverts, fallbacks definis |
| 5 | Gestion complete : erreurs, edge cases, inputs invalides, fallbacks |

Indicateurs positifs : "si X n'est pas fourni", "en cas d'erreur", validation inputs

### Axe 6 : Reutilisabilite

| Score | Critere |
|-------|---------|
| 1 | Valeurs en dur, prompt a usage unique |
| 2 | Quelques elements parametriques mais incomplet |
| 3 | Variables identifiees mais pas documentees |
| 4 | Variables en `{{}}` avec descriptions |
| 5 | Variables documentees avec types, defaults, tableau complet, modulaire |

Indicateurs positifs : `{{SCREAMING_SNAKE_CASE}}`, tableau de variables, defaults

### Axe 7 : Verification

| Score | Critere |
|-------|---------|
| 1 | Aucun critere d'auto-verification |
| 2 | Mention vague de "verifier" |
| 3 | Quelques criteres de qualite listes |
| 4 | Checklist de verification complete |
| 5 | Pattern Constitutional (generer → critiquer → reviser), criteres verifiables |

Indicateurs positifs : checklist `- [ ]`, etape de relecture, criteres mesurables

### Axe 8 : Concision

| Score | Critere |
|-------|---------|
| 1 | Tres verbeux, beaucoup de redondances, filler words |
| 2 | Quelques redondances, phrases inutilement longues |
| 3 | Globalement concis mais quelques passages superflus |
| 4 | Dense, peu de mots inutiles |
| 5 | Chaque mot influence la sortie, zero redondance, densite maximale |

Indicateurs negatifs : "il est important de noter que", "vous devez absolument", repetitions

---

## Interpretation des scores

### Score global

| Plage | Verdict | Action |
|-------|---------|--------|
| 35-40 | Excellent | Prompt pret a l'emploi. Encapsuler en livrable. |
| 28-34 | Bon | Corriger les axes < 4, re-diagnostiquer. |
| 20-27 | Moyen | Retravailler les axes < 3. Possible retour en Phase 2. |
| < 20 | Insuffisant | Refonte complete. Reprendre depuis Phase 1 (idea-challenger). |

### Profils typiques de prompts faibles

| Profil | Axes faibles typiques | Correction prioritaire |
|--------|----------------------|----------------------|
| "Prompt brut" | Structure, Specificite, Verification | Restructurer + exemples + checklist |
| "Prompt verbeux" | Concision, Structure | Eliminer redondances + XML tags |
| "Prompt rigide" | Reutilisabilite, Robustesse | Variables + fallbacks |
| "Prompt magique" | Clarte, Raisonnement | Forme imperative + CoT |

---

## Format du rapport de diagnostic

```markdown
## Diagnostic de prompt

**Fichier** : {{FICHIER}}
**Score global** : {{SCORE}}/40 — {{VERDICT}}

### Scores par axe

| Axe | Score | Commentaire |
|-----|-------|-------------|
| Clarte | X/5 | ... |
| Specificite | X/5 | ... |
| Structure | X/5 | ... |
| Raisonnement | X/5 | ... |
| Robustesse | X/5 | ... |
| Reutilisabilite | X/5 | ... |
| Verification | X/5 | ... |
| Concision | X/5 | ... |

### Points forts
- ...

### Ameliorations recommandees
1. [Axe] : [Technique a appliquer] — gain estime +X points
2. ...

### Gain potentiel
Score actuel : {{SCORE}}/40 → Score estime apres corrections : {{SCORE_ESTIME}}/40
```
