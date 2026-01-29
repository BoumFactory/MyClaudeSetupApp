#!/usr/bin/env python3
"""
Script de verification de la couverture des programmes officiels.

Detecte les lacunes dans l'extraction des competences en verifiant :
- Presence des themes attendus par niveau
- Nombre minimum de competences par domaine
- Mots-cles essentiels du programme

Usage:
    python check_coverage.py              # Verification complete
    python check_coverage.py --niveau 2G  # Verification d'un niveau
    python check_coverage.py --fix        # Proposer corrections
"""

import sys
import io
import json
from pathlib import Path
from collections import defaultdict

# Forcer UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
NORMALIZED_DIR = DATA_DIR / "normalized"

# ============================================================
# THEMES ATTENDUS PAR NIVEAU
# ============================================================
# Format: {niveau: {domaine: [mots-cles essentiels, ...]}}
# Si un mot-cle n'apparait pas, c'est une lacune potentielle

EXPECTED_COVERAGE = {
    "6": {  # 6eme / Cycle 3
        "NOMBRES": ["fraction", "decimal", "divisibilite", "multiple", "quotient", "proportion"],
        "GEOMETRIE": ["triangle", "rectangle", "carre", "parallelogramme", "symetrie", "axiale", "aire", "perimetre"],
        "GRANDEURS": ["unite", "mesure", "longueur", "aire", "volume", "duree"],
        "ALGORITHMIQUE": ["scratch", "algorithme", "programme", "boucle"],
        "STATISTIQUES": ["moyenne", "effectif", "frequence", "diagramme"],
    },
    "5": {  # 5eme
        "NOMBRES": ["fraction", "relatif", "priorite", "calcul"],
        "ALGEBRE": ["expression", "egalite", "equation"],
        "GEOMETRIE": ["parallelogramme", "triangle", "symetrie", "centrale", "angle"],
        "GRANDEURS": ["proportionnalite", "echelle", "vitesse"],
        "STATISTIQUES": ["moyenne", "tableau", "diagramme"],
        "ALGORITHMIQUE": ["scratch", "variable", "boucle", "condition"],
    },
    "4": {  # 4eme
        "NOMBRES": ["puissance", "notation scientifique", "fraction", "relatif"],
        "ALGEBRE": ["equation", "expression", "developper", "factoriser"],
        "GEOMETRIE": ["thales", "pythagore", "triangle", "cercle", "translation"],
        "PROBABILITES": ["probabilite", "experience", "aleatoire", "issue"],
        "ALGORITHMIQUE": ["variable", "fonction", "boucle"],
    },
    "3": {  # 3eme
        "NOMBRES": ["racine", "puissance", "fraction", "arithmetique"],
        "ALGEBRE": ["equation", "inequation", "systeme", "factoriser", "developper", "identite remarquable"],
        "ANALYSE": ["fonction", "lineaire", "affine", "proportionnalite"],
        "GEOMETRIE": ["thales", "trigonometrie", "cosinus", "sinus", "homothethie"],
        "PROBABILITES": ["probabilite", "experience", "frequence"],
        "ALGORITHMIQUE": ["python", "fonction", "boucle", "condition"],
    },
    "2G": {  # 2nde GT
        "NOMBRES": ["ensemble", "intervalle", "valeur absolue", "racine"],
        "ALGEBRE": ["equation", "inequation", "polynome", "second degre", "identite remarquable"],
        "ANALYSE": ["fonction", "carre", "inverse", "variation", "extremum", "courbe"],
        "GEOMETRIE": ["vecteur", "coordonnees", "repere", "milieu", "distance", "colineaire"],
        "STATISTIQUES": ["ecart-type", "variance", "quartile", "mediane"],
        "PROBABILITES": ["probabilite", "arbre", "evenement"],
        "ALGORITHMIQUE": ["python", "fonction", "boucle", "condition", "liste"],
    },
    "1S": {  # 1ere Spe
        "ALGEBRE": ["polynome", "second degre", "discriminant", "racine"],
        "ANALYSE": ["suite", "derivee", "variation", "fonction", "exponentielle", "logarithme"],
        "GEOMETRIE": ["vecteur", "produit scalaire", "droite", "plan", "equation cartesienne"],
        "TRIGONOMETRIE": ["cosinus", "sinus", "cercle trigonometrique", "radian"],
        "PROBABILITES": ["variable aleatoire", "esperance", "variance", "loi binomiale", "independance"],
        "ALGORITHMIQUE": ["python", "liste", "fonction", "seuil"],
    },
    "0S": {  # Terminale Spe
        "ALGEBRE": ["combinatoire", "denombrement", "arrangement"],
        "ANALYSE": ["limite", "continuite", "derivee", "primitive", "integrale", "logarithme", "exponentielle", "convexite"],
        "GEOMETRIE": ["espace", "vecteur", "orthogonalite", "produit scalaire", "equation parametrique"],
        "PROBABILITES": ["loi normale", "densite", "intervalle de fluctuation", "estimation"],
        "ALGORITHMIQUE": ["python", "dichotomie", "methode de Newton", "simulation"],
    },
    "0E": {  # Terminale Expert
        "NOMBRES": ["divisibilite", "congruence", "PGCD", "bezout", "nombres premiers"],
        "ALGEBRE": ["matrice", "determinant", "systeme lineaire", "complexe"],
        "GEOMETRIE": ["similitude", "complexe", "barycentre"],
        "ANALYSE": ["equation differentielle"],
    },
}

# Nombre minimum de competences attendues par domaine
MIN_COMPETENCES_PER_DOMAIN = {
    "NOMBRES": 10,
    "ALGEBRE": 10,
    "ANALYSE": 15,
    "GEOMETRIE": 20,
    "GRANDEURS": 10,
    "STATISTIQUES": 5,
    "PROBABILITES": 10,
    "ALGORITHMIQUE": 10,
    "TRIGONOMETRIE": 5,
    "LOGIQUE": 5,
}


def load_all_competences():
    """Charge toutes les competences normalisees."""
    all_comps = []

    # Charger fichier par fichier (chaque fichier a une structure avec "competences")
    for json_file in NORMALIZED_DIR.glob("*_normalized.json"):
        if json_file.name == "all_normalized.json":
            continue
        if json_file.name == "code_mapping.json":
            continue

        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extraire les competences (structure: {"meta": ..., "competences": [...]})
            if isinstance(data, dict) and 'competences' in data:
                all_comps.extend(data['competences'])
            elif isinstance(data, list):
                all_comps.extend(data)
        except Exception as e:
            print(f"  Erreur lecture {json_file.name}: {e}")

    return all_comps


def group_by_niveau(competences):
    """Groupe les competences par niveau."""
    grouped = defaultdict(list)
    for comp in competences:
        niveau = comp.get('niveau', 'UNKNOWN')
        grouped[niveau].append(comp)
    return grouped


def search_keyword(competences, keyword):
    """Recherche un mot-cle dans les competences."""
    keyword_lower = keyword.lower()
    results = []
    for comp in competences:
        text = f"{comp.get('intitule', '')} {comp.get('description', '')} {comp.get('formulation_bo', '')}".lower()
        if keyword_lower in text:
            results.append(comp)
    return results


def check_niveau_coverage(niveau_code, competences, expected):
    """Verifie la couverture d'un niveau."""
    issues = []
    stats = {
        'niveau': niveau_code,
        'total_competences': len(competences),
        'domaines': defaultdict(int),
        'keywords_missing': [],
        'domains_low': [],
    }

    # Compter par domaine
    for comp in competences:
        domaine = comp.get('domaine_nom', comp.get('domaine', 'UNKNOWN'))
        stats['domaines'][domaine] += 1

    # Verifier les mots-cles attendus
    for domaine, keywords in expected.items():
        for kw in keywords:
            matches = search_keyword(competences, kw)
            if len(matches) == 0:
                stats['keywords_missing'].append({
                    'domaine': domaine,
                    'keyword': kw,
                    'count': 0
                })
                issues.append(f"[{niveau_code}] Mot-cle '{kw}' absent du domaine {domaine}")
            elif len(matches) < 2:
                issues.append(f"[{niveau_code}] Mot-cle '{kw}' sous-represente ({len(matches)} occurrence(s))")

    # Verifier le nombre minimum par domaine
    for domaine, count in stats['domaines'].items():
        min_expected = MIN_COMPETENCES_PER_DOMAIN.get(domaine, 5)
        if count < min_expected:
            stats['domains_low'].append({
                'domaine': domaine,
                'count': count,
                'expected': min_expected
            })
            issues.append(f"[{niveau_code}] Domaine {domaine} sous-represente: {count}/{min_expected}")

    # Verifier les domaines attendus mais absents
    for expected_domain in expected.keys():
        if expected_domain not in stats['domaines'] or stats['domaines'][expected_domain] == 0:
            issues.append(f"[{niveau_code}] Domaine {expected_domain} ABSENT ou VIDE")
            stats['domains_low'].append({
                'domaine': expected_domain,
                'count': 0,
                'expected': MIN_COMPETENCES_PER_DOMAIN.get(expected_domain, 5)
            })

    return stats, issues


def calculate_coverage_score(stats):
    """Calcule un score de couverture 0-100."""
    score = 100.0

    # Penalites pour mots-cles manquants
    score -= len(stats['keywords_missing']) * 5

    # Penalites pour domaines faibles
    for dom in stats['domains_low']:
        ratio = dom['count'] / dom['expected'] if dom['expected'] > 0 else 0
        score -= (1 - ratio) * 10

    return max(0, min(100, score))


def print_report(all_stats, all_issues):
    """Affiche le rapport de couverture."""
    print("=" * 70)
    print("RAPPORT DE COUVERTURE DES PROGRAMMES")
    print("=" * 70)

    for stats in all_stats:
        niveau = stats['niveau']
        score = calculate_coverage_score(stats)
        status = "OK" if score >= 80 else ("WARN" if score >= 50 else "CRITICAL")

        print(f"\n[{niveau}] Score: {score:.0f}% [{status}]")
        print(f"  Total competences: {stats['total_competences']}")

        if stats['domaines']:
            print("  Par domaine:")
            for dom, count in sorted(stats['domaines'].items()):
                expected = MIN_COMPETENCES_PER_DOMAIN.get(dom, 5)
                marker = "OK" if count >= expected else "LOW"
                print(f"    - {dom}: {count} [{marker}]")

        if stats['keywords_missing']:
            print(f"  Mots-cles manquants: {len(stats['keywords_missing'])}")
            for kw in stats['keywords_missing'][:5]:
                print(f"    - {kw['keyword']} ({kw['domaine']})")
            if len(stats['keywords_missing']) > 5:
                print(f"    ... et {len(stats['keywords_missing']) - 5} autres")

    # Resume des problemes critiques
    print("\n" + "=" * 70)
    print("PROBLEMES CRITIQUES")
    print("=" * 70)

    critical = [i for i in all_issues if "ABSENT" in i or "VIDE" in i]
    if critical:
        for issue in critical:
            print(f"  ! {issue}")
    else:
        print("  Aucun probleme critique detecte.")

    print("\n" + "=" * 70)
    print("RECOMMANDATIONS")
    print("=" * 70)

    recommendations = set()
    for stats in all_stats:
        for dom in stats['domains_low']:
            if dom['count'] == 0:
                recommendations.add(f"Re-extraire le domaine {dom['domaine']} pour {stats['niveau']}")
            elif dom['count'] < dom['expected'] // 2:
                recommendations.add(f"Completer le domaine {dom['domaine']} pour {stats['niveau']}")

    if recommendations:
        for rec in sorted(recommendations):
            print(f"  -> {rec}")
    else:
        print("  Aucune recommandation particuliere.")


def main():
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(__doc__)
        return

    # Charger les competences
    print("Chargement des competences...", end=" ", flush=True)
    competences = load_all_competences()
    print(f"OK ({len(competences)} competences)")

    # Grouper par niveau
    by_niveau = group_by_niveau(competences)

    # Filtrer par niveau si demande
    niveau_filter = None
    for i, arg in enumerate(args):
        if arg == "--niveau" and i + 1 < len(args):
            niveau_filter = args[i + 1]

    # Verifier chaque niveau
    all_stats = []
    all_issues = []

    for niveau_code, expected in EXPECTED_COVERAGE.items():
        if niveau_filter and niveau_code != niveau_filter:
            continue

        # Trouver les competences de ce niveau
        niveau_comps = by_niveau.get(niveau_code, [])

        # Aussi chercher avec les anciens codes
        old_mappings = {
            "6": ["C3", "6E"],
            "5": ["5E"],
            "4": ["4E"],
            "3": ["3E"],
            "2G": ["2GT"],
            "2H": ["2STHR"],
            "1S": ["1SPE"],
            "1T": ["1TECHNO"],
            "1E": ["1ENS_SCI", "1ENS_SCI_V2"],
            "0S": ["TSPE", "TSPE_V2"],
            "0C": ["TCOMP"],
            "0E": ["TEXP"],
            "0T": ["TTECHNO"],
        }

        for old_code in old_mappings.get(niveau_code, []):
            niveau_comps.extend(by_niveau.get(old_code, []))

        stats, issues = check_niveau_coverage(niveau_code, niveau_comps, expected)
        all_stats.append(stats)
        all_issues.extend(issues)

    print_report(all_stats, all_issues)

    # Sauvegarder le rapport
    report = {
        'stats': [{k: dict(v) if isinstance(v, defaultdict) else v for k, v in s.items()} for s in all_stats],
        'issues': all_issues,
        'total_issues': len(all_issues)
    }

    report_path = DATA_DIR / "coverage_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\nRapport sauvegarde: {report_path}")


if __name__ == "__main__":
    main()
