#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour obtenir les informations d'un modèle de document.
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
    from document_creator_server import get_template_info
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Obtient les informations détaillées d'un modèle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python get_template_info.py --template "Cours"
  python get_template_info.py --template "Devoir"
        """
    )

    parser.add_argument(
        "--template",
        required=True,
        help="Nom du modèle (sans .tex)"
    )

    args = parser.parse_args()

    print(f"🔍 Analyse du modèle: {args.template}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await get_template_info(template_name=args.template)
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        fields = result.get("fields", {})
        required_fields = result.get("required_fields", [])
        print(f"\n✅ Modèle: {result.get('template', '')}", file=sys.stderr)
        print(f"\n📋 Champs à remplir ({len(fields)}):\n", file=sys.stderr)

        for field_name, field_info in fields.items():
            field_type = field_info.get("type", "text")
            default = field_info.get("default", "")
            required = field_info.get("required", field_name in required_fields)

            marker = "OBLIGATOIRE" if required else "optionnel"
            print(f"   • {field_name} ({field_type}, {marker})", file=sys.stderr)

            if field_type == "choice":
                options = field_info.get("options", [])
                print(f"     Options: {', '.join(options)}", file=sys.stderr)

            if default:
                print(f"     Défaut: {default}", file=sys.stderr)

            if "user_default" in field_info:
                print(f"     Préférence utilisateur: {field_info['user_default']}", file=sys.stderr)

            print("", file=sys.stderr)

        if required_fields:
            print(f"⚠️  Champs obligatoires (aucun défaut exploitable): {', '.join(required_fields)}\n", file=sys.stderr)

        example_fields_file = result.get("example_fields_file")
        if example_fields_file:
            print("📄 Exemple de fields-file complet (à copier avec Write, compléter les", file=sys.stderr)
            print("   <A_COMPLETER:...>, puis lancer create_document.py --fields-file <chemin>) :\n", file=sys.stderr)
            for line in json.dumps(example_fields_file, ensure_ascii=False, indent=2).splitlines():
                print(f"   {line}", file=sys.stderr)
            print("", file=sys.stderr)

        # Options de structure
        struct_opts = result.get("structure_options", {})
        print(f"🏗️  Options de structure:", file=sys.stderr)
        print(f"   create_folder: {struct_opts.get('create_folder', True)}", file=sys.stderr)
        print(f"   create_figures_file: {struct_opts.get('create_figures_file', True)}", file=sys.stderr)

    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
