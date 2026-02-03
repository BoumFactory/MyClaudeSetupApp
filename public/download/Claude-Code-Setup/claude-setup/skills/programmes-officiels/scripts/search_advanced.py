#!/usr/bin/env python3
"""
Recherche avancee avec filtres multiples.

Usage:
    # Recherche simple
    python search_advanced.py --query "fraction"

    # Avec filtres
    python search_advanced.py --query "calcul" --niveau 5E --domaine NOMBRES --type capacite

    # Filtres multiples
    python search_advanced.py --query "triangle" --niveau 4E,3E --domaine GEOMETRIE

    # Exclure un terme
    python search_advanced.py --query "equation" --exclude "inequation"

    # Seulement les nouveautes
    python search_advanced.py --query "fonction" --niveau 3E --only-new

    # Format compact
    python search_advanced.py --query "probabilite" --all-levels --compact
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"
NIVEAUX = ["C3", "5E", "4E", "3E"]
NIVEAUX_ORDER = {"C3": 0, "5E": 1, "4E": 2, "3E": 3}

def load_flat_competences(niveau: str) -> list:
    file_path = DATA_DIR / f"{niveau}_competences_flat.json"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f).get("competences", [])

def match_query(comp: dict, query: str, exclude: Optional[str] = None) -> bool:
    """Verifie si une competence correspond a la requete."""
    searchable = " ".join([
        comp.get("intitule", ""),
        comp.get("description_detaillee", ""),
        comp.get("formulation_bo", ""),
        comp.get("sous_domaine", ""),
        " ".join(comp.get("connaissances_associees", []))
    ]).lower()

    if query.lower() not in searchable:
        return False

    if exclude and exclude.lower() in searchable:
        return False

    return True

def filter_competences(
    competences: list,
    query: str,
    domaine: Optional[str] = None,
    type_comp: Optional[str] = None,
    exclude: Optional[str] = None
) -> list:
    """Filtre les competences selon les criteres."""
    results = []
    for comp in competences:
        # Filtre requete
        if not match_query(comp, query, exclude):
            continue

        # Filtre domaine
        if domaine and comp.get("domaine", "").upper() != domaine.upper():
            continue

        # Filtre type
        if type_comp and comp.get("type", "") != type_comp:
            continue

        results.append(comp)

    return results

def is_new_at_level(notion: str, niveau: str) -> bool:
    """Verifie si la notion est nouvelle a ce niveau."""
    current_order = NIVEAUX_ORDER.get(niveau, 0)
    lower_levels = [n for n, order in NIVEAUX_ORDER.items() if order < current_order]

    for lvl in lower_levels:
        comps = load_flat_competences(lvl)
        for comp in comps:
            searchable = " ".join([
                comp.get("intitule", ""),
                comp.get("description_detaillee", "")
            ]).lower()
            if notion.lower() in searchable:
                return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Recherche avancee avec filtres")

    # Requete
    parser.add_argument("--query", "-q", required=True, help="Terme a rechercher")

    # Filtres de niveau
    parser.add_argument("--niveau", "-n", help="Niveau(x) - separes par virgule (ex: 5E,4E)")
    parser.add_argument("--all-levels", action="store_true", help="Tous les niveaux")

    # Filtres de contenu
    parser.add_argument("--domaine", "-d", help="Filtrer par domaine")
    parser.add_argument("--type", dest="type_comp", help="Type (capacite, contenu, demonstration, algorithme)")
    parser.add_argument("--exclude", "-e", help="Exclure les resultats contenant ce terme")

    # Filtres speciaux
    parser.add_argument("--only-new", action="store_true", help="Seulement les notions nouvelles au niveau")

    # Options de sortie
    parser.add_argument("--compact", action="store_true", help="Sortie compacte")
    parser.add_argument("--limit", "-l", type=int, default=50, help="Limite (defaut: 50)")

    args = parser.parse_args()

    # Determiner les niveaux
    if args.all_levels:
        niveaux = NIVEAUX
    elif args.niveau:
        niveaux = [n.strip().upper() for n in args.niveau.split(",")]
    else:
        print(json.dumps({"error": "--niveau ou --all-levels requis"}))
        return

    # Recherche
    all_results = []
    results_by_niveau = {}

    for niveau in niveaux:
        competences = load_flat_competences(niveau)
        results = filter_competences(
            competences,
            args.query,
            args.domaine,
            args.type_comp,
            args.exclude
        )

        # Filtre nouveautes
        if args.only_new:
            results = [r for r in results if is_new_at_level(args.query, niveau)]

        for r in results:
            r["_niveau"] = niveau

        results_by_niveau[niveau] = len(results)
        all_results.extend(results)

    # Limiter
    all_results = all_results[:args.limit]

    # Construire la sortie
    output = {
        "query": args.query,
        "filtres": {
            "niveaux": niveaux,
            "domaine": args.domaine,
            "type": args.type_comp,
            "exclude": args.exclude,
            "only_new": args.only_new
        },
        "resultats_par_niveau": results_by_niveau,
        "total": len(all_results)
    }

    if args.compact:
        output["competences"] = [
            {
                "niveau": c.get("_niveau"),
                "code": c.get("code"),
                "intitule": c.get("intitule")
            }
            for c in all_results
        ]
    else:
        output["competences"] = [
            {
                "niveau": c.get("_niveau"),
                "code": c.get("code"),
                "intitule": c.get("intitule"),
                "domaine": c.get("domaine"),
                "sous_domaine": c.get("sous_domaine"),
                "type": c.get("type"),
                "description": c.get("description_detaillee")
            }
            for c in all_results
        ]

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
