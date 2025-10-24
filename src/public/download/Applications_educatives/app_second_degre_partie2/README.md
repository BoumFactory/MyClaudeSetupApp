# Second Degré - Partie 2 - Révisions 1ère Spé

Application éducative interactive pour réviser la factorisation des trinômes du second degré.

## Description

Cette application complète permet aux élèves de **Première Spécialité** de réviser la **Partie 2** du cours sur le second degré de manière interactive et autonome.

### Contenu pédagogique

L'application couvre 3 grandes sections :

1. **Factorisation d'un trinôme**
   - Définition du discriminant
   - Forme factorisée selon le signe de Δ

2. **Signe du trinôme et discriminant**
   - Tableau de signes
   - Méthode pour établir le tableau de signes

3. **Équations et inéquations du second degré**
   - Résolution d'équations
   - Résolution d'inéquations

### Exercices interactifs

4 exercices corrigés avec :
- Vérification automatique des réponses
- Indices disponibles
- Solutions détaillées
- Système de points (20 points au total)

## Fonctionnalités

- ✅ Interface moderne et responsive (mobile/desktop)
- ✅ Formules mathématiques rendues avec MathJax
- ✅ Vérification automatique des réponses
- ✅ Feedback immédiat et solutions détaillées
- ✅ Système de progression et score
- ✅ Sauvegarde automatique de la progression (localStorage)
- ✅ Navigation fluide entre cours et exercices
- ✅ Design professionnel avec thème éducatif

## Installation et Utilisation

### Option 1 : Exécutable Standalone (Recommandé pour les élèves)

#### Windows

1. Télécharger `SecondDegre_Partie2.exe` depuis le dossier `dist/`
2. Double-cliquer sur l'exécutable
3. Attendre quelques secondes (démarrage du serveur Flask)
4. L'application s'ouvre automatiquement dans votre navigateur
5. Si ce n'est pas le cas, ouvrir : http://localhost:5000

**Note** : Aucune installation de Python ou dépendance nécessaire.

### Option 2 : Depuis les Sources (Pour développement)

#### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

#### Installation

```bash
# Se placer dans le répertoire de l'application
cd Applications_educatives/app_second_degre_partie2

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py
```

L'application sera accessible sur `http://localhost:5000`

#### Ports

- **Cours** : http://localhost:5000/
- **Exercices** : http://localhost:5000/exercices

## Utilisation

### Page Cours

1. Consultez les compétences travaillées
2. Parcourez les 3 sections de cours
3. Lisez les définitions, propriétés et méthodes
4. Cliquez sur "Aller aux exercices" pour vous entraîner

### Page Exercices

1. Lisez attentivement chaque question
2. Remplissez tous les champs de réponse
3. Cliquez sur "Vérifier ma réponse" ou appuyez sur Entrée
4. Consultez le feedback :
   - ✅ Réponse correcte : points gagnés
   - ❌ Réponse incorrecte : consultez la solution détaillée
5. Utilisez l'indice si vous êtes bloqué
6. Votre progression est sauvegardée automatiquement

### Système de notation

- **Exercice 1** : 3 points (Facile)
- **Exercice 2** : 5 points (Facile)
- **Exercice 3** : 6 points (Moyen)
- **Exercice 4** : 6 points (Moyen)
- **Total** : 20 points

## Développement

### Structure du projet

```
app_second_degre_partie2/
├── app.py                      # Application Flask principale
├── config.py                   # Configuration
├── requirements.txt            # Dépendances Python
├── requirements-dev.txt        # Dépendances de développement
├── .env.example               # Exemple de variables d'environnement
├── static/
│   ├── css/
│   │   ├── main.css           # Styles principaux
│   │   └── components.css     # Styles des composants
│   └── js/
│       ├── utils.js           # Fonctions utilitaires
│       ├── main.js            # Script principal
│       └── exercises.js       # Logique des exercices
├── templates/
│   ├── base.html              # Template de base
│   ├── index.html             # Page cours
│   ├── exercices.html         # Page exercices
│   └── error.html             # Page d'erreur
├── data/
│   └── content.json           # Contenu éducatif structuré
├── tests/
│   └── test_app.py            # Tests automatisés
├── build/
│   └── build_exe.py           # Script de build PyInstaller
└── dist/                      # Exécutables générés
```

### Tests

Lancer les tests automatisés :

```bash
# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Lancer les tests
pytest tests/ -v

# Avec rapport de couverture
pytest tests/ --cov=app --cov-report=html
```

### Build de l'exécutable

```bash
# Installer PyInstaller
pip install pyinstaller

# Construire l'exécutable
python build/build_exe.py

# L'exécutable sera dans dist/SecondDegre_Partie2.exe
```

### Personnalisation

#### Modifier le contenu

Éditer le fichier `data/content.json` pour :
- Ajouter/modifier des sections de cours
- Ajouter/modifier des exercices
- Changer les réponses attendues

#### Modifier le style

Éditer les fichiers CSS dans `static/css/` :
- `main.css` : Variables CSS, layout général
- `components.css` : Styles spécifiques aux composants

#### Modifier la logique

Éditer les fichiers JS dans `static/js/` :
- `utils.js` : Fonctions utilitaires
- `main.js` : Script principal (toutes les pages)
- `exercises.js` : Logique des exercices

## Technologies

- **Backend** : Flask 3.0 (Python)
- **Frontend** : HTML5, CSS3, JavaScript ES6+
- **Formules mathématiques** : MathJax 3
- **Tests** : pytest, pytest-flask
- **Packaging** : PyInstaller 6.3

## Compétences travaillées

1. Calculer le discriminant associé à un polynôme de degré 2
2. Connaître le lien entre discriminant et signe d'un polynôme de degré 2
3. Dresser le tableau de signes d'une fonction polynôme de degré 2
4. Résoudre des équations et des inéquations du second degré

## Licence

Application éducative créée pour le **Lycée Camille Claudel**.
Version 1.0.0 - 2025

## Support

Pour toute question ou problème :
- Consulter ce README
- Vérifier la console du navigateur (F12)
- Consulter les logs de l'application
- Contacter l'équipe pédagogique

## Crédits

- **Contenu pédagogique** : Cours de Première Spécialité, Lycée Camille Claudel
- **Développement** : Educational App Builder
- **Technologies** : Flask, MathJax, PyInstaller
