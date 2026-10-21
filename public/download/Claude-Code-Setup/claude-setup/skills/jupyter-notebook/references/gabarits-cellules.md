# Gabarits de cellules d'un notebook pédagogique

Gabarits à copier et adapter, dans l'ordre d'un notebook. Les titres sont écrits **sans emoji** (voir la section « Emojis » du `SKILL.md`). Si l'option emojis est activée, préfixer les titres h2/h3 selon la table du `SKILL.md`.

Les blocs ci-dessous sont encadrés par quatre apostrophes inverses pour pouvoir contenir des blocs de code Python.

## 1. En-tête du notebook

````markdown
# Titre du notebook

<div style="background-color: #e3f2fd; padding: 15px; border-radius: 10px; border-left: 5px solid #2196F3;">
    <strong>Niveau :</strong> [Seconde/Première/Terminale]<br>
    <strong>Thème :</strong> [Thème mathématique]<br>
    <strong>Durée estimée :</strong> [XX min]
</div>

---

## Objectifs

À la fin de cette activité, vous serez capable de :
- Objectif 1
- Objectif 2
- Objectif 3

---

## Prérequis

<div style="background-color: #fff3cd; padding: 10px; border-radius: 5px;">
Pour cette activité, vous devez savoir :

- Prérequis 1
- Prérequis 2
</div>

---

## Introduction

[Contexte et motivation pour cette notion]

<div style="background-color: #f0f4c3; padding: 10px; border-radius: 5px; margin: 10px 0;">
    <strong>Problème :</strong> [Problème que résout cette notion]<br>
    <strong>Solution :</strong> [Ce que Python permet de faire]
</div>

---
````

## 2. Structure d'une notion

Pour CHAQUE notion du notebook, suivre cette structure.

Cellule markdown du cours :

````markdown
## Notion X : [Titre de la notion]

### Cours

[Explication théorique avec syntaxe et règles]

**Syntaxe :**
```python
# Format général
```

| Élément | Description | Exemple |
|---------|-------------|---------|
| ... | ... | ... |

**Exemple résolu :**
````

Puis une **cellule de code** avec l'exemple exécutable :

```python
# Exemple commenté
resultat = calcul()
print(resultat)
```

Puis le **QCM de vérification** (cellule markdown) :

````markdown
### Vérification : QCM

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
<summary>Correction</summary>

**Question 1 :** [Lettre]) [Réponse]
**Explication :** [Justification]

**Question 2 :** [Lettre]) [Réponse]
**Explication :** [Justification]

**Question 3 :** [Lettre]) [Réponse]
**Explication :** [Justification]
</details>
````

Puis **l'exercice de compréhension** (cellule markdown) :

````markdown
### Exercice 1 : Comprendre un programme

Que fait le programme suivant ?
````

Cellule de code à analyser :

```python
# Programme à comprendre
x = [1, 2, 3]
for i in x:
    print(i * 2)
```

Cellule markdown de correction :

````markdown
<details>
<summary>Correction</summary>

Ce programme [explication détaillée].
</details>
````

Puis **l'exercice d'application** (cellule markdown) :

````markdown
### Exercice 2 : Application

#### A) Compléter le code suivant
````

Cellule de code à compléter :

```python
# Description de ce qu'il faut faire
x = 5
y = ...  # Complétez
```

Cellule markdown :

````markdown
#### B) [Exercice plus libre]

*Indice : [Indication utile]*
````

Cellule vide pour l'élève :

```python
# Écrivez votre code ici
```

Cellule markdown de corrections :

````markdown
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
````

## 3. Boîte « Outils » dépliante (RARE)

**Uniquement pour rappeler des notions d'AUTRES notebooks** (pas du notebook actuel).

````markdown
<details>
<summary><strong>Rappel - Notion vue dans un autre module</strong></summary>

`fonction(parametre)` — vu dans : [Nom du notebook source]
</details>
````

Quand l'utiliser :
- quand une notion d'un **autre** notebook est nécessaire ;
- **JAMAIS** pour rappeler ce qui est dans le cours du notebook actuel.

## 4. Exercices de synthèse

````markdown
## Exercices de synthèse

Ces exercices mobilisent plusieurs notions vues dans cette activité.

### Exercice 1 : [Titre descriptif]

[Énoncé complet du problème]

*Indice : [Indication si nécessaire]*
````

Cellule vide :

```python
# Écrivez votre code ici
```

Cellule markdown de correction :

````markdown
<details>
<summary>Correction</summary>

```python
# Solution avec commentaires
```

**Explication :** [Détails sur la méthode]
</details>
````

## 5. Séparation des exercices optionnels

````markdown
---

<div style="background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107;">
    <strong>À partir d'ici, les exercices sont optionnels.</strong><br>
    Vous pouvez passer au module suivant ou continuer pour vous entraîner davantage.
</div>

---

## Exercices supplémentaires (optionnel)

### Exercice A : [Titre]
[...]

### Exercice B : [Titre]
[...]
````

## 6. Challenge final (optionnel)

````markdown
## Challenge final

### [Titre du challenge]

[Énoncé élaboré d'un problème complet]

**Indice pour scatter :**
```python
# Exemple de syntaxe utile
```
````

## 7. Synthèse finale

````markdown
## Synthèse

<div style="background-color: #e8eaf6; padding: 20px; border-radius: 10px; border-left: 5px solid #3f51b5;">

### Ce que vous avez appris

- [Point clé 1]
- [Point clé 2]
- [Point clé 3]

### Points clés à retenir

| Fonction/Syntaxe | Utilité |
|------------------|---------|
| `fonction()` | [Description] |
| `autre()` | [Description] |

**Important :** [Point d'attention majeur]

### Applications mathématiques

- [Application 1]
- [Application 2]
- [Application 3]

</div>

---

<div style="background-color: #c8e6c9; padding: 15px; border-radius: 10px; text-align: center;">
    <strong>Bravo ! Vous avez terminé cette activité !</strong><br>
    [Message de félicitations personnalisé]
</div>
````
