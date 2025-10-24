# 🚀 Serveurs MCP pour les Agents Pédagogiques

## 🎯 Vue d'ensemble

Ce dossier contient **6 serveurs MCP** qui permettent à tous tes agents de se documenter automatiquement et de travailler de façon autonome :

1. **🎓 Serveur Compétences** - Accès aux compétences du programme scolaire
2. **📝 Serveur LaTeX Search** - Exploration et analyse des packages LaTeX
3. **📄 Serveur PDF Analyzer** - Analyse complète de documents PDF
4. **📝 Serveur Document Creator** - Création automatique de documents LaTeX
5. **🔧 Serveur LaTeX Compiler** - Compilation automatisée avec gestion d'erreurs
6. **🔤 Serveur Encoding Fixer** - Correction automatique d'encodage UTF-8

## ⚡ Installation rapide

### Option 1 : Installation complète (recommandée)
```bash
setup_all_mcp.bat
```

### Option 2 : Installation séparée
```bash
# Serveur compétences uniquement
setup_mcp.bat

# Serveur LaTeX uniquement  
setup_latex_mcp.bat
```

## 📊 Serveur Compétences (286 compétences)

### 🎯 Objectif
Permet aux agents d'accéder aux compétences du programme pour créer des contenus pédagogiques adaptés.

### 🔧 Outils (10)
- `search_competences` - Recherche par texte libre
- `filter_by_niveau` - CM1, CM2, SIXIEME, CINQUIEME, QUATRIEME
- `filter_by_theme` - DONNEES, GEOMETRIE, GRANDEURS, INFORMATIQUE, NOMBRES
- `filter_by_palier` - Paliers de difficulté 1-5
- `get_competence_by_code` - Recherche par code exact (ex: C1D1-1)
- `get_niveaux_available` - Liste des niveaux
- `get_themes_available` - Liste des thèmes
- `get_paliers_available` - Liste des paliers
- `get_competences_stats` - Statistiques complètes
- `advanced_search` - Recherche multicritères combinés

### 💡 Exemple d'usage
```
Utilise advanced_search avec niveau="CINQUIEME" et theme="GEOMETRIE" pour trouver toutes les compétences de géométrie en 5ème
```

## 🔍 Serveur LaTeX Search

### 🎯 Objectif  
Permet aux agents d'explorer, comprendre et analyser tes packages LaTeX pour :
- Se documenter sur les commandes disponibles
- Comprendre l'implémentation du code
- Adapter et personnaliser les commandes existantes

### 🔧 Outils (5)
- `search_exact_command` - Recherche exacte d'une commande
- `search_fuzzy_command` - Recherche floue avec scoring
- `list_available_packages` - Packages configurés
- `scan_package_commands` - Vue d'ensemble d'un package
- `get_command_definition` - Définition avec contexte étendu

### 🎯 Patterns reconnus
- `\newcommand`, `\renewcommand`
- `\def`, `\gdef`, `\edef`, `\xdef`  
- `\newenvironment`, `\renewenvironment`
- `\newtcolorbox`, `\DeclareTColorBox`
- `\newtheorem`, `\newcounter`
- LaTeX3 : `\NewDocumentCommand`, `\DeclareDocumentCommand`
- `\definecolor`

### 💡 Exemple d'usage
```
Utilise get_command_definition avec command_name="MultiColonnes" et show_context=true pour analyser complètement cette commande
```

## 📁 Structure des fichiers

```
mcp_servers/
├── 📄 README_SERVEURS_MCP.md        # Ce fichier
├── 
├── 🎓 SERVEUR COMPETENCES
│   ├── competences_server_fixed.py   # Serveur principal
│   ├── setup_mcp.bat                 # Installation
│   └── GUIDE_INSTALLATION.md        # Documentation
│
├── 🔍 SERVEUR LATEX
│   ├── latex_search_server.py       # Serveur principal  
│   ├── setup_latex_mcp.bat          # Installation
│   └── GUIDE_LATEX_SEARCH.md        # Documentation
│
├── 📄 SERVEUR PDF ANALYZER
│   ├── pdf_analyzer_server_lite.py  # Serveur principal
│   ├── install_pdf_analyzer_deps.bat # Installation
│   └── GUIDE_PDF_ANALYZER.md        # Documentation
│
├── 📝 SERVEUR DOCUMENT CREATOR
│   ├── document_creator_server.py   # Serveur principal
│   ├── setup_document_creator_mcp.bat # Installation
│   └── GUIDE_DOCUMENT_CREATOR.md    # Documentation
│
├── 🔧 SERVEUR LATEX COMPILER
│   ├── latex_compiler_server.py     # Serveur principal
│   ├── setup_latex_compiler_mcp.bat # Installation
│   └── GUIDE_LATEX_COMPILER.md      # Documentation
│
├── 🔤 SERVEUR ENCODING FIXER (NOUVEAU)
│   ├── encoding_fixer_server.py     # Serveur principal
│   ├── setup_encoding_fixer_mcp.bat # Installation
│   └── GUIDE_ENCODING_FIXER.md      # Documentation
│
├── ⚡ GLOBAL
│   ├── setup_all_mcp.bat            # Installation des serveurs
│   ├── setup_all_mcp_complete.bat   # Installation complète
│   └── requirements.txt             # Dépendances Python
│
└── 📊 DATA SOURCE
    └── ../datas/competences.json    # Base de données compétences
    └── ../datas/latex-modeles/      # Modèles LaTeX
    └── mcp.json                      # Configuration serveurs
```

## 🎯 Avantages pour tes agents

### 🤖 Autonomie renforcée
- **Auto-documentation** : Plus besoin d'expliquer les compétences ou commandes
- **Contextualisation** : Adaptation automatique au niveau et programme
- **Exploration** : Découverte autonome des fonctionnalités

### 📚 Qualité pédagogique
- **Précision** : Contenus alignés sur le programme officiel
- **Cohérence** : Utilisation correcte de tes packages LaTeX
- **Efficacité** : Réutilisation intelligente du code existant

### 🔄 Workflow optimisé
- **Recherche** : Accès direct aux informations pertinentes
- **Adaptation** : Personnalisation basée sur le contexte réel
- **Innovation** : Combinaison créative des éléments existants

## 🔍 Vérification de l'installation

```bash
# Voir tous les serveurs
claude mcp list

# Vérifier dans Claude Code
/mcp
```

Tu devrais voir :
- ✅ `competences-server`
- ✅ `latex-search-server`
- ✅ `pdf-analyzer-server`
- ✅ `document-creator-server`
- ✅ `latex-compiler-server`
- ✅ `encoding-fixer-server`

## 🧪 Test rapide

### Test Compétences
```
Utilise get_competences_stats pour avoir un aperçu des 286 compétences disponibles
```

### Test LaTeX
```
Utilise list_available_packages puis search_exact_command avec "chapitre" pour voir comment cette commande est définie
```

### Test Encoding Fixer
```
Utilise detect_file_encoding sur un fichier .tex pour analyser son encodage actuel
```

## 🎉 Résultat

Tes agents peuvent maintenant :
- 🎓 **Se référer au programme officiel** (compétences pédagogiques)
- 🔍 **Explorer tes packages LaTeX** (commandes, environnements, etc.)
- 📄 **Analyser des PDF** (texte, images, tableaux)
- 📝 **Créer des documents** automatiquement à partir de modèles
- 🔧 **Compiler LaTeX** avec gestion d'erreurs intelligente
- 🔤 **Corriger l'encodage UTF-8** automatiquement (NOUVEAU)
- 🤖 **Travailler de façon autonome** sans intervention manuelle
- 📚 **Produire du contenu de qualité** adapté au contexte

**Plus besoin d'expliquer à tes agents comment faire - ils savent où chercher ! 🚀**

## 🆕 Nouveau : Serveur Encoding Fixer

**Problème résolu** : Caractères accentués corrompus (é → �) dans les fichiers générés par Claude.

**Solution** : Détection et conversion automatique vers UTF-8 pour tous les fichiers LaTeX.

**Utilisation obligatoire** : Après chaque `Write` ou `Edit` de fichier contenant des caractères français.