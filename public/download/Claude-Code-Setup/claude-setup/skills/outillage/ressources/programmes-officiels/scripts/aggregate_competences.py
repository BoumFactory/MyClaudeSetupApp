#!/usr/bin/env python3
"""
Script d'agregation des competences extraites des programmes officiels.
- Agregation par niveau
- Detection des doublons (fingerprint)
- Reorganisation par theme (domaine > sous_domaine)
- Generation de rapport de doublons
"""

import json
import os
import sys
from pathlib import Path
from collections import defaultdict
from datetime import datetime

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
EXTRACTIONS_DIR = DATA_DIR / "extractions"
OUTPUT_DIR = DATA_DIR / "aggregated"

# Mapping des dossiers vers les niveaux
NIVEAU_MAPPING = {
    # Collège
    "cycle3_v2": "C3",
    "14-Maths-5e-attendus-eduscol_1114744": "5E",
    "16-Maths-4e-attendus-eduscol_1114746": "4E",
    "18-Maths-3e-attendus-eduscol_1114748": "3E",
    # Lycée - Seconde
    "2GT": "2GT",
    "2STHR": "2STHR",
    # Lycée - Première
    "1GT": "1SPE",
    "1ere_techno": "1TECHNO",
    "Mathematiques_integrees_EnsSci_1reG": "1ENS_SCI",
    "premiere_ens_sci": "1ENS_SCI_V2",
    # Lycée - Terminale
    "terminale_spe": "TSPE",
    "TG_comp": "TCOMP",
    "TG_expertes": "TEXP",
    "TG_spe": "TSPE_V2",
    "Tle_techno": "TTECHNO",
    # Autres
    "spe265_annexe_1159134": "SPE_ANNEXE"
}

def load_json_files(extraction_dir: Path) -> list:
    """Charge tous les fichiers JSON de competences d'un dossier."""
    competences = []
    json_files = sorted(extraction_dir.glob("*_competences.json"))

    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if "competences" in data:
                    for comp in data["competences"]:
                        comp["_source_file"] = json_file.name
                        competences.append(comp)
        except Exception as e:
            print(f"Erreur lecture {json_file}: {e}")

    return competences

def detect_duplicates(competences: list) -> dict:
    """
    Detecte les doublons par fingerprint.
    Retourne un dict avec les fingerprints en doublon et leurs occurrences.
    """
    fingerprint_map = defaultdict(list)

    for i, comp in enumerate(competences):
        fp = comp.get("fingerprint", "")
        if fp:
            fingerprint_map[fp].append({
                "index": i,
                "code": comp.get("code", "N/A"),
                "intitule": comp.get("intitule", "N/A"),
                "source_file": comp.get("_source_file", "N/A"),
                "page": comp.get("source", {}).get("page", "N/A")
            })

    # Filtrer pour garder seulement les doublons
    duplicates = {fp: occurrences for fp, occurrences in fingerprint_map.items()
                  if len(occurrences) > 1}

    return duplicates

def organize_by_theme(competences: list) -> dict:
    """
    Reorganise les competences par domaine > sous_domaine.
    """
    organized = defaultdict(lambda: defaultdict(list))

    for comp in competences:
        domaine = comp.get("domaine", "AUTRE")
        sous_domaine = comp.get("sous_domaine", "General")

        # Nettoyer la competence pour l'export
        clean_comp = {k: v for k, v in comp.items() if not k.startswith("_")}
        organized[domaine][sous_domaine].append(clean_comp)

    # Convertir en dict normal pour JSON
    return {domaine: dict(sous_domaines) for domaine, sous_domaines in organized.items()}

def generate_duplicate_report(duplicates: dict, niveau: str, output_file: Path):
    """Genere un rapport detaille des doublons pour intervention manuelle."""
    report = {
        "meta": {
            "niveau": niveau,
            "generated": datetime.now().isoformat(),
            "total_duplicates_groups": len(duplicates),
            "total_duplicate_entries": sum(len(v) for v in duplicates.values())
        },
        "action_required": len(duplicates) > 0,
        "duplicates": []
    }

    for fingerprint, occurrences in duplicates.items():
        report["duplicates"].append({
            "fingerprint": fingerprint,
            "count": len(occurrences),
            "occurrences": occurrences,
            "suggestion": "Garder la premiere occurrence, supprimer les autres"
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    return report

def aggregate_niveau(niveau_code: str, extraction_folder: str) -> dict:
    """
    Agregation complete pour un niveau.
    Retourne les statistiques.
    """
    extraction_dir = EXTRACTIONS_DIR / extraction_folder

    if not extraction_dir.exists():
        print(f"Dossier non trouve: {extraction_dir}")
        return None

    print(f"\n{'='*60}")
    print(f"Agregation {niveau_code} ({extraction_folder})")
    print(f"{'='*60}")

    # Charger toutes les competences
    competences = load_json_files(extraction_dir)
    print(f"Competences chargees: {len(competences)}")

    # Detecter les doublons
    duplicates = detect_duplicates(competences)
    print(f"Groupes de doublons detectes: {len(duplicates)}")

    # Creer dossier de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Generer rapport de doublons
    if duplicates:
        dup_report_file = OUTPUT_DIR / f"{niveau_code}_doublons.json"
        report = generate_duplicate_report(duplicates, niveau_code, dup_report_file)
        print(f"Rapport doublons: {dup_report_file}")

    # Reorganiser par theme
    by_theme = organize_by_theme(competences)

    # Compter par domaine
    stats_domaine = {}
    for domaine, sous_domaines in by_theme.items():
        count = sum(len(comps) for comps in sous_domaines.values())
        stats_domaine[domaine] = count

    print(f"Repartition par domaine: {stats_domaine}")

    # Generer le fichier agrege par theme
    output_theme = {
        "meta": {
            "niveau": niveau_code,
            "source_folder": extraction_folder,
            "generated": datetime.now().isoformat(),
            "total_competences": len(competences),
            "duplicates_count": len(duplicates),
            "organization": "domaine > sous_domaine > competences"
        },
        "stats": {
            "by_domaine": stats_domaine,
            "by_type": defaultdict(int)
        },
        "competences_by_theme": by_theme
    }

    # Stats par type
    for comp in competences:
        output_theme["stats"]["by_type"][comp.get("type", "autre")] += 1
    output_theme["stats"]["by_type"] = dict(output_theme["stats"]["by_type"])

    # Sauvegarder
    output_file = OUTPUT_DIR / f"{niveau_code}_competences.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_theme, f, ensure_ascii=False, indent=2)

    print(f"Fichier agrege: {output_file}")

    # Generer aussi une liste plate pour recherche rapide
    flat_output = {
        "meta": {
            "niveau": niveau_code,
            "generated": datetime.now().isoformat(),
            "total": len(competences)
        },
        "competences": [
            {k: v for k, v in comp.items() if not k.startswith("_")}
            for comp in competences
        ]
    }

    flat_file = OUTPUT_DIR / f"{niveau_code}_competences_flat.json"
    with open(flat_file, "w", encoding="utf-8") as f:
        json.dump(flat_output, f, ensure_ascii=False, indent=2)

    print(f"Fichier plat: {flat_file}")

    return {
        "niveau": niveau_code,
        "total": len(competences),
        "duplicates": len(duplicates),
        "by_domaine": stats_domaine
    }

def main():
    """Point d'entree principal."""
    print("="*60)
    print("AGREGATION DES COMPETENCES - PROGRAMMES OFFICIELS")
    print("="*60)

    all_stats = []

    for folder, niveau in NIVEAU_MAPPING.items():
        stats = aggregate_niveau(niveau, folder)
        if stats:
            all_stats.append(stats)

    # Resume global
    print("\n" + "="*60)
    print("RESUME GLOBAL")
    print("="*60)

    total_competences = sum(s["total"] for s in all_stats)
    total_duplicates = sum(s["duplicates"] for s in all_stats)

    print(f"Total competences: {total_competences}")
    print(f"Total groupes doublons: {total_duplicates}")

    for stats in all_stats:
        print(f"\n{stats['niveau']}: {stats['total']} competences, {stats['duplicates']} doublons")
        for dom, count in stats["by_domaine"].items():
            print(f"  - {dom}: {count}")

    # Sauvegarder le resume
    summary = {
        "generated": datetime.now().isoformat(),
        "total_competences": total_competences,
        "total_duplicate_groups": total_duplicates,
        "by_niveau": all_stats
    }

    summary_file = OUTPUT_DIR / "summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nResume sauvegarde: {summary_file}")

    if total_duplicates > 0:
        print(f"\n⚠️  ATTENTION: {total_duplicates} groupes de doublons detectes!")
        print("Consultez les fichiers *_doublons.json pour details.")

if __name__ == "__main__":
    main()
