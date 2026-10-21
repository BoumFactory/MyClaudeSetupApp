#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
get.py — Affiche le détail complet d'une compétence à partir de son code.

Sortie : intitulé, formulation BO verbatim, sous-domaine, source PDF/page,
image-preuve, prérequis/liens (si présents).

Usage :
    python scripts/get.py CM1-NB-014
    python scripts/get.py TSPE-AN-031
    python scripts/get.py 4E-GEO-004 --format json

Codes inconnus → suggestion des 5 codes les plus proches dans le même
niveau+domaine.
"""

import argparse
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"


def load_all() -> list[dict]:
    if not ALL_FLAT.exists():
        print("Erreur : data/json/all_flat.json absent. Lancer 05_build_indexes.py.", file=sys.stderr)
        sys.exit(1)
    return json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]


def render_text(c: dict) -> str:
    src = c.get("source", {})
    out = []
    out.append(f"Code         : {c['code']}")
    out.append(f"Niveau       : {c['niveau']}")
    out.append(f"Domaine      : {c['domaine']}")
    out.append(f"Sous-domaine : {c.get('sous_domaine', '(non renseigné)')}")
    out.append(f"Type         : {c['type']}")
    out.append("")
    out.append(f"Intitulé     : {c['intitule']}")
    out.append("")
    out.append("Formulation BO (verbatim) :")
    out.append(f"  « {c['formulation_bo']} »")
    out.append("")
    out.append(f"Source       : {src.get('pdf', '?')}, page {src.get('page', '?')}")
    if src.get("bo_reference"):
        out.append(f"BO référence : {src['bo_reference']}")
    if src.get("page_image"):
        out.append(f"Image-preuve : {src['page_image']}")
    if src.get("bo_url"):
        out.append(f"BO URL       : {src['bo_url']}")
    if c.get("prerequis"):
        out.append("")
        out.append(f"Prérequis    : {', '.join(c['prerequis'])}")
    if c.get("liens"):
        out.append(f"Liens        : {', '.join(c['liens'])}")
    if c.get("demonstrations_exigibles"):
        out.append("")
        out.append("Démonstrations exigibles :")
        for d in c["demonstrations_exigibles"]:
            out.append(f"  - {d}")
    if c.get("algorithmes_attendus"):
        out.append("")
        out.append("Algorithmes attendus :")
        for a in c["algorithmes_attendus"]:
            out.append(f"  - {a.get('titre', '?')}")
            if a.get("code_python"):
                out.append("    ```python")
                for ln in a["code_python"].splitlines():
                    out.append(f"    {ln}")
                out.append("    ```")
    return "\n".join(out)


def suggest_close(code: str, all_comps: list[dict]) -> list[str]:
    """Suggère 5 codes proches au sein du même niveau-domaine."""
    parts = code.split("-")
    if len(parts) < 2:
        return []
    niveau, dom = parts[0], parts[1]
    same = sorted(c["code"] for c in all_comps if c["niveau"] == niveau and c["domaine"] == dom)
    return same[:5]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("code", help="Code d'une compétence (ex: CM1-NB-014)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    all_comps = load_all()
    target = next((c for c in all_comps if c["code"] == args.code), None)

    if target is None:
        print(f"Code introuvable : {args.code}", file=sys.stderr)
        suggestions = suggest_close(args.code, all_comps)
        if suggestions:
            print(f"  Codes proches au sein du niveau-domaine : {', '.join(suggestions)}",
                  file=sys.stderr)
        sys.exit(2)

    if args.format == "json":
        print(json.dumps(target, ensure_ascii=False, indent=2))
    else:
        print(render_text(target))


if __name__ == "__main__":
    main()
