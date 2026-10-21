# Code complet ou code à compléter : choisir selon le niveau

Deux approches pédagogiques selon le niveau et la notion.

## A) Code COMPLET (notebooks de base, Seconde principalement)

Pour les **notions fondamentales** où l'élève apprend la syntaxe Python :
- l'élève écrit **tout le code** dans une cellule vide ;
- on fournit uniquement des indices (briques, variables) ;
- objectif : maîtriser la syntaxe Python.

```python
# Écrivez votre code ici
```

**Utiliser pour :** variables, conditions, boucles for, fonctions de base, listes.

## B) Exemples de COURS actifs (notebooks avancés)

**Principe fondamental :** même dans les exemples de cours, l'élève doit être **actif**.

Dans les exemples qui illustrent une notion :
- la quasi-totalité du code est implémentée (structure, boucles, affichage) ;
- l'élève complète **uniquement les formules mathématiques** (`...`) ;
- objectif : forcer l'élève à suivre et comprendre, pas à recopier passivement.

**Avant (passif) :**
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

**Après (actif) :**
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
- l'élève doit réfléchir à `somme = de1 + de2` ;
- l'élève doit comprendre l'incrémentation `nb_somme_10 + 1` ;
- l'élève doit calculer la fréquence `nb_somme_10 / nb_simulations`.

**Règle générale pour les exemples de cours :**
- tout le squelette Python est donné ;
- les `...` portent sur les **expressions mathématiques** ;
- l'élève ne peut pas juste exécuter sans réfléchir.

## C) Code à COMPLÉTER dans les exercices (notebooks avancés, Première/Terminale)

Pour les **notions mathématiques avancées** où le concept prime sur la syntaxe :
- l'enrobage Python est pré-rempli (imports, compteurs, affichage) ;
- l'élève doit **adapter le code** au nouveau contexte mathématique ;
- objectif : se concentrer sur le raisonnement et l'adaptation.

**Philosophie du préremplissage :**

| Ce qu'on pré-remplit | Pourquoi |
|---------------------|----------|
| `import random` | Pas une compétence maths |
| Initialisation des compteurs | Cadrer la structure |
| `print(f"...")` final | Contrainte de sortie |
| Rappel d'outils (si nécessaire) | Connaissance Python non exigible |
| Données/datasets | Fournir le contexte |

**Ce que l'élève doit faire :**
- adapter la logique vue précédemment au nouveau contexte ;
- écrire la boucle et les conditions ;
- compléter les formules mathématiques (`...`).

**Utiliser pour :** suites, probabilités, statistiques, analyse, géométrie vectorielle.

### Exemple concret bien équilibré

Cellule markdown :

````markdown
### À vous de coder !

**Mission :** Estimez la probabilité d'obtenir un **nombre pair** en lançant un dé,
en réalisant **20 000 simulations**.

Affichez la fréquence observée et comparez avec la probabilité théorique (0.5).
````

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
- import pré-rempli (pas une compétence maths) ;
- compteur initialisé (cadre la structure) ;
- **pas d'indice « Outils »** : `randint` a déjà été vu dans l'exemple de cours ;
- sortie formatée imposée (contrainte) ;
- l'élève doit écrire la boucle et adapter la condition de parité ;
- la ligne `frequence = ...` force l'élève à réfléchir au calcul.

**Le compromis :** l'élève n'a pas la solution, mais il a des **contraintes** qui le guident. Il doit adapter ce qu'il a vu dans l'exemple précédent à ce nouveau contexte.

**Réfléchir à fond sur chaque exercice** : le préremplissage n'est pas arbitraire.
- Ce qui aide l'élève sans lui donner la réponse.
- Ce qui le force à réfléchir au bon endroit (la partie maths).
- **Pas d'indice « Outils » si les fonctions ont été vues.**

### Autre exemple avec dataset pré-rempli

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

### Règles pour le code à compléter

1. Pré-remplir ce qui n'est **pas** une compétence mathématique.
2. Laisser l'élève écrire la **logique centrale** (boucles, conditions).
3. Utiliser `...` pour les **formules** qu'il doit compléter.
4. Imposer la **sortie** pour contraindre le format.
5. Rappeler les outils Python dans la boîte « Outils » seulement si nécessaire (voir les règles d'indices du `SKILL.md`).

**La boîte « Outils » est OPTIONNELLE et minimaliste :**
- uniquement pour des rappels de **syntaxe non vue** dans ce notebook ;
- **PAS de liste d'outils** à utiliser (boucle, condition, etc.).

**Exemple TROP guidant (à éviter) :**
````markdown
<details>
<summary>Outils</summary>
- **Simuler deux dés** : `de1 = random.randint(1, 6)` et `de2 = random.randint(1, 6)`
</details>
````

**Mieux : pas d'indice** si `randint` a été vu dans le cours. L'élève doit **retrouver lui-même** les outils à utiliser en relisant le cours si besoin.
