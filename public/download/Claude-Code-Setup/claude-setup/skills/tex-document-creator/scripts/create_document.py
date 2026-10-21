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
Exemple RECOMMANDE (--fields-file) :
  1. Ecrire le fichier de champs avec l'outil Write (jamais via Bash/heredoc,
     Git Bash altere les antislashs des valeurs LaTeX comme $\\mathbf{...}$) :

     fields.json :
     {
       "niveau": "$\\mathbf{2^{\\text{nde}}}$",
       "theme": "Vecteurs",
       "type_etablissement": "Lycee",
       "nom_etablissement": "Lycée Exemple"
     }

  2. Lancer le script :
     python create_document.py --destination "./Test" --name "Mon_Cours" \\
       --template "Cours" --fields-file "./fields.json" --create-sections

Exemples (format --field, pour un champ isole ou une valeur sans antislash) :
  python create_document.py --destination "." --name "DS_Fonctions" --template "Devoir" \\
    --field "theme=Fonctions" --field "duree=55" --create-sections

Exemples (ancien format JSON en ligne de commande, legacy - deconseille) :
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
        "--fields-file",
        dest="fields_file",
        required=False,
        help=(
            "RECOMMANDE : chemin vers un fichier JSON (écrit avec l'outil Write) contenant "
            "les valeurs des champs, ex. {\"niveau\": \"$\\\\mathbf{2^{\\\\text{nde}}}$\"}. "
            "Évite les problèmes d'échappement des antislashs LaTeX en Bash/Git Bash."
        )
    )

    parser.add_argument(
        "--fields",
        required=False,
        help="[LEGACY] Dictionnaire JSON des valeurs de champs passé en ligne de commande"
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

    # Parser les champs - priorité : --fields-file (base) puis --field (surcouche/override),
    # avec --fields (legacy) comme base alternative si --fields-file n'est pas fourni.
    field_values = {}

    if args.fields_file:
        fields_file_path = Path(args.fields_file)
        if not fields_file_path.exists():
            print(f"❌ ERREUR: Fichier --fields-file introuvable: {fields_file_path}", file=sys.stderr)
            sys.exit(1)
        try:
            with open(fields_file_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ ERREUR: JSON invalide dans --fields-file ({fields_file_path}): {e}", file=sys.stderr)
            sys.exit(1)
        if not isinstance(loaded, dict):
            print(
                "❌ ERREUR: --fields-file doit contenir un objet JSON de la forme "
                "{\"champ\": \"valeur\", ...}",
                file=sys.stderr
            )
            sys.exit(1)
        field_values.update({str(k): ("" if v is None else str(v)) for k, v in loaded.items()})
    elif args.fields:
        # Legacy format : --fields JSON en ligne de commande (sujet aux problèmes d'échappement)
        try:
            field_values.update(json.loads(args.fields))
        except json.JSONDecodeError as e:
            print(f"❌ ERREUR: Format JSON invalide pour --fields: {e}", file=sys.stderr)
            sys.exit(1)

    if args.fields_list:
        # --field nom=valeur : complète ou surcharge les champs déjà chargés
        for field_arg in args.fields_list:
            if '=' not in field_arg:
                print(f"❌ ERREUR: Format invalide pour --field: '{field_arg}'", file=sys.stderr)
                print("   Format attendu: --field nom=valeur", file=sys.stderr)
                sys.exit(1)
            key, value = field_arg.split('=', 1)
            field_values[key.strip()] = value

    fields_source_provided = bool(args.fields_file or args.fields or args.fields_list)
    if not field_values and not fields_source_provided:
        print(
            "❌ ERREUR: Aucun champ fourni. Utilisez --fields-file (recommandé), --field ou --fields.",
            file=sys.stderr
        )
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

        warnings = result.get("warnings", [])
        if warnings:
            print(f"\n⚠️  Avertissements (non bloquants):", file=sys.stderr)
            for w in warnings:
                print(f"   - {w}", file=sys.stderr)

        next_steps = result.get("next_steps", [])
        if next_steps:
            print(f"\n⏭️  Prochaines étapes:", file=sys.stderr)
            for i, step in enumerate(next_steps, 1):
                print(f"   {i}. {step}", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('message', 'Erreur inconnue')}", file=sys.stderr)
        if "missing_fields" in result:
            print(f"   Champs manquants: {', '.join(result['missing_fields'])}", file=sys.stderr)
        if "example_fields_file" in result:
            print(
                "\n   Exemple de fields-file à compléter (écrire ce JSON avec l'outil Write, "
                "compléter les <A_COMPLETER:...>, puis relancer avec --fields-file) :",
                file=sys.stderr
            )
            print(
                "   " + json.dumps(result["example_fields_file"], ensure_ascii=False, indent=2).replace("\n", "\n   "),
                file=sys.stderr
            )
        if "hint" in result:
            print(f"\n   💡 {result['hint']}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    asyncio.run(main())
