# Guide d'utilisation des scripts bfcours-latex

## Localisation des scripts

Tous les scripts sont dans : `.claude/skills/bfcours-latex/scripts/`

## Scripts disponibles

### 1. search_command.py - Recherche de commandes bfcours

Cherche dans les conventions bfcours par nom de commande ou mot-cle.

**Recherche floue** (par mot-cle) :
```bash
python ".claude/skills/bfcours-latex/scripts/search_command.py" --query "tableau"
python ".claude/skills/bfcours-latex/scripts/search_command.py" --query "espace reponse" --limit 3
```

**Recherche exacte** (par commande) :
```bash
python ".claude/skills/bfcours-latex/scripts/search_command.py" --exact "\\encadrer"
python ".claude/skills/bfcours-latex/scripts/search_command.py" --exact "\\acc"
```

**Arguments** :
- `--query` / `-q` : Recherche floue par mot-cle
- `--exact` / `-e` : Recherche exacte d'une commande LaTeX
- `--limit` / `-l` : Nombre max de resultats (defaut: 5)

**Sortie JSON** : sections pertinentes avec titre, score, commandes trouvees et extrait.

### 2. search_examples.py - Recherche dans les exemples

Cherche des patterns dans les fichiers .tex du dossier `assets/usecase/`.

**Chercher un pattern** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_examples.py" --pattern "\\begin{EXO}" --context 10
python ".claude/skills/bfcours-latex/scripts/search_examples.py" --pattern "\\tcbtab" --context 15
python ".claude/skills/bfcours-latex/scripts/search_examples.py" --pattern "\\exocorrection" --context 20
```

**Lister tous les environnements utilises** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_examples.py" --list-envs
```

**Arguments** :
- `--pattern` / `-p` : Pattern LaTeX a chercher
- `--context` / `-c` : Lignes de contexte apres le match (defaut: 5)
- `--limit` / `-l` : Nombre max de resultats (defaut: 10)
- `--list-envs` : Lister tous les environnements avec leur frequence

**Sortie JSON** : fichier, ligne, match et extrait avec contexte.

### 3. search_package.py - Recherche dans un package LaTeX installe

Utilise `kpsewhich` pour localiser le fichier .sty d'un package sur le systeme, puis cherche dans son code source.

**Localiser un package** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package tcolorbox --locate
```

**Chercher dans un package** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package tcolorbox --query "raster"
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package siunitx --query "unit"
```

**Lister les commandes definies** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package siunitx --list-commands
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package pgfplots --list-commands --limit 30
```

**Lister les environnements definis** :
```bash
python ".claude/skills/bfcours-latex/scripts/search_package.py" --package tcolorbox --list-envs
```

**Arguments** :
- `--package` / `-p` : Nom du package (obligatoire)
- `--query` / `-q` : Recherche dans le contenu du .sty
- `--list-commands` : Lister les commandes (\newcommand, \NewDocumentCommand, etc.)
- `--list-envs` : Lister les environnements et styles
- `--locate` : Afficher les chemins des fichiers .sty
- `--context` / `-c` : Lignes de contexte (defaut: 3)
- `--limit` / `-l` : Nombre max de resultats (defaut: 20)

**Sortie JSON** : commandes avec nom, type de declaration, arguments et numero de ligne.

## Workflow typique

1. **Trouver comment utiliser une commande** :
   ```bash
   python ".claude/skills/bfcours-latex/scripts/search_command.py" --exact "\\tcbtab"
   ```

2. **Voir des exemples reels** :
   ```bash
   python ".claude/skills/bfcours-latex/scripts/search_examples.py" --pattern "\\begin{tcbtab}" --context 10
   ```

3. **Explorer les environnements disponibles** :
   ```bash
   python ".claude/skills/bfcours-latex/scripts/search_examples.py" --list-envs
   ```
