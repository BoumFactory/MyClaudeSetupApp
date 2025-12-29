#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour tester la configuration avec un document LaTeX simple.
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
    from latex_compiler_server import test_compilation
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Teste la configuration avec un document LaTeX simple",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python test_compilation.py
  python test_compilation.py --content "\\documentclass{article}..."
        """
    )

    parser.add_argument(
        "--content",
        help="Contenu LaTeX à tester (optionnel, utilise un document par défaut)"
    )

    args = parser.parse_args()

    print("🧪 Test de compilation", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = test_compilation(test_content=args.content)
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"\n✅ {result.get('message', 'Test réussi')}", file=sys.stderr)
        print(f"📄 Fichier test: {result.get('test_file', '')}", file=sys.stderr)
    else:
        print(f"\n❌ {result.get('message', 'Test échoué')}", file=sys.stderr)

        comp_result = result.get("compilation_result", {})
        if comp_result.get("message"):
            print(f"   {comp_result['message']}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
