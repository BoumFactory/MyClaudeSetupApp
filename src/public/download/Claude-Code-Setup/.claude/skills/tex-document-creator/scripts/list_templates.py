#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour lister les modèles de documents disponibles.
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
    from document_creator_server import list_templates
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    print("📚 Liste des modèles de documents disponibles", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await list_templates()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        templates = result.get("templates", [])
        print(f"\n✅ {result.get('total', 0)} modèle(s) trouvé(s) dans: {result.get('path', '')}\n", file=sys.stderr)

        for template in templates:
            print(f"   📄 {template['name']}", file=sys.stderr)
            print(f"      Fichier: {template['file']}", file=sys.stderr)
            print(f"      Taille: {template['size']} octets\n", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
