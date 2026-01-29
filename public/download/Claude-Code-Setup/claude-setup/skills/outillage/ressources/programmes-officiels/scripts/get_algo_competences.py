#!/usr/bin/env python3
"""
Recupere les competences algorithmiques/programmation d'un niveau.

Usage:
    python get_algo_competences.py --niveau 5E
    python get_algo_competences.py --niveau 4E --scratch-only
    python get_algo_competences.py --niveau 3E --python-only
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

def filter_algo(competences: list, scratch_only: bool = False, python_only: bool = False) -> list:
    results = []
    for comp in competences:
        # Verifier domaine ALGORITHMIQUE ou type algorithme
        is_algo = (
            comp.get("domaine") == "ALGORITHMIQUE" or
            comp.get("type") == "algorithme"
        )

        if not is_algo:
            searchable = " ".join([
                comp.get("intitule", ""),
                comp.get("description_detaillee", ""),
                " ".join(comp.get("connaissances_associees", []))
            ]).lower()
            is_algo = any(kw in searchable for kw in [
                "algorithme", "programme", "scratch", "python", "boucle",
                "variable", "instruction", "script", "code"
            ])

        if is_algo:
            searchable = (comp.get("intitule", "") + " " + comp.get("description_detaillee", "")).lower()

            if scratch_only and "scratch" not in searchable:
                continue
            if python_only and "python" not in searchable:
                continue

            results.append(comp)

    return results

def main():
    parser = argparse.ArgumentParser(description="Competences algorithmiques")
    parser.add_argument("--niveau", "-n", required=True, help="Niveau")
    parser.add_argument("--scratch-only", action="store_true", help="Scratch uniquement")
    parser.add_argument("--python-only", action="store_true", help="Python uniquement")

    args = parser.parse_args()
    niveau = args.niveau.upper()

    competences = load_flat_competences(niveau)
    results = filter_algo(competences, args.scratch_only, args.python_only)

    output = {
        "niveau": niveau,
        "type": "scratch" if args.scratch_only else ("python" if args.python_only else "tous"),
        "total": len(results),
        "competences": [
            {
                "code": c.get("code"),
                "intitule": c.get("intitule"),
                "description": c.get("description_detaillee"),
                "type": c.get("type")
            }
            for c in results
        ]
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
