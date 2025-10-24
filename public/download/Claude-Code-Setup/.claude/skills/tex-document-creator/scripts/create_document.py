#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour créer un document à partir d'un modèle.
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
    from document_creator_server import create_document
except ImportError:
    print("❌ ERREUR: Impossible d'importer document_creator_server", file=sys.stderr)
    sys.exit(1)


async def main():
    parser = argparse.ArgumentParser(
        description="Crée un document à partir d'un modèle",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples (nouveau format recommandé):
  python create_document.py --destination "./Test" --name "Mon_Cours" --template "Cours" \\
    --field "niveau=$\\mathbf{2^{\\text{nde}}}$" --field "theme=Vecteurs" \\
    --field "type_etablissement=Lycée" --field "nom_etablissement=Camille Claudel"

  python create_document.py --destination "." --name "DS_Fonctions" --template "Devoir" \\
    --field "niveau=$\\mathbf{1^{\\text{ère}}}$" --field "duree=55" --create-sections

Exemples (ancien format JSON, legacy):
  python create_document.py --destination "./Test" --name "Mon_Cours" --template "Cours" \\
    --fields '{"niveau": "2nde", "theme": "Vecteurs"}'
        """
    )

    parser.add_argument(
        "--destination",
        required=True,
        help="Chemin de destination"
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Nom du document (sans .tex)"
    )

    parser.add_argument(
        "--template",
        required=True,
        help="Nom du modèle à utiliser"
    )

    parser.add_argument(
        "--field",
        action='append',
        dest='fields_list',
        help="Champ à remplir (format: nom=valeur). Peut être répété."
    )

    parser.add_argument(
        "--fields",
        required=False,
        help="[LEGACY] Dictionnaire JSON des valeurs de champs"
    )

    parser.add_argument(
        "--no-folder",
        dest="create_folder",
        action="store_false",
        default=True,
        help="Ne pas créer de dossier pour le document"
    )

    parser.add_argument(
        "--create-images",
        dest="create_images_folder",
        action="store_true",
        default=False,
        help="Créer le dossier images"
    )

    parser.add_argument(
        "--create-annexes",
        dest="create_annexes_folder",
        action="store_true",
        default=False,
        help="Créer le dossier annexes"
    )

    parser.add_argument(
        "--create-sections",
        dest="create_sections_folder",
        action="store_true",
        default=False,
        help="Créer le dossier sections"
    )

    parser.add_argument(
        "--no-figures",
        dest="create_figures_file",
        action="store_false",
        default=True,
        help="Ne pas créer le fichier enonce_figures.tex"
    )

    parser.add_argument(
        "--claude-instructions",
        dest="include_claude_instructions",
        action="store_true",
        default=False,
        help="Inclure un fichier CLAUDE.md"
    )

    args = parser.parse_args()

    # Parser les champs - priorité au nouveau format --field
    field_values = {}

    if args.fields_list:
        # Nouveau format : --field nom=valeur
        for field_arg in args.fields_list:
            if '=' not in field_arg:
                print(f"❌ ERREUR: Format invalide pour --field: '{field_arg}'", file=sys.stderr)
                print("   Format attendu: --field nom=valeur", file=sys.stderr)
                sys.exit(1)
            key, value = field_arg.split('=', 1)
            field_values[key.strip()] = value
    elif args.fields:
        # Legacy format : --fields JSON
        try:
            field_values = json.loads(args.fields)
        except json.JSONDecodeError as e:
            print(f"❌ ERREUR: Format JSON invalide pour --fields: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("❌ ERREUR: Vous devez fournir au moins un --field ou --fields", file=sys.stderr)
        sys.exit(1)

    print(f"📝 Création du document: {args.name}", file=sys.stderr)
    print(f"   Modèle: {args.template}", file=sys.stderr)
    print(f"   Destination: {args.destination}", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = await create_document(
        destination_path=args.destination,
        document_name=args.name,
        template_name=args.template,
        field_values=field_values,
        create_folder=args.create_folder,
        create_images_folder=args.create_images_folder,
        create_annexes_folder=args.create_annexes_folder,
        create_sections_folder=args.create_sections_folder,
        create_figures_file=args.create_figures_file,
        include_claude_instructions=args.include_claude_instructions
    )

    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"\n✅ {result.get('message', 'Document créé')}", file=sys.stderr)
        print(f"\n📁 Emplacement: {result.get('path', '')}", file=sys.stderr)
        print(f"📄 Fichier principal: {result.get('main_file', '')}", file=sys.stderr)

        created_files = result.get("created_files", [])
        if created_files:
            print(f"\n📝 Fichiers créés ({len(created_files)}):", file=sys.stderr)
            for f in created_files:
                print(f"   - {f}", file=sys.stderr)

        created_folders = result.get("created_folders", [])
        if created_folders:
            print(f"\n📂 Dossiers créés ({len(created_folders)}):", file=sys.stderr)
            for d in created_folders:
                print(f"   - {d}", file=sys.stderr)

        next_steps = result.get("next_steps", [])
        if next_steps:
            print(f"\n⏭️  Prochaines étapes:", file=sys.stderr)
            for i, step in enumerate(next_steps, 1):
                print(f"   {i}. {step}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)
        if "missing_fields" in result:
            print(f"   Champs manquants: {', '.join(result['missing_fields'])}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
