#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
02_generate_page_images.py — Rend chaque page PDF en image PNG ~1200 px de large.

Pipeline programmes-officiels, phase 3.

Lit data/pdf/_mapping.json et, pour chaque PDF, produit
    data/pages/{page_folder}/page_NNN.png

Cible :
  - largeur ~1200 px (lisible mais léger)
  - taille raisonnable (50-500 Ko / image)

Usage :
    python scripts/build/02_generate_page_images.py             # toutes les pages
    python scripts/build/02_generate_page_images.py 2gt.pdf     # un seul PDF
    python scripts/build/02_generate_page_images.py --force     # réécrit
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz  # PyMuPDF 1.23

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_DIR = DATA_DIR / "pages"
MAPPING_FILE = PDF_DIR / "_mapping.json"

TARGET_WIDTH_PX = 1200
MIN_SIZE_KB = 30
WARN_SIZE_KB = 600  # warning si dépassé


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def compute_zoom_for_width(page: fitz.Page, target_px: int = TARGET_WIDTH_PX) -> float:
    """Retourne le facteur de zoom pour que la page rendue fasse ~target_px de large."""
    page_width_pt = page.rect.width  # en points (1 pt = 1/72 inch)
    if page_width_pt <= 0:
        return 2.0
    return target_px / page_width_pt


def render_one_pdf(pdf_filename: str, mapping_entry: dict, force: bool = False) -> dict:
    pdf_path = PDF_DIR / pdf_filename
    page_folder = mapping_entry["page_folder"]
    out_dir = PAGES_DIR / page_folder
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\nRendu {pdf_filename} → pages/{page_folder}/")
    doc = fitz.open(str(pdf_path))
    total = doc.page_count

    summary = {
        "source_pdf": pdf_filename,
        "page_folder": page_folder,
        "total_pages": total,
        "target_width_px": TARGET_WIDTH_PX,
        "rendered_at": now_iso(),
        "renderer": "fitz get_pixmap",
        "pages": []
    }

    sizes_kb = []
    warnings = []

    for i in range(total):
        page_num = i + 1
        png_path = out_dir / f"page_{page_num:03d}.png"
        if png_path.exists() and not force:
            sz_kb = png_path.stat().st_size / 1024
            sizes_kb.append(sz_kb)
            summary["pages"].append({"page": page_num, "filename": png_path.name, "size_kb": round(sz_kb, 1), "skipped": True})
            print(f"   [SKIP] page {page_num}/{total} ({sz_kb:.0f} KB)", end="\r")
            continue

        page = doc.load_page(i)
        zoom = compute_zoom_for_width(page)
        matrix = fitz.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(png_path))

        sz_kb = png_path.stat().st_size / 1024
        sizes_kb.append(sz_kb)
        if sz_kb > WARN_SIZE_KB:
            warnings.append((page_num, sz_kb))
        summary["pages"].append({
            "page": page_num,
            "filename": png_path.name,
            "size_kb": round(sz_kb, 1),
            "width_px": pix.width,
            "height_px": pix.height
        })
        print(f"   ✓ page {page_num}/{total} ({pix.width}x{pix.height}, {sz_kb:.0f} KB)", end="\r")

    doc.close()
    avg_kb = sum(sizes_kb) / len(sizes_kb) if sizes_kb else 0
    print(f"   ✓ {total} images. Taille moyenne : {avg_kb:.0f} KB           ")
    if warnings:
        print(f"   ⚠ {len(warnings)} page(s) > {WARN_SIZE_KB} KB (informatif)")

    summary["avg_size_kb"] = round(avg_kb, 1)
    summary["warnings_over"] = warnings

    idx_path = out_dir / "index.json"
    with open(idx_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return summary


def process_all(force: bool = False) -> dict:
    with open(MAPPING_FILE, encoding='utf-8') as f:
        mapping = json.load(f)

    grand = {"started_at": now_iso(), "results": []}
    total_pages = 0
    for pdf_filename, entry in mapping["files"].items():
        res = render_one_pdf(pdf_filename, entry, force=force)
        grand["results"].append({
            "pdf": pdf_filename, "folder": res["page_folder"],
            "pages": res["total_pages"], "avg_kb": res["avg_size_kb"]
        })
        total_pages += res["total_pages"]
    grand["total_pages_rendered"] = total_pages
    grand["finished_at"] = now_iso()

    summary_file = DATA_DIR / "images_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(grand, f, ensure_ascii=False, indent=2)
    print(f"\n→ Résumé : {summary_file}")
    return grand


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__); return
    force = "--force" in args
    if force:
        args.remove("--force")

    with open(MAPPING_FILE, encoding='utf-8') as f:
        mapping = json.load(f)

    if args:
        target = args[0]
        if target not in mapping["files"]:
            print(f"PDF inconnu : {target}"); sys.exit(2)
        render_one_pdf(target, mapping["files"][target], force=force)
    else:
        grand = process_all(force=force)
        print("\n" + "=" * 60)
        print("RÉSUMÉ IMAGES")
        print("=" * 60)
        for r in grand["results"]:
            print(f"  {r['pdf']:12} → {r['folder']:8} ({r['pages']:3} images, ~{r['avg_kb']:.0f} KB)")
        print(f"\n  Total : {grand['total_pages_rendered']} images générées")


if __name__ == "__main__":
    main()
