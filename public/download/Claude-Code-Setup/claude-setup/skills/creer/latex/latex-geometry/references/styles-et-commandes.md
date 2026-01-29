# Référence complète des styles et commandes - Tikzset Géométrie

## Bibliothèques TikZ requises

```latex
\usetikzlibrary{decorations.markings,angles,quotes,positioning}
```

## Styles disponibles

### Grilles et axes

| Style | Description | Exemple d'utilisation |
|-------|-------------|----------------------|
| `quadrillage` | Grille d'aide en gris clair | `\draw[quadrillage] (-1,-1) grid (5,4);` |
| `epais` | Trait épais (1.2pt) | `\draw[epais] (0,0) -- (2,2);` |
| `axe` | Flèche pour axes | `\draw[axe] (0,0) -- (5,0);` |

### Points

| Style | Description | Apparence |
|-------|-------------|-----------|
| `point` | Croix pour points (5pt, 0.8pt) | Croix noire |
| `point correction` | Croix rouge pour corrections (5pt, 1.2pt) | Croix rouge épaisse |
| `label point` | Police normale pour labels de points | Font normale, espacement 2pt |

### Segments et vecteurs

| Style | Description | Exemple |
|-------|-------------|---------|
| `segment` | Trait épais standard | `\draw[segment] (A) -- (B);` |
| `vecteur` | Flèche pour vecteurs | `\draw[vecteur] (0,0) -- (2,1);` |

### Couleurs standards

| Style | Couleur | Usage |
|-------|---------|-------|
| `couleur1` | Bleu | Premier élément d'une figure |
| `couleur2` | Rouge | Deuxième élément |
| `couleur3` | Vert foncé | Troisième élément |
| `prop` | Cyan/bleu clair | Propriétés, constructions |

### Cercles

| Style | Description | Exemple |
|-------|-------------|---------|
| `cercle` | Cercle avec trait épais | `\draw[cercle] (3,2) circle (1.5cm);` |
| `cercle epais` | Cercle très épais (1.2pt) | `\draw[cercle epais] (3,2) circle (2cm);` |
| `cercle pointille` | Cercle pointillé | `\draw[cercle pointille] (3,2) circle (1cm);` |

### Angles

| Style | Description |
|-------|-------------|
| `angle` | Style pour tracer des angles |
| `angle droit` | Style pour angles droits |

### Codages géométriques

| Style | Description | Usage |
|-------|-------------|-------|
| `codage segment` | Marque simple sur segment (égalité de longueurs) | `\draw[segment,codage segment] (A) -- (B);` |
| `codage segment double` | Double marque sur segment | `\draw[segment,codage segment double] (C) -- (D);` |
| `codage segment triple` | Triple marque sur segment | `\draw[segment,codage segment triple] (E) -- (F);` |

### Lignes remarquables

| Style | Description | Apparence |
|-------|-------------|-----------|
| `mediatrice` | Médiatrice | Trait pointillé gris |
| `bissectrice` | Bissectrice | Trait pointillé bleu |
| `hauteur` | Hauteur | Trait pointillé rouge |
| `mediane` | Médiane | Trait pointillé vert |

### Style général

| Style | Description |
|-------|-------------|
| `general` | Combinaison de `point`, `segment`, `couleur1` |

## Commandes disponibles

### Commande pour vecteurs

```latex
\Vecteur{nom}
```

Produit une flèche extensible au-dessus du nom de vecteur.

**Note importante :** Le package `esvect` (commande `\vv`) est incompatible avec LuaLaTeX + bfcours-fonts.

**Alternatives compatibles :**
- `\overrightarrow{#1}` - Flèche extensible (défaut)
- `\vec{#1}` - Petite flèche
- `\mathbf{#1}` - Gras (notation anglo-saxonne)
- `\boldsymbol{#1}` - Gras italique

### Repères orthonormés

#### Axe des abscisses

```latex
\XAxe{min}{max}{graduations}
```

**Paramètres :**
- `min` : valeur minimale de l'axe
- `max` : valeur maximale de l'axe
- `graduations` : liste des graduations à afficher (séparées par des virgules)

**Exemple :**
```latex
\XAxe{-1}{5}{1,2,3,4,5}
```

#### Axe des ordonnées

```latex
\YAxe{min}{max}{graduations}
```

**Paramètres :** Identiques à `\XAxe`

**Exemple :**
```latex
\YAxe{-1}{4}{1,2,3,4}
```

#### Origine

```latex
\origine
```

Trace l'origine O du repère.

### Points

#### Point standard

```latex
\point{x}{y}{label}{position}
```

**Paramètres :**
- `x` : coordonnée x du point
- `y` : coordonnée y du point
- `label` : étiquette du point (ex: A, B, M)
- `position` : position du label par rapport au point

**Positions possibles :**
- `above` : au-dessus
- `below` : en-dessous
- `left` : à gauche
- `right` : à droite
- `above left` : en haut à gauche
- `above right` : en haut à droite
- `below left` : en bas à gauche
- `below right` : en bas à droite

**Exemple :**
```latex
\point{3}{2}{A}{above right}
```

#### Point correction (rouge)

```latex
\pointCorrection{x}{y}{label}{position}
```

**Paramètres :** Identiques à `\point`

**Exemple :**
```latex
\pointCorrection{3}{2.5}{M}{above}
```

### Angles droits

```latex
\angleDroit[orientation]{sommet}{taille}
```

**Paramètres :**
- `orientation` (optionnel, défaut=1) : orientation du symbole (1 à 4)
  - `1` : en haut à droite (0°)
  - `2` : en haut à gauche (90°)
  - `3` : en bas à gauche (180°)
  - `4` : en bas à droite (270°)
- `sommet` : coordonnées du sommet de l'angle droit (peut être un point nommé ou des coordonnées)
- `taille` : taille du symbole (ex: 0.3)

**Exemples :**
```latex
\angleDroit[2]{5,1}{0.3}        % Orientation 2, au point (5,1)
\angleDroit{B}{0.3}             % Orientation 1 (défaut), au point B
```

## Exemples d'utilisation complète

### Repère orthonormé simple

```latex
\begin{tikzpicture}
    \draw[quadrillage] (-1,-1) grid (5,4);
    \XAxe{-1}{5}{1,2,3,4,5}
    \YAxe{-1}{4}{1,2,3,4}
    \origine
\end{tikzpicture}
```

### Triangle avec points et segments

```latex
\begin{tikzpicture}
    \draw[quadrillage] (-1,-1) grid (6,5);
    \XAxe{-1}{6}{1,2,3,4,5,6}
    \YAxe{-1}{5}{1,2,3,4,5}
    \origine

    % Points du triangle
    \point{1}{1}{A}{below left}
    \point{5}{1}{B}{below right}
    \point{5}{4}{C}{above right}

    % Segments avec couleurs
    \draw[segment,couleur1] (1,1) -- (5,1);
    \draw[segment,couleur2] (5,1) -- (5,4);
    \draw[segment,couleur3] (5,4) -- (1,1);
\end{tikzpicture}
```

### Triangle rectangle avec codages

```latex
\begin{tikzpicture}
    % Triangle
    \point{0}{0}{A}{below left}
    \point{3}{0}{B}{below right}
    \point{3}{2}{C}{above right}

    % Côtés avec codages d'égalité
    \draw[segment,couleur1,codage segment] (0,0) -- (3,0);
    \draw[segment,couleur2,codage segment double] (3,0) -- (3,2);
    \draw[segment,couleur3] (3,2) -- (0,0);

    % Angle droit en B
    \angleDroit[2]{3,0}{0.3}
\end{tikzpicture}
```

### Cercle et médiatrice

```latex
\begin{tikzpicture}[scale=1.2]
    \coordinate (A) at (0,0);
    \coordinate (B) at (4,0);
    \coordinate (M) at (2,0);

    % Segment
    \draw[segment] (A) -- (B);

    % Médiatrice
    \draw[mediatrice] (M) -- ++(0,3.5);

    % Cercle de centre M
    \draw[cercle,couleur1] (M) circle (2cm);

    % Points
    \node[point] at (A) {};
    \node[label point,below] at (A) {$A$};
    \node[point] at (B) {};
    \node[label point,below] at (B) {$B$};
\end{tikzpicture}
```

### Vecteurs

```latex
\begin{tikzpicture}
    \draw[quadrillage] (-1,-1) grid (6,5);
    \XAxe{-1}{6}{1,2,3,4,5,6}
    \YAxe{-1}{5}{1,2,3,4,5}
    \origine

    % Vecteurs avec différentes couleurs
    \draw[vecteur,couleur1] (1,1) -- (3,2) node[midway,above] {$\Vecteur{u}$};
    \draw[vecteur,couleur2] (2,3) -- (5,4) node[midway,above] {$\Vecteur{v}$};
\end{tikzpicture}
```
