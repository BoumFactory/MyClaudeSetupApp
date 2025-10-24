# /create-app - Créer une Application Éducative Interactive

## Description

Transforme automatiquement une ressource éducative (fichier LaTeX, PDF, document, ou dossier) en application web interactive complète et standalone.

Cette commande lance l'agent spécialisé `app-creator-agent` qui :
- Analyse la ressource fournie
- Crée une application Flask complète (backend + frontend)
- Génère un exécutable standalone (.exe)
- Fournit une documentation complète

## Usage

```bash
/create-app <chemin_vers_ressource> [options]
```

### Arguments

- `<chemin_vers_ressource>` : Chemin vers le fichier ou dossier à transformer
  - Fichier `.tex` (LaTeX)
  - Fichier `.pdf`
  - Fichier `.md` (Markdown)
  - Dossier contenant plusieurs fichiers
  - Texte brut copié-collé

### Options (optionnelles)

- `--name <nom>` : Nom de l'application (par défaut : basé sur le fichier)
- `--type <type>` : Type d'application (exerciseur, visualiseur, quiz, mixte)
- `--no-exe` : Ne pas générer l'exécutable (dev uniquement)
- `--test-only` : Générer et tester sans construire l'exe

## Exemples

### Exemple 1 : Transformer des exercices LaTeX

```bash
/create-app ./1. Cours/2nde/Sequence-Vecteurs/Exercices_vecteurs.tex
```

**Résultat** :
- Application exerciseur interactive
- Vérification automatique des réponses
- Feedback et solutions
- Exécutable `EducationalApp.exe` généré

### Exemple 2 : Transformer un cours PDF

```bash
/create-app ./Documents/Cours_fonctions.pdf --name "CoursInteractifFonctions"
```

**Résultat** :
- Visualiseur de cours avec navigation
- Formules mathématiques rendues
- Recherche dans le contenu
- Exécutable personnalisé

### Exemple 3 : Dossier complet (cours + exercices)

```bash
/create-app ./1. Cours/1ere_spe/Sequence-Produit_scalaire/ --type mixte
```

**Résultat** :
- Application mixte (cours + exercices)
- Navigation entre sections
- Mode exercices interactif
- Tableau de bord de progression

### Exemple 4 : Développement rapide (sans exe)

```bash
/create-app ./Exercices.tex --no-exe
```

**Résultat** :
- Application Flask créée et testée
- Pas de build d'exécutable (gain de temps)
- Prête pour le développement

## Workflow Automatique

Lorsque vous lancez `/create-app`, l'agent :

### Phase 1 : Analyse (30 secondes)
1. ✅ Lit la ressource fournie
2. ✅ Détecte le type de contenu (cours, exercices, etc.)
3. ✅ Extrait les métadonnées (niveau, thème)
4. ✅ Identifie le type d'application optimal

### Phase 2 : Questions (1 minute max)
1. ❓ Confirme le nom de l'application
2. ❓ Valide le type détecté (si ambiguïté)
3. ❓ Demande les fonctionnalités optionnelles

**Note** : L'agent pose 3-4 questions maximum et continue automatiquement avec des valeurs par défaut si pas de réponse.

### Phase 3 : Génération (2-3 minutes)
1. ✅ Crée la structure du projet Flask
2. ✅ Génère le backend Python (app.py, config.py)
3. ✅ Crée le frontend (HTML, CSS, JS modernes)
4. ✅ Extrait et structure le contenu (JSON)
5. ✅ Génère les tests automatisés
6. ✅ Crée la documentation (README, guide)

### Phase 4 : Tests (1 minute)
1. ✅ Lance les tests automatisés (pytest)
2. ✅ Vérifie le démarrage de l'application
3. ✅ Teste les routes et API
4. ✅ Valide le rendu frontend

### Phase 5 : Packaging (2-3 minutes)
1. ✅ Construit l'exécutable standalone (.exe)
2. ✅ Inclut tous les assets (templates, static, data)
3. ✅ Teste l'exécutable généré
4. ✅ Optimise la taille du fichier

### Phase 6 : Livraison (instantané)
1. ✅ Génère le rapport de création
2. ✅ Fournit les chemins d'accès
3. ✅ Donne les instructions d'utilisation
4. ✅ Suggère les prochaines étapes

**Temps total** : 5-10 minutes pour une application complète

## Structure de l'Application Générée

```
app_<nom>/
├── app.py                    # ✅ Application Flask
├── config.py                 # ✅ Configuration
├── requirements.txt          # ✅ Dépendances production
├── requirements-dev.txt      # ✅ Dépendances développement
├── README.md                 # ✅ Documentation principale
├── GUIDE_UTILISATION.md      # ✅ Guide utilisateur détaillé
├── .env.example             # ✅ Variables d'environnement
│
├── static/                   # Fichiers statiques
│   ├── css/
│   │   ├── main.css         # ✅ Styles principaux
│   │   └── components.css   # ✅ Composants UI
│   ├── js/
│   │   ├── main.js          # ✅ Logique principale
│   │   ├── interactions.js  # ✅ Interactions utilisateur
│   │   └── utils.js         # ✅ Fonctions utilitaires
│   ├── images/              # Images et ressources
│   └── fonts/               # Polices personnalisées
│
├── templates/               # Templates Jinja2
│   ├── base.html           # ✅ Template de base
│   ├── index.html          # ✅ Page principale
│   ├── components/         # Composants réutilisables
│   └── partials/           # Fragments HTML
│
├── data/                    # Données de l'application
│   ├── content.json        # ✅ Contenu structuré
│   └── resources/          # Ressources additionnelles
│
├── tests/                   # Tests automatisés
│   ├── test_app.py         # ✅ Tests application
│   ├── test_routes.py      # ✅ Tests routes API
│   └── test_content.py     # ✅ Tests contenu
│
├── build/                   # Scripts de build
│   ├── build_exe.py        # ✅ Script PyInstaller
│   └── build.spec          # Configuration build
│
└── dist/                    # Exécutables générés
    └── EducationalApp.exe  # ✅ Application standalone
```

## Types d'Applications Disponibles

### 1. Exerciseur Interactif

**Quand** : Ressource contient majoritairement des exercices/questions

**Fonctionnalités** :
- ✅ Affichage des exercices un par un
- ✅ Champs de saisie de réponses
- ✅ Vérification automatique
- ✅ Feedback immédiat (correct/incorrect)
- ✅ Indices sur demande
- ✅ Solutions détaillées
- ✅ Barre de progression
- ✅ Score final et statistiques

**Exemple** : Exercices sur les vecteurs, équations, probabilités

### 2. Visualiseur de Cours

**Quand** : Ressource contient majoritairement du cours/théorie

**Fonctionnalités** :
- ✅ Affichage structuré par sections
- ✅ Navigation fluide
- ✅ Table des matières dynamique
- ✅ Recherche dans le contenu
- ✅ Annotations personnelles
- ✅ Mode lecture optimisé
- ✅ Export PDF
- ✅ Marque-pages

**Exemple** : Cours sur les fonctions, dérivées, suites

### 3. Quiz Interactif

**Quand** : Ressource contient des QCM, questionnaires

**Fonctionnalités** :
- ✅ Questions à choix multiples
- ✅ Questions ouvertes
- ✅ Timer configurable
- ✅ Mode examen (une seule tentative)
- ✅ Correction immédiate ou différée
- ✅ Score détaillé par catégorie
- ✅ Historique des tentatives
- ✅ Classement (si mode multi-joueurs)

**Exemple** : QCM de révision, évaluations formatives

### 4. Application Mixte (Recommandé)

**Quand** : Ressource contient cours ET exercices

**Fonctionnalités** :
- ✅ **Tout des 3 types ci-dessus**
- ✅ Navigation entre cours et exercices
- ✅ Progression guidée
- ✅ Tableau de bord complet
- ✅ Mode révision
- ✅ Mode entraînement
- ✅ Statistiques d'apprentissage

**Exemple** : Séquence complète (cours + exos + éval)

## Fonctionnalités Techniques

### Backend (Flask)

- ✅ Routes API REST
- ✅ Gestion des sessions
- ✅ Configuration par environnement
- ✅ Logging structuré
- ✅ Gestion d'erreurs
- ✅ CORS (si nécessaire)

### Frontend (HTML/CSS/JS)

- ✅ Design responsive (mobile/tablet/desktop)
- ✅ Animations fluides
- ✅ Thème moderne et professionnel
- ✅ Rendu formules mathématiques (MathJax)
- ✅ LocalStorage pour progression
- ✅ Service Worker (mode hors ligne optionnel)

### Tests (pytest)

- ✅ Tests unitaires
- ✅ Tests d'intégration
- ✅ Tests de routes API
- ✅ Tests de rendu
- ✅ Couverture de code > 80%

### Packaging (PyInstaller)

- ✅ Exécutable monofichier
- ✅ Icône personnalisée (optionnel)
- ✅ Tous les assets inclus
- ✅ Optimisation de taille
- ✅ Compatible Windows 10/11

## Prérequis

### Sur Votre Machine

- ✅ Python 3.8+ installé
- ✅ pip (gestionnaire de paquets)
- ✅ Connexion internet (pour MathJax, fonts)
- ✅ ~200 Mo d'espace disque

### Dans le Projet

Aucun prérequis ! L'agent installe automatiquement :
- Flask
- Jinja2
- pytest
- PyInstaller
- Toutes les dépendances nécessaires

## Utilisation de l'Application Générée

### Développement

```bash
# Aller dans le dossier
cd app_<nom>

# Installer les dépendances (si pas fait)
pip install -r requirements.txt

# Lancer l'application
python app.py

# Ouvrir dans le navigateur
# http://localhost:5000
```

### Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Avec couverture de code
pytest tests/ --cov=app --cov-report=html

# Voir le rapport : htmlcov/index.html
```

### Build

```bash
# Construire l'exécutable
python build/build_exe.py

# L'exécutable sera dans dist/
```

### Distribution

```bash
# Copier l'exécutable
cp dist/EducationalApp.exe /chemin/destination/

# L'utilisateur double-clique pour lancer
# Aucune installation nécessaire !
```

## Exemples d'Utilisation Réels

### Cas 1 : Professeur créant des exercices interactifs

**Contexte** : Vous avez créé un fichier LaTeX avec 15 exercices sur les vecteurs pour vos secondes.

**Commande** :
```bash
/create-app ./2nde/Exercices_vecteurs.tex
```

**Résultat** :
- Application web avec les 15 exercices
- Vérification automatique des réponses
- Feedback adapté à chaque exercice
- Exécutable à distribuer aux élèves
- Les élèves peuvent s'entraîner chez eux

**Temps** : 5 minutes

---

### Cas 2 : Collègue partageant son cours

**Contexte** : Un collègue vous a envoyé un PDF de son cours sur les fonctions (40 pages).

**Commande** :
```bash
/create-app ./Cours_fonctions.pdf --name "VisualiseurFonctions"
```

**Résultat** :
- Visualiseur interactif du cours
- Navigation par sections
- Formules mathématiques bien rendues
- Recherche dans tout le cours
- Exécutable à partager avec d'autres collègues

**Temps** : 7 minutes

---

### Cas 3 : Séquence complète pour révisions

**Contexte** : Vous avez un dossier complet (cours + exos + éval) sur le produit scalaire.

**Commande** :
```bash
/create-app ./1ere_spe/Sequence-Produit_scalaire/ --type mixte
```

**Résultat** :
- Application complète de révision
- Cours consultable
- Exercices interactifs
- Évaluation avec correction automatique
- Tableau de bord de progression
- Parfait pour les révisions autonomes

**Temps** : 10 minutes

---

### Cas 4 : Quiz de révision rapide

**Contexte** : Vous voulez créer un QCM de 20 questions pour vérifier les acquis.

**Commande** :
```bash
/create-app ./QCM_revision.md --type quiz
```

**Résultat** :
- Quiz interactif avec timer
- Correction immédiate
- Score détaillé
- Statistiques par chapitre
- Les élèves peuvent le refaire plusieurs fois

**Temps** : 4 minutes

## Avantages

### Pour les Élèves

✅ **Interactif** : Plus engageant qu'un PDF
✅ **Feedback immédiat** : Savent tout de suite si c'est correct
✅ **Autonomie** : Peuvent travailler seuls à leur rythme
✅ **Motivation** : Progression visible, scores
✅ **Accessibilité** : Fonctionne sur tout ordinateur (Windows/Mac/Linux)
✅ **Hors ligne** : Pas besoin d'internet après installation

### Pour les Enseignants

✅ **Gain de temps** : Transformation automatique en 5-10 min
✅ **Réutilisation** : Vos ressources existantes deviennent interactives
✅ **Professionnalisme** : Applications au design moderne
✅ **Partage facile** : Un seul .exe à distribuer
✅ **Pas de maintenance** : Application standalone, pas de serveur
✅ **Personnalisable** : Code source accessible et modifiable

## Limitations et Notes

### Limitations Actuelles

- ⚠️ Exécutable Windows uniquement (Linux/Mac : lancer depuis sources)
- ⚠️ Formules mathématiques nécessitent internet (MathJax CDN)
- ⚠️ Pas de sauvegarde serveur (progression locale uniquement)
- ⚠️ Pas de mode multi-utilisateurs

### Solutions de Contournement

**Pour Linux/Mac** :
```bash
# Utiliser depuis les sources
python app.py
```

**Pour MathJax hors ligne** :
- Télécharger MathJax localement
- Modifier les templates pour pointer vers version locale

**Pour sauvegarde centralisée** :
- Ajouter une base de données (SQLite/PostgreSQL)
- Implémenter un système de comptes utilisateurs

## Personnalisation Post-Génération

L'application générée est **entièrement personnalisable**.

### Modifier les Couleurs

Éditer `static/css/main.css` :

```css
:root {
    --primary: #4F46E5;  /* Changer ici */
    --success: #10B981;
    --danger: #EF4444;
}
```

### Ajouter des Exercices

Éditer `data/content.json` et ajouter :

```json
{
  "id": 99,
  "title": "Nouvel exercice",
  "question": "Question ici",
  "answer": "Réponse",
  ...
}
```

### Modifier le Comportement

Éditer `static/js/main.js` pour changer la logique.

### Changer le Design

Éditer `templates/base.html` et les fichiers CSS.

## Support et Aide

### Documentation

- ✅ README.md complet dans le projet
- ✅ GUIDE_UTILISATION.md détaillé
- ✅ Code source commenté en français
- ✅ Exemples d'utilisation

### Dépannage

**L'application ne démarre pas** :
1. Vérifier que Python 3.8+ est installé
2. Réinstaller les dépendances : `pip install -r requirements.txt`
3. Vérifier que le port 5000 est libre

**Les tests échouent** :
1. Vérifier les dépendances dev : `pip install -r requirements-dev.txt`
2. Relancer : `pytest tests/ -v`

**L'exécutable ne se construit pas** :
1. Installer PyInstaller : `pip install pyinstaller`
2. Vérifier les chemins dans `build/build_exe.py`
3. Relancer : `python build/build_exe.py`

## Roadmap Futures Améliorations

Fonctionnalités prévues pour les prochaines versions :

- 🔮 Mode collaboratif (plusieurs élèves)
- 🔮 Génération de rapports enseignants
- 🔮 Intégration avec Pronote/ENT
- 🔮 Mode hors ligne complet (PWA)
- 🔮 Export des résultats (PDF, CSV)
- 🔮 Graphiques de progression avancés
- 🔮 Système de badges/récompenses
- 🔮 Mode sombre
- 🔮 Support multi-langues

## Workflow Complet - Exemple Réel

```bash
# 1. Vous avez créé un fichier LaTeX d'exercices
cd "1. Cours/2nde/Sequence-Vecteurs/"
ls
# → Exercices_vecteurs.tex (votre fichier)

# 2. Lancer la création d'application
/create-app Exercices_vecteurs.tex

# 3. L'agent pose 3 questions (30 secondes)
# → Nom : "Exercices Vecteurs 2nde" [OK]
# → Type : Exerciseur [OK]
# → Fonctionnalités : Sauvegarde progression [OK]

# 4. L'agent travaille (5 minutes)
# ✅ Analyse du fichier LaTeX
# ✅ Extraction de 12 exercices
# ✅ Génération du code Flask
# ✅ Création du frontend
# ✅ Tests automatisés (12/12 passés)
# ✅ Build de l'exécutable

# 5. Application prête !
cd app_exercices_vecteurs_2nde

# 6. Tester en local
python app.py
# → http://localhost:5000

# 7. Distribuer aux élèves
# Copier dist/EducationalApp.exe
# Les élèves double-cliquent et c'est parti !
```

## Conclusion

La commande `/create-app` vous permet de transformer **n'importe quelle ressource éducative** en **application interactive professionnelle** en quelques minutes.

**Processus** :
1. `/create-app <votre_fichier>`
2. Répondre à 3-4 questions
3. Attendre 5-10 minutes
4. Application prête !

**Résultat** :
- Application web complète
- Exécutable standalone
- Documentation complète
- Prête à distribuer

---

✨ **Prêt à créer votre première application éducative ?**

```bash
/create-app <chemin_vers_votre_ressource>
```

🚀 **C'est parti !**
