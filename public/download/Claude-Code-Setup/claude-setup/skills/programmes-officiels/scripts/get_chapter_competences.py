#!/usr/bin/env python3
"""
Recupere toutes les competences d'un chapitre/theme.
Retourne un JSON compact pour l'agent.

Usage:
    python get_chapter_competences.py --niveau 5E --theme "fractions"
    python get_chapter_competences.py --niveau 4E --theme "pythagore"
    python get_chapter_competences.py --niveau 3E --theme "fonction"
"""

import json
import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data" / "aggregated"

# Mapping des themes courants vers les mots-cles de recherche
THEMES_MAPPING = {
    # Nombres
    "fractions": ["fraction", "numerateur", "denominateur", "simplif"],
    "relatifs": ["relatif", "oppose", "negatif", "positif"],
    "puissances": ["puissance", "exposant", "carre", "cube"],
    "racines": ["racine", "carree"],
    "decimaux": ["decimal", "virgule"],
    "pourcentages": ["pourcentage", "proportion"],

    # Algebre
    "calcul_litteral": ["litteral", "developp", "factor", "reduire", "expression"],
    "equations": ["equation", "inconnue", "resoudre", "solution"],
    "inequations": ["inequation", "intervalle"],
    "fonctions": ["fonction", "image", "antecedent", "courbe", "affine", "lineaire"],
    "systemes": ["systeme", "deux equations"],

    # Geometrie
    "pythagore": ["pythagore", "triangle rectangle", "hypotenuse"],
    "thales": ["thales", "proportionnel", "parallele"],
    "triangles": ["triangle", "somme angles", "inegalite"],
    "parallelogrammes": ["parallelogramme", "rectangle", "losange", "carre"],
    "cercles": ["cercle", "rayon", "diametre", "corde", "arc"],
    "angles": ["angle", "alterne", "correspondant", "oppose"],
    "symetries": ["symetrie", "axiale", "centrale"],
    "transformations": ["translation", "rotation", "homothetie"],
    "trigonometrie": ["cosinus", "sinus", "tangente", "trigonometr"],
    "aires": ["aire", "surface"],
    "volumes": ["volume", "patron", "solide", "pave", "cylindre", "cone", "pyramide", "sphere"],
    "reperage": ["repere", "coordonnee", "abscisse", "ordonnee"],

    # Stats/Probas
    "statistiques": ["moyenne", "mediane", "etendue", "effectif", "frequence"],
    "probabilites": ["probabilite", "hasard", "aleatoire", "experience"],

    # Algo
    "algorithmique": ["algorithme", "scratch", "python", "boucle", "variable", "instruction"],
    "programmation": ["programme", "script", "code", "fonction python"],
}

def load_flat_competences(niveau: str) -> list:
    file_path = DATA_DIR / f"{niveau}_competences_flat.json"
    if not file_path.exists():
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f).get("competences", [])

def search_theme(competences: list, theme: str) -> list:
    """Recherche les competences liees a un theme."""
    # Recuperer les mots-cles associes au theme
    theme_lower = theme.lower()
    keywords = THEMES_MAPPING.get(theme_lower, [theme_lower])

    results = []
    for comp in competences:
        # Champs a rechercher
        searchable = " ".join([
            comp.get("intitule", ""),
            comp.get("description_detaillee", ""),
            comp.get("formulation_bo", ""),
            comp.get("sous_domaine", ""),
            " ".join(comp.get("connaissances_associees", []))
        ]).lower()

        # Verifier si un des mots-cles est present
        for kw in keywords:
            if kw in searchable:
                results.append(comp)
                break

    return results

def format_output(competences: list, niveau: str, theme: str) -> dict:
    """Formate la sortie pour l'agent."""
    # Grouper par sous-domaine
    by_sous_domaine = {}
    for comp in competences:
        sd = comp.get("sous_domaine", "General")
        if sd not in by_sous_domaine:
            by_sous_domaine[sd] = []
        by_sous_domaine[sd].append({
            "code": comp.get("code"),
            "intitule": comp.get("intitule"),
            "type": comp.get("type", "capacite")
        })

    return {
        "niveau": niveau,
        "theme": theme,
        "total": len(competences),
        "par_sous_domaine": by_sous_domaine,
        "liste_complete": [
            {
                "code": c.get("code"),
                "intitule": c.get("intitule"),
                "description": c.get("description_detaillee"),
                "formulation_bo": c.get("formulation_bo")
            }
            for c in competences
        ]
    }

def main():
    parser = argparse.ArgumentParser(description="Competences par chapitre/theme")
    parser.add_argument("--niveau", "-n", required=True, help="Niveau (C3, 5E, 4E, 3E)")
    parser.add_argument("--theme", "-t", required=True, help="Theme/chapitre a rechercher")
    parser.add_argument("--list-themes", action="store_true", help="Lister les themes disponibles")

    args = parser.parse_args()

    if args.list_themes:
        print("Themes disponibles:")
        for theme in sorted(THEMES_MAPPING.keys()):
            print(f"  - {theme}")
        return

    competences = load_flat_competences(args.niveau.upper())
    if not competences:
        print(json.dumps({"error": f"Niveau {args.niveau} non trouve"}))
        sys.exit(1)

    results = search_theme(competences, args.theme)
    output = format_output(results, args.niveau.upper(), args.theme)

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
