#!/usr/bin/env python3
"""
Script de renormalisation des codes de competences.

Format: [niveau][filiere][theme][index]-[palier]

Exemples:
- 6N1 : 6eme, Nombres, competence 1
- 1SY3 : 1ere Spe, Analyse, competence 3
- 0EA2-1 : Terminale Expert, Algebre, competence 2, palier 1
"""

import json
import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
AGGREGATED_DIR = DATA_DIR / "aggregated"
OUTPUT_DIR = DATA_DIR / "normalized"

# Mapping niveau -> code numerique
NIVEAU_TO_CODE = {
    # College
    "C3": "6",      # Cycle 3 assimile a 6eme
    "5E": "5",
    "4E": "4",
    "3E": "3",
    # Lycee - Seconde
    "2GT": "2G",
    "2STHR": "2H",
    # Lycee - Premiere
    "1SPE": "1S",
    "1TECHNO": "1T",
    "1ENS_SCI": "1E",
    "1ENS_SCI_V2": "1E",  # Fusion avec 1ENS_SCI
    # Lycee - Terminale
    "TSPE": "0S",
    "TSPE_V2": "0S",     # Fusion avec TSPE
    "TCOMP": "0C",
    "TEXP": "0E",
    "TTECHNO": "0T",
    # Autres
    "SPE_ANNEXE": "0X",  # Annexe
}

# Mapping domaine -> lettre theme
# Regle: premiere lettre, si doublon prendre la premiere lettre differente
DOMAINE_TO_LETTER = {
    "NOMBRES": "N",
    "ALGEBRE": "A",
    "ANALYSE": "Y",          # analYse (A pris)
    "ALGORITHMIQUE": "L",    # aLgorithmique (A pris)
    "GEOMETRIE": "G",
    "GRANDEURS": "R",        # gRandeurs (G pris)
    "STATISTIQUES": "S",
    "PROBABILITES": "P",
    "TRIGONOMETRIE": "T",
    "LOGIQUE": "O",          # lOgique (L pris)
    "AUTRE": "X",
}

def load_aggregated_file(filepath: Path) -> dict:
    """Charge un fichier JSON agrege."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_new_code(niveau: str, domaine: str, index: int, palier: int = None) -> str:
    """
    Genere le nouveau code normalise.

    Format: [niveau][theme][index]-[palier]
    Exemples: 6N1, 1SY3, 0EA2-1
    """
    niveau_code = NIVEAU_TO_CODE.get(niveau, "X")
    theme_letter = DOMAINE_TO_LETTER.get(domaine, "X")

    code = f"{niveau_code}{theme_letter}{index}"

    if palier is not None:
        code += f"-{palier}"

    return code

def renormalize_niveau(niveau_code: str, input_file: Path) -> dict:
    """
    Renormalise toutes les competences d'un niveau.
    Retourne les statistiques et les competences renormalisees.
    """
    print(f"\n{'='*60}")
    print(f"Renormalisation {niveau_code}")
    print(f"{'='*60}")

    data = load_aggregated_file(input_file)

    # Compteurs par domaine pour generer les index
    domain_counters = defaultdict(int)

    # Mapping ancien code -> nouveau code
    code_mapping = {}

    # Competences renormalisees
    normalized_competences = []

    # Parcourir les competences par theme
    if "competences_by_theme" in data:
        for domaine, sous_domaines in data["competences_by_theme"].items():
            for sous_domaine, competences in sous_domaines.items():
                for comp in competences:
                    # Incrementer le compteur pour ce domaine
                    domain_counters[domaine] += 1
                    index = domain_counters[domaine]

                    # Ancien code
                    old_code = comp.get("code", "N/A")

                    # Nouveau code
                    new_code = generate_new_code(niveau_code, domaine, index)

                    # Enregistrer le mapping
                    code_mapping[old_code] = new_code

                    # Creer la competence renormalisee
                    normalized_comp = {
                        "code": new_code,
                        "old_code": old_code,
                        "intitule": comp.get("intitule", ""),
                        "fingerprint": comp.get("fingerprint", ""),
                        "niveau": niveau_code,
                        "niveau_code": NIVEAU_TO_CODE.get(niveau_code, "X"),
                        "domaine": domaine,
                        "domaine_code": DOMAINE_TO_LETTER.get(domaine, "X"),
                        "sous_domaine": sous_domaine,
                        "type": comp.get("type", ""),
                        "description_detaillee": comp.get("description_detaillee", ""),
                        "formulation_bo": comp.get("formulation_bo", ""),
                        "connaissances_associees": comp.get("connaissances_associees", []),
                        "source": comp.get("source", {})
                    }

                    normalized_competences.append(normalized_comp)

    # Afficher les stats
    print(f"Competences traitees: {len(normalized_competences)}")
    print(f"Repartition par domaine:")
    for domaine, count in sorted(domain_counters.items()):
        letter = DOMAINE_TO_LETTER.get(domaine, "X")
        print(f"  {domaine} ({letter}): {count}")

    return {
        "niveau": niveau_code,
        "niveau_code": NIVEAU_TO_CODE.get(niveau_code, "X"),
        "total": len(normalized_competences),
        "by_domaine": dict(domain_counters),
        "code_mapping": code_mapping,
        "competences": normalized_competences
    }

def main():
    """Point d'entree principal."""
    print("="*60)
    print("RENORMALISATION DES CODES DE COMPETENCES")
    print("="*60)
    print(f"\nFormat: [niveau][filiere][theme][index]-[palier]")
    print(f"Exemple: 6N1 = 6eme, Nombres, competence 1")
    print(f"         1SY3 = 1ere Spe, Analyse, competence 3")

    # Creer le dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    all_stats = []
    all_competences = []
    global_code_mapping = {}

    # Traiter chaque fichier agrege
    for niveau, code in NIVEAU_TO_CODE.items():
        flat_file = AGGREGATED_DIR / f"{niveau}_competences.json"

        if not flat_file.exists():
            print(f"\nFichier non trouve: {flat_file.name}")
            continue

        result = renormalize_niveau(niveau, flat_file)

        all_stats.append({
            "niveau": niveau,
            "niveau_code": result["niveau_code"],
            "total": result["total"],
            "by_domaine": result["by_domaine"]
        })

        all_competences.extend(result["competences"])
        global_code_mapping.update(result["code_mapping"])

        # Sauvegarder le fichier normalise pour ce niveau
        output_file = OUTPUT_DIR / f"{niveau}_normalized.json"
        output_data = {
            "meta": {
                "niveau": niveau,
                "niveau_code": result["niveau_code"],
                "generated": datetime.now().isoformat(),
                "total": result["total"],
                "format": "[niveau][filiere][theme][index]-[palier]"
            },
            "stats": result["by_domaine"],
            "competences": result["competences"]
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"Fichier normalise: {output_file.name}")

    # Resume global
    print("\n" + "="*60)
    print("RESUME GLOBAL")
    print("="*60)

    total_competences = sum(s["total"] for s in all_stats)
    print(f"\nTotal competences renormalisees: {total_competences}")

    # Tableau recapitulatif des codes
    print("\n" + "-"*40)
    print("MAPPING DES CODES")
    print("-"*40)
    print(f"{'Niveau':<15} {'Code':<6}")
    print("-"*40)
    for niveau, code in sorted(NIVEAU_TO_CODE.items(), key=lambda x: x[1]):
        print(f"{niveau:<15} {code:<6}")

    print("\n" + "-"*40)
    print(f"{'Domaine':<20} {'Lettre':<6}")
    print("-"*40)
    for domaine, letter in sorted(DOMAINE_TO_LETTER.items()):
        print(f"{domaine:<20} {letter:<6}")

    # Sauvegarder le fichier global
    global_output = {
        "meta": {
            "generated": datetime.now().isoformat(),
            "total": total_competences,
            "format": "[niveau][filiere][theme][index]-[palier]",
            "niveau_mapping": NIVEAU_TO_CODE,
            "domaine_mapping": DOMAINE_TO_LETTER
        },
        "by_niveau": all_stats,
        "code_mapping": global_code_mapping,
        "all_competences": all_competences
    }

    global_file = OUTPUT_DIR / "all_normalized.json"
    with open(global_file, "w", encoding="utf-8") as f:
        json.dump(global_output, f, ensure_ascii=False, indent=2)

    print(f"\nFichier global: {global_file}")

    # Sauvegarder juste le mapping pour reference
    mapping_file = OUTPUT_DIR / "code_mapping.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump({
            "meta": {
                "generated": datetime.now().isoformat(),
                "description": "Mapping ancien code -> nouveau code"
            },
            "niveau_mapping": NIVEAU_TO_CODE,
            "domaine_mapping": DOMAINE_TO_LETTER,
            "codes": global_code_mapping
        }, f, ensure_ascii=False, indent=2)

    print(f"Fichier mapping: {mapping_file}")

if __name__ == "__main__":
    main()
