# 📖 Guide du Serveur MCP LaTeX Compiler

## 🎯 Objectif

Ce serveur MCP standardise et simplifie la compilation de documents LaTeX pour les agents. Plus de galères avec les commandes de compilation ! Les agents ont maintenant un canal fiable et configurable.

## ✨ Fonctionnalités Principales

### 🚀 Compilation Intelligente
- **Profils prédéfinis** : simple, standard, complete, bibliography
- **Détection automatique** des compilateurs installés
- **Gestion d'erreurs** claire et explicite
- **Nettoyage automatique** des fichiers auxiliaires

### ⚙️ Configuration Flexible
- **Chemins personnalisés** pour chaque compilateur
- **Arguments configurables** par compilateur
- **Profils personnalisés** créables par l'utilisateur
- **Préférences persistantes** dans un fichier JSON

### 🛡️ Robustesse
- **Timeout configurable** pour éviter les blocages
- **Messages d'erreur clairs** pour l'agent
- **Test de compilation** intégré
- **Cache intelligent** des statuts de compilateurs

## 📋 Méthodes Disponibles

### Compilation Principale

#### `compile_document(file_path, compilation_type, clean_aux)`
**La méthode principale pour compiler un document LaTeX.**

```python
# Compilation standard (2 passes)
compile_document("mon_cours.tex", "standard", True)

# Compilation avec bibliographie
compile_document("these.tex", "bibliography", True)

# Compilation simple sans nettoyage
compile_document("test.tex", "simple", False)
```

**Profils disponibles :**
- `simple` : 1 passe pdflatex
- `standard` : 2 passes pdflatex (références croisées)
- `complete` : 3 passes pdflatex
- `bibliography` : pdflatex + bibtex + pdflatex x2
- `glossary` : pdflatex + makeglossaries + pdflatex
- `index` : pdflatex + makeindex + pdflatex
- `custom` : Vos profils personnalisés

#### `quick_compile(file_path)`
**Compilation rapide avec le profil par défaut.**

```python
# Équivalent à compile_document(file, "default", True)
quick_compile("document.tex")
```

### Configuration et Détection

#### `detect_compilers()`
**Détecte automatiquement les compilateurs LaTeX installés.**

```python
result = detect_compilers()
# Retourne:
{
  "compilers": {
    "pdflatex": {"available": true, "version": "pdfTeX 3.14..."},
    "lualatex": {"available": false},
    "xelatex": {"available": true, "version": "XeTeX 3.14..."}
  }
}
```

#### `update_compiler_config(compiler_name, path, args, enabled)`
**Configure un compilateur spécifique.**

```python
# Activer lualatex avec arguments personnalisés
update_compiler_config(
    "lualatex",
    path="/usr/local/bin/lualatex",
    args='["-interaction=nonstopmode", "-shell-escape"]',
    enabled=True
)

# Désactiver un compilateur
update_compiler_config("xelatex", enabled=False)
```

### Gestion des Profils

#### `get_compilation_profiles()`
**Liste tous les profils de compilation disponibles.**

```python
profiles = get_compilation_profiles()
# Affiche les profils et celui par défaut
```

#### `add_compilation_profile(name, description, steps)`
**Crée un profil de compilation personnalisé.**

```python
# Profil pour présentation Beamer
add_compilation_profile(
    "beamer",
    "Compilation pour présentations Beamer",
    '[{"compiler": "pdflatex", "count": 2}]'
)

# Profil complexe avec glossaire et bibliographie
add_compilation_profile(
    "thesis",
    "Compilation complète pour thèse",
    '''[
        {"compiler": "pdflatex", "count": 1},
        {"compiler": "bibtex", "count": 1},
        {"compiler": "makeglossaries", "count": 1},
        {"compiler": "pdflatex", "count": 2}
    ]'''
)
```

#### `set_default_profile(profile_name)`
**Définit le profil par défaut.**

```python
set_default_profile("complete")  # 3 passes par défaut
```

### Utilitaires

#### `test_compilation(test_content)`
**Teste la configuration avec un document simple.**

```python
# Test avec document par défaut
test_compilation()

# Test avec contenu personnalisé
test_compilation(r"\documentclass{beamer}...")
```

#### `clean_build_files(directory, extensions)`
**Nettoie les fichiers auxiliaires dans un répertoire.**

```python
# Nettoyer avec extensions par défaut
clean_build_files("/path/to/project")

# Extensions personnalisées
clean_build_files("/path", '["*.aux", "*.log", "*.synctex.gz"]')
```

#### `get_preferences()` / `reset_preferences()`
**Gère les préférences globales.**

```python
# Voir toutes les préférences
prefs = get_preferences()

# Réinitialiser aux valeurs par défaut
reset_preferences()
```

## 📁 Structure du Fichier de Configuration

Le fichier `latex-compiler-preferences.json` contient :

```json
{
  "compilers": {
    "pdflatex": {
      "path": "pdflatex",
      "args": ["-interaction=nonstopmode", "-halt-on-error"],
      "enabled": true
    },
    "lualatex": {
      "path": "lualatex",
      "args": ["-interaction=nonstopmode"],
      "enabled": false
    }
  },
  "compilation_profiles": {
    "standard": {
      "description": "Compilation standard (2 passes)",
      "steps": [{"compiler": "pdflatex", "count": 2}]
    },
    "custom_profile": {
      "description": "Mon profil personnalisé",
      "steps": [...]
    }
  },
  "default_profile": "standard",
  "output_directory": "build",
  "clean_aux_files": true,
  "aux_extensions": [".aux", ".log", ".toc", ".out"],
  "verbose_output": false,
  "timeout_seconds": 120
}
```

## 🎯 Cas d'Usage pour les Agents

### Workflow Typique d'un Agent

```python
# 1. L'agent vérifie d'abord les compilateurs disponibles
compilers = detect_compilers()

# 2. Configure si nécessaire
if not compilers["lualatex"]["available"]:
    print("LuaLaTeX non détecté, utilisation de pdflatex")

# 3. Compile le document
result = compile_document("cours_maths.tex", "standard")

# 4. Vérifie le résultat
if result["pdf_generated"]:
    print(f"PDF créé: {result['pdf_path']}")
else:
    print(f"Erreur: {result['steps'][-1]['stderr']}")
```

### Gestion des Erreurs Claire

L'agent reçoit des messages explicites :

```json
{
  "status": "error",
  "compilation_type": "bibliography",
  "steps": [
    {"compiler": "pdflatex", "pass": 1, "success": true},
    {
      "compiler": "bibtex", 
      "success": false,
      "error": "Compilateur bibtex non disponible ou non configuré"
    }
  ],
  "message": "Compilation échouée"
}
```

### Profils Adaptés au Contexte

```python
# L'agent choisit le bon profil selon le document

# Document simple -> compilation rapide
if "\\bibliography" not in content:
    compile_document(file, "simple")

# Document avec bibliographie
elif "\\bibliography" in content:
    compile_document(file, "bibliography")

# Document avec glossaire
elif "\\makeglossaries" in content:
    compile_document(file, "glossary")

# Par défaut
else:
    compile_document(file, "standard")
```

## 🔧 Configuration Initiale Recommandée

### 1. Détection et Activation

```python
# Détecter les compilateurs
detected = detect_compilers()

# Activer ceux qui sont disponibles
for compiler, info in detected["compilers"].items():
    if info["available"] and not info["enabled"]:
        update_compiler_config(compiler, enabled=True)
```

### 2. Créer des Profils Métier

```python
# Profil pour cours avec TikZ
add_compilation_profile(
    "cours_tikz",
    "Compilation pour cours avec figures TikZ",
    '[{"compiler": "pdflatex", "count": 2}]'
)

# Profil pour documents avec PythonTeX
add_compilation_profile(
    "pythontex",
    "Documents avec code Python intégré",
    '''[
        {"compiler": "pdflatex", "count": 1},
        {"compiler": "pythontex", "count": 1},
        {"compiler": "pdflatex", "count": 1}
    ]'''
)
```

### 3. Optimiser les Paramètres

```python
# Pour compilation plus rapide (draft mode)
update_compiler_config(
    "pdflatex",
    args='["-interaction=nonstopmode", "-draftmode"]'
)

# Pour beamer avec transitions
update_compiler_config(
    "pdflatex",
    args='["-interaction=nonstopmode", "-shell-escape"]'
)
```

## 🚨 Résolution de Problèmes

### Compilateur Non Trouvé

```python
# Vérifier le chemin
detect_compilers()  # Voir ce qui est détecté

# Spécifier le chemin complet
update_compiler_config(
    "pdflatex",
    path="C:/Program Files/MiKTeX/miktex/bin/x64/pdflatex.exe"
)
```

### Timeout sur Gros Documents

```python
# Augmenter le timeout
prefs = get_preferences()
prefs["preferences"]["timeout_seconds"] = 300  # 5 minutes
# Puis sauvegarder via update_compiler_config ou directement
```

### Fichiers Auxiliaires Non Nettoyés

```python
# Ajouter des extensions
prefs = get_preferences()
prefs["preferences"]["aux_extensions"].append(".synctex.gz")
prefs["preferences"]["aux_extensions"].append(".fdb_latexmk")
```

## 📊 Exemples de Retours

### Succès Complet

```json
{
  "status": "success",
  "compilation_type": "standard",
  "file": "/path/to/document.tex",
  "pdf_generated": true,
  "pdf_path": "/path/to/document.pdf",
  "steps": [
    {"compiler": "pdflatex", "pass": 1, "success": true},
    {"compiler": "pdflatex", "pass": 2, "success": true}
  ],
  "cleaned_files": ["document.aux", "document.log"],
  "message": "Compilation réussie"
}
```

### Erreur LaTeX

```json
{
  "status": "error",
  "steps": [{
    "compiler": "pdflatex",
    "pass": 1,
    "success": false,
    "stderr": "! Undefined control sequence.\nl.42 \\unknowncommand"
  }],
  "message": "Compilation échouée"
}
```

## 🎉 Avantages pour les Agents

1. **Standardisation** : Même interface pour tous les types de compilation
2. **Fiabilité** : Gestion d'erreurs robuste et messages clairs
3. **Flexibilité** : Profils adaptables selon les besoins
4. **Performance** : Cache des détections, timeout configurable
5. **Simplicité** : `quick_compile("fichier.tex")` et c'est parti !

## 🚀 Commandes de Démarrage

```bash
# Installation des dépendances
pip install mcp

# Lancement du serveur
python latex_compiler_server.py

# Test rapide
# L'agent peut ensuite utiliser:
test_compilation()  # Vérifie que tout fonctionne
```

## 💡 Tips pour les Agents

- Toujours utiliser `detect_compilers()` au premier usage
- Préférer `quick_compile()` pour les documents simples
- Utiliser `test_compilation()` en cas de doute sur la config
- Consulter `get_compilation_profiles()` pour voir les options
- Les messages d'erreur contiennent toujours la solution !

---

Ce serveur transforme la compilation LaTeX en une opération simple et fiable pour tous les agents ! 🎓