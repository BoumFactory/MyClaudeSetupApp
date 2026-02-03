# Exercices dans Beamer - Guide complet

## Philosophie

Les exercices dans une présentation Beamer ont un double objectif :
1. **Vérifier la compréhension** immédiate de la notion présentée
2. **Dynamiser la présentation** en cassant la monotonie du cours magistral

## L'environnement `exobeamer`

### Définition

L'environnement `exobeamer` est un environnement personnalisé pour intégrer des exercices avec :
- Estimation du temps nécessaire
- Indicateur de difficulté
- Zone modifiable pour le temps réel (professeur)
- Mise en page adaptée

### Syntaxe

```latex
\begin{exobeamer}[Estimation : X min | Difficulté : ★☆☆]
  % Contenu de l'exercice
\end{exobeamer}
```

### Implémentation de l'environnement

À ajouter dans le préambule de votre présentation :

```latex
\usepackage{tcolorbox}
\tcbuselibrary{skins, breakable}

% Définition de l'environnement exobeamer
\newtcolorbox{exobeamer}[1][]{
  enhanced,
  breakable,
  colback=blue!5,
  colframe=blue!50!black,
  coltitle=white,
  fonttitle=\bfseries,
  title={Exercice},
  attach boxed title to top left={yshift=-2mm, xshift=5mm},
  boxed title style={
    colback=blue!50!black,
    sharp corners,
    boxrule=0pt,
  },
  top=5mm,
  bottom=3mm,
  left=3mm,
  right=3mm,
  overlay unbroken and first={
    \node[anchor=north east, font=\small\itshape, text=blue!50!black]
      at ([xshift=-5mm, yshift=-2mm]frame.north east) {#1};
  }
}
```

### Utilisation dans une slide

```latex
\begin{frame}{Application directe}
  \begin{exobeamer}[Estimation : 5 min | Difficulté : ★☆☆]
    \textbf{Énoncé :}

    Calculer la dérivée de $f(x) = 3x^2 - 5x + 2$.

    \pause
    \vspace{1em}

    \textbf{Solution :}

    \uncover<2->{
      $f'(x) = 6x - 5$
    }
  \end{exobeamer}
\end{frame}
```

## Estimation du temps

### Règles générales

L'estimation du temps dépend de :
1. **Complexité de l'exercice**
2. **Niveau des élèves**
3. **Contexte** (découverte vs révision)
4. **Autonomie attendue**

### Guide d'estimation par type

| Type d'exercice | Temps collège | Temps lycée | Temps académique |
|-----------------|---------------|-------------|------------------|
| **Application directe** | 5-7 min | 3-5 min | 2-3 min |
| **Exercice à étapes** | 8-12 min | 5-8 min | 3-5 min |
| **Problème** | 15-20 min | 10-15 min | 8-12 min |
| **Investigation** | 25-30 min | 20-25 min | 15-20 min |

### Facteurs d'ajustement

**Ajouter du temps si :**
- Première fois que la notion est utilisée (+30%)
- Exercice nécessitant une réflexion (+20%)
- Calculs complexes ou longs (+20%)
- Classe hétérogène (+10%)

**Réduire le temps si :**
- Notion vue plusieurs fois (-20%)
- Exercice de routine (-15%)
- Classe habituée à la méthode (-10%)

### Exemples calibrés

#### Collège - Application directe (5 min)

```latex
\begin{frame}{Exercice : Calcul mental}
  \begin{exobeamer}[Estimation : 5 min | Difficulté : ★☆☆]
    \textbf{Calculer :}

    \begin{enumerate}
      \item $(-3) + (+7) = $
      \item $(+5) - (+8) = $
      \item $(-2) \times (-4) = $
    \end{enumerate}

    \pause

    \textbf{Solutions :}
    \begin{enumerate}
      \item<2-> $(-3) + (+7) = +4$
      \item<3-> $(+5) - (+8) = -3$
      \item<4-> $(-2) \times (-4) = +8$
    \end{enumerate}
  \end{exobeamer}
\end{frame}
```

#### Lycée - Exercice guidé (8 min)

```latex
\begin{frame}{Exercice : Équation du second degré}
  \begin{exobeamer}[Estimation : 8 min | Difficulté : ★★☆]
    \textbf{Résoudre dans $\mathbb{R}$ :}
    \[
      x^2 - 5x + 6 = 0
    \]

    \textbf{Méthode :}
    \begin{enumerate}
      \item<2-> Calculer le discriminant : $\Delta = b^2 - 4ac = 25 - 24 = 1$
      \item<3-> $\Delta > 0$ donc deux solutions
      \item<4-> $x_1 = \frac{5 - 1}{2} = 2$ et $x_2 = \frac{5 + 1}{2} = 3$
    \end{enumerate}

    \uncover<5->{
      \textbf{Ensemble solution :} $S = \{2 ; 3\}$
    }
  \end{exobeamer}
\end{frame}
```

#### Académique - Problème (12 min)

```latex
\begin{frame}{Exercice : Convergence de suite}
  \begin{exobeamer}[Estimation : 12 min | Difficulté : ★★★]
    \textbf{Soit $(u_n)$ définie par :}
    \[
      u_0 = 1, \quad u_{n+1} = \frac{1}{2}u_n + 1
    \]

    \textbf{Questions :}
    \begin{enumerate}
      \item Montrer que $(u_n)$ est bornée
      \item Étudier la monotonie
      \item Calculer la limite
    \end{enumerate}

    \only<2->{
      \footnotesize
      \textbf{Indication :} Étudier $|u_n - 2|$
    }
  \end{exobeamer}
\end{frame}
```

## Indicateurs de difficulté

### Échelle de difficulté

- **★☆☆** : Application directe, routine
- **★★☆** : Exercice à étapes, réflexion modérée
- **★★★** : Problème complexe, réflexion approfondie

### Correspondance avec les niveaux

**Collège** :
- ★☆☆ : Calculs simples, application immédiate
- ★★☆ : Problème à étapes, nécessite méthode
- ★★★ : Investigation, recherche, tâche complexe

**Lycée** :
- ★☆☆ : Application formule, technique standard
- ★★☆ : Exercice guidé, plusieurs questions
- ★★★ : Problème ouvert, démonstration

**Académique** :
- ★☆☆ : Vérification de propriété
- ★★☆ : Application de théorème
- ★★★ : Démonstration originale, généralisation

## Zone modifiable pour le professeur

### Principe

L'enseignant doit pouvoir noter le **temps réel** pris par les élèves, pour :
- Ajuster les futures présentations
- Calibrer son estimation
- Adapter le rythme de la séance

### Implémentation

```latex
% Version avec zone de notes
\newtcolorbox{exobeamer}[1][]{
  enhanced,
  breakable,
  colback=blue!5,
  colframe=blue!50!black,
  coltitle=white,
  fonttitle=\bfseries,
  title={Exercice},
  attach boxed title to top left={yshift=-2mm, xshift=5mm},
  boxed title style={
    colback=blue!50!black,
    sharp corners,
    boxrule=0pt,
  },
  top=5mm,
  bottom=3mm,
  left=3mm,
  right=3mm,
  overlay unbroken and first={
    % Estimation (à gauche)
    \node[anchor=north west, font=\small\itshape, text=blue!50!black]
      at ([xshift=5mm, yshift=-10mm]frame.north west) {#1};
    % Zone modifiable (à droite)
    \node[anchor=north east, font=\small, text=red!70!black, draw=red!70!black,
          fill=white, inner sep=2pt, minimum width=3cm]
      at ([xshift=-5mm, yshift=-10mm]frame.north east) {Temps réel : \underline{\hspace{1.5cm}}};
  }
}
```

### Exemple d'utilisation

```latex
\begin{frame}{Exercice guidé}
  \begin{exobeamer}[Estimation : 8 min | Difficulté : ★★☆]
    % Énoncé de l'exercice...
  \end{exobeamer}

  % Après la séance, le professeur note :
  % "Temps réel : 12 min" → ajuster pour la prochaine fois
\end{frame}
```

## Types d'exercices en présentation

### 1. Application directe

**Objectif** : Vérifier la compréhension immédiate

**Caractéristiques** :
- 1 question, 1 réponse
- Calcul simple ou définition
- Pas de piège

**Exemple** :

```latex
\begin{frame}{Application}
  \begin{exobeamer}[Estimation : 3 min | Difficulté : ★☆☆]
    Si $f(x) = x^2$, calculer $f(3)$.

    \pause

    \textbf{Solution :} $f(3) = 3^2 = 9$
  \end{exobeamer}
\end{frame}
```

### 2. Exercice à trous

**Objectif** : Compléter un raisonnement

**Caractéristiques** :
- Structure donnée
- Compléter les étapes manquantes
- Guidage fort

**Exemple** :

```latex
\begin{frame}{Compléter la démonstration}
  \begin{exobeamer}[Estimation : 6 min | Difficulté : ★★☆]
    Montrer que $f(x) = x^2$ est croissante sur $[0, +\infty[$.

    \textbf{Démonstration :}

    Soient $a, b \in [0, +\infty[$ tels que $a < b$.

    \only<2->{On a : $b^2 - a^2 = (b-a)(b+a)$}

    \only<3->{Comme $b > a \geq 0$, on a $b - a > 0$ et $b + a > 0$}

    \only<4->{Donc $b^2 - a^2 > 0$, soit $f(b) > f(a)$}

    \only<5->{Conclusion : $f$ est croissante sur $[0, +\infty[$}
  \end{exobeamer}
\end{frame}
```

### 3. QCM interactif

**Objectif** : Tester plusieurs notions rapidement

**Caractéristiques** :
- Choix multiples
- Révélation progressive de la réponse
- Feedback immédiat

**Exemple** :

```latex
\begin{frame}{QCM}
  \begin{exobeamer}[Estimation : 4 min | Difficulté : ★☆☆]
    La dérivée de $f(x) = 3x^2$ est :

    \begin{enumerate}[a)]
      \item $f'(x) = 3x$
      \item $f'(x) = 6x$
      \item $f'(x) = 3$
    \end{enumerate}

    \pause

    \textbf{Réponse :} \alert{b) $f'(x) = 6x$}
  \end{exobeamer}
\end{frame}
```

### 4. Problème ouvert

**Objectif** : Recherche, investigation

**Caractéristiques** :
- Pas de guidage
- Plusieurs approches possibles
- Temps plus long

**Exemple** :

```latex
\begin{frame}{Investigation}
  \begin{exobeamer}[Estimation : 20 min | Difficulté : ★★★]
    \textbf{Problème :}

    On considère la suite $(u_n)$ définie par :
    \[
      u_0 = 1, \quad u_{n+1} = \sqrt{2 + u_n}
    \]

    \textbf{Questions :}
    \begin{itemize}
      \item Cette suite est-elle convergente ?
      \item Si oui, quelle est sa limite ?
    \end{itemize}

    \vspace{0.5em}

    \footnotesize
    \emph{Piste : Étudier la monotonie et la majoration.}
  \end{exobeamer}
\end{frame}
```

### 5. Exercice avec TikZ interactif

**Objectif** : Visualisation progressive

**Caractéristiques** :
- Construction géométrique étape par étape
- Annotations progressives
- Interactivité visuelle

**Exemple** :

```latex
\begin{frame}{Construction géométrique}
  \begin{exobeamer}[Estimation : 10 min | Difficulté : ★★☆]
    Construire le symétrique de $A$ par rapport à $B$.

    \begin{center}
      \begin{tikzpicture}[scale=1.5]
        % Points initiaux
        \fill (0,0) circle (2pt) node[below] {$B$};
        \fill (-2,1) circle (2pt) node[above left] {$A$};

        % Construction progressive
        \only<2->{
          \draw[dashed, gray] (-2,1) -- (0,0);
          \node[gray, above] at (-1, 0.5) {$d$};
        }
        \only<3->{
          \draw[dashed, gray] (0,0) -- (2,-1);
        }
        \only<4->{
          \fill[red] (2,-1) circle (2pt) node[below right, red] {$A'$};
        }
        \only<5->{
          \draw[<->, thick] (-2.5,1) -- (2.5,-1);
          \node[above] at (0, 1) {$BA = BA'$};
        }
      \end{tikzpicture}
    \end{center}
  \end{exobeamer}
\end{frame}
```

## Intégration dans la présentation

### Fréquence recommandée

**Règle générale** : 1 exercice toutes les 5-7 slides de cours

| Style | Fréquence | Type privilégié |
|-------|-----------|-----------------|
| Collège | 1 exercice / 4-5 slides | Application directe, QCM |
| Lycée | 1 exercice / 6-7 slides | Guidé, à trous |
| Académique | 1 exercice / 10 slides | Problème ouvert (optionnel) |

### Positionnement

**Bon moment pour un exercice** :
- Après l'introduction d'une nouvelle notion
- Avant une pause (rupture naturelle)
- Après une section dense (respiration)
- En fin de présentation (synthèse)

**Mauvais moment** :
- Au milieu d'une démonstration
- Juste après une transition de section
- Trop tôt (notion non expliquée)

### Slides de transition vers l'exercice

```latex
% Slide de préparation
\begin{frame}{À vous de jouer !}
  \begin{center}
    {\Large Exercice d'application}

    \vspace{1em}

    Mettez en pratique ce que nous venons de voir.
  \end{center}
\end{frame}

% Slide d'exercice
\begin{frame}{Exercice}
  \begin{exobeamer}[...]
    % Contenu
  \end{exobeamer}
\end{frame}
```

## Correction des exercices

### Révélation progressive

```latex
\begin{frame}{Exercice}
  \begin{exobeamer}[Estimation : 8 min | Difficulté : ★★☆]
    \textbf{Énoncé :}

    Résoudre $2x + 3 = 7$

    \pause
    \vspace{1em}

    \textbf{Solution :}

    \begin{enumerate}
      \item<3-> Soustraire 3 : $2x = 4$
      \item<4-> Diviser par 2 : $x = 2$
      \item<5-> Vérification : $2 \times 2 + 3 = 7$ ✓
    \end{enumerate}
  \end{exobeamer}
\end{frame}
```

### Correction détaillée sur slide séparée

```latex
% Slide 1 : Énoncé
\begin{frame}{Exercice 1}
  \begin{exobeamer}[Estimation : 10 min | Difficulté : ★★☆]
    Résoudre le système :
    \[
      \begin{cases}
        2x + y = 5 \\
        x - y = 1
      \end{cases}
    \]
  \end{exobeamer}
\end{frame}

% Slide 2 : Correction
\begin{frame}{Correction exercice 1}
  \textbf{Méthode par substitution :}

  \begin{align*}
    \uncover<2->{x - y &= 1 \implies x = y + 1} \\
    \uncover<3->{2(y+1) + y &= 5} \\
    \uncover<4->{3y + 2 &= 5} \\
    \uncover<5->{y &= 1} \\
    \uncover<6->{x &= 2}
  \end{align*}

  \uncover<7->{
    \textbf{Solution :} $(x, y) = (2, 1)$
  }
\end{frame}
```

## Gestion du temps en séance

### Chronométrage

Pendant la présentation :
1. **Annoncer le temps estimé** : "Vous avez 5 minutes"
2. **Lancer un chronomètre** (visible si possible)
3. **Alerter à mi-parcours** : "Plus que 2 minutes"
4. **Noter le temps réel** dans la zone dédiée

### Adaptation en temps réel

**Si les élèves ont fini avant** :
- Proposer une variante plus complexe
- Passer à la correction immédiatement
- Anticiper la slide suivante

**Si les élèves n'ont pas fini** :
- Donner 2-3 minutes supplémentaires (MAX)
- Corriger collectivement
- Noter l'écart pour ajustement futur

## Récapitulatif des bonnes pratiques

✅ **FAIRE** :
- Estimer le temps de manière réaliste
- Indiquer la difficulté clairement
- Révéler la solution progressivement
- Prévoir une zone de notes pour le temps réel
- Alterner cours et exercices régulièrement

❌ **ÉVITER** :
- Sous-estimer le temps nécessaire
- Exercices sans indication de difficulté
- Tout révéler d'un coup
- Trop d'exercices (lassitude)
- Exercices inadaptés au niveau

---

**Avec ces pratiques, vos exercices Beamer seront efficaces, bien calibrés et permettront une gestion optimale du temps en présentation.**
