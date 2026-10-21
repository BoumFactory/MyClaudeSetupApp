# Outils audio : qui fait quoi, pourquoi, poids, installation, pièges

Chaîne « voix → vérification → horodatage » depuis le 20/10/2026 : **tout tourne sur processeur**. La carte graphique NVIDIA n'accélère plus que Whisper, devenu facultatif pour les voix de synthèse.

Ce document sert aussi à l'agent qui écrit `installation/installer.ps1` et `first_check` : clés de `config.json`, commandes d'installation, contrôles.

## Rôle de chaque outil

| Étape | Outil (défaut) | Repli | Script | Clé `config.json` |
|---|---|---|---|---|
| Voix de synthèse | Pocket TTS `french_24l` (processeur) | Piper (`voix.py`) | `voix_pocket.py` | `python_pocket` |
| Contrôle de fidélité (la voix a-t-elle dit le texte ?) | **Parakeet TDT 0.6B v3**, ONNX int8, processeur | Whisper (`--controle whisper`) | `controle_fidelite.py` | `python_parakeet`, `asr_fidelite` |
| Arbitre du contrôle (seuls les temps forts signalés) | Whisper large-v3 | aucun | `controle_fidelite.py` | `python_asr`, `arbitre_fidelite` |
| Horodatage au mot, texte connu | **MFA** (Montreal Forced Aligner), processeur | Whisper avec le texte en indice | `aligner_mfa.py` (appelé par `transcrire.py`) | `mfa`, `horodatage` |
| Transcription d'un enregistrement du prof | **Whisper** large-v3 (carte graphique, sinon medium sur processeur) | Parakeet (`--asr parakeet`) | `transcrire.py`, `nettoyer_audio.py` | `python_asr`, `asr_enregistrements`, `whisper_device` |
| Horodatage d'un enregistrement | MFA sur le texte transcrit | temps de la reconnaissance | `aligner_mfa.affiner_enregistrement` | `mfa` |

Modules partagés : `asr_whisper.py` (chargement de Whisper selon `whisper_device`), `asr_parakeet.py` (chargement, texte, mots horodatés avec découpage VAD), `commun.py` (`python_de`, `relancer_pour` : chaque script se relance seul dans le Python du moteur).

## Pourquoi ces choix (bancs du 20/10/2026)


- **MFA pour l'horodatage** : le texte dit est connu, il suffit de le poser sur l'audio. Médiane 20 ms contre 40 à 60 ms pour Whisper ; après un silence, p90 40 ms contre 260 ms ; 100 % des mots posés, aucune phrase sautée. Whisper avec le texte en indice saute des phrases entières (quatre gestes du tuto recalés à la main ; MFA les retrouve à 50 ms près).
- **Parakeet pour le contrôle** : 0,5 s par temps fort sur processeur, chargé en 3,5 à 7 s, sans CUDA. Un peu plus bavard que Whisper (12 erreurs signalées contre 7 sur 22 temps forts), jamais d'invention. L'arbitre Whisper réécoute les seuls temps forts signalés et lève les fausses alertes.
- **Whisper pour les enregistrements du prof** : meilleur sur le jargon (`--vocab`), il garde les bégaiements d'un mot (« mais mais ») et les « euh » que `nettoyer_audio.py` doit couper ; Parakeet les efface.
- **Un seul chargement par génération** : `voix_pocket.py` ouvre un serveur de contrôle (`controle_fidelite.py --serveur`) au début, qui charge son modèle pendant que Pocket synthétise, puis sert toutes les manches. Avant : Whisper large-v3 était rechargé à chaque manche.

## Performances mesurées (poste RTX 3060 portable, 12 threads, 20/10/2026)

| Mesure | Avant (Whisper partout) | Maintenant |
|---|---|---|
| Contrôle de 36 temps forts du tuto (5 min 21 de voix) | une manche Whisper large-v3 sur carte graphique : chargement + ≈ 4 s par temps fort (89 s pour 22 au banc) ; ≈ 18 s par temps fort sur processeur | **Parakeet : 24,5 s** de bout en bout, chargement compris ; avec l'arbitre Whisper sur les 6 signalés : 68 s (dont 37 s de chargement de Whisper ralenti par le proxy, ramené à 12 s depuis : cache local d'abord) |
| Manches suivantes d'une génération | rechargement de Whisper à chaque manche | 0,2 à 0,5 s par temps fort, rien à recharger |
| Horodatage du tuto (`transcrire.py`) | 96 s (carte libre) à 940 s (carte occupée) | **MFA : 74 s**, processeur, 805/805 mots posés ; script recollé : 809/818 appariés, 9 « groupe », **0 interpolé** (Whisper : 43 interpolés) |
| Petite capsule de 2 temps forts | — | MFA : 47 s (coût fixe de lancement ≈ 45 s, quelle que soit la longueur) |
| Enregistrement du prof nettoyé (5 min 24) | Whisper GPU 35 s | Whisper GPU 35 s + **MFA 63 s** ; reprise de parole après un silence : p90 91 ms contre 239 ms pour Whisper |
| Même enregistrement, `--asr parakeet` | — | Parakeet 69 s + MFA 104 s, tout sur processeur |
| Tuto entier, estimation | 1 923 s de voix (synthèse 470 s, le reste en contrôles Whisper) | ≈ 470 s de synthèse + ≈ 1 min de contrôle + 74 s d'horodatage, soit ≈ 10 min au lieu de 32 |

Le coût dominant est désormais la synthèse Pocket (≈ 1,2 à 1,6 s de calcul par seconde d'audio sur processeur).

## Installation (à reprendre dans `installation/installer.ps1`)

Fait par `installation/installer.ps1` : tout sous `<base>/outils/` (`venv-rendu`, `venv-pocket`, `venv-parakeet`, `venv-whisper`, `mfa/`, `cache-hf/`, `navigateurs/`, `voix-piper/`), jamais Anaconda. Les commandes ci-dessous en sont le détail (racine = `<base>/outils`, MFA dans `<base>/outils/mfa`).

### Parakeet (≈ 800 Mo, 6 min dont 5 min 40 de téléchargement du modèle)

```powershell
py -3.13 -m venv "<racine>\venv-parakeet"
"<racine>\venv-parakeet\Scripts\python.exe" -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org "onnx-asr[cpu,hub]" soundfile num2words
```

- `num2words` est indispensable : la comparaison du contrôle remet les nombres en mots (sans lui, `controle_fidelite.py --capsule` ne peut pas comparer).
- Le modèle (640 Mo, `istupakov/parakeet-tdt-0.6b-v3-onnx`) et le VAD Silero (2 Mo) se téléchargent au premier chargement dans `HF_HOME` = `cache_modeles`. Pour le précharger pendant l'installation : `HF_HOME=<cache_modeles>` puis `python -c "import onnx_asr; onnx_asr.load_model('nemo-parakeet-tdt-0.6b-v3', quantization='int8'); onnx_asr.load_vad('silero')"`.
- Écrire `"python_parakeet": "<racine>/venv-parakeet/Scripts/python.exe"` et `"asr_fidelite": "parakeet"`.

### MFA (≈ 2,5 Go, 7 min 20)

```powershell
python "<skill>\scripts\installer_mfa.py" --racine "<racine>" --config "<skill>\config.json" --maj-config
```

- N'importe quel Python (bibliothèque standard). Relançable : chaque étape déjà faite est sautée (21 s).
- Il télécharge micromamba (11 Mo) dans `<racine>\outils\`, crée `<racine>\env-mfa` (conda-forge, `montreal-forced-aligner` + `kaldi=*=cpu*` : variante processeur, 2,4 fois plus légère que la variante CUDA, mêmes résultats), télécharge `french_mfa` (acoustique, dictionnaire, g2p) dans `<racine>\mfa-modeles\`.
- `--maj-config` écrit la clé `mfa` (`micromamba`, `env`, `modeles`, `root`) et `horodatage: "mfa"`.
- Masquer le long tableau des paquets de micromamba dans l'installeur (sortie redirigée vers un journal).

### Whisper (facultatif : enregistrements du prof et arbitre)

Inchangé : venv avec `faster-whisper` (+ `nvidia-cublas-cu12`, `nvidia-cudnn-cu12` si carte NVIDIA), clé `python_asr`. Sans carte NVIDIA : `whisper_device: "cpu"` (modèle medium), ou ne pas l'installer et mettre `asr_enregistrements: "parakeet"`, `arbitre_fidelite: null`.

### Valeurs de `config.json` selon le poste

| Poste | `asr_fidelite` | `arbitre_fidelite` | `asr_enregistrements` | `horodatage` | `whisper_device` |
|---|---|---|---|---|---|
| Carte NVIDIA, tout installé | `parakeet` | `whisper` | `whisper` | `mfa` | `auto` |
| Sans carte NVIDIA, Whisper installé | `parakeet` | `null` (ou `whisper` : lent mais limité aux signalés) | `whisper` | `mfa` | `cpu` |
| Installation minimale (sans Whisper) | `parakeet` | `null` | `parakeet` | `mfa` | — |
| Sans MFA | idem | idem | idem | `whisper` (Whisper requis) | `auto` |

## Contrôles pour `first_check` (rapides, sans rien télécharger)

- Parakeet : `"<python_parakeet>" -c "import onnx_asr, soundfile, num2words"` ; modèle présent : dossier `<cache_modeles>/hub/models--istupakov--parakeet-tdt-0.6b-v3-onnx`.
- MFA : `aligner_mfa.disponible()` (vrai si `<env>/Scripts/mfa.exe`, `<modeles>/pretrained_models/acoustic/french_mfa.zip` et `dictionary/french_mfa.dict` existent). Essai réel : `python scripts/aligner_mfa.py <capsule existante>` (≈ 45 s minimum).
- Whisper : `"<python_asr>" -c "import faster_whisper"`.
- Absent = repli sans blocage : MFA absent → horodatage Whisper ; Parakeet absent → contrôle Whisper ; ni l'un ni l'autre → `voix_pocket.py --sans-controle` seulement.

## Pièges

- **MFA, DLL `libsndfile.dll` introuvable** (`OSError 0x7e`) : `<env>`, `<env>/Scripts`, `<env>/Library/bin` doivent être dans le PATH du processus (fait par `aligner_mfa.py`, sans toucher au PATH du poste). Sous Git Bash, écrire ces chemins en `/d/...`.
- **MFA, `unable to open database file`** (sqlite) : `TEMP` pointe vers un dossier inexistant. `aligner_mfa.py` crée un dossier de travail propre à chaque appel sous `<racine>/tmp-mfa/` (`-t`), le supprime à la fin : deux capsules alignées en même temps ne se gênent pas.
- **`~/.conda/environments.txt`** : micromamba y inscrit l'environnement (liste partagée avec un Anaconda existant) ; `installer_mfa.py` retire sa ligne.
- **MFA, coût fixe** : ≈ 45 s de lancement même pour deux phrases ; un seul appel par capsule (tous les temps forts ensemble).
- **MFA, mots hors dictionnaire** (formes conjuguées, anglicismes, graphies phonétiques « Kiou-taille », 3 % du tuto) : prononciation générée à la volée (`--g2p_model_path french_mfa`), jamais bloquant.
- **MFA sur un enregistrement** : l'audio est coupé en morceaux de 20 à 40 s au milieu des silences entre mots ; faisceau élargi (`--beam 100 --retry_beam 400`). Un morceau que MFA refuse garde les temps de la reconnaissance (signalé). Les élisions coupées par Whisper (« J » + « 'ajoute ») sont recollées.
- **MFA ne vérifie rien** : il pose le texte qu'on lui donne. Un mot que la voix n'a pas dit fait dériver localement l'alignement : le contrôle de fidélité reste en amont.
- **Parakeet, plus de ≈ 6 min en un appel** : plantage ONNX. `asr_parakeet.py` découpe au-delà de 300 s avec le VAD Silero.
- **Parakeet, voix anglaise** : le temps fort de `peter_yearsley` (« Hello ! Moi, c'est Peter… ») est revenu **vide** (35 erreurs) ; l'arbitre Whisper l'a rétabli. Garder l'arbitre quand une voix à accent est utilisée.
- **Parakeet, écritures** : `π`, chiffres romains (« XVIIIe »), ordinaux (« 18e », « 1er ») et homophones fréquents (ses/ces, son/sont…) sont normalisés par `controle_fidelite.normaliser` et `HOMOPHONES` avant comparaison. Compléter ces listes plutôt que d'ignorer une fausse alerte récurrente.
- **Parakeet, jargon** : « LaTeX » écrit « la tech », « dièse begin » méconnaissable ; aucun vocabulaire injectable. D'où Whisper pour les enregistrements.
- **Whisper derrière un proxy qui casse le SSL** : faster-whisper interrogeait Hugging Face à chaque chargement (≈ 30 s perdues) ; `asr_whisper.py` lit d'abord le cache local (`local_files_only`).
- **Pas de `select` sur les tuyaux** sous Windows : le client du serveur de contrôle lit ses réponses ligne à ligne (préfixe `@@RESULTAT`), les messages des bibliothèques passent sur stderr ou sont relayés.
