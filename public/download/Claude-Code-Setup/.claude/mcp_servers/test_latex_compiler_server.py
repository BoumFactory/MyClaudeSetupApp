#!/usr/bin/env python3
"""
Script de test pour le serveur LaTeX Compiler MCP
"""

import json
import tempfile
from pathlib import Path

def create_test_document():
    """Crée un document LaTeX de test"""
    test_content = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}
\usepackage{amsmath}

\title{Test LaTeX Compiler MCP}
\author{Serveur MCP}
\date{\today}

\begin{document}
\maketitle

\section{Introduction}
Ce document teste le serveur MCP de compilation LaTeX.

\section{Mathématiques}
Voici une formule mathématique :
\begin{equation}
    E = mc^2
\end{equation}

Et une autre :
\[
    \int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}
\]

\section{Liste}
\begin{itemize}
    \item Premier élément
    \item Deuxième élément
    \item Troisième élément
\end{itemize}

\section{Tableau}
\begin{tabular}{|c|c|}
\hline
A & B \\
\hline
1 & 2 \\
3 & 4 \\
\hline
\end{tabular}

\section{Conclusion}
Si ce document compile sans erreur, le serveur fonctionne correctement !

\end{document}
"""
    return test_content

def manual_test_guide():
    """Guide de test manuel pour le serveur"""
    print("=" * 60)
    print("GUIDE DE TEST - SERVEUR LATEX COMPILER MCP")
    print("=" * 60)
    print()
    
    print("📋 ÉTAPES DE TEST:")
    print()
    
    print("1. Démarrer le serveur:")
    print("   python latex_compiler_server.py")
    print()
    
    print("2. Dans Claude Code, tester les méthodes MCP:")
    print()
    
    # Test 1: Détection des compilateurs
    print("🔍 TEST 1: Détection des compilateurs")
    print("   mcp__latex-compiler-server__detect_compilers()")
    print("   → Doit lister pdflatex, lualatex, xelatex avec leur statut")
    print()
    
    # Test 2: Configuration
    print("⚙️ TEST 2: Configuration d'un compilateur")
    print("   mcp__latex-compiler-server__update_compiler_config(")
    print("     compiler_name='pdflatex',")
    print("     enabled=True")
    print("   )")
    print("   → Doit activer pdflatex")
    print()
    
    # Test 3: Profils
    print("📝 TEST 3: Liste des profils")
    print("   mcp__latex-compiler-server__get_compilation_profiles()")
    print("   → Doit afficher simple, standard, complete, bibliography")
    print()
    
    # Test 4: Test de compilation
    print("🧪 TEST 4: Test de compilation")
    print("   mcp__latex-compiler-server__test_compilation()")
    print("   → Doit compiler un document de test et retourner le résultat")
    print()
    
    # Test 5: Compilation d'un vrai fichier
    print("📄 TEST 5: Compilation d'un fichier réel")
    
    # Créer le fichier de test
    test_file = Path.cwd() / "test_document.tex"
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(create_test_document())
    
    print(f"   Fichier créé: {test_file}")
    print("   mcp__latex-compiler-server__quick_compile(")
    print(f"     file_path='{test_file}'")
    print("   )")
    print("   → Doit créer test_document.pdf")
    print()
    
    # Test 6: Compilation avec profil spécifique
    print("🎯 TEST 6: Compilation avec profil")
    print("   mcp__latex-compiler-server__compile_document(")
    print(f"     file_path='{test_file}',")
    print("     compilation_type='complete',")
    print("     clean_aux=True")
    print("   )")
    print("   → Doit faire 3 passes de compilation")
    print()
    
    # Test 7: Nettoyage
    print("🧹 TEST 7: Nettoyage des fichiers")
    print("   mcp__latex-compiler-server__clean_build_files(")
    print(f"     directory='{test_file.parent}'")
    print("   )")
    print("   → Doit nettoyer les .aux, .log, etc.")
    print()
    
    print("=" * 60)
    print("RÉSULTATS ATTENDUS:")
    print("=" * 60)
    
    print("✅ detect_compilers(): Liste des compilateurs avec versions")
    print("✅ test_compilation(): Document de test compilé avec succès")
    print("✅ quick_compile(): PDF généré rapidement")
    print("✅ Messages d'erreur clairs en cas de problème")
    print("✅ Fichiers auxiliaires nettoyés automatiquement")
    print()
    
    print("⚠️ EN CAS DE PROBLÈME:")
    print("- Vérifier que pdflatex est installé (MiKTeX ou TeX Live)")
    print("- Vérifier les chemins dans latex-compiler-preferences.json")
    print("- Utiliser get_preferences() pour voir la configuration")
    print("- Utiliser reset_preferences() pour repartir à zéro")
    print()

def automatic_compilation_test():
    """Test automatique de compilation"""
    print("🤖 TEST AUTOMATIQUE DE COMPILATION")
    print("-" * 40)
    
    # Créer un fichier temporaire
    with tempfile.NamedTemporaryFile(mode='w', suffix='.tex', delete=False, encoding='utf-8') as f:
        f.write(create_test_document())
        temp_file = Path(f.name)
    
    print(f"Fichier test créé: {temp_file}")
    
    # Simulation de ce que ferait l'agent MCP
    test_scenarios = [
        {
            "name": "Détection des compilateurs",
            "method": "detect_compilers",
            "params": {}
        },
        {
            "name": "Test de compilation intégré",
            "method": "test_compilation",
            "params": {}
        },
        {
            "name": "Compilation rapide du fichier test",
            "method": "quick_compile",
            "params": {"file_path": str(temp_file)}
        },
        {
            "name": "Compilation complète",
            "method": "compile_document",
            "params": {
                "file_path": str(temp_file),
                "compilation_type": "complete",
                "clean_aux": True
            }
        }
    ]
    
    print("\nScénarios de test préparés:")
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"  {i}. {scenario['name']}")
        print(f"     → {scenario['method']}({', '.join(f'{k}={v}' for k, v in scenario['params'].items())})")
    
    print(f"\nPour exécuter ces tests, lancez le serveur et utilisez les méthodes MCP dans Claude Code.")
    print(f"Le fichier test sera disponible à: {temp_file}")
    
    return temp_file

def check_latex_installation():
    """Vérifie l'installation LaTeX sur le système"""
    import subprocess
    import shutil
    
    print("🔍 VÉRIFICATION DE L'INSTALLATION LATEX")
    print("-" * 45)
    
    latex_commands = [
        ("pdflatex", "Compilateur principal"),
        ("lualatex", "Compilateur moderne avec Lua"),
        ("xelatex", "Compilateur avec support Unicode"),
        ("bibtex", "Gestionnaire de bibliographie"),
        ("makeindex", "Générateur d'index"),
        ("latexmk", "Système de compilation automatique")
    ]
    
    found_commands = []
    missing_commands = []
    
    for cmd, description in latex_commands:
        if shutil.which(cmd):
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=5)
                if result.returncode == 0:
                    version_line = result.stdout.split('\n')[0]
                    found_commands.append((cmd, description, version_line))
                    print(f"✅ {cmd:<12} - {description}")
                    print(f"   {version_line}")
                else:
                    missing_commands.append((cmd, description))
                    print(f"❌ {cmd:<12} - {description} (erreur)")
            except (subprocess.TimeoutExpired, Exception):
                missing_commands.append((cmd, description))
                print(f"❌ {cmd:<12} - {description} (timeout/erreur)")
        else:
            missing_commands.append((cmd, description))
            print(f"❌ {cmd:<12} - {description} (non trouvé)")
    
    print()
    print("=" * 45)
    if len(found_commands) >= 1:  # Au moins pdflatex
        print("✅ Installation LaTeX détectée !")
        print(f"   {len(found_commands)} compilateur(s) trouvé(s)")
        if "pdflatex" in [cmd for cmd, _, _ in found_commands]:
            print("   → Le serveur MCP devrait fonctionner")
        else:
            print("   ⚠️ pdflatex non trouvé - fonctionnement limité")
    else:
        print("❌ Aucun compilateur LaTeX trouvé !")
        print("   → Installez MiKTeX ou TeX Live pour utiliser le serveur")
    
    if missing_commands:
        print(f"\n📦 Compilateurs manquants: {len(missing_commands)}")
        print("   Considérez installer une distribution LaTeX complète")
    
    return len(found_commands) > 0

def main():
    """Fonction principale de test"""
    print("🧪 UTILITAIRE DE TEST - SERVEUR LATEX COMPILER MCP")
    print("=" * 60)
    print()
    
    # Vérification LaTeX
    latex_ok = check_latex_installation()
    print()
    
    if latex_ok:
        print("🚀 PRÊT POUR LES TESTS !")
        print()
        
        # Créer le fichier de test automatique
        test_file = automatic_compilation_test()
        print()
        
        # Guide manuel
        manual_test_guide()
        
        print("📁 FICHIERS CRÉÉS:")
        print(f"   - Fichier de test: {test_file}")
        print("   - Guide complet dans ce script")
        
    else:
        print("⚠️ INSTALLATION LATEX REQUISE")
        print()
        print("Pour utiliser le serveur LaTeX Compiler MCP, vous devez installer:")
        print("- MiKTeX (Windows): https://miktex.org/")
        print("- TeX Live (Multi-plateforme): https://www.tug.org/texlive/")
        print()
        print("Après installation, relancez ce script pour vérifier.")

if __name__ == "__main__":
    main()