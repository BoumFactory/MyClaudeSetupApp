#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script CLI pour réinitialiser les préférences de compilation.
Utilise le serveur MCP latex-compiler-server.
"""

import sys
import json
from pathlib import Path

# Ajouter le chemin du serveur MCP au path
MCP_SERVER_PATH = Path(__file__).parent.parent.parent.parent / "mcp_servers"
sys.path.insert(0, str(MCP_SERVER_PATH))

try:
    from latex_compiler_server import reset_preferences
except ImportError:
    print("❌ ERREUR: Impossible d'importer latex_compiler_server", file=sys.stderr)
    sys.exit(1)


def main():
    print("🔄 Réinitialisation des préférences de compilation", file=sys.stderr)
    print("⚠️  Cette action réinitialisera TOUTES les préférences", file=sys.stderr)

    # Demander confirmation
    response = input("\nÊtes-vous sûr ? (oui/non): ")

    if response.lower() not in ["oui", "o", "yes", "y"]:
        print("❌ Opération annulée", file=sys.stderr)
        sys.exit(0)

    # Appeler la fonction du serveur MCP
    result_json = reset_preferences()
    result = json.loads(result_json)

    # Affichage humain sur stderr
    if result.get("status") == "success":
        print(f"\n✅ {result.get('message', 'Préférences réinitialisées')}", file=sys.stderr)

        prefs = result.get("preferences", {})
        print(f"\n📋 Profil par défaut: {prefs.get('default_profile', '')}", file=sys.stderr)
        print(f"🔧 Compilateurs: {len(prefs.get('compilers', {}))} configurés", file=sys.stderr)
        print(f"📚 Profils: {len(prefs.get('compilation_profiles', {}))} disponibles", file=sys.stderr)
    else:
        print(f"❌ Erreur: {result.get('error', 'Erreur inconnue')}", file=sys.stderr)

    # Sortie JSON pour l'agent
    print(result_json)

    sys.exit(0 if result.get("status") == "success" else 1)


if __name__ == "__main__":
    main()
