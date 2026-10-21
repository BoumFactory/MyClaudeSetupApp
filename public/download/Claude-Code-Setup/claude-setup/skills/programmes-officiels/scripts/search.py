#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
search.py — Recherche principale dans le skill programmes-officiels.

Lit data/json/all_flat.json + data/search_index.sqlite (FTS5).

Usage :
    python scripts/search.py --keyword "pythagore"
    python scripts/search.py --keyword "derivee" --niveau TSPE
    python scripts/search.py --code 2GT-NB-008
    python scripts/search.py --niveau 2GT --domaine NB --type demonstration
    python scripts/search.py --query "loi des grands nombres" --format json
    python scripts/search.py --type algorithme --format short
"""

import argparse
import io
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
ALL_FLAT = DATA_DIR / "json" / "all_flat.json"
FTS = DATA_DIR / "search_index.sqlite"

NIVEAUX_VALIDES = ["CM1", "CM2", "6E", "5E", "4E", "3E", "2GT", "1SPE", "1ENS", "1TEC", "TSPE", "TCOMP", "TTEC"]
DOMAINES_VALIDES = ["NB", "AL", "AN", "GEO", "GM", "STA", "PR", "OGD", "ALGO", "TRG", "LOG"]
TYPES_VALIDES = ["contenu", "capacite", "demonstration", "algorithme", "approfondissement"]


def load_all() -> list[dict]:
    if not ALL_FLAT.exists():
        print("Erreur : all_flat.json manquant. Lancer scripts/build/05_build_indexes.py.", file=sys.stderr)
        sys.exit(1)
    return json.load(open(ALL_FLAT, encoding='utf-8'))["competences"]


def filter_structural(comps, niveau=None, domaine=None, type_=None, code=None):
    out = comps
    if code:
        out = [c for c in out if c["code"] == code]
    if niveau:
        out = [c for c in out if c["niveau"] == niveau]
    if domaine:
        out = [c for c in out if c["domaine"] == domaine]
    if type_:
        out = [c for c in out if c["type"] == type_]
    return out


def search_keyword(keyword: str) -> list[str]:
    """Retourne la liste des codes matchés via FTS5."""
    if not FTS.exists():
        print("Erreur : search_index.sqlite manquant. Lancer scripts/build/05_build_indexes.py.", file=sys.stderr)
        sys.exit(1)
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    # Échappement minimal des caractères spéciaux FTS5
    safe = keyword.replace('"', '""')
    cur.execute(f'SELECT code FROM competences_fts WHERE competences_fts MATCH ? ORDER BY rank LIMIT 100', (f'"{safe}"',))
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows


def search_query_fts(query: str) -> list[str]:
    """Recherche FTS5 brute (peut contenir des opérateurs MATCH)."""
    if not FTS.exists():
        sys.exit(1)
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    cur.execute('SELECT code FROM competences_fts WHERE competences_fts MATCH ? ORDER BY rank LIMIT 100', (query,))
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows


def search_automatismes(keyword: str, niveau: str | None = None) -> list[dict]:
    """Recherche dans la table automatismes_fts. Retourne dicts avec auto_id, niveau, text."""
    if not FTS.exists():
        return []
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    safe = keyword.replace('"', '""')
    sql = 'SELECT auto_id, niveau, text FROM automatismes_fts WHERE automatismes_fts MATCH ?'
    params = [f'"{safe}"']
    if niveau:
        sql += ' AND niveau = ?'
        params.append(niveau)
    sql += ' ORDER BY rank LIMIT 50'
    cur.execute(sql, params)
    rows = [{"auto_id": r[0], "niveau": r[1], "text": r[2]} for r in cur.fetchall()]
    con.close()
    return rows


def format_output(comps, fmt="medium"):
    if fmt == "json":
        return json.dumps(comps, ensure_ascii=False, indent=2)
    if fmt == "short":
        return "\n".join(f"{c['code']} | {c['niveau']} {c['domaine']} {c['type']:14} | {c['intitule']}" for c in comps)
    # medium
    lines = []
    for c in comps:
        lines.append(f"━━━ {c['code']} ({c['niveau']} {c['domaine']} {c['type']}) ━━━")
        lines.append(f"  {c['intitule']}")
        if c.get("formulation_bo"):
            fbo = c["formulation_bo"]
            if len(fbo) > 220:
                fbo = fbo[:220] + "…"
            lines.append(f"  BO : « {fbo} »")
        src = c.get("source", {})
        lines.append(f"  Source : {src.get('pdf')} p.{src.get('page')} — {src.get('bo_reference')}")
        lines.append("")
    return "\n".join(lines)


def format_automatismes(autos, fmt="medium"):
    if not autos:
        return ""
    if fmt == "json":
        return json.dumps(autos, ensure_ascii=False, indent=2)
    if fmt == "short":
        return "\n".join(f"{a['auto_id']} | {a['niveau']:5} AUTOMATISME    | {a['text']}" for a in autos)
    lines = ["", "═══ Automatismes correspondants ═══"]
    for a in autos:
        lines.append(f"  [{a['niveau']}] {a['text']}")
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description="Recherche compétences programmes-officiels")
    p.add_argument("--keyword", help="Mot-clé simple (FTS5)")
    p.add_argument("--query", help="Requête FTS5 brute (opérateurs OR/AND/NOT)")
    p.add_argument("--code", help="Code exact d'une compétence (ex: 2GT-NB-008)")
    p.add_argument("--niveau", choices=NIVEAUX_VALIDES, help="Filtre niveau")
    p.add_argument("--domaine", choices=DOMAINES_VALIDES, help="Filtre domaine")
    p.add_argument("--type", dest="type_", choices=TYPES_VALIDES, help="Filtre type")
    p.add_argument("--all-levels", action="store_true", help="Ne filtre pas par niveau (défaut)")
    p.add_argument("--format", choices=["json", "medium", "short"], default="medium")
    p.add_argument("--limit", type=int, default=50)
    p.add_argument("--no-automatismes", action="store_true", help="N'inclut pas les automatismes dans les résultats")
    p.add_argument("--only-automatismes", action="store_true", help="Cherche uniquement dans automatismes")
    args = p.parse_args()

    if args.keyword == "":
        print("Erreur : --keyword vide.", file=sys.stderr); sys.exit(2)

    all_comps = load_all()
    if args.code:
        results = [c for c in all_comps if c["code"] == args.code]
        if not results:
            print(f"Code non trouvé : {args.code}", file=sys.stderr); sys.exit(3)
    elif args.keyword or args.query:
        matched = search_keyword(args.keyword) if args.keyword else search_query_fts(args.query)
        by_code = {c["code"]: c for c in all_comps}
        results = [by_code[code] for code in matched if code in by_code]
        results = filter_structural(results, niveau=args.niveau, domaine=args.domaine, type_=args.type_)
    else:
        results = filter_structural(all_comps, niveau=args.niveau, domaine=args.domaine, type_=args.type_)

    # Recherche dans automatismes (si keyword/query, pas si --code)
    autos = []
    if (args.keyword or args.query) and not args.code and not args.no_automatismes:
        kw = args.keyword or args.query
        autos = search_automatismes(kw, niveau=args.niveau)

    if not results and not autos:
        print("(aucun résultat)", file=sys.stderr); sys.exit(4)

    if args.only_automatismes:
        print(format_automatismes(autos, args.format) if autos else "(aucun automatisme)")
        return

    if results:
        results = results[: args.limit]
        print(format_output(results, args.format))

    if autos and not args.no_automatismes:
        print(format_automatismes(autos[: args.limit], args.format))


if __name__ == "__main__":
    main()
