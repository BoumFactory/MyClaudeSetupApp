# Utilisation des figures TikZ avec tikzinclude

## Principe de fonctionnement

Le système de figures TikZ dans les documents bfcours utilise un mécanisme de définition/appel en deux parties :

### 1. Définition dans enonce_figures.tex

Les figures TikZ sont définies comme des commandes dans le fichier `enonce_figures.tex` avec la convention de nommage suivante :

```latex
\newcommand{\tikzfigNOMFIGURE}{%
    % Code TikZ de la figure
    \begin{tikzpicture}
        % ...
    \end{tikzpicture}%
}
```

**IMPORTANT** : Le nom de la figure (NOMFIGURE) doit :
- Commencer par `\tikzfig`
- Contenir **uniquement des lettres** (pas de chiffres, pas de caractères spéciaux, pas de tirets, pas d'underscores)
- Exemples valides : `\tikzfigrectMilieux`, `\tikzfigfigureComplexe`, `\tikzfigtriangle`
- Exemples invalides : `\tikzfigrect_milieux`, `\tikzfigfigure1`, `\tikzfig-complexe`

### 2. Appel dans enonce.tex

Dans le fichier `enonce.tex`, on appelle la figure avec la commande `\tikzinclude{}` en passant **uniquement la partie nom** (sans le préfixe `\tikzfig`) :

```latex
\tikzinclude{NOMFIGURE}
```

### 3. Mécanisme interne

Le fichier principal définit la commande `\tikzinclude` qui :
1. Incrémente un compteur (pour numéroter les figures si nécessaire)
2. Reconstitue le nom complet de la commande en ajoutant le préfixe `\tikzfig`
3. Appelle la commande correspondante

```latex
\newcounter{tikzfigcounter}
\newcommand{\tikzinclude}[1]{%
    \stepcounter{tikzfigcounter}%
    \csname tikzfig#1\endcsname
}
\input{enonce_figures}
```

## Exemples complets

### Exemple 1 : Figure simple

**Dans enonce_figures.tex :**
```latex
\newcommand{\tikzfigtriangle}{%
\begin{tikzpicture}[scale=0.5]
    \draw (0,0) node[below]{$A$} -- (4,0) node[below]{$B$} -- (2,3) node[above]{$C$} -- cycle;
\end{tikzpicture}%
}
```

**Dans enonce.tex :**
```latex
On considère le triangle $ABC$ ci-dessous :

\tikzinclude{triangle}
```

### Exemple 2 : Rectangle avec milieux

**Dans enonce_figures.tex :**
```latex
\newcommand{\tikzfigrectMilieux}{%
\begin{tikzpicture}[scale=0.4]
   \draw (0,0) rectangle (4,7);
   \draw (0,0) node[below]{$E$};
   \draw (4,0) node[below]{$F$};
   \draw (4,7) node[above]{$G$};
   \draw (0,7) node[above]{$H$};
   \fill (2,0) circle (2pt) node[below]{$I$};
   \fill (4,3.5) circle (2pt) node[right]{$J$};
   \fill (2,7) circle (2pt) node[above]{$K$};
   \fill (0,3.5) circle (2pt) node[left]{$L$};
\end{tikzpicture}%
}
```

**Dans enonce.tex :**
```latex
On considère le rectangle $EFGH$ ci-dessous, tel que $EF=4$ et $EH=7$, et les points $I$, $J$, $K$ et $L$, milieux respectifs des côtés $[EF]$, $[FG]$, $[GH]$ et $[EH]$.

\tikzinclude{rectMilieux}
```

## Erreurs courantes

### Erreur 1 : Utiliser `\tikzfig` au lieu de `\tikzinclude`

❌ **INCORRECT :**
```latex
\tikzfig{triangle}  % Cette commande n'existe pas !
```

✅ **CORRECT :**
```latex
\tikzinclude{triangle}
```

### Erreur 2 : Nom de figure avec caractères interdits

❌ **INCORRECT :**
```latex
% Dans enonce_figures.tex
\newcommand{\tikzfigfigure_complexe}{...}  % underscore interdit
\newcommand{\tikzfigfigure1}{...}          % chiffre interdit
\newcommand{\tikzfigfigure-test}{...}      % tiret interdit
```

✅ **CORRECT :**
```latex
% Dans enonce_figures.tex
\newcommand{\tikzfigfigureComplexe}{...}   % camelCase autorisé
\newcommand{\tikzfigfigureUn}{...}         % lettres uniquement
\newcommand{\tikzfigfigureTest}{...}       % lettres uniquement
```

### Erreur 3 : Oublier le % à la fin de l'environnement

❌ **INCORRECT :**
```latex
\newcommand{\tikzfigtriangle}{
\begin{tikzpicture}
    \draw (0,0) -- (1,1);
\end{tikzpicture}
}
```

✅ **CORRECT :**
```latex
\newcommand{\tikzfigtriangle}{%  % Noter le % ici
\begin{tikzpicture}
    \draw (0,0) -- (1,1);
\end{tikzpicture}%                 % Et ici
}
```

Le `%` évite l'insertion d'espaces parasites dans le document.

## Configuration dans le fichier principal

Le fichier principal (ex: `Exercices_Produit_scalaire.tex`) doit contenir :

```latex
\documentclass[a4paper,11pt,fleqn]{article}

\usepackage{bfcours}
\usepackage{bfcours-fonts}

% Compteur pour les figures tikz
\newcounter{tikzfigcounter}

% Définition de la commande tikzinclude
\newcommand{\tikzinclude}[1]{%
    \stepcounter{tikzfigcounter}%
    \csname tikzfig#1\endcsname
}

% Import des figures
\input{enonce_figures}

\begin{document}
\input{enonce}
\end{document}
```

## Bonnes pratiques

1. **Nommer les figures de manière descriptive** : `rectMilieux`, `triangleRectangle`, `cercleInscrit`

2. **Grouper les figures par thème** dans enonce_figures.tex avec des commentaires :
   ```latex
   % ========================================
   % FIGURES GÉOMÉTRIE PLANE
   % ========================================

   \newcommand{\tikzfigtriangle}{...}
   \newcommand{\tikzfigrectangle}{...}
   ```

3. **Utiliser une échelle cohérente** pour toutes les figures d'un même document

4. **Toujours fermer avec %** pour éviter les espaces parasites

5. **Tester la figure** en compilant le document après chaque ajout
