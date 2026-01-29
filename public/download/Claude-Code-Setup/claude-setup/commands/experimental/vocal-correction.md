# /vocal-correction - Génération de fiches de correction à partir de transcriptions vocales

Transforme une transcription vocale de correction de copies en un fichier LaTeX avec des fiches personnalisées par élève.

## Utilisation

```
/vocal-correction [chemin_transcription] [chemin_evaluation]
```

**Arguments :**
- `chemin_transcription` : Fichier texte contenant la transcription vocale
- `chemin_evaluation` : Fichier PDF ou LaTeX de l'évaluation (pour le barème)

## Workflow

### Phase 1 : Chargement des données

1. **Lire le fichier de transcription** fourni par l'utilisateur
2. **Lire l'évaluation** pour comprendre :
   - La structure des exercices
   - Le barème par question
   - Les réponses attendues

### Phase 2 : Analyse de la transcription

Pour chaque élève détecté dans la transcription :

1. **Extraire les informations** :
   - Nom/prénom de l'élève
   - Points par exercice
   - Remarques spécifiques
   - Note finale si mentionnée

2. **Identifier les erreurs types** :
   - Erreurs de calcul
   - Erreurs de méthode
   - Éléments manquants
   - Confusions conceptuelles

3. **Générer des conseils personnalisés** basés sur les erreurs identifiées

### Phase 3 : Génération LaTeX

1. **Charger le template** depuis `.claude\skills\experimental\vocal-correction\template_fiche_correction.tex`

2. **Pour chaque élève**, générer une page avec :
   - En-tête avec nom et note
   - Un bloc par exercice avec points et remarques
   - Une boîte "À revoir" avec les conseils
   - Une appréciation générale

3. **Compiler le fichier** (optionnel) en PDF

### Phase 4 : Sortie

- Sauvegarder le fichier LaTeX dans le dossier de l'évaluation
- Nom du fichier : `corrections_vocales_[NomEval].tex`
- Afficher un résumé des élèves traités

## Format de transcription attendu

Le professeur dicte naturellement ses remarques. Le skill est flexible sur le format :

```
Élève : [Prénom NOM]
Exercice 1 : [points]/[max] - [remarques libres]
...
Note finale : [note]/20

Élève suivant : [Prénom NOM]
...
```

**Variantes acceptées :**
- "Copie de Emma" / "Pour Lucas" / "Emma Martin"
- "Exo 1" / "Premier exercice" / "Question 1"
- Notation implicite ("bien", "moitié", "rien")

## Exemple

```
/vocal-correction tests/rapports_vocaux_eval/transcription.txt tests/rapports_vocaux_eval/Evaluation_Derivation_Trigo.pdf
```

## Dépendances

- Skill `bfcours-latex` pour la génération LaTeX
- Skill `tex-compiling-skill` pour la compilation (optionnel)
