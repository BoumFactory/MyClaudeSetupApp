#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour ajouter une habitude utilisateur.
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
    from document_creator_server import add_user_habit
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Ajoute une habitude utilisateur (valeur par défaut ou option favorite)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python add_user_habit.py --field "niveau" --value "2nde"
  python add_user_habit.py --field "type_etablissement" --value "Lycée" --is-choice
        """
    )

    parser.add_argument(
        "--field",
        required=True,
        help="Nom du champ"
    )

    parser.add_argument(
        "--value",
        required=True,
        help="Valeur à enregistrer"
    )

    parser.add_argument(
        "--is-choice",
        action="store_true",
        default=False,
        help="True si c'est un champ à choix multiple"
    )

    args = parser.parse_args()

    print(f"⭐ Ajout d'une habitude pour le champ: {args.field}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await add_user_habit(
        field_name=args.field,
        value=args.value,
        is_choice=args.is_choice
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"✅ {result.get('message', 'Habitude enregistrée')}", file=sys.stderr)
        print(f"   Champ: {result.get('field', '')}", file=sys.stderr)
        print(f"   Valeur: {result.get('value', '')}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
