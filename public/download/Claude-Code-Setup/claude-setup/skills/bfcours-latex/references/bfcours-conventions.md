# Connaissances des conventions bfcours

Le package bfcours charge toutes les extensions latex nécessaires à la production de documents.
Il est nécessaire de respecter les conventions de nommage, de formatage et de structure du contenu LaTeX pour exploiter le package à son plein potentiel.

## ⚠️ RÈGLES CRITIQUES : Caractères interdits dans LaTeX

**NE JAMAIS utiliser de symboles Unicode dans les fichiers .tex** - ils causent des erreurs de compilation !

### Symboles absolument interdits :

- ❌ **Émojis et symboles décoratifs** : ✓ ✔ ✅ ❌ ⚠ ⚡ 🎯 🎉 📝 📋 📄 📁 📂 🔧 🧹 💡 ⭐
- ❌ **Flèches Unicode** : → ← ↑ ↓ ⟵ ⟶
- ❌ **Symboles mathématiques Unicode** : ≠ ≤ ≥ × ÷ ∞ ∑ ∏ ∫ √ ∈ ∉ ⊂ ⊃ ∪ ∩ ∀ ∃ ∅ ∂ ∇

### Remplacements obligatoires :

**Ligatures** :
- `œ` → **`\oe `** (CRITIQUE - erreur de compilation sinon !)
- `Œ` → **`\OE `**
- `æ` → **`\ae `**
- `Æ` → **`\AE `**

**Symboles mathématiques** :
- `≠` → `\neq`
- `≤` → `\leq`
- `≥` → `\geq`
- `×` → `\times`
- `÷` → `\div`
- `∞` → `\infty`
- `√` → `\sqrt`
- `∈` → `\in`
- `°` → `$^{\circ}$`

**Mots typiques contenant œ** :
- c\oe ur, n\oe ud, \oe il, s\oe ur, b\oe uf, v\oe u, \oe uvre

### ✅ Utiliser à la place :

Pour les emphases visuelles dans LaTeX, utiliser :
- `\acc{texte}` pour l'emphase colorée
- `\textbf{texte}` pour le gras (mais préférer `\acc{}`)
- Texte simple pour les explications

## Règles typographiques générales

### Point final dans les listes : seulement si l'item est une phrase

**RÈGLE** : un item de liste (itemize, enumerate, tcbenumerate, MultiColonnes avec puces) se
termine par un **point final si — et seulement si — c'est une phrase** : une consigne, une
proposition rédigée, une explication. Un item qui n'est qu'une **expression mathématique nue**
(un calcul à effectuer, une expression à simplifier, une égalité à démontrer) **ne prend pas de
point** : le point y est lu comme un symbole parasite collé à la formule.

```latex
% CORRECT — phrases : point final
\begin{tcbenumerate}[2]
    \tcbitem \acc{Calculer} la valeur de $f(3)$.
    \tcbitem \acc{En déduire} le signe de $f$.
\end{tcbenumerate}

% CORRECT — expressions nues : pas de point
\begin{tcbenumerate}[3]
    \tcbitem $2^{12}$
    \tcbitem $4^{6}$
    \tcbitem $\dfrac{2^{20}}{2^{8}}$
\end{tcbenumerate}

% INCORRECT — point parasite après une expression nue
\begin{tcbenumerate}[3]
    \tcbitem $2^{12}$.
    \tcbitem $4^{6}$.
\end{tcbenumerate}

% INCORRECT — phrase sans point
\begin{tcbenumerate}[2]
    \tcbitem \acc{Calculer} la valeur de $f(3)$
\end{tcbenumerate}
```

**Critère opérationnel** : si le contenu de l'item est un **unique groupe `$...$` sans aucun texte
autour**, c'est une expression nue -> pas de point. Dès qu'il y a un verbe, un connecteur ou un
quantificateur rédigé (« Pour tout réel $x$, $\sqrt{x^{2}}=|x|$. », « Si $a$ est impair, alors
$a^{2}$ est impair. »), c'est une phrase -> point final.

La règle vaut **aussi dans les corrections** : un item de correction qui n'est qu'une chaîne de
calculs (`$B=\dfrac{4}{5}\div\dfrac{6}{5}=\dots=\dfrac{2}{3}$`) ne prend pas de point, alors qu'un
item rédigé (« Le numérateur vaut ... Donc $A=\dots$ ») le garde.

### Accents français obligatoires

Les accents français (é, è, ê, à, ù, ç, î, ô, etc.) doivent **toujours** être présents et correctement encodés dans les documents. Ne jamais écrire de texte français sans accents.

```latex
% CORRECT
Déterminer l'équation réduite de la droite passant par les points $A$ et $B$.

% INCORRECT (accents manquants)
Determiner l'equation reduite de la droite passant par les points $A$ et $B$.
```

### Commande \Coordonnees pour les coordonnées de points

**RÈGLE OBLIGATOIRE** : Pour écrire les coordonnées d'un point, utiliser **systématiquement** la commande `\Coordonnees` du package bfcours.

**Définition** : `\newcommand{\Coordonnees}[3][]{$#1(#2~;~#3)$}`

**Syntaxe** : `\Coordonnees[label]{x}{y}`

```latex
% CORRECT
Le point \Coordonnees[A]{2}{3} appartient à la droite.
On place les points \Coordonnees[A]{-1}{4} et \Coordonnees[B]{3}{-2}.

% INCORRECT (écriture manuelle)
Le point $A(2~;~3)$ appartient à la droite.
On place les points $A(-1;4)$ et $B(3;-2)$.
```

**Attention** : Ne pas écrire `A(x;y)` ou `$A(x~;~y)$` manuellement. Toujours passer par `\Coordonnees`.

## Environnements de structure

Il s'agit des environnements pour présenter en colonne, centrer, énumérer et les tableaux.

### Présentation en grille avec MultiColonnes

L'environnement par défaut pour formater en colonnes.

**⚠️ CRITIQUE** : Il faut **TOUJOURS** laisser une ligne vide avant `\begin{MultiColonnes}` pour que l'affichage soit correct. Sans ce saut de ligne, le rendu visuel sera incorrect.

- nbCol : obligatoire, peut être ajusté pour répartir l'espace efficacement.
- options : defaut ColonnesBaseStyle ( un tcbset ) - Il s'agit des options tcolorbox pour toutes les boites tcbitem. Peut être adapté selon les cas d'utilisation.

Dans les tcbitem, on peut spécifier les styles tcolorbox pour la boite actuelle.

```latex
\begin{MultiColonnes}{nbCol}[options]
    \tcbitem[raster multicolumn=2] Contenu large sur 2 colonnes
    \tcbitem[style tcolorbox pour cet item] Contenu colonne 1
    \tcbitem Contenu colonne 2
\end{MultiColonnes}
```

Exemple complexe :

```latex
\begin{MultiColonnes}{7}[colframe=\currentAccentColor,boxrule=0.4pt,coltitle=white]
    \tcbitem[raster multicolumn=4,title=Large :] Contenu colonne 1 large sur 2 colonnes

    \begin{MultiColonnes}{2} % ouvre un deuxième niveau qui se répartira l'espace disponible sur deux colonnes.
        \tcbitem \textbullet Un asset
        \tcbitem \textbullet Un autre asset
    \end{MultiColonnes}
    \tcbitem[raster multicolumn=3] Contenu colonne 2 %sans titre
\end{MultiColonnes}
```

Définition de l'environnement MultiColonnes :

```latex
% Définir un style de base plus complet et modulaire
\tcbset{%
ColonnesBaseStyle/.style={%
    top=0pt,
    bottom=0pt,
    left=0pt,
    right=0pt,
    colback=white,
    colframe=white,
    boxrule=0pt,
    boxsep=3pt,
    nobeforeafter,
    size=fbox,%
    halign=left,
}%
}%
\NewDocumentEnvironment{MultiColonnes}{m O{ColonnesBaseStyle}}{%
        \begin{tcolorbox}[blank,nobeforeafter,size=minimal, width=\textwidth,boxrule=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,halign=left,boxsep=0pt,
        colback            = \currentBackgroundColor,
        colframe           = \currentBackgroundColor]%
    
    % (4) le raster proprement dit
    \begin{tcbitemize}[%
        raster equal height=rows,
        nobeforeafter,
        boxsep=0pt,
        breakable,
        raster column skip = 5pt,
        raster row skip    = 2pt,
        raster columns     = #1,
        colback            = \currentBackgroundColor,
        colframe           = \currentBackgroundColor,
        boxrule            = 0pt,
        top                = 0pt,
        bottom             = 0pt,
        left               = 0pt,
        right              = 0pt,
        after skip         = 0pt,
        after upper        = {},
        after lower        = {},
        size=minimal,
        raster every box/.style={
        enhanced,
        breakable,
        size=small,
        #2
        }%
    ]%
    \ignorespaces
    }{%
    \end{tcbitemize}%
    %\IfInsideTcolorboxTF{ 
    \end{tcolorbox}
    %}{}%
    \ignorespacesafterend% ⟵ gobe les blancs après \end
    }
```

### Listes énumérées avec tcbenumerate

L'environnement à utiliser obligatoirement qui remplace enumerate.

Il gère en partie la disposition en grille comme MultiColonnes, mais avec une syntaxe différente.

- nbCol : par défaut 1 - le nombre de colonnes dans lequel on veut disposer les items.
- nbStart : par défaut 1 - point de départ du compteur pour des utilisations spécifiques.
- style : par défaut num - style de numérotation, alternative 'alph' pour avoir l'énumération alphanumérique.

```latex
\begin{tcbenumerate}[nbCol][nbStart][style]
    \tcbitem Premier item
    \tcbitem Second item
\end{tcbenumerate}
```

Exemple complexe avec imbrication :

```latex
\begin{tcbenumerate}[3]
    \tcbitem Premier item, peut être avec une figure.
    \tcbitem[raster multicolumn=2, colframe=black,boxrule=0.4pt] Second item :
        \begin{tcbenumerate}[2][1][alph]
            \tcbitem Sous item a
            \tcbitem Sous item b
        \end{tcbenumerate}
\end{tcbenumerate}
```

**Remarques** :

- Tu dois le plus souvent possible utiliser tcbenumerate[2] en deux colonnes pour optimiser l'utilisation de l'espace. Il faut cependant veiller à ce que la présentation soit cohérente.
- Dans le cas d'imbrication, le premier niveau doit avoir une bordure pour clarifier la présentation.
- Il est naturel et puissant de terminer un tcbenumerate pour le reprendre plus bas avec une autre géométrie en saisissant le bon index de départ.

**Heuristique pour choisir le nombre de colonnes** (évaluer chaque énoncé d'EXO) :

| Profil des items | Choix recommandé | Exemple |
|------------------|------------------|---------|
| 2 items courts (1 ligne) | `[2]` | « Déterminer $f'(x)$. » / « En déduire $f''(x)$. » |
| 3 items courts (1 ligne) | `[3]` | « Conjecturer. » / « Démontrer. » / « Confirmer. » |
| 4-6 items moyens (1-2 lignes) | `[2]` | Étude complète d'une fonction |
| Items longs (3+ lignes ou maths affichées) | `[1]` | Affirmations vrai-faux à justifier |
| Items asymétriques (1 long + plusieurs courts) | `[1]` puis sous-`tcbenumerate[2 ou 3]` | Voir ci-dessous |

**Reformulation pour gagner en compacité** : avant de baisser à `[1]`, essayer de raccourcir l'énoncé sans en altérer le sens (« suivant les valeurs de $x$ » → « selon $x$ », « la fonction $f$ définie sur $\R$ par » → « $f : \R \to \R$ »). L'objectif est de tenir sur 1-2 lignes par item pour permettre `[2]` ou `[3]`.

### Respecter la structure de l'énoncé source (sous-questions a/b)

**RÈGLE CRITIQUE** : Quand un énoncé source possède une numérotation hiérarchique (1.a, 1.b, 2.a, 2.b...), **ne pas l'aplatir** en une simple liste 1, 2, 3, 4. La hiérarchie porte du sens pédagogique (regroupement thématique, progression).

Utiliser l'imbrication `tcbenumerate` :

```latex
\begin{tcbenumerate}[1]
\tcbitem \tcbitempoint{4}
\begin{tcbenumerate}[2][1][alph]
\tcbitem \acc{Étudier} les variations de $C$.
\tcbitem \acc{Tracer} la courbe représentative.
\end{tcbenumerate}
\tcbitem \tcbitempoint{4}On dit que les rendements sont décroissants lorsque $C_m$ est croissant.
\begin{tcbenumerate}[2][1][alph]
\tcbitem \acc{Étudier} les variations de $C_m$.
\tcbitem À quoi cela correspond-il pour $C$ ?
\end{tcbenumerate}
\tcbitem \tcbitempoint{3}\acc{Déterminer} ce nombre.
\end{tcbenumerate}
```

L'utilisateur peut explicitement demander d'aplatir, mais par défaut la fidélité à l'énoncé prime sur l'aplatissement.

**Compactage des corrections** : à l'inverse, dans les corrections, mieux vaut éviter les `\\` à répétition et les sauts de ligne forcés. Préférer :
- regrouper les calculs en une seule ligne avec des `\iff` ou des `;` quand c'est court ;
- conserver des `\begin{itemize}` brefs pour énumérer les cas (signe, intervalles) plutôt que des phrases successives.

**Mode maths affiché — INTERDIT** : NE JAMAIS utiliser `\[ ... \]` ni `$$ ... $$`. Pour une équation à mettre en valeur, utiliser le mode `$...$` inline éventuellement avec un saut de ligne avant/après, ou un environnement `align*` / `gather*` quand plusieurs lignes sont nécessaires. La raison : `\[ ... \]` casse le rythme typographique du document bfcours et produit un espacement disgracieux.

Définition latex de tcbenumerate :

```latex
\NewDocumentEnvironment{tcbenumerate}{O{1} O{1} O{num}}{%
% #1 = nombre de colonnes (défaut: 1)
% #2 = valeur de départ (défaut: 1)
% #3 = format de numérotation: num (défaut) ou alph
% Vérifier si on est déjà dans un tcbenumerate
\ifintcbenumerate
    % On est dans une imbrication, sauvegarder la valeur actuelle
    \setcounter{savedtcbenumcounter}{\value{tcbenumcounter}}%
\else
    % C'est le premier niveau, on active le flag
    \intcbenumeratetrue
\fi
% Réinitialiser le compteur
\edef\startcounter{#2-1}%
\setcounter{tcbenumcounter}{\startcounter}%
% Définir la commande de formatage en fonction du type choisi
\def\tcbenumformat{#3}%
\ifx\tcbenumformat\@empty\def\tcbenumformat{num}\fi% Au cas où le paramètre est vide
% Définir le format (numérique ou alpha)
\tcbenumisalphafalse % Par défaut, on utilise des nombres
\def\tempformat{#3}%
\def\alphformat{alph}%
\ifx\tempformat\alphformat
    \tcbenumisalphatrue
\fi
\begin{tcolorbox}[blank, width=\textwidth,boxrule=0pt,left=0pt,right=0pt,top=0pt,bottom=0pt,halign=left]%
% Configuration de tcbitemize
\begin{tcbitemize}[%
    raster columns=#1,
    raster equal height=rows,
    raster column skip=0.5em,
    raster row skip=5pt,
    breakable,
    % Style semblable à un enumerate standard
    raster every box/.style={
        enhanced,
        breakable,
        nobeforeafter,            
        % Style prédéfini pour le titre (utilisé seulement s'il y a un titre)
        colbacktitle=\itemBaseColor,
        colback=\currentBackgroundColor,
        boxrule=-1pt,
        colframe=\itemBaseColor,
        fonttitle=\bfseries\color{white},
        arc=5pt, % Coins arrondis en haut
        sharp corners=south, % Coins pointus en bas
        left=0pt, % Réduit la marge gauche
        right=0pt,  % Pas de marge droite
        top=0pt,    % Pas de marge en haut
        bottom=0pt, % Pas de marge en bas
        valign=top,
        toptitle=2pt,
        bottomtitle=3pt,
        lefttitle=5pt,
        righttitle=5pt,
        before upper={\stepcounter{tcbenumcounter}\tikz[baseline=(numbox.base)]{\node[%
                inner sep=3pt,
                font=\large\bfseries,
                text=white,
                fill=\itemBaseColor,
                minimum width=1.5em,
                minimum height=1.5em,
                rounded corners=2pt,
                text centered
            ] (numbox) {%
                \iftcbenumisalpha
                    \alph{tcbenumcounter}.%
                \else
                    \arabic{tcbenumcounter}.%
                \fi
            };}%
            \hspace{3pt}% Espace entre la boîte et le texte
        },
    }%
]%
}{%
\end{tcbitemize}%
% Restaurer la valeur précédente ou réinitialiser
\ifintcbenumerate
    % Vérifier si on a une valeur sauvegardée
    \ifnum\value{savedtcbenumcounter}>0
        % On est dans une imbrication, restaurer la valeur sauvegardée
        \setcounter{tcbenumcounter}{\value{savedtcbenumcounter}}%
        \setcounter{savedtcbenumcounter}{0}% Réinitialiser la sauvegarde
    \else
        % C'est la fin du niveau le plus externe, désactiver le flag
        \intcbenumeratefalse
        \setcounter{tcbenumcounter}{0}% Réinitialiser le compteur
    \fi
\fi%
\end{tcolorbox}%
\ignorespacesafterend% ⟵ gobe les blancs après \end
}
```

### Tableaux avec tcbtab

Tous les tableaux doivent utiliser tcbtab dans bfcours. Il est basé sur l'environnement tabular avec des améliorations.

**Note critique tcbtab** : La première ligne du contenu doit être l'entête directement contrairement à tabular qui nécessite un hline.

**Le titre** : Uniquement le titre, sans clé.

**⚠️ RÈGLE CRITIQUE : jamais de virgule dans le titre d'un `tcbtab`**

Le titre optionnel de `tcbtab` est injecté dans `title=#1` d'un `\newtcolorbox`, donc **parsé comme une liste de clés tcolorbox**. Une virgule y démarre une fausse clé et provoque une erreur fatale :

```
Package pgfkeys Error: I do not know the key '/tcb/deux écritures'
```

C'est exactement la même contrainte que pour les titres d'`EXO`. Remplacer la virgule par un tiret cadratin `--`, un point-virgule ou deux-points.

```latex
% INCORRECT (erreur pgfkeys fatale)
\begin{tcbtab}[Le même nombre, deux écritures]{c|c|c}

% CORRECT
\begin{tcbtab}[Le même nombre -- deux écritures]{c|c|c}
```

Les accents, apostrophes et `--` dans le titre ne posent aucun problème : **seule la virgule** est interdite.

```latex
\begin{tcbtab}[Titre du tableau]{structure tabular}%
    \cellcolor{\currentTableColbackTitleColor}{\color{\currentTableColTitleColor} Header&content}\\
    \hline
    contenu
\end{tcbtab}
```

```latex
\begin{tcbtab}[Joli tableau]{l|c|r}%

Colonne 1 & Colonne 2 & Colonne 3\\
\hline
a&b&c\\
\end{tcbtab}
```

**Définition de l'environnement tcbtab** :

```latex
%style tcolorbox pour les tableaux : 
\tcbset{
    TableauBox/.style={%
colframe=\currentTableFrameColor,colback=\currentTableColbackColor,colupper=\currentTableColupperColor,
colbacktitle=\currentTableColbackTitleColor, coltitle=\currentTableColTitleColor,
breakable,
fonttitle=\bfseries,nobeforeafter,center title,left=0mm,right=0mm,top=0mm,bottom=0mm,boxsep=0mm,
    toptitle=0.5mm,bottomtitle=0.5mm,}
}
%Tableaux
\newtcolorbox{tcbtab}[3][]{%
    TableauBox,
    drop fuzzy shadow,%
    center title,
    title=#1,
    hbox,
    before upper*=\begin{tabular}{#2},
    after upper*=\end{tabular}, % Structure du tableau passée en paramètre
}
```

## Règles de formatage du texte

Il y a différentes manières de formater le texte, chacune ayant son but.

### Couleurs disponibles

Le système de coloration de bfcours est un peu complexe mais très utile. Veille à l'utiliser de façon optimale.

Voici le code qui a été défini dans bfcours et que tu peux utiliser : 

```latex
\definecolor{nombres}{cmyk}{0,.8,.95,0}
\definecolor{gestion}{cmyk}{.75,1,.11,.12}
\definecolor{gestionbis}{cmyk}{.75,1,.11,.12}
\definecolor{grandeurs}{cmyk}{.02,.44,1,0}
\definecolor{geo}{cmyk}{.62,.1,0,0}
\definecolor{algo}{cmyk}{.69,.02,.36,0}
\definecolor{correction}{cmyk}{.63,.23,.93,.06}
\definecolor{couleur_theme}{HTML}{000000}
\arrayrulecolor{couleur_theme} % Couleur des filets des tableaux
\definecolor{bluegreen}{rgb}{0.0, 0.87, 0.87}
\definecolor{lightyellow}{rgb}{1.0, 1.0, 0.6}
\definecolor{lightred}{rgb}{1.0, 0.6, 0.6}


% Couleurs liées aux environnements
\definecolor{defi}{RGB}{56,128,77}
\definecolor{ex}{RGB}{39,61,112}
\definecolor{nota}{RGB}{144,55,222}
\definecolor{rem}{RGB}{128,128,128}
\definecolor{thm}{RGB}{207,8,77}
\definecolor{prop}{RGB}{0,0,200}
\definecolor{demo}{RGB}{255,128,0}
\definecolor{act}{RGB}{255,128,0}
\definecolor{meth}{RGB}{151,74,0}

% Couleurs liées aux commandes d'accentuation
%\newcommand{\vocColor}{red!65!black}%Pour les mots de vocabulaire
\newcommand{\lienInterneColor}{red!50!yellow}%pour les lien internes au document.
\definecolor{monrose}{HTML}{FF1493}%Couleur de correction officielle, et les liens externes au document

\newcommand{\currentBackgroundColor}{white}
% Système de coloration automatique de bfcours
% Pour les accentuations de texte
\newcommand{\currentAccentColor}{black}

% Pour les tableaux primaires
\newcommand{\currentTableFrameColor}{blue!50!black}
\newcommand{\currentTableColbackTitleColor}{blue!50!black}
\newcommand{\currentTableColTitleColor}{white}

\newcommand{\currentTableColbackColor}{white}
\newcommand{\currentTableColupperColor}{red!50!black}

% Pour les tableaux secondaires
\newcommand{\currentSecondaryTableFrameColor}{red!50!black}
\newcommand{\currentSecondaryTableColbackTitleColor}{Salmon!30!white}
\newcommand{\currentSecondaryTableColTitleColor}{black}

\newcommand{\currentSecondaryTableColbackColor}{yellow!10!white}
\newcommand{\currentSecondaryTableColupperColor}{red!50!black}

% Commande générale pour changer les couleurs des tableaux
\newcommand{\CouleursTabular}[5]{
    % Couleurs pour les tableaux primaires
    \renewcommand{\currentTableFrameColor}{#1}
    \renewcommand{\currentTableColbackTitleColor}{#2}
    \renewcommand{\currentTableColTitleColor}{#3}
    \renewcommand{\currentTableColbackColor}{#4}
    \renewcommand{\currentTableColupperColor}{#5}
    \arrayrulecolor{#1} % Couleur des filets des tableaux
}
\newcommand{\CouleursSecondaryTabular}[5]{
    % Couleurs pour les tableaux secondaires (si besoin de distinctions)
    \renewcommand{\currentSecondaryTableFrameColor}{#1}
    \renewcommand{\currentSecondaryTableColbackTitleColor}{#2}
    \renewcommand{\currentSecondaryTableColTitleColor}{#3}
    \renewcommand{\currentSecondaryTableColbackColor}{#4}
    \renewcommand{\currentSecondaryTableColupperColor}{#5}
}
```

### Commandes disponibles et fonction

- Accentuation : \acc{mot} - couleur adaptative **Remplace textbf**.
- Nouveau mot de vocabulaire : \voc{mot} - OBLIGATOIRE dans les cours pour la première occurence d'un mot de vocabulaire
- Citation : \frquote{expr}
- Notation degré ( obligatoire ) : a$^{\circ}$
- encadrer ( une formule, un résultat.. ) : \encadrer[couleur]{mot} ou \encadrer[couleur]{$maths$}
  - Sensible au mode maths depuis le 22/07/2026 : appelée dans `$...$` ou `\[...\]`, elle garde le mode maths et son style (`\[P = \dfrac{1}{2} = \encadrer[prop]{0{,}5}\]` est correct) ; hors maths, on met soi-même les `$...$` à l'intérieur (`\encadrer{$x+1$}`). Ne vaut PAS pour `\acc`, qui reste `\acc{$...$}` et jamais dans `\[...\]`.
- outil du cours ( correction d'exercice ) : \outilcours{texte} ou \outilcours[Étiquette]{texte}
  - Ligne grise « ▹ *Outil du cours :* … » qui nomme la méthode ou la propriété du cours à mobiliser, pour la distinguer de la **rédaction attendue sur copie** qui suit en noir. À placer en tête de chaque `\tcbitem` de correction, suivie d'une ligne vide ; l'argument optionnel remplace l'étiquette (`[Rappel]`).
  - Gabarit de correction « modèle de rédaction » : `\outilcours{...}`, phrase qui situe le calcul, formule générale puis calcul en `\[...\]` (jamais de fraction en ligne isolée, `parskip` nul dans un `\tcbitem`), résultat `\encadrer[prop]{...}`, phrase de conclusion. Une question par `\begin{tcbenumerate}[1][n]` pour que la correction reste sécable entre les questions. Exemple complet : `1. Cours/1ere-techno-TC/Sequence-Probabilites_conditionnelles/Exercices/enonce.tex`.
- logique : \Si ; \Alors ; \Donc ; \Mais ; \SSI ; \Et

### Cas d'utilisation de \acc{}

Au sein des environnements didactiques, on met systématiquement en acc les mots de vocabulaire déjà définis.

Les informations cruciales peuvent être encadrées.

**⚠️ RÈGLE CRITIQUE pour les énoncés d'exercices** : L'accentuation `\acc{}` doit être utilisée pour **DEUX éléments** :

1. **Les verbes d'action** : `\acc{Calculer}`, `\acc{Déterminer}`, `\acc{Résoudre}`, `\acc{Simplifier}`, `\acc{Comparer}`, etc.

2. **La forme de la réponse attendue** : Toute indication sur ce que l'élève doit produire ou comment présenter sa réponse :
   - `\acc{résultat simplifié}`
   - `\acc{sous forme d'intervalle(s)}`
   - `\acc{justifier le signe}`
   - `\acc{en déduire}`
   - `\acc{arrondi au centième}`
   - `\acc{forme canonique}`
   - etc.

**Exemples corrects** :
```latex
\acc{Calculer} les valeurs absolues en donnant un \acc{résultat simplifié}.
\acc{Résoudre} les inéquations et donner les solutions \acc{sous forme d'intervalle(s)}.
\acc{Simplifier} les expressions suivantes (\acc{justifier le signe}).
```

**Pourquoi ?** Ces accentuations guident l'élève en pointant :
- CE qu'il doit faire (verbe d'action)
- COMMENT il doit le présenter (forme attendue) 

## Environnement EXO

**⚠️ RÈGLE ABSOLUE : Environnement EXO OBLIGATOIRE pour TOUS les exercices**

L'environnement `EXO` est **OBLIGATOIRE** pour créer des exercices, quelle que soit la nature du document :

- Feuilles d'exercices : Utiliser EXO
- Exercices dans les activités (environnement Activite) : Utiliser EXO
- Exercices dans les évaluations : Utiliser EXO
- Devoirs maison : Utiliser EXO

**Principe fondamental** :
1. Tout exercice DOIT être encapsulé dans `\begin{EXO}...\end{EXO}`
2. Les corrections sont TOUJOURS intégrées après `\exocorrection` dans le même environnement
3. JAMAIS de fichier `solution.tex` séparé - les corrections font partie intégrante de l'environnement EXO

Cette règle permet :
- La gestion automatique des compétences
- L'affichage conditionnel des corrections (versions élève/professeur)
- Le calcul automatique des scores via `\tcbitempoint`

C'est l'environnement dédié aux exercices. C'est lui qui est lié au système de compétences.

- La définition de \rdifficulty gère l'affichage de la difficulté pour cet exercice ( nombre décimal entre 1 et 3 - 1.5 accepté par exemple ).
- Le code correspond au code de la compétence utilisée pour résoudre l'exercice.
- Le titre doit être le titre de la compétence.
- L'énoncé doit comporter les consignes clairement formatées.
- Si demandé, il faut insérer des espaces réponses avec le contenu attendu à produire par l'élève.
- La correction de l'exercice peut comporter plus de détails dans le cas de problèmes complexes par exemples, ou d'astuces.

    Cependant, on veillera à reprendre dans la plupart des cas la même présentation que l'énoncé dans laquelle on aura inséré les espaces réponses.

### Syntaxe de EXO

```latex
\def\rdifficulty{n}
\begin{EXO}{Mon Titre - sans virgule}{code}

Contenu de l'énoncé avec ou sans espace réponse. 
La consigne comportera systématiquement des points via la commande \tcbitempoint.

\exocorrection

contenu de la solution.
\end{Envname}
```

### Règle d'utilisation de \tcbitempoint

Le score de chaque exercice est calculé automatiquement via la commande \tcbitempoint{i} ou i est le nombre de points.
Veille à noter les points :

- 1 point pour une action basique de l'élève ( développer, donner du cours, effectuer un calcul...)
- 2 points si demande de figure, tableau, production plus complexe.
- On cumule les points dans une question ou il y a manifestement plusieurs actions élève à effectuer.
- 5 points pour des actions de recherche ( englobe souvent les actions élève donc pas de cumul ici ).

**Activer ou désactiver l'affichage des boîtes pour les points**
%\displayitempointsfalse % Ne pas afficher les boîtes
\displayitempointstrue % Afficher les boîtes

### Un exemple d'EXO avec espace réponse

```latex
% Niveau - 1ere-spe
\begin{EXO}{Se repérer sur le cercle trigonométrique}{}
\tcbitempoint{4}Donner un réel associé à chaque point du cercle.
 \begin{tcbenumerate}[4]
    \tcbitem \begin{tikzpicture}[scale=1.5]
  \draw (0,0) circle (1);
  \draw (0.87,0.5)--(-0.87,-0.5);
  \draw (-0.87,0.5)--(0.87,-0.5);
  \draw[dashed] (0,1)--(0,-1);
  \draw[dashed] (1,0)--(-1,0);
  \draw[color=red] (0.3,0) arc (0:30:0.3);
  \draw[color=red] (0.4,0) arc (0:30:0.4);
  \draw[color=red] (-0.3,0) arc (180:150:0.3);
  \draw[color=red] (-0.4,0) arc (180:150:0.4);
  \draw[color=red] (-0.35,0) arc (180:210:0.3);
  \draw[color=red] (-0.45,0) arc (180:210:0.4);
  \draw[color=red] (0.35,0) arc (360:330:0.35);
  \draw[color=red] (0.45,0) arc (360:330:0.45);
  \draw[color=red] (0.75,0.15) node[left] {\bfseries 30$^\circ$};
  \draw (0.87,0.5) node[right] {$A$};
  \draw (-0.87,-0.5) node[left] {$B$};
  \draw (0.87,-0.5) node[right] {$C$};
  \draw(-0.87,0.5) node[left] {$D$};
  \draw(-0.1,-0.2) node {$O$};
  \draw (0,1) node[above] {$\phantom{A}$};
  \draw (0,-1) node[below] {$\phantom{D}$};
 \end{tikzpicture}
 \begin{crep}[extra lines=4]
 \end{crep}

    \tcbitem \begin{tikzpicture}[scale=1.5]
  \draw (0,0) circle (1);
  \draw (0,0)--(0.71,0.71);
  \draw (0,0)--(-0.71,0.71);
  \draw[dashed] (0,0)--(-0.71,-0.71);
  \draw[dashed] (1,0)--(-1,0);
  \draw[dashed] (0,1)--(0,-1);
  \draw (0,1) node[above] {$A$};
  \draw (-0.71,0.71) node[left] {$B$};
  \draw (-0.71,-0.71) node[left] {$C$};
  \draw(0,-1) node[below] {$D$};
  \draw(-0.1,-0.2) node {$O$};
  \draw[color=red] (0.3,0) arc (0:45:0.3);
  \draw[color=red] (0.4,0.2) node {\bfseries 45$^\circ$};
  \draw[color=red] (-0.3,0) arc (180:135:0.3);
  \draw[color=red] (-0.4,0.2) node {\bfseries 45$^\circ$};
 \end{tikzpicture}
 \begin{crep}[extra lines=4]
 \end{crep}

    \tcbitem \begin{tikzpicture}[scale=1.5]
  \draw (0,0) circle (1);
  \draw[dashed] (1,0)--(-1,0);
  \draw[dashed] (0,1)--(0,-1);
  \draw (0.5,0.87)--(-0.5,-0.87);
 \draw (0.5,0.87) node[above right] {$A$};
  \draw (-0.5,0.87) node[above left] {$B$};
  \draw (-1,0) node[left] {$C$};
  \draw (-0.5,-0.87) node[below left] {$D$};
  \draw (0,0)--(-0.5,0.87);
  \draw(0.1,-0.2) node {$O$};
  \draw[color=red] (0.3,0) arc (0:60:0.3);
  \draw[color=red] (0,0.3) arc (90:120:0.3);
  \draw[color=red] (0.4,0.25) node{\bfseries 60$^\circ$};
  \draw[color=red] (-0.1,0.5) node{\bfseries 30$^\circ$};
 \end{tikzpicture}
 \begin{crep}[extra lines=4]
 \end{crep}

    \tcbitem \begin{tikzpicture}[scale=1.5]
  \draw (0,0) circle (1);
  \draw (0.71,0.71)--(-0.71,-0.71);
  \draw (-0.71,0.71)--(0.71,-0.71); 
  \draw (0.71,0.71) node[right] {$A$};
  \draw (-0.71,-0.71) node[left] {$B$};
  \draw (-0.71,0.71) node[left] {$C$};
  \draw (0.71,-0.71) node[right] {$D$};
  \draw (0.15,0.15)--(0,0.3)--(-0.15,0.15);
  \draw(0,-0.2) node {$O$};
  \draw (-0.5,-0.87) node[below left] {$\phantom{D}$};
  \draw (0.71,0.71)--(0.71,-0.71);
  \draw (-1,0)--(1,0);
  \draw (0.71,0.355) node[color=red] {{\boldmath $\approx$}};
  \draw (0.71,-0.355) node[color=red] {{\boldmath $\approx$}};
 \end{tikzpicture}
 \begin{crep}[extra lines=4]
 \end{crep}
 \end{tcbenumerate}

\exocorrection

\begin{tcbenumerate}[2]
\tcbitem[boxrule=0.4pt,colframe=black,colback=white] Points du cercle avec angles de 30$^\circ$ :
\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$ : $\dfrac{\pi}{6}$ (30$^\circ$)
\tcbitem \textbullet Point $B$ : $\dfrac{7\pi}{6}$ (210$^\circ$)
\tcbitem \textbullet Point $C$ : $\dfrac{11\pi}{6}$ (330$^\circ$)
\tcbitem \textbullet Point $D$ : $\dfrac{5\pi}{6}$ (150$^\circ$)
\end{MultiColonnes}

\tcbitem[boxrule=0.4pt,colframe=black,colback=white] Points du cercle avec angles de 45$^\circ$ :
\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$ : $\dfrac{\pi}{2}$ (90$^\circ$)
\tcbitem \textbullet Point $B$ : $\dfrac{3\pi}{4}$ (135$^\circ$)
\tcbitem \textbullet Point $C$ : $\dfrac{5\pi}{4}$ (225$^\circ$)
\tcbitem \textbullet Point $D$ : $\dfrac{3\pi}{2}$ (270$^\circ$)
\end{MultiColonnes}

\tcbitem[boxrule=0.4pt,colframe=black,colback=white] Points du cercle avec angles de 60$^\circ$ et 30$^\circ$ :
\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$ : $\dfrac{\pi}{3}$ (60$^\circ$)
\tcbitem \textbullet Point $B$ : $\dfrac{2\pi}{3}$ (120$^\circ$)
\tcbitem \textbullet Point $C$ : $\pi$ (180$^\circ$)
\tcbitem \textbullet Point $D$ : $\dfrac{4\pi}{3}$ (240$^\circ$)
\end{MultiColonnes}

\tcbitem[boxrule=0.4pt,colframe=black,colback=white] Points du cercle sur les diagonales :
\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$ : $\dfrac{\pi}{4}$ (45$^\circ$)
\tcbitem \textbullet Point $B$ : $\dfrac{5\pi}{4}$ (225$^\circ$)
\tcbitem \textbullet Point $C$ : $\dfrac{3\pi}{4}$ (135$^\circ$)
\tcbitem \textbullet Point $D$ : $\dfrac{7\pi}{4}$ (315$^\circ$)
\end{MultiColonnes}
\end{tcbenumerate}

\end{EXO}
```

### Un exemple d'EXO sans espace réponse

```latex
% Niveau - 2nde
\def\rdifficulty{1}
\begin{EXO}{Calcul d'image pour fonction polynomiale}{C2N18-2}
Soit la fonction $f$ définie par $f(x)=3x^2-4x+1$.

\tcbitempoint{2}\acc{Calculer} $f(2)$.
\exocorrection
On remplace $x$ par 2 dans l'expression de $f(x)$ :
\begin{align*}
f(2) &= 3 \times 2^2 - 4 \times 2 + 1 \\
     &= 3 \times 4 - 8 + 1 \\
     &= 12 - 8 + 1 \\
     &= 5
\end{align*}
Donc : \encadrer[defi]{$f(2) = 5$}
\end{EXO}
```

## Environnements didactiques

Il s'agit des environnements qui encapsulent le contenu.
Ils sont répertoriés dans la table des matières, adaptent les couleurs, bref ils s'occuppent de la partie design.

Chaque environnement a une seule responsabilité didactique.

Le titre est obligatoire, sans clé, court, adapté au contexte.

### Syntaxe des environnements didactiques

```latex
\begin{Envname}[Mon Titre]
contenu
\end{Envname}
```

### Environnements disponibles

Propriete, Definition, Remarque, Demonstration, Theoreme, Activite, Notation, Exemple, ContreExemple, Methode

### ⚠️ Règle : séparer Methode et Exemple d'application

**Ne jamais mettre l'application d'une méthode à l'intérieur de l'environnement `Methode`.**

L'environnement `Methode` ne doit contenir **que les étapes théoriques** (la marche à suivre générale). L'exemple d'application qui illustre la méthode sur un cas concret doit être placé dans un environnement `Exemple` **séparé**, juste après.

**Pourquoi ?**

- **Lisibilité** : la méthode reste un bloc de référence court et générique, l'exemple reste un bloc indépendant facilement repérable.
- **Évite les bugs de mise en page** : un `Exemple` (ou tout contenu long avec `tcbenumerate`) imbriqué dans `Methode` qui se casse sur deux pages provoque la duplication du titre du bloc et un rendu cassé.

**À faire** :

```latex
\begin{Methode}[Étudier la convexité d'une fonction]
Pour étudier la convexité de $f$ sur un intervalle $I$ :
\begin{tcbenumerate}[1]
    \tcbitem Vérifier que $f$ est deux fois dérivable sur $I$.
    \tcbitem Calculer $f'(x)$ puis $f''(x)$.
    \tcbitem Étudier le signe de $f''(x)$ sur $I$.
    \tcbitem Conclure selon le signe.
\end{tcbenumerate}
\end{Methode}

\begin{Exemple}
\acc{Application} : étudions la convexité de $f(x)=x^4$ sur $\R$.
\begin{tcbenumerate}[1]
    \tcbitem $f$ est polynomiale, deux fois dérivable sur $\R$.
    \tcbitem $f'(x)=4x^3$ et $f''(x)=12x^2$.
    \tcbitem Pour tout $x\in\R$, $12x^2\geqslant 0$, donc $f''\geqslant 0$.
    \tcbitem $f$ est convexe sur $\R$.
\end{tcbenumerate}
\end{Exemple}
```

**À NE PAS faire** :

```latex
% INCORRECT : application dans la méthode -> risque de duplication de titre au break
\begin{Methode}[Étudier la convexité]
Pour étudier la convexité de $f$ sur $I$ :
\begin{tcbenumerate}[1]
    \tcbitem ...
\end{tcbenumerate}

\acc{Application} : ...   % INTERDIT, sortir dans un Exemple séparé
\begin{tcbenumerate}[1]
    \tcbitem ...
\end{tcbenumerate}
\end{Methode}
```

### ⚠️ Bloc didactique coupé en fin de page : titre fantôme sur la page suivante

**Symptôme visuel** : quelques glyphes parasites isolés (fragments de mots en gras) apparaissent au haut d'une page, décalés à gauche d'une colonne de texte, sans rapport avec le contenu.

**Cause** : les environnements didactiques bfcours sont `breakable` et posent leur titre en `attach boxed title`. Quand le bloc se coupe entre deux pages, tcolorbox **redessine le titre** au haut de la portion suivante, mais celui-ci est recouvert par le fond blanc du contenu : il n'en dépasse que quelques lettres. Le titre se retrouve alors présent **deux fois** dans le PDF.

**Détection fiable** (à faire systématiquement après compilation d'un cours) : extraire les titres `\begin{Env}[...]` du source, puis vérifier qu'aucun n'apparaît sur deux pages du corps du PDF.

```python
import fitz, re, io
pages = [' '.join(p.get_text().replace(chr(8217), "'").split()) for p in fitz.open(pdf)]
# pour chaque titre normalisé : len([i for i,t in enumerate(pages,1) if titre in t and i>2]) doit valoir 1
```

Attention à deux pièges de comparaison : le PDF rend l'apostrophe droite `'` en apostrophe typographique `’` (à normaliser), et un titre préfixe d'un autre (`Droite des moindres carrés` ⊂ `Droite des moindres carrés de notre série`) produit un faux positif.

**Correctifs, par ordre de préférence** :

1. **Scinder le bloc** en plusieurs environnements plus courts. C'est presque toujours meilleur pédagogiquement : un `Exemple` qui enchaîne trois situations devient trois `Exemple` titrés séparément.
2. **Alléger le bloc** : sortir une figure volumineuse de la `Definition` pour la placer juste avant, dans un `MultiColonnes` autonome.
3. **Réserver la place** avec `needspace` (`\usepackage{needspace}` dans le préambule du fichier maître, le package n'est pas chargé par `bfcours.sty`) :

   ```latex
   \Needspace*{11\baselineskip}
   \begin{Exemple}[Une suite croissante]
   ...
   \end{Exemple}
   ```

   Compter environ 1 `\baselineskip` par ligne rendue, plus 2 pour le titre et les marges du bloc.

**Itérer** : déplacer un bloc en repousse un autre en fin de page (effet domino). Recompiler et relancer la détection après chaque `\Needspace` ajouté, jusqu'à zéro bloc coupé (2 à 3 passes suffisent en pratique).

### Code LaTeX d'un des environnements didactiques

```latex
%Environnement de Définitions
\NewDocumentEnvironment{Definition}{O{} +b}{
\begin{tcolorbox}[
    enhanced,
    before skip=2mm,after skip=2mm,
    colback=white,colframe=defi!50,boxrule=0pt,
    attach boxed title to top left={xshift=1cm,yshift*=1mm-\tcboxedtitleheight},
    varwidth boxed title*=-3cm,
    boxed title style={frame code={
    \path[fill=white!20!defi]
    ([yshift=-1mm,xshift=-1mm]frame.north west)
    arc[start angle=0,end angle=180,radius=1mm]
    ([yshift=-1mm,xshift=1mm]frame.north east)
    arc[start angle=180,end angle=0,radius=1mm];
    \path[left color=defi!100!black,right color=defi!100!black]
    ([xshift=-2mm]frame.north west) -- ([xshift=2mm]frame.north east)
    [rounded corners=1mm]-- ([xshift=1mm,yshift=-1mm]frame.north east)
    -- (frame.south east) -- (frame.south west)
    -- ([xshift=-1mm,yshift=-1mm]frame.north west)
    [sharp corners]-- cycle;
    },interior engine=empty,
    },
    fonttitle=\bfseries,
    title={\large{\liencontent{Définition}{#1}}},
    coltitle =white,
    drop shadow,
    borderline west={0.05mm}{0pt}{defi!80},
    borderline south={0.05mm}{0pt}{defi!80!black},
    overlay={
    \draw[line width=0.5mm, defi!50] 
        ([xshift=0mm,yshift=-0.25mm]frame.south west)--([xshift=0mm]frame.north west); % Bordure gauche
    \draw[line width=0.5mm, defi!50] 
        ([yshift=0mm]frame.south west)--([yshift=0mm]frame.south east); % Bordure du bas
    \ifx#1\empty
        \else
        % Calcul dynamique de la largeur avec \dimexpr
        \node[anchor=north east, fill=white, draw=defi!50, rounded corners] 
        at ([xshift=-0.1\columnwidth]frame.north east) 
        {\begin{minipage}{\dimexpr(\columnwidth - 4cm - 0.2\columnwidth)\relax} 
        \centering \textbf{#1}
        \end{minipage}}; % Correctement fermer la minipage ici
    \fi%
    }
    ]

    \CouleurTexteAccent{defi}
    \CouleursTabular{defi}{defi}{white}{defi!5}{blue!50!black}%{yellow!10!white}
    \CouleursSecondaryTabular{defi}{defi!30!white}{black}{defi!5}{defi}
    \couleurItem{defi}
    #2
    \resetItemBaseColor
    \ResetCouleursTabular
    \ResetCouleursSecondaryTabular
    \ResetCouleurTexteAccent
\end{tcolorbox}
}
```

## Code Python : environnement BFCodePython

`bfcours.sty` ne charge **pas** les boîtes de code (la ligne `\RequirePackage{bfcours-lightLST}` y est commentée, comme `ProfLycee`). Pour afficher un programme Python, charger le package dans le préambule du fichier maître, **après** `bfcours-fonts` (les boîtes utilisent `\faPython` de `fontawesome5`, fourni par `bfcours-fonts`) :

```latex
\usepackage{bfcours}
\usepackage{bfcours-fonts}
\usepackage{bfcours-lightLST} % boîtes BFCodePython
```

Environnements disponibles : `BFCodePython` (sans numéros de ligne), `BFCodePythonNum` (numérotées, 1er numéro en argument), `BFCodePythonAlt` et `BFCodePythonAltNum` (variante graphique).

```latex
\begin{BFCodePython}
def u(n):
    return 2*n + 3

print(u(50))   # affiche 103
\end{BFCodePython}
```

Les accents français dans les commentaires passent sans problème (`inputencoding=utf8` est déclaré dans le style `MonPython`).

**⚠️ CONTRAINTE MAJEURE : jamais de `BFCodePython` dans un environnement didactique.**

Les environnements didactiques (`Definition`, `Methode`, `Exemple`, `Remarque`...) capturent leur contenu en **argument body** (`+b` de `xparse`). Le verbatim ne survit pas à cette tokenisation : la compilation casse avec `\begin{lstlisting} ... ended by \end{...}` ou `Emergency stop`. C'est la même contrainte que pour un `EXO` avec `save lower`.

Placer le bloc de code **dans le flux du document**, encadré par des phrases de cours, et réserver l'environnement didactique au commentaire de la méthode :

```latex
\begin{Methode}[Calculer les termes d'une suite au tableur]
...étapes théoriques uniquement...
\end{Methode}

Le mode par \acc{récurrence} se traduit par une \acc{boucle} \texttt{for} :

\begin{BFCodePython}
v = 100
for i in range(10):
    v = 0.8 * v
print(v)
\end{BFCodePython}
```

## Fichier maître : la boîte du niveau de \chapitre

La commande `\chapitre[niveau]{thème}{type d'établissement}{établissement}{supplément}{type de document}` place le niveau dans une `tcolorbox` de **largeur fixe 1,5 cm** (définie dans `bfcours-exoplus.sty`). Un niveau plus long **déborde silencieusement** et vient chevaucher le titre du document dans le bandeau.

Les valeurs standard (`$\mathbf{2^{\text{nde}}}$`, `$\mathbf{1^{\text{ère}}}$`, `$\mathbf{T^{\text{Le}}}$`) tiennent. Pour un niveau composé (séries technologiques, options), empiler sur deux lignes :

```latex
\chapitre[
    \shortstack{$\mathbf{1^{\text{ère}}}$\\[-2pt]{\scriptsize techno}}%
    ]{
    Suites numériques%
    }{ Lycée }{ Établissement exemple }{ }{ Cours : }
```

Toujours vérifier le bandeau de la page 1 sur le PDF rendu : le débordement ne produit **aucun avertissement** dans le `.log`.

## Environnement générique bfEnv

A utiliser dans le cas ou aucun environnement didactique approprié ne correspond.
Il s'agit de l'environnement bfEnv.

### Syntaxe de bfEnv

```latex
\begin{bfEnv}{Envname}[Mon Titre][color]
contenu
\end{bfEnv}
```

## Gestion des espaces réponses pour les élèves

- short_line :

    ```latex
    \repsim[1.5cm]{contenu} % Taille largeur adaptable.
    ```

- adaptive_line :

    ```latex
    \tcfillcrep{texte}
    ```

- multiline :

    ```latex
    \setrdcrep{seyes=true,correction font=\normalsize,correction color=prop} % configuration par défaut à ne pas recharger.
    \begin{crep}[style tcolorbox optionnel de la boite]
        contenu
    \end{crep}
    ```

**Styles tcolorbox pour crep**: La configuration par défaut est la plus souvent utilisée. Mais on pourra utiliser des variantes :

Variante pour les figures :

```latex
\setrdcrep{seyes=false,correction font=\normalsize,correction color=black}
\begin{crep}[colback=white,colframe=black,boxrule=0.4pt,halign=center,valign=center]
    contenu
\end{crep}
```

**Note critique** : Utiliser systématiquement ces environnements pour accueillir les réponses élèves.

## Styles TikZ pour la géométrie

Les documents bfcours incluent des presets TikZ pour la géométrie. Ces styles sont définis dans le fichier principal et doivent être utilisés pour assurer la cohérence visuelle.

### Commande Vecteur

```latex
\newcommand{\Vecteur}[1]{\overrightarrow{#1}}
```

### Styles TikZ disponibles

```latex
\tikzset{
    quadrillage/.style={help lines, gray!40},
    epais/.style={thick, line width=1.2pt},
    axe/.style={->, >=stealth, thick, black},
    % Points avec croix droites visibles
    point/.style={cross out, draw, minimum size=5pt, line width=0.8pt, inner sep=0pt},
    point correction/.style={cross out, draw, minimum size=5pt, line width=1.2pt, inner sep=0pt, red},
    % Segments standard
    segment/.style={thick},
    % Vecteurs avec flèches
    vecteur/.style={->, >=stealth, thick},
    % Couleurs standard pour différencier
    couleur1/.style={blue},
    couleur2/.style={red},
    couleur3/.style={green!60!black},
    prop/.style={blue!60!cyan},
    % Labels de points
    label point/.style={font=\normalsize},
}
```

### Commandes de géométrie

**Axes** :
```latex
\XAxe{xmin}{xmax}{liste graduations}  % Axe des abscisses
\YAxe{ymin}{ymax}{liste graduations}  % Axe des ordonnées
\origine                               % Point O à l'origine
```

**Points** :
```latex
\pointC{x}{y}{Label}{position}           % Point standard (croix)
\pointCorrection{x}{y}{Label}{position}  % Point en rouge pour corrections
```

### Figures placées dans une colonne de MultiColonnes

Une `tikzpicture` insérée dans un `\tcbitem` est **rognée au bord de la colonne** si elle est trop large : le symptôme typique est un label d'axe coupé en plein mot (« $n$ (séance »), accompagné d'un `Overfull \hbox` dans le `.log`.

Deux réflexes :

1. **Ancrer les labels d'axes vers l'intérieur de la figure.** Un node `below right` en bout de flèche déborde vers la droite ; `above left` le fait au contraire s'étendre vers l'intérieur, dans la zone laissée libre par le nuage.

   ```latex
   % INCORRECT : le label déborde à droite et se fait rogner
   \draw[->,>=stealth,thick] (0,0) -- (7.6,0) node[below right,font=\scriptsize] {$n$ (séances)};

   % CORRECT : le label reste dans la boîte
   \draw[->,>=stealth,thick] (0,0) -- (7.3,0) node[above left,font=\scriptsize] {$n$ (séances)};
   ```

2. **Piloter la taille par `x=` et `y=` plutôt que par `scale`.** Deux unités indépendantes permettent d'ajuster la largeur (contrainte par la colonne) sans écraser la hauteur. Dans une `MultiColonnes{2}` sur `\textwidth` = 19 cm, viser **6,5 cm de large maximum**, labels d'axes compris — soit environ `x=0.70cm` pour un repère de $0$ à $7$.

   ```latex
   \begin{tikzpicture}[x=0.70cm,y=0.058cm,baseline=(current bounding box.center)]
   ```

   `baseline=(current bounding box.center)` est indispensable pour que la figure s'aligne correctement avec le texte de la colonne voisine.

Toujours contrôler `grep -c "Overfull .hbox" <log>` après ajout d'une figure : un débordement supérieur à ~2 pt est visible à l'impression.

### Exemple d'utilisation

```latex
\begin{tikzpicture}[scale=0.7]
% Droites
\draw[gray,thin] (-0.5,-0.17) -- (3.5,1.17);
% Vecteurs
\draw[vecteur,blue] (3,1) -- (0,0) node[midway,below] {$\Vecteur{AB}$};
% Points avec le style point
\node[point] at (0,0) {}; \node[below left] at (0,0) {$A$};
\node[point] at (3,1) {}; \node[below right] at (3,1) {$B$};
% Ou avec la commande pointC
\pointC{0.5}{1.5}{E}{above left}
\end{tikzpicture}
```

### ⚠️ RÈGLE ABSOLUE : Tous les points en cross out

**Tout point mathématique tracé dans une figure TikZ DOIT être représenté par une croix (cross out)**, jamais par un disque rempli, un cercle plein ou un point Unicode. C'est la convention universelle en mathématiques (collège, lycée, prépa, université). « C'est comme ça qu'on fait des maths. »

S'applique à **tous les contextes** sans exception :

- Points d'une figure géométrique (sommets, milieux, intersections)
- Points d'une courbe (points de tangence, points de sécante, points remarquables)
- Points d'inflexion, extrema locaux, racines
- Points dans une activité, un exercice, un cours, une évaluation

**Toujours faire** :

```latex
% Point neutre (noir)
\node[point] at (1,2) {};

% Point coloré (la couleur s'applique au trait de la croix)
\node[point,blue] at (-1,1) {};
\node[point,red!80!black] at (2,4) {};

% Point d'inflexion / point remarquable - croix plus grosse
\node[point,green!50!black,line width=1.2pt,minimum size=7pt] at (0,0) {};

% Boucle sur plusieurs points (ex : points de tangence)
\foreach \a in {-1.5,-0.5,0.5,1.5} \node[point,blue] at (\a,{\a*\a}) {};

% Equivalent via la commande haut niveau (avec label)
\pointC{0.5}{1.5}{E}{above left}
\pointCorrection{2}{3}{F}{above right}  % en rouge pour les corrections
```

**À NE JAMAIS faire** :

```latex
% INTERDIT : disque rempli
\node[circle,fill=blue,inner sep=1.3pt] at (1,2) {};
\fill[blue] (1,2) circle (2pt);

% INTERDIT : caractere Unicode ou puce
\node at (1,2) {•};
\node at (1,2) {\textbullet};

% INTERDIT : cercle plein dessine via draw
\draw[fill=red] (1,2) circle (0.05);
```

**Pourquoi** : la croix (cross out) marque la position exacte par l'intersection des deux traits, contrairement à un disque qui n'indique que le centre approximatif. C'est la convention pédagogique attendue, du collège à la terminale.

**Style officiel défini dans le préambule bfcours** :
```latex
point/.style={cross out, draw, minimum size=5pt, line width=0.8pt, inner sep=0pt}
point correction/.style={cross out, draw, minimum size=5pt, line width=1.2pt, inner sep=0pt, red}
```

## Comportements normaux à connaître avant d'écrire

Ces trois comportements ne sont pas des bugs : c'est à celui qui écrit le document de les connaître. Ne pas les « diagnostiquer » ni chercher à les corriger dans le package.

- **`\tcfillcrep` demande deux passes de compilation.** Il mesure la place restante sur la ligne à partir de la passe précédente : après une seule passe, le rendu est faux (contenu mal placé ou qui déborde). Juger le rendu seulement après `quick_compile.py --passes 2`. Il reste réservé aux réponses courtes en fin de ligne ; une phrase va dans `\repsim` ou `\repline`.
- **`halign=center` d'une tcolorbox justifie un texte long.** Une ligne courte est centrée ; un paragraphe de plusieurs lignes est justifié, seule la dernière ligne reste centrée. C'est le comportement prévu. Pour centrer chaque ligne d'un texte long (titre en gros corps, par exemple), écrire `halign=flush center`.
- **`tcbraster` (et `tcbitemize`) ne forme sa grille que dans une tcolorbox.** Posé nu dans le corps du document, il empile ses boîtes les unes sous les autres. L'imbriquer dans une tcolorbox conteneur, par exemple `\begin{tcolorbox}[blankest, nobeforeafter] … \end{tcolorbox}`. `MultiColonnes` fournit déjà ce conteneur.

## Anti-patterns sans message d'erreur

Pièges bfcours qui compilent sans avertissement (ou avec un message trompeur) mais produisent un rendu faux — le `.log` ne les signale pas, seule la relecture du PDF les révèle. Ces comportements viennent de LaTeX lui-même ou d'interactions entre paquets, pas d'un bug de bfcours : pas de correctif dans le package, seulement une manière de l'éviter.

### 1. `\resizebox` pour caler un mot sur une largeur de cellule

**Symptôme** : le mot déborde sur la ligne du dessus, ou la marge basse du bandeau semble amputée — sans erreur ni warning.

**Cause** : `\resizebox` ne redimensionne que la largeur/hauteur demandées, il ne réserve pas l'espace vertical d'origine du contenu. Un `\mbox` composé uniquement de capitales a par ailleurs une profondeur (depth) quasi nulle, ce qui ampute toute marge basse calculée dessus.

**À faire** : mesurer la largeur cible avec `\settowidth`, choisir un `\fontsize` qui produit un mot de cette largeur, et envelopper le résultat d'un `\strut` pour restaurer une hauteur/profondeur cohérente.

```latex
% INCORRECT : ne réserve pas sa hauteur, chevauche la ligne du dessus
\resizebox{2cm}{!}{\textbf{MATERIEL}}

% CORRECT
\newlength{\largeurcible}
\settowidth{\largeurcible}{MATERIEL}
\mbox{\strut\fontsize{14}{16}\selectfont MATERIEL}
```

### 2. bfcours-fonts écrase la taille de `\documentclass`

**Symptôme** : `\documentclass[14pt]{...}` n'a visiblement aucun effet, tout le corps de texte reste à sa taille par défaut.

**Cause** : `bfcours-fonts` charge `\usepackage[fontsize=12]{scrextend}`, qui réinitialise silencieusement la taille de police globale et écrase l'option de taille passée à `\documentclass`.

**À faire** : ne pas compter sur l'option de taille de la classe dans un document chargeant bfcours-fonts (affiche, etc.) ; calibrer chaque bloc de texte explicitement avec `\fontsize{..}{..}\selectfont`.

```latex
% INCORRECT : sans effet avec bfcours-fonts
\documentclass[14pt]{article}

% CORRECT : taille fixée bloc par bloc
{\fontsize{18}{20}\selectfont Titre de bloc}
```

### 3. Noms réservés : ne jamais redéfinir `\lg`, `\deg`, `\min`, `\max`, `\arg`, `\det`...

**Symptôme** : compilation cassée ou comportement incohérent après avoir déclaré une longueur ou une commande personnelle nommée `\lg` (ou un autre opérateur mathématique standard).

**Cause** : `\lg` est déjà l'opérateur logarithme natif de LaTeX, au même titre que `\deg`, `\min`, `\max`, `\arg`, `\det`, `\sin`... Le redéfinir via `\newlength`/`\newcommand` écrase silencieusement l'opérateur existant.

**À faire** : préfixer systématiquement les noms de longueurs et commandes personnelles, ne jamais utiliser le nom nu d'un opérateur mathématique.

```latex
% INCORRECT
\newlength{\lg}

% CORRECT
\newlength{\lgCellule}
```

### 4. xcolor : composer une couleur déjà mélangée

**Symptôme** : `Undefined color '25'`, `Undefined color '70'`, ou une cascade `Missing number` / `Illegal unit` en aval — typiquement dans un `\foreach` ou une macro qui reçoit une couleur en argument.

**Cause** : xcolor ne sait composer qu'une expression `couleur!pourcentage!couleur` à la fois. Si la couleur reçue en argument (ou itérée dans un `\foreach`) est déjà un mélange (`black!45`, `black!75`), la composer une seconde fois par simple concaténation (`#2!70!black`, `\c!25!white`) produit une chaîne invalide (`black!45!70!black`).

**À faire** : figer la couleur reçue avec `\colorlet` dans un identifiant neuf avant de composer.

```latex
% INCORRECT : #2 peut déjà être un mélange (ex. black!75)
\newcommand{\Picto}[2]{\draw[#2!70!black] (0,0) circle (1);}

% CORRECT : on fige la couleur avant de composer
\newcommand{\Picto}[2]{%
    \colorlet{couleurPicto}{#2}%
    \draw[couleurPicto!70!black] (0,0) circle (1);
}
```

### 5. `\underbrace` dans un `crep` seyes

**Symptôme** : l'accolade et son annotation débordent sous la ligne de base et se superposent au texte de la ligne suivante — aucun avertissement dans le `.log`.

**Cause** : la grille seyes du `crep` fixe un interligne rigide pour aligner les lignes du cahier. Un élément qui descend en profondeur (underbrace, indice de grande taille) n'a pas d'espace réservé et mord sur la ligne suivante.

**À faire** : placer toute formule annotée par un `\underbrace` en **dernière ligne** du `crep`, jamais au milieu.

```latex
% INCORRECT : underbrace au milieu du crep -> chevauche la ligne suivante
\begin{crep}
$P(A) = \underbrace{P(A \cap B)}_{=0,2} + P(A \cap \bar B)$
Donc $P(A \cap \bar B) = \dots$
\end{crep}

% CORRECT : underbrace en dernière ligne
\begin{crep}
Donc $P(A \cap \bar B) = \dots$

$P(A) = \underbrace{P(A \cap B)}_{=0,2} + P(A \cap \bar B)$
\end{crep}
```

### 6. Icônes fontawesome5 indéfinies (`\faFileAlt`, `\faShieldAlt`...)

**Symptôme** : `Undefined control sequence` sur `\faFileAlt` ou `\faShieldAlt`, alors que les entrées `file-alt` et `shield-alt` existent bien dans la documentation fontawesome5.

**Cause** : bfcours charge à la fois `fontawesome` (v4) et `fontawesome5` ; pour certaines icônes renommées entre les deux versions, l'entrée du mapping v5 a un premier argument vide (collision de nom avec la v4) : aucune macro `\faXxx` n'est générée pour elles.

**À faire** : utiliser systématiquement la macro générique `\faIcon{nom-avec-tirets}`, dont l'existence ne dépend pas du mapping court.

```latex
% INCORRECT : Undefined control sequence
\faFileAlt \faShieldAlt

% CORRECT
\faIcon{file-alt} \faIcon{shield-alt}
```

### 7. `\degres` (babel-french) rendu en « r caron » avec bfcours-fonts

**Symptôme** : le symbole degré s'affiche comme un « ř » dans le PDF (ex. « n°1 » devient « nř1 »), sans erreur de compilation.

**Cause** : bfcours-fonts change la police active ; le glyphe attendu par la commande babel-french `\degres` n'existe pas dans cette police, et un glyphe de substitution visuellement proche — mais faux — est utilisé à la place.

**À faire** : utiliser `\textdegree` en mode texte, ou la notation `$^{\circ}$` en mode math (déjà la convention bfcours pour les angles, voir plus haut) ; ne jamais utiliser `\degres`.

```latex
% INCORRECT : rendu "nř1" au lieu de "n°1"
Devoir surveillé n\degres{}1

% CORRECT
Devoir surveillé n\textdegree{}1
```

### 8. `couleur1`/`couleur2`/`couleur3` sont des styles TikZ, pas des couleurs xcolor

**Symptôme** : `Undefined color 'couleur1'` (ou une variante avec un pourcentage, `couleur1!10`) en essayant d'utiliser `couleur1`, `couleur2` ou `couleur3` comme couleur (`colback=`, `\color{}`, mélange `!`).

**Cause** : ces trois noms sont des styles `\tikzset` (`couleur1/.style={blue}`, etc. — voir la section « Styles TikZ pour la géométrie » ci-dessus), enregistrés uniquement dans l'espace de noms des styles TikZ, jamais déclarés comme couleurs xcolor.

**À faire** : dans un contexte TikZ, les utiliser tels quels comme option de style (`[couleur1]`) ; dans un contexte xcolor (mélange, `colback`, `\color{}`), utiliser la couleur réelle qu'ils désignent (`blue`, `red`, `green!60!black`).

```latex
% INCORRECT : couleur1 n'est pas une couleur xcolor
\draw[couleur1!10] (0,0) circle (1);

% CORRECT : style TikZ tel quel
\draw[couleur1] (0,0) circle (1);
% CORRECT : couleur xcolor réelle si un mélange est nécessaire
\draw[blue!10] (0,0) circle (1);
```

### 9. `MultiColonnes` après un `\tcbitem` court : la ligne vide reste obligatoire

**Symptôme** : dans une correction d'EXO, un `MultiColonnes` qui suit immédiatement un court texte de `\tcbitem` (sans ligne vide entre les deux) se place à côté ou au-dessus du texte au lieu d'être dessous.

**Cause** : cas particulier de la règle déjà documentée plus haut (« Présentation en grille avec MultiColonnes », ligne vide obligatoire avant `\begin{MultiColonnes}`) : un texte de `\tcbitem` très court laisse croire, à tort, que la contrainte ne s'applique qu'aux longs paragraphes. Elle s'applique identiquement.

**À faire** : toujours séparer un `\tcbitem` de texte du `MultiColonnes` qui suit par une ligne vide, y compris quand le texte est court.

```latex
% INCORRECT : pas de ligne vide -> le bloc se place mal
\tcbitem[boxrule=0.4pt,colframe=black] Points du cercle à 30$^\circ$ :
\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$
\tcbitem \textbullet Point $B$
\end{MultiColonnes}

% CORRECT
\tcbitem[boxrule=0.4pt,colframe=black] Points du cercle à 30$^\circ$ :

\begin{MultiColonnes}{2}
\tcbitem \textbullet Point $A$
\tcbitem \textbullet Point $B$
\end{MultiColonnes}
```

Par la même contrainte de largeur fixe des colonnes, un `\encadrer` ou un `\tcfillcrep` dont le contenu est trop long pour sa colonne est **rogné sans avertissement** dans un `MultiColonnes` : raccourcir le contenu ou réduire le nombre de colonnes plutôt que de laisser déborder.

### 10. `\ExoSaut` par défaut (6,5 cm) trop court pour un EXO insécable avec figure

**Symptôme** : le bandeau titre d'un exercice reste isolé en bas de page, son corps (un `MultiColonnes` avec figure, ~9 cm) démarrant en haut de la page suivante — aucun avertissement dans le `.log`.

**Cause** : `\ExoSaut` est une macro locale déclarée en tête d'un `enonce.tex` de fiche d'exercices (pas dans le package bfcours), qui force un saut de page conditionnel si la place restante sur la page est inférieure à un seuil par défaut de 6,5 cm. Si le premier bloc insécable de l'exercice suivant est plus haut que ce seuil, le calcul ne protège pas assez et le bandeau se retrouve seul en bas de page.

**À faire** : donner explicitement à `\ExoSaut` un seuil couvrant la hauteur réelle du bloc insécable qui suit, via son argument optionnel. Revérifier ce seuil après tout réordonnancement d'exercices (déplacer un exercice invalide les seuils déjà calibrés pour ses voisins).

```latex
% INCORRECT : seuil par défaut (6.5cm) trop court pour un corps de ~9cm
\ExoSaut
\input{Exercice/coordonnees_lecture_somme}

% CORRECT : seuil explicite couvrant la hauteur réelle du bloc suivant
\ExoSaut[10.5cm]
\input{Exercice/coordonnees_lecture_somme}
```

### 11. Formule isolée dans un `\tcbitem` : `parskip` nul, collée au texte

**Symptôme** : dans un `\tcbitem` de `tcbenumerate`/`MultiColonnes`, une formule en mode `$...$` inline placée sur sa propre ligne (ou un `\encadrer` en fin de ligne) se colle visuellement au texte qui précède ou qui suit, rendu illisible.

**Cause** : `\tcbitem` fixe `parskip` à 0 en interne ; un `\setlength{\parskip}` placé après `\exocorrection` est sans effet, le contenu de l'EXO étant rejoué via `save lower`.

**À faire** : ne jamais isoler une formule en mode inline sur sa propre ligne dans un `\tcbitem` ; la passer en mode display (`align*` pour plusieurs lignes, ou intégrer la formule dans la phrase).

```latex
% INCORRECT : formule isolée en inline, collée au texte
\tcbitem Le taux d'évolution est
$\tau = \dfrac{V_f - V_i}{V_i}$
donc le résultat est \encadrer[defi]{$\tau \approx 0,12$}

% CORRECT : formule en mode display
\tcbitem Le taux d'évolution est :
\begin{align*}
\tau = \dfrac{V_f - V_i}{V_i}
\end{align*}
Donc \encadrer[defi]{$\tau \approx 0,12$}.
```

### 12. Argument vide de `\chapitre` écrit sur sa propre ligne : `\par` fatal

**Symptôme** : `Paragraph ended before \chapitre was complete` suivi de `Too many }s` (parfois en double, un jeu par appel de `\chapitre`).

**Cause** : `\chapitre` n'est pas déclaré `\long` ; une ligne blanche à l'intérieur d'un de ses arguments produit un `\par` implicite, ce qui met fin prématurément à l'argument en cours de lecture. Un générateur de fichier maître qui écrit un argument vide sur sa propre ligne (`{` puis retour à la ligne puis `}`) déclenche systématiquement l'erreur.

**À faire** : écrire tous les arguments de `\chapitre`, y compris les arguments vides, sur la **même ligne** que les accolades voisines — jamais un `{` seul suivi d'un retour à la ligne.

```latex
% INCORRECT : argument vide sur sa propre ligne -> \par fatal
\chapitre[...]{Probabilités conditionnelles}{Lycée}{Établissement exemple}{
}{Exercices :}

% CORRECT : argument vide sur la même ligne
\chapitre[...]{Probabilités conditionnelles}{Lycée}{Établissement exemple}{ }{Exercices :}
```
