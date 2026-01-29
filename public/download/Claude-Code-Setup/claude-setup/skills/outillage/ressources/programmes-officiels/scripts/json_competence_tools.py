#!/usr/bin/env python3
"""
Outils atomiques pour manipuler les JSON de competences sans les charger entierement.

Ces scripts sont concus pour etre appeles par un agent IA qui ne doit pas
charger les gros fichiers JSON dans son contexte.

Usage:
    python json_competence_tools.py insert <json_file> <competence_json>
    python json_competence_tools.py delete <json_file> <code>
    python json_competence_tools.py update <json_file> <code> <field> <value>
    python json_competence_tools.py get <json_file> <code>
    python json_competence_tools.py list_codes <json_file>
    python json_competence_tools.py search <json_file> <keyword>
    python json_competence_tools.py validate <json_file>
"""

import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional

# Forcer UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
EXTRACTIONS_DIR = DATA_DIR / "extractions"


def load_json_file(json_path: Path) -> dict:
    """Charge un fichier JSON."""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json_file(json_path: Path, data: dict):
    """Sauvegarde un fichier JSON avec backup."""
    # Creer backup
    backup_path = json_path.with_suffix('.json.bak')
    if json_path.exists():
        import shutil
        shutil.copy2(json_path, backup_path)

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Fichier sauvegarde: {json_path.name}")


def insert_competence(json_path: Path, competence_json: str) -> bool:
    """
    Insere une nouvelle competence dans le fichier JSON.

    Args:
        json_path: Chemin vers le fichier JSON
        competence_json: JSON string de la competence a inserer

    Returns:
        True si succes, False sinon
    """
    try:
        data = load_json_file(json_path)
        new_comp = json.loads(competence_json)

        # Verifier que le code n'existe pas deja
        existing_codes = {c.get('code') for c in data.get('competences', [])}
        if new_comp.get('code') in existing_codes:
            print(f"[ERREUR] Code deja existant: {new_comp.get('code')}")
            return False

        # Ajouter la competence
        if 'competences' not in data:
            data['competences'] = []

        data['competences'].append(new_comp)
        data['_last_modified'] = datetime.now().isoformat()

        save_json_file(json_path, data)
        print(f"[OK] Competence inseree: {new_comp.get('code')}")
        return True

    except Exception as e:
        print(f"[ERREUR] {e}")
        return False


def delete_competence(json_path: Path, code: str) -> bool:
    """
    Supprime une competence par son code.

    Args:
        json_path: Chemin vers le fichier JSON
        code: Code de la competence a supprimer

    Returns:
        True si succes, False sinon
    """
    try:
        data = load_json_file(json_path)

        original_count = len(data.get('competences', []))
        data['competences'] = [c for c in data.get('competences', []) if c.get('code') != code]

        if len(data['competences']) == original_count:
            print(f"[WARN] Code non trouve: {code}")
            return False

        data['_last_modified'] = datetime.now().isoformat()
        save_json_file(json_path, data)
        print(f"[OK] Competence supprimee: {code}")
        return True

    except Exception as e:
        print(f"[ERREUR] {e}")
        return False


def update_competence_field(json_path: Path, code: str, field: str, value: str) -> bool:
    """
    Met a jour un champ specifique d'une competence.

    Args:
        json_path: Chemin vers le fichier JSON
        code: Code de la competence
        field: Nom du champ a modifier
        value: Nouvelle valeur (sera parsee comme JSON si possible)

    Returns:
        True si succes, False sinon
    """
    try:
        data = load_json_file(json_path)

        # Trouver la competence
        found = False
        for comp in data.get('competences', []):
            if comp.get('code') == code:
                # Parser la valeur si c'est du JSON
                try:
                    parsed_value = json.loads(value)
                except json.JSONDecodeError:
                    parsed_value = value

                old_value = comp.get(field)
                comp[field] = parsed_value
                found = True
                print(f"[OK] {code}.{field}: {old_value} -> {parsed_value}")
                break

        if not found:
            print(f"[ERREUR] Code non trouve: {code}")
            return False

        data['_last_modified'] = datetime.now().isoformat()
        save_json_file(json_path, data)
        return True

    except Exception as e:
        print(f"[ERREUR] {e}")
        return False


def get_competence(json_path: Path, code: str) -> Optional[dict]:
    """
    Recupere une competence par son code.

    Args:
        json_path: Chemin vers le fichier JSON
        code: Code de la competence

    Returns:
        La competence ou None
    """
    try:
        data = load_json_file(json_path)

        for comp in data.get('competences', []):
            if comp.get('code') == code:
                print(json.dumps(comp, ensure_ascii=False, indent=2))
                return comp

        print(f"[WARN] Code non trouve: {code}")
        return None

    except Exception as e:
        print(f"[ERREUR] {e}")
        return None


def list_codes(json_path: Path) -> list:
    """
    Liste tous les codes de competences d'un fichier.

    Args:
        json_path: Chemin vers le fichier JSON

    Returns:
        Liste des codes
    """
    try:
        data = load_json_file(json_path)
        codes = [c.get('code') for c in data.get('competences', []) if c.get('code')]

        print(f"[INFO] {len(codes)} competences dans {json_path.name}")
        for code in codes:
            print(f"  - {code}")

        return codes

    except Exception as e:
        print(f"[ERREUR] {e}")
        return []


def search_competences(json_path: Path, keyword: str) -> list:
    """
    Recherche des competences par mot-cle.

    Args:
        json_path: Chemin vers le fichier JSON
        keyword: Mot-cle a rechercher

    Returns:
        Liste des competences trouvees
    """
    try:
        data = load_json_file(json_path)
        keyword_lower = keyword.lower()

        results = []
        for comp in data.get('competences', []):
            # Chercher dans tous les champs texte
            searchable = ' '.join([
                str(comp.get('intitule', '')),
                str(comp.get('description_detaillee', '')),
                str(comp.get('formulation_bo', '')),
                str(comp.get('fingerprint', ''))
            ]).lower()

            if keyword_lower in searchable:
                results.append(comp)

        print(f"[INFO] {len(results)} resultats pour '{keyword}'")
        for comp in results:
            print(f"  - {comp.get('code')}: {comp.get('intitule', '')[:60]}...")

        return results

    except Exception as e:
        print(f"[ERREUR] {e}")
        return []


def validate_json(json_path: Path) -> dict:
    """
    Valide la structure d'un fichier JSON de competences.

    Args:
        json_path: Chemin vers le fichier JSON

    Returns:
        Rapport de validation
    """
    required_fields = ['code', 'intitule', 'domaine', 'type']
    optional_fields = ['fingerprint', 'sous_domaine', 'description_detaillee',
                       'formulation_bo', 'connaissances_associees']

    try:
        data = load_json_file(json_path)

        report = {
            'valid': True,
            'total': len(data.get('competences', [])),
            'errors': [],
            'warnings': []
        }

        for i, comp in enumerate(data.get('competences', [])):
            # Verifier champs requis
            for field in required_fields:
                if not comp.get(field):
                    report['errors'].append(f"Competence {i}: champ '{field}' manquant")
                    report['valid'] = False

            # Verifier code unique
            code = comp.get('code', '')
            if not re.match(r'^[A-Za-z0-9_-]+$', code):
                report['warnings'].append(f"Code suspect: {code}")

        # Afficher rapport
        status = "VALIDE" if report['valid'] else "INVALIDE"
        print(f"[{status}] {json_path.name}: {report['total']} competences")

        for err in report['errors'][:10]:
            print(f"  [ERREUR] {err}")
        for warn in report['warnings'][:10]:
            print(f"  [WARN] {warn}")

        return report

    except Exception as e:
        print(f"[ERREUR] {e}")
        return {'valid': False, 'errors': [str(e)]}


def resolve_path(path_str: str) -> Path:
    """Resout un chemin (relatif au dossier extractions ou absolu)."""
    path = Path(path_str)

    if path.is_absolute():
        return path

    # Essayer dans extractions
    if (EXTRACTIONS_DIR / path_str).exists():
        return EXTRACTIONS_DIR / path_str

    # Essayer avec extension .json
    if (EXTRACTIONS_DIR / f"{path_str}.json").exists():
        return EXTRACTIONS_DIR / f"{path_str}.json"

    # Chercher dans les sous-dossiers
    for subdir in EXTRACTIONS_DIR.iterdir():
        if subdir.is_dir():
            candidate = subdir / path_str
            if candidate.exists():
                return candidate
            candidate = subdir / f"{path_str}.json"
            if candidate.exists():
                return candidate

    return path


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "insert" and len(sys.argv) >= 4:
        json_path = resolve_path(sys.argv[2])
        competence_json = sys.argv[3]
        insert_competence(json_path, competence_json)

    elif command == "delete" and len(sys.argv) >= 4:
        json_path = resolve_path(sys.argv[2])
        code = sys.argv[3]
        delete_competence(json_path, code)

    elif command == "update" and len(sys.argv) >= 6:
        json_path = resolve_path(sys.argv[2])
        code = sys.argv[3]
        field = sys.argv[4]
        value = sys.argv[5]
        update_competence_field(json_path, code, field, value)

    elif command == "get" and len(sys.argv) >= 4:
        json_path = resolve_path(sys.argv[2])
        code = sys.argv[3]
        get_competence(json_path, code)

    elif command == "list_codes" and len(sys.argv) >= 3:
        json_path = resolve_path(sys.argv[2])
        list_codes(json_path)

    elif command == "search" and len(sys.argv) >= 4:
        json_path = resolve_path(sys.argv[2])
        keyword = sys.argv[3]
        search_competences(json_path, keyword)

    elif command == "validate" and len(sys.argv) >= 3:
        json_path = resolve_path(sys.argv[2])
        validate_json(json_path)

    else:
        print(__doc__)


if __name__ == "__main__":
    main()
