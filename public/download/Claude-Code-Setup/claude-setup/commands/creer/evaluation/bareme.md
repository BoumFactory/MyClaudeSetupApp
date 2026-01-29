# /bareme - Génération de Barème Actions Élèves

## Description

Génère un barème rationnel basé sur l'atomisation des actions élèves à partir d'un document LaTeX d'évaluation existant. Produit un fichier `bareme.json` et une interface `bareme.html` pour la correction interactive.

## Usage

```
/bareme [chemin_document] [--note-cible N] [--output-dir DIR]
```

### Arguments

| Argument | Description | Défaut |
|----------|-------------|--------|
| `chemin_document` | Chemin vers le .tex ou dossier d'évaluation | Dossier courant |
| `--note-cible N` | Note maximale souhaitée | 20 |
| `--output-dir DIR` | Dossier de sortie | Même que le document |

## Exemples

```bash
# Générer le barème pour le DS dans le dossier courant
/bareme

# Générer pour un DS spécifique sur 30 points
/bareme "1. Devoirs_communs/2nde/DS_Fonctions" --note-cible 30

# Générer dans un dossier spécifique
/bareme "DS_Calculs.tex" --output-dir "./correction"
```

---

## PROTOCOLE D'EXÉCUTION

### ÉTAPE 0 : Chargement des Connaissances

1. Charger le skill `bareme-actions-eleves` pour la méthodologie
2. Identifier le document LaTeX source

### ÉTAPE 1 : Analyse du Document

1. **Lire le fichier principal** (.tex)
2. **Identifier les fichiers de contenu** : `enonce.tex`, `sections/*.tex`
3. **Extraire la structure** :
   - Environnements `EXO` avec leurs titres et codes compétences
   - Questions avec `\tcbitempoint{N}`
   - Corrections après `\exocorrection`

### ÉTAPE 2 : Détection du Type d'Exercice

Pour chaque exercice, déterminer le coefficient :

| Mots-clés dans le titre | Coefficient |
|------------------------|-------------|
| "géométrie", "repère", "figure", "construction", "tracer" | 0.5 |
| "QCM", "calcul", "littéral", "équation", "intervalle" | 1 |
| Par défaut | 1 |

### ÉTAPE 3 : Atomisation des Corrections

Pour chaque question avec correction :

1. **Lire la correction** après `\exocorrection`
2. **Identifier les actions atomiques** :
   - Chaque calcul intermédiaire = 1 action
   - Chaque identification (IR, facteur commun...) = 1 action
   - Chaque conclusion/réponse = 1 action
   - Chaque point placé sur un graphique = 1 action

3. **Formuler les critères** :
   - Description courte et vérifiable
   - Ex: "Calcul xM = (-2+6)/2 = 2"

### ÉTAPE 4 : Génération du JSON

Créer `bareme.json` avec la structure :

```json
{
  "titre": "Titre du document",
  "noteCible": 20,
  "exercices": [
    {
      "titre": "Exercice 1 : Titre",
      "coef": 1,
      "questions": [
        {
          "numero": "1",
          "enonce": "Texte de la question",
          "criteres": [
            { "points": 1, "description": "Action atomique" }
          ]
        }
      ]
    }
  ],
  "totalPoints": 0
}
```

### ÉTAPE 5 : Génération de l'Interface HTML

Copier le template `bareme.html` depuis :
```
.claude\skills\outillage\evaluation\bareme-actions-eleves\templates\bareme.html
```

Ou utiliser le template de référence existant si disponible dans le projet.

L'interface doit inclure :
- Navigation par onglets (exercices)
- Édition inline des critères
- Calcul automatique des totaux
- Onglet Synthèse avec accordéon
- Export JSON/CSV

### ÉTAPE 6 : Calcul des Métriques

Afficher les métriques finales :

```
═══════════════════════════════════════════
  BARÈME GÉNÉRÉ
═══════════════════════════════════════════

  Document    : DS Calculs et Géométrie
  Note cible  : /20

  ┌─────────────────────────────────────┐
  │ RÉSUMÉ                              │
  ├─────────────────────────────────────┤
  │ Total actions     : 63              │
  │ Total points      : 50              │
  │ Ratio conversion  : 0.40            │
  │ Densité           : 3.15 (standard) │
  └─────────────────────────────────────┘

  Fichiers générés :
  • bareme.json
  • bareme.html

═══════════════════════════════════════════
```

### ÉTAPE 7 : Interprétation de la Densité

| Densité | Interprétation | Recommandation |
|---------|----------------|----------------|
| > 4 | Très dense | Réduire le nombre de questions ou augmenter le temps |
| 3-4 | Standard | OK |
| 2-3 | Accessible | Convient aux évaluations diagnostiques |
| < 2 | Légère | Ajouter des questions ou réduire la note cible |

---

## QUESTIONS À POSER SI NÉCESSAIRE

1. **Correction absente** : "La correction de l'exercice N n'est pas rédigée. Voulez-vous que je l'atomise manuellement ou que vous la rédigiez d'abord ?"

2. **Type d'exercice ambigu** : "L'exercice 'Problème' contient de la géométrie et du calcul. Quel coefficient appliquer : 1 (calcul) ou 0.5 (géométrie) ?"

3. **Note cible non standard** : "La note cible est 20 par défaut. Voulez-vous une autre valeur ?"

---

## FICHIERS GÉNÉRÉS

| Fichier | Description |
|---------|-------------|
| `bareme.json` | Structure du barème (portable, éditable) |
| `bareme.html` | Interface de correction interactive |

---

## INTÉGRATION AVEC LE WORKFLOW

Cette commande s'intègre dans le workflow d'évaluation :

1. `/createTex` → Créer l'évaluation
2. Rédiger les exercices avec `bfcours-latex`
3. `/bareme` → Générer le barème
4. Corriger avec `bareme.html`
5. Analyser les résultats

---

## SKILL UTILISÉ

- `bareme-actions-eleves` : Méthodologie d'atomisation et calculs
