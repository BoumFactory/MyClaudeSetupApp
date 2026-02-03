#!/usr/bin/env python3
"""
Resume des competences par domaine pour un niveau.
Utile pour avoir une vue d'ensemble rapide.

Usage:
    python get_domain_summary.py --niveau 5E
    python get_domain_summary.py --niveau 4E --domaine GEOMETRIE
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"

def load_competences(niveau: str) -> dict:
    file_path = DATA_DIR / f"{niveau}_competences.json"
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Resume par domaine")
    parser.add_argument("--niveau", "-n", required=True, help="Niveau")
    parser.add_argument("--domaine", "-d", help="Domaine specifique")

    args = parser.parse_args()
    niveau = args.niveau.upper()

    data = load_competences(niveau)
    if not data:
        print(json.dumps({"error": f"Niveau {niveau} non trouve"}))
        return

    themes = data.get("competences_by_theme", {})

    if args.domaine:
        # Domaine specifique
        domaine = args.domaine.upper()
        if domaine not in themes:
            print(json.dumps({"error": f"Domaine {domaine} non trouve"}))
            return

        sous_domaines = themes[domaine]
        output = {
            "niveau": niveau,
            "domaine": domaine,
            "sous_domaines": {}
        }

        total = 0
        for sd, comps in sous_domaines.items():
            output["sous_domaines"][sd] = {
                "count": len(comps),
                "intitules": [c.get("intitule") for c in comps[:5]]  # Max 5
            }
            total += len(comps)

        output["total"] = total

    else:
        # Resume de tous les domaines
        output = {
            "niveau": niveau,
            "domaines": {},
            "total": data.get("meta", {}).get("total_competences", 0)
        }

        for domaine, sous_domaines in themes.items():
            count = sum(len(comps) for comps in sous_domaines.values())
            output["domaines"][domaine] = {
                "count": count,
                "sous_domaines": list(sous_domaines.keys())
            }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
