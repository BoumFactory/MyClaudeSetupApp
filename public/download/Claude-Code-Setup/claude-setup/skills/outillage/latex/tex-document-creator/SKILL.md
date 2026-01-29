---
name: tex-document-creator
description: Skill pour l'initialisation de nouveaux projets LaTeX à partir de modèles. Gère la création de structure de dossiers, le remplissage de templates et la configuration initiale de documents LaTeX éducatifs. Utiliser de manière proactive lors de la création de nouveaux documents.
---

# LaTeX Document Creator

Système expert pour l'initialisation automatique de projets LaTeX basés sur des modèles configurables. Ce skill gère la création de la structure de projet, le remplissage intelligent de templates et la configuration initiale.

## Objectif

Créer rapidement des projets LaTeX structurés avec des modèles prédéfinis, en automatisant la génération de fichiers, dossiers et configuration initiale.

## ⚠️ RÈGLE CRITIQUE

**NE JAMAIS créer manuellement des fichiers ou dossiers LaTeX.**

**TOUJOURS utiliser les scripts Python via Bash**.

### 📖 Guide complet des scripts

**LIRE IMPÉRATIVEMENT** le guide de référence des scripts :
`.claude/skills/tex-document-creator/references/scripts_to_use.md`

Ce guide contient :
- ✅ Description détaillée de tous les scripts disponibles
- ✅ Syntaxe complète et arguments de chaque script
- ✅ Exemples d'utilisation pour chaque cas
- ✅ Workflow recommandé
- ✅ Règles d'utilisation critiques

Scripts principaux :
- `create_document.py` : Création automatique de documents
- `get_template_info.py` : Informations sur les templates
- `list_templates.py` : Liste des templates disponibles

Ces scripts :
- ✅ Créent automatiquement tous les fichiers et dossiers nécessaires
- ✅ Remplissent les templates avec les bonnes valeurs
- ✅ Génèrent une structure cohérente
- ✅ Fournissent un rapport détaillé de création

Si tu crées des fichiers manuellement avec Write, tu ignores le système de templates et tu risques des incohérences.

## Workflow Principal : Créer un Nouveau Projet

**Quand utiliser** : Lorsque l'utilisateur demande un nouveau document (cours, évaluation, exercices, etc.)

**Étapes :**

1. **Analyser la demande** pour extraire :
   - **Type de document** (obligatoire) : Cours, Devoir, Devoir_maison, Exercices heavy, Exercices light, Découverte, Plan sequence, Recap_seance, AP, Groupe, Info, Jeux, Rapport incident, SOUAP, Nouveau
   - **Niveau** (optionnel selon contexte) : 6eme, 5eme, 4eme, 3eme, 2nde, 1ere_spe, Terminale
   - **Thème** (optionnel) : Le sujet (vecteurs, fonctions, probabilités, etc.)

2. **Vérifier la structure des répertoires** avec Glob ou LS :
   - Vérifier si le répertoire de destination existe
   - Identifier si un dossier de séquence/thème existe déjà
   - Déterminer le chemin de destination approprié

3. **Consulter les modèles disponibles** :
   ```
   list_templates()  # Voir les modèles disponibles
   get_template_info(template_name)  # Connaître les champs du template
   ```

4. **Remplir intelligemment les champs du template** :
   Adapter les valeurs selon le type de document et les informations fournies

5. **Créer le document via le script Python** :

   **IMPORTANT** : Utiliser UNIQUEMENT le script Python via Bash, PAS de création manuelle de fichiers.

   **Syntaxe recommandée (nouveau format --field)** :
   ```bash
   python .claude/skills/tex-document-creator/scripts/create_document.py \
     --destination "CHEMIN_ABSOLU_DESTINATION" \
     --name "Nom_Document" \
     --template "Nom_Template" \
     --field "champ1=valeur1" \
     --field "champ2=valeur2" \
     [--create-sections] \
     [--create-images] \
     [--create-annexes] \
     [--no-folder] \
     [--no-figures] \
     [--claude-instructions]
   ```

   **Syntaxe legacy (format JSON, déprécié)** :
   ```bash
   python .claude/skills/tex-document-creator/scripts/create_document.py \
     --destination "CHEMIN_ABSOLU_DESTINATION" \
     --name "Nom_Document" \
     --template "Nom_Template" \
     --fields '{"niveau": "...", "theme": "...", ...}' \
     [options...]
   ```

   **Exemples recommandés** :

```bash
# Créer un cours sur les vecteurs en 2nde
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/chemin/vers/projet/1. Cours/2nde/Sequence-Vecteurs" \
  --name "Cours_Vecteurs" \
  --template "Cours" \
  --field "niveau=$\\mathbf{2^{\\text{nde}}}$" \
  --field "theme=Vecteurs du plan" \
  --field "type_etablissement=Lycée" \
  --field "nom_etablissement=Camille Claudel" \
  --field "type_document_principal=Cours :" \
  --field "contenu_principal=\\input{enonce}," \
  --create-sections

# Créer un devoir sur les fonctions en 1ère
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/chemin/vers/projet/2. Evaluations/1ere_spe" \
  --name "DS_Fonctions" \
  --template "Devoir" \
  --field "niveau=$\\mathbf{1^{\\text{ère}}}$" \
  --field "theme=Fonctions" \
  --field "duree=55" \
  --field "type_etablissement=Lycée" \
  --field "nom_etablissement=Camille Claudel"
```

   **Options** :

   - `--destination` : OBLIGATOIRE - Chemin absolu de destination
   - `--name` : OBLIGATOIRE - Nom du document (sans .tex)
   - `--template` : OBLIGATOIRE - Nom du template (Cours, Devoir, etc.)
   - `--field "nom=valeur"` : RECOMMANDÉ - Définit un champ (peut être répété). Format: `nom=valeur`. Les valeurs LaTeX avec backslashes sont gérées automatiquement.
   - `--fields '{"json":"..."}'` : LEGACY - JSON des champs à remplir (déprécié, utiliser --field à la place)
   - `--create-sections` : Crée le dossier sections/ (recommandé pour Cours)
   - `--create-images` : Crée le dossier images/
   - `--create-annexes` : Crée le dossier annexes/
   - `--no-folder` : Ne crée PAS de dossier projet (rare)
   - `--no-figures` : Ne crée PAS enonce_figures.tex (rare)
   - `--claude-instructions` : Ajoute un fichier CLAUDE.md

   **⚠️ NOTE IMPORTANTE** : Le nouveau format `--field` est **fortement recommandé** car il évite tous les problèmes d'échappement des caractères spéciaux LaTeX (backslashes, accolades, etc.). Le format JSON `--fields` est conservé pour compatibilité mais peut causer des erreurs avec les caractères LaTeX complexes.

6. **Post-traitement** (optionnel) :
   - Créer des fichiers auxiliaires supplémentaires
   - Initialiser un dépôt git si demandé

7. **Fournir un rapport détaillé** avec résumé de création, emplacement et prochaines étapes

## Exemples d'Utilisation

### Exemple 1 : Créer une nouvelle évaluation

```
Utilisateur : "Une évaluation sur les vecteurs en seconde, 55 minutes"

1. Analyser : type=Devoir, niveau=2nde, theme=vecteurs, duree=55
2. Vérifier répertoire de destination
3. Obtenir template info pour "Devoir"
4. Remplir les champs automatiquement
5. Exécuter le script Python :

python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/1. Cours/2nde/Sequence-Vecteurs" \
  --name "DS_Vecteurs" \
  --template "Devoir" \
  --fields '{"niveau": "$\\mathbf{2^{\\text{nde}}}$", "theme": "Vecteurs", "type_etablissement": "Lycée", "nom_etablissement": "Eugène Belgrand", "duree": "55", "type_document_principal": "Devoir :"}'

6. Rapporter succès
```

### Exemple 2 : Créer un cours avec sections

```
Utilisateur : "Nouveau cours sur les fonctions pour la première"

1. Analyser : type=Cours, niveau=1ere_spe, theme=fonctions
2. Obtenir template "Cours"
3. Exécuter le script Python avec --create-sections :

python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/1. Cours/1ere_spe/Sequence-Fonctions" \
  --name "Cours_Fonctions" \
  --template "Cours" \
  --fields '{"niveau": "$\\mathbf{1^{\\text{ère}}}$", "theme": "Fonctions de référence", "type_etablissement": "Lycée", "nom_etablissement": "Amadis Jamyn", "supplement": "", "type_document_principal": "Cours :", "contenu_principal": "\\input{enonce},"}' \
  --create-sections

4. Rapporter avec chemins et prochaines étapes
```

### Exemple 3 : Commande complète pour un cours (Produit scalaire)

```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/1. Cours/1ere_spe/Sequence-Produit_scalaire" \
  --name "Cours_Produit_scalaire" \
  --template "Cours" \
  --fields '{"niveau": "$\\mathbf{1^{\\text{ère}}}$", "theme": "Produit scalaire dans le plan", "type_etablissement": "Lycée", "nom_etablissement": "Eugène Belgrand", "supplement": "", "type_document_principal": "Cours :", "contenu_principal": "\\input{enonce},"}' \
  --create-sections
```

## Bonnes Pratiques : Fichier CLAUDE.md

**RÈGLE IMPORTANTE** : Toujours créer un fichier CLAUDE.md dans chaque projet LaTeX.

### Pourquoi créer CLAUDE.md ?

Le fichier `CLAUDE.md` sert de **mémoire de projet** pour les agents qui travailleront sur le document. Il permet :
- De savoir quel modèle a été utilisé
- De connaître les paramètres du document (niveau, thème, type)
- De comprendre la structure du projet
- D'avoir les instructions de compilation
- De tracker l'état d'avancement du projet

### Comment créer CLAUDE.md ?

**Lors de la création du projet** : Utiliser l'option `--claude-instructions`

```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "chemin/vers/projet" \
  --name "Mon_Document" \
  --template "Cours" \
  --field "niveau=..." \
  --field "theme=..." \
  --claude-instructions  # ← Cette option crée le fichier CLAUDE.md
```

### Contenu type de CLAUDE.md

Le script génère automatiquement un fichier avec :
- Modèle utilisé et date de création
- Paramètres du document (tous les champs remplis)
- Structure du projet (fichiers générés)
- Instructions de compilation

### Mise à jour de CLAUDE.md

**IMPORTANT** : Les agents qui modifient le projet doivent mettre à jour CLAUDE.md pour refléter :
- Les modifications apportées
- L'état de compilation actuel
- Les problèmes rencontrés et résolus
- Les étapes suivantes suggérées

Voir aussi : **`tex-compiling-skill`** qui contient les bonnes pratiques pour maintenir CLAUDE.md à jour après compilation.

## Rappels Critiques

- TOUJOURS vérifier que le modèle existe avant de créer
- TOUJOURS fournir tous les champs requis par le template
- TOUJOURS utiliser des chemins absolus
- TOUJOURS créer un fichier CLAUDE.md avec `--claude-instructions`
- NE JAMAIS écraser un document existant sans confirmation
