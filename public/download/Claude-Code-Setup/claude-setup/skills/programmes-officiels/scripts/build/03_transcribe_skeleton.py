#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
03_transcribe_skeleton.py — Pré-génère un squelette markdown pour chaque page.

Ce script ne fait PAS la transcription ULTRATHINK (c'est le rôle de l'agent).
Il prépare seulement le frontmatter YAML et insère le texte brut dans une
zone "raw_text" du markdown, pour que l'agent n'ait qu'à RAFFINER (réparer
formules, restaurer tableaux, ajouter blockquotes BO).

Le squelette est écrit dans data/transcriptions/{folder}/page_NNN.md avec
un flag `status: skeleton` que l'agent passera à `clean` après ultrathink.

Usage :
    python scripts/build/03_transcribe_skeleton.py             # tous niveaux
    python scripts/build/03_transcribe_skeleton.py 2GT         # un niveau
    python scripts/build/03_transcribe_skeleton.py --force     # réécrit
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_TXT_DIR = DATA_DIR / "pages_txt"
TRANSCRIPTIONS_DIR = DATA_DIR / "transcriptions"
MAPPING_FILE = PDF_DIR / "_mapping.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def build_skeleton(folder: str, page_num: int, mapping_entry: dict, raw_text: str) -> str:
    """Construit le contenu markdown squelette d'une page."""
    niveaux = mapping_entry.get("niveaux", [folder])
    niveau_display = ",".join(niveaux) if len(niveaux) > 1 else niveaux[0]
    bo_ref = mapping_entry.get("bo_reference", "")
    bo_url = mapping_entry.get("bo_url", "")
    pdf_name = next(
        (k for k, v in load_mapping()["files"].items() if v["page_folder"] == folder),
        f"{folder.lower()}.pdf"
    )

    # Compter approximativement les lignes
    lines = raw_text.splitlines()
    has_formulas_hint = any(c in raw_text for c in ['𝑥', '𝑛', '∑', '∫', '√', '≤', '≥', '∞', 'ƒ'])
    has_tables_hint = (
        raw_text.count('\t') > 5
        or raw_text.count('|') > 5
        or any(len(ln.split()) > 8 and ln.count(' ') > 12 for ln in lines)
    )

    image_rel = f"../../pages/{folder}/page_{page_num:03d}.png"

    fm_niveau = niveau_display if len(niveaux) == 1 else "A_DETERMINER"
    fm_niveau_comment = ""
    if len(niveaux) > 1:
        fm_niveau_comment = (
            f"  # cycle4 : choisir parmi {niveaux} en lisant la page (5E / 4E / 3E)\n"
        )

    md = f"""---
niveau: {fm_niveau}
{fm_niveau_comment}page: {page_num}
pdf: {pdf_name}
page_folder: {folder}
bo_reference: "{bo_ref}"
bo_url: "{bo_url}"
page_image: {image_rel}
transcription_meta:
  date: "{now_iso()}"
  status: skeleton          # passer à 'clean' après ultrathink
  confidence: 0.5           # ré-évaluer après nettoyage
  has_formulas: {str(has_formulas_hint).lower()}
  has_tables: {str(has_tables_hint).lower()}
  source: "fitz get_text('text')"
---

# Page {page_num}{' — [Titre à déduire]' if page_num > 1 else ' — Couverture / Sommaire'}

> [TRANSCRIPTION SQUELETTE — à raffiner par l'agent en ultrathink]
>
> Étapes obligatoires :
> 1. Consulter l'image-preuve `{image_rel}` (capacité multimodale).
> 2. Réparer les formules LaTeX cassées (`$...$` inline, `$$...$$` display).
> 3. Restaurer les tableaux markdown si présents.
> 4. Préserver les citations BO en blockquote `>` (verbatim).
> 5. Mettre `status: clean` et ajuster `confidence`.

## Texte brut (matière première à raffiner)

```text-brut
{raw_text}
```

## Notes de l'agent (décisions, ambiguïtés)

(à remplir lors du raffinement ultrathink)
"""
    return md


_mapping_cache = None


def load_mapping() -> dict:
    global _mapping_cache
    if _mapping_cache is None:
        with open(MAPPING_FILE, encoding='utf-8') as f:
            _mapping_cache = json.load(f)
    return _mapping_cache


def process_folder(folder: str, mapping_entry: dict, force: bool = False) -> int:
    txt_folder = PAGES_TXT_DIR / folder
    out_folder = TRANSCRIPTIONS_DIR / folder
    out_folder.mkdir(parents=True, exist_ok=True)

    pages_txt = sorted(txt_folder.glob("page_*.txt"))
    if not pages_txt:
        print(f"   (aucun texte trouvé pour {folder})")
        return 0

    n = 0
    for txt_path in pages_txt:
        page_num = int(txt_path.stem.split("_")[-1])
        out_path = out_folder / f"page_{page_num:03d}.md"
        if out_path.exists() and not force:
            continue
        raw = txt_path.read_text(encoding='utf-8')
        skel = build_skeleton(folder, page_num, mapping_entry, raw)
        out_path.write_text(skel, encoding='utf-8', newline='\n')
        n += 1
    return n


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__); return
    force = "--force" in args
    if force:
        args.remove("--force")

    mapping = load_mapping()
    folder_to_entry = {v["page_folder"]: v for v in mapping["files"].values()}

    targets = [args[0]] if args else list(folder_to_entry.keys())

    grand_total = 0
    for folder in targets:
        if folder not in folder_to_entry:
            print(f"Folder inconnu : {folder}"); continue
        print(f"\nSquelette {folder}/")
        n = process_folder(folder, folder_to_entry[folder], force=force)
        print(f"   {n} fichiers créés (ou déjà existants)")
        grand_total += n
    print(f"\nTotal squelettes générés : {grand_total}")


if __name__ == "__main__":
    main()
