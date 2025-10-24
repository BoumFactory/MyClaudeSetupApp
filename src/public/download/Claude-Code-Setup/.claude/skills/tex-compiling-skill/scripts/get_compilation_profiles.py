#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour lister les profils de compilation disponibles.
Utilise le serveur MCP latex-compiler-server.
"""

import sys
import json
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from latex_compiler_server import get_compilation_profiles
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    print("📋 Profils de compilation disponibles", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = get_compilation_profiles()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        profiles = result.get("profiles", {})
        default_profile = result.get("default_profile", "")

        print(f"\n🎯 Profil par défaut: {default_profile}\n", file=sys.stderr)
        print(f"📚 Profils disponibles ({len(profiles)}):\n", file=sys.stderr)

        for name, info in profiles.items():
            is_default = "⭐" if info.get("is_default") else "  "
            print(f"{is_default} {name}", file=sys.stderr)
            print(f"   {info.get('description', '')}", file=sys.stderr)

            steps = info.get("steps", [])
            if steps:
                print(f"   Étapes:", file=sys.stderr)
                for step in steps:
                    compiler = step.get("compiler", "")
                    count = step.get("count", 1)
                    print(f"      - {compiler} × {count}", file=sys.stderr)

            print("", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
