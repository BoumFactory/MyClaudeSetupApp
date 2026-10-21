#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
01_split_pdfs.py — Découpe les PDFs sources en pages individuelles.

Pipeline programmes-officiels, phase 2.

Pour chaque PDF déclaré dans data/pdf/_mapping.json :
  - Extrait le texte page par page (PyMuPDF / fitz) → data/pages_txt/{page_folder}/page_NNN.txt
  - Sauvegarde chaque page comme PDF isolé          → data/pages_pdf/{page_folder}/page_NNN.pdf
  - Génère data/pages_txt/{page_folder}/index.json (liste des pages + taille texte + statut)

Particularités :
  - une seule dépendance (PyMuPDF / fitz)
  - pages_txt/ et pages_pdf/ sont séparés
  - le mapping est lu depuis data/pdf/_mapping.json

Usage :
    python scripts/build/01_split_pdfs.py             # traite tous les PDFs
    python scripts/build/01_split_pdfs.py 2gt.pdf     # traite un PDF spécifique
    python scripts/build/01_split_pdfs.py --status    # statut
    python scripts/build/01_split_pdfs.py --force     # force le retraitement
"""

import io
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Encodage UTF-8 forcé pour la sortie console (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import fitz  # PyMuPDF 1.23+ : 'import fitz' (l'alias 'pymupdf' n'existe qu'à partir de 1.24)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_TXT_DIR = DATA_DIR / "pages_txt"
PAGES_PDF_DIR = DATA_DIR / "pages_pdf"
MAPPING_FILE = PDF_DIR / "_mapping.json"


def load_mapping() -> dict:
    """Charge le mapping PDF → niveaux/page_folder."""
    with open(MAPPING_FILE, encoding='utf-8') as f:
        return json.load(f)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def split_one_pdf(pdf_filename: str, mapping_entry: dict, force: bool = False) -> dict:
    """Découpe un PDF en pages. Retourne le résumé pour STATE."""
    pdf_path = PDF_DIR / pdf_filename
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF introuvable : {pdf_path}")

    page_folder = mapping_entry["page_folder"]
    txt_dir = PAGES_TXT_DIR / page_folder
    pdf_dir = PAGES_PDF_DIR / page_folder
    txt_dir.mkdir(parents=True, exist_ok=True)
    pdf_dir.mkdir(parents=True, exist_ok=True)

    index_file = txt_dir / "index.json"
    if index_file.exists() and not force:
        with open(index_file, encoding='utf-8') as f:
            existing = json.load(f)
        print(f"  [SKIP] {pdf_filename} déjà traité ({existing['total_pages']} pages). --force pour retraiter.")
        return existing

    print(f"\nTraitement de {pdf_filename} → {page_folder}/")
    doc = fitz.open(str(pdf_path))
    total = doc.page_count
    print(f"   {total} pages détectées")

    result = {
        "source_pdf": pdf_filename,
        "page_folder": page_folder,
        "niveaux": mapping_entry.get("niveaux", []),
        "bo_reference": mapping_entry.get("bo_reference", ""),
        "total_pages": total,
        "extraction_date": now_iso(),
        "extractor": "fitz (PyMuPDF) get_text('text')",
        "pages": []
    }

    for i in range(total):
        page_num = i + 1
        page = doc.load_page(i)

        # Extraction texte simple, ordre de lecture respecté.
        page_text = page.get_text("text") or ""

        # Sauvegarde texte
        txt_path = txt_dir / f"page_{page_num:03d}.txt"
        with open(txt_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(page_text)

        # Sauvegarde page PDF isolée (1 page)
        page_pdf_path = pdf_dir / f"page_{page_num:03d}.pdf"
        single = fitz.open()
        single.insert_pdf(doc, from_page=i, to_page=i)
        single.save(str(page_pdf_path))
        single.close()

        result["pages"].append({
            "page_number": page_num,
            "txt_filename": txt_path.name,
            "pdf_filename": page_pdf_path.name,
            "text_length": len(page_text),
            "status": "pending"
        })

        print(f"   ✓ page {page_num}/{total} ({len(page_text)} chars)", end="\r")

    doc.close()
    print(f"   ✓ {total} pages extraites ({page_folder})              ")

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Index secondaire dans pages_pdf/ pour cohérence
    with open(pdf_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump({
            "source_pdf": pdf_filename,
            "page_folder": page_folder,
            "total_pages": total,
            "format": "pdf isolé par page",
        }, f, ensure_ascii=False, indent=2)

    return result


def process_all(force: bool = False) -> dict:
    mapping = load_mapping()
    summary = {
        "processed_at": now_iso(),
        "total_pdfs": len(mapping["files"]),
        "pdfs": []
    }
    grand_total_pages = 0
    for pdf_filename, entry in mapping["files"].items():
        result = split_one_pdf(pdf_filename, entry, force=force)
        grand_total_pages += result["total_pages"]
        summary["pdfs"].append({
            "name": pdf_filename,
            "page_folder": result["page_folder"],
            "pages": result["total_pages"],
            "niveaux": result["niveaux"]
        })
    summary["grand_total_pages"] = grand_total_pages

    summary_file = DATA_DIR / "split_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"\n→ Résumé global : {summary_file}")
    print(f"→ Total pages : {grand_total_pages}")
    return summary


def show_status():
    mapping = load_mapping()
    print("Statut du split :\n")
    total = 0
    for pdf_filename, entry in mapping["files"].items():
        page_folder = entry["page_folder"]
        idx = PAGES_TXT_DIR / page_folder / "index.json"
        if idx.exists():
            with open(idx, encoding='utf-8') as f:
                data = json.load(f)
            n = data["total_pages"]
            total += n
            status = f"OK ({n} pages)"
        else:
            status = "(non traité)"
        print(f"  {pdf_filename:12} → {page_folder:8}  {status}")
    print(f"\nTotal pages traitées : {total}")


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__)
        return
    if "--status" in args:
        show_status()
        return
    force = "--force" in args
    if force:
        args.remove("--force")

    mapping = load_mapping()

    if args:
        target = args[0]
        if target not in mapping["files"]:
            print(f"PDF inconnu : {target}")
            print(f"Disponibles : {list(mapping['files'].keys())}")
            sys.exit(2)
        split_one_pdf(target, mapping["files"][target], force=force)
    else:
        summary = process_all(force=force)
        print("\n" + "="*60)
        print("RÉSUMÉ")
        print("="*60)
        for p in summary["pdfs"]:
            niveaux = ",".join(p["niveaux"])
            print(f"  {p['name']:12} → {p['page_folder']:8} ({p['pages']:3} pages) [{niveaux}]")
        print(f"\n  Total : {summary['grand_total_pages']} pages")


if __name__ == "__main__":
    main()
