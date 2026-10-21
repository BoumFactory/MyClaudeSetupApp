# -*- coding: utf-8 -*-
"""Methode: image isolee (capture d'ecran, photo de tableau, schema)."""

from __future__ import annotations

from pathlib import Path

from base import Workspace, has_module

NAME = "image"
VERSION = "1.0"
MATURITY = "partial"
GAPS = [
    "Pas d'OCR local (tesseract absent): le contenu est lu par Claude directement sur l'image, "
    "ce qui marche bien mais n'apparait pas dans content.md.",
]


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    path = Path(source)
    rel = ws.add_asset(path)
    dims = ""
    if has_module("PIL"):
        from PIL import Image  # type: ignore

        with Image.open(path) as im:
            dims = f"{im.width}x{im.height}"

    ws.write_content(
        "\n".join(
            [
                f"# {path.stem}",
                "",
                f"- **Fichier** : `{path}`",
                f"- **Dimensions** : {dims or '?'}",
                "",
                "## Contenu",
                "",
                f"Le contenu de cette image n'est pas transcrit automatiquement. "
                f"Lire `{rel}` pour en tirer la substance.",
                "",
            ]
        )
    )
    ws.suggest(f"Ouvrir `{rel}` : tout le contenu de la ressource s'y trouve.")

    return {
        "title": path.stem,
        "coverage": {"text": "missing", "visual": "ok", "structure": "n/a"},
        "stats": {"images": 1},
        "extra": {"dimensions": dims},
    }
