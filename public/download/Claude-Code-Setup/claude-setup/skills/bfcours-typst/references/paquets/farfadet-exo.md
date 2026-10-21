# farfadet-exo

Fiche générée par `scripts/regenerer.py` le 21/10/2026 depuis l'index des fonctions et les guides des paquets. **Ne pas éditer à la main.**

- Import : `#import "@preview/farfadet:0.2.0": *` (toute la suite) ou, pour cette partie seule, `#import "@preview/farfadet:0.2.0": exercices` puis `#import exercices: *`.
- Réglage : `setrdexo` (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).
- Guide complet : `docs/farfadet-exo.pdf` du dépôt (sources : `docs/guide.typ` du paquet `farfadet-exo`).

## Sommaire

- `exo` — Exercice de bfcours (`\begin{EXO}{titre}{tags}`) et environnement `exo` de rdexo (fusionnés) : en-tête « ■ Exercice n – titre » avec étoile…
- `exo-eval` — Exercice d'évaluation (`\begin{EXOEVAL}{titre}{compétence}`) : EXO dont l'en-tête porte la grille d'auto-évaluation MI / MF / MS / TBM ; se…
- `setrdexo` — L'unique réglage du paquet : exercices, thèmes, étoiles, boîtes de points, tableaux de compétences, cartouches d'évaluation, sujets d'exame…
- `rdexo-skin` — Déclare un thème (\rdexoSkin{nom}{en-tête tcbox}{en-tête tcolorbox}). Les en-têtes sont des fonctions qui reçoivent un dictionnaire `info` …
- `rdexostars` — Étoiles de niveau (\rdexostars[options]{niveau}{total}) ; un niveau décimal remplit une étoile en partie. Les défauts se règlent par `setrd…
- `rdexocorrection` — Rejoue les corrections (\rdexocorrection[options]{liste}) sous un en-tête de solution, avec des liens cliquables vers les énoncés. Le style…
- `exocorrection` — Marqueur `#exocorrection` (le `\exocorrection` de LaTeX) : dans le corps d'un `exo` ou `exo-eval`, ce qui le suit est la correction de l'ex…
- `tcblower` — Marqueur facultatif `#tcblower` : dans le corps d'un `exo` ou `exo-eval`, ce qui le suit est la partie basse de l'exercice (zone de réponse…
- `rdexofilter` — N'affiche que les exercices dont les étiquettes satisfont l'expression (\rdexofilter) : opérateurs `!` (non), `&` (et), `\|` (ou), parenthè…
- `rdexoresetfilter` — Supprime le filtre d'étiquettes (\rdexoresetfilter).
- `rdexohlist` — Liste horizontale (\rdexohlist[options]{liste}).
- `rdexotikzlist` — Liste en matrice qui choisit son nombre de colonnes selon la largeur (\rdexotikzlist).
- `rdexocountlist` — Nombre d'éléments d'une liste (\rdexocountlist).
- `thenumexo` — Numéro de l'exercice en cours (\thenumexo[*][avant][après]) ; `etoile` : seulement si `display-numexo`.
- `rdexonumexo` — Valeur du compteur d'exercices (\rdexonumexo = `\value{rdexo@numexo}`) ; `f` reçoit l'entier, pour calculer avec.
- `thescore` — Score de l'exercice en cours (\thescore[*][avant][après]), à la française.
- `thescore-libelle` — Score avec son libellé (\theScore[*][avant][après]) : « 2,5 points ».
- `rdexoscore` — Valeur brute du score de l'exercice en cours (\rdexoscore).
- `thelevel` — Niveau (nombre d'étoiles) de l'exercice en cours (\thelevel).
- `theexotitle` — Titre de l'exercice en cours (\theexotitle[*][avant][après]).
- `theexotitle-style` — Titre dans sa police et sa couleur (\theExotitle[*][avant][après]).
- `rdexotitlefont` — Applique au texte la police des titres d'exercice (\rdexotitlefont) : celle de l'exercice en cours, sinon celle du réglage `exotitle-font`.
- `thetags` — Étiquettes de l'exercice en cours, au style du thème (\thetags[*][max cols]).
- `thelabel` — Libellé des exercices (\thelabel) : « Exercice ».
- `rdexotags` — Étiquettes de l'exercice en cours, séparées par des virgules (\rdexotags).
- `tf-numexo` — `oui` si le numéro de l'exercice en cours est affiché, `non` sinon (\TFNumexo{oui}{non}).
- `tf-score` — `oui` si le score de l'exercice en cours est affiché, `non` sinon (\TFScore{oui}{non}).
- `tf-level` — `oui` si le niveau de l'exercice en cours est affiché, `non` sinon (\TFLevel{oui}{non}).
- `tf-title` — `oui` si le titre de l'exercice en cours est affiché, `non` sinon (\TFTitle{oui}{non}).
- `tf-tags` — `oui` si les étiquettes de l'exercice en cours sont affichées (`display-tags`), `non` sinon (\TFTags{oui}{non}).
- `rdexo-enonce-label` — Texte cliquable vers la solution de l'exercice n (\rdexoEnonceLabel{n}{texte}).
- `rdexo-solution-label` — Texte cliquable vers l'énoncé de l'exercice n (\rdexoSolutionLabel{n}{texte}).
- `rdifficulty` — Niveau par défaut des exercices suivants (\def\rdifficulty{n}) ; équivaut à `setrdexo(level: n)`.
- `rdexo-mod` — Modulo (\rdexoMod{a}{b}) : `a - b ⌊a / b⌋`.
- `rdexoinclude` — Inclut un exercice rangé dans un fichier (\rdexoinclude[*][options]{fichier}). Le fichier est lu par le document (`include "fichier.typ"`) …
- `itempoint` — Points d'un item (\tcbitempoint{points}[décalage v][décalage h] et \itempoint, fusionnés) : ajoute des points au barème et, si `displayitem…
- `infotcbitempoint` — Points « informatique » (\infotcbitempoint) : boîte verte avec icône d'ordinateur, totaux séparés (`getinfoexopoint`, `getsavedinfototalpoi…
- `displayitempoints` — Affiche ou masque les boîtes de points (\displayitempointstrue / \displayitempointsfalse).
- `baremepoint` — Boîte rouge « n pts » au-dessus d'un contenu (\baremepoint{contenu}{points}), si `displaybaremepoints(true)` ; n'entre dans aucun total.
- `displaybaremepoints` — Affiche ou masque les boîtes de `baremepoint` (\displaybaremepointstrue / false).
- `getinfoexopoint` — Points « informatique » de l'exercice n (\getinfoexopoint{n}).
- `getsavedtotalpoints` — Total des points du document (\getsavedtotalpoints), suivi d'un \phantom{A}.
- `getsavedinfototalpoints` — Total des points « informatique » du document (\getsavedinfototalpoints).
- `competence` — Ligne d'un tableau de compétences (\competence[code]{texte}) : puce, intitulé, code encadré à droite.
- `tableaucompetence` — Tableau « Compétences travaillées » (\tableaucompetence) : une ligne par compétence et quatre colonnes d'auto-évaluation MI, MF, MS, TBM. L…
- `tableaucompetence-eval` — Tableau « Compétences évaluées » (\tableaucompetenceEval).
- `printcompindex` — Index des compétences du document (\printcompindex) : un tableau « Compétences évaluées » dont les lignes sont les compétences inscrites pa…
- `tableau-eval` — Cartouche d'évaluation (\tableauEval{durée}) : « Nom / Prénom » sur 3/4, « Durée » et chronomètre sur 1/4.
- `tableau-projet-eval` — Cartouche de projet (\tableauProjetEval{date}) : case de droite « Date de rendu : ».
- `tableau-presente-eval-sixieme` — Cartouche de sixième (\tableauPresenteEvalSixieme{…}{note max}) : « Nom / Prénom » et « Bilan : ▢ / note ▢ ».
- `chrono` — Chronomètre encadré « Durée : » (\chrono{minutes}).
- `overlaychrono` — Cadran en surimpression (\overlaychrono{minutes}) : secteur jusqu'aux minutes, puis « minutes’ ».
- `mi` — Niveau de maîtrise « Maîtrise insuffisante » (\mi) : émoji, ou « MI » si `setrdexo(emoji: false)`.
- `mf` — « Maîtrise fragile » (\mf).
- `ms` — « Maîtrise satisfaisante » (\ms).
- `tbm` — « Très bonne maîtrise » (\tbm).
- `chapitre-bac` — Sujet de baccalauréat (\chapitreBac[clés]) : police sans empattement, pied de page officiel (code du sujet, « Page : n/N » du sujet seul), …
- `chapitre-brevet` — Sujet du DNB (\chapitreBrevet[clés] = \chapitreBac[style=brevet, …]).
- `style-exo-bac` — Active le skin « exobac » (\styleExoBac[clés rdexo]) : « Exercice n » souligné, « (5 points) » en gras.
- `style-exo-brevet` — Active le skin « exobrevet » (\styleExoBrevet[clés rdexo]) : « Exercice n : titre (X points) » en gras.
- `style-questions-bac` — Partie « Questions » (\styleQuestionsBac[*][clés]) : items « Question n » sans barème ni titre, numérotés à partir de 1 (`etoile: true` : l…
- `style-exercices-bac` — Partie « Exercices » (\styleExercicesBac[*][clés]) : « Exercice n (X points) », titre affiché.
- `numeroter-bac` — Le prochain exercice portera le numéro n + 1 (\numeroterBac[n]).
- `partie-bac` — Titre de partie centré et gras (\partieBac[*]{titre}) ; sans étoile, entrée de sommaire.
- `consigne-bac` — Cadre de consignes en gras italique centré (\consigneBac[*]{texte}) ; `etoile` : gras au fil du texte.
- `encadre-bac` — Petit cadre pleine largeur (\encadreBac[titre]{contenu}).
- `encadre-bac-etroit` — Même cadre, à la largeur du contenu (\encadreBacEtroit[titre]{contenu}).
- `corrige-bac` — Clôt le sujet et ouvre le corrigé, à pagination séparée (\corrigeBac[*][titre=CORRIGÉ]) ; rejoue toutes les corrections, sauf avec `etoile:…
- `bfexobac-uline` — Souligne exactement la largeur du texte (\bfexobacUline{texte}).
- `exolombards` — Charge l'habillage « exolombards » (\usepackage[options]{bfcours-exolombards-skin}, ajout) : règle les options, active le skin (`auto`) et …
- `style-exo-lombards` — Active le skin « exolombards » (\styleExoLombards[clés rdexo]) : « [Exercice n] » encadré en ligne.
- `corrections-lombards` — Change le mode des corrections (\correctionsLombards{auto\|suite\|separee}).
- `corrige-lombards` — Corrigé n à la manière du document de correction d'origine (\corrigeLombards[réf.]{n}), ou « Pas de corrigé disponible pour cet exercice. ».
- `exolombards-etiquette` — Étiquette encadrée en gras (\exolombardsEtiquette{texte}).
- `exolombards-titre` — Titre discret en italique (\exolombardsTitre{titre}).
- `exolombards-bareme` — Barème entre parenthèses (\exolombardsBareme{points}).
- `exolombards-mot-correction` — Mot placé devant une correction (\exolombardsMotCorrection) : « Correction : ».

## Clés communes

Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = réglage du setter, sinon défaut du paquet).

| Clé | Rôle | Option LaTeX | Fonctions |
|---|---|---|---|
| `avant` |  |  | 5 : `thenumexo`, `thescore`, `thescore-libelle`, `theexotitle`, `theexotitle-style` |
| `apres` |  |  | 5 : `thenumexo`, `thescore`, `thescore-libelle`, `theexotitle`, `theexotitle-style` |
| `etoile` |  |  | 9 : `thescore`, `thescore-libelle`, `theexotitle`, `theexotitle-style`, `style-questions-bac`, `style-exercices-bac`, `partie-bac`, `consigne-bac` … |
| `titre` |  |  | 3 : `encadre-bac`, `encadre-bac-etroit`, `corrige-bac` |

## exo

```typ
exo(..args)
```

Exercice de bfcours (`\begin{EXO}{titre}{tags}`) et environnement `exo` de rdexo (fusionnés) : en-tête « ■ Exercice n – titre » avec étoiles de niveau et case de score, puis l'énoncé. Le titre entre dans l'index des compétences (`printcompindex`) et dans le sommaire. Le corps se coupe aux marqueurs `#tcblower` (ce qui suit est la partie basse, dans la boîte) et `#exocorrection` (ce qui suit est la correction, qui n'est pas affichée ici : `rdexocorrection` la rejoue plus loin, avec des liens cliquables dans les deux sens).

Toutes les clés de `setrdexo` s'emploient localement ; la clé locale l'emporte sur un style nommé, lui-même sur le réglage du type (`setrdexo(pour: "EXO", …)`), puis sur le réglage global. Les clés de couleur d'un thème (`bg-color`, `score-bg-color`…) s'emploient aussi localement, pour ce seul exercice.

LaTeX : `\EXO`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-exercices.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `tags` | `()` | str \| array |  | Étiquettes de l'exercice : « a, b » ou un tableau. Affichées selon `display-tags` ; filtrées par `rdexofilter`. |
| `level` | `auto` | int \| float \| auto |  | Niveau de 0 à 3, demi-étoiles permises. `auto` : le dernier `rdifficulty` (1 au départ). `none` : pas de niveau du tout. |
| `score` | `auto` | int \| float \| auto |  | Barème. `auto` : la somme des `itempoint` de l'énoncé. |
| `competence` | `auto` | content \| str \| auto |  | Entrée de l'exercice dans l'index des compétences. `auto` : le titre. |
| `skin` | `"bouyachakka"` | str | `bouyachakka`, `default`, `pooja`, `rikid`, `griba`, `exobac`, `exobrevet`, `exolombards` | Thème de l'en-tête. |
| `exo-header` | `"tcolorbox"` | str | `tcolorbox`, `tcbox`, `none` | Forme de l'en-tête. |
| `style` | `auto` | str \| array |  | Style(s) nommé(s) défini(s) par `setrdexo(definir: …)`. |
| `args` | (positionnel) | content |  | Le titre (facultatif), puis les étiquettes (facultatives), puis le corps : l'énoncé, éventuellement suivi de `#tcblower` et de la partie basse, de `#exocorrection` et de la correction. |

Variante `exo(exotitle: …)` : Un exercice dont le titre est une clé. Toutes les clés de `setrdexo` s'emploient comme options.
- `exotitle` (défaut `none`) : Titre de l'exercice.
- `numexo` (défaut `auto`) : Numéro de CET exercice ; les suivants continuent à partir de lui.
- `level` (défaut `auto`) : Niveau de 0 à 3.
- `score` (défaut `auto`) : Barème.
- `tags` (défaut `()`) : Étiquettes.
- `corps` : Le corps : l'énoncé et, après les marqueurs `#tcblower` et `#exocorrection`, la partie basse et la correction (un seul positionnel).

Exemple :

```typ
#exo(tags: "équations", level: 2)[Une équation][
  #itempoint(2)[Résoudre $2 x + 1 = 7$.]
  #exocorrection
  $2 x = 6$, donc $x = 3$.
]
```

## exo-eval

```typ
exo-eval(..args)
```

Exercice d'évaluation (`\begin{EXOEVAL}{titre}{compétence}`) : EXO dont l'en-tête porte la grille d'auto-évaluation MI / MF / MS / TBM ; ses étiquettes (`tags`) entrent dans l'index des compétences.

LaTeX : `\EXOEVAL`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-exercices.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `tags` | `()` | str \| array |  | Compétence(s) évaluée(s), inscrite(s) dans `printcompindex`. |
| `level` | `auto` | int \| float \| auto |  | Niveau de 0 à 3. |
| `score` | `auto` | int \| float \| auto |  | Barème. |
| `competence` | `auto` | content \| str \| auto |  | Entrée de l'index. `auto` : les étiquettes. |
| `args` | (positionnel) | content |  | Le titre (facultatif), puis le corps : l'énoncé, `#tcblower` et la partie basse, `#exocorrection` et la correction (les deux marqueurs sont facultatifs). |

Exemple :

```typ
#exo-eval(tags: "Résoudre une équation")[Équations][
  #itempoint(1.5)[Résoudre $2 x + 1 = 7$.]
  #exocorrection
  $2 x = 6$, donc $x = 3$.
]
```

## setrdexo

```typ
setrdexo(pour: none, reinitialiser: false, definir: none, ..cles)
```

L'unique réglage du paquet : exercices, thèmes, étoiles, boîtes de points, tableaux de compétences, cartouches d'évaluation, sujets d'examen.

- Sans `pour` : réglage global des exercices (clés ci-dessous). - `pour: "EXO"` ou `"EXOEVAL"` : réglage de ce seul type d'exercice. - `pour: "<thème>"` (`"default"`, `"pooja"`, `"rikid"`, `"griba"`, `"objiva"`, `"bouyachakka"`, `"exobac"`, `"exobrevet"`) : couleurs et cotes du thème : `bg-color`, `fg-color`, `frame-color`, `star-fg-color`, `star-bg-color`, `star-line-color`, `score-fg-color`, `score-bg-color`, `lower-bg-color`, `tags-bg-color`, `tags-fg-color`, `title-color`, `label-color` (objiva), `rule-color` et `correction-fg-color` (exobac), `square-color` (carré devant « Exercice n » ; `auto` : couleur du texte du bandeau), `arc`, `righthand-width`. - `pour: "rdexostars"` : étoiles : `star-color`, `star-background`, `line-color`, `line-width`, `raise`, `scale`, `show-bg`, `display-mode`, `background`, `background-app`. - `pour: "itempoint"`, `"itempoint"`, `"infotcbitempoint"`, `"baremepoint"` : boîtes de points ; `"competences"`, `"tableauEval"`, `"tableauProjetEval"`, `"tableauPresenteEvalSixieme"`, `"overlaychrono"`, `"chrono"` : tableaux et cartouches ; `"bfexobacUline"`, `"chapitreBac"` : sujets d'examen. - `pour: "exolombards"` : options de l'habillage exolombards (`pied`, `auteur`, `etablissement`, `decalage`, `correction`, `etiquette`, `titre`, `bareme`, `mot-correction`). - `definir: "nom"` : définit un style nommé, appelé ensuite par `style: "nom"`. - `reinitialiser: true` : oublie les réglages (tous, ou ceux de `pour`) ; `"tout"` : et les styles nommés.

Actions immédiates : `numexo: n` met le compteur à n (le prochain exercice porte le numéro n + 1) ; `correction-style` range des styles de boîte de correction par numéro d'exercice (une seule fois).

LaTeX : `\setrdexo`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `pour` | `none` | str, array, none | type réglé (voir plus haut) ou none (global). |  |
| `reinitialiser` | `false` | bool, str | true, false ou "tout". |  |
| `definir` | `none` | str, none | nom du style défini. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-personnaliser.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `skin` | `"bouyachakka"` | str |  | Thème : un des neuf thèmes, ou un thème déclaré par `rdexo-skin`. |
| `exo-header` | `"tcolorbox"` | str | `tcolorbox`, `tcbox`, `none` | Forme de l'en-tête. |
| `header-skip` | `6pt` | length |  | Espace sous l'en-tête. |
| `label` | `"Exercice"` | str \| content |  | Libellé devant le numéro. |
| `display-numexo` | `true` | bool |  | Numéro affiché. |
| `numexo` | `auto` | int |  | Valeur du compteur (action immédiate) : le prochain exercice porte le numéro `n + 1`. |
| `display-score` | `true` | bool |  | Score affiché. |
| `score` | `auto` | int \| float \| auto |  | Barème par défaut. |
| `display-zero-score` | `false` | bool |  | Un score nul s'affiche-t-il (« / 0 ») ? (ajout) |
| `score-label` | `("point", "points")` | array |  | Libellés du score : (singulier, pluriel). |
| `display-level` | `true` | bool |  | Étoiles affichées. |
| `level` | `auto` | int \| float \| auto |  | Niveau par défaut. `auto` : `rdifficulty`. `none` : pas de niveau. |
| `display-exotitle` | `true` | bool |  | Titre affiché. |
| `exotitle-color` | `black` | color \| str |  | Couleur du titre. |
| `exotitle-font` | `"\sffamily\bfseries\footnotesize"` | str \| dictionary |  | Police du titre : une police LaTeX (`"\sffamily\bfseries\small"`) ou un dictionnaire (`font`, `weight`, `style`, `size`). |
| `display-lower` | `auto` | auto \| bool |  | Boîte basse : `auto` (si contenu), `true`, `false`. |
| `lower` | `(:)` | dictionary |  | Position, largeur, habillage de la boîte basse (voir le chapitre « Les exercices »). |
| `save-lower` | `false` | bool |  | Accepté, sans effet (comme dans `rdexo.sty`). |
| `display-tags` | `"correction"` | bool \| str | `true`, `false`, `correction` | Affichage des étiquettes. |
| `tags-wrap` | `50%` | ratio \| none |  | Part de la ligne que les étiquettes (sous le bandeau) peuvent occuper pour que l'énoncé commence sur leur ligne, à leur gauche ; `none` : elles gardent toujours leur ligne. |
| `tags` | `()` | str \| array |  | Étiquettes par défaut. |
| `correction-as-lower` | `false` | bool |  | La correction devient la boîte basse. |
| `cadre` | `auto` | auto \| none \| function |  | Cadre autour de l'exercice entier : `auto` (celui du thème, aucun pour les thèmes intégrés), `none` (aucun) ou une fonction `(info, contenu) => contenu` (voir « Encadrer l'exercice »). |
| `cadre-correction` | `auto` | auto \| none \| function |  | Idem pour chaque bloc de correction rejoué par `rdexocorrection`. |
| `breakable` | `true` | bool |  | Exercice sécable d'une page à l'autre. |
| `after-skip` | `10pt` | length |  | Espace après l'exercice. |
| `sommaire` | `true` | bool |  | `exo` entre au sommaire (ajout). |
| `exo` | `(:)` | dictionary |  | Styles par numéro : `("3": (display-score: false))`. |
| `emoji` | `true` | bool \| str |  | Niveaux de maîtrise `mi`, `mf`, `ms`, `tbm` en émojis (`true`, `"images"`) ou en texte gras (`false`). |
| `correction-style` | `(:)` | dictionary |  | Styles de boîte de correction par numéro, pour le prochain `rdexocorrection` (voir « Corrections, filtre et macros »). |
| `correction` | `(:)` | dictionary |  | Défauts de `rdexocorrection` : `columns`, `raster`, `mirror`, `mirror-style`, `reset-num-start`. |
| `style` | `auto` | str \| array |  | Style(s) nommé(s) appliqué(s) à ce niveau de réglage. |

Variante `setrdexo(definir: …)` : Définit un style nommé d'exercice.
- `definir` (défaut `none`) : Nom du style défini.
- `pour` (défaut `none`) : Type réservé (`"EXO"`, `"EXOEVAL"`) ou `none`.
- `cles` (défaut `(:)`) : Toutes les clés de `setrdexo`, dont `style` pour hériter.

Variante `setrdexo(pour: objet)` : Règle les valeurs propres à une boîte, un tableau ou un sujet.
- `pour` (défaut `none`), valeurs `itempoint`, `infotcbitempoint`, `baremepoint`, `competences`, `tableauEval`, `tableauProjetEval`, `tableauPresenteEvalSixieme`, `overlaychrono`, `chrono`, `bfexobacUline`, `chapitreBac` : Objet réglé. Un objet inconnu arrête la compilation, avec la liste des objets possibles.
- `reinitialiser` (défaut `false`) : Repart des défauts de l'objet.
- `cles` (défaut `(:)`) : Les clés de l'objet (voir la fiche de chaque fonction).

Variante `setrdexo(pour: "exolombards")` : Règle les options de l'habillage.
- `reinitialiser` (défaut `false`) : Repart des défauts (y compris auteur et établissement).
- `etiquette` (défaut `auto`) : Présentation de l'étiquette : `texte => contenu`.
- `titre` (défaut `auto`) : Présentation du titre : `titre => contenu`.
- `bareme` (défaut `auto`) : Présentation du barème : `points => contenu`.
- `mot-correction` (défaut `[Correction :]`) : Mot placé devant une correction.
- `cles` (défaut `(:)`) : Les clés de `exolombards` : `auteur`, `etablissement`, `decalage`, `correction`.

Variante `setrdexo(pour: thème)` : Règle les couleurs d'un thème. Une clé inconnue, ou une valeur invalide, arrête la compilation avec la liste des possibilités.
- `pour` : Le thème réglé : l'un des neuf thèmes, ou un thème déclaré par `rdexo-skin`.
- `reinitialiser` (défaut `false`) : Rend au thème ses couleurs d'origine.
- `label-color` (défaut `selon le thème`) : Texte de l'étiquette « Exercice n » (`objiva`).
- `bg-color` (défaut `selon le thème`) : Fond de l'en-tête.
- `fg-color` (défaut `selon le thème`) : Texte de l'en-tête.
- `square-color` (défaut `auto`) : Carré ■ devant « Exercice n » ; `auto` : la couleur du texte de l'en-tête (`fg-color`).
- `frame-color` (défaut `selon le thème`) : Cadre de l'en-tête.
- `star-fg-color` (défaut `selon le thème`) : Étoiles pleines.
- `star-bg-color` (défaut `selon le thème`) : Étoiles vides.
- `star-line-color` (défaut `selon le thème`) : Contour des étoiles.
- `score-fg-color` (défaut `selon le thème`) : Texte de la pastille de score.
- `score-bg-color` (défaut `selon le thème`) : Fond de la pastille de score.
- `lower-bg-color` (défaut `selon le thème`) : En-tête des corrections (`griba`, `rikid`, `bouyachakka`).
- `tags-bg-color` (défaut `selon le thème`) : Fond des étiquettes.
- `tags-fg-color` (défaut `selon le thème`) : Texte des étiquettes.
- `title-color` (défaut `auto`) : Couleur du titre ; relayée vers `exotitle-color`.
- `rule-color` (défaut `black`) : Filets (thèmes d'examen).
- `correction-fg-color` (défaut `black`) : Texte des corrigés (thèmes d'examen).
- `arc` (défaut `selon le thème`) : Arrondi de l'en-tête.
- `righthand-width` (défaut `selon le thème`) : Largeur de la partie droite (`pooja`, `bouyachakka`).

Variante `setrdexo(pour: "rdexostars")` : Défauts des étoiles pour la suite du document.
- `reinitialiser` (défaut `false`) : Repart du style `default`.
- `cles` (défaut `(:)`) : Toutes les clés de `rdexostars`.

Exemple :

```typ
#setrdexo(label: "Problème", display-level: false)
#setrdexo(pour: "EXOEVAL", score-label: ("pt", "pts"))
#setrdexo(pour: "pooja", score-bg-color: "teal")
#setrdexo(definir: "sobre", display-score: false)
```

## rdexo-skin

```typ
rdexo-skin(nom, tcbox: none, tcolorbox: none, correction: none, cadre: none, cadre-correction: none, couleurs: (:))
```

Déclare un thème (\rdexoSkin{nom}{en-tête tcbox}{en-tête tcolorbox}). Les en-têtes sont des fonctions qui reçoivent un dictionnaire `info` (n, label, titre, score, niveau, tags, c (couleurs)…) et renvoient l'en-tête ; un en-tête omis reprend celui du thème `default`. Les couleurs du thème se règlent ensuite par `setrdexo(pour: "<nom>", …)`.

LaTeX : `\rdexoSkin`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `nom` | (positionnel) | str | nom du thème. |  |
| `tcbox` | `none` | function, none | en-tête en ligne (`exo-header: "tcbox"`). |  |
| `tcolorbox` | `none` | function, none | en-tête en bandeau (`exo-header: "tcolorbox"` ou `"none"`). |  |
| `correction` | `none` | function, none | en-tête de correction (reçoit n, label, titre, cible, c). |  |
| `cadre` | `none` | function, none | cadre facultatif autour de l'exercice entier : `(info, contenu) => contenu`, où `contenu` est l'en-tête suivi de l'énoncé (et de la boîte basse). `info` reçoit en plus `couleur` (cadre du thème), `fond`, `breakable` et … |  |
| `cadre-correction` | `none` | function, none | même forme, pour chaque bloc de `rdexocorrection` (`info.correction` vaut true, `breakable` vaut true). Défaut : aucun cadre. |  |
| `couleurs` | `(:)` | dictionary | couleurs du thème (clés de `setrdexo(pour: "<thème>")`). |  |

Exemple :

```typ
#rdexo-skin("simple", tcolorbox: info => block(stroke: (bottom: 1pt), [*#info.label #info.n* -- #info.titre]))
#exo(skin: "simple", exotitle: [Essai])[Énoncé.]
```

## rdexostars

```typ
rdexostars(niveau, total, ..cles)
```

Étoiles de niveau (\rdexostars[options]{niveau}{total}) ; un niveau décimal remplit une étoile en partie. Les défauts se règlent par `setrdexo(pour: "rdexostars", …)`.

LaTeX : `\rdexostars`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `niveau` | (positionnel) | int, float | nombre d'étoiles remplies. |  |
| `total` | (positionnel) | int | nombre d'étoiles. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-themes.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `star-color` | `"yellow"` | color \| str |  | Étoiles pleines. |
| `star-background` | `"gray"` | color \| str |  | Étoiles vides. |
| `line-color` | `black` | color \| str |  | Contour. |
| `line-width` | `0.6pt` | length |  | Épaisseur du contour. |
| `raise` | `0pt` | length |  | Décalage vertical. |
| `scale` | `1` | int \| float |  | Échelle. |
| `show-bg` | `false` | bool |  | Boîte de fond. |
| `display-mode` | `"horizontal"` | str | `horizontal`, `vertical` | Disposition. |
| `background` | `(:)` | dictionary |  | Boîte de fond : `colback`, `colframe`, `boxrule`, `arc`, `boxsep`, `opacityback`. |
| `background-app` | `(:)` | dictionary |  | Idem pour la forme en application. |

Exemple :

```typ
#rdexostars(1.5, 3) #rdexostars(2, 3, star-color: red, scale: 1.5)
#rdexostars(2, 3, display-mode: "vertical")
```

## rdexocorrection

```typ
rdexocorrection(liste, ..cles)
```

Rejoue les corrections (\rdexocorrection[options]{liste}) sous un en-tête de solution, avec des liens cliquables vers les énoncés. Le style d'une boîte de correction se règle par `setrdexo(correction-style: …)`.

LaTeX : `\rdexocorrection`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `liste` | (positionnel) | int, str, array | 0 (depuis le dernier appel), "1,3", "2,...,5", (2, 4), ou "tous" (ajout). |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-corrections.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `columns` | `1` | int |  | Nombre de colonnes. |
| `raster` | `(:)` | dictionary |  | `raster-column-skip`, `raster-row-skip`, `raster-before-skip`. |
| `mirror` | `false` | bool |  | Corrections tournées de 180° (partage d'un écran ou d'une feuille). |
| `mirror-style` | `(:)` | dictionary |  | Habillage du bloc tourné (`colback`, `colframe`, `boxrule`…). |
| `reset-num-start` | `true` | bool |  | Le prochain `rdexocorrection(0)` repart d'ici. |

Exemple :

```typ
#rdexocorrection(0)
#rdexocorrection("1,3", columns: 2)
```

## exocorrection

```typ
exocorrection
```

Marqueur `#exocorrection` (le `\exocorrection` de LaTeX) : dans le corps d'un `exo` ou `exo-eval`, ce qui le suit est la correction de l'exercice. Elle n'est pas affichée à cet endroit : `rdexocorrection` la rejoue plus loin.

À écrire sans parenthèses, une seule fois, au premier niveau du corps (pas dans une liste ni des colonnes). Hors d'un exercice, il n'affiche rien.

LaTeX : `\exocorrection`

Exemple :

```typ
#exo[Une équation][
  Résoudre $2 x + 1 = 7$.
  #exocorrection
  $2 x = 6$, donc $x = 3$.
]
#rdexocorrection(0)
```

## tcblower

```typ
tcblower
```

Marqueur facultatif `#tcblower` : dans le corps d'un `exo` ou `exo-eval`, ce qui le suit est la partie basse de l'exercice (zone de réponse, `crep`), affichée dans sa boîte.

À écrire sans parenthèses, une seule fois, au premier niveau du corps, avant `#exocorrection`. Hors d'un exercice, il n'affiche rien.

Exemple :

```typ
#exo[Un calcul][Calculer $3 times 4$. #tcblower $3 times 4 = 12$.]
```

## rdexofilter

```typ
rdexofilter(expr, match-case: false)
```

N'affiche que les exercices dont les étiquettes satisfont l'expression (\rdexofilter) : opérateurs `!` (non), `&` (et), `|` (ou), parenthèses ; les exercices écartés ne sont ni numérotés ni comptés.

LaTeX : `\rdexofilter`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `expr` | (positionnel) | str | expression booléenne d'étiquettes. |  |
| `match-case` | `false` | bool | respecter la casse. Défaut : false. |  |

Exemple :

```typ
#rdexofilter("calcul & !difficile")
```

## rdexoresetfilter

```typ
rdexoresetfilter()
```

Supprime le filtre d'étiquettes (\rdexoresetfilter).

LaTeX : `\rdexoresetfilter`

Exemple :

```typ
#rdexoresetfilter()
```

## rdexohlist

```typ
rdexohlist(liste, ..cles)
```

Liste horizontale (\rdexohlist[options]{liste}).

LaTeX : `\rdexohlist`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `liste` | (positionnel) | str, array | éléments. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-corrections.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `list-sep` | `","` | str |  | Séparateur de la liste d'entrée. |
| `sep` | `auto` | content \| auto |  | Séparateur affiché (`auto` : « ; » entouré de 0,5 em). |
| `before` | `none` | content \| none |  | Contenu avant la liste. |
| `after` | `none` | content \| none |  | Contenu après la liste. |
| `macro` | `none` | function \| none |  | Mise en forme de chaque élément ; avec `avec-rang: true`, elle reçoit aussi le rang et le nombre d'éléments : `(t, i, n) => …`. |
| `avec-rang` | `false` | bool |  | Passe le rang `i` et le total `n` à `macro`. |

Exemple :

```typ
#rdexohlist("a, b, c")
#rdexohlist("x; y", list-sep: ";", sep: [ -- ], macro: t => strong(t))
#rdexohlist("a, b, c", avec-rang: true, macro: (t, i, n) => [#t (#i/#n)])
```

## rdexotikzlist

```typ
rdexotikzlist(liste, ..cles)
```

Liste en matrice qui choisit son nombre de colonnes selon la largeur (\rdexotikzlist).

LaTeX : `\rdexotikzlist`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `liste` | (positionnel) | str, array | éléments. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-corrections.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `col-sep` | `2em` | length |  | Écart entre colonnes. |
| `row-sep` | `0.5em` | length |  | Écart entre lignes. |
| `max-cols` | `0` | int |  | Nombre maximal de colonnes (0 : sans limite). |
| `macro` | `none` | function \| none |  | Mise en forme de chaque élément. |

Exemple :

```typ
#rdexotikzlist("alpha, beta, gamma, delta, epsilon", max-cols: 2)
```

## rdexocountlist

```typ
rdexocountlist(liste, sep: ",")
```

Nombre d'éléments d'une liste (\rdexocountlist).

LaTeX : `\rdexocountlist`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `liste` | (positionnel) | str, array | liste. |  |
| `sep` | `","` |  |  |  |

Exemple :

```typ
#rdexocountlist("a, b, c")
```

## thenumexo

```typ
thenumexo(etoile: false, avant: [], apres: [])
```

Numéro de l'exercice en cours (\thenumexo[*][avant][après]) ; `etoile` : seulement si `display-numexo`.

LaTeX : `\thenumexo`

Clés communes acceptées (voir en tête) : `avant`, `apres`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `etoile` | `false` | bool | forme étoilée. |  |

Exemple :

```typ
#exo(exotitle: [Essai])[Je suis l'exercice #thenumexo().]
```

## rdexonumexo

```typ
rdexonumexo(f: none)
```

Valeur du compteur d'exercices (\rdexonumexo = `\value{rdexo@numexo}`) ; `f` reçoit l'entier, pour calculer avec.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `f` | `none` | function, none | fonction appliquée à l'entier. Défaut : none (affiche le numéro). |  |

Exemple :

```typ
#exo(exotitle: [Essai])[Le suivant portera le numéro #rdexonumexo(f: n => n + 1).]
```

## thescore

```typ
thescore(etoile: false, avant: [], apres: [])
```

Score de l'exercice en cours (\thescore[*][avant][après]), à la française.

Clés communes acceptées (voir en tête) : `etoile`, `avant`, `apres`.

Exemple :

```typ
#exo(score: 2.5)[Barème : #thescore().]
```

## thescore-libelle

```typ
thescore-libelle(etoile: false, avant: [], apres: [])
```

Score avec son libellé (\theScore[*][avant][après]) : « 2,5 points ».

Clés communes acceptées (voir en tête) : `etoile`, `avant`, `apres`.

Exemple :

```typ
#exo(score: 1)[Barème : #thescore-libelle().]
```

## rdexoscore

```typ
rdexoscore()
```

Valeur brute du score de l'exercice en cours (\rdexoscore).

LaTeX : `\rdexoscore`

Exemple :

```typ
#exo(score: 4)[Valeur brute : #rdexoscore().]
```

## thelevel

```typ
thelevel()
```

Niveau (nombre d'étoiles) de l'exercice en cours (\thelevel).

Exemple :

```typ
#exo(level: 2)[Niveau : #thelevel().]
```

## theexotitle

```typ
theexotitle(etoile: false, avant: [], apres: [])
```

Titre de l'exercice en cours (\theexotitle[*][avant][après]).

Clés communes acceptées (voir en tête) : `etoile`, `avant`, `apres`.

Exemple :

```typ
#exo(exotitle: [Pythagore])[Rappel du titre : #theexotitle().]
```

## theexotitle-style

```typ
theexotitle-style(etoile: false, avant: [], apres: [])
```

Titre dans sa police et sa couleur (\theExotitle[*][avant][après]).

Clés communes acceptées (voir en tête) : `etoile`, `avant`, `apres`.

Exemple :

```typ
#exo(exotitle: [Pythagore])[Titre mis en forme : #theexotitle-style().]
```

## rdexotitlefont

```typ
rdexotitlefont(corps)
```

Applique au texte la police des titres d'exercice (\rdexotitlefont) : celle de l'exercice en cours, sinon celle du réglage `exotitle-font`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) |  |  |  |

Exemple :

```typ
#rdexotitlefont[Texte à la police des titres]
```

## thetags

```typ
thetags(etoile: false, max-cols: 0)
```

Étiquettes de l'exercice en cours, au style du thème (\thetags[*][max cols]).

LaTeX : `\thetags`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `etoile` | `false` | bool | seulement si `display-tags` les montre. |  |
| `max-cols` | `0` | int | colonnes au plus (0 : autant que possible). |  |

Exemple :

```typ
#exo(tags: "calcul, fractions")[Étiquettes : #thetags()]
```

## thelabel

```typ
thelabel()
```

Libellé des exercices (\thelabel) : « Exercice ».

LaTeX : `\thelabel`

Exemple :

```typ
#thelabel()
```

## rdexotags

```typ
rdexotags()
```

Étiquettes de l'exercice en cours, séparées par des virgules (\rdexotags).

LaTeX : `\rdexotags`

Exemple :

```typ
#exo(tags: "calcul, fractions")[#rdexotags()]
```

## tf-numexo

```typ
tf-numexo(oui, non)
```

`oui` si le numéro de l'exercice en cours est affiché, `non` sinon (\TFNumexo{oui}{non}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `oui` | (positionnel) |  |  |  |
| `non` | (positionnel) |  |  |  |

Exemple :

```typ
#exo[#tf-numexo[Numéro affiché][Numéro masqué]]
```

## tf-score

```typ
tf-score(oui, non)
```

`oui` si le score de l'exercice en cours est affiché, `non` sinon (\TFScore{oui}{non}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `oui` | (positionnel) |  |  |  |
| `non` | (positionnel) |  |  |  |

Exemple :

```typ
#exo(score: 2)[#tf-score[Score affiché][Score masqué]]
```

## tf-level

```typ
tf-level(oui, non)
```

`oui` si le niveau de l'exercice en cours est affiché, `non` sinon (\TFLevel{oui}{non}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `oui` | (positionnel) |  |  |  |
| `non` | (positionnel) |  |  |  |

Exemple :

```typ
#exo(level: 2)[#tf-level[Étoiles affichées][Étoiles masquées]]
```

## tf-title

```typ
tf-title(oui, non)
```

`oui` si le titre de l'exercice en cours est affiché, `non` sinon (\TFTitle{oui}{non}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `oui` | (positionnel) |  |  |  |
| `non` | (positionnel) |  |  |  |

Exemple :

```typ
#exo(exotitle: [Essai])[#tf-title[Titre affiché][Titre masqué]]
```

## tf-tags

```typ
tf-tags(oui, non)
```

`oui` si les étiquettes de l'exercice en cours sont affichées (`display-tags`), `non` sinon (\TFTags{oui}{non}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `oui` | (positionnel) |  |  |  |
| `non` | (positionnel) |  |  |  |

Exemple :

```typ
#exo(tags: "calcul", display-tags: true)[#tf-tags[Étiquettes affichées][Étiquettes masquées]]
```

## rdexo-enonce-label

```typ
rdexo-enonce-label(n, corps)
```

Texte cliquable vers la solution de l'exercice n (\rdexoEnonceLabel{n}{texte}).

LaTeX : `\rdexoEnonceLabel`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) |  |  |  |
| `corps` | (positionnel) |  |  |  |

Exemple :

```typ
#rdexo-enonce-label(1)[voir la solution de l'exercice 1]
```

## rdexo-solution-label

```typ
rdexo-solution-label(n, corps)
```

Texte cliquable vers l'énoncé de l'exercice n (\rdexoSolutionLabel{n}{texte}).

LaTeX : `\rdexoSolutionLabel`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) |  |  |  |
| `corps` | (positionnel) |  |  |  |

Exemple :

```typ
#rdexo-solution-label(1)[retour à l'énoncé 1]
```

## rdifficulty

```typ
rdifficulty(n)
```

Niveau par défaut des exercices suivants (\def\rdifficulty{n}) ; équivaut à `setrdexo(level: n)`.

LaTeX : `\rdifficulty`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int, float | niveau de 0 à 3. |  |

Exemple :

```typ
#rdifficulty(2)
```

## rdexo-mod

```typ
rdexo-mod(a, b)
```

Modulo (\rdexoMod{a}{b}) : `a - b ⌊a / b⌋`.

- a, b (int, float): dividende et diviseur.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `a` | (positionnel) |  |  |  |
| `b` | (positionnel) |  |  |  |

Exemple :

```typ
#rdexo-mod(17, 5) et #rdexo-mod(-3, 5)
```

## rdexoinclude

```typ
rdexoinclude(contenu, etoile: false, ..cles)
```

Inclut un exercice rangé dans un fichier (\rdexoinclude[*][options]{fichier}). Le fichier est lu par le document (`include "fichier.typ"`) : un paquet Typst ne peut pas lire les fichiers de l'utilisateur.

LaTeX : `\rdexoinclude`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `contenu` | (positionnel) | content | contenu du fichier (`include "…"`). |  |
| `etoile` | `false` | bool | le fichier contient déjà ses exercices, qui reçoivent les options. Défaut : false. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-exercices.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `cles` | `(:)` | any |  | Clés de `setrdexo` : options appliquées à l'exercice inclus. |

Exemple :

```typ
#rdexoinclude(exotitle: [Inclus])[Contenu lu dans un fichier.]
```

## itempoint

```typ
itempoint(n, ..args)
```

Points d'un item (\tcbitempoint{points}[décalage v][décalage h] et \itempoint, fusionnés) : ajoute des points au barème et, si `displayitempoints(true)` ou `boite: true`, pose la boîte « n pts ». Les points d'un exercice alimentent la case de score de son en-tête.

*Écriture normale : les points en tête, le texte de l'item en second argument.* Le professeur voit tout de suite ce que vaut la question, et la fonction sait où poser la boîte : à droite, en haut de l'item, le texte de la première ligne coulant à sa gauche puis reprenant toute la largeur dessous (`position: "droite"`, défaut), ou en ligne, juste avant le premier mot (`position: "gauche"`). Le texte ne passe jamais sous la boîte.

Ancien usage conservé : appel en fin d'item, sans texte (`Texte. #itempoint(2)`). La boîte est alors posée à droite de la dernière ligne, dont la place est réservée.

LaTeX : `\itempoint`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) | int, float | nombre de points (0,5 permis). |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-points.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `corps` | (positionnel) | content |  | Texte de la question, entre crochets, juste après les points. Sans lui : ancien usage, l'appel en fin de question (voir plus bas). |
| `position` | `"droite"` | str | `droite`, `gauche` | Place de la boîte. Réglable par `setrdexo(pour: "itempoint", position: …)`. |
| `reserver` | `true` | bool |  | Appel en fin de question (sans texte) : réserve la place de la boîte au bout de la dernière ligne, pour que le texte ne passe jamais dessous. |
| `variante` | `"standard"` | str | `standard`, `gris` | Aspect de la boîte. |
| `dy` | `0pt` | length |  | Décalage vertical, vers le haut. |
| `dx` | `auto` | length \| auto |  | Décalage horizontal, vers la gauche. `auto` : aucun, ou 2 cm si `dys` est vrai. |
| `dys` | `false` | bool |  | Boîte décalée de 2 cm vers la gauche, pour un document adapté aux élèves dys. |
| `boite` | `auto` | bool \| auto |  | Affiche la boîte pour ce seul appel. `auto` : suit `displayitempoints`. |
| `colback` | `"purple!10"` | color \| str |  | Fond de la boîte. |
| `colframe` | `black` | color \| str |  | Cadre de la boîte. |
| `boxrule` | `0.4pt` | length |  | Épaisseur du cadre. |
| `arc` | `4pt` | length |  | Arrondi des coins. |
| `boxsep` | `3pt` | length |  | Marge intérieure. |
| `min-width` | `1cm` | length |  | Largeur minimale. |
| `xshift` | `1.6cm` | length |  | Position à partir du bord droit. |
| `singular` | `"pt"` | content |  | Mot du singulier. |
| `plural` | `"pts"` | content |  | Mot du pluriel. |
| `style` | `auto` | str \| array |  | Style(s) nommé(s) défini(s) par `setrdexo(definir: …)`. |

Exemple :

```typ
#displayitempoints(true)
+ #itempoint(1)[Calculer $3 + 4$.]
+ #itempoint(0.5, dx: 5mm)[Calculer $3 times 4$.]
+ #itempoint(2)[Étudier les variations de la fonction $f(x) = (3x^2 - 5x + 2) e^(-x/2) + ln(x^2 + 1)$ sur l'intervalle $[0 ; 10]$ et dresser son tableau.]
+ #itempoint(1, position: "gauche")[Boîte en ligne, avant le texte.]
```

## infotcbitempoint

```typ
infotcbitempoint(n, ..args)
```

Points « informatique » (\infotcbitempoint) : boîte verte avec icône d'ordinateur, totaux séparés (`getinfoexopoint`, `getsavedinfototalpoints`). Mêmes écritures et mêmes clés qu'`itempoint`.

LaTeX : `\infotcbitempoint`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) |  |  |  |

Exemple :

```typ
#displayitempoints(true)
#infotcbitempoint(3)[Programme Python.]
```

## displayitempoints

```typ
displayitempoints(valeur)
```

Affiche ou masque les boîtes de points (\displayitempointstrue / \displayitempointsfalse).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) | bool | true pour afficher. |  |

Exemple :

```typ
#displayitempoints(true)
```

## baremepoint

```typ
baremepoint(contenu, n, ..cles)
```

Boîte rouge « n pts » au-dessus d'un contenu (\baremepoint{contenu}{points}), si `displaybaremepoints(true)` ; n'entre dans aucun total.

LaTeX : `\baremepoint`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `contenu` | (positionnel) | content | contenu repéré. |  |
| `n` | (positionnel) | int, float | points. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-points.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `colback` | `"red!2!white"` | color \| str |  | Fond. |
| `colframe` | `"red"` | color \| str |  | Cadre. |
| `coltext` | `"red"` | color \| str |  | Couleur du texte. |
| `raise` | `0.2cm` | length |  | Hauteur au-dessus du contenu. |

Exemple :

```typ
#displaybaremepoints(true)
#v(1em) Résultat : #baremepoint[$x = 3$][2]
```

## displaybaremepoints

```typ
displaybaremepoints(valeur)
```

Affiche ou masque les boîtes de `baremepoint` (\displaybaremepointstrue / false).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `valeur` | (positionnel) |  |  |  |

Exemple :

```typ
#displaybaremepoints(true)
```

## getinfoexopoint

```typ
getinfoexopoint(n)
```

Points « informatique » de l'exercice n (\getinfoexopoint{n}).

LaTeX : `\getinfoexopoint`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) |  |  |  |

Exemple :

```typ
#getinfoexopoint(1)
```

## getsavedtotalpoints

```typ
getsavedtotalpoints()
```

Total des points du document (\getsavedtotalpoints), suivi d'un \phantom{A}.

LaTeX : `\getsavedtotalpoints`

Exemple :

```typ
Le devoir est noté sur#getsavedtotalpoints()points.
```

## getsavedinfototalpoints

```typ
getsavedinfototalpoints()
```

Total des points « informatique » du document (\getsavedinfototalpoints).

LaTeX : `\getsavedinfototalpoints`

Exemple :

```typ
#getsavedinfototalpoints()
```

## competence

```typ
competence(code: none, corps)
```

Ligne d'un tableau de compétences (\competence[code]{texte}) : puce, intitulé, code encadré à droite.

LaTeX : `\competence`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `code` | `none` | str, content, none | code de la compétence, encadré à droite. Défaut : none. |  |
| `corps` | (positionnel) | content | intitulé. |  |

Exemple :

```typ
#tableaucompetence(competence[Reconnaître une fonction affine], competence(code: "C2")[Calculer une image])
```

## tableaucompetence

```typ
tableaucompetence(..items)
```

Tableau « Compétences travaillées » (\tableaucompetence) : une ligne par compétence et quatre colonnes d'auto-évaluation MI, MF, MS, TBM. Les titres et en-têtes se règlent par `setrdexo(pour: "competences", …)`.

La syntaxe environnement donne un tableau sans codes : `#begin(tableaucompetence)` puis une compétence par item `-`, puis `#end(tableaucompetence)`.

- ..items (dictionary, content): lignes : `competence(…)` ou simples contenus ; ou un seul corps d'items `-`.

LaTeX : `\tableaucompetence`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-evaluation.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `items` | (positionnel) | dictionary \| content |  | Les lignes : `competence(…)`, de simples contenus. |

Exemple :

```typ
#tableaucompetence(competence[Résoudre une équation], competence(code: "C3")[Justifier])
```

## tableaucompetence-eval

```typ
tableaucompetence-eval(..items)
```

Tableau « Compétences évaluées » (\tableaucompetenceEval).

LaTeX : `\tableaucompetenceEval`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-evaluation.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `items` | (positionnel) | dictionary \| content |  | Les lignes, comme pour `tableaucompetence`. |

Exemple :

```typ
#tableaucompetence-eval(competence[Calculer], competence(code: "C2")[Raisonner])
```

## printcompindex

```typ
printcompindex()
```

Index des compétences du document (\printcompindex) : un tableau « Compétences évaluées » dont les lignes sont les compétences inscrites par les exercices (titres des EXO, étiquettes des EXOEVAL), sans doublon.

LaTeX : `\printcompindex`

Exemple :

```typ
#printcompindex()
```

## tableau-eval

```typ
tableau-eval(duree, ..cles)
```

Cartouche d'évaluation (\tableauEval{durée}) : « Nom / Prénom » sur 3/4, « Durée » et chronomètre sur 1/4.

LaTeX : `\tableauEval`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `duree` | (positionnel) | int | durée en minutes. |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-evaluation.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `colback` | `white` | color \| str |  | Fond. |
| `colframe` | `black` | color \| str |  | Cadre. |
| `boxrule` | `1pt` | length |  | Épaisseur du cadre. |
| `arc` | `2pt` | length |  | Arrondi. |
| `nom` | `[Nom :]` | content |  | Intitulé de la case du nom. |
| `prenom` | `[Prénom :]` | content |  | Intitulé de la case du prénom. L'intitulé de la durée se règle de même par la clé `duree` de `setrdexo(pour: "tableauEval", …)`. |
| `raster-columns` | `4` | int |  | Nombre de colonnes du raster. |
| `raster-column-skip, raster-row-skip` | `5pt, 1pt` | length |  | Espaces du raster. |

Exemple :

```typ
#tableau-eval(55)
```

## tableau-projet-eval

```typ
tableau-projet-eval(date, ..cles)
```

Cartouche de projet (\tableauProjetEval{date}) : case de droite « Date de rendu : ».

LaTeX : `\tableauProjetEval`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `date` | (positionnel) |  |  |  |

Exemple :

```typ
#tableau-projet-eval[12 octobre]
```

## tableau-presente-eval-sixieme

```typ
tableau-presente-eval-sixieme(inutilise, note, ..cles)
```

Cartouche de sixième (\tableauPresenteEvalSixieme{…}{note max}) : « Nom / Prénom » et « Bilan : ▢ / note ▢ ».

LaTeX : `\tableauPresenteEvalSixieme`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `inutilise` | (positionnel) | any | premier argument LaTeX (sans effet). |  |
| `note` | (positionnel) | int, content | note maximale. |  |

Exemple :

```typ
#tableau-presente-eval-sixieme([], 20)
```

## chrono

```typ
chrono(minutes, ..cles)
```

Chronomètre encadré « Durée : » (\chrono{minutes}).

LaTeX : `\chrono`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `minutes` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-evaluation.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `title` | `[Durée :]` | content |  | Titre de l'encadré. |
| `width` | `3cm` | length |  | Largeur. |
| `colframe` | `"gray!75!black"` | color \| str |  | Couleur du cadre. |

Exemple :

```typ
#chrono(30)
```

## overlaychrono

```typ
overlaychrono(minutes, ..cles)
```

Cadran en surimpression (\overlaychrono{minutes}) : secteur jusqu'aux minutes, puis « minutes’ ».

- radius (length), color (color, str), opacity (float), line-width, circle-width, label-sep (length): réglables (`setrdexo(pour: "overlaychrono", …)`).

LaTeX : `\overlaychrono`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `minutes` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-evaluation.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `radius` | `0.4cm` | length |  | Rayon du cadran. |
| `color` | `"red"` | color \| str |  | Couleur du secteur. |
| `opacity` | `0.7` | float |  | Opacité du secteur. |
| `line-width` | `0.8pt` | length |  | Épaisseur de l'aiguille. |
| `circle-width` | `0.4pt` | length |  | Épaisseur du cercle. |
| `label-sep` | `0.7cm` | length |  | Distance du texte « minutes’ ». |

Exemple :

```typ
Durée : #h(1cm) #overlaychrono(45) #h(2cm)
```

## mi

```typ
mi()
```

Niveau de maîtrise « Maîtrise insuffisante » (\mi) : émoji, ou « MI » si `setrdexo(emoji: false)`.

LaTeX : `\mi`

Exemple :

```typ
#mi() #mf() #ms() #tbm()
```

## mf

```typ
mf()
```

« Maîtrise fragile » (\mf).

LaTeX : `\mf`

Exemple :

```typ
#mf()
```

## ms

```typ
ms()
```

« Maîtrise satisfaisante » (\ms).

LaTeX : `\ms`

Exemple :

```typ
#ms()
```

## tbm

```typ
tbm()
```

« Très bonne maîtrise » (\tbm).

LaTeX : `\tbm`

Exemple :

```typ
#tbm()
```

## chapitre-bac

```typ
chapitre-bac(..cles, doc)
```

Sujet de baccalauréat (\chapitreBac[clés]) : police sans empattement, pied de page officiel (code du sujet, « Page : n/N » du sujet seul), skin « exobac » et page de garde. En Typst c'est un modèle : `#show: chapitreBac.with(…)` (en LaTeX, une commande de préambule).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `doc` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `style` | `"bac"` | str | `bac`, `brevet` | Style du sujet. |
| `examen, epreuve, matiere, serie, duree` | `none` | content |  | Textes de la page de garde. `none` : le texte officiel du style. |
| `session` | `auto` | int \| str \| auto |  | Année. `auto` : l'année en cours. |
| `coefficient` | `none` | int \| content |  | Coefficient de l'épreuve. |
| `code` | `none` | str \| content |  | Code du sujet, en pied de page à gauche. |
| `pages` | `auto` | int \| auto |  | Nombre de pages annoncé. `auto` : les pages du sujet, sans le corrigé. |
| `calculatrice, annonce, composition, qualite, infos` | `none` | content |  | Paragraphes de la page de garde. |
| `bareme` | `none` | array \| content |  | Barème du DNB : `((intitulé, points), …)`. |
| `famille` | `TeX Gyre Heros` | str \| array \| none |  | Police du document (substitut d'Arial). |
| `garde` | `true` | bool |  | Ajoute la page de garde. |
| `sans-serif` | `true` | bool |  | Police sans empattement. |
| `mise-en-page` | `true` | bool |  | Retraits nuls. |
| `skin` | `true` | bool |  | Active le thème `exobac`. |

Exemple :

```typ
#show: chapitre-bac.with(session: 2026, code: "26-MATJ1ME1", garde: false)
#exo(score: 5)[Suites][Énoncé de l'exercice.]
```

## chapitre-brevet

```typ
chapitre-brevet(..cles, doc)
```

Sujet du DNB (\chapitreBrevet[clés] = \chapitreBac[style=brevet, …]).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `doc` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Mêmes clés que `chapitre-bac`. |

Exemple :

```typ
#show: chapitre-brevet.with(session: 2026, code: "26GENMATMEAG1", garde: false)
#exo(score: 2.5)[Statistiques][Énoncé.]
```

## style-exo-bac

```typ
style-exo-bac(..cles)
```

Active le skin « exobac » (\styleExoBac[clés rdexo]) : « Exercice n » souligné, « (5 points) » en gras.

LaTeX : `\styleExoBac`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Clés de `setrdexo`. |

Exemple :

```typ
#style-exo-bac()
#exo(score: 5)[Probabilités][Énoncé.]
```

## style-exo-brevet

```typ
style-exo-brevet(..cles)
```

Active le skin « exobrevet » (\styleExoBrevet[clés rdexo]) : « Exercice n : titre (X points) » en gras.

LaTeX : `\styleExoBrevet`

Exemple :

```typ
#style-exo-brevet()
#exo(score: 2.5)[Géométrie][Énoncé.]
```

## style-questions-bac

```typ
style-questions-bac(etoile: false, ..cles)
```

Partie « Questions » (\styleQuestionsBac[*][clés]) : items « Question n » sans barème ni titre, numérotés à partir de 1 (`etoile: true` : la numérotation continue).

LaTeX : `\styleQuestionsBac`

Clés communes acceptées (voir en tête) : `etoile`.

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Clés de `setrdexo`. |

Exemple :

```typ
#style-exo-bac()
#style-questions-bac()
#exo[Calculer $2^10$.]
```

## style-exercices-bac

```typ
style-exercices-bac(etoile: false, ..cles)
```

Partie « Exercices » (\styleExercicesBac[*][clés]) : « Exercice n (X points) », titre affiché.

LaTeX : `\styleExercicesBac`

Clés communes acceptées (voir en tête) : `etoile`.

Exemple :

```typ
#style-exercices-bac()
```

## numeroter-bac

```typ
numeroter-bac(n: 0)
```

Le prochain exercice portera le numéro n + 1 (\numeroterBac[n]).

LaTeX : `\numeroterBac`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | `0` | int | décalage. Défaut : 0. |  |

Exemple :

```typ
#numeroter-bac(n: 3)
```

## partie-bac

```typ
partie-bac(titre, etoile: false)
```

Titre de partie centré et gras (\partieBac[*]{titre}) ; sans étoile, entrée de sommaire.

LaTeX : `\partieBac`

Clés communes acceptées (voir en tête) : `titre`, `etoile`.

Exemple :

```typ
#partie-bac[PREMIÈRE PARTIE : AUTOMATISMES]
```

## consigne-bac

```typ
consigne-bac(texte, etoile: false)
```

Cadre de consignes en gras italique centré (\consigneBac[*]{texte}) ; `etoile` : gras au fil du texte.

LaTeX : `\consigneBac`

Clés communes acceptées (voir en tête) : `etoile`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `texte` | (positionnel) |  |  |  |

Exemple :

```typ
#consigne-bac[Pour chaque question, une seule réponse est exacte.]
```

## encadre-bac

```typ
encadre-bac(corps, titre: none)
```

Petit cadre pleine largeur (\encadreBac[titre]{contenu}).

LaTeX : `\encadreBac`

Clés communes acceptées (voir en tête) : `titre`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) |  |  |  |

Exemple :

```typ
#encadre-bac(titre: [Aide au calcul.])[$2^10 = 1024$]
```

## encadre-bac-etroit

```typ
encadre-bac-etroit(corps, titre: none)
```

Même cadre, à la largeur du contenu (\encadreBacEtroit[titre]{contenu}).

LaTeX : `\encadreBacEtroit`

Clés communes acceptées (voir en tête) : `titre`.

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) |  |  |  |

Exemple :

```typ
#encadre-bac-etroit(titre: [Rappel :])[$e^0 = 1$]
```

## corrige-bac

```typ
corrige-bac(titre: [CORRIGÉ], etoile: false)
```

Clôt le sujet et ouvre le corrigé, à pagination séparée (\corrigeBac[*][titre=CORRIGÉ]) ; rejoue toutes les corrections, sauf avec `etoile: true`.

LaTeX : `\corrigeBac`

Clés communes acceptées (voir en tête) : `titre`, `etoile`.

Exemple :

```typ
#corrige-bac()
```

## bfexobac-uline

```typ
bfexobac-uline(corps, ..cles)
```

Souligne exactement la largeur du texte (\bfexobacUline{texte}).

LaTeX : `\bfexobacUline`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `corps` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `depth` | `2.4pt` | length |  | Profondeur du filet sous la ligne de base. |
| `width` | `0.5pt` | length |  | Épaisseur du filet. |

Exemple :

```typ
#bfexobac-uline[*Exercice 1*] #bfexobac-uline(depth: 3pt, width: 1pt)[*épais*]
```

## exolombards

```typ
exolombards(..cles, doc)
```

Charge l'habillage « exolombards » (\usepackage[options]{bfcours-exolombards-skin}, ajout) : règle les options, active le skin (`auto`) et pose le pied de page d'origine (`pied`). Les options se règlent aussi, en cours de document, par `setrdexo(pour: "exolombards", …)` (`decalage`, `correction`, `etiquette`, `titre`, `bareme`, `mot-correction`).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `doc` | (positionnel) |  |  |  |

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `auto` | `true` | bool |  | Active le thème. |
| `pied` | `false` | bool |  | Pied de page « auteur, page, établissement ». |
| `auteur` | `[M. Dupont]` | content |  | Auteur du pied de page. |
| `etablissement` | `[Lycée du Parc]` | content |  | Établissement du pied de page. |
| `decalage` | `-0.25cm` | length |  | Débordement de l'étiquette dans la marge. |
| `correction` | `"auto"` | str | `auto`, `suite`, `separee` | Mode des corrections. |

Exemple :

```typ
#show: exolombards.with(pied: true, auteur: [M. Dupont])
#exo(score: 5)[Fonctions][L'énoncé démarre sur la ligne de l'étiquette.]
```

## style-exo-lombards

```typ
style-exo-lombards(..cles)
```

Active le skin « exolombards » (\styleExoLombards[clés rdexo]) : « [Exercice n] » encadré en ligne.

LaTeX : `\styleExoLombards`

Clés documentées dans le guide (`farfadet-exo/docs/chapitre-sujets.typ`) :

| Clé | Défaut | Type | Valeurs | Rôle |
|---|---|---|---|---|
| `..cles` | `(:)` | any |  | Clés de `setrdexo`. |

Exemple :

```typ
#style-exo-lombards()
#exo(score: 3)[Suites][Énoncé sur la même ligne.]
```

## corrections-lombards

```typ
corrections-lombards(mode)
```

Change le mode des corrections (\correctionsLombards{auto|suite|separee}).

LaTeX : `\correctionsLombards`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `mode` | (positionnel) |  |  |  |

Exemple :

```typ
#corrections-lombards("separee")
```

## corrige-lombards

```typ
corrige-lombards(n, reference: none)
```

Corrigé n à la manière du document de correction d'origine (\corrigeLombards[réf.]{n}), ou « Pas de corrigé disponible pour cet exercice. ».

LaTeX : `\corrigeLombards`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `n` | (positionnel) |  |  |  |
| `reference` | `none` |  |  |  |

Exemple :

```typ
#corrige-lombards(1, reference: "PO020")
```

## exolombards-etiquette

```typ
exolombards-etiquette(texte)
```

Étiquette encadrée en gras (\exolombardsEtiquette{texte}).

LaTeX : `\exolombardsEtiquette`

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `texte` | (positionnel) |  |  |  |

Exemple :

```typ
#exolombards-etiquette[Exercice 1]
```

## exolombards-titre

```typ
exolombards-titre(texte)
```

Titre discret en italique (\exolombardsTitre{titre}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `texte` | (positionnel) |  |  |  |

Exemple :

```typ
#exolombards-titre[Suites géométriques]
```

## exolombards-bareme

```typ
exolombards-bareme(texte)
```

Barème entre parenthèses (\exolombardsBareme{points}).

| Clé | Défaut | Type | Rôle | Option LaTeX |
|---|---|---|---|---|
| `texte` | (positionnel) |  |  |  |

Exemple :

```typ
#exolombards-bareme[5 points]
```

## exolombards-mot-correction

```typ
exolombards-mot-correction()
```

Mot placé devant une correction (\exolombardsMotCorrection) : « Correction : ».

LaTeX : `\exolombardsMotCorrection`

Exemple :

```typ
#exolombards-mot-correction()
```
