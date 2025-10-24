#!/usr/bin/env python3
"""
MCP Server AMÉLIORÉ pour la recherche de définitions de commandes LaTeX.
Version avec CRUD, pagination et patterns enrichis.
"""

import json
import logging
import sys
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from difflib import SequenceMatcher

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("latex-search-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("latex-search-server")

# ============= PATTERNS ENRICHIS =============

# Patterns de base (existants)
COMMAND_PATTERNS = [
    r'\\(?:re)?newcommand\{?\\([^}]+)\}?',
    r'\\(?:re)?newcommand\*\{?\\([^}]+)\}?',
    r'\\def\\([^{]+)',
    r'\\gdef\\([^{]+)',
    r'\\edef\\([^{]+)',
    r'\\xdef\\([^{]+)',
    r'\\newtheorem\{([^}]+)\}',
    r'\\newcounter\{([^}]+)\}',
    r'\\definecolor\{?([^}]+)\}?',
]

# Environnements
ENVIRONMENT_PATTERNS = [
    r'\\(?:re)?newenvironment\{([^}]+)\}',
    r'\\NewDocumentEnvironment\{([^}]+)\}',
]

# LaTeX3
LATEX3_PATTERNS = [
    r'\\NewDocumentCommand\{?\\([^}]+)\}?',
    r'\\NewDocumentCommand\{([^}]+)\}',
    r'\\DeclareDocumentCommand\{?\\([^}]+)\}?',
    r'\\DeclareDocumentCommand\{([^}]+)\}',
    r'\\ProvideDocumentCommand\{?\\([^}]+)\}?',
    r'\\ProvideDocumentCommand\{([^}]+)\}',
    r'\\NewExpandableDocumentCommand\{?\\([^}]+)\}?',
    r'\\RenewExpandableDocumentCommand\{?\\([^}]+)\}?',
]

# NOUVEAUX : Booléens et conditionnels
BOOLEAN_PATTERNS = [
    r'\\newif\\(if[a-zA-Z]+)',
    r'\\newbool\{([^}]+)\}',
    r'\\providebool\{([^}]+)\}',
    r'\\newtoggle\{([^}]+)\}',
    r'\\providetoggle\{([^}]+)\}',
]

# NOUVEAUX : Longueurs et dimensions
LENGTH_PATTERNS = [
    r'\\newlength\{?\\([^}]+)\}?',
    r'\\newdimen\\([a-zA-Z]+)',
    r'\\newskip\\([a-zA-Z]+)',
    r'\\newcount\\([a-zA-Z]+)',
]

# NOUVEAUX : Macros avancées
ADVANCED_PATTERNS = [
    r'\\let\\([a-zA-Z]+)=',
    r'\\cs(?:def|let|new)\{([^}]+)\}',
    r'\\(?:new|renew|provide)robustcmd\{?\\([^}]+)\}?',
]

# NOUVEAUX : TikZ
TIKZ_PATTERNS = [
    r'\\tikzset\{([^/]+)/\.style',
    r'\\tikzstyle\{([^}]+)\}',
    r'\\pgfkeys\{/([^/]+)',
]

# NOUVEAUX : tcolorbox (TRÈS IMPORTANT!)
TCOLORBOX_PATTERNS = [
    r'\\tcbset\{([^/]+)/\.style',          # CRITIQUE pour les styles
    r'\\newtcolorbox\{([^}]+)\}',
    r'\\DeclareTColorBox\{([^}]+)\}',
    r'\\newtcbtheorem\{([^}]+)\}',
    r'\\DeclareTCBListing\{([^}]+)\}',
]

# Regrouper tous les patterns
ALL_PATTERNS = (
    COMMAND_PATTERNS + ENVIRONMENT_PATTERNS + LATEX3_PATTERNS +
    BOOLEAN_PATTERNS + LENGTH_PATTERNS + ADVANCED_PATTERNS +
    TIKZ_PATTERNS + TCOLORBOX_PATTERNS
)

# ============= SYSTÈME CRUD =============

class PackageRegistry:
    """Registre des packages avec système CRUD."""
    
    def __init__(self, config_file=".claude/mcp_servers/packages_registry.json"):
        self.config_file = Path(config_file)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.packages = self.load_registry()
        self.detector = LaTeXInstallationDetector()
    
    def load_registry(self) -> dict:
        """Charge le registre des packages."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {"packages": {}, "last_updated": None}
    
    def save_registry(self):
        """Sauvegarde le registre."""
        self.packages["last_updated"] = datetime.now().isoformat()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.packages, f, indent=2)
    
    def add_package(self, package_identifier: str) -> dict:
        """Ajoute un package au registre."""
        # Cas 1: Chemin absolu
        if os.path.isabs(package_identifier):
            if not os.path.exists(package_identifier):
                return {
                    "status": "error",
                    "error_type": "PATH_NOT_FOUND",
                    "message": f"Le chemin {package_identifier} n'existe pas",
                    "suggestion": "Vérifiez le chemin ou utilisez le nom du package"
                }
            
            package_name = Path(package_identifier).stem
            self.packages["packages"][package_name] = {
                "path": package_identifier,
                "added_date": datetime.now().isoformat(),
                "detection_method": "manual_path",
                "verified": True
            }
            self.save_registry()
            return {
                "status": "success",
                "message": f"Package {package_name} ajouté avec chemin manuel"
            }
        
        # Cas 2: Nom de package - tenter détection
        package_name = package_identifier
        detected_path = self.detector.find_package_location(package_name)
        
        if detected_path:
            self.packages["packages"][package_name] = {
                "path": str(detected_path),
                "added_date": datetime.now().isoformat(),
                "detection_method": "auto_detected",
                "verified": True
            }
            self.save_registry()
            return {
                "status": "success",
                "message": f"Package {package_name} détecté et ajouté",
                "path": str(detected_path)
            }
        
        return {
            "status": "error",
            "error_type": "PACKAGE_NOT_FOUND",
            "message": f"Package {package_name} introuvable dans l'installation LaTeX",
            "suggestion": f"Fournissez le chemin absolu avec add_package('/chemin/vers/{package_name}')"
        }
    
    def remove_package(self, package_name: str) -> dict:
        """Supprime un package du registre."""
        if package_name in self.packages["packages"]:
            del self.packages["packages"][package_name]
            self.save_registry()
            return {"status": "success", "message": f"Package {package_name} supprimé"}
        return {
            "status": "error",
            "error_type": "PACKAGE_NOT_IN_REGISTRY",
            "message": f"Package {package_name} n'est pas dans le registre"
        }
    
    def update_package_path(self, package_name: str, new_path: str) -> dict:
        """Met à jour le chemin d'un package."""
        if package_name not in self.packages["packages"]:
            return {
                "status": "error",
                "error_type": "PACKAGE_NOT_IN_REGISTRY",
                "message": f"Package {package_name} n'est pas dans le registre",
                "suggestion": f"Utilisez add_package('{package_name}') d'abord"
            }
        
        if not os.path.exists(new_path):
            return {
                "status": "error",
                "error_type": "PATH_NOT_FOUND",
                "message": f"Le nouveau chemin {new_path} n'existe pas"
            }
        
        self.packages["packages"][package_name]["path"] = new_path
        self.packages["packages"][package_name]["updated_date"] = datetime.now().isoformat()
        self.packages["packages"][package_name]["verified"] = True
        self.save_registry()
        
        return {"status": "success", "message": f"Chemin du package {package_name} mis à jour"}
    
    def get_package_path(self, package_name: str) -> Optional[str]:
        """Récupère le chemin d'un package avec vérification."""
        if package_name not in self.packages["packages"]:
            return None
        
        package_info = self.packages["packages"][package_name]
        path = package_info["path"]
        
        if not os.path.exists(path):
            package_info["verified"] = False
            self.save_registry()
            return None
        
        return path
    
    def list_packages(self) -> dict:
        """Liste tous les packages enregistrés."""
        result = {"packages": []}
        
        for name, info in self.packages["packages"].items():
            exists = os.path.exists(info["path"])
            result["packages"].append({
                "name": name,
                "path": info["path"],
                "exists": exists,
                "detection_method": info.get("detection_method", "unknown"),
                "added_date": info.get("added_date"),
                "verified": exists
            })
        
        return result


class LaTeXInstallationDetector:
    """Détection UNIQUEMENT lors de l'ajout d'un package."""
    
    def find_package_location(self, package_name: str) -> Optional[Path]:
        """Trouve l'emplacement d'un package - appelé UNIQUEMENT lors de add_package()."""
        # Essayer kpsewhich (TeX Live, MacTeX)
        try:
            result = subprocess.run(
                ['kpsewhich', f'{package_name}.sty'],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                return Path(result.stdout.strip()).parent
        except:
            pass
        
        # Fallback Windows/MiKTeX
        if sys.platform == "win32":
            miktex_paths = [
                Path(r"C:\Program Files\MiKTeX\tex\latex"),
                Path(os.path.expanduser(r"~\AppData\Roaming\MiKTeX\tex\latex"))
            ]
            for base_path in miktex_paths:
                if base_path.exists():
                    package_path = base_path / package_name
                    if package_path.exists():
                        return package_path
        
        # Chercher dans les chemins de la config existante (compatibilité)
        config = load_config()
        for package_dir in config.get("packageDirs", []):
            if os.path.exists(package_dir):
                if package_name.lower() in os.path.basename(package_dir).lower():
                    return Path(package_dir)
        
        return None


# ============= FONCTIONS DE RECHERCHE =============

def load_config() -> Dict[str, Any]:
    """Charge la configuration depuis mcp.json (compatibilité)."""
    config_path = Path(__file__).parent / "mcp.json"
    try:
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                full_config = json.load(f)
                return full_config.get('latex_search_server', {
                    "packageDirs": [],
                    "fileExtensions": [".tex", ".sty", ".cls", ".dtx"],
                    "maxResults": 20
                })
    except:
        pass
    return {
        "packageDirs": [],
        "fileExtensions": [".tex", ".sty", ".cls", ".dtx"],
        "maxResults": 20
    }


def search_in_file(file_path: str, command_name: str, patterns: List[str], exact_match: bool = False) -> List[Dict[str, Any]]:
    """Recherche dans un fichier avec les patterns spécifiés."""
    results = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        for line_number, line in enumerate(lines, 1):
            for pattern in patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                
                for match in matches:
                    found_name = match.group(1) if match.group(1) else ""
                    found_name = found_name.strip()
                    
                    if not found_name:
                        continue
                    
                    # Vérifier la correspondance
                    is_match = False
                    score = 0
                    
                    if exact_match:
                        is_match = found_name.lower() == command_name.lower()
                        score = 100 if is_match else 0
                    else:
                        # Si pas de pattern, tout matcher
                        if not command_name:
                            is_match = True
                            score = 50
                        else:
                            similarity = SequenceMatcher(None, command_name.lower(), found_name.lower()).ratio()
                            if found_name.lower() == command_name.lower():
                                score = 100
                            elif found_name.lower().startswith(command_name.lower()):
                                score = 90
                            elif command_name.lower() in found_name.lower():
                                score = 70
                            elif similarity > 0.6:
                                score = similarity * 60
                            is_match = score > 40
                    
                    if is_match:
                        # Contexte ultra-minimal : uniquement la ligne de définition
                        results.append({
                            "command_name": found_name,
                            "file": os.path.basename(file_path),
                            "line": line_number,
                            "definition": line.strip()[:150],  # Limiter à 150 chars
                            "score": score
                        })
    except Exception as e:
        logger.error(f"Erreur lecture {file_path}: {e}")
    
    return results


def scan_directory(dir_path: str, command_name: str, patterns: List[str], file_extensions: List[str] = None) -> List[Dict[str, Any]]:
    """Scan un répertoire avec les patterns donnés."""
    if file_extensions is None:
        file_extensions = [".tex", ".sty", ".cls", ".dtx"]
    
    results = []
    
    try:
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if any(file.lower().endswith(ext.lower()) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    file_results = search_in_file(file_path, command_name, patterns)
                    results.extend(file_results)
    except Exception as e:
        logger.error(f"Erreur scan {dir_path}: {e}")
    
    return results


# ============= FONCTIONS MCP =============

@mcp.tool()
def add_package(package_identifier: str) -> str:
    """
    Ajoute un package au registre pour les recherches futures.
    
    Args:
        package_identifier: Nom du package (ex: "tikz") OU chemin absolu
    
    Returns:
        JSON avec status détaillé
    """
    registry = PackageRegistry()
    result = registry.add_package(package_identifier)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def remove_package(package_name: str) -> str:
    """
    Supprime un package du registre.
    
    Args:
        package_name: Nom du package à supprimer
    
    Returns:
        JSON avec status
    """
    registry = PackageRegistry()
    result = registry.remove_package(package_name)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def update_package_path(package_name: str, new_path: str) -> str:
    """
    Met à jour le chemin d'un package existant.
    
    Args:
        package_name: Nom du package
        new_path: Nouveau chemin absolu
    
    Returns:
        JSON avec status
    """
    registry = PackageRegistry()
    result = registry.update_package_path(package_name, new_path)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def list_registered_packages() -> str:
    """
    Liste tous les packages enregistrés avec leur statut.
    
    Returns:
        JSON avec la liste des packages
    """
    registry = PackageRegistry()
    result = registry.list_packages()
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def search_in_specific_package(
    package_name: str, 
    command_pattern: str = "", 
    search_type: str = "all",
    offset: int = 0,
    limit: int = 20
) -> str:
    """
    Recherche dans un package LaTeX spécifique avec pagination.
    
    Args:
        package_name: Nom du package (doit être dans le registre)
        command_pattern: Pattern de recherche (vide = lister avec limite)
        search_type: Type ("commands", "environments", "booleans", "styles", "all")
        offset: Index de départ pour la pagination (défaut: 0)
        limit: Nombre max de résultats (défaut: 20, max: 50)
    
    Returns:
        JSON avec résultats paginés OU message d'erreur détaillé
    """
    registry = PackageRegistry()
    
    # Vérifier que le package est enregistré
    package_path = registry.get_package_path(package_name)
    
    if package_path is None:
        if package_name not in registry.packages["packages"]:
            return json.dumps({
                "status": "error",
                "error_type": "PACKAGE_NOT_REGISTERED",
                "message": f"Le package '{package_name}' n'est pas dans le registre",
                "registered_packages": list(registry.packages["packages"].keys()),
                "suggestion": f"Utilisez d'abord: add_package('{package_name}')"
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "status": "error",
                "error_type": "PATH_INVALID",
                "message": f"Le chemin du package '{package_name}' n'est plus valide",
                "old_path": registry.packages["packages"][package_name]["path"],
                "suggestion": f"Utilisez: update_package_path('{package_name}', '/nouveau/chemin')"
            }, ensure_ascii=False, indent=2)
    
    # Sélectionner les patterns
    patterns = []
    if search_type in ["commands", "all"]:
        patterns.extend(COMMAND_PATTERNS + LATEX3_PATTERNS + ADVANCED_PATTERNS)
    if search_type in ["environments", "all"]:
        patterns.extend(ENVIRONMENT_PATTERNS)
    if search_type in ["booleans", "all"]:
        patterns.extend(BOOLEAN_PATTERNS + LENGTH_PATTERNS)
    if search_type in ["styles", "all"]:
        patterns.extend(TCOLORBOX_PATTERNS + TIKZ_PATTERNS)
    
    if not patterns:
        patterns = ALL_PATTERNS
    
    # Limiter à 50 max
    limit = min(limit, 50)
    
    # Scanner le package
    try:
        config = load_config()
        all_results = scan_directory(package_path, command_pattern, patterns, config.get("fileExtensions"))
        
        if not all_results:
            return json.dumps({
                "status": "warning",
                "warning_type": "NO_RESULTS",
                "message": f"Aucune commande '{command_pattern}' trouvée dans '{package_name}'",
                "package": package_name,
                "path": package_path,
                "search_type": search_type,
                "suggestion": "Essayez un pattern plus général ou vérifiez l'orthographe"
            }, ensure_ascii=False, indent=2)
        
        # Trier par score
        all_results.sort(key=lambda x: (-x["score"], x["command_name"]))
        
        # Pagination
        total_results = len(all_results)
        paginated_results = all_results[offset:offset + limit]
        has_more = (offset + limit) < total_results
        
        return json.dumps({
            "status": "success",
            "package": package_name,
            "path": package_path,
            "search_type": search_type,
            "pattern": command_pattern,
            "pagination": {
                "offset": offset,
                "limit": limit,
                "total": total_results,
                "returned": len(paginated_results),
                "has_more": has_more,
                "next_offset": offset + limit if has_more else None
            },
            "results": paginated_results
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error_type": "SCAN_ERROR",
            "message": f"Erreur lors du scan du package '{package_name}'",
            "error_details": str(e),
            "path": package_path,
            "suggestion": "Vérifiez les permissions ou réessayez"
        }, ensure_ascii=False, indent=2)


# Garder les anciennes fonctions pour compatibilité
@mcp.tool()
def search_exact_command(command_name: str) -> str:
    """
    Recherche exacte d'une commande (compatibilité).
    Utilise les packages du mcp.json existant.
    """
    config = load_config()
    all_results = []
    
    for package_dir in config["packageDirs"]:
        if os.path.exists(package_dir):
            results = scan_directory(package_dir, command_name, ALL_PATTERNS, config["fileExtensions"])
            # Filtrer pour correspondance exacte
            exact_results = [r for r in results if r["command_name"].lower() == command_name.lower()]
            all_results.extend(exact_results)
    
    return json.dumps({
        "command": command_name,
        "search_type": "exact",
        "found": len(all_results),
        "results": all_results[:20]  # Limiter
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def search_fuzzy_command(command_pattern: str, max_results: int = 5) -> str:
    """
    Recherche floue d'une commande (compatibilité).

    ASTUCE: Pour une recherche plus précise, utilisez search_in_specific_package()
    qui retourne uniquement le code LaTeX de la commande.
    """
    config = load_config()
    all_results = []
    
    for package_dir in config["packageDirs"]:
        if os.path.exists(package_dir):
            results = scan_directory(package_dir, command_pattern, ALL_PATTERNS, config["fileExtensions"])
            all_results.extend(results)
    
    # Trier par score
    all_results.sort(key=lambda x: (-x.get("score", 0), x["command_name"]))

    # Message si trop de résultats
    message = None
    if len(all_results) > max_results:
        message = f"⚠️  {len(all_results)} résultats trouvés. Affichage des {max_results} meilleurs. Pour une recherche exacte, utilisez search_in_specific_package()."

    return json.dumps({
        "pattern": command_pattern,
        "search_type": "fuzzy",
        "found": len(all_results[:max_results]),
        "total_matches": len(all_results),
        "message": message,
        "results": all_results[:max_results]
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def list_available_packages() -> str:
    """
    Liste les packages disponibles (registre + mcp.json).
    """
    # Packages du registre
    registry = PackageRegistry()
    registry_info = registry.list_packages()
    
    # Packages de mcp.json (compatibilité)
    config = load_config()
    legacy_packages = []
    for package_dir in config["packageDirs"]:
        if os.path.exists(package_dir):
            legacy_packages.append({
                "path": package_dir,
                "name": os.path.basename(package_dir),
                "source": "mcp.json",
                "exists": True
            })
    
    return json.dumps({
        "registered_packages": registry_info["packages"],
        "legacy_packages": legacy_packages,
        "total": len(registry_info["packages"]) + len(legacy_packages)
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logger.info("Serveur MCP LaTeX Search AMÉLIORÉ démarré")
    logger.info("Nouvelles fonctionnalités: CRUD, pagination, patterns enrichis (tcbset, booléens, etc.)")
    mcp.run()