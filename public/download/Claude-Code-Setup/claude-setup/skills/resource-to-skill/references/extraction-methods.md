# Méthodes d'extraction : utiliser, améliorer, créer

À lire quand `ingest.py` renvoie `no_method` ou `method_failed`, ou quand la
couverture annoncée est faible.

## Sommaire

- [Principe](#principe)
- [Le workspace normalisé](#le-workspace-normalisé)
- [Améliorer une méthode existante](#améliorer-une-méthode-existante)
- [Créer une méthode](#créer-une-méthode)
- [Contrat d'un module méthode](#contrat-dun-module-méthode)
- [Boîte à outils commune](#boîte-à-outils-commune)
- [Méthodes livrées](#méthodes-livrées)

---

## Principe

Le registre (`scripts/methods/registry.json`) associe un type de ressource à un
module Python. Chaque module déclare sa maturité et ses lacunes connues, ce qui
donne trois conduites :

| Situation | Conduite |
|---|---|
| Une méthode couvre le type, `MATURITY = "full"` | L'utiliser telle quelle |
| Une méthode couvre le type mais bute sur ce cas précis, ou `MATURITY` vaut `partial`/`stub` | **L'améliorer**, puis relancer |
| Aucune méthode ne couvre le type | **En créer une** |

Cette discipline est ce qui empêche le skill de s'user. Extraire une fois à la
main règle un problème ; corriger la méthode règle tous les suivants.

Pour voir l'état du parc :

```bash
python "scripts/ingest.py" --list
```

## Le workspace normalisé

Toute méthode, quel que soit le type de ressource, produit la même structure —
c'est ce qui permet à la suite du parcours d'être identique pour un PDF et pour
une vidéo :

```
<out>/
  manifest.json   type, méthode, couverture, statistiques, avertissements
  content.md      le texte extrait, structuré, avec ancres (page, timecode)
  assets/         images destinées à être regardées
  raw/            fichiers d'origine conservés pour vérification
```

Le champ `coverage` porte le diagnostic, dimension par dimension :

| Valeur | Sens |
|---|---|
| `ok` | dimension entièrement captée |
| `sampled` | captée par échantillonnage (frames, extraits) — on peut demander plus |
| `partial` | captée de façon incomplète — candidat à l'amélioration |
| `missing` | présente dans la ressource mais non captée — à signaler |
| `n/a` | la ressource ne possède pas cette dimension |

Un `sampled` est un état normal et satisfaisant pour une vidéo. Un `missing`
sur `text` veut dire que le skill ne peut pas s'appuyer sur ce que dit la
ressource : il faut soit lire les images, soit corriger la méthode.

## Améliorer une méthode existante

1. Lire `GAPS` dans le module concerné (`scripts/methods/m_*.py`) : la lacune
   est peut-être déjà connue et documentée.
2. Corriger au bon endroit — pas de rustine dans `ingest.py`, qui ne fait que du
   routage.
3. Mettre à jour `GAPS` (retirer ce qui est corrigé, ajouter ce qu'on découvre)
   et `MATURITY` si le niveau change. Incrémenter `VERSION`.
4. Relancer l'extraction sur la ressource qui avait échoué, et vérifier que le
   `coverage` reflète le progrès.

Un `GAPS` honnête vaut mieux qu'un `GAPS` vide : c'est lui qui permet de savoir,
à la prochaine extraction, s'il faut compléter à la main.

## Créer une méthode

```bash
python "scripts/new_method.py" notebook \
  --extensions .ipynb --label "Notebook Jupyter"
```

Le script écrit `scripts/methods/m_notebook.py` et l'enregistre dans le registre
(avant la méthode `web`, qui capte toutes les URL restantes). Le squelette
échoue proprement tant qu'il n'est pas implémenté, ce qui permet de vérifier le
routage avant d'écrire la logique.

Reste à écrire `extract()`, puis à passer `MATURITY` de `stub` à `partial` ou
`full` et à vider `GAPS` de ce qui est couvert.

Deux conseils tirés des méthodes existantes :

- **Extraire le sens, pas les octets.** Un dump brut de XML ou de JSON n'aide
  personne. Restituer un markdown lisible, avec des ancres pour retrouver
  l'endroit dans la ressource d'origine.
- **Dire ce qu'on n'a pas su faire.** `ws.warn()` et un `coverage` sincère
  valent bien mieux qu'une extraction qui paraît complète et ne l'est pas : la
  suite du parcours prend ses décisions à partir de ce diagnostic.

## Contrat d'un module méthode

```python
NAME = "notebook"          # doit correspondre à la clé du registre
VERSION = "1.0"
MATURITY = "full"          # "stub" | "partial" | "full"
GAPS = ["Les sorties d'exécution volumineuses sont tronquées."]

def extract(source: str, ws: Workspace, opts: dict) -> dict:
    ...
    ws.write_content(markdown)          # obligatoire
    ws.register_asset("figure-01.png")  # image déjà écrite dans assets/
    ws.add_asset(Path(externe))         # image à copier depuis ailleurs
    ws.warn("…")                        # ce qui n'a pas pu être capté
    ws.suggest("…")                     # action concrète pour la suite
    return {
        "title": "…",
        "coverage": {"text": "ok", "visual": "sampled", "structure": "partial"},
        "stats": {"cells": 42},
        "extra": {},
    }
```

`opts` contient `visual` (`auto` | `deep` | `off`) et `lang`. Une méthode qui
n'a pas de dimension visuelle ignore simplement `visual` et déclare
`"visual": "n/a"`.

Lever `ExtractionError` pour un échec explicable (dépendance absente, format
inattendu) : `ingest.py` le transforme en rapport lisible avec le code de
sortie 4. Toute autre exception est capturée et sa trace écrite dans
`traceback.txt` du workspace.

## Boîte à outils commune

`scripts/methods/base.py` :

| Fonction | Usage |
|---|---|
| `run(cmd, timeout, check)` | commande externe, encodage UTF-8 forcé (indispensable sous Windows) |
| `which(name)` / `require(name, hint)` | localiser un exécutable, avec variantes `.exe`/`.cmd` |
| `has_module(m)` / `pip_install(pkg)` | dépendance Python à la demande, avec repli `--trusted-host` (certificat auto-signé sur ce poste) |
| `clip(text, n)` | tronquer proprement |

`scripts/methods/video_common.py`, réutilisable par toute méthode audiovisuelle :

| Fonction | Usage |
|---|---|
| `parse_vtt(text)` | WebVTT → transcription horodatée, doublons des sous-titres automatiques supprimés |
| `transcribe_locally(media, ws)` | repli faster-whisper, installé à la demande |
| `sample_frames(video, ws, mode)` | images aux changements de scène, complétées par un échantillonnage régulier si la vidéo est statique |
| `build_contact_sheets(frames, ws)` | planches de 12 vignettes horodatées |
| `fmt_time(s)` | secondes → `m:ss` / `h:mm:ss` |

## Méthodes livrées

| Méthode | Couvre | Maturité | Limite principale |
|---|---|---|---|
| `video_youtube` | YouTube, Vimeo, Dailymotion, Twitch (yt-dlp) | full | vidéos privées ou soumises à un âge gate |
| `video_local` | `.mp4 .mkv .mov .webm .avi .mp3 .wav` | full | transcription dépendante de faster-whisper |
| `pdf` | PDF natif ou scanné | full | pas d'OCR : les pages scannées sont rendues en images |
| `office` | `.docx .odt .pptx .xlsx` | partial | images non replacées dans le flux du texte |
| `image` | `.png .jpg .webp .gif …` | partial | pas d'OCR local, lecture par Claude |
| `text` | markdown, code, JSON, CSV, sous-titres | full | troncature au-delà de 400 Ko |
| `codebase` | dossier de projet | full | carte du dépôt, pas d'analyse sémantique |
| `web` | toute URL non reconnue ailleurs | partial | pages rendues par JavaScript souvent vides |

Quand la méthode `web` renvoie un contenu quasi vide, l'outil `WebFetch` de
Claude prend le relais utilement : il exécute davantage la page.
