# /makePythonEval - Génération d'évaluations Python pour le lycée

## Description

Génère automatiquement un sujet d'évaluation Python (15-20 min) pour vérifier la compréhension des élèves après un ou plusieurs notebooks Jupyter. L'évaluation suit une structure fixe en 3 exercices, adaptée à un contrôle rapide de connaissances en informatique.

## Usage

```
/makePythonEval <notebook(s)_source> [--duree <minutes>] [--niveau <2nde|1ere|Tle>]
```

## Paramètres

- `<notebook(s)_source>` : Chemins vers un ou plusieurs notebooks Jupyter (.ipynb)
- `--duree <minutes>` : Durée de l'évaluation (défaut: 15 minutes)
- `--niveau <niveau>` : Niveau scolaire (défaut: détecté depuis le nom du notebook)

## Exemples

```bash
/makePythonEval "notebooks/seconde_calculs_decouverte_python.ipynb"
/makePythonEval "notebooks/seconde_boucles_for_range.ipynb" "notebooks/seconde_calculs_decouverte_python.ipynb" --duree 20
/makePythonEval "notebooks/premiere_suites_recurrence.ipynb" --niveau 1ere
```

---

## STRUCTURE OBLIGATOIRE DE L'ÉVALUATION PYTHON

### Format fixe : 3 exercices

```
┌─────────────────────────────────────────────────────────────────────┐
│ Exercice 1 : Analyse d'algorithme (6 points)                        │
│─────────────────────────────────────────────────────────────────────│
│ MISE EN PAGE : minipage 65% (exercice) + 33% (code Python)          │
│ On donne un programme Python court (5-10 lignes)                    │
│ Questions :                                                         │
│   a) Que fait ce programme ? (2 pts)                                │
│   b) Quel est le résultat affiché ? (3 pts)                         │
│   c) Que se passe-t-il si on change X ? (1 pt)                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Exercice 2 : Construction de programme (8 points)                   │
│─────────────────────────────────────────────────────────────────────│
│ L'élève doit écrire un programme complet                            │
│ Indications claires sur les éléments à utiliser                     │
│ CORRECTION : Code solution affiché à côté avec minipage             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│ Exercice 3 : Identification d'erreurs (6 points)                    │
│─────────────────────────────────────────────────────────────────────│
│ MISE EN PAGE : multicols{3} pour les 3 programmes                   │
│ 3 programmes proposés (A, B, C) pour un même problème               │
│   - Un correct                                                       │
│   - Un avec erreur de syntaxe                                        │
│   - Un avec erreur de logique                                        │
└─────────────────────────────────────────────────────────────────────┘
```

---

## RÈGLES CRITIQUES DE MISE EN PAGE

### 1. Environnement CodePythonLst - TOUJOURS EN DEHORS DES EXO

**JAMAIS** de code Python à l'intérieur d'un environnement `EXO` (conflits tcolorbox).

**Syntaxe** :
- `\begin{CodePythonLst}{title=Titre}` : avec numéros de lignes
- `\begin{CodePythonLst}*{title=Titre}` : sans numéros de lignes (version étoilée)

### 2. Exercice 1 : minipage côte à côte

```latex
\begin{minipage}{0.65\textwidth}
    \def\rdifficulty{1.5}
    \begin{EXO}{Analyser un programme Python}{INFO-ANALYSE}
    On considère le programme Python ci-dessous.

    \begin{tcbenumerate}[1]
    \tcbitem \tcbitempoint{2}\acc{Décrire} en une phrase ce que fait ce programme.
    \tcbitem \tcbitempoint{3}\acc{Donner} la valeur affichée par ce programme.
    \tcbitem \tcbitempoint{1}Si on remplace \texttt{range(1, 6)} par \texttt{range(1, 4)},
    quelle serait la nouvelle valeur affichée ?
    \end{tcbenumerate}

    \exocorrection

    \begin{tcbenumerate}[1]
    \tcbitem Ce programme calcule la somme des entiers de 1 à 5.
    \tcbitem Détail des étapes...
    \encadrer[defi]{Le programme affiche \texttt{15}}.
    \tcbitem Avec \texttt{range(1, 4)}, le programme afficherait \texttt{6}.
    \end{tcbenumerate}

    \end{EXO}
\end{minipage}
\begin{minipage}{0.33\textwidth}
    \begin{center}
    \begin{CodePythonLst}{title=Programme à analyser}
total = 0
for i in range(1, 6):
    total = total + i
print(total)
    \end{CodePythonLst}
    \end{center}
\end{minipage}
```

### 3. Exercice 2 : énoncé simple

```latex
\def\rdifficulty{2}
\begin{EXO}{Écrire un programme Python}{INFO-ECRIRE}

\tcbitempoint{8}On souhaite écrire un programme qui \acc{affiche les carrés des nombres de 1 à 5}.

\acc{Écrire} ce programme en utilisant :
\begin{itemize}
\item une boucle \texttt{for} avec \texttt{range}
\item l'opérateur puissance \texttt{**}
\item la fonction \texttt{print()}
\end{itemize}

\exocorrection

\textbf{Explications :}
\begin{itemize}
\item \texttt{range(1, 6)} génère les nombres 1, 2, 3, 4, 5
\item \texttt{i ** 2} calcule le carré de \texttt{i}
\item \texttt{print()} affiche le résultat à chaque tour de boucle
\end{itemize}

\end{EXO}
```

### 4. Exercice 3 : multicols pour les 3 programmes

```latex
\def\rdifficulty{1.5}
\begin{EXO}{Identifier les erreurs}{INFO-DEBUG}

On souhaite écrire un programme qui \acc{calcule et affiche la somme des nombres pairs de 2 à 10}.

Parmi les trois programmes proposés ci-dessous. \acc{Un seul est correct}.

\begin{tcbenumerate}[1]
\tcbitem \tcbitempoint{2}\acc{Identifier} le programme qui fonctionne \acc{sans déclencher d'erreur}.

Pour chaque programme comportant une erreur, \acc{justifier} en expliquant \acc{quelle ligne} comporte une erreur, et \acc{quelle est cette erreur}.
\end{tcbenumerate}

\exocorrection

\begin{tcbenumerate}[1]
\tcbitem Le \textbf{Programme A} contient une \acc{erreur de syntaxe} : il manque les deux-points \texttt{:}...
\tcbitem Le \textbf{Programme B} est correct car...
\tcbitem Le \textbf{Programme C} \acc{n'affiche rien} car il n'y a pas d'instruction \texttt{print()}.
\end{tcbenumerate}

\end{EXO}

% CODES PYTHON - APRÈS l'exercice
\begin{multicols}{3}

\begin{CodePythonLst}*{title=Programme A}
somme = 0
for i in range(2, 11, 2)
    somme = somme + i
print(somme)
\end{CodePythonLst}

\columnbreak

\begin{CodePythonLst}*{title=Programme B}
somme = 0
for i in range(2, 11, 2):
    somme = somme + i
print(somme)
\end{CodePythonLst}

\columnbreak

\begin{CodePythonLst}*{title=Programme C}
somme = 0
for i in range(2, 11, 2):
    somme = somme + i
\end{CodePythonLst}

\end{multicols}
```

---

## FICHIER PRINCIPAL : STRUCTURE DE CORRECTION

Le fichier principal doit inclure une page de correction avec `\rdexocorrection{n}`.

**Structure du fichier principal après `\input{enonce}` :**

```latex
\input{enonce}%

\newpage
\setcounter{pagecounter}{0}
\setcounter{ExoMA}{0}

\chapitre[
    $\mathbf{2^{\text{nde}}}$%
    ]{
    Python - Découverte et Boucles%
    }{
    Lycée%
    }{
    Camille Claudel%
    }{
    %
    }{
    Solutions :
    }
\setrdcrep{seyes, correction=true, correction color=monrose, correction font = \large\bfseries}
\tcbset{
    rdexo/default/.cd,correction style/.style={
        before upper=%
        \textbf{\thelabel~
        \thecorrectionnum~:~}
    }
}

\rdexocorrection{1}

\begin{minipage}{0.6\textwidth}
\rdexocorrection{2}
\end{minipage}
\hfill
\begin{minipage}{0.33\textwidth}
\begin{center}
    \begin{CodePythonLst}*{title=Solution}
for i in range(1, 6):
    print(i ** 2)
    \end{CodePythonLst}
\end{center}
\end{minipage}

\rdexocorrection{3}
```

**Points clés :**
- `\rdexocorrection{n}` affiche la correction de l'exercice n
- Pour l'exercice 2, le code solution est dans une `minipage` à côté
- Utiliser `CodePythonLst*` (sans numéros) pour les solutions

---

## PROTOCOLE D'EXÉCUTION

### ÉTAPE 1 : ANALYSE DES NOTEBOOKS SOURCES

1. **Lire intégralement les notebooks fournis**
2. **Extraire les notions enseignées** :
   - Opérateurs (`+`, `-`, `*`, `/`, `**`, `//`, `%`)
   - Variables et affectation
   - `print()` et guillemets
   - `range()` et boucles `for`
   - Variables accumulatrices (somme, produit)
   - Listes (si abordées)
   - Fonctions intégrées (`abs()`, `round()`, etc.)

3. **Identifier le niveau de difficulté** adapté aux élèves

### ÉTAPE 2 : CONCEPTION DES EXERCICES

#### Exercice 1 : Analyse d'algorithme

**Concevoir un programme de 5-10 lignes** qui :
- Utilise les notions vues dans les notebooks
- A un résultat prévisible par simulation manuelle
- N'est ni trivial ni trop complexe

**Types de programmes adaptés** :
- Calcul avec variables et opérations
- Boucle `for` avec compteur ou accumulateur
- Combinaison variables + boucle

#### Exercice 2 : Construction de programme

**Choisir une tâche** parmi :
- Calculer une somme/produit avec une boucle
- Afficher une séquence de valeurs
- Utiliser des variables pour un calcul mathématique
- Application de la division euclidienne

**Donner des indications claires** (sans donner la solution) :
- "Vous utiliserez une boucle `for`"
- "Pensez à initialiser une variable pour stocker le résultat"

#### Exercice 3 : Identification d'erreurs

**Créer 3 versions d'un même programme** :
1. **Version correcte** : Fonctionne parfaitement
2. **Version avec erreur de syntaxe** :
   - Deux-points `:` manquant après `for` ou `if`
   - Mauvaise indentation
   - Parenthèse manquante dans `print()`
3. **Version avec erreur de logique** :
   - Oubli du `print()` donc pas d'affichage
   - Mauvaise borne dans `range()`
   - Variable non mise à jour

### ÉTAPE 3 : CRÉATION DU PROJET LATEX

1. **Utiliser le skill `tex-document-creator`** :
   - Type de document : `Devoir`
   - Niveau : celui détecté ou spécifié
   - Thème : `Python - [Notions abordées]`

2. **Modifier le fichier principal** pour ajouter la structure de correction

### ÉTAPE 4 : RÉDACTION

1. **Charger le skill `bfcours-latex`**
2. **Rédiger enonce.tex** en respectant les mises en page ci-dessus
3. **Vérifier** que tous les `CodePythonLst` sont EN DEHORS des `EXO`

### ÉTAPE 5 : VALIDATION ET COMPILATION

1. **Utiliser le skill `tex-compiling-skill`** pour compiler
2. **Vérifier le rendu PDF**
3. **Ajuster** si nécessaire

---

## BARÈME STANDARD (20 points)

| Exercice | Points | Détail |
|----------|--------|--------|
| Exercice 1 | 6 pts | a) 2 pts - b) 3 pts - c) 1 pt |
| Exercice 2 | 8 pts | Programme complet et fonctionnel |
| Exercice 3 | 6 pts | 2 pts par programme analysé |

---

## SKILLS UTILISÉS

- `tex-document-creator` : Création du projet LaTeX
- `bfcours-latex` : Rédaction du contenu
- `tex-compiling-skill` : Compilation

---

## NOTES IMPORTANTES

1. **CodePythonLst TOUJOURS en dehors des EXO** : Évite les conflits tcolorbox

2. **Syntaxe CodePythonLst** :
   - `{title=Titre}` : avec numéros
   - `*{title=Titre}` : sans numéros (étoile AVANT l'accolade)

3. **Pas d'espaces réponse** (`crep`) : C'est un devoir, pas une fiche à compléter

4. **Correction intégrée** : Utiliser `\exocorrection` dans chaque EXO + `\rdexocorrection{n}` dans le fichier principal

5. **multicols{3}** pour l'exercice 3 : Présentation claire des 3 programmes côte à côte
