# Guide d'utilisation - Serveur MCP LaTeX Search

## 🎯 Objectif

Ce serveur MCP permet à tes agents de rechercher automatiquement dans tes packages LaTeX pour :
- Comprendre comment les commandes sont définies
- Analyser le code source des packages
- Se documenter automatiquement sur les fonctionnalités disponibles
- Adapter et personnaliser le code existant

## 🚀 Installation rapide

### Étape 1 : Installation
Exécute le fichier `setup_latex_mcp.bat` :
```bash
setup_latex_mcp.bat
```

### Étape 2 : Vérification
```bash
claude mcp list
```
Tu devrais voir `latex-search-server` dans la liste.

## 🔧 Outils disponibles

### 1. `search_exact_command`
**Recherche exacte d'une définition de commande LaTeX**

**Usage :**
```
search_exact_command command_name="exercice"
```

**Exemple de résultat :**
- Fichier où la commande est définie
- Numéro de ligne exact
- Contexte autour de la définition
- Code complet de la définition

### 2. `search_fuzzy_command` 
**Recherche floue/approximative**

**Usage :**
```
search_fuzzy_command command_pattern="exer" max_results=10
```

**Caractéristiques :**
- Recherche même avec orthographe approximative
- Score de pertinence (100% = correspondance exacte)
- Triés par relevance
- Bonus pour les définitions longues et complexes

### 3. `list_available_packages`
**Liste tous les packages configurés**

**Usage :**
```
list_available_packages
```

**Retourne :**
- Chemins des packages
- Nombre de fichiers dans chaque package
- Extensions supportées (.tex, .sty, .cls, .dtx)

### 4. `scan_package_commands`
**Scan complet des commandes d'un package**

**Usage :**
```
# Scanner un package spécifique
scan_package_commands package_name="BFcours" max_results=50

# Scanner tous les packages
scan_package_commands max_results=100
```

**Utilité :**
- Vue d'ensemble de toutes les commandes disponibles
- Découverte de commandes oubliées
- Audit des packages

### 5. `get_command_definition`
**Définition complète avec contexte étendu**

**Usage :**
```
get_command_definition command_name="tcbitem" show_context=true
```

**Caractéristiques :**
- Contexte étendu (10 lignes avant/après)
- Toutes les occurrences de la commande
- Idéal pour comprendre l'implémentation complète

## 📝 Patterns LaTeX supportés

Le serveur reconnaît ces types de définitions :
- `\newcommand{\maCommande}` et `\renewcommand`
- `\def\maCommande` et variantes (`\gdef`, `\edef`, `\xdef`)
- `\newenvironment{monEnv}` et `\renewenvironment`
- `\newtcolorbox{maBoite}` et `\DeclareTColorBox`
- `\newtheorem{monTheoreme}` et `\newcounter`
- Commandes LaTeX3 (`\NewDocumentCommand`, `\DeclareDocumentCommand`, etc.)
- `\definecolor{maCouleur}`

## 🎯 Exemples d'utilisation pour les agents

### Découvrir les commandes disponibles
```
Utilise list_available_packages pour voir quels packages sont disponibles, puis scan_package_commands pour découvrir toutes les commandes du package BFcours
```

### Comprendre une commande spécifique
```
Utilise search_exact_command pour trouver la définition de "tcbitem" puis get_command_definition pour avoir le contexte complet
```

### Recherche exploratoire
```
Utilise search_fuzzy_command avec "couleur" pour trouver toutes les commandes liées aux couleurs dans mes packages
```

### Analyse de code pour personnalisation
```
Utilise get_command_definition avec show_context=true pour analyser complètement la commande "MultiColonnes" et comprendre comment elle fonctionne
```

## 🛠️ Configuration

Le serveur utilise la configuration depuis `../base-scripts/config.json` :
```json
{
  "packageDirs": [
    "C:\\chemin\\vers\\BFcours",
    "C:\\chemin\\vers\\autres\\packages"
  ],
  "fileExtensions": [".tex", ".sty", ".cls", ".dtx"],
  "maxResults": 20
}
```

## 💡 Avantages pour les agents

- **Auto-documentation** : Les agents peuvent découvrir tes commandes automatiquement
- **Compréhension du code** : Analyse du code source pour adaptation
- **Exploration** : Découverte de fonctionnalités cachées ou oubliées  
- **Contextualisation** : Compréhension complète avec le contexte
- **Efficacité** : Plus besoin de chercher manuellement dans les fichiers

## 🔍 Test rapide

Une fois installé, teste avec :
```
Utilise search_exact_command pour trouver la définition de "chapitre"
```

Tes agents peuvent maintenant explorer et comprendre tes packages LaTeX de façon autonome ! 🚀