# farfadet-modele

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": modeles` puis `#import modeles: *`.
- Réglage : `setbfmodele` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-modele.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-modele`).

## Sommaire

- `farfadet` — Modèle de document bfcours : page A4, polices Erewhon, équations, bandeau de chapitre (niveau, thème, type de document), pied de page, somm…
- `sequence-item` — \SequenceItem{forme}{description}{commentaire} : une ligne d'une progression de séquence : forme en chevron contenant un libellé (« Séance …
- `chap-eval` — \chapEval : bandeau d'évaluation. Comme `chapitre`, avec les cases « Classe » et « Date » à droite et un contenu facultatif juste sous le b…
- `chapitre` — \chapitre : bandeau de chapitre. Étiquette de niveau, titre « type thème » sur un dégradé gris, zone libre à droite. Il enregistre aussi le…
- `pied-de-page` — Pied de page de bfcours : filet, « type thème » à gauche, « cycle établissement » à droite, numéro de page dans un disque gris. Il lit les …
- `modele` — Point d'entrée unique des modèles de document. Renvoie une fonction `document => …` à employer avec `#show:`. Le nom du modèle est la clé d…
- `choice-fonts-dys` — \choiceFontsDys{nom} (bfcours-fonts) : choisit la famille de la variante dys ; elle s'applique quand `dys: true` (clé de `farfadet`). Écrir…
- `setbfmodele` — Règle le modèle de document et ses en-têtes à partir de cet endroit : un seul setter pour tout le paquet (réglage global, réglage d'un type…

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `etablissement` | établissement, à droite du pied de page. |  | 3 : `farfadet`, `chap-eval`, `chapitre` |
| `style` | style(s) nommé(s). |  | 3 : `sequence-item`, `chap-eval`, `pied-de-page` |

## farfadet

```typ
farfadet(correction: auto, fontsize: auto, fleqn: auto, mathindent: auto, baselineskip: auto, dys: auto, niveau: auto, theme: auto, type-document: auto, cycle: auto, etablissement: auto, zone-droite: auto, titres: auto, numeros: auto, sommaire: auto, titre-sommaire: auto, colonnes-sommaire: auto, environnements: auto, style: auto, papier: "a4", marges: (left: 1cm, right: 0.5cm, top: 0.5cm, bottom: 2cm), decalage: 2.5pt * 72 / 72.27, avec-page: true, pied: true, doc, ..options)
```

Modèle de document bfcours : page A4, polices Erewhon, équations, bandeau de chapitre (niveau, thème, type de document), pied de page, sommaire facultatif et réglage des environnements.

Les clés sont toutes facultatives et toutes nommées ; les valeurs par défaut sont celles de bfcours. Le bandeau de chapitre n'est posé que si `niveau` ou `theme` est renseigné. Les clés se règlent aussi une fois pour toutes (`setbfmodele`) ou par style nommé (`style:`) ; priorité : clé locale > style nommé > réglage du type `"bfcours"` > réglage global > défaut.

Clés communes acceptées (voir en tête) : `etablissement`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `correction` | `auto` | bool | `true` : version professeur ; `false` : version élève. `--input correction=true\|false` l'emporte. Défaut : `true`. |  |
| `fontsize` | `auto` | length, auto | taille nominale du texte (option de `scrextend`). Défaut : `auto` (12pt ; 14pt en dys). |  |
| `fleqn` | `auto` | bool | `true` : équations en display alignées à gauche avec retrait (option de classe `fleqn`) ; `false` : centrées. Défaut : `true`. |  |
| `mathindent` | `auto` | length, auto | retrait des équations de `fleqn` (`\mathindent`). Défaut : `auto` (27.37pt TeX). |  |
| `baselineskip` | `auto` | length, auto | interligne (`\baselineskip`). Défaut : `auto` (14.5pt TeX, proportionnel à `fontsize`). |  |
| `dys` | `auto` | bool | variante dys de `bfcours-fonts` : police sans empattement (`police-dys`), 14 pt, interligne × 1,2, espaces élargis, texte non justifié. Défaut : `false`. |  |
| `niveau` | `auto` | str, content | niveau du bandeau. Écritures courtes : `"6e"`, `"5e"`, `"4e"`, `"3e"`, `"2nde"`, `"1ère"` (ou `"1re"`), `"Tle"` (exposant ajouté) ; tout autre texte ou contenu est affiché tel quel. |  |
| `theme` | `auto` | content, str | titre du chapitre, dans le bandeau et le pied de page. |  |
| `type-document` | `auto` | "cours" \| "exercices" \| "activite" \| "fiche" \| "evaluation" \| content | nature du document. `"evaluation"` pose le bandeau d'évaluation `chap-eval` (cases Classe et Date) ; un contenu quelconque sert de libellé libre sur un bandeau ordinaire. Les types et leurs libellés se règlent par la cl… |  |
| `cycle` | `auto` | content, str | cycle, à droite du pied de page. Défaut : « Lycée ». |  |
| `zone-droite` | `auto` | content | contenu libre à droite du bandeau (hors évaluation). |  |
| `titres` | `auto` | "bfcours" \| "sobre" \| "classique" \| "documentation" \| "rd" | jeu de titres des niveaux 1 à 4 (rendu dans le sectionnement de farfadet-didactique). `"bfcours"` : bandeaux des cours (défaut) ; `"sobre"` : numéro coloré et filet fin ; `"classique"` : titres gras d'article ; `"docume… |  |
| `numeros` | `auto` | "arabe" \| "romain" \| "lettres" \| array | style de numérotation des titres. `"arabe"` : 1, 1.1, 1.1.1 ; `"romain"` : I, II… pour les sections, puis 1., 2.… pour les sous-sections et a), b)… au niveau 3 ; `"lettres"` : A, B… puis 1., 2.… et a), b)… ; un tableau … |  |
| `sommaire` | `auto` | bool | `true` : table des matières sous le bandeau. Défaut : `false`. |  |
| `titre-sommaire` | `auto` | content | titre de la table des matières. Défaut : « Table des matières ». |  |
| `colonnes-sommaire` | `auto` | int | nombre de colonnes de la table des matières. Défaut : `2`. |  |
| `environnements` | `auto` | dictionary, none | réglages des environnements, même contenu que les arguments de `setbfenvironments` : `(tous: (…), Definition: (…))`. |  |
| `style` | `auto` | str, array | style(s) nommé(s) défini(s) par `setbfmodele(definir: …)`. |  |
| `papier` | `"a4"` | str | format de papier Typst : `"a4"` (défaut), `"a5"`, `"us-letter"`… (page : argument direct). |  |
| `marges` | `(left: 1cm, right: 0.5cm, top: 0.5cm, bottom: 2cm)` | dictionary | marges à modifier, parmi `left`, `right`, `top`, `bottom` ; les clés absentes gardent la valeur de bfcours (1 cm, 0,5 cm, 0,5 cm, 2 cm). |  |
| `decalage` | `2.5pt * 72 / 72.27` | length | décalage vertical de 2,5 pt TeX des documents bfcours (`\headheight` porté à 14,5 pt après geometry). Défaut : `2.5pt` TeX. |  |
| `avec-page` | `true` | bool | `false` : ne règle ni le format de page ni le pied de page, seulement le style du texte (aperçus encadrés, documentation). Défaut : `true`. |  |
| `pied` | `true` | bool | `false` : pas de pied de page (voir `pied-de-page()` pour le poser soi-même). Défaut : `true`. |  |
| `doc` | (positionnel) | content | le document, fourni par `#show:`. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `professeur` | `auto` | content |  | Champ d'identité pour ce document seul, comme `academie`, `annee`, `classe`, `matiere`, `logo`, `mentions` (chapitre « Personnaliser l'identité et l'en-tête »). |
| `separateur-type` | `auto` | content \| auto |  | Ce qui s'écrit entre le type et le thème dans le bandeau et le pied de ce document : `[ : ]`, `" - "`… (chapitre « Personnaliser l'identité et l'en-tête »). |
| `libelles-types` | `auto` | dictionary |  | Libellés des types de document, remplacés ou complétés : `(cours: [Leçon], tp: [TP])` ; `type-document: "tp"` s'emploie ensuite (chapitre « Personnaliser l'identité et l'en-tête »). |
| `rendu` | `auto` | str \| function |  | Rendu de l'en-tête pour ce document : `"bf"`, `"rd"`, `"sobre"`, `"encadre"` ou une fonction ; avec `skin` et `champs` (chapitre « Personnaliser l'identité et l'en-tête »). |
| `abovedisplayskip` | `12pt TeX` | length |  | Espace avant une équation. |
| `belowdisplayskip` | `12pt TeX` | length |  | Espace après une équation. |
| `police` | `auto` | array \| auto |  | Polices du texte, par ordre de préférence. `auto` : `("Erewhon", "Libertinus Serif")`. |
| `police-maths` | `auto` | array \| auto |  | Polices des formules. `auto` : `("Erewhon Math", "New Computer Modern Math")`. Sans aucune police installée, Typst utilise les polices intégrées. |

Exemple :

```typ
#show: farfadet.with(niveau: "2nde", theme: [Les vecteurs], correction: false)
#show: farfadet.with(fontsize: 11pt, fleqn: false, sommaire: true)
#show: farfadet.with(dys: true)
```

## sequence-item

```typ
sequence-item(forme, description, commentaire, style: auto, ..options)
```

\SequenceItem{forme}{description}{commentaire} : une ligne d'une progression de séquence : forme en chevron contenant un libellé (« Séance 1 »), suivie d'une boîte à deux volets (description, commentaire).

En LaTeX la commande se pose dans une `tikzpicture` à des coordonnées choisies ; ici elle est un bloc, qui s'empile. Les options de `[…]` (couleur de la forme) sont des clés nommées.

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `forme` | (positionnel) | content, str | libellé dans le chevron. |  |
| `description` | (positionnel) | content, str | volet de gauche. |  |
| `commentaire` | (positionnel) | content, str | volet de droite, plus clair. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleur` | `"myblue"` | color \| str |  | Couleur de la forme et du cadre (couleur nommée `myblue`, suit `setbfcolors`). |
| `hauteur` | `3cm` | length |  | Hauteur de la ligne. |
| `largeur-boite` | `15cm` | length |  | Largeur de la boîte. |
| `ombre` | `true` | bool |  | Ombre portée. |

Exemple :

```typ
#sequence-item([Séance 1], [Découvrir les vecteurs], [Prérequis : repère du plan])
```

## chap-eval

```typ
chap-eval(niveau: auto, theme: auto, cycle: auto, etablissement: auto, apres: auto, type: auto, style: auto, ..options)
```

\chapEval : bandeau d'évaluation. Comme `chapitre`, avec les cases « Classe » et « Date » à droite et un contenu facultatif juste sous le bandeau. Les clés de réglage sont celles de `chapitre` (type de réglage `"chapEval"`).

En LaTeX : `\chapEval[niveau]{thème}{cycle}{établissement}{contenu sous le bandeau}{type}` ; ici les positionnels sont `theme, cycle, etablissement, apres, type`.

LaTeX : `\chapEval`

Clés communes acceptées (voir en tête) : `etablissement`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `niveau` | `auto` | str, content | niveau de la classe (voir `chapitre`). |  |
| `theme` | `auto` | content, str | titre du chapitre. |  |
| `cycle` | `auto` | content, str | cycle, à droite du pied de page. |  |
| `apres` | `auto` | content | contenu placé juste sous le bandeau : consignes, barème… |  |
| `type` | `auto` | content, str | nature du document ; `"evaluation"` (défaut) donne « Évaluation ». |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `colonnes-titre` | `4` | int |  | Colonnes occupées par le titre. |

Exemple :

```typ
#chap-eval(niveau: "3e", theme: [Théorème de Thalès], type: [Contrôle n° 2])
```

## chapitre

```typ
chapitre(niveau: auto, theme: auto, cycle: auto, etablissement: auto, zone-droite: auto, type: auto, style: auto, ..options)
```

\chapitre : bandeau de chapitre. Étiquette de niveau, titre « type thème » sur un dégradé gris, zone libre à droite. Il enregistre aussi les textes du pied de page, qui les reprend à chaque page suivante.

Le bandeau est le début d'une fiche, d'un cours ou d'une activité. Le modèle `farfadet` le pose pour vous quand on lui donne `niveau` ou `theme` ; on l'écrit à la main pour changer de bandeau en cours de document, ou pour un document sans modèle. Comme en LaTeX, `theme, cycle, etablissement, zone-droite, type` peuvent aussi se donner par position, dans cet ordre.

Clés communes acceptées (voir en tête) : `etablissement`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `niveau` | `auto` | str, content | niveau de la classe. Écritures courtes : `"6e"`, `"5e"`, `"4e"`, `"3e"`, `"2nde"`, `"1ère"`, `"Tle"` (exposant ajouté) ; tout autre texte est affiché tel quel. Défaut : vide. |  |
| `theme` | `auto` | content, str | titre du chapitre, dans le bandeau et le pied de page. |  |
| `cycle` | `auto` | content, str | cycle, à droite du pied de page. |  |
| `zone-droite` | `auto` | content | contenu libre à droite du bandeau. |  |
| `type` | `auto` | content, str | nature du document, devant le thème : `"cours"` (défaut), `"exercices"`, `"activite"`, `"fiche"`, `"evaluation"` (libellé correspondant, modifiable par `libelles-types`), un type ajouté par `libelles-types`, ou un conte… |  |
| `style` | `auto` | str, array | style(s) nommé(s) défini(s) par `setbfmodele(definir: …)`. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `hauteur` | `1.5cm` | length |  | Hauteur du bandeau. |
| `colonnes-titre` | `6` | int |  | Colonnes occupées par le titre (sur 9) ; le reste va à la zone de droite. |
| `couleur-debut` | `"gray!60"` | color \| str |  | Couleur du dégradé, à gauche (couleur nommée de bfcours, suit `setbfcolors`). |
| `couleur-fin` | `"gray!10"` | color \| str |  | Couleur du dégradé, à droite. |
| `couleur-etiquette` | `"gray!60"` | color \| str |  | Fond du carré de niveau. |
| `pied` | `true` | bool |  | `false` : le bandeau ne renseigne pas le pied de page. |
| `rendu` | `"bf"` | str \| function |  | Dessin de l'en-tête : `"bf"`, `"rd"`, `"sobre"`, `"encadre"` ou une fonction (chapitre « Personnaliser l'identité et l'en-tête »). |
| `champs` | `auto` | dictionary \| auto |  | Champs affichés dans les zones `gauche`, `centre`, `droite` (chapitre « Personnaliser l'identité et l'en-tête »). |
| `separateur-type` | `auto` | content \| auto |  | Ce qui s'écrit entre le type et le thème : `[ : ]` donne « Cours : Thème » ; `auto` écrit « : » (une espace seule si le libellé finit déjà par deux-points ; `[ ]` redonne l'ancien rendu) (chapitre « Personnaliser l'iden… |
| `libelles-types` | `(:)` | dictionary |  | Libellés des types de document : `(cours: [Leçon], tp: [TP])` remplace ou ajoute des types (@sec-separateur-type). |
| `professeur` | `[]` | content |  | Champ d'identité, comme `academie`, `annee`, `classe`, `matiere`, `logo`, `mentions` (chapitre « Personnaliser l'identité et l'en-tête »). |

Exemple :

```typ
#chapitre(niveau: "2nde", theme: [Les vecteurs], cycle: [Lycée], etablissement: [Lycée du Parc])
#chapitre(niveau: "6e", [La proportionnalité], [Collège], [Marie Curie], [], [Cours])   // forme LaTeX
```

## pied-de-page

```typ
pied-de-page(disposition: auto, gauche: auto, centre: auto, droite: auto, numero: auto, style: auto, ..options)
```

Pied de page de bfcours : filet, « type thème » à gauche, « cycle établissement » à droite, numéro de page dans un disque gris. Il lit les textes posés par le dernier `chapitre` ou `chap-eval` rencontré, et ne montre rien avant le premier (sauf si `gauche`, `centre` ou `droite` sont donnés). Quand deux bandeaux sont posés sur la même page, le pied de cette page porte le second, comme celui des pages suivantes qui n'ont pas de bandeau.

Le modèle `farfadet` l'installe tout seul. On s'en sert pour une mise en page personnelle :

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `disposition` | `auto` | str, function | `"bfcours"` (défaut : disque de numéro à droite), `"simple"` (texte à gauche, numéro au centre, texte à droite : pied du skin exolombards) ou une fonction `d => contenu` qui dessine tout le pied (zone de `hauteur` de ha… |  |
| `gauche` | `auto` | content, array, function, auto | texte de gauche ; une liste de champs (`("professeur", "annee")`, séparés par `separateur`) ou une fonction `d => contenu` ; `auto` : « type thème » du dernier bandeau. |  |
| `centre` | `auto` | content, array, function, auto | texte du centre (mêmes formes) ; `auto` : rien (disposition `"bfcours"`) ou le numéro de page (`"simple"`). |  |
| `droite` | `auto` | content, array, function, auto | texte de droite (mêmes formes) ; `auto` : « cycle établissement » du dernier bandeau. |  |
| `numero` | `auto` | bool | afficher le numéro de page. Défaut : `true`. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `separateur` | `auto` | content \| auto |  | Entre les champs d'une zone donnée par une liste (`gauche: ("professeur", "annee")`) ; `auto` : point médian. |
| `separateur-type` | `auto` | content \| auto |  | Entre le type et le thème du « type thème » de gauche ; `auto` : celui du dernier bandeau, à défaut « : » selon la même règle (@sec-separateur-type). |
| `professeur` | `[]` | content |  | Champ d'identité, utilisé quand le dernier bandeau ne le renseigne pas, comme les autres champs d'identité (chapitre « Personnaliser l'identité et l'en-tête »). |
| `hauteur` | `30pt` | length |  | Hauteur de la zone du pied (`\footskip`). |
| `epaisseur-filet` | `0.3985pt` | length |  | Épaisseur du filet (`\footrulewidth`). |
| `couleur-disque` | `"gray!80!black"` | color \| str |  | Couleur du disque du numéro. |

Exemple :

```typ
#set page(footer: pied-de-page(), footer-descent: 0pt)
#set page(footer: pied-de-page(disposition: "simple", gauche: [Mon nom]), footer-descent: 0pt)
```

## modele

```typ
modele(nom, ..reglages)
```

Point d'entrée unique des modèles de document. Renvoie une fonction `document => …` à employer avec `#show:`. Le nom du modèle est la clé du choix ; un nom inconnu arrête la compilation et liste les modèles disponibles.

- `"cours"` : `farfadet` (mêmes clés : `niveau`, `theme`, `titres`, `sommaire`, `dys`…). - `"documentation"` : document de documentation (paquet `@local/bfdoc:0.2.0`) : couverture, sommaire, titres numérotés, en-têtes avec la section en cours, pied avec version et numéro de page, fond décoré. Clés : `titre`, `sous-titre`, `version`, `auteur`, `date` (`auto` : date du jour), `resume`, `sommaire` (page de sommaire, `true`), `motif` (`auto`, `"constellation"`, `"hexagones"`, `"ondes"`, `"triangles"`, `"grille"`, liste ou `none`), `repere` (repère de section dans la marge droite, `true`). Les fiches `fonction`, les exemples, les blocs `note`, `astuce`… s'importent séparément : `#import "@local/bfdoc:0.2.0": *`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | "cours" \| "documentation" | le modèle à installer. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `reglages` | `(:)` | arguments |  | Les clés du modèle choisi, toutes nommées : celles de `farfadet` pour `"cours"`, celles de la documentation pour `"documentation"` (voir plus bas). |

Exemple :

```typ
#show: modele("cours", niveau: "2nde", theme: [Les vecteurs])
#show: modele("documentation", titre: "Mon paquet", version: "1.0")
```

## choice-fonts-dys

```typ
choice-fonts-dys(nom)
```

\choiceFontsDys{nom} (bfcours-fonts) : choisit la famille de la variante dys ; elle s'applique quand `dys: true` (clé de `farfadet`). Écrire avant `#show: farfadet`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | `"Fira"` (Fira Sans et Fira Math), `"lmodern"` (Latin Modern Sans) ou `"tgheros"` (TeX Gyre Heros). |  |

Exemple :

```typ
#choice-fonts-dys("lmodern")
#show: farfadet.with(dys: true)
```

## setbfmodele

```typ
setbfmodele(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle le modèle de document et ses en-têtes à partir de cet endroit : un seul setter pour tout le paquet (réglage global, réglage d'un type, style nommé, remise à zéro).

En LaTeX, bfcours se règle une fois pour toutes au `\usepackage` : les clés du modèle sont le réglage global. Ici, `setbfmodele` s'écrit n'importe où avant ce qu'il règle. Les arguments de page de `farfadet` (`papier`, `marges`, `decalage`, `avec-page`, `pied`) font exception : Typst interdit de régler la page depuis un état, ils se passent à `farfadet` lui-même.

Identité et en-tête : les champs d'identité (`etablissement`, `cycle`, `professeur`, `academie`, `annee`, `classe`, `matiere`, `logo`, `mentions`) se règlent par `pour: "identite"` (bandeaux et pied de page à la fois) ; le dessin des bandeaux par `pour: "entete"` (`chapitre` et `chap-eval`) : clé `rendu` (`"bf"`, `"rd"`, `"sobre"`, `"encadre"` ou une fonction), `champs`, couleurs, polices, filets, logo ; le pied par `pour: "pied-de-page"`. Un document reprend la main pour lui seul en passant les mêmes clés à `modele("cours", …)` ou à `chapitre`, ou en rappelant `setbfmodele`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type à régler : `"bfcours"`, `"chapitre"`, `"chapEval"`, `"pied-de-page"`, `"SequenceItem"`, ou un groupe : `"entete"` (les deux bandeaux), `"identite"` (les deux bandeaux et le pied de page) ; ou un tableau de types et… |  |
| `reinitialiser` | `false` | bool, str | `true` : oublie les réglages global et par type (les styles nommés restent) ; avec des clés, repart des défauts puis les applique. `"tout"` : oublie aussi les styles nommés. |  |
| `definir` | `none` | str, none | nom d'un style à définir ; les clés deviennent le contenu du style, appelé ensuite par `style: "nom"`. `pour:` contrôle les clés contre un type. |  |

Clés documentées dans le guide (`farfadet-modele/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | `(:)` | arguments |  | Les clés à régler, nommées ; la clé `style` appelle un ou plusieurs styles nommés ; la clé `titres` choisit le jeu de titres. |

Exemple :

```typ
#setbfmodele(cycle: [Lycée], etablissement: [Lycée du Parc])
#setbfmodele(pour: "chapitre", hauteur: 2cm, couleur-debut: luma(230))
#setbfmodele(definir: "sobre", couleur-debut: luma(240), couleur-fin: luma(240))
#setbfmodele(titres: "sobre")
#setbfmodele(pour: "identite", etablissement: [Lycée du Parc], professeur: [M. Durand], annee: [2026-2027])
#setbfmodele(pour: "entete", rendu: "sobre", couleur-filet: rgb("#1d4e89"))
#setbfmodele(pour: "pied-de-page", droite: ("professeur", "annee"))
#setbfmodele(reinitialiser: true)
```
