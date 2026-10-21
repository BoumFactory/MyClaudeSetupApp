#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
algos.py — Liste les algorithmes Python attendus (type='algorithme').

Inclut le code Python attendu (champ `algorithmes_attendus[*].code_python`)
quand il est présent dans la compétence.

Usage :
    python scripts/algos.py                          # tous niveaux
    python scripts/algos.py --niveau 1SPE            # 1SPE uniquement
    python scripts/algos.py --niveau TSPE --code     # avec code Python
    python scripts/algos.py --format json
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


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--niveau", choices=NIVEAUX)
    ap.add_argument("--code", action="store_true",
                    help="Afficher le code Python attendu (sinon : titres seulement)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if not ALL_FLAT.exists():
        print("Erreur : data/json/all_flat.json absent.", file=sys.stderr)
        sys.exit(1)
    all_comps = json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]

    algos = [c for c in all_comps if c["type"] == "algorithme"]
    if args.niveau:
        algos = [c for c in algos if c["niveau"] == args.niveau]

    if args.format == "json":
        print(json.dumps(algos, ensure_ascii=False, indent=2))
        return

    if not algos:
        print("(aucun algorithme trouvé pour ce filtre)")
        return

    by_niv: dict[str, list[dict]] = {}
    for c in algos:
        by_niv.setdefault(c["niveau"], []).append(c)
    order = {n: i for i, n in enumerate(NIVEAUX)}

    total = 0
    for niveau in sorted(by_niv, key=lambda n: order.get(n, 99)):
        comps = by_niv[niveau]
        total += len(comps)
        print(f"\n=== {niveau} — {len(comps)} algorithme(s) ===")
        for c in comps:
            sd = c.get("sous_domaine") or "(à classer)"
            src = c.get("source", {})
            print(f"  {c['code']:14} | {sd[:35]:35} | p.{src.get('page','?'):>3}")
            print(f"                 « {c['intitule']} »")
            if args.code and c.get("algorithmes_attendus"):
                for a in c["algorithmes_attendus"]:
                    if a.get("code_python"):
                        print(f"     --- {a.get('titre','algorithme')} ---")
                        for ln in a["code_python"].splitlines():
                            print(f"     | {ln}")
    print(f"\nTotal : {total} algorithme(s)")


if __name__ == "__main__":
    main()
