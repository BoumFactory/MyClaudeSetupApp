#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server pour la correction automatique d'encodage des fichiers LaTeX.
Résout les problèmes d'encodage UTF-8 sous Windows.
"""

import json
import logging
import sys
import codecs
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configuration du logging pour écrire dans stderr seulement
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("encoding-fixer-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("encoding-fixer-server")

# Encodages courants à essayer (par ordre de probabilité)
ENCODAGES_COURANTS = [
    'utf-8',
    'latin-1',
    'iso-8859-1',
    'cp1252',  # Windows Western European
    'cp850',   # DOS Western European
    'utf-8-sig',  # UTF-8 avec BOM
]

def try_read_file(file_path: Path) -> tuple[Optional[str], Optional[str]]:
    """
    Essaie de lire le fichier avec différents encodages.

    Args:
        file_path: Chemin du fichier à lire

    Returns:
        Tuple (contenu, encodage_détecté) ou (None, None) si échec
    """
    for encoding in ENCODAGES_COURANTS:
        try:
            with codecs.open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            # Vérifier que le contenu est cohérent (pas trop de caractères bizarres)
            if content.count('�') < len(content) * 0.01:  # Moins de 1% de caractères invalides
                logger.info(f"Encodage détecté: {encoding}")
                return content, encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    return None, None


@mcp.tool()
def fix_file_encoding(
    file_path: str,
    output_path: str = "",
    create_backup: bool = True
) -> str:
    """
    Corrige l'encodage d'un fichier en le convertissant vers UTF-8.

    Args:
        file_path: Chemin du fichier à corriger
        output_path: Chemin du fichier de sortie (vide = écrase l'original)
        create_backup: Créer une sauvegarde du fichier original

    Returns:
        JSON string avec le résultat de l'opération
    """
    try:
        input_path = Path(file_path)

        if not input_path.exists():
            return json.dumps({
                "success": False,
                "error": f"Fichier introuvable: {file_path}",
                "file": file_path
            }, ensure_ascii=False, indent=2)

        logger.info(f"Analyse de: {input_path.name}")

        # Tentative de lecture
        content, detected_encoding = try_read_file(input_path)

        if content is None:
            return json.dumps({
                "success": False,
                "error": "Impossible de détecter l'encodage",
                "file": file_path,
                "encodings_tried": ENCODAGES_COURANTS
            }, ensure_ascii=False, indent=2)

        # Déterminer le fichier de sortie
        if output_path == "":
            # Créer backup et écraser l'original
            if create_backup:
                backup_path = input_path.with_suffix(input_path.suffix + '.backup')
                if backup_path.exists():
                    logger.warning(f"Backup existe déjà: {backup_path.name}")
                else:
                    input_path.rename(backup_path)
                    logger.info(f"Backup créé: {backup_path.name}")
                output_final = input_path
            else:
                output_final = input_path
        else:
            output_final = Path(output_path)

        # Écriture en UTF-8
        with codecs.open(output_final, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Fichier converti: {output_final.name}")

        # Vérification
        with codecs.open(output_final, 'r', encoding='utf-8') as f:
            test_read = f.read()

        return json.dumps({
            "success": True,
            "file": str(output_final),
            "original_encoding": detected_encoding,
            "new_encoding": "utf-8",
            "characters_count": len(test_read),
            "backup_created": create_backup and output_path == "",
            "backup_path": str(input_path.with_suffix(input_path.suffix + '.backup')) if create_backup and output_path == "" else None
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur lors de la correction d'encodage: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "file": file_path
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def detect_file_encoding(file_path: str) -> str:
    """
    Détecte l'encodage d'un fichier sans le modifier.

    Args:
        file_path: Chemin du fichier à analyser

    Returns:
        JSON string avec l'encodage détecté
    """
    try:
        input_path = Path(file_path)

        if not input_path.exists():
            return json.dumps({
                "success": False,
                "error": f"Fichier introuvable: {file_path}",
                "file": file_path
            }, ensure_ascii=False, indent=2)

        content, detected_encoding = try_read_file(input_path)

        if content is None:
            return json.dumps({
                "success": False,
                "error": "Impossible de détecter l'encodage",
                "file": file_path,
                "encodings_tried": ENCODAGES_COURANTS
            }, ensure_ascii=False, indent=2)

        # Statistiques sur le contenu
        stats = {
            "total_chars": len(content),
            "lines": content.count('\n') + 1,
            "accented_chars": sum(1 for c in content if ord(c) > 127),
            "invalid_chars": content.count('�')
        }

        return json.dumps({
            "success": True,
            "file": file_path,
            "detected_encoding": detected_encoding,
            "is_utf8": detected_encoding == 'utf-8',
            "needs_conversion": detected_encoding != 'utf-8',
            "statistics": stats
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur lors de la détection d'encodage: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "file": file_path
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def fix_directory_encoding(
    directory_path: str,
    pattern: str = "*.tex",
    create_backup: bool = True,
    recursive: bool = False
) -> str:
    """
    Corrige l'encodage de tous les fichiers correspondant au pattern dans un répertoire.

    Args:
        directory_path: Chemin du répertoire à traiter
        pattern: Pattern de fichiers (ex: "*.tex", "*.md")
        create_backup: Créer une sauvegarde de chaque fichier
        recursive: Traiter les sous-répertoires récursivement

    Returns:
        JSON string avec le résumé des opérations
    """
    try:
        dir_path = Path(directory_path)

        if not dir_path.exists() or not dir_path.is_dir():
            return json.dumps({
                "success": False,
                "error": f"Répertoire introuvable: {directory_path}"
            }, ensure_ascii=False, indent=2)

        # Trouver les fichiers
        if recursive:
            files = list(dir_path.rglob(pattern))
        else:
            files = list(dir_path.glob(pattern))

        results = {
            "success": True,
            "directory": str(dir_path),
            "pattern": pattern,
            "recursive": recursive,
            "files_found": len(files),
            "files_processed": 0,
            "files_converted": 0,
            "files_already_utf8": 0,
            "files_failed": 0,
            "details": []
        }

        for file_path in files:
            # Ignorer les backups
            if file_path.suffix == '.backup':
                continue

            content, detected_encoding = try_read_file(file_path)

            if content is None:
                results["files_failed"] += 1
                results["details"].append({
                    "file": str(file_path),
                    "status": "failed",
                    "reason": "Encodage non détectable"
                })
                continue

            results["files_processed"] += 1

            if detected_encoding == 'utf-8':
                results["files_already_utf8"] += 1
                results["details"].append({
                    "file": str(file_path),
                    "status": "skipped",
                    "encoding": "utf-8"
                })
                continue

            # Conversion nécessaire
            if create_backup:
                backup_path = file_path.with_suffix(file_path.suffix + '.backup')
                if not backup_path.exists():
                    file_path.rename(backup_path)

            # Écriture en UTF-8
            with codecs.open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            results["files_converted"] += 1
            results["details"].append({
                "file": str(file_path),
                "status": "converted",
                "original_encoding": detected_encoding,
                "new_encoding": "utf-8"
            })

        return json.dumps(results, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur lors du traitement du répertoire: {e}")
        return json.dumps({
            "success": False,
            "error": str(e),
            "directory": directory_path
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_encoding_stats() -> str:
    """
    Retourne des informations sur les encodages supportés.

    Returns:
        JSON string avec la liste des encodages supportés
    """
    return json.dumps({
        "supported_encodings": ENCODAGES_COURANTS,
        "default_output": "utf-8",
        "description": "Serveur MCP pour la correction automatique d'encodage des fichiers LaTeX"
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    logger.info("Démarrage du serveur MCP encoding-fixer-server")
    mcp.run()
