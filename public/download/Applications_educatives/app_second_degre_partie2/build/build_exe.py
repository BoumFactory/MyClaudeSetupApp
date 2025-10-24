# -*- coding: utf-8 -*-
"""
Script de construction de l'exécutable standalone avec PyInstaller
Pour l'application Second Degré - Partie 2
"""

import PyInstaller.__main__
import os
import sys
import shutil
import io

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemin de base du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_DIR = os.path.join(BASE_DIR, 'build')
DIST_DIR = os.path.join(BASE_DIR, 'dist')

print("=" * 80)
print("Construction de l'exécutable : Second Degré - Partie 2")
print("=" * 80)
print(f"\nRépertoire du projet : {BASE_DIR}")
print(f"Répertoire de build : {BUILD_DIR}")
print(f"Répertoire de sortie : {DIST_DIR}")
print()

# Nettoyer les anciens builds
if os.path.exists(os.path.join(BUILD_DIR, 'SecondDegre_Partie2')):
    print("Nettoyage de l'ancien build...")
    shutil.rmtree(os.path.join(BUILD_DIR, 'SecondDegre_Partie2'))

if os.path.exists(os.path.join(DIST_DIR, 'SecondDegre_Partie2.exe')):
    print("Suppression de l'ancien exécutable...")
    os.remove(os.path.join(DIST_DIR, 'SecondDegre_Partie2.exe'))

# Options PyInstaller
pyinstaller_args = [
    os.path.join(BASE_DIR, 'app.py'),
    '--name=SecondDegre_Partie2',
    '--onefile',
    '--windowed',
    '--noupx',
    f'--distpath={DIST_DIR}',
    f'--workpath={BUILD_DIR}',
    f'--specpath={BUILD_DIR}',
    # Ajouter les dossiers de données
    f'--add-data={os.path.join(BASE_DIR, "templates")};templates',
    f'--add-data={os.path.join(BASE_DIR, "static")};static',
    f'--add-data={os.path.join(BASE_DIR, "data")};data',
    # Hooks et imports cachés
    '--hidden-import=flask',
    '--hidden-import=jinja2',
    '--hidden-import=werkzeug',
    '--hidden-import=click',
    '--hidden-import=itsdangerous',
    '--hidden-import=markupsafe',
    # Options de performance
    '--clean',
    '--noconfirm',
]

print("Démarrage de PyInstaller...")
print("Options :")
for arg in pyinstaller_args:
    print(f"  {arg}")
print()

try:
    PyInstaller.__main__.run(pyinstaller_args)
    print("\n" + "=" * 80)
    print("✅ BUILD RÉUSSI !")
    print("=" * 80)

    exe_path = os.path.join(DIST_DIR, 'SecondDegre_Partie2.exe')
    if os.path.exists(exe_path):
        size_mb = os.path.getsize(exe_path) / (1024 * 1024)
        print(f"\nExécutable créé : {exe_path}")
        print(f"Taille : {size_mb:.2f} MB")
        print("\nPour tester :")
        print(f'  {exe_path}')
        print("\nPour distribuer :")
        print(f"  Copiez le fichier {os.path.basename(exe_path)} aux élèves")
    else:
        print("\n⚠️  L'exécutable n'a pas été trouvé après le build")
        sys.exit(1)

except Exception as e:
    print("\n" + "=" * 80)
    print("❌ ERREUR LORS DU BUILD")
    print("=" * 80)
    print(f"\nErreur : {e}")
    sys.exit(1)
