#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour analyser un fichier .log LaTeX.
Utilise le serveur MCP latex-compiler-server.
"""

import sys
import json
import argparse
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from latex_compiler_server import analyze_latex_log
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Analyse un fichier .log LaTeX pour diagnostiquer les erreurs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python analyze_latex_log.py --log "mon_cours.log"
  python analyze_latex_log.py --log "devoir.log" --tex "devoir.tex"
        """
    )

    parser.add_argument(
        "--log",
        required=True,
        help="Chemin vers le fichier .log"
    )

    parser.add_argument(
        "--tex",
        help="Chemin vers le fichier .tex correspondant (optionnel, pour contexte)"
    )

    args = parser.parse_args()

    print(f"🔍 Analyse du fichier log: {args.log}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = analyze_latex_log(
        log_file_path=args.log,
        tex_file_path=args.tex
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        analysis = result.get("analysis", {})

        total_errors = analysis.get("total_errors", 0)
        total_warnings = analysis.get("total_warnings", 0)

        print(f"\n📊 Résultats de l'analyse:", file=sys.stderr)
        print(f"   ❌ Erreurs: {total_errors}", file=sys.stderr)
        print(f"   ⚠️  Avertissements: {total_warnings}", file=sys.stderr)

        # Afficher les erreurs principales
        errors = analysis.get("errors", [])
        if errors:
            print(f"\n🔴 Erreurs détectées:\n", file=sys.stderr)
            for i, error in enumerate(errors[:5], 1):
                line = error.get("line_number", "?")
                msg = error.get("message", "")
                print(f"   {i}. Ligne {line}: {msg}", file=sys.stderr)

                if error.get("problem_line"):
                    print(f"      > {error['problem_line']}", file=sys.stderr)

                print("", file=sys.stderr)

        # Analyse générale
        analysis_text = analysis.get("analysis", "")
        if analysis_text and analysis_text != "Analyse automatique indisponible":
            print(f"💡 Analyse: {analysis_text}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
