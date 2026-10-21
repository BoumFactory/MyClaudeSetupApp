#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
demos.py — Liste les démonstrations exigibles (type='demonstration').

Usage :
    python scripts/demos.py                                # toutes
    python scripts/demos.py --niveau TSPE                  # TSPE uniquement
    python scripts/demos.py --niveau TSPE --domaine AN     # TSPE / Analyse
    python scripts/demos.py --format json                  # JSON
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

NIVEAUX = ["CM1", "CM2", "6E", "5E", "4E", "3E", "2GT", "1SPE", "1ENS", "1TEC",
           "TSPE", "TCOMP", "TTEC"]
DOMAINES = ["NB", "AL", "AN", "GEO", "GM", "STA", "PR", "OGD", "ALGO", "TRG", "LOG"]


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--niveau", choices=NIVEAUX)
    ap.add_argument("--domaine", choices=DOMAINES)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if not ALL_FLAT.exists():
        print("Erreur : data/json/all_flat.json absent.", file=sys.stderr)
        sys.exit(1)
    all_comps = json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]

    demos = [c for c in all_comps if c["type"] == "demonstration"]
    if args.niveau:
        demos = [c for c in demos if c["niveau"] == args.niveau]
    if args.domaine:
        demos = [c for c in demos if c["domaine"] == args.domaine]

    if args.format == "json":
        print(json.dumps(demos, ensure_ascii=False, indent=2))
        return

    if not demos:
        print("(aucune démonstration trouvée pour ce filtre)")
        return

    # Groupement par niveau pour lisibilité
    by_niv: dict[str, list[dict]] = {}
    for c in demos:
        by_niv.setdefault(c["niveau"], []).append(c)
    order = {n: i for i, n in enumerate(NIVEAUX)}

    total = 0
    for niveau in sorted(by_niv, key=lambda n: order.get(n, 99)):
        comps = by_niv[niveau]
        total += len(comps)
        print(f"\n=== {niveau} — {len(comps)} démonstration(s) ===")
        for c in comps:
            sd = c.get("sous_domaine") or "(à classer)"
            src = c.get("source", {})
            print(f"  {c['code']:14} | {c['domaine']:5} | {sd[:30]:30} | p.{src.get('page','?'):>3}")
            print(f"                 « {c['intitule']} »")
    print(f"\nTotal : {total} démonstration(s)")


if __name__ == "__main__":
    main()
