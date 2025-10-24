#!/usr/bin/env python3
"""
Serveur MCP pour la compilation de documents LaTeX.
Fournit des outils standardisés pour compiler des documents LaTeX avec gestion
des préférences utilisateur, détection automatique des compilateurs et gestion d'erreurs.
"""

import json
import logging
import sys
import subprocess
import os
import shutil
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("latex-compiler-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("latex-compiler-server")

# Chemins de configuration
PREFERENCES_FILE = Path(__file__).parent / ".." / "datas" / "latex-compiler-preferences.json"
CACHE_DIR = Path(__file__).parent / ".." / "datas" / ".latex-cache"

# Types de compilation
class CompilationType(str, Enum):
    SIMPLE = "simple"           # pdflatex une fois
    STANDARD = "standard"       # pdflatex 2 fois
    COMPLETE = "complete"       # pdflatex 3 fois
    BIBLIOGRAPHY = "bibliography" # pdflatex + bibtex + pdflatex x2
    GLOSSARY = "glossary"       # pdflatex + makeglossaries + pdflatex
    INDEX = "index"             # pdflatex + makeindex + pdflatex
    LUALATEX = "lualatex"       # lualatex au lieu de pdflatex
    XELATEX = "xelatex"         # xelatex au lieu de pdflatex
    CUSTOM = "custom"           # Commandes personnalisées

# Configuration par défaut
DEFAULT_PREFERENCES = {
    "compilers": {
        "pdflatex": {
            "path": "pdflatex",
            "args": ["-synctex=1", "-interaction=nonstopmode", "-file-line-error"],
            "enabled": True
        },
        "lualatex": {
            "path": "lualatex",
            "args": ["-synctex=1", "-interaction=nonstopmode", "-file-line-error", "-shell-escape"],
            "enabled": True
        },
        "xelatex": {
            "path": "xelatex",
            "args": ["-synctex=1", "-interaction=nonstopmode", "-file-line-error"],
            "enabled": False
        },
        "bibtex": {
            "path": "bibtex",
            "args": [],
            "enabled": False
        },
        "makeindex": {
            "path": "makeindex",
            "args": [],
            "enabled": False
        },
        "makeglossaries": {
            "path": "makeglossaries",
            "args": [],
            "enabled": False
        }
    },
    "compilation_profiles": {
        "lualatex_reims_favorite": {
            "description": "Profil optimisé Reims - LuaLaTeX avec shell-escape (recommandé 99% du temps)",
            "steps": [
                {"compiler": "lualatex", "count": 1}
            ]
        },
        "simple": {
            "description": "Compilation simple (2 passes - setup + final)",
            "steps": [
                {"compiler": "pdflatex", "count": 2}
            ]
        },
        "standard": {
            "description": "Compilation standard (3 passes pour références)",
            "steps": [
                {"compiler": "pdflatex", "count": 3}
            ]
        },
        "safe": {
            "description": "Compilation sécurisée avec passes multiples",
            "steps": [
                {"compiler": "pdflatex", "count": 4}
            ]
        },
        "complete": {
            "description": "Compilation complète (3 passes)",
            "steps": [
                {"compiler": "pdflatex", "count": 3}
            ]
        },
        "bibliography": {
            "description": "Compilation avec bibliographie",
            "steps": [
                {"compiler": "pdflatex", "count": 1},
                {"compiler": "bibtex", "count": 1},
                {"compiler": "pdflatex", "count": 2}
            ]
        }
    },
    "default_profile": "lualatex_reims_favorite",
    "output_directory": "build",
    "clean_aux_files": True,
    "aux_extensions": [".aux", ".log", ".toc", ".lof", ".lot", ".out", ".bbl", ".blg"],
    "verbose_output": False,
    "timeout_seconds": 120,
    "last_updated": "2025-09-11T00:00:00Z"
}

# Cache global
_preferences_cache: Optional[Dict[str, Any]] = None
_compiler_status_cache: Dict[str, bool] = {}

# Limite de tokens pour les réponses (approximativement 5k tokens)
MAX_RESPONSE_LENGTH = 20000  # ~5000 tokens * 4 chars/token

def truncate_response(response_data: Dict[str, Any], max_length: int = MAX_RESPONSE_LENGTH) -> Dict[str, Any]:
    """
    Tronque les données de réponse pour respecter la limite de tokens.
    Préserve les informations essentielles et tronque les détails verbeux.
    """
    # Convertir en JSON pour mesurer la taille
    json_str = json.dumps(response_data, ensure_ascii=False, indent=2)

    if len(json_str) <= max_length:
        return response_data

    # Copie des données à modifier
    truncated_data = response_data.copy()

    # Tronquer les sorties verboses en priorité
    if "steps" in truncated_data and isinstance(truncated_data["steps"], list):
        for step in truncated_data["steps"]:
            if isinstance(step, dict):
                # Limiter stdout/stderr
                if "stdout" in step and len(step["stdout"]) > 1000:
                    step["stdout"] = step["stdout"][:800] + "\n... [TRONQUÉ - sortie trop longue]"
                if "stderr" in step and len(step["stderr"]) > 1000:
                    step["stderr"] = step["stderr"][:800] + "\n... [TRONQUÉ - sortie trop longue]"

                # Limiter les analyses d'erreurs
                if "error_analysis" in step and isinstance(step["error_analysis"], dict):
                    error_analysis = step["error_analysis"]
                    if "errors" in error_analysis and isinstance(error_analysis["errors"], list):
                        # Garder max 3 erreurs avec contexte réduit
                        error_analysis["errors"] = error_analysis["errors"][:3]
                        for error in error_analysis["errors"]:
                            if "file_context" in error:
                                # Réduire le contexte de fichier
                                if "context_lines" in error["file_context"]:
                                    context_lines = error["file_context"]["context_lines"]
                                    if len(context_lines) > 10:
                                        error["file_context"]["context_lines"] = context_lines[:10]
                                        error["file_context"]["truncated"] = True

                    if "warnings" in error_analysis and isinstance(error_analysis["warnings"], list):
                        # Limiter à 5 warnings maximum
                        error_analysis["warnings"] = error_analysis["warnings"][:5]

    # Tronquer les préférences si présentes
    if "preferences" in truncated_data and isinstance(truncated_data["preferences"], dict):
        prefs = truncated_data["preferences"]
        if "compilation_profiles" in prefs:
            # Garder seulement les noms des profils pour économiser l'espace
            profiles = prefs["compilation_profiles"]
            truncated_data["preferences"]["compilation_profiles"] = {
                name: {"description": profile.get("description", "")}
                for name, profile in list(profiles.items())[:10]
            }
            if len(profiles) > 10:
                truncated_data["preferences"]["compilation_profiles"]["..."] = f"et {len(profiles)-10} autres profils"

    # Ajouter un indicateur de troncature
    truncated_data["_response_truncated"] = True
    truncated_data["_truncation_reason"] = "Réponse trop longue, détails réduits pour respecter la limite de tokens"

    # Vérifier la taille après troncature
    final_json = json.dumps(truncated_data, ensure_ascii=False, indent=2)
    if len(final_json) > max_length:
        # Troncature plus agressive si nécessaire
        if "analysis" in truncated_data:
            if isinstance(truncated_data["analysis"], dict):
                if "errors" in truncated_data["analysis"]:
                    truncated_data["analysis"]["errors"] = truncated_data["analysis"]["errors"][:1]
                if "warnings" in truncated_data["analysis"]:
                    truncated_data["analysis"]["warnings"] = truncated_data["analysis"]["warnings"][:2]
            elif isinstance(truncated_data["analysis"], str) and len(truncated_data["analysis"]) > 500:
                truncated_data["analysis"] = truncated_data["analysis"][:500] + "... [TRONQUÉ]"

    return truncated_data

def format_response(data: Dict[str, Any]) -> str:
    """
    Formate une réponse JSON en respectant la limite de tokens.
    """
    truncated_data = truncate_response(data)
    return json.dumps(truncated_data, ensure_ascii=False, indent=2)

def load_preferences() -> Dict[str, Any]:
    """Charge les préférences utilisateur."""
    global _preferences_cache
    
    if _preferences_cache is None:
        try:
            with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                _preferences_cache = json.load(f)
                logger.info(f"Préférences chargées: {len(_preferences_cache.get('compilers', {}))} compilateurs configurés")
        except FileNotFoundError:
            logger.info("Fichier de préférences non trouvé, création avec valeurs par défaut")
            _preferences_cache = DEFAULT_PREFERENCES.copy()
            save_preferences(_preferences_cache)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur JSON dans les préférences: {e}")
            _preferences_cache = DEFAULT_PREFERENCES.copy()
    
    return _preferences_cache

def save_preferences(preferences: Dict[str, Any]) -> None:
    """Sauvegarde les préférences utilisateur."""
    global _preferences_cache
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        preferences["last_updated"] = datetime.now().isoformat() + "Z"
        
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, ensure_ascii=False, indent=2)
        
        _preferences_cache = preferences
        logger.info("Préférences sauvegardées avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des préférences: {e}")
        raise

def check_compiler(compiler_name: str) -> bool:
    """Vérifie si un compilateur est disponible sur le système."""
    global _compiler_status_cache
    
    if compiler_name in _compiler_status_cache:
        return _compiler_status_cache[compiler_name]
    
    preferences = load_preferences()
    compiler_config = preferences.get("compilers", {}).get(compiler_name, {})
    compiler_path = compiler_config.get("path", compiler_name)
    
    try:
        result = subprocess.run(
            [compiler_path, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        available = result.returncode == 0
        _compiler_status_cache[compiler_name] = available
        return available
    except (subprocess.TimeoutExpired, FileNotFoundError):
        _compiler_status_cache[compiler_name] = False
        return False

def parse_latex_log(log_file_path: Path) -> Dict[str, Any]:
    """
    Analyse un fichier .log LaTeX pour extraire les erreurs détaillées.
    Retourne un dictionnaire avec les erreurs trouvées.
    """
    if not log_file_path.exists():
        return {"errors": [], "warnings": [], "analysis": "Fichier log non trouvé"}
    
    try:
        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
            log_content = f.read()
    except Exception as e:
        return {"errors": [], "warnings": [], "analysis": f"Erreur lecture log: {e}"}
    
    errors = []
    warnings = []
    
    # Pattern pour les erreurs LaTeX
    error_pattern = r'! (.+?)\n(.+?)\n(.+?)\nl\.(\d+)(.*)'
    error_matches = re.finditer(error_pattern, log_content, re.MULTILINE | re.DOTALL)
    
    for match in error_matches:
        error_msg = match.group(1).strip()
        context_line = match.group(2).strip()
        problem_line = match.group(3).strip()
        line_number = match.group(4)
        additional_context = match.group(5).strip() if match.group(5) else ""
        
        errors.append({
            "type": "LaTeX Error",
            "message": error_msg,
            "line_number": int(line_number),
            "context": context_line,
            "problem_line": problem_line,
            "additional_context": additional_context
        })
    
    # Pattern pour les erreurs de compilation plus générales
    general_error_pattern = r'! (.+?)(?=\n|$)'
    general_matches = re.finditer(general_error_pattern, log_content, re.MULTILINE)
    
    for match in general_matches:
        error_msg = match.group(1).strip()
        # Éviter les doublons avec les erreurs déjà capturées
        if not any(err["message"] == error_msg for err in errors):
            errors.append({
                "type": "Compilation Error",
                "message": error_msg,
                "line_number": None,
                "context": "",
                "problem_line": "",
                "additional_context": ""
            })
    
    # Pattern pour les avertissements
    warning_pattern = r'LaTeX Warning: (.+?)(?=\n|$)'
    warning_matches = re.finditer(warning_pattern, log_content, re.MULTILINE)
    
    for match in warning_matches:
        warning_msg = match.group(1).strip()
        # Extraire le numéro de ligne si présent
        line_match = re.search(r'on input line (\d+)', warning_msg)
        line_number = int(line_match.group(1)) if line_match else None
        
        warnings.append({
            "type": "LaTeX Warning",
            "message": warning_msg,
            "line_number": line_number
        })
    
    # Analyse générale du log
    analysis = []
    if "Undefined control sequence" in log_content:
        analysis.append("Commandes LaTeX inconnues détectées")
    if "Missing $ inserted" in log_content:
        analysis.append("Erreurs de mode mathématique ($ manquant)")
    if "File not found" in log_content or "I couldn't open file name" in log_content:
        analysis.append("Fichiers manquants (images, packages, etc.)")
    if "Package" in log_content and "Error" in log_content:
        analysis.append("Erreurs de packages LaTeX")
    
    return {
        "errors": errors,
        "warnings": warnings[:10],  # Limiter les warnings
        "analysis": "; ".join(analysis) if analysis else "Analyse automatique indisponible",
        "total_errors": len(errors),
        "total_warnings": len(warnings)
    }

def get_tex_file_context(tex_file_path: Path, line_number: int, context_lines: int = 3) -> Dict[str, Any]:
    """
    Récupère le contexte autour d'une ligne spécifique dans un fichier .tex
    """
    try:
        with open(tex_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        start_line = max(1, line_number - context_lines)
        end_line = min(total_lines, line_number + context_lines)
        
        context = []
        for i in range(start_line - 1, end_line):  # -1 car les listes sont 0-indexées
            line_num = i + 1
            line_content = lines[i].rstrip()
            is_error_line = line_num == line_number
            context.append({
                "line_number": line_num,
                "content": line_content,
                "is_error_line": is_error_line
            })
        
        return {
            "file": str(tex_file_path),
            "error_line": line_number,
            "context_start": start_line,
            "context_end": end_line,
            "context_lines": context
        }
    
    except Exception as e:
        return {
            "file": str(tex_file_path),
            "error_line": line_number,
            "error": f"Impossible de lire le contexte: {e}",
            "context_lines": []
        }

def run_compilation_step(
    file_path: Path,
    compiler_name: str,
    working_dir: Optional[Path] = None,
    pass_number: int = 1
) -> Tuple[bool, str, str, Dict[str, Any]]:
    """
    Exécute une étape de compilation avec analyse des erreurs.
    Retourne (success, stdout, stderr, error_analysis)
    """
    preferences = load_preferences()
    compiler_config = preferences.get("compilers", {}).get(compiler_name, {})
    
    if not compiler_config.get("enabled", False):
        return False, "", f"Compilateur {compiler_name} non activé", {}
    
    # Convertir automatiquement en Path objects si ce sont des strings
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    if working_dir and not isinstance(working_dir, Path):
        working_dir = Path(working_dir)
    
    compiler_path = compiler_config.get("path", compiler_name)
    compiler_args = compiler_config.get("args", [])
    timeout = preferences.get("timeout_seconds", 120)
    
    # Construire la commande
    if compiler_name in ["bibtex", "makeindex", "makeglossaries"]:
        # Ces outils prennent juste le nom du fichier sans extension
        cmd = [compiler_path] + compiler_args + [file_path.stem]
    else:
        # Les compilateurs LaTeX prennent le fichier complet
        cmd = [compiler_path] + compiler_args + [str(file_path)]
    
    # Définir le répertoire de travail
    cwd = working_dir or file_path.parent
    
    try:
        logger.info(f"Exécution (passe {pass_number}): {' '.join(cmd)} dans {cwd}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(cwd),
            timeout=timeout
        )
        
        success = result.returncode == 0
        error_analysis = {}
        
        # Analyse du log seulement pour les compilateurs LaTeX et en cas d'erreur
        if compiler_name in ["pdflatex", "lualatex", "xelatex"] and not success:
            log_file = file_path.parent / (file_path.stem + ".log")
            error_analysis = parse_latex_log(log_file)
            
            # Ajouter le contexte pour chaque erreur avec numéro de ligne
            if error_analysis.get("errors"):
                for error in error_analysis["errors"]:
                    if error.get("line_number"):
                        context = get_tex_file_context(file_path, error["line_number"])
                        error["file_context"] = context
        
        # Logique de tolérance aux erreurs selon le type de compilateur et la passe
        if not success and compiler_name in ["pdflatex", "lualatex", "xelatex"]:
            # Avec -interaction=nonstopmode et -file-line-error, le compilateur continue
            # même avec des erreurs. On vérifie si un PDF a été généré malgré les erreurs
            pdf_file = file_path.parent / (file_path.stem + ".pdf")
            
            # Si un PDF est créé malgré le code de retour != 0, c'est souvent OK pour continuer
            if pdf_file.exists():
                logger.info(f"PDF généré malgré code de retour {result.returncode}, continuation...")
                success = "partial"  # Succès partiel pour continuer
            
            # Analyser le log pour déterminer la gravité
            else:
                log_file = file_path.parent / (file_path.stem + ".log")
                if log_file.exists():
                    log_analysis = parse_latex_log(log_file)
                    
                    # Erreurs critiques qui doivent vraiment arrêter
                    critical_patterns = [
                        "Emergency stop",
                        "File ended",
                        "Runaway argument",
                        "! LaTeX Error: File .* not found",
                        "! I can't find file",
                        "! Undefined control sequence"
                    ]
                    
                    # Erreurs spéciales pour bfcours qui nécessitent plusieurs passes
                    bfcours_continuation_patterns = [
                        "Something's wrong--perhaps a missing \\\\item",
                        "printvocindex",
                        "printbfpoints",
                        "voc{",
                        "competence{"
                    ]
                    
                    has_critical_error = False
                    has_bfcours_error = False
                    
                    for error in log_analysis.get("errors", []):
                        error_msg = error.get("message", "")
                        # Vérifier les erreurs critiques
                        if any(re.search(pattern, error_msg, re.IGNORECASE) for pattern in critical_patterns):
                            has_critical_error = True
                            break
                        # Vérifier les erreurs bfcours qui nécessitent continuation
                        if any(re.search(pattern, error_msg, re.IGNORECASE) for pattern in bfcours_continuation_patterns):
                            has_bfcours_error = True
                    
                    # Pour LuaLaTeX avec des erreurs bfcours, continuer systématiquement
                    if compiler_name == "lualatex" and has_bfcours_error and not has_critical_error:
                        logger.info(f"Passe {pass_number} - Erreur bfcours détectée avec LuaLaTeX, continuation nécessaire...")
                        success = "partial"
                    # Sinon, tolérance normale sur les premières passes
                    elif pass_number <= 2 and not has_critical_error:
                        logger.info(f"Passe {pass_number} avec erreurs non-critiques, continuation...")
                        success = "partial"
        
        return success, result.stdout, result.stderr, error_analysis
        
    except subprocess.TimeoutExpired:
        return False, "", f"Timeout après {timeout} secondes", {}
    except FileNotFoundError:
        return False, "", f"Compilateur {compiler_path} non trouvé", {}
    except Exception as e:
        return False, "", str(e), {}

def clean_auxiliary_files(file_path) -> List[str]:
    """Nettoie les fichiers auxiliaires après compilation."""
    preferences = load_preferences()
    
    if not preferences.get("clean_aux_files", True):
        return []
    
    # Convertir en Path si nécessaire
    if not isinstance(file_path, Path):
        file_path = Path(file_path)
    
    aux_extensions = preferences.get("aux_extensions", [])
    cleaned_files = []
    
    base_path = file_path.parent / file_path.stem
    
    for ext in aux_extensions:
        aux_file = Path(str(base_path) + ext)
        if aux_file.exists():
            try:
                aux_file.unlink()
                cleaned_files.append(str(aux_file))
            except Exception as e:
                logger.warning(f"Impossible de supprimer {aux_file}: {e}")
    
    return cleaned_files

# ========== MÉTHODES MCP ==========

@mcp.tool()
def compile_document(
    file_path: str,
    compilation_type: str = "default",
    clean_aux: bool = True
) -> str:
    """
    Compile un document LaTeX selon le profil spécifié.
    
    Args:
        file_path: Chemin vers le fichier .tex à compiler
        compilation_type: Type de compilation (simple, standard, complete, bibliography, etc.)
        clean_aux: Nettoyer les fichiers auxiliaires après compilation
    
    Returns:
        JSON avec le résultat de la compilation
    """
    try:
        preferences = load_preferences()
        tex_file = Path(file_path)
        
        # Vérifier que le fichier existe
        if not tex_file.exists():
            return format_response({
                "status": "error",
                "error": f"Fichier non trouvé: {file_path}"
            })
        
        # Déterminer le profil de compilation
        if compilation_type == "default":
            compilation_type = preferences.get("default_profile", "lualatex_reims_favorite")
        
        profile = preferences.get("compilation_profiles", {}).get(compilation_type)
        
        if not profile:
            return format_response({
                "status": "error",
                "error": f"Profil de compilation inconnu: {compilation_type}",
                "available_profiles": list(preferences.get("compilation_profiles", {}).keys())
            })
        
        # Exécuter les étapes de compilation
        results = []
        overall_success = True
        partial_success_count = 0
        
        for step in profile.get("steps", []):
            compiler = step.get("compiler")
            count = step.get("count", 1)
            
            # Vérifier que le compilateur est disponible
            if not check_compiler(compiler):
                results.append({
                    "compiler": compiler,
                    "success": False,
                    "error": f"Compilateur {compiler} non disponible ou non configuré",
                    "error_analysis": {}
                })
                overall_success = False
                break
            
            # Exécuter le nombre de fois requis
            for i in range(count):
                success, stdout, stderr, error_analysis = run_compilation_step(tex_file, compiler, None, i + 1)
                
                # Gérer les succès partiels
                if success == "partial":
                    partial_success_count += 1
                    actual_success = True  # Continuer la compilation
                    logger.info(f"Passe {i + 1} avec succès partiel, continuation...")
                else:
                    actual_success = success
                
                result_entry = {
                    "compiler": compiler,
                    "pass": i + 1,
                    "success": success,  # Garder le statut original pour l'historique
                    "actual_success": actual_success,  # Statut pour la logique de continuation
                    "stdout": stdout if preferences.get("verbose_output", False) else "",
                    "stderr": stderr if not actual_success else "",
                    "error_analysis": error_analysis,
                    "pdf_exists": (tex_file.parent / (tex_file.stem + ".pdf")).exists()
                }
                
                results.append(result_entry)
                
                # Arrêter seulement si échec réel (pas partiel)
                if not actual_success:
                    overall_success = False
                    break
            
            if not overall_success:
                break
        
        # Nettoyer les fichiers auxiliaires si demandé
        cleaned_files = []
        if clean_aux and overall_success:
            cleaned_files = clean_auxiliary_files(tex_file)
        
        # Vérifier si le PDF a été généré
        pdf_file = tex_file.parent / (tex_file.stem + ".pdf")
        pdf_generated = pdf_file.exists()
        
        # Message détaillé selon les résultats
        if overall_success:
            message = "Compilation réussie"
            if partial_success_count > 0:
                message += f" (avec {partial_success_count} passe(s) de setup)"
        else:
            message = "Compilation échouée"
            # Ajouter les détails des erreurs principales
            main_errors = []
            for result in results:
                if not result["success"] and result.get("error_analysis", {}).get("errors"):
                    for error in result["error_analysis"]["errors"][:2]:  # Max 2 erreurs principales
                        if error.get("line_number"):
                            main_errors.append(f"Ligne {error['line_number']}: {error['message']}")
                        else:
                            main_errors.append(error['message'])
            
            if main_errors:
                message += f" - {'; '.join(main_errors[:3])}"  # Max 3 erreurs dans le message
        
        return format_response({
            "status": "success" if overall_success else "error",
            "compilation_type": compilation_type,
            "file": str(tex_file),
            "pdf_generated": pdf_generated,
            "pdf_path": str(pdf_file) if pdf_generated else None,
            "steps": results,
            "cleaned_files": cleaned_files,
            "message": message,
            "partial_success_passes": partial_success_count
        })
        
    except Exception as e:
        import traceback
        logger.error(f"Erreur dans compile_document: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return format_response({
            "status": "error",
            "error": str(e),
            "traceback": traceback.format_exc()
        })

@mcp.tool()
def quick_compile(file_path: str, passes: int = 1) -> str:
    """
    Compilation rapide avec le profil lualatex_reims_favorite (LuaLaTeX + shell-escape).

    Args:
        file_path: Chemin vers le fichier .tex
        passes: Nombre de passes de compilation (par défaut: 1)

    Returns:
        JSON avec le résultat de la compilation
    """
    # Créer un profil temporaire avec le nombre de passes demandé
    preferences = load_preferences()

    # Créer dynamiquement le profil si passes != 1
    if passes != 1:
        profile_name = f"lualatex_reims_favorite-{passes}passes"
        preferences["compilation_profiles"][profile_name] = {
            "description": f"Profil Reims avec {passes} passes LuaLaTeX",
            "steps": [
                {"compiler": "lualatex", "count": passes}
            ]
        }
        save_preferences(preferences)
        return compile_document(file_path, profile_name, True)
    else:
        return compile_document(file_path, "lualatex_reims_favorite", True)

@mcp.tool()
def detect_compilers() -> str:
    """
    Détecte automatiquement les compilateurs LaTeX disponibles sur le système.
    
    Returns:
        JSON avec la liste des compilateurs détectés
    """
    try:
        preferences = load_preferences()
        compilers_to_check = ["pdflatex", "lualatex", "xelatex", "bibtex", "makeindex", "makeglossaries", "latexmk"]
        detected = {}
        
        for compiler in compilers_to_check:
            available = check_compiler(compiler)
            detected[compiler] = {
                "available": available,
                "configured": compiler in preferences.get("compilers", {}),
                "enabled": preferences.get("compilers", {}).get(compiler, {}).get("enabled", False)
            }
            
            # Obtenir la version si disponible
            if available:
                try:
                    result = subprocess.run(
                        [compiler, "--version"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        version_line = result.stdout.split('\n')[0]
                        detected[compiler]["version"] = version_line
                except:
                    pass
        
        return format_response({
            "status": "success",
            "compilers": detected,
            "recommendation": "Activez les compilateurs détectés avec 'update_compiler_config'"
        })
        
    except Exception as e:
        logger.error(f"Erreur dans detect_compilers: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def get_compilation_profiles() -> str:
    """
    Liste tous les profils de compilation disponibles.
    
    Returns:
        JSON avec les profils et leurs descriptions
    """
    try:
        preferences = load_preferences()
        profiles = preferences.get("compilation_profiles", {})
        
        profiles_info = {}
        for name, profile in profiles.items():
            profiles_info[name] = {
                "description": profile.get("description", ""),
                "steps": profile.get("steps", []),
                "is_default": name == preferences.get("default_profile", "lualatex_reims_favorite")
            }

        return format_response({
            "status": "success",
            "profiles": profiles_info,
            "default_profile": preferences.get("default_profile", "lualatex_reims_favorite")
        })
        
    except Exception as e:
        logger.error(f"Erreur dans get_compilation_profiles: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def add_compilation_profile(
    name: str,
    description: str,
    steps: str
) -> str:
    """
    Ajoute un nouveau profil de compilation personnalisé.
    
    Args:
        name: Nom du profil
        description: Description du profil
        steps: JSON string des étapes de compilation
    
    Returns:
        JSON avec le résultat de l'opération
    """
    try:
        preferences = load_preferences()
        
        # Parser les étapes
        try:
            steps_list = json.loads(steps)
        except json.JSONDecodeError:
            return format_response({
                "status": "error",
                "error": "Format JSON invalide pour les étapes"
            })
        
        # Ajouter le profil
        preferences["compilation_profiles"][name] = {
            "description": description,
            "steps": steps_list
        }
        
        save_preferences(preferences)
        
        return format_response({
            "status": "success",
            "message": f"Profil '{name}' ajouté avec succès",
            "profile": preferences["compilation_profiles"][name]
        })
        
    except Exception as e:
        logger.error(f"Erreur dans add_compilation_profile: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def update_compiler_config(
    compiler_name: str,
    path: str = None,
    args: str = None,
    enabled: bool = None
) -> str:
    """
    Met à jour la configuration d'un compilateur.
    
    Args:
        compiler_name: Nom du compilateur (pdflatex, lualatex, etc.)
        path: Chemin vers l'exécutable (optionnel)
        args: Arguments en JSON string (optionnel)
        enabled: Activer/désactiver le compilateur (optionnel)
    
    Returns:
        JSON avec le résultat de l'opération
    """
    try:
        preferences = load_preferences()
        
        # Créer la config si elle n'existe pas
        if compiler_name not in preferences["compilers"]:
            preferences["compilers"][compiler_name] = {
                "path": compiler_name,
                "args": [],
                "enabled": False
            }
        
        # Mettre à jour les champs fournis
        if path is not None:
            preferences["compilers"][compiler_name]["path"] = path
        
        if args is not None:
            try:
                args_list = json.loads(args) if isinstance(args, str) else args
                preferences["compilers"][compiler_name]["args"] = args_list
            except json.JSONDecodeError:
                return format_response({
                    "status": "error",
                    "error": "Format JSON invalide pour les arguments"
                })
        
        if enabled is not None:
            preferences["compilers"][compiler_name]["enabled"] = enabled
        
        save_preferences(preferences)
        
        # Invalider le cache de statut
        global _compiler_status_cache
        if compiler_name in _compiler_status_cache:
            del _compiler_status_cache[compiler_name]
        
        return format_response({
            "status": "success",
            "message": f"Configuration mise à jour pour {compiler_name}",
            "config": preferences["compilers"][compiler_name]
        })
        
    except Exception as e:
        logger.error(f"Erreur dans update_compiler_config: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def set_default_profile(profile_name: str) -> str:
    """
    Définit le profil de compilation par défaut.
    
    Args:
        profile_name: Nom du profil à utiliser par défaut
    
    Returns:
        JSON avec le résultat de l'opération
    """
    try:
        preferences = load_preferences()
        
        if profile_name not in preferences.get("compilation_profiles", {}):
            return format_response({
                "status": "error",
                "error": f"Profil '{profile_name}' non trouvé",
                "available_profiles": list(preferences.get("compilation_profiles", {}).keys())
            })
        
        preferences["default_profile"] = profile_name
        save_preferences(preferences)
        
        return format_response({
            "status": "success",
            "message": f"Profil par défaut défini sur '{profile_name}'",
            "default_profile": profile_name
        })
        
    except Exception as e:
        logger.error(f"Erreur dans set_default_profile: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def get_preferences() -> str:
    """
    Récupère toutes les préférences de compilation.
    
    Returns:
        JSON avec les préférences actuelles
    """
    try:
        preferences = load_preferences()
        return format_response({
            "status": "success",
            "preferences": preferences
        })
        
    except Exception as e:
        logger.error(f"Erreur dans get_preferences: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def clean_build_files(directory: str, extensions: str = None) -> str:
    """
    Nettoie les fichiers de build dans un répertoire.
    
    Args:
        directory: Répertoire à nettoyer
        extensions: Liste d'extensions en JSON (optionnel, utilise les préférences par défaut)
    
    Returns:
        JSON avec les fichiers supprimés
    """
    try:
        preferences = load_preferences()
        dir_path = Path(directory)
        
        if not dir_path.exists():
            return format_response({
                "status": "error",
                "error": f"Répertoire non trouvé: {directory}"
            })
        
        # Déterminer les extensions à nettoyer
        if extensions:
            try:
                ext_list = json.loads(extensions) if isinstance(extensions, str) else extensions
            except json.JSONDecodeError:
                return format_response({
                    "status": "error",
                    "error": "Format JSON invalide pour les extensions"
                })
        else:
            ext_list = preferences.get("aux_extensions", [])
        
        # Nettoyer les fichiers
        cleaned_files = []
        for ext in ext_list:
            for file_path in dir_path.glob(f"*{ext}"):
                try:
                    file_path.unlink()
                    cleaned_files.append(str(file_path))
                except Exception as e:
                    logger.warning(f"Impossible de supprimer {file_path}: {e}")
        
        return format_response({
            "status": "success",
            "directory": str(dir_path),
            "cleaned_files": cleaned_files,
            "count": len(cleaned_files)
        })
        
    except Exception as e:
        logger.error(f"Erreur dans clean_build_files: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def test_compilation(test_content: str = None) -> str:
    """
    Teste la configuration avec un document LaTeX simple.
    
    Args:
        test_content: Contenu LaTeX à tester (optionnel)
    
    Returns:
        JSON avec le résultat du test
    """
    try:
        # Créer un fichier test temporaire
        test_dir = CACHE_DIR / "test"
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file = test_dir / "test_compilation.tex"
        
        # Contenu par défaut si non fourni
        if not test_content:
            test_content = r"""
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[french]{babel}

\title{Test de Compilation}
\author{LaTeX Compiler Server}
\date{\today}

\begin{document}
\maketitle

\section{Test}
Ceci est un document de test pour vérifier la configuration du compilateur LaTeX.

Formule mathématique: $E = mc^2$

\end{document}
"""
        
        # Écrire le fichier test
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(test_content)
        
        # Compiler avec le profil par défaut
        result = compile_document(str(test_file), "lualatex_reims_favorite", True)
        result_dict = json.loads(result)
        
        # Nettoyer
        if test_file.exists():
            test_file.unlink()
        pdf_file = test_file.with_suffix('.pdf')
        if pdf_file.exists():
            pdf_file.unlink()
        
        return format_response({
            "status": "success" if result_dict["status"] == "success" else "error",
            "test_file": str(test_file),
            "compilation_result": result_dict,
            "message": "Test de compilation " + ("réussi" if result_dict["status"] == "success" else "échoué")
        })
        
    except Exception as e:
        logger.error(f"Erreur dans test_compilation: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def analyze_latex_log(log_file_path: str, tex_file_path: str = None) -> str:
    """
    Analyse un fichier .log LaTeX existant pour diagnostiquer les erreurs.
    
    Args:
        log_file_path: Chemin vers le fichier .log à analyser
        tex_file_path: Chemin vers le fichier .tex correspondant (optionnel)
    
    Returns:
        JSON avec l'analyse détaillée des erreurs
    """
    try:
        log_path = Path(log_file_path)
        
        if not log_path.exists():
            return format_response({
                "status": "error",
                "error": f"Fichier log non trouvé: {log_file_path}"
            })
        
        # Analyser le log
        analysis = parse_latex_log(log_path)
        
        # Si le fichier .tex est fourni, ajouter le contexte pour chaque erreur
        if tex_file_path:
            tex_path = Path(tex_file_path)
            if tex_path.exists():
                for error in analysis.get("errors", []):
                    if error.get("line_number"):
                        context = get_tex_file_context(tex_path, error["line_number"])
                        error["file_context"] = context
        
        return format_response({
            "status": "success",
            "log_file": str(log_path),
            "tex_file": tex_file_path,
            "analysis": analysis
        })
        
    except Exception as e:
        logger.error(f"Erreur dans analyze_latex_log: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def get_file_context(file_path: str, line_number: int, context_lines: int = 5) -> str:
    """
    Récupère le contexte autour d'une ligne spécifique dans un fichier.
    
    Args:
        file_path: Chemin vers le fichier à analyser
        line_number: Numéro de ligne (1-indexé)
        context_lines: Nombre de lignes de contexte avant et après
    
    Returns:
        JSON avec le contexte de la ligne
    """
    try:
        file_path_obj = Path(file_path)
        context = get_tex_file_context(file_path_obj, line_number, context_lines)
        
        return format_response({
            "status": "success",
            "context": context
        })
        
    except Exception as e:
        logger.error(f"Erreur dans get_file_context: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

@mcp.tool()
def reset_preferences() -> str:
    """
    Réinitialise les préférences aux valeurs par défaut.
    
    Returns:
        JSON avec le résultat de l'opération
    """
    try:
        global _preferences_cache, _compiler_status_cache
        
        save_preferences(DEFAULT_PREFERENCES)
        _preferences_cache = None
        _compiler_status_cache = {}
        
        return format_response({
            "status": "success",
            "message": "Préférences réinitialisées aux valeurs par défaut",
            "preferences": DEFAULT_PREFERENCES
        })
        
    except Exception as e:
        logger.error(f"Erreur dans reset_preferences: {e}")
        return format_response({
            "status": "error",
            "error": str(e)
        })

if __name__ == "__main__":
    logger.info("Démarrage du serveur LaTeX Compiler MCP")
    logger.info("Chargement des préférences...")
    load_preferences()
    logger.info("Détection des compilateurs...")
    
    # Détection automatique au démarrage
    for compiler in ["pdflatex", "lualatex", "xelatex"]:
        if check_compiler(compiler):
            logger.info(f"✓ {compiler} détecté")
        else:
            logger.info(f"✗ {compiler} non disponible")
    
    logger.info("Serveur prêt")
    mcp.run()