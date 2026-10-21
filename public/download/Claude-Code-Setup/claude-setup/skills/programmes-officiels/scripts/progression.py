#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
progression.py — Trace la progression verticale d'une notion à travers les niveaux.

Cherche un mot-clé (FTS5) et regroupe les compétences par niveau dans l'ordre
scolaire (CM1 → CM2 → 6E → 5E → 4E → 3E → 2GT → 1SPE/1ENS/1TEC →
TSPE/TCOMP/TTEC). Utile pour voir comment une notion (ex: "fraction") est
introduite, consolidée et étendue de l'école élémentaire au lycée.

Usage :
    python scripts/progression.py "fraction*"
    python scripts/progression.py "pythagore" --type capacite
    python scripts/progression.py "derivation"
    python scripts/progression.py "binomiale" --format json

Le wildcard FTS5 (*) est conseillé pour couvrir singulier et pluriel.
"""

import argparse
import io
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"
FTS = SKILL_DIR / "data" / "search_index.sqlite"

NIVEAUX_ORDER = ["CM1", "CM2", "6E", "5E", "4E", "3E", "2GT", "1SPE", "1ENS",
                 "1TEC", "TSPE", "TCOMP", "TTEC"]
TYPES_VALIDES = ["contenu", "capacite", "demonstration", "algorithme", "approfondissement"]


def search_fts(keyword: str) -> list[str]:
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    cur.execute(
        "SELECT code FROM competences_fts WHERE competences_fts MATCH ? ORDER BY rank LIMIT 1000",
        (keyword,),
    )
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("keyword", help="Mot-clé FTS5 (wildcard * conseillé)")
    ap.add_argument("--type", choices=TYPES_VALIDES)
    ap.add_argument("--format", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if not ALL_FLAT.exists() or not FTS.exists():
        print("Erreur : indexes manquants (all_flat.json / search_index.sqlite).",
              file=sys.stderr)
        sys.exit(1)
    all_comps = json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]
    by_code = {c["code"]: c for c in all_comps}

    codes = search_fts(args.keyword)
    matched = [by_code[c] for c in codes if c in by_code]
    if args.type:
        matched = [c for c in matched if c["type"] == args.type]

    # Groupement par niveau dans l'ordre scolaire
    by_niv: dict[str, list[dict]] = {n: [] for n in NIVEAUX_ORDER}
    for c in matched:
        if c["niveau"] in by_niv:
            by_niv[c["niveau"]].append(c)

    if args.format == "json":
        out = {n: by_niv[n] for n in NIVEAUX_ORDER if by_niv[n]}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    if not matched:
        print(f"(aucun résultat pour « {args.keyword} »)")
        return

    print(f"Progression de « {args.keyword} » à travers les niveaux\n")
    total = 0
    for niveau in NIVEAUX_ORDER:
        comps = by_niv[niveau]
        if not comps:
            continue
        total += len(comps)
        print(f"--- {niveau} ({len(comps)}) ---")
        for c in comps:
            sd = c.get("sous_domaine") or "(à classer)"
            print(f"  {c['code']:14} [{c['type']:14}] {sd[:30]:30}")
            print(f"                 « {c['intitule'][:100]} »")
        print()
    print(f"Total : {total} compétence(s) sur {sum(1 for n in NIVEAUX_ORDER if by_niv[n])} niveau(x)")


if __name__ == "__main__":
    main()
