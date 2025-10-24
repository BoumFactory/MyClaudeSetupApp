---
name: educational-app-builder
description: Skill complet pour créer des applications éducatives interactives basées sur Flask. Génère un projet Flask complet (backend Python, frontend HTML/CSS/JS) à partir de ressources éducatives. Inclut outils de packaging en exécutable standalone et tests automatisés.
---

# Educational App Builder - Créateur d'Applications Éducatives Interactives

## Vue d'ensemble

Ce skill permet de transformer n'importe quelle ressource éducative (document LaTeX, PDF, exercices, cours) en application web interactive standalone. L'application générée est complète, testée et packagée en exécutable monofichier pour une distribution facile.

## Objectifs

1. Analyser une ressource éducative (fichier, contenu)
2. Créer une application Flask complète et fonctionnelle
3. Générer un frontend moderne et interactif (HTML/CSS/JS)
4. Tester automatiquement l'application
5. Packager en exécutable standalone (.exe Windows)
6. Fournir documentation d'utilisation et de déploiement

## Architecture de l'Application Flask

### Structure de Projet Standard

```
app_<nom_ressource>/
├── app.py                     # Application Flask principale
├── config.py                  # Configuration de l'application
├── requirements.txt           # Dépendances Python
├── .env.example              # Variables d'environnement exemple
├── static/                   # Fichiers statiques
│   ├── css/
│   │   ├── main.css         # Styles principaux
│   │   └── components.css   # Composants réutilisables
│   ├── js/
│   │   ├── main.js          # JavaScript principal
│   │   ├── interactions.js  # Interactions utilisateur
│   │   └── utils.js         # Fonctions utilitaires
│   ├── images/              # Images et ressources
│   └── fonts/               # Polices personnalisées
├── templates/               # Templates Jinja2
│   ├── base.html           # Template de base
│   ├── index.html          # Page d'accueil
│   ├── components/         # Composants réutilisables
│   └── partials/           # Fragments HTML
├── data/                   # Données de l'application
│   ├── content.json        # Contenu éducatif structuré
│   └── resources/          # Ressources additionnelles
├── tests/                  # Tests automatisés
│   ├── test_app.py        # Tests de l'application
│   └── test_routes.py     # Tests des routes
├── build/                  # Scripts de build
│   ├── build_exe.py       # Script PyInstaller
│   └── build.spec         # Configuration PyInstaller
├── dist/                   # Exécutables générés (ignoré par git)
└── README.md              # Documentation

```

### Composants Techniques Essentiels

#### 1. Application Flask (app.py)

**Structure de base** :

```python
from flask import Flask, render_template, jsonify, request, send_from_directory
from config import Config
import json
import os

app = Flask(__name__)
app.config.from_object(Config)

# Chargement des données éducatives
def load_educational_content():
    with open(os.path.join('data', 'content.json'), 'r', encoding='utf-8') as f:
        return json.load(f)

CONTENT = load_educational_content()

@app.route('/')
def index():
    """Page d'accueil principale"""
    return render_template('index.html', title="Application Éducative")

@app.route('/api/content')
def get_content():
    """API pour récupérer le contenu"""
    return jsonify(CONTENT)

@app.route('/api/check_answer', methods=['POST'])
def check_answer():
    """Vérifier une réponse d'exercice"""
    data = request.get_json()
    # Logique de vérification
    return jsonify({'correct': True, 'feedback': 'Bravo !'})

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
```

#### 2. Configuration (config.py)

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration de l'application"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'

    # Chemins
    STATIC_FOLDER = 'static'
    TEMPLATE_FOLDER = 'templates'
    DATA_FOLDER = 'data'

    # Paramètres éducatifs
    APP_NAME = os.environ.get('APP_NAME', 'Application Éducative')
    APP_VERSION = '1.0.0'
```

#### 3. Frontend HTML/CSS/JS

**Base Template (templates/base.html)** :

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title }}{% endblock %}</title>

    <!-- Styles -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/components.css') }}">

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">

    {% block extra_css %}{% endblock %}
</head>
<body>
    <div class="app-container">
        <!-- Navigation -->
        <nav class="navbar">
            <div class="nav-brand">
                <h1>{{ config.APP_NAME }}</h1>
            </div>
            {% block nav %}{% endblock %}
        </nav>

        <!-- Contenu principal -->
        <main class="main-content">
            {% block content %}{% endblock %}
        </main>

        <!-- Footer -->
        <footer class="footer">
            {% block footer %}
            <p>&copy; 2025 Application Éducative - Version {{ config.APP_VERSION }}</p>
            {% endblock %}
        </footer>
    </div>

    <!-- Scripts -->
    <script src="{{ url_for('static', filename='js/utils.js') }}"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

**CSS Moderne (static/css/main.css)** :

```css
:root {
    --primary-color: #4F46E5;
    --secondary-color: #10B981;
    --danger-color: #EF4444;
    --background: #F9FAFB;
    --surface: #FFFFFF;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --border-color: #E5E7EB;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background: var(--background);
    color: var(--text-primary);
    line-height: 1.6;
}

.app-container {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Navigation */
.navbar {
    background: var(--surface);
    padding: 1rem 2rem;
    box-shadow: var(--shadow);
    border-bottom: 1px solid var(--border-color);
}

.nav-brand h1 {
    font-size: 1.5rem;
    color: var(--primary-color);
    font-weight: 700;
}

/* Contenu principal */
.main-content {
    flex: 1;
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
}

/* Composants réutilisables */
.card {
    background: var(--surface);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.5rem;
}

.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
    font-size: 1rem;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: #4338CA;
    transform: translateY(-1px);
    box-shadow: 0 4px 6px rgba(79, 70, 229, 0.3);
}

/* Footer */
.footer {
    background: var(--surface);
    padding: 2rem;
    text-align: center;
    border-top: 1px solid var(--border-color);
    color: var(--text-secondary);
}
```

**JavaScript Interactif (static/js/main.js)** :

```javascript
// API Client
class EducationalAppAPI {
    constructor() {
        this.baseURL = window.location.origin;
    }

    async getContent() {
        const response = await fetch(`${this.baseURL}/api/content`);
        return await response.json();
    }

    async checkAnswer(questionId, answer) {
        const response = await fetch(`${this.baseURL}/api/check_answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ questionId, answer })
        });
        return await response.json();
    }
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    const api = new EducationalAppAPI();
    console.log('Application éducative chargée');

    // Charger le contenu initial
    api.getContent().then(content => {
        console.log('Contenu chargé:', content);
    });
});
```

## Packaging en Exécutable Standalone

### Prérequis

**Dépendances pour PyInstaller** :

```txt
# requirements.txt
Flask==3.0.0
python-dotenv==1.0.0
Jinja2==3.1.2
Werkzeug==3.0.1

# requirements-dev.txt (pour le développement)
pytest==7.4.3
pytest-flask==1.3.0
pyinstaller==6.3.0
```

### Script de Build (build/build_exe.py)

```python
import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Configuration
APP_NAME = "EducationalApp"
MAIN_SCRIPT = "app.py"
ICON_PATH = "static/images/icon.ico"  # Optionnel

def clean_build():
    """Nettoyer les dossiers de build précédents"""
    folders = ['build', 'dist', '__pycache__']
    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    # Supprimer les fichiers .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()

def build_executable():
    """Construire l'exécutable avec PyInstaller"""

    args = [
        MAIN_SCRIPT,
        '--name', APP_NAME,
        '--onefile',  # Un seul fichier exécutable
        '--windowed',  # Pas de console (optionnel)
        '--add-data', 'templates;templates',
        '--add-data', 'static;static',
        '--add-data', 'data;data',
        '--hidden-import', 'flask',
        '--hidden-import', 'jinja2',
        '--clean',
    ]

    # Ajouter l'icône si disponible
    if os.path.exists(ICON_PATH):
        args.extend(['--icon', ICON_PATH])

    print(f"Building {APP_NAME}...")
    PyInstaller.__main__.run(args)
    print(f"\nBuild complete! Executable: dist/{APP_NAME}.exe")

if __name__ == '__main__':
    clean_build()
    build_executable()
```

### Utilisation du Build

```bash
# Installer PyInstaller
pip install pyinstaller

# Construire l'exécutable
python build/build_exe.py

# L'exécutable sera dans dist/EducationalApp.exe
```

## Tests Automatisés

### Tests de l'Application (tests/test_app.py)

```python
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test de la page d'accueil"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Application' in response.data

def test_api_content(client):
    """Test de l'API de contenu"""
    response = client.get('/api/content')
    assert response.status_code == 200
    assert response.is_json

def test_check_answer(client):
    """Test de vérification de réponse"""
    response = client.post('/api/check_answer', json={
        'questionId': 1,
        'answer': 'test'
    })
    assert response.status_code == 200
    assert 'correct' in response.get_json()
```

### Lancer les Tests

```bash
# Installer pytest
pip install pytest pytest-flask

# Lancer les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html
```

## Workflow de Création Automatique

### 1. Analyse de la Ressource

L'agent doit extraire :
- Type de ressource (exercices, cours, évaluation, etc.)
- Niveau scolaire
- Thème/Sujet
- Structure du contenu (sections, exercices, questions)
- Éléments interactifs potentiels

### 2. Génération du Contenu JSON

```json
{
    "metadata": {
        "title": "Exercices sur les Vecteurs",
        "level": "Seconde",
        "theme": "Vecteurs",
        "type": "exercices",
        "version": "1.0.0"
    },
    "sections": [
        {
            "id": 1,
            "title": "Introduction aux vecteurs",
            "type": "theory",
            "content": "Les vecteurs sont...",
            "images": []
        },
        {
            "id": 2,
            "title": "Exercices d'application",
            "type": "exercises",
            "exercises": [
                {
                    "id": 1,
                    "question": "Calculer le vecteur AB...",
                    "type": "input",
                    "answer": "3",
                    "hint": "Utiliser la formule...",
                    "solution": "Détail de la solution..."
                }
            ]
        }
    ]
}
```

### 3. Types d'Applications Éducatives

#### Type A : Visualiseur de Cours Interactif
- Affichage structuré du cours
- Navigation par sections
- Recherche dans le contenu
- Annotations personnelles
- Export PDF

#### Type B : Exerciseur avec Correction Automatique
- Affichage des exercices
- Saisie de réponses
- Vérification automatique
- Feedback immédiat
- Suivi de progression

#### Type C : Quiz Interactif
- Questions à choix multiples
- Questions ouvertes
- Timer configurable
- Score final
- Historique des tentatives

#### Type D : Application Mixte (Recommandé)
- Combinaison de cours et exercices
- Progression guidée
- Tableau de bord
- Statistiques d'apprentissage

## Fonctionnalités Avancées

### 1. Rendu LaTeX dans le Browser

Pour afficher des formules mathématiques :

```html
<!-- Dans base.html -->
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

<!-- Configuration -->
<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  }
};
</script>
```

### 2. Sauvegarde de Progression (LocalStorage)

```javascript
// utils.js
class ProgressManager {
    constructor(appId) {
        this.appId = appId;
        this.storageKey = `edu_app_${appId}_progress`;
    }

    saveProgress(data) {
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    loadProgress() {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : null;
    }

    clearProgress() {
        localStorage.removeItem(this.storageKey);
    }
}
```

### 3. Mode Hors Ligne (PWA)

**Service Worker basique** :

```javascript
// static/sw.js
const CACHE_NAME = 'edu-app-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/api/content'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});
```

## Documentation Utilisateur

### README.md Standard

```markdown
# [Nom de l'Application]

Application éducative interactive sur [Thème] - Niveau [Niveau]

## Installation

### Option 1 : Exécutable Standalone (Recommandé)

1. Télécharger `EducationalApp.exe`
2. Double-cliquer pour lancer
3. L'application s'ouvre dans le navigateur par défaut

### Option 2 : Depuis les sources

1. Installer Python 3.8+
2. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
3. Lancer l'application :
   ```bash
   python app.py
   ```
4. Ouvrir http://localhost:5000

## Utilisation

[Instructions spécifiques à l'application]

## Développement

### Tests
```bash
pytest tests/ -v
```

### Build
```bash
python build/build_exe.py
```

## Support

Pour toute question : [contact]
```

## Checklist de Qualité

Avant de livrer l'application, vérifier :

- [ ] L'application Flask démarre sans erreur
- [ ] Tous les tests passent (pytest)
- [ ] Le frontend est responsive (mobile/tablet/desktop)
- [ ] Les formules LaTeX s'affichent correctement (si applicable)
- [ ] L'exécutable se construit sans erreur
- [ ] L'exécutable fonctionne sur un système propre
- [ ] Le README est complet et clair
- [ ] Le code est commenté en français
- [ ] Les chemins de fichiers sont portables (Windows/Linux)
- [ ] Les données sensibles ne sont pas hardcodées

## Ressources et Références

### Libraries Frontend Recommandées

- **MathJax** : Rendu de formules mathématiques
- **Chart.js** : Graphiques de progression
- **TailwindCSS** : Framework CSS moderne (optionnel)
- **Alpine.js** : Interactions légères (alternative à JS vanilla)

### Outils de Développement

- **Flask-CORS** : Si besoin d'API externe
- **Flask-Session** : Gestion de sessions
- **SQLite** : Base de données légère (si besoin de persistance)

## Exemples de Templates par Type de Ressource

### Exercices LaTeX → Application Exerciseur

```python
# Extraction automatique depuis LaTeX
import re

def parse_latex_exercises(latex_content):
    """Parser pour extraire exercices depuis LaTeX"""
    exercises = []

    # Regex pour détecter les environnements d'exercices
    pattern = r'\\begin{exercice}(.*?)\\end{exercice}'
    matches = re.findall(pattern, latex_content, re.DOTALL)

    for i, match in enumerate(matches, 1):
        exercises.append({
            'id': i,
            'content': match.strip(),
            'type': 'open'
        })

    return exercises
```

### Cours LaTeX → Visualiseur

```python
def parse_latex_course(latex_content):
    """Parser pour extraire sections de cours"""
    sections = []

    # Détecter les sections
    pattern = r'\\section{(.*?)}(.*?)(?=\\section|$)'
    matches = re.findall(pattern, latex_content, re.DOTALL)

    for i, (title, content) in enumerate(matches, 1):
        sections.append({
            'id': i,
            'title': title,
            'content': content.strip(),
            'type': 'theory'
        })

    return sections
```

## Optimisations Performance

### 1. Compression des Assets

```python
# Dans app.py
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  # Active la compression gzip
```

### 2. Cache Statique

```python
# Configuration du cache
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename,
                             max_age=31536000)  # 1 an
```

### 3. Lazy Loading Images

```html
<img src="placeholder.jpg"
     data-src="actual-image.jpg"
     loading="lazy"
     alt="Description">
```

## Notes Importantes

- **Encodage** : TOUJOURS utiliser UTF-8 pour tous les fichiers
- **Chemins** : Utiliser `os.path.join()` pour la portabilité
- **Sécurité** : Ne jamais exposer de données sensibles côté client
- **Performance** : Minimiser les requêtes réseau, utiliser le cache
- **Accessibilité** : Respecter les standards WCAG 2.1
- **Documentation** : Commenter le code complexe en français

## Conclusion

Ce skill fournit tous les outils et templates nécessaires pour créer des applications éducatives de qualité professionnelle. L'agent qui utilise ce skill doit :

1. Analyser intelligemment la ressource fournie
2. Choisir le bon type d'application
3. Générer un code propre et testé
4. Packager l'application en exécutable
5. Fournir une documentation complète

L'objectif final est de livrer un produit fini, prêt à l'emploi, sans intervention manuelle supplémentaire.
