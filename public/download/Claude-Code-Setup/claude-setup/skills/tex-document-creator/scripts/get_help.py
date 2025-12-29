#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour obtenir l'aide du serveur document-creator.
Utilise le serveur MCP document-creator-server.
"""

import sys
import json
import asyncio
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from document_creator_server import get_help
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    print("📖 Aide du Document Creator Server", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await get_help()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        help_text = result.get("help", "")
        available_functions = result.get("available_functions", [])

        print("\n" + "="*60, file=sys.stderr)
        print(help_text, file=sys.stderr)
        print("="*60, file=sys.stderr)

        print(f"\n📋 Fonctions disponibles ({len(available_functions)}):", file=sys.stderr)
        for func in available_functions:
            print(f"   • {func}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
