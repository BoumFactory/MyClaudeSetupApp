#!/usr/bin/env python3
"""
Script de verification de la qualite d'extraction des pages PDF.

Detecte les problemes d'encodage, symboles manquants, texte corrompu.

Usage:
    python verify_extraction_quality.py                    # Verifie toutes les pages
    python verify_extraction_quality.py 1GT                # Verifie un PDF specifique
    python verify_extraction_quality.py --report           # Genere un rapport detaille
"""

import sys
import io
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

# Forcer l'encodage UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Chemins
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
PAGES_DIR = DATA_DIR / "pages"

# Patterns suspects a detecter
SUSPECT_PATTERNS = [
    # Caracteres de remplacement/corrompus
    (r'[�□■]', 'caractere_remplacement'),
    (r'[\x00-\x08\x0b\x0c\x0e-\x1f]', 'caractere_controle'),

    # Sequences bizarres (doublons de lettres suspects)
    (r'([a-z])\1{3,}', 'repetition_lettre'),  # aaaa, bbbb...
    (r'vv(?![aeiouy])', 'double_v_suspect'),  # vv non suivi de voyelle

    # Symboles mathematiques potentiellement mal extraits
    (r'(?<=[a-zA-Z])2(?=\s|$|[,\.])', 'exposant_2_suspect'),  # x2 au lieu de x²
    (r'(?<=[a-zA-Z])3(?=\s|$|[,\.])', 'exposant_3_suspect'),  # x3 au lieu de x³
    (r'(?<=[a-zA-Z])n(?=\s|$|[,\.])', 'exposant_n_suspect'),  # xn potentiel

    # Formules mathematiques potentiellement corrompues
    (r'[A-Z]{2,4}(?:\s*[A-Z]{2,4})+(?=\s*[=<>0])', 'formule_vecteurs_suspect'),  # MAMB = 0

    # Ligatures et caracteres speciaux
    (r'ﬁ|ﬂ|ﬀ|ﬃ|ﬄ', 'ligature_detectee'),  # Ligatures PDF

    # Tirets et espaces suspects
    (r'- (?=[a-z])', 'tiret_espace_mot_coupe'),  # Mot coupe en fin de ligne
    (r'\s{3,}', 'espaces_multiples'),  # Trop d'espaces
]

# Mots-cles mathematiques attendus (pour verifier la qualite)
MATH_KEYWORDS = [
    'fonction', 'equation', 'derivee', 'integrale', 'limite', 'suite',
    'vecteur', 'droite', 'cercle', 'angle', 'triangle',
    'probabilite', 'variable', 'aleatoire', 'esperance',
    'algorithme', 'python', 'boucle',
    'theoreme', 'demonstration', 'propriete', 'definition'
]


def analyze_text_quality(text: str, filename: str) -> dict:
    """Analyse la qualite d'un texte extrait."""
    issues = []
    stats = {
        'length': len(text),
        'lines': text.count('\n') + 1,
        'words': len(text.split()),
        'math_keywords_found': 0
    }

    # Detecter les patterns suspects
    for pattern, issue_type in SUSPECT_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches[:5]:  # Limiter a 5 exemples
                context_start = max(0, text.find(match if isinstance(match, str) else match) - 20)
                context_end = min(len(text), context_start + 60)
                context = text[context_start:context_end].replace('\n', ' ')

                issues.append({
                    'type': issue_type,
                    'match': match if isinstance(match, str) else str(match),
                    'context': f"...{context}..."
                })

    # Compter les mots-cles mathematiques
    text_lower = text.lower()
    for kw in MATH_KEYWORDS:
        if kw in text_lower:
            stats['math_keywords_found'] += 1

    # Detecter le texte trop court (page presque vide)
    if stats['length'] < 100:
        issues.append({
            'type': 'page_quasi_vide',
            'match': f"{stats['length']} caracteres",
            'context': text[:50]
        })

    # Detecter les ratios suspects
    if stats['words'] > 0:
        avg_word_length = stats['length'] / stats['words']
        if avg_word_length > 15:  # Mots anormalement longs
            issues.append({
                'type': 'mots_anormalement_longs',
                'match': f"moyenne: {avg_word_length:.1f} car/mot",
                'context': ""
            })

    return {
        'filename': filename,
        'stats': stats,
        'issues': issues,
        'quality_score': calculate_quality_score(stats, issues)
    }


def calculate_quality_score(stats: dict, issues: list) -> float:
    """Calcule un score de qualite de 0 a 100."""
    score = 100.0

    # Penalites par type de probleme
    penalties = {
        'caractere_remplacement': 10,
        'caractere_controle': 5,
        'repetition_lettre': 3,
        'double_v_suspect': 2,
        'exposant_2_suspect': 1,  # Faible car frequent et interpretable
        'exposant_3_suspect': 1,
        'exposant_n_suspect': 1,
        'formule_vecteurs_suspect': 2,
        'ligature_detectee': 1,
        'tiret_espace_mot_coupe': 1,
        'espaces_multiples': 1,
        'page_quasi_vide': 20,
        'mots_anormalement_longs': 5
    }

    issue_counts = Counter(issue['type'] for issue in issues)

    for issue_type, count in issue_counts.items():
        penalty = penalties.get(issue_type, 2) * min(count, 5)  # Cap a 5 occurrences
        score -= penalty

    # Bonus pour mots-cles mathematiques trouves
    score += min(stats.get('math_keywords_found', 0) * 2, 10)

    return max(0, min(100, score))


def verify_pdf_folder(folder_path: Path) -> dict:
    """Verifie toutes les pages d'un dossier PDF."""
    results = {
        'folder': folder_path.name,
        'pages': [],
        'summary': {
            'total_pages': 0,
            'good_quality': 0,  # score >= 80
            'medium_quality': 0,  # 50 <= score < 80
            'low_quality': 0,  # score < 50
            'common_issues': Counter()
        }
    }

    for txt_file in sorted(folder_path.glob("page_*.txt")):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            text = f"[ERREUR LECTURE: {e}]"

        analysis = analyze_text_quality(text, txt_file.name)
        results['pages'].append(analysis)
        results['summary']['total_pages'] += 1

        # Classifier par qualite
        score = analysis['quality_score']
        if score >= 80:
            results['summary']['good_quality'] += 1
        elif score >= 50:
            results['summary']['medium_quality'] += 1
        else:
            results['summary']['low_quality'] += 1

        # Compter les types de problemes
        for issue in analysis['issues']:
            results['summary']['common_issues'][issue['type']] += 1

    return results


def print_summary(results: list[dict]):
    """Affiche un resume des resultats."""
    print("=" * 70)
    print("RAPPORT DE QUALITE D'EXTRACTION")
    print("=" * 70)

    total_pages = 0
    total_good = 0
    total_medium = 0
    total_low = 0
    all_issues = Counter()

    for result in results:
        summary = result['summary']
        total_pages += summary['total_pages']
        total_good += summary['good_quality']
        total_medium += summary['medium_quality']
        total_low += summary['low_quality']
        all_issues.update(summary['common_issues'])

        # Affichage par PDF
        pct_good = 100 * summary['good_quality'] / summary['total_pages'] if summary['total_pages'] > 0 else 0
        status = "OK" if pct_good >= 80 else ("WARN" if pct_good >= 50 else "ATTENTION")

        print(f"\n{result['folder']:40} [{status}]")
        print(f"  Pages: {summary['total_pages']:3} | "
              f"Bonne: {summary['good_quality']:3} | "
              f"Moyenne: {summary['medium_quality']:3} | "
              f"Faible: {summary['low_quality']:3}")

        if summary['common_issues']:
            top_issues = summary['common_issues'].most_common(3)
            issues_str = ", ".join(f"{t}: {c}" for t, c in top_issues)
            print(f"  Problemes: {issues_str}")

    print("\n" + "=" * 70)
    print("RESUME GLOBAL")
    print("=" * 70)
    print(f"Total pages analysees: {total_pages}")
    print(f"  - Bonne qualite (>=80):  {total_good:3} ({100*total_good/total_pages:.1f}%)")
    print(f"  - Qualite moyenne:       {total_medium:3} ({100*total_medium/total_pages:.1f}%)")
    print(f"  - Qualite faible (<50):  {total_low:3} ({100*total_low/total_pages:.1f}%)")

    print("\nProblemes les plus frequents:")
    for issue_type, count in all_issues.most_common(10):
        print(f"  - {issue_type}: {count} occurrences")


def generate_report(results: list[dict], output_path: Path):
    """Genere un rapport JSON detaille."""
    report = {
        'generated_at': datetime.now().isoformat(),
        'total_pdfs': len(results),
        'results': results
    }

    # Convertir Counter en dict pour JSON
    for result in report['results']:
        result['summary']['common_issues'] = dict(result['summary']['common_issues'])

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nRapport sauvegarde: {output_path}")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    generate_detailed_report = "--report" in args
    if generate_detailed_report:
        args.remove("--report")

    # Determiner quels dossiers analyser
    if args:
        folders = [PAGES_DIR / args[0]]
        if not folders[0].exists():
            print(f"Dossier non trouve: {folders[0]}")
            return
    else:
        folders = [f for f in PAGES_DIR.iterdir() if f.is_dir()]

    print(f"Analyse de {len(folders)} dossier(s)...\n")

    results = []
    for folder in sorted(folders):
        print(f"Analyse de {folder.name}...", end=" ", flush=True)
        result = verify_pdf_folder(folder)
        results.append(result)
        print(f"OK ({result['summary']['total_pages']} pages)")

    print_summary(results)

    if generate_detailed_report:
        report_path = DATA_DIR / "quality_report.json"
        generate_report(results, report_path)


if __name__ == "__main__":
    main()
