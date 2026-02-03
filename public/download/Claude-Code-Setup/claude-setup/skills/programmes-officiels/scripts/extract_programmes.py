#!/usr/bin/env python3
"""
Script d'extraction des programmes officiels depuis les PDF du BO.
Utilise pdfplumber pour extraire le texte et la structure.
"""

import json
import pdfplumber
from pathlib import Path
from typing import Dict, List, Any

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PDF_DIR = SKILL_DIR / "pdf"
DATA_DIR = SKILL_DIR / "data"
REF_FILE = SKILL_DIR / "references_bo.json"

# S'assurer que le dossier data existe
DATA_DIR.mkdir(exist_ok=True)

def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrait tout le texte d'un PDF."""
    print(f"Extraction de {pdf_path.name}...")

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for i, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text += f"\n\n--- PAGE {i} ---\n\n{page_text}"

        print(f"  -> {len(pdf.pages)} pages extraites")
        return text


def parse_cycle3(text: str) -> Dict[str, Any]:
    """Parse le programme de cycle 3."""
    return {
        "niveau": "CYCLE3",
        "niveaux_concernes": ["CM1", "CM2", "6EME"],
        "texte_complet": text,
        "themes": [],  # À compléter après analyse manuelle
        "note": "Structure à affiner après analyse du texte complet"
    }


def parse_seconde(text: str) -> Dict[str, Any]:
    """Parse le programme de seconde."""
    return {
        "niveau": "SECONDE",
        "texte_complet": text,
        "themes": [],  # À compléter
        "note": "Structure à affiner après analyse du texte complet"
    }


def parse_terminale_spe(text: str) -> Dict[str, Any]:
    """Parse le programme de terminale spécialité."""
    return {
        "niveau": "TERMINALE_SPE",
        "texte_complet": text,
        "themes": [],  # À compléter
        "note": "Structure à affiner après analyse du texte complet"
    }


def parse_premiere_ens_sci(text: str) -> Dict[str, Any]:
    """Parse le programme d'enseignement scientifique de première."""
    return {
        "niveau": "PREMIERE_ENS_SCI",
        "texte_complet": text,
        "themes": [],  # À compléter
        "note": "Structure à affiner après analyse du texte complet"
    }


def main():
    """Fonction principale."""
    print("=== Extraction des programmes officiels ===\n")

    # Charger les références BO
    with open(REF_FILE, 'r', encoding='utf-8') as f:
        references = json.load(f)

    # Fichiers à traiter
    pdf_files = {
        "cycle3": ("cycle3_v2.pdf", parse_cycle3),
        "seconde": ("seconde.pdf", parse_seconde),
        "terminale_specialite": ("terminale_spe.pdf", parse_terminale_spe),
        "premiere_enseignement_scientifique": ("premiere_ens_sci.pdf", parse_premiere_ens_sci),
    }

    for key, (pdf_name, parser) in pdf_files.items():
        pdf_path = PDF_DIR / pdf_name

        if not pdf_path.exists():
            print(f"[WARN] {pdf_name} non trouve, ignore.")
            continue

        # Extraire le texte
        text = extract_text_from_pdf(pdf_path)

        # Parser selon le niveau
        data = parser(text)

        # Ajouter les métadonnées du BO
        if key in references["programmes_officiels"]:
            bo_info = references["programmes_officiels"][key]
            data["bo_reference"] = bo_info.get("bo_reference", "")
            data["url_bo"] = bo_info.get("url_bo", "")
            data["url_pdf"] = bo_info.get("url_pdf", "")
            data["date_publication"] = bo_info.get("date", "")

        # Sauvegarder le JSON
        output_file = DATA_DIR / f"{data['niveau'].lower()}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[OK] Sauvegarde dans {output_file.name}\n")

    # Sauvegarder aussi les textes bruts pour analyse
    print("Sauvegarde des textes bruts pour analyse manuelle...")

    for key, (pdf_name, _) in pdf_files.items():
        pdf_path = PDF_DIR / pdf_name
        if pdf_path.exists():
            text = extract_text_from_pdf(pdf_path)
            txt_file = DATA_DIR / f"{pdf_name.replace('.pdf', '_raw.txt')}"
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"  -> {txt_file.name}")

    print("\n=== Extraction terminée ===")
    print("Les fichiers JSON ont été créés dans le dossier 'data/'")
    print("Les fichiers texte bruts sont disponibles pour analyse.")


if __name__ == "__main__":
    main()
