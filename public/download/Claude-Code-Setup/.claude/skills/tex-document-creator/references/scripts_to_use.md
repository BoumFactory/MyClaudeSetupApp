# Guide d'utilisation des scripts tex-document-creator

## Localisation des scripts

Tous les scripts sont situés dans : `.claude/skills/tex-document-creator/scripts/`

## Scripts disponibles

### 1. create_document.py

**SCRIPT PRINCIPAL** - Création automatique de documents LaTeX à partir de templates.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "CHEMIN_ABSOLU_DESTINATION" \
  --name "Nom_Document" \
  --template "Nom_Template" \
  --fields '{"niveau": "...", "theme": "...", ...}' \
  [--create-sections] \
  [--create-images] \
  [--create-annexes] \
  [--no-folder] \
  [--no-figures] \
  [--claude-instructions]
```

**Arguments obligatoires :**
- `--destination` : Chemin absolu où créer le document
- `--name` : Nom du document (sans extension .tex)
- `--template` : Nom du template à utiliser
- `--fields` : JSON contenant les valeurs des champs du template

**Arguments optionnels :**
- `--create-sections` : Crée un dossier sections/
- `--create-images` : Crée un dossier images/
- `--create-annexes` : Crée un dossier annexes/
- `--no-folder` : Ne crée pas de dossier projet (crée directement les fichiers)
- `--no-figures` : Ne crée pas le fichier enonce_figures.tex
- `--claude-instructions` : Ajoute un fichier CLAUDE.md avec instructions

**Exemple :**
```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/1. Cours/1ere_spe/Sequence-Produit_scalaire" \
  --name "Cours_Produit_scalaire" \
  --template "Cours" \
  --fields '{"niveau": "$\\mathbf{1^{\\text{ère}}}$", "theme": "Produit scalaire dans le plan", "type_etablissement": "Lycée", "nom_etablissement": "Eugène Belgrand"}' \
  --create-sections
```

### 2. list_templates.py

Liste tous les templates disponibles.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/list_templates.py
```

**Retourne :**
- Liste des noms de templates disponibles
- Chemins des fichiers template

### 3. get_template_info.py

Obtient les informations détaillées sur un template spécifique.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/get_template_info.py --template "Nom_Template"
```

**Arguments :**
- `--template` : Nom du template à examiner

**Retourne :**
- Liste des champs requis
- Description de chaque champ
- Valeurs par défaut éventuelles
- Structure du template

**Exemple :**
```bash
python .claude/skills/tex-document-creator/scripts/get_template_info.py --template "Cours"
```

### 4. get_user_preferences.py

Affiche les préférences utilisateur enregistrées.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/get_user_preferences.py
```

**Retourne :**
- Préférences globales (établissement, niveau par défaut, etc.)
- Habitudes de création
- Configurations personnalisées

### 5. update_user_preferences.py

Met à jour les préférences utilisateur.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/update_user_preferences.py \
  --preference "nom_preference" \
  --value "valeur"
```

**Arguments :**
- `--preference` : Nom de la préférence à modifier
- `--value` : Nouvelle valeur

**Exemple :**
```bash
python .claude/skills/tex-document-creator/scripts/update_user_preferences.py \
  --preference "nom_etablissement" \
  --value "Lycée Eugène Belgrand"
```

### 6. add_user_habit.py

Enregistre une habitude de création pour automatiser les futurs documents.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/add_user_habit.py \
  --template "Nom_Template" \
  --habits '{"champ1": "valeur1", "champ2": "valeur2"}'
```

**Arguments :**
- `--template` : Template concerné
- `--habits` : JSON des valeurs à mémoriser

**Exemple :**
```bash
python .claude/skills/tex-document-creator/scripts/add_user_habit.py \
  --template "Devoir" \
  --habits '{"type_etablissement": "Lycée", "duree": "55"}'
```

### 7. remove_user_habit.py

Supprime une habitude enregistrée.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/remove_user_habit.py \
  --template "Nom_Template" \
  --habit "nom_champ"
```

**Arguments :**
- `--template` : Template concerné
- `--habit` : Nom du champ à supprimer des habitudes

### 8. get_help.py

Affiche l'aide générale du système de création de documents.

**Usage :**
```bash
python .claude/skills/tex-document-creator/scripts/get_help.py
```

## Workflow typique

1. **Lister les templates disponibles :**
   ```bash
   python .claude/skills/tex-document-creator/scripts/list_templates.py
   ```

2. **Obtenir les champs requis pour un template :**
   ```bash
   python .claude/skills/tex-document-creator/scripts/get_template_info.py --template "Cours"
   ```

3. **Créer le document :**
   ```bash
   python .claude/skills/tex-document-creator/scripts/create_document.py \
     --destination "chemin/destination" \
     --name "Mon_Document" \
     --template "Cours" \
     --fields '{"niveau": "...", "theme": "..."}' \
     --create-sections
   ```

## Règles d'utilisation

1. **TOUJOURS** utiliser ces scripts via Bash, jamais créer manuellement avec Write
2. **TOUJOURS** vérifier que le template existe avec `list_templates.py` avant de créer
3. **TOUJOURS** obtenir les champs requis avec `get_template_info.py` avant de remplir
4. **TOUJOURS** utiliser des chemins absolus pour `--destination`
5. **TOUJOURS** corriger l'encodage après création avec `encoding-fixer-server`
