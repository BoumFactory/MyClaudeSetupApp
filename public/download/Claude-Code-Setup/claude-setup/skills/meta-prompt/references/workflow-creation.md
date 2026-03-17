# Workflow de Creation — Detail des 6 Phases

Pipeline complet pour creer un prompt optimise de zero. Toutes les phases sont obligatoires.

---

## Phase 1 : Challenger la demande (OBLIGATOIRE)

Invoquer le skill `idea-challenger` pour clarifier la demande avant toute generation.

Le skill idea-challenger va :
1. Analyser la demande sur 7 dimensions (Objectif, Public, Perimetre, Format, Contraintes, Contexte, Qualite)
2. Poser des questions iteratives pour lever les ambiguites
3. Produire une specification claire en markdown

Ne JAMAIS sauter cette phase. Un prompt genere sans clarification sera generique et peu utile.

---

## Phase 2 : Selection des techniques

Apres clarification, selectionner les techniques optimales selon le contexte.

### Matrice de decision

| Contexte | Techniques prioritaires |
|----------|------------------------|
| **Logiciel/Code** | Role expert + XML tags + CoT structure + Structured Output + ReAct |
| **Education/Cours** | Role pedagogique + Few-shot + CoT + Constitutional (verification) |
| **Analyse de donnees** | RAG + Structured Output + Self-Consistency + CoT |
| **Generation creative** | Role + Temperature guidance + Few-shot style + Constitutional |
| **Agent autonome** | System prompt architecture + ReAct + State management + Agentic 3-reminders |
| **Classification/Tri** | Structured Output + Few-shot + Zero-shot CoT |
| **Refactoring prompt** | Diagnostic → Techniques manquantes → Restructuration |

Consulter `references/techniques-catalogue.md` pour le catalogue complet des 23 techniques avec exemples.
Consulter `references/context-patterns.md` pour les templates par contexte.

### Processus de selection

1. Identifier le contexte principal dans la matrice
2. Verifier si des contextes secondaires s'appliquent
3. Lister les techniques selectionnees (3-6 techniques optimal)
4. Pour chaque technique, noter comment elle sera integree dans le prompt

---

## Phase 3 : Specification interactive (RECOMMANDEE)

Collecter les specifications detaillees du prompt via formulaire HTML ou CLI.

### Option A : Formulaire HTML

```bash
python .claude/skills/meta-prompt/scripts/generate_form.py --context "{{CONTEXTE}}" --output /tmp/prompt-workshop.html
```

Le formulaire propose :
- Sections pre-remplies cochees par defaut, decochables si non voulues
- Suggestions de reponse pour chaque champ
- Extraits de code/figures illustrant les patterns recommandes
- Export JSON des specifications

### Option B : CLI interactive

Utiliser `AskUserQuestion` avec des options structurees pour chaque dimension :

1. **Role** : Quel expert doit incarner l'IA ?
2. **Tache** : Que doit produire le prompt exactement ?
3. **Format** : Quel format de sortie (JSON, LaTeX, Markdown, texte libre) ?
4. **Exemples** : Disposez-vous d'exemples entree/sortie ?
5. **Contraintes** : Quelles regles absolues respecter ?
6. **Variables** : Quels elements doivent etre parametriques ?

---

## Phase 4 : Generation du prompt

Appliquer les techniques selectionnees pour generer le prompt final.

### Structure obligatoire

```markdown
# [Titre descriptif]

## Role
[Role specifique, contextualise, oriente tache]
[Traits de personnalite/expertise pertinents]

## Contexte
[Situation, public cible, cadre d'utilisation]

## Instructions
[Instructions en forme imperative, etape par etape]
[Utiliser des balises XML pour les donnees variables]
[Integrer CoT si tache complexe]

### Etape 1 : [Titre]
[Description precise avec sous-etapes si necessaire]

### Etape 2 : [Titre]
...

## Contraintes
- [Contraintes positives : ce qui DOIT etre fait]
- [Contraintes negatives : ce qui NE DOIT PAS etre fait]

## Format de sortie
[Format precis : type, structure, longueur]
[Schema JSON, exemple LaTeX, template markdown...]

## Exemples

### Entree
[Exemple d'input]

### Sortie attendue
[Exemple d'output]

## Variables

| Variable | Description | Defaut |
|----------|-------------|--------|
| `{{VAR}}` | Description | Valeur ou "obligatoire" |

## Criteres de qualite (auto-verification)
- [ ] [Critere 1]
- [ ] [Critere 2]
```

### Regles de generation

1. **XML tags** pour toute donnee variable : `<input>`, `<context>`, `<examples>`
2. **Forme imperative** : "Generer X", pas "Vous devez generer X"
3. **Variables** en `{{SCREAMING_SNAKE_CASE}}` pour tout element reutilisable
4. **Few-shot** : minimum 2 exemples si le format de sortie est precis
5. **CoT** : integrer "raisonner etape par etape" pour les taches complexes
6. **Structured Output** : toujours specifier le format exact de sortie
7. **Constitutional** : ajouter des criteres d'auto-verification en fin de prompt
8. **Primacy/Recency** : instructions critiques en debut ET en fin de prompt

---

## Phase 5 : Diagnostic automatique

Executer le script de diagnostic sur le prompt genere :

```bash
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file "{{FICHIER_PROMPT}}"
```

Le script evalue sur 8 axes (voir `references/workflow-diagnostic.md`).

### Seuils de qualite

| Score global | Verdict |
|-------------|---------|
| 35-40/40 | Excellent — passer en Phase 6 |
| 28-34/40 | Bon — corriger les axes < 4 puis Phase 6 |
| 20-27/40 | Moyen — retravailler les axes < 3, re-diagnostiquer |
| < 20/40 | Insuffisant — revenir en Phase 2 |

Pour chaque axe faible (< 3/5), appliquer la correction correspondante :

| Axe faible | Correction |
|------------|------------|
| Clarte | Restructurer, forme imperative, eliminer ambiguites |
| Specificite | Ajouter exemples few-shot, preciser format sortie |
| Structure | Appliquer XML tags, sections ordonnees, headings |
| Raisonnement | Integrer CoT, etapes numerotees |
| Robustesse | Ajouter gestion d'erreurs, fallbacks, cas limites |
| Reutilisabilite | Extraire variables `{{}}`, parametriser |
| Verification | Ajouter criteres auto-verification |
| Concision | Eliminer redondances, optimiser tokens |

Re-diagnostiquer apres corrections. Iterer jusqu'a score >= 28/40.

---

## Phase 6 : Rendre utile (OBLIGATOIRE)

Le prompt brut n'a aucune valeur s'il n'est pas encapsule dans un livrable reutilisable. Cette phase transforme le prompt en outil concret.

### Decision de livrable

| Le prompt est destine a... | Livrable | Skill a invoquer |
|---------------------------|----------|-----------------|
| Une tache repetitive avec variations | **Skill** | `skill-creator` |
| Piloter un agent autonome | **Agent** | `agent-generator` |
| Une action rapide en une commande | **Commande** `.claude/commands/` | Ecriture directe |
| Un system prompt d'application | **Fichier .md** | Ecriture directe |

### Workflow par defaut : Skill

Dans la majorite des cas, le prompt doit devenir un skill reutilisable :

1. Invoquer `skill-creator` avec le prompt genere comme input
2. Le skill-creator va :
   - Creer la structure `skills/NOM/SKILL.md`
   - Extraire les references dans `references/`
   - Creer les scripts si necessaire dans `scripts/`
   - Optimiser la description pour le triggering
3. Valider que le skill se declenche correctement

### Workflow agent

Si le prompt pilote un agent autonome :

1. Invoquer `agent-generator` avec le prompt
2. L'agent-generator va :
   - Creer le fichier agent `.claude/agents/NOM.md`
   - Configurer les outils, le modele, les contraintes
   - Tester le declenchement

### Workflow commande

Pour une action simple en une commande :

1. Creer `.claude/commands/NOM.md` avec le prompt
2. Tester avec `/NOM`

### Verification finale

Apres encapsulation, verifier :
- [ ] Le livrable se declenche sur les phrases attendues
- [ ] Le prompt genere est de qualite (score diagnostic >= 28/40)
- [ ] Les variables sont documentees
- [ ] Au moins un test d'utilisation reelle effectue
