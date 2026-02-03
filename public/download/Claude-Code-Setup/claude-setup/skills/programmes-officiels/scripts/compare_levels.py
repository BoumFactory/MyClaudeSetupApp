#!/usr/bin/env python3
"""
Compare les competences sur une notion entre deux niveaux.

Usage:
    python compare_levels.py --notion "fraction" --niveau1 5E --niveau2 4E
    python compare_levels.py --notion "equation" --niveau1 4E --niveau2 3E
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"

def load_flat_competences(niveau: str) -> list:
    file_path = DATA_DIR / f"{niveau}_competences_flat.json"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f).get("competences", [])

def search_notion(competences: list, notion: str) -> list:
    notion_lower = notion.lower()
    results = []
    for comp in competences:
        searchable = " ".join([
            comp.get("intitule", ""),
            comp.get("description_detaillee", ""),
            comp.get("sous_domaine", ""),
            " ".join(comp.get("connaissances_associees", []))
        ]).lower()
        if notion_lower in searchable:
            results.append(comp)
    return results

def main():
    parser = argparse.ArgumentParser(description="Comparer deux niveaux")
    parser.add_argument("--notion", "-n", required=True, help="Notion a comparer")
    parser.add_argument("--niveau1", required=True, help="Premier niveau")
    parser.add_argument("--niveau2", required=True, help="Deuxieme niveau")

    args = parser.parse_args()
    n1 = args.niveau1.upper()
    n2 = args.niveau2.upper()

    comps1 = search_notion(load_flat_competences(n1), args.notion)
    comps2 = search_notion(load_flat_competences(n2), args.notion)

    output = {
        "question": f"Comparaison de '{args.notion}' entre {n1} et {n2}",
        "notion": args.notion,
        n1: {
            "count": len(comps1),
            "competences": [
                {"code": c.get("code"), "intitule": c.get("intitule")}
                for c in comps1
            ]
        },
        n2: {
            "count": len(comps2),
            "competences": [
                {"code": c.get("code"), "intitule": c.get("intitule")}
                for c in comps2
            ]
        },
        "evolution": f"{len(comps1)} -> {len(comps2)} competences"
    }

    if len(comps2) > len(comps1):
        output["analyse"] = f"Approfondissement en {n2} (+{len(comps2) - len(comps1)} competences)"
    elif len(comps2) < len(comps1):
        output["analyse"] = f"Moins de focus en {n2} ({len(comps1) - len(comps2)} competences en moins)"
    else:
        output["analyse"] = "Meme volume de competences"

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
