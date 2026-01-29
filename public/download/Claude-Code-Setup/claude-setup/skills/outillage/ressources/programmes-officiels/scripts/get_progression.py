#!/usr/bin/env python3
"""
Affiche la progression d'une notion a travers les niveaux.
Utile pour voir l'evolution d'un concept de C3 a 3E.

Usage:
    python get_progression.py --notion "fraction"
    python get_progression.py --notion "pythagore"
    python get_progression.py --notion "equation"
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
    parser = argparse.ArgumentParser(description="Progression d'une notion")
    parser.add_argument("--notion", "-n", required=True, help="Notion a suivre")
    parser.add_argument("--compact", action="store_true", help="Sortie compacte")

    args = parser.parse_args()

    progression = {
        "notion": args.notion,
        "progression": {}
    }

    total = 0
    for niveau in NIVEAUX:
        competences = load_flat_competences(niveau)
        results = search_notion(competences, args.notion)
        total += len(results)

        if args.compact:
            progression["progression"][niveau] = {
                "count": len(results),
                "intitules": [c.get("intitule") for c in results[:10]]  # Max 10
            }
        else:
            progression["progression"][niveau] = {
                "count": len(results),
                "competences": [
                    {
                        "code": c.get("code"),
                        "intitule": c.get("intitule"),
                        "sous_domaine": c.get("sous_domaine")
                    }
                    for c in results
                ]
            }

    progression["total"] = total
    print(json.dumps(progression, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
