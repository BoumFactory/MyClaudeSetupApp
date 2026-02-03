#!/usr/bin/env python3
"""
Script de detection des pages non extraites.

Compare les pages texte disponibles avec les fichiers d'extraction de competences.
Identifie les pages qui n'ont pas encore ete traitees par l'agent d'extraction.

Usage:
    python check_missing_extractions.py              # Verifie tous les PDFs
    python check_missing_extractions.py 2GT          # Verifie un PDF specifique
    python check_missing_extractions.py --verbose    # Affiche le contenu resume des pages manquantes
"""

import sys
import io
import json
from pathlib import Path

# Forcer UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
PAGES_DIR = DATA_DIR / "pages"
EXTRACTIONS_DIR = DATA_DIR / "extractions"

# Mots-cles importants a detecter dans les pages manquantes
IMPORTANT_KEYWORDS = [
    "vecteur", "coordonnee", "repere", "milieu", "distance",
    "fonction", "derivee", "variation", "extremum", "courbe",
    "probabilite", "esperance", "variance", "loi",
    "suite", "arithmetique", "geometrique",
    "equation", "inequation", "polynome",
    "theoreme", "demonstration", "propriete"
]


def get_page_numbers(folder: Path, extension: str) -> set:
    """Extrait les numeros de page des fichiers d'un dossier."""
    numbers = set()
    for f in folder.glob(f"page_*.{extension}"):
        # Extraire le numero: page_001.txt -> 1
        try:
            num = int(f.stem.split("_")[1])
            numbers.add(num)
        except (IndexError, ValueError):
            pass
    return numbers


def get_extraction_numbers(folder: Path) -> set:
    """Extrait les numeros des pages extraites."""
    numbers = set()
    for f in folder.glob("page_*_competences.json"):
        try:
            # page_001_competences.json -> 1
            num = int(f.stem.split("_")[1])
            numbers.add(num)
        except (IndexError, ValueError):
            pass
    return numbers


def analyze_page_content(txt_path: Path) -> dict:
    """Analyse le contenu d'une page pour identifier les themes."""
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
    except:
        return {"keywords": [], "preview": "[Erreur lecture]"}

    found_keywords = []
    for kw in IMPORTANT_KEYWORDS:
        if kw in content:
            found_keywords.append(kw)

    # Extrait les 200 premiers caracteres
    preview = content[:200].replace('\n', ' ').strip()

    return {
        "keywords": found_keywords,
        "preview": preview
    }


def check_pdf_folder(pdf_name: str, verbose: bool = False) -> dict:
    """Verifie un dossier PDF pour les pages manquantes."""
    pages_folder = PAGES_DIR / pdf_name
    extractions_folder = EXTRACTIONS_DIR / pdf_name

    result = {
        "pdf": pdf_name,
        "pages_available": 0,
        "pages_extracted": 0,
        "missing_pages": [],
        "missing_with_keywords": []
    }

    if not pages_folder.exists():
        result["error"] = "Dossier pages introuvable"
        return result

    # Pages texte disponibles
    available = get_page_numbers(pages_folder, "txt")
    result["pages_available"] = len(available)

    # Pages extraites
    if extractions_folder.exists():
        extracted = get_extraction_numbers(extractions_folder)
    else:
        extracted = set()
    result["pages_extracted"] = len(extracted)

    # Pages manquantes
    missing = sorted(available - extracted)
    result["missing_pages"] = missing

    # Analyser les pages manquantes
    for page_num in missing:
        txt_path = pages_folder / f"page_{page_num:03d}.txt"
        if txt_path.exists():
            analysis = analyze_page_content(txt_path)
            if analysis["keywords"]:
                result["missing_with_keywords"].append({
                    "page": page_num,
                    "keywords": analysis["keywords"],
                    "preview": analysis["preview"] if verbose else None
                })

    return result


def print_report(results: list, verbose: bool = False):
    """Affiche le rapport des pages manquantes."""
    print("=" * 70)
    print("RAPPORT DES PAGES NON EXTRAITES")
    print("=" * 70)

    total_missing = 0
    total_critical = 0

    for result in results:
        if "error" in result:
            print(f"\n{result['pdf']}: {result['error']}")
            continue

        missing_count = len(result["missing_pages"])
        critical_count = len(result["missing_with_keywords"])
        total_missing += missing_count
        total_critical += critical_count

        if missing_count == 0:
            status = "OK"
        elif critical_count > 0:
            status = "CRITICAL"
        else:
            status = "WARN"

        print(f"\n{result['pdf']:50} [{status}]")
        print(f"  Pages disponibles: {result['pages_available']}")
        print(f"  Pages extraites:   {result['pages_extracted']}")
        print(f"  Pages manquantes:  {missing_count}")

        if result["missing_pages"]:
            pages_str = ", ".join(str(p) for p in result["missing_pages"])
            print(f"  → Numeros: {pages_str}")

        if result["missing_with_keywords"]:
            print(f"  ⚠️  Pages avec mots-cles importants: {critical_count}")
            for item in result["missing_with_keywords"]:
                kw_str = ", ".join(item["keywords"][:5])
                print(f"     Page {item['page']}: {kw_str}")
                if verbose and item.get("preview"):
                    print(f"        → {item['preview'][:80]}...")

    print("\n" + "=" * 70)
    print("RESUME")
    print("=" * 70)
    print(f"Total pages manquantes: {total_missing}")
    print(f"Pages critiques (mots-cles importants): {total_critical}")

    if total_critical > 0:
        print("\n⚠️  ACTION REQUISE: Relancer l'agent bo-competence-extractor")
        print("   sur les pages critiques listees ci-dessus.")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    verbose = "--verbose" in args or "-v" in args
    if verbose:
        args = [a for a in args if a not in ("--verbose", "-v")]

    # Determiner quels PDFs verifier
    if args:
        pdf_names = [args[0]]
    else:
        pdf_names = [f.name for f in PAGES_DIR.iterdir() if f.is_dir()]

    results = []
    for pdf_name in sorted(pdf_names):
        result = check_pdf_folder(pdf_name, verbose)
        results.append(result)

    print_report(results, verbose)

    # Sauvegarder le rapport
    report_path = DATA_DIR / "missing_extractions_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nRapport sauvegarde: {report_path}")


if __name__ == "__main__":
    main()
