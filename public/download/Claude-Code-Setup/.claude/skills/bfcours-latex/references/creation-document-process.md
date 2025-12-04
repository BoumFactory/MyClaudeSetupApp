## Description
Crée automatiquement un document LaTeX pédagogique en utilisant le serveur MCP `document-creator-server`. Analyse la requête de l'utilisateur pour identifier le type de document, le niveau, le thème, puis choisit le modèle approprié et le place au bon emplacement dans l'arborescence.

## Usage
```
/createTex <description_du_document>
```

## Exemples d'utilisation
```bash
# Évaluation / Contrôle / DS
/createTex évaluation sur les vecteurs en seconde
→ Modèle: Devoir, Niveau: 2nde, Emplacement: 1. Cours\2nde\Sequence-Vecteurs\Evaluation_vecteurs\

# Cours
/createTex cours sur les fonctions affines en troisième
→ Modèle: Cours, Niveau: 3eme, Emplacement: 1. Cours\3eme\Sequence-Fonctions_affines\Cours_fonctions_affines\

# Activité découverte
/createTex activité découverte des suites en première
→ Modèle: Découverte, Niveau: 1ere_spe, Emplacement: 1. Cours\1ere_spe\Sequence-Suites\Activite_decouverte_suites\

# Exercices (version light par défaut)
/createTex exercices sur les probabilités en terminale
→ Modèle: Exercices light, Niveau: Terminale, Emplacement: 1. Cours\Terminale\Sequence-Probabilites\Exercices_probabilites\

# Exercices avec corrections détaillées (version heavy)
/createTex exercices avec corrections complètes sur les équations
→ Modèle: Exercices heavy, Niveau: 3eme, Emplacement: 1. Cours\3eme\Sequence-Equations\Exercices_equations\

# Devoir maison
/createTex DM sur le produit scalaire en première
→ Modèle: Devoir_maison, Niveau: 1ere_spe, Emplacement: 1. Cours\1ere_spe\Sequence-Produit_scalaire\DM_produit_scalaire\

# Plan de séquence
/createTex plan de séquence sur les fonctions en seconde
→ Modèle: Plan sequence, Niveau: 2nde, Emplacement: 1. Cours\2nde\Sequence-Fonctions\Plan_sequence_fonctions\
```

## Protocole d'exécution

### ÉTAPE 1 : ANALYSE DE LA REQUÊTE

Tu dois extraire de la description de l'utilisateur :

1. **Type de document** (obligatoire) - **MODÈLES RÉELS DISPONIBLES** :
   - Cours → modèle `Cours`
   - Évaluation / Contrôle / DS / Devoir surveillé → modèle `Devoir`
   - DM / Devoir maison → modèle `Devoir_maison`
   - Exercices avec corrections détaillées → modèle `Exercices heavy`
   - Exercices rapides sans corrections → modèle `Exercices light`
   - Activité découverte / Investigation → modèle `Découverte`
   - Plan de séquence / Planification → modèle `Plan sequence`
   - Récapitulatif de séance → modèle `Recap_seance`
   - AP / Accompagnement personnalisé → modèle `AP`
   - Travail de groupe → modèle `Groupe`
   - Activité informatique / Algo → modèle `Info`
   - Jeux mathématiques → modèle `Jeux`
   - Rapport d'incident → modèle `Rapport incident`
   - SOUAP → modèle `SOUAP`
   - Nouveau document générique → modèle `Nouveau`

2. **Niveau** (obligatoire) :
   - Seconde / 2nde / 2de → `2nde`
   - Première / 1ère / 1ere → `1ere_spe`
   - Terminale / Term / Tle → `Terminale`
   - Troisième / 3ème / 3eme → `3eme`
   - Quatrième / 4ème / 4eme → `4eme`
   - Cinquième / 5ème / 5eme → `5eme`
   - Sixième / 6ème / 6eme → `6eme`

3. **Thème/Sujet** (obligatoire) :
   - Extraire le sujet principal (vecteurs, fonctions, probabilités, etc.)
   - Normaliser : minuscules, underscores, sans accents
   - Exemples : "vecteurs", "fonctions_affines", "probabilites", "produit_scalaire"

### ÉTAPE 2 : VÉRIFICATION DE L'ARBORESCENCE

**OBLIGATOIRE** : Utiliser `LS` ou `Glob` pour explorer la structure existante :
1. Vérifier que le dossier du niveau existe (`1. Cours\2nde\`)
2. Identifier si une séquence sur le thème existe déjà
3. Respecter la structure découverte

**Structure type attendue** :
```
1. Cours/
├── 2nde/
│   ├── Sequence-Vecteurs/
│   │   ├── Cours/
│   │   ├── Evaluations/
│   │   ├── Exercices/
│   │   └── [autres sous-dossiers]
│   └── [autres séquences]
├── 1ere_spe/
└── [autres niveaux]
```

### ÉTAPE 3 : CONSULTATION MCP `document-creator-server`

**OBLIGATOIRE** : Avant de créer le document, consulter le serveur MCP :

1. **Lister les modèles disponibles** :
   ```
   list_templates()
   ```

2. **Obtenir les informations du modèle choisi** :
   ```
   get_template_info(template_name)
   ```
   → Connaître tous les champs paramétrables

### ÉTAPE 4 : DÉTERMINATION DU CHEMIN DE DESTINATION

**Règles de construction** :
1. **Chemin de base** : `C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\`
2. **Niveau** : Ajouter le dossier du niveau (`2nde`, `1ere_spe`, etc.)
3. **Séquence** :
   - Si séquence existe → utiliser son nom exact
   - Sinon → créer `Sequence-<Thème_normalisé>`
4. **Nom du document** : `<Type>_<thème_normalisé>` (exemple : `Evaluation_vecteurs`)

**Exemples complets** :
```
# Requête : "évaluation sur les vecteurs en seconde"
destination_path = C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\2nde\Sequence-Vecteurs
document_name = Evaluation_vecteurs

# Requête : "cours sur les suites en première"
destination_path = C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\1. Cours\1ere_spe\Sequence-Suites
document_name = Cours_suites
```

### ÉTAPE 5 : REMPLISSAGE INTELLIGENT DES CHAMPS

**Pour chaque champ du template**, remplir intelligemment selon le contexte :

#### Champs communs (basés sur les vrais templates) :

**TOUS les modèles utilisent ces champs dans `\chapitre[]` :**

- **niveau** : Niveau LaTeX formaté
  - Sixième → `$\mathbf{6^{\text{ème}}}$`
  - Seconde → `$\mathbf{2^{\text{nde}}}$`
  - Première → `$\mathbf{1^{\text{ère}}}$`
  - Terminale → `$\mathbf{T^{\text{Le}}}$`

   ATTENTION : Il faut **échapper les caractères** pour passer les paramètres.

- **theme** : Thème du document (Vecteurs, Équations, Probabilités, etc.)

- **type_etablissement** : "Collège" ou "Lycée" selon le niveau

- **nom_etablissement** : Nom de l'établissement
  - Choix : "Amadis Jamyn", "Eugène Belgrand", "Othe et Vanne" (ou laisser vide)

- **supplement** : Éléments supplémentaires optionnels
  - Pour cours : `\tableofcontents`, `\tableauPresenteEvalSixieme{}{10}`
  - Laisser vide par défaut

- **type_document_principal** : Type de document affiché en en-tête
  - Pour Cours : "Cours :"
  - Pour Exercices : "Exercices"
  - Pour Devoir : "Devoir :"

- **contenu_principal** : Contenu du document (laisser le commentaire pour l'utilisateur)
  - Par défaut : `\input{enonce},`

#### Champs spécifiques selon le modèle :

**Pour Devoir** (évaluations, DS, contrôles) :
- **duree** : Durée en minutes
  - Choix : 10, 15, 30, 55
  - Format dans `\tableauEval{...}` : `{10}`, `{15}`, `{30}`, `{55}`

**Pour Devoir_maison** :
- **date_rendu** : Date de rendu du DM
  - Format : "JJ/MM/AAAA" ou "lundi 15 janvier"
  - Utilisé dans `\messageDevoir` : "Devoir à rendre pour le ..."

**Pour Exercices heavy/light** :
- **type_document_secondaire** : Pour la page de solutions
  - Par défaut : "Solution"

- **contenu_secondaire** : Contenu des solutions
  - Choix : `\input{solutions}`, `\rdexocorrection[columns=1]{0}`, `\rdexocorrection[columns=2]{0}`

**Pour Cours** :
- **supplement** : Éléments additionnels
  - `\tableofcontents` → Table des matières
  - `\tableauPresenteEvalSixieme{}{10}` → Tableau de présentation

- Le cours inclut automatiquement :
  - `\tableaucompetence{\competence{nobug}}`
  - `\printvocindex`
  - `\voc{nobug}`

### ÉTAPE 6 : OPTIONS DE CRÉATION

**TOUJOURS utiliser ces options** :
- `create_folder = true` → **OBLIGATOIRE** pour créer le dossier du document
- `create_images_folder = false` → Sauf si demandé explicitement
- `create_annexes_folder = false` → Sauf si demandé explicitement
- `create_sections_folder = true` → Pour les cours uniquement
- `create_figures_file = true` → Pour avoir le fichier enonce_figures.tex
- `include_claude_instructions = true` → Pour faciliter les modifications futures

### ÉTAPE 7 : CRÉATION VIA MCP

**Utiliser la fonction MCP** :
```python
create_document(
    destination_path = "<chemin_calculé>",
    document_name = "<nom_document>",
    template_name = "<modele_choisi>",  # Ex: "Devoir", "Cours", "Devoir_maison", "Exercices heavy"
    field_values = '{
        "niveau": "$\\mathbf{2^{\\text{nde}}}$",  # Formaté selon le niveau
        "theme": "Vecteurs",  # Thème du document
        "type_etablissement": "Lycée",  # "Collège" ou "Lycée"
        "nom_etablissement": "",  # Vide ou nom de l'établissement
        "supplement": "",  # Éléments supplémentaires (tableofcontents, etc.)
        "type_document_principal": "Devoir :",  # Type affiché en en-tête
        "contenu_principal": "\\input{enonce},",  # Contenu par défaut
        # Champs spécifiques selon le modèle :
        "duree": "55}",  # Pour Devoir uniquement
        "date_rendu": "lundi 20 janvier",  # Pour Devoir_maison uniquement
        "contenu_secondaire": "\\rdexocorrection[columns=1]{0},",  # Pour Exercices
        # ... autres champs selon le modèle
    }',
    create_folder = true,
    create_images_folder = false,
    create_annexes_folder = false,
    create_sections_folder = <true pour cours, false sinon>,
    create_figures_file = true,
    include_claude_instructions = true
)
```

### ÉTAPE 8 : ENRICHISSEMENT PÉDAGOGIQUE

**APRÈS création**, enrichir le document :

1. **Compétences** :
   - Utiliser `competences-server` → `advanced_search(query, niveau)`
   - Identifier les compétences pertinentes
   - Les intégrer dans le document créé

2. **Compilation de test** :
   - **OBLIGATOIRE** : Tester avec `latex-compiler-server`
   - `quick_compile(file_path)` pour vérifier que tout compile
   - Corriger les erreurs éventuelles

### ÉTAPE 9 : RAPPORT DE CRÉATION

**Fournir un rapport détaillé** :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 DOCUMENT LATEX CRÉÉ AVEC SUCCÈS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type          : <type_document>
Niveau        : <niveau>
Thème         : <theme>
Modèle        : <template_name>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📂 EMPLACEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dossier       : <destination_path>
Fichier       : <document_name>.tex
Structure     : <liste des dossiers/fichiers créés>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMPÉTENCES ASSOCIÉES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
<liste des compétences identifiées via competences-server>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VÉRIFICATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Compilation testée avec succès
✓ Instructions Claude intégrées (CLAUDE.md)
✓ Fichier enonce_figures.tex créé

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 PROCHAINES ÉTAPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Compléter le contenu du document
2. Ajouter les exercices/activités pédagogiques
3. Intégrer des illustrations (TikZ, images, etc.)
4. Vérifier la cohérence avec la progression pédagogique
```

## ⚠️ POINTS D'ATTENTION

### Gestion des cas particuliers

1. **Séquence inexistante** :
   - Créer automatiquement `Sequence-<Theme>` dans le bon dossier niveau
   - Informer l'utilisateur de la création

2. **Niveau ambigu** :
   - Si "première" sans précision → demander "générale" ou "spécialité"
   - Par défaut : `1ere_spe` (spécialité est plus fréquent)

3. **Thème complexe** :
   - "fonctions affines et linéaires" → normaliser en `fonctions_affines_lineaires`
   - Éviter les noms trop longs (max 30 caractères)

4. **Type de document ambigu** :
   - "fiche" seul → demander précision (exercices, méthode, etc.)
   - "exercices" sans précision → utiliser `Exercices light` (version légère)
   - Si corrections détaillées demandées explicitement → utiliser `Exercices heavy`
   - Par défaut : modèle `Exercices light` (version rapide sans corrections)

### Serveurs MCP utilisés

**OBLIGATOIRES** :
1. `document-creator-server` → Création du document
2. `encoding-fixer-server` → Correction UTF-8
3. `latex-compiler-server` → Test de compilation
4. `competences-server` → Identification des compétences

## Exemples détaillés d'exécution

### Exemple 1 : Évaluation simple

**Input** : `/createTex évaluation sur les vecteurs en seconde`

**Analyse** :
- Type : Devoir
- Niveau : 2nde
- Thème : vecteurs

**Exécution** :
```
1. Explorer : 1. Cours\2nde\
2. Chercher : Sequence-Vecteurs (existe ou à créer)
3. Modèle : Devoir
4. Destination : C:\...\1. Cours\2nde\Sequence-Vecteurs\
5. Nom : Evaluation_vecteurs
6. Champs :
   - niveau: "$\mathbf{2^{\text{nde}}}$"
   - theme: "Vecteurs"
   - type_etablissement: "Lycée"
   - nom_etablissement: "" (vide ou selon préférences)
   - duree: "55}" (55 minutes = 1h environ)
   - type_document_principal: "Devoir :"
   - contenu_principal: "\input{enonce},"
7. Créer avec create_folder=true, create_figures_file=true
8. Encoder UTF-8
9. Compiler test
10. Rapport
```

### Exemple 2 : Cours avec sections

**Input** : `/createTex cours sur les suites géométriques en première`

**Analyse** :
- Type : Cours
- Niveau : 1ere_spe
- Thème : suites_geometriques

**Exécution** :
```
1. Explorer : 1. Cours\1ere_spe\
2. Chercher : Sequence-Suites (existe ou à créer)
3. Modèle : Cours
4. Destination : C:\...\1. Cours\1ere_spe\Sequence-Suites\
5. Nom : Cours_suites_geometriques
6. Champs :
   - niveau: "$\mathbf{1^{\text{ère}}}$"
   - theme: "Suites géométriques"
   - type_etablissement: "Lycée"
   - nom_etablissement: "" (vide ou selon préférences)
   - supplement: "\tableofcontents" (table des matières)
   - type_document_principal: "Cours :"
   - contenu_principal: "\input{enonce},"
7. Créer avec create_folder=true, create_sections_folder=true, create_figures_file=true
8. Compétences : advanced_search("suites", "PREMIERE")
9. Encoder UTF-8
10. Compiler test
11. Rapport
```

### Exemple 3 : DM complexe

**Input** : `/createTex DM sur le produit scalaire et les équations de droites en première`

**Analyse** :
- Type : Devoir_maison
- Niveau : 1ere_spe
- Thème : produit_scalaire

**Exécution** :
```
1. Explorer : 1. Cours\1ere_spe\
2. Chercher : Sequence-Produit_scalaire (existe ou à créer)
3. Modèle : Devoir_maison
4. Destination : C:\...\1. Cours\1ere_spe\Sequence-Produit_scalaire\
5. Nom : DM_produit_scalaire
6. Champs :
   - niveau: "$\mathbf{1^{\text{ère}}}$"
   - theme: "Produit scalaire et équations de droites"
   - type_etablissement: "Lycée"
   - nom_etablissement: "" (vide ou selon préférences)
   - supplement: "" (vide)
   - type_document_principal: "Exercices"
   - date_rendu: "lundi 20 janvier 2025" (calculer : aujourd'hui + 7 jours)
   - contenu_principal: "\input{enonce},"
   - contenu_secondaire: "\rdexocorrection[columns=1]{0},"
7. Créer avec create_folder=true, create_figures_file=true
8. Compétences : advanced_search("produit scalaire", "PREMIERE")
9. Encoder UTF-8
10. Compiler test
11. Rapport
```

## 🔧 Intégration avec autres commandes

Cette commande `/createTex` crée la structure de base. Pour remplir le contenu :
- Utiliser `/adaptTex` pour adapter du contenu existant
- Déléguer aux agents spécialisés pour créer le contenu pédagogique

## Notes techniques

**Normalisation des noms** :
```python
def normaliser_nom(texte):
    # Minuscules
    texte = texte.lower()
    # Remplacer accents
    texte = texte.replace('é', 'e').replace('è', 'e').replace('à', 'a')
    # Espaces → underscores
    texte = texte.replace(' ', '_')
    # Garder seulement a-z, 0-9, _
    texte = re.sub(r'[^a-z0-9_]', '', texte)
    return texte
```

**Mapping niveau complet** :
```python
NIVEAUX = {
    "6eme": "Sixième",
    "5eme": "Cinquième",
    "4eme": "Quatrième",
    "3eme": "Troisième",
    "2nde": "Seconde",
    "1ere_spe": "Première spécialité",
    "Terminale": "Terminale"
}
```

## IMPORTANT

**TOUJOURS** :
- Vérifier l'arborescence existante avec LS/Glob AVANT de créer
- Utiliser `competences-server` pour enrichir pédagogiquement
- Utiliser `encoding-fixer-server` pour garantir UTF-8
- Utiliser `latex-compiler-server` pour valider la compilation
- Fournir un rapport détaillé de création
- Répondre entièrement en français
