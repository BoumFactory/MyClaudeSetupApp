#!/usr/bin/env python3
"""
Compare deux versions d'un programme (ancien vs nouveau).

Identifie les pages modifiees et genere un rapport des differences.
Ce script prepare le travail pour l'agent qui fera l'analyse semantique.

Usage:
    python compare_programs.py <ancien_dossier> <nouveau_dossier>
    python compare_programs.py <ancien_dossier> <nouveau_dossier> --html
    python compare_programs.py <ancien_dossier> <nouveau_dossier> --json

Exemple:
    python compare_programs.py 16-Maths-4e-attendus-eduscol_1114746 nouveau_4e

Le script compare page par page le texte extrait et identifie:
- Pages identiques (aucune action requise)
- Pages modifiees (re-extraction necessaire)
- Pages ajoutees (nouvelle extraction necessaire)
- Pages supprimees (suppression des competences associees)
"""

import sys
import io
import json
import difflib
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
PAGES_DIR = DATA_DIR / "pages"
NOUVEAUX_DIR = SKILL_DIR / "nouveaux_programmes"
REPORTS_DIR = DATA_DIR / "update_reports"


def normalize_text(text: str) -> str:
    """Normalise le texte pour comparaison (enleve espaces, lowercase)."""
    import re
    # Enlever espaces multiples
    text = re.sub(r'\s+', ' ', text)
    # Enlever accents pour comparaison robuste
    text = text.lower().strip()
    return text


def compute_similarity(text1: str, text2: str) -> float:
    """Calcule le ratio de similarite entre deux textes (0-1)."""
    if not text1 and not text2:
        return 1.0
    if not text1 or not text2:
        return 0.0

    norm1 = normalize_text(text1)
    norm2 = normalize_text(text2)

    return difflib.SequenceMatcher(None, norm1, norm2).ratio()


def get_text_diff(text1: str, text2: str) -> list:
    """Genere un diff lisible entre deux textes."""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    differ = difflib.unified_diff(
        lines1, lines2,
        fromfile='ancien',
        tofile='nouveau',
        lineterm=''
    )

    return list(differ)


def load_page_text(folder: Path, page_num: int) -> Optional[str]:
    """Charge le texte d'une page."""
    txt_file = folder / f"page_{page_num:03d}.txt"
    if txt_file.exists():
        with open(txt_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def get_page_count(folder: Path) -> int:
    """Compte le nombre de pages dans un dossier."""
    return len(list(folder.glob("page_*.txt")))


def compare_programs(old_folder: Path, new_folder: Path) -> dict:
    """
    Compare deux versions d'un programme.

    Returns:
        Rapport de comparaison avec les actions a effectuer
    """
    report = {
        'comparison_date': datetime.now().isoformat(),
        'old_program': old_folder.name,
        'new_program': new_folder.name,
        'old_page_count': get_page_count(old_folder),
        'new_page_count': get_page_count(new_folder),
        'pages': {
            'identical': [],      # Aucune action
            'modified': [],       # Re-extraction necessaire
            'added': [],          # Nouvelle extraction
            'removed': []         # Suppression competences
        },
        'summary': {
            'total_changes': 0,
            'actions_required': []
        }
    }

    old_pages = set(range(1, report['old_page_count'] + 1))
    new_pages = set(range(1, report['new_page_count'] + 1))

    # Pages communes
    common_pages = old_pages & new_pages
    # Pages ajoutees
    added_pages = new_pages - old_pages
    # Pages supprimees
    removed_pages = old_pages - new_pages

    # Comparer les pages communes
    for page_num in sorted(common_pages):
        old_text = load_page_text(old_folder, page_num)
        new_text = load_page_text(new_folder, page_num)

        similarity = compute_similarity(old_text or '', new_text or '')

        if similarity > 0.95:  # Quasi identiques
            report['pages']['identical'].append({
                'page': page_num,
                'similarity': round(similarity, 3)
            })
        else:
            # Page modifiee
            diff = get_text_diff(old_text or '', new_text or '')
            report['pages']['modified'].append({
                'page': page_num,
                'similarity': round(similarity, 3),
                'diff_lines': len([l for l in diff if l.startswith('+') or l.startswith('-')]),
                'diff_preview': diff[:20]  # Premiers 20 lignes du diff
            })

    # Pages ajoutees
    for page_num in sorted(added_pages):
        new_text = load_page_text(new_folder, page_num)
        report['pages']['added'].append({
            'page': page_num,
            'text_length': len(new_text) if new_text else 0,
            'preview': (new_text or '')[:200]
        })

    # Pages supprimees
    for page_num in sorted(removed_pages):
        old_text = load_page_text(old_folder, page_num)
        report['pages']['removed'].append({
            'page': page_num,
            'text_length': len(old_text) if old_text else 0,
            'preview': (old_text or '')[:200]
        })

    # Calculer resume
    total_changes = (
        len(report['pages']['modified']) +
        len(report['pages']['added']) +
        len(report['pages']['removed'])
    )
    report['summary']['total_changes'] = total_changes

    # Actions requises
    if report['pages']['modified']:
        report['summary']['actions_required'].append({
            'action': 'RE_EXTRACT',
            'pages': [p['page'] for p in report['pages']['modified']],
            'description': f"Re-extraire {len(report['pages']['modified'])} pages modifiees"
        })

    if report['pages']['added']:
        report['summary']['actions_required'].append({
            'action': 'NEW_EXTRACT',
            'pages': [p['page'] for p in report['pages']['added']],
            'description': f"Extraire {len(report['pages']['added'])} nouvelles pages"
        })

    if report['pages']['removed']:
        report['summary']['actions_required'].append({
            'action': 'DELETE_COMPETENCES',
            'pages': [p['page'] for p in report['pages']['removed']],
            'description': f"Supprimer competences de {len(report['pages']['removed'])} pages"
        })

    return report


def generate_html_report(report: dict, output_path: Path):
    """Genere un rapport HTML visuel des differences."""
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Comparaison: {report['old_program']} vs {report['new_program']}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        h2 {{ color: #34495e; margin-top: 30px; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; }}
        .stat {{ display: inline-block; padding: 15px 25px; margin: 5px; border-radius: 5px; color: white; }}
        .stat.identical {{ background: #27ae60; }}
        .stat.modified {{ background: #e67e22; }}
        .stat.added {{ background: #3498db; }}
        .stat.removed {{ background: #e74c3c; }}
        .actions {{ background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .page-list {{ background: white; padding: 15px; border-radius: 5px; margin: 10px 0; }}
        .page-item {{ padding: 8px; border-bottom: 1px solid #eee; }}
        .page-item:hover {{ background: #f8f9fa; }}
        .diff {{ background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 5px; font-family: monospace; font-size: 12px; overflow-x: auto; }}
        .diff .add {{ color: #a6e22e; }}
        .diff .del {{ color: #f92672; }}
        .similarity {{ font-size: 0.8em; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #3498db; color: white; }}
    </style>
</head>
<body>
    <h1>Comparaison des programmes</h1>

    <div class="summary">
        <h2>Resume</h2>
        <p><strong>Ancien:</strong> {report['old_program']} ({report['old_page_count']} pages)</p>
        <p><strong>Nouveau:</strong> {report['new_program']} ({report['new_page_count']} pages)</p>
        <p><strong>Date:</strong> {report['comparison_date']}</p>

        <div>
            <span class="stat identical">{len(report['pages']['identical'])} identiques</span>
            <span class="stat modified">{len(report['pages']['modified'])} modifiees</span>
            <span class="stat added">{len(report['pages']['added'])} ajoutees</span>
            <span class="stat removed">{len(report['pages']['removed'])} supprimees</span>
        </div>
    </div>
"""

    # Actions requises
    if report['summary']['actions_required']:
        html += """
    <div class="actions">
        <h3>Actions requises</h3>
        <ul>
"""
        for action in report['summary']['actions_required']:
            pages_str = ', '.join(str(p) for p in action['pages'][:10])
            if len(action['pages']) > 10:
                pages_str += f" ... (+{len(action['pages'])-10})"
            html += f"            <li><strong>{action['action']}</strong>: {action['description']}<br><small>Pages: {pages_str}</small></li>\n"

        html += """        </ul>
    </div>
"""

    # Pages modifiees (detail)
    if report['pages']['modified']:
        html += """
    <h2>Pages modifiees (detail)</h2>
    <table>
        <tr><th>Page</th><th>Similarite</th><th>Lignes modifiees</th></tr>
"""
        for page in report['pages']['modified']:
            sim_pct = round(page['similarity'] * 100, 1)
            html += f"        <tr><td>Page {page['page']}</td><td>{sim_pct}%</td><td>{page['diff_lines']}</td></tr>\n"

        html += "    </table>\n"

    # Pages ajoutees
    if report['pages']['added']:
        html += """
    <h2>Pages ajoutees</h2>
    <div class="page-list">
"""
        for page in report['pages']['added']:
            preview = page['preview'].replace('<', '&lt;').replace('>', '&gt;')[:150]
            html += f"        <div class='page-item'><strong>Page {page['page']}</strong> ({page['text_length']} car.)<br><small>{preview}...</small></div>\n"

        html += "    </div>\n"

    # Pages supprimees
    if report['pages']['removed']:
        html += """
    <h2>Pages supprimees</h2>
    <div class="page-list">
"""
        for page in report['pages']['removed']:
            preview = page['preview'].replace('<', '&lt;').replace('>', '&gt;')[:150]
            html += f"        <div class='page-item'><strong>Page {page['page']}</strong> ({page['text_length']} car.)<br><small>{preview}...</small></div>\n"

        html += "    </div>\n"

    html += """
</body>
</html>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[OK] Rapport HTML genere: {output_path}")


def print_summary(report: dict):
    """Affiche un resume console."""
    print("=" * 60)
    print("COMPARAISON DES PROGRAMMES")
    print("=" * 60)
    print(f"Ancien: {report['old_program']} ({report['old_page_count']} pages)")
    print(f"Nouveau: {report['new_program']} ({report['new_page_count']} pages)")
    print()
    print(f"Pages identiques:  {len(report['pages']['identical']):3}")
    print(f"Pages modifiees:   {len(report['pages']['modified']):3}")
    print(f"Pages ajoutees:    {len(report['pages']['added']):3}")
    print(f"Pages supprimees:  {len(report['pages']['removed']):3}")
    print()

    if report['summary']['actions_required']:
        print("ACTIONS REQUISES:")
        for action in report['summary']['actions_required']:
            pages = ', '.join(str(p) for p in action['pages'][:5])
            if len(action['pages']) > 5:
                pages += f" ... (+{len(action['pages'])-5})"
            print(f"  [{action['action']}] {action['description']}")
            print(f"    Pages: {pages}")
    else:
        print("Aucune action requise - programmes identiques")

    print("=" * 60)


def resolve_folder(name: str) -> Path:
    """Resout le chemin d'un dossier de pages."""
    # Chemin absolu
    if Path(name).is_absolute():
        return Path(name)

    # Dans PAGES_DIR
    if (PAGES_DIR / name).exists():
        return PAGES_DIR / name

    # Dans NOUVEAUX_DIR
    if (NOUVEAUX_DIR / name).exists():
        return NOUVEAUX_DIR / name

    # Chercher par prefix
    for folder in PAGES_DIR.iterdir():
        if folder.is_dir() and name.lower() in folder.name.lower():
            return folder

    return Path(name)


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args or len(args) < 2:
        print(__doc__)
        return

    old_name = args[0]
    new_name = args[1]

    generate_html = "--html" in args
    generate_json = "--json" in args

    old_folder = resolve_folder(old_name)
    new_folder = resolve_folder(new_name)

    if not old_folder.exists():
        print(f"[ERREUR] Dossier ancien non trouve: {old_folder}")
        return

    if not new_folder.exists():
        print(f"[ERREUR] Dossier nouveau non trouve: {new_folder}")
        return

    print(f"Comparaison: {old_folder.name} vs {new_folder.name}")
    print()

    # Comparer
    report = compare_programs(old_folder, new_folder)

    # Afficher resume
    print_summary(report)

    # Sauvegarder rapport
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if generate_html or not generate_json:
        html_path = REPORTS_DIR / f"diff_{report['old_program']}_vs_{report['new_program']}_{timestamp}.html"
        generate_html_report(report, html_path)

    if generate_json:
        json_path = REPORTS_DIR / f"diff_{report['old_program']}_vs_{report['new_program']}_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"[OK] Rapport JSON genere: {json_path}")


if __name__ == "__main__":
    main()
