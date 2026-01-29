# /createTex - Création automatique de documents LaTeX pédagogiques

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

### ÉTAPE 3 : DÉTERMINATION DU CHEMIN DE DESTINATION

L'utilisateur va te donner un dossier dans lequel initier la création du projet.

Sinon tu détermine l'endroit idéal, et tu lui demande si ça convient.

### ÉTAPE 4 : Création du document grâce à ton skill

Utilise ton skill tex-document-creator pour créer le projet.
