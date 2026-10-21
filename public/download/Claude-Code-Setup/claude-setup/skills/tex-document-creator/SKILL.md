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
   ```bash
   python .claude/skills/tex-document-creator/scripts/list_templates.py
   python .claude/skills/tex-document-creator/scripts/get_template_info.py --template "Nom_Template"
   ```

   `get_template_info` renvoie, pour CHAQUE champ, son caractère `"required": true/false`,
   une liste `"required_fields"` (les champs sans défaut exploitable — `create_document`
   échouera s'ils manquent), et surtout un `"example_fields_file"` : un dictionnaire déjà
   prêt à copier tel quel dans un fichier JSON.

4. **Construire le fields-file** :
   Copier `example_fields_file` renvoyé par `get_template_info`, compléter les valeurs
   `<A_COMPLETER:...>` selon le contexte (niveau, thème, établissement...), puis **écrire
   ce JSON avec l'outil Write** dans un fichier (ex. `fields.json` à côté du document, ou
   dans le scratchpad).

5. **Créer le document via le script Python** :

   **IMPORTANT** : Utiliser UNIQUEMENT le script Python via Bash, PAS de création manuelle de fichiers.

   **⚠️ RÈGLE ABSOLUE — jamais de valeurs LaTeX avec antislash en argument Bash** : les
   valeurs comme `$\mathbf{2^{\text{nde}}}$` contiennent des doubles antislashs
   (`\\mathbf`, `\\text`) qui sont altérés par Git Bash lors du passage en argument de
   ligne de commande (`--field`/`--fields`), provoquant des erreurs `Invalid escape` ou
   des champs mal remplis. **Toujours passer par `--fields-file`** : écrire le JSON avec
   l'outil **Write** (jamais via heredoc ni `python -c` en Bash), puis fournir son chemin.

   **Syntaxe recommandée (`--fields-file`)** :
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

   **Exemples recommandés** :

```
# 1. Ecrire (outil Write) fields.json avec le contenu suivant :
{
  "niveau": "$\\mathbf{2^{\\text{nde}}}$",
  "theme": "Vecteurs du plan",
  "type_etablissement": "Lycée",
  "nom_etablissement": "Lycée Exemple",
  "type_document_principal": "Cours :",
  "contenu_principal": "\\input{enonce},"
}
```

```bash
# 2. Créer le cours en pointant sur ce fichier
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "C:/chemin/vers/projet/1. Cours/2nde/Sequence-Vecteurs" \
  --name "Cours_Vecteurs" \
  --template "Cours" \
  --fields-file "C:/chemin/vers/projet/1. Cours/2nde/Sequence-Vecteurs/fields.json" \
  --create-sections
```

   **Options** :

   - `--destination` : OBLIGATOIRE - Chemin absolu de destination. Un chemin relatif n'est pas résolu depuis la racine du projet mais depuis « 1. Cours » (`WORKSPACE_PATH` de `.claude/mcp_servers/mcp.json`) : `.claude/tmp` créerait `1. Cours/.claude/tmp`.
   - `--name` : OBLIGATOIRE - Nom du document (sans .tex)
   - `--template` : OBLIGATOIRE - Nom du template (Cours, Devoir, etc.)
   - `--fields-file "chemin.json"` : **RECOMMANDÉ** - Fichier JSON (écrit avec Write) des valeurs de champs. Seule méthode fiable pour les valeurs LaTeX avec antislashes.
   - `--field "nom=valeur"` : Définit UN champ isolé (peut être répété, se combine avec `--fields-file` en surcouche). À réserver aux valeurs sans antislash (ex. `theme=Vecteurs`, `duree=55`).
   - `--fields '{"json":"..."}'` : LEGACY - JSON en ligne de commande, déconseillé (même problème d'échappement que `--field`)
   - `--create-sections` : Crée le dossier sections/ (recommandé pour Cours)
   - `--create-images` : Crée le dossier images/
   - `--create-annexes` : Crée le dossier annexes/
   - `--no-folder` : Ne crée PAS de dossier projet (rare)
   - `--no-figures` : Ne crée PAS enonce_figures.tex (rare)
   - `--claude-instructions` : Ajoute un fichier CLAUDE.md

### ⚠️ En cas d'échec : champs manquants

Si `create_document.py` échoue avec `"missing_fields"`, **aucun fichier n'a été créé**
(le script vérifie tous les champs requis AVANT toute écriture sur le disque). La sortie
contient déjà un `"example_fields_file"` complet, prêt à corriger.

**Procédure obligatoire** :
1. Reprendre le JSON `example_fields_file` affiché dans l'erreur.
2. Compléter les valeurs `<A_COMPLETER:...>` restantes.
3. Réécrire le fields-file avec l'outil **Write**.
4. Relancer `create_document.py --fields-file <chemin>`.

**NE JAMAIS**, en cas d'échec, écrire à la main le document ou le fichier maître à la
place du script : cela contourne le remplissage des templates, désynchronise la
structure attendue, et c'est précisément la cause des documents mal formés que ce skill
doit éviter. Toujours corriger les champs et relancer le script.

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
3. Obtenir template info pour "Devoir" (récupère required_fields + example_fields_file)
4. Écrire (outil Write) le fields-file en complétant l'exemple renvoyé, ex. fields.json :
   {
     "niveau": "$\\mathbf{2^{\\text{nde}}}$", "theme": "Vecteurs",
     "type_etablissement": "Lycée", "nom_etablissement": "Lycée Exemple",
     "duree": "55", "type_document_principal": "Devoir :", "supplement": ""
   }
5. Exécuter le script Python :

python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "<dossier du projet>/2nde/Sequence-Vecteurs" \
  --name "DS_Vecteurs" \
  --template "Devoir" \
  --fields-file "C:/chemin/vers/fields.json"

6. Rapporter succès (et signaler les éventuels avertissements non bloquants, ex. niveau trop long)
```

### Exemple 2 : Créer un cours avec sections

```
Utilisateur : "Nouveau cours sur les fonctions pour la première"

1. Analyser : type=Cours, niveau=1ere_spe, theme=fonctions
2. Obtenir template "Cours"
3. Écrire (outil Write) fields.json :
   {
     "niveau": "$\\mathbf{1^{\\text{ère}}}$", "theme": "Fonctions de référence",
     "type_etablissement": "Lycée", "nom_etablissement": "Lycée Exemple",
     "supplement": "", "type_document_principal": "Cours :",
     "contenu_principal": "\\input{enonce},"
   }
4. Exécuter le script Python avec --create-sections :

python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "<dossier du projet>/1ere_spe/Sequence-Fonctions" \
  --name "Cours_Fonctions" \
  --template "Cours" \
  --fields-file "C:/chemin/vers/fields.json" \
  --create-sections

5. Rapporter avec chemins et prochaines étapes
```

### Exemple 3 : Commande complète pour un cours (Produit scalaire)

```
# fields.json (écrit avec Write) :
{
  "niveau": "$\\mathbf{1^{\\text{ère}}}$",
  "theme": "Produit scalaire dans le plan",
  "type_etablissement": "Lycée",
  "nom_etablissement": "Lycée Exemple",
  "supplement": "",
  "type_document_principal": "Cours :",
  "contenu_principal": "\\input{enonce},"
}
```

```bash
python .claude/skills/tex-document-creator/scripts/create_document.py \
  --destination "<dossier du projet>/1ere_spe/Sequence-Produit_scalaire" \
  --name "Cours_Produit_scalaire" \
  --template "Cours" \
  --fields-file "<dossier du projet>/1ere_spe/Sequence-Produit_scalaire/fields.json" \
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
  --fields-file "chemin/vers/fields.json" \
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

## Convention d'écriture des commentaires dans les templates

**RÈGLE À RESPECTER dans tout template de `.claude/datas/latex-modeles/`.**

Le parseur de `document_creator_server.py` distingue un **champ** d'un **commentaire
LaTeX ordinaire** par l'espace qui suit le `%` :

| Écriture | Interprétation |
|---|---|
| `% nom_champ` | **champ** à remplir |
| `% nom_champ : option1, option2` | **champ** avec liste d'options |
| `%commentaire libre` (collé) | **commentaire**, ignoré par le parseur |

Un commentaire ordinaire écrit avec une espace (`% Activer ou désactiver…`) est donc
lu comme un champ nommé `Activer`, et le template devient **inutilisable** : toute
création échoue avec `{"status":"error","missing_fields":["Activer", …]}`.

Corollaire pour les commentaires en fin de ligne :

```latex
\displayitempointsfalse %Ne pas afficher les boîtes    % correct
\displayitempointsfalse % Ne pas afficher les boîtes   % CASSE le template
```

Les séparateurs (`% =====`) et les commentaires commençant par une ponctuation ne
posent pas de problème : le parseur ne capture qu'un mot (`\w+`).

**En cas de doute**, contrôler avant d'utiliser un template :

```bash
python ".claude/skills/tex-document-creator/scripts/get_template_info.py" --template "<nom>"
```

Tout champ listé qui n'est pas un vrai paramètre (`niveau`, `theme`,
`type_etablissement`, `nom_etablissement`, `supplement`, `type_document_*`,
`contenu_*`, `duree`…) signale un commentaire mal écrit dans le template : coller
son `%` au texte.

## Détection des champs : une seule source de vérité

`get_template_info.py` et `create_document.py` partagent la **même fonction**
d'analyse des champs (`analyze_template_fields`) et le **même calcul** de
« requis vs optionnel » (`compute_field_requirements`), dans
`.claude/mcp_servers/document_creator_server.py`. Conséquence : la liste des champs
manquants annoncée par `get_template_info` est **toujours identique** à celle qui
ferait échouer `create_document`. Il n'y a plus besoin de deviner : `required_fields`
et `example_fields_file` dans la réponse de `get_template_info` sont directement
exploitables.

## Filet de sécurité : lignes vides dans \chapitre / \chapEval

`\chapitre` et `\chapEval` sont déclarées avec des arguments xparse `m` (non `+m`,
donc non longs) : une ligne totalement vide à l'intérieur d'un de leurs 6 groupes
provoque `Paragraph ended before \chapitre was complete`. Cela peut arriver si une
valeur de champ collée par l'agent contient elle-même un saut de paragraphe (texte
multi-lignes copié tel quel dans `theme` ou `supplement`).

`create_document.py` neutralise automatiquement ce cas : après remplissage des
champs, toute ligne vide repérée à l'intérieur d'un appel `\chapitre[...]`/
`\chapEval[...]` est protégée par un `%` (rien à faire côté agent). Néanmoins,
**éviter de coller des valeurs multi-lignes** dans les champs de `\chapitre` (niveau,
thème, établissement, supplément) : ce sont des champs d'en-tête, censés tenir sur
une ligne visuelle.

## Avertissement : niveau trop long dans le bandeau

La boîte de niveau de `\chapitre`/`\chapEval` mesure une largeur fixe de **1,5 cm**
en police `\Large` (voir `bfcours-conventions.md`, section « Fichier maître : la
boîte du niveau »). Au-delà d'environ **5 caractères rendus** (ex. `STI2D` tient tout
juste, `Techno` déborde déjà légèrement), le texte déborde silencieusement et
chevauche le titre du document — sans aucune erreur de compilation.

`create_document.py` estime la longueur rendue du champ `niveau` (en retirant le
balisage LaTeX) et émet un **avertissement non bloquant** dans la réponse
(`"warnings"`) si ce seuil est dépassé. Le document est créé quand même : vérifier
alors le rendu PDF et envisager `\shortstack` sur deux lignes pour un niveau composé
(séries technologiques, options).

## Rappels Critiques

- TOUJOURS vérifier que le modèle existe avant de créer
- TOUJOURS utiliser `--fields-file` (jamais de valeurs LaTeX à antislashes en argument
  Bash direct) : écrire le JSON avec l'outil Write, jamais via heredoc ni `python -c`
- TOUJOURS fournir tous les champs requis par le template (voir `required_fields` de
  `get_template_info`)
- TOUJOURS utiliser des chemins absolus
- TOUJOURS créer un fichier CLAUDE.md avec `--claude-instructions`
- NE JAMAIS écraser un document existant sans confirmation
- NE JAMAIS écrire à la main le document ou le fichier maître quand `create_document.py`
  échoue : compléter le `example_fields_file` renvoyé par l'erreur et relancer le script
- Dans un nouveau template, écrire les commentaires ordinaires **collés au `%`**
  (voir la section ci-dessus), sinon le template devient inutilisable
