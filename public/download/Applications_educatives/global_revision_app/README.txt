APPLICATION DE RÉVISIONS
========================

Application web de révision multi-matières avec QCM et questions à réponse libre.


STRUCTURE DU PROJET
-------------------

global_revision_app/
├── data/               <- Base de données exemple
│   └── questions.json
├── dist/               <- Fichiers à distribuer aux élèves
│   ├── revision-app.html
│   └── questions.json
├── prompts/            <- Prompts pour générer des questions avec l'IA
│   └── generer-questions.md
├── src/                <- Code source (développement)
│   ├── css/
│   ├── js/
│   └── index.html
├── build.js            <- Script de build
└── README.txt          <- Ce fichier


POUR LES ÉLÈVES
---------------

Donnez-leur le contenu du dossier dist/ :
- revision-app.html (l'application)
- questions.json (la base de données)

Les deux fichiers doivent être dans le même dossier.
Ouvrir revision-app.html dans un navigateur.


POUR LE DÉVELOPPEMENT
---------------------

1. Modifier les fichiers dans src/
2. Lancer le build : node build.js
3. Tester dist/revision-app.html


FONCTIONNALITÉS
---------------

- QCM et questions à réponse libre
- Support LaTeX (MathJax) pour les maths
- Support du code avec coloration syntaxique
- Support des formules chimiques (mhchem)
- Gestion des matières (activer/désactiver/ajouter)
- Import de questions via JSON
- Export de la base de données
- Statistiques de révision (nombre d'accès)
- Mode révision intelligent (priorité aux moins révisées)
- Mode révision aléatoire


GÉNÉRER DES QUESTIONS AVEC L'IA
-------------------------------

Voir le fichier prompts/generer-questions.md pour les prompts
à utiliser avec ChatGPT, Mistral, Claude, etc.










  Structure créée :
  global_revision_app/
  ├── src-tauri/
  │   ├── Cargo.toml      # Config Rust + dépendances
  │   ├── build.rs        # Script build Tauri
  │   ├── tauri.conf.json # Config fenêtre + ressources
  │   └── src/main.rs     # Backend Rust (lecture/écriture JSON)
  ├── src/
  │   ├── js/
  │   │   ├── database.js # Adapté pour invoke() Tauri
  │   │   └── app.js      # Simplifié (plus d'écran connexion)
  │   └── css/main.css
  ├── dist/
  │   ├── index.html      # Frontend monolithique compilé
  │   └── questions.json  # Base de données
  ├── data/questions.json
  └── build.js            # Script de build mis à jour

  Une fois Rust installé, tu pourras :

  1. Tester en dev :
  cd Applications_educatives/global_revision_app/src-tauri
  cargo tauri dev

  2. Créer l'exécutable final :
  cargo tauri build

  L'exécutable (~3-5 MB) sera dans src-tauri/target/release/ et le JSON sera lu/écrit directement à côté de l'exe, sans aucune permission à demander.

  Dis-moi quand Rust est installé pour qu'on teste.

✻ Baked for 11m 17s