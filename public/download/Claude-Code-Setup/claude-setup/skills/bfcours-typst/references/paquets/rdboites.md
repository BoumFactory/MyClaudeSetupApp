# rdboites

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": rd-boites` puis `#import rd-boites: *`.
- Réglage : `setrdboites` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/rdboites.pdf` du dépôt (sources : `docs/guide.typ` du paquet `rdboites`).

## Sommaire

- `cles-rd` — Dictionnaire des clés d'une boîte et de leurs valeurs par défaut (sans `context`) : sert à découvrir ce qu'on peut régler. Sans `pour`, ce …
- `setrdboites` — Règle les boîtes pour la suite du document : réglage global, réglage d'une ou de plusieurs boîtes, définition d'un style nommé, remise à zé…
- `rd.icone-alerte` — Triangle d'avertissement (point d'exclamation dans un triangle orange), dessiné en Typst : aucune image externe. Remplace `misc/warning` de…
- `rd.ombre-floue` — Ombre floue, à poser DERRIÈRE une boîte de dimensions `largeur` × `hauteur` : dix rectangles de plus en plus opaques vers le centre, décalé…
- `rd.reinitialiser-compteur` — Remet à zéro le ou les compteurs des boîtes nommées. Noms utiles : `"exemplerealisation"`, `"vf"`, `"scratchblock"`, `"scratchfig"`, `"scra…
- `rd.alignbox` — Boîte invisible qui centre son contenu horizontalement et verticalement. Sert à aligner des cellules dans une grille ou à neutraliser des m…
- `rd.attention` — Boîte d'alerte : large bande rouge à gauche portant un triangle d'avertissement, fond rose très pâle. Pour avertir d'un piège ou d'un dange…
- `rd.blankbox` — Boîte vide en ligne : même chose que `tcalignbox`, sans cadre ni fond.
- `rd.boiteprog` — Listing de programme ou pseudo-code sobre : fond gris très clair, filet noir de 2 pt à gauche, texte sans empattement réduit.
- `rd.casio` — Mode d'emploi de calculatrice : fond vert pâle, cadre vert, large bande à gauche portant « Calculatrice » en vertical.
- `rd.centragebox` — Comme `alignbox`, mais avec l'espace vertical habituel autour de la boîte (les sauts avant et après sont conservés).
- `rd.domino` — Domino à deux moitiés égales : trait de séparation central, ombre floue, contenu centré. Pour des jeux d'association (question et réponse, …
- `rd.encadre` — Encadré gris générique, la boîte la plus neutre du lot : fond gris clair, cadre fin.
- `rd.encadregrille` — Encadré à fond quadrillé pointillé, au pas de 7,5 mm : espace de calcul, zone pour tracer une figure à main levée, réponse de l'élève sur q…
- `rd.encadreOB` — Encadré « flottant » sans cadre mais avec une ombre floue : fond gris clair. Pour une note secondaire ou un aparté qui doit se détacher de …
- `rd.entete` — Bannière dégradée : filets haut et bas dégradés du noir au blanc, fond dégradé gris. Pour un titre de page ou un bandeau d'ouverture de sec…
- `rd.etiquette` — Étiquette ou carte de largeur fixe : cadre noir arrondi, titre blanc sur un bandeau noir, fond gris clair. Pour des cartes de vocabulaire o…
- `rd.exem` — Exemple compact : petit titre italique « ▸ Exemple » au-dessus d'une boîte grise à angles vifs. Plus discret que `exemple`, pour un exemple…
- `rd.exemplerealisation` — Exemple de réalisation numéroté : bandeau bleu portant un badge « 001 » et le titre, corps en deux colonnes (texte à gauche, figure ou répo…
- `rd.ficheno` — Fiche numérotée : boîte de 7 cm, bandeau « Fiche n° X ».
- `rd.figbox` — Conteneur de figure avec titre : sans cadre, titre en haut à gauche, contenu centré.
- `rd.formula` — Formule mise en avant, avec onglet vertical « Formule » : fond teinté, bande sombre à gauche. Version bloc ; `myformule` est la version en …
- `rd.miniexemple` — Petit encart à coins en crochets : fond gris, deux crochets dessinés au milieu des bords (en haut à gauche et en bas à droite), contenu cen…
- `rd.mydoc` — Encadré gris titré, façon « document » : bandeau gris foncé, fond gris clair. Pour un extrait de programme, une fiche, un encart neutre. Le…
- `rd.myformule` — Formule mise en avant, EN LIGNE : même aspect que `formula`, à la taille du contenu, dans le fil du texte.
- `rd.rappelbox` — Rappel en ligne : comme `myformule`, avec l'onglet « Rappel ». Pour rappeler une propriété déjà vue.
- `rd.regularcell` — Une cellule de grille bordée : fond blanc, filet noir, contenu centré. La grille complète, avec hauteurs égales, est `regulartcbitemize`.
- `rd.regulartcbitemize` — Grille de cellules bordées, de hauteurs égales par rangée. Le premier argument est le nombre de colonnes (`raster columns`) ; le corps est …
- `rd.schemamainlevee` — Zone « Schéma à main levée » : invite l'élève à tracer un croquis. Le style nommé `schemamainleveetyle` (vide par défaut) est appliqué d'of…
- `rd.scratchuse` — Encadré coloré à bandeau de titre : magenta de Scratch par défaut, fond de la même teinte à 10 %. Pour une consigne ou une explication liée…
- `rd.tcalignbox` — Version EN LIGNE de `alignbox` : une boîte sans cadre qui centre son contenu.
- `rd.tcencadre` — Encadré gris EN LIGNE : un mot ou une courte expression dans un cadre arrondi gris clair.
- `rd.tcwhite` — Boîte blanche semi-transparente EN LIGNE : fond blanc à 70 %, coins arrondis, sans cadre. Pour poser du texte lisible par-dessus une image …
- `rd.zone` — Zone thématique à titre en ruban : cadre arrondi bleu, titre blanc dans un bandeau plein, contenu centré. Pour « À retenir », un objectif d…
- `rd.acocher` — Proposition à cocher : mince colonne bleutée à gauche, qui tient lieu de case, texte centré à droite. En version professeur, une propositio…
- `rd.boxpointlignesrep` — Trace les liaisons d'une activité « à relier » : un segment rouge entre le point de gauche et le point de droite de chaque paire. Les numér…
- `rd.casesvf` — Les deux cases « Vrai » et « Faux » empilées. Avec `reponse`, la bonne case est cochée en version professeur.
- `rd.cinema` — Cadre « pellicule de film » : deux bandes noires perforées de blanc, en haut et en bas, le contenu entre les deux. Pour le storytelling, de…
- `rd.coinpli` — Note à coin plié : fond gris clair, coin inférieur droit « replié », contenu centré. Pour une astuce, un mémo, un effet post-it.
- `rd.corrdembox` — Correction de démonstration en rouge : texte rouge en gras, titre blanc centré sur un bandeau rouge, fond gris clair. Surcouche « correctio…
- `rd.cours` — Bloc de cours haut de gamme : bandeau de titre dégradé du noir au gris, fond gris clair avec un léger voile en biais dans le coin inférieur…
- `rd.dottedbox` — Boîte de base des éléments à relier : bloc sans cadre à angles vifs, fond uni, numéroté par un compteur automatique (remis à zéro par `rd.r…
- `rd.dottedleftbox` — Élément de GAUCHE d'une activité « à relier » : fond gris clair, texte aligné à droite, puis une petite case blanche portant le point d'anc…
- `rd.dottedrightbox` — Élément de DROITE d'une activité « à relier » : un point d'ancrage dans une case blanche, puis le texte sur fond gris clair.
- `rd.ernum` — Badge numéroté à trois chiffres : « 012 » en gras sans empattement. Sert à numéroter des éléments (c'est le numéro de `exemplerealisation`).
- `rd.exemple` — Bloc d'exemples à décor en crochet : pastille grise « Exemple(s) » en haut à gauche, filets gris dessinés sous la pastille, à sa droite et …
- `rd.exemplereduit` — Exemple réduit, pour un encart étroit ou en marge : comme `exemple`, avec une pastille décalée vers l'extérieur. Se règle par `width` (8 cm…
- `rd.helpblock` — Bloc d'aide, coup de pouce : cadre turquoise, large bande à gauche portant « Aide » en vertical, partie gauche pour une illustration ou un …
- `rd.jourleague` — Carte « journée de championnat » : 5 cm sur 1,5 cm, titre centré sur un bandeau gris, puis les lignes équipe, score, score, équipe. Cas d'u…
- `rd.leftpoint` — Élément de GAUCHE d'une activité « à relier » : texte aligné à droite, point d'ancrage dans la marge droite. Variante sans fond des `dotted…
- `rd.listecocher` — Rangée horizontale de cases à cocher : une case et son libellé par élément, en colonnes égales. En version professeur, la ou les bonnes rép…
- `rd.ltitlebox` — Boîte à titre vertical sur le bord gauche : bande sombre portant le titre écrit de bas en haut, contenu à droite sur fond gris. Pour des en…
- `rd.mylink` — Bouton « Aide en ligne » EN LIGNE : bande orange foncé portant « Aide en ligne » en blanc, puis le texte (souvent un lien) sur fond orange …
- `rd.mytcbitembox` — Un item numéroté isolé : numéro automatique à gauche, texte justifié sur fond gris clair. Le compteur est remis à zéro par `rd.reinitialise…
- `rd.mytcbitemize` — Items numérotés disposés en grille : chaque item porte son numéro « 1) » à gauche, texte justifié sur fond gris clair à droite. Pour des qu…
- `rd.opbox` — Boîte pour poser des opérations : les opérations en colonnes centrées, puis une zone grise où l'élève effectue ses calculs. En version prof…
- `rd.parchemin` — Parchemin : papier déchiré à fond dégradé, plus sombre sur les bords, qui tient lieu de texture. Pour une narration, l'histoire des maths, …
- `rd.partieDNB` — Label « ■ Partie X » EN LIGNE : badge gris clair en gras avec une légère ombre, pour marquer les parties d'un sujet de brevet.
- `rd.progbox` — Boîte de programme ou d'algorithme colorée et titrée : cyan, coins arrondis, ombre floue, dégradé intérieur, titre centré en gras. Version …
- `rd.rightpoint` — Élément de DROITE d'une activité « à relier » : point d'ancrage dans la marge gauche, texte aligné à gauche.
- `rd.sans-coin` — Cadre dont un coin n'est pas dessiné : le trait s'interrompt à l'approche du coin, pour y raccorder un onglet, un ruban ou une autre boîte.
- `rd.scratchblock` — Bloc de programme Scratch numéroté EN LIGNE : bandeau gris « Programme N », contenu sur fond blanc. Le numéro s'incrémente à chaque bloc ; …
- `rd.scratchblockenv` — Bloc de programme Scratch numéroté, version BLOC pleine largeur.
- `rd.scratchcapture` — Capture d'écran numérotée « Image N » : cadre orange, bandeau orange pâle centré, fond blanc. Pour montrer le résultat visuel d'un programm…
- `rd.scratchfig` — Figure numérotée EN LIGNE : bandeau beige « Figure N », contenu centré. Le compteur est partagé avec `scratchfigbox`.
- `rd.scratchfigbox` — Figure numérotée, version BLOC ; mêmes numéros que `scratchfig`.
- `rd.tccoinpli` — Note à coin plié EN LIGNE : la version de `coinpli` à la taille du contenu.
- `rd.thermobox` — Thermomètre graphique : tube bleu de 1,5 cm sur 3 cm avec un niveau de liquide. Pour des problèmes de température, des jauges, des niveaux.
- `rd.tornpage` — Feuille de papier déchirée : fond papier, contour irrégulier, ombre portée. Pour une note manuscrite, un extrait « arraché », un aparté déc…
- `rd.vf` — Item vrai ou faux numéroté : énoncé à gauche, colonne grise à droite avec deux cases « Vrai » et « Faux » (`casesvf`), numéro sur fond noir…
- `rd.designbox` — Encart « design » sophistiqué, inspiré d'InDesign : cadre arrondi, bandeau de titre sombre à droite dont le bord se creuse en biseau (effet…
- `rd.ggbentrainer` — Bloc « S'entraîner en autonomie » : un cadre bleu à angle supérieur gauche vif, un onglet « S'entraîner / en autonomie » en haut à gauche, …
- `rd.ggbqr` — Encart GeoGebra : capture d'écran et QR code vers une ressource. Le titre, en bas, est le lien lui-même. La boîte épouse la taille de son c…
- `rd.ggbqrenv` — Encart GeoGebra pleine largeur : comme `ggbqr`, mais la boîte occupe la largeur disponible, capture et QR code centrés chacun dans une colo…
- `rd.icone-tablette` — Dessin d'une tablette : cadre gris, écran bleu, bouton.
- `rd.methode` — Bloc « méthode » : un onglet sombre à gauche portant le titre, un ruban dégradé du noir au gris qui court en haut, et en bas un filet qui s…
- `rd.tache` — Tâche complexe, au format des problèmes ouverts : fond arrondi vert pâle sans cadre, avec ombre floue, titre en gras en haut, et un ruban o…
- `rd.resetScratchCounters` — Remet à zéro les trois compteurs Scratch (`scratchblock`, `scratchfig`, `scratchcapture`) : pour que la numérotation recommence à 1.

## cles-rd

```typ
cles-rd(pour: none)
```

Dictionnaire des clés d'une boîte et de leurs valeurs par défaut (sans `context`) : sert à découvrir ce qu'on peut régler. Sans `pour`, ce sont les clés communes à toutes les boîtes.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str | nom de la boîte (`"zone"`, `"cours"`…). |  |

Exemple :

```typ
#cles-rd(pour: "zone")
```

## setrdboites

```typ
setrdboites(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les boîtes pour la suite du document : réglage global, réglage d'une ou de plusieurs boîtes, définition d'un style nommé, remise à zéro. Un seul setter, de signature commune à tous les paquets bfcours.

| Appel | Effet | |---|---| | `setrdboites(colframe: red)` | réglage global : toutes les boîtes qui ont la clé | | `setrdboites(pour: "zone", arc: 0pt)` | réglage d'une boîte (ou d'un tableau de boîtes) | | `setrdboites(definir: "sobre", arc: 0pt)` | définit le style nommé « sobre », appelé par `style: "sobre"` | | `setrdboites(reinitialiser: true)` | oublie les réglages global et par boîte (styles gardés) | | `setrdboites(reinitialiser: "tout")` | idem, et ramène les styles aux cinq styles prédéfinis |

Avec des clés, `reinitialiser` repart d'abord des défauts puis applique les clés. La priorité est : clé locale, puis style nommé, puis réglage de la boîte, puis réglage global, puis défaut.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | none, str, array | nom de la boîte à régler (`"zone"`, `"cours"`…) ou tableau de noms ; `none` : réglage global. Avec `definir`, réserve le style à une boîte (contrôle des clés). |  |
| `reinitialiser` | `false` | bool, str | `true` repart des défauts (styles gardés) ; `"tout"` ramène aussi les styles aux styles prédéfinis. |  |
| `definir` | `none` | none, str | nom du style à définir ; les clés deviennent le contenu du style. |  |

Clés documentées dans le guide (`rdboites/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | (positionnel) | arguments |  | Les clés à régler : `colframe: …`, `arc: …`, `style: "mon-style"`… Voir `cles-rd()`. |

Exemple :

```typ
#setrdboites(police-sans: "Latin Modern Sans", before-skip: 1em)
#setrdboites(pour: "zone", colframe: rgb("#2a9d8f"))
#setrdboites(pour: ("zone", "cours"), arc: 0pt)
#setrdboites(definir: "discret", colframe: gray, colback: white)
```

## rd.icone-alerte

```typ
rd.icone-alerte(taille: 8mm, couleur: rgb("#FF8000"), contour: rgb("#5A2600"))
```

Triangle d'avertissement (point d'exclamation dans un triangle orange), dessiné en Typst : aucune image externe. Remplace `misc/warning` de la boîte `attention`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `taille` | `8mm` | length | largeur de l'icône. |  |
| `couleur` | `rgb("#FF8000")` | color | couleur de remplissage. |  |
| `contour` | `rgb("#5A2600")` | color | couleur du contour et du point d'exclamation. |  |

Exemple :

```typ
#rd.icone-alerte(taille: 10mm)
```

## rd.ombre-floue

```typ
rd.ombre-floue(largeur, hauteur, decalage: 2.5pt, flou: 1.4pt, couleur: gris, opacite: 50%, rayon: 1mm)
```

Ombre floue, à poser DERRIÈRE une boîte de dimensions `largeur` × `hauteur` : dix rectangles de plus en plus opaques vers le centre, décalés de `decalage`. C'est l'équivalent de `drop fuzzy shadow` et `fuzzy shadow` de tcolorbox. Le résultat n'occupe aucune place (tout est en `place`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `largeur` | (positionnel) | length | largeur de la boîte ombrée. |  |
| `hauteur` | (positionnel) | length | hauteur de la boîte ombrée. |  |
| `decalage` | `2.5pt` | length | décalage de l'ombre vers la droite et vers le bas. |  |
| `flou` | `1.4pt` | length | demi-épaisseur de la zone floue. |  |
| `couleur` | `gris` | color | couleur de l'ombre. |  |
| `opacite` | `50%` | ratio | opacité au centre de la zone floue. |  |
| `rayon` | `1mm` | length | arrondi des coins de la boîte ombrée. |  |

Exemple :

```typ
#box(width: 4cm, height: 1.2cm, {
  rd.ombre-floue(4cm, 1.2cm)
  rect(width: 4cm, height: 1.2cm, fill: white, stroke: 0.5pt)
})
```

## rd.reinitialiser-compteur

```typ
rd.reinitialiser-compteur(..noms)
```

Remet à zéro le ou les compteurs des boîtes nommées. Noms utiles : `"exemplerealisation"`, `"vf"`, `"scratchblock"`, `"scratchfig"`, `"scratchcapture"`, `"ficheno"`, `"gauche"`, `"droite"` (points à relier).

Exemple :

```typ
#rd.reinitialiser-compteur("vf")
```

## rd.alignbox

```typ
rd.alignbox(corps, ..cles)
```

Boîte invisible qui centre son contenu horizontalement et verticalement. Sert à aligner des cellules dans une grille ou à neutraliser des marges.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.alignbox(width: 4cm, height: 1.2cm)[Centré]
```

## rd.attention

```typ
rd.attention(corps, ..cles)
```

Boîte d'alerte : large bande rouge à gauche portant un triangle d'avertissement, fond rose très pâle. Pour avertir d'un piège ou d'un danger.

L'icône est dessinée en Typst (`rd.icone-alerte`), pas une image. `leftrule` règle la largeur de la bande.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le message. |  |

Exemple :

```typ
#rd.attention[*Attention !* On ne peut pas diviser par zéro.]
```

## rd.blankbox

```typ
rd.blankbox(corps, ..cles)
```

Boîte vide en ligne : même chose que `tcalignbox`, sans cadre ni fond.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
avant #rd.blankbox[vide stylé] après
```

## rd.boiteprog

```typ
rd.boiteprog(corps, ..cles)
```

Listing de programme ou pseudo-code sobre : fond gris très clair, filet noir de 2 pt à gauche, texte sans empattement réduit.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le code ou l'algorithme. |  |

Exemple :

```typ
#rd.boiteprog[Tant que le reste est non nul, on continue les divisions successives.]
```

## rd.casio

```typ
rd.casio(corps, ..cles)
```

Mode d'emploi de calculatrice : fond vert pâle, cadre vert, large bande à gauche portant « Calculatrice » en vertical.

La boîte est au moins aussi haute que son étiquette : le mot ne déborde jamais, même pour un contenu d'une ligne.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.casio[Menu RUN-MAT, puis taper `2 + 3 EXE` affiche `5`.]
```

## rd.centragebox

```typ
rd.centragebox(corps, ..cles)
```

Comme `alignbox`, mais avec l'espace vertical habituel autour de la boîte (les sauts avant et après sont conservés).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.centragebox(width: 5cm)[Contenu centré dans sa boîte.]
```

## rd.domino

```typ
rd.domino(gauche, droite, ..cles)
```

Domino à deux moitiés égales : trait de séparation central, ombre floue, contenu centré. Pour des jeux d'association (question et réponse, mot et traduction) et des cartes à découper.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `gauche` | (positionnel) | content | moitié de gauche. |  |
| `droite` | (positionnel) | content | moitié de droite. |  |

Exemple :

```typ
#rd.domino[$7 times 8$][$56$]
```

## rd.encadre

```typ
rd.encadre(corps, ..cles)
```

Encadré gris générique, la boîte la plus neutre du lot : fond gris clair, cadre fin.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.encadre[Résultat : $x = 5$.]
```

## rd.encadregrille

```typ
rd.encadregrille(corps, ..cles)
```

Encadré à fond quadrillé pointillé, au pas de 7,5 mm : espace de calcul, zone pour tracer une figure à main levée, réponse de l'élève sur quadrillage.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu (souvent vide). |  |

Exemple :

```typ
#rd.encadregrille(height: 2.5cm)[]
```

## rd.encadreOB

```typ
rd.encadreOB(corps, ..cles)
```

Encadré « flottant » sans cadre mais avec une ombre floue : fond gris clair. Pour une note secondaire ou un aparté qui doit se détacher de la page. Le style nommé `encadreOB` (vide par défaut) est appliqué d'office.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.encadreOB[Un encadré simple avec une ombre douce.]
```

## rd.entete

```typ
rd.entete(corps, ..cles)
```

Bannière dégradée : filets haut et bas dégradés du noir au blanc, fond dégradé gris. Pour un titre de page ou un bandeau d'ouverture de section. Le texte est en gras et en grand, dans la police de titre du paquet (clé globale `police-titre`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le titre. |  |

Exemple :

```typ
#rd.entete[Chapitre 3 — Le théorème de Pythagore]
```

## rd.etiquette

```typ
rd.etiquette(titre, corps, ..cles)
```

Étiquette ou carte de largeur fixe : cadre noir arrondi, titre blanc sur un bandeau noir, fond gris clair. Pour des cartes de vocabulaire ou des étiquettes à découper.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre du bandeau. |  |
| `corps` | (positionnel) | content | contenu. |  |

Clés documentées dans le guide (`farfadet-geom/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `p` | (positionnel) | array |  | Coordonnées `(x, y)`. |
| `pos` | `auto` | auto \| str \| angle | `auto`, `n`, `s`, `e`, `o`, `ne`, `no`, `se`, `so` | Côté du point où se place le texte ; un angle est accepté. |
| `couleur` | `auto` | auto \| str \| color |  | Couleur du texte. |
| `taille` | `auto` | auto \| length |  | Taille du texte ; `auto` suit `taille-texte`. |

Exemple :

```typ
#rd.etiquette[Vocabulaire][Hypoténuse : le plus grand côté d'un triangle rectangle.]
```

## rd.exem

```typ
rd.exem(corps, ..cles)
```

Exemple compact : petit titre italique « ▸ Exemple » au-dessus d'une boîte grise à angles vifs. Plus discret que `exemple`, pour un exemple court dans le fil du cours.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.exem[$(-3)^2 = 9$ tandis que $-3^2 = -9$.]
```

## rd.exemplerealisation

```typ
rd.exemplerealisation(..args)
```

Exemple de réalisation numéroté : bandeau bleu portant un badge « 001 » et le titre, corps en deux colonnes (texte à gauche, figure ou réponse à droite).

Le titre peut renvoyer à une cible du document (`cible: <fiche-med>`) : il devient alors un lien cliquable. Le titre est blanc sur le bandeau.

Exemple :

```typ
#rd.exemplerealisation(lateral: [Schéma])[Tracer une médiatrice][On trace un arc de cercle de chaque côté.]
```

## rd.ficheno

```typ
rd.ficheno(corps, ..cles)
```

Fiche numérotée : boîte de 7 cm, bandeau « Fiche n° X ».

Toutes les clés de tcolorbox (`colframe`, `coltext`…) sont prises en compte. Le numéro peut être automatique (compteur qui s'incrémente à chaque fiche) ou imposé.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.ficheno[Cette fiche regroupe les exercices d'application directe.]
#rd.ficheno(numero: 7, colframe: rgb("#2a9d8f"))[Fiche de révision.]
```

## rd.figbox

```typ
rd.figbox(corps, ..cles)
```

Conteneur de figure avec titre : sans cadre, titre en haut à gauche, contenu centré.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la figure. |  |

Exemple :

```typ
#rd.figbox(title: [Figure 1], width: 5cm, height: 2cm)[Aire d'un disque]
```

## rd.formula

```typ
rd.formula(corps, ..cles)
```

Formule mise en avant, avec onglet vertical « Formule » : fond teinté, bande sombre à gauche. Version bloc ; `myformule` est la version en ligne.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la formule. |  |

Exemple :

```typ
#rd.formula[$a^2 + b^2 = c^2$]
```

## rd.miniexemple

```typ
rd.miniexemple(corps, ..cles)
```

Petit encart à coins en crochets : fond gris, deux crochets dessinés au milieu des bords (en haut à gauche et en bas à droite), contenu centré. Pour un mini-exemple ou une citation.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.miniexemple[$2/3 + 1/6 = 5/6$]
```

## rd.mydoc

```typ
rd.mydoc(titre, corps, ..cles)
```

Encadré gris titré, façon « document » : bandeau gris foncé, fond gris clair. Pour un extrait de programme, une fiche, un encart neutre. Le style nommé `mydoc` (vide par défaut) est appliqué d'office.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre dans le bandeau. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.mydoc[Document de référence][Extrait du programme officiel.]
```

## rd.myformule

```typ
rd.myformule(corps, ..cles)
```

Formule mise en avant, EN LIGNE : même aspect que `formula`, à la taille du contenu, dans le fil du texte.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la formule. |  |

Exemple :

```typ
On retient #rd.myformule[$E = m c^2$] pour la suite.
```

## rd.rappelbox

```typ
rd.rappelbox(corps, ..cles)
```

Rappel en ligne : comme `myformule`, avec l'onglet « Rappel ». Pour rappeler une propriété déjà vue.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte rappelé. |  |

Exemple :

```typ
#rd.rappelbox[un rappel]
```

## rd.regularcell

```typ
rd.regularcell(corps, ..cles)
```

Une cellule de grille bordée : fond blanc, filet noir, contenu centré. La grille complète, avec hauteurs égales, est `regulartcbitemize`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu de la cellule. |  |

Exemple :

```typ
#rd.regularcell(width: 3cm)[$2 times 3 = 6$]
```

## rd.regulartcbitemize

```typ
rd.regulartcbitemize(colonnes, ..cellules)
```

Grille de cellules bordées, de hauteurs égales par rangée. Le premier argument est le nombre de colonnes (`raster columns`) ; le corps est UN SEUL bloc `[…]`, une cellule par `-`.

La syntaxe environnement donne le même résultat : `#begin(rd.regulartcbitemize, 3)` … `#end(rd.regulartcbitemize)`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `colonnes` | (positionnel) | int | nombre de colonnes. |  |

Exemple :

```typ
#rd.regulartcbitemize(3)[
  - $2 times 3 = 6$
  - $5 + 7 = 12$
  - $9 - 4 = 5$
  - $8 div 2 = 4$
]
```

## rd.schemamainlevee

```typ
rd.schemamainlevee(corps, titre: [Schéma à main levée], ..cles)
```

Zone « Schéma à main levée » : invite l'élève à tracer un croquis. Le style nommé `schemamainleveetyle` (vide par défaut) est appliqué d'office.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | consigne. |  |
| `titre` | `[Schéma à main levée]` | content | titre du bandeau. |  |

Exemple :

```typ
#rd.schemamainlevee(height: 2cm)[Dessine un triangle approximatif.]
```

## rd.scratchuse

```typ
rd.scratchuse(titre, corps, ..cles)
```

Encadré coloré à bandeau de titre : magenta de Scratch par défaut, fond de la même teinte à 10 %. Pour une consigne ou une explication liée à un usage de Scratch, ou plus généralement un encart coloré titré.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre dans le bandeau. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.scratchuse[Bloc Scratch utilisé][On déplace le lutin de *10 pas*.]
```

## rd.tcalignbox

```typ
rd.tcalignbox(corps, ..cles)
```

Version EN LIGNE de `alignbox` : une boîte sans cadre qui centre son contenu.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
avant #rd.tcalignbox(width: 2cm)[aligné] après
```

## rd.tcencadre

```typ
rd.tcencadre(corps, ..cles)
```

Encadré gris EN LIGNE : un mot ou une courte expression dans un cadre arrondi gris clair.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
Le mot #rd.tcencadre[encadré] est entouré.
```

## rd.tcwhite

```typ
rd.tcwhite(corps, ..cles)
```

Boîte blanche semi-transparente EN LIGNE : fond blanc à 70 %, coins arrondis, sans cadre. Pour poser du texte lisible par-dessus une image ou une figure.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.tcwhite[boîte blanche]
```

## rd.zone

```typ
rd.zone(titre, corps, ..cles)
```

Zone thématique à titre en ruban : cadre arrondi bleu, titre blanc dans un bandeau plein, contenu centré. Pour « À retenir », un objectif de séance, un encart thématique.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre dans le bandeau. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.zone[Objectif de la séance][Savoir reconnaître un triangle rectangle.]
```

## rd.acocher

```typ
rd.acocher(corps, ..cles)
```

Proposition à cocher : mince colonne bleutée à gauche, qui tient lieu de case, texte centré à droite. En version professeur, une proposition `juste` est cochée en rouge (style nommé prédéfini `br`).

Le contenu s'affiche à droite de la case.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la proposition. |  |

Exemple :

```typ
#rd.acocher(juste: true)[Cette affirmation est vraie.]
#rd.acocher[Cette affirmation est fausse.]
```

## rd.boxpointlignesrep

```typ
rd.boxpointlignesrep(..paires)
```

Trace les liaisons d'une activité « à relier » : un segment rouge entre le point de gauche et le point de droite de chaque paire. Les numéros sont ceux d'apparition, en partant de 1, côté gauche et côté droit séparément.

Par défaut, les traits n'apparaissent QU'EN VERSION PROFESSEUR (correction). Appeler la fonction après les éléments concernés ; elle remet ensuite les deux compteurs à zéro, ce qui permet d'enchaîner plusieurs activités dans un même document.

Exemple :

```typ
#grid(columns: (1fr, 1fr), column-gutter: 3cm,
  rd.leftpoint[$2^3$], rd.rightpoint[$8$],
  rd.leftpoint[$3^2$], rd.rightpoint[$9$])
#rd.boxpointlignesrep((1, 1), (2, 2))
```

## rd.casesvf

```typ
rd.casesvf(..cles)
```

Les deux cases « Vrai » et « Faux » empilées. Avec `reponse`, la bonne case est cochée en version professeur.

Exemple :

```typ
#rd.casesvf(reponse: true)
```

## rd.cinema

```typ
rd.cinema(corps, ..cles)
```

Cadre « pellicule de film » : deux bandes noires perforées de blanc, en haut et en bas, le contenu entre les deux. Pour le storytelling, des séquences d'images, un thème cinéma.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.cinema(width: 6cm)[#align(center)[*Séquence vidéo*]]
```

## rd.coinpli

```typ
rd.coinpli(corps, ..cles)
```

Note à coin plié : fond gris clair, coin inférieur droit « replié », contenu centré. Pour une astuce, un mémo, un effet post-it.

Le texte est en Erewhon italique (clé globale `police-manuscrite`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.coinpli[Note repliée dans le coin.]
```

## rd.corrdembox

```typ
rd.corrdembox(titre, corps, ..cles)
```

Correction de démonstration en rouge : texte rouge en gras, titre blanc centré sur un bandeau rouge, fond gris clair. Surcouche « correction » d'une démonstration.

Par défaut, la boîte n'apparaît QU'EN VERSION PROFESSEUR ; `visible: true` l'impose partout.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre du bandeau. |  |
| `corps` | (positionnel) | content | le texte de la correction. |  |

Exemple :

```typ
#rd.corrdembox[Correction][$x = 7$ est la solution de l'équation $x - 2 = 5$.]
```

## rd.cours

```typ
rd.cours(titre, corps, ..cles)
```

Bloc de cours haut de gamme : bandeau de titre dégradé du noir au gris, fond gris clair avec un léger voile en biais dans le coin inférieur droit, coins arrondis. Le titre est précédé d'une puce et suivi de « : ».

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre du bloc. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.cours[Définition][Un triangle rectangle est un triangle qui possède un angle droit.]
```

## rd.dottedbox

```typ
rd.dottedbox(corps, ..cles)
```

Boîte de base des éléments à relier : bloc sans cadre à angles vifs, fond uni, numéroté par un compteur automatique (remis à zéro par `rd.reinitialiser-compteur("dottedbox")`). `dottedleftbox` et `dottedrightbox` en sont les spécialisations.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.dottedbox[Un élément]
```

## rd.dottedleftbox

```typ
rd.dottedleftbox(corps, ..cles)
```

Élément de GAUCHE d'une activité « à relier » : fond gris clair, texte aligné à droite, puis une petite case blanche portant le point d'ancrage. À disposer dans une grille à deux colonnes avec `dottedrightbox`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte de l'élément. |  |

Exemple :

```typ
#grid(columns: (1fr, 1fr), column-gutter: 3cm, row-gutter: 3pt,
  rd.dottedleftbox[Carré], rd.dottedrightbox[4 côtés égaux],
  rd.dottedleftbox[Triangle], rd.dottedrightbox[3 côtés])
```

## rd.dottedrightbox

```typ
rd.dottedrightbox(corps, ..cles)
```

Élément de DROITE d'une activité « à relier » : un point d'ancrage dans une case blanche, puis le texte sur fond gris clair.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte de l'élément. |  |

Exemple :

```typ
#rd.dottedrightbox[4 côtés égaux]
```

## rd.ernum

```typ
rd.ernum(n)
```

Badge numéroté à trois chiffres : « 012 » en gras sans empattement. Sert à numéroter des éléments (c'est le numéro de `exemplerealisation`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int | le numéro. |  |

Exemple :

```typ
#rd.ernum(12) (numéro d'exercice)
```

## rd.exemple

```typ
rd.exemple(corps, ..cles)
```

Bloc d'exemples à décor en crochet : pastille grise « Exemple(s) » en haut à gauche, filets gris dessinés sous la pastille, à sa droite et en équerre en bas à droite. Pour illustrer une notion dans un cours.

À ne pas confondre avec `exemple`, l'environnement didactique du paquet farfadet-didactique : celle-ci est la boîte du module `rd` (toujours appelée `rd.exemple`). Le style nommé prédéfini `exemplewithinterior` ajoute un fond blanc translucide.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.exemple[Calculons $3 + 4 times 2 = 3 + 8 = 11$ en respectant les priorités.]
```

## rd.exemplereduit

```typ
rd.exemplereduit(corps, ..cles)
```

Exemple réduit, pour un encart étroit ou en marge : comme `exemple`, avec une pastille décalée vers l'extérieur. Se règle par `width` (8 cm par défaut).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.exemplereduit(width: 8cm)[On factorise : $2x + 4 = 2(x + 2)$.]
```

## rd.helpblock

```typ
rd.helpblock(..args)
```

Bloc d'aide, coup de pouce : cadre turquoise, large bande à gauche portant « Aide » en vertical, partie gauche pour une illustration ou un mot-clé, trait pointillé, puis le texte d'aide. Pour différencier ou étayer un exercice difficile.

Avec UN seul contenu, la boîte n'a pas de partie gauche.

Exemple :

```typ
#rd.helpblock[Indice][Pense à utiliser la propriété de Pythagore dans le triangle $A B C$.]
```

## rd.jourleague

```typ
rd.jourleague(titre, ..lignes)
```

Carte « journée de championnat » : 5 cm sur 1,5 cm, titre centré sur un bandeau gris, puis les lignes équipe, score, score, équipe. Cas d'usage rare : confrontations, classements.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre centré. |  |

Exemple :

```typ
#rd.jourleague([Lundi], ([Calcul mental], [3], [2], [Géométrie]))
```

## rd.leftpoint

```typ
rd.leftpoint(corps, ..cles)
```

Élément de GAUCHE d'une activité « à relier » : texte aligné à droite, point d'ancrage dans la marge droite. Variante sans fond des `dottedleftbox`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte de l'élément. |  |

Exemple :

```typ
#rd.leftpoint[$2^3$]
```

## rd.listecocher

```typ
rd.listecocher(elements, ..cles)
```

Rangée horizontale de cases à cocher : une case et son libellé par élément, en colonnes égales. En version professeur, la ou les bonnes réponses sont cochées en rouge.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `elements` | (positionnel) | array | les libellés, un par case. |  |

Exemple :

```typ
#rd.listecocher(([12], [15], [18]), br: 2)
```

## rd.ltitlebox

```typ
rd.ltitlebox(titre, corps, ..cles)
```

Boîte à titre vertical sur le bord gauche : bande sombre portant le titre écrit de bas en haut, contenu à droite sur fond gris. Pour des encarts à étiquette verticale (« DÉFINITION »).

La bande s'ajuste à la hauteur du titre, et la boîte est au moins aussi haute que le titre est long. `ltitle-width` impose la largeur.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre vertical. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.ltitlebox[Titre][Le titre est écrit verticalement dans la bande de gauche.]
```

## rd.mylink

```typ
rd.mylink(corps, ..cles)
```

Bouton « Aide en ligne » EN LIGNE : bande orange foncé portant « Aide en ligne » en blanc, puis le texte (souvent un lien) sur fond orange pâle. Pour marquer un renvoi vers une aide.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte du bouton. |  |

Exemple :

```typ
Voir #rd.mylink[cliquer ici] pour une aide.
```

## rd.mytcbitembox

```typ
rd.mytcbitembox(corps, ..cles)
```

Un item numéroté isolé : numéro automatique à gauche, texte justifié sur fond gris clair. Le compteur est remis à zéro par `rd.reinitialiser-compteur("mytcbitembox")`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le contenu. |  |

Exemple :

```typ
#rd.mytcbitembox[Calculer $12 times 11$.]
```

## rd.mytcbitemize

```typ
rd.mytcbitemize(..items)
```

Items numérotés disposés en grille : chaque item porte son numéro « 1) » à gauche, texte justifié sur fond gris clair à droite. Pour des questions ou exercices numérotés sur plusieurs colonnes.

La syntaxe environnement donne le même résultat : `#begin(rd.mytcbitemize)` … `#end(rd.mytcbitemize)`.

Exemple :

```typ
#rd.mytcbitemize[
  - Calculer $12 times 11$.
  - Donner le PGCD de $24$ et $36$.
  - Simplifier $display(18/24)$.
]
```

## rd.opbox

```typ
rd.opbox(operations, ..cles)
```

Boîte pour poser des opérations : les opérations en colonnes centrées, puis une zone grise où l'élève effectue ses calculs. En version professeur, la zone grise montre la `solution`.

La zone grise est toujours dessinée ; son contenu ne l'est qu'en version professeur.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `operations` | (positionnel) | array | les opérations à poser, un contenu par colonne. |  |

Exemple :

```typ
#rd.opbox(
  ([347 \ + 126], [58 \ $times$ 7]),
  solution: ([473], [406]),
)
```

## rd.parchemin

```typ
rd.parchemin(corps, ..cles)
```

Parchemin : papier déchiré à fond dégradé, plus sombre sur les bords, qui tient lieu de texture. Pour une narration, l'histoire des maths, une énigme à thème.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.parchemin[Un vieux parchemin pour présenter un énoncé historique.]
```

## rd.partieDNB

```typ
rd.partieDNB(corps, ..cles)
```

Label « ■ Partie X » EN LIGNE : badge gris clair en gras avec une légère ombre, pour marquer les parties d'un sujet de brevet.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le numéro ou le nom de la partie. |  |

Exemple :

```typ
#rd.partieDNB[1] Activités numériques
```

## rd.progbox

```typ
rd.progbox(titre, corps, ..cles)
```

Boîte de programme ou d'algorithme colorée et titrée : cyan, coins arrondis, ombre floue, dégradé intérieur, titre centré en gras. Version plus affirmée de `boiteprog`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre centré. |  |
| `corps` | (positionnel) | content | le programme. |  |

Exemple :

```typ
#rd.progbox[Programme de calcul][Choisir un nombre, le multiplier par 3, ajouter 5.]
```

## rd.rightpoint

```typ
rd.rightpoint(corps, ..cles)
```

Élément de DROITE d'une activité « à relier » : point d'ancrage dans la marge gauche, texte aligné à gauche.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le texte de l'élément. |  |

Exemple :

```typ
#rd.rightpoint[$8$]
```

## rd.sans-coin

```typ
rd.sans-coin(corps, ..cles)
```

Cadre dont un coin n'est pas dessiné : le trait s'interrompt à l'approche du coin, pour y raccorder un onglet, un ruban ou une autre boîte.

Seul le coin manque : le reste du cadre est dessiné.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.sans-coin(coin: top + left, title: [Coin haut-gauche absent])[Le coin supérieur gauche n'est pas dessiné.]
```

## rd.scratchblock

```typ
rd.scratchblock(corps, ..cles)
```

Bloc de programme Scratch numéroté EN LIGNE : bandeau gris « Programme N », contenu sur fond blanc. Le numéro s'incrémente à chaque bloc ; `rd.resetScratchCounters()` le remet à zéro.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le programme (texte ou figure). |  |

Exemple :

```typ
#rd.scratchblock[bloc Scratch]
```

## rd.scratchblockenv

```typ
rd.scratchblockenv(corps, ..cles)
```

Bloc de programme Scratch numéroté, version BLOC pleine largeur.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | le programme. |  |

Exemple :

```typ
#rd.scratchblockenv[quand le drapeau vert est cliqué : avancer de 10 pas.]
```

## rd.scratchcapture

```typ
rd.scratchcapture(corps, ..cles)
```

Capture d'écran numérotée « Image N » : cadre orange, bandeau orange pâle centré, fond blanc. Pour montrer le résultat visuel d'un programme.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la capture. |  |

Exemple :

```typ
#rd.scratchcapture[(capture d'écran d'un programme)]
```

## rd.scratchfig

```typ
rd.scratchfig(corps, ..cles)
```

Figure numérotée EN LIGNE : bandeau beige « Figure N », contenu centré. Le compteur est partagé avec `scratchfigbox`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la figure. |  |

Exemple :

```typ
#rd.scratchfig[figure]
```

## rd.scratchfigbox

```typ
rd.scratchfigbox(corps, ..cles)
```

Figure numérotée, version BLOC ; mêmes numéros que `scratchfig`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | la figure. |  |

Exemple :

```typ
#rd.scratchfigbox(width: 5cm)[(figure produite par le programme)]
```

## rd.tccoinpli

```typ
rd.tccoinpli(corps, ..cles)
```

Note à coin plié EN LIGNE : la version de `coinpli` à la taille du contenu.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
avant #rd.tccoinpli[coin plié] après
```

## rd.thermobox

```typ
rd.thermobox(..cles)
```

Thermomètre graphique : tube bleu de 1,5 cm sur 3 cm avec un niveau de liquide. Pour des problèmes de température, des jauges, des niveaux.

Exemple :

```typ
#rd.thermobox()
```

## rd.tornpage

```typ
rd.tornpage(corps, ..cles)
```

Feuille de papier déchirée : fond papier, contour irrégulier, ombre portée. Pour une note manuscrite, un extrait « arraché », un aparté décoratif.

Le contour est tracé par un petit générateur pseudo-aléatoire interne et DÉTERMINISTE : la même `graine` donne toujours le même bord, d'une compilation à l'autre. Changer `graine` donne un autre bord.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.tornpage[Une feuille au bord déchiré, parfaite pour une citation manuscrite.]
```

## rd.vf

```typ
rd.vf(corps, ..cles)
```

Item vrai ou faux numéroté : énoncé à gauche, colonne grise à droite avec deux cases « Vrai » et « Faux » (`casesvf`), numéro sur fond noir dans le coin. En version professeur, la bonne case est cochée si `reponse` est donnée. Le compteur est remis à zéro par `rd.reinitialiser-compteur("vf")`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | l'affirmation. |  |

Exemple :

```typ
#rd.vf(reponse: true)[Tout carré est un rectangle.]
```

## rd.designbox

```typ
rd.designbox(titre, corps, ..cles)
```

Encart « design » sophistiqué, inspiré d'InDesign : cadre arrondi, bandeau de titre sombre à droite dont le bord se creuse en biseau (effet de coin « pelé »), fond dégradé vers le bas, sous-texte facultatif à gauche du titre. Pour l'ouverture d'un chapitre ou un contenu vedette.

Avec `flat: false`, le bandeau reçoit un dégradé et le titre une ombre portée (`shadow-title`). Le style nommé `designboxstyle` (vide par défaut) est appliqué d'office.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | (positionnel) | content | titre, à droite du bandeau. |  |
| `corps` | (positionnel) | content | contenu. |  |

Exemple :

```typ
#rd.designbox(sous-texte: [Pythagore])[Théorème][Le carré de l'hypoténuse est égal à la somme des carrés des deux autres côtés.]
```

## rd.ggbentrainer

```typ
rd.ggbentrainer(..args)
```

Bloc « S'entraîner en autonomie » : un cadre bleu à angle supérieur gauche vif, un onglet « S'entraîner / en autonomie » en haut à gauche, une tablette dessinée, puis une colonne de droite (10 cm) pour la consigne. Pour un entraînement adossé à une ressource en ligne.

Les textes utilisent la police sans empattement du paquet (clé globale `police-sans`).

Exemple :

```typ
#rd.ggbentrainer[Suis le lien pour t'entraîner.][Construire un triangle équilatéral avec GeoGebra.]
```

## rd.ggbqr

```typ
rd.ggbqr(url, ..cles)
```

Encart GeoGebra : capture d'écran et QR code vers une ressource. Le titre, en bas, est le lien lui-même. La boîte épouse la taille de son contenu.

Les images ne sont plus cherchées par nom de fichier (`capture_ggb_<clé>`) : on passe directement le contenu, par exemple `image("capture.png")`. Le QR code de l'adresse sera généré par le paquet de QR code embarqué ; tant qu'il ne l'est pas, une place réservée en pointillés le remplace (ou on passe l'image d'un QR code dans `qr:`). Sans `capture`, une place réservée en pointillés la remplace aussi.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `url` | (positionnel) | str | la fin de l'adresse (l'identifiant de la ressource). |  |

Exemple :

```typ
#rd.ggbqr("demo123", height: 1.6cm)
```

## rd.ggbqrenv

```typ
rd.ggbqrenv(url, ..cles)
```

Encart GeoGebra pleine largeur : comme `ggbqr`, mais la boîte occupe la largeur disponible, capture et QR code centrés chacun dans une colonne.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `url` | (positionnel) | str | la fin de l'adresse. |  |

Exemple :

```typ
#rd.ggbqrenv("demo123", height: 1.6cm)
```

## rd.icone-tablette

```typ
rd.icone-tablette(hauteur: 1cm, couleur: o.palette.ggb)
```

Dessin d'une tablette : cadre gris, écran bleu, bouton.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `hauteur` | `1cm` | length | hauteur de la tablette. |  |
| `couleur` | `o.palette.ggb` | color | couleur de l'écran. |  |

Exemple :

```typ
#rd.icone-tablette(hauteur: 1cm)
```

## rd.methode

```typ
rd.methode(corps, ..cles)
```

Bloc « méthode » : un onglet sombre à gauche portant le titre, un ruban dégradé du noir au gris qui court en haut, et en bas un filet qui se termine en bosse avec un petit rond blanc. Le texte s'écrit à droite de l'onglet. Pour présenter une technique pas à pas.

Le titre est « Méthode ». Pour d'autres titres (« Technique », « Astuce »…), utiliser `title:`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) | content | contenu de la méthode. |  |

Exemple :

```typ
#rd.methode[*1.* Repérer l'angle droit. *2.* Identifier l'hypoténuse. *3.* Appliquer la relation de Pythagore.]
```

## rd.tache

```typ
rd.tache(etiquette, titre, corps, ..cles)
```

Tâche complexe, au format des problèmes ouverts : fond arrondi vert pâle sans cadre, avec ombre floue, titre en gras en haut, et un ruban orange légèrement incliné, accroché au bord gauche, portant l'étiquette (« Défi », « Tâche complexe »…) en blanc ; sous son bout gauche, un pli sombre en demi-disque déborde du fond. Pour une situation-problème ou un problème ouvert.

Le ruban mesure 1,2 cm ; il s'allonge si l'étiquette n'y tient pas, et le titre se décale d'autant : le ruban ne le recouvre jamais.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `etiquette` | (positionnel) | content | texte du ruban orange. |  |
| `titre` | (positionnel) | content | titre de la tâche. |  |
| `corps` | (positionnel) | content | l'énoncé. |  |

Exemple :

```typ
#rd.tache[Défi][Construire un cerf-volant][À partir de deux diagonales perpendiculaires, construis un cerf-volant.]
```

## rd.resetScratchCounters

```typ
rd.resetScratchCounters()
```

Remet à zéro les trois compteurs Scratch (`scratchblock`, `scratchfig`, `scratchcapture`) : pour que la numérotation recommence à 1.

LaTeX : `\resetScratchCounters`

Exemple :

```typ
#rd.resetScratchCounters()
```
