---
description: Lance un agent d'investigation en arrière-plan pour analyser les erreurs et corriger automatiquement la configuration
tags: [meta, investigation, background, auto-correction]
---

# Investigation et auto-correction en arrière-plan

Cette commande lance l'agent d'investigation qui analyse les logs d'erreurs et la conversation actuelle pour identifier et corriger les problèmes de configuration.

## Comment ça fonctionne

1. **Hook de logging** : Un hook PostToolUse enregistre automatiquement les erreurs d'agents dans `.claude/agent-errors.log`

2. **Agent d'investigation** : Analyse les logs + conversation pour identifier les causes racines

3. **Corrections automatiques** : Implémente directement les corrections évidentes (validations, gestion d'erreurs)

4. **Propositions** : Suggère les corrections nécessitant validation dans `amelioration-proposals.md`

## Instructions

Lance l'agent `error-investigator-agent` en arrière-plan avec le Task tool :

**Prompt pour l'agent** :

```
Lance une investigation complète des erreurs loguées et de la conversation actuelle.

## Données à analyser

1. **Fichier de logs d'erreurs** : `.claude/agent-errors.log`
   - Format JSONL
   - Contient les erreurs loguées par le hook PostToolUse
   - Chaque ligne = une erreur avec timestamp, type, message, contexte

2. **Conversation actuelle** :
   - Récupère le fichier JSONL le plus récent avec :
   ```bash
   powershell -Command "Get-ChildItem -Path \"C:\Users\Utilisateur\.claude\projects\C--Users-Utilisateur-Documents-Professionnel-1--Reims-2025---2026\" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Select-Object -ExpandProperty Name"
   ```
   - Chemin complet : `C:\Users\Utilisateur\.claude\projects\C--Users-Utilisateur-Documents-Professionnel-1--Reims-2025---2026\[nom-fichier].jsonl`

3. **Configuration actuelle** :
   - `.claude/agents/` - Prompts des agents
   - `.claude/skills/` - Skills disponibles
   - `.claude/commands/` - Commandes slash
   - `CLAUDE.md` - Instructions globales

## Objectifs

1. **Analyser** chaque erreur loguée et déterminer sa cause racine
2. **Tracer** le chemin de l'erreur (utilisateur → commande → agent → tool → erreur)
3. **Identifier** quel élément de configuration aurait dû prévenir l'erreur
4. **Corriger** automatiquement les problèmes évidents :
   - Ajouter des validations manquantes dans les prompts d'agents
   - Ajouter de la gestion d'erreurs
   - Documenter les erreurs connues dans les skills
   - Améliorer les messages d'erreur
5. **Proposer** les corrections nécessitant validation dans `amelioration-proposals.md`
6. **Prévenir** la récurrence en anticipant les erreurs similaires

## Format du rapport

Crée `amelioration-proposals.md` à la racine avec :
- Investigation détaillée de chaque erreur
- Causes racines identifiées
- Corrections implémentées automatiquement (avec diff)
- Corrections proposées nécessitant validation
- Recommandations préventives
- Métriques (erreurs résolues, taux de correction auto, etc.)

## Contraintes

- ❌ Ne modifie JAMAIS les fichiers de travail (.tex, .pdf, etc.)
- ✅ Garde TOUJOURS l'historique des modifications en commentaire
- ✅ Documente TOUJOURS pourquoi chaque changement est fait
- ✅ Implémente directement les corrections évidentes (validations, gestion d'erreurs)
- ⚠️ Propose (sans implémenter) les changements de comportement

## Critères de succès

- Chaque erreur loguée est investiguée avec cause racine identifiée
- Au moins 70% des erreurs ont une correction implémentée ou proposée
- Aucune régression introduite
- Documentation claire pour chaque modification

Travaille de manière autonome, méthodique et exhaustive.
```

**Subagent type** : `general-purpose`

## Résultats attendus

L'agent créera :
- `amelioration-proposals.md` - Rapport complet d'investigation et corrections
- Modifications directes dans `.claude/agents/`, `.claude/skills/`, etc. (corrections évidentes)

## Après l'exécution

1. Lire `amelioration-proposals.md`
2. Valider et implémenter les corrections proposées si pertinentes
3. Relancer `/background` après quelques sessions pour vérifier l'efficacité

## Note sur le système de logging

Le hook PostToolUse est configuré dans `.claude/settings.json` :
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/log-agent-errors.js\""
          }
        ]
      }
    ]
  }
}
```

Le hook s'exécute après **TOUS les outils** (Task, Bash, Edit, Write, etc.) et détecte automatiquement :
- Erreurs LaTeX
- Erreurs de compilation
- Erreurs Bash (command not found, permission denied, etc.)
- Erreurs d'outils (Edit, Write, Read)
- Erreurs Python (Traceback, Exception)
- Erreurs Node.js
- Dépendances manquantes
- Échecs d'agents
