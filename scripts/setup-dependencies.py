#!/usr/bin/env python3
"""
Script d'installation automatique des dépendances pour Claude Code

Ce script :
1. Détecte automatiquement tous les requirements.txt dans .claude/skills et .claude/mcp_servers
2. Collecte toutes les dépendances Python
3. Installe tout dans le venv du projet
4. Détecte et installe les dépendances Node.js si nécessaire

Usage:
    python scripts/setup-dependencies.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Set, Dict

# Couleurs pour l'affichage
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(msg: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 60}{Colors.ENDC}\n")

def print_success(msg: str):
    print(f"{Colors.OKGREEN}[OK] {msg}{Colors.ENDC}")

def print_info(msg: str):
    print(f"{Colors.OKCYAN}[INFO] {msg}{Colors.ENDC}")

def print_warning(msg: str):
    print(f"{Colors.WARNING}[WARN] {msg}{Colors.ENDC}")

def print_error(msg: str):
    print(f"{Colors.FAIL}[ERROR] {msg}{Colors.ENDC}")

def get_project_root() -> Path:
    """Retourne la racine du projet"""
    return Path(__file__).parent.parent

def find_requirements_files() -> List[Path]:
    """Trouve tous les fichiers requirements.txt dans .claude/"""
    project_root = get_project_root()
    claude_dir = project_root / ".claude"

    if not claude_dir.exists():
        print_warning(f"Le dossier .claude n'existe pas: {claude_dir}")
        return []

    requirements_files = []

    # Chercher dans skills
    skills_dir = claude_dir / "skills"
    if skills_dir.exists():
        requirements_files.extend(skills_dir.rglob("requirements.txt"))

    # Chercher dans mcp_servers
    mcp_dir = claude_dir / "mcp_servers"
    if mcp_dir.exists():
        requirements_files.extend(mcp_dir.rglob("requirements.txt"))

    return requirements_files

def find_package_json_files() -> List[Path]:
    """Trouve tous les fichiers package.json dans .claude/mcp_servers"""
    project_root = get_project_root()
    mcp_dir = project_root / ".claude" / "mcp_servers"

    if not mcp_dir.exists():
        return []

    return list(mcp_dir.rglob("package.json"))

def collect_python_dependencies(requirements_files: List[Path]) -> Set[str]:
    """Collecte toutes les dépendances Python uniques"""
    all_deps = set()

    for req_file in requirements_files:
        print_info(f"Lecture: {req_file.relative_to(get_project_root())}")
        try:
            with open(req_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Ignorer les commentaires et lignes vides
                    if line and not line.startswith('#'):
                        all_deps.add(line)
        except Exception as e:
            print_error(f"Erreur de lecture de {req_file}: {e}")

    return all_deps

def check_venv() -> bool:
    """Vérifie si un venv existe"""
    project_root = get_project_root()
    venv_dir = project_root / "venv"
    return venv_dir.exists()

def create_venv():
    """Crée un venv si nécessaire"""
    project_root = get_project_root()
    venv_dir = project_root / "venv"

    if venv_dir.exists():
        print_success("Environnement virtuel déjà existant")
        return True

    print_info("Création de l'environnement virtuel...")
    try:
        subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            check=True,
            capture_output=True
        )
        print_success("Environnement virtuel créé")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Échec de création du venv: {e}")
        return False

def get_pip_path() -> Path:
    """Retourne le chemin vers pip du venv"""
    project_root = get_project_root()
    if sys.platform == "win32":
        return project_root / "venv" / "Scripts" / "pip.exe"
    else:
        return project_root / "venv" / "bin" / "pip"

def install_python_dependencies(dependencies: Set[str]):
    """Installe les dépendances Python dans le venv"""
    if not dependencies:
        print_info("Aucune dépendance Python à installer")
        return

    print_info(f"Installation de {len(dependencies)} dépendances Python...")

    pip_path = get_pip_path()

    # Créer un fichier requirements temporaire
    project_root = get_project_root()
    temp_requirements = project_root / "temp_requirements.txt"

    try:
        with open(temp_requirements, 'w', encoding='utf-8') as f:
            for dep in sorted(dependencies):
                f.write(f"{dep}\n")

        # Installer les dépendances
        print_info("Installation en cours...")
        result = subprocess.run(
            [str(pip_path), "install", "-r", str(temp_requirements)],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print_success("Toutes les dépendances Python sont installées")
        else:
            print_error("Erreur lors de l'installation:")
            print(result.stderr)

    finally:
        # Supprimer le fichier temporaire
        if temp_requirements.exists():
            temp_requirements.unlink()

def check_node_installed() -> bool:
    """Vérifie si Node.js est installé"""
    try:
        subprocess.run(
            ["node", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_node_dependencies(package_files: List[Path]):
    """Installe les dépendances Node.js"""
    if not package_files:
        print_info("Aucune dépendance Node.js détectée")
        return

    if not check_node_installed():
        print_warning("Node.js n'est pas installé, impossible d'installer les dépendances Node.js")
        return

    print_info(f"Détection de {len(package_files)} serveurs MCP Node.js")

    for package_file in package_files:
        mcp_dir = package_file.parent
        print_info(f"Installation dans {mcp_dir.relative_to(get_project_root())}")

        try:
            # Vérifier si pnpm est disponible
            use_pnpm = False
            try:
                subprocess.run(["pnpm", "--version"], capture_output=True, check=True)
                use_pnpm = True
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass

            # Installer avec pnpm ou npm
            cmd = ["pnpm", "install"] if use_pnpm else ["npm", "install"]
            subprocess.run(
                cmd,
                cwd=str(mcp_dir),
                capture_output=True,
                check=True
            )
            print_success(f"Dépendances installées dans {mcp_dir.name}")

        except subprocess.CalledProcessError as e:
            print_error(f"Erreur d'installation dans {mcp_dir.name}: {e}")

def create_activation_scripts():
    """Crée des scripts d'activation pratiques"""
    project_root = get_project_root()

    # Script pour Windows
    activate_bat = project_root / "activate-venv.bat"
    with open(activate_bat, 'w') as f:
        f.write("@echo off\n")
        f.write("call venv\\Scripts\\activate.bat\n")
        f.write("echo Environnement virtuel active!\n")
        f.write("echo Utilisez 'deactivate' pour sortir\n")

    # Script pour Unix/Mac
    activate_sh = project_root / "activate-venv.sh"
    with open(activate_sh, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("source venv/bin/activate\n")
        f.write("echo 'Environnement virtuel activé!'\n")
        f.write("echo \"Utilisez 'deactivate' pour sortir\"\n")

    # Rendre exécutable sur Unix
    if sys.platform != "win32":
        os.chmod(activate_sh, 0o755)

    print_success("Scripts d'activation créés:")
    print_info(f"  Windows: activate-venv.bat")
    print_info(f"  Unix/Mac: ./activate-venv.sh")

def main():
    print_header("Installation automatique des dépendances Claude Code")

    # 1. Créer ou vérifier le venv
    print_header("Étape 1: Environnement virtuel Python")
    if not create_venv():
        print_error("Impossible de continuer sans venv")
        sys.exit(1)

    # 2. Détecter les dépendances Python
    print_header("Étape 2: Détection des dépendances Python")
    requirements_files = find_requirements_files()

    if requirements_files:
        print_success(f"Trouvé {len(requirements_files)} fichier(s) requirements.txt")
        dependencies = collect_python_dependencies(requirements_files)
        print_success(f"Total: {len(dependencies)} dépendance(s) unique(s)")

        # 3. Installer les dépendances Python
        print_header("Étape 3: Installation des dépendances Python")
        install_python_dependencies(dependencies)
    else:
        print_info("Aucun fichier requirements.txt trouvé")

    # 4. Détecter et installer les dépendances Node.js
    print_header("Étape 4: Dépendances Node.js (serveurs MCP)")
    package_files = find_package_json_files()
    install_node_dependencies(package_files)

    # 5. Créer les scripts d'activation
    print_header("Étape 5: Scripts d'activation")
    create_activation_scripts()

    # Résumé final
    print_header("Installation terminée!")
    print_success("Toutes les dépendances sont installées")
    print()
    print_info("Pour utiliser les scripts Python des skills:")
    if sys.platform == "win32":
        print_info("  1. Activez le venv: activate-venv.bat")
    else:
        print_info("  1. Activez le venv: ./activate-venv.sh")
    print_info("  2. Lancez vos scripts: python .claude/skills/[skill]/scripts/[script].py")
    print()

if __name__ == "__main__":
    main()
