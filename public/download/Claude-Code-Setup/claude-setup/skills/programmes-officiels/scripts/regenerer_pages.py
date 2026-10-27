#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
regenerer_pages.py — Régénère les images (PNG) et/ou pages PDF isolées du BO
à partir des PDF complets de data/pdf/.

Les dossiers data/pages/ (PNG) et data/pages_pdf/ (PDF de page) ne sont pas
fournis avec le skill : ils se recréent à la demande, de façon idempotente
(une page déjà présente est ignorée, sauf avec --force).

Seul PyMuPDF est requis, et uniquement pour ce script :  pip install pymupdf

Usage :
    python scripts/regenerer_pages.py                         # tout, PNG + PDF
    python scripts/regenerer_pages.py --niveau 5E             # un niveau
    python scripts/regenerer_pages.py --niveau cycle4 --page 7
    python scripts/regenerer_pages.py --niveau 2GT --png      # PNG seulement
    python scripts/regenerer_pages.py --niveau 2GT --pdf      # PDF seulement
    python scripts/regenerer_pages.py --force                 # réécrit l'existant

--niveau accepte un code de niveau (5E, 2GT, TSPE...) ou un dossier
(cycle3, cycle4, 2GT...). Les niveaux 6E/CM1/CM2 -> cycle3 ; 5E/4E/3E -> cycle4.
"""

import argparse
import io
import json
import sys
from pathlib import Path

if __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_DIR = DATA_DIR / "pages"
PAGES_PDF_DIR = DATA_DIR / "pages_pdf"
MAPPING_FILE = PDF_DIR / "_mapping.json"

TARGET_WIDTH_PX = 1200

MSG_PYMUPDF = ("PyMuPDF est requis pour régénérer les images de pages du BO.\n"
               "Installer avec :  pip install pymupdf")


def _import_fitz():
    try:
        import fitz  # PyMuPDF
        return fitz
    except ImportError:
        try:
            import pymupdf as fitz
            return fitz
        except ImportError:
            return None


def charger_mapping() -> dict:
    with open(MAPPING_FILE, encoding="utf-8") as f:
        return json.load(f)["files"]


def resoudre_entrees(mapping: dict, niveau: str | None) -> list[tuple[str, dict]]:
    """Retourne les (fichier pdf, entrée) correspondant au niveau ou dossier demandé."""
    if not niveau:
        return list(mapping.items())
    n = niveau.strip().lower()
    res = [(pdf, e) for pdf, e in mapping.items()
           if n == e["page_folder"].lower()
           or n in [x.lower() for x in e.get("niveaux", [])]
           or n == pdf.lower().removesuffix(".pdf")]
    return res


def regenerer_page(doc, fitz, entree: dict, num: int, png: bool, pdf: bool, force: bool) -> int:
    """Génère une page (1-indexée). Retourne le nombre de fichiers écrits."""
    ecrits = 0
    dossier = entree["page_folder"]
    nom = f"page_{num:03d}"
    if png:
        sortie = PAGES_DIR / dossier / f"{nom}.png"
        if force or not sortie.exists():
            sortie.parent.mkdir(parents=True, exist_ok=True)
            page = doc.load_page(num - 1)
            zoom = TARGET_WIDTH_PX / page.rect.width if page.rect.width > 0 else 2.0
            page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False).save(str(sortie))
            ecrits += 1
    if pdf:
        sortie = PAGES_PDF_DIR / dossier / f"{nom}.pdf"
        if force or not sortie.exists():
            sortie.parent.mkdir(parents=True, exist_ok=True)
            single = fitz.open()
            single.insert_pdf(doc, from_page=num - 1, to_page=num - 1)
            single.save(str(sortie), garbage=4, deflate=True)
            single.close()
            ecrits += 1
    return ecrits


def generer(niveau: str | None = None, page: int | None = None,
            png: bool = True, pdf: bool = True, force: bool = False,
            verbose: bool = True) -> int:
    """Régénère les pages demandées. Retourne le nombre de fichiers écrits, -1 si PyMuPDF manque."""
    fitz = _import_fitz()
    if fitz is None:
        print(MSG_PYMUPDF, file=sys.stderr)
        return -1
    entrees = resoudre_entrees(charger_mapping(), niveau)
    if not entrees:
        print(f"Niveau inconnu : {niveau}", file=sys.stderr)
        return 0
    total = 0
    for fichier, entree in entrees:
        chemin = PDF_DIR / fichier
        if not chemin.exists():
            print(f"PDF absent : {chemin}", file=sys.stderr)
            continue
        doc = fitz.open(str(chemin))
        pages = [page] if page else range(1, doc.page_count + 1)
        n = 0
        for p in pages:
            if p < 1 or p > doc.page_count:
                print(f"Page {p} hors limites ({fichier} : {doc.page_count} pages)", file=sys.stderr)
                continue
            n += regenerer_page(doc, fitz, entree, p, png, pdf, force)
        doc.close()
        total += n
        if verbose:
            print(f"{fichier} -> {entree['page_folder']}/ : {n} fichier(s) écrit(s)")
    return total


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--niveau", help="code de niveau ou dossier (5E, 2GT, cycle4...) ; défaut : tous")
    ap.add_argument("--page", type=int, help="numéro de page unique (avec --niveau)")
    ap.add_argument("--png", action="store_true", help="PNG seulement")
    ap.add_argument("--pdf", action="store_true", help="PDF de page seulement")
    ap.add_argument("--force", action="store_true", help="réécrire les fichiers existants")
    a = ap.parse_args()
    if a.page and not a.niveau:
        ap.error("--page nécessite --niveau")
    png = a.png or not a.pdf
    pdf = a.pdf or not a.png
    n = generer(a.niveau, a.page, png, pdf, a.force)
    if n < 0:
        sys.exit(1)
    print(f"Total : {n} fichier(s) écrit(s).")


if __name__ == "__main__":
    main()
