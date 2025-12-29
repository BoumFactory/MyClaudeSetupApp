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
  - **⚠️ CRITIQUE** : La commande `\encadrer` **sort du mode maths** même si elle est appelée dans un environnement mathématique. Il faut donc **TOUJOURS ré-entrer en mode maths** à l'intérieur de `\encadrer` quand on encadre des maths.
  - **Exemple correct** : `\[u_{\text{display}} = \encadrer[red]{$\dfrac{5}{6}$} - 4\]`
  - **Exemple incorrect** : `\[\encadrer[red]{\dfrac{5}{6}}\]` (provoque une erreur de compilation)
- logique : \Si ; \Alors ; \Donc ; \Mais ; \SSI ; \Et

### Cas d'utilisation

Au sein des environnements didactiques, on met systématiquement en acc les mots de vocabulaire déjà définis.

Les informations cruciales peuvent être encadrées.

Les verbes d'action élèves doivent être en acc. \acc{Calculer} ... \acc{Déterminer} ... 

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

Propriete, Definition, Remarque, Demonstration, Theoreme, Activite, Notation, Exemple

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

**Note** : Toujours utiliser `node[point]` ou `\pointC` pour placer des points, jamais `\fill ... circle`.
