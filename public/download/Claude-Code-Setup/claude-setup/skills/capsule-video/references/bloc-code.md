# Blocs « tutoriel logiciel » : code qui s'écrit, terminal, compilation

Plugin du moteur canvas, **chargé à côté** : `assets/plugins-canvas/blocs.js` (+ police JetBrains Mono, licence OFL). Il s'enregistre dans les tables ouvertes du moteur (`CV.CLES`, `CV.TYPES`, `CV.GABARITS`) et enveloppe `CV.creerGestes` ; `moteur-canvas/` n'est pas modifié (donc `maj_moteur.py` reste sans effet sur lui).

## Installer dans une capsule

```bash
$PY .claude/skills/capsule-video/scripts/installer_blocs.py "<capsule>"
```

Copie `plugins-canvas/` dans la capsule et ajoute **une ligne de chargement en tête de `spec.js`** (idempotent). Cette ligne charge le plugin dans la page, l'aperçu et les workers de rendu. Exemple validé : `assets/exemples/blocs-demo/` (frappe sur les mots, terminal, compile, voix mixtes).

## Gabarits

| Gabarit | Zones (x, y, l × h) |
|---|---|
| `code-rendu` | `bandeau` · `code` (40, 134, 1060 × 896) · `rendu` (1130, 134, 750 × 896) |
| `code-terminal-rendu` | `bandeau` · `code` (40, 134, 1060 × 590) · `terminal` (40, 748, 1060 × 282) · `rendu` (1130, 134, 750 × 896) |

Pour le rendu, une `pile` { carte « le rendu apparaîtra ici » ; image } : la compilation remplace l'attente par l'image (voir la démo).

## Élément `code` (éditeur façon VS Code)

```js
{ id: 'ed', h: 590, taille: 36, fichier: 'cours.typ', langage: 'typst',
  code: `
    #set text(lang: "fr")
    = Fonctions affines
    $ f(x) = 2 x + 1 $
  `,
  frappe: [ { lignes: [1, 2], de: '@b02+0.2', a: '@b02~"langue".fin' },     // lignes 1 à 2 tapées entre deux ancres
            { lignes: 3, de: '@b04~"dollars".fin', a: '@b04~"un".fin' } ],
  surlignage: [ { lignes: 2, de: '@b02~"langue"', jusque: '@b02.fin' } ],   // bande jaune, fondu entrée et sortie
  regard: [ { t: '@b09', ligne: 12 } ] }                                     // défilement imposé (sinon automatique)
```

- **Frappe** : caractère par caractère, rythme humain déterministe (pause aux retours à la ligne, indentation instantanée), curseur, numéro de ligne actif, « Ln, Col » de la barre d'état. `de` obligatoire, `a` facultatif (sinon `vitesse` caractères/s, 14). Une ligne sans frappe est visible dès le début ; une ligne avec frappe apparaît à son premier caractère, les suivantes descendent.
- **Défilement** : automatique pour suivre le curseur quand le code dépasse la fenêtre (lissé, fonction du temps) ; `regard` impose une ligne.
- **Lisibilité** : `taille` (32 par défaut) est **réduite toute seule** pour que la ligne la plus longue tienne (jamais sous 18 px) : en 1080p viser ≤ 45 colonnes pour une fenêtre de 1060 px. `h` = hauteur de la zone (toujours la donner).
- **Langages** : `typst` (`#fonction`, mots-clés `#set` `#show` `#let`, chaînes, commentaires, maths `$…$`, titres `=`, listes, `*gras*`, `<label>`, `@ref`, crochets colorés par profondeur), `latex`, `bash`, sinon texte brut. `clair: true` = palette Light+. `numeros: false`, `curseur: false`, `branche`, `statut`, `statutInitial` ajustent la fenêtre.
- Écrire le code entre apostrophes inversées : première ligne vide et indentation commune retirées.

## Élément `terminal`

```js
{ id: 'term', h: 282, taille: 30, invite: '$',
  terminal: [ { cmd: 'typst compile cours.typ', de: '@b05~"je"', a: '@b06~"terminal".fin' },   // commande tapée
              { sortie: 'Compilation…', t: '@b06~"confirme"' },                                // ligne grise (ou plusieurs avec \n, `cadence` s entre lignes)
              { ok: 'cours.pdf prêt en 0,4 s', t: '@b06~"fichier"' } ] }                       // ligne verte avec coche dessinée (`erreur` : croix rouge)
```

Les sorties défilent quand elles dépassent la hauteur (lissé). Sans `h` : hauteur naturelle (≤ 420).

## Geste `compile`

```js
C.compile('#ed', '@b06~"fichier"', { rendu: '#rendu', remplace: '#attente', zoom: { a: 1.3, fx: 0.3, fy: 0.5, dur: 2.2 } });
```

Flash vert sur l'éditeur, pastille « Compilation… » puis « ✓ Compilé » dans la barre d'état, grande coche qui se dessine ; 0,5 s plus tard (`delai`) l'image `rendu` apparaît (elle part cachée), `remplace` fait disparaître l'attente, `zoom` lance un zoom lent (`C.zoom` : `a`, `fx`, `fy`, `dur`, `apres` = délai avant le zoom, 1 s). Plusieurs compilations possibles dans le même éditeur (chacune avec son `rendu` et son `remplace`). **Le PNG du rendu doit être un vrai rendu** (typst, compilateur du logiciel montré) ; zoomer en gardant les bords du texte dans la fenêtre (`fx` décale le pivot).

Option `fondu: true` (ou une durée en s) : changement d'image sans recréer le panneau. `remplace` (ancien rendu) et `rendu` (nouveau) se fondent l'un dans l'autre au même endroit, sans glissement ni zoom d'entrée. Pour revenir à une image déjà montrée, la déclarer une seconde fois dans la `pile` (autre `id`).

## Éditer le code sur place : `remplace`, `efface`, `insere`

```js
C.remplace('#ed', '@b01~"abord"', { ligne: 3, ancien: 'prop', par: 'monrose', a: '@b01~"rose".fin' });   // effacement lettre à lettre au curseur, puis frappe
C.remplace('#ed', '@b02~"ensuite"', { ligne: 3, ancien: 'monrose', par: 'red', mode: 'selection' });     // sélection bleue, puis frappe
C.efface('#ed', '@b03~"on"', { lignes: 2 });                 // ligne 2 repliée (bande rouge), les suivantes remontent ; { lignes: [2, 4] } pour une plage
C.efface('#ed', t, { ligne: 3, ancien: 'prop' });            // portion d'une ligne effacée au curseur
C.insere('#ed', t, { apres: 3, code: '#set text(lang: "fr")', tape: false });   // ligne(s) ouverte(s) après la ligne 3 (0 = en tête), bande verte ; tape: true ou a/vitesse = frappée
C.compile('#ed', '@b01.fin', { rendu: '#r1', remplace: '#r0', fondu: true });
C.verifieCode('#ed', 8.2, `…texte exact attendu à cet instant…`);
```

- **Numéros de ligne** : ceux du texte AFFICHÉ à l'instant du geste (lignes insérées comprises, lignes effacées exclues). `frappe`, `surlignage` et `regard` gardent la numérotation du `code` initial.
- **Cible dans la ligne** : `ancien` (+ `occurrence: 2` pour la deuxième), ou `cols: [c1, c2]` (colonnes 1-based, bornes incluses ; `[c, c-1]` = insertion pure), ou rien = toute la ligne. `par` : nouveau texte (`''` = suppression).
- **Durée** : `a` (ancre de fin) ou `dur` ; sinon effacement 24 car/s, pause 0,12 s, frappe 13 car/s (`vitesse`, `vitesseEfface`). `mode: 'selection'` met en bleu l'ancien texte (0,45 s) avant de le remplacer par la frappe. La coloration suit chaque état intermédiaire (la ligne est colorée seule, sans le contexte multi-lignes).
- **`insere`** : `code` commençant par un retour à la ligne = bloc nettoyé comme `code` (indentation commune retirée) ; sinon texte pris tel quel.
- **Vérifications** (l'erreur arrête le rendu, comme les autres) : `remplace` dont la cible est introuvable (message avec le texte de la ligne), ligne hors du code, éditions qui se chevauchent sur une ligne, édition avant la fin de la frappe ; clé `attendu: \`…\`` de l'élément `code` = texte final exact ; `C.verifieCode` = texte exact à un instant donné ; contrôle interne calculé/affiché.
- **Largeur** : la taille de police est calculée avant les gestes. Si une ligne s'allonge, la déclarer via `attendu` ou `colonnes: 45` sur l'élément `code`.
- Hauteur : prévoir `h` pour le nombre de lignes MAX affichées (sinon défilement automatique).
- `C.remplace` existe aussi dans le moteur (bascule de pile `a`, `b`, `t`) : le moteur garde ce comportement dès que la cible n'est pas un élément `code` ; alias explicite `C.codeRemplace`.
- Déterminisme : tout est fonction de `t` (mêmes images à n'importe quel `seek`). Exemple : `assets/exemples/blocs-demo-edition/` (prop → monrose → red → prop, 8 s, voix Piper tom).

## Geste `badgeVoix`

`C.badgeVoix({ voix: 'tom', texte: 'Voix de synthèse' })` : badge (3 barres d'onde animées) visible seulement pendant les temps forts dont le champ `voix` vaut `tom` (fournis par `assembler_voix.py`, voir `voix-mixtes.md`). Ne pas combiner avec `mention:`.

## Rendre en 1080p

`$PY $S/rendre_canvas.py "<capsule>" --images 6,16,23` (planche, 3 s) puis `--qualite projection` → `capsule.mp4`. La démo (27 s) : 826 images en 8 s.

## Pièges et limites

- Les clés de l'élément `code` ne doivent pas reprendre un raccourci de geste du moteur : c'est `surlignage` (pas `surligne`, qui lancerait `C.surligne`).
- Écrire **avant** de compiler : le rendu ne reflète que le dernier état ; le plugin ne compile rien, il filme.
- Pas d'autocomplétion, de sélection libre à la souris, d'annulation ni de plusieurs curseurs. Une seule édition à la fois par ligne, une seule frappe active pour le curseur (le plus récent gagne). Les éditions ne portent que sur une ligne (pas de remplacement à cheval sur deux lignes : `efface` des lignes puis `insere`).
- Police JetBrains Mono « latin » : accents français et ponctuation courante, pas de ✓ ni d'émojis (coches dessinées).
- `maj_moteur.py` n'actualise pas le plugin : relancer `installer_blocs.py` après une évolution de `assets/plugins-canvas/`.
