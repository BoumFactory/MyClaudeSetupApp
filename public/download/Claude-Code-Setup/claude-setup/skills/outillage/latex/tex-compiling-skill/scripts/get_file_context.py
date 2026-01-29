#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour récupérer le contexte autour d'une ligne dans un fichier.
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
    from latex_compiler_server import get_file_context
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Récupère le contexte autour d'une ligne spécifique",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python get_file_context.py --file "mon_cours.tex" --line 42
  python get_file_context.py --file "devoir.tex" --line 100 --context 10
        """
    )

    parser.add_argument(
        "--file",
        required=True,
        help="Chemin du fichier"
    )

    parser.add_argument(
        "--line",
        type=int,
        required=True,
        help="Numéro de ligne (1-indexé)"
    )

    parser.add_argument(
        "--context",
        type=int,
        default=5,
        help="Nombre de lignes de contexte avant et après (défaut: 5)"
    )

    args = parser.parse_args()

    print(f"📄 Contexte du fichier: {args.file}", file=sys.stderr)
    print(f"   Ligne: {args.line} (±{args.context} lignes)", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = get_file_context(
        file_path=args.file,
        line_number=args.line,
        context_lines=args.context
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        context = result.get("context", {})
        context_lines = context.get("context_lines", [])

        print(f"\n📝 Contexte (lignes {context.get('context_start', 0)}-{context.get('context_end', 0)}):\n", file=sys.stderr)

        for line_info in context_lines:
            line_num = line_info.get("line_number", 0)
            content = line_info.get("content", "")
            is_error = line_info.get("is_error_line", False)

            marker = ">>>" if is_error else "   "
            print(f"{marker} {line_num:4d} | {content}", file=sys.stderr)

    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
