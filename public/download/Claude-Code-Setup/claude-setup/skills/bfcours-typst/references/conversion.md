# Retoucher un document après la préconversion LaTeX → Typst

**Ce guide vaut pour les sources déjà écrites avec bfcours ; pour un `.tex` ordinaire, voir `SKILL.md` (section « Convertir un document LaTeX »).**

`convertir.py` fait l'essentiel de la conversion d'un document LaTeX bfcours : il écrit un `.typ` qui compile en version professeur et élève. Ce guide sert à **finir le travail** : lire le rapport, regarder le rendu, retoucher ce que le script signale. La démarche courte est dans `SKILL.md` ; ici, le détail.

## Sommaire

1. Ce que fait le convertisseur, ce qu'il ne fait pas
2. Lancer la préconversion
3. Lire le rapport
4. Traiter chaque catégorie du rapport
5. Contrôle visuel : prof, élève, PDF LaTeX d'origine
6. Correspondances pour retoucher à la main
7. Figures : garder l'extrait LaTeX ou redessiner
8. Maintenir le convertisseur (« le paquet a changé »)

## 1. Ce que fait le convertisseur, ce qu'il ne fait pas

Il fait :

- lire le maître et tous ses `\input` (macros locales comprises) ;
- traduire chaque **commande** bfcours vers la fonction de même nom en kebab-case (`Definition` → `definition`, table `scripts/donnees/kebab.json`) ; les options deviennent des clés, **validées contre l'index** des fonctions (une option sans clé connue est écartée et notée, jamais devinée) ;
- traduire chaque **environnement** `\begin{X}…\end{X}` dont la fonction a la forme environnement en syntaxe `#begin(X, clés)[titre]` … `#end(X)` (voir plus bas) ;
- traduire les formules en mode maths Typst lisible (lettres séparées, `display`, virgule décimale…) ;
- traduire `tkz-tab` en `tabvar`, les minipages en `#begin(multi-colonnes, largeurs: …)`, le préambule en `#show: modele(…)` ;
- garder **fidèlement** ce qui n'a pas d'équivalent (figure TikZ, pstricks, environnement inconnu) sous forme d'extrait `#latex[…]`, rendu par LaTeX à la compilation ;
- copier les images citées dans `images/` à côté du `.typ` ;
- compiler les deux versions et **réparer** ce que Typst refuse : un bloc fautif devient un extrait LaTeX, un élément en ligne devient un marqueur orange `#a-reprendre("…")` ;
- envelopper dans `#ifcorrection[…]` ce que l'élève ne doit pas voir (partie « Solutions » de fin, `\rdexocorrection` laissé hors de `\ifcorrection`) ;
- écrire un rapport de ce qui reste à reprendre.

Il ne fait pas :

- **juger la mise en page** : coupures de page, `\vspace` de calage, `\newpage` d'ajustement ne se transposent pas ; c'est le rendu Typst qui décide ;
- redessiner une figure : un extrait LaTeX reste un extrait LaTeX ;
- deviner une macro locale compliquée, une option sans équivalent, une commande inconnue de l'index ;
- modifier les `.tex` d'origine (jamais).

### La sortie : commande ou environnement

Règle : une commande LaTeX donne une commande Typst ; un environnement LaTeX donne la syntaxe environnement. Le corps est indenté de 2 espaces par niveau d'imbrication.

```typ
#begin(exo, tags: "2A05")[Résoudre des équations]
  Énoncé.
  #begin(tcbenumerate, columns: 2)
    + #itempoint(1)[Première question.]
      #begin(crep)
        Réponse.
      #end(crep)
    #tcbitem(raster-multicolumn: 2)[Case sur toute la largeur.]
    + Troisième question.
  #end(tcbenumerate)
  #tcblower
  #exocorrection
  Correction.
#end(exo)
```

- **Environnements convertis en `#begin`/`#end`** (liste `FORME_ENVIRONNEMENT` de `regles.py`) : les 20 didactiques (definition, propriete, theoreme, methode, exemple, remarque…, `tcolorbox` isolée → `boite`), exo, exo-eval, chapitre-bac, chapitre-brevet, exolombards, encadre-bac, encadre-bac-etroit, tcbenumerate, enumerate, itemize, multi-colonnes (et minipages côte à côte), tcbraster, crep, mcq, bf-code-python. Les noms LaTeX restent ceux de bfcours (`\begin{Definition}`, `\begin{EXO}`) : `tex2typ/catalogue.py` les traduit par `scripts/kebab.py`.
- **Restent des commandes** : tcbtab et ses variantes (filets, `\multicolumn`, `\cellcolor` sans équivalent en items), tableaux, `geo`/`figure-geo`, `wrapfigure` (le texte enveloppé suit l'environnement en LaTeX), clip-image, filmbox, boîtes `rd*`, extraits `#latex`.
- **Items** : `\item` → `+` (`tcbenumerate`, `enumerate`) ou `-` (`itemize`, `multi-colonnes`, `tcbraster`), contenu multiligne indenté de 2 espaces. `\tcbitem[options]` à clés connues → `#tcbitem(clés)[…]` sur sa propre ligne dans le corps (jamais `+ #tcbitem`). `\tcbitem` sans options → `+` ou `-`. Plus aucune écriture à blocs multiples `[Q1][Q2]`.
- **Options** : `\begin{tcbenumerate}[2][3][\alph]` → `#begin(tcbenumerate, columns: 2, depart: 3, format: "alph")` (alias `columns`) ; `\begin{enumerate}[a)]` → `label: "a)"` ; `\begin{MultiColonnes}{3}` → `#begin(multi-colonnes, 3)` ; `\begin{Definition}[Titre]` → `#begin(definition)[Titre]`.
- **`#exocorrection` et `#tcblower`** restent au premier niveau du corps de l'EXO, entre `#begin(exo…)` et `#end(exo)`.
- **Éléments opaques** : un `#begin` n'est regroupé que dans un corps d'environnement ou au niveau du document ; dans `#ifcorrection[…]`, `#align`, `#block`, `#box`, une cellule de tableau, un `tcbitem(…)[…]`, il faut `#environnements[…]` autour. Le convertisseur l'écrit lui-même (`#ifcorrection[#environnements[…]]`) ; une liste `-`/`+` dans une cellule de tableau reste du balisage natif.
- **Retouche à la main** : ne pas séparer un `#begin` de son `#end` (erreur explicite « begin/end dépareillé » sinon) ; garder le même niveau d'indentation pour les deux.

## 2. Lancer la préconversion

Directement vers le dossier où le `.typ` doit vivre, avec le Python qui a le module `typst` :

```bash
python "<skill>/scripts/convertir.py" "source/cours.tex" -o "dossier/de/travail/"           # → dossier/de/travail/cours.typ
python "<skill>/scripts/convertir.py" "source/cours.tex" -o "dossier/de/travail/fiche.typ"  # nom imposé
python "<skill>/scripts/convertir.py" "source/Exercice/ex1.tex" --fragment --maitre "source/Cours.tex" -o "dossier/"
```

- Sans `-o`, le `.typ` s'écrit à côté du `.tex` : ne l'utiliser que si l'utilisateur veut travailler dans le dossier de la source.
- Un `.typ` existant n'est jamais écrasé sans `--remplacer` : le script écrit alors `<nom>-converti.typ`. Avant `--remplacer`, regarder le fichier existant : il contient peut-être des retouches de l'utilisateur.
- `--fragment` : fichier sans préambule (un `\input`) ; `--maitre` lui donne les réglages et les macros du maître qui l'inclut.
- `--compiler` enchaîne sur `compiler.py --png` ; sinon lancer `compiler.py` soi-même (section 5).

Code de sortie : 0 si les deux versions compilent, 1 sinon (le diagnostic Typst est affiché : le corriger à la main, section 4).

## 3. Lire le rapport

Le rapport s'affiche à la fin de la préconversion. Ses rubriques, dans l'ordre :

| Rubrique | Ce que c'est | Que faire |
|---|---|---|
| `Compilation : OK` / `ÉCHEC` | état des deux versions avant le rendu des extraits LaTeX | `ÉCHEC` : lire l'erreur (fichier:ligne:colonne) et corriger d'abord |
| `Fichiers \input introuvables` | un `\input` dont le fichier manque | retrouver le fichier ; sinon signaler le trou à l'utilisateur |
| `Caractères illisibles` | encodage cassé dans une source | corriger dans le `.typ` (pas dans le `.tex`) |
| `Extraits LaTeX (n)` | figures et constructions gardées en LaTeX, comptées par type | section 7 : les garder sauf demande ou gain net |
| `Replis automatiques` | nœuds que Typst refusait, repliés (extrait ou marqueur orange) | relire chacun : le repli compile mais n'est pas idéal |
| `À reprendre (n)` | la liste de travail : chaque entrée a un marqueur dans le `.typ` | section 4, entrée par entrée |
| `Options LaTeX sans clé Typst (écartées)` | options absentes de l'index | `chercher.py --fiche <fonction>` : une autre clé fait-elle l'effet voulu ? |
| `Commandes inconnues` | commandes sans traduction, avec leur nombre | `chercher.py --latex <nom>`, puis à la main |
| `Ignorées` | commandes sans effet en Typst (`\setcounter`, `\tcbset`…) | rien, sauf si le rendu montre un manque |
| `Images copiées` | images recopiées dans `images/` | vérifier qu'elles s'affichent |

Dans le `.typ`, tout ce qui reste à faire se retrouve par une recherche du mot `a-reprendre` (marqueurs orange visibles dans le PDF) et des commentaires `//` laissés par le convertisseur.

## 4. Traiter chaque catégorie du rapport

**Marqueur `#a-reprendre("…")`.** Le texte entre guillemets est la source LaTeX d'origine. Écrire l'équivalent Typst à sa place (`chercher.py --latex <commande>`, section 6, `typst-essentiel.md`). Quand plus aucun `a-reprendre(` ne reste dans le corps, supprimer la ligne `#let a-reprendre(…)` et son commentaire en tête du fichier.

**« formule à vérifier (…) ».** La formule contient une commande que le traducteur de maths ne connaît pas (nommée entre parenthèses). Regarder la formule dans l'image : si elle est juste, rien à faire ; sinon la réécrire (une macro locale : un `#let` en tête du fichier, `#let Norme(x) = $norm(#x)$`).

**Extrait `#latex[…]`.** Fidèle par construction : il est rendu par LaTeX, mis en cache dans `rendus-tex/` à côté du document. Section 7 pour décider s'il faut le redessiner. Un extrait qui contient une zone de réponse (`\tccrep`, `\crep`…) est écrit deux fois, dans `#ifcorrection[prof][élève]` : retoucher les deux branches à l'identique. Le réglage `#setbflatex(paquets: …, preambule: …)` en tête du fichier charge ce que les extraits demandent (bfcours, polices, macros du document) : ne pas le supprimer tant qu'il reste un extrait.

**Option écartée.** L'option LaTeX n'a pas de clé du même nom. Souvent sans objet (overlay TikZ, `save lower`) ; sinon chercher la clé qui fait l'effet : `chercher.py --fiche exo`, `chercher.py --cle <mot>`. Ne jamais inventer une clé : une clé inconnue arrête la compilation.

**Commande inconnue.** `chercher.py --latex <nom>` d'abord (renommages compris) ; puis `chercher.py "<ce que fait la commande>"`. Une macro du document lui-même : un `#let`.

**Partie « Solutions » enveloppée dans `#ifcorrection[…]`.** Le LaTeX laissait la page des corrigés hors de `\ifcorrection` (le maître élève ne l'incluait pas). En Typst, un seul fichier : sans l'enveloppe, l'élève verrait les corrigés. Vérifier sur l'image élève que la partie a disparu, et sur l'image prof que le second bandeau (`chapitre(…, type: [Solutions :])`) commence bien en tête de page.

**`\rdexocorrection` enveloppé.** Même raison : `#ifcorrection[#rdexocorrection(0)]`.

**`\ifthenelse`, autres conditionnelles : « seule la branche vrai est gardée ».** Décider avec le document d'origine ; si la condition portait sur la version, la remplacer par `#ifcorrection[prof][élève]`.

**Zone de réponse sortie d'une formule.** `$f_1 = \tcfillcrep{…}$` devient `$f_1 =$ #tcfillcrep[…]` : une zone de réponse est un objet de texte, pas de maths. Vérifier la ligne sur l'image ; si la réponse elle-même est une formule, elle s'écrit dans le crochet : `#tcfillcrep[$3 x + 1$]`.

**Échelle d'image.** `\includegraphics[scale=0.5]` n'a pas d'équivalent exact : régler `width:` à la main en regardant l'image.

**Échec persistant de compilation.** Lire le diagnostic : une erreur citée dans un fichier de paquet vient presque toujours d'un argument mal formé dans l'appel du document (remonter la trace). Les erreurs du langage : `typst-essentiel.md`, section 9.

## 5. Contrôle visuel : prof, élève, PDF LaTeX d'origine

```bash
python "<skill>/scripts/compiler.py" "dossier/de/travail/cours.typ" --png
```

- Écrit `cours-prof.pdf` et `cours-eleve.pdf` à côté du `.typ`, rend les extraits LaTeX (cache `rendus-tex/`), et une image par page dans `.apercu/cours-prof/` et `.apercu/cours-eleve/`. C'est exactement ce que l'utilisateur obtient au Ctrl+Maj+B dans VS Code.
- **Regarder les images des deux versions.** Prof : réponses en couleur, corrigés présents. Élève : mêmes places, vides ; aucune réponse, aucun corrigé.
- **Comparer au PDF LaTeX d'origine** s'il existe à côté de la source (`Cours.pdf`, `Cours_ELEVE.pdf` ; ne pas le recompiler). Le rendre en images avec PyMuPDF (`fitz.open(pdf)`, `page.get_pixmap(dpi=80).save(…)`) dans `.apercu/<nom>-latex/` du dossier de travail, par un petit script écrit avec Write ; `--nettoyer` les retirera avec les autres.
- Écarts acceptables : coupures de page un peu différentes, Seyès ou espacements de quelques millimètres. Écarts à corriger : contenu manquant, réponse visible chez l'élève, formule fausse, figure absente ou vide, tableau mal placé.
- Retoucher, relancer `compiler.py --png`, regarder de nouveau. En fin de travail : `compiler.py <doc>.typ --nettoyer` retire `.apercu/`. Garder `rendus-tex/` : c'est le cache des extraits, l'extension s'en sert au Ctrl+Maj+B. Le convertisseur écrit déjà `lire: p => read(p, encoding: none)` dans le `#setbflatex` du document : l'aperçu Tinymist (Ctrl+S) montre ainsi les extraits déjà rendus ; Ctrl+Maj+B (ou `compiler.py`) rend les nouveaux et produit les PDF. Pour un document existant sans cette clé, l'ajouter à son `setbflatex` (ou une ligne `#setbflatex(lire: …)`).

## 6. Correspondances pour retoucher à la main

Pour une commande bfcours absente de ces tables : `chercher.py --latex <nom>` (sans antislash). Pour le LaTeX standard : `typst-essentiel.md`, section 8.

### Préambule et en-tête

| LaTeX bfcours | Typst |
|---|---|
| `\documentclass…`, `\usepackage{bfcours}`, `bfcours-fonts` | `#import "@preview/farfadet:0.2.0": *` puis `#show: modele("cours", …)` |
| `geometry{left=1cm,…}` | clé `marges: (left: 1cm, right: 1cm)` du modèle |
| `\usepackage{bfcours-fonts-dys}` | clé `dys: true` |
| `\chapitre[2nde]{Thème}{Cycle}{Établissement}{zone droite}{Cours :}` | clés `niveau`, `theme`, `cycle`, `etablissement`, `zone-droite`, `type-document` du modèle ; « Cours : », « Exercices : », « Activité : », « Fiche : » donnent le type court (`type-document: "cours"`…, le « : » est le séparateur par défaut) ; autre libellé en contenu : `type-document: [Fiche 1 :]` (une espace suffit après un libellé qui finit par « : ») ; séparateur : `separateur-type: " - "` (texte entre guillemets : `[ - ]` serait lu comme une puce), `[ ]` pour l'ancien rendu sans deux-points ; libellés renommés : `libelles-types: (cours: [Leçon], tp: [TP])` |
| second bandeau | `#pagebreak()` puis `#chapitre(niveau: …, theme: …, type: [Solutions :])` (sans le saut, le pied de page change de libellé) |
| `\chapEval` | `type-document: "evaluation"` |
| `\setrdexo{display exotitle, display score=false, skin=…}` | `#setrdexo(display-exotitle: true, display-score: false, skin: "…")` |
| `\setrdcrep{seyes, correction=true, correction color=prop}` | `#setrdcrep(seyes: true, correction-color: "prop")` ; **ne pas reporter `correction=…`** : la version vient de la compilation |
| `\def\rdifficulty{1.5}` | `#rdifficulty(1.5)` ou `level: 1.5` sur l'exercice |
| `\displayitempointsfalse` / `true` | `#displayitempoints(false)` / `(true)` |
| `\tcbset{tccrepdefaultstyle/.style={…}}` | `#setrdcrep(pour: "tccrep", …)` (clés : `--fiche tccrep`) |

### Corps

| LaTeX bfcours | Typst |
|---|---|
| `\begin{Definition}[Titre] … \end{Definition}` (et Propriete, Theoreme, Methode, Exemple…) | `#begin(definition)[Titre]` … `#end(definition)` ; sans titre `#begin(definition)` |
| `\begin{EXO}{Titre}{tags} énoncé \exocorrection correction \end{EXO}` | `#begin(exo, tags: "tags")[Titre]` puis énoncé, `#exocorrection`, correction, `#end(exo)` |
| `\tcblower` dans un EXO | `#tcblower`, avant `#exocorrection`, au premier niveau du corps |
| `\begin{EXOEVAL}{Titre}{compétence}` | `#begin(exo-eval, tags: "compétence")[Titre]` … `#end(exo-eval)` |
| `\ifcorrection A \else B \fi` | `#ifcorrection[A][B]` (`#environnements[…]` autour d'un contenu qui a un `#begin`) |
| `\begin{tcbenumerate}[2] \tcbitem A \tcbitem B` | `#begin(tcbenumerate, columns: 2)` puis `+ A`, `+ B`, `#end(tcbenumerate)` ; reprise : `depart: 3` |
| `\tcbitem \tcbitempoint{2} Énoncé` | `+ #itempoint(2)[Énoncé]` |
| `\begin{enumerate}[a)] \item …`, `\begin{itemize} \item …` | `#begin(enumerate, label: "a)")` + items `+` ; `#begin(itemize)` + items `-` |
| `\begin{MultiColonnes}{3} \tcbitem A …` | `#begin(multi-colonnes, 3)` puis une colonne par `- A`, `- B`, `- C` |
| `\tcbitem[halign=flush center]` | `#tcbitem(halign: "center")[…]` sur sa propre ligne du corps, à la place d'un `+` ou d'un `-` |
| `\begin{crep} réponse \end{crep}`, `\repline[2]` | `#begin(crep, extra-lines: 2)` + réponse + `#end(crep)` (ou `lines: 2`) |
| `\tccrep{3cm}{réponse}`, `\tcfillcrep{…}` | `#tccrep(3cm)[réponse]`, `#tcfillcrep[…]` |
| `\Vecteur{AB}`, `\Coordonnees[A]{x}{y}` | `$vect(A B)$`, `$coordonnees(x, y, nom: A)$` ; `-1{,}5` → `-1","5` |
| `\acc{x}`, `\encadrer[defi]{x}`, `\voc{mot}` | `#acc[x]`, `#encadrer(couleur: "defi")[x]`, `#voc[mot]` |
| `\oe`, `\OE`, `\euro` | `c#oe;ur`, `#oe-maj;uvre`, `#euro` (farfadet-socle ; le `;` clôt l'appel au milieu d'un mot), ou les caractères `œ`, `Œ`, `€` |
| `\begin{tcbtab}{\|c\|c\|}` | `#tcbtab("\|c\|c\|", …cellules)` : spécification acceptée telle quelle ; **collé à gauche** comme `\tcbtab` ; filets horizontaux entre toutes les rangées (comme un `\hline` après chaque rangée) |
| `\tcbtabc` | `tcbtab(…, align: center)` |
| tableau aux seuls filets verticaux (ancien rendu) | `filets: "verticaux"` ; en-tête coloré par `\cellcolor` → `entete: true` |
| `\competence{…}` dans `\tableaucompetence{…}` | `#tableaucompetence(competence[…], competence[…])` |
| `\newpage`, `\Needspace*{13\baselineskip}` | `#pagebreak()` seulement pour un vrai changement de partie ; `#needspace(13em)` seulement si un titre reste seul en bas de page sur l'image |

### Tableaux de signes et de variations : `tkz-tab` → `tabvar`

| tkz-tab | farfadet-tabvar |
|---|---|
| `\tkzTabInit[lgt=1.5,espcl=2.4]{$x$/1,$f(x)$/2}{$-\infty$,$-1$,$+\infty$}` | `tabvar(("-oo", "-1", "+oo"), …lignes…, lgt: 1.5cm, espcl: 2.4cm)` ; nom et hauteur d'une ligne dans la ligne (`h: 2`) |
| `\tkzTabLine{,+,z,-,}` | `tkz-tab-line($f'(x)$, ",+,z,-,")` |
| `\tkzTabVar{-/$-\infty$, +/$2$}` | `tkz-tab-var($f(x)$, ("-", "-oo"), ("+", "2"))` ; `R/` → `"R"` ; `+D-/a/b` → `("+D-", a, b)` |
| `\tkzTabIma`, `\tkzTabVal`, `\tkzTabDeriv` | `("im", v)` dans la colonne ; les deux autres sans équivalent |
| version élève | `tabvar(…, a-completer: true)` |

## 7. Figures : garder l'extrait LaTeX ou redessiner

Par défaut, **garder l'extrait `#latex[…]`** : il reproduit la figure d'origine au pixel près et l'utilisateur la retrouve telle qu'il l'a conçue. Le redessiner seulement si l'utilisateur le demande, ou si le gain est net (figure de géométrie plane simple que l'on voudra modifier en Typst, extrait qui échoue à se rendre).

Redessiner une figure de géométrie plane : `farfadet-geom` (réexporté par le méta-paquet), tout dans `#geo({ … })`, points en couples `let A = (0, 0)`.

| TikZ / bfcours LaTeX | farfadet-geom |
|---|---|
| `tikzpicture` | `#geo({ … })` (`unite: 0.9cm`, `fenetre: ((x0, y0), (x1, y1))`) ; légendée : `figure-geo` |
| `\XAxe`, `\YAxe`, `\origine`, grille | `repere(x: (-3, 4), y: (-2, 5), grille: true)` |
| `\point{x}{y}{A}{above right}` | `point((x, y), "A", pos: "ne")` |
| `\draw (A) -- (B)` | `segment(A, B)` (codage : `codage: 1`) ; prolongé : `droite(A, B)` |
| `\draw[->] (A) -- (B) node {$\vec u$}` | `fleche(A, B, nom: "u")` |
| `circle`, `arc` | `cercle(O, r)`, `arc(O, r, 20deg, 160deg)` |
| `-- cycle` | `polygone(A, B, C)`, `triangle(A, B, C, noms: ("A", "B", "C"))` |
| angle droit, médiatrice, milieu | `angle-droit(S, A, B)`, `mediatrice(A, B)`, `milieu(A, B)` (calcul pur) |
| courbe `plot` | `courbe(x => …, x: (a, b))` |

Hors de farfadet-geom (3D, calques, `\clip`, décorations) : cetz brut dans le même `geo` (`typst-essentiel.md`, section 8), ou garder l'extrait. Après un redessin, comparer l'image à celle de l'extrait LaTeX.

## 8. Maintenir le convertisseur (« le paquet a changé »)

Le convertisseur lit l'index des fonctions à chaque lancement : noms, clés, types d'arguments, noms LaTeX des options. Il suit donc les paquets sans modification, sauf pour ce que l'index ne peut pas dire, écrit dans `scripts/tex2typ/regles.py` (renommages comme `\tcbtabc` → `tcbtab(align: center)`, arguments facultatifs sans nom, commandes ignorées, environnements rendus en extrait LaTeX, et `FORME_ENVIRONNEMENT` : les fonctions dont l'environnement LaTeX s'écrit `#begin`/`#end`). Quand un paquet gagne ou perd la forme environnement pour une fonction, modifier cet ensemble ; les corps à items se règlent dans `traductions.py` (`_corps_items`, `begin_end`).

Quand un paquet change :

1. `python "<skill>/scripts/regenerer.py"` : index, fiches `references/paquets/`, signatures ;
2. recompiler un document converti pour vérifier ;
3. une règle à corriger : `regles.py`.
