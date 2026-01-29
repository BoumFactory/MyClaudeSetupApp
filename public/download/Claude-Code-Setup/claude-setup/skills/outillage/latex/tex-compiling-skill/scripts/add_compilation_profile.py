#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour ajouter un profil de compilation personnalisé.
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
    from latex_compiler_server import add_compilation_profile
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Ajoute un nouveau profil de compilation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python add_compilation_profile.py --name "mon_profil" --description "Mon profil perso" --steps '[{"compiler": "lualatex", "count": 2}]'
  python add_compilation_profile.py --name "biblio" --description "Avec bibliographie" --steps '[{"compiler": "pdflatex", "count": 1}, {"compiler": "bibtex", "count": 1}, {"compiler": "pdflatex", "count": 2}]'
        """
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Nom du profil"
    )

    parser.add_argument(
        "--description",
        required=True,
        help="Description du profil"
    )

    parser.add_argument(
        "--steps",
        required=True,
        help="JSON string des étapes de compilation"
    )

    args = parser.parse_args()

    print(f"➕ Ajout du profil: {args.name}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = add_compilation_profile(
        name=args.name,
        description=args.description,
        steps=args.steps
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"✅ {result.get('message', 'Profil ajouté')}", file=sys.stderr)

        profile = result.get("profile", {})
        steps = profile.get("steps", [])
        print(f"\n📋 Configuration:", file=sys.stderr)
        for step in steps:
            print(f"   - {step.get('compiler', '')} × {step.get('count', 1)}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
