# Animations 3D three.js dans une capsule (plugin « trois »)

Plugin du moteur canvas, **chargé à côté** comme le plugin « blocs » : `assets/plugins-canvas/trois.js` + `three.min.js` (three.js r159, build classique UMD, licence MIT, `THREE-LICENSE`). `moteur-canvas/` n'est pas modifié (`maj_moteur.py` reste sans effet sur lui).

## Installer dans une capsule

```bash
$PY .claude/skills/capsule-video/scripts/installer_trois.py "<capsule>"
```

Copie `three.min.js`, `trois.js` et la licence dans `<capsule>/plugins-canvas/` et ajoute **une ligne de chargement en tête de `spec.js`** (`chargeur-trois.txt`, idempotent). Elle charge three.js puis trois.js dans la page, l'aperçu **et les workers de rendu**. Compatible avec `installer_blocs.py` (deux lignes indépendantes ; ce dernier ne copie plus three.js). La ligne neutralise le `console.warn` de dépréciation de three.min.js le temps du chargement, puis le rétablit.

Exemple complet : une frise de 15 époques et 22 temps forts, 4 min 36 (non fournie dans le skill).

## Principe

Un `OffscreenCanvas` WebGL dédié par vue, à la **taille réelle du rendu** (960×540, 1280×720 ou 1920×1080 selon `--qualite`), `THREE.WebGLRenderer({ alpha: true, antialias: true })`, recopié par `ctx.drawImage` dans la toile 2D. La scène est construite **une seule fois** (à la première image dessinée, donc dans chaque worker), puis `maj(t)` la positionne en fonction de `t` seulement, et elle est rendue.

## API

```js
gestes(C) {
  // 1) fond plein écran, SOUS les cartes 2D (dessiné juste après le fond nuit)
  C.trois({ scene3d: (THREE, scene, camera, o) => {
    o.eclairer(scene);                                   // ambiante + 2 directionnelles
    const cube = new THREE.Mesh(new THREE.BoxGeometry(2, 2, 2), o.mat('#22d3ee'));
    scene.add(cube);
    camera.position.set(0, 2, 8); camera.lookAt(0, 0, 0);
    return t => { cube.rotation.y = t; };                // maj(t) : tout est fonction de t
  } });                                                  // options : fov, opacite: t => 0..1, dessus: true (au-dessus des scènes), antialias: false
}
// 2) élément dans une zone de mise en page
{ scene3d: (THREE, scene, camera, o) => maj, l: 800, h: 600, id: 'vue', rayon: 24 }
```

`scene3d(THREE, scene, camera, o)` renvoie obligatoirement la fonction `maj(t)`. `o` fournit :

| Clé | Rôle |
|---|---|
| `o.hasard(graine)` | générateur déterministe (jamais `Math.random`) |
| `o.couleur('cyan')`, `o.col('cyan')` | couleur du thème en CSS / en `THREE.Color` (les couleurs sémantiques de la capsule) |
| `o.ease` | `etape(t, t0, t1)` (0..1), `lisse`, `entree`, `sortie`, `rebond`, `lerp`, `borne` |
| `o.texte(chaine, { hauteur, couleur, police, gras, lueur })` | plan portant un texte (texture canvas, accents et π corrects, police Atkinson ou `police:` au choix) |
| `o.lueur(couleur, taille, opacite)` | halo additif (sprite) |
| `o.mat(couleur, opts)`, `o.verre(couleur, opacite)`, `o.eclairer(scene)` | matériaux lumineux sur fond sombre, éclairage |
| `o.k`, `o.L`, `o.H`, `o.vue.px/py` | échelle du rendu (0,5 en 540p), taille de la vue, taille en pixels |
| `o.C`, `o.a` | l'objet de gestes et la résolution des ancres (voir ci-dessous) |

**Ancres** : la fonction `scene3d` s'exécute à la première image, trop tard pour que les ancres signalent leurs erreurs. Résoudre toutes les ancres **dans `gestes(C)` avant** `C.trois`, dans un objet `T`, que la fonction utilise par fermeture :

```js
const T = { b10_pi: C.a('@b10~"pi"'), b11_tiers: C.a('@b11~"tiers"') };
C.trois({ scene3d: (THREE, scene, camera, o) => { …  t > T.b10_pi …  } });
```

Une ancre introuvable est ainsi refusée au rendu comme toute autre. Mêmes écritures qu'ailleurs (`'@b10~"Archimède"'`, `'@b10.fin'`).

## Déterminisme

`maj(t)` est une fonction pure : pas d'horloge, pas de `Math.random`, pas d'état qui s'accumule d'une image à l'autre (chaque worker saute à sa tranche sans pré-rouler le dessin, seul `seek` est pré-roulé). Pour une animation « jusqu'à un état final » (dés qui se posent) : état final exact à `e = 1`, jamais une simulation. `performance.now()` sert uniquement aux statistiques (`CV.TROIS.stats`).

## Pièges rencontrés

- **Texte 3D** : Atkinson barre les zéros et n'a pas π ni √ ; pour des chiffres ou des symboles, passer `police: "'Segoe UI', Arial, sans-serif"` ou `"'Times New Roman', serif"`.
- **Lignes** : `THREE.Line` fait 1 pixel quelle que soit `linewidth` (WebGL). Pour un contour visible, `TubeGeometry` sur un `CurvePath` de `LineCurve3` (polygone) ou sur une courbe (tracé de fonction).
- **Étoiles** : `PointsMaterial` avec `sizeAttenuation: false` et `size: 5 * o.k` (taille en pixels de sortie, identique de 540p à 1080p).
- **Éclairage** : depuis r155, les lumières sont physiques ; `MeshStandardMaterial` sombre sans émission paraît noir. `o.mat` ajoute une émission (0,35) : l'objet reste lisible sur le fond nuit.
- **Brouillard** : `scene.fog` de la couleur du fond estompe le lointain ; l'élargir (`near`, `far`) pour une vue d'ensemble.
- **Taille apparente** : à 12,8 unités de distance et 45° de champ, la hauteur visible fait ≈ 9,6 unités (112 px par unité en 1080p) ; prévoir les objets dans ±3 unités. Décaler le sujet à droite d'une carte 2D avec `camera.setViewOffset(W, H, -0.18 * W, 0, W, H)` (W, H = `o.vue.px/py`), pas en déplaçant la caméra.
- **Objets de taille croissante** : une échelle liée à l'éloignement de la caméra doit être retardée (`1 + 0,8 G²`) sinon les objets grossissent pendant que la caméra les quitte.
- **Rayons verticaux** (jalons) : ils traversent les objets vus de près ; ne les montrer qu'en vue d'ensemble.
- **Échecs** : si WebGL échoue (contexte perdu, pas de WebGL), le worker lève une erreur et le rendu s'arrête (jamais de vidéo noire silencieuse). Dans l'aperçu et la planche, l'erreur est dans la console et la 3D est absente.
- **Gabarit `plein` + zones** : cartes en `pile` dans une zone personnalisée à gauche, 3D à droite.
- Éviter d'écrire du code JS avec antislashs par Bash : Write/Edit (le hook refuse les heredocs).

## Coûts mesurés (20/10/2026, RTX 3060 portable, Vulkan, 540p)

| Capsule | Durée | Rendu pur | Débit |
|---|---|---|---|
| frise 3D complète (15 objets, ruban, 650 étoiles, 8 315 images) | 4 min 37 | 31,3 s (total 35,5 s) | 266 images/s |
| même capsule, un seul cube en fond | 4 min 37 | 22,4 s | 372 images/s |
| référence sans 3D (exo5, 2D seule) | 3 min 50 | 16 s | ≈ 400 images/s |

Temps de dessin par worker : 2,8 s (cube) contre 8,8 à 12 s (frise) ; l'encodeur H.264 reste le goulot, donc la 3D n'ajoute que ≈ 50 % au total. Planche d'un instant : 3 à 5 s. Mémoire de pointe 0,72 Go (contre 0,6).

Modes graphiques : `--gpu vulkan` (défaut auto) et `--gpu intel` (Direct3D 11) rendent la 3D ; `--gpu logiciel` (SwiftShader) aussi, en planche (≈ 1,4 fois plus lent). Les trois ont été essayés en planche : mêmes images.

## Rendu par défaut d'une capsule 3D : 720p + finition x264 (20/10/2026)

L'encodeur H.264 du navigateur (WebCodecs, logiciel) compresse mal les dégradés et lueurs de la 3D. `rendre_canvas.py` détecte donc le plugin trois dans `spec.js` et, sans option :

- prend la qualité `envoi` (720p) au lieu de 540p ;
- applique `--finition x264` : rendu intermédiaire à haut débit (≈ 6000 kb/s en 720p), puis deux passes x264 `fast` / `animation` au débit vidéo de la qualité (ou de `--debit`), audio copié. Fichier intermédiaire et journaux de passe supprimés à la fin.

`--finition aucune` rétablit l'encodeur du navigateur seul ; `--finition x264` l'impose à une capsule 2D. Les capsules 2D restent en 540p, sans finition.

Mesure sur la frise 3D (4 min 37, 720p) :

| Rendu | Débit vidéo | SSIM | Taille | Temps |
|---|---|---|---|---|
| encodeur du navigateur seul | 363 kb/s | 0,969 | 15,9 Mo | 52 s |
| intermédiaire à 6000 kb/s + x264 fast 2 passes au même débit | 363 kb/s | 0,987 | 16,0 Mo | 47 s + 35 s |

Même poids, qualité nettement meilleure. Le rendu intermédiaire pèse ≈ 174 Mo (prévoir la place dans le dossier de la capsule).

## Limites

- Une `WebGLRenderer` par vue : prévoir peu de vues simultanées (le fond plein écran + 1 ou 2 éléments).
- Pas de physique ni d'ombres portées ; tout est fonction de `t`.
- `maj_moteur.py` n'actualise pas le plugin : relancer `installer_trois.py` après une évolution de `assets/plugins-canvas/`.
