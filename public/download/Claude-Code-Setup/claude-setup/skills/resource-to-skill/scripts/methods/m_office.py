# -*- coding: utf-8 -*-
"""Methode: documents bureautiques (.docx, .odt, .pptx, .xlsx)."""

from __future__ import annotations

import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree

from base import ExtractionError, Workspace, has_module, pip_install

NAME = "office"
VERSION = "1.0"
MATURITY = "partial"
GAPS = [
    "Les images incluses dans les documents sont extraites mais pas replacees dans le flux du texte.",
    "xlsx: seules les premieres lignes de chaque feuille sont restituees (inventaire, pas dump complet).",
]

MAX_ROWS = 40


def _docx(path: Path, ws: Workspace) -> tuple[str, dict]:
    if not has_module("docx") and not pip_install("python-docx"):
        raise ExtractionError("python-docx requis: pip install python-docx")
    import docx  # type: ignore

    doc = docx.Document(str(path))
    lines = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = (para.style.name or "").lower()
        if "heading 1" in style or style == "title":
            lines.append(f"\n## {text}\n")
        elif "heading" in style:
            lines.append(f"\n### {text}\n")
        else:
            lines.append(text)
    for t_idx, table in enumerate(doc.tables):
        lines.append(f"\n**Tableau {t_idx + 1}**\n")
        for row in table.rows[:MAX_ROWS]:
            lines.append("| " + " | ".join(c.text.strip().replace("\n", " ") for c in row.cells) + " |")
    return "\n".join(lines), {"paragraphs": len(doc.paragraphs), "tables": len(doc.tables)}


def _odt(path: Path, ws: Workspace) -> tuple[str, dict]:
    with zipfile.ZipFile(path) as z:
        xml = z.read("content.xml").decode("utf-8", errors="replace")
    text = re.sub(r"</text:(p|h)>", "\n", xml)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [ln.strip() for ln in text.splitlines()]
    body = "\n".join(ln for ln in lines if ln)
    return body, {"chars": len(body)}


def _pptx(path: Path, ws: Workspace) -> tuple[str, dict]:
    """Lecture par le XML brut: python-pptx n'est pas installe sur ce poste et
    l'ouverture du zip suffit pour recuperer le texte de chaque diapositive."""
    lines, count = [], 0
    with zipfile.ZipFile(path) as z:
        slides = sorted(
            (n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)),
            key=lambda n: int(re.search(r"(\d+)", n).group(1)),
        )
        for name in slides:
            count += 1
            xml = z.read(name).decode("utf-8", errors="replace")
            texts = re.findall(r"<a:t>(.*?)</a:t>", xml, flags=re.S)
            lines.append(f"\n### Diapositive {count}\n")
            lines += [re.sub(r"<[^>]+>", "", t).strip() for t in texts if t.strip()]
        media = [n for n in z.namelist() if n.startswith("ppt/media/")]
        for m in media[:20]:
            out = ws.assets_dir / Path(m).name
            out.write_bytes(z.read(m))
            ws.register_asset(out.name)
    return "\n".join(lines), {"slides": count, "media": len(media)}


def _xlsx(path: Path, ws: Workspace) -> tuple[str, dict]:
    if not has_module("openpyxl") and not pip_install("openpyxl"):
        raise ExtractionError("openpyxl requis: pip install openpyxl")
    import openpyxl  # type: ignore

    wb = openpyxl.load_workbook(str(path), data_only=True, read_only=True)
    lines, sheets = [], 0
    for ws_x in wb.worksheets:
        sheets += 1
        lines.append(f"\n### Feuille « {ws_x.title} »\n")
        for r_idx, row in enumerate(ws_x.iter_rows(values_only=True)):
            if r_idx >= MAX_ROWS:
                lines.append(f"_… ({ws_x.max_row - MAX_ROWS} lignes supplementaires non restituees)_")
                break
            lines.append("| " + " | ".join("" if c is None else str(c) for c in row) + " |")
    return "\n".join(lines), {"sheets": sheets}


HANDLERS = {".docx": _docx, ".odt": _odt, ".pptx": _pptx, ".xlsx": _xlsx}


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    path = Path(source)
    handler = HANDLERS.get(path.suffix.lower())
    if not handler:
        raise ExtractionError(f"Extension bureautique non geree: {path.suffix}")
    body, stats = handler(path, ws)

    ws.write_content(
        "\n".join([f"# {path.stem}", "", f"- **Fichier** : `{path}`", "", "## Contenu", "", body])
    )
    if stats.get("media"):
        ws.suggest("Les visuels de la presentation sont dans `assets/` : les regarder si le texte seul est elliptique.")

    return {
        "title": path.stem,
        "coverage": {
            "text": "ok" if len(body) > 800 else "partial",
            "visual": "sampled" if ws.assets else "n/a",
            "structure": "partial",
        },
        "stats": stats,
        "extra": {"format": path.suffix.lower()},
    }
