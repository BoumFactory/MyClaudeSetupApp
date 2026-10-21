# Mode voix de synthèse (« script d'abord »)

Quand il n'y a pas d'enregistrement : le texte est écrit d'abord, la voix est générée ensuite, l'animation se cale sur la voix. Tout est local et gratuit.

**Moteur par défaut : Pocket TTS** (Kyutai, `voix_pocket.py`, depuis le 20/10/2026) : voix du catalogue ou **voix clonée** (`cloner-sa-voix.md`), une voix par temps fort. **Piper** (`voix.py`) reste la voix de **secours** : instantané, mais plus mécanique.

## 1. Écrire le texte relaté : `<capsule>/script.md`

```
## b01 [pause 0.6]
Allez, on corrige l'exercice 5 ! Un tableau croisé, construit à partir d'un énoncé en pourcentages.

## b02 [pause 0.4]
Un magasin de sport interroge 600 clients. On a trois informations.
```

- Un temps fort = une idée = une phrase ou deux (5 à 15 s). Il devient l'unité d'ancrage et de régénération.
- `[pause s]` = silence APRÈS le temps fort : 0,3 entre deux données, 0,6 entre deux étapes, 1,0 avant une nouvelle question ou après un résultat.
- **Écrit pour l'oreille** : notations en toutes lettres (« P de S sachant C », jamais « P_C(S) »), pas de parenthèses, pas d'abréviations. Les nombres restent en chiffres : `voix.py` les dit (0,625 → « zéro virgule six cent vingt-cinq », 40 % → « quarante pour cent »). `relire_script.py` repère les notations restées dans le texte lu (`$`, `\frac`, `^`, `[AB]`, « triangle RIS »…) et **propose** la forme orale (`scripts/maths_parlees.py`) ; corriger le script soi-même (ou `--appliquer`), jamais de traduction silencieuse dans la chaîne audio : l'ancrage se résout sur les mots du script.
- Structure type d'une correction : rappel de l'énoncé (contexte, données une par une, événements), annonce des questions, puis chaque question (méthode → calculs → résultat → vérification ou interprétation).
- Ton : direct, enjoué, phrases courtes, interpellations (« Attention, c'est là le piège ! », « Regardez : … »). Le contenu mathématique suit exactement le corrigé validé (après la revue critique de `SKILL.md`) et les outils du programme du niveau.
- En tête du script, une section « Choix didactiques » (hors temps forts) consigne les choix de la revue critique : démarche retenue, vocabulaire ajouté.

### Rigueur orale (une vidéo peut être vue par un inspecteur)

L'oral doit désigner **exactement** l'écriture affichée, sans qu'on puisse la lire autrement.

| Écriture | Dire | Ne pas dire |
|---|---|---|
| $\dfrac{0+2}{2}$ | « 0 plus 2, le tout divisé par 2 » ou « la fraction de numérateur 0 plus 2 et de dénominateur 2 » | « 0 plus 2 sur 2 » (= $0+\frac{2}{2}$) |
| $\dfrac{x_A+x_B}{2}$ | « x A plus x B, le tout divisé par 2 » | « x A plus x B sur 2 » |
| $(x_B-x_A)^2$ | « x B moins x A, le tout au carré » ou « le carré de x B moins x A » | « x B moins x A au carré » |
| $\sqrt{x^2+y^2}$ | « la racine carrée de : x au carré plus y au carré » (petite pause après « de ») | « racine de x au carré plus y au carré » sans pause |
| $1-(-5)$ | « 1 moins, entre parenthèses, moins 5 » puis « soit 1 plus 5 » | « 1 moins moins 5 » |
| $(-3)^2$ | « moins 3, entre parenthèses, au carré » ou « le carré de moins 3 » | « moins 3 au carré » (= $-3^2$) |
| $x_D$, $y_I$ | « x D », « y I » (voix.py dit « i grec I ») | — |

Vocabulaire : des **droites** sont perpendiculaires, des **vecteurs** sont orthogonaux (« les droites O I et O J sont perpendiculaires : on dit que les vecteurs i et j sont orthogonaux ») ; une **longueur** se mesure, la **norme** est celle du vecteur ; « si, et seulement si » pour une équivalence ; nommer la propriété utilisée (« d'après la réciproque du théorème de Pythagore ») ; on calcule les **coordonnées** d'un vecteur, jamais « le vecteur » ; une conclusion nomme toujours ses objets (« les vecteurs E F et H G ont les mêmes coordonnées : ils sont égaux »), jamais un « Égaux : … » elliptique.

### Chaînes d'égalités (exigence du professeur, 03/10/2026)

- Une égalité se DIT avec « égale » : « La norme de u égale la racine carrée de : 3 au carré plus 4 au carré. Égale la racine carrée de : 9 plus 16. Égale la racine carrée de 25. Égale 5. » Jamais « soit », « ça fait », « c'est », ni un résultat jeté après deux-points (« : 5 ») pour enchaîner deux membres d'une égalité.
- Le calcul dit est celui de la copie : chaque phrase « Égale … » est un membre de la chaîne écrite à l'écran.
- Un calcul annexe (carré d'un négatif, somme de décimaux) s'annonce « Au brouillon : le carré de moins 5 égale 25. » AVANT la chaîne ; à l'écran il va dans l'encart Brouillon, jamais dans la chaîne.
- Équations : « 1 moins x D égale moins 5. On soustrait 1 des deux côtés : moins x D égale moins 6. » (une équation par ligne, l'opération dite) reste la forme correcte.

### Rythme des calculs

Un élève qui révise doit pouvoir suivre chaque étape sans mettre pause.

- **Un calcul intermédiaire par phrase** : énoncer la formule, remplacer, calculer, conclure (quatre temps, pas un seul). Exemple : « Abscisse : x B moins x A. On remplace : moins 7 moins 2. Ça fait moins 9. »
- `[lent 1.15]` (1,1 à 1,25) sur les temps forts de calcul : débit ralenti par Piper (`length_scale`), sans changer la voix. **Pocket l'ignore** (pas de réglage de débit) : le rythme vient de l'échantillon cloné, lu posément, et des phrases courtes du script.
- `[pause 0.8]` à `[pause 1.0]` après chaque résultat intermédiaire, le temps que le nombre « tombe » et que l'œil revienne à la ligne suivante.
- Les gestes suivent ce rythme : une ligne de calcul n'apparaît qu'au moment où elle est dite (recette « dérouler puis compacter » de `design.md`).

### Prononciation (Piper, voix de secours)

Ces retouches ne servent qu'à Piper : `voix_pocket.py` ne les applique pas (les écrire pour Pocket serait nuisible : « ha » ou « plusse » seraient dits tels quels).

`voix.py` corrige automatiquement ce que la phonémisation de Piper dit mal (mesuré le 03/10/2026) :
- « y » ou « Y » isolé (variable, nom de point) est lu « i » → remplacé par « i grec » (le pronom de « il y a », « n'y va » est conservé) ;
- « A » isolé suivi d'un mot n'est pas accentué et se fond dans la voyelle suivante (« le point A a » → « a a », effet haché) → remplacé par « ha » (h aspiré : pas de liaison ; l'ancien « ah » donnait « les droites-z-ah I », « le sommet-t-ah », corrigé le 09/10/2026). Éviter en plus d'écrire « A a » : « A, de coordonnées… » ou « A a pour… » → « Le point A est de coordonnées… ».
- « I » isolé devant un mot à voyelle initiale devient une semi-voyelle enchaînée (`ˈiʲ e`) : « les droites A I et B C » est entendu « les droites assies et B C » → virgule ajoutée automatiquement après « I » (`ˈi, e`), 09/10/2026.
- **Liaison devant une lettre isolée** : « Cas a. » est lu « saza » (le s de « cas » se lie au « a »). Ne jamais écrire un mot à consonne finale muette suivi d'une lettre-étiquette (« cas a », « cas b ») : dire « Premier cas », « Deuxième cas »… et garder a, b, c à l'écran.
- **« plus » opérateur ou signe** est lu « ply » (« trois plus deux » → `ply`, « plus un » → `plyz œ̃`) → remplacé par « plusse » devant un nombre, une lettre, « moins », « plus », « les », une parenthèse, et dans « de plus » en fin de phrase ; « la plus grande » reste `ply` (13/10/2026).
- **Nombre devant un nom féminin** : « 1 tuile » était lu « un tuile » (num2words ne connaît que le masculin) → « une » (et « vingt et une ») devant les noms de `NOMS_FEMININS` dans `voix.py` ; compléter cette liste quand un nouveau nom féminin suit un chiffre (13/10/2026).
- **Phrase qui commence par un chiffre** : converti en minuscule (« six unités »), Piper ne la sépare pas de la précédente → `voix.py` remet la majuscule après `. ! ?` (13/10/2026).
- **Respiration** : Piper enchaîne les phrases d'un temps fort sans pause (« 5 unités, c'est trop court. 6 unités, c'est trop long. » dit d'une traite) → `voix.py` synthétise phrase par phrase avec `--silence-phrase 0.45` s entre elles, ralentit tout de `--debit 1.1` et ajoute `--pause-en-plus 0.2` s à chaque `[pause]` (réglages par défaut demandés le 13/10/2026 : « débit moins rapide, pauses un peu plus marquées, sans que ça devienne chiant »).
- Dictionnaire propre à une capsule : `<capsule>/prononciation.json`, `{"écrit": "dit"}` (mot entier), appliqué avant les règles générales.
- Contrôle sans écouter : `PiperVoice.phonemize(texte)` montre les phonèmes ; une lettre sans accent tonique (`ˈ`) devant un mot risque d'être avalée ; un `z` ou un `t` collé au mot qui précède une lettre isolée (`dʁwˈatz ˈa`) trahit une liaison parasite.

### Prononciation (Pocket TTS, voix par défaut depuis le 20/10/2026)

Installation, `-X utf8`, `HF_HOME` et accès au clonage : `installation/LISEZMOI.md` et `cloner-sa-voix.md` ; `voix_pocket.py` s'en occupe seul (relance dans `python_pocket`, UTF-8, cache de `config.json`). Corrections de mots : `<capsule>/prononciation.json` `{"écrit": "dit"}`, appliqué avant les chiffres.

Pocket TTS (modèle `french_24l`) n'a pas la phonémisation de Piper : les graphies phonétiques écrites pour Piper ne se transposent pas telles quelles. Relevé sur le tuto bfcours-typst (Whisper sans indice) :
- « if » lu « yves » → écrire « iffe ».
- « Taïpste » : le « e » final n'est pas toujours dit (« Taipst ») ; « bé èffe cours » entendu « BF Court » ; « latek » entendu « la tech » ; « èm cé cu » entendu « mcq ». À tester : l'orthographe normale (« Typst », « LaTeX ») est peut-être mieux lue que la graphie Piper.
- Noms propres (frise des maths, voix `peter_yearsley`) : Rhind → « reined », Playfair → « Playford », Viète → « Viette », Leonhard → « Léonard » ; Brahmagupta, al-Khwarizmi, Fibonacci, Plimpton, Euclide, Archimède, Descartes passent. « aire » parfois dit comme la lettre « r » ; « 3,16 » risque de perdre son « virgule » ; « pi r » entendu « piret ».
- Corrections par `prononciation.json` (voix clonée, exemple d'une frise) : « Rhind » → « Rinde » fonctionne ; « Playfair » → « Plèffère » entendu « Pfeffer » (mieux, à confirmer) ; « Leonhard » → « Léonarte » sans effet ; « pi r » toujours « piret » (essayer « pi èrre »). « aire » / « ère » : homophones, c'est Whisper qui hésite, pas un défaut.
- Génération variable d'un essai à l'autre (mot avalé, « cherche » → « recherche ») : si l'utilisateur signale un mot mal dit, régénérer le temps fort avec `--controle` (contrôle de fidélité à la demande).
- Alignement : avec Whisper, moins sûr qu'avec Piper (91 % des mots appariés contre 99 %) ; avec **MFA** (défaut depuis le 20/10/2026), 100 % des mots du texte dit posés sur le tuto, 0 mot interpolé.
- **Ne pas étirer l'audio** (`rubberband`, `atempo`) : essayé jusqu'au facteur 0,75, la voix devient robotique (verdict de l'utilisateur, 20/10/2026). Ralentir uniquement par un échantillon cloné lu lentement.
- **Débit** : une voix du catalogue (`peter_yearsley`) est environ 30 % plus courte que Piper ralenti à 1,1, jugée trop rapide ; un clone lu posément est un peu plus court que Piper (232 s contre 256 s sur un exemple de frise). Pas de `length_scale` : le débit est celui de la voix ou de l'échantillon cloné.
- Voix brute très basse (−33 LUFS) : `voix_pocket.py` la nivelle à −16 LUFS, voix par voix.
- Voix anglaises du catalogue (`peter_yearsley`, `cosette`, `marius`…) : accent anglais en français. Voix française du catalogue : `estelle` (femme).
- Noms d'outils (essais avec une voix clonée) : écrits normalement, « Pocket TTS », « Whisper », « Chromium », « Hugging Face », « 540p », « 1080p » passent ; « three.js » est dit « Cree Gaze » → `prononciation.json` `"three.js": "Tri J S"` (entendu « 3JS ») ; « Kyutai » entendu « Q-Type » / « Qtai » avec toutes les graphies essayées (« Kyoutaï », « Kiou-taille ») : à écouter ; « TeX » entendu « TX » et « ffmpeg » « Fanpeg » : les éviter à l'oral (« formules », « l'outil de montage ») ; « pèse » après « 24 l » entendu « épaisse ». « Claude » est écrit « Cloud » par Whisper : homophone, pas un défaut.
- **Alignement des débuts de temps fort** (horodatage Whisper seulement, quand MFA n'est pas installé) : Whisper rate souvent la PREMIÈRE phrase d'un temps fort ; ses mots sont alors interpolés, jusqu'à 0,5 s d'écart. Pour un geste important sur un tel mot : lire les bornes des phrases sur les silences de `voix/bXX.wav` (`ffmpeg -i voix/b20.wav -af silencedetect=n=-40dB:d=0.12 -f null -`) et ancrer en `'@b20+1.3'`. **Avec MFA, inutile** : ancrer directement sur le mot (`'@b20~"clair"'`) ; les quatre recalages manuels du tuto (b18, b20, b26, b30) tombent à 50 ms près sur les mots posés par MFA.

## 2. Générer la voix : `voix_pocket.py` (défaut) ou `voix.py` (secours)

### Pocket TTS : `voix_pocket.py`

```bash
$PY $S/voix_pocket.py "<capsule>"                                 # voix par défaut (config.json : voix_pocket_defaut), modèle french_24l
$PY $S/voix_pocket.py "<capsule>" --seulement b07,b12             # régénérer deux temps forts après correction du script
$PY $S/voix_pocket.py "<capsule>" --modifies                      # ne refaire que ce qui a changé (texte dit, voix, modèle) ; reprend après un arrêt
$PY $S/voix_pocket.py "<capsule>" --modele french                 # modèle 2 fois plus rapide, un peu moins bon (brouillon)
$PY $S/voix_pocket.py "<capsule>" --voix estelle                  # autre voix par défaut
$PY $S/voix_pocket.py "<capsule>" --seulement b07 --controle      # À LA DEMANDE : avec contrôle de fidélité (--essais 3 au plus par temps fort)
```

`$PY` peut être n'importe quel Python : le script se relance seul avec `python_pocket` (UTF-8, cache des modèles de `config.json`). Puis TOUJOURS `transcrire.py` : les bornes changent à chaque synthèse.

**Une voix par temps fort**, par une étiquette dans le titre :

```
## b01 [pause 0.6]                    voix par défaut de config.json
## b07 [estelle] [pause 0.5]          voix du catalogue Pocket (française : estelle ; anglaises : peter_yearsley, cosette, marius, javert, jean…)
## b09 [ma-voix]                       alias d'une voix clonée, déclaré dans config.json (« voix_clonees », voir cloner-sa-voix.md)
```

Une étiquette inconnue arrête le script en listant le catalogue et les alias déclarés. L'état de chaque voix (un clone demande quelques secondes de calcul) n'est calculé qu'une fois par exécution. Mélange avec la voix enregistrée du professeur : `voix-mixtes.md`.

Ce que fait le script, temps fort par temps fort :
1. texte dit = `pour_l_oreille` de `voix.py` SANS les rustines de Piper (nombres, pourcentages, décimaux et milliers en mots) + `prononciation.json` ;
2. génération phrase par phrase (0,4 s de silence entre phrases), blancs de tête et de queue rognés, graine fixe par essai ;
3. **contrôle de fidélité, À LA DEMANDE** (désactivé par défaut : un seul essai par temps fort ; actif avec `--controle` ou `"controle_fidelite_auto": true` dans `config.json`), SANS indice de texte (`controle_fidelite.py`) : **Parakeet** ONNX sur processeur (`python_parakeet`, `--controle parakeet`, défaut) réécoute chaque candidat ; les seuls candidats signalés sont réécoutés par **Whisper** (`--arbitre whisper`, `arbitre_fidelite`), et le verdict qui trouve le moins d'erreurs est gardé (une vraie erreur de synthèse est entendue par les deux, une fausse alerte est propre à un moteur). Mot sauté, ajouté ou changé = erreur ; homophone (ses/ces…), nom propre, lettre mal entendue = « flou » (non bloquant) ; jusqu'à 3 essais, le meilleur est gardé. Les deux modèles sont chargés **une fois** pour toute la génération, dans un serveur de contrôle lancé dès le début (Parakeet se charge pendant que Pocket synthétise). Avec le texte en indice, Whisper hallucine (« Sous-titrage Société Radio-Canada ») : jamais d'indice ;
4. nivellement à −16 LUFS **voix par voix** (la voix brute sort à −33 LUFS), aucun étirement ;
5. assemblage : 0,25 s au début, `[pause] + 0,2 s` entre temps forts.

Sorties : `audio.wav`, `voix/<id>.wav`, `data/temps-forts.json|js` (champ `voix` = étiquette), **`data/fidelite-voix.json`** (par temps fort : voix, essais, retenu, erreurs, flous, texte entendu, moteur retenu, verdict de l'autre moteur dans `autre_moteur` ; liste `a_ecouter`), `voix-brut/` (candidats et état de reprise : à supprimer une fois la capsule validée). Le script termine en listant les temps forts qui gardent une erreur : les écouter, puis corriger par `prononciation.json` ou reformulation et relancer avec `--seulement`. La reconnaissance vérifie les mots, pas le naturel : **l'écoute reste le dernier juge**.

Recontrôler des voix déjà produites, sans resynthèse : `controle_fidelite.py --capsule "<capsule>" [--arbitre aucun]` (bilan dans `data/controle-fidelite.json`).

Alignement : `transcrire.py` pose le texte dit avec MFA puis y recolle les mots du script (sources `mfa`, `groupe` pour un passage écrit autrement : « 240 » dit « deux cent quarante », « 540p ») ; un mot `"source": "interpole"` n'apparaît plus qu'avec l'horodatage Whisper (MFA absent) : le vérifier avant le rendu.

**Contrôle et horodatage mesurés sur le tuto** (36 temps forts, 5 min 21 de voix, 20/10/2026 ; détail : `outils-audio.md`) :

| | Avant (Whisper) | Maintenant |
|---|---|---|
| Contrôle de fidélité | Whisper large-v3 rechargé à chaque manche, ≈ 4 s par temps fort sur carte graphique, ≈ 18 s sur processeur | Parakeet 24,5 s pour 36 temps forts, chargement compris (6 signalés) ; + arbitre Whisper sur ces 6 : 3 fausses alertes levées |
| Horodatage | 96 à 940 s, 43 mots interpolés, 4 gestes recalés à la main | MFA 74 s, processeur, 0 mot interpolé |
| Voix de bout en bout | 1 923 s (≈ 1 450 s hors synthèse, surtout les trois manches de contrôle Whisper) | ≈ 10 min estimées : la synthèse Pocket (≈ 470 s) domine |

Fausses alertes de Parakeet relevées sur le tuto : graphies phonétiques (« Kiou-taille » entendu « QTI », « Tri J S » entendu « 3GS »), anglicismes (« DeepSeek »), et le temps fort de `peter_yearsley` (accent anglais, commence par « Hello ») revenu vide : l'arbitre Whisper le rétablit.

### Performances mesurées (processeur seul, sauf Whisper sur RTX 3060 ; octobre 2026)

| | Piper (`voix.py`, secours) | Pocket `french` | Pocket `french_24l` (défaut) |
|---|---|---|---|
| Vitesse de calcul | 12 à 23 s pour 3 min 30 d'audio (≈ 0,1 s par s) | ≈ 0,5 s de calcul par s d'audio (2 fois plus rapide que le temps réel) | ≈ 1,2 à 1,6 s par s d'audio (≈ temps réel) |
| Chargement du modèle | ≈ 1 s | quelques s (poids en cache) | 2 à 6 s en cache ; **1 à 5 min la première fois** (téléchargement) |
| Poids | ≈ 60 Mo par voix, 200 Mo les trois | 209 Mo | 641 Mo |
| Clonage de voix | non | oui (poids verrouillés) | oui (retenu) |
| Réglage du débit | oui (`length_scale`, `[lent]`) | non (échantillon cloné lu posément) | non (idem) |
| Fidélité au texte (Whisper sans indice, mesures antérieures au contrôle Parakeet) | lit exactement le texte ; alignement des mots 672/678 (99 %) sur la frise | non mesurée sur une capsule entière | peter_yearsley : frise 21/22 temps forts sans erreur de mot, alignement 618/678 (91 %) ; tuto 10/10 sans mot manquant. Voix clonée : frise 19/22 sans erreur (les 3 restants : homophones « aire/ère », « XVIIIe »), alignement 645/678 (95 %) |
| Essais nécessaires | 1 | — | 1 à 3 (tuto : 18 essais pour 10 temps forts ; frise : 22 temps forts en 32 essais) |
| Durée de parole, même texte | frise 255,8 s ; tuto 102,7 s (tom, débit 1,1) | — | peter_yearsley : frise 202,2 s, tuto 72,0 s ; clone : frise 232,3 s |
| Qualité d'écoute | claire, un peu mécanique ; liaisons, nombres et accent sûrs | — | plus naturelle, mais variable d'un essai à l'autre (mot avalé, « cherche » devenu « recherche ») |
| Mots à corriger à la main | « ha », « i grec », « plusse » (automatique) | — | noms propres rares (Rhind, Playfair), « pi r » → « piret », sigles et graphies phonétiques |

Sources : des comparatifs d'essai (leurs chiffres sont repris ici) et l'essai de 4 temps forts à 3 voix du 20/10/2026 (voir fin de ce tableau).

**Essai de `voix_pocket.py` du 20/10/2026** (capsule de 4 temps forts : clone, `estelle`, `peter_yearsley`, clone par défaut ; `french_24l`, processeur, Whisper large-v3 sur RTX 3060) : 30,7 s d'audio en 71 s de bout en bout (modèle chargé en 2 s, clone prêt en 4 s, 5 essais, 2 manches de contrôle), 4/4 temps forts sans erreur de mot. Sonies brutes : `estelle` -21, clone -21, `peter_yearsley` -32 LUFS, d'où le nivellement voix par voix. Voix mixtes (prof + `estelle` + clone + Piper `tom`) : `assembler_voix.py` assemble le tout, 16 s d'audio, mélange à -16,7 LUFS. Un premier passage avait compté de fausses erreurs (Whisper écrit « 0,625 », « 62,5% », « 3² » en chiffres) : la comparaison remet ces écritures en mots avant de comparer.

Verdict d'écoute (utilisateur, 20/10/2026) : Pocket avec une voix clonée est jugée la meilleure ; une voix du catalogue anglaise est jugée trop rapide ; l'audio étiré est jugé robotique.

### Piper : `voix.py` (voix de secours)

À utiliser si Pocket n'est pas installé, pour un brouillon instantané, ou quand le réglage `[lent]` est indispensable.

```bash
$PY $S/voix.py "<capsule>"                                        # Piper siwis (défaut) : voix féminine native, CPU, ~15 s pour 3 min
$PY $S/voix.py "<capsule>" --voix-piper tom                       # voix masculine native (upmc : autre voix d'homme)
$PY $S/voix.py "<capsule>" --seulement b07,b12                    # régénérer deux phrases après correction du script
$PY $S/voix.py "<capsule>" --modifies                             # régénérer tout ce qui a changé (texte dit, [lent], voix)
```

Mêmes sorties que `voix_pocket.py` (sans `fidelite-voix.json`). Piper lit exactement le texte. Verdict d'écoute (02/10/2026) : **siwis** et **tom** gèrent bien les subtilités du français (liaisons, nombres, accent). Chatterbox (clonage de timbre) a été essayé puis abandonné le 09/10/2026 : il changeait parfois les mots et prononçait mal le français.

## 3. Puis le déroulé normal

`nouvelle_capsule.py "<capsule>" "<capsule>/audio.wav"` → `transcrire.py` → `mots.py` → storyboard (les temps forts du script SONT le storyboard : y ajouter la colonne visuel/gestes) → `spec.js` ancré en `'@b10~"mot"'` → planche (`rendre_canvas.py --images`) → rendu.

Plusieurs voix DANS la même capsule : étiquettes `[estelle]`, `[ma-voix]`… par temps fort (§ 2). Plusieurs versions de la même capsule avec des voix différentes : un dossier par voix, même `spec.js` copié à l'identique (ancres par temps fort), un rendu par dossier.

## Transparence

Afficher discrètement « Voix de synthèse » (coin bas, pendant toute la capsule ou au moins au début et à la fin). Ne cloner que sa propre voix, ou celle d'une personne qui a donné son accord (`cloner-sa-voix.md`). L'échantillon et la déclaration du clone dans `config.json` restent personnels.
