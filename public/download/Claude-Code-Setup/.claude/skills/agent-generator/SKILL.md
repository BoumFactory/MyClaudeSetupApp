---
name: agent-generator
description: Skill spécialisé pour créer des agents autonomes avec des prompts structurés et efficaces. Utiliser ce skill pour générer de nouveaux agents avec des capacités spécialisées (scraping, analyse, génération de contenu, etc.). Fournit templates, scripts d'initialisation et guidelines pour créer des agents robustes.
---

# Agent Generator Skill

Ce skill permet de créer des agents autonomes avec des prompts structurés et des capacités spécialisées.

## Quand utiliser ce skill

Utiliser ce skill lorsque :
- L'utilisateur demande de créer un nouvel agent pour une tâche spécifique
- Il faut automatiser une tâche complexe nécessitant plusieurs étapes
- Une spécialisation fonctionnelle est nécessaire (scraping, analyse, génération)
- Il faut déléguer une responsabilité à un agent autonome

## Processus de création d'agent

### Étape 1 : Comprendre le besoin

Avant de créer un agent, clarifier :
1. **Objectif principal** : Que doit faire l'agent ? (scraping, analyse, génération, transformation)
2. **Entrées attendues** : Quelles données l'agent reçoit-il ?
3. **Sorties attendues** : Quel est le format et le contenu des résultats ?
4. **Outils nécessaires** : Quels outils l'agent doit-il avoir (Read, Write, Bash, WebFetch, etc.) ?
5. **Contraintes** : Y a-t-il des limites, formats spécifiques, ou exigences ?

### Étape 2 : Initialiser l'agent

Utiliser le script `scripts/init_agent.py` pour créer la structure :

```bash
python .claude/skills/agent-generator/scripts/init_agent.py <agent-name> --output-dir .claude/agents
```

Le script crée :
- `<agent-name>.md` : Fichier de configuration avec frontmatter YAML et instructions
- Structure de base avec sections TODO à compléter

### Étape 3 : Définir les métadonnées

Remplir le frontmatter YAML avec :

```yaml
---
name: agent-name
description: Description concise de l'objectif de l'agent (50-150 mots)
model: sonnet  # ou haiku pour tâches simples et rapides
tools:
  - Read
  - Write
  - Bash
  - WebFetch  # Adapter selon les besoins
---
```

**Choix du modèle** :
- `haiku` : Tâches simples, rapides, peu coûteuses (scraping basique, transformations simples)
- `sonnet` : Tâches complexes nécessitant raisonnement approfondi (analyse, génération de contenu)

### Étape 4 : Structurer le prompt

Organiser le corps du fichier en sections claires :

#### 1. Rôle et contexte
```markdown
# Rôle

Tu es un agent spécialisé dans [DOMAINE]. Ta mission est de [OBJECTIF].
```

#### 2. Capacités et outils
```markdown
## Capacités

Tu disposes des outils suivants :
- **Read** : Pour lire les fichiers source
- **Write** : Pour écrire les résultats
- **WebFetch** : Pour récupérer du contenu web
- **Bash** : Pour exécuter des commandes (npm, python, etc.)
```

#### 3. Workflow détaillé
```markdown
## Processus de travail

### Étape 1 : [NOM_ETAPE]
[Instructions précises sur ce que l'agent doit faire]

### Étape 2 : [NOM_ETAPE]
[Instructions précises]
```

#### 4. Format de sortie
```markdown
## Format de sortie attendu

[Décrire le format exact des résultats : structure de fichier, format JSON, etc.]

Exemple :
\`\`\`json
{
  "resultat": "...",
  "metadata": {}
}
\`\`\`
```

#### 5. Gestion d'erreurs
```markdown
## Gestion des erreurs

Si [CONDITION], alors :
1. [ACTION]
2. [FALLBACK]

En cas d'échec complet :
- Documenter l'erreur dans le rapport final
- Proposer des solutions alternatives
```

### Étape 5 : Ajouter des exemples

Inclure des exemples concrets d'utilisation :

```markdown
## Exemples

### Exemple 1 : [CAS_USAGE]

**Entrée** :
\`\`\`
[Données d'entrée]
\`\`\`

**Sortie attendue** :
\`\`\`
[Résultat attendu]
\`\`\`
```

### Étape 6 : Tester l'agent

Après création, tester l'agent avec :

```javascript
// Dans la conversation
Task tool avec subagent_type="agent-name"
```

Vérifier :
- L'agent comprend son rôle
- Les outils sont correctement utilisés
- Le format de sortie est respecté
- Les erreurs sont gérées proprement

## Scripts disponibles

### `scripts/init_agent.py`

Script d'initialisation pour créer rapidement la structure d'un nouvel agent.

**Usage** :
```bash
python .claude/skills/agent-generator/scripts/init_agent.py <agent-name> --output-dir <path>
```

**Arguments** :
- `agent-name` : Nom de l'agent (kebab-case recommandé)
- `--output-dir` : Dossier de destination (par défaut : `.claude/agents`)

### `scripts/validate_agent.py`

Script de validation pour vérifier qu'un agent respecte les bonnes pratiques.

**Usage** :
```bash
python .claude/skills/agent-generator/scripts/validate_agent.py <path/to/agent.md>
```

**Vérifications** :
- Frontmatter YAML valide
- Présence des sections essentielles
- Qualité de la description
- Cohérence des outils listés

## Références

Consulter les fichiers de référence pour plus de détails :

- `references/agent-best-practices.md` : Bonnes pratiques pour créer des agents efficaces
- `references/agent-examples.md` : Exemples d'agents bien conçus
- `references/tools-reference.md` : Liste complète des outils disponibles pour les agents

## Bonnes pratiques

### Prompts clairs et spécifiques

- Utiliser un langage impératif et direct
- Éviter l'ambiguïté : spécifier exactement ce qui est attendu
- Donner des exemples concrets

### Modularité

- Un agent = une responsabilité principale
- Si l'agent devient trop complexe, envisager de créer plusieurs agents spécialisés

### Gestion d'erreurs robuste

- Anticiper les cas d'échec
- Prévoir des fallbacks
- Documenter les limites de l'agent

### Performance

- Utiliser `haiku` pour les tâches simples (coût réduit, vitesse accrue)
- Éviter de charger des fichiers volumineux inutilement
- Utiliser des outils spécialisés (Grep, Glob) plutôt que Bash quand possible

### Documentation

- La description doit être suffisamment détaillée pour comprendre quand utiliser l'agent
- Inclure des exemples d'utilisation
- Documenter les formats d'entrée/sortie

## Workflow complet : Création d'un agent

1. **Analyser le besoin** : Comprendre l'objectif et les contraintes
2. **Initialiser** : `python scripts/init_agent.py <name>`
3. **Configurer** : Remplir le frontmatter (model, tools, description)
4. **Structurer** : Écrire le prompt avec sections (Rôle, Processus, Format, Erreurs)
5. **Exemples** : Ajouter des cas d'usage concrets
6. **Valider** : `python scripts/validate_agent.py <agent.md>`
7. **Tester** : Utiliser l'agent via Task tool
8. **Itérer** : Améliorer selon les résultats

## Notes importantes

- Les agents héritent du contexte général (CLAUDE.md) mais ne peuvent pas voir les conversations précédentes
- Les agents sont stateless : chaque invocation est indépendante
- Les agents retournent un seul message final : concevoir le workflow en conséquence
- Privilégier l'autonomie : l'agent doit pouvoir accomplir sa tâche sans intervention
