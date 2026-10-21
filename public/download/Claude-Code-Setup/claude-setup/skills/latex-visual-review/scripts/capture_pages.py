#!/usr/bin/env python3
"""
Capture les pages d'un PDF en images PNG via PyMuPDF.

Usage:
    python capture_pages.py --pdf <chemin.pdf> --output <dossier> [--dpi 150] [--pages all|1-3|2,5,7]

Sortie standard:
    - Une ligne par fichier PNG produit (chemin absolu, pour streaming)
    - Une dernière ligne JSON: {"pdf": ..., "pages_captured": N, "output_dir": ..., "files": [...], "dpi": ...}

Codes retour:
    0 = succès
    1 = PDF introuvable ou illisible
    2 = erreur d'écriture du dossier de sortie
"""
import argparse
import json
import sys
from pathlib import Path

import fitz  # PyMuPDF


def parse_pages(spec: str, total: int) -> list:
    """Convertit une spec textuelle en liste d'indices 0-based.

    Exemples : 'all', '1-3', '2,5,7', '1-2,5'.
    """
    if not spec or spec.lower() == "all":
        return list(range(total))
    indices = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            indices.update(range(int(a) - 1, int(b)))
        else:
            indices.add(int(part) - 1)
    return sorted(i for i in indices if 0 <= i < total)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Capture les pages d'un PDF en images PNG via PyMuPDF."
    )
    parser.add_argument("--pdf", required=True, help="Chemin du PDF source")
    parser.add_argument("--output", required=True, help="Dossier de sortie pour les PNG")
    parser.add_argument("--dpi", type=int, default=150, help="Résolution en DPI (défaut : 150)")
    parser.add_argument(
        "--pages",
        default="all",
        help="Sélection de pages : 'all', '1-3', '2,5,7' (défaut : all)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    out_dir = Path(args.output).resolve()

    if not pdf_path.is_file():
        print(
            json.dumps({"status": "error", "message": f"PDF introuvable : {pdf_path}"}),
            file=sys.stderr,
        )
        return 1

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print(
            json.dumps({"status": "error", "message": f"Dossier non écrivable : {exc}"}),
            file=sys.stderr,
        )
        return 2

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:  # pymupdf lève des FileDataError
        print(
            json.dumps({"status": "error", "message": f"PDF illisible : {exc}"}),
            file=sys.stderr,
        )
        return 1

    pages_in_pdf = doc.page_count
    indices = parse_pages(args.pages, pages_in_pdf)
    zoom = args.dpi / 72.0  # 72 DPI = base PDF
    matrix = fitz.Matrix(zoom, zoom)

    produced = []
    for idx in indices:
        page = doc.load_page(idx)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        name = f"page_{idx + 1:03d}.png"
        out_file = out_dir / name
        pix.save(str(out_file))
        produced.append(str(out_file))
        print(str(out_file), flush=True)
    doc.close()

    result = {
        "status": "ok",
        "pdf": str(pdf_path),
        "pages_captured": len(produced),
        "pages_in_pdf": pages_in_pdf,
        "output_dir": str(out_dir),
        "files": produced,
        "dpi": args.dpi,
    }
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
