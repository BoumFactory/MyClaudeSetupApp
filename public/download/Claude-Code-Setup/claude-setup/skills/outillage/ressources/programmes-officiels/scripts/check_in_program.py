#!/usr/bin/env python3
"""
Verifie si une notion est au programme d'un niveau donne.

Usage:
    python check_in_program.py --notion "pythagore" --niveau 5E
    python check_in_program.py --notion "thales" --niveau 4E
    python check_in_program.py --notion "equation" --niveau 3E
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
    parser = argparse.ArgumentParser(description="Verifier si une notion est au programme")
    parser.add_argument("--notion", "-n", required=True, help="Notion a verifier")
    parser.add_argument("--niveau", required=True, help="Niveau (C3, 5E, 4E, 3E)")

    args = parser.parse_args()
    niveau = args.niveau.upper()

    competences = load_flat_competences(niveau)
    if not competences:
        print(json.dumps({"error": f"Niveau {niveau} non trouve"}))
        return

    results = search_notion(competences, args.notion)

    output = {
        "question": f"Est-ce que '{args.notion}' est au programme de {niveau} ?",
        "reponse": len(results) > 0,
        "niveau": niveau,
        "notion": args.notion,
        "count": len(results)
    }

    if results:
        output["verdict"] = f"OUI - {len(results)} competence(s) trouvee(s)"
        output["exemples"] = [
            {"code": c.get("code"), "intitule": c.get("intitule")}
            for c in results[:5]
        ]
    else:
        output["verdict"] = f"NON - '{args.notion}' n'est pas au programme de {niveau}"

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
