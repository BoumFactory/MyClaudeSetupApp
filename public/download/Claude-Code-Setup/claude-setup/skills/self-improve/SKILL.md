---
name: self-improve
description: Skill d'auto-amélioration proactive. Ce skill doit être utilisé automatiquement en fin de tâche complexe pour analyser les difficultés rencontrées, proposer des améliorations ciblées aux skills/agents/commandes/scripts, et les appliquer après validation utilisateur. Utilisation obligatoire après chaque tâche non triviale.
---

# Skill d'Auto-amélioration Continue

Ce skill permet d'analyser les difficultés rencontrées pendant une tâche et de proposer des améliorations ciblées à la configuration Claude (skills, agents, commandes, scripts).

## Quand utiliser ce skill

- **Automatiquement** en fin de toute tâche non triviale
- Après avoir rencontré des erreurs ou des corrections multiples
- Quand l'utilisateur a dû intervenir pour corriger des actions
- Après une tâche complexe impliquant plusieurs outils/skills

## Workflow d'auto-amélioration

### Phase 1 : Collecte silencieuse pendant la tâche

Pendant l'exécution de la tâche principale, noter mentalement :

1. **Erreurs bash répétées** (même commande échoue 2+ fois)
2. **Corrections utilisateur** ("non", "c'est faux", modifications après actions)
3. **Outils mal utilisés** (paramètres manquants, mauvais format)
4. **Instructions manquantes** dans les skills/agents utilisés
5. **Étapes répétitives** qui auraient pu être automatisées
6. **Informations découvertes** qui auraient dû être documentées

### Phase 2 : Analyse en fin de tâche

Une fois la tâche principale terminée, effectuer l'analyse suivante :

#### Classification des problèmes détectés

Pour chaque problème, identifier :

| Catégorie | Fichiers concernés | Exemple |
|-----------|-------------------|---------|
| `script` | `.claude/scripts/*.py` | Bug dans fix_encoding_simple.py |
| `agent` | `.claude/agents/*.md` | Prompt insuffisant, étape oubliée |
| `skill` | `.claude/skills/*/SKILL.md` | Instructions manquantes, cas non géré |
| `command` | `.claude/commands/*.md` | Commande mal définie, paramètres flous |
| `hook` | `.claude/hooks/*` | Hook mal configuré |
| `global` | `CLAUDE.md` racine | Instruction globale à ajouter |

#### Sévérité des problèmes

- **high** : Bloque la tâche, nécessite intervention manuelle
- **medium** : Ralentit le workflow, génère des erreurs
- **low** : Petits irritants, améliorations de confort

### Phase 3 : Présentation à l'utilisateur

**Format obligatoire de présentation** :

```
## Analyse d'auto-amélioration

J'ai relevé [N] points d'amélioration potentiels pendant cette tâche :

### 1. [Titre court du problème] (sévérité: [high/medium/low])

**Constat** : [Ce qui s'est passé]
**Fichier concerné** : `[chemin/fichier]`
**Proposition** : [Modification précise proposée]

---

### 2. [Autre problème]
[...]

---

**Actions proposées :**
- [ ] Appliquer la correction 1
- [ ] Appliquer la correction 2
- [ ] Appliquer toutes les corrections
- [ ] Ignorer (ne rien modifier)
```

### Phase 4 : Application des corrections

Après validation utilisateur :

1. **Lire le fichier** avant modification (obligatoire)
2. **Comprendre la structure** existante
3. **Insérer** la correction au bon endroit (pas d'append brutal)
4. **Respecter** le style et le format du fichier
5. **Documenter** la raison du changement si pertinent

#### Règles d'insertion contextuelle

**Mauvais** (append brutal) :
```markdown
## Section ajoutée à la fin

Blabla...
```

**Bon** (insertion contextuelle) :
```markdown
[Identifier la section pertinente]
[Ajouter l'information à l'endroit logique]
[Maintenir la cohérence du document]
```

### Phase 5 : Logging (optionnel)

Si des erreurs significatives ont été rencontrées, les logger dans `.claude/logs/frequent-errors.jsonl` :

```jsonl
{"ts":"2026-01-01T10:30:00","type":"[type]","context":{"description":"[description]","file_affected":"[fichier]","action_taken":"[action]","outcome":"[résultat]","user_intervention":"[intervention utilisateur]","related_files":["[fichiers liés]"]},"scope":{"primary":"[script/agent/skill/command]","files_to_investigate":["[fichiers]"]},"severity":"[high/medium/low]","root_cause_hypothesis":"[hypothèse cause]"}
```

## Exemples de corrections types

### Correction d'un skill incomplet

**Problème** : Le skill `bfcours-latex` ne mentionne pas comment utiliser `\frquote{}` pour les citations françaises.

**Correction** : Ajouter dans la section appropriée du SKILL.md :
```markdown
### Citations françaises

Utiliser `\frquote{texte}` pour les citations avec guillemets français.
```

### Correction d'un agent qui oublie une étape

**Problème** : L'agent `latex-main-worker` oublie de compiler après modification.

**Correction** : Ajouter dans le workflow de l'agent :
```markdown
4. **Compiler le fichier maître** avec le skill tex-compiling-skill
5. Si erreur de compilation, corriger et recompiler
```

### Correction d'un script bugué

**Problème** : `fix_encoding_simple.py` détecte mal l'encodage cp1252 vs utf-8.

**Correction** : Modifier l'algorithme de scoring dans le script Python.

## Contraintes importantes

- **Ne jamais modifier** les fichiers de travail de l'utilisateur (.tex, .pdf, etc.)
- **Ne jamais supprimer** de configuration sans validation explicite
- **Toujours lire** les fichiers avant modification
- **Rester conservateur** : petites améliorations ciblées
- **Prioriser** les corrections high > medium > low
- **Proposer, pas imposer** : l'utilisateur valide toujours

## Intégration avec les commandes

Ce skill est conçu pour être activé automatiquement par la méta-commande `/do` en fin de tâche. Il peut aussi être invoqué manuellement après n'importe quelle tâche complexe.

## Rappel final

L'objectif est l'amélioration continue et non-intrusive du système. Chaque correction doit :
1. Résoudre un problème réel rencontré
2. S'intégrer harmonieusement dans la structure existante
3. Être validée par l'utilisateur avant application
4. Bénéficier aux futures sessions
