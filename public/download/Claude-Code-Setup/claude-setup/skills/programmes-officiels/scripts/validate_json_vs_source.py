#!/usr/bin/env python3
"""
Valide que les competences extraites (JSON) correspondent au texte source (BO).

Approche BIDIRECTIONNELLE :
- Extrait les mots-cles du JSON (competence)
- Extrait les mots-cles du BO (page source)
- Compare l'intersection des deux ensembles

Usage:
    python validate_json_vs_source.py                    # Valide tout
    python validate_json_vs_source.py 1GT                # Valide un niveau
    python validate_json_vs_source.py --report           # Genere rapport detaille
    python validate_json_vs_source.py --verbose          # Affiche details

Seuils:
- OK: intersection >= 50% des mots-cles JSON
- WARN: intersection >= 30%
- ERROR: intersection < 30%
"""

import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
import unicodedata

# Forcer UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
PAGES_DIR = DATA_DIR / "pages"
EXTRACTIONS_DIR = DATA_DIR / "extractions"

# Mots vides francais (a ignorer)
STOPWORDS = {
    # Articles et determinants
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'a', 'au', 'aux',
    # Conjonctions
    'et', 'ou', 'mais', 'donc', 'or', 'ni', 'car', 'que', 'qui', 'quoi',
    # Prepositions
    'dans', 'sur', 'sous', 'avec', 'sans', 'pour', 'par', 'en', 'vers',
    # Pronoms
    'ce', 'cette', 'ces', 'son', 'sa', 'ses', 'leur', 'leurs', 'il', 'elle',
    # Verbes communs
    'est', 'sont', 'etre', 'avoir', 'fait', 'faire', 'peut', 'doit', 'etre',
    # Adverbes/quantificateurs
    'plus', 'moins', 'tres', 'bien', 'tout', 'tous', 'toute', 'toutes',
    'autre', 'autres', 'meme', 'aussi', 'comme', 'entre', 'depuis',
    # Mots generiques supplementaires (recommandation agent)
    'plusieurs', 'ayant', 'dont', 'lorsque', 'puis', 'chaque', 'differents',
    'cas', 'deux', 'trois', 'premier', 'premiere', 'second', 'seconde',
    'partir', 'utilisant', 'permettant', 'notamment', 'ainsi', 'lors',
    'eleve', 'eleves', 'niveau', 'classe', 'attendu', 'attendus',
    'capacite', 'capacites', 'competence', 'competences', 'savoir', 'savoirs'
}

# Seuils de validation (ajustes selon recommandations)
THRESHOLD_OK = 0.50      # >= 50% intersection = OK
THRESHOLD_WARN = 0.30    # >= 30% = Warning, < 30% = Erreur
MIN_KEYWORDS = 3         # Minimum de mots-cles pour valider


def normalize_text(text: str) -> str:
    """Normalise le texte : enleve accents, lowercase."""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower()


def extract_keywords_from_text(text: str, min_length: int = 4) -> set:
    """
    Extrait les mots-cles significatifs d'un texte.

    Filtre: mots < min_length caracteres, stopwords, chiffres
    """
    if not text:
        return set()

    normalized = normalize_text(text)
    words = re.findall(r'[a-z]+', normalized)

    keywords = set()
    for word in words:
        if len(word) >= min_length and word not in STOPWORDS:
            keywords.add(word)

    return keywords


def extract_keywords_from_competence(competence: dict) -> set:
    """
    Extrait les mots-cles d'une competence JSON.
    Combine: intitule + fingerprint + sous_domaine + description
    """
    text_parts = [
        competence.get('intitule', ''),
        competence.get('fingerprint', '').replace('_', ' '),
        competence.get('sous_domaine', ''),
        competence.get('description_detaillee', ''),
        competence.get('formulation_bo', '')
    ]

    full_text = ' '.join(text_parts)
    return extract_keywords_from_text(full_text)


def compute_keyword_overlap(json_keywords: set, source_keywords: set) -> dict:
    """
    Calcule le recouvrement entre mots-cles JSON et source BO.

    Returns:
        {
            'intersection': set,
            'json_only': set,
            'source_only': set,
            'ratio_json': float,  # % des mots JSON trouves dans source
            'ratio_source': float,  # % des mots source trouves dans JSON
            'ratio_combined': float,  # moyenne des deux
            'status': str
        }
    """
    if not json_keywords:
        return {
            'intersection': set(),
            'json_only': set(),
            'source_only': source_keywords,
            'ratio_json': 1.0,
            'ratio_source': 0.0,
            'ratio_combined': 0.5,
            'status': 'OK'
        }

    intersection = json_keywords & source_keywords
    json_only = json_keywords - source_keywords
    source_only = source_keywords - json_keywords

    # Ratio principal: combien de mots-cles JSON sont dans la source
    ratio_json = len(intersection) / len(json_keywords) if json_keywords else 1.0

    # Ratio secondaire: combien de mots-cles source sont dans JSON
    ratio_source = len(intersection) / len(source_keywords) if source_keywords else 1.0

    # Ratio combine (moyenne ponderee, plus de poids sur ratio_json)
    ratio_combined = 0.7 * ratio_json + 0.3 * ratio_source

    # Determiner le statut
    if ratio_json >= THRESHOLD_OK:
        status = 'OK'
    elif ratio_json >= THRESHOLD_WARN:
        status = 'WARN'
    else:
        status = 'ERROR'

    return {
        'intersection': intersection,
        'json_only': json_only,
        'source_only': source_only,
        'ratio_json': round(ratio_json, 2),
        'ratio_source': round(ratio_source, 2),
        'ratio_combined': round(ratio_combined, 2),
        'status': status
    }


def load_page_text(level: str, page_num: int) -> str:
    """Charge le texte d'une page source."""
    page_file = PAGES_DIR / level / f"page_{page_num:03d}.txt"
    if page_file.exists():
        with open(page_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def load_extraction_json(extraction_path: Path) -> dict:
    """Charge un fichier JSON d'extraction."""
    with open(extraction_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_extraction_file(extraction_path: Path, verbose: bool = False) -> dict:
    """
    Valide un fichier JSON d'extraction contre sa source.
    """
    report = {
        'file': extraction_path.name,
        'competences_checked': 0,
        'ok': 0,
        'warnings': 0,
        'errors': 0,
        'details': []
    }

    try:
        data = load_extraction_json(extraction_path)
    except Exception as e:
        report['errors'] = 1
        report['details'].append({'error': f"Erreur lecture JSON: {e}"})
        return report

    # Determiner la page
    source_info = data.get('source', {})
    page_num = source_info.get('page', 0)

    # Charger le texte source
    level_folder = extraction_path.parent.name
    source_text = load_page_text(level_folder, page_num)

    if not source_text:
        report['details'].append({
            'warning': f"Page source non trouvee: {level_folder}/page_{page_num:03d}.txt"
        })
        return report

    # Extraire mots-cles du BO (une seule fois par page)
    source_keywords = extract_keywords_from_text(source_text)

    # Valider chaque competence
    for comp in data.get('competences', []):
        report['competences_checked'] += 1
        code = comp.get('code', 'UNKNOWN')

        # Extraire mots-cles de la competence
        json_keywords = extract_keywords_from_competence(comp)

        # Calculer le recouvrement
        overlap = compute_keyword_overlap(json_keywords, source_keywords)

        if overlap['status'] == 'OK':
            report['ok'] += 1
        elif overlap['status'] == 'WARN':
            report['warnings'] += 1
            if verbose:
                report['details'].append({
                    'code': code,
                    'status': 'WARN',
                    'ratio': overlap['ratio_json'],
                    'intersection': len(overlap['intersection']),
                    'json_total': len(json_keywords),
                    'missing': list(overlap['json_only'])[:5]
                })
        else:  # ERROR
            report['errors'] += 1
            report['details'].append({
                'code': code,
                'status': 'ERROR',
                'ratio': overlap['ratio_json'],
                'intersection': len(overlap['intersection']),
                'json_total': len(json_keywords),
                'missing': list(overlap['json_only'])[:5],
                'intitule': comp.get('intitule', '')[:60]
            })

    return report


def validate_level(level_name: str, verbose: bool = False) -> dict:
    """Valide toutes les extractions d'un niveau."""
    level_dir = EXTRACTIONS_DIR / level_name

    if not level_dir.exists():
        return {'level': level_name, 'error': 'Dossier non trouve'}

    report = {
        'level': level_name,
        'files_checked': 0,
        'total_competences': 0,
        'total_ok': 0,
        'total_warnings': 0,
        'total_errors': 0,
        'error_details': []
    }

    for json_file in sorted(level_dir.glob("page_*_competences.json")):
        file_report = validate_extraction_file(json_file, verbose)
        report['files_checked'] += 1
        report['total_competences'] += file_report['competences_checked']
        report['total_ok'] += file_report['ok']
        report['total_warnings'] += file_report['warnings']
        report['total_errors'] += file_report['errors']

        # Collecter les erreurs
        for detail in file_report.get('details', []):
            if detail.get('status') == 'ERROR':
                detail['file'] = file_report['file']
                report['error_details'].append(detail)

    return report


def validate_all(verbose: bool = False) -> list:
    """Valide toutes les extractions."""
    results = []

    for level_dir in sorted(EXTRACTIONS_DIR.iterdir()):
        if level_dir.is_dir():
            print(f"Validation de {level_dir.name}...", end=" ", flush=True)
            report = validate_level(level_dir.name, verbose)
            results.append(report)

            if report.get('error'):
                print(f"[ERREUR] {report['error']}")
            else:
                total = report['total_competences']
                ok = report['total_ok']
                warn = report['total_warnings']
                err = report['total_errors']

                if err == 0 and warn == 0:
                    print(f"[OK] {total} competences valides")
                elif err == 0:
                    print(f"[OK] {ok} OK, {warn} warnings")
                else:
                    print(f"[WARN] {ok} OK, {warn} warn, {err} erreurs")

    return results


def print_summary(results: list):
    """Affiche un resume des validations."""
    print("\n" + "=" * 70)
    print("VALIDATION BIDIRECTIONNELLE - Intersection mots-cles JSON/BO")
    print("=" * 70)
    print(f"Seuils: OK >= {THRESHOLD_OK*100:.0f}% | Warn >= {THRESHOLD_WARN*100:.0f}% | Erreur < {THRESHOLD_WARN*100:.0f}%")
    print()

    total_competences = 0
    total_ok = 0
    total_warnings = 0
    total_errors = 0
    all_errors = []

    for report in results:
        if 'error' in report:
            continue

        total_competences += report['total_competences']
        total_ok += report['total_ok']
        total_warnings += report['total_warnings']
        total_errors += report['total_errors']
        all_errors.extend(report.get('error_details', []))

        # Calculer pourcentage OK
        total = report['total_competences']
        if total > 0:
            pct_ok = 100 * report['total_ok'] / total
        else:
            pct_ok = 100

        # Status
        if report['total_errors'] == 0:
            status = "OK"
        elif report['total_errors'] <= 3:
            status = "GOOD"
        else:
            status = "WARN"

        print(f"{report['level']:40} [{status}] {pct_ok:5.1f}% OK")

        if report['total_errors'] > 0 or report['total_warnings'] > 0:
            print(f"  Competences: {total:4} | OK: {report['total_ok']:4} | "
                  f"Warn: {report['total_warnings']:3} | Err: {report['total_errors']:3}")

    print("\n" + "=" * 70)
    print("RESUME GLOBAL")
    print("=" * 70)

    if total_competences > 0:
        pct_ok = 100 * total_ok / total_competences
        pct_warn = 100 * total_warnings / total_competences
        pct_err = 100 * total_errors / total_competences

        print(f"Total competences: {total_competences}")
        print(f"  OK:       {total_ok:5} ({pct_ok:.1f}%)")
        print(f"  Warnings: {total_warnings:5} ({pct_warn:.1f}%)")
        print(f"  Erreurs:  {total_errors:5} ({pct_err:.1f}%)")

        if pct_ok >= 95:
            print("\n[EXCELLENT] Base tres coherente avec les sources BO.")
        elif pct_ok >= 85:
            print("\n[BON] Base coherente, quelques competences a verifier.")
        else:
            print("\n[ATTENTION] Verification manuelle recommandee.")

    # Afficher les erreurs critiques
    if all_errors:
        print("\n" + "-" * 70)
        print(f"ERREURS A VERIFIER ({len(all_errors)} competences):")
        print("-" * 70)
        for err in all_errors[:15]:
            ratio_pct = int(err.get('ratio', 0) * 100)
            inter = err.get('intersection', 0)
            total = err.get('json_total', 0)
            missing = ', '.join(err.get('missing', [])[:3])
            print(f"  [{err.get('code')}] {ratio_pct}% ({inter}/{total}) - manquants: {missing}")

        if len(all_errors) > 15:
            print(f"  ... et {len(all_errors) - 15} autres")


def generate_report_file(results: list, output_path: Path):
    """Genere un rapport JSON detaille."""
    all_errors = []
    for r in results:
        all_errors.extend(r.get('error_details', []))

    report = {
        'generated_at': datetime.now().isoformat(),
        'method': 'bidirectional_keywords',
        'thresholds': {'ok': THRESHOLD_OK, 'warn': THRESHOLD_WARN},
        'summary': {
            'total_levels': len(results),
            'total_competences': sum(r.get('total_competences', 0) for r in results),
            'total_ok': sum(r.get('total_ok', 0) for r in results),
            'total_warnings': sum(r.get('total_warnings', 0) for r in results),
            'total_errors': sum(r.get('total_errors', 0) for r in results)
        },
        'errors_to_review': all_errors,
        'levels': results
    }

    # Nettoyer les sets pour JSON
    for level in report['levels']:
        if 'error_details' in level:
            del level['error_details']

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nRapport sauvegarde: {output_path}")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    generate_report = "--report" in args
    verbose = "--verbose" in args or "-v" in args

    # Nettoyer args
    args = [a for a in args if not a.startswith('-')]

    if args:
        # Valider un niveau specifique
        level_name = args[0]
        print(f"Validation de {level_name}...\n")
        report = validate_level(level_name, verbose)
        print_summary([report])
    else:
        # Valider tout
        print("Validation BIDIRECTIONNELLE (intersection JSON/BO)...\n")
        results = validate_all(verbose)
        print_summary(results)

        if generate_report:
            report_path = DATA_DIR / "validation_report.json"
            generate_report_file(results, report_path)


if __name__ == "__main__":
    main()
