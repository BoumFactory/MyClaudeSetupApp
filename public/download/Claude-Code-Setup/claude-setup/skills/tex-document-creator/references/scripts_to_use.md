# Guide d'utilisation des scripts tex-document-creator

## Localisation des scripts

Tous les scripts sont situés dans : `.claude/skills/tex-document-creator/scripts/`

## Scripts disponibles

### 1. create_document.py

**SCRIPT PRINCIPAL** - Création automatique de documents LaTeX à partir de templates.

**Usage (recommandé, `--fields-file`) :**
```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "CHEMIN_ABSOLU_DESTINATION" \
  --name "Nom_Document" \
  --template "Nom_Template" \
  --fields-file "CHEMIN_ABSOLU_VERS_fields.json" \
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
- `--fields-file` : Chemin vers un fichier JSON (écrit avec l'outil **Write**, jamais via
  heredoc ni `python -c` en Bash) contenant les valeurs des champs du template. Seule
  méthode fiable pour les valeurs LaTeX à antislashes (`$\mathbf{2^{\text{nde}}}$..) :
  Git Bash altère les antislashs passés en argument de ligne de commande, provoquant des
  erreurs `Invalid escape` ou des champs mal remplis avec `--field`/`--fields`.

**Arguments optionnels :**
- `--field "nom=valeur"` : Définit un champ isolé (peut être répété), combinable en
  surcouche avec `--fields-file`. À réserver aux valeurs sans antislash.
- `--fields '{"json":"..."}'` : LEGACY, déconseillé (mêmes problèmes d'échappement que `--field`)
- `--create-sections` : Crée un dossier sections/
- `--create-images` : Crée un dossier images/
- `--create-annexes` : Crée un dossier annexes/
- `--no-folder` : Ne crée pas de dossier projet (crée directement les fichiers)
- `--no-figures` : Ne crée pas le fichier enonce_figures.tex
- `--claude-instructions` : Ajoute un fichier CLAUDE.md avec instructions

**Exemple :**
```
# 1. Ecrire (outil Write) fields.json :
{
  "niveau": "$\\mathbf{1^{\\text{ère}}}$",
  "theme": "Produit scalaire dans le plan",
  "type_etablissement": "Lycée",
  "nom_etablissement": "Lycée Exemple"
}
```
```bash
# 2. Créer le document
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "<dossier du projet>/1ere_spe/Sequence-Produit_scalaire" \
  --name "Cours_Produit_scalaire" \
  --template "Cours" \
  --fields-file "C:/chemin/vers/fields.json" \
  --create-sections
```

**En cas d'échec (`missing_fields`)** : aucun fichier n'est créé. Compléter le
`example_fields_file` renvoyé dans l'erreur (déjà au format fields-file) et relancer —
ne jamais écrire le document ou le fichier maître à la main à la place du script.

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

**Retourne (fonction de détection PARTAGÉE avec create_document.py — mêmes champs, même
définition du « requis »)** :
- Chaque champ avec `"required": true/false` (aucune valeur par défaut exploitable ⇒ requis)
- `"required_fields"` : liste des noms de champs obligatoires
- `"example_fields_file"` : dictionnaire prêt à copier tel quel dans un fichier JSON
  (`--fields-file`), valeurs par défaut déjà renseignées quand elles existent
- Description de chaque champ, options pour les champs à choix, préférences utilisateur

**Exemple :**
```bash
python .claude/skills/tex-document-creator/scripts/get_template_info.py --template "Cours"
```

**Workflow associé** : copier `example_fields_file`, compléter les `<A_COMPLETER:...>`,
écrire le résultat avec l'outil Write, puis passer ce fichier à `create_document.py
--fields-file`.

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
  --value "Lycée Exemple"
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

3. **Écrire le fields-file avec l'outil Write** (à partir de `example_fields_file`) :
   ```
   {"niveau": "...", "theme": "...", ...}
   ```

4. **Créer le document :**
   ```bash
   python .claude/skills/tex-document-creator/scripts/create_document.py \
     --destination "chemin/destination" \
     --name "Mon_Document" \
     --template "Cours" \
     --fields-file "chemin/vers/fields.json" \
     --create-sections
   ```

## Règles d'utilisation

1. **TOUJOURS** utiliser ces scripts via Bash, jamais créer manuellement avec Write
   (le fields-file JSON, lui, s'écrit avec Write — mais pas le document ni le maître)
2. **TOUJOURS** vérifier que le template existe avec `list_templates.py` avant de créer
3. **TOUJOURS** obtenir les champs requis avec `get_template_info.py` avant de remplir,
   et réutiliser son `example_fields_file`
4. **TOUJOURS** utiliser des chemins absolus pour `--destination`
5. **TOUJOURS** passer par `--fields-file` pour les valeurs LaTeX à antislashes (jamais
   `--field`/`--fields` en ligne de commande pour ces valeurs : Git Bash les altère)
6. **En cas d'échec** (`missing_fields`) : compléter le `example_fields_file` renvoyé et
   relancer le script — ne jamais écrire le document ou le fichier maître à la main
