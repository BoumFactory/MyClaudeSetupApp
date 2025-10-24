#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour récupérer les préférences de compilation.
Utilise le serveur MCP latex-compiler-server.
"""

import sys
import json
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from latex_compiler_server import get_preferences
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    print("⚙️  Récupération des préférences de compilation", file=sys.stderr)

    # Appeler la fonction du serveur MCP
    result_json = get_preferences()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        prefs = result.get("preferences", {})

        print(f"\n✅ Préférences chargées\n", file=sys.stderr)

        # Profil par défaut
        print(f"🎯 Profil par défaut: {prefs.get('default_profile', '')}", file=sys.stderr)

        # Compilateurs configurés
        compilers = prefs.get("compilers", {})
        print(f"\n🔧 Compilateurs configurés ({len(compilers)}):", file=sys.stderr)
        for name, config in compilers.items():
            enabled = "🟢" if config.get("enabled") else "🔴"
            print(f"   {enabled} {name}", file=sys.stderr)

        # Profils de compilation
        profiles = prefs.get("compilation_profiles", {})
        print(f"\n📋 Profils de compilation: {len(profiles)}", file=sys.stderr)

        # Options diverses
        print(f"\n🧹 Nettoyage automatique: {'Oui' if prefs.get('clean_aux_files') else 'Non'}", file=sys.stderr)
        print(f"⏱️  Timeout: {prefs.get('timeout_seconds', 120)}s", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
