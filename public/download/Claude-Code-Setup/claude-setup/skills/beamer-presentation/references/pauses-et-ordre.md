# Règles strictes pour les pauses et l'ordre des frames

## Objectif

Créer des présentations Beamer avec des animations **efficaces** et **pédagogiques** sans créer un nombre excessif de pages PDF. Une présentation de 55 minutes doit faire environ 25-30 pages PDF maximum, pas 60-70 pages.

## Problème identifié

❌ **MAUVAISE PRATIQUE** : Trop de pauses créent trop de pages PDF
- 1 frame avec 4 pauses = 5 pages PDF
- 20 frames avec 3-4 pauses chacune = 80-100 pages PDF
- Présentation trop longue, navigation difficile, perte de tempo

✅ **BONNE PRATIQUE** : Pauses stratégiques et limitées
- 1 frame avec 1-2 pauses = 2-3 pages PDF maximum
- 20 frames avec 1-2 pauses chacune = 40-60 pages PDF
- Présentation fluide, tempo maîtrisé

## RÈGLE D'OR : Maximum 2-3 pauses par frame de solution

**IMPÉRATIF** : Une frame de solution ne doit JAMAIS contenir plus de 3 pauses.

### Structure idéale d'un exercice

```latex
% ========================================
% FRAME 1 : ÉNONCÉ (sans pause)
% ========================================
\begin{frame}{Exercice X : Titre}
  \begin{block}{Énoncé}
    Texte de l'énoncé complet...

    Données, questions, figure si nécessaire
  \end{block}

  \vspace{0.3cm}
  \textbf{Estimation :} Y minutes
\end{frame}

% ========================================
% FRAME 2 : SOLUTION (2 pauses max)
% ========================================
\begin{frame}{Exercice X : Solution}
  % Étape 1 : Méthode/formule à utiliser
  On utilise la formule :
  \[
    \text{Formule mathématique}
  \]

  \pause  % PAUSE 1 : Laisser réfléchir à la méthode

  % Étape 2 : Calcul complet d'un seul coup
  Application numérique :
  \begin{align*}
    \text{Ligne 1} \\
    \text{Ligne 2} \\
    \text{Ligne 3}
  \end{align*}

  \pause  % PAUSE 2 : Laisser digérer le calcul

  % Étape 3 : Résultat final encadré
  \begin{alertblock}{Résultat}
    $\text{Résultat final}$
  \end{alertblock}
\end{frame}
```

**Pages PDF générées** : 3 pages (frame initiale + 2 pauses)

## Règles par type de frame

### 1. Frame d'énoncé : ZÉRO pause

```latex
\begin{frame}{Exercice : Application}
  \begin{block}{Énoncé}
    Calculer le produit scalaire de $\vec{u}$ et $\vec{v}$.
  \end{block}

  \vspace{0.3cm}
  \textbf{Estimation :} 5 minutes
\end{frame}
```

**Pages PDF** : 1 page
**Raison** : L'énoncé doit être visible en entier immédiatement. Pas de surprise.

### 2. Frame de rappel : UNE pause maximum

```latex
\begin{frame}{Rappel : Formule du produit scalaire}
  \begin{block}{Formule}
    Pour deux vecteurs $\vec{u}$ et $\vec{v}$ :
    \[
      \vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}\| \times \cos(\alpha)
    \]
  \end{block}

  \pause

  \begin{exampleblock}{Points clés}
    \begin{itemize}
      \item Angle entre $0°$ et $180°$
      \item Valeurs remarquables : $\cos(60°) = \frac{1}{2}$
    \end{itemize}
  \end{exampleblock}
\end{frame}
```

**Pages PDF** : 2 pages
**Raison** : Formule d'abord, puis points clés. Une seule pause pour séparer.

### 3. Frame de solution simple : DEUX pauses maximum

**Exercice simple** (difficulté 1) = calcul direct en 2-3 lignes

```latex
\begin{frame}{Exercice 1 : Solution}
  On applique la formule :
  \[
    \vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}\| \times \cos(\alpha)
  \]

  \pause  % PAUSE 1

  Application numérique :
  \[
    \vec{u} \cdot \vec{v} = 2 \times 3 \times \cos(60°) = 6 \times \frac{1}{2} = 3
  \]

  \pause  % PAUSE 2

  \begin{alertblock}{Résultat}
    $\vec{u} \cdot \vec{v} = 3$
  \end{alertblock}
\end{frame}
```

**Pages PDF** : 3 pages
**Structure** :
1. Formule seule
2. Formule + calcul
3. Formule + calcul + résultat

❌ **NE PAS FAIRE** : Pause entre chaque ligne de calcul !

```latex
% MAUVAIS EXEMPLE - 5 pauses = 6 pages !
\begin{frame}{Exercice 1 : Solution}
  On applique la formule :
  \[
    \vec{u} \cdot \vec{v} = \|\vec{u}\| \times \|\vec{v}\| \times \cos(\alpha)
  \]

  \pause  % Pause 1

  Application numérique :
  \begin{align*}
    \vec{u} \cdot \vec{v} &= 2 \times 3 \times \cos(60°) \\
    \pause  % Pause 2 - INUTILE !
    &= 6 \times \frac{1}{2} \\
    \pause  % Pause 3 - INUTILE !
    &= 3
  \end{align*}

  \pause  % Pause 4 - INUTILE !

  \begin{alertblock}{Résultat}
    $\vec{u} \cdot \vec{v} = 3$
  \end{alertblock}
\end{frame}
```

**Pages PDF** : 6 pages (BEAUCOUP TROP !)

### 4. Frame de solution moyenne : TROIS pauses maximum

**Exercice moyen** (difficulté 2) = calcul en plusieurs étapes distinctes

```latex
\begin{frame}{Exercice 4 : Solution}
  \textbf{Coordonnées :} $E(0;0)$, $F(4;0)$, $G(4;7)$, $H(0;7)$

  \pause  % PAUSE 1 : Laisser visualiser les coordonnées

  \textbf{Calcul 1 :} $\vec{EG}\begin{pmatrix}4\\7\end{pmatrix}$ et $\vec{FH}\begin{pmatrix}-4\\7\end{pmatrix}$

  \[
    \vec{EG}\cdot\vec{FH} = 4 \times (-4) + 7 \times 7 = \boxed{33}
  \]

  \pause  % PAUSE 2 : Laisser digérer le calcul 1

  \textbf{Calcul 2 :} $\vec{JL}\begin{pmatrix}-4\\0\end{pmatrix}$ et $\vec{EG}\begin{pmatrix}4\\7\end{pmatrix}$

  \[
    \vec{JL}\cdot\vec{EG} = (-4) \times 4 + 0 \times 7 = \boxed{-16}
  \]
\end{frame}
```

**Pages PDF** : 3 pages
**Structure** :
1. Coordonnées seules
2. Coordonnées + calcul 1
3. Coordonnées + calcul 1 + calcul 2

❌ **NE PAS FAIRE** : Pause entre chaque vecteur et son résultat !

```latex
% MAUVAIS EXEMPLE - 5 pauses = 6 pages !
\begin{frame}{Exercice 4 : Solution}
  \textbf{Coordonnées :} $E(0;0)$, $F(4;0)$, $G(4;7)$, $H(0;7)$

  \pause  % Pause 1

  \textbf{Calcul 1 :} $\vec{EG}\begin{pmatrix}4\\7\end{pmatrix}$ et $\vec{FH}\begin{pmatrix}-4\\7\end{pmatrix}$

  \pause  % Pause 2 - INUTILE !

  \[
    \vec{EG}\cdot\vec{FH} = 4 \times (-4) + 7 \times 7 = \boxed{33}
  \]

  \pause  % Pause 3 - INUTILE !

  \textbf{Calcul 2 :} $\vec{JL}\begin{pmatrix}-4\\0\end{pmatrix}$ et $\vec{EG}\begin{pmatrix}4\\7\end{pmatrix}$

  \pause  % Pause 4 - INUTILE !

  \[
    \vec{JL}\cdot\vec{EG} = (-4) \times 4 + 0 \times 7 = \boxed{-16}
  \]
\end{frame}
```

**Pages PDF** : 6 pages (BEAUCOUP TROP !)

### 5. Frame avec liste d'items : Utiliser `[<+->]` intelligemment

✅ **BONNE PRATIQUE** : Révélation progressive avec `[<+->]`

```latex
\begin{frame}{Méthode de calcul}
  \begin{enumerate}[<+->]  % Révélation automatique
    \item Déterminer les coordonnées
    \item Calculer le produit scalaire
    \item En déduire l'angle
  \end{enumerate}
\end{frame}
```

**Pages PDF** : 4 pages (1 initiale + 3 items)

❌ **MAUVAISE PRATIQUE** : Pause manuelle entre chaque item

```latex
\begin{frame}{Méthode de calcul}
  \begin{enumerate}
    \item Déterminer les coordonnées
    \pause
    \item Calculer le produit scalaire
    \pause
    \item En déduire l'angle
  \end{enumerate}
\end{frame}
```

**Pages PDF** : 3 pages (identique mais code moins élégant)

## Règles spécifiques par contexte

### Collège : 2-3 pauses par frame autorisées

Les élèves de collège ont besoin de plus de guidage visuel.

```latex
\begin{frame}{Exercice : Calcul}
  \textbf{Données :} $a = 5$ et $b = 3$

  \pause

  \textbf{Calcul :}
  \[
    a + b = 5 + 3 = 8
  \]

  \pause

  \begin{alertblock}{Résultat}
    $a + b = 8$
  \end{alertblock}
\end{frame}
```

**Pages PDF** : 3 pages (acceptable pour collège)

### Lycée : 2 pauses par frame maximum

Les élèves de lycée peuvent suivre des calculs plus longs d'un seul coup.

```latex
\begin{frame}{Exercice : Dérivée}
  On calcule la dérivée de $f(x) = x^2 + 3x$ :

  \pause

  \[
    f'(x) = 2x + 3
  \]

  \pause

  \begin{alertblock}{Résultat}
    $f'(x) = 2x + 3$
  \end{alertblock}
\end{frame}
```

**Pages PDF** : 3 pages

### Académique : 1-2 pauses par frame maximum

Public expert, révélation minimale.

```latex
\begin{frame}{Théorème}
  \begin{theorem}
    Pour tout espace de Hilbert $H$, on a...
  \end{theorem}

  \pause

  \begin{proof}
    Démonstration en 3 lignes...
  \end{proof}
\end{frame}
```

**Pages PDF** : 2 pages

## Ordre strict des frames pour un exercice

**STRUCTURE OBLIGATOIRE** :

```
Frame 1 : ÉNONCÉ
Frame 2 : SOLUTION (ou MÉTHODE + SOLUTION)
Frame 3 (optionnel) : VARIANTE ou REMARQUE
```

❌ **NE PAS FAIRE** :
- Répéter l'énoncé dans la frame de solution
- Séparer la méthode et le calcul en 2 frames (sauf si exercice très long)
- Créer une frame juste pour le résultat

✅ **FAIRE** :
- Énoncé complet dans frame dédiée
- Solution complète dans UNE frame (méthode + calcul + résultat)
- Maximum 2-3 pauses dans la frame de solution

## Exemple complet d'exercice bien structuré

```latex
% ========================================
% EXERCICE 3 : PRODUIT SCALAIRE AVEC COORDONNÉES
% ========================================

% Frame 1 : ÉNONCÉ (0 pause)
\begin{frame}{Exercice 3 : Produits scalaires directs}
  \begin{block}{Énoncé}
    Calculer les produits scalaires suivants :
    \begin{enumerate}
      \item $\vec{u}\cdot\vec{v}$ avec $\vec{u}\begin{pmatrix}15\\-8\end{pmatrix}$ et $\vec{v}\begin{pmatrix}6\\9\end{pmatrix}$
      \item $\vec{s}\cdot\vec{t}$ avec $\vec{s}\begin{pmatrix}-1\\-2\end{pmatrix}$ et $\vec{t}\begin{pmatrix}-3\\-4\end{pmatrix}$
    \end{enumerate}
  \end{block}

  \vspace{0.3cm}
  \textbf{Estimation :} 5 minutes
\end{frame}

% Frame 2 : SOLUTION (2 pauses)
\begin{frame}{Exercice 3 : Solution}
  \textbf{1.} $\vec{u}\cdot\vec{v} = 15 \times 6 + (-8) \times 9 = 90 - 72 = \boxed{18}$

  \pause  % PAUSE 1 : Séparer les deux calculs

  \vspace{0.5cm}

  \textbf{2.} $\vec{s}\cdot\vec{t} = (-1) \times (-3) + (-2) \times (-4) = 3 + 8 = \boxed{11}$
\end{frame}
```

**Total pages PDF** : 3 pages (1 énoncé + 2 solution)

**Temps de présentation** : ~5 minutes
- Énoncé : 30 secondes
- Pause réflexion : 2 minutes
- Calcul 1 : 1 minute
- Pause : 30 secondes
- Calcul 2 : 1 minute

## Comptage des pages PDF

**Formule** : `Pages PDF = Nombre de frames + Total des pauses`

**Objectif pour 55 minutes** :
- ~15-20 frames
- ~1-2 pauses par frame en moyenne
- **Total visé : 25-35 pages PDF**

**Alerte si** : Pages PDF > 2 × Nombre de frames
→ Trop de pauses, simplifier !

## Vérification finale

**Checklist pauses** :

- [ ] Aucune frame d'énoncé ne contient de pause
- [ ] Chaque frame de solution contient ≤ 3 pauses
- [ ] Pas de pause entre chaque ligne de calcul
- [ ] Pas de pause juste pour afficher un résultat encadré si le calcul est déjà affiché
- [ ] Les pauses servent à séparer des **étapes conceptuelles**, pas des lignes
- [ ] Nombre de pages PDF ≈ 1,5-2 × nombre de frames (pas 3-4×)

**Checklist ordre** :

- [ ] Chaque exercice suit : Énoncé → Solution
- [ ] Pas de répétition de l'énoncé dans la solution
- [ ] Méthode et calcul dans la MÊME frame
- [ ] Résultat dans la même frame que le calcul

## Règle de décision : Faut-il une pause ?

**OUI si** :
- Changement d'étape conceptuelle (méthode → calcul, calcul 1 → calcul 2)
- Besoin de laisser réfléchir les élèves
- Séparation logique entre deux idées distinctes

**NON si** :
- Juste une nouvelle ligne de calcul dans la même étape
- Juste pour afficher un résultat qui découle immédiatement
- Juste pour "faire joli" ou "créer du suspense"

## Résumé : Les 5 commandements des pauses

1. **Maximum 2-3 pauses par frame de solution**, jamais plus
2. **Aucune pause dans les frames d'énoncé**
3. **Une pause = une étape conceptuelle**, pas une ligne de calcul
4. **Calcul complet d'un coup**, pas ligne par ligne avec des pauses
5. **Pages PDF cible ≈ 1,5-2 × nombre de frames**, pas 3-4×

---

**En respectant ces règles, vos présentations seront fluides, efficaces et adaptées au temps imparti !**
