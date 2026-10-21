#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
01b_split_pdfs_bicolumn.py — Ré-extraction du texte pour les BO bi-colonne.

Phase 2-bis : surcharge les pages_txt/ pour les niveaux 1ENS / 1TEC / TTEC
qui utilisent une mise en page 2 colonnes (« Situations et problèmes » à
gauche, « Contenus mathématiques » à droite — seule la colonne droite est
exigible).

Algorithme :
  1. Pour chaque page, récupère page.get_text('blocks') (coords).
  2. Détecte si la page est bi-colonne (distribution X bimodale des centres
     des blocs, hors blocs plein-largeur).
  3. Si bi-colonne : conserve blocs plein-largeur (titres, sections H2) +
     blocs de la colonne droite uniquement. Trie par y croissant.
  4. Sinon : conserve le texte standard get_text('text').
  5. Réécrit pages_txt/{folder}/page_NNN.txt si bi-colonne détecté.

Usage :
    python scripts/build/01b_split_pdfs_bicolumn.py             # tous niveaux candidats
    python scripts/build/01b_split_pdfs_bicolumn.py 1ENS
    python scripts/build/01b_split_pdfs_bicolumn.py --dry-run   # ne sauvegarde pas
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_TXT_DIR = DATA_DIR / "pages_txt"
MAPPING_FILE = PDF_DIR / "_mapping.json"

# Niveaux candidats au parsing bi-colonne (BO Hebdo 14 2026 lycée — module / techno)
BICOLUMN_CANDIDATES = {"1ENS", "1TEC", "TTEC"}


def is_full_width_block(b, page_width: float, tol_left: float = 0.15, tol_right: float = 0.85) -> bool:
    """Bloc s'étendant de gauche à droite : titre, intro, section H2 plein-largeur."""
    x0, y0, x1, y1 = b[0], b[1], b[2], b[3]
    return x0 < page_width * tol_left and x1 > page_width * tol_right


def detect_and_extract_bicolumn(page) -> tuple[str, bool, dict]:
    """Retourne (texte, is_bicolumn, diagnostic)."""
    page_width = page.rect.width
    blocks = page.get_text("blocks")
    # Garder uniquement blocs textuels non vides (block_type == 0)
    text_blocks = [b for b in blocks if len(b) >= 7 and b[6] == 0 and (b[4] or "").strip()]

    if not text_blocks:
        return page.get_text("text"), False, {"reason": "no_text_blocks"}

    # Séparer plein-largeur vs latéraux
    full_width_blocks = [b for b in text_blocks if is_full_width_block(b, page_width)]
    side_blocks = [b for b in text_blocks if not is_full_width_block(b, page_width)]

    # Distribution X des centres des blocs latéraux
    if not side_blocks:
        return page.get_text("text"), False, {"reason": "no_side_blocks", "full_width_count": len(full_width_blocks)}

    centers = [(b[0] + b[2]) / 2 for b in side_blocks]
    left_count = sum(1 for c in centers if c < page_width / 2)
    right_count = sum(1 for c in centers if c >= page_width / 2)
    total_side = left_count + right_count

    # Heuristique bi-colonne : >= 15 % à gauche ET >= 15 % à droite, et au moins 4 blocs latéraux.
    # Seuil bas car la colonne droite (Contenus mathématiques) est souvent plus condensée que la gauche.
    is_bicol = (
        total_side >= 4
        and left_count / total_side >= 0.15
        and right_count / total_side >= 0.15
    )

    diag = {
        "page_width": page_width,
        "total_blocks": len(text_blocks),
        "full_width": len(full_width_blocks),
        "side_left": left_count,
        "side_right": right_count,
        "is_bicolumn": is_bicol,
    }

    if not is_bicol:
        return page.get_text("text"), False, diag

    # Bi-colonne : garder plein-largeur + colonne droite ; trier par y
    kept = list(full_width_blocks)
    for b in side_blocks:
        center = (b[0] + b[2]) / 2
        if center >= page_width / 2:
            kept.append(b)
    kept.sort(key=lambda b: (b[1], b[0]))
    text = "\n".join((b[4] or "").rstrip() for b in kept)
    return text, True, diag


def process_folder(folder: str, dry_run: bool = False) -> dict:
    pdf = next(
        k for k, v in json.load(open(MAPPING_FILE, encoding='utf-8'))["files"].items()
        if v["page_folder"] == folder
    )
    pdf_path = PDF_DIR / pdf
    if not pdf_path.exists():
        print(f"PDF introuvable : {pdf_path}")
        return {}

    txt_dir = PAGES_TXT_DIR / folder
    summary = {
        "folder": folder, "pdf": pdf, "pages": [],
        "bicolumn_pages": 0, "dry_run": dry_run
    }

    print(f"\n[{folder}] {pdf}")
    doc = fitz.open(str(pdf_path))
    for i in range(doc.page_count):
        page_num = i + 1
        page = doc.load_page(i)
        text, is_bicol, diag = detect_and_extract_bicolumn(page)

        out_path = txt_dir / f"page_{page_num:03d}.txt"
        action = "OVERWRITE" if is_bicol else "KEEP"
        if is_bicol and not dry_run:
            out_path.write_text(text, encoding='utf-8', newline='\n')

        summary["pages"].append({
            "page": page_num,
            "is_bicolumn": is_bicol,
            "blocks_kept": diag.get("full_width", 0) + diag.get("side_right", 0) if is_bicol else None,
            "diag": diag
        })
        if is_bicol:
            summary["bicolumn_pages"] += 1
        print(f"   page {page_num:2}  {action:10}  "
              f"blocs={diag['total_blocks']:3} (FW:{diag['full_width']}, L:{diag.get('side_left',0)}, R:{diag.get('side_right',0)})  "
              f"{'BICOL' if is_bicol else 'mono'}")
    total_pages = doc.page_count
    doc.close()

    print(f"   → {summary['bicolumn_pages']}/{total_pages} pages bi-colonne {'(dry-run, non sauvé)' if dry_run else 'écrasées'}")
    return summary


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__); return
    dry_run = "--dry-run" in args
    if dry_run:
        args.remove("--dry-run")

    targets = []
    if args:
        if args[0] in BICOLUMN_CANDIDATES:
            targets = [args[0]]
        else:
            print(f"Niveau non candidat : {args[0]}. Candidats : {BICOLUMN_CANDIDATES}")
            sys.exit(2)
    else:
        targets = sorted(BICOLUMN_CANDIDATES)

    grand = {"started_at": datetime.now(timezone.utc).isoformat(timespec='seconds'), "results": []}
    for folder in targets:
        s = process_folder(folder, dry_run=dry_run)
        grand["results"].append(s)
    print("\n" + "=" * 60)
    print("RÉSUMÉ bi-colonne")
    print("=" * 60)
    for r in grand["results"]:
        print(f"  {r['folder']:8} : {r['bicolumn_pages']}/{len(r['pages'])} pages bi-colonne détectées et {'simulées' if dry_run else 'écrasées'}")


if __name__ == "__main__":
    main()
