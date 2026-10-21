#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
05_build_indexes.py — Construit les indexes dérivés depuis les JSON niveau.

Phase 6 du pipeline. Produit :
  - data/json/all_flat.json : liste plate de toutes les compétences (tous niveaux confondus)
  - data/index.json : index principal (stats + lookup par code)
  - data/search_index.sqlite : index FTS5 SQLite pour recherche full-text

Usage :
    python scripts/build/05_build_indexes.py
"""

import io
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
JSON_DIR = DATA_DIR / "json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def list_niveau_files() -> list[Path]:
    return sorted(p for p in JSON_DIR.glob("*.json") if p.name not in ("schema.json", "all_flat.json"))


def flatten_competences() -> tuple[list[dict], dict]:
    """Retourne (liste plate compétences, stats)."""
    flat = []
    by_niveau = {}
    by_domaine = {}
    by_type = {}
    for f in list_niveau_files():
        data = json.load(open(f, encoding='utf-8'))
        niveau = data["meta"]["niveau"]
        for dom, themes in data.get("competences_by_theme", {}).items():
            for theme, comps in themes.items():
                for c in comps:
                    flat.append(c)
                    by_niveau[niveau] = by_niveau.get(niveau, 0) + 1
                    by_domaine[dom] = by_domaine.get(dom, 0) + 1
                    by_type[c["type"]] = by_type.get(c["type"], 0) + 1
    stats = {
        "total_competences": len(flat),
        "by_niveau": by_niveau,
        "by_domaine": by_domaine,
        "by_type": by_type
    }
    return flat, stats


def build_all_flat(flat: list[dict]):
    out = DATA_DIR / "json" / "all_flat.json"
    payload = {
        "version": "2.0",
        "generated_at": now_iso(),
        "total": len(flat),
        "competences": flat
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
    print(f"  → all_flat.json ({len(flat)} compétences)")


def build_index_json(flat: list[dict], stats: dict):
    out = DATA_DIR / "index.json"
    DOMAIN_KEBAB = {
        "NB": "nombres", "AL": "algebre", "AN": "analyse", "GEO": "geometrie",
        "GM": "grandeurs-mesures", "STA": "statistiques", "PR": "probabilites",
        "OGD": "organisation-gestion-donnees", "ALGO": "algorithmique",
        "TRG": "trigonometrie", "LOG": "logique"
    }
    CYCLE = {"5E": "college/cycle4", "4E": "college/cycle4", "3E": "college/cycle4",
             "2GT": "lycee", "1SPE": "lycee", "1ENS": "lycee", "1TEC": "lycee",
             "TSPE": "lycee", "TCOMP": "lycee", "TTEC": "lycee"}

    competences = {}
    for c in flat:
        cycle = CYCLE.get(c["niveau"], "lycee")
        dom_k = DOMAIN_KEBAB.get(c["domaine"], c["domaine"].lower())
        competences[c["code"]] = {
            "json_path": f"json/{c['niveau']}.json",
            "md_path": f"markdown/{cycle}/{c['niveau']}/{dom_k}/{c['code']}.md",
            "intitule": c.get("intitule", ""),
            "fingerprint": c.get("fingerprint", ""),
            "niveau": c["niveau"],
            "domaine": c["domaine"],
            "type": c["type"],
            "tags": c.get("tags", []),
            "source": {"pdf": c["source"].get("pdf", ""), "page": c["source"].get("page", 0)}
        }
    payload = {
        "version": "2.0",
        "generated_at": now_iso(),
        "stats": stats,
        "competences": competences
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
    print(f"  → index.json ({len(competences)} entrées)")


def build_fts_sqlite(flat: list[dict]):
    db_path = DATA_DIR / "search_index.sqlite"
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    # Table 1 : compétences atomiques
    cur.execute("""
        CREATE VIRTUAL TABLE competences_fts USING fts5(
            code UNINDEXED,
            intitule,
            formulation_bo,
            description_detaillee,
            connaissances,
            capacites,
            tags,
            niveau UNINDEXED,
            domaine UNINDEXED,
            type UNINDEXED,
            tokenize='unicode61 remove_diacritics 2'
        )
    """)
    # Table 2 : automatismes (string array du JSON niveau)
    cur.execute("""
        CREATE VIRTUAL TABLE automatismes_fts USING fts5(
            auto_id UNINDEXED,
            niveau UNINDEXED,
            text,
            tokenize='unicode61 remove_diacritics 2'
        )
    """)
    # Insertion automatismes depuis les JSON niveau
    auto_count = 0
    for f in list_niveau_files():
        data = json.load(open(f, encoding='utf-8'))
        niveau = data["meta"]["niveau"]
        for i, auto_text in enumerate(data.get("automatismes", []) or [], 1):
            if not auto_text or not auto_text.strip():
                continue
            auto_id = f"{niveau}-AUTO-{i:03d}"
            cur.execute(
                "INSERT INTO automatismes_fts (auto_id, niveau, text) VALUES (?,?,?)",
                (auto_id, niveau, auto_text)
            )
            auto_count += 1

    for c in flat:
        cur.execute(
            "INSERT INTO competences_fts (code,intitule,formulation_bo,description_detaillee,connaissances,capacites,tags,niveau,domaine,type) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (
                c["code"],
                c.get("intitule", ""),
                c.get("formulation_bo", ""),
                c.get("description_detaillee", ""),
                " ".join(c.get("connaissances_associees", [])),
                " ".join(c.get("capacites_attendues", [])),
                " ".join(c.get("tags", [])),
                c["niveau"],
                c["domaine"],
                c["type"]
            )
        )
    con.commit()

    # Tests de perf
    import time
    t0 = time.perf_counter()
    cur.execute("SELECT code FROM competences_fts WHERE competences_fts MATCH 'demonstration OR derivee OR pythagore'")
    rows = cur.fetchall()
    dt_ms = (time.perf_counter() - t0) * 1000
    print(f"  → search_index.sqlite : {len(flat)} compétences indexées, query test {dt_ms:.1f} ms, {len(rows)} hits")

    t1 = time.perf_counter()
    cur.execute("SELECT auto_id FROM automatismes_fts WHERE automatismes_fts MATCH 'thales OR pythagore OR mediane'")
    arows = cur.fetchall()
    dt2_ms = (time.perf_counter() - t1) * 1000
    print(f"  → automatismes_fts    : {auto_count} automatismes indexés, query test {dt2_ms:.1f} ms, {len(arows)} hits")
    con.close()


def main():
    flat, stats = flatten_competences()
    print(f"Build indexes ({stats['total_competences']} compétences)")
    build_all_flat(flat)
    build_index_json(flat, stats)
    build_fts_sqlite(flat)
    print("OK")


if __name__ == "__main__":
    main()
