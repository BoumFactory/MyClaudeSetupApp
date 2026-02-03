#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour récupérer les préférences utilisateur.
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
    from document_creator_server import get_user_preferences
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    print("⚙️  Récupération des préférences utilisateur", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await get_user_preferences()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        prefs = result.get("preferences", {})

        print(f"\n✅ Préférences chargées depuis: {result.get('file_path', '')}\n", file=sys.stderr)

        # Valeurs par défaut
        default_vals = prefs.get("default_values", {})
        if default_vals:
            print(f"📝 Valeurs par défaut ({len(default_vals)}):", file=sys.stderr)
            for key, val in default_vals.items():
                print(f"   {key}: {val}", file=sys.stderr)
            print("", file=sys.stderr)

        # Options favorites
        fav_opts = prefs.get("favorite_options", {})
        if fav_opts:
            print(f"⭐ Options favorites ({len(fav_opts)}):", file=sys.stderr)
            for key, val in fav_opts.items():
                print(f"   {key}: {val}", file=sys.stderr)
            print("", file=sys.stderr)

        # Options de structure
        print(f"🏗️  Options de structure:", file=sys.stderr)
        print(f"   create_folder: {prefs.get('create_folder', True)}", file=sys.stderr)
        print(f"   create_images_folder: {prefs.get('create_images_folder', False)}", file=sys.stderr)
        print(f"   create_annexes_folder: {prefs.get('create_annexes_folder', False)}", file=sys.stderr)
        print(f"   create_sections_folder: {prefs.get('create_sections_folder', False)}", file=sys.stderr)
        print(f"   create_figures_file: {prefs.get('create_figures_file', True)}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
