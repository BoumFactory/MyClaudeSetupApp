# 📄 Serveur MCP PDF Analyzer - Vue d'ensemble

## 🎯 Objectif

Le serveur `pdf-analyzer-server` permet aux agents LaTeX d'analyser complètement des fichiers PDF pour :
- Extraire des exemples pédagogiques
- Récupérer des images et schémas
- Analyser la structure des documents
- Rechercher des compétences et concepts
- Extraire des tableaux de données

## 🚀 Installation rapide

```batch
cd .claude\mcp_servers
setup_pdf_analyzer_mcp.bat
```

## 📋 Fonctions principales

### 1. **analyze_pdf** - Analyse complète
```python
analyze_pdf("document.pdf")
# Retourne : texte, images, métadonnées, structure, statistiques
```

### 2. **extract_pdf_text** - Texte uniquement
```python
extract_pdf_text("cours.pdf", page_numbers=[1, 2, 3])
# Retourne : texte par page avec compteurs
```

### 3. **extract_pdf_images** - Images
```python
extract_pdf_images("figures.pdf", output_format="base64")
# Retourne : images encodées en base64 avec métadonnées
```

### 4. **extract_pdf_tables** - Tableaux
```python
extract_pdf_tables("statistiques.pdf")
# Retourne : tableaux structurés en JSON
```

### 5. **search_in_pdf** - Recherche
```python
search_in_pdf("programme.pdf", "compétence C1D1")
# Retourne : occurrences avec contexte et position
```

## 🎓 Cas d'usage pédagogiques

### Pour latex-bfcours-writer
- Analyser des documents modèles pour structure
- Extraire des exercices existants
- Récupérer des images pédagogiques

### Pour tkz-euclide-master
- Extraire des figures géométriques
- Analyser des constructions existantes
- Récupérer des schémas complexes

### Pour nicematrix-expert
- Extraire des tableaux de données
- Analyser des matrices existantes
- Récupérer des statistiques

### Pour proflycee-expert
- Extraire des arbres de probabilités
- Récupérer des graphiques
- Analyser des exercices Python

## 🔧 Configuration

Ajouter au `claude_desktop_config.json` :
```json
"pdf-analyzer-server": {
  "command": "...\\venv_pdf_analyzer\\Scripts\\python.exe",
  "args": ["...\\pdf_analyzer_server.py"],
  "env": {"PYTHONIOENCODING": "utf-8"}
}
```

## 📊 Performances
- Texte : ~100 pages/seconde
- Images : ~20 images/seconde
- Recherche : ~50 pages/seconde

## ⚡ Protocole d'utilisation

1. **Analyse initiale** : `get_pdf_metadata()` pour comprendre le document
2. **Extraction ciblée** : Selon le besoin (texte, images, tableaux)
3. **Recherche spécifique** : Pour localiser des éléments précis
4. **Sauvegarde** : Stocker les découvertes dans agents-data

## 🔒 Sécurité
- Lecture seule (aucune modification)
- Fichiers temporaires nettoyés automatiquement
- Validation des chemins d'accès