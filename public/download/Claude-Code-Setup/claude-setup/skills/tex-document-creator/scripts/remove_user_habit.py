#!/usr'bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour supprimer une habitude utilisateur.
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
    from document_creator_server import remove_user_habit
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Supprime une habitude utilisateur",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python remove_user_habit.py --field "niveau"
  python remove_user_habit.py --field "type_etablissement" --type "favorite"
        """
    )

    parser.add_argument(
        "--field",
        required=True,
        help="Nom du champ"
    )

    parser.add_argument(
        "--type",
        default="auto",
        choices=["auto", "default", "favorite"],
        help="Type d'habitude à supprimer (auto détecte automatiquement)"
    )

    args = parser.parse_args()

    print(f"🗑️  Suppression de l'habitude pour: {args.field}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await remove_user_habit(
        field_name=args.field,
        habit_type=args.type
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"✅ {result.get('message', 'Habitude supprimée')}", file=sys.stderr)
        removed = result.get("removed", [])
        if removed:
            print(f"   Supprimé: {', '.join(removed)}", file=sys.stderr)
    elif result.get("status") == "warning":
        print(f"⚠️  {result.get('message', '')}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") in ["success", "warning"] else 1)


if __name__ == "__main__":
    asyncio.run(main())
