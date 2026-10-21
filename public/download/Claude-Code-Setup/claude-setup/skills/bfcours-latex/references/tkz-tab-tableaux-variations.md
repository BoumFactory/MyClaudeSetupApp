# Tableaux de variations avec `tkz-tab`

Référence pour la création de tableaux de variations en LaTeX via le package `tkz-tab` (chargé automatiquement par bfcours). Couvre la syntaxe de base et les **astuces pour cas particuliers** : valeurs intermédiaires non critiques (`\tkzTabIma`), `f'` qui s'annule sans changer de signe, structure de TV à compléter par l'élève via `\ifcorrection`.

## Syntaxe de base

Un tableau de variations se construit toujours dans un environnement `tikzpicture`, lui-même centré dans un `\begin{center}...\end{center}` :

```latex
\begin{center}
\begin{tikzpicture}
\tkzTabInit[lgt=2, espcl=2.5]{$x$/1, $f'(x)$/1, $f$/2}{$-\infty$, $1$, $3$, $+\infty$}
\tkzTabLine{, -, z, +, z, -,}
\tkzTabVar{+/, -/$0$, +/$4\,\bfe^{-1}$, -/}
\end{tikzpicture}
\end{center}
```

### `\tkzTabInit[options]{lignes}{colonnes}`

- **Options communes** :
  - `lgt=<dim>` : largeur (en cm) du label de chaque ligne (colonne « variable »).
  - `espcl=<dim>` : espacement (en cm) entre deux valeurs de $x$ successives.
- **lignes** : liste `$label$/hauteur` séparée par des virgules. La hauteur est en cm.
- **colonnes** : valeurs de $x$ aux bornes et points critiques (séparées par des virgules). Inclut $-\infty$ et $+\infty$ si la fonction est définie sur $\R$. Le **nombre de colonnes** est la longueur de cette liste.

### `\tkzTabLine{, val_1, sym_1, val_2, sym_2, ..., val_M, }`

Ligne du signe de la dérivée. La syntaxe alterne :

- `val_i` : signe sur l'intervalle (`+`, `-`).
- `sym_i` : symbole au point critique (`z` pour zéro avec changement de signe, `d` pour double, `t` pour zéro touchant — pas de changement).
- Commencer et terminer la liste par une virgule vide (cellules de bordure).

Pour 4 colonnes (3 intervalles, 2 points critiques) :

```latex
\tkzTabLine{, +, z, -, z, +,}
%          ^                ^
%          bordure          bordure
%             ^  ^  ^  ^  ^
%             |  |  |  |  +-- signe sur ]3 ; +∞[
%             |  |  |  +----- zéro en x = 3
%             |  |  +-------- signe sur ]1 ; 3[
%             |  +----------- zéro en x = 1
%             +-------------- signe sur ]-∞ ; 1[
```

### `\tkzTabVar{cellule_1, cellule_2, ..., cellule_N}`

Ligne des variations de $f$. **Une cellule par colonne** (N = nombre de valeurs de $x$).

Chaque cellule a la forme `direction/valeur` :

- `+/` : sommet d'une flèche montante (en haut).
- `-/` : creux d'une flèche descendante (en bas).
- `R/` : point intermédiaire **sans valeur propre** (la flèche traverse sans rupture). Voir astuce `\tkzTabIma` ci-dessous.
- `D/` : descente directe (peu utilisé).
- `U/` : montée directe (peu utilisé).

La `valeur` après `/` est ce qu'on affiche au point critique (laisser vide aux bornes $-\infty$ / $+\infty$).

## Astuce `\tkzTabIma` — Valeur intermédiaire non critique

`\tkzTabIma{from_col}{to_col}{at_col}{label}` permet d'afficher une **valeur intermédiaire** au passage d'une flèche, **sans ajouter de colonne** au tableau ni casser la monotonie.

- `from_col`, `to_col` : numéros des colonnes (1-indexé) qui bornent la portion de flèche sur laquelle on veut placer le label.
- `at_col` : colonne où afficher le label (doit être entre `from_col` et `to_col`).
- `label` : étiquette à afficher au-dessus de la flèche.

### Cas 1 — Valeur de référence sur une flèche monotone

Le cours sur l'exponentielle utilise cette astuce pour marquer $\bfe^0 = 1$ et $\bfe^1 = \bfe$ sur la flèche monotone croissante :

```latex
\tkzTabInit{$x$/1, $\bfe^x$/1.8}{$-\infty$, $0$, $1$, $+\infty$}
\tkzTabVar{-/$0$, R/, R/, +/$+\infty$}
\tkzTabIma{1}{4}{2}{$1$}        % e^0 = 1 affiché au-dessus de la colonne 2 (x = 0)
\tkzTabIma{1}{4}{3}{$\bfe$}     % e^1 = e affiché au-dessus de la colonne 3 (x = 1)
```

- `\tkzTabVar` n'a que **deux valeurs propres** (en colonnes 1 et 4) ; les colonnes 2 et 3 sont en `R/` (intermédiaires).
- `\tkzTabIma{1}{4}{...}` place les valeurs **sur** la flèche allant de la colonne 1 (où la fonction vaut $0$) à la colonne 4 (où elle vaut $+\infty$).

Référence : `1. Cours/1ere_spe/Sequence-Fonction_exponentielle/Cours_Fonction_exponentielle/sections/Graphique/tableau_variation.tex`.

### Cas 2 — `f'` qui s'annule SANS changer de signe (CAS TRICKY)

Quand $f'(x_0) = 0$ mais $f'$ ne change pas de signe en $x_0$ (typiquement à cause d'un facteur $(x - x_0)^{2}$), le tableau a une flèche monotone qui « passe » par $x_0$. **Deux approches** :

#### ❌ Approche naïve (visuellement ambiguë)

```latex
% f(x) = (x³ - 2x² + 3x)·e^(-x)  →  f'(x) = (x-1)²(3-x)·e^(-x)
% f' s'annule en x=1 SANS changer de signe, et en x=3 EN changeant.
\tkzTabInit{$x$/1, $f'(x)$/1, $f$/2}{$-\infty$, $1$, $3$, $+\infty$}
\tkzTabLine{, +, z, +, z, -,}
\tkzTabVar{-/, +/$\frac{2}{\bfe}$, +/$\frac{18}{\bfe^{3}}$, -/}
```

Visuellement : **deux flèches montantes consécutives** qui se touchent en $f(1) = 2/\bfe$. Cela suggère (à tort) une rupture dans la monotonie alors que $f$ est strictement croissante sur $]-\infty\,;\,3]$.

#### ✅ Approche correcte avec `\tkzTabIma`

```latex
\tkzTabInit{$x$/1, $f'(x)$/1, $f$/2}{$-\infty$, $1$, $3$, $+\infty$}
\tkzTabLine{, +, z, +, z, -,}
\tkzTabVar{-/, R/, +/$\frac{18}{\bfe^{3}}$, -/}
\tkzTabIma{1}{3}{2}{$\dfrac{2}{\bfe}$}
```

- `R/` en colonne 2 : la flèche **traverse** $x = 1$ sans rupture.
- `\tkzTabIma{1}{3}{2}{$2/\bfe$}` affiche la valeur $f(1) = 2/\bfe$ comme point d'intérêt au-dessus de la colonne 2, sur la flèche montante allant de la colonne 1 (-∞) à la colonne 3 (où $f$ atteint son maximum $18/\bfe^{3}$).

**Résultat** : une seule flèche montante continue de $-\infty$ à $x = 3$, avec $f(1)$ marqué au passage. La monotonie est claire.

**Règle pratique** : dès qu'on a un zéro de $f'$ qui ne change pas de signe (racine double, racine de multiplicité paire), utiliser `R/` + `\tkzTabIma` pour marquer la valeur intermédiaire **sans casser la flèche**.

## Astuce — Structure de TV vide à compléter par l'élève

Pour une fiche d'exercices **interactive** (mode élève), afficher uniquement la grille (valeurs de $x$ aux bornes et points critiques) en pilotant `\tkzTabLine` et `\tkzTabVar` via `\ifcorrection` :

```latex
\begin{center}
\begin{tikzpicture}
\tkzTabInit[lgt=1.6, espcl=3]{$x$/0.9, $f'(x)$/0.9, $f$/1.7}{$-\infty$, $\frac{1}{2}$, $+\infty$}
\ifcorrection
\tkzTabLine{, -, z, +,}
\tkzTabVar{+/, -/$-2\,\bfe^{\frac{3}{2}}$, +/}
\fi
\end{tikzpicture}
\end{center}
```

- **Mode élève** (`\ifcorrection` faux) : seul `\tkzTabInit` est exécuté → grille vide avec la ligne des $x$ remplie, les lignes $f'(x)$ et $f$ entièrement à compléter à la main.
- **Mode prof / correction** (`\ifcorrection` vrai) : grille complète avec signes et flèches.

Référence projet : `1. Cours/1ere_spe/Revisions-bac/Etude_de_fonctions_poly_exp/enonce.tex` (Exo 1).

## Récapitulatif — Symboles `\tkzTabLine` et `\tkzTabVar`

| Symbole | Usage | Endroit |
|---------|-------|---------|
| `+`, `-` | Signe sur un intervalle | `\tkzTabLine` |
| `z` | Zéro **avec** changement de signe | `\tkzTabLine` |
| `d` | Double (annulation double, change de signe selon contexte) | `\tkzTabLine` |
| `t` | Zéro **sans** changement de signe (touche l'axe) | `\tkzTabLine` |
| `+/val` | Sommet (flèche montante atteint la valeur) | `\tkzTabVar` |
| `-/val` | Creux (flèche descendante atteint la valeur) | `\tkzTabVar` |
| `R/` | Cellule intermédiaire **sans valeur** (flèche traverse) | `\tkzTabVar` |
| `D/`, `U/` | Descente/montée directe (variantes) | `\tkzTabVar` |

## Conseils pratiques

1. **Toujours centrer** le `tikzpicture` dans un `\begin{center}...\end{center}`.
2. **Compter les cellules** de `\tkzTabVar` : il en faut exactement autant que de colonnes dans `\tkzTabInit`.
3. **Compter les entrées** de `\tkzTabLine` : pour $N$ intervalles séparés par $N - 1$ points critiques, il faut $2(N-1) + 1 + 2 = 2N + 1$ entrées (bordures vides incluses).
4. **Bornes vides** : pour $-\infty$ et $+\infty$, laisser la valeur vide après `/` dans `\tkzTabVar` (ex. `+/`).
5. **Format des valeurs** : utiliser `\dfrac` plutôt que `\frac` dans les cellules de variations pour une meilleure lisibilité.
6. **Largeur du tableau** : ajuster `espcl` (espacement entre colonnes) si le tableau est trop large ou trop étroit. Valeurs typiques : 2 à 3.5.
7. **Hauteur de la ligne de variation** : `$f$/2` est une bonne valeur par défaut. Augmenter à 2.5 ou 3 si beaucoup d'allers-retours de la flèche.

## Cas extrêmes — Quand utiliser autre chose

- Tableaux de signes seuls (sans variations) : utiliser `\tkzTabInit` avec deux lignes seulement (`$x$/0.7, Signe de $f'(x)$/0.7`) et `\tkzTabLine` (pas de `\tkzTabVar`).
- Tableaux avec valeurs intermédiaires multiples sur une seule flèche : enchaîner plusieurs `\tkzTabIma` en spécifiant `at_col` différent pour chaque valeur (voir cas 1 ci-dessus).
- Tableaux où la fonction n'est pas définie sur $\R$ : remplacer $-\infty$ et $+\infty$ par les bornes du domaine, et adapter les symboles d'annulation aux bornes (pas de zéro de $f'$ aux bornes si on étudie sur $[a, b]$).
