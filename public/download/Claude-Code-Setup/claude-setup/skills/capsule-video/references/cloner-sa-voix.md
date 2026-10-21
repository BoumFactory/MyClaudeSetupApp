# Cloner sa voix (Pocket TTS)

Pocket TTS peut imiter une voix à partir d'un enregistrement de 15 à 20 secondes : timbre, **débit** et ton. Les capsules parlent alors avec VOTRE voix, générée par le texte du script. Tout est local et gratuit ; seule l'autorisation de télécharger les poids de clonage se demande une fois sur Hugging Face.

## Règles avant de commencer

- **Ne cloner que sa propre voix**, ou celle d'une personne qui a donné son accord. Jamais la voix d'un collègue, d'un élève ou d'une personnalité sans consentement.
- Une capsule à voix clonée est une voix de **synthèse** : l'écrire à l'écran (`mention: 'Voix de synthèse'` dans `spec.js`).
- **L'échantillon et sa déclaration dans `config.json` sont PERSONNELS.** Voir « Statut personnel » en fin de page.

## 1. Obtenir l'accès aux poids de clonage (une seule fois)

Le clonage utilise des poids « verrouillés » (`kyutai/pocket-tts`, 641 Mo avec la version `french_24l`). Sans eux, seules les voix du catalogue marchent, et le clonage s'arrête avec le message `requires approval` ou `We could not download the weights for the model with voice cloning`.

1. Créer un compte gratuit sur https://huggingface.co.
2. Ouvrir https://huggingface.co/kyutai/pocket-tts, lire les conditions d'utilisation, cliquer sur **Agree and access repository**. La page doit afficher « You have been granted access ».
3. Créer un jeton de lecture : https://huggingface.co/settings/tokens → *Create new token* → type **Read**. Le copier.
4. L'enregistrer dans le cache du skill (le même que celui qui sert au rendu : valeur `cache_modeles` de `config.json`). Dans PowerShell :

```
$env:HF_HOME = "<cache_modeles de config.json>"
& "<dossier du venv de python_pocket>\Scripts\hf.exe" auth login
```

Coller le jeton ; répondre `n` à « Add token as git credential ». Le jeton est rangé dans `HF_HOME` : les scripts du skill le retrouvent seuls.

**Piège** : un jeton créé sans avoir accepté les conditions (étape 2) ne donne aucun accès. Accepter d'abord, puis tester.

## 2. Enregistrer l'échantillon

Deux enregistrements, à lire à voix haute (téléphone ou micro-casque, format libre : m4a, mp3, wav).

| Fichier | Contenu | Rôle |
|---|---|---|
| échantillon | Partie A, environ 20 s | Ce que Pocket imite : timbre, **débit**, ton |
| texte de comparaison | Partie B, environ 2 min 30 | Sert seulement à juger le clone (étape 5) |

Conseils :
- Pièce calme, micro à 20 cm, pas de musique ni de ventilateur : le clone reproduit aussi le souffle et l'écho.
- **Lire la partie A AU DÉBIT VOULU pour les capsules** : posé, articulé, comme en classe quand on veut que les élèves suivent. Pocket copie le rythme de l'échantillon ; **c'est le seul moyen de ralentir la voix** (pas de réglage de débit, et étirer l'audio après coup la rend robotique).
- Ton naturel, sourire dans la voix. Une erreur : une seconde de silence et on reprend la phrase entière (on coupera).
- Texte **sans maths** pour l'échantillon.

### Partie A : échantillon (20 secondes)

> Bonjour à toutes et à tous. Aujourd'hui, on prend le temps de regarder ensemble comment on s'y prend. Pas de panique : on avance pas à pas, et à chaque étape, je vous montre ce qu'il faut écrire sur votre copie. Allez, c'est parti !

À adapter à sa manière de parler : l'essentiel est un débit et un ton qu'on veut retrouver dans toutes les capsules.

### Partie B : texte de comparaison (lu comme on le dirait au tableau)

Six paragraphes qui concentrent les difficultés d'une capsule de maths.

1. **Nombres et pourcentages** : « Un magasin vend 1 tuile à 2,75 euros. Il en vend 21 le lundi, et 80 le mardi. Après une hausse de 15 %, le prix est multiplié par 1,15. Une baisse de 30 % correspond à un coefficient multiplicateur de 0,7, et non de 0,3. En 2026, la population de la ville passe de 3 200 à 3 680 habitants. »
2. **Lettres et points** : « Dans le repère, on place les points A, B, I et Y. Le point A a pour coordonnées 2 et moins 3. Il y a un piège : les droites A I et B C sont parallèles, mais les droites O I et O J sont perpendiculaires. On dit que les vecteurs i et j sont orthogonaux. »
3. **Calculs et fractions** : « x A plus x B, le tout divisé par 2, est égal à 0 plus 4, le tout divisé par 2. est égal à 2. Le carré de moins 5 est égal à 25, alors que moins 5 au carré est égal à moins 25. 1 moins, entre parenthèses, moins 5, est égal à 1 plus 5, est égal à 6. »
4. **Racines, puissances, probabilités** : « La norme du vecteur u est égale à la racine carrée de : 3 au carré plus 4 au carré. Elle est égale à la racine carrée de 25. Elle est égale à 5. Dix puissance moins trois est égal à zéro virgule zéro zéro un. La probabilité de S sachant C est égale à zéro virgule six cent vingt-cinq. Pi vaut environ 3,14. »
5. **Noms propres** : « Vers 1800 avant notre ère, les Babyloniens gravent la tablette Plimpton 322. Vers 300 avant notre ère, Euclide écrit les Éléments. En 628, Brahmagupta décrit le zéro. Vers 825, al-Khwarizmi donne son nom à l'algorithme. En 1591, Viète écrit les inconnues avec des lettres, et en 1637, Descartes publie La Géométrie. »
6. **Liaisons et enchaînements** : « Les deux angles aigus sont égaux. Trois points alignés, cinq entiers impairs, vingt et une unités, quatre-vingts élèves, cent onze euros. Et voilà : on a terminé. Vous avez maintenant tous les outils en main. »

## 3. Convertir et nettoyer l'échantillon

Pocket attend un wav **24 kHz mono**. La commande retire aussi les blancs de début et de fin et règle le niveau :

```
ffmpeg -i "mon-enregistrement.m4a" -ac 1 -ar 24000 -af "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.15,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.15,areverse,loudnorm=I=-20:TP=-2" "mon-echantillon.wav"
```

Vérifier la durée (15 à 20 s) et réécouter : un bruit, une respiration très forte ou une erreur de lecture se retrouveront dans toutes les voix générées. Ranger ce fichier **hors du dossier du skill** (par exemple `<dossier de base>\outils\voix-clonees\`).

## 4. Déclarer la voix dans `config.json`

```json
"voix_clonees": {
  "prenom": {
    "echantillon": "<dossier d'installation>/voix-clonees/mon-echantillon.wav",
    "statut": "personnel — ne jamais partager"
  }
},
"voix_pocket_defaut": "prenom"
```

- `prenom` est l'**alias** : il s'écrit tel quel dans le script (`## b03 [prenom]`), à côté des voix du catalogue (`[estelle]`).
- `voix_pocket_defaut` : la voix des temps forts sans étiquette. Sans clone, laisser `estelle`.
- Chemin avec des barres obliques `/`, sans accents.
- Si l'échantillon est refait (même chemin), `voix_pocket.py` le détecte (date du fichier) et régénère les temps forts concernés.

## 5. Tester et comparer

1. Créer une capsule d'essai `<dossier_capsules>/essai-voix/` avec un `script.md` qui reprend les six paragraphes de la partie B, un par temps fort :

```
## b01 [prenom] [pause 0.8]
Un magasin vend 1 tuile à 2,75 euros. Il en vend 21 le lundi, et 80 le mardi. …
## b02 [prenom] [pause 0.8]
Dans le repère, on place les points A, B, I et Y. …
```

2. Générer : `$PY $S/voix_pocket.py "<dossier_capsules>/essai-voix"`. Compter environ une seconde de calcul par seconde d'audio (la première fois, chargement du modèle : 1 à 5 min).
3. Écouter `voix/b0N.wav` et le comparer à son propre enregistrement de la partie B ; lire `data/fidelite-voix.json` (mots sautés, ajoutés ou changés repérés par Whisper).
4. Mots mal dits : les corriger par `prononciation.json` (voir `voix-synthese.md` § Prononciation Pocket TTS), puis `--seulement b04`.
5. **Débit trop rapide ou trop lent** : refaire l'échantillon en le lisant au rythme voulu (étape 2). Aucun réglage ne le remplace.

## Pièges

| Symptôme | Cause | Remède |
|---|---|---|
| `requires approval`, `could not download the weights for the model with voice cloning` | conditions de `kyutai/pocket-tts` non acceptées, ou jeton absent de ce `HF_HOME` | étape 1 ; vérifier que `hf auth login` a été lancé avec le bon `HF_HOME` |
| `UnicodeDecodeError ... cp1252` au chargement | Python lancé sans le mode UTF-8 | `python -X utf8` (les scripts du skill le font seuls) |
| Voix trop rapide | échantillon lu vite | le relire posément |
| Souffle, écho, bruit dans la voix générée | pièce ou micro | refaire l'enregistrement : le clone copie tout |
| Mot avalé, ajouté ou changé d'un essai à l'autre | variabilité de Pocket | normal : contrôle Whisper et jusqu'à 3 essais déjà intégrés |
| Chargement très long la première fois | téléchargement des poids | une seule fois ; ensuite 2 à 5 s |
| Une voix du catalogue anglaise (`peter_yearsley`…) a l'accent anglais | voix non française | choisir `estelle` (française) ou un clone |

## Poids, vitesse, mesures (processeur seul, 20/10/2026)

- Poids : `french` 209 Mo, `french_24l` 641 Mo (version avec clonage). Une fois téléchargés : dans `cache_modeles`.
- `french_24l` (défaut, meilleure qualité) : environ **1 s de calcul par seconde d'audio** ; `french` : environ 2 fois plus rapide, un peu moins bon.
- Voix brute très basse (-33 LUFS) : `voix_pocket.py` la nivelle à -16 LUFS.
- Tableau comparatif Piper / Pocket : `voix-synthese.md` § Mesures.

## Statut personnel

- Le clone est une **donnée personnelle** (une voix). Il vit dans `voix_clonees` de `config.json` (chemins sur le disque de l'utilisateur) et dans l'échantillon, rangé hors du skill.
- **Avant de partager le skill** : vider `voix_clonees`, remettre `voix_pocket_defaut` à `estelle`, ne jamais copier un échantillon dans le dossier du skill. L'installeur (`installation/installer.ps1`) écrit de toute façon un `config.json` neuf chez le collègue, sans voix clonée.
- Les capsules déjà rendues avec une voix clonée peuvent circuler (la voix y est enregistrée) ; l'échantillon et la possibilité de générer de nouvelles phrases, non.
