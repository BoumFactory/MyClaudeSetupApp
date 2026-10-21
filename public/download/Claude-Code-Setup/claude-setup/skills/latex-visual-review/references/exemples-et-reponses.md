# Exemples, synthèses de cours et espaces réponses

À lire à l'**Étape 4** quand le document contient des `Exemple` à étapes, des espaces réponses (`\repsim`, `\tcfillcrep`, `crep`), un tableau à compléter par l'élève ou des `Remarque` de cours. Couvre les Recettes G à J, les Techniques T1 et T2 et le Levier 6.

Principe commun : **l'espace réponse ne rétrécit jamais**. On déplace un bloc, on le met côte à côte, on ne réduit pas ce que l'élève doit pouvoir écrire à la main. Rappel bfcours : pas de `\[ … \]` ni de `$$ … $$` ; une formule mise en valeur s'écrit en `$…$` ou en `align*`.

---

## Recette G — Deux étapes consécutives d'un `Exemple` côte à côte

Paires typiques : « tableau de la loi » + « utilisation immédiate » ; « hypothèses » + « conclusion calculée » ; « découpage d'un intervalle » + « algorithme correspondant ».

Garde-fou : ne jamais paralléliser deux étapes dont l'une dépend conceptuellement de l'autre. Le côte à côte convient à deux étapes consultables indépendamment.

```latex
\begin{MultiColonnes}{2}
    \tcbitem
    \acc{Étape 3 : tableau de la loi.}
    \begin{center}\begin{tcbtab}...\end{tcbtab}\end{center}
    \tcbitem
    \acc{Étape 4 : probabilité de gagner au moins 5~\euro.}
    \begin{align*}
    P(X \geqslant 5) &= \tcfillcrep{...} \\
                     &= \tcfillcrep{...}
    \end{align*}
\end{MultiColonnes}
```

---

## Recette H — Items 1 et 2 parallèles, conclusion 3 en pleine largeur

Pattern conditionnel. Vérifier **les trois** points avant d'appliquer, sinon passer :

1. les calculs 1 et 2 tiennent dans une demi-colonne (au besoin avec T2) ;
2. l'item 3 est une vraie conclusion qui relie 1 et 2 (s'il est un troisième calcul indépendant, envisager 3 colonnes) ;
3. les items 1 et 2 sont pédagogiquement parallèles (deux variantes, deux applications symétriques), pas une suite où 2 dépend de 1.

```latex
\begin{MultiColonnes}{2}
    \tcbitem
    \acc{1. Espérance du gain brut.}
    \begin{align*}
    E(X) &= \tcfillcrep{0 \times 0{,}8 + 5 \times 0{,}15 + 50 \times 0{,}05} \\
         &= \tcfillcrep{3{,}25~\text{\euro}}
    \end{align*}
    \tcbitem
    \acc{2. Gain net.} On a $G = X - 2$. Par linéarité :
    \begin{align*}
    E(G) &= E(X - 2) \\
         &= \tcfillcrep{E(X) - 2 = 1{,}25~\text{\euro}}
    \end{align*}
\end{MultiColonnes}

\acc{3. Conclusion.}
\begin{crep}[extra lines=1]
Le gain net moyen est positif ($1{,}25$~\euro), donc ce jeu est favorable au joueur.
\end{crep}
```

---

## Recette I — `bfd methode` et `bfd exemple` côte à côte

Après une `Propriete`, un `Theoreme` ou une `Definition` qui donne un résultat sans la procédure : protocole numéroté à gauche, application immédiate sur un cas minimal à droite, lecture en regard étape par étape. Gain typique : 8 à 15 lignes par rapport à une `Methode` et un `Exemple` empilés, et surtout une procédure collée à son application.

```latex
\begin{MultiColonnes}{2}
    \tcbitem[bfd methode, bfd colors=meth, bfd sub={Calculer une intégrale}]
      Pour calculer $\displaystyle\int_a^b f(x)\,dx$ :
      \begin{tcbenumerate}[1]
        \tcbitem \acc{Chercher} $F$ une primitive de $f$.
        \tcbitem \acc{Évaluer} $F(b)$ puis $F(a)$.
        \tcbitem \acc{Soustraire} : $F(b) - F(a)$.
      \end{tcbenumerate}

    \tcbitem[bfd exemple, bfd sub={Application}]
      Calculer $\displaystyle\int_1^2 2x\,dx$.
      \begin{tcbenumerate}[1]
        \tcbitem Primitive : $F(x) = x^2$.
        \tcbitem $F(2) = 4$ et $F(1) = 1$.
        \tcbitem $\displaystyle\int_1^2 2x\,dx = 4 - 1 = $ \encadrer[defi]{$3$}.
      \end{tcbenumerate}
\end{MultiColonnes}
```

| Aspect | Règle |
|---|---|
| Étapes | 3 idéalement (une ligne chacune), 4 au plus ; au-delà, scinder ou renoncer |
| Verbes | Un verbe d'action à l'infinitif par item, en `\acc{…}` |
| Symétrie | L'étape n de la méthode correspond à l'étape n de l'exemple ; si l'exemple en a une de plus, ajouter « \acc{Vérifier} » à la méthode |
| Exemple | Le plus simple possible (coefficients entiers) ; il illustre la procédure, il n'épuise pas la difficulté |
| Fin | Résultat de l'exemple en `\encadrer[defi]{…}` (ou `[prop]`, `[meth]`) |
| Titres | `bfd sub` = nom de la procédure côté méthode, « Application » côté exemple ; `bfd colors=meth` sur la méthode |

Placement idéal : juste après le résultat théorique, avant un `Exemple` complet plus riche. À éviter juste après une `Methode` qui dit la même chose (sauf si elle n'énonce qu'un principe général).

Ne pas appliquer si la procédure tient en 1-2 étapes, si l'`Exemple` suivant fait déjà la même chose, si la méthode n'est pas séquentielle (étude de cas, choix de méthode) ou si le résultat est purement conceptuel.

---

## Recette J — EXO entier avec tableau-réponse latéralisé

Un énoncé qui contient un tableau à compléter par l'élève (méthode d'Euler, suite tabulée, loi à compléter, tableau de valeurs), habituellement sous les questions : intro et questions à gauche, tableau à droite. Différence avec G : c'est la séparation **énoncé / espace réponse** qui est latéralisée, pas deux étapes.

```latex
\begin{EXO}{Titre de l'EXO}{}
\begin{MultiColonnes}{2}
    \tcbitem
    Phrase d'introduction.

    \begin{tcbenumerate}[1]
        \tcbitem \tcbitempoint{2}\acc{Compléter} le tableau.
        \tcbitem \tcbitempoint{2}\acc{Déterminer} l'expression exacte.
    \end{tcbenumerate}
    \tcbitem[halign=center]
        \renewcommand{\arraystretch}{1.5}
        \begin{tabular}{|c|c|c|c|}
            \hline
            ... tableau-réponse intact ...
            \hline
        \end{tabular}
\end{MultiColonnes}
\exocorrection
... correction non touchée ...
\end{EXO}
```

Garde-fous :

1. Le tableau-réponse est une zone protégée : seul son emplacement change. Pas de cases réduites, pas de `\arraystretch` baissé, pas d'en-têtes abrégés au-delà de T1. S'il ne tient pas en demi-colonne sans cela, renoncer.
2. Tableau de 3 à 4 colonnes au plus ; questions courtes ; pas de figure qui concurrencerait le tableau.
3. Vérifier après déplacement que la première ligne du `tabular` est bien précédée de `\hline` (souvent perdu).

---

## Technique T1 — Faire tenir un tableau dans une demi-colonne

Le critère décisif est le réalisme pour l'élève : il doit pouvoir écrire à la main dans chaque case.

| Action | Gain | Limite |
|---|---|---|
| Réduire `\repsim[Xcm]` | 2-3 cm | Plancher 0,7 cm (fractions simples) ; 0,55 cm seulement pour des entiers de 1-2 chiffres ; 1 cm minimum pour décimaux et expressions |
| Abréger les en-têtes (« Total » → « Tot. ») | 0,3 cm | Pas d'abréviation cryptique |
| Raccourcir le titre du `tcbtab` (« Loi de probabilité du gain $X$ » → « Loi de $X$ ») | évite le wrap du titre | Garder l'identité du tableau |
| Resserrer `P(X = x_i)` en `P(X{=}x_i)` dans les en-têtes | 0,3 cm | Typographique seulement |

Après application : compiler, capturer, regarder. Si les cases sont trop petites, remonter `\repsim` quitte à renoncer au côte à côte.

---

## Technique T2 — Scinder un long `\tcfillcrep` en deux lignes `align*`

Un long `\tcfillcrep{…}` qui ne tient plus dans une colonne étroite devient deux `\tcfillcrep` : décomposition (règle ou formule) puis calcul numérique.

```latex
% AVANT : un seul trou, trop long pour la colonne
$P(X \geqslant 5) = \tcfillcrep{P(X = 5) + P(X = 7) = \dfrac{3}{32} + \dfrac{1}{32} = \dfrac{1}{8}}$
% APRÈS : deux étapes, deux trous
\begin{align*}
P(X \geqslant 5) &= \tcfillcrep{P(X = 5) + P(X = 7)} \\
                 &= \tcfillcrep{\dfrac{3}{32} + \dfrac{1}{32} = \dfrac{1}{8}}
\end{align*}
```

Souvent plus formateur : l'élève explicite la décomposition. Ne pas scinder un calcul trivial (`E(X) = 5 \times 0{,}2 = 1`) : le découpage doit refléter deux étapes réelles.

---

## Levier 6 — Retirer une `Remarque` redondante

Une `Remarque` qui reformule en intuition ce que la `Propriete` ou le `Theoreme` voisin vient d'énoncer (exemple type : « tangente qui monte, courbe qui monte » juste après « $f' \geqslant 0$ sur $I$ donc $f$ croissante sur $I$ »).

Redondance avérée si **les trois** critères sont réunis :

1. aucun terme nouveau par rapport à la propriété ;
2. aucun cas particulier ni contre-exemple absent de la propriété ;
3. une intuition équivalente figure déjà plus tôt dans le document.

Action : supprimer la `Remarque` (gain 4 à 8 lignes). Ne jamais supprimer une remarque de mise en garde (« attention au cas où $f$ n'est pas dérivable », « la réciproque est fausse »), une lecture de schéma absente ailleurs, ni une annonce d'usage pratique reprise plus loin (lire la suite avant de retirer).

Faire ce scan des `Remarque` **avant** le colonnage : une suppression nette vaut souvent trois colonnages marginaux. C'est une modification de contenu : la signaler explicitement dans le rapport.
