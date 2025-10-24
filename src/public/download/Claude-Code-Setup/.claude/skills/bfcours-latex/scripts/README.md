# Scripts CLI pour le Skill BFCours-LaTeX

Ce répertoire contient des scripts Python qui permettent d'utiliser les serveurs MCP directement en ligne de commande, sans passer par le système MCP complet.

## 📋 Organisation

```
scripts/
├── fix-encoding/          # Correction d'encodage UTF-8
│   ├── fix_file_encoding.py
│   ├── detect_file_encoding.py
│   ├── fix_directory_encoding.py
│   └── get_encoding_stats.py
│
├── document-creator/      # Création de documents LaTeX
│   ├── list_templates.py
│   ├── get_template_info.py
│   ├── create_document.py
│   ├── get_user_preferences.py
│   ├── update_user_preferences.py
│   ├── add_user_habit.py
│   ├── remove_user_habit.py
│   └── get_help.py
│
└── latex-compiler/        # Compilation de documents LaTeX
    ├── compile_document.py
    ├── quick_compile.py
    ├── detect_compilers.py
    ├── get_compilation_profiles.py
    ├── add_compilation_profile.py
    ├── update_compiler_config.py
    ├── set_default_profile.py
    ├── get_preferences.py
    ├── clean_build_files.py
    ├── test_compilation.py
    ├── analyze_latex_log.py
    ├── get_file_context.py
    └── reset_preferences.py
```

## 🎯 Principe de fonctionnement

Chaque script :

1. **Importe les fonctions** des serveurs MCP depuis `.claude/mcp_servers/`
2. **Accepte des arguments** en ligne de commande (format argparse)
3. **Affiche deux sorties** :
   - **JSON sur stdout** → pour l'agent (parsing facile)
   - **Texte formaté sur stderr** → pour l'utilisateur (lisibilité humaine)

## 🚀 Utilisation

### Correction d'encodage

```bash
# Corriger l'encodage d'un fichier
python fix-encoding/fix_file_encoding.py --file "mon_cours.tex"

# Sans créer de backup
python fix-encoding/fix_file_encoding.py --file "devoir.tex" --no-backup

# Détecter l'encodage sans modifier
python fix-encoding/detect_file_encoding.py --file "enonce.tex"

# Corriger tout un répertoire
python fix-encoding/fix_directory_encoding.py --directory "./Sequence-Vecteurs" --recursive
```

### Création de documents

```bash
# Lister les modèles disponibles
python document-creator/list_templates.py

# Obtenir les infos d'un modèle
python document-creator/get_template_info.py --template "Cours"

# Créer un document
python document-creator/create_document.py \
    --destination "./Test" \
    --name "Mon_Cours_Vecteurs" \
    --template "Cours" \
    --fields '{"niveau": "$\\mathbf{2^{\\text{nde}}}$", "theme": "Vecteurs"}'
```

### Compilation LaTeX

```bash
# Compilation rapide (LuaLaTeX - profil Reims)
python latex-compiler/quick_compile.py --file "mon_cours.tex"

# Compilation avec profil spécifique
python latex-compiler/compile_document.py --file "devoir.tex" --type "standard"

# Détecter les compilateurs disponibles
python latex-compiler/detect_compilers.py

# Analyser un fichier .log
python latex-compiler/analyze_latex_log.py --log "cours.log" --tex "cours.tex"

# Nettoyer les fichiers de build
python latex-compiler/clean_build_files.py --directory "./Sequence-Fonctions"
```

## 📊 Format de sortie

### Pour l'utilisateur (stderr)

```
🔧 Correction d'encodage: mon_cours.tex
💾 Création d'une sauvegarde activée
✅ Succès!
   Encodage d'origine: latin-1
   Nouveau fichier: C:\...\mon_cours.tex
   Backup: C:\...\mon_cours.tex.backup
```

### Pour l'agent (stdout)

```json
{
  "success": true,
  "file": "C:\\...\\mon_cours.tex",
  "original_encoding": "latin-1",
  "new_encoding": "utf-8",
  "characters_count": 1542,
  "backup_created": true,
  "backup_path": "C:\\...\\mon_cours.tex.backup"
}
```

## 🤖 Utilisation par l'agent

L'agent peut appeler ces scripts via l'outil Bash :

```python
# Exemple dans le skill bfcours-latex
result = Bash(
    command="python .claude/skills/bfcours-latex/scripts/fix-encoding/fix_file_encoding.py --file enonce.tex --no-backup"
)

# Parser le JSON de stdout
import json
data = json.loads(result.stdout)

if data["success"]:
    print(f"Encodage corrigé : {data['original_encoding']} → {data['new_encoding']}")
```

## 🔧 Dépendances

Les scripts nécessitent :

- Python 3.7+
- Les serveurs MCP dans `.claude/mcp_servers/`
- Le package `mcp` (installé avec les serveurs MCP)

## 📝 Conventions

### Arguments

- `--file` : chemin de fichier
- `--directory` : chemin de répertoire
- `--template` : nom de modèle
- `--fields` : dictionnaire JSON
- `--backup` / `--no-backup` : créer ou non une sauvegarde
- `--enabled` / `--disabled` : activer/désactiver

### Codes de retour

- `0` : succès
- `1` : échec

### Aide

Tous les scripts supportent `--help` :

```bash
python fix-encoding/fix_file_encoding.py --help
```

## 💡 Avantages

1. **Simplicité** : Pas besoin de comprendre le protocole MCP
2. **Autonomie** : Utilisable sans serveur MCP actif
3. **Flexibilité** : Utilisable par humains ET agents
4. **Debugging** : Affichage humain facilite le diagnostic

## ⚠️ Limitations

- Les scripts importent directement les fonctions MCP (dépendance)
- Nécessitent que les serveurs MCP soient dans le bon répertoire
- Les fonctions async nécessitent `asyncio.run()`

## 📖 Documentation complète

Pour plus d'informations sur chaque serveur MCP :

```bash
python document-creator/get_help.py
```
