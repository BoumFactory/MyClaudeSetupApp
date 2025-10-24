#!/usr/bin/env python3
"""
MCP Server AMÉLIORÉ pour la gestion des compétences pédagogiques.
Recherche intelligente avec scoring de pertinence et tri avancé.
"""

import json
import logging
import sys
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict

# Configuration du logging pour écrire dans stderr seulement
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("competences-server-enhanced")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)

# Créer l'instance du serveur MCP
mcp = FastMCP("competences-server-enhanced")

# Chemins vers les fichiers de configuration
PREFERENCES_FILE = Path(__file__).parent / ".." / "datas" / "competence-server-user-preferences.json"
COMPETENCES_DIR = Path(__file__).parent / ".." / "datas" / "competences"

# Seuil de pertinence minimum pour filtrer les résultats peu pertinents
MINIMUM_RELEVANCE_SCORE = 15  # Score minimum requis pour qu'une compétence soit incluse dans les résultats

# Cache pour les données des compétences
_all_competences_cache: Optional[List[Dict[str, Any]]] = None
_preferences_cache: Optional[Dict[str, Any]] = None

def load_preferences() -> Dict[str, Any]:
    """Charge les préférences utilisateur depuis le fichier de configuration."""
    global _preferences_cache

    if _preferences_cache is None:
        try:
            with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                _preferences_cache = json.load(f)
                logger.info(f"Préférences chargées: {len(_preferences_cache.get('default_data_sources', {}))} niveaux configurés")
        except FileNotFoundError:
            logger.info("Fichier de préférences non trouvé, utilisation des valeurs par défaut")
            _preferences_cache = {
                "default_data_sources": {
                    "CM1": str(COMPETENCES_DIR / "CM1.json"),
                    "CM2": str(COMPETENCES_DIR / "CM2.json"),
                    "SIXIEME": str(COMPETENCES_DIR / "6eme.json"),
                    "CINQUIEME": str(COMPETENCES_DIR / "5eme.json"),
                    "QUATRIEME": str(COMPETENCES_DIR / "4eme.json"),
                    "TROISIEME": str(COMPETENCES_DIR / "3eme.json"),
                    "SECONDE": str(COMPETENCES_DIR / "2nde.json"),
                    "PREMIERE_SPE": str(COMPETENCES_DIR / "1ere_spe.json"),
                    "TERMINALE": str(COMPETENCES_DIR / "Terminale.json")
                },
                "fallback_behavior": "show_error_message",
                "last_updated": "2025-09-13T00:00:00Z"
            }
            save_preferences(_preferences_cache)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur lors du décodage JSON des préférences: {e}")
            _preferences_cache = {
                "default_data_sources": {},
                "fallback_behavior": "show_error_message",
                "last_updated": "2025-09-13T00:00:00Z"
            }

    return _preferences_cache

def save_preferences(preferences: Dict[str, Any]) -> None:
    """Sauvegarde les préférences dans le fichier de configuration."""
    global _preferences_cache
    try:
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        preferences["last_updated"] = datetime.now().isoformat() + "Z"

        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, ensure_ascii=False, indent=2)

        _preferences_cache = preferences
        logger.info("Préférences sauvegardées avec succès")

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des préférences: {e}")
        raise

def load_all_competences() -> List[Dict[str, Any]]:
    """Charge toutes les compétences de tous les niveaux configurés."""
    global _all_competences_cache

    if _all_competences_cache is None:
        all_competences = []
        preferences = load_preferences()
        data_sources = preferences.get('default_data_sources', {})

        for niveau, file_path in data_sources.items():
            try:
                file_path_obj = Path(file_path)
                if not file_path_obj.is_absolute():
                    file_path_obj = COMPETENCES_DIR / file_path

                if file_path_obj.exists():
                    with open(file_path_obj, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        competences = data.get('competences', [])

                        # Enrichir chaque compétence avec le niveau si manquant
                        for comp in competences:
                            if not comp.get('niveau'):
                                comp['niveau'] = niveau

                        all_competences.extend(competences)
                        logger.info(f"Chargé {len(competences)} compétences pour {niveau}")
                else:
                    logger.warning(f"Fichier non trouvé: {file_path_obj}")

            except Exception as e:
                logger.error(f"Erreur lors du chargement de {file_path} pour {niveau}: {e}")
                continue

        _all_competences_cache = all_competences
        logger.info(f"Total compétences chargées: {len(all_competences)}")

    return _all_competences_cache

def normalize_text(text: str) -> str:
    """Normalise le texte pour la recherche (minuscules, sans accents, etc.)."""
    if not text:
        return ""

    # Conversion en minuscules
    text = text.lower()

    # Suppression des accents
    accents = {
        'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
        'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
        'ç': 'c', 'ñ': 'n'
    }

    for accent, char in accents.items():
        text = text.replace(accent, char)

    return text

def calculate_relevance_score(competence: Dict[str, Any], query_terms: List[str], niveau_filter: str = None) -> Tuple[int, int]:
    """
    Calcule un score de pertinence STRICT pour une compétence par rapport aux termes de recherche.

    Returns:
        Tuple (score_pertinence, palier) pour le tri
    """
    score = 0

    # FILTRE STRICT NIVEAU OBLIGATOIRE - Si niveau spécifié, éliminer immédiatement les autres
    if niveau_filter:
        comp_niveau = competence.get('niveau', '').upper()
        niveau_upper = niveau_filter.upper()

        # Utiliser le mapping des niveaux
        niveau_mappings = {
            'SIXIEME': ['SIXIEME', '6EME', '6'],
            'CINQUIEME': ['CINQUIEME', '5EME', '5'],
            'QUATRIEME': ['QUATRIEME', '4EME', '4'],
            'TROISIEME': ['TROISIEME', '3EME', '3'],
            'SECONDE': ['SECONDE', '2NDE', '2'],
            'PREMIERE': ['PREMIERE', '1ERE', '1'],
            'PREMIERE_SPE': ['PREMIERE_SPE', '1ERE_SPE', 'PREMIERE SPECIALITE'],
            'TERMINALE': ['TERMINALE', 'TERM']
        }

        possible_names = [niveau_upper]
        for standard, variants in niveau_mappings.items():
            if niveau_upper in variants:
                possible_names.extend(variants)
                break

        if comp_niveau not in possible_names:
            return (0, 0)  # Élimination immédiate

    # Textes à analyser avec leurs poids RENFORCÉS pour pertinence stricte
    fields_weights = {
        'nom': 20,           # Le nom est TRÈS important
        'description': 15,   # Description très importante
        'code': 12,          # Code important pour recherche précise
        'source_sequence': 10, # Séquence importante
        'objectifApprentissageCours': 8,  # Objectifs cours
        'objectifApprentissageExercice': 8, # Objectifs exercices
        'categorie': 5,      # Catégorie
        'themes': 7          # Thèmes plus importants
    }

    # Compter combien de termes de recherche sont trouvés
    terms_found = 0
    total_terms = len(query_terms)

    for field, weight in fields_weights.items():
        field_value = competence.get(field, "")

        # Traitement spécial pour les listes
        if isinstance(field_value, list):
            if field in ['themes', 'objectifApprentissageCours', 'objectifApprentissageExercice']:
                field_text = " ".join(str(item) for item in field_value)
            else:
                field_text = str(field_value)
        else:
            field_text = str(field_value)

        normalized_field = normalize_text(field_text)

        # Calculer le score pour ce champ
        field_score = 0
        field_terms_found = 0

        for term in query_terms:
            term_norm = normalize_text(term)
            term_found_in_field = False

            # Correspondance exacte du terme (bonus maximal)
            if term_norm in normalized_field.split():
                field_score += weight * 3  # Bonus renforcé
                term_found_in_field = True

            # Correspondance partielle (contient le terme)
            elif term_norm in normalized_field:
                field_score += weight * 2  # Bonus renforcé
                term_found_in_field = True

            # Correspondance floue seulement pour termes longs (> 4 caractères)
            elif len(term_norm) > 4:
                pattern = re.compile(r'\b' + re.escape(term_norm) + r'\w*', re.IGNORECASE)
                matches = pattern.findall(normalized_field)
                if matches:
                    field_score += weight // 2
                    term_found_in_field = True

            if term_found_in_field:
                field_terms_found += 1

        score += field_score
        if field_terms_found > 0:
            terms_found += field_terms_found

    # PÉNALITÉ SÉVÈRE si trop peu de termes trouvés
    if total_terms > 1:
        coverage_ratio = terms_found / (total_terms * len(fields_weights))
        if coverage_ratio < 0.1:  # Moins de 10% de couverture
            score = score // 4  # Division par 4 du score
        elif coverage_ratio < 0.2:  # Moins de 20% de couverture
            score = score // 2  # Division par 2 du score

    # Bonus réduit pour contenu détaillé (moins généreux)
    content_bonus = 0
    if competence.get('objectifApprentissageCours') and len(competence['objectifApprentissageCours']) > 2:
        content_bonus += 2
    if competence.get('objectifApprentissageExercice') and len(competence['objectifApprentissageExercice']) > 2:
        content_bonus += 2
    if competence.get('description') and len(competence['description']) > 100:
        content_bonus += 3

    score += content_bonus

    # Retourner le score et le palier pour le tri
    palier = competence.get('palier', 0)
    return (score, palier)

@mcp.tool()
def search_competences(query: str, limit: int = 20, offset: int = 0) -> str:
    """
    Recherche AMÉLIORÉE des compétences par texte libre avec scoring de pertinence.

    Args:
        query: Terme de recherche (recherche dans TOUS les champs)
        limit: Nombre maximum de résultats à retourner (défaut: 20)
        offset: Décalage pour la pagination (défaut: 0)

    Returns:
        JSON string avec les résultats de la recherche paginés et triés par pertinence
    """
    try:
        all_competences = load_all_competences()

        if not query.strip():
            return json.dumps({
                "query": query,
                "found": 0,
                "message": "Requête vide",
                "competences": []
            }, ensure_ascii=False, indent=2)

        query_terms = query.split()

        # Calculer le score de pertinence pour chaque compétence
        scored_competences = []
        for comp in all_competences:
            score, palier = calculate_relevance_score(comp, query_terms)
            if score >= MINIMUM_RELEVANCE_SCORE:  # Filtrer avec le seuil de pertinence minimum
                scored_competences.append((score, palier, comp))

        # Trier par score décroissant, puis par palier décroissant
        scored_competences.sort(key=lambda x: (-x[0], -x[1]))

        # Extraire seulement les compétences (sans les scores)
        results = [comp for _, _, comp in scored_competences]

        total_found = len(results)
        paginated_results = results[offset:offset + limit]

        # Ajouter les scores de debug si nécessaire
        debug_results = []
        for i, comp in enumerate(paginated_results):
            original_idx = offset + i
            if original_idx < len(scored_competences):
                score, palier, _ = scored_competences[original_idx]
                comp_with_debug = comp.copy()
                comp_with_debug['_debug_score'] = score
                debug_results.append(comp_with_debug)
            else:
                debug_results.append(comp)

        return json.dumps({
            "query": query,
            "found": total_found,
            "pagination": {
                "offset": offset,
                "limit": limit,
                "returned": len(paginated_results),
                "has_more": offset + limit < total_found,
                "next_offset": offset + limit if offset + limit < total_found else None
            },
            "competences": debug_results,
            "info": "Résultats triés par pertinence puis par palier"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans search_competences: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def filter_by_niveau(niveau: str) -> str:
    """
    Filtre les compétences par niveau scolaire.

    Args:
        niveau: Niveau scolaire (CM1, CM2, SIXIEME, CINQUIEME, QUATRIEME, etc.)

    Returns:
        JSON string avec les compétences du niveau demandé
    """
    try:
        all_competences = load_all_competences()
        niveau_upper = niveau.upper()

        # Normalisation des noms de niveaux
        niveau_mappings = {
            'SIXIEME': ['SIXIEME', '6EME', '6'],
            'CINQUIEME': ['CINQUIEME', '5EME', '5'],
            'QUATRIEME': ['QUATRIEME', '4EME', '4'],
            'TROISIEME': ['TROISIEME', '3EME', '3'],
            'SECONDE': ['SECONDE', '2NDE', '2'],
            'PREMIERE': ['PREMIERE', '1ERE', '1'],
            'PREMIERE_SPE': ['PREMIERE_SPE', '1ERE_SPE', 'PREMIERE SPECIALITE'],
            'TERMINALE': ['TERMINALE', 'TERM']
        }

        # Chercher les variantes possibles
        possible_names = [niveau_upper]
        for standard, variants in niveau_mappings.items():
            if niveau_upper in variants:
                possible_names.extend(variants)
                break

        results = []
        for comp in all_competences:
            comp_niveau = comp.get('niveau', '').upper()
            if comp_niveau in possible_names:
                results.append(comp)

        # Trier par palier puis par code
        results.sort(key=lambda x: (x.get('palier', 0), x.get('code', '')))

        return json.dumps({
            "niveau": niveau,
            "found": len(results),
            "competences": results
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans filter_by_niveau: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def search_competences_strict(query: str, niveau: str, limit: int = 20, offset: int = 0) -> str:
    """
    Recherche STRICTE des compétences avec query et niveau OBLIGATOIRES.

    Args:
        query: Terme de recherche (OBLIGATOIRE)
        niveau: Niveau scolaire (OBLIGATOIRE)
        limit: Nombre maximum de résultats à retourner (défaut: 20)
        offset: Décalage pour la pagination (défaut: 0)

    Returns:
        JSON string avec les résultats de la recherche strictement filtrés
    """
    try:
        if not query.strip():
            return json.dumps({
                "error": "Le paramètre 'query' est obligatoire et ne peut pas être vide"
            }, ensure_ascii=False, indent=2)

        if not niveau.strip():
            return json.dumps({
                "error": "Le paramètre 'niveau' est obligatoire et ne peut pas être vide"
            }, ensure_ascii=False, indent=2)

        all_competences = load_all_competences()
        query_terms = query.split()

        # Calculer le score de pertinence avec filtrage strict par niveau
        scored_competences = []
        for comp in all_competences:
            score, palier = calculate_relevance_score(comp, query_terms, niveau)
            if score >= MINIMUM_RELEVANCE_SCORE:  # Filtrage strict avec seuil élevé
                scored_competences.append((score, palier, comp))

        # Trier par score décroissant, puis par palier décroissant
        scored_competences.sort(key=lambda x: (-x[0], -x[1]))

        # Extraire seulement les compétences (sans les scores)
        results = [comp for _, _, comp in scored_competences]

        total_found = len(results)
        paginated_results = results[offset:offset + limit]

        # Ajouter les scores de debug
        debug_results = []
        for i, comp in enumerate(paginated_results):
            original_idx = offset + i
            if original_idx < len(scored_competences):
                score, palier, _ = scored_competences[original_idx]
                comp_with_debug = comp.copy()
                comp_with_debug['_debug_score'] = score
                debug_results.append(comp_with_debug)
            else:
                debug_results.append(comp)

        return json.dumps({
            "query": query,
            "niveau": niveau,
            "found": total_found,
            "pagination": {
                "offset": offset,
                "limit": limit,
                "returned": len(paginated_results),
                "has_more": offset + limit < total_found,
                "next_offset": offset + limit if offset + limit < total_found else None
            },
            "competences": debug_results,
            "info": "Recherche STRICTE - Résultats filtrés par niveau puis triés par pertinence"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans search_competences_strict: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def advanced_search(query: str = "", niveau: str = "", theme: str = "", palier: int = 0, nombre_max: int = 2, offset: int = 0) -> str:
    """
    Recherche avancée AMÉLIORÉE avec plusieurs critères combinés et tri intelligent.

    Args:
        query: Terme de recherche optionnel (recherche approfondie dans tous les champs)
        niveau: Niveau scolaire optionnel
        theme: Thème optionnel
        palier: Palier optionnel (0 = ignoré)
        nombre_max: Nombre maximum de résultats à retourner (défaut: 2)
        offset: Décalage pour la pagination (défaut: 0)

    Returns:
        JSON string avec les résultats de la recherche multicritères paginés et triés
    """
    try:
        all_competences = load_all_competences()
        results = all_competences.copy()
        filters_applied = []

        # Étape 1: Filtres de base
        if niveau:
            niveau_upper = niveau.upper()
            # Utiliser le même système de mapping que filter_by_niveau
            niveau_mappings = {
                'SIXIEME': ['SIXIEME', '6EME', '6'],
                'CINQUIEME': ['CINQUIEME', '5EME', '5'],
                'QUATRIEME': ['QUATRIEME', '4EME', '4'],
                'TROISIEME': ['TROISIEME', '3EME', '3'],
                'SECONDE': ['SECONDE', '2NDE', '2'],
                'PREMIERE': ['PREMIERE', '1ERE', '1'],
                'PREMIERE_SPE': ['PREMIERE_SPE', '1ERE_SPE', 'PREMIERE SPECIALITE'],
                'TERMINALE': ['TERMINALE', 'TERM']
            }

            possible_names = [niveau_upper]
            for standard, variants in niveau_mappings.items():
                if niveau_upper in variants:
                    possible_names.extend(variants)
                    break

            results = [comp for comp in results if comp.get('niveau', '').upper() in possible_names]
            filters_applied.append(f"niveau: {niveau}")

        if theme:
            theme_upper = theme.upper()
            results = [comp for comp in results if theme_upper in [t.upper() for t in comp.get('themes', [])]]
            filters_applied.append(f"theme: {theme}")

        if palier > 0:
            results = [comp for comp in results if comp.get('palier') == palier]
            filters_applied.append(f"palier: {palier}")

        # Étape 2: Recherche textuelle avec scoring si query fournie
        if query and query.strip():
            query_terms = query.split()
            scored_competences = []

            for comp in results:
                # Utiliser le scoring avec filtrage niveau si fourni
                score, comp_palier = calculate_relevance_score(comp, query_terms, niveau if niveau else None)
                if score >= MINIMUM_RELEVANCE_SCORE:  # Filtrer avec le seuil de pertinence minimum
                    scored_competences.append((score, comp_palier, comp))

            # Trier par score décroissant, puis par palier décroissant
            scored_competences.sort(key=lambda x: (-x[0], -x[1]))
            results = [comp for _, _, comp in scored_competences]
            filters_applied.append(f"texte: '{query}' (avec scoring de pertinence STRICT)")
        else:
            # Pas de recherche textuelle, trier par palier puis code
            results.sort(key=lambda x: (-x.get('palier', 0), x.get('code', '')))

        total_found = len(results)
        paginated_results = results[offset:offset + nombre_max]

        return json.dumps({
            "filtres_appliques": filters_applied,
            "found": total_found,
            "pagination": {
                "offset": offset,
                "limit": nombre_max,
                "returned": len(paginated_results),
                "has_more": offset + nombre_max < total_found,
                "next_offset": offset + nombre_max if offset + nombre_max < total_found else None
            },
            "competences": paginated_results,
            "info": "Résultats triés par pertinence (si recherche textuelle) puis par palier"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans advanced_search: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# Garder toutes les autres méthodes existantes inchangées
@mcp.tool()
def filter_by_theme(theme: str) -> str:
    """Filtre les compétences par thème."""
    try:
        all_competences = load_all_competences()
        theme_upper = theme.upper()

        results = [comp for comp in all_competences if theme_upper in [t.upper() for t in comp.get('themes', [])]]
        results.sort(key=lambda x: (-x.get('palier', 0), x.get('code', '')))

        return json.dumps({
            "theme": theme,
            "found": len(results),
            "competences": results
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans filter_by_theme: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def filter_by_palier(palier: int) -> str:
    """Filtre les compétences par palier de difficulté."""
    try:
        all_competences = load_all_competences()

        results = [comp for comp in all_competences if comp.get('palier') == palier]
        results.sort(key=lambda x: (x.get('niveau', ''), x.get('code', '')))

        return json.dumps({
            "palier": palier,
            "found": len(results),
            "competences": results
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans filter_by_palier: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_competence_by_code(code: str) -> str:
    """Récupère une compétence par son code exact."""
    try:
        all_competences = load_all_competences()
        code_upper = code.upper()

        for comp in all_competences:
            if comp.get('code', '').upper() == code_upper:
                return json.dumps({
                    "code": code,
                    "found": True,
                    "competence": comp
                }, ensure_ascii=False, indent=2)

        return json.dumps({
            "code": code,
            "found": False,
            "message": f"Aucune compétence trouvée avec le code '{code}'"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_competence_by_code: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_niveaux_available() -> str:
    """Liste tous les niveaux scolaires disponibles."""
    try:
        all_competences = load_all_competences()
        niveaux = sorted(set(comp.get('niveau', '') for comp in all_competences if comp.get('niveau')))

        return json.dumps({
            "niveaux_disponibles": niveaux,
            "total": len(niveaux)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_niveaux_available: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_themes_available() -> str:
    """Liste tous les thèmes de compétences disponibles."""
    try:
        all_competences = load_all_competences()
        themes = set()
        for comp in all_competences:
            themes.update(comp.get('themes', []))
        themes_list = sorted(list(themes))

        return json.dumps({
            "themes_disponibles": themes_list,
            "total": len(themes_list)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_themes_available: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_paliers_available() -> str:
    """Liste tous les paliers de difficulté disponibles."""
    try:
        all_competences = load_all_competences()
        paliers = sorted(set(comp.get('palier', 0) for comp in all_competences if comp.get('palier')))

        return json.dumps({
            "paliers_disponibles": paliers,
            "total": len(paliers)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_paliers_available: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_competences_stats() -> str:
    """Obtient les statistiques générales des compétences."""
    try:
        all_competences = load_all_competences()

        niveaux_count = defaultdict(int)
        themes_count = defaultdict(int)
        paliers_count = defaultdict(int)

        for comp in all_competences:
            # Compter par niveau
            niveau = comp.get('niveau', 'Inconnu')
            niveaux_count[niveau] += 1

            # Compter par thème
            for theme in comp.get('themes', []):
                themes_count[theme] += 1

            # Compter par palier
            palier = comp.get('palier', 0)
            if palier:
                paliers_count[palier] += 1

        return json.dumps({
            "total_competences": len(all_competences),
            "repartition_par_niveau": dict(niveaux_count),
            "repartition_par_theme": dict(themes_count),
            "repartition_par_palier": dict(paliers_count),
            "version": "enhanced_with_deep_search"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_competences_stats: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)

# Méthodes de gestion des préférences (inchangées)
@mcp.tool()
def get_user_preferences() -> str:
    """Récupère les préférences utilisateur actuelles."""
    try:
        preferences = load_preferences()
        return json.dumps({
            "status": "success",
            "preferences": preferences
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans get_user_preferences: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

@mcp.tool()
def add_data_source(niveau: str, file_path: str) -> str:
    """Ajoute une nouvelle source de données pour un niveau."""
    try:
        preferences = load_preferences()
        niveau_upper = niveau.upper()

        preferences['default_data_sources'][niveau_upper] = file_path
        save_preferences(preferences)

        # Invalider le cache pour forcer le rechargement
        global _all_competences_cache
        _all_competences_cache = None

        return json.dumps({
            "status": "success",
            "message": f"Source de données ajoutée pour {niveau}: {file_path}",
            "niveau": niveau_upper,
            "file_path": file_path
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans add_data_source: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

@mcp.tool()
def reset_preferences() -> str:
    """Remet les préférences aux valeurs par défaut."""
    try:
        global _all_competences_cache, _preferences_cache
        _all_competences_cache = None
        _preferences_cache = None

        # Recharger avec les valeurs par défaut
        load_preferences()

        return json.dumps({
            "status": "success",
            "message": "Préférences remises à zéro et cache rechargé"
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans reset_preferences: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

def get_category_letter(categorie: str) -> str:
    """Retourne la lettre correspondant à une catégorie."""
    category_mapping = {
        'NOMBRES': 'N',
        'GEOMETRIE': 'G',
        'GRANDEURS': 'R',
        'DONNEES': 'D',
        'INFORMATIQUE': 'I'
    }
    return category_mapping.get(categorie, 'N')

def get_niveau_number(niveau: str) -> str:
    """Retourne le numéro correspondant à un niveau scolaire."""
    niveau_mapping = {
        'CM1': '0',
        'CM2': '0',
        'SIXIEME': '6',
        'CINQUIEME': '5',
        'QUATRIEME': '4',
        'TROISIEME': '3',
        'SECONDE': '2',
        'PREMIERE_SPE': '1',
        'TERMINALE': '1'
    }
    return niveau_mapping.get(niveau, '1')

def generate_competence_code(niveau: str, categorie: str, index_suggestion: str = None) -> Tuple[str, int]:
    """
    Génère automatiquement un code de compétence avec auto-incrémentation des paliers.

    Args:
        niveau: Niveau scolaire
        categorie: Catégorie de la compétence
        index_suggestion: Index suggéré (ex: "03") pour lier à des compétences existantes

    Returns:
        Tuple (code_complet, palier_attribué)
    """
    try:
        # Obtenir le fichier du niveau
        file_path = get_niveau_file_path(niveau)

        # Charger les compétences existantes
        existing_competences = []
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                existing_competences = data.get('competences', [])

        niveau_num = get_niveau_number(niveau)
        category_letter = get_category_letter(categorie)

        if index_suggestion:
            # Utiliser l'index suggéré et trouver le palier suivant disponible
            base_code = f"C{niveau_num}{category_letter}{index_suggestion.zfill(2)}"

            # Trouver tous les paliers existants pour cet index
            existing_paliers = []
            for comp in existing_competences:
                code = comp.get('code', '')
                if code.startswith(base_code + '-'):
                    try:
                        palier = int(code.split('-')[1])
                        existing_paliers.append(palier)
                    except (IndexError, ValueError):
                        continue

            # Attribuer le palier suivant (1 si aucun n'existe)
            next_palier = max(existing_paliers, default=0) + 1

        else:
            # Créer un nouvel index et commencer au palier 1
            existing_indices = set()

            for comp in existing_competences:
                code = comp.get('code', '')
                # Pattern: CxYzz-n
                pattern = f"C{niveau_num}{category_letter}(\d{{2}})-\d+"
                match = re.match(pattern, code)
                if match:
                    existing_indices.add(int(match.group(1)))

            # Trouver le prochain index disponible
            next_index = 1
            while next_index in existing_indices:
                next_index += 1

            base_code = f"C{niveau_num}{category_letter}{next_index:02d}"
            next_palier = 1

        final_code = f"{base_code}-{next_palier}"
        return final_code, next_palier

    except Exception as e:
        logger.error(f"Erreur dans generate_competence_code: {e}")
        # Fallback: génération basique
        base_code = f"C{get_niveau_number(niveau)}{get_category_letter(categorie)}01"
        return f"{base_code}-1", 1

def validate_competence_structure(competence_data: Dict[str, Any], auto_generated: bool = False) -> Tuple[bool, str]:
    """
    Valide la structure d'une compétence selon le schéma attendu.

    Args:
        competence_data: Données de la compétence
        auto_generated: Si True, le code et palier sont auto-générés (pas de validation)

    Returns:
        Tuple (is_valid, error_message)
    """
    if auto_generated:
        # Pour les compétences auto-générées, on ne vérifie pas code et palier
        required_fields = ['nom', 'description', 'niveau', 'categorie', 'themes']
    else:
        required_fields = ['code', 'nom', 'description', 'niveau', 'categorie', 'themes', 'palier']

    # Vérifier les champs obligatoires
    for field in required_fields:
        if field not in competence_data:
            return False, f"Champ obligatoire manquant: '{field}'"

        if not competence_data[field]:
            return False, f"Le champ '{field}' ne peut pas être vide"

    # Vérifications spécifiques
    if not isinstance(competence_data['themes'], list):
        return False, "Le champ 'themes' doit être une liste"

    if not auto_generated and ('palier' in competence_data):
        if not isinstance(competence_data['palier'], int) or competence_data['palier'] < 1 or competence_data['palier'] > 5:
            return False, "Le champ 'palier' doit être un entier entre 1 et 5"

    valid_categories = ['NOMBRES', 'GEOMETRIE', 'GRANDEURS', 'DONNEES', 'INFORMATIQUE']
    if competence_data['categorie'] not in valid_categories:
        return False, f"Catégorie invalide. Doit être l'une de: {', '.join(valid_categories)}"

    valid_niveaux = ['CM1', 'CM2', 'SIXIEME', 'CINQUIEME', 'QUATRIEME', 'TROISIEME', 'SECONDE', 'PREMIERE_SPE', 'TERMINALE']
    if competence_data['niveau'] not in valid_niveaux:
        return False, f"Niveau invalide. Doit être l'un de: {', '.join(valid_niveaux)}"

    # Validation du format du code (ex: C1N01-1) seulement si pas auto-généré
    if not auto_generated and 'code' in competence_data:
        if not re.match(r'^C\d+[NGDIR]\d+-\d+$', competence_data['code']):
            return False, "Format de code invalide. Attendu: CxYzz-n (ex: C1N01-1)"

    return True, "Structure valide"

def get_niveau_file_path(niveau: str) -> Path:
    """Retourne le chemin du fichier JSON pour un niveau donné."""
    preferences = load_preferences()
    data_sources = preferences.get('default_data_sources', {})

    niveau_upper = niveau.upper()
    if niveau_upper not in data_sources:
        raise ValueError(f"Niveau '{niveau}' non configuré. Niveaux disponibles: {list(data_sources.keys())}")

    file_path = Path(data_sources[niveau_upper])
    if not file_path.is_absolute():
        file_path = COMPETENCES_DIR / file_path

    return file_path

@mcp.tool()
def create_competence(niveau: str, competence_data: Dict[str, Any]) -> str:
    """
    Créer une nouvelle compétence avec génération automatique du code et du palier.

    Args:
        niveau: Niveau scolaire (CM1, CM2, SIXIEME, etc.)
        competence_data: Dictionnaire avec les données de la compétence
                        Champs obligatoires: nom, description, niveau, categorie, themes
                        Champs optionnels: index_suggestion (pour lier à des compétences existantes)

    Returns:
        JSON avec le résultat de la création
    """
    try:
        # Extraction de l'index suggéré si fourni
        index_suggestion = competence_data.pop('index_suggestion', None)

        # Validation automatique (sans code ni palier)
        is_valid, error_message = validate_competence_structure(competence_data, auto_generated=True)
        if not is_valid:
            return json.dumps({
                "status": "error",
                "message": "Erreur de validation",
                "details": error_message,
                "help": "Champs obligatoires: nom, description, niveau, categorie, themes (liste). Champ optionnel: index_suggestion (pour lier à des compétences existantes)"
            }, ensure_ascii=False, indent=2)

        # Vérifier que le niveau correspond
        if competence_data['niveau'].upper() != niveau.upper():
            return json.dumps({
                "status": "error",
                "message": "Incohérence de niveau",
                "details": f"Le niveau dans la compétence ('{competence_data['niveau']}') ne correspond pas au niveau cible ('{niveau}')"
            }, ensure_ascii=False, indent=2)

        # Génération automatique du code et du palier
        try:
            auto_code, auto_palier = generate_competence_code(
                niveau,
                competence_data['categorie'],
                index_suggestion
            )

            # Ajouter le code et palier générés
            competence_data['code'] = auto_code
            competence_data['palier'] = auto_palier

        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": "Erreur de génération de code",
                "details": f"Impossible de générer le code automatiquement: {str(e)}"
            }, ensure_ascii=False, indent=2)

        # Obtenir le fichier du niveau
        file_path = get_niveau_file_path(niveau)

        # Charger le fichier existant
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"competences": []}

        # Double vérification que le code généré n'existe pas déjà (sécurité)
        for comp in data.get('competences', []):
            if comp.get('code') == competence_data['code']:
                return json.dumps({
                    "status": "error",
                    "message": "Conflit de code généré",
                    "details": f"Le code généré '{competence_data['code']}' existe déjà. Veuillez réessayer."
                }, ensure_ascii=False, indent=2)

        # Ajouter la nouvelle compétence
        data.setdefault('competences', []).append(competence_data)

        # Sauvegarder
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Invalider le cache
        global _all_competences_cache
        _all_competences_cache = None

        return json.dumps({
            "status": "success",
            "message": "Compétence créée avec succès",
            "code": competence_data['code'],
            "palier": auto_palier,
            "niveau": niveau,
            "index_used": index_suggestion if index_suggestion else "nouveau",
            "file_path": str(file_path)
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans create_competence: {e}")
        return json.dumps({
            "status": "error",
            "message": "Erreur interne",
            "details": str(e)
        }, ensure_ascii=False)

@mcp.tool()
def update_competence(code: str, competence_data: Dict[str, Any]) -> str:
    """
    Modifier une compétence existante (validation automatique).

    Args:
        code: Code de la compétence à modifier
        competence_data: Nouvelles données de la compétence

    Returns:
        JSON avec le résultat de la modification
    """
    try:
        # Validation automatique
        is_valid, error_message = validate_competence_structure(competence_data)
        if not is_valid:
            return json.dumps({
                "status": "error",
                "message": "Erreur de validation",
                "details": error_message
            }, ensure_ascii=False, indent=2)

        # Trouver la compétence existante
        all_competences = load_all_competences()
        found_competence = None
        for comp in all_competences:
            if comp.get('code') == code:
                found_competence = comp
                break

        if not found_competence:
            return json.dumps({
                "status": "error",
                "message": "Compétence non trouvée",
                "details": f"Aucune compétence avec le code '{code}'"
            }, ensure_ascii=False, indent=2)

        # Obtenir le fichier du niveau
        niveau = found_competence['niveau']
        file_path = get_niveau_file_path(niveau)

        # Charger et modifier
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for i, comp in enumerate(data.get('competences', [])):
            if comp.get('code') == code:
                data['competences'][i] = competence_data
                break

        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Invalider le cache
        global _all_competences_cache
        _all_competences_cache = None

        return json.dumps({
            "status": "success",
            "message": "Compétence mise à jour avec succès",
            "code": code,
            "niveau": niveau
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans update_competence: {e}")
        return json.dumps({
            "status": "error",
            "message": "Erreur interne",
            "details": str(e)
        }, ensure_ascii=False)

@mcp.tool()
def delete_competence(code: str) -> str:
    """
    Supprimer une compétence.

    Args:
        code: Code de la compétence à supprimer

    Returns:
        JSON avec le résultat de la suppression
    """
    try:
        # Trouver la compétence existante
        all_competences = load_all_competences()
        found_competence = None
        for comp in all_competences:
            if comp.get('code') == code:
                found_competence = comp
                break

        if not found_competence:
            return json.dumps({
                "status": "error",
                "message": "Compétence non trouvée",
                "details": f"Aucune compétence avec le code '{code}'"
            }, ensure_ascii=False, indent=2)

        # Obtenir le fichier du niveau
        niveau = found_competence['niveau']
        file_path = get_niveau_file_path(niveau)

        # Charger et supprimer
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        original_count = len(data.get('competences', []))
        data['competences'] = [comp for comp in data.get('competences', []) if comp.get('code') != code]

        if len(data['competences']) == original_count:
            return json.dumps({
                "status": "error",
                "message": "Compétence non supprimée",
                "details": f"Le code '{code}' n'a pas été trouvé dans le fichier {niveau}"
            }, ensure_ascii=False, indent=2)

        # Sauvegarder
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # Invalider le cache
        global _all_competences_cache
        _all_competences_cache = None

        return json.dumps({
            "status": "success",
            "message": "Compétence supprimée avec succès",
            "code": code,
            "niveau": niveau
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Erreur dans delete_competence: {e}")
        return json.dumps({
            "status": "error",
            "message": "Erreur interne",
            "details": str(e)
        }, ensure_ascii=False)

if __name__ == "__main__":
    logger.info("Démarrage du serveur MCP Compétences AMÉLIORÉ...")
    logger.info("Préchargement des préférences utilisateur...")
    load_preferences()
    logger.info("Préchargement de toutes les compétences...")
    all_comps = load_all_competences()
    logger.info(f"Serveur MCP Compétences AMÉLIORÉ prêt - {len(all_comps)} compétences chargées")

    # Démarrer le serveur
    mcp.run()