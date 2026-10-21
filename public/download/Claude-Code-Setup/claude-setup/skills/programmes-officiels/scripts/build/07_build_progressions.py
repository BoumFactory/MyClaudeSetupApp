#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
07_build_progressions.py — Construit le graphe de progressions.

Phase 8 du pipeline. Lit data/json/all_flat.json (généré par 05_build_indexes.py),
extrait les champs `prerequis` et `liens` de chaque compétence, et produit
data/progressions.json (nodes + edges) au format :

  {
    "nodes": ["2GT-NB-001", ...],
    "edges": [
      {"from": "3E-NB-007", "to": "2GT-NB-001", "type": "prerequis"},
      {"from": "2GT-NB-001", "to": "1SPE-NB-003", "type": "lien"}
    ]
  }

Usage :
    python scripts/build/07_build_progressions.py
"""

import io
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
ALL_FLAT = DATA_DIR / "json" / "all_flat.json"
OUT = DATA_DIR / "progressions.json"


def main():
    if not ALL_FLAT.exists():
        print("all_flat.json manquant — lancer scripts/build/05_build_indexes.py d'abord.")
        sys.exit(1)
    payload = json.load(open(ALL_FLAT, encoding='utf-8'))
    flat = payload["competences"]

    nodes = [c["code"] for c in flat]
    edges = []
    unresolved = []

    code_set = set(nodes)

    for c in flat:
        # Prérequis : autre compétence → compétence courante
        for pre in c.get("prerequis", []) or []:
            if pre in code_set:
                edges.append({"from": pre, "to": c["code"], "type": "prerequis"})
            else:
                unresolved.append({"code": c["code"], "missing_prerequis": pre})
        # Liens transversaux : bidirectionnels (1 seul edge stocké, on évite doublon)
        for li in c.get("liens", []) or []:
            if li in code_set:
                pair = tuple(sorted([c["code"], li]))
                edges.append({"from": pair[0], "to": pair[1], "type": "lien"})

    # Déduplication des liens
    seen = set()
    dedup = []
    for e in edges:
        k = (e["from"], e["to"], e["type"])
        if k in seen:
            continue
        seen.add(k)
        dedup.append(e)

    out_payload = {
        "version": "2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec='seconds'),
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(dedup),
            "by_type": {
                "prerequis": sum(1 for e in dedup if e["type"] == "prerequis"),
                "lien": sum(1 for e in dedup if e["type"] == "lien")
            },
            "unresolved_prerequis": len(unresolved)
        },
        "nodes": nodes,
        "edges": dedup,
        "unresolved_prerequis": unresolved
    }
    OUT.write_text(json.dumps(out_payload, ensure_ascii=False, indent=2), encoding='utf-8', newline='\n')
    print(f"progressions.json : {len(nodes)} nodes, {len(dedup)} edges")
    print(f"  prérequis : {out_payload['stats']['by_type']['prerequis']}, liens : {out_payload['stats']['by_type']['lien']}")
    if unresolved:
        print(f"  ⚠ {len(unresolved)} prérequis non résolus (compétences référencées mais pas encore extraites — normal en cours de construction)")
        for u in unresolved[:5]:
            print(f"    - {u['code']} → manque {u['missing_prerequis']}")


if __name__ == "__main__":
    main()
