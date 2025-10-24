# Guide des styles Beamer - Collège, Lycée, Académique

## Vue d'ensemble

Ce guide présente les trois styles de présentation Beamer disponibles, leurs caractéristiques et leurs cas d'usage.

## Style Collège

### Caractéristiques

**Public** : Élèves de 6ème à 3ème (11-15 ans)

**Objectifs pédagogiques** :
- Capter l'attention avec des couleurs vives
- Faciliter la lecture avec une police grande
- Encourager la participation avec des animations fréquentes
- Simplifier la présentation visuelle

### Spécifications techniques

```latex
\documentclass[14pt, xcolor={svgnames}]{beamer}
\usetheme{Boadilla}  % ou Szeged
\usecolortheme{whale}

% Couleurs vives
\definecolor{college-main}{RGB}{41, 128, 185}      % Bleu vif
\definecolor{college-accent}{RGB}{243, 156, 18}    % Orange
\definecolor{college-alert}{RGB}{231, 76, 60}      % Rouge vif

\setbeamercolor{structure}{fg=college-main}
\setbeamercolor{block title}{bg=college-main, fg=white}
\setbeamercolor{block body}{bg=college-main!10}
```

### Mise en page

- **Taille de police** : 14pt minimum (titre 20pt)
- **Densité maximale** : 60% de remplissage (encore plus aéré que la règle générale)
- **Items par slide** : Maximum 5
- **Lignes de texte** : Maximum 8

### Animations recommandées

```latex
% Animation item par item (systématique)
\begin{itemize}[<+->]
  \item Point 1
  \item Point 2
  \item Point 3
\end{itemize}

% Révélation progressive avec effet
\transfade<2>
\uncover<2->{Texte révélé avec fondu}
```

### Éléments visuels

- **Pictogrammes** : Utiliser des icônes visuelles
- **Couleurs** : Palette vive mais limitée à 3 couleurs principales
- **Graphiques** : Grands, simples, colorés
- **Photos** : Encouragées pour illustrer

### Exemple de slide type

```latex
\begin{frame}{Les nombres relatifs}
  \begin{center}
    \includegraphics[width=0.3\textwidth]{thermometre.png}
  \end{center}

  \begin{itemize}[<+->]
    \item Les nombres \textcolor{college-alert}{négatifs} sont plus petits que zéro
    \item Les nombres \textcolor{college-main}{positifs} sont plus grands que zéro
    \item Le zéro est \textbf{neutre}
  \end{itemize}

  \pause

  \begin{exampleblock}{Exemple}
    $-5 < 0 < +3$
  \end{exampleblock}
\end{frame}
```

### Structure de présentation collège

```
1. Titre animé (1 slide)
2. Rappel avec images (2 slides)
3. Nouvelle notion par étapes (4-5 slides, 1 idée/slide)
4. Exercice guidé interactif (2-3 slides)
5. Synthèse visuelle (1 slide)

Total : 10-12 slides pour 30-40 minutes
```

### Exercices style collège

```latex
\begin{frame}{À toi de jouer !}
  \begin{exobeamer}[Temps : 5 min | Difficulté : ★☆☆]
    \textbf{Exercice :}

    Calcule :
    \[
      3 + (-5) = \textcolor{white}{?}
    \]

    \pause
    \vspace{1em}

    \textbf{Solution :}

    \uncover<2->{
      \begin{tikzpicture}[scale=1.2]
        % Droite graduée
        \draw[<->, thick] (-6,0) -- (6,0);
        \foreach \x in {-5,...,5}
          \draw (\x, -0.1) -- (\x, 0.1) node[above] {\x};

        % Animation de la solution
        \uncover<3->{
          \draw[->, red, very thick] (3, -0.5) -- (-2, -0.5);
          \node[red, below] at (0.5, -0.5) {$-5$};
        }
        \uncover<4->{
          \node[blue, above, font=\Large] at (-2, 0.5) {$-2$};
        }
      \end{tikzpicture}
    }
  \end{exobeamer}
\end{frame}
```

---

## Style Lycée

### Caractéristiques

**Public** : Élèves de 2nde à Terminale (15-18 ans)

**Objectifs pédagogiques** :
- Équilibre entre accessibilité et rigueur
- Introduction progressive du formalisme mathématique
- Développement de l'autonomie
- Préparation au supérieur

### Spécifications techniques

```latex
\documentclass[12pt, xcolor={svgnames}]{beamer}
\usetheme{Madrid}
\usecolortheme{default}

% Couleurs équilibrées
\definecolor{lycee-main}{RGB}{0, 51, 102}          % Bleu marine
\definecolor{lycee-accent}{RGB}{153, 0, 0}         % Bordeaux
\definecolor{lycee-light}{RGB}{230, 230, 250}      % Lavande

\setbeamercolor{structure}{fg=lycee-main}
\setbeamercolor{block title}{bg=lycee-main, fg=white}
\setbeamercolor{block body}{bg=lycee-light}
```

### Mise en page

- **Taille de police** : 12pt (titre 16-18pt)
- **Densité maximale** : 70% de remplissage
- **Items par slide** : Maximum 6-7
- **Lignes de texte** : Maximum 10-12

### Animations recommandées

```latex
% Révélation modérée (pas systématique)
\begin{frame}{Propriétés}
  Propriété principale :
  \[
    f'(x) = nx^{n-1}
  \]

  \pause

  \begin{block}<2->{Démonstration}
    Par définition de la dérivée...
  \end{block}

  \uncover<3->{
    Application immédiate : ...
  }
\end{frame}
```

### Éléments visuels

- **Graphiques** : Précis, annotés, professionnels
- **Couleurs** : Palette sobre (bleu, bordeaux, gris)
- **Formules** : Mises en valeur mais nombreuses
- **Schémas** : Techniques et rigoureux

### Exemple de slide type

```latex
\begin{frame}{Dérivation des fonctions puissances}
  \begin{block}{Théorème}
    Soit $f$ la fonction définie sur $\mathbb{R}$ par $f(x) = x^n$ où $n \in \mathbb{N}^*$.

    Alors $f$ est dérivable sur $\mathbb{R}$ et :
    \[
      \forall x \in \mathbb{R}, \quad f'(x) = nx^{n-1}
    \]
  \end{block}

  \pause

  \begin{exampleblock}{Exemples}
    \begin{itemize}
      \item<3-> Si $f(x) = x^3$, alors $f'(x) = 3x^2$
      \item<4-> Si $f(x) = x^5$, alors $f'(x) = 5x^4$
    \end{itemize}
  \end{exampleblock}
\end{frame}
```

### Structure de présentation lycée

```
1. Titre (1 slide)
2. Plan (1 slide) - pour présentations > 15 slides
3. Rappels et prérequis (2-3 slides)
4. Introduction problématisée (1-2 slides)
5. Cours structuré
   - Section 1 (5-7 slides)
   - Section 2 (5-7 slides)
6. Méthodes et exemples (3-4 slides)
7. Exercices d'application (3-5 slides)
8. Synthèse (1-2 slides)

Total : 20-30 slides pour 55 minutes (1h)
```

### Exercices style lycée

```latex
\begin{frame}{Exercice : Étude de fonction}
  \begin{exobeamer}[Temps : 8 min | Difficulté : ★★☆]
    \textbf{Énoncé :}

    Soit $f$ définie sur $\mathbb{R}$ par $f(x) = x^3 - 3x + 1$.

    \begin{enumerate}
      \item Calculer $f'(x)$
      \item Étudier le signe de $f'(x)$
      \item En déduire les variations de $f$
    \end{enumerate}

    \pause

    \textbf{Solution :}
    \begin{enumerate}
      \item<3-> $f'(x) = 3x^2 - 3 = 3(x^2 - 1) = 3(x-1)(x+1)$
      \item<4-> $f'(x) \geq 0 \Leftrightarrow x \in ]-\infty, -1] \cup [1, +\infty[$
      \item<5-> $f$ est croissante sur $]-\infty, -1]$ et $[1, +\infty[$, décroissante sur $[-1, 1]$
    \end{enumerate}
  \end{exobeamer}
\end{frame}
```

---

## Style Académique

### Caractéristiques

**Public** : Conférences, colloques, soutenances, formations professionnelles

**Objectifs** :
- Présentation rigoureuse et sobre
- Densité d'information maîtrisée
- Références bibliographiques
- Professionnalisme maximal

### Spécifications techniques

```latex
\documentclass[11pt, aspectratio=169]{beamer}  % Format 16:9
\usetheme{default}
\usecolortheme{dove}

% Couleurs sobres
\definecolor{acad-main}{RGB}{0, 0, 0}             % Noir
\definecolor{acad-accent}{RGB}{51, 51, 51}        % Gris foncé
\definecolor{acad-light}{RGB}{245, 245, 245}      % Gris très clair

\setbeamercolor{structure}{fg=acad-main}
\setbeamercolor{block title}{bg=acad-accent, fg=white}
\setbeamercolor{block body}{bg=acad-light}

% Pas de symboles de navigation
\setbeamertemplate{navigation symbols}{}

% Numérotation des slides
\setbeamertemplate{footline}[frame number]
```

### Mise en page

- **Taille de police** : 11pt (titre 14-16pt)
- **Densité maximale** : 70% de remplissage (rigueur académique)
- **Items par slide** : Maximum 7
- **Lignes de texte** : Maximum 12-14

### Animations recommandées

```latex
% Animations minimales (quasi inexistantes)
\begin{frame}{Résultats principaux}
  \begin{theorem}[Nom, Année]
    Énoncé du théorème...
  \end{theorem}

  \vspace{0.5em}

  \begin{proof}[Esquisse]
    Démonstration...
  \end{proof}
\end{frame}
```

**Règle** : Pas de transitions, pas d'effets, sobriété maximale.

### Éléments visuels

- **Graphiques** : Vectoriels, haute résolution, noir et blanc compatibles
- **Couleurs** : Noir, gris, blanc (couleur parcimonieuse)
- **Formules** : Nombreuses, rigoureuses, numérotées si nécessaire
- **Citations** : Formatées avec références

### Exemple de slide type

```latex
\begin{frame}{Convergence du schéma numérique}
  \begin{theorem}[Lax-Richtmyer, 1956]
    Pour un problème bien posé et un schéma consistant, la stabilité est équivalente à la convergence.
  \end{theorem}

  \vspace{1em}

  \textbf{Hypothèses :}
  \begin{itemize}
    \item Problème bien posé au sens d'Hadamard
    \item Schéma consistant : $\tau(h, \Delta t) \to 0$ quand $h, \Delta t \to 0$
    \item Condition CFL respectée
  \end{itemize}

  \vspace{0.5em}

  \footnotesize
  \textbf{Référence :} P. Lax \& R. Richtmyer, \emph{Survey of the stability of linear finite difference equations}, Comm. Pure Appl. Math., 1956.
\end{frame}
```

### Structure de présentation académique

```
1. Titre avec affiliations (1 slide)
2. Plan détaillé (1 slide)
3. Contexte et état de l'art (3-5 slides)
4. Problématique et objectifs (1-2 slides)
5. Méthodologie (3-5 slides)
6. Résultats
   - Résultats théoriques (5-7 slides)
   - Résultats numériques (3-5 slides)
7. Discussion (2-3 slides)
8. Conclusion et perspectives (1-2 slides)
9. Références bibliographiques (1 slide)
10. Annexes (optionnelles)

Total : 25-40 slides pour 30-45 minutes
```

### Slide de références

```latex
\begin{frame}[allowframebreaks]{Références}
  \footnotesize
  \begin{thebibliography}{99}
    \bibitem{lax1956} P. Lax, R. Richtmyer,
      \emph{Survey of the stability of linear finite difference equations},
      Comm. Pure Appl. Math., vol. 9, pp. 267-293, 1956.

    \bibitem{godunov1959} S. Godunov,
      \emph{A difference method for numerical calculation of discontinuous solutions},
      Mat. Sb., vol. 47, pp. 271-306, 1959.

    % [allowframebreaks] permet de créer plusieurs slides si nécessaire
  \end{thebibliography}
\end{frame}
```

---

## Tableau comparatif

| Critère | Collège | Lycée | Académique |
|---------|---------|-------|------------|
| **Police principale** | 14pt | 12pt | 11pt |
| **Police titres** | 20pt | 16-18pt | 14-16pt |
| **Densité max** | 60% | 70% | 70% |
| **Items/slide** | 5 | 6-7 | 7 |
| **Animations** | Fréquentes | Modérées | Rares |
| **Couleurs** | Vives | Équilibrées | Sobres |
| **Format** | 4:3 | 4:3 | 16:9 |
| **Références** | Non | Rares | Systématiques |
| **Exercices** | Interactifs | Appliqués | Optionnels |
| **Slides/heure** | 15-20 | 25-35 | 40-60 |

## Choix du style selon le contexte

### Collège

✅ Cours en classe 6e-3e
✅ Activités découverte
✅ Présentations ludiques
✅ Supports de rappel

❌ Conférences formelles
❌ Présentations denses

### Lycée

✅ Cours en classe 2nde-Tale
✅ Conférences lycéennes
✅ Olympiades, concours
✅ Formations enseignants

❌ Élèves jeunes collège
❌ Colloques académiques

### Académique

✅ Soutenances de thèse
✅ Colloques scientifiques
✅ Séminaires de recherche
✅ Formations universitaires

❌ Enseignement secondaire
❌ Vulgarisation grand public

## Personnalisation des styles

### Ajouter un logo d'établissement

```latex
% Logo en haut à droite
\logo{\includegraphics[height=0.8cm]{logo.png}}

% OU logo en pied de page
\setbeamertemplate{footline}{
  \hbox{%
    \begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1ex,left]{author in head/foot}%
      \hspace*{1em}\insertshortauthor
    \end{beamercolorbox}%
    \begin{beamercolorbox}[wd=.5\paperwidth,ht=2.5ex,dp=1ex,right]{title in head/foot}%
      \insertshorttitle\hspace*{1em}
      \insertframenumber{} / \inserttotalframenumber\hspace*{1em}
    \end{beamercolorbox}%
  }
  \vskip0pt%
}
```

### Modifier les couleurs d'un style

```latex
% Personnalisation du style lycée en vert
\definecolor{lycee-main}{RGB}{0, 102, 51}     % Vert foncé
\definecolor{lycee-accent}{RGB}{153, 0, 76}   % Rose
```

### Créer un style hybride

```latex
% Mélange lycée-académique pour classe prépa
\documentclass[11pt, aspectratio=169]{beamer}  % Format académique
\usetheme{Madrid}                               % Thème lycée
\usecolortheme{default}                         % Sobre

% Police académique avec couleurs lycée
\definecolor{hybrid-main}{RGB}{0, 51, 102}
```

---

**En choisissant le bon style, vous garantissez une présentation adaptée à votre public et à vos objectifs pédagogiques.**
