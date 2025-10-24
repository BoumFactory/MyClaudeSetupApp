# Guide MCP Document Creator - Workflow Guidé

## 🎯 Objectif

Ce serveur MCP permet à l'agent `latex-bfcours-writer` de créer automatiquement des documents LaTeX structurés via un **workflow guidé en dialogue**. Fini la création manuelle !

## 🚀 Installation

Exécute le fichier `setup_document_creator_mcp.bat` :
```bash
setup_document_creator_mcp.bat
```

## 🔄 Workflow en Dialogue

### Mode 1 : Création Guidée (Recommandé)

L'agent suit un dialogue pas-à-pas :

#### Étape 1 : Démarrage
```
Utilise start_document_creation pour commencer
```

**Réponse du serveur :**
- Liste des modèles disponibles
- Instructions pour la suite

#### Étape 2 : Sélection du modèle
```
Utilise select_template avec template_name="Cours"
```

**Réponse du serveur :**
- Champs paramétrables du modèle
- Types de champs et options disponibles

#### Étape 3 : Remplissage des champs
```
Utilise fill_template_fields avec field_values={
  "niveau": "$\\mathbf{5^{\\text{ème}}}$",
  "theme": "Équations",
  "type_etablissement": "Collège",
  "nom_etablissement": "Gaston Bachelard"
}
```

**Réponse du serveur :**
- Structure du workspace analysée
- Options de destination disponibles

#### Étape 4 : Configuration finale
```
Utilise configure_destination avec :
- destination_path="C:/Users/Utilisateur/Documents/.../5eme/Equations"
- document_name="Cours_Equations_Intro"
- create_images_folder=false
- create_figures_file=true
- include_claude_instructions=true
```

**Résultat :**
- Document créé avec structure complète
- Fichiers générés automatiquement
- Prêt pour édition du contenu

### Mode 2 : Création Rapide

Pour les agents expérimentés :

```
Utilise quick_create_document avec tous les paramètres d'un coup :
- destination_path="C:/chemin/vers/destination"
- document_name="Mon_Document"
- template_name="Exercices heavy"
- field_values={"niveau": "...", "theme": "..."}
- create_images_folder=true
- include_claude_instructions=true
```

## 🛠️ Outils Disponibles

### Outils de Workflow
1. **`start_document_creation`** - Démarre le processus guidé
2. **`select_template`** - Sélectionne un modèle
3. **`fill_template_fields`** - Remplit les champs paramétrables
4. **`configure_destination`** - Configure destination et options

### Outils Rapides
5. **`quick_create_document`** - Création en une commande

### Outils d'Information
6. **`list_available_templates`** - Liste tous les modèles
7. **`get_template_info`** - Détails d'un modèle spécifique
8. **`get_workspace_info`** - Structure du workspace

## 📝 Modèles Disponibles

Les modèles sont dans `datas/latex-modeles/` :
- **Cours.tex** - Document de cours
- **Exercices heavy.tex** - Exercices avec corrections
- **Exercices light.tex** - Exercices simples
- **Devoir.tex** - Évaluations
- **Devoir_maison.tex** - Devoirs à la maison
- **AP.tex** - Accompagnement personnalisé
- **Découverte.tex** - Activités de découverte
- **Info.tex** - Documents informatique
- **Jeux.tex** - Activités ludiques
- **SOUAP.tex** - Documents spécialisés

## 🔧 Champs Paramétrables

Les modèles contiennent des champs au format :
```latex
% niveau : $\mathbf{6^{\text{ème}}}$,$\mathbf{5^{\text{ème}}}$,...
% theme : ,Equations
% type_etablissement : Collège,Lycée
% nom_etablissement : Gaston Bachelard,Amadis Jamyn
% date_rendu : commande(get_current_date())
```

Le serveur :
- **Détecte automatiquement** les champs
- **Propose les options** disponibles
- **Remplace les valeurs** dans le modèle généré

## 📁 Structure Générée

Pour chaque document créé :

```
Mon_Document/
├── Mon_Document.tex          # Fichier principal (modèle adapté)
├── enonce.tex               # Contenu à remplir par l'agent
├── enonce_figures.tex       # Figures TikZ (optionnel)
├── CLAUDE.md               # Instructions agent (optionnel)
├── images/                 # Dossier images (optionnel)
├── annexes/               # Dossier annexes (optionnel)
└── sections/              # Sections multiples (optionnel)
```

## 🤖 Exemples d'Usage pour l'Agent

### Création de cours
```
Je veux créer un cours sur les équations pour les 4èmes.

1. start_document_creation
2. select_template template_name="Cours"  
3. fill_template_fields avec niveau="4ème", theme="Équations"
4. configure_destination avec le bon chemin et les options
```

### Création d'exercices
```
Crée des exercices lourds sur Pythagore pour les 3èmes.

Utilise quick_create_document directement avec tous les paramètres.
```

### Exploration des modèles
```
Quels modèles sont disponibles pour créer une évaluation ?

Utilise list_available_templates puis get_template_info pour "Devoir"
```

## ⚡ Avantages pour l'Agent

- **Autonomie totale** : Crée des documents sans intervention humaine
- **Structure cohérente** : Tous les documents suivent les mêmes conventions
- **Paramétrage intelligent** : Adaptation automatique aux besoins
- **Workflow guidé** : Processus étape par étape sécurisé
- **Mode rapide** : Pour les cas d'usage répétitifs

## 🎯 Workflow Typique

1. **Agent reçoit** une demande de création de document
2. **Démarre le workflow** avec `start_document_creation`  
3. **Sélectionne** le modèle approprié selon le type demandé
4. **Analyse** les champs paramétrables
5. **Remplit** les champs selon le contexte (niveau, thème, etc.)
6. **Configure** la destination dans l'arborescence
7. **Crée** automatiquement la structure complète
8. **Édite** le contenu dans les fichiers générés

## 🔍 Test Rapide

```
Utilise list_available_templates pour voir tous les modèles disponibles
```

L'agent `latex-bfcours-writer` devient maintenant **complètement autonome** pour créer des documents ! 🚀