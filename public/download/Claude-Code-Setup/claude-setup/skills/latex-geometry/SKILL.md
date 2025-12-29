---
name: latex-geometry
description: Skill pour créer des figures géométriques en LaTeX avec TikZ dans les documents bfcours. Utiliser pour tracer des repères orthonormés, points, segments, vecteurs, cercles, triangles, codages géométriques et lignes remarquables. Fournit un tikzset complet avec styles prédéfinis et commandes simplifiées.
---

# LaTeX Geometry - Figures géométriques avec TikZ

Skill spécialisé pour la création de figures géométriques en LaTeX avec TikZ dans le contexte de l'enseignement des mathématiques au collège et lycée.

## Quand utiliser ce skill

Utiliser ce skill de manière proactive lorsque :

1. **Création de figures géométriques** dans un document LaTeX bfcours
2. **Repères orthonormés** avec axes gradués et points
3. **Codages géométriques** (égalité de longueurs, angles droits, etc.)
4. **Vecteurs** dans un repère
5. **Cercles, triangles** et autres figures usuelles
6. **Lignes remarquables** (médiatrice, hauteur, médiane, bissectrice)

## Prérequis

Le tikzset nécessite :

```latex
\usepackage{bfcours}
\usepackage{bfcours-fonts}
\usetikzlibrary{decorations.markings,angles,quotes,positioning}
```

## Mise en place du tikzset

### Option 1 : Copier le tikzset dans le préambule

Copier le contenu de `assets/tikzset-geometrie.tex` dans le préambule du document LaTeX, après les `\usepackage` et avant `\begin{document}`.

### Option 2 : Inclure le fichier

Placer le fichier `assets/tikzset-geometrie.tex` dans le même répertoire que le document LaTeX et l'inclure avec :

```latex
\input{tikzset-geometrie.tex}
```

## Structure du tikzset

Le tikzset fournit :

1. **Styles prédéfinis** : `quadrillage`, `point`, `segment`, `vecteur`, `cercle`, `codage segment`, etc.
2. **Couleurs standards** : `couleur1` (bleu), `couleur2` (rouge), `couleur3` (vert), `prop` (cyan)
3. **Commandes simplifiées** : `\point`, `\XAxe`, `\YAxe`, `\origine`, `\angleDroit`, `\Vecteur`

## Utilisation dans le code

### Créer un repère orthonormé

Pour tracer un repère orthonormé avec quadrillage et axes gradués :

```latex
\begin{tikzpicture}
    \draw[quadrillage] (-1,-1) grid (5,4);
    \XAxe{-1}{5}{1,2,3,4,5}
    \YAxe{-1}{4}{1,2,3,4}
    \origine
\end{tikzpicture}
```

### Placer des points

Utiliser la commande `\point{x}{y}{label}{position}` :

```latex
\point{3}{2}{A}{above right}
\point{1}{4}{B}{above left}
```

Pour des points de correction (en rouge) :

```latex
\pointCorrection{3}{2.5}{M}{above}
```

### Tracer des segments et vecteurs

**Segments avec styles :**

```latex
\draw[segment,couleur1] (1,1) -- (5,1);
\draw[segment,couleur2,codage segment] (A) -- (B);  % Segment avec codage
```

**Vecteurs :**

```latex
\draw[vecteur,couleur1] (1,1) -- (3,2) node[midway,above] {$\Vecteur{u}$};
```

### Codages géométriques

Pour indiquer l'égalité de longueurs :

```latex
\draw[segment,codage segment] (A) -- (B);        % Simple barre
\draw[segment,codage segment double] (C) -- (D);  % Double barre
\draw[segment,codage segment triple] (E) -- (F);  % Triple barre
```

### Angles droits

Utiliser `\angleDroit[orientation]{sommet}{taille}` :

```latex
\angleDroit[2]{5,1}{0.3}  % Orientation 2 (en haut à gauche), au point (5,1)
\angleDroit{B}{0.3}        % Orientation 1 (défaut), au point B
```

Orientations disponibles :
- `1` : en haut à droite (0°)
- `2` : en haut à gauche (90°)
- `3` : en bas à gauche (180°)
- `4` : en bas à droite (270°)

### Cercles

```latex
\draw[cercle,couleur1] (3,2.5) circle (1.5cm);
\draw[cercle pointille,couleur2] (0,0) circle (2cm);
```

### Lignes remarquables

```latex
\draw[mediatrice] (M) -- ++(0,3.5);     % Médiatrice
\draw[hauteur] (C) -- (M);               % Hauteur
\draw[mediane] (C) -- (M);               % Médiane
\draw[bissectrice] (A) -- ++(2,1.5);    % Bissectrice
```

## Référence complète

Pour consulter la liste exhaustive de tous les styles et commandes disponibles, lire le fichier `references/styles-et-commandes.md` qui contient :

- Tableau de tous les styles avec descriptions et exemples
- Documentation détaillée de toutes les commandes
- Exemples d'utilisation complète

Pour rechercher un style ou une commande spécifique dans ce fichier de référence :

```bash
grep -i "style_recherché" .claude/skills/latex-geometry/references/styles-et-commandes.md
```

## Bonnes pratiques

1. **Couleurs cohérentes** : Utiliser `couleur1`, `couleur2`, `couleur3` pour différencier les éléments d'une même figure
2. **Labels de points** : Positionner les labels pour éviter les chevauchements (`above right`, `below left`, etc.)
3. **Codages** : Utiliser les codages géométriques pour indiquer les égalités de longueurs
4. **Échelle** : Utiliser `scale=...` dans l'environnement tikzpicture si nécessaire
5. **Vecteurs** : La commande `\Vecteur{nom}` utilise `\overrightarrow` par défaut (compatible bfcours-fonts)

## Note importante sur les vecteurs

Le package `esvect` (commande `\vv`) est **incompatible** avec LuaLaTeX + bfcours-fonts.

Utiliser à la place :
- `\Vecteur{nom}` : défini par défaut comme `\overrightarrow{nom}`
- Modifier la définition selon les préférences : `\vec`, `\mathbf`, `\boldsymbol`

## Exemple complet

```latex
\begin{tikzpicture}[scale=1.3]
    \draw[quadrillage] (-1,-1) grid (6,5);
    \XAxe{-1}{6}{1,2,3,4,5,6}
    \YAxe{-1}{5}{1,2,3,4,5}
    \origine

    % Points du triangle
    \point{1}{1}{A}{below left}
    \point{5}{1}{B}{below right}
    \point{5}{4}{C}{above right}

    % Triangle avec codages
    \draw[segment,couleur1,codage segment] (1,1) -- (5,1);
    \draw[segment,couleur2] (5,1) -- (5,4);
    \draw[segment,couleur3] (5,4) -- (1,1);

    % Angle droit en B
    \angleDroit[2]{5,1}{0.3}

    % Milieu de [AC]
    \pointCorrection{3}{2.5}{M}{above left}
\end{tikzpicture}
```

## Support et amélioration

Si un style ou une commande manquante est identifié, ajouter :
1. Le nouveau style dans `assets/tikzset-geometrie.tex`
2. La documentation dans `references/styles-et-commandes.md`
3. Un exemple d'utilisation dans ce fichier SKILL.md
