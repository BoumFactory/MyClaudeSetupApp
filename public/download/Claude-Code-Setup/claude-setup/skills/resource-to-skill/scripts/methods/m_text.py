# -*- coding: utf-8 -*-
"""Methode: fichier texte isole (.md, .txt, .tex, code source, .json, .csv…)."""

from __future__ import annotations

import re
from pathlib import Path

from base import Workspace

NAME = "text"
VERSION = "1.0"
MATURITY = "full"
GAPS = ["Au-dela de ~400 Ko, le contenu est tronque avec un avertissement explicite."]

MAX_CHARS = 400_000


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    path = Path(source)
    raw = path.read_text(encoding="utf-8", errors="replace")
    truncated = len(raw) > MAX_CHARS
    if truncated:
        raw = raw[:MAX_CHARS]
        ws.warn(f"Fichier tronque a {MAX_CHARS} caracteres (taille reelle: {path.stat().st_size} octets).")
        ws.suggest("Lire directement le fichier source pour les parties manquantes.")

    headings = re.findall(r"^#{1,3} .+$", raw, flags=re.M)[:60]
    fence = "````" if "```" in raw else "```"
    is_markdownish = path.suffix.lower() in (".md", ".markdown", ".txt", ".rst")
    body = raw if is_markdownish else f"{fence}{path.suffix.lstrip('.')}\n{raw}\n{fence}"

    ws.write_content(
        "\n".join([f"# {path.name}", "", f"- **Fichier** : `{path}`", "", "## Contenu", "", body])
    )

    return {
        "title": path.stem,
        "coverage": {
            "text": "partial" if truncated else "ok",
            "visual": "n/a",
            "structure": "ok" if headings else "partial",
        },
        "stats": {"chars": len(raw), "headings": len(headings)},
        "extra": {"headings": headings[:20], "suffix": path.suffix.lower()},
    }
