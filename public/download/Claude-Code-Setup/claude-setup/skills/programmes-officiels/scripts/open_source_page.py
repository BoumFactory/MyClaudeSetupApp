#!/usr/bin/env python3
"""
Script pour ouvrir la page source PDF d'une competence.

Usage:
    python open_source_page.py --code 5G40
    python open_source_page.py --code 5G40 --viewer vscode
    python open_source_page.py --code 5G40 --viewer edge
    python open_source_page.py --code 5G40 --viewer chrome
    python open_source_page.py --list-viewers
"""

import json
import argparse
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional, Dict

# Chemins
BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config.json"
NORMALIZED_DIR = BASE_DIR / "data" / "normalized"
PAGES_DIR = BASE_DIR / "data" / "pages"
PDF_DIR = BASE_DIR / "pdf"

# Mapping PDF source -> dossier de pages
PDF_TO_FOLDER = {
    "14-Maths-5e-attendus-eduscol_1114744.pdf": "14-Maths-5e-attendus-eduscol_1114744",
    "16-Maths-4e-attendus-eduscol_1114746.pdf": "16-Maths-4e-attendus-eduscol_1114746",
    "18-Maths-3e-attendus-eduscol_1114748.pdf": "18-Maths-3e-attendus-eduscol_1114748",
    "cycle3_v2.pdf": "cycle3_v2",
    "2GT.pdf": "2GT",
    "2STHR.pdf": "2STHR",
    "1GT.pdf": "1GT",
    "1ere_techno.pdf": "1ere_techno",
    "Mathematiques_integrees_EnsSci_1reG.pdf": "Mathematiques_integrees_EnsSci_1reG",
    "premiere_ens_sci.pdf": "premiere_ens_sci",
    "terminale_spe.pdf": "terminale_spe",
    "TG_comp.pdf": "TG_comp",
    "TG_expertes.pdf": "TG_expertes",
    "TG_spe.pdf": "TG_spe",
    "Tle_techno.pdf": "Tle_techno",
    "spe265_annexe_1159134.pdf": "spe265_annexe_1159134",
}


def load_config() -> Dict:
    """Charge la configuration du visualiseur."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "viewer": {
            "default": "auto",
            "preferences": ["vscode", "edge", "chrome"],
            "commands": {
                "vscode": "code",
                "edge": "start msedge",
                "chrome": "start chrome",
                "default_pdf": "start"
            }
        }
    }


def save_config(config: Dict):
    """Sauvegarde la configuration."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def detect_available_viewer() -> str:
    """Detecte le meilleur visualiseur disponible."""
    config = load_config()
    preferences = config.get("viewer", {}).get("preferences", ["vscode", "edge", "chrome"])

    for viewer in preferences:
        if viewer == "vscode":
            if shutil.which("code"):
                return "vscode"
        elif viewer == "edge":
            # Edge est generalement disponible sur Windows
            edge_path = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
            if edge_path.exists() or shutil.which("msedge"):
                return "edge"
        elif viewer == "chrome":
            chrome_paths = [
                Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
                Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
            ]
            if any(p.exists() for p in chrome_paths) or shutil.which("chrome"):
                return "chrome"

    return "default_pdf"


def find_competence_source(code: str) -> Optional[Dict]:
    """Trouve la source d'une competence par son code."""
    all_file = NORMALIZED_DIR / "all_normalized.json"
    if not all_file.exists():
        print(f"Erreur: Fichier {all_file} non trouve")
        return None

    with open(all_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    code_upper = code.upper()
    for comp in data.get("all_competences", []):
        if comp.get("code", "").upper() == code_upper:
            return comp
        if comp.get("old_code", "").upper() == code_upper:
            return comp

    return None


def get_page_pdf_path(pdf_name: str, page_num: int) -> Optional[Path]:
    """Retourne le chemin vers la page PDF extraite."""
    folder_name = PDF_TO_FOLDER.get(pdf_name)

    # Si pas de mapping, essayer de trouver le dossier par le nom du PDF
    if not folder_name:
        pdf_stem = Path(pdf_name).stem
        for folder in PAGES_DIR.iterdir():
            if folder.is_dir() and pdf_stem in folder.name:
                folder_name = folder.name
                break

    if not folder_name:
        return None

    page_file = PAGES_DIR / folder_name / f"page_{page_num:03d}.pdf"
    if page_file.exists():
        return page_file

    return None


def open_with_viewer(file_path: Path, viewer: str):
    """Ouvre un fichier avec le visualiseur specifie."""
    file_str = str(file_path.resolve())

    try:
        if viewer == "vscode":
            # VS Code peut ouvrir les PDFs avec une extension
            subprocess.run(["code", file_str], shell=True)
            print(f"Ouvert dans VS Code: {file_path.name}")
        elif viewer == "edge":
            subprocess.run(f'start msedge "{file_str}"', shell=True)
            print(f"Ouvert dans Edge: {file_path.name}")
        elif viewer == "chrome":
            subprocess.run(f'start chrome "{file_str}"', shell=True)
            print(f"Ouvert dans Chrome: {file_path.name}")
        else:
            # Utiliser l'application par defaut du systeme
            subprocess.run(f'start "" "{file_str}"', shell=True)
            print(f"Ouvert avec l'application par defaut: {file_path.name}")
    except Exception as e:
        print(f"Erreur lors de l'ouverture: {e}")
        # Fallback vers l'application par defaut
        subprocess.run(f'start "" "{file_str}"', shell=True)


def open_folder(folder_path: Path):
    """Ouvre le dossier dans l'explorateur de fichiers."""
    folder_str = str(folder_path.resolve())
    try:
        subprocess.run(f'explorer "{folder_str}"', shell=True)
        print(f"Dossier ouvert: {folder_path.name}")
    except Exception as e:
        print(f"Erreur lors de l'ouverture du dossier: {e}")


def list_viewers():
    """Liste les visualiseurs disponibles et leur statut."""
    print("\nVISUALISEURS DISPONIBLES")
    print("-" * 50)

    viewers = {
        "vscode": "VS Code (avec extension PDF)",
        "edge": "Microsoft Edge",
        "chrome": "Google Chrome",
        "default_pdf": "Application PDF par defaut"
    }

    for key, name in viewers.items():
        available = False
        if key == "vscode":
            available = shutil.which("code") is not None
        elif key == "edge":
            available = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe").exists()
        elif key == "chrome":
            available = Path("C:/Program Files/Google/Chrome/Application/chrome.exe").exists()
        else:
            available = True

        status = "OK" if available else "Non trouve"
        print(f"  {key:<15} {name:<30} [{status}]")

    config = load_config()
    default = config.get("viewer", {}).get("default", "auto")
    print(f"\nVisualiseur par defaut: {default}")
    if default == "auto":
        detected = detect_available_viewer()
        print(f"Detection automatique: {detected}")


def set_default_viewer(viewer: str):
    """Definit le visualiseur par defaut."""
    config = load_config()
    if "viewer" not in config:
        config["viewer"] = {}
    config["viewer"]["default"] = viewer
    save_config(config)
    print(f"Visualiseur par defaut defini: {viewer}")


def main():
    parser = argparse.ArgumentParser(
        description="Ouvrir la page source PDF d'une competence",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  --code 5G40                   Ouvrir la source de la competence 5G40
  --code 5G40 --viewer edge     Ouvrir avec Edge
  --list-viewers                Lister les visualiseurs disponibles
  --set-default vscode          Definir VS Code comme visualiseur par defaut
        """
    )

    parser.add_argument("--code", "-c", help="Code de la competence")
    parser.add_argument("--viewer", "-v",
                        choices=["auto", "vscode", "edge", "chrome", "default_pdf"],
                        default="auto",
                        help="Visualiseur a utiliser")
    parser.add_argument("--list-viewers", action="store_true",
                        help="Lister les visualiseurs disponibles")
    parser.add_argument("--set-default",
                        choices=["auto", "vscode", "edge", "chrome", "default_pdf"],
                        help="Definir le visualiseur par defaut")
    parser.add_argument("--info", action="store_true",
                        help="Afficher les infos de source sans ouvrir")
    parser.add_argument("--folder", "-f", action="store_true",
                        help="Ouvrir le dossier contenant la page (pour naviguer)")

    args = parser.parse_args()

    # Mode liste visualiseurs
    if args.list_viewers:
        list_viewers()
        return

    # Mode set default
    if args.set_default:
        set_default_viewer(args.set_default)
        return

    # Validation
    if not args.code:
        print("Erreur: --code requis")
        print("Utilisez --help pour l'aide")
        sys.exit(1)

    # Trouver la competence
    comp = find_competence_source(args.code)
    if not comp:
        print(f"Competence non trouvee: {args.code}")
        sys.exit(1)

    # Extraire la source
    source = comp.get("source", {})
    if not source:
        print(f"Pas de source disponible pour: {args.code}")
        print("Cette competence n'a pas d'information de page source.")
        sys.exit(1)

    pdf_name = source.get("pdf", "")
    page_num = source.get("page", 0)

    print(f"\nCompetence: [{comp.get('code')}] {comp.get('intitule', 'N/A')}")
    print(f"Source: {pdf_name} - Page {page_num}")

    if args.info:
        print(f"\nDomaine: {comp.get('domaine', 'N/A')}")
        print(f"Sous-domaine: {comp.get('sous_domaine', 'N/A')}")
        print(f"Type: {comp.get('type', 'N/A')}")
        return

    # Trouver le fichier PDF de la page
    page_path = get_page_pdf_path(pdf_name, page_num)

    if not page_path:
        print(f"\nPage PDF non trouvee: {pdf_name} page {page_num}")
        print("Verifiez que les pages ont ete extraites avec split_pdf_pages.py")
        sys.exit(1)

    print(f"Fichier: {page_path}")

    # Mode dossier : ouvrir le dossier contenant la page
    if args.folder:
        open_folder(page_path.parent)
        return

    # Determiner le visualiseur
    viewer = args.viewer
    if viewer == "auto":
        config = load_config()
        default = config.get("viewer", {}).get("default", "auto")
        if default == "auto":
            viewer = detect_available_viewer()
        else:
            viewer = default

    # Ouvrir le fichier
    open_with_viewer(page_path, viewer)


if __name__ == "__main__":
    main()
