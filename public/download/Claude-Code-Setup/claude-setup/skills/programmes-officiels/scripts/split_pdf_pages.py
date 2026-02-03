#!/usr/bin/env python3
"""
Script de scission des PDFs de programmes officiels en pages individuelles.

Usage:
    python split_pdf_pages.py                    # Traite tous les PDFs
    python split_pdf_pages.py 2GT.pdf            # Traite un PDF spécifique
    python split_pdf_pages.py --list             # Liste les PDFs disponibles
    python split_pdf_pages.py --status           # Affiche le statut des scissions
"""

import sys
import json
import io
from pathlib import Path
from datetime import datetime

# Forcer l'encodage UTF-8 pour la sortie console (Windows)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Import des bibliothèques PDF
from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
PDF_DIR = SKILL_DIR / "pdf"
DATA_DIR = SKILL_DIR / "data"
PAGES_DIR = DATA_DIR / "pages"  # Dossier racine pour les pages


def ensure_directories():
    """Crée les dossiers nécessaires."""
    DATA_DIR.mkdir(exist_ok=True)
    PAGES_DIR.mkdir(exist_ok=True)


def get_pdf_list() -> list[Path]:
    """Retourne la liste des PDFs disponibles."""
    return sorted(PDF_DIR.glob("*.pdf"))


def get_safe_folder_name(pdf_name: str) -> str:
    """Génère un nom de dossier sûr à partir du nom du PDF."""
    # Enlève l'extension et remplace les caractères spéciaux
    name = pdf_name.replace(".pdf", "")
    name = name.replace(" ", "_")
    name = "".join(c if c.isalnum() or c in "_-" else "_" for c in name)
    return name


def split_single_pdf(pdf_path: Path, force: bool = False) -> dict:
    """
    Scinde un PDF en pages individuelles.

    Retourne un dictionnaire avec les métadonnées de la scission.
    """
    folder_name = get_safe_folder_name(pdf_path.name)
    output_dir = PAGES_DIR / folder_name

    # Vérifier si déjà fait
    index_file = output_dir / "index.json"
    if index_file.exists() and not force:
        print(f"  [SKIP] {pdf_path.name} déjà traité (utilisez --force pour retraiter)")
        with open(index_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    print(f"\n📄 Traitement de {pdf_path.name}...")

    # Créer le dossier de sortie
    output_dir.mkdir(exist_ok=True)

    # Ouvrir le PDF avec PyPDF2 pour la scission
    reader = PdfReader(str(pdf_path))
    total_pages = len(reader.pages)
    print(f"   -> {total_pages} pages détectées")

    # Préparer les métadonnées
    result = {
        "source_pdf": pdf_path.name,
        "folder_name": folder_name,
        "total_pages": total_pages,
        "extraction_date": datetime.now().isoformat(),
        "pages": []
    }

    # Extraire chaque page
    for page_num in range(total_pages):
        page_index = page_num + 1  # Numérotation 1-based
        page_filename = f"page_{page_index:03d}.pdf"
        page_path = output_dir / page_filename

        # Créer un PDF pour cette page uniquement
        writer = PdfWriter()
        writer.add_page(reader.pages[page_num])

        with open(page_path, 'wb') as output_file:
            writer.write(output_file)

        # Extraire le texte de la page pour l'index
        page_text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                if page_num < len(pdf.pages):
                    page_text = pdf.pages[page_num].extract_text() or ""
        except Exception as e:
            page_text = f"[Erreur extraction: {e}]"

        # Résumé court du contenu (premiers 500 caractères)
        text_preview = page_text[:500].replace("\n", " ").strip()
        if len(page_text) > 500:
            text_preview += "..."

        # Détecter les sections/thèmes potentiels
        detected_themes = detect_themes(page_text)

        page_info = {
            "page_number": page_index,
            "filename": page_filename,
            "text_length": len(page_text),
            "preview": text_preview,
            "detected_themes": detected_themes,
            "status": "pending"  # Pour le traitement par agent
        }

        result["pages"].append(page_info)

        # Sauvegarder aussi le texte brut
        txt_filename = f"page_{page_index:03d}.txt"
        txt_path = output_dir / txt_filename
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(page_text)

        print(f"   ✓ Page {page_index}/{total_pages}", end="\r")

    print(f"   ✓ {total_pages} pages extraites            ")

    # Sauvegarder l'index
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"   ✓ Index sauvegardé: {index_file.name}")

    return result


def detect_themes(text: str) -> list[str]:
    """
    Détecte les thèmes mathématiques présents dans le texte.
    Retourne une liste de thèmes identifiés.
    """
    themes_keywords = {
        "nombres": ["nombre", "entier", "décimal", "fraction", "rationnel", "réel", "calcul", "opération"],
        "algèbre": ["algèbre", "expression", "équation", "inéquation", "fonction", "variable", "polynôme", "factorisation"],
        "géométrie": ["géométrie", "figure", "triangle", "cercle", "droite", "angle", "vecteur", "coordonnée", "repère"],
        "analyse": ["limite", "dérivée", "primitive", "intégrale", "continuité", "suite", "convergence", "exponentielle", "logarithme"],
        "probabilités": ["probabilité", "événement", "aléatoire", "variable aléatoire", "espérance", "variance", "loi"],
        "statistiques": ["statistique", "moyenne", "médiane", "écart-type", "effectif", "fréquence", "diagramme"],
        "algorithmique": ["algorithme", "programme", "python", "boucle", "condition", "fonction", "instruction"],
        "trigonométrie": ["trigonométrie", "cosinus", "sinus", "tangente", "radian", "cercle trigonométrique"],
        "grandeurs": ["grandeur", "mesure", "unité", "conversion", "proportionnalité", "pourcentage", "vitesse"],
        "logique": ["logique", "démonstration", "raisonnement", "implication", "équivalence", "réciproque", "contraposée"]
    }

    text_lower = text.lower()
    detected = []

    for theme, keywords in themes_keywords.items():
        if any(kw in text_lower for kw in keywords):
            detected.append(theme)

    return detected


def process_all_pdfs(force: bool = False) -> dict:
    """Traite tous les PDFs disponibles."""
    ensure_directories()

    pdf_files = get_pdf_list()
    print(f"📚 {len(pdf_files)} PDFs trouvés dans {PDF_DIR}\n")

    results = {
        "processed_date": datetime.now().isoformat(),
        "total_pdfs": len(pdf_files),
        "pdfs": []
    }

    for pdf_path in pdf_files:
        result = split_single_pdf(pdf_path, force=force)
        results["pdfs"].append({
            "name": pdf_path.name,
            "folder": result.get("folder_name", ""),
            "pages": result.get("total_pages", 0)
        })

    # Sauvegarder le résumé global
    summary_file = DATA_DIR / "split_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Résumé global sauvegardé: {summary_file}")
    return results


def show_status():
    """Affiche le statut des scissions."""
    print("📊 Statut des scissions PDF\n")

    pdf_files = get_pdf_list()

    for pdf_path in pdf_files:
        folder_name = get_safe_folder_name(pdf_path.name)
        output_dir = PAGES_DIR / folder_name
        index_file = output_dir / "index.json"

        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            pages_done = len([p for p in data.get("pages", []) if p.get("status") == "processed"])
            total = data.get("total_pages", 0)
            status = "✅" if pages_done == total else f"⏳ {pages_done}/{total}"
        else:
            status = "❌ Non traité"

        print(f"  {pdf_path.name:40} {status}")


def list_pdfs():
    """Liste les PDFs disponibles."""
    print("📚 PDFs disponibles:\n")
    for pdf_path in get_pdf_list():
        size = pdf_path.stat().st_size / 1024  # KB
        print(f"  • {pdf_path.name:40} ({size:.1f} KB)")


def main():
    """Point d'entrée principal."""
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    if "--list" in args:
        list_pdfs()
        return

    if "--status" in args:
        show_status()
        return

    force = "--force" in args
    if force:
        args.remove("--force")

    ensure_directories()

    if args:
        # Traiter un PDF spécifique
        pdf_name = args[0]
        pdf_path = PDF_DIR / pdf_name

        if not pdf_path.exists():
            print(f"❌ PDF non trouvé: {pdf_path}")
            print("\nPDFs disponibles:")
            list_pdfs()
            return

        split_single_pdf(pdf_path, force=force)
    else:
        # Traiter tous les PDFs
        results = process_all_pdfs(force=force)

        print("\n" + "="*50)
        print("📊 RÉSUMÉ")
        print("="*50)
        total_pages = sum(p["pages"] for p in results["pdfs"])
        print(f"  • PDFs traités: {results['total_pdfs']}")
        print(f"  • Pages totales: {total_pages}")
        print(f"  • Dossier de sortie: {PAGES_DIR}")


if __name__ == "__main__":
    main()
