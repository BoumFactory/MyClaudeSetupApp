#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour définir le profil de compilation par défaut.
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
    from latex_compiler_server import set_default_profile
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Définit le profil de compilation par défaut",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python set_default_profile.py --profile "lualatex_reims_favorite"
  python set_default_profile.py --profile "standard"
        """
    )

    parser.add_argument(
        "--profile",
        required=True,
        help="Nom du profil à utiliser par défaut"
    )

    args = parser.parse_args()

    print(f"🎯 Définition du profil par défaut: {args.profile}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = set_default_profile(profile_name=args.profile)
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"✅ {result.get('message', 'Profil par défaut défini')}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

        if "available_profiles" in result:
            print(f"\n📋 Profils disponibles:", file=sys.stderr)
            for prof in result["available_profiles"]:
                print(f"   - {prof}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
