# farfadet-didactique

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": didactique` puis `#import didactique: *`.
- Réglage : `setbfenvironments`, `setbfskins`, `setbfsections` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-didactique.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-didactique`).

## Sommaire

- `activite` — Activité de découverte, en banderole de la couleur `act` ; sécable par défaut.
- `aide` — Coup de pouce, dans un cadre déchiré à étiquette inclinée de la couleur `nota`.
- `contre-exemple` — Contre-exemple, dans le cadre à équerre rouge.
- `definition` — Définition d'un mot ou d'une notion, en banderole de la couleur `defi`.
- `demonstration` — Démonstration, en banderole de la couleur `demo` ; cadre tracé à la craie par défaut.
- `exemple` — Exemple, dans le cadre à équerre de bfcours.
- `histoire` — Encart « Un peu d'histoire » : onglet sépia, titre (premier contenu, obligatoire) et auteur facultatif.
- `methode` — Méthode de résolution, en banderole de la couleur `meth`.
- `neutre` — Conteneur neutre : ni cadre, ni fond, ni marge. (Distinct du mot-clé `none` de Typst.)
- `notation` — Notation, dans un cadre déchiré à étiquette inclinée de la couleur `defi`.
- `propriete` — Propriété à retenir, en banderole de la couleur `prop`.
- `remarque` — Remarque en marge, avec le crayon et la barre en serpentin. Le titre éventuel n'est pas affiché (il sert au sommaire et aux cartes Anki).
- `solution` — Solution d'un exercice ou d'une activité, en banderole verte.
- `theoreme` — Théorème : énoncé central du cours, en banderole de la couleur `thm`.
- `vocabulaire` — Encadré de vocabulaire, en banderole de la couleur `nota`.
- `bf-env` — Environnement didactique à couleur libre : le titre (premier contenu, obligatoire) est le texte de la banderole.
- `bfbox` — Forme « environnement » de `boite` (même rendu, mêmes clés tcolorbox).
- `boite` — Boîte à cadre et titre en bandeau, à la couleur d'accent courante (`\boitecouleur`) : gris foncé hors environnement, couleur de l'environne…
- `boite-figure` — Cadre de figure légendée : étiquette noire (premier contenu) dans l'angle supérieur gauche, contenu centré.
- `cracked` — Cadre à bord déchiré et étiquette inclinée (base de `notation` et `aide`). Le titre de l'étiquette est le premier contenu (facultatif, « Pr…
- `new-bfd-palette` — Déclare une palette (`\NewBfdPalette{nom}{thm=…, defi=…}`). Les couleurs absentes gardent leur valeur au moment de l'activation. Valeurs : …
- `bfd-activate-palette` — Active une palette (`\bfdActivatePalette{nom}`) : `default`, `ocean`, `vintage` ou une palette déclarée par `new-bfd-palette`. Les environn…
- `bfd-activate-variant` — Choisit l'habillage des environnements à banderole (`\bfdActivateVariant{…}`) : `"lignes"` (défaut : filets gauche et bas, sous-titre centr…
- `bfset` — Interface unique de configuration de new-bfcours-environments (`\bfset{palette=…, variant=…}`).
- `setbfenvironments` — Règle les environnements didactiques pour la suite du document : le setter de farfadet-didactique pour les environnements (signature commun…
- `bfskin` — Variante d'un skin : un skin (fonction `d => contenu`) dont certaines options sont figées.
- `setbfskins` — Enregistre des skins sous un nom, pour la suite du document : `rendu: "<nom>"` les appelle ensuite partout où la clé `rendu` est acceptée (…
- `coloredsquare` — Carré plein de 3 ex de côté (`\coloredsquare{couleur}`).
- `dimcoloredsquare` — Carré plein de côté choisi en ex (`\dimcoloredsquare{couleur}{taille}`).
- `liencontent` — Affiche une catégorie en gras et dépose une entrée au sommaire « **catégorie** - titre » (`\liencontent{catégorie}{titre}`, avec la mise au…
- `setbfsections` — Règle les titres (`=`, `==`, `===`, `====`) pour la suite du document : le setter de farfadet-didactique pour le sectionnement (signature c…
- `tableofcontents` — Table des matières sur plusieurs colonnes (`\tableofcontents` de bfcours) : titres de section et de sous-section, et environnements didacti…
- `printvocindex` — Boîte « Vocabulaire utilisé » (`\printvocindex`) : tous les mots passés à `voc`, en gras, avec leur page (lien cliquable). À placer en fin …
- `tableau-vocabulaire-sommaire` — Tableau de révision du vocabulaire (`\tableauVocabulaireSommaire`) : une ligne par mot (le mot est précédé d'un crayon), colonnes « Vu en c…
- `voc` — Mot de vocabulaire (`\voc{mot}`) : en gras, à la couleur d'accent courante, et noté pour l'index du vocabulaire (`printvocindex`). Seule la…
- `vocref` — Mot en gras rose (la couleur nommée `monrose`, lue au rendu : `setbfcolors(monrose: …)`), lien vers une adresse (`\vocref{url}{mot}`). En L…

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `label` | Rend l'environnement référençable : avec `label: <chasles>`, `@chasles` affiche « Propriété 2.3 » s'il est numéroté, sinon son titre. Propre à chaque objet. LaTeX : `label`. |  | 16 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `version` | `"toutes"`, `"prof"` ou `"eleve"` : n'affiche l'objet que dans la version indiquée du document. Défaut : `"toutes"`. LaTeX : ajout. |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `rendu` | Rendu de la boîte : `"bf"` (le rendu de bfcours), `"rd"` (la boîte du paquet `rdboites` qui correspond à l'environnement), un skin intégré (`"cahier"`, `"outil"`, `"pastille"`, `"manchette"`, `"filet"`, `"suspendu"`, `"… |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `rd` | Clés passées à la boîte `rdboites` en style `"rd"` (`colframe`, `arc`, `colback`…) ; sans effet en style `"bf"`. Elles l'emportent sur les clés de bfcours réglées (`couleur`, `colback`, `colframe`…), que le style « rd »… |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `skin` | Options transmises au skin (champ `d.options`) : `icone`, `epaisseur`… pour un skin intégré (`skin: (icone: "cle")`), libres pour un skin personnel ; elles l'emportent sur celles d'une variante `bfskin`. Sans effet avec… |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `before-skip` | Espace vertical avant l'objet. `auto` : calibrage de bfcours. Défaut : `auto`. LaTeX : `before skip`. |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `after-skip` | Espace vertical après l'objet. `auto` : calibrage de bfcours. Défaut : `auto`. LaTeX : `after skip`. |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `anki` | Dépose une carte Anki (recto : type et titre ou numéro ; verso : corps), invisible dans le PDF. Défaut : `false`. LaTeX : ajout. |  | 11 : `activite`, `aide`, `contre-exemple`, `demonstration`, `exemple`, `histoire`, `notation`, `remarque` … |
| `sommaire` | Entrée au sommaire (`tableofcontents`). Un contenu remplace le libellé de l'entrée. Défaut : `true`. LaTeX : ajout (en LaTeX, `\liencontent` met toujours au sommaire). |  | 12 : `activite`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode`, `propriete` … |
| `numero` | Numérote l'environnement (« Définition 2.3 »). Défaut : `false`. LaTeX : ajout (les environnements bfcours ne sont pas numérotés). |  | 16 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `numerotation` | Remise à zéro du compteur : `"section"` (numéro « 2.3 ») ou `"globale"` (numéro « 3 »). Défaut : `"section"`. LaTeX : ajout. |  | 16 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `compteur` | `"par-type"` (un compteur par type) ou `"commun"` (un compteur partagé par tous les types qui le choisissent). Défaut : `"par-type"`. LaTeX : ajout. |  | 16 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `nameref` | Texte affiché par `@étiquette` quand l'environnement n'est pas numéroté. `auto` : le titre, sinon le nom du type. Défaut : `auto`. LaTeX : `nameref`. | nameref | 16 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `craie` | Cadre « à la craie » (replié sur le cadre net si l'environnement se coupe). Défaut : `false`. LaTeX : ajout. |  | 8 : `activite`, `definition`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire`, `bf-env` |
| `icone` | Pictogramme devant le nom dans la banderole (à la place du crayon pour la remarque). Défaut : `none`. LaTeX : ajout ; sur `\begin{Remarque}` : option bclogo `logo`. |  | 11 : `activite`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `methode`, `propriete`, `solution` … |
| `variant` | Habillage des bords : `"lignes"` (filets gauche et bas), `"minimal"` (fin filet gauche, sans sous-titre), `"sidebar"` (bande pleine à gauche). Se règle pour tout le document par `bfd-activate-variant` ou `bfset(variant:… | \bfdActivateVariant, \bfset{variant=…} | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `colback` | Couleur du fond. Défaut : `white`. LaTeX : `colback`. | colback | 12 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `colframe` | Couleur des filets et du cadre du sous-titre. `auto` : couleur!50. Défaut : `auto`. LaTeX : `colframe`. | colframe | 13 : `activite`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `methode`, `propriete`, `solution` … |
| `colbacktitle` | Couleur du ruban (ou du bandeau) de titre. `auto` : la couleur de l'environnement. Défaut : `auto`. LaTeX : `colbacktitle`. | colbacktitle | 11 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `banner-arc` | Couleur des deux arcs sous la banderole. `auto` : couleur!80. Défaut : `auto`. LaTeX : 1er argument de `bfd banner arc`. | 1er argument de bfd banner arc | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `coltitle` | Couleur du texte du titre. Défaut : `white`. LaTeX : `coltitle`. | coltitle | 11 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `fonttitle` | Taille du titre : nom de taille LaTeX (`"large"`, `"Large"`…) ou longueur. Défaut : `"large"`. LaTeX : `fonttitle`. | fonttitle | 12 : `activite`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `methode`, `propriete`, `remarque` … |
| `arc` | Rayon des coins. Défaut : `1mm`. LaTeX : `arc`. | arc | 11 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `edge-width` | Épaisseur des filets gauche et bas. Défaut : `0.5mm`. LaTeX : `line width` de `bfd edge overlay`. | line width de bfd edge overlay | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `left` | Marge intérieure gauche (sans `boxsep`). Défaut : `4mm`. LaTeX : `left`. | left | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `right` | Marge intérieure droite (sans `boxsep`). Défaut : `4mm`. LaTeX : `right`. | right | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `top` | Marge intérieure haute (sans `boxsep`). Défaut : `2mm`. LaTeX : `top`. | top | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `bottom` | Marge intérieure basse (sans `boxsep`). Défaut : `2mm`. LaTeX : `bottom`. | bottom | 8 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` |
| `boxsep` | Marge ajoutée sur les quatre côtés. Défaut : `1mm`. LaTeX : `boxsep`. | boxsep | 11 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `drop-shadow` | Ombre portée. Défaut : `true`. LaTeX : `drop shadow` (`drop fuzzy shadow` pour `cracked`). | drop shadow (drop fuzzy shadow pour cracked) | 12 : `activite`, `aide`, `definition`, `demonstration`, `methode`, `notation`, `propriete`, `solution` … |
| `title-xshift` | Décalage horizontal de la banderole depuis le bord gauche. Défaut : `1cm`. LaTeX : `xshift` de `attach boxed title to top left`. | xshift de attach boxed title to top left | 9 : `activite`, `definition`, `demonstration`, `methode`, `propriete`, `solution`, `theoreme`, `vocabulaire` … |
| `style` | style(s) nommé(s) à appliquer (sous les clés écrites ici). |  | 20 : `activite`, `aide`, `contre-exemple`, `definition`, `demonstration`, `exemple`, `histoire`, `methode` … |
| `sommaire` | Entrée au sommaire (`tableofcontents`). Un contenu remplace le libellé de l'entrée. Défaut : `false`. LaTeX : ajout (en LaTeX, `\liencontent` met toujours au sommaire). |  | 4 : `aide`, `notation`, `remarque`, `cracked` |
| `embleme` | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  | 9 : `aide`, `histoire`, `methode`, `vocabulaire`, `bf-env`, `bfbox`, `boite`, `boite-figure` … |
| `fonttitle` | Taille du titre : nom de taille LaTeX (`"large"`, `"Large"`…) ou longueur. Défaut : `16pt`. LaTeX : `fonttitle`. | fonttitle | 3 : `aide`, `notation`, `cracked` |
| `left` | Marge intérieure gauche (sans `boxsep`). Défaut : `5mm`. LaTeX : `left`. | left | 3 : `aide`, `notation`, `cracked` |
| `right` | Marge intérieure droite (sans `boxsep`). Défaut : `5mm`. LaTeX : `right`. | right | 3 : `aide`, `notation`, `cracked` |
| `top` | Marge intérieure haute (sans `boxsep`). Défaut : `10mm`. LaTeX : `top`. | top | 3 : `aide`, `notation`, `cracked` |
| `bottom` | Marge intérieure basse (sans `boxsep`). Défaut : `5mm`. LaTeX : `bottom`. | bottom | 3 : `aide`, `notation`, `cracked` |
| `line-width` | Épaisseur des traits du cadre. Défaut : `1.594pt`. LaTeX : `line width` / `ultra thick`. | line width / ultra thick | 3 : `aide`, `notation`, `cracked` |
| `couleur-titre` | Couleur de l'étiquette inclinée. `auto` : celle du cadre. Défaut : `auto`. LaTeX : 4e argument `[couleur titre]`. | 4e argument [couleur titre] | 3 : `aide`, `notation`, `cracked` |
| `largeur-titre` | Largeur de l'étiquette inclinée. `auto` : celle du type. Défaut : `auto`. LaTeX : 5e argument `[largeur titre]`. | 5e argument [largeur titre] | 3 : `aide`, `notation`, `cracked` |
| `amplitude` | Amplitude du bord déchiré. Défaut : `2.49pt`. LaTeX : `amplitude` de `random steps`. | amplitude de random steps | 3 : `aide`, `notation`, `cracked` |
| `segment-length` | Pas du bord déchiré. Défaut : `0.4cm`. LaTeX : `segment length` de `random steps`. | segment length de random steps | 3 : `aide`, `notation`, `cracked` |
| `title-angle` | Inclinaison de l'étiquette. Défaut : `-10deg`. LaTeX : `rotate=10` du titre. | rotate=10 du titre | 3 : `aide`, `notation`, `cracked` |
| `couleur` | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  | 3 : `contre-exemple`, `exemple`, `remarque` |
| `breakable` | Autorise la coupure entre deux pages. Défaut : `false`. LaTeX : `breakable`. | breakable | 13 : `contre-exemple`, `definition`, `demonstration`, `exemple`, `methode`, `neutre`, `propriete`, `solution` … |
| `colback` | Couleur du fond. Défaut : `auto`. LaTeX : `colback`. | colback | 3 : `contre-exemple`, `exemple`, `histoire` |
| `couleur-accent` | Couleur d'accent du corps (`acc`, `voc`…). `auto` : celle du type. Défaut : `auto`. LaTeX : `\CouleurTexteAccent` du corps. | \CouleurTexteAccent du corps | 3 : `contre-exemple`, `exemple`, `remarque` |
| `anki` | Dépose une carte Anki (recto : type et titre ou numéro ; verso : corps), invisible dans le PDF. Défaut : `true`. LaTeX : ajout. |  | 5 : `definition`, `methode`, `propriete`, `theoreme`, `vocabulaire` |
| `bottom` | Marge intérieure basse (sans `boxsep`). Défaut : `0pt`. LaTeX : `bottom`. | bottom | 3 : `bf-env`, `bfbox`, `boite` |

## activite

```typ
activite(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Activité de découverte, en banderole de la couleur `act` ; sécable par défaut.

Syntaxe : `#activite[Titre][Corps]` ou `#activite[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Activite", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1567.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `craie`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `breakable` | `auto` | bool | Autorise la coupure entre deux pages. Défaut : `true`. LaTeX : `breakable`. | breakable |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#activite[Découverte][Tracer deux vecteurs de même direction.]
```

## aide

```typ
aide(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, embleme: auto, fonttitle: auto, left: auto, right: auto, top: auto, bottom: auto, drop-shadow: auto, line-width: auto, couleur-titre: auto, largeur-titre: auto, amplitude: auto, segment-length: auto, title-angle: auto, style: auto, ..args)
```

Coup de pouce, dans un cadre déchiré à étiquette inclinée de la couleur `nota`.

Syntaxe : `#aide[Titre][Corps]` ou `#aide[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Aide", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1687.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `embleme`, `fonttitle`, `left`, `right`, `top`, `bottom`, `drop-shadow`, `line-width`, `couleur-titre`, `largeur-titre`, `amplitude`, `segment-length`, `title-angle`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |

Exemple :

```typ
#aide[Pense à factoriser.]
```

## contre-exemple

```typ
contre-exemple(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, icone: auto, embleme: auto, colback: auto, colframe: auto, fonttitle: auto, couleur-accent: auto, line-width: auto, corner-size: auto, style: auto, ..args)
```

Contre-exemple, dans le cadre à équerre rouge.

Syntaxe : `#contre-exemple[Titre][Corps]` ou `#contre-exemple[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "ContreExemple", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1640.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `couleur`, `breakable`, `icone`, `colback`, `colframe`, `fonttitle`, `couleur-accent`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |
| `line-width` | `auto` | length | Épaisseur des traits du cadre. Défaut : `1.494pt`. LaTeX : `line width` / `ultra thick`. | line width / ultra thick |
| `corner-size` | `auto` | length | Longueur des branches de l'équerre et du trait vertical. Défaut : `2cm`. LaTeX : `2cm` de `bfd tikz corners overlay`. | 2cm de bfd tikz corners overlay |

Exemple :

```typ
#contre-exemple[Une fonction][$x |-> |x|$ n'est pas dérivable en $0$.]
```

## definition

```typ
definition(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Définition d'un mot ou d'une notion, en banderole de la couleur `defi`.

Syntaxe : `#definition[Titre][Corps]` ou `#definition[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Definition", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1563.

LaTeX : `\Definition`

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#definition[Vecteur][Un vecteur est défini par une direction, un sens et une norme.]
```

## demonstration

```typ
demonstration(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Démonstration, en banderole de la couleur `demo` ; cadre tracé à la craie par défaut.

Syntaxe : `#demonstration[Titre][Corps]` ou `#demonstration[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Demonstration", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1565.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `craie` | `auto` | bool | Cadre « à la craie » (replié sur le cadre net si l'environnement se coupe). Défaut : `true`. LaTeX : ajout. |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#demonstration[Chasles][On décompose $arrow(A C)$ en passant par $B$.]
```

## exemple

```typ
exemple(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, icone: auto, embleme: auto, colback: auto, colframe: auto, fonttitle: auto, couleur-accent: auto, line-width: auto, corner-size: auto, style: auto, ..args)
```

Exemple, dans le cadre à équerre de bfcours.

Syntaxe : `#exemple[Titre][Corps]` ou `#exemple[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Exemple", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1617.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `couleur`, `breakable`, `icone`, `colback`, `colframe`, `fonttitle`, `couleur-accent`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |
| `line-width` | `auto` | length | Épaisseur des traits du cadre. Défaut : `1.494pt`. LaTeX : `line width` / `ultra thick`. | line width / ultra thick |
| `corner-size` | `auto` | length | Longueur des branches de l'équerre et du trait vertical. Défaut : `2cm`. LaTeX : `2cm` de `bfd tikz corners overlay`. | 2cm de bfd tikz corners overlay |

Exemple :

```typ
#exemple[Avec des entiers][$3 + 4 = 7$.]
```

## histoire

```typ
histoire(auteur: none, label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, embleme: auto, colback: auto, arc: auto, onglet: auto, boxrule: auto, style: auto, ..args)
```

Encart « Un peu d'histoire » : onglet sépia, titre (premier contenu, obligatoire) et auteur facultatif.

Syntaxe : `#histoire[Titre][Corps]` (titre obligatoire, comme en LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Histoire", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:2610.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `embleme`, `colback`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `auteur` | `none` | content, none | Auteur ou source, en italique sous le titre. Défaut : `none`. LaTeX : `[auteur]` (2e argument, optionnel). |  |
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `arc` | `auto` | length | Rayon des coins. Défaut : `4pt`. LaTeX : `arc`. | arc |
| `onglet` | `auto` | content | Libellé de l'onglet. Défaut : `[Un peu d'histoire]`. LaTeX : 2e argument de `bfd syBrisse`. | 2e argument de bfd syBrisse |
| `boxrule` | `auto` | length | Épaisseur du cadre. Défaut : `0.8pt * 72 / 72.27`. LaTeX : `boxrule`. | boxrule |

Exemple :

```typ
#histoire(auteur: [D'après Euclide])[Les Éléments][Euclide rédige les *Éléments* vers 300 avant notre ère.]
```

## methode

```typ
methode(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Méthode de résolution, en banderole de la couleur `meth`.

Syntaxe : `#methode[Titre][Corps]` ou `#methode[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Methode", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1566.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `embleme`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |

Exemple :

```typ
#methode[Résoudre une équation][Isoler l'inconnue.]
```

## neutre

```typ
neutre(version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, breakable: auto, style: auto, ..args)
```

Conteneur neutre : ni cadre, ni fond, ni marge. (Distinct du mot-clé `none` de Typst.)

Syntaxe : `#neutre[Corps]`. Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "None", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:2113.

Clés communes acceptées (voir en tête) : `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `breakable`, `style`.

Exemple :

```typ
#neutre[Contenu groupé.]
```

## notation

```typ
notation(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, embleme: auto, fonttitle: auto, left: auto, right: auto, top: auto, bottom: auto, drop-shadow: auto, line-width: auto, couleur-titre: auto, largeur-titre: auto, amplitude: auto, segment-length: auto, title-angle: auto, style: auto, ..args)
```

Notation, dans un cadre déchiré à étiquette inclinée de la couleur `defi`.

Syntaxe : `#notation[Titre][Corps]` ou `#notation[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Notation", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1680.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `fonttitle`, `left`, `right`, `top`, `bottom`, `drop-shadow`, `line-width`, `couleur-titre`, `largeur-titre`, `amplitude`, `segment-length`, `title-angle`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#notation[Vecteur][On note $arrow(u)$ un vecteur.]
```

## propriete

```typ
propriete(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Propriété à retenir, en banderole de la couleur `prop`.

Syntaxe : `#propriete[Titre][Corps]` ou `#propriete[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Propriete", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1564.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#propriete[Relation de Chasles][$arrow(A B) + arrow(B C) = arrow(A C)$.]
```

## remarque

```typ
remarque(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, icone: auto, embleme: auto, fonttitle: auto, couleur-accent: auto, barre: auto, logo-size: auto, style: auto, ..args)
```

Remarque en marge, avec le crayon et la barre en serpentin. Le titre éventuel n'est pas affiché (il sert au sommaire et aux cartes Anki).

Syntaxe : `#remarque[Titre][Corps]` ou `#remarque[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Remarque", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1581.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `couleur`, `fonttitle`, `couleur-accent`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `breakable` | `auto` | bool | Autorise la coupure entre deux pages. Défaut : `true`. LaTeX : `breakable`. | breakable |
| `icone` | `auto` | content, none, auto | Pictogramme devant le nom dans la banderole (à la place du crayon pour la remarque). Défaut : `auto`. LaTeX : ajout ; sur `\begin{Remarque}` : option bclogo `logo`. |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |
| `barre` | `auto` | str | Barre verticale : serpentin, trait droit ou aucune. Défaut : `"snake"`. LaTeX : option bclogo `barre`. | option bclogo barre |
| `logo-size` | `auto` | length | Côté du logo (crayon). Défaut : `16.9pt`. LaTeX : taille de `\bccrayon`. | taille de \bccrayon |

Exemple :

```typ
#remarque[Cette égalité reste vraie pour des vecteurs nuls.]
```

## solution

```typ
solution(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Solution d'un exercice ou d'une activité, en banderole verte.

Syntaxe : `#solution[Titre][Corps]` ou `#solution[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Solution", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1570.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#solution[Question 1][On trouve $x = 3$.]
```

## theoreme

```typ
theoreme(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Théorème : énoncé central du cours, en banderole de la couleur `thm`.

Syntaxe : `#theoreme[Titre][Corps]` ou `#theoreme[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Theoreme", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1529.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |
| `embleme` | `auto` | str, function, content, none, auto | Icône préférentielle du type pour les skins (`"auto"` ou `none` : l'icône propre au skin) : nom d'une icône du jeu commun, fonction `couleur => contenu` ou contenu. Passe après la clé `icone` et l'option `icone` du skin… |  |

Exemple :

```typ
#theoreme[Pythagore][Dans un triangle rectangle, $a^2 + b^2 = c^2$.]
```

## vocabulaire

```typ
vocabulaire(label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Encadré de vocabulaire, en banderole de la couleur `nota`.

Syntaxe : `#vocabulaire[Titre][Corps]` ou `#vocabulaire[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "Vocabulaire", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1568.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `embleme`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |

Exemple :

```typ
#vocabulaire[Hypoténuse][Côté opposé à l'angle droit.]
```

## bf-env

```typ
bf-env(sous-titre: none, label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, breakable: auto, craie: auto, icone: auto, embleme: auto, variant: auto, colback: auto, colframe: auto, colbacktitle: auto, banner-arc: auto, coltitle: auto, fonttitle: auto, arc: auto, edge-width: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, drop-shadow: auto, title-xshift: auto, style: auto, ..args)
```

Environnement didactique à couleur libre : le titre (premier contenu, obligatoire) est le texte de la banderole.

Syntaxe : `#bf-env[Titre][Corps]` (titre obligatoire, comme en LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "bfEnv", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:2139.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `breakable`, `craie`, `icone`, `embleme`, `variant`, `colback`, `colframe`, `colbacktitle`, `banner-arc`, `coltitle`, `fonttitle`, `arc`, `edge-width`, `left`, `right`, `top`, `bottom`, `boxsep`, `drop-shadow`, `title-xshift`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sous-titre` | `none` | content, none | Sous-titre, dans le nœud à droite de la banderole. Défaut : `none`. LaTeX : `[sous-titre]`. |  |
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |

Exemple :

```typ
#bf-env(sous-titre: [à retenir], couleur: "meth")[Bilan][Ce qu'il faut retenir.]
```

## bfbox

```typ
bfbox(version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, breakable: auto, embleme: auto, colback: auto, colframe: auto, colbacktitle: auto, coltitle: auto, arc: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, boxrule: auto, width: auto, style: auto, ..args)
```

Forme « environnement » de `boite` (même rendu, mêmes clés tcolorbox).

Syntaxe : `#bfbox[Titre][Corps]` ou `#bfbox[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "bfbox", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:2199.

Clés communes acceptées (voir en tête) : `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `breakable`, `embleme`, `colback`, `colframe`, `colbacktitle`, `coltitle`, `arc`, `bottom`, `boxsep`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `left` | `auto` | length | Marge intérieure gauche (sans `boxsep`). Défaut : `0pt`. LaTeX : `left`. | left |
| `right` | `auto` | length | Marge intérieure droite (sans `boxsep`). Défaut : `0pt`. LaTeX : `right`. | right |
| `top` | `auto` | length | Marge intérieure haute (sans `boxsep`). Défaut : `0pt`. LaTeX : `top`. | top |
| `boxrule` | `auto` | length | Épaisseur du cadre. Défaut : `0.4pt`. LaTeX : `boxrule`. | boxrule |
| `width` | `auto` | length, ratio | Largeur de la boîte. Défaut : `100%`. LaTeX : `width`. | width |

Exemple :

```typ
#bfbox(colframe: "defi")[Bilan][Ce qu'il faut retenir.]
```

## boite

```typ
boite(version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, breakable: auto, embleme: auto, colback: auto, colframe: auto, colbacktitle: auto, coltitle: auto, arc: auto, left: auto, right: auto, top: auto, bottom: auto, boxsep: auto, boxrule: auto, width: auto, style: auto, ..args)
```

Boîte à cadre et titre en bandeau, à la couleur d'accent courante (`\boitecouleur`) : gris foncé hors environnement, couleur de l'environnement dedans.

Syntaxe : `#boite[Titre][Corps]` ou `#boite[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "boite", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : BRI:12.

LaTeX : `\boite`

Clés communes acceptées (voir en tête) : `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `breakable`, `embleme`, `colback`, `colframe`, `colbacktitle`, `coltitle`, `arc`, `bottom`, `boxsep`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `left` | `auto` | length | Marge intérieure gauche (sans `boxsep`). Défaut : `0pt`. LaTeX : `left`. | left |
| `right` | `auto` | length | Marge intérieure droite (sans `boxsep`). Défaut : `0pt`. LaTeX : `right`. | right |
| `top` | `auto` | length | Marge intérieure haute (sans `boxsep`). Défaut : `0pt`. LaTeX : `top`. | top |
| `boxrule` | `auto` | length | Épaisseur du cadre. Défaut : `0.4pt`. LaTeX : `boxrule`. | boxrule |
| `width` | `auto` | length, ratio | Largeur de la boîte. Défaut : `100%`. LaTeX : `width`. | width |

Exemple :

```typ
#boite[Bilan][Ce qu'il faut retenir.]
```

## boite-figure

```typ
boite-figure(version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, embleme: auto, colback: auto, colframe: auto, arc: auto, top: auto, boxrule: auto, halign: auto, style: auto, ..args)
```

Cadre de figure légendée : étiquette noire (premier contenu) dans l'angle supérieur gauche, contenu centré.

Syntaxe : `#boite-figure[Titre][Corps]` (titre obligatoire, comme en LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "boiteFigure", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1608.

Clés communes acceptées (voir en tête) : `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `embleme`, `colback`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `colframe` | `auto` | color, str, auto | Couleur des filets et du cadre du sous-titre. `auto` : couleur!50. Défaut : `"black!50"`. LaTeX : `colframe`. | colframe |
| `arc` | `auto` | length | Rayon des coins. Défaut : `2mm`. LaTeX : `arc`. | arc |
| `top` | `auto` | length | Marge intérieure haute (sans `boxsep`). Défaut : `7mm`. LaTeX : `top`. | top |
| `boxrule` | `auto` | length | Épaisseur du cadre. Défaut : `0.5mm`. LaTeX : `boxrule`. | boxrule |
| `halign` | `auto` | str | Alignement horizontal du contenu. Défaut : `"center"`. LaTeX : `halign`. | halign |

Exemple :

```typ
#boite-figure[Figure 1][Un schéma.]
```

## cracked

```typ
cracked(sous-titre: none, label: none, version: auto, rendu: auto, rd: auto, skin: auto, before-skip: auto, after-skip: auto, anki: auto, sommaire: auto, numero: auto, numerotation: auto, compteur: auto, nameref: auto, couleur: auto, embleme: auto, fonttitle: auto, left: auto, right: auto, top: auto, bottom: auto, drop-shadow: auto, line-width: auto, couleur-titre: auto, largeur-titre: auto, amplitude: auto, segment-length: auto, title-angle: auto, style: auto, ..args)
```

Cadre à bord déchiré et étiquette inclinée (base de `notation` et `aide`). Le titre de l'étiquette est le premier contenu (facultatif, « Propriété » par défaut). Couleur par défaut : orange.

Syntaxe : `#cracked[Titre][Corps]` ou `#cracked[Corps]` (titre facultatif : l'argument optionnel LaTeX). Toutes les clés se règlent aussi pour le document : `setbfenvironments(pour: "cracked", …)`, ou par un style nommé (`setbfenvironments(definir: "nom", …)`, clé `style`). Source LaTeX : NBE:1668.

Clés communes acceptées (voir en tête) : `label`, `version`, `rendu`, `rd`, `skin`, `before-skip`, `after-skip`, `anki`, `sommaire`, `numero`, `numerotation`, `compteur`, `nameref`, `embleme`, `fonttitle`, `left`, `right`, `top`, `bottom`, `drop-shadow`, `line-width`, `couleur-titre`, `largeur-titre`, `amplitude`, `segment-length`, `title-angle`, `style`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `sous-titre` | `none` | content, none | Sous-titre, dans le nœud en haut à droite. Défaut : `none`. LaTeX : 2e argument `[sous-titre]`. |  |
| `couleur` | `auto` | color, str, auto | Teinte de l'environnement : couleur Typst ou nom xcolor (`"thm"`, `"red!50!black"`). Par défaut, la couleur nommée de bfcours propre au type, lue au moment du rendu : `setbfcolors(thm: …)`, `definecolor` et les palettes… |  |

Exemple :

```typ
#cracked(sous-titre: [rappel])[À savoir][Un cadre à bord déchiré.]
```

## new-bfd-palette

```typ
new-bfd-palette(nom, ..couleurs)
```

Déclare une palette (`\NewBfdPalette{nom}{thm=…, defi=…}`). Les couleurs absentes gardent leur valeur au moment de l'activation. Valeurs : couleur Typst ou expression xcolor (`"blue!70!cyan"`).

LaTeX : `\NewBfdPalette`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom de la palette. |  |

Clés documentées dans le guide (`farfadet-didactique/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `couleurs` | (positionnel) | color \| str |  | Un argument nommé par couleur sémantique : `thm`, `defi`, `prop`, `demo`, `meth`, `act`, `rem`, `nota`, `ex`. Une couleur absente garde sa valeur au moment de l'activation. |

Exemple :

```typ
#new-bfd-palette("foret", thm: "olive", defi: "teal", prop: rgb("#2e7d32"))
#bfd-activate-palette("foret")
#propriete[Verte][Texte.]
```

## bfd-activate-palette

```typ
bfd-activate-palette(nom)
```

Active une palette (`\bfdActivatePalette{nom}`) : `default`, `ocean`, `vintage` ou une palette déclarée par `new-bfd-palette`. Les environnements suivants prennent ses couleurs.

LaTeX : `\bfdActivatePalette`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom de la palette. |  |

Exemple :

```typ
#bfd-activate-palette("ocean")
#theoreme[Bleu][Texte.]
#bfd-activate-palette("default")
```

## bfd-activate-variant

```typ
bfd-activate-variant(variante)
```

Choisit l'habillage des environnements à banderole (`\bfdActivateVariant{…}`) : `"lignes"` (défaut : filets gauche et bas, sous-titre centré), `"minimal"` (fin filet gauche, sans sous-titre) ou `"sidebar"` (bande pleine à gauche, sous-titre à droite). Équivaut à `setbfenvironments(variant: …)`.

LaTeX : `\bfdActivateVariant`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `variante` | (positionnel) | str | `"lignes"`, `"minimal"` ou `"sidebar"`. |  |

Exemple :

```typ
#bfd-activate-variant("sidebar")
#definition[Barre latérale][Texte.]
#bfd-activate-variant("lignes")
```

## bfset

```typ
bfset(palette: none, variant: none)
```

Interface unique de configuration de new-bfcours-environments (`\bfset{palette=…, variant=…}`).

LaTeX : `\bfset`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `palette` | `none` | str, none | palette à activer (voir `bfd-activate-palette`). Défaut : `none` (inchangée). |  |
| `variant` | `none` | str, none | variante à activer (voir `bfd-activate-variant`). Défaut : `none` (inchangée). |  |

Exemple :

```typ
#bfset(palette: "vintage", variant: "minimal")
#methode[Ton chaud][Texte.]
#bfset(palette: "default", variant: "lignes")
```

## setbfenvironments

```typ
setbfenvironments(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les environnements didactiques pour la suite du document : le setter de farfadet-didactique pour les environnements (signature commune de tous les setters de bfcours).

| Appel | Effet | |---|---| | `setbfenvironments(cle: v)` | réglage global (toutes les clés que le type connaît) | | `setbfenvironments(pour: "Definition", cle: v)` | réglage d'un type, d'un groupe ou d'un tableau de types | | `setbfenvironments(definir: "nom", cle: v)` | définit le style nommé « nom » (appel : `style: "nom"`) | | `setbfenvironments(style: "rd")` | rendu par les boîtes de `rdboites` (`"bf"`, le défaut, rend le style de bfcours) | | `setbfenvironments(pour: "anki", paquet: …)` | export Anki (clés `paquet`, `etiquettes`, `format`) | | `setbfenvironments(reinitialiser: true)` | oublie réglages global et par type (styles gardés) ; avec des clés, repart des défauts puis les applique | | `setbfenvironments(reinitialiser: "tout")` | idem, et ramène les styles aux styles prédéfinis |

Priorité : clé écrite sur l'environnement > style nommé > réglage du type > réglage global > défaut. Un type, une clé, une valeur ou un style inconnus arrêtent la compilation avec la liste des possibilités. Styles prédéfinis (styles LaTeX de bfcours) : `bf`, `rd` (rendus), `bfd theoreme`, `bfd definition`, `bfd propriete`, `bfd demonstration`, `bfd methode`, `bfd activite`, `bfd vocabulaire`, `bfd solution`, `bfd histoire`, `exempleboxstyle`, `contreexempleboxstyle`, `bfd edge overlay lignes`, `bfd edge overlay minimal`, `bfd edge overlay sidebar`.

Anki : l'export se fait hors de Typst, par l'outil `ankify` (Node ou Deno) qui lit les métadonnées du PDF ; les cartes sont déposées par la clé `anki` des environnements. `paquet` : nom du paquet de cartes (`none` : celui d'ankify), `etiquettes` : étiquettes ajoutées à toutes les cartes, `format` : `"png"`, `"svg"` ou `"plain"`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type d'environnement (nom LaTeX exact : `definition`, `exemple`, `bf-env`, `boite`…), tableau de types, ou `"anki"` ; `none` : réglage global. |  |
| `reinitialiser` | `false` | bool, str | `true`, `false` ou `"tout"`. |  |
| `definir` | `none` | str, none | nom d'un style à définir ; les clés qui suivent en forment le contenu. |  |

Clés documentées dans le guide (`farfadet-didactique/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | (positionnel) | any |  | Les clés à régler, nommées (voir la fiche de chaque environnement) ; `style: "rd"` choisit le style de rendu. |

Variante `setbfenvironments(pour: "anki")` : Règle l'export Anki.
- `paquet` (défaut `none`) : Nom du paquet Anki ; `none` : le paquet par défaut d'ankify.
- `etiquettes` (défaut `()`) : Étiquettes ajoutées à toutes les cartes.
- `format` (défaut `none`), valeurs `png`, `svg`, `plain`, `none` : Format des cartes.
- `reinitialiser` (défaut `false`) : Repart des défauts.

Exemple :

```typ
#setbfenvironments(sommaire: false)
#setbfenvironments(pour: "Definition", numero: true, couleur: "teal")
#setbfenvironments(definir: "sobre", drop-shadow: false, variant: "minimal")
#propriete(style: "sobre")[Sobre][Texte.]
#setbfenvironments(pour: "anki", paquet: "Maths - 2nde", etiquettes: ("vecteurs",))
```

## bfskin

```typ
bfskin(base, ..options)
```

Variante d'un skin : un skin (fonction `d => contenu`) dont certaines options sont figées.

`base` est le nom d'un skin intégré (`"cahier"`, `"outil"`, `"pastille"`, `"manchette"`, `"filet"`, `"suspendu"`, `"minimal"`) ou enregistré par `setbfskins`, ou une fonction skin. Les options données ici sont les valeurs par défaut de la variante ; celles de la clé `skin:` de l'appel (ou d'un réglage) l'emportent. La variante s'emploie directement (`rendu: bfskin(…)`) ou s'enregistre sous un nom (`setbfskins`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `base` | (positionnel) | str, function | skin de départ, par son nom ou sa fonction. |  |

Clés documentées dans le guide (`farfadet-didactique/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `options` | (positionnel) | any |  | Les options figées, en arguments nommés (`icone: "cle"`, `epaisseur: 2pt`…). Ce sont celles du skin de base. |

Exemple :

```typ
#setbfskins(cle-rouge: bfskin("suspendu", icone: "cle", epaisseur: 1.6pt))
#setbfenvironments(pour: "Theoreme", rendu: "cle-rouge")
#definition(rendu: bfskin("manchette", icone: "fanion"))[Vecteur][Direction, sens et norme.]
```

## setbfskins

```typ
setbfskins(reinitialiser: false, ..skins)
```

Enregistre des skins sous un nom, pour la suite du document : `rendu: "<nom>"` les appelle ensuite partout où la clé `rendu` est acceptée (sur l'environnement, `setbfenvironments(pour: …, rendu: …)`, `setbfenvironments(rendu: …)`, style nommé). Un nom déjà enregistré est remplacé.

Un skin est une fonction `d => contenu` : elle reçoit un dictionnaire résolu (`type`, `nom`, `numero`, `titre`, `corps`, `couleur`, `fond`, `cadre`, `couleur-titre`, `icone`, `breakable`, `avant`, `apres`, `options`, `auteur`, `explicites`, `r`) et dessine la boîte. Elle ne gère ni la numérotation, ni l'étiquette, ni le sommaire, ni Anki, ni la version prof/élève. Contrat complet : `skins/CONTRAT.md`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `reinitialiser` | `false` | bool | `true` oublie d'abord tous les skins enregistrés. |  |

Clés documentées dans le guide (`farfadet-didactique/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `skins` | (positionnel) | function |  | Un argument nommé par skin ou par variante : `nom: fonction`. |

Exemple :

```typ
#let filet(d) = block(stroke: (left: 2pt + d.couleur), inset: (left: 8pt, y: 4pt), breakable: d.breakable)[
  #smallcaps(d.nom)#if d.numero != none [ #d.numero]#if d.titre != none [ — #d.titre] \ #d.corps
]
#setbfskins(filet: filet)
#definition(rendu: "filet")[Vecteur][Direction, sens et norme.]
```

## coloredsquare

```typ
coloredsquare(couleur, taille: 3)
```

Carré plein de 3 ex de côté (`\coloredsquare{couleur}`).

LaTeX : `\coloredsquare`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | la couleur. |  |
| `taille` | `3` | int, float | côté en ex. Défaut : `3`. |  |

Exemple :

```typ
Légende : #coloredsquare("thm") théorèmes, #coloredsquare(teal) autre.
```

## dimcoloredsquare

```typ
dimcoloredsquare(couleur, taille)
```

Carré plein de côté choisi en ex (`\dimcoloredsquare{couleur}{taille}`).

LaTeX : `\dimcoloredsquare`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `couleur` | (positionnel) | color, str | la couleur. |  |
| `taille` | (positionnel) | int, float | côté en ex. |  |

Exemple :

```typ
#dimcoloredsquare("prop", 2) #dimcoloredsquare("prop", 4)
```

## liencontent

```typ
liencontent(categorie, titre)
```

Affiche une catégorie en gras et dépose une entrée au sommaire « **catégorie** - titre » (`\liencontent{catégorie}{titre}`, avec la mise au sommaire de `\bfdLiencontentRegister`).

LaTeX : `\liencontent`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `categorie` | (positionnel) | content | catégorie, affichée en gras. |  |
| `titre` | (positionnel) | content, none | titre de l'entrée. |  |

Exemple :

```typ
#liencontent[Définition][Vecteur nul]
```

## setbfsections

```typ
setbfsections(pour: none, reinitialiser: false, definir: none, ..cles)
```

Règle les titres (`=`, `==`, `===`, `====`) pour la suite du document : le setter de farfadet-didactique pour le sectionnement (signature commune de tous les setters de bfcours). Ajout : en LaTeX on redéfinit les styles `SectionBox` et `SubSectionBox` par `\tcbset`.

**Jeux de titres.** Cinq jeux prédéfinis, choisis par la clé `jeu` (ou par la clé `titres:` du modèle `farfadet`) :

| Jeu | Rendu | |---|---| | `"bfcours"` (défaut) | bandeau gris-noir arrondi pour `=` (`SectionBox`), cadre ouvert à numéro pour `==` (`SubSectionBox`), niveau 3 gras numéroté, niveau 4 gras non numéroté | | `"sobre"` | numéro coloré et filet fin sous les niveaux 1 et 2, sans grande taille (fiches, activités) | | `"classique"` | titres gras d'article, sans bandeau ni filet (documents denses, copies) | | `"documentation"` | rendu de bfdoc : gros numéro coloré, filet pâle sous le niveau 1 | | `"rd"` | niveau 1 en badge « ■ Titre » de rdboites (`rd.partieDNB`), niveau 2 en gras précédé d'un carré, niveaux 3 et 4 en gras compact |

**Clés communes à tous les jeux** (réglage global, ou d'un niveau par `pour: "SectionBox"` pour le niveau 1 et `pour: "SubSectionBox"` pour le niveau 2) : `couleur` (couleur du bandeau, du numéro ou du filet ; défaut : une couleur nommée de bfcours propre au jeu, lue au rendu), `hauteur` (hauteur du bandeau, ou hauteur minimale de la zone du titre), `numerotation` (`false` : titres sans numéro), `coltitle`, `fonttitle`, `before-skip`, `after-skip`. Clés de `SectionBox` : `left` (3mm), `arc` (1mm) ; de `SubSectionBox` : `lefthand-width` (1cm), `sidebyside-gap` (5mm), `left-skip` (1cm), `right` (20pt), `line-width` (2pt), `arc` (10pt), `width-extra` (3cm, ajout de `\calcwidth`), `width-max` (80 %). La couleur de base du jeu `bfcours` se règle aussi comme en LaTeX : `setbfcolors(BaseColor: …)`.

**Style de numérotation** : la clé `numeros` (réglage global, valable pour tout le document : à placer avant le premier titre) vaut pour les cinq jeux, la table des matières, les renvois et le numéro des environnements.

| `numeros` | Niveau 1 | Niveau 2 | Niveau 3 | |---|---|---|---| | `"arabe"` (défaut) | 1, 2… | 1.1, 1.2… | 1.1.1… | | `"romain"` | I, II… | 1., 2.… | a), b)… | | `"lettres"` | A, B… | 1., 2.… | a), b)… |

Un tableau de motifs Typst, un par niveau, règle chaque niveau : `numeros: ("I", "A.", "i)")` (chaque motif s'applique au seul compteur de son niveau). Les renvois (`@étiquette`) affichent le chemin complet (« II.1 », « II.1.a »).

| Appel | Effet | |---|---| | `setbfsections(jeu: "sobre")` | change de jeu de titres | | `setbfsections(numeros: "romain")` | numérote les sections en chiffres romains (ou `"lettres"`) | | `setbfsections(cle: v)` | réglage global (les deux niveaux de bandeau) | | `setbfsections(pour: "SectionBox", cle: v)` | réglage du niveau 1 (ou `"SubSectionBox"`, niveau 2) | | `setbfsections(definir: "nom", cle: v)` | définit un style nommé (appel : `style: "nom"`) | | `setbfsections(reinitialiser: true)` | retour aux défauts (jeu `bfcours`) ; styles gardés | | `setbfsections(reinitialiser: "tout")` | idem, et oublie les styles |

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | `"SectionBox"`, `"SubSectionBox"`, un tableau des deux ; `none` : les deux niveaux. |  |
| `reinitialiser` | `false` | bool, str | `true`, `false` ou `"tout"`. |  |
| `definir` | `none` | str, none | nom d'un style à définir. |  |

Exemple :

```typ
#setbfsections(numeros: "romain")
```

Autre exemple :

```typ
#setbfsections(pour: "SectionBox", couleur: "prop!70!black", hauteur: 1cm)
#setbfsections(couleur: "defi")
#setbfsections(jeu: "sobre", numerotation: false)
#setbfsections(reinitialiser: true)
```

## tableofcontents

```typ
tableofcontents(titre: [Table des matières], colonnes: 2, profondeur: 2)
```

Table des matières sur plusieurs colonnes (`\tableofcontents` de bfcours) : titres de section et de sous-section, et environnements didactiques titrés (« **Définition** - sous-titre »).

LaTeX : `\tableofcontents`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `titre` | `[Table des matières]` | content | titre de la table (LaTeX : `\contentsname`). Défaut : `[Table des matières]`. |  |
| `colonnes` | `2` | int | nombre de colonnes (LaTeX : `multicols{2}`). Défaut : `2`. |  |
| `profondeur` | `2` | int | niveau de titre le plus profond retenu (LaTeX : `tocdepth`). Défaut : `2`. |  |

Exemple :

```typ
#tableofcontents(titre: [Sommaire], colonnes: 2)
```

## printvocindex

```typ
printvocindex(colonnes: 3, titre: [Vocabulaire utilisé], colframe: auto, colback: auto, coltitle: white)
```

Boîte « Vocabulaire utilisé » (`\printvocindex`) : tous les mots passés à `voc`, en gras, avec leur page (lien cliquable). À placer en fin de chapitre.

LaTeX : `\printvocindex`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `colonnes` | `3` | int | nombre de colonnes (ajout ; LaTeX : `\badprintvocindex[colonnes=3]`). Défaut : `3`. |  |
| `titre` | `[Vocabulaire utilisé]` | content | titre de la boîte. Défaut : `[Vocabulaire utilisé]`. |  |
| `colframe` | `auto` | color, str, auto | cadre et bandeau de titre. `auto` : blue!50!black. |  |
| `colback` | `auto` | color, str, auto | fond. `auto` : gray!10 (gray!5 si la liste est vide). |  |
| `coltitle` | `white` | color, str | texte du titre. Défaut : `white`. |  |

Exemple :

```typ
#printvocindex(colonnes: 2)
```

## tableau-vocabulaire-sommaire

```typ
tableau-vocabulaire-sommaire(..mots)
```

Tableau de révision du vocabulaire (`\tableauVocabulaireSommaire`) : une ligne par mot (le mot est précédé d'un crayon), colonnes « Vu en classe le », « Définition apprise le », « Prêt ». (Les lignes `\vocabulaireSommaire{mot}` de LaTeX deviennent simplement les mots.)

LaTeX : `\tableauVocabulaireSommaire`

Clés documentées dans le guide (`farfadet-didactique/docs/guide.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `mots` | (positionnel) | content |  | Un contenu par mot de vocabulaire. |

Exemple :

```typ
#tableau-vocabulaire-sommaire[hypoténuse][cathète]
```

## voc

```typ
voc(mot)
```

Mot de vocabulaire (`\voc{mot}`) : en gras, à la couleur d'accent courante, et noté pour l'index du vocabulaire (`printvocindex`). Seule la première occurrence d'un même mot compte.

LaTeX : `\voc`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mot` | (positionnel) | content, str | le mot défini. |  |

Exemple :

```typ
On appelle #voc[hypoténuse] le côté opposé à l'angle droit.
```

## vocref

```typ
vocref(cible, mot)
```

Mot en gras rose (la couleur nommée `monrose`, lue au rendu : `setbfcolors(monrose: …)`), lien vers une adresse (`\vocref{url}{mot}`). En LaTeX le mot va aussi à l'index de makeidx, que bfcours n'imprime pas : ce dépôt n'est pas porté. (`\vocnoindexref`, identique en Typst, n'existe plus.)

LaTeX : `\vocref`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `cible` | (positionnel) | str, label, location | adresse ou étiquette du lien. |  |
| `mot` | (positionnel) | content | le mot. |  |

Exemple :

```typ
#vocref("https://fr.wikipedia.org/wiki/Hypoténuse")[hypoténuse]
```
