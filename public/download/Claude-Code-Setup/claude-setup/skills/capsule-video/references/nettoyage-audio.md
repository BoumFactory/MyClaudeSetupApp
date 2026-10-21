# Nettoyer l'enregistrement du professeur (`nettoyer_audio.py`)

Pour la voie A quand le prof s'est enregistré « en vrai » : blancs trop longs, « euh », phrase recommencée. Le script propose des coupes **lisibles et modifiables**, puis les applique sans clic. Il ne touche à aucun autre script : il appelle `transcrire.py` tel quel pour la nouvelle transcription.

```bash
S=.claude/skills/capsule-video/scripts
$PY $S/nettoyer_audio.py analyse "<audio>" "<sortie>" [--seuil-db -35] [--blanc-min 0.8] [--garder 0.3]
#   → <sortie>/coupes.json (éditable) et coupes.txt (résumé à relire)
$PY $S/nettoyer_audio.py applique "<sortie>" [--bloc "<capsule>/script.md"] [--vocab "Typst, notations"]
#   → audio-nettoye.wav, data/transcript.* (nouvelle transcription horodatée), prof-blocs/ si --bloc
$PY $S/nettoyer_audio.py tout "<audio>" "<sortie>" [--bloc script.md]      # sans validation
# --asr parakeet (analyse, applique, tout) : repli sans Whisper, voir plus bas
```

**Reconnaissance** : Whisper (défaut, `asr_enregistrements` de `config.json` ; carte graphique si disponible, sinon medium sur processeur). Après `applique`, `transcrire.py` retranscrit l'audio nettoyé avec Whisper puis **MFA refait le temps de chaque mot** sur ce texte (mesuré le 20/10/2026 sur 5 min 24 nettoyées : Whisper 35 s sur carte graphique + MFA 63 s ; reprise de parole après un silence à 91 ms près au p90, contre 239 ms avec les temps de Whisper).

**`--asr parakeet`** (poste sans Whisper) : Parakeet ONNX sur processeur, ≈ 10 fois plus rapide que Whisper sur processeur, mais **il efface les « euh » et les mots répétés à la suite** (« mais mais » devient « mais ») : hésitations et bégaiements ne sont pas détectés, seules les reprises de phrases entières et les blancs le sont ; `--vocab` est sans effet et le jargon est moins bien reconnu (« LaTeX » écrit « la tech »). À réserver au repli.

## Ce qui est détecté

| Type | Méthode | Réglage |
|---|---|---|
| blanc | `ffmpeg silencedetect` ; un blanc de 2,5 s est réduit à `--garder` (0,3 s), moitié de chaque côté | `--seuil-db`, `--blanc-min`, `--garder` |
| hésitation | faster-whisper configuré pour **conserver** « euh / hum » : `initial_prompt` qui en contient, `suppress_tokens=[]`, pas de VAD, horodatage au mot ; la coupe suit les bornes du mot (±0,04 s, sans mordre sur les mots voisins) | `--hesitation-extra heure` pour les formes que Whisper entend à la place (« euh » → « heure ») |
| reprise | n-gramme de mots répété peu après (≥ 4 mots, ou répétition immédiate) : on coupe la prise précédente, on **garde la dernière** | `--min-reprise` (3), `--ecart-mots` (40), `--ecart-s` (20) |

Les reprises courtes (3 mots, non immédiates) et les mots répétés hors mots-outils sont proposés **inactifs** (`"actif": false`) : peuvent être voulus. `--sans-blancs`, `--sans-hesitations`, `--sans-reprises` coupent une famille. Un mot reconnu au milieu d'un long silence est écarté (hallucination de Whisper).

## Valider

Relire `coupes.txt` (une ligne par coupe : type, bornes, texte retiré, texte gardé pour une reprise). Dans `coupes.json` : `"actif": false` garde la coupe, `debut` / `fin` l'ajustent, une coupe `{"type": "manuel", "debut": 12.3, "fin": 13.0, "texte": "toux"}` s'ajoute. Puis `applique`.

## Application

Intervalles gardés = complémentaire de l'union des coupes actives ; chaque jonction a un micro-fondu (10 ms, `--fondu`) puis `concat` : pas de clic. Les coupes sont dans `filtre-coupes.txt` si l'on veut comprendre un résultat.

## `--bloc script.md`

Le script lu est découpé en blocs `## bNN [prof]` / `## bNN [tom]` (voir `voix-mixtes.md`). Les blocs `[prof]` sont alignés sur la transcription de l'audio nettoyé (difflib, mots du script contre mots reconnus) : la frontière entre deux blocs tombe dans le **plus grand silence** entre leurs mots, donc un mot mal reconnu reste avec son bloc. Sortie : `prof-blocs/bNN.wav` (mono 44,1 kHz, fondus 8 ms), `prof-blocs.json` (avec, par bloc, `texte_reconnu` : ce que le prof a réellement dit, que MFA alignera dans la capsule mixte) et `alignement-blocs.txt` (couverture par bloc : en dessous de 60 %, l'enregistrement s'écarte du script, relire). Passer `--vocab` pour les mots rares : un nom propre mal reconnu fait baisser la couverture, pas la découpe.

## Limites

- Whisper fait foi : un « euh » très bref ou chuchoté peut échapper ; relire `coupes.txt` et écouter les jonctions sensibles.
- Un bruit de fond constant au-dessus de `--seuil-db` empêche de détecter les blancs : remonter le seuil (−30).
- Le modèle se charge depuis le cache local (`config.json`) ; sans GPU, repli processeur (modèle medium, ou `whisper_device: "cpu"`).
- Les coupes se font sur les temps de Whisper (assez précis avec les fondus de 10 ms) ; seule la transcription finale est affinée par MFA.
