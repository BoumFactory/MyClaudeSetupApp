# Référence des outils disponibles pour les agents

Ce document liste tous les outils que les agents peuvent utiliser avec leurs capacités et cas d'usage.

## Outils de manipulation de fichiers

### Read

**Description** : Lit le contenu d'un fichier local

**Paramètres** :
- `file_path` (requis) : Chemin absolu vers le fichier
- `offset` (optionnel) : Ligne de début (pour fichiers volumineux)
- `limit` (optionnel) : Nombre de lignes à lire

**Formats supportés** :
- Fichiers texte (.txt, .md, .tex, .py, .js, etc.)
- Images (.png, .jpg, .pdf) - affichage visuel
- PDF - extraction page par page
- Jupyter notebooks (.ipynb)

**Quand utiliser** :
- Lire le contenu d'un fichier spécifique
- Analyser du code ou du contenu structuré
- Extraire des informations d'un document

**Bonnes pratiques** :
- Utiliser Read plutôt que `Bash("cat file.txt")`
- Pour les gros fichiers, utiliser offset/limit
- Toujours vérifier que le fichier existe avant lecture

**Exemple** :
```markdown
1. Lire le fichier source avec Read("data/exercises.json")
2. Parser le contenu JSON
3. Extraire les exercices
```

---

### Write

**Description** : Écrit ou écrase un fichier local

**Paramètres** :
- `file_path` (requis) : Chemin absolu du fichier
- `content` (requis) : Contenu à écrire

**Quand utiliser** :
- Créer un nouveau fichier
- Écraser complètement un fichier existant
- Écrire des résultats, rapports, ou données générées

**Bonnes pratiques** :
- TOUJOURS lire le fichier avant de l'écraser s'il existe
- Utiliser Edit plutôt que Write pour des modifications partielles
- Vérifier que le dossier parent existe

**Exemple** :
```markdown
1. Générer le contenu Markdown
2. Écrire avec Write("output/result.md", content)
```

**⚠️ Attention** :
- Write écrase le contenu existant sans avertissement
- Ne pas utiliser pour des modifications partielles

---

### Edit

**Description** : Remplace une chaîne spécifique dans un fichier

**Paramètres** :
- `file_path` (requis) : Chemin du fichier
- `old_string` (requis) : Texte à remplacer (doit être unique)
- `new_string` (requis) : Texte de remplacement
- `replace_all` (optionnel) : Remplacer toutes les occurrences

**Quand utiliser** :
- Modification ciblée d'un fichier
- Remplacement de valeurs spécifiques
- Mise à jour de configuration

**Bonnes pratiques** :
- TOUJOURS lire le fichier avec Read avant Edit
- S'assurer que `old_string` est unique (sinon utiliser `replace_all: true`)
- Préserver l'indentation exacte

**Exemple** :
```markdown
1. Read("config.json") pour voir le contenu
2. Edit("config.json", old_string='"debug": false', new_string='"debug": true')
```

---

### MultiEdit

**Description** : Applique plusieurs éditions simultanées sur un ou plusieurs fichiers

**Paramètres** :
- Liste d'éditions avec file_path, old_string, new_string

**Quand utiliser** :
- Modifications multiples sur le même fichier
- Renommage de variables/fonctions sur plusieurs fichiers
- Refactoring coordonné

**Bonnes pratiques** :
- Lire tous les fichiers avant MultiEdit
- Vérifier que les old_string sont uniques
- Grouper les éditions logiquement reliées

---

## Outils de recherche

### Glob

**Description** : Recherche de fichiers par patterns glob

**Paramètres** :
- `pattern` (requis) : Pattern glob (ex: `**/*.tex`, `src/**/*.js`)
- `path` (optionnel) : Dossier de recherche (défaut: working directory)

**Quand utiliser** :
- Trouver des fichiers par nom ou extension
- Lister tous les fichiers d'un type dans une arborescence
- Découvrir la structure d'un projet

**Patterns courants** :
- `*.tex` : Tous les .tex dans le dossier courant
- `**/*.tex` : Tous les .tex récursivement
- `src/**/*.js` : Tous les .js dans src/ et sous-dossiers
- `**/test_*.py` : Tous les fichiers test Python

**Bonnes pratiques** :
- Préférer Glob à `Bash("find . -name '*.tex'")`
- Utiliser des patterns spécifiques pour limiter les résultats
- Les résultats sont triés par date de modification

**Exemple** :
```markdown
1. Trouver tous les exercices : Glob("**/*exercice*.tex")
2. Pour chaque fichier trouvé, analyser avec Read
```

---

### Grep

**Description** : Recherche de contenu dans des fichiers (basé sur ripgrep)

**Paramètres** :
- `pattern` (requis) : Expression régulière
- `path` (optionnel) : Fichier ou dossier de recherche
- `glob` (optionnel) : Filtre de fichiers (ex: `*.tex`)
- `type` (optionnel) : Type de fichier (ex: `js`, `py`, `rust`)
- `output_mode` : `content` (lignes), `files_with_matches` (fichiers), `count` (comptage)
- `-i` : Recherche insensible à la casse
- `-A`, `-B`, `-C` : Lignes de contexte après/avant/autour
- `multiline` : Patterns sur plusieurs lignes

**Quand utiliser** :
- Chercher une commande, fonction, ou pattern dans le code
- Identifier quels fichiers contiennent une notion spécifique
- Compter les occurrences d'un pattern

**Bonnes pratiques** :
- Préférer Grep à `Bash("grep pattern files")`
- Utiliser `glob` ou `type` pour filtrer les fichiers
- Utiliser `-i` pour recherche insensible à la casse
- output_mode=`files_with_matches` pour lister les fichiers, puis Read pour détails

**Exemples** :
```markdown
# Trouver les fichiers contenant "fraction"
Grep(pattern="fraction", glob="*.tex", output_mode="files_with_matches")

# Afficher les lignes avec contexte
Grep(pattern="\\section", output_mode="content", -A=2, -B=1)

# Recherche multi-lignes
Grep(pattern="\\begin{exercice}.*?\\end{exercice}", multiline=true)
```

---

### LS

**Description** : Liste le contenu d'un dossier

**Paramètres** :
- `path` (optionnel) : Chemin du dossier

**Quand utiliser** :
- Explorer la structure d'un dossier
- Vérifier l'existence de fichiers/dossiers
- Lister les fichiers avant traitement

**Bonnes pratiques** :
- Utiliser pour explorer la structure avant Glob/Grep
- Combiner avec Read pour analyser des fichiers spécifiques

---

## Outils réseau

### WebFetch

**Description** : Récupère et traite du contenu web

**Paramètres** :
- `url` (requis) : URL complète (HTTPS recommandé)
- `prompt` (requis) : Instructions pour analyser le contenu

**Quand utiliser** :
- Scraper du contenu de pages web
- Récupérer des données depuis des APIs
- Télécharger de la documentation en ligne

**Bonnes pratiques** :
- Toujours fournir un prompt spécifique (ex: "Extraire les exercices et leurs IDs")
- Le HTML est converti en Markdown avant traitement
- Les URLs HTTP sont automatiquement upgradées en HTTPS
- Cache de 15 minutes pour les requêtes répétées

**Exemple** :
```markdown
WebFetch(
  url="https://coopmaths.fr/alea/?id=5N10",
  prompt="Extraire le code LaTeX de l'exercice et ses métadonnées"
)
```

**⚠️ Limitations** :
- Ne peut pas exécuter JavaScript (pas de rendu dynamique)
- Limité aux contenus accessibles publiquement
- Peut échouer sur sites avec protection anti-scraping

---

### WebSearch

**Description** : Recherche web avec Google

**Paramètres** :
- `query` (requis) : Requête de recherche
- `allowed_domains` (optionnel) : Limiter à certains domaines
- `blocked_domains` (optionnel) : Exclure certains domaines

**Quand utiliser** :
- Rechercher de la documentation
- Trouver des ressources externes
- Obtenir des informations récentes

**Bonnes pratiques** :
- Utiliser des requêtes spécifiques
- Filtrer par domaine si possible
- Combiner avec WebFetch pour extraire le contenu

**Exemple** :
```markdown
WebSearch(
  query="mathAlea exercices fractions 5eme",
  allowed_domains=["coopmaths.fr"]
)
```

---

## Outils système

### Bash

**Description** : Exécute des commandes shell

**Paramètres** :
- `command` (requis) : Commande à exécuter
- `description` (recommandé) : Description claire de l'action
- `timeout` (optionnel) : Timeout en ms (défaut 120000ms)
- `run_in_background` (optionnel) : Exécution en arrière-plan

**Quand utiliser** :
- Opérations système (git, npm, pip, etc.)
- Exécution de scripts Python/Node
- Manipulation de fichiers complexes

**Quand NE PAS utiliser** :
- Lecture de fichiers → Utiliser Read
- Recherche de fichiers → Utiliser Glob
- Recherche dans fichiers → Utiliser Grep
- Écriture de fichiers → Utiliser Write
- Communication → Utiliser le texte de réponse

**Bonnes pratiques** :
- Toujours fournir une description claire
- Utiliser des chemins absolus ou relatifs au working directory
- Chaîner les commandes avec `&&` si dépendantes
- Utiliser `run_in_background=true` pour processus longs

**Exemples** :
```markdown
# Installation de packages
Bash("pip install requests beautifulsoup4", description="Install Python dependencies")

# Compilation LaTeX
Bash("lualatex -output-directory=build cours.tex", description="Compile LaTeX document")

# Exécution de script
Bash("python scripts/process_data.py input.json output.json", description="Process data")

# Commandes chaînées
Bash("cd build && pdflatex main.tex && cp main.pdf ../output/", description="Build and copy PDF")
```

**⚠️ Attention** :
- Ne pas utiliser de commandes interactives (git commit -i, vim, etc.)
- Quoter les chemins avec espaces : `cd "path with spaces"`
- Timeout par défaut : 2 minutes (ajuster si nécessaire)

---

## Outils de coordination

### Task

**Description** : Lance un agent spécialisé pour une sous-tâche

**Paramètres** :
- `subagent_type` (requis) : Nom de l'agent à lancer
- `prompt` (requis) : Instructions détaillées pour l'agent
- `description` (requis) : Description courte (3-5 mots)
- `model` (optionnel) : Modèle à utiliser (sonnet/haiku/opus)

**Quand utiliser** :
- Déléguer une tâche complexe à un agent spécialisé
- Paralléliser des tâches indépendantes
- Séparer les responsabilités

**Bonnes pratiques** :
- Fournir un prompt détaillé et autonome
- Spécifier exactement ce que l'agent doit retourner
- Lancer plusieurs agents en parallèle si les tâches sont indépendantes

**Exemple** :
```markdown
Task(
  subagent_type="mathalea-scraper",
  description="Scrape exercise 5N10",
  prompt="Récupérer l'exercice 5N10 depuis mathAlea et extraire le code LaTeX. Retourner un JSON avec le code et les métadonnées."
)
```

**Note** : Les agents sont stateless ; chaque invocation est indépendante.

---

### TodoWrite

**Description** : Gère une liste de tâches

**Paramètres** :
- `todos` : Liste d'objets {content, status, activeForm}
  - `content` : Description impérative (ex: "Run tests")
  - `activeForm` : Forme continue (ex: "Running tests")
  - `status` : `pending`, `in_progress`, `completed`

**Quand utiliser** :
- Tâches complexes avec plusieurs étapes
- Suivi de progression pour l'utilisateur
- Organisation de workflows multi-étapes

**Bonnes pratiques** :
- Créer la todo list au début d'une tâche complexe
- Maintenir exactement 1 tâche `in_progress` à la fois
- Marquer completed immédiatement après achèvement
- Supprimer les tâches obsolètes

**Exemple** :
```markdown
TodoWrite(todos=[
  {content: "Fetch exercises from mathAlea", activeForm: "Fetching exercises", status: "in_progress"},
  {content: "Parse LaTeX code", activeForm: "Parsing LaTeX", status: "pending"},
  {content: "Write output file", activeForm: "Writing output", status: "pending"}
])
```

---

### Skill

**Description** : Invoque un skill spécialisé

**Paramètres** :
- `command` : Nom du skill (ex: `pdf`, `xlsx`, `bfcours-latex`)

**Quand utiliser** :
- Besoin d'expertise spécialisée (PDF, Excel, LaTeX)
- Tâches nécessitant des connaissances procédurales

**Exemple** :
```markdown
Skill(command="bfcours-latex")
```

---

## Outils spécialisés (selon contexte)

### NotebookEdit

**Description** : Édite des cellules Jupyter Notebook

**Paramètres** :
- `notebook_path` : Chemin du .ipynb
- `cell_id` : ID de la cellule
- `new_source` : Nouveau contenu
- `cell_type` : `code` ou `markdown`
- `edit_mode` : `replace`, `insert`, `delete`

**Quand utiliser** :
- Modification de notebooks Jupyter
- Génération de notebooks automatisée

---

### mcp__ide__getDiagnostics

**Description** : Récupère les diagnostics VS Code (erreurs, warnings)

**Paramètres** :
- `uri` (optionnel) : URI du fichier

**Quand utiliser** :
- Vérifier les erreurs de compilation
- Analyser les problèmes de typage
- Validation de code

---

### mcp__ide__executeCode

**Description** : Exécute du code Python dans le kernel Jupyter

**Paramètres** :
- `code` : Code Python à exécuter

**Quand utiliser** :
- Tests de code Python
- Validation de scripts
- Calculs interactifs

---

## Tableau récapitulatif : Quel outil utiliser ?

| Tâche | Outil recommandé | Alternative |
|-------|------------------|-------------|
| Lire un fichier | Read | ❌ Bash("cat") |
| Écrire un fichier | Write | ❌ Bash("echo >") |
| Éditer un fichier | Edit | ❌ Bash("sed") |
| Trouver des fichiers | Glob | ❌ Bash("find") |
| Chercher dans fichiers | Grep | ❌ Bash("grep") |
| Scraper une page web | WebFetch | WebSearch + WebFetch |
| Exécuter un script Python | Bash("python script.py") | mcp__ide__executeCode |
| Compiler LaTeX | Bash("lualatex") | - |
| Installer des packages | Bash("pip install") | - |
| Lancer un agent | Task | - |
| Gérer des tâches | TodoWrite | - |
| Manipuler des PDF | Skill("pdf") | - |
| Travailler avec Excel | Skill("xlsx") | - |

---

## Patterns de combinaison d'outils

### Pattern 1 : Exploration → Analyse → Transformation

```markdown
1. Glob("**/*.tex") pour trouver les fichiers
2. Pour chaque fichier :
   - Read(file) pour lire le contenu
   - Analyser et extraire les données
3. Write("output.json", results) pour écrire les résultats
```

### Pattern 2 : Recherche → Extraction → Traitement

```markdown
1. Grep(pattern="\\section", glob="*.tex") pour identifier les fichiers
2. Read chaque fichier avec correspondance
3. Extraire les sections
4. Write le résumé
```

### Pattern 3 : Web → Local → Transformation

```markdown
1. WebFetch(url) pour récupérer le contenu
2. Extraire les données pertinentes
3. Write en fichier local
4. Bash pour post-traitement (si nécessaire)
```

### Pattern 4 : Parallélisation de tâches

```markdown
Lancer en parallèle :
- Task(subagent_type="scraper1", ...)
- Task(subagent_type="scraper2", ...)
- Task(subagent_type="scraper3", ...)

Puis agréger les résultats
```

---

## Erreurs courantes à éviter

### ❌ Utiliser Bash au lieu d'outils spécialisés

```markdown
# Mauvais
Bash("cat file.txt")
Bash("find . -name '*.tex'")
Bash("grep pattern file.txt")

# Bon
Read("file.txt")
Glob("**/*.tex")
Grep(pattern="pattern", path="file.txt")
```

### ❌ Oublier de lire avant d'éditer

```markdown
# Mauvais
Edit("config.json", old_string="...", new_string="...")

# Bon
Read("config.json")  # D'abord lire
Edit("config.json", old_string="...", new_string="...")
```

### ❌ Utiliser Write au lieu de Edit

```markdown
# Mauvais (écrase tout le fichier)
content = read_entire_file()
content_modified = modify_one_line(content)
Write("file.txt", content_modified)

# Bon (édition ciblée)
Edit("file.txt", old_string="old line", new_string="new line")
```

### ❌ Ne pas gérer les erreurs d'outils

```markdown
# Mauvais
WebFetch(url) puis assumer le succès

# Bon
result = WebFetch(url)
Si erreur réseau :
  - Logger et retourner erreur
Sinon :
  - Continuer le traitement
```
