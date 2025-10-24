# Scripts de recherche de commandes LaTeX

Deux scripts Node.js pour rechercher efficacement des définitions de commandes LaTeX dans vos packages personnels.

## 📁 Fichiers

- `find_latex_def_command.js` : Recherche exacte de commandes
- `large_find_latex_def_commands.js` : Recherche floue avec gestion de la casse
- `config.json` : Configuration pour la recherche exacte
- `large_config.json` : Configuration pour la recherche floue

## 🚀 Installation

1. Assurez-vous d'avoir Node.js installé sur votre système ( https://nodejs.org/fr/download )
2. Placez tous les fichiers dans le même répertoire
3. Configurez les chemins de recherche dans `config.json` et `large_config.json`

## ⚙️ Configuration

### config.json / large_config.json

```json
{
  "packageDirs": [
    "C:\\chemin\\vers\\vos\\packages1",
    "C:\\chemin\\vers\\vos\\packages2"
  ],
  "fileExtensions": [".tex", ".sty", ".cls", ".dtx"],
  "nbResultatMax": 20  // uniquement dans large_config.json
}
```

## 📋 Utilisation

### Recherche exacte

Pour trouver une commande dont vous connaissez le nom exact :

```bash
# Mode interactif
node find_latex_def_command.js

# Recherche directe
node find_latex_def_command.js nomCommande
```

**Exemple :**
```bash
node find_latex_def_command.js exercice
```

### Recherche floue

Pour trouver des commandes même si vous n'êtes pas sûr de l'orthographe :

```bash
# Mode interactif
node large_find_latex_def_commands.js

# Recherche directe
node large_find_latex_def_commands.js termeApproximatif
```

**Exemple :**
```bash
node large_find_latex_def_commands.js exer
```

## 🎯 Fonctionnalités

### Recherche exacte
- ✅ Recherche rapide et précise
- ✅ Ouverture automatique dans VS Code à la ligne exacte
- ✅ Support de multiples résultats avec sélection

### Recherche floue
- ✅ Gestion intelligente de la casse (camelCase, snake_case, etc.)
- ✅ Score de pertinence basé sur :
  - Similarité du nom
  - Longueur de la définition
  - Présence d'environnements LaTeX
- ✅ Filtrage automatique :
  - ❌ Commandes commençant par "old" (ignorées)
  - ⬇️ Fichier `bfcours-useCanMathalea.sty` (score réduit de 90%)
- ✅ Affichage des résultats triés par pertinence
- ✅ Intégration avec la recherche exacte

## 📊 Interprétation des scores

Dans la recherche floue, les scores indiquent la pertinence :
- **100%** : Correspondance exacte
- **90%+** : Commence par le terme recherché
- **70%+** : Contient le terme recherché
- **Bonus** : +15 points max pour la longueur, +20 points pour les environnements

## 💡 Conseils d'utilisation

1. **Recherche quotidienne** : Utilisez `find_latex_def_command.js` quand vous connaissez le nom exact
2. **Exploration** : Utilisez `large_find_latex_def_commands.js` pour découvrir des commandes similaires
3. **Raccourcis** : Créez des alias dans votre shell :
   ```bash
   alias fltx='node /chemin/vers/find_latex_def_command.js'
   alias fltxl='node /chemin/vers/large_find_latex_def_commands.js'
   ```

## 🔧 Dépannage

- **Erreur "config.json not found"** : Le script utilisera une configuration par défaut
- **Aucun résultat trouvé** : Vérifiez les chemins dans les fichiers de configuration
- **VS Code ne s'ouvre pas** : Le script essaiera d'ouvrir avec l'application par défaut

## 📝 Notes

- Les recherches sont récursives dans tous les sous-dossiers
- Les patterns LaTeX supportés incluent : `\newcommand`, `\def`, `\newenvironment`, `\newtcolorbox`, etc.
- La recherche floue limite les résultats au nombre configuré dans `nbResultatMax`
