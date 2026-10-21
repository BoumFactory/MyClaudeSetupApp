# Voix mixtes : professeur enregistré + Claude synthétisé (`assembler_voix.py`)

Pour un tutoriel où le prof parle (voix enregistrée) et où Claude intervient avec une voix de synthèse : **Pocket TTS** (voix du catalogue `[estelle]`, voix clonée `[ma-voix]`…, par défaut depuis le 20/10/2026) ou Piper **tom** (secours). Un seul `audio.wav`, une seule transcription mot à mot : les ancres `'@b05~"mot"'` de `spec.js` marchent comme dans toute capsule voie B.

## Format du script

```markdown
## b01 [prof] [pause 0.4]
Texte que le professeur dit.
> visuel : ligne ignorée (idées d'écran, notes)

## b02 [estelle] [pause 0.5]
Texte lu par Claude avec Pocket TTS. Mêmes règles d'écriture pour l'oreille que voix-synthese.md.

## b03 [tom] [pause 0.5] [lent 1.1]
Même chose avec Piper (voix de secours).
```

Étiquette de voix **obligatoire** :
- `[prof]` : voix enregistrée ;
- **Pocket TTS** : nom du catalogue (`[estelle]` française ; `[peter_yearsley]`, `[cosette]`… anglaises, accent) ou alias d'une voix clonée déclarée dans `config.json` (`[ma-voix]`, voir `cloner-sa-voix.md`) ; plusieurs voix Pocket dans un même script sont possibles ;
- Piper (secours) : `[tom]`, `[siwis]`, `[upmc]`.

`[pause s]` = silence après le bloc (0,5), `[lent f]` = ralentissement Piper (ignoré par Pocket). Les lignes `>` et les titres hors `## id` ne sont jamais dits. Prononciation : `prononciation.json` de la capsule (corrections de mots, communes à `voix.py` et `voix_pocket.py` ; les rustines de lettres « ha », « i grec » ne valent que pour Piper).

## Chaîne

```bash
S=.claude/skills/capsule-video/scripts
$PY $S/nettoyer_audio.py tout "<audio prof>" "<sortie>" --bloc "<capsule>/script.md"   # voir nettoyage-audio.md
$PY $S/assembler_voix.py "<capsule>" --prof-blocs "<sortie>" [--debit 1.1] [--cible -16]
$PY $S/nouvelle_capsule.py "<capsule>" "<capsule>/audio.wav" --titre "..."
```

Sans enregistrement réel, déposer les segments du prof dans `<capsule>/prof/bNN.wav` (MFA alignera alors le texte du script sur ces segments : à vérifier si le prof s'en est écarté). Sans MFA ni Whisper : `--sans-transcription` (mots estimés au prorata des lettres : ancres `@bNN` exactes, `~"mot"` approximatives).

## Ce que fait `assembler_voix.py`

1. synthétise les blocs de synthèse : **Pocket** par `voix_pocket.py --brut-seulement` lancé dans `python_pocket` (contrôle Parakeet + arbitre Whisper, jusqu'à 3 essais, reprise automatique ; bilan dans `data/fidelite-voix.json`), **Piper** (tom…) directement (nombres en mots, lettres, `prononciation.json` : même code que `voix.py`, débit `--debit` 1,1) ;
2. met tous les blocs en mono 44,1 kHz et les **nivelle voix par voix** (prof, estelle, ma-voix, tom… chacune séparément) à la même sonie (EBU R128, `--cible` −16 LUFS, limiteur −1 dB) : plus de volume à régler entre deux phrases (mesure du mélange affichée en fin) ;
3. assemble avec 0,25 s au début et `pause + 0,2 s` entre les blocs ;
4. appelle `transcrire.py` : MFA pose sur chaque bloc son texte dit (blocs de synthèse) ou son `texte_reconnu` (blocs `[prof]`, transmis par `prof-blocs.json` : ce que le prof a réellement dit), puis les mots exacts du script y sont recollés.

## Sorties

| Fichier | Contenu |
|---|---|
| `audio.wav`, `voix/bNN.wav` | mélange assemblé, un fichier par bloc (niveaux appliqués) |
| `data/temps-forts.json\|js` | `{id, texte, voix, debut, fin, mots:[{mot, debut, fin, source, bloc, voix}]}` : ancres `@bNN` |
| `data/transcript.json\|js\|txt` | transcription unifiée ; **chaque mot et chaque segment porte `bloc` et `voix`** ; liste `blocs` |
| `data/voix-intervalles.json\|js` | `{"prof": [[début, fin], …], "tom": [[début, fin], …]}` |

## Badge « Voix de synthèse » seulement pendant tom

Ne pas mettre `mention:` dans `spec.js` (permanente). Avec le plugin blocs (`bloc-code.md`) : `C.badgeVoix({ voix: 'tom', texte: 'Voix de synthèse' })` dans `gestes(C)` (`voix: 'estelle'` ou `'ma-voix'` pour une voix Pocket : c'est l'étiquette du script). Il lit les temps forts (champ `voix`), fond les plages voisines (< 0,6 s) et apparaît en fondu. Sans le plugin : `data/voix-intervalles.json` donne les plages pour un `C.ajouter` à la main.

## Limites

- Chaque bloc `[prof]` doit exister dans l'enregistrement : le script s'arrête en listant les segments manquants.
- Le nivellement égalise la sonie moyenne de chaque voix, pas les dynamiques internes : un prof qui chuchote par moments reste à retravailler à la source.
- Un seul fichier prof par bloc : pour re-prendre une phrase, ré-enregistrer et relancer `nettoyer_audio.py applique`.
- Exemple complet : `assets/exemples/blocs-demo/` (script, données, spec ; vidéo et audio à régénérer).
