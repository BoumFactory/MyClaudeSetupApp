#!/usr/bin/env python3
"""
Trouve le premier niveau ou une notion apparait.

Usage:
    python find_first_level.py --notion "pythagore"
    python find_first_level.py --notion "equation"
    python find_first_level.py --notion "fonction affine"
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"
NIVEAUX = ["C3", "5E", "4E", "3E"]

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
    parser = argparse.ArgumentParser(description="Trouver le premier niveau d'une notion")
    parser.add_argument("--notion", "-n", required=True, help="Notion a chercher")

    args = parser.parse_args()

    output = {
        "question": f"A quel niveau introduit-on '{args.notion}' ?",
        "notion": args.notion,
        "premier_niveau": None,
        "presence_par_niveau": {}
    }

    for niveau in NIVEAUX:
        competences = load_flat_competences(niveau)
        results = search_notion(competences, args.notion)
        count = len(results)
        output["presence_par_niveau"][niveau] = count

        if count > 0 and output["premier_niveau"] is None:
            output["premier_niveau"] = niveau
            output["premieres_competences"] = [
                {"code": c.get("code"), "intitule": c.get("intitule")}
                for c in results[:3]
            ]

    if output["premier_niveau"]:
        output["reponse"] = f"'{args.notion}' est introduit en {output['premier_niveau']}"
    else:
        output["reponse"] = f"'{args.notion}' n'est pas au programme du college"

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
