#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour mettre à jour la configuration d'un compilateur.
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
    from latex_compiler_server import update_compiler_config
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Met à jour la configuration d'un compilateur",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python update_compiler_config.py --compiler "lualatex" --enabled
  python update_compiler_config.py --compiler "pdflatex" --path "/usr/bin/pdflatex"
  python update_compiler_config.py --compiler "lualatex" --args '["-synctex=1", "-shell-escape"]'
        """
    )

    parser.add_argument(
        "--compiler",
        required=True,
        help="Nom du compilateur (pdflatex, lualatex, etc.)"
    )

    parser.add_argument(
        "--path",
        help="Chemin vers l'exécutable"
    )

    parser.add_argument(
        "--args",
        help="Arguments en JSON string"
    )

    parser.add_argument(
        "--enabled",
        dest="enabled",
        action="store_true",
        help="Activer le compilateur"
    )

    parser.add_argument(
        "--disabled",
        dest="enabled",
        action="store_false",
        help="Désactiver le compilateur"
    )

    parser.set_defaults(enabled=None)

    args = parser.parse_args()

    print(f"⚙️  Configuration du compilateur: {args.compiler}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = update_compiler_config(
        compiler_name=args.compiler,
        path=args.path,
        args=args.args,
        enabled=args.enabled
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"✅ {result.get('message', 'Configuration mise à jour')}", file=sys.stderr)

        config = result.get("config", {})
        print(f"\n📋 Nouvelle configuration:", file=sys.stderr)
        print(f"   Chemin: {config.get('path', '')}", file=sys.stderr)
        print(f"   Arguments: {config.get('args', [])}", file=sys.stderr)
        print(f"   Activé: {'Oui' if config.get('enabled') else 'Non'}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
