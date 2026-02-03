#!/usr/bin/env python3
"""
Script d'orchestration de l'extraction des competences depuis les pages PDF.

Usage:
    python orchestrate_extraction.py                    # Affiche le statut
    python orchestrate_extraction.py --list-pending     # Liste les pages a traiter
    python orchestrate_extraction.py --process [N]      # Traite N pages (defaut: toutes)
    python orchestrate_extraction.py --merge            # Fusionne les extractions en fichiers par niveau
"""

import sys
import io
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Forcer l'encodage UTF-8 pour la sortie console (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
PAGES_DIR = DATA_DIR / "pages"
EXTRACTIONS_DIR = DATA_DIR / "extractions"
OUTPUT_DIR = Path("C:/Users/Utilisateur/Documents/Professionnel/1. Reims 2025 - 2026/.claude/datas/competences")

# Mapping PDF -> Niveau
PDF_TO_NIVEAU = {
    "1GT": "1SPE",
    "1ere_techno": "1TC",
    "2GT": "2GT",
    "2STHR": "2STHR",
    "cycle3_v2": "CYCLE3",
    "Mathematiques_integrees_EnsSci_1reG": "1ENS_SCI",
    "premiere_ens_sci": "1ENS_SCI",
    "spe265_annexe_1159134": "CYCLE4",  # A verifier
    "terminale_spe": "TSPE",
    "TG_comp": "TCOMP",
    "TG_expertes": "TEXPERTES",
    "TG_spe": "TSPE",
    "Tle_techno": "TTC"
}


def ensure_directories():
    """Cree les dossiers necessaires."""
    EXTRACTIONS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_all_pages() -> list[dict]:
    """Retourne la liste de toutes les pages avec leur statut."""
    pages = []

    for pdf_folder in PAGES_DIR.iterdir():
        if not pdf_folder.is_dir():
            continue

        index_file = pdf_folder / "index.json"
        if not index_file.exists():
            continue

        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)

        niveau = PDF_TO_NIVEAU.get(pdf_folder.name, "UNKNOWN")

        for page in index.get("pages", []):
            # Verifier si l'extraction existe
            extraction_folder = EXTRACTIONS_DIR / pdf_folder.name
            extraction_file = extraction_folder / f"page_{page['page_number']:03d}_competences.json"

            pages.append({
                "pdf_folder": pdf_folder.name,
                "pdf_source": index.get("source_pdf", ""),
                "niveau": niveau,
                "page_number": page["page_number"],
                "text_file": pdf_folder / f"page_{page['page_number']:03d}.txt",
                "extraction_file": extraction_file,
                "status": "extracted" if extraction_file.exists() else "pending",
                "themes": page.get("detected_themes", []),
                "text_length": page.get("text_length", 0)
            })

    return pages


def get_pending_pages() -> list[dict]:
    """Retourne les pages non encore traitees."""
    return [p for p in get_all_pages() if p["status"] == "pending"]


def get_extraction_stats() -> dict:
    """Retourne les statistiques d'extraction."""
    pages = get_all_pages()

    stats = {
        "total_pages": len(pages),
        "extracted": len([p for p in pages if p["status"] == "extracted"]),
        "pending": len([p for p in pages if p["status"] == "pending"]),
        "by_niveau": {},
        "by_pdf": {}
    }

    for page in pages:
        niveau = page["niveau"]
        pdf = page["pdf_folder"]

        if niveau not in stats["by_niveau"]:
            stats["by_niveau"][niveau] = {"total": 0, "extracted": 0, "pending": 0}
        stats["by_niveau"][niveau]["total"] += 1
        stats["by_niveau"][niveau][page["status"]] += 1

        if pdf not in stats["by_pdf"]:
            stats["by_pdf"][pdf] = {"total": 0, "extracted": 0, "pending": 0, "niveau": niveau}
        stats["by_pdf"][pdf]["total"] += 1
        stats["by_pdf"][pdf][page["status"]] += 1

    return stats


def print_status():
    """Affiche le statut global de l'extraction."""
    stats = get_extraction_stats()

    print("=" * 60)
    print("STATUT DE L'EXTRACTION DES COMPETENCES")
    print("=" * 60)
    print(f"\nTotal pages   : {stats['total_pages']}")
    print(f"Extraites     : {stats['extracted']} ({100*stats['extracted']/stats['total_pages']:.1f}%)")
    print(f"En attente    : {stats['pending']}")

    print("\n" + "-" * 60)
    print("PAR NIVEAU:")
    print("-" * 60)
    for niveau, data in sorted(stats["by_niveau"].items()):
        pct = 100 * data["extracted"] / data["total"] if data["total"] > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {niveau:15} [{bar}] {data['extracted']:3}/{data['total']:3} ({pct:5.1f}%)")

    print("\n" + "-" * 60)
    print("PAR PDF:")
    print("-" * 60)
    for pdf, data in sorted(stats["by_pdf"].items()):
        pct = 100 * data["extracted"] / data["total"] if data["total"] > 0 else 0
        status = "✅" if data["extracted"] == data["total"] else "⏳"
        print(f"  {status} {pdf:35} {data['extracted']:2}/{data['total']:2} pages")


def list_pending():
    """Liste les pages en attente de traitement."""
    pending = get_pending_pages()

    print(f"\n📋 {len(pending)} pages en attente de traitement:\n")

    current_pdf = None
    for page in sorted(pending, key=lambda p: (p["pdf_folder"], p["page_number"])):
        if page["pdf_folder"] != current_pdf:
            current_pdf = page["pdf_folder"]
            print(f"\n  [{page['niveau']}] {page['pdf_source']}:")

        themes = ", ".join(page["themes"][:3]) if page["themes"] else "?"
        print(f"    Page {page['page_number']:2} ({page['text_length']:4} car.) - {themes}")


def generate_extraction_prompt(page: dict) -> str:
    """Genere le prompt pour l'extraction d'une page."""
    return f"""Extrais les competences de cette page du programme officiel.

**Source:** {page['pdf_source']} - Page {page['page_number']}
**Niveau:** {page['niveau']}
**Themes detectes:** {', '.join(page['themes'])}

**Fichier texte:** {page['text_file']}

Lis le fichier texte et extrait TOUTES les competences atomiques.
Sauvegarde le resultat dans: {page['extraction_file']}

Utilise le format defini dans le schema SCHEMA_COMPETENCES_BO.json.
Sois exhaustif et atomise bien chaque competence."""


def merge_extractions():
    """Fusionne toutes les extractions en fichiers par niveau."""
    print("\n🔄 Fusion des extractions par niveau...\n")

    ensure_directories()

    # Collecter toutes les competences par niveau
    competences_by_niveau = {}

    for extraction_folder in EXTRACTIONS_DIR.iterdir():
        if not extraction_folder.is_dir():
            continue

        niveau = PDF_TO_NIVEAU.get(extraction_folder.name, "UNKNOWN")
        if niveau not in competences_by_niveau:
            competences_by_niveau[niveau] = []

        for extraction_file in extraction_folder.glob("*_competences.json"):
            try:
                with open(extraction_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for comp in data.get("competences", []):
                    comp["_source_file"] = extraction_file.name
                    competences_by_niveau[niveau].append(comp)

            except Exception as e:
                print(f"  ⚠️ Erreur lecture {extraction_file.name}: {e}")

    # Sauvegarder par niveau
    for niveau, competences in competences_by_niveau.items():
        if not competences:
            continue

        # Deduplication par code
        seen_codes = set()
        unique_competences = []
        for comp in competences:
            code = comp.get("code", "")
            if code and code not in seen_codes:
                seen_codes.add(code)
                unique_competences.append(comp)

        output_file = OUTPUT_DIR / f"{niveau.lower()}_bo.json"

        output_data = {
            "metadata": {
                "niveau": niveau,
                "source": "Programmes officiels (BO)",
                "extraction_date": datetime.now().isoformat(),
                "total_competences": len(unique_competences)
            },
            "competences": unique_competences
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"  ✅ {niveau}: {len(unique_competences)} competences -> {output_file.name}")

    print("\n✅ Fusion terminee!")


def main():
    """Point d'entree principal."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    ensure_directories()

    if "--list-pending" in args:
        list_pending()
        return

    if "--merge" in args:
        merge_extractions()
        return

    if "--process" in args:
        idx = args.index("--process")
        n = int(args[idx + 1]) if idx + 1 < len(args) and args[idx + 1].isdigit() else None

        pending = get_pending_pages()
        if n:
            pending = pending[:n]

        print(f"\n🚀 Traitement de {len(pending)} pages...")
        print("\nPour chaque page, utilisez l'agent bo-competence-extractor avec ce prompt:\n")

        for i, page in enumerate(pending, 1):
            print(f"\n--- Page {i}/{len(pending)} ---")
            print(generate_extraction_prompt(page))

        return

    # Par defaut: afficher le statut
    print_status()


if __name__ == "__main__":
    main()
