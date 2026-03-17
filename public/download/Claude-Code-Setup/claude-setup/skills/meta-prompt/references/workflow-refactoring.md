# Workflow de Refactoring — Detail des 4 Phases

Pipeline pour ameliorer un prompt existant. Diagnostic → corrections ciblees → validation.

---

## Phase 1 : Charger le prompt existant

Lire le fichier du prompt a ameliorer. Identifier :
- Ou il est utilise (skill, agent, commande, system prompt)
- Quel est son objectif declare
- Quelle est sa structure actuelle

Si le prompt n'a pas de fichier, demander a l'utilisateur de le coller ou de pointer vers le fichier.

---

## Phase 2 : Diagnostic complet

Executer le diagnostic automatique :

```bash
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file "{{FICHIER}}"
```

Le script evalue sur 8 axes (1-5 chacun, total /40). Voir `references/workflow-diagnostic.md` pour le detail des axes.

Analyser le rapport et identifier :
- Les axes forts (>= 4/5) — a preserver
- Les axes faibles (< 3/5) — priorite de correction
- Les axes moyens (3/5) — amelioration si le temps le permet

---

## Phase 3 : Appliquer les techniques manquantes

Pour chaque axe faible, appliquer la correction correspondante :

### Clarte (score < 3)

Problemes typiques :
- Instructions vagues ("faire quelque chose de bien")
- Ambiguites sur le format attendu
- Melange d'instructions et de donnees

Corrections :
- Restructurer en sections claires avec headings
- Reformuler en forme imperative
- Separer instructions et donnees avec XML tags
- Eliminer tout mot ambigu

### Specificite (score < 3)

Problemes typiques :
- Pas d'exemples
- Format de sortie non precise
- Variables en dur

Corrections :
- Ajouter 2-3 exemples few-shot entree/sortie
- Specifier le format exact de sortie (JSON schema, template)
- Extraire les variables en `{{SCREAMING_SNAKE_CASE}}`

### Structure (score < 3)

Problemes typiques :
- Bloc de texte monolithique
- Pas de sections
- Donnees melangees aux instructions

Corrections :
- Decouper en sections Role / Contexte / Instructions / Contraintes / Format / Exemples
- Envelopper les donnees variables dans des XML tags
- Ajouter des headings Markdown hierarchiques

### Raisonnement (score < 3)

Problemes typiques :
- Pas de guidance sur comment raisonner
- Tache complexe traitee en une seule instruction

Corrections :
- Ajouter "raisonner etape par etape" (Zero-Shot CoT)
- Decomposer en etapes numerotees
- Ajouter `<thinking>` / `<answer>` si tache complexe
- Considerer Tree-of-Thought si probleme de planification

### Robustesse (score < 3)

Problemes typiques :
- Pas de gestion des cas limites
- Pas de fallback si l'input est incomplet

Corrections :
- Ajouter des instructions pour les cas limites
- Prevoir des fallbacks ("si X n'est pas fourni, utiliser Y")
- Ajouter validation des inputs

### Reutilisabilite (score < 3)

Problemes typiques :
- Valeurs en dur dans le prompt
- Pas de parametrisation

Corrections :
- Extraire toute valeur en dur en variable `{{NOM}}`
- Ajouter un tableau de variables avec descriptions et defaults
- Rendre le prompt modulaire

### Verification (score < 3)

Problemes typiques :
- Pas d'auto-check
- Pas de criteres de qualite

Corrections :
- Ajouter une section "Criteres de qualite" avec checklist
- Integrer le pattern Constitutional AI (generer → critiquer → reviser)
- Ajouter des contraintes verifiables

### Concision (score < 3)

Problemes typiques :
- Redondances entre sections
- Instructions trop verbeuses
- Details inutiles

Corrections :
- Eliminer les phrases qui ne changent pas le comportement
- Fusionner les sections redondantes
- Deplacer les details en references si applicable
- Viser le ratio : chaque mot doit influencer la sortie

---

## Phase 4 : Presenter le diff

Montrer les changements avant/apres avec explications.

### Format de presentation

Pour chaque modification :
```
### [Axe ameliore] : [Description courte]

**Avant** :
> [Extrait original]

**Apres** :
> [Extrait modifie]

**Pourquoi** : [Technique appliquee et benefice attendu]
```

### Re-diagnostic

Apres toutes les corrections, re-executer le diagnostic :

```bash
python .claude/skills/meta-prompt/scripts/diagnose_prompt.py --file "{{FICHIER_CORRIGE}}"
```

Comparer les scores avant/apres. Si le score global reste < 28/40, iterer.

### Proposition de livrable

Si le prompt refactore n'est pas encore encapsule dans un skill/agent/commande, proposer la Phase 6 du workflow de creation pour le rendre reutilisable.
