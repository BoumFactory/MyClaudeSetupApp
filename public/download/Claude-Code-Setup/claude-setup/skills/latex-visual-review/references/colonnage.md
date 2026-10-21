# Colonnage : le levier principal

À lire à l'**Étape 4** (audit) et à l'**Étape 5** (batch) du SKILL.md, dès qu'un énoncé ou un bloc de cours peut passer côte à côte. Couvre les Leviers 1 à 4, les Recettes A à F, les Techniques T3 et T4 et les signaux d'arrêt.

Référence de syntaxe : `bfcours-latex/references/bfcours-conventions.md`, sections `MultiColonnes` et `tcbenumerate` (signature `\begin{tcbenumerate}[nbCol][nbStart][num|alph]`, trois arguments optionnels seulement ; `\begin{MultiColonnes}{nbCol}[options]`).

**Rappels de syntaxe valables pour tout ce fichier** :

- toujours une ligne vide avant `\begin{MultiColonnes}` (sinon rendu incorrect) ;
- ne jamais oublier l'argument obligatoire `{n}` de `MultiColonnes` (sinon cascade d'erreurs jusqu'à `\end{document}`) ;
- jamais de colonnage entre `\exocorrection` et `\end{EXO}` : la correction reste en une colonne (projection item par item).

---

## Levier 1 — Augmenter `[n]` d'un `tcbenumerate` d'énoncé

Recommandation bfcours : utiliser le plus souvent possible `tcbenumerate[2]`, tant que la présentation reste cohérente.

| Profil des items | Choix |
|---|---|
| 2 items courts (1 ligne) | `[2]` |
| 3 items courts (1 ligne) | `[3]` |
| 4-6 items moyens (1-2 lignes) | `[2]` |
| Items longs (3+ lignes ou maths affichées) | `[1]` |
| 1 item long + plusieurs courts | `[1]` + sous-`tcbenumerate[2]` ou `[3]` (Levier 3) |
| 1 item conceptuellement « lourd » + 1 court | `[3]` + `raster multicolumn=2` / `=1` (asymétrique) |
| Un seul item wrappe alors que ses voisins tiennent sur une ligne | Technique T4 |

Avant de redescendre à `[1]`, essayer de raccourcir l'énoncé sans en changer le sens (« suivant les valeurs de $x$ » → « selon $x$ »).

```latex
% AVANT : trois lignes
\begin{tcbenumerate}
    \tcbitem \tcbitempoint{2}\acc{Calculer} $E(X)$.
    \tcbitem \tcbitempoint{2}\acc{Calculer} $V(X)$.
    \tcbitem \tcbitempoint{1}\acc{En déduire} $\sigma(X)$.
\end{tcbenumerate}
% APRÈS : une ligne
\begin{tcbenumerate}[3]
    ... mêmes items ...
\end{tcbenumerate}
```

**Variante asymétrique** : deux items de longueur voisine mais de charge différente (« Dresser le tableau de la loi » / « Calculer $P(X>0)$ ») → l'item lourd reçoit 2/3, à gauche par convention de lecture.

```latex
\begin{tcbenumerate}[3]
    \tcbitem[raster multicolumn=2] \acc{Dresser} le tableau de la loi.
    \tcbitem[raster multicolumn=1] \acc{Calculer} $P(X > 0)$.
\end{tcbenumerate}
```

---

## Levier 2 — `MultiColonnes` pour mettre deux blocs côte à côte

Quand deux ou trois blocs apparentés sont empilés alors qu'ils tiendraient côte à côte.

| Configuration empilée | Refonte | Bordure |
|---|---|---|
| Tableau de loi + questions | Tableau à gauche, questions à droite | Aucune (Recette A) |
| Deux tableaux (jeu A / jeu B) | Côte à côte | Légère si confusion possible (Recette B) |
| Code Python + tableau | Code à gauche | `boxrule=0.4pt` autour du code |
| Méthode 1 / Méthode 2 | Côte à côte | Bordure + titres obligatoires (Recette C) |
| Tableau de variations + tableau de signes | Selon la largeur | Optionnelle |
| Deux définitions parallèles avec `\encadrer` | Côte à côte, asymétrie selon les formules | `colframe=black!15, boxrule=0.4pt` (Recette E) |
| Formule `\encadrer` + commentaire « Pourquoi / Lecture » | Formule étroite, commentaire large | Aucune (Recette F) |

**Recette A — sans bordure** (séparation naturelle) :

```latex
\begin{MultiColonnes}{2}
    \tcbitem[halign=center]
        \begin{tcbtab}[Loi de $X$]{|c|c|c|c|}
        $x_i$ & $-10$ & $0$ & $30$ \\ \hline
        $P(X = x_i)$ & $0{,}5$ & $0{,}3$ & $0{,}2$ \\ \hline
        \end{tcbtab}
    \tcbitem
        \begin{tcbenumerate}[1]
            \tcbitem \acc{Calculer} $E(X)$ et $\sigma(X)$.
            \tcbitem Quel jeu un joueur prudent doit-il choisir ?
        \end{tcbenumerate}
\end{MultiColonnes}
```

**Recette B — séparation discrète** : `\begin{MultiColonnes}{2}[colframe=black!20, boxrule=0.4pt]`.

**Recette C — comparaison titrée** :

```latex
\begin{MultiColonnes}{2}[colframe=\currentAccentColor, boxrule=0.4pt, coltitle=white]
    \tcbitem[title=Méthode 1 -- par la définition] $V(X) = \sum p_i \big(x_i - E(X)\big)^2$ ...
    \tcbitem[title=Méthode 2 -- König-Huygens] $V(X) = E(X^2) - E(X)^2$ ...
\end{MultiColonnes}
```

---

## Levier 3 — Imbrication asymétrique

Une question longue de contexte suivie de sous-questions courtes. Respecter la hiérarchie 1.a / 1.b de l'énoncé source : ne pas l'aplatir.

```latex
\begin{tcbenumerate}[1]
\tcbitem \tcbitempoint{4}On considère $f$ définie sur $\R$ par $f(x) = x^2 - 3x + 2$.
    \begin{tcbenumerate}[2][1][alph]
        \tcbitem \acc{Étudier} les variations de $f$.
        \tcbitem \acc{Tracer} la courbe représentative.
    \end{tcbenumerate}
\tcbitem \tcbitempoint{3}\acc{Déterminer} les racines.
\end{tcbenumerate}
```

**Recette D — bordure au premier niveau** (règle bfcours : en cas d'imbrication dense, le premier niveau porte une bordure). `tcbenumerate` n'accepte pas d'options graphiques : la bordure se pose **sur le `\tcbitem`** qui contient le sous-`tcbenumerate`.

```latex
\begin{tcbenumerate}[3]
    \tcbitem Premier item.
    \tcbitem[raster multicolumn=2, colframe=black, boxrule=0.4pt] Second item :
        \begin{tcbenumerate}[2][1][alph]
            \tcbitem Sous-item a
            \tcbitem Sous-item b
        \end{tcbenumerate}
\end{tcbenumerate}
```

Il est aussi possible de fermer un `tcbenumerate` et de le rouvrir plus bas avec une autre géométrie : `\begin{tcbenumerate}[2][4]` reprend la numérotation à 4.

---

## Levier 4 — Paramètres graphiques de clarté

Toute compaction perd de la séparation naturelle : la compenser.

| Option | Effet | Quand |
|---|---|---|
| `colframe=\currentAccentColor` | Cadre à la couleur de l'environnement | Deux contenus fortement comparables |
| `boxrule=0.4pt` | Filet fin | Compromis idéal lisibilité / discrétion |
| `boxrule=1pt` | Filet visible | 3+ colonnes serrées, contenus hétérogènes |
| `colback=white` | Fond blanc | Le parent a une teinte qui bave |
| `title=…`, `coltitle=white` | Titre intégré | « Méthode 1 / 2 », « Jeu A / B » |
| `raster column skip=5pt` | Espace entre colonnes | Défaut bfcours ; jamais sous 3pt |
| `raster row skip=2pt` | Espace entre lignes | Défaut bfcours |
| `raster equal height=rows` | Hauteurs égales par ligne | Colonnes visuellement déséquilibrées |

Pas de double bordure : un `MultiColonnes` posé dans une `Propriete` ou une `Definition` déjà encadrée reste sans cadre, sauf pour séparer deux formules parallèles (Recette E).

### Largeurs asymétriques : grille virtuelle + `raster multicolumn`

`MultiColonnes{N}` répartit à parts égales. Pour des largeurs inégales, déclarer une grille de `N` colonnes virtuelles et attribuer `raster multicolumn=k` à chaque `\tcbitem`.

```latex
\begin{MultiColonnes}{5}            % 60/40
    \tcbitem[raster multicolumn=3] ... tableau ...
    \tcbitem[raster multicolumn=2] ... questions ...
\end{MultiColonnes}
% 35/65 : grille {20} et multicolumn=7 / =13 ; au pour cent près : grille {100}
% trois blocs 25/50/25 : grille {4} et multicolumn=1 / =2 / =1
```

| Contenus | Répartition |
|---|---|
| Tableau de 2-3 colonnes / énoncé long | 35/65 ou 40/60 |
| Tableau de 4-5 colonnes / questions courtes | 60/40 |
| Code Python / commentaire | 70/30 |

Si le 50/50 étire le tableau ou fait déborder les questions (`Overfull \hbox`), tester une largeur asymétrique avant toute autre piste.

---

## Centrer un élément dans une colonne (Technique T3)

Un `tcbtab`, un `\encadrer` ou une figure posé dans un `\tcbitem` s'aligne **à gauche** par défaut.

- **Cellule à contenu centré unique** (formule seule, tableau seul, figure seule) : option `halign=center` sur le `\tcbitem` (ajouter `valign=center` pour l'aligner verticalement sur une voisine plus haute).
- **Cellule qui mélange texte et élément centré** : `\begin{center}…\end{center}` autour de l'élément seul, sinon `halign` centrerait aussi le texte.
- **Cellule contenant un `tcbenumerate`** : pas de centrage, l'énumération s'aligne à gauche.

```latex
% ANTI-PATTERN : \par et espace parasites
\tcbitem[raster multicolumn=2]
    \begin{center}
    \encadrer[defi]{$X : \omega \in \Omega \longmapsto X(\omega) \in \R$}
    \end{center}
% CORRECT
\tcbitem[raster multicolumn=2, halign=center]
    \encadrer[defi]{$X : \omega \in \Omega \longmapsto X(\omega) \in \R$}
```

Détection : tout `\tcbitem` suivi immédiatement d'un `\begin{center}` qui se ferme juste avant le `\tcbitem` suivant ou la fin du `MultiColonnes` est candidat.

---

## Recettes E et F — formules encadrées dans un cours

**Recette E — deux définitions ou propriétés parallèles** (variance et écart-type). Bordure légère obligatoire : sans elle, les deux blocs paraissent fondus. Formule longue à gauche (3/5), courte à droite (2/5) ; très longue : 7/3 sur `{10}` ou 13/7 sur `{20}`.

```latex
% E.a — formule seule par colonne : halign=center
\begin{MultiColonnes}{2}[colframe=black!15, boxrule=0.4pt]
    \tcbitem[halign=center] \encadrer[defi]{$X : \omega \in \Omega \longmapsto X(\omega) \in \R$}
    \tcbitem[halign=center] \encadrer[defi]{$X(\Omega) = \{x_1, x_2, \dots, x_n\}$}
\end{MultiColonnes}

% E.b — phrase d'introduction + formule : center localisé
\begin{MultiColonnes}{5}[colframe=black!15, boxrule=0.4pt]
    \tcbitem[raster multicolumn=3]
        \textbullet\ La \voc{variance} de $X$ est définie par :
        \begin{center}\encadrer[defi]{$V(X) = \sum p_i (x_i - E(X))^2$}\end{center}
    \tcbitem[raster multicolumn=2]
        \textbullet\ L'\voc{écart-type} de $X$ est défini par :
        \begin{center}\encadrer[defi]{$\sigma(X) = \sqrt{V(X)}$}\end{center}
\end{MultiColonnes}
```

**Recette F — formule + commentaire pédagogique** (40/60, sans bordure car déjà dans la `Propriete`) :

```latex
\begin{MultiColonnes}{5}
    \tcbitem[raster multicolumn=2]
        \begin{center}\encadrer[prop]{$V(X) = E(X^2) - (E(X))^2$}\end{center}
        où $E(X^2) = \sum p_i x_i^2$.
    \tcbitem[raster multicolumn=3]
        \acc{Pourquoi cette formule est utile ?} Elle évite de calculer chaque $(x_i - E(X))^2$.
\end{MultiColonnes}
```

---

## Technique T4 — Grille virtuelle pour absorber un item qui wrappe

**Déclencheur obligatoire, vu sur le PNG** : dans un `tcbenumerate[2]` ou `[3]` d'énoncé, **un** item (ou très peu) passe à la ligne alors que ses voisins tiennent sur une ligne. Augmenter le nombre de colonnes n'y fait rien : c'est l'item fautif qui doit recevoir plus de largeur.

```latex
% AVANT : l'item c. wrappe à cause de la mention « (sur ]-1;+oo[) »
\begin{tcbenumerate}[2][1][alph] ... \end{tcbenumerate}
% APRÈS : grille de 6, ligne 1 en 3/3, ligne 2 en 4/2
\begin{tcbenumerate}[6][1][alph]
    \tcbitem[raster multicolumn=3] $f(x) = -2x + 4$ \quad et \quad $F(2) = 3$
    \tcbitem[raster multicolumn=3] $f(x) = 8x^3 - 3x$ \quad et \quad $F(1) = 2$
    \tcbitem[raster multicolumn=4] $f(x) = \dfrac{1}{(x+1)^2} + 1$ \quad et \quad $F(0) = 2$ \quad (sur $]-1;+\infty[$)
    \tcbitem[raster multicolumn=2] $f(x) = 2\cos(2x) + 2$ \quad et \quad $F\left(\dfrac{\pi}{4}\right) = 1$
\end{tcbenumerate}
```

Dimensionnement : grille = 2 ou 3 × (items par ligne) ; items normaux `grille / N` ; item qui wrappe `grille / N + k` (souvent `k = 1`) ; la somme de chaque ligne vaut la grille.

Ne pas appliquer si aucun item ne wrappe (le symétrique suffit), si tous wrappent (redescendre à `[2]` ou `[1]`), ni sur une correction.

---

## Quand NE PAS compacter (signaux d'arrêt)

1. Cible = correction d'EXO (`\exocorrection` → `\end{EXO}`). Toujours.
2. Cible = espace réponse élève (`\repsim`, `\tcfillcrep`, `crep`). Toujours.
3. Items contenant des maths affichées multilignes (`align*`, `gather*`) ou des tableaux larges.
4. Cible = `Activite` : le déroulé pédagogique prime.
5. Page déjà dense (`is_dense = true` ou `fill_ratio` > 0,55).
6. Item long + item court en 2 colonnes sans refonte possible : le blanc sous l'item court est disgracieux (essayer d'abord l'asymétrie ou T4).
