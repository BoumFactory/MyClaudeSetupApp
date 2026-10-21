#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
stats.py — Vue d'ensemble du skill : compteurs niveau × domaine × type.

Usage :
    python scripts/stats.py                       # vue globale
    python scripts/stats.py --niveau TSPE         # drill-down TSPE
    python scripts/stats.py --format json
"""

import argparse
import io
import json
import sys
import time
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"
FTS = SKILL_DIR / "data" / "search_index.sqlite"

NIVEAUX = ["CM1", "CM2", "6E", "5E", "4E", "3E", "2GT", "1SPE", "1ENS", "1TEC",
           "TSPE", "TCOMP", "TTEC"]
DOMAINES = ["NB", "AL", "AN", "GEO", "GM", "STA", "PR", "OGD", "ALGO", "TRG", "LOG"]
TYPES = ["contenu", "capacite", "demonstration", "algorithme", "approfondissement"]


def fts_query_ms() -> float | None:
    if not FTS.exists():
        return None
    try:
        import sqlite3
        con = sqlite3.connect(str(FTS))
        cur = con.cursor()
        t0 = time.perf_counter()
        cur.execute("SELECT code FROM competences_fts WHERE competences_fts MATCH 'fonction*' LIMIT 50")
        cur.fetchall()
        ms = (time.perf_counter() - t0) * 1000
        con.close()
        return round(ms, 2)
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--niveau", choices=NIVEAUX, help="Drill-down sur un niveau")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if not ALL_FLAT.exists():
        print("Erreur : data/json/all_flat.json absent.", file=sys.stderr)
        sys.exit(1)
    payload = json.load(open(ALL_FLAT, encoding="utf-8"))
    all_comps = payload["competences"]
    if args.niveau:
        all_comps = [c for c in all_comps if c["niveau"] == args.niveau]

    by_niv = Counter(c["niveau"] for c in all_comps)
    by_dom = Counter(c["domaine"] for c in all_comps)
    by_type = Counter(c["type"] for c in all_comps)
    top_sd = Counter(c.get("sous_domaine") or "(à classer)" for c in all_comps).most_common(10)

    data = {
        "total_competences": len(all_comps),
        "by_niveau": {n: by_niv.get(n, 0) for n in NIVEAUX if by_niv.get(n, 0)},
        "by_domaine": {d: by_dom.get(d, 0) for d in DOMAINES if by_dom.get(d, 0)},
        "by_type": {t: by_type.get(t, 0) for t in TYPES if by_type.get(t, 0)},
        "top_sous_domaines": [{"sous_domaine": sd, "n": n} for sd, n in top_sd],
        "fts5_query_ms": fts_query_ms(),
    }

    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    print(f"=== Skill programmes-officiels — stats {'(' + args.niveau + ')' if args.niveau else 'globales'} ===\n")
    print(f"Total compétences : {data['total_competences']}\n")

    print("Par niveau :")
    for n, k in data["by_niveau"].items():
        bar = "█" * min(40, k // 5 + 1)
        print(f"  {n:6} | {k:4} {bar}")
    print()

    print("Par domaine :")
    for d, k in sorted(data["by_domaine"].items(), key=lambda x: -x[1]):
        print(f"  {d:5} | {k:4}")
    print()

    print("Par type :")
    for t, k in sorted(data["by_type"].items(), key=lambda x: -x[1]):
        print(f"  {t:18} | {k:4}")
    print()

    print("Top 10 sous-domaines :")
    for sd, k in top_sd:
        print(f"  {k:4} | {sd}")
    print()

    if data["fts5_query_ms"] is not None:
        print(f"Performance : FTS5 query test ~{data['fts5_query_ms']} ms")


if __name__ == "__main__":
    main()
