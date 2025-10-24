#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour une compilation rapide avec LuaLaTeX (profil Reims).
Contient la logique complète de compilation sans dépendance au serveur MCP.
"""

import sys
import json
import argparse
import subprocess
import re
from pathlib import Path
from typing import Tuple, Dict, Any


def run_lualatex(
    file_path: Path,
    pass_number: int = 1
) -> Tuple[bool, str, str]:
    """
    Exécute une passe de compilation LuaLaTeX.

    Args:
        file_path: Chemin du fichier .tex
        pass_number: Numéro de la passe

    Returns:
        (success, stdout, stderr)
    """
    # Configuration LuaLaTeX recommandée Reims
    args = ["-synctex=1", "-interaction=nonstopmode", "-file-line-error", "-shell-escape"]

    cmd = ["lualatex"] + args + [str(file_path.name)]
    cwd = file_path.parent

    try:
        print(f"⚙️  Passe {pass_number}: {' '.join(cmd)}", file=sys.stderr)
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=120
        )

        success = result.returncode == 0

        # Logique de tolérance : vérifier si le PDF est généré malgré les erreurs
        if not success:
            pdf_file = file_path.with_suffix('.pdf')
            if pdf_file.exists():
                print(f"ℹ️  PDF généré malgré code retour {result.returncode}, continuation...", file=sys.stderr)
                success = True  # Tolérance

        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return False, "", "Timeout après 120 secondes"
    except FileNotFoundError:
        return False, "", "lualatex non trouvé - vérifiez votre installation LaTeX"
    except Exception as e:
        return False, "", str(e)


def parse_latex_log_simple(log_file_path: Path) -> Dict[str, Any]:
    """
    Analyse rapide d'un fichier .log LaTeX.
    Retourne les principales erreurs.
    """
    if not log_file_path.exists():
        return {"errors": [], "warnings": []}

    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
    except Exception:
        return {"errors": [], "warnings": []}

    errors = []

    # Pattern pour les erreurs LaTeX
    error_pattern = r'! (.+?)\n.*?l\.(\d+)'
    error_matches = re.finditer(error_pattern, log_content, re.MULTILINE | re.DOTALL)

    for match in error_matches:
        error_msg = match.group(1).strip()
        line_number = match.group(2)
        errors.append({
            "message": error_msg,
            "line": int(line_number)
        })

    return {"errors": errors[:5]}  # Limiter à 5 erreurs principales


def clean_aux_files(file_path: Path) -> int:
    """
    Nettoie les fichiers auxiliaires après compilation.

    Returns:
        Nombre de fichiers supprimés
    """
    aux_extensions = [".aux", ".log", ".toc", ".lof", ".lot", ".out", ".bbl", ".blg", ".synctex.gz"]
    cleaned_count = 0

    base_path = file_path.with_suffix('')

    for ext in aux_extensions:
        aux_file = Path(str(base_path) + ext)
        if aux_file.exists():
            try:
                aux_file.unlink()
                cleaned_count += 1
            except Exception:
                pass

    return cleaned_count


def main():
    parser = argparse.ArgumentParser(
        description="Compilation rapide avec LuaLaTeX (profil Reims recommandé)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python quick_compile.py --file "mon_cours.tex"
  python quick_compile.py --file "devoir.tex" --passes 2
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier .tex à compiler"
    )

    parser.add_argument(
        "--passes",
        type=int,
        default=1,
        help="Nombre de passes de compilation (défaut: 1)"
    )

    args = parser.parse_args()

    # Vérifier le fichier
    tex_file = Path(args.file)
    if not tex_file.exists():
        print(f"❌ Fichier non trouvé: {args.file}", file=sys.stderr)
        sys.exit(1)

    print(f"⚡ Compilation rapide (LuaLaTeX): {args.file}", file=sys.stderr)
    print(f"   Nombre de passes: {args.passes}", file=sys.stderr)

    # Compiler
    overall_success = True
    for i in range(args.passes):
        success, stdout, stderr = run_lualatex(tex_file, i + 1)

        if not success:
            overall_success = False
            print(f"❌ Échec à la passe {i + 1}", file=sys.stderr)

            # Analyser le log
            log_file = tex_file.with_suffix('.log')
            analysis = parse_latex_log_simple(log_file)

            if analysis["errors"]:
                print(f"\n📋 Erreurs principales:", file=sys.stderr)
                for error in analysis["errors"][:3]:
                    print(f"   Ligne {error['line']}: {error['message']}", file=sys.stderr)

            break

    # Vérifier le PDF
    pdf_file = tex_file.with_suffix('.pdf')
    pdf_generated = pdf_file.exists()

    if overall_success and pdf_generated:
        print(f"\n✅ Compilation réussie", file=sys.stderr)
        print(f"📄 PDF: {pdf_file}", file=sys.stderr)

        # Nettoyer les fichiers auxiliaires
        cleaned_count = clean_aux_files(tex_file)
        if cleaned_count > 0:
            print(f"🧹 {cleaned_count} fichier(s) auxiliaire(s) nettoyé(s)", file=sys.stderr)

        # Sortie JSON pour l'agent
        print(json.dumps({
            "status": "success",
            "message": "Compilation réussie",
            "pdf_generated": True,
            "pdf_path": str(pdf_file)
        }))
        sys.exit(0)
    else:
        print(f"\n❌ Compilation échouée", file=sys.stderr)

        # Sortie JSON pour l'agent
        print(json.dumps({
            "status": "error",
            "message": "Compilation échouée",
            "pdf_generated": pdf_generated
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
