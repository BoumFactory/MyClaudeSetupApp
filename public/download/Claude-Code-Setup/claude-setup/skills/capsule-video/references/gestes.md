# Catalogue des gestes (moteur canvas)

Tous les gestes s'écrivent `C.geste(cible, t, options)` dans `gestes(C)` de `spec.js`. Mêmes noms, options et ancres que l'ancien moteur HTML : un `scenes.js` se porte geste pour geste.

- **cible** : `'#id'` (ou `'id'`), `'.classe'`, ou tableau (`['#a', '#b']`). L'id peut désigner un élément, un **morceau de texte** `[mots]{#id}`, une **sous-partie de formule** `\cssId{id}{…}`, un **objet de figure**, une **case de tableau** (`'#tab-l1c2'`, la case entière ; le nombre qu'elle contient garde son propre id).
- **t** : spécification de temps, résolue par `C.temps` (code repris tel quel de l'ancien moteur, `moteur-canvas/ancres.js`) :

| Écriture | Sens |
|---|---|
| `'#147'` | début du mot 147 (index de `mots.py`) |
| `'#147.fin'` | fin du mot 147 |
| `'#147+0.3'`, `'#147.fin-0.2'` | décalage en secondes |
| `'"150"@60'` | premier mot « 150 » après 60 s (recherche sans accents ni ponctuation ; plusieurs mots possibles) |
| `'@b10'`, `'@b10.fin'` | début / fin du temps fort `b10` (mode voix de synthèse, `data/temps-forts.js`) |
| `'@b10~"fait"'` | le mot « fait » à l'intérieur du temps fort b10 ; `'@b10~"fait"2'` = 2e occurrence ; `'@b10~"ça fait".fin+0.1'` |
| `12.5` | secondes brutes (à éviter : ne suit pas la voix) |

**Voix de synthèse : ancrer en `@id~"mot"`, jamais en `#index`.** Le même `spec.js` sert alors pour plusieurs voix (débits différents). Préférer des mots ordinaires (« fait », « soit », « reste », « sachant », « carte ») : Whisper écrit les nombres en chiffres (« 75% », « 4 ») et déforme les notations (« P2C » pour « P de C »). Vérifier les mots réels avec `mots.py` avant d'ancrer.

Anticiper de 0,1 à 0,3 s (`'#153-0.2'`) les gestes longs, pour que l'élément soit lisible au moment où le mot sonne.

**État de départ automatique** : un élément dont le premier geste est une entrée (montre, tombe, ecrit, trace, apparait, remplace, compte, cible de vole) part caché ; les autres sont visibles dès l'ouverture de leur scène. `visible: false` force le départ caché.

## Apparitions et sorties

| Geste | Effet | Options |
|---|---|---|
| `montre(c, t)` | glisse + zoom léger, apparition | `dur`, `y`, `scale`, `stagger`, `ease` |
| `cache(c, t)` | disparition | `dur`, `y`, `stagger` |
| `tombe(c, t)` | **chute avec rebond** + onde à l'impact : le nombre « tombe à sa place » | `hauteur` (260), `rotation`, `stagger`, `couleur` (de l'onde), `onde:false` |
| `ecrit(c, t)` | dévoilement gauche → droite (écriture) | `dur` (0,9) |
| `scene` | changement de scène plein écran (fondu flou) : clé `debut` de la scène dans `spec.js` | |
| `remplace(a, b, t)` | `a` sort vers le haut, `b` entre au même endroit (étapes d'une `pile`) | |
| `compacte(details, resume, t)` | les lignes `details` se replient (contenu rogné, hauteur → 0) ; tout ce qui suit remonte et les cartes traversées rétrécissent ; le résultat est rangé dans `resume` (morceau d'en-tête, AU-DESSUS des détails) | `depuis` (élément qui vole vers `resume`), `couleur`, `dur` |
| `compte(c, t)` | compteur animé, virgule décimale française ; sur une formule `{ tex: '\\mathbf{250}', gras: true }` (contenu final = place réservée), dégradé et lueur possibles | `de`, `a`, `dur`, `decimales` |
| `trace(c, t, dur)` | un objet de figure se dessine | `dur` (0,7), `ease` |
| `apparait(c, t, dur, vers)` | fondu vers une opacité (secteur qui se colore ; `vers: 0` efface) | |
| `clignote(c, t, n, bas)` | n clignotements jusqu'à l'opacité `bas` | |
| `zoom(c, t, o)` | zoom lent dans une image (« Ken Burns ») | `a` (1,15), `dur` (8), `fx`, `fy` (point fixe, 0–1) |

## Désigner, relier, célébrer

| Geste | Effet | Options |
|---|---|---|
| `vole(source, cible, t)` | **geste signature** : un clone du contenu de la source décolle en arc, grossit, et atterrit à la place de la cible (cachée jusqu'à l'atterrissage), avec rebond élastique et onde | `dur` (1,0), `arc`, `couleur`, `onde:false`, `tex` / `html` (le clone montre un autre contenu : `tex: '0{,}40'` pour « 40 % ») |
| `allume(c, t)` | halo lumineux autour d'un élément ou de l'**union** de plusieurs (ligne, colonne de tableau) ; renvoie les halos | `couleur`, `jusque` (t d'extinction), `chacun:true`, `marge` |
| `eteint(halos, t)` | éteint des halos renvoyés par `allume` | |
| `pointe(c, t)` / `pointe(null, t)` | pointeur lumineux qui se déplace (le doigt du professeur) / le retire | `fx`, `fy` (0–1 dans la boîte), `dur` |
| `pulse(c, t)` | pop élastique d'un élément visible | `scale` (1,18), `dur` |
| `secoue(c, t)` | « non ! » (erreur fréquente) | `dur` |
| `surligne(c, t)` | trait de surligneur fluo derrière un texte | `couleur`, `dur` |
| `entoure(c, t)` | ellipse tracée à la main | `couleur`, `marge`, `epaisseur`, `jusque` |
| `encadre(c, t)` | rectangle arrondi tracé (résultat final) | idem |
| `fleche(a, b, t)` | flèche courbe tracée de `a` vers `b` | `couleur`, `courbure` (±0,25), `jusque` |
| `onde(c, t)` | onde de choc circulaire | `couleur`, `taille` |
| `eclat(c, t)` | gerbe de confettis (résultat trouvé) | `n`, `force`, `couleurs`, `graine` |
| `focus(cs, t)` / `defocus(t)` | assombrit les éléments `focus: true` sauf `cs` / rallume tout | `dur` |

Couleurs : noms du thème (`'--violet'` ou `'violet'`, `cyan`, `rose`, `ambre`, `vert`, `corail`, `bleu`) ou toute couleur CSS.

## Tuiles algébriques

Éléments et ids : `references/moteur-canvas.md` § Tuiles algébriques. `montre`, `cache`, `tombe`, `allume`, `entoure`, `encadre`, `pulse`, `secoue`, `vole` marchent sur une tuile (`'#a-3'`) ou sur toutes (`'.a-tuiles'` avec `stagger`). Les gestes ci-dessous sont à écrire dans l'ordre chronologique : une tuile déplacée se souvient de sa position.

| Geste | Effet | Options |
|---|---|---|
| `deplace(c, cible, t)` | la tuile **glisse** (ce n'est pas un clone) jusqu'à `cible` : un id, une tuile, un groupe, ou `{ dx, dy }` (décalage depuis sa position actuelle) ; un tableau de cibles est apparié aux tuiles. Elle passe au-dessus de tout pendant le trajet | `dur` (0,8), `ancre` : `centre` (défaut), `fin` (à droite de la cible), `debut`, `dessus`, `dessous`, `coin` ; `ecart` (10), `dx`, `dy` (réglage fin), `retourne: true` (se retourne en route), `arc` (px de courbe), `stagger`, `rebond: false`, `ease` |
| `retourne(c, t)` | l'**opposé** : la tuile se met de chant, change de couleur et d'étiquette à mi-course (+1 ↔ −1, x ↔ −x), se rouvre ; vise aussi un groupe | `dur` (0,7), `stagger`, `vers: 'positif' \| 'negatif'`, `onde: true` |
| `annule(a, b, t)` | **paire nulle** : `b` glisse sur `a`, éclat et onde, flash blanc, les deux s'effacent ensemble ; tableaux appariés (`annule(['a-1','a-2'], ['a-4','a-5'], t)`) | `dur` (0,7), `stagger` (0,45), `zero: true` (pastille « 0 » à leur place ; une chaîne remplace le « 0 »), `tenue` (1 s), `couleur`, `etincelles: false`, `arc` |
| `ajoutePaire(cible, t)` | fait **apparaître** une paire nulle (+1 et −1 déclarés dans la spec, p. ex. `{ tuiles: '1 -1', id: 'z' }`, cible `'#z'`) : pop élastique, onde, pastille facultative | `zero` (pastille « 0 » au-dessus), `stagger` (0,15), `couleur`, `vers` (après `pause` s, les tuiles vont se ranger à la suite de cet élément : `vers: '#a'`), `ancre` (`fin`), `ecart`, `pause` (1,2) |

- **Soustraire ce qu'on n'a pas** (2 − 5) : `ajoutePaire` autant de fois que nécessaire (déclarer plusieurs paires, ou un groupe par paire), puis `deplace` des tuiles à ôter hors du tapis (`{ dx: 0, dy: -300 }`) suivi de `cache`.
- **Multiplier par −1** : `retourne` du groupe. **Passer à l'autre membre** : `deplace('#m-g-3', '#m-d', t, { ancre: 'fin', retourne: true })`.
- Les tuiles apparaissent par un geste d'entrée (`montre`, `tombe`) : ne pas les cacher par `visible: false` sur le groupe. Un `annule` n'est pas une entrée : les tuiles visées restent visibles jusqu'à l'annulation.
- Limites : le trajet d'une tuile soulevée ignore l'échelle ou le décalage de son groupe (ne pas déplacer le groupe lui-même en même temps) ; les halos `allume`/`entoure` visent la position d'origine, pas une tuile déjà déplacée.

## Outils

- `C.W(i)`, `C.W(i, 'fin')`, `C.cherche('texte', apres)`, `C.a(t)` : instants des mots.
- `C.un(c)`, `C.tous(c)`, `C.boite(c)` (boîte dans le repère 1920×1080).
- `C.tl` + `C.etat(c)` : effet sur mesure, `C.tl.to(C.etat('#x'), { x: 100, rotation: 8 }, C.a('#90'))` (état : x, y, scale, scaleX, scaleY, rotation, o, clip, trace).
- `C.surSeek(t => …)` : effet continu, fonction pure du temps.
- `C.ajouter((ctx, E, s, t) => {…})` : élément dessiné à la main au-dessus des scènes.
- `C.hasard(graine)` : générateur pseudo-aléatoire déterministe.

## Formules à trous (cibles de `vole`)

```js
{ tex: 'P(M)=\\dfrac{\\cssId{n1}{150}}{\\cssId{d1}{250}}' }
C.vole('#v-mt', '#n1', '#153', { couleur: '--violet' });   // 150 quitte le tableau pour le numérateur
```
La barre de fraction reste visible, les emplacements vides attendent leurs nombres : c'est très lisible.

## Pièges connus

- **Source de `vole`** : viser le nombre (`{ n: 105, id: 'v-mb' }` dans un tableau, ou une sous-partie `\cssId`), pas la case entière.
- **Tracés et halos persistants** : `entoure`, `encadre`, `fleche` et `allume` vivent au-dessus des scènes ; sans `jusque` (ou `eteint`), ils restent visibles après un changement d'étape ou de scène. Un `jusque` antérieur ou égal au début du geste est refusé (erreur « allume sur c1 : jusque … ne suit pas le début du geste ») : corriger l'ancre plutôt que d'obtenir un halo jamais visible.
- **`vole` avec `tex:` ou `html:`** : le clone provisoire n'est jamais peint à la place de la source (seul son sprite vole) ; sa taille suit la source, puis celle de la cible à l'arrivée.
- **Positions mesurées une seule fois**, à la construction : un tracé, un halo ou un pointeur ne suit pas un élément qui bouge ensuite (le zoom lent `zoom` déplace le contenu d'une image, pas sa boîte : on peut l'entourer).
- `tombe` remet `rotation` à 0 à l'arrivée.
- `id` uniques dans toute la capsule, y compris ceux de `\cssId`, de `decoupe` et des cases de tableau : un doublon est une erreur bloquante.
- Un élément visé par plusieurs `montre`/`cache` successifs : les écrire dans l'ordre chronologique.
- Les scènes s'enchaînent dans l'ordre du tableau `scenes` (clé `debut`).
- Emojis : rendus en couleur ; les garder décoratifs (jamais porteurs de sens mathématique).
