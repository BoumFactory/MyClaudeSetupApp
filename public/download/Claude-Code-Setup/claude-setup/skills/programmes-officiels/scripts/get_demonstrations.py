#!/usr/bin/env python3
"""
Liste les demonstrations exigibles d'un niveau.

Usage:
    python get_demonstrations.py --niveau 4E
    python get_demonstrations.py --all-levels
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

def filter_demonstrations(competences: list) -> list:
    results = []
    for comp in competences:
        if comp.get("type") == "demonstration":
            results.append(comp)
        else:
            # Verifier dans le contenu
            searchable = " ".join([
                comp.get("intitule", ""),
                comp.get("description_detaillee", "")
            ]).lower()
            if any(kw in searchable for kw in ["demontrer", "prouver", "demonstration", "justifier"]):
                results.append(comp)
    return results

def main():
    parser = argparse.ArgumentParser(description="Demonstrations exigibles")
    parser.add_argument("--niveau", "-n", help="Niveau")
    parser.add_argument("--all-levels", action="store_true", help="Tous niveaux")

    args = parser.parse_args()

    if not args.niveau and not args.all_levels:
        print("Erreur: --niveau ou --all-levels requis")
        return

    niveaux = NIVEAUX if args.all_levels else [args.niveau.upper()]

    output = {"demonstrations": {}}

    for niveau in niveaux:
        competences = load_flat_competences(niveau)
        results = filter_demonstrations(competences)
        output["demonstrations"][niveau] = [
            {
                "code": c.get("code"),
                "intitule": c.get("intitule"),
                "domaine": c.get("domaine"),
                "formulation_bo": c.get("formulation_bo")
            }
            for c in results
        ]

    output["total"] = sum(len(v) for v in output["demonstrations"].values())
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
