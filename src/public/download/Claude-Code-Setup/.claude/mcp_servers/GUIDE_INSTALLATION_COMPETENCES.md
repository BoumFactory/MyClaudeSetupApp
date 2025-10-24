# Guide d'installation - Serveur MCP Compétences

## 🚀 Installation rapide

### Étape 1 : Installation des dépendances
```bash
pip install "mcp[cli]"
```

### Étape 2 : Ajout du serveur à Claude Code

Utilise l'une de ces méthodes :

#### Méthode automatique (recommandée)
Exécute le fichier `setup_mcp.bat` :
```bash
setup_mcp.bat
```

#### Méthode manuelle
```bash
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\.claude\mcp_servers"
claude mcp add --scope project competences-server -- python competences_server_fixed.py
```

## ✅ Vérification de l'installation

### 1. Vérifier que le serveur est ajouté
```bash
claude mcp list
```
Tu devrais voir `competences-server` dans la liste.

### 2. Vérifier le statut du serveur
```bash
/mcp
```
Dans Claude Code, cette commande affiche l'état de tous les serveurs MCP.

## 🛠️ Outils disponibles

Une fois installé, tes agents auront accès à ces 10 outils :

1. **`search_competences`** - Recherche par texte libre
2. **`filter_by_niveau`** - Filtre par niveau scolaire  
3. **`filter_by_theme`** - Filtre par thème
4. **`filter_by_palier`** - Filtre par palier de difficulté
5. **`get_competence_by_code`** - Recherche par code exact
6. **`get_niveaux_available`** - Liste des niveaux disponibles
7. **`get_themes_available`** - Liste des thèmes disponibles  
8. **`get_paliers_available`** - Liste des paliers disponibles
9. **`get_competences_stats`** - Statistiques générales
10. **`advanced_search`** - Recherche multicritères

## 🔧 Dépannage

### Le serveur n'apparaît pas dans `claude mcp list`
1. Vérifiez que vous êtes dans le bon répertoire
2. Réexécutez la commande d'ajout
3. Vérifiez que Python est dans le PATH

### Erreur "Module 'mcp' not found"
```bash
pip install "mcp[cli]"
```

### Le serveur ne répond pas
1. Vérifiez que le fichier `competences.json` existe dans `../datas/`
2. Vérifiez les permissions du fichier
3. Consultez les logs avec `/mcp` dans Claude Code

### Erreur de chemin sur Windows
Assurez-vous d'utiliser des chemins complets avec des antislashes doubles (`\\`) ou des slashes normaux (`/`).

## 📁 Structure des fichiers

```
.claude/
├── mcp_servers/
│   ├── competences_server_fixed.py  # Serveur principal
│   ├── requirements.txt             # Dépendances
│   ├── setup_mcp.bat               # Installation automatique
│   └── README.md                   # Documentation
├── datas/
│   └── competences.json            # Base de données (286 compétences)
└── .mcp.json                       # Configuration du projet
```

## 🎯 Test rapide

Une fois installé, teste dans Claude Code :
```
Utilise get_competences_stats pour afficher les statistiques des compétences
```

Tes agents devraient maintenant pouvoir accéder aux 286 compétences du programme !