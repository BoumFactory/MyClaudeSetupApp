# farfadet-maths

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": maths` puis `#import maths: *`.
- Réglage : `setbfmaths` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-maths.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-maths`).

## Sommaire

- `setbfmaths` — Règle la mise en valeur du texte, les connecteurs, les coordonnées, les intervalles et les crochets pour toute la suite du document. Les cl…
- `sisetup` — Règle l'écriture des nombres et des unités qui suivent (`num`, `qty`, `unit`), avec les clés de siunitx. Les valeurs par défaut sont frança…
- `crochetd` — Crochet droit « ] » (le `\CrochetD` de LaTeX), à taille adaptative selon le contenu : avec un argument, il se place juste après ce contenu …
- `crochetg` — Crochet gauche « [ » (le `\CrochetG` de LaTeX), à taille adaptative selon le contenu : avec un argument, sa hauteur suit celle de ce conten…
- `coordonnees` — Coordonnées d'un point ou d'un vecteur : chaque valeur sur son fond gris, séparées par un point-virgule espacé à la française (`\Coordonnee…
- `dd` — L'ensemble des nombres décimaux, noté 𝔻 comme `RR` note ℝ : à employer dans une formule (le `\D` de LaTeX, repli de nom : une lettre seule …
- `rep` — Le repère orthonormé (O ; I ; J) (le `\Rep` de LaTeX).
- `vect` — Vecteur : le nom (ou les deux points) surmonté d'une flèche qui s'étire avec lui (`\overrightarrow`).
- `intervalle` — Intervalle de nombres réels, entre crochets qui s'adaptent à la hauteur de ce qu'ils entourent (un intervalle de fractions a de grands croc…
- `affiche` — Nombre relatif entre parenthèses quand il est négatif (`\affiche[code]{nombre}`).
- `acc` — Met un mot en valeur : gras, dans la couleur d'accent du contexte (celle de l'environnement où l'on se trouve, noir ailleurs). Les formules…
- `encadrer` — Encadre un texte ou une formule : fond très pâle, filet de la même teinte en plus foncé, texte noir. Dans une formule, l'appeler sans `#` :…
- `frquote` — Texte entre guillemets français, avec les espaces insécables : « comme ceci ».
- `lien` — Lien interne vers une étiquette du document (le `\hyperref` de bfcours) : texte en gras, couleur des liens internes (`red!50!yellow`).
- `needspace` — Réserve de la place : si moins de `longueur` reste sur la page, passe à la page suivante ; sinon ne fait rien : quand la place suffit, aucu…
- `outilcours` — Ligne grise, en petit, qui nomme la méthode ou la propriété du cours à mobiliser : « ▷ Outil du cours : … ». Elle se distingue ainsi de la …
- `pascalc` — Mention « Calculatrice interdite », en gras.
- `surligner` — Surligne un texte ou une formule, comme un marqueur : fond clair, texte dans la teinte foncée.
- `alors` — Connecteur « Alors » (bleu par défaut).
- `car` — Connecteur « Car » (vert par défaut).
- `donc` — Connecteur « Donc » (violet par défaut).
- `et` — Connecteur « Et » (vert par défaut).
- `mais` — Connecteur « Mais » (rouge par défaut).
- `puisque` — Connecteur « Puisque » (violet par défaut).
- `ssi` — Connecteur « si et seulement si » (violet par défaut, taille normale).
- `si` — Connecteur « Si » : le mot, coloré, sur un fond pâle de la même teinte (rouge par défaut).
- `np` — Alias de `num` (le `\np` de numprint) : mêmes arguments, même rendu.
- `num` — Écrit un nombre à la française : virgule décimale et espace fine entre les groupes de trois chiffres.
- `qty` — Écrit une grandeur : un nombre suivi de son unité, séparés par une espace fine insécable.
- `unit` — Écrit une unité seule.

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `style` | nom d'un style de `setbfmaths(definir: …)`. |  | 17 : `coordonnees`, `intervalle`, `acc`, `encadrer`, `frquote`, `lien`, `outilcours`, `pascalc` … |
| `couleur` | couleur du connecteur. |  | 7 : `alors`, `car`, `donc`, `et`, `mais`, `puisque`, `ssi` |
| `style` | nom d'un style de `sisetup(definir: …)`. |  | 4 : `np`, `num`, `qty`, `unit` |

## setbfmaths

```typ
setbfmaths(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle la mise en valeur du texte, les connecteurs, les coordonnées, les intervalles et les crochets pour toute la suite du document. Les clés valables dépendent de la commande visée (`pour:`) ; une clé inconnue ou une valeur invalide arrête la compilation en listant les possibilités.

Priorité : clé locale > style nommé > réglage du type (`pour:`) > réglage global > défaut. Les couleurs par défaut sont des couleurs nommées de bfcours : `setbfcolors` les change.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str, array | type visé : `"acc"`, `"encadrer"`, `"surligner"`, `"Si"`, `"Alors"`, `"Donc"`, `"Et"`, `"Mais"`, `"Car"`, `"Puisque"`, `"SSI"`, `"connecteurs"` (les huit), `"Coordonnees"`, `"intervalle"`, `"Crochet"`, `"outilcours"`, `… |  |
| `reinitialiser` | `false` | bool, str | `true` : repart des défauts (réglages global et par type effacés ; les styles nommés restent) ; `"tout"` : oublie aussi les styles définis. |  |
| `definir` | `none` | none, str | nom d'un style à définir avec les clés données ; on l'appelle ensuite par `style: "nom"` (`pour:` contrôle alors les clés contre un type). |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Les clés à régler, celles de la commande visée. |

Exemple :

```typ
#setbfmaths(pour: "connecteurs", fond: 20)
#setbfmaths(pour: "Si", couleur: "orange")
#setbfmaths(pour: "encadrer", couleur: "green")
#si() $x > 0$, #alors() $sqrt(x)$ existe : #encadrer[$a^2 + b^2$].
```

## sisetup

```typ
sisetup(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle l'écriture des nombres et des unités qui suivent (`num`, `qty`, `unit`), avec les clés de siunitx. Les valeurs par défaut sont françaises : virgule décimale, espace fine tous les trois chiffres à partir de quatre chiffres. Priorité : clé locale > style > réglage du type > réglage global.

LaTeX : `\sisetup`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | `"num"`, `"qty"` ou `"unit"` ; `none` : toutes les commandes. |  |
| `reinitialiser` | `false` | bool, str | `true` : retour aux défauts (styles conservés) ; `"tout"` : oublie aussi les styles. |  |
| `definir` | `none` | none, str | nom d'un style à définir, appelé ensuite par la clé locale `style:` de `num`, `qty`, `unit`. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Les clés de `num` ; `per-mode` et `inter-unit-product` pour `qty` et `unit`. |

Exemple :

```typ
#sisetup(round-precision: 2)
#num("3.14159") et #num("2")
```

## crochetd

```typ
crochetd(..args)
```

Crochet droit « ] » (le `\CrochetD` de LaTeX), à taille adaptative selon le contenu : avec un argument, il se place juste après ce contenu et en prend la hauteur. Sans argument : crochet seul (voir `crochetg`).

- ..args (content): au plus un contenu (positionnel), dont le crochet prend la hauteur et qu'il suit ; sans contenu : crochet seul. Mêmes clés nommées que `crochetg`.

LaTeX : `\CrochetD`

Exemple :

```typ
$ crochetg(1/2) ; crochetd(3/4) $
$ crochetg() 0 ; 1 crochetd() $
```

## crochetg

```typ
crochetg(..args)
```

Crochet gauche « [ » (le `\CrochetG` de LaTeX), à taille adaptative selon le contenu : avec un argument, sa hauteur suit celle de ce contenu, écrit juste après lui, comme `\left[ … \right]`. Sans argument, c'est un crochet seul à la taille du texte courant ; `taille:` impose une autre taille (elle remplace l'ancien `CrochetGSize`).

- ..args (content): au plus un contenu (positionnel), dont le crochet prend la hauteur et qu'il précède ; sans contenu : crochet seul. Clés nommées : `taille` (crochet seul : nom LaTeX comme `"large"`, ou longueur ; `auto` : celle du contexte), `style` (style défini par `setbfmaths(definir: …)`), cotes du crochet (`trait`, `patte`, `marge`, `ecart`, `approche`, `ex` : longueur d'un « ex »).

LaTeX : `\CrochetG`

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `contenu` | (positionnel) | content |  | Au plus un contenu : le crochet prend sa hauteur et le précède (`crochetd` : le suit). Sans contenu : crochet seul. |
| `taille` | `auto` | auto \| str \| length |  | Crochet seul : un nom LaTeX (`"large"`) ou une longueur ; `auto` : celle du contexte. |

Exemple :

```typ
$ crochetg(1/2) ; crochetd(3/4) $
$ crochetg() 0 ; 1 crochetd() $
#crochetg(taille: "Large") x ; y #crochetd(taille: "Large")
```

## coordonnees

```typ
coordonnees(..args, nom: none, style: auto)
```

Coordonnées d'un point ou d'un vecteur : chaque valeur sur son fond gris, séparées par un point-virgule espacé à la française (`\Coordonnees[A]{x}{y}`). Deux valeurs dans le plan, trois dans l'espace.

- ..args (content): les coordonnées, dans l'ordre : `x`, `y` (et `z`) ; les clés nommées de la boîte : `colback`, `colframe`, `arc`, `boxsep`, `boxrule`, `left`, `right`, `top`, `bottom`, `separateur`.

LaTeX : `\Coordonnees`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | `none` | content, none | nom du point, écrit devant la parenthèse : `A(3 ; -1)`. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `valeurs` | (positionnel) | content |  | Les coordonnées dans l'ordre : deux dans le plan, trois dans l'espace. |
| `separateur` | `pvfr` | content |  | Séparateur : le point-virgule espacé à la française. |
| `colback` | `gray!15` | color \| str |  | Fond de chaque valeur. |
| `colframe` | `auto` | color \| str \| auto |  | Filet de chaque valeur (`auto` : aucun). |
| `arc` | `2 pt` | length |  | Rayon des coins. |
| `boxsep` | `1 pt` | length |  | Marge intérieure. |
| `boxrule` | `0,5 mm` | length |  | Épaisseur du filet. |

Exemple :

```typ
$ coordonnees(3, -1, nom: A) $
$ coordonnees(1, 2, 3, colback: "yellow!30", arc: #4pt) $
```

## dd

```typ
dd
```

L'ensemble des nombres décimaux, noté 𝔻 comme `RR` note ℝ : à employer dans une formule (le `\D` de LaTeX, repli de nom : une lettre seule est lue comme une lettre en mode maths). Typst fournit déjà `NN`, `ZZ`, `QQ`, `RR` et `CC` ; seul `dd` est ajouté.

Exemple :

```typ
$ NN subset ZZ subset dd subset QQ subset RR $
```

## rep

```typ
rep
```

Le repère orthonormé (O ; I ; J) (le `\Rep` de LaTeX).

LaTeX : `\Rep`

Exemple :

```typ
$ "Dans le repère" rep $
```

## vect

```typ
vect(nom, accent: math.arrow)
```

Vecteur : le nom (ou les deux points) surmonté d'une flèche qui s'étire avec lui (`\overrightarrow`).

LaTeX : `\Vecteur`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | content | ce qu'on surmonte de la flèche : `A B`, `u`… |  |
| `accent` | `math.arrow` | symbol | l'accent (`math.arrow` par défaut ; `math.harpoon`, `math.tilde`…). |  |

Exemple :

```typ
$ vect(A B) + vect(B C) = vect(A C) $
```

## intervalle

```typ
intervalle(a, b, forme: auto, style: auto, ..options)
```

Intervalle de nombres réels, entre crochets qui s'adaptent à la hauteur de ce qu'ils entourent (un intervalle de fractions a de grands crochets). Le point-virgule est espacé à la française (`\intervalle[forme]{a}{b}`).

La `forme` dit comment chaque crochet est tourné : `f` (fermé) regarde vers l'intérieur, `o` (ouvert) vers l'extérieur. Première lettre : borne de gauche ; seconde : borne de droite.

LaTeX : `\intervalle`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) | content | borne de gauche. |  |
| `b` | (positionnel) | content | borne de droite. |  |
| `forme` | `auto` | auto, str | `"ff"` : [a ; b], `"oo"` : ]a ; b[, `"fo"` : [a ; b[, `"of"` : ]a ; b]. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `separateur` | `pvfr` | content |  | Le point-virgule espacé à la française. |
| `trait` | `0,8 pt` | length |  | Épaisseur du trait des crochets. |
| `patte` | `0,30 em` | length |  | Longueur du retour horizontal. |
| `marge` | `0,10 em` | length |  | Dépassement vertical. |
| `ecart` | `0,16 em` | length |  | Blanc entre crochet et contenu. |
| `approche` | `0,06 em` | length |  | Blanc à l'extérieur du crochet. |

Exemple :

```typ
$ intervalle(0, 1) $
$ intervalle(-2, +oo, forme: "of") $
$ intervalle(1/2, 3/4, forme: "oo") $
```

## affiche

```typ
affiche(nombre, code: auto, style: auto)
```

Nombre relatif entre parenthèses quand il est négatif (`\affiche[code]{nombre}`).

`code` : `0` (défaut) : parenthèses si négatif ; `1` : toujours ; `-1` : jamais.

LaTeX : `\affiche`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nombre` | (positionnel) | int, float, str | le nombre. |  |
| `code` | `auto` | auto, int | `1`, `0` ou `-1`. |  |
| `style` | `auto` | auto, str, array | nom d'un style défini par `setbfmaths(definir: …)`. |  |

Exemple :

```typ
$ 3 times #affiche(-2) quad 3 times #affiche(2) quad 3 times #affiche(2, code: 1) $
```

## acc

```typ
acc(corps, couleur: auto, graisse: auto, formules-regulieres: auto, style: auto)
```

Met un mot en valeur : gras, dans la couleur d'accent du contexte (celle de l'environnement où l'on se trouve, noir ailleurs). Les formules gardent leur graisse normale.

LaTeX : `\acc`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte à mettre en valeur. |  |
| `couleur` | `auto` | auto, color, str | `auto` : couleur d'accent courante ; sinon une couleur Typst ou une expression xcolor (`"thm"`, `"red!50!black"`). |  |
| `graisse` | `auto` | auto, str, int | graisse du texte (`"bold"` par défaut). |  |
| `formules-regulieres` | `auto` | auto, bool | `true` (défaut) : les formules du texte gardent leur graisse normale. |  |

Exemple :

```typ
Une fonction est *affine* si elle s'écrit #acc[$a x + b$].
Dans un #acc(couleur: "red")[texte rouge], ou #acc(couleur: "thm")[couleur de la palette].
```

## encadrer

```typ
encadrer(corps, couleur: auto, style: auto, ..options)
```

Encadre un texte ou une formule : fond très pâle, filet de la même teinte en plus foncé, texte noir. Dans une formule, l'appeler sans `#` : `$ f(x) = encadrer(1/x) $` garde le style de la formule (une fraction reste grande en maths affichées), comme le `\mathpalette` de LaTeX ; `#encadrer($1/x$)` composerait la fraction en petit.

LaTeX : `\encadrer`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le contenu encadré. |  |
| `couleur` | `auto` | auto, color, str | couleur de la boîte (`"blue"` par défaut) : couleur Typst ou expression xcolor. |  |

Exemple :

```typ
À retenir : #encadrer[$a^2 + b^2 = c^2$]
#encadrer(couleur: "green", arc: 0pt)[coins droits] #encadrer(fond: 20, boxrule: 1pt)[fond plus soutenu]
$ f(x) = encadrer(1/x) $
```

## frquote

```typ
frquote(corps, ouvrant: auto, fermant: auto, espace: auto, style: auto)
```

Texte entre guillemets français, avec les espaces insécables : « comme ceci ».

LaTeX : `\frquote`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte cité. |  |
| `ouvrant` | `auto` | auto, content | guillemet ouvrant (`«`). |  |
| `fermant` | `auto` | auto, content | guillemet fermant (`»`). |  |
| `espace` | `auto` | auto, content | espace entre guillemet et texte (insécable par défaut). |  |

Exemple :

```typ
On dit qu'une fonction est #frquote[croissante].
```

## lien

```typ
lien(ancre, corps, couleur: auto, graisse: auto, style: auto)
```

Lien interne vers une étiquette du document (le `\hyperref` de bfcours) : texte en gras, couleur des liens internes (`red!50!yellow`).

LaTeX : `\lien`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `ancre` | (positionnel) | str, label | nom de l'étiquette visée (`"def-aire"` pour `<def-aire>`). |  |
| `corps` | (positionnel) | content | le texte du lien. |  |
| `couleur` | `auto` | auto, color, str | couleur du lien (`auto` : celle des liens internes). |  |
| `graisse` | `auto` | auto, str, int | graisse (`"bold"`). |  |

Exemple :

```typ
Voir #lien("def-aire")[la définition de l'aire].
#lien("def-aire", couleur: "blue")[Autre couleur]
#[Aire d'un rectangle.] <def-aire>
```

## needspace

```typ
needspace(longueur, conteneur: false)
```

Réserve de la place : si moins de `longueur` reste sur la page, passe à la page suivante ; sinon ne fait rien : quand la place suffit, aucun espace n'est ajouté ni retiré, l'écart avec l'élément suivant est identique à celui d'un document sans `needspace`. Sert à ne pas laisser un titre seul en bas de page. Une seule forme (le `\Needspace*` de LaTeX). À écrire au niveau de la page ; dans un `block`, un `box` ou des colonnes (où un saut de page est interdit), ajouter `conteneur: true`.

LaTeX : `\Needspace*`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `longueur` | (positionnel) | length | hauteur à réserver. |  |
| `conteneur` | `false` | bool | `true` dans un conteneur : bloc insécable de la hauteur demandée plutôt qu'un saut de page. |  |

Exemple :

```typ
#needspace(6em)
```

## outilcours

```typ
outilcours(corps, etiquette: auto, couleur: auto, taille: auto, symbole: auto, italique: auto, espace-sous: auto, style: auto)
```

Ligne grise, en petit, qui nomme la méthode ou la propriété du cours à mobiliser : « ▷ Outil du cours : … ». Elle se distingue ainsi de la rédaction attendue, composée en noir à la suite.

LaTeX : `\outilcours`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte de l'outil. |  |
| `etiquette` | `auto` | auto, content | libellé en italique (`Outil du cours`). |  |
| `couleur` | `auto` | auto, color, str | couleur de la ligne (`"gray"`). |  |
| `taille` | `auto` | auto, str, length | taille du texte : nom LaTeX (`"small"`) ou longueur. |  |
| `symbole` | `auto` | auto, content | symbole de tête (▷). |  |
| `italique` | `auto` | auto, bool | étiquette en italique. |  |
| `espace-sous` | `auto` | auto, length | espace sous la ligne (`\smallskip`, 3 pt). |  |

Exemple :

```typ
#outilcours[Méthode « lire une probabilité dans un tableau ».]
#outilcours(etiquette: "Rappel")[la formule du contraire.]
```

## pascalc

```typ
pascalc(libelle: auto, graisse: auto, style: auto)
```

Mention « Calculatrice interdite », en gras.

LaTeX : `\pascalc`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `libelle` | `auto` | auto, content | le texte affiché. |  |
| `graisse` | `auto` | auto, str, int | graisse (`"bold"`). |  |

Exemple :

```typ
#pascalc()
#pascalc(libelle: "Sans calculatrice")
```

## surligner

```typ
surligner(corps, couleur: auto, style: auto, ..options)
```

Surligne un texte ou une formule, comme un marqueur : fond clair, texte dans la teinte foncée.

LaTeX : `\surligner`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le contenu surligné. |  |
| `couleur` | `auto` | auto, color, str | couleur du marqueur (`"blue"` par défaut). |  |

Exemple :

```typ
Le résultat est #surligner(couleur: "red")[faux] si l'on oublie le signe.
```

## alors

```typ
alors(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Alors » (bleu par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`alors`). |  |

Exemple :

```typ
#si() $x > 0$, #alors() $sqrt(x)$ existe.
```

## car

```typ
car(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Car » (vert par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`car`). |  |

Exemple :

```typ
$x = 2$ #car() $2 x = 4$.
```

## donc

```typ
donc(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Donc » (violet par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`donc`). |  |

Exemple :

```typ
$A B C$ est rectangle en $A$, #donc() $B C^2 = A B^2 + A C^2$.
```

## et

```typ
et(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Et » (vert par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`et`). |  |

Exemple :

```typ
$x > 0$ #et() $x < 5$.
```

## mais

```typ
mais(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Mais » (rouge par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`mais`). |  |

Exemple :

```typ
Il est positif, #mais() pas nul.
```

## puisque

```typ
puisque(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Puisque » (violet par défaut).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`puisque`). |  |

Exemple :

```typ
#puisque() $x = 2$, $x^2 = 4$.
```

## ssi

```typ
ssi(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « si et seulement si » (violet par défaut, taille normale).

Clés communes acceptées (voir en tête) : `couleur`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | `auto` | auto, content | le mot affiché (`si et seulement si`). |  |

Exemple :

```typ
$a b = 0$ #ssi() $a = 0$ ou $b = 0$.
```

## si

```typ
si(couleur: auto, mot: auto, style: auto, ..options)
```

Connecteur « Si » : le mot, coloré, sur un fond pâle de la même teinte (rouge par défaut).

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | auto, color, str | couleur du connecteur : couleur Typst ou expression xcolor (`"red"`). |  |
| `mot` | `auto` | auto, content | le mot affiché (`si`). |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `fontupper` | `"large"` | str \| length |  | Taille du mot (`"normalsize"` pour `ssi`). |
| `espace-apres` | `true` | bool |  | Espace après le mot. |

Exemple :

```typ
#si() $x > 0$, #alors() $sqrt(x)$ existe.
#si(couleur: "orange") ou #si(mot: "Supposons que")
```

## np

```typ
np(valeur, style: auto, ..options)
```

Alias de `num` (le `\np` de numprint) : mêmes arguments, même rendu.

LaTeX : `\np`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | str, int, float | le nombre. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..options` | `(:)` | any |  | Les clés de `num`. |

Exemple :

```typ
#np("1234567.5")
```

## num

```typ
num(valeur, style: auto, ..options)
```

Écrit un nombre à la française : virgule décimale et espace fine entre les groupes de trois chiffres.

La valeur se passe de préférence en chaîne (`"1234.5"`), pour que Typst ne l'arrondisse pas avant zero. Les clés locales (celles de siunitx) l'emportent sur `sisetup`.

LaTeX : `\num`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | str, int, float | le nombre. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `output-decimal-marker` | `","` | content |  | Séparateur décimal. |
| `group-separator` | `sym.space.thin` | content \| none |  | Séparateur de groupes ; `none` : pas de groupes. |
| `group-minimum-digits` | `4` | int |  | Nombre minimal de chiffres pour grouper (siunitx : 5). |
| `group-digits` | `"integer"` | str | `integer`, `none` | Où grouper. |
| `round-mode` | `"none"` | str | `none`, `places`, `figures` | Mode d'arrondi. |
| `round-precision` | `none` | none \| int |  | Précision de l'arrondi. |
| `round-pad` | `true` | bool |  | Complète par des zéros jusqu'à la précision. |
| `exponent-mode` | `"input"` | str | `input`, `scientific`, `engineering` | Notation de l'exposant. |
| `exponent-product` | `sym.times` | content |  | Signe devant la puissance de 10. |
| `print-unity-mantissa` | `true` | bool |  | Écrit la mantisse 1 (`1 × 10³`). |
| `print-zero-exponent` | `true` | bool |  | Écrit un exposant nul. |
| `retain-explicit-plus` | `false` | bool |  | Garde un « + » saisi. |
| `uncertainty-mode` | `"separate"` | str | `separate`, `compact`, `compact-marker` | Écriture de l'incertitude. |
| `zero` | `(:)` | dictionary |  | Échappatoire : clés brutes de `zero`, passées telles quelles. |

Exemple :

```typ
#num("1234567.891") ; #num("0.000125", exponent-mode: "scientific") ; #num(12.5, round-precision: 2)
```

## qty

```typ
qty(valeur, unite, style: auto, ..options)
```

Écrit une grandeur : un nombre suivi de son unité, séparés par une espace fine insécable.

L'unité se note comme en texte : `"m/s^2"`, `"kg m"`, `"mus"` (µs).

LaTeX : `\qty`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | str, int, float | la valeur. |  |
| `unite` | (positionnel) | str | l'unité. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `per-mode` | `"power"` | str | `power`, `fraction`, `symbol` | Écriture des « par ». |
| `inter-unit-product` | `sym.space.thin` | content |  | Séparateur entre unités. |
| `..options` | `(:)` | any |  | Toutes les clés de `num`. |

Exemple :

```typ
#qty("9.81", "m/s^2") ; #qty("20", "°C") ; #qty(1234.5, "kg", round-precision: 0)
```

## unit

```typ
unit(unite, style: auto, ..options)
```

Écrit une unité seule.

LaTeX : `\unit`

Clés communes acceptées (voir en tête) : `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `unite` | (positionnel) | str | l'unité, par exemple `"m/s^2"`. |  |

Clés documentées dans le guide (`farfadet-maths/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `per-mode` | `"power"` | str |  | Voir `qty`. |
| `inter-unit-product` | `sym.space.thin` | content |  | Séparateur entre unités. |

Exemple :

```typ
l'unité #unit("kg m/s^2") ; #unit("m/s^2", per-mode: "fraction")
```
