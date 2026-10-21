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

## Fichiers de référence (à lire au moment utile)

| Fichier | Quand le lire |
|---------|---------------|
| `references/gabarits-cellules.md` | Pour rédiger les cellules : en-tête, notion (cours, exemple, QCM, exercices), boîte Outils, synthèse, optionnels, challenge, synthèse finale |
| `references/code-complet-ou-completion.md` | Pour décider ce que l'élève écrit lui-même (code complet, exemple actif, code à compléter) et ce qu'on préremplit |
| `references/template_notebook.json` | Squelette `.ipynb` complet à copier comme point de départ |

## Outils de navigation (notebook_tools.py)

Script Python pour naviguer et valider les notebooks **avant** de les modifier.

**Localisation :** `.claude/skills/jupyter-notebook/notebook_tools.py` (chemin relatif à la racine du projet ; à adapter si le skill est installé ailleurs, par exemple `~/.claude/skills/jupyter-notebook/notebook_tools.py`).

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

## Protocole pédagogique : plan d'un notebook

Les gabarits détaillés de chaque partie sont dans `references/gabarits-cellules.md`.

1. **En-tête** : titre, niveau, thème, durée estimée, objectifs, prérequis, introduction (problème / solution).
2. **Notions** (autant que nécessaire). Pour CHAQUE notion, dans cet ordre : cours (syntaxe, règles, tableau) ; cellule de code d'exemple exécutable ; QCM de vérification de 3 questions avec correction dépliante ; exercice de compréhension d'un programme ; exercice d'application (compléter, puis écrire).
3. **Boîte « Outils » dépliante (RARE)** : uniquement pour rappeler des notions d'AUTRES notebooks, jamais ce qui est dans le cours du notebook actuel.
4. **Approche selon le niveau** (code complet / exemple actif / code à compléter) : voir `references/code-complet-ou-completion.md`.
5. **Exercices de synthèse** mobilisant plusieurs notions.
6. **Exercices optionnels** après un séparateur explicite, puis **challenge final** facultatif.
7. **Synthèse finale** : ce qui a été appris, points clés, applications mathématiques, message de félicitations.

## Bonnes pratiques

### Cellules de code

1. **Toujours `plt.clf()` avant matplotlib** pour nettoyer les graphiques précédents
2. **Commentaires explicatifs** dans chaque cellule de code
3. **Cellules vides** avec `# Écrivez votre code ici` pour les exercices
4. **Pas de cellules trop longues** : max 15-20 lignes

### Cellule utilitaire : ne jamais divulguer l'exercice d'au-dessus

Une cellule « de vérification » placée après un exercice ne doit **pas** en
contenir la solution. Le piège est facile : pour montrer comment afficher un
type, on recopie le programme complet de l'exercice précédent, et l'élève lit
la réponse juste sous la question.

Relire tout carnet **dans l'ordre**, en se demandant à chaque cellule ce
qu'elle révèle de ce qui précède. Une cellule utilitaire ne porte qu'un
commentaire de consigne (`# À toi : afficher le type de A`) et s'appuie sur les
variables que l'élève a créées lui-même — les cellules partagent leur état.

### Alternance stricte consigne → programme

Une consigne, un programme, la consigne suivante, le programme suivant. Jamais
un bloc de toutes les consignes suivi d'un bloc de toutes les cellules :
l'élève doit pouvoir descendre le carnet sans jamais remonter. Quand une fiche
source pose deux algorithmes côte à côte, le carnet en fait deux séquences
successives.

### Zone de réponse : une cellule markdown, et rien de plus

La zone où l'élève note sa réponse est **une cellule markdown** qu'il
double-clique pour écrire. Son contenu est du source, donc il est conservé
quand l'élève sauvegarde ; il s'édite dans CodeMirror, donc les raccourcis du
mode commande ne le mangent pas. **Aucun HTML dedans** : c'est ce source que
l'élève voit au double-clic, et un empilement de balises l'empêcherait de
trouver où écrire. Le bloc de citation `>` suffit à faire un cadre au rendu.

```markdown
> **Ta réponse** — double-clique dans ce cadre pour écrire, puis `Maj` + `Entrée`.
>
> **Le programme affiche à la fin :** ......................
>
> **A est une variable Python de type :** ......................
```

Un exercice tient alors en trois cellules, toujours les mêmes : la consigne
(markdown), le programme (code, avec le seul squelette donné par l'énoncé), la
réponse (markdown). Plus le volet vert de correction.

**Ne jamais faire taper le programme deux fois.** Là où une fiche papier met un
cadre « Python » à compléter au crayon, le carnet met une flèche vers la
cellule de code : c'est le seul endroit où le programme peut tourner. La
cellule de réponse ne recueille que ce qui n'est pas du code — une valeur
affichée, un type, une observation.

#### Deux dispositifs à ne pas réintroduire

**Des champs `<input>` dans une cellule markdown : impossible.** Deux raisons
indépendantes, chacune suffisante.

- *Rien n'est enregistré.* Un `.ipynb` ne stocke que le source des cellules ;
  l'état du DOM d'une sortie rendue n'en fait pas partie, et une cellule
  markdown n'a même pas de sortie stockée. Sauvegarder perd tout. **Vérifier la
  contrainte de persistance AVANT de choisir un dispositif de saisie.**
- *La saisie est impossible.* Cliquer dans un champ ne sort pas le carnet du
  mode commande : chaque lettre est lue comme un raccourci (`f` rechercher,
  `a` insérer une cellule, `i` interrompre, `dd` supprimer, `Entrée` repasse la
  cellule en édition et efface les champs). Le mot « float » ne peut pas
  s'écrire. Et le correctif JavaScript qui neutraliserait ces raccourcis ne
  tourne pas : **Jupyter et Basthon retirent les `<script>` des cellules
  markdown** depuis la v5. Corollaire de méthode : un essai de ce correctif
  dans une page HTML fabriquée pour l'occasion conclut à tort qu'il fonctionne,
  puisque rien n'y est assaini. **Éprouver un correctif dans l'environnement
  cible, pas dans une maquette.**

**Une cellule d'installation plus un `verifier(...)` par exercice : trop
lourd.** Techniquement cela marche (réponses jugées à la volée, bonnes réponses
rangées en empreintes sha256 pour rester illisibles), mais c'est de la
machinerie qui compense une contrainte au lieu de supprimer le besoin : une
cellule à exécuter au début, un appel de fonction à laisser intact après chaque
exercice, deux sources d'erreur pour une classe de lycée. Le point à retenir :
**dans un carnet, exécuter le programme est déjà la vérification.** Les
pointillés d'une fiche papier n'existent que parce que le papier ne sait pas
exécuter.


### Styles en ligne, et une seule colonne

Écrire les styles **dans l'attribut `style`** de chaque élément, pas seulement
dans un bloc `<style>` de la première cellule : nbviewer et GitHub retirent les
`<style>` des cellules markdown, et la mise en page doit survivre à ce
nettoyage. Le bloc `<style>` ne porte que l'agrément.

Rester **à une colonne** presque partout. Les rangées `display:flex` tiennent
dans un aperçu large et se cassent dans la largeur réelle d'une cellule
Jupyter. Seuls les vrais `<table>` restent en colonnes, dans un conteneur
`overflow-x:auto`. Relire le rendu à **deux largeurs** (900 px, la largeur
utile d'une cellule sur un portable de lycée, et 1200 px) : un défaut de mise
en page ne se voit jamais à la même.

### Document élève, pas document prof

Quand la source est une fiche de professeur, elle contient des passages qui ne
sont pas adressés à l'élève : commentaires de conduite de séance, notes
d'intention, enthousiasme pour un outil. Les écarter, même quand la demande
est de « retranscrire exactement » — la fidélité s'entend sur le contenu
pédagogique, pas sur le hors-champ.

De même, les consignes de navigation vers un site externe n'ont plus d'objet
quand le carnet est ouvert dans ce site : dans un carnet destiné à Basthon, on
n'écrit pas « tester ce programme dans Basthon », on écrit « exécute ».

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
**Outils** : boucle `for`, `range()`, `random.randint()`, condition `if`
**Variables** : `succes`, `nombre_simulations`, `frequence`
**Affichage** : `f"{frequence:.4f}"` pour 4 décimales
```

**Exemple BON** (minimaliste) :
```markdown
**Affichage** : `f"{frequence:.4f}"` pour 4 décimales
```

Ou encore mieux, **pas d'indice du tout** si l'exercice est faisable avec les notions vues.

---

**Quand donner un indice ?**

| Situation | Indice ? | Exemple |
|-----------|----------|---------|
| Fonction Python déjà vue | Non | - |
| Structure algo (for, if) | Non | - |
| 1ère utilisation d'une fonction | Oui | `random.randint(1, 6)` |
| Format d'affichage imposé | Oui | `f"{x:.2f}"` |
| Module spécial à importer | Oui | `from math import sqrt` |

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

1. **Titres sans emoji par défaut** (voir « Emojis » ci-dessous).

   **Typage correct des cellules** : les cellules contenant des balises HTML (`<details>`, `<summary>`) doivent être de type **markdown**, pas code !

   Si une cellule de correction est typée "code" au lieu de "markdown", Python essaiera d'interpréter
   le HTML comme du code Python → `SyntaxError: invalid character`.

   **Symptôme typique :**
   ```
   SyntaxError: invalid character (U+...)
     <summary>Correction</summary>
   ```

   **Cause réelle :** La cellule est typée "code" au lieu de "markdown".
   **Solution :** Changer le type de cellule en markdown.

   **Vérification :** S'assurer que toutes les cellules avec `<details>` sont bien en markdown.

2. **Séparateurs** : `---` entre les sections majeures

3. **Balises `<details>`** pour toutes les corrections

### Emojis (option désactivée par défaut)

Par défaut, les titres de sections sont écrits **sans emoji** (c'est le cas dans tous les gabarits). Les emojis ne sont ajoutés que si l'utilisateur les demande explicitement. Dans ce cas, préfixer uniquement les titres h2/h3, avec cette table :

| Section | Emoji |
|---------|-------|
| Notion / Cours | 📚 |
| Explication théorique | 📖 |
| QCM / Vérification | ✅ |
| Comprendre un programme | 🔍 |
| Synthèse | 🏋️ |
| Supplémentaire | 🎯 |
| Challenge | 🏆 |
| Attention | ⚠️ |

Garder les emojis hors des balises `<summary>` et hors des cellules de code, et rester cohérent dans tout le notebook.

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
8. **ÉTAPE AUTO-RÉFLEXIVE : vérifier l'indépendance des unités**
   - Relire chaque correction : donne-t-elle la réponse d'un exercice suivant ?
   - Relire chaque exemple de cours : spoile-t-il un exercice ?
   - S'assurer que chaque exercice peut être résolu **sans avoir lu les corrections précédentes**
   - Les exercices doivent être des **unités indépendantes** (pas de dépendance cachée)
   - **Éviter les recoupements numériques** : si un exercice utilise des dés (6 faces),
     ne pas utiliser 6 dans l'exercice suivant (collectionneur → 24 figurines, pas 6)
   - **On est en info, on peut être ambitieux !** Les nombres peuvent être grands (20000 simulations,
     32 figurines, etc.). Ça montre la puissance du calcul et évite les confusions.
   - **Limite pratique : 100 000 simulations max** (ordinateurs des élèves, au-delà ça rame).

9. **VALIDATION TECHNIQUE : vérifier le rendu et la syntaxe**
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
- [ ] Les titres sont cohérents (avec ou sans emojis, selon l'option choisie)
- [ ] L'en-tête est complète (niveau, durée, objectifs)
