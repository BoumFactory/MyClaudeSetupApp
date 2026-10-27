---
name: bareme-actions-eleves
description: Skill pour établir des barèmes basés sur l'atomisation des actions élèves. Calcule les points via coefficient × actions, permet la conversion sur 20, et fournit une métrique d'analyse du barème (densité). Le skill produit uniquement des barèmes : la notation des copies se fait hors du skill. Utiliser après la rédaction d'un document LaTeX pour générer un barème rationnel.
---

# Barème Basé sur les Actions Élèves

Système expert pour établir des barèmes rationnels et analysables, basés sur l'atomisation des attendus de correction en actions élèves distinctes.

**Périmètre** : le skill produit uniquement des barèmes (fichiers `bareme.json`, `bareme.html`, `bareme.csv`). La notation des copies est externe au skill : il ne saisit ni ne calcule aucune note d'élève.

## Philosophie

### Le Problème du Barème Traditionnel

Les barèmes traditionnels attribuent des points de manière arbitraire :
- "Question 1 : 3 points" → Pourquoi 3 ? Sur quels critères ?
- Impossible de comparer la difficulté entre évaluations
- Impossible de justifier ou d'ajuster la répartition des points

### La Solution : Actions Élèves

**Principe fondamental** : Chaque point correspond à une **action cognitive élémentaire** réalisée par l'élève.

Une **action élève** est :
- Une opération atomique (non décomposable)
- Observable dans la copie
- Réussie ou non (pas de demi-mesure au niveau atomique)

## Architecture du Barème

### Structure Hiérarchique

```
Évaluation
├── Exercice 1 (coef: 1)
│   ├── Question 1
│   │   ├── Critère 1 (1 action)
│   │   ├── Critère 2 (1 action)
│   │   └── Critère 3 (1 action)
│   └── Question 2
│       └── Critère 1 (1 action)
├── Exercice 2 - Géométrie (coef: 0.5)
│   └── Question 1
│       ├── Critère 1 (1 action)
│       └── Critère 2 (1 action)
└── ...
```

### Coefficients par Type d'Exercice

| Type d'exercice | Coefficient | Justification |
|-----------------|-------------|---------------|
| **Calcul numérique** | 1 | Charge cognitive standard |
| **Calcul littéral** | 1 | Charge cognitive standard |
| **Résolution d'équations** | 1 | Raisonnement structuré |
| **Problème ouvert** | 1 | Raisonnement complexe |
| **Géométrie repérée** | 0.5 | Actions plus mécaniques (placer, tracer) |
| **Géométrie pure** | 0.5 | Construction, lecture graphique |
| **QCM** | 1 | Mais 1 action = 1 bonne réponse |
| **Tâche complexe** | 1 | Éventuellement 5 pts forfaitaires |

### Formules de Calcul

```
Points_question = Σ(actions_critères) × coef_exercice
Points_exercice = Σ(points_questions)
Total_libre = Σ(points_exercices)
Coefficient_de_conversion = Note_cible / Total_libre
```

Le coefficient de conversion est communiqué avec le barème ; son application aux copies relève de l'outil de notation de l'enseignant, hors skill.

## Règles d'Atomisation

### Principe : Une Action = Une Trace

Chaque action doit correspondre à quelque chose de **visible dans la copie**.

### Exemples d'Atomisation

#### Calcul de Fraction

**Énoncé** : Calculer 3/4 + 5/6

**Atomisation** :
| Action | Description | Points |
|--------|-------------|--------|
| 1 | Mise au même dénominateur (12) | 1 |
| 2 | Numérateurs transformés (9/12 + 10/12) | 1 |
| 3 | Addition des numérateurs (19/12) | 1 |

**Total** : 3 actions × coef 1 = 3 points

#### Développement avec Identité Remarquable

**Énoncé** : Développer (2x + 3)²

**Atomisation** :
| Action | Description | Points |
|--------|-------------|--------|
| 1 | Identification IR (a+b)² | 1 |
| 2 | Identification a=2x, b=3 | 1 |
| 3 | Application formule a² + 2ab + b² | 1 |
| 4 | Calcul : 4x² + 12x + 9 | 1 |

**Total** : 4 actions × coef 1 = 4 points

#### Géométrie : Placer des Points

**Énoncé** : Placer A(-2;1), B(4;1), C(6;5), D(0;5)

**Atomisation** :
| Action | Description | Points |
|--------|-------------|--------|
| 1 | Point A bien placé | 1 |
| 2 | Point B bien placé | 1 |
| 3 | Point C bien placé | 1 |
| 4 | Point D bien placé | 1 |

**Total** : 4 actions × coef 0.5 = 2 points

#### Calcul de Distance

**Énoncé** : Calculer AB avec A(1;2) et B(4;6)

**Atomisation** :
| Action | Description | Points |
|--------|-------------|--------|
| 1 | Formule distance posée | 1 |
| 2 | Substitution des coordonnées | 1 |
| 3 | Calcul sous la racine | 1 |
| 4 | Simplification si possible | 1 |

**Total** : 4 actions × coef 0.5 = 2 points (géométrie)

### Cas Particuliers

#### QCM
- 1 bonne réponse = 1 action
- Coefficient 1 (le raisonnement est implicite)

#### Tâche de Recherche / Problème Ouvert
- Attribution forfaitaire : **5 points**
- Ne pas atomiser (trop complexe)
- Évaluation globale de la démarche

#### Justification / Rédaction
- "Justifier" = 1 action (la phrase de conclusion)
- "Démontrer" = plusieurs actions selon les étapes

## Métriques d'Analyse

### Densité d'une Évaluation

```
Densité = Total_actions / Note_cible
```

| Densité | Interprétation |
|---------|----------------|
| > 4 | Évaluation très dense (difficile) |
| 3-4 | Évaluation standard |
| 2-3 | Évaluation accessible |
| < 2 | Évaluation légère |

**Exemple** : 63 actions pour une note sur 20 → Densité = 3.15 (standard)

### Temps par Action

Pour calibrer la durée d'une évaluation :

| Type d'action | Temps estimé |
|---------------|--------------|
| QCM simple | 30s |
| Calcul basique | 1-2 min |
| Raisonnement | 2-3 min |
| Construction géométrique | 1-2 min |
| Rédaction justification | 2 min |

**Règle** : Prévoir 1.5× le temps théorique pour les élèves.

## Workflow d'Utilisation

### Étape 1 : Rédiger le Document LaTeX

Utiliser le skill `bfcours-latex` pour rédiger l'évaluation avec :
- Environnement `EXO` pour chaque exercice
- `\tcbitempoint{N}` pour indiquer les points prévus
- `\exocorrection` suivi de la correction détaillée

### Étape 2 : Atomiser la Correction

Pour chaque question, lister les actions attendues dans la correction :

```latex
\exocorrection
% ACTION 1 : Identification de l'identité remarquable
On reconnaît $(a+b)^2$ avec $a = 2x$ et $b = 3$.
% ACTION 2 : Application de la formule
$(2x+3)^2 = (2x)^2 + 2 \times 2x \times 3 + 3^2$
% ACTION 3 : Calcul final
$= 4x^2 + 12x + 9$
```

### Étape 3 : Générer le Barème JSON

Structure du fichier `bareme.json` :

```json
{
  "titre": "Nom de l'évaluation",
  "noteCible": 20,
  "exercices": [
    {
      "titre": "Exercice 1 : Calcul littéral",
      "coef": 1,
      "questions": [
        {
          "numero": "1",
          "enonce": "Développer (2x+3)²",
          "criteres": [
            { "points": 1, "description": "Identification IR (a+b)²" },
            { "points": 1, "description": "Identification a=2x, b=3" },
            { "points": 1, "description": "Application formule" },
            { "points": 1, "description": "Calcul : 4x² + 12x + 9" }
          ]
        }
      ]
    }
  ],
  "totalPoints": 63
}
```

### Étape 4 : Utiliser l'Interface HTML

L'interface `bareme.html` permet de :
- Visualiser et éditer le barème (exercices, questions, critères)
- Modifier les coefficients en temps réel
- Voir la synthèse avec accordéon
- Sauvegarder en JSON et exporter en CSV pour tableur
- Afficher le coefficient de conversion (note cible ÷ total des points) et la densité

L'interface est un éditeur de barème : elle ne note aucune copie.

### Étape 5 : Exploiter le barème

1. Relire la synthèse (total des points, densité) et ajuster les critères ou les coefficients
2. Exporter `bareme.json` / `bareme.csv`
3. Communiquer le barème aux élèves ou le reporter dans l'outil de notation de l'enseignant (la notation des copies est externe au skill)

## Intégration avec bfcours-latex

### Correspondance \tcbitempoint

Dans `bfcours-latex`, `\tcbitempoint{N}` indique N points. Avec ce skill :

```latex
% Avant atomisation (estimation grossière)
\tcbitempoint{3}\acc{Développer} $(2x+3)^2$.

% Après atomisation (précis)
\tcbitempoint{4}\acc{Développer} $(2x+3)^2$ et \acc{réduire}.
```

### Recommandation

Toujours rédiger la correction **avant** d'attribuer les points. L'atomisation de la correction donne le nombre exact d'actions.

## Format de Sortie

### Fichiers Générés

| Fichier | Description |
|---------|-------------|
| `bareme.json` | Structure du barème (portable) |
| `bareme.html` | Éditeur et synthèse du barème |
| `bareme.csv` | Export tableur |

### Structure Minimale du JSON

```json
{
  "titre": "string",
  "noteCible": 20,
  "exercices": [
    {
      "titre": "string",
      "coef": 1,
      "questions": [
        {
          "numero": "string",
          "enonce": "string",
          "criteres": [
            { "points": 1, "description": "string" }
          ]
        }
      ]
    }
  ],
  "totalPoints": 0
}
```

## Rappels Critiques

1. **Toujours atomiser la correction d'abord** avant d'attribuer les points
2. **Un critère = une action** = quelque chose de visible dans la copie
3. **Coefficient 0.5 pour la géométrie** (actions moins cognitives) : choix personnel, réglable selon vos pratiques
4. **Utiliser l'interface HTML** pour éditer et relire le barème (pas pour noter)
5. **Analyser la densité** pour calibrer vos évaluations

## Références

- Éditeur de barème : `templates/bareme.html` (monolithique, portable)
- Template JSON : Généré automatiquement depuis le document LaTeX
- Intégration : Skill `bfcours-latex` pour la rédaction
