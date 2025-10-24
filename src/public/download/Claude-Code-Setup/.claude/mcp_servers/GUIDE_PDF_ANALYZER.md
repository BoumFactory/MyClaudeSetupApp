# 📄 Guide du serveur MCP PDF Analyzer

## Vue d'ensemble

Le serveur `pdf-analyzer-server` est un serveur MCP (Model Context Protocol) permettant l'analyse complète de fichiers PDF. Il offre des fonctionnalités avancées d'extraction de texte, d'images, de métadonnées et de structure des documents PDF.

## 🚀 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)

### Installation automatique
```batch
cd C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\.claude\mcp_servers
setup_pdf_analyzer_mcp.bat
```

### Installation manuelle
```bash
# Créer un environnement virtuel
python -m venv venv_pdf_analyzer

# Activer l'environnement
venv_pdf_analyzer\Scripts\activate  # Windows
source venv_pdf_analyzer/bin/activate  # Linux/Mac

# Installer les dépendances
pip install PyPDF2 pymupdf pdfplumber pillow pikepdf mcp
```

## 📋 Fonctionnalités disponibles

### 1. `analyze_pdf` - Analyse complète
Analyse complète d'un fichier PDF avec toutes les informations disponibles.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `extract_images` : Extraire les images (défaut: true)
- `extract_text` : Extraire le texte (défaut: true)
- `extract_metadata` : Extraire les métadonnées (défaut: true)
- `extract_structure` : Extraire la structure (défaut: true)
- `page_range` : Pages à analyser (ex: "1-5,7,10-15")

**Exemple d'utilisation :**
```python
result = analyze_pdf(
    pdf_path="documents/cours_maths.pdf",
    extract_images=True,
    page_range="1-10"
)
```

### 2. `extract_pdf_text` - Extraction de texte
Extrait uniquement le texte d'un PDF, page par page.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `page_numbers` : Liste des pages à extraire (défaut: toutes)
- `preserve_layout` : Préserver la mise en page (défaut: false)

**Retour :**
```json
{
  "pages": {
    "1": {
      "text": "Contenu de la page 1...",
      "char_count": 1234,
      "word_count": 200
    }
  },
  "total_text": "Tout le texte concatené...",
  "total_pages": 50,
  "extracted_pages": 10
}
```

### 3. `extract_pdf_images` - Extraction d'images
Extrait toutes les images d'un PDF avec leurs métadonnées.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `output_format` : "base64" ou "path" (défaut: "base64")
- `image_format` : "png" ou "jpg" (défaut: "png")
- `min_width` : Largeur minimale des images (défaut: 50)
- `min_height` : Hauteur minimale des images (défaut: 50)

**Retour :**
```json
{
  "images": [
    {
      "page": 1,
      "index": 0,
      "width": 800,
      "height": 600,
      "format": "png",
      "data": "base64_encoded_image_data..."
    }
  ],
  "total_count": 5
}
```

### 4. `extract_pdf_tables` - Extraction de tableaux
Extrait les tableaux trouvés dans le PDF.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `page_numbers` : Pages à analyser
- `output_format` : "json" ou "csv" (défaut: "json")

### 5. `get_pdf_metadata` - Métadonnées
Récupère toutes les métadonnées du PDF.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `include_xmp` : Inclure les métadonnées XMP (défaut: true)

**Retour :**
```json
{
  "document_info": {
    "title": "Cours de Mathématiques",
    "author": "Prof. Dupont",
    "subject": "Algèbre linéaire",
    "creator": "LaTeX",
    "creation_date": "2024-01-15",
    "keywords": "maths, algèbre, vecteurs"
  },
  "structure": {
    "pages": 50,
    "encrypted": false,
    "pdf_version": "1.7"
  }
}
```

### 6. `search_in_pdf` - Recherche
Recherche du texte dans un PDF avec contexte.

**Paramètres :**
- `pdf_path` (requis) : Chemin du fichier PDF
- `search_text` (requis) : Texte à rechercher
- `case_sensitive` : Sensible à la casse (défaut: false)
- `whole_words` : Mots entiers uniquement (défaut: false)

## 🔧 Configuration

### Ajout au fichier de configuration MCP

Ajoutez cette configuration à votre `settings.local.json` :

```json
{
  "mcpServers": {
    "pdf-analyzer-server": {
      "command": "C:\\...\\venv_pdf_analyzer\\Scripts\\python.exe",
      "args": [
        "C:\\...\\pdf_analyzer_server.py"
      ],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
}
```

## 📚 Cas d'usage pour les agents LaTeX

### 1. Analyse de documents de référence
Les agents peuvent analyser des PDF existants pour :
- Extraire des exemples de mise en page
- Récupérer des exercices ou théorèmes
- Analyser la structure pédagogique

### 2. Extraction d'images pédagogiques
- Récupérer des schémas et diagrammes
- Extraire des graphiques pour réutilisation
- Identifier des figures géométriques

### 3. Recherche de compétences
- Rechercher des codes de compétences dans les documents
- Identifier les niveaux et thèmes abordés
- Extraire les objectifs pédagogiques

### 4. Analyse de mise en page
- Étudier l'organisation des documents existants
- Identifier les styles et conventions utilisés
- Extraire des modèles de présentation

## 🎯 Intégration avec les agents

### Pour tous les agents LaTeX

Les agents peuvent utiliser le serveur PDF pour :

```python
# Analyser un document de référence
reference_doc = analyze_pdf("references/cours_modele.pdf")

# Extraire uniquement les images
images = extract_pdf_images(
    "exercices/geometrie.pdf",
    output_format="base64",
    min_width=200
)

# Rechercher des compétences
competences = search_in_pdf(
    "programme_officiel.pdf",
    "C1D1",
    whole_words=True
)

# Extraire des tableaux de données
tables = extract_pdf_tables(
    "statistiques.pdf",
    output_format="json"
)
```

### Protocole MCP pour les agents

1. **Démarrage** : `get_pdf_metadata()` pour comprendre le document
2. **Exploration** : `extract_pdf_text()` pour le contenu pédagogique
3. **Ressources** : `extract_pdf_images()` pour les éléments visuels
4. **Recherche** : `search_in_pdf()` pour localiser des éléments spécifiques
5. **Données** : `extract_pdf_tables()` pour les tableaux et statistiques

## 🐛 Dépannage

### Erreurs courantes

1. **Module non trouvé**
   ```
   ModuleNotFoundError: No module named 'PyPDF2'
   ```
   Solution : Réinstallez les dépendances avec `setup_pdf_analyzer_mcp.bat`

2. **Fichier PDF corrompu**
   ```
   PDF file is corrupted or invalid
   ```
   Solution : Vérifiez l'intégrité du fichier PDF

3. **Mémoire insuffisante**
   Pour les gros PDF avec beaucoup d'images, augmentez la mémoire Python :
   ```python
   import sys
   sys.setrecursionlimit(10000)
   ```

## 📊 Performances

- **Texte** : ~100 pages/seconde
- **Images** : ~10-20 images/seconde selon la taille
- **Métadonnées** : Instantané
- **Recherche** : ~50 pages/seconde

## 🔒 Sécurité

- Le serveur n'effectue que des opérations de lecture
- Aucune modification des PDF sources
- Les images extraites sont stockées temporairement
- Nettoyage automatique des fichiers temporaires

## 📝 Exemples d'utilisation avancée

### Analyse complète avec filtrage
```python
# Analyser seulement les 10 premières pages
result = analyze_pdf(
    pdf_path="document.pdf",
    page_range="1-10",
    extract_images=True,
    extract_text=True
)

# Statistiques
print(f"Nombre de mots: {result['statistics']['text']['total_words']}")
print(f"Images trouvées: {result['statistics']['images']['total_count']}")
```

### Extraction d'images haute qualité
```python
# Extraire uniquement les grandes images
images = extract_pdf_images(
    pdf_path="presentation.pdf",
    min_width=400,
    min_height=300,
    image_format="png",
    output_format="base64"
)
```

### Recherche avancée
```python
# Rechercher un terme exact
matches = search_in_pdf(
    pdf_path="cours.pdf",
    search_text="théorème de Pythagore",
    case_sensitive=False,
    whole_words=False
)

# Afficher les contextes
for match in matches["matches"]:
    print(f"Page {match['page']}: ...{match['context']}...")
```