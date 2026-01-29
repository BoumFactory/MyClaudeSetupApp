#!/usr/bin/env python3
"""
Verifie si une notion est nouvelle a un niveau ou si c'est un prerequis.

Usage:
    python is_new_at_level.py --notion "pythagore" --niveau 4E
    python is_new_at_level.py --notion "fraction" --niveau 5E
"""

import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"
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
    current_order = NIVEAUX_ORDER.get(niveau.upper(), 0)
    return [n for n, order in NIVEAUX_ORDER.items() if order < current_order]

def main():
    parser = argparse.ArgumentParser(description="Verifier si une notion est nouvelle")
    parser.add_argument("--notion", "-n", required=True, help="Notion a verifier")
    parser.add_argument("--niveau", required=True, help="Niveau cible")

    args = parser.parse_args()
    niveau = args.niveau.upper()
    lower_levels = get_lower_levels(niveau)

    # Verifier au niveau cible
    current_comps = load_flat_competences(niveau)
    current_results = search_notion(current_comps, args.notion)

    # Verifier aux niveaux inferieurs
    prerequis_found = {}
    total_prerequis = 0
    for lvl in lower_levels:
        comps = load_flat_competences(lvl)
        results = search_notion(comps, args.notion)
        prerequis_found[lvl] = len(results)
        total_prerequis += len(results)

    output = {
        "question": f"'{args.notion}' est-elle une nouveaute en {niveau} ?",
        "notion": args.notion,
        "niveau": niveau,
        "present_au_niveau": len(current_results) > 0,
        "prerequis_niveaux_inferieurs": prerequis_found,
        "total_prerequis": total_prerequis
    }

    if len(current_results) == 0:
        output["reponse"] = f"'{args.notion}' n'est PAS au programme de {niveau}"
        output["statut"] = "ABSENT"
    elif total_prerequis == 0:
        output["reponse"] = f"'{args.notion}' est une NOUVEAUTE en {niveau}"
        output["statut"] = "NOUVEAUTE"
        output["competences_introduites"] = [
            {"code": c.get("code"), "intitule": c.get("intitule")}
            for c in current_results[:5]
        ]
    else:
        output["reponse"] = f"'{args.notion}' est un APPROFONDISSEMENT en {niveau} (deja vu avant)"
        output["statut"] = "APPROFONDISSEMENT"
        output["competences_niveau"] = [
            {"code": c.get("code"), "intitule": c.get("intitule")}
            for c in current_results[:3]
        ]

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
