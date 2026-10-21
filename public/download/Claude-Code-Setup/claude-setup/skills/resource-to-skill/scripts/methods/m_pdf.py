# -*- coding: utf-8 -*-
"""Methode: PDF (natif ou scanne)."""

from __future__ import annotations

from pathlib import Path

from base import ExtractionError, Workspace, has_module, pip_install

NAME = "pdf"
VERSION = "1.0"
MATURITY = "full"
GAPS = [
    "Pas d'OCR: un PDF scanne est rendu en images que Claude doit lire lui-meme "
    "(efficace, mais coute du contexte sur les documents longs).",
    "Les tableaux complexes perdent leur mise en colonnes dans le texte extrait.",
]

# En dessous de ce nombre de caracteres par page, le PDF est considere comme
# scanne ou majoritairement graphique: le texte seul ne suffira pas.
TEXT_PER_PAGE_THRESHOLD = 120
MAX_RENDERED_PAGES = 20


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    if not has_module("fitz") and not pip_install("pymupdf"):
        raise ExtractionError("PyMuPDF requis: pip install pymupdf")
    import fitz  # type: ignore

    path = Path(source)
    doc = fitz.open(str(path))
    n_pages = doc.page_count
    meta = doc.metadata or {}

    pages_text: list[str] = []
    total_chars = 0
    for i, page in enumerate(doc):
        text = page.get_text("text").strip()
        total_chars += len(text)
        pages_text.append(f"\n\n---\n\n### Page {i + 1}\n\n{text}" if text else f"\n\n---\n\n### Page {i + 1}\n\n_(page sans texte)_")

    per_page = total_chars / max(n_pages, 1)
    scanned = per_page < TEXT_PER_PAGE_THRESHOLD

    # Un PDF pauvre en texte doit etre regarde, pas seulement lu: on rend les
    # pages en images pour que Claude puisse en tirer le contenu reel.
    rendered: list[str] = []
    if scanned or opts.get("visual") == "deep":
        limit = min(n_pages, MAX_RENDERED_PAGES)
        for i in range(limit):
            pix = doc[i].get_pixmap(dpi=140)
            name = f"page-{i + 1:03d}.png"
            pix.save(str(ws.assets_dir / name))
            ws.register_asset(name)
            rendered.append(name)
        if n_pages > limit:
            ws.warn(f"Rendu limite aux {limit} premieres pages sur {n_pages}.")
        if scanned:
            ws.warn(f"PDF pauvre en texte ({per_page:.0f} caracteres/page): probablement scanne.")
            ws.suggest("Lire les images `assets/page-*.png` pour recuperer le contenu reel.")

    # Figures integrees: utiles pour un skill qui doit reproduire des schemas.
    figures: list[str] = []
    if opts.get("visual", "auto") != "off" and not scanned:
        for i, page in enumerate(doc):
            for j, img in enumerate(page.get_images(full=True)):
                try:
                    pix = fitz.Pixmap(doc, img[0])
                    if pix.width < 220 or pix.height < 220:
                        continue
                    if pix.n - pix.alpha >= 4:
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    name = f"figure-p{i + 1:03d}-{j}.png"
                    pix.save(str(ws.assets_dir / name))
                    ws.register_asset(name)
                    figures.append(name)
                except Exception:
                    continue
                if len(figures) >= 30:
                    break
            if len(figures) >= 30:
                break

    toc = doc.get_toc() or []
    header = [
        f"# {meta.get('title') or path.stem}",
        "",
        f"- **Fichier** : `{path}`",
        f"- **Pages** : {n_pages}",
        f"- **Auteur** : {meta.get('author') or '?'}",
        f"- **Nature** : {'scanne / graphique' if scanned else 'texte natif'}",
        "",
    ]
    if toc:
        header += ["## Sommaire du document", ""]
        header += [f"{'  ' * (lvl - 1)}- {title} (p. {page})" for lvl, title, page in toc[:120]]
        header.append("")
    if rendered:
        header += ["## Pages rendues en images", ""]
        header += [f"- `assets/{r}`" for r in rendered]
        header.append("")
    if figures:
        header += ["## Figures extraites", ""]
        header += [f"- `assets/{f}`" for f in figures]
        header.append("")
    header += ["## Texte", ""]
    ws.write_content("\n".join(header) + "".join(pages_text))
    doc.close()

    return {
        "title": meta.get("title") or path.stem,
        "coverage": {
            "text": "missing" if scanned else "ok",
            "visual": "ok" if (rendered or figures) else "n/a",
            "structure": "ok" if toc else "partial",
        },
        "stats": {"pages": n_pages, "chars": total_chars, "figures": len(figures), "rendered_pages": len(rendered)},
        "extra": {"scanned": scanned, "chars_per_page": round(per_page)},
    }
