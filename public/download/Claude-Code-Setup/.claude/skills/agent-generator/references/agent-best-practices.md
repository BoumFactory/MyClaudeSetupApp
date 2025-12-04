# Bonnes pratiques pour créer des agents efficaces

## Principes fondamentaux

### 1. Un agent = une responsabilité

Chaque agent doit avoir une mission claire et bien définie. Si un agent devient trop complexe avec plusieurs responsabilités, le diviser en plusieurs agents spécialisés.

**Bon exemple** :
- Agent scraper mathAlea : récupère les exercices
- Agent analyzer : analyse les exercices récupérés
- Agent formatter : formate les exercices au format LaTeX

**Mauvais exemple** :
- Agent tout-en-un qui scrape, analyse, formate, et compile

### 2. Prompts impératifs et sans ambiguïté

Utiliser un langage direct et impératif. Éviter les formulations vagues.

**Bon exemple** :
```
## Étape 1 : Extraire les métadonnées

1. Lire le fichier source avec Read tool
2. Parser le contenu JSON
3. Extraire les champs : titre, niveau, theme
4. Valider que chaque champ est non vide
```

**Mauvais exemple** :
```
Tu devrais essayer de récupérer les métadonnées du fichier si possible.
```

### 3. Gestion d'erreurs exhaustive

Anticiper tous les cas d'échec possibles et prévoir des fallbacks.

**Structure recommandée** :
```markdown
## Gestion des erreurs

### Erreur : Fichier introuvable
**Cause** : Le fichier spécifié n'existe pas
**Action** :
1. Vérifier le chemin avec Bash ls
2. Proposer des chemins alternatifs avec Glob
3. Si aucun fichier trouvé, retourner une erreur claire

### Erreur : Format invalide
**Cause** : Le contenu ne respecte pas le format attendu
**Action** :
1. Logger l'erreur avec le contenu problématique
2. Essayer de parser avec un format alternatif
3. Si échec, retourner les données brutes avec avertissement
```

### 4. Format de sortie structuré

Toujours définir un format de sortie clair, idéalement JSON pour faciliter le parsing.

**Bon exemple** :
```json
{
  "status": "success",
  "data": {
    "exercises": [
      {
        "id": "ex001",
        "title": "Fractions",
        "latex": "\\frac{1}{2}",
        "metadata": {
          "niveau": "5eme",
          "theme": "nombres"
        }
      }
    ]
  },
  "errors": [],
  "summary": {
    "total_processed": 10,
    "successful": 9,
    "failed": 1
  }
}
```

### 5. Autonomie maximale

Un agent doit pouvoir accomplir sa tâche de bout en bout sans intervention manuelle.

**À éviter** :
- "Demander à l'utilisateur de..."
- "Attendre une confirmation avant de..."

**À privilégier** :
- Prendre des décisions basées sur des heuristiques claires
- Retourner un rapport détaillé permettant à l'utilisateur de vérifier a posteriori

## Choix du modèle

### Utiliser `haiku` pour :
- Tâches simples et répétitives
- Scraping de données structurées
- Transformations de format basiques
- Validation de données
- Extraction d'informations avec patterns clairs

**Avantages** : Rapide, économique, suffisant pour des tâches bien définies

### Utiliser `sonnet` pour :
- Analyse complexe nécessitant compréhension contextuelle
- Génération de contenu créatif ou pédagogique
- Résolution de problèmes avec plusieurs approches possibles
- Raisonnement multi-étapes avec décisions conditionnelles

**Avantages** : Compréhension approfondie, meilleure gestion de l'ambiguïté

### Utiliser `opus` pour :
- Tâches exceptionnellement complexes
- Raisonnement critique avec enjeux importants

**Note** : Opus est rarement nécessaire ; sonnet suffit dans la plupart des cas.

## Utilisation optimale des outils

### Préférer les outils spécialisés

**Bon** :
- `Glob("**/*.tex")` pour trouver des fichiers
- `Grep("\\section", pattern="*.tex")` pour chercher dans des fichiers
- `Read(file)` pour lire un fichier

**Mauvais** :
- `Bash("find . -name '*.tex'")` au lieu de Glob
- `Bash("grep 'section' *.tex")` au lieu de Grep
- `Bash("cat file.txt")` au lieu de Read

### Paralléliser les opérations indépendantes

Si plusieurs opérations sont indépendantes, les exécuter en parallèle.

**Bon exemple** :
```markdown
## Étape 1 : Collecte des données

Exécuter en parallèle :
1. Read("source1.json") pour les métadonnées
2. Read("source2.json") pour les exercices
3. WebFetch("https://api.example.com/config") pour la configuration
```

## Structure de workflow

### Workflow linéaire simple

Pour des tâches séquentielles :

```markdown
## Processus de travail

### Étape 1 : Préparation
[Instructions]

### Étape 2 : Traitement
[Instructions]

### Étape 3 : Finalisation
[Instructions]
```

### Workflow conditionnel

Pour des tâches avec embranchements :

```markdown
## Processus de travail

### Étape 1 : Analyse initiale
1. Lire le fichier source
2. Détecter le format :
   - Si JSON → Aller à Étape 2A
   - Si XML → Aller à Étape 2B
   - Si texte brut → Aller à Étape 2C

### Étape 2A : Traitement JSON
[Instructions spécifiques JSON]

### Étape 2B : Traitement XML
[Instructions spécifiques XML]

### Étape 2C : Traitement texte
[Instructions spécifiques texte]

### Étape 3 : Normalisation
[Instructions communes à tous les formats]
```

### Workflow itératif

Pour des tâches sur plusieurs éléments :

```markdown
## Processus de travail

### Étape 1 : Initialisation
1. Lire la liste des fichiers à traiter
2. Créer un rapport vide

### Étape 2 : Traitement itératif

Pour chaque fichier :
1. Lire le contenu
2. Extraire les données
3. Valider les données
4. Ajouter au rapport

### Étape 3 : Consolidation
1. Agréger tous les résultats
2. Calculer les statistiques
3. Écrire le rapport final
```

## Documentation et exemples

### Exemples concrets obligatoires

Toujours inclure au moins 2 exemples d'utilisation réelle.

**Structure recommandée** :
```markdown
## Exemples

### Exemple 1 : Cas simple

**Contexte** : Scraper un exercice sur les fractions
**Entrée** : URL https://coopmaths.fr/alea/?id=5N10
**Commande** : `Task(subagent_type="mathalea-scraper", prompt="Récupérer l'exercice 5N10")`
**Sortie attendue** :
\`\`\`json
{
  "status": "success",
  "data": {
    "id": "5N10",
    "latex": "...",
    "metadata": {...}
  }
}
\`\`\`

### Exemple 2 : Cas avec erreur

**Contexte** : Exercice inexistant
**Entrée** : URL invalide
**Sortie attendue** :
\`\`\`json
{
  "status": "error",
  "message": "Exercice introuvable",
  "suggestions": [...]
}
\`\`\`
```

### Notes et limitations

Documenter explicitement les limites :

```markdown
## Notes et limitations

- L'agent ne peut scraper que les exercices publics (pas de contenu premium)
- Le parsing peut échouer si la structure HTML change
- Limite de 100 exercices par session pour éviter la surcharge
- Les images doivent être téléchargées séparément
```

## Tests et validation

### Checklist avant déploiement

- [ ] Le frontmatter YAML est valide
- [ ] La description est claire et complète
- [ ] Les outils listés sont utilisés dans le workflow
- [ ] Tous les TODOs ont été remplacés
- [ ] Au moins 2 exemples sont fournis
- [ ] Les erreurs principales sont gérées
- [ ] Le format de sortie est défini
- [ ] L'agent a été testé sur un cas réel
- [ ] Les limitations sont documentées

### Validation avec script

```bash
python .claude/skills/agent-generator/scripts/validate_agent.py <agent.md>
```

## Anti-patterns à éviter

### ❌ Prompts trop verbeux

Ne pas sur-expliquer ou ajouter du contexte inutile.

**Mauvais** :
```
Tu es un agent très intelligent qui va aider à scraper le site mathAlea.
C'est un site très important pour les enseignants car il contient plein
d'exercices. Tu vas devoir utiliser tes compétences pour...
```

**Bon** :
```
Tu es un agent spécialisé dans le scraping du site mathAlea (https://coopmaths.fr/alea/).
Ta mission est d'extraire les exercices au format LaTeX.
```

### ❌ Dépendances non documentées

Toujours lister les dépendances externes.

**Bon** :
```markdown
## Dépendances

- Python 3.8+
- npm package `puppeteer` (pour le scraping JavaScript)
- Accès réseau à coopmaths.fr
```

### ❌ Formats de sortie implicites

Le format doit être explicite, pas "deviné".

**Mauvais** :
```
Retourne les exercices dans un format approprié.
```

**Bon** :
```
Retourne un fichier JSON avec la structure suivante :
\`\`\`json
{
  "exercises": [...]
}
\`\`\`
```

### ❌ Gestion d'erreurs absente

Ne jamais ignorer les cas d'erreur.

**Mauvais** :
```
1. Récupérer le contenu de l'URL
2. Parser le HTML
3. Extraire les exercices
```

**Bon** :
```
1. Récupérer le contenu de l'URL
   - En cas d'erreur réseau : retourner {status: "error", message: "Network error"}
2. Parser le HTML
   - En cas de structure invalide : logger et retourner les données brutes
3. Extraire les exercices
   - Si aucun exercice trouvé : retourner tableau vide avec avertissement
```

## Itération et amélioration

### Signaux qu'un agent doit être amélioré

- L'agent échoue fréquemment sur certains cas
- L'utilisateur doit souvent corriger les sorties
- Le prompt est devenu trop complexe (>500 lignes)
- Plusieurs responsabilités mélangées

### Processus d'amélioration

1. **Analyser les échecs** : Logger les cas d'erreur
2. **Identifier les patterns** : Quels types d'erreurs reviennent ?
3. **Modifier le prompt** : Ajouter des instructions pour ces cas
4. **Tester** : Valider sur les cas problématiques
5. **Documenter** : Ajouter dans les exemples ou limitations

### Versioning

Considérer de versionner les agents critiques :

```
.claude/agents/
├── mathalea-scraper.md          # Version actuelle
├── mathalea-scraper-v1.md       # Backup version 1
└── mathalea-scraper-v2.md       # Backup version 2
```
