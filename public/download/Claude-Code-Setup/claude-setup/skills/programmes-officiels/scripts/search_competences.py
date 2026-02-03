#!/usr/bin/env python3
"""
Script de recherche de competences dans les programmes officiels.
Utilise les codes normalises: [niveau][filiere][theme][index]-[palier]

Usage:
    python search_competences.py --niveau 1S --keyword "suite"
    python search_competences.py --niveau 6 --domaine N
    python search_competences.py --keyword "pythagore" --all-levels
    python search_competences.py --code 1SY10
    python search_competences.py --stats
    python search_competences.py --list-niveaux
    python search_competences.py --list-domaines
"""

import json
import argparse
import sys
import io
from pathlib import Path
from typing import List, Dict, Optional
import unicodedata

# ============================================================================
# FORCER ENCODAGE UTF-8 POUR WINDOWS
# ============================================================================
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# CHEMINS
# ============================================================================
BASE_DIR = Path(__file__).parent.parent
NORMALIZED_DIR = BASE_DIR / "data" / "normalized"
AGGREGATED_DIR = BASE_DIR / "data" / "aggregated"

# ============================================================================
# SYNONYMES ET MOTS-CLES POUR AMELIORER LA RECHERCHE
# ============================================================================
SEARCH_SYNONYMS = {
    # Calcul numérique
    "fraction": ["fractions", "quotient", "numerateur", "denominateur", "rationnel"],
    "puissance": ["puissances", "exposant", "exposants", "10^", "a^n", "carré", "cube"],
    "racine": ["racines", "sqrt", "carree", "radical", "radicaux"],
    "notation scientifique": ["puissance de 10", "10^", "ecriture scientifique"],

    # Ensembles de nombres
    "ensemble": ["ensembles", "appartient", "appartenance", "inclusion"],
    "entier": ["entiers", "naturel", "naturels", "relatif", "relatifs", "N", "Z"],
    "decimal": ["decimaux", "D", "virgule"],
    "rationnel": ["rationnels", "Q", "fraction"],
    "reel": ["reels", "R", "irrationnel", "irrationnels"],

    # Calcul littéral
    "identite remarquable": ["identites remarquables", "(a+b)^2", "(a-b)^2", "a^2-b^2",
                             "carre parfait", "difference de carres", "developpement", "factorisation"],
    "developper": ["developpement", "distribuer", "distributivite"],
    "factoriser": ["factorisation", "facteur commun", "mettre en facteur"],
    "reduire": ["reduction", "simplifier", "simplification"],

    # Intervalles et valeur absolue
    "intervalle": ["intervalles", "borne", "bornes", "ouvert", "ferme", "semi-ouvert"],
    "intersection": ["inter", "cap", "et"],
    "reunion": ["union", "cup", "ou"],
    "valeur absolue": ["absolue", "|x|", "distance", "module"],
    "inegalite": ["inegalites", "inequation", "inequations", "superieur", "inferieur"],

    # Géométrie repérée
    "repere": ["reperes", "reperage", "orthonorme", "coordonnees", "abscisse", "ordonnee"],
    "coordonnee": ["coordonnees", "abscisse", "ordonnee", "repere", "point"],
    "milieu": ["milieux", "centre", "median", "mediane"],
    "distance": ["distances", "longueur", "longueurs", "norme", "ecart"],
    "vecteur": ["vecteurs", "vectoriel", "fleche", "translation", "composantes"],
    "parallelogramme": ["parallelogrammes", "diagonales", "quadrilatere"],
    "symetrique": ["symetrie", "symetral", "central", "axial"],

    # Fonctions
    "fonction": ["fonctions", "f(x)", "application", "image", "antecedent"],
    "affine": ["affines", "lineaire", "lineaires", "ax+b", "droite"],
    "carre": ["carree", "parabole", "x^2", "second degre"],

    # Statistiques et probabilités
    "moyenne": ["moyennes", "esperance"],
    "mediane": ["medianes", "quartile", "quartiles"],
    "ecart-type": ["ecart type", "variance", "dispersion"],
    "probabilite": ["probabilites", "proba", "chance", "aleatoire"],

    # Algorithmique
    "algorithme": ["algorithmes", "algo", "programme", "python", "boucle", "condition"],
    "boucle": ["boucles", "for", "while", "iteration", "repeter"],

    # Théorèmes
    "pythagore": ["pythagoricien", "hypotenuse", "triangle rectangle"],
    "thales": ["proportionnalite", "paralleles"],
}

# Mots-clés inversés (mot -> concepts associés)
KEYWORD_TO_CONCEPTS = {}
for concept, synonyms in SEARCH_SYNONYMS.items():
    KEYWORD_TO_CONCEPTS[concept.lower()] = concept
    for syn in synonyms:
        KEYWORD_TO_CONCEPTS[syn.lower()] = concept


# ============================================================================
# MAPPINGS NIVEAUX ET DOMAINES
# ============================================================================
NIVEAU_NAME_TO_CODE = {
    "C3": "6", "6E": "6", "6EME": "6",
    "5E": "5", "5EME": "5",
    "4E": "4", "4EME": "4",
    "3E": "3", "3EME": "3",
    "2GT": "2G", "2NDE": "2G", "SECONDE": "2G",
    "2STHR": "2H",
    "1SPE": "1S", "1ERE": "1S", "PREMIERE": "1S",
    "1TECHNO": "1T",
    "1ENS_SCI": "1E", "1ENS_SCI_V2": "1E",
    "TSPE": "0S", "TSPE_V2": "0S", "TERMINALE": "0S", "TERM": "0S",
    "TCOMP": "0C",
    "TEXP": "0E",
    "TTECHNO": "0T",
    "SPE_ANNEXE": "0X",
}

NIVEAU_CODE_TO_NAME = {
    "6": "6eme (C3)",
    "5": "5eme",
    "4": "4eme",
    "3": "3eme",
    "2G": "2nde GT",
    "2H": "2nde STHR",
    "1S": "1ere Spe",
    "1T": "1ere Techno",
    "1E": "1ere Ens.Sci",
    "0S": "Term. Spe",
    "0C": "Term. Comp",
    "0E": "Term. Expert",
    "0T": "Term. Techno",
    "0X": "Annexe Spe",
}

NIVEAU_CODE_TO_FILE = {
    "6": "C3",
    "5": "5E",
    "4": "4E",
    "3": "3E",
    "2G": "2GT",
    "2H": "2STHR",
    "1S": "1SPE",
    "1T": "1TECHNO",
    "1E": "1ENS_SCI",
    "0S": "TSPE",
    "0C": "TCOMP",
    "0E": "TEXP",
    "0T": "TTECHNO",
    "0X": "SPE_ANNEXE",
}

DOMAINE_NAME_TO_LETTER = {
    "NOMBRES": "N",
    "ALGEBRE": "A",
    "ANALYSE": "Y",
    "ALGORITHMIQUE": "L",
    "GEOMETRIE": "G",
    "GRANDEURS": "R",
    "STATISTIQUES": "S",
    "PROBABILITES": "P",
    "TRIGONOMETRIE": "T",
    "LOGIQUE": "O",
    "AUTRE": "X",
}

DOMAINE_LETTER_TO_NAME = {
    "N": "Nombres",
    "A": "Algebre",
    "Y": "Analyse",
    "L": "Algorithmique",
    "G": "Geometrie",
    "R": "Grandeurs",
    "S": "Statistiques",
    "P": "Probabilites",
    "T": "Trigonometrie",
    "O": "Logique",
    "X": "Autre",
}

ALL_NIVEAU_CODES = list(NIVEAU_CODE_TO_NAME.keys())


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================
def normalize_text(text: str) -> str:
    """Normalise le texte pour la recherche (accents, casse)."""
    # Enlever les accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower()


def expand_keywords(keyword: str) -> List[str]:
    """Etend un mot-cle avec ses synonymes."""
    keyword_lower = keyword.lower()
    keywords = [keyword_lower]

    # Chercher le concept associé
    concept = KEYWORD_TO_CONCEPTS.get(keyword_lower)
    if concept:
        # Ajouter le concept et tous ses synonymes
        keywords.append(concept.lower())
        keywords.extend([s.lower() for s in SEARCH_SYNONYMS.get(concept, [])])

    # Chercher aussi si le keyword est un concept lui-même
    if keyword_lower in SEARCH_SYNONYMS:
        keywords.extend([s.lower() for s in SEARCH_SYNONYMS[keyword_lower]])

    return list(set(keywords))


def normalize_niveau(niveau: str) -> str:
    """Convertit un niveau (nom ou code) en code normalise."""
    niveau_upper = niveau.upper()
    if niveau_upper in NIVEAU_CODE_TO_NAME:
        return niveau_upper
    return NIVEAU_NAME_TO_CODE.get(niveau_upper, niveau_upper)


def normalize_domaine(domaine: str) -> str:
    """Convertit un domaine (nom ou lettre) en lettre."""
    domaine_upper = domaine.upper()
    if domaine_upper in DOMAINE_LETTER_TO_NAME:
        return domaine_upper
    return DOMAINE_NAME_TO_LETTER.get(domaine_upper, domaine_upper)


# ============================================================================
# CHARGEMENT DES DONNEES
# ============================================================================
def load_normalized_competences(niveau_code: str) -> List[Dict]:
    """Charge les competences normalisees d'un niveau."""
    file_key = NIVEAU_CODE_TO_FILE.get(niveau_code)
    if not file_key:
        return []

    file_path = NORMALIZED_DIR / f"{file_key}_normalized.json"
    if not file_path.exists():
        return []

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("competences", [])


def load_all_competences() -> List[Dict]:
    """Charge toutes les competences normalisees."""
    all_file = NORMALIZED_DIR / "all_normalized.json"
    if not all_file.exists():
        return []

    with open(all_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("all_competences", [])


# ============================================================================
# RECHERCHE
# ============================================================================
def search_by_code(code: str) -> Optional[Dict]:
    """Recherche une competence par son code exact."""
    all_comps = load_all_competences()
    code_upper = code.upper()

    for comp in all_comps:
        if comp.get("code", "").upper() == code_upper:
            return comp
        if comp.get("old_code", "").upper() == code_upper:
            return comp

    return None


def search_keyword(competences: List[Dict], keyword: str, limit: int = 20, fuzzy: bool = True) -> List[Dict]:
    """
    Recherche par mot-cle dans les competences.
    Si fuzzy=True, utilise les synonymes pour elargir la recherche.
    """
    # Etendre les mots-cles avec synonymes
    if fuzzy:
        keywords = expand_keywords(keyword)
    else:
        keywords = [keyword.lower()]

    # Normaliser pour comparaison sans accents
    keywords_normalized = [normalize_text(k) for k in keywords]

    results = []
    seen_codes = set()

    for comp in competences:
        # Construire le texte cherchable
        searchable_parts = [
            comp.get("intitule", ""),
            comp.get("description_detaillee", ""),
            comp.get("formulation_bo", ""),
            comp.get("sous_domaine", ""),
            " ".join(comp.get("connaissances_associees", [])),
            " ".join(comp.get("keywords", [])),  # Nouveau champ keywords
        ]
        combined = " ".join(searchable_parts)
        combined_normalized = normalize_text(combined)

        # Chercher chaque mot-cle
        for kw in keywords_normalized:
            if kw in combined_normalized:
                code = comp.get("code", "")
                if code not in seen_codes:
                    results.append(comp)
                    seen_codes.add(code)
                break

        if len(results) >= limit:
            break

    return results


def filter_by_domaine(competences: List[Dict], domaine_letter: str) -> List[Dict]:
    """Filtre les competences par lettre de domaine."""
    return [c for c in competences if c.get("domaine_code", "") == domaine_letter]


# ============================================================================
# FORMATAGE
# ============================================================================
def safe_str(text: str) -> str:
    """Convertit un texte en ASCII safe pour affichage console."""
    if not text:
        return ""
    # Remplacer les caractères problématiques
    replacements = {
        'ℕ': 'N', 'ℤ': 'Z', 'ℚ': 'Q', 'ℝ': 'R', 'ℂ': 'C', '𝔻': 'D',
        '√': 'sqrt', '∞': 'inf', '≤': '<=', '≥': '>=', '≠': '!=',
        '×': 'x', '÷': '/', '±': '+/-', '∈': 'in', '∉': 'not in',
        '∩': 'inter', '∪': 'union', '⊂': 'subset', '⊃': 'supset',
        'π': 'pi', 'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
        '→': '->', '←': '<-', '↔': '<->',
        '⩽': '<=', '⩾': '>=',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def format_competence_short(comp: Dict) -> str:
    """Format court pour affichage console."""
    return f"[{comp.get('code', 'N/A')}] {safe_str(comp.get('intitule', 'N/A'))}"


def format_competence_medium(comp: Dict) -> str:
    """Format moyen avec description."""
    source = comp.get("source", {})
    source_str = f"{source.get('pdf', 'N/A')} p.{source.get('page', '?')}" if source else "N/A"
    lines = [
        f"Code: {comp.get('code', 'N/A')} (ancien: {comp.get('old_code', 'N/A')})",
        f"Intitule: {safe_str(comp.get('intitule', 'N/A'))}",
        f"Niveau: {comp.get('niveau', 'N/A')} ({comp.get('niveau_code', '?')})",
        f"Domaine: {comp.get('domaine', 'N/A')} ({comp.get('domaine_code', '?')})",
        f"Sous-domaine: {safe_str(comp.get('sous_domaine', 'N/A'))}",
        f"Type: {comp.get('type', 'N/A')}",
        f"Description: {safe_str(comp.get('description_detaillee', 'N/A'))}",
        f"Source: {source_str}"
    ]
    return "\n".join(lines)


def format_competence_json(comp: Dict) -> Dict:
    """Format JSON compact pour agents."""
    result = {
        "code": comp.get("code"),
        "old_code": comp.get("old_code"),
        "intitule": comp.get("intitule"),
        "niveau": comp.get("niveau_code"),
        "domaine": comp.get("domaine_code"),
        "domaine_nom": comp.get("domaine"),
        "sous_domaine": comp.get("sous_domaine"),
        "type": comp.get("type"),
        "description": comp.get("description_detaillee"),
        "formulation_bo": comp.get("formulation_bo")
    }
    source = comp.get("source", {})
    if source:
        result["source"] = {
            "pdf": source.get("pdf", ""),
            "page": source.get("page", 0)
        }
    return result


# ============================================================================
# STATISTIQUES ET LISTES
# ============================================================================
def get_stats() -> Dict:
    """Retourne les statistiques globales."""
    all_file = NORMALIZED_DIR / "all_normalized.json"
    if not all_file.exists():
        return {"error": "Fichier all_normalized.json non trouve"}

    with open(all_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return {
        "total": data["meta"]["total"],
        "format": data["meta"]["format"],
        "niveaux": {
            s["niveau_code"]: {
                "nom": NIVEAU_CODE_TO_NAME.get(s["niveau_code"], s["niveau"]),
                "total": s["total"],
                "domaines": s["by_domaine"]
            }
            for s in data["by_niveau"]
        },
        "mapping_niveaux": data["meta"]["niveau_mapping"],
        "mapping_domaines": data["meta"]["domaine_mapping"]
    }


def list_niveaux():
    """Affiche la liste des niveaux disponibles."""
    print("\nNIVEAUX DISPONIBLES")
    print("-" * 40)
    print(f"{'Code':<6} {'Niveau':<20} {'Aliases'}")
    print("-" * 40)

    aliases_by_code = {}
    for name, code in NIVEAU_NAME_TO_CODE.items():
        if code not in aliases_by_code:
            aliases_by_code[code] = []
        aliases_by_code[code].append(name)

    for code, name in sorted(NIVEAU_CODE_TO_NAME.items(), key=lambda x: x[0], reverse=True):
        aliases = ", ".join(aliases_by_code.get(code, [])[:3])
        print(f"{code:<6} {name:<20} {aliases}")


def list_domaines():
    """Affiche la liste des domaines disponibles."""
    print("\nDOMAINES DISPONIBLES")
    print("-" * 40)
    print(f"{'Lettre':<8} {'Domaine'}")
    print("-" * 40)

    for letter, name in sorted(DOMAINE_LETTER_TO_NAME.items()):
        print(f"{letter:<8} {name}")


def list_synonyms():
    """Affiche la liste des synonymes disponibles pour la recherche."""
    print("\nSYNONYMES DISPONIBLES POUR LA RECHERCHE")
    print("=" * 60)

    for concept, synonyms in sorted(SEARCH_SYNONYMS.items()):
        syn_str = ", ".join(synonyms[:5])
        if len(synonyms) > 5:
            syn_str += f" (+{len(synonyms)-5})"
        print(f"{concept:<25} -> {syn_str}")


# ============================================================================
# MAIN
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Recherche de competences - Codes normalises",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  --niveau 1S --keyword "suite"      Suites en 1ere Spe
  --niveau 6 --domaine N             Nombres en 6eme
  --code 1SY10                       Competence par code exact
  --keyword "pythagore" --all-levels Recherche tous niveaux
  --stats                            Statistiques globales
  --list-synonyms                    Affiche les synonymes de recherche
        """
    )

    # Options de recherche
    parser.add_argument("--niveau", "-n", help="Niveau (6,5,4,3,2G,2H,1S,1T,1E,0S,0C,0E,0T ou nom)")
    parser.add_argument("--keyword", "-k", help="Mot-cle a rechercher")
    parser.add_argument("--domaine", "-d", help="Filtrer par domaine (N,A,Y,L,G,R,S,P,T,O ou nom)")
    parser.add_argument("--code", "-c", help="Recherche par code exact (ex: 1SY10)")
    parser.add_argument("--all-levels", action="store_true", help="Rechercher tous niveaux")
    parser.add_argument("--exact", action="store_true", help="Recherche exacte (pas de synonymes)")

    # Options d'affichage
    parser.add_argument("--limit", "-l", type=int, default=20, help="Limite resultats (defaut: 20)")
    parser.add_argument("--format", "-f", choices=["short", "medium", "json"], default="short")

    # Options d'info
    parser.add_argument("--stats", action="store_true", help="Afficher statistiques")
    parser.add_argument("--list-niveaux", action="store_true", help="Lister les niveaux")
    parser.add_argument("--list-domaines", action="store_true", help="Lister les domaines")
    parser.add_argument("--list-synonyms", action="store_true", help="Lister les synonymes de recherche")

    args = parser.parse_args()

    # Mode stats
    if args.stats:
        stats = get_stats()
        print(json.dumps(stats, ensure_ascii=True, indent=2))
        return

    # Mode liste niveaux
    if args.list_niveaux:
        list_niveaux()
        return

    # Mode liste domaines
    if args.list_domaines:
        list_domaines()
        return

    # Mode liste synonymes
    if args.list_synonyms:
        list_synonyms()
        return

    # Recherche par code exact
    if args.code:
        result = search_by_code(args.code)
        if result:
            if args.format == "json":
                print(json.dumps(format_competence_json(result), ensure_ascii=True, indent=2))
            elif args.format == "medium":
                print(format_competence_medium(result))
            else:
                print(format_competence_short(result))
        else:
            print(f"Code non trouve: {args.code}")
        return

    # Validation
    if not args.niveau and not args.all_levels:
        print("Erreur: --niveau, --code, ou --all-levels requis")
        print("Utilisez --list-niveaux pour voir les niveaux disponibles")
        sys.exit(1)

    # Determiner les niveaux a rechercher
    if args.all_levels:
        niveaux_to_search = ALL_NIVEAU_CODES
    else:
        niveau_code = normalize_niveau(args.niveau)
        if niveau_code not in NIVEAU_CODE_TO_NAME:
            print(f"Niveau inconnu: {args.niveau}")
            print("Utilisez --list-niveaux pour voir les niveaux disponibles")
            sys.exit(1)
        niveaux_to_search = [niveau_code]

    # Normaliser le domaine si specifie
    domaine_filter = None
    if args.domaine:
        domaine_filter = normalize_domaine(args.domaine)

    all_results = []

    for niveau_code in niveaux_to_search:
        competences = load_normalized_competences(niveau_code)

        if not competences:
            continue

        # Filtrer par domaine si specifie
        if domaine_filter:
            competences = filter_by_domaine(competences, domaine_filter)

        # Recherche par mot-cle
        if args.keyword:
            results = search_keyword(competences, args.keyword, args.limit, fuzzy=not args.exact)
        else:
            results = competences[:args.limit]

        all_results.extend(results)

    # Limiter le total
    all_results = all_results[:args.limit]

    # Affichage
    if args.format == "json":
        output = [format_competence_json(c) for c in all_results]
        print(json.dumps(output, ensure_ascii=True, indent=2))
    elif args.format == "medium":
        for i, c in enumerate(all_results):
            print(f"\n--- Resultat {i+1} ---")
            print(format_competence_medium(c))
    else:
        for c in all_results:
            print(format_competence_short(c))

    print(f"\n{len(all_results)} resultat(s) trouve(s)")


if __name__ == "__main__":
    main()
