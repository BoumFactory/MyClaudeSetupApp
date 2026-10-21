# Moteur canvas : une capsule = un `spec.js`

Le moteur dessine lui-même dans un canvas et encode en H.264 dans Chromium (WebCodecs, 1 ou 2 workers). Tout le contenu d'une capsule tient dans **un seul fichier de données**, `spec.js` : pas de HTML, pas de CSS, pas de contrôle de débordement. La mise en page réduit le texte pour qu'il tienne dans sa zone, donc aucun débordement n'est possible.

Mesuré le 09/10/2026, à froid, en 540p : labomaths (2 min 05) en ≈ 9 s, tableau-croise (2 min 51) en 14 s, exo5 (3 min 50) en 16 s. Le moteur HTML met 48 s, 66 s et 87 s pour les mêmes capsules, avec un rendu à l'identique (planches `planches/comparaison.png` des trois capsules `*-canvas` de `<dossier_capsules>/`).

**Exemples validés à imiter** (`assets/exemples/`) : `labomaths-canvas/` (figure à main levée, panneau en étapes, formules à trous, rédaction en cartouches), `tableau-croise-canvas/` (voie A, tableau croisé, focus, compteur, flèche), `exo5-canvas/` (voie B, 3 min 50 : énoncé en cartes, méthode en étapes, dizaines de vols tableau ↔ calculs).

## Fichiers et commandes

Une capsule contient `spec.js`, `index.html` (l'aperçu, copié de `assets/gabarit-canvas/`, qui ne se modifie pas), `moteur-canvas/` (copie de `assets/moteur-canvas/`), `data/` (transcript, temps forts), l'audio et éventuellement des images.

```bash
$PY $S/nouvelle_capsule.py "<capsule>" ["<audio>"] --titre "..." [--formules grandes|compactes]   # moteur-canvas/, index.html, spec.js, audio (facultatif en voie B)
$PY $S/maj_moteur.py "<capsule>" [...]                     # recopie assets/moteur-canvas/ dans des capsules existantes
$PY $S/rendre_canvas.py "<capsule>" --images 12,40.5,63   # planche : PNG dans <capsule>/planches/, sans vidéo (2 à 3 s)
$PY $S/rendre_canvas.py "<capsule>" [--qualite 540|envoi|projection] [--allegees 370,220] [--fenetre]
```

- **Aperçu** : ouvrir `index.html` (Espace = lecture, ←/→ = ±2 s, C = commenter, « Copier pour Claude »). Les erreurs (mot introuvable, id inconnu ou en double, formule TeX fausse, clé inconnue, image absente) s'affichent dans un bandeau rouge ; la console liste les zones dont le texte a été réduit.
- **Rendu** : `capsule-540p.mp4` (220 kb/s, ≈ 2,2 Mo/min), `capsule-envoi.mp4` (720p), `capsule.mp4` (1080p). Le rendu refuse de partir s'il reste une erreur. Une image clé est forcée après chaque changement de scène.
- **N'importe quel PC Windows** : `--gpu auto` (défaut) essaie Vulkan (carte dédiée), puis Direct3D 11 (puce Intel ou AMD intégrée), puis le rendu logiciel (avertissement, ≈ 1,4 fois plus lent sur 12 cœurs). `--workers 0` (défaut) met 2 workers dès 4 cœurs et 2 Go libres, sinon 1 ; mémoire de pointe mesurée ≈ 0,6 Go. Mesuré sur labomaths : NVIDIA Vulkan 10,6 s · Intel UHD Direct3D 11 12,5 s · logiciel 14,6 s (22,7 s avec 1 worker), mêmes images.
- L'encodeur H.264 logiciel de Chromium est le défaut : `--accel materiel` ignore la consigne de débit et donne des fichiers plus lourds.
- **Après une évolution du moteur** : `maj_moteur.py "<capsule>"` remplace `moteur-canvas/` de la capsule (refuse un dossier sans `spec.js`). Le rendu utilise la copie de la capsule quand elle existe.

## Structure de `spec.js`

```js
CAPSULE({
  titre: 'Droites parallèles et angles', audio: 'audio.wav',      // ou 'audio-mix.wav' (musique.py)
  theme: 'nuit', ambiance: true, mention: 'Voix de synthèse',      // theme : nuit | jour ; mention : bas droite (tailleMention : 26)
  sousTitres: false, corrections: { 'P2M': 'P de M' },             // sous-titres sur demande ; corrections appliquées au texte
  macros: { BAC: '\\cyan{\\widehat{BAC}}' },                       // \BAC utilisable dans toutes les formules
  formules: 'grandes',                                              // taille des formules : grandes | compactes (voir plus bas)
  scenes: [
    { id: 's-titre', gabarit: 'titre', debut: 0, haut: [ … ], centre: [ … ] },
    { id: 's-main', gabarit: 'figure-panneau', debut: '@b02-0.3', bandeau: […], figure: […], panneau: […] },
  ],
  gestes(C) { C.montre('#p-q1', '@b06~"Déterminer"-0.2'); … },     // catalogue : references/gestes.md
});
```

`debut` d'une scène = l'instant du changement de scène (fondu flou) ; les scènes s'enchaînent dans l'ordre du tableau.

## Gabarits de mise en page

Une scène choisit un gabarit, puis remplit ses zones par leur nom (repère 1920×1080) :

| Gabarit | Zones (x, y, largeur × hauteur) |
|---|---|
| `titre` | `haut` (90, 110, 1740 × 230) · `centre` (90, 360, 1740 × 680) |
| `figure-panneau` | `bandeau` (60, 34, 900 × 80) · `figure` (40, 150, 960 × 500) · `sous-figure` (40, 656, 960 × 390) · `panneau` (1060, 130, 800 × 910) |
| `tableau-calcul` | `bandeau` · `donnees` (90, 130, 1740 × 130) · `tableau` (60, 290, 960 × 640) · `calcul` (1060, 290, 800 × 640) · `bas` (90, 950, 1740 × 100) |
| `colonne` | `bandeau` · `centre` (260, 150, 1400 × 880) |
| `plein` | `centre` (90, 70, 1740 × 940) |

- Une zone reçoit une liste d'éléments empilés (écart 26), ou `{ contenu: [...], valign: 'haut' | 'centre' | 'bas', ecart, align }`.
- `zones: { maZone: { x, y, l, h } }` dans la scène ajoute une zone ou en redéfinit une : c'est ainsi qu'on reproduit une mise en page sur mesure (voir `tableau-croise-canvas`, `exo5-canvas`).
- **Panneau en étapes** : une zone qui contient **une seule `pile`** ajuste chaque étape séparément (question 1, question 2, rédaction…). Les étapes se superposent ; `montre`/`cache`/`remplace` les font se succéder. `dy: 50` sur une étape la décale vers le bas. Une pile de pilules prend la largeur de la plus longue.
- **Ajustement** : si le contenu ne tient pas, toute la zone (ou l'étape) est réduite à l'identique (texte, formules, marges). Viser 100 % : en dessous de 85 %, alléger le contenu plutôt que laisser réduire.

## Éléments

Une clé donne le type ; une simple chaîne vaut `{ texte }`.

| Élément | Exemple | Options |
|---|---|---|
| texte | `'L\'angle $\\BAI$ mesure **50°**'` | `taille` (40), `gras`, `it`, `doux`, `couleur`, `nowrap`, `interligne` (1,3), `tailleTex` (1,1 × taille), `decoupe`, `degrade: ['ambre', 'rose']`, `lueur` (true = 30 px), `majuscules`, `espacementLettres` (em) |
| surTitre, titre | `{ titre: 'Droites [et angles]{.grad}' }` | surTitre : 30 px, capitales cyan ; titre : 92 px |
| tex | `{ tex: '\\CAI=\\cssId{dv2}{140^\\circ}', id: 'f1' }` | `taille` (selon `formules` : 66 ou ratio × la taille héritée, voir § Taille des formules), `display`, `couleur`, `lueur`, `degrade` (compteur) |
| carte | `{ carte: [...] ou 'texte', couleur: 'rose', id }` | `titre` (étiquette noire « Propriété : »), `puce` (pilule en tête), `marge: [v, h]` ([28, 36]), `margeHaut`, `margeBas`, `ecart` (12 ; 16 en `compactes`), `alignEnfants: 'centre'`, `l` (largeur fixe), `h` (hauteur minimale) + `justifie` (centre, fin, entre), `rayon` (28), `forte` |
| puce | `{ puce: 'Question 1', couleur: 'rose' }` | `taille` (32), `margeH`, `margeV`, `numero: 1` (pastille ronde avant le texte) |
| lettre, pastille | `{ lettre: 'M', couleur: 'violet' }`, `{ pastille: 1 }` | `taille` (74 / 56 : côté de la boîte) |
| resultat | `{ resultat: '$\\mathbf{0{,}6}$', couleur: 'violet' }` | pilule lumineuse du résultat ; `taille` (62 ; 46 en `compactes`) |
| ligne, colonne, pile | `{ ligne: [...], ecart: 18, egal: true }` | `justifie` (debut, centre, fin, entre), `valign` (centre ; `base` = lignes de base alignées), `alignEnfants` |
| calcul | `{ calcul: [[g, '=', d], ['', '=', d2]] }` | cases = TeX ou éléments ; `colonnesL: [200, 66]`, `hauteurLigne`, `ecart: [lignes, colonnes]` ([12, 14] ; [14, 14] en `compactes`) ; alignement droite / centre / gauche |
| tableau | `{ tableau: lignes, id: 'tab', totaux: true }` | 1re ligne et 1re colonne = en-têtes (doux) ; case = nombre (TeX gras), `{ n: 105, id: 'v-mb', couleur }`, texte, `'$…$'` ou élément ; `colonnes: [1.35, 1, 1, 1]`, `hauteurCase` (108), `taille` (50), `tailleEntete` (34) ; cases visables `'tab-l1c2'` |
| figure | `{ figure: { vue, points, objets }, l, h, id }` | voir ci-dessous |
| image | `{ image: 'exo-source.png', l: 900, h: 480, cadre: true }` | `ajuste: 'contenir' | 'couvrir'`, `rayon`, `fond` ; zoom lent : geste `C.zoom` |
| trait | `{ trait: 'vertical', h: 60 }` | séparateur (ou `'horizontal'`, `l`) |
| methode, encadrer, etape | `{ methode: [...], titre: 'Méthode' }`, `{ encadrer: '$x=3$' }`, `{ etape: 'Dresser', n: 1 }` | composants façon bfcours (boîte méthode, `\encadrer`, étape numérotée) ; texte : `[mot]{.acc}` = `\acc` |
| icone, espace | `{ icone: '🎯', taille: 80 }`, `{ espace: 40 }` | emoji décoratif seulement |
| dessin | `{ dessin: (ctx, boite, t, outils) => {…}, l, h }` | échappatoire, redessiné à chaque image |

Clés communes : `id`, `align` (dans une colonne : `gauche`, `centre`, `droite`, `etire` ; textes et cartes s'étirent par défaut, pilules et formules non), `l` (largeur), `h` (hauteur minimale), `visible: false`, `focus: true`, et les raccourcis de gestes. `taille`, `tailleTex`, `gras` et `formules` se transmettent aux éléments contenus : `{ carte: [...], taille: 46 }` règle tout le texte de la carte. **Héritage de la taille d'une formule** : `taille` sur la formule, sinon `tailleTex` du plus proche conteneur, sinon ratio × `taille` du plus proche conteneur (ratio selon `formules`), sinon la taille par défaut du préréglage. Une formule `$…$` dans un texte reste à 1,1 × la taille du texte (`tailleTex` du texte), quel que soit le préréglage.

### Taille des formules : clé `formules`

Deux goûts coexistent dans le même moteur ; la clé choisit un préréglage pour la capsule, une scène ou un conteneur (carte, colonne…), le plus proche l'emporte. **Clé absente = comportement historique** (capsules existantes inchangées au pixel près).

```js
CAPSULE({ formules: 'grandes', … })                      // ou 'compactes'
{ id: 's-redaction', formules: 'compactes', … }          // surcharge pour une scène (ou une carte)
formules: { base: 'grandes', ratio: 1.3, padV: 0.06 }    // réglage fin : n'importe quel paramètre ci-dessous
```

| Paramètre | `grandes` | `compactes` | clé absente |
|---|---|---|---|
| `ratio` (formule sans taille dans un conteneur à `taille` t) | 1,6 × t (carte 40 → 64 px) | 1,1 × t (carte 32 → 35 px) | 1,1 × t |
| `defaut` (aucune taille héritée) | 66 px | 44 px | 66 px |
| `padV` (respiration au-dessus et au-dessous de chaque formule, × taille) | 0 | 0,12 | 0 |
| `ecartCarte` / `ecartGrille` | 12 / [12, 14] | 16 / [14, 14] | 12 / [12, 14] |
| `resultat` (pilule) | 62 | 46 | 62 |
| `figurePanneau` (gabarit `figure-panneau`) | inchangé | figure y 136, h 480 ; sous-figure y 700, h 350 | inchangé |

- **`grandes`** : la formule est l'objet principal de l'écran ; une étape à la fois, les lignes précédentes s'effacent ou se réduisent. Ni `tailleTex` ni `taille` en dur sur la carte de calcul : `taille: 40` sur la carte suffit (64 px). Une zone réduite de plus de 20 % donne un **AVERTISSEMENT** dans la planche (« formules réduites de 24 % … couper la scène en deux étapes ») : sinon « grandes » redevient « compactes » en silence.
- **`compactes`** : formules à la taille du texte, rédaction complète visible qui se construit ligne par ligne.
- Non concernés : tuiles, scènes 3D, étiquettes de figure (taille propre, 46), nombres phares à `taille` explicite.
- `nouvelle_capsule.py --formules` écrit la valeur dans le `spec.js` neuf (défaut : clé `formules` de `config.json`, sinon `grandes`).

**Texte riche** : `$…$` formule en ligne, `**gras**`, `\n` retour à la ligne forcé, `[mots]{#id .classe}` morceau visable par les gestes. Classes : `kw` (mot-clé ambre gras), `tt` (gras, couleur de la carte), `grad` (dégradé du titre), `acc` (rose bfcours), `gras`, `it`, `doux`, ou un nom de couleur. `decoupe: 'p'` + `'Si deux droites | [sécante]{.kw} | …'` crée les morceaux `p1`, `p2`… ; un morceau ne se coupe pas en fin de ligne. **Nombres** : à l'intérieur d'une formule (fractions, calculs), en TeX (`$0{,}04$`). Les nombres mis en valeur seuls (cases de tableau, cartes « 40 % », compteur, résultat encadré, clone volant) sont en Atkinson gras comme dans le moteur HTML, zéro barré compris. Cases, compteurs et clones `html:` utilisent les chiffres tabulaires (`tab: true`, famille `AtkinsonT`) : le `1` a la largeur des autres chiffres. `tab: true` s'hérite des conteneurs et se met sur n'importe quel texte.

**Figure** (en-tête de `moteur-canvas/figure.js` pour le détail) : `vue: [x, y, l, h]` (comme un viewBox), `points: { A: [455, 70] }`, `objets` :
`segment: ['A', 'B']` (`t: [0, 1.2]` prolonge ; `main: [4, -3]` = tracé à main levée) · `droite` (d'un bord à l'autre de la vue) · `demi` · `angle: ['C', 'A', 'I'], r` (arc de C vers I, sens horaire à l'écran) · `secteur` (rempli) · `droit` (codage d'angle droit) · `egal: ['A', 'B'], n` (codage de longueurs) · `bande: [['A', 'I'], ['B', 'C']]` · `polygone` · `cercle` · `point` · `chemin: 'M… A… Z'` (chemin SVG quelconque, ex. courbe de fonction calculée dans spec.js) · `etiquette: 'A', en: [x, y]` (TeX centré en ce point, **sans `$`** : un `$` est une erreur ; `rotation: 34.5` en degrés pour poser une cote le long d'un segment, sens horaire à l'écran). Style : `couleur`, `epaisseur` (5), `remplir`, `opacite`, `pointilles: [a, b]`, `bout: 'butt'`. Chaque objet porte un `id` et se vise comme un élément.

## Tuiles algébriques

Trois éléments dessinent des tuiles (conventions de mathsbot.com et des tuiles plastifiées) : unité jaune « 1 », x verte, x² bleue, y violette, y² rose, xy orange, **toute tuile négative rouge** (étiquette « −1 », « −x », « −x² » avec le vrai signe moins). Les couleurs sont des couleurs d'objet : identiques en thème `nuit` et `jour`. Exemple validé : `assets/exemples/tuiles-canvas/`. Gestes : `references/gestes.md` § Tuiles algébriques.

| Élément | Exemple | Ids générés |
|---|---|---|
| tuiles | `{ tuiles: '3x2 -2x +4', id: 'a' }` | tuiles `a-1`, `a-2`… dans l'ordre ; classe `.a-tuiles` (toutes) ; `a` = le groupe |
| produit | `{ produit: { haut: 'x +3', gauche: '2' }, id: 'p' }` | facteurs `p-h1…` (haut) et `p-g1…` (gauche) ; produits `p-l1c2` (ligne 1, colonne 2) ; classes `.p-haut`, `.p-gauche`, `.p-produits` |
| tapis | `{ tapis: { gauche: 'x +2', droite: '5' }, id: 'm' }` | groupes `m-g` et `m-d` ; tuiles `m-g-1…`, `m-d-1…` ; classes `.m-g-tuiles`, `.m-d-tuiles` |

**Écriture des tuiles** (chaîne ou tableau de chaînes) : un jeton = signe facultatif, nombre de tuiles facultatif, variable. `'2x2 -x2 3x -2x y xy 4 -3'` : `x2` (ou `x²`, `x^2`) est le carré, `xy` le rectangle, un entier seul des unités (`4` = quatre « 1 », `-3` = trois « −1 »). Pour 3 tuiles x puis 2 unités, écrire `'3x +2'` (`3x2` serait 3 tuiles x²). Une tuile x ou y se met à la verticale avec `|` (`'2x|'`) ou pour tout le groupe avec `vertical: true`. Un tableau accepte aussi des objets `{ t: 'x', neg: true, vertical: true, vide: true, id: 'mon-id' }`.

| Option | Effet |
|---|---|
| `taille` | côté de l'unité u en px (80 ; ≈ 40 px en 540p) |
| `ecart`, `ecartV` | espace entre tuiles (8) ; `colonnes: n` range par n tuiles, sinon une seule rangée qui passe à la ligne si elle ne tient pas (`retour: false` pour l'interdire) |
| `alignV` | `centre` (défaut), `bas`, `haut` : alignement des tuiles de tailles différentes dans une rangée |
| `vide: true` | emplacement : contour pointillé sans remplissage (cible d'un `deplace`) |
| `rapportX`, `rapportY` | longueur de x et de y en unités (3,2 et 0,7 × rapportX) |
| `align` | `centre` par défaut (le bloc garde sa taille naturelle) |

- **produit** : cadre en L (facteurs sur le bord haut et le bord gauche, 1, x ou y seulement) et, dans le rectangle, **une tuile produit par case**, de signe calculé (− fois − = +), posée sur un emplacement pointillé. Les tuiles produits ne sont pas peintes tant qu'un geste d'entrée ne les a pas fait apparaître (c'est le cas de tout élément dont le premier geste est une entrée). Options : `cadre` (14, espace facteurs / intérieur), `ecart` (0, tuiles jointes), `guide: false` (sans pointillés), `signe: false` (sans le « × » de l'angle). Factorisation : faire apparaître d'abord l'intérieur (`.p-produits`), puis les facteurs.
- **tapis** : fond arrondi coupé par un trait vertical, signe « = » au milieu, un groupe de tuiles de chaque côté (rangées centrées dans chaque moitié). Options : `l` (largeur, défaut = zone), `hMin` (hauteur minimale, 300), `marge` (36), plus `taille`, `ecart`, `rapportX`… transmis aux deux groupes.
- **Réglage de capsule** (facultatif, clé `tuiles` de `CAPSULE`) : `tuiles: { couleurs: { un: '#ffd21f', x: '#d6249f', x2: '#2fb34a', y, y2, xy, negatif: '#e5322d' }, rapportX: 5.6, taille: 80 }`. Chaque couleur est un fond (`'#…'`) ou `{ f, b, t }` (fond, bordure, étiquette) ; bordure et étiquette sont déduites du fond sinon. Pour suivre MathBits : `x` magenta, `x2` vert, `rapportX: 5.6`.
- **Pièges** : ne pas mettre `visible: false` sur un groupe de tuiles (toutes les tuiles disparaîtraient) ; faire entrer les tuiles par un geste. Les ids `a-1`… comptent dans l'unicité des ids. Les tuiles se dessinent directement (sans image mémorisée) et collent aux pixels de la vidéo : les bords communs de deux tuiles jointes coïncident.

## Macros TeX et sous-parties

- Couleurs du thème : `\violet{…}`, `\cyan{…}`, `\ambre{…}`, `\rose{…}`, `\vert{…}`, `\corail{…}`, `\bleu{…}`, `\texte{…}`, `\doux{…}` (aussi `\textcolor{ambre}{…}`). Elles suivent le thème nuit ou jour.
- `macros: { BAC: '\\cyan{\\widehat{BAC}}' }` : une couleur sémantique par objet, écrite une seule fois.
- **Parallélisme** : `\para` et `\parallel` affichent « // » (règle fixe de `rigueur.md`, 14 bis), avec l'espacement d'une relation : `(AB) \para (CD)`.
- **Viser un nombre dans une formule** : `\cssId{dv2}{140^\circ}` crée la sous-partie `#dv2`, que visent `vole`, `montre`, `tombe`, `allume`, `entoure` ; une sous-partie cible de `montre` reste à sa place (la formule ne bouge pas) et part cachée. Une ligne de calcul révélée membre par membre s'écrit en une formule : `'\\cssId{c1a}{\\CAI}\\cssId{c1m}{-}\\cssId{c1b}{\\BAC}'`.

## Gestes

Catalogue complet, ancres et pièges : **`references/gestes.md`**. En plus des gestes de l'ancien moteur : `C.trace`, `C.apparait`, `C.clignote` (figures) et `C.zoom` (image). Raccourci : un élément peut porter son geste, `{ texte: '…', montre: '@b03~"codage"' }` ou `montre: ['@b03', { y: 20 }]` (montre, ecrit, tombe, cache, apparait, trace, pulse, surligne, compte). Garder les gestes enchaînés dans `gestes(C)`, dans l'ordre du script : c'est plus lisible pour une relecture.

## Échappatoires JS (cas rares)

- `C.tl.to(C.etat('#x'), { x: 120, rotation: 8 }, C.a('@b05'))` : tween sur l'état d'un élément.
- `C.ajouter((ctx, E, s, t) => { … })` : élément dessiné à la main au-dessus des scènes ; `C.boite('#id')` donne sa boîte (repère 1920×1080).
- `{ dessin: (ctx, boite, t, { couleur, theme, z }) => { … }, l, h }` : élément personnalisé dans la mise en page.
- `C.surSeek(t => …)` : effet continu, fonction pure du temps ; `C.hasard(graine)` pour le hasard.

## Pièges connus

- **Aucune horloge** : ni `Date`, ni `Math.random`, ni `setTimeout` dans `spec.js` (sinon les workers ne dessinent plus les mêmes images).
- **ids uniques**, y compris ceux de `\cssId` et les ids générés (`p1`… de `decoupe`, `tab-l1c2`) : un doublon est une erreur bloquante.
- **Espacement autour d'un signe isolé dans `\cssId`** : `\cssId{z2}{\parallel(AI)}` perd l'espace avant « // » ; écrire `\cssId{z2}{{}\parallel(AI)}`.
- **Fractions dans un calcul** : `hauteurLigne` ≥ 64 pour que deux lignes à fraction ne se touchent pas, et `ecart: [10, 14]` ; jamais `ecart: [x, 0]`, qui colle le « = » aux deux membres (« RS²=RI² »).
- **`\vert{` est la couleur verte**, pas la barre `\vert` de TeX : pour une barre, écrire `|` ou `\lvert`.
- **Une carte a une clé `titre`** (étiquette) et peut avoir une clé `puce` : le type est donné par la première clé de conteneur (carte, methode, encadrer, resultat, ligne, colonne, pile, figure, calcul, tableau…).
- **Couleur d'un texte vs d'une formule** : `couleur` sur un `texte` ne colore pas les formules voisines ; pour une étiquette colorée de carte, `{ texte: 'Total samedi', couleur: 'cyan' }`.
- **Compteur** : le contenu de l'élément est la valeur FINALE (`{ tex: '\\mathbf{600}' }`) : elle réserve la place ; le compteur l'écrit de gauche à droite.
- **Contenu centré dans une carte** : `alignEnfants: 'centre'` sur la carte.
- **Tracés et halos persistants** (`entoure`, `encadre`, `fleche`, `allume`) : donner `jusque` quand l'étape change. Un `jusque` qui ne suit pas le début du geste (halo jamais visible ou figé) est une **erreur** qui bloque la planche et le rendu.
- **Aperçu** : un saut de plus de 20 s dans la barre de lecture ne rejoue pas les images intermédiaires ; un détail d'état peut différer du rendu à cet instant. La vidéo et `--images` sont exacts.

## Limites (09/10/2026)

- `compacte` ne réarrange pas une `ligne` ni un `tableau` (la hauteur ne se propage que dans les colonnes et les cartes).
- Le compteur garde la place de sa valeur finale (l'ancien moteur décalait le texte voisin pendant le comptage).
- Les ondes fines de `tombe` peuvent paraître tremblées à 220 kb/s (compression) ; monter `--debit` si besoin.
- Les capsules à `scenes.js` restent du ressort du skill `capsule-video-html`.
