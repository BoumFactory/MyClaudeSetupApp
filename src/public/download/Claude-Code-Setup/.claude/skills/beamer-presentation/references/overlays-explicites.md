# Overlays explicites Beamer : Contrôle précis de l'affichage

## Principe fondamental

❌ **NE PAS utiliser `\pause`** : contrôle imprécis, difficile à maintenir, effets non prévisibles

✅ **TOUJOURS utiliser les overlays explicites** : contrôle total sur ce qui s'affiche à chaque étape

## Syntaxe des overlays Beamer

### Numérotation des slides

Dans Beamer, chaque "étape" d'une frame est numérotée :
- `<1>` = première vue de la frame
- `<2>` = deuxième vue (après premier clic)
- `<3>` = troisième vue (après deuxième clic)
- etc.

### Syntaxe de spécification

```latex
<2>      % Seulement au slide 2
<2->     % À partir du slide 2 (2, 3, 4, ...)
<-3>     % Jusqu'au slide 3 (1, 2, 3)
<2-4>    % Du slide 2 au slide 4 (2, 3, 4)
<1,3,5>  % Seulement aux slides 1, 3 et 5
```

## Commandes d'overlay

### `\only<spec>{contenu}`

**Affiche le contenu UNIQUEMENT aux slides spécifiés, SANS réserver d'espace ailleurs**

```latex
\only<1>{Texte visible seulement au slide 1}
\only<2>{Texte visible seulement au slide 2}
```

**Usage** : Remplacement de contenu (un texte disparaît, un autre apparaît)

**Exemple** :
```latex
\begin{frame}{Résultat}
  Le résultat est :
  \only<1>{À calculer...}
  \only<2->{$x = 5$}
\end{frame}
```

### `\uncover<spec>{contenu}`

**Affiche le contenu aux slides spécifiés, MAIS réserve l'espace sur tous les slides**

```latex
\uncover<2->{Ce texte apparaît au slide 2, mais l'espace est réservé dès le slide 1}
```

**Usage** : Révélation progressive sans décalage de mise en page

**Exemple** :
```latex
\begin{frame}{Formule}
  \[
    f(x) = x^2
  \]

  \uncover<2->{La dérivée est : $f'(x) = 2x$}
\end{frame}
```

### `\visible<spec>{contenu}`

**Identique à `\uncover`** (alias)

### `\invisible<spec>{contenu}`

**Inverse de `\visible`** : rend invisible aux slides spécifiés

```latex
\invisible<1>{Caché au slide 1, visible ensuite}
```

### `\alert<spec>{contenu}`

**Met en évidence (généralement en rouge) aux slides spécifiés**

```latex
\alert<2>{Texte mis en évidence au slide 2}
```

### `\temporal<spec>{avant}{pendant}{après}`

**Affiche différents contenus avant/pendant/après un slide**

```latex
\temporal<3>{Avant le slide 3}{Au slide 3}{Après le slide 3}
```

## Structure d'un exercice avec overlays explicites

### Exercice simple : 3 étapes

```latex
\begin{frame}{Exercice 1 : Application directe}
  % ========================================
  % SLIDE 1 : Énoncé + Formule
  % ========================================
  \only<1->{%
    \textbf{Énoncé :} Calculer $\vec{u} \cdot \vec{v}$ avec :
    \begin{itemize}
      \item $\|\vec{u}\| = \num{2}$
      \item $\|\vec{v}\| = \num{3}$
      \item $\widehat{(\vec{u},\vec{v})} = 60°$
    \end{itemize}
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 2 : + Formule à appliquer
  % ========================================
  \uncover<2->{%
    \textbf{Formule :}
    \[
      \vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}\| \times \cos(\alpha)
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 3 : + Calcul complet
  % ========================================
  \uncover<3->{%
    \textbf{Application numérique :}
    \[
      \vec{u} \cdot \vec{v} = \num{2} \times \num{3} \times \cos(60°)
                             = \num{6} \times \frac{1}{2} = \num{3}
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 4 : + Résultat encadré
  % ========================================
  \uncover<4>{%
    \begin{alertblock}{Résultat}
      $\vec{u} \cdot \vec{v} = \num{3}$
    \end{alertblock}
  }
\end{frame}
```

**Pages PDF générées** : 4 pages
- Slide 1 : Énoncé seul
- Slide 2 : Énoncé + Formule
- Slide 3 : Énoncé + Formule + Calcul
- Slide 4 : Énoncé + Formule + Calcul + Résultat encadré

### Exercice avec étapes de calcul décomposées

```latex
\begin{frame}{Exercice 2 : Calcul progressif}
  % ========================================
  % SLIDE 1 : Données
  % ========================================
  \only<1->{%
    \textbf{Données :} $\vec{u}\begin{pmatrix}\num{15}\\-\num{8}\end{pmatrix}$
    et $\vec{v}\begin{pmatrix}\num{6}\\\num{9}\end{pmatrix}$
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 2 : Formule
  % ========================================
  \uncover<2->{%
    \textbf{Formule :} $\vec{u} \cdot \vec{v} = x_u x_v + y_u y_v$
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 3 : Substitution
  % ========================================
  \uncover<3->{%
    \textbf{Substitution :}
    \[
      \vec{u} \cdot \vec{v} = \num{15} \times \num{6} + (-\num{8}) \times \num{9}
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 4 : Calcul partiel
  % ========================================
  \uncover<4->{%
    \[
      = \num{90} + (-\num{72})
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 5 : Résultat final
  % ========================================
  \uncover<5>{%
    \[
      = \boxed{\num{18}}
    \]
  }
\end{frame}
```

**Pages PDF** : 5 pages

**Contrôle précis** :
- Slide 1 : Données seules
- Slide 2 : Données + Formule
- Slide 3 : Données + Formule + Substitution
- Slide 4 : Données + Formule + Substitution + Calcul partiel
- Slide 5 : Données + Formule + Substitution + Calcul partiel + Résultat

### Exercice avec remplacement dynamique

```latex
\begin{frame}{Exercice 3 : Étapes remplaçantes}
  \textbf{Calculer :} $\sqrt{18}$

  \vspace{1cm}

  % ========================================
  % SLIDE 1 : Question
  % ========================================
  \only<1>{%
    \centering
    \Large
    Comment simplifier $\sqrt{18}$ ?
  }

  % ========================================
  % SLIDE 2 : Décomposition (remplace le slide 1)
  % ========================================
  \only<2>{%
    \[
      \sqrt{18} = \sqrt{9 \times 2}
    \]
  }

  % ========================================
  % SLIDE 3 : Séparation (remplace le slide 2)
  % ========================================
  \only<3>{%
    \[
      \sqrt{18} = \sqrt{9 \times 2} = \sqrt{9} \times \sqrt{2}
    \]
  }

  % ========================================
  % SLIDE 4 : Simplification (remplace le slide 3)
  % ========================================
  \only<4->{%
    \[
      \sqrt{18} = \sqrt{9 \times 2} = \sqrt{9} \times \sqrt{2} = \num{3}\sqrt{2}
    \]
  }
\end{frame}
```

**Pages PDF** : 4 pages

**Effet** : Le contenu se **remplace** à chaque étape (pas d'accumulation)

### Exercice avec mise en évidence

```latex
\begin{frame}{Exercice 4 : Angles remarquables}
  Calculer $\cos(45°)$, $\cos(60°)$, $\cos(90°)$

  \vspace{1cm}

  \begin{itemize}
    \item $\cos(45°) = \alert<2>{\dfrac{\sqrt{2}}{2}}$
    \item $\cos(60°) = \alert<3>{\dfrac{1}{2}}$
    \item $\cos(90°) = \alert<4>{\num{0}}$
  \end{itemize}

  \vspace{1cm}

  \uncover<5>{%
    \begin{exampleblock}{Remarque}
      L'angle droit a un cosinus nul.
    \end{exampleblock}
  }
\end{frame}
```

**Pages PDF** : 5 pages

**Effet** :
- Slide 1 : Toutes les valeurs visibles
- Slide 2 : $\cos(45°)$ mis en évidence (rouge)
- Slide 3 : $\cos(60°)$ mis en évidence
- Slide 4 : $\cos(90°)$ mis en évidence
- Slide 5 : Remarque apparaît

## Utilisation avec les environnements

### Blocs

```latex
\begin{frame}{Méthode}
  % Bloc visible dès le slide 1
  \begin{block}{Étape 1}
    Identifier les données
  \end{block}

  % Bloc visible à partir du slide 2
  \uncover<2->{%
    \begin{block}{Étape 2}
      Appliquer la formule
    \end{block}
  }

  % Bloc visible à partir du slide 3
  \uncover<3>{%
    \begin{alertblock}{Attention}
      Vérifier le signe !
    \end{alertblock}
  }
\end{frame}
```

### Listes

#### Révélation item par item

```latex
\begin{frame}{Liste progressive}
  \begin{itemize}
    \item<1-> Premier item (visible dès le slide 1)
    \item<2-> Deuxième item (visible à partir du slide 2)
    \item<3-> Troisième item (visible à partir du slide 3)
  \end{itemize}
\end{frame}
```

**Équivalent automatique** :

```latex
\begin{itemize}[<+->]  % Révélation automatique successive
  \item Premier
  \item Deuxième
  \item Troisième
\end{itemize}
```

#### Mise en évidence item par item

```latex
\begin{frame}{Liste avec focus}
  \begin{itemize}
    \item<1-| alert@2> Première méthode
    \item<1-| alert@3> Deuxième méthode
    \item<1-| alert@4> Troisième méthode
  \end{itemize}
\end{frame}
```

**Effet** :
- Slide 1 : Toutes visibles, aucune en rouge
- Slide 2 : Toutes visibles, première en rouge
- Slide 3 : Toutes visibles, deuxième en rouge
- Slide 4 : Toutes visibles, troisième en rouge

### Colonnes

```latex
\begin{frame}{Comparaison}
  \begin{columns}[T]
    % Colonne gauche : visible dès le slide 1
    \begin{column}{0.48\textwidth}
      \uncover<1->{%
        \textbf{Méthode 1}

        Utiliser l'angle...
      }
    \end{column}

    % Colonne droite : visible à partir du slide 2
    \begin{column}{0.48\textwidth}
      \uncover<2->{%
        \textbf{Méthode 2}

        Utiliser les coordonnées...
      }
    \end{column}
  \end{columns}
\end{frame}
```

### Équations align

```latex
\begin{frame}{Calcul détaillé}
  \begin{align*}
    \uncover<1->{f(x) &= (2x+1)^2 \\}
    \uncover<2->{     &= (2x)^2 + 2 \times 2x \times 1 + 1^2 \\}
    \uncover<3->{     &= \num{4}x^2 + \num{4}x + \num{1}}
  \end{align*}
\end{frame}
```

**Pages PDF** : 3 pages
- Slide 1 : Première ligne seule
- Slide 2 : Première + deuxième ligne
- Slide 3 : Les trois lignes

## Package siunitx pour les nombres

### Installation et chargement

```latex
\documentclass{beamer}

\usepackage{siunitx}

% Configuration française
\sisetup{
  locale = FR,                    % Virgule comme séparateur décimal
  group-separator = {\,},         % Espace fine pour grouper les milliers
  output-decimal-marker = {,},    % Virgule pour décimales
  exponent-product = \cdot,       % Point médian pour 10^n
}
```

### Commande `\num{nombre}`

**Usage** : Afficher un nombre avec la bonne typographie

```latex
% Entiers
\num{3}          % → 3
\num{1234}       % → 1 234 (espace fine automatique)
\num{1234567}    % → 1 234 567

% Décimaux
\num{3.14}       % → 3,14 (virgule française)
\num{2.71828}    % → 2,718 28

% Négatifs
\num{-5}         % → -5
\num{-72}        % → -72

% Notation scientifique
\num{6.022e23}   % → 6,022 × 10²³

% Fractions décimales
\num{0.5}        % → 0,5
\num{3.25}       % → 3,25
```

### Exemples en Beamer

#### Calcul avec nombres

```latex
\begin{frame}{Exercice : Calcul}
  \uncover<1->{%
    Calculer : $\num{15} \times \num{6} + (-\num{8}) \times \num{9}$
  }

  \uncover<2->{%
    \[
      = \num{90} + (-\num{72})
    \]
  }

  \uncover<3>{%
    \[
      = \num{18}
    \]
  }
\end{frame}
```

#### Résultats décimaux

```latex
\begin{frame}{Résultat approché}
  \uncover<1->{%
    $\cos(\alpha) = \num{0.7071}$
  }

  \uncover<2>{%
    Donc $\alpha \approx \num{45}°$
  }
\end{frame}
```

#### Coordonnées

```latex
\begin{frame}{Vecteur}
  Le vecteur $\vec{u}$ a pour coordonnées :
  \[
    \vec{u}\begin{pmatrix}\num{3.5}\\\num{-2.75}\end{pmatrix}
  \]
\end{frame}
```

### Ne PAS utiliser `\num{}` pour :

❌ **Variables mathématiques** : `x`, `y`, `n`, `a`, `b`
❌ **Exposants** : `x^2`, `10^{-3}` (sauf notation scientifique)
❌ **Indices** : `x_1`, `a_n`
❌ **Constantes symboliques** : `\pi`, `e`

✅ **UNIQUEMENT pour les valeurs numériques concrètes**

## Exemple complet d'exercice bien structuré

```latex
\begin{frame}{Exercice : Produit scalaire avec coordonnées}
  % ========================================
  % SLIDE 1-4 : Énoncé présent partout
  % ========================================
  \only<1->{%
    \textbf{Énoncé :} Calculer $\vec{u} \cdot \vec{v}$ avec
    $\vec{u}\begin{pmatrix}\num{15}\\-\num{8}\end{pmatrix}$
    et $\vec{v}\begin{pmatrix}\num{6}\\\num{9}\end{pmatrix}$
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 2-4 : Formule apparaît
  % ========================================
  \uncover<2->{%
    \textbf{Formule :}
    \[
      \vec{u} \cdot \vec{v} = x_u x_v + y_u y_v
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 3-4 : Application apparaît
  % ========================================
  \uncover<3->{%
    \textbf{Application :}
    \[
      \vec{u} \cdot \vec{v} = \num{15} \times \num{6} + (-\num{8}) \times \num{9}
    \]
  }

  \vspace{0.5cm}

  % ========================================
  % SLIDE 4 : Résultat final apparaît
  % ========================================
  \uncover<4>{%
    \[
      = \num{90} - \num{72} = \boxed{\num{18}}
    \]
  }
\end{frame}
```

**Pages PDF** : 4 pages parfaitement contrôlées

## Règles de bonnes pratiques

### 1. Toujours spécifier les plages

✅ **BON** :
```latex
\uncover<2->{Texte}      % Visible à partir du slide 2 jusqu'à la fin
\only<1-3>{Texte}        % Visible slides 1, 2, 3 seulement
```

❌ **MAUVAIS** :
```latex
\uncover<2>{Texte}       % Visible SEULEMENT au slide 2 (disparaît après)
```

### 2. Utiliser `\only<1->{...}` pour le contenu permanent

```latex
\only<1->{%              % Visible sur TOUS les slides
  Texte toujours présent
}
```

### 3. Grouper les overlays complexes avec `{...}`

```latex
\uncover<2->{%
  Tout ce contenu
  sur plusieurs lignes
  apparaît ensemble
  au slide 2
}
```

### 4. Éviter les overlays imbriqués complexes

❌ **COMPLEXE** :
```latex
\uncover<2->{%
  Texte 1
  \uncover<3->{%
    Texte 2
    \uncover<4->{%
      Texte 3
    }
  }
}
```

✅ **SIMPLE** :
```latex
\uncover<2->{Texte 1}
\uncover<3->{Texte 2}
\uncover<4->{Texte 3}
```

### 5. Utiliser `\num{}` systématiquement pour les nombres

✅ **BON** :
```latex
$x = \num{3.14}$
$\vec{u}\begin{pmatrix}\num{2}\\-\num{5}\end{pmatrix}$
Le résultat est $\num{42}$.
```

❌ **MAUVAIS** :
```latex
$x = 3.14$               % Point au lieu de virgule
$\vec{u}\begin{pmatrix}2\\-5\end{pmatrix}$  % Pas de \num
Le résultat est 42.      % Pas de \num
```

## Résumé : Les commandes essentielles

| Commande | Usage | Réserve l'espace ? |
|----------|-------|-------------------|
| `\only<spec>{...}` | Affichage sans réserver d'espace | Non |
| `\uncover<spec>{...}` | Révélation avec espace réservé | Oui |
| `\visible<spec>{...}` | Identique à `\uncover` | Oui |
| `\invisible<spec>{...}` | Inverse de `\visible` | Oui |
| `\alert<spec>{...}` | Mise en évidence (rouge) | - |
| `\item<spec>` | Item avec overlay | - |

| Package siunitx | Usage |
|-----------------|-------|
| `\num{nombre}` | Afficher un nombre avec bonne typo |
| `\num{3.14}` | → 3,14 (virgule française) |
| `\num{1234}` | → 1 234 (espace fine) |

---

**Avec les overlays explicites et siunitx, vous avez un contrôle total et professionnel sur vos présentations Beamer !**
