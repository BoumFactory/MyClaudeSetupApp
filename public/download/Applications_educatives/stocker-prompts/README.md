# Prompt Manager - Gestionnaire de Prompts pour Élèves

Application pour stocker, organiser et créer des prompts IA de manière simple et ergonomique.

## Fonctionnalités

### 1. Stockage de Prompts
- **Arbre décisionnel** : Catégorisation guidée (Action → Matière → Niveau → Thème)
- **26 actions disponibles** : Créer, Réviser, Expliquer, Corriger, Résumer, Comparer... + 20 actions supplémentaires configurables
- **Filtres et recherche** : Retrouver facilement un prompt
- **Export/Import** : Sauvegarder et partager ses prompts

### 2. Fabricateur de Prompts
- **Structures prédéfinies** : 8 templates pour les cas d'usage courants (révision, exercices, correction...)
- **Briques modulaires** : 16 briques combinables (contexte, demande, format, contrainte)
- **Paramétrage** : Remplir les variables (niveau, matière, thème...)
- **Aperçu en direct** : Voir le prompt se construire

### 3. Générateur de Concaténation
- **Prompt pré-écrit** : À coller dans une conversation IA pour obtenir un résumé
- **3 variantes** : Standard, Court, Structuré
- **Instructions claires** : Guide pas à pas pour les élèves

## Installation

### Pour les élèves (version simple)

1. Télécharger le fichier `dist/prompt-manager.html`
2. L'ouvrir dans un navigateur (Chrome, Firefox, Edge...)
3. C'est prêt !

Les données sont stockées automatiquement dans le navigateur (localStorage).

### Application Desktop (Tauri)

```bash
# Se placer dans le dossier
cd "C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\Applications_educatives\stocker-prompts"

# Installer les dépendances
pnpm install

# Lancer en mode développement (hot reload)
pnpm run tauri:dev

# Construire l'exécutable (.exe)
pnpm run tauri:build
```

L'exécutable sera généré dans `src-tauri/target/release/`.
Le fichier `mes-prompts.json` sera créé à côté de l'exécutable.

### Pour le développement web

```bash
# Installer les dépendances (optionnel, pour le mode développement)
pnpm install

# Lancer en mode développement
pnpm run dev

# Construire la version production
pnpm run build

# Reconstruire automatiquement lors des modifications
pnpm run watch
```

## Structure du projet

```
stocker-prompts/
├── src/                          # Code source modulaire
│   ├── config/                   # Configuration
│   │   ├── actions.js            # Actions disponibles (26)
│   │   ├── subjects.js           # Matières et niveaux
│   │   ├── bricks.js             # Briques du fabricateur
│   │   ├── structures.js         # Structures prédéfinies
│   │   └── concatenation-prompt.js  # Prompts de résumé
│   ├── core/                     # Logique métier
│   │   ├── database.js           # Gestion stockage (Tauri/localStorage)
│   │   └── prompt-builder.js     # Construction de prompts
│   ├── ui/                       # Interface utilisateur
│   │   ├── components/           # Composants
│   │   │   ├── wizard.js         # Arbre décisionnel
│   │   │   ├── prompt-list.js    # Liste des prompts
│   │   │   ├── builder-panel.js  # Fabricateur
│   │   │   ├── concatenation-panel.js  # Résumeur
│   │   │   ├── settings-panel.js # Paramètres
│   │   │   └── save-modal.js     # Modal de sauvegarde
│   │   └── styles/
│   │       └── main.css          # Styles
│   ├── app.js                    # Application principale
│   └── index.html                # Point d'entrée dev
├── src-tauri/                    # Backend Tauri (Rust)
│   ├── src/main.rs               # Commandes IPC (load/save database)
│   ├── Cargo.toml                # Dépendances Rust
│   ├── tauri.conf.json           # Configuration Tauri
│   └── icons/                    # Icônes de l'application
├── dist/                         # Version production
│   ├── prompt-manager.html       # Fichier unique (web)
│   └── index.html                # Point d'entrée Tauri
├── data/                         # Données (mode dev)
│   └── mes-prompts.json          # Base de données
├── build.js                      # Script de build
├── package.json                  # Configuration npm
└── README.md                     # Ce fichier
```

## Personnalisation

### Ajouter des actions

Modifier `src/config/actions.js` et ajouter dans le tableau `ACTIONS` :

```javascript
{
  id: 'mon_action',
  label: 'Mon Action',
  emoji: '🎯',
  description: 'Description de l\'action',
  enabled: true,  // true = visible par défaut
  category: 'production'  // production, apprentissage, comprehension...
}
```

### Ajouter des briques

Modifier `src/config/bricks.js` et ajouter dans le tableau `DEFAULT_BRICKS` :

```javascript
{
  id: 'ma_brique',
  category: 'demande',  // contexte, demande, format, contrainte
  label: 'Ma brique',
  template: 'Je veux {parametre} pour {autre_parametre}.',
  params: ['parametre', 'autre_parametre'],
  enabled: true
}
```

### Ajouter des structures

Modifier `src/config/structures.js` et ajouter dans le tableau `DEFAULT_STRUCTURES` :

```javascript
{
  id: 'ma_structure',
  label: 'Ma Structure',
  description: 'Description',
  bricks: ['context_eleve', 'demande_explication', 'format_simple'],
  icon: '📚',
  enabled: true
}
```

## Export des données

Les élèves peuvent exporter leurs prompts via les paramètres pour :
- Sauvegarder sur une clé USB
- Partager avec d'autres élèves
- Changer de navigateur/ordinateur

Le fichier exporté est un JSON qui peut être réimporté.

## Thème sombre

L'application supporte un thème sombre configurable dans les paramètres.

## Compatibilité

- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

L'application fonctionne hors ligne une fois chargée.
