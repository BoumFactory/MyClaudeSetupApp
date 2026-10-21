#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour mettre à jour les préférences utilisateur.
Utilise le serveur MCP document-creator-server.
"""

import sys
import json
import asyncio
import argparse
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from document_creator_server import update_user_preferences
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Met à jour les préférences utilisateur",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python update_user_preferences.py --default-values '{"niveau": "2nde", "nom_etablissement": "Exemple"}'
  python update_user_preferences.py --favorite-options '{"type_etablissement": "Lycée"}'
  python update_user_preferences.py --structure-options '{"create_folder": true, "create_sections_folder": true}'
        """
    )

    parser.add_argument(
        "--default-values",
        help="Dictionnaire JSON des valeurs par défaut"
    )

    parser.add_argument(
        "--favorite-options",
        help="Dictionnaire JSON des options favorites"
    )

    parser.add_argument(
        "--structure-options",
        help="Dictionnaire JSON des options de structure"
    )

    args = parser.parse_args()

    if not any([args.default_values, args.favorite_options, args.structure_options]):
        print("❌ ERREUR: Au moins une option doit être fournie", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    print("⚙️  Mise à jour des préférences utilisateur", file=sys.stderr)

    # Parser les arguments JSON
    default_values = None
    favorite_options = None
    structure_options = None

    try:
        if args.default_values:
            default_values = json.loads(args.default_values)
        if args.favorite_options:
            favorite_options = json.loads(args.favorite_options)
        if args.structure_options:
            structure_options = json.loads(args.structure_options)
    except json.JSONDecodeError as e:
        print(f"❌ ERREUR: Format JSON invalide - {e}", file=sys.stderr)
        sys.exit(1)

    # Appeler la fonction du serveur MCP
    result_json = await update_user_preferences(
        default_values=default_values,
        favorite_options=favorite_options,
        structure_options=structure_options
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"\n✅ {result.get('message', 'Préférences mises à jour')}", file=sys.stderr)

        prefs = result.get("preferences", {})
        print(f"\n📝 Nouvelles préférences:", file=sys.stderr)
        print(f"   Valeurs par défaut: {len(prefs.get('default_values', {}))} champ(s)", file=sys.stderr)
        print(f"   Options favorites: {len(prefs.get('favorite_options', {}))} champ(s)", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
