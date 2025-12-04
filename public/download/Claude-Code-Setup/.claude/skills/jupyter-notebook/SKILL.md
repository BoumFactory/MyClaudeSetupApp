---
name: jupyter-notebook
description: Skill pour créer ou modifier des notebooks Jupyter pédagogiques Python. Protocole structuré avec cours, exemples corrigés, QCM de vérification, exercices progressifs et boîte outils dépliante. Utiliser pour toute création/modification de notebooks .ipynb éducatifs.
---

# Jupyter Notebook Pédagogique - Skill de création

## Description

Skill spécialisé pour créer des notebooks Jupyter pédagogiques structurés selon un protocole quasi-systématique :
1. **Cours** : Explication théorique
2. **Exemple simple corrigé** : Code exécutable commenté
3. **QCM vérification** : 3 questions pour valider la compréhension
4. **Exercice d'analyse** : Comprendre un programme existant
5. **Exercice d'application** : Compléter/écrire du code
6. **Boîte "Outils"** : Rappel dépliant des notions externes si besoin

## Outils de navigation (notebook_tools.py)

Script Python pour naviguer et valider les notebooks **avant** de les modifier.

**Localisation :** `.claude/skills/jupyter-notebook/notebook_tools.py`

### Commandes disponibles

```bash
# Lister toutes les cellules avec aperçu
python .claude/skills/jupyter-notebook/notebook_tools.py list <notebook.ipynb>

# Rechercher une cellule par contenu
python .claude/skills/jupyter-notebook/notebook_tools.py find <notebook.ipynb> --pattern "Monte-Carlo"

# Valider la structure (balises HTML, types de cellules)
python .claude/skills/jupyter-notebook/notebook_tools.py validate <notebook.ipynb>

# Sortie JSON (pour traitement)
python .claude/skills/jupyter-notebook/notebook_tools.py list <notebook.ipynb> --json
```

### Exemple de sortie `list`

```
IDX  ID           TYPE       TITRE/APERCU
--------------------------------------------------------------------------------
0    cell-0       [M] markdown Estimer une probabilite par simulation
1    cell-1       [M] markdown Notion 1 : Principe de la simulation...
2    cell-2       [C] code     import random nb_face = 0 nb_simulations...
3    cell-3       [M] markdown Verification : QCM
```

`[M]` = markdown, `[C]` = code

### Exemple de sortie `validate`

```
Statut: [!!] INVALIDE
Nombre de cellules: 25

[ERREURS] (1):
  - [cell-12] HTML detecte dans une cellule CODE (devrait etre markdown)

[AVERTISSEMENTS] (2):
  - [cell-5] Cellule vide
  - [cell-18] Balises <div> non equilibrees
```

### Workflow de modification d'un notebook existant

1. **Explorer** : Lancer `list` pour voir la structure
2. **Cibler** : Lancer `find --pattern "..."` pour trouver les cellules à modifier
3. **Noter** : Relever les `cell_id` des cellules concernées
4. **Lire** : Utiliser `Read` pour voir le contenu complet si besoin
5. **Modifier** : Utiliser `NotebookEdit` avec les `cell_id` identifiés
6. **Valider** : Lancer `validate` pour vérifier la structure
7. **Relire** : `Read` final pour confirmer les modifications

**Important :** Toujours utiliser les outils de navigation AVANT de modifier pour éviter les erreurs de ciblage.

---

## Structure JSON d'un notebook Jupyter

```json
{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {},
      "source": ["# Titre\n", "Contenu markdown..."]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {},
      "outputs": [],
      "source": ["# Code Python\n", "print('Hello')"]
    }
  ],
  "metadata": {
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    },
    "language_info": {
      "name": "python",
      "version": "3.9.0"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 4
}
```

## Protocole pédagogique complet

### 1. En-tête du notebook

```markdown
# [EMOJI] Titre du notebook

<div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;">
    <strong>📚 Niveau :</strong> [Seconde/Première/Terminale]<br>
    <strong>🎯 Thème :</strong> [Thème mathématique]<br>
    <strong>⏱️ Durée estimée :</strong> [XX min]
</div>

---

## 🎯 Objectifs

À la fin de cette activité, vous serez capable de :
- ✅ Objectif 1
- ✅ Objectif 2
- ✅ Objectif 3

---

## 📋 Prérequis

<div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
Pour cette activité, vous devez savoir :

- 📌 Prérequis 1
- 📌 Prérequis 2
</div>

---

## 💡 Introduction

[Contexte et motivation pour cette notion]

<div style="background-color: #f0f4c3; padding: 10px; border-radius: 5px; margin: 10px 0;">
    <strong>🤔 Problème :</strong> [Problème que résout cette notion]<br>
    <strong>✨ Solution :</strong> [Ce que Python permet de faire]
</div>

---
```

### 2. Structure d'une notion

Pour CHAQUE notion du notebook, suivre cette structure :

```markdown
## 📚 Notion X : [Titre de la notion]

### 📖 Cours

[Explication théorique avec syntaxe et règles]

**Syntaxe :**
```python
# Format général
```

| Élément | Description | Exemple |
|---------|-------------|---------|
| ... | ... | ... |

**Exemple résolu :**
```

Puis une **cellule de code** avec l'exemple exécutable :

```python
# Exemple commenté
resultat = calcul()
print(resultat)
```

Puis le **QCM de vérification** :

```markdown
### ✅ Vérification : QCM

**Question 1 :** [Question sur la syntaxe]
- A) [Option A]
- B) [Option B]
- C) [Option C]

**Question 2 :** [Question sur le comportement]
- A) [Option A]
- B) [Option B]
- C) [Option C]

**Question 3 :** [Question de compréhension]
- A) [Option A]
- B) [Option B]
- C) [Option C]

<details>
<summary>✅ Correction</summary>

**Question 1 :** [Lettre]) [Réponse]
**Explication :** [Justification]

**Question 2 :** [Lettre]) [Réponse]
**Explication :** [Justification]

**Question 3 :** [Lettre]) [Réponse]
**Explication :** [Justification]
</details>
```

Puis **l'exercice de compréhension** :

```markdown
### 🔍 Exercice 1 : Comprendre un programme

Que fait le programme suivant ?
```

Cellule de code à analyser :

```python
# Programme à comprendre
x = [1, 2, 3]
for i in x:
    print(i * 2)
```

```markdown
<details>
<summary>Correction</summary>

Ce programme [explication détaillée].
</details>
```

Puis **l'exercice d'application** :

```markdown
### 💡 Exercice 2 : Application

#### A) Compléter le code suivant
```

Cellule de code à compléter :

```python
# Description de ce qu'il faut faire
x = 5
y = ...  # Complétez
```

```markdown
#### B) [Exercice plus libre]

*Indice : [Indication utile]*
```

Cellule vide pour l'élève :

```python
# Écrivez votre code ici
```

```markdown
<details>
<summary>Correction A</summary>

```python
y = x * 2
```
</details>

<details>
<summary>Correction B</summary>

```python
# Solution complète
```
</details>

---
```

### 3. Boîte "Outils" dépliante (RARE)

⚠️ **UNIQUEMENT pour rappeler des notions d'AUTRES notebooks** (pas du notebook actuel).

```markdown
<details>
<summary><strong>Rappel - Notion vue dans un autre module</strong></summary>

`fonction(parametre)` — vu dans : [Nom du notebook source]
</details>
```

**Quand utiliser ?**
- Quand une notion d'un **autre** notebook est nécessaire
- **JAMAIS** pour rappeler ce qui est dans le cours du notebook actuel

### 4. Approches selon le niveau : Code complet vs Complétion

**Deux approches pédagogiques selon le niveau et la notion :**

#### A) Code COMPLET (Notebooks de base - Seconde principalement)

Pour les **notions fondamentales** où l'élève apprend la syntaxe Python :
- L'élève écrit **tout le code** dans une cellule vide
- On fournit uniquement des indices (briques, variables)
- Objectif : maîtriser la syntaxe Python

```python
# Écrivez votre code ici
```

**Utiliser pour :** Variables, conditions, boucles for, fonctions de base, listes.

#### B) Exemples de COURS actifs (Notebooks avancés)

**Principe fondamental :** Même dans les exemples de cours, l'élève doit être **actif**.

Dans les exemples qui illustrent une notion :
- La quasi-totalité du code est implémentée (structure, boucles, affichage)
- L'élève complète **uniquement les formules mathématiques** (`...`)
- Objectif : forcer l'élève à suivre et comprendre, pas à recopier passivement

**Exemple - AVANT (passif) :**
```python
import random

nb_somme_10 = 0
nb_simulations = 20000

for i in range(nb_simulations):
    de1 = random.randint(1, 6)
    de2 = random.randint(1, 6)
    somme = de1 + de2
    if somme == 10:
        nb_somme_10 = nb_somme_10 + 1

frequence = nb_somme_10 / nb_simulations
print(f"Estimation de P(somme = 10) : {frequence:.4f}")
```

**Exemple - APRÈS (actif) :**
```python
import random

nb_somme_10 = 0
nb_simulations = 20000

for i in range(nb_simulations):
    de1 = random.randint(1, 6)
    de2 = random.randint(1, 6)
    somme = ...                     # À compléter
    if somme == 10:
        nb_somme_10 = ...           # À compléter

frequence = ...                     # À compléter
print(f"Estimation de P(somme = 10) : {frequence:.4f}")
```

**Ce qui change :**
- L'élève doit réfléchir à `somme = de1 + de2`
- L'élève doit comprendre l'incrémentation `nb_somme_10 + 1`
- L'élève doit calculer la fréquence `nb_somme_10 / nb_simulations`

**Règle générale pour les exemples de cours :**
- Tout le squelette Python est donné
- Les `...` portent sur les **expressions mathématiques**
- L'élève ne peut pas juste exécuter sans réfléchir

---

#### C) Code à COMPLÉTER dans les exercices (Notebooks avancés - Première/Terminale)

Pour les **notions mathématiques avancées** où le concept prime sur la syntaxe :
- L'enrobage Python est pré-rempli (imports, compteurs, affichage)
- L'élève doit **adapter le code** au nouveau contexte mathématique
- Objectif : se concentrer sur le raisonnement et l'adaptation

**Philosophie du préremplissage :**

| Ce qu'on pré-remplit | Pourquoi |
|---------------------|----------|
| `import random` | Pas une compétence maths |
| Initialisation des compteurs | Cadrer la structure |
| `print(f"...")` final | Contrainte de sortie |
| Rappel d'outils dans 🛠️ | Connaissance Python non exigible |
| Données/datasets | Fournir le contexte |

**Ce que l'élève doit faire :**
- Adapter la logique vue précédemment au nouveau contexte
- Écrire la boucle et les conditions
- Compléter les formules mathématiques (`...`)

**Utiliser pour :** Suites, probabilités, statistiques, analyse, géométrie vectorielle.

---

**Exemple concret bien équilibré :**

```markdown
### 🎯 À vous de coder !

**Mission :** Estimez la probabilité d'obtenir un **nombre pair** en lançant un dé,
en réalisant **20 000 simulations**.

Affichez la fréquence observée et comparez avec la probabilité théorique (0.5).
```

Cellule de code :

```python
import random

nb_pairs = 0

# Écrivez votre code ici


frequence = ...

# Sortie :
print(f"Fréquence de nombres pairs : {frequence:.4f}")
```

**Analyse de cet exemple :**
- ✅ Import pré-rempli (pas compétence maths)
- ✅ Compteur initialisé (cadre la structure)
- ✅ **PAS d'indice "Outils"** : `randint` a déjà été vu dans l'exemple de cours
- ✅ Sortie formatée imposée (contrainte)
- ✅ L'élève doit écrire la boucle et adapter la condition de parité
- ✅ La `frequence = ...` force l'élève à réfléchir au calcul

**Le compromis :** L'élève n'a pas la solution, mais il a des **contraintes** qui le guident.
Il doit adapter ce qu'il a vu dans l'exemple précédent à ce nouveau contexte.

⚠️ **THINK HARD sur chaque exercice** : Le préremplissage n'est pas arbitraire !
- Ce qui aide l'élève sans lui donner la réponse
- Ce qui le force à réfléchir au bon endroit (la partie maths)
- **Pas d'indice "Outils" si les fonctions ont été vues**

---

**Autre exemple avec dataset pré-rempli :**

```python
# Dataset fourni
temperatures = [12.5, 14.2, 15.8, 13.1, 16.4, 14.9, 15.2, 13.8]

# Calculez la moyenne
moyenne = ...

# Calculez l'écart-type
ecart_type = ...

print(f"Moyenne : {moyenne:.2f}°C")
print(f"Écart-type : {ecart_type:.2f}°C")
```

Ici le dataset est fourni, l'élève se concentre sur les formules statistiques.

---

**Règles pour le code à compléter :**
1. Pré-remplir ce qui n'est **pas** une compétence mathématique
2. Laisser l'élève écrire la **logique centrale** (boucles, conditions)
3. Utiliser `...` pour les **formules** qu'il doit compléter
4. Imposer la **sortie** pour contraindre le format
5. Rappeler les outils Python dans la boîte 🛠️

**La boîte 🛠️ Outils est OPTIONNELLE et minimaliste :**
- Uniquement pour des rappels de **syntaxe non vue** dans ce notebook
- **PAS de liste d'outils** à utiliser (boucle, condition, etc.)

**Exemple TROP guidant (à éviter) :**
```markdown
<details>
<summary>Outils</summary>
- **Simuler deux dés** : `de1 = random.randint(1, 6)` et `de2 = random.randint(1, 6)`
</details>
```

**Mieux : pas d'indice** si `randint` a été vu dans le cours.

L'élève doit **retrouver lui-même** les outils à utiliser en relisant le cours si besoin.

---

### 5. Exercices de synthèse

```markdown
## 🏋️ Exercices de synthèse

Ces exercices mobilisent plusieurs notions vues dans cette activité.

### Exercice 1 : [Titre descriptif]

[Énoncé complet du problème]

*Indice : [Indication si nécessaire]*
```

Cellule vide :

```python
# Écrivez votre code ici
```

```markdown
<details>
<summary>Correction</summary>

```python
# Solution avec commentaires
```

**Explication :** [Détails sur la méthode]
</details>
```

### 6. Séparation exercices optionnels

```markdown
---

<div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107;">
    <strong>📌 À partir d'ici, les exercices sont optionnels.</strong><br>
    Vous pouvez passer au module suivant ou continuer pour vous entraîner davantage.
</div>

---

## 🎯 Exercices supplémentaires (optionnel)

### Exercice A : [Titre]
[...]

### Exercice B : [Titre]
[...]
```

### 7. Challenge final (optionnel)

```markdown
## 🏆 Challenge final

### [Titre du challenge]

[Énoncé élaboré d'un problème complet]

**Indice pour scatter :**
```python
# Exemple de syntaxe utile
```
```

### 8. Synthèse finale

```markdown
## 📚 Synthèse

<div style="background-color: #e8eaf6; padding: 20px; border-radius: 10px; border-left: 5px solid #3f51b5;">

### ✨ Ce que vous avez appris

- ✅ [Point clé 1]
- ✅ [Point clé 2]
- ✅ [Point clé 3]

### 🔑 Points clés à retenir

| Fonction/Syntaxe | Utilité |
|------------------|---------|
| `fonction()` | [Description] |
| `autre()` | [Description] |

⚠️ **Important :** [Point d'attention majeur]

### 🎯 Applications mathématiques

- 📊 [Application 1]
- 📈 [Application 2]
- 🔍 [Application 3]

</div>

---

<div style="background-color: #c8e6c9; padding: 15px; border-radius: 10px; text-align: center;">
    <strong>🎉 Bravo ! Vous avez terminé cette activité !</strong><br>
    [Message de félicitations personnalisé]
</div>
```

## Bonnes pratiques

### Cellules de code

1. **Toujours `plt.clf()` avant matplotlib** pour nettoyer les graphiques précédents
2. **Commentaires explicatifs** dans chaque cellule de code
3. **Cellules vides** avec `# Écrivez votre code ici` pour les exercices
4. **Pas de cellules trop longues** : max 15-20 lignes

### Indices dans les exercices

**RÈGLE IMPORTANTE** : Les indices sont **minimalistes**. L'élève doit chercher !

**Philosophie** : On rappelle uniquement ce qui est **hors programme** ou **syntaxe Python non évidente**.
On ne liste PAS les structures algorithmiques à utiliser (boucle, condition, etc.).

**Ce qu'on peut rappeler** :
- Une fonction Python spécifique (`random.randint(a, b)` si c'est la 1ère fois)
- Le format d'affichage imposé (`f"{x:.4f}"`)
- Un module à importer si inhabituel

**Ce qu'on NE rappelle JAMAIS** :
- Les structures algorithmiques (boucle `for`, `if`, `while`)
- La liste des variables à créer
- L'ordre des étapes
- Les fonctions déjà vues dans le notebook

---

**Exemple MAUVAIS** (trop guidant) :
```markdown
🛠️ **Outils** : boucle `for`, `range()`, `random.randint()`, condition `if`
📦 **Variables** : `succes`, `nombre_simulations`, `frequence`
💡 **Affichage** : `f"{frequence:.4f}"` pour 4 décimales
```

**Exemple BON** (minimaliste) :
```markdown
💡 **Affichage** : `f"{frequence:.4f}"` pour 4 décimales
```

Ou encore mieux, **pas d'indice du tout** si l'exercice est faisable avec les notions vues.

---

**Quand donner un indice ?**

| Situation | Indice ? | Exemple |
|-----------|----------|---------|
| Fonction Python déjà vue | ❌ Non | - |
| Structure algo (for, if) | ❌ Non | - |
| 1ère utilisation d'une fonction | ✅ Oui | `random.randint(1, 6)` |
| Format d'affichage imposé | ✅ Oui | `f"{x:.2f}"` |
| Module spécial à importer | ✅ Oui | `from math import sqrt` |

L'élève doit **réfléchir** aux outils à utiliser, pas les trouver dans l'indice.

### Formulation des exercices d'application

**RÈGLE IMPORTANTE** : Être explicite sur ce que le programme doit produire !

**Problème fréquent** : Énoncé vague qui ne dit pas ce que Python doit afficher.

---

**Exemple MAUVAIS** (trop vague) :
```markdown
A) Estimez la probabilité d'obtenir une somme de 7 en lançant 2 dés.
```

**Exemple BON** (explicite) :
```markdown
A) Écrivez un programme qui **simule 10000 lancers de 2 dés** et **affiche la fréquence**
d'obtention d'une somme égale à 7.
```

---

**Formulations explicites** :
- "Écrivez un programme qui **affiche**..."
- "Le programme doit **renvoyer/calculer/afficher**..."
- "Affichez la fréquence obtenue sous la forme..."

---

### Corrections enrichies

La correction peut contenir des **bonus** que l'élève n'avait pas à faire, mais clairement identifiés :

```python
# === SOLUTION ATTENDUE ===
succes = 0
for i in range(10000):
    de1 = random.randint(1, 6)
    de2 = random.randint(1, 6)
    if de1 + de2 == 7:
        succes += 1

frequence = succes / 10000
print(f"Fréquence observée : {frequence:.4f}")

# === BONUS (non demandé) ===
# Probabilité théorique : 6 combinaisons sur 36 = 1/6 ≈ 0.1667
# Combinaisons : (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
proba_theorique = 6/36
print(f"Probabilité théorique : {proba_theorique:.4f}")
```

**Balises à utiliser dans les corrections** :
- `# === SOLUTION ATTENDUE ===` : Ce que l'élève devait écrire
- `# === BONUS (non demandé) ===` : Enrichissements optionnels

### Markdown

1. **Émojis** dans les titres markdown (h2, h3) :
   - 📚 Notion/Cours
   - 📖 Explication théorique
   - ✅ QCM/Vérification
   - 🔍 Comprendre
   - 🏋️ Synthèse
   - 🎯 Supplémentaire
   - 🏆 Challenge
   - ⚠️ Attention

   ⚠️ **ATTENTION : Typage correct des cellules** !
   Les cellules contenant des balises HTML (`<details>`, `<summary>`) doivent être de type **markdown**, pas code !

   Si une cellule de correction est typée "code" au lieu de "markdown", Python essaiera d'interpréter
   le HTML comme du code Python → `SyntaxError: invalid character`.

   **Symptôme typique :**
   ```
   SyntaxError: invalid character '💡' (U+1F4A1)
     <summary>💡 Correction</summary>
   ```

   **Cause réelle :** La cellule est typée "code" au lieu de "markdown".
   **Solution :** Changer le type de cellule en markdown (les emojis sont OK en markdown).

   **Vérification :** S'assurer que toutes les cellules avec `<details>` sont bien en markdown.

2. **Séparateurs** : `---` entre les sections majeures

3. **Balises `<details>`** pour toutes les corrections

### Structure pédagogique

1. **Progression** : Du simple vers le complexe
2. **QCM** : 3 questions par notion, tester syntaxe + comportement + compréhension
3. **Exercices** :
   - D'abord comprendre un programme existant
   - Puis compléter du code
   - Puis écrire du code complet
4. **Boîte outils** : Rappeler les prérequis externes avant les exercices complexes

## Niveaux et thèmes

### Seconde
- Calculs et variables
- Conditions (if/else)
- Boucles (for/range)
- Fonctions (def/return)
- Listes
- Aléatoire (random)
- Graphiques (matplotlib)
- Algorithmes de recherche

### Première
- Boucle while (seuil)
- Suites et récurrence
- Taux d'accroissement
- Variations de fonction
- Statistiques descriptives
- Probabilités et simulations

### Terminale
- Méthodes numériques
- Équations différentielles
- Méthode de Monte-Carlo
- Approximations

## Workflow de création

1. **Identifier le niveau et le thème**
2. **Lister les notions à couvrir** (autant que nécessaire, pas de minimum)
3. **Pour chaque notion** :
   - Rédiger le cours avec syntaxe
   - Créer l'exemple actif (formules à compléter)
   - Écrire 3 questions QCM avec distracteurs plausibles
   - Concevoir exercice de compréhension
   - Concevoir exercice d'application (préremplissage réfléchi)
4. **Ajouter boîte outils** si notions externes nécessaires
5. **Créer exercices de synthèse** (2-3)
6. **Ajouter exercices optionnels et challenge**
7. **Rédiger la synthèse finale**
8. **⚠️ ÉTAPE AUTO-RÉFLEXIVE : Vérifier l'indépendance des unités**
   - Relire chaque correction : donne-t-elle la réponse d'un exercice suivant ?
   - Relire chaque exemple de cours : spoile-t-il un exercice ?
   - S'assurer que chaque exercice peut être résolu **sans avoir lu les corrections précédentes**
   - Les exercices doivent être des **unités indépendantes** (pas de dépendance cachée)
   - **Éviter les recoupements numériques** : si un exercice utilise des dés (6 faces),
     ne pas utiliser 6 dans l'exercice suivant (collectionneur → 24 figurines, pas 6)
   - **On est en info, on peut être ambitieux !** Les nombres peuvent être grands (20000 simulations,
     32 figurines, etc.). Ça montre la puissance du calcul et évite les confusions.
   - **Limite pratique : 100 000 simulations max** (ordinateurs de la région). Au-delà, ça rame.

9. **🔍 VALIDATION TECHNIQUE : Vérifier le rendu et la syntaxe**
   - **Ouvrir le notebook dans JupyterLab** et vérifier le rendu visuel des cellules markdown
   - **Exécuter toutes les cellules de code** (Kernel → Restart & Run All) pour détecter les erreurs
   - **Vérifier les balises HTML** : `<details>`, `<summary>`, `<div>` bien fermées
   - **Tester les `<details>`** : cliquer pour vérifier qu'ils se déplient correctement
   - **Pas d'emojis dans `<summary>`** : vérifier qu'aucun emoji ne cause de SyntaxError
   - **Commande de validation JSON** (optionnel) :
     ```bash
     python -m json.tool notebook.ipynb > /dev/null && echo "JSON valide"
     ```
   - **Nbval pour tester l'exécution** (optionnel) :
     ```bash
     pip install nbval
     pytest --nbval notebook.ipynb
     ```

## Validation

Avant de finaliser un notebook :

- [ ] Toutes les cellules de code sont exécutables
- [ ] Les corrections sont dans des `<details>`
- [ ] Les QCM ont exactement 3 questions
- [ ] Les exercices ont des indices si nécessaire
- [ ] La boîte outils est présente pour les exercices complexes
- [ ] La progression est logique
- [ ] Les émojis sont cohérents
- [ ] L'en-tête est complète (niveau, durée, objectifs)
