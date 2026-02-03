#!/usr/bin/env python3
"""
Trouve les prerequis d'une notion (competences des niveaux inferieurs).

Usage:
    python get_prerequisites.py --niveau 4E --notion "pythagore"
    python get_prerequisites.py --niveau 3E --notion "fonction"
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"

# Ordre des niveaux
NIVEAUX_ORDER = {"C3": 0, "5E": 1, "4E": 2, "3E": 3}

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

def get_lower_levels(niveau: str) -> list:
    """Retourne les niveaux inferieurs."""
    current_order = NIVEAUX_ORDER.get(niveau.upper(), 0)
    return [n for n, order in NIVEAUX_ORDER.items() if order < current_order]

def main():
    parser = argparse.ArgumentParser(description="Prerequis d'une notion")
    parser.add_argument("--niveau", "-n", required=True, help="Niveau cible")
    parser.add_argument("--notion", required=True, help="Notion a etudier")

    args = parser.parse_args()
    niveau = args.niveau.upper()
    lower_levels = get_lower_levels(niveau)

    output = {
        "niveau_cible": niveau,
        "notion": args.notion,
        "prerequis": {}
    }

    total = 0
    for lvl in lower_levels:
        competences = load_flat_competences(lvl)
        results = search_notion(competences, args.notion)
        total += len(results)
        output["prerequis"][lvl] = [
            {
                "code": c.get("code"),
                "intitule": c.get("intitule"),
                "type": c.get("type")
            }
            for c in results
        ]

    output["total_prerequis"] = total

    # Ajouter aussi les competences du niveau cible pour comparaison
    current_competences = load_flat_competences(niveau)
    current_results = search_notion(current_competences, args.notion)
    output["competences_niveau_cible"] = [
        {"code": c.get("code"), "intitule": c.get("intitule")}
        for c in current_results
    ]

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
