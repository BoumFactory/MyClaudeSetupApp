# -*- coding: utf-8 -*-
"""Methode: dossier de projet (code, configuration, corpus de fichiers).

Le but n'est pas de tout aspirer — Claude sait lire un depot — mais de produire
une carte: ce que contient le dossier, ou se trouve la substance, quels fichiers
meritent une lecture integrale. Le savoir-faire d'un projet vit surtout dans son
README, ses points d'entree et ses fichiers de configuration.
"""

from __future__ import annotations

import os
from collections import Counter
from pathlib import Path

from base import Workspace, clip

NAME = "codebase"
VERSION = "1.0"
MATURITY = "full"
GAPS = [
    "Aucune analyse semantique du code (pas de graphe d'appels): la carte oriente la lecture, "
    "elle ne la remplace pas.",
]

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build",
    ".next", ".cache", "site-packages", ".pytest_cache", ".mypy_cache", "out",
}
KEY_NAMES = {
    "readme.md", "readme.txt", "readme", "claude.md", "agents.md", "package.json",
    "pyproject.toml", "requirements.txt", "makefile", "dockerfile", "index.js",
    "main.py", "app.py", "__init__.py", "setup.py", "cargo.toml", "skill.md",
}
TEXT_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".md", ".txt", ".json", ".yml", ".yaml",
    ".toml", ".ini", ".cfg", ".sh", ".ps1", ".tex", ".sty", ".html", ".css", ".sql",
}
MAX_TREE_ENTRIES = 400
MAX_KEY_FILE_CHARS = 12_000


def extract(source: str, ws: Workspace, opts: dict) -> dict:
    root = Path(source)
    tree_lines: list[str] = []
    ext_counter: Counter[str] = Counter()
    key_files: list[Path] = []
    n_files = 0

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and not d.startswith("."))
        rel_dir = Path(dirpath).relative_to(root)
        depth = len(rel_dir.parts)
        if depth > 4:
            dirnames[:] = []
            continue
        if str(rel_dir) != ".":
            tree_lines.append(f"{'  ' * (depth - 1)}- **{rel_dir.name}/**")
        for fname in sorted(filenames):
            n_files += 1
            fpath = Path(dirpath) / fname
            ext_counter[fpath.suffix.lower() or "(sans extension)"] += 1
            if len(tree_lines) < MAX_TREE_ENTRIES:
                tree_lines.append(f"{'  ' * depth}- {fname}")
            if fname.lower() in KEY_NAMES and len(key_files) < 12:
                key_files.append(fpath)

    sections = [
        f"# {root.name}",
        "",
        f"- **Dossier** : `{root}`",
        f"- **Fichiers** : {n_files}",
        "",
        "## Composition",
        "",
    ]
    sections += [f"- `{ext}` : {count}" for ext, count in ext_counter.most_common(20)]
    sections += ["", "## Arborescence", ""] + tree_lines[:MAX_TREE_ENTRIES]
    if n_files > MAX_TREE_ENTRIES:
        sections.append(f"\n_… arborescence tronquee ({n_files} fichiers au total)._")

    sections += ["", "## Fichiers cles (contenu)", ""]
    for f in key_files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")[:MAX_KEY_FILE_CHARS]
        except OSError:
            continue
        rel = f.relative_to(root)
        fence = "````" if "```" in text else "```"
        lang = f.suffix.lstrip(".")
        sections += [f"### `{rel}`", "", f"{fence}{lang}", text, fence, ""]

    if not key_files:
        ws.warn("Aucun fichier d'entree canonique (README, package.json, main.py…) reconnu.")
        ws.suggest("Identifier a la main les 2-3 fichiers qui portent le savoir-faire, puis les lire directement.")

    ws.write_content("\n".join(sections))

    return {
        "title": root.name,
        "coverage": {
            "text": "sampled",
            "visual": "n/a",
            "structure": "ok",
        },
        "stats": {"files": n_files, "key_files": len(key_files), "extensions": len(ext_counter)},
        "extra": {
            "top_extensions": [e for e, _ in ext_counter.most_common(8)],
            "key_files": [str(f.relative_to(root)) for f in key_files],
        },
    }
