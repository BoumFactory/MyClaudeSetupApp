#!/usr/bin/env python3
"""
Serveur MCP pour la gestion des progressions pédagogiques.
Permet de rechercher et filtrer dans les progressions par niveau.
"""

import json
import logging
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Configuration du logging pour écrire dans stderr seulement
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger("progression-server")

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    logger.error("Erreur: Le package 'mcp' n'est pas installé. Installez-le avec: pip install mcp")
    sys.exit(1)


@dataclass
class ProgressionEntry:
    """Représente une entrée de progression"""
    name: str
    code: str
    description: str
    theme: List[str]
    objectif_apprentissage_cours: List[str]
    objectif_apprentissage_exercice: List[str]
    duree_estimee: int
    duree_moyenne_mesuree: Optional[int]
    sequence_name: str
    category: str


@dataclass
class SequenceAvancee:
    """Représente une séquence de progression avancée"""
    numero: int
    titre: str
    date_debut_theorique: str
    date_fin_theorique: str
    classes: Dict[str, Any]


class ProgressionServer:
    """Serveur de gestion des progressions pédagogiques"""
    
    def __init__(self, data_directory: str, preferences: Dict[str, Any] = None):
        self.data_directory = Path(data_directory)
        self.preferences = preferences or {}
        self._progression_cache = {}
        self._load_all_progressions()
    
    def _load_all_progressions(self):
        """Charge toutes les progressions disponibles selon les préférences"""
        logger.info(f"Recherche des progressions dans : {self.data_directory}")
        
        if not self.data_directory.exists():
            logger.error(f"Répertoire non trouvé : {self.data_directory}")
            return
        
        # Charger selon les préférences si disponibles
        data_sources = self.preferences.get('default_data_sources', {})
        
        if data_sources:
            # Charger selon la configuration utilisateur
            for niveau, file_path in data_sources.items():
                self._load_progression_from_path(niveau, file_path)
        else:
            # Recherche des fichiers de progression par défaut
            for fichier in self.data_directory.glob("progression-*.json"):
                niveau = self._extract_niveau_from_filename(fichier.name)
                if niveau:
                    self._load_progression_from_file(niveau, fichier)
    
    def _load_progression_from_path(self, niveau: str, file_path: str):
        """Charge une progression depuis un chemin spécifique"""
        try:
            if Path(file_path).is_absolute():
                progression_file = Path(file_path)
            else:
                # Chemin relatif par rapport au répertoire des données
                progression_file = self.data_directory / file_path
                
            with open(progression_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._progression_cache[niveau] = self._parse_progression(data)
                logger.info(f"Progression {niveau} chargée depuis {file_path} ({len(self._progression_cache[niveau])} entrées)")
                
        except FileNotFoundError:
            logger.error(f"Fichier de progression non trouvé pour {niveau}: {file_path}")
            self._progression_cache[niveau] = []
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la progression {niveau}: {e}")
            self._progression_cache[niveau] = []
    
    def _load_progression_from_file(self, niveau: str, fichier: Path):
        """Charge une progression depuis un fichier"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._progression_cache[niveau] = self._parse_progression(data)
                logger.info(f"Progression {niveau} chargée ({len(self._progression_cache[niveau])} entrées)")
        except Exception as e:
            logger.error(f"Erreur lors du chargement de {fichier}: {e}")
    
    def _extract_niveau_from_filename(self, filename: str) -> Optional[str]:
        """Extrait le niveau du nom de fichier"""
        match = re.search(r'progression-(.+)\.json', filename)
        return match.group(1).upper() if match else None
    
    def _parse_progression(self, data: Dict[str, Any]) -> List[ProgressionEntry]:
        """Parse une progression au format JSON"""
        entries = []
        
        if "progression" in data and "sequences" in data["progression"]:
            # Format progression standard
            for sequence in data["progression"]["sequences"]:
                sequence_name = sequence.get("name", "")
                category = sequence.get("category", "")
                
                for entry in sequence.get("entries", []):
                    entries.append(ProgressionEntry(
                        name=entry.get("name", ""),
                        code=entry.get("code", ""),
                        description=entry.get("description", ""),
                        theme=entry.get("theme", []),
                        objectif_apprentissage_cours=entry.get("objectifApprentissageCours", []),
                        objectif_apprentissage_exercice=entry.get("objectifApprentissageExercice", []),
                        duree_estimee=entry.get("dureeEstimee", 0),
                        duree_moyenne_mesuree=entry.get("dureeMoyenneMesuree"),
                        sequence_name=sequence_name,
                        category=category
                    ))
        
        return entries
    
    def search_progressions(self, niveau: str, query: str = "") -> List[Dict[str, Any]]:
        """Recherche dans les progressions d'un niveau"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            # Retourner une liste vide avec un message d'erreur implicite
            logger.warning(f"Aucune progression configurée pour le niveau {niveau}")
            return []
        
        entries = self._progression_cache[niveau_upper]
        
        # Si pas d'entrées chargées, indiquer le problème
        if not entries:
            logger.warning(f"Aucune donnée de progression disponible pour le niveau {niveau}")
            return []
        
        if not query:
            # Retourne toutes les entrées si pas de requête
            return [self._entry_to_dict(entry) for entry in entries]
        
        # Recherche dans le nom, description, thèmes et objectifs
        query_lower = query.lower()
        results = []
        
        for entry in entries:
            if (query_lower in entry.name.lower() or
                query_lower in entry.description.lower() or
                any(query_lower in theme.lower() for theme in entry.theme) or
                any(query_lower in obj.lower() for obj in entry.objectif_apprentissage_cours) or
                any(query_lower in obj.lower() for obj in entry.objectif_apprentissage_exercice) or
                query_lower in entry.sequence_name.lower()):
                results.append(self._entry_to_dict(entry))
        
        return results
    
    def filter_by_theme(self, niveau: str, theme: str) -> List[Dict[str, Any]]:
        """Filtre les progressions par thème"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return []
        
        entries = self._progression_cache[niveau_upper]
        results = []
        
        theme_upper = theme.upper()
        for entry in entries:
            if any(theme_upper in t.upper() for t in entry.theme):
                results.append(self._entry_to_dict(entry))
        
        return results
    
    def filter_by_sequence(self, niveau: str, sequence_name: str) -> List[Dict[str, Any]]:
        """Filtre les progressions par nom de séquence"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return []
        
        entries = self._progression_cache[niveau_upper]
        results = []
        
        for entry in entries:
            if sequence_name.lower() in entry.sequence_name.lower():
                results.append(self._entry_to_dict(entry))
        
        return results
    
    def get_entry_by_code(self, niveau: str, code: str) -> Optional[Dict[str, Any]]:
        """Récupère une entrée par son code exact"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return None
        
        entries = self._progression_cache[niveau_upper]
        
        for entry in entries:
            if entry.code == code:
                return self._entry_to_dict(entry)
        
        return None
    
    def get_niveaux_available(self) -> List[str]:
        """Liste tous les niveaux disponibles"""
        return list(self._progression_cache.keys())
    
    def get_themes_available(self, niveau: str) -> List[str]:
        """Liste tous les thèmes disponibles pour un niveau"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return []
        
        entries = self._progression_cache[niveau_upper]
        themes = set()
        
        for entry in entries:
            themes.update(entry.theme)
        
        return sorted(list(themes))
    
    def get_sequences_available(self, niveau: str) -> List[str]:
        """Liste toutes les séquences disponibles pour un niveau"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return []
        
        entries = self._progression_cache[niveau_upper]
        sequences = set()
        
        for entry in entries:
            sequences.add(entry.sequence_name)
        
        return sorted(list(sequences))
    
    def get_progression_stats(self, niveau: str = "") -> Dict[str, Any]:
        """Obtient les statistiques des progressions"""
        if niveau:
            niveau_upper = niveau.upper()
            if niveau_upper not in self._progression_cache:
                return {"error": f"Niveau {niveau} non trouvé"}
            
            entries = self._progression_cache[niveau_upper]
            themes = {}
            sequences = {}
            
            for entry in entries:
                # Comptage par thème
                for theme in entry.theme:
                    themes[theme] = themes.get(theme, 0) + 1
                
                # Comptage par séquence
                sequences[entry.sequence_name] = sequences.get(entry.sequence_name, 0) + 1
            
            return {
                "niveau": niveau_upper,
                "total_entries": len(entries),
                "themes": themes,
                "sequences": sequences,
                "duree_totale_estimee": sum(e.duree_estimee for e in entries)
            }
        else:
            # Stats globales
            stats = {}
            for niveau, entries in self._progression_cache.items():
                stats[niveau] = len(entries)
            
            return {
                "niveaux_disponibles": list(self._progression_cache.keys()),
                "total_par_niveau": stats,
                "total_global": sum(stats.values())
            }
    
    def advanced_search(self, niveau: str, query: str = "", theme: str = "", 
                       sequence: str = "") -> List[Dict[str, Any]]:
        """Recherche avancée avec plusieurs critères combinés"""
        niveau_upper = niveau.upper()
        
        if niveau_upper not in self._progression_cache:
            return []
        
        entries = self._progression_cache[niveau_upper]
        results = []
        
        for entry in entries:
            # Filtrage par requête
            if query:
                query_lower = query.lower()
                if not (query_lower in entry.name.lower() or
                       query_lower in entry.description.lower() or
                       any(query_lower in theme.lower() for theme in entry.theme) or
                       any(query_lower in obj.lower() for obj in entry.objectif_apprentissage_cours) or
                       any(query_lower in obj.lower() for obj in entry.objectif_apprentissage_exercice)):
                    continue
            
            # Filtrage par thème
            if theme:
                theme_upper = theme.upper()
                if not any(theme_upper in t.upper() for t in entry.theme):
                    continue
            
            # Filtrage par séquence
            if sequence:
                if sequence.lower() not in entry.sequence_name.lower():
                    continue
            
            results.append(self._entry_to_dict(entry))
        
        return results
    
    def _entry_to_dict(self, entry: ProgressionEntry) -> Dict[str, Any]:
        """Convertit une ProgressionEntry en dictionnaire"""
        return {
            "name": entry.name,
            "code": entry.code,
            "description": entry.description,
            "theme": entry.theme,
            "objectif_apprentissage_cours": entry.objectif_apprentissage_cours,
            "objectif_apprentissage_exercice": entry.objectif_apprentissage_exercice,
            "duree_estimee": entry.duree_estimee,
            "duree_moyenne_mesuree": entry.duree_moyenne_mesuree,
            "sequence_name": entry.sequence_name,
            "category": entry.category
        }


# Créer l'instance du serveur MCP
mcp = FastMCP("progression-server")

# Chemins vers les fichiers de configuration
PREFERENCES_FILE = Path(__file__).parent / ".." / "datas" / "progression-server-user-preferences.json"
DATA_DIR = Path(__file__).parent / ".." / "datas"

# Cache pour les préférences
_preferences_cache: Optional[Dict[str, Any]] = None

# Instance du serveur de progression
progression_server = None


@mcp.tool()
def search_progressions(niveau: str, query: str = "") -> str:
    """
    Recherche des entrées de progression par texte libre.
    
    Args:
        niveau: Niveau scolaire (SIXIEME, CINQUIEME, etc.)
        query: Terme de recherche optionnel (nom, description, thème, objectifs)
    
    Returns:
        JSON string avec les résultats de la recherche
    """
    try:
        results = progression_server.search_progressions(niveau, query)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "query": query,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def filter_by_theme(niveau: str, theme: str) -> str:
    """
    Filtre les progressions par thème.
    
    Args:
        niveau: Niveau scolaire
        theme: Thème de progression (NOMBRES, GEOMETRIE, GRANDEURS, etc.)
    
    Returns:
        JSON string avec les progressions du thème demandé
    """
    try:
        results = progression_server.filter_by_theme(niveau, theme)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "theme": theme,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def filter_by_sequence(niveau: str, sequence_name: str) -> str:
    """
    Filtre les progressions par nom de séquence.
    
    Args:
        niveau: Niveau scolaire
        sequence_name: Nom ou partie du nom de la séquence
    
    Returns:
        JSON string avec les progressions de la séquence demandée
    """
    try:
        results = progression_server.filter_by_sequence(niveau, sequence_name)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "sequence_name": sequence_name,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_entry_by_code(niveau: str, code: str) -> str:
    """
    Récupère une entrée de progression par son code exact.
    
    Args:
        niveau: Niveau scolaire
        code: Code exact de l'entrée (ex: C6N1-1)
    
    Returns:
        JSON string avec l'entrée trouvée ou un message d'erreur
    """
    try:
        result = progression_server.get_entry_by_code(niveau, code)
        if result:
            return json.dumps({
                "success": True,
                "niveau": niveau,
                "code": code,
                "result": result
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "success": False,
                "error": f"Aucune entrée trouvée pour le code {code} au niveau {niveau}"
            }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_niveaux_available() -> str:
    """
    Liste tous les niveaux scolaires disponibles.
    
    Returns:
        JSON string avec la liste des niveaux disponibles
    """
    try:
        niveaux = progression_server.get_niveaux_available()
        return json.dumps({
            "success": True,
            "niveaux_disponibles": niveaux,
            "count": len(niveaux)
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_themes_available(niveau: str) -> str:
    """
    Liste tous les thèmes disponibles pour un niveau.
    
    Args:
        niveau: Niveau scolaire
    
    Returns:
        JSON string avec la liste des thèmes disponibles
    """
    try:
        themes = progression_server.get_themes_available(niveau)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "themes_disponibles": themes,
            "count": len(themes)
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_sequences_available(niveau: str) -> str:
    """
    Liste toutes les séquences disponibles pour un niveau.
    
    Args:
        niveau: Niveau scolaire
    
    Returns:
        JSON string avec la liste des séquences disponibles
    """
    try:
        sequences = progression_server.get_sequences_available(niveau)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "sequences_disponibles": sequences,
            "count": len(sequences)
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def get_progression_stats(niveau: str = "") -> str:
    """
    Obtient les statistiques des progressions.
    
    Args:
        niveau: Niveau scolaire optionnel (vide = toutes les stats)
    
    Returns:
        JSON string avec les statistiques détaillées
    """
    try:
        stats = progression_server.get_progression_stats(niveau)
        return json.dumps({
            "success": True,
            "stats": stats
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


@mcp.tool()
def advanced_search(niveau: str, query: str = "", theme: str = "", 
                   sequence: str = "") -> str:
    """
    Recherche avancée avec plusieurs critères combinés.
    
    Args:
        niveau: Niveau scolaire (obligatoire)
        query: Terme de recherche optionnel
        theme: Thème optionnel
        sequence: Nom de séquence optionnel
    
    Returns:
        JSON string avec les résultats de la recherche multicritères
    """
    try:
        results = progression_server.advanced_search(niveau, query, theme, sequence)
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "criteres": {
                "query": query,
                "theme": theme,
                "sequence": sequence
            },
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)


# Fonctions de gestion des préférences
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
                "default_data_sources": {},
                "fallback_behavior": "show_error_message",
                "last_updated": "2025-09-11T00:00:00Z"
            }
            # Sauvegarder le fichier de préférences par défaut
            save_preferences(_preferences_cache)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur lors du décodage JSON des préférences: {e}")
            _preferences_cache = {
                "default_data_sources": {},
                "fallback_behavior": "show_error_message",
                "last_updated": "2025-09-11T00:00:00Z"
            }
            
    return _preferences_cache

def save_preferences(preferences: Dict[str, Any]) -> None:
    """Sauvegarde les préférences dans le fichier de configuration."""
    global _preferences_cache, progression_server
    try:
        # Créer le répertoire si nécessaire
        PREFERENCES_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        # Mettre à jour le timestamp
        from datetime import datetime
        preferences["last_updated"] = datetime.now().isoformat() + "Z"
        
        with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
            json.dump(preferences, f, ensure_ascii=False, indent=2)
        
        _preferences_cache = preferences
        
        # Recréer l'instance du serveur avec les nouvelles préférences
        progression_server = ProgressionServer(DATA_DIR, preferences)
        
        logger.info("Préférences sauvegardées avec succès")
        
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde des préférences: {e}")
        raise

# Nouvelles méthodes CRUD pour la gestion des préférences
@mcp.tool()
def get_user_preferences() -> str:
    """
    Récupère les préférences utilisateur actuelles.
    
    Returns:
        JSON string avec les préférences utilisateur
    """
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
def update_data_source(niveau: str, file_path: str) -> str:
    """
    Met à jour le chemin du fichier de données pour un niveau.
    
    Args:
        niveau: Niveau scolaire (ex: SIXIEME, CINQUIEME, etc.)
        file_path: Chemin vers le fichier de progression
    
    Returns:
        JSON string avec le résultat de l'opération
    """
    try:
        preferences = load_preferences()
        niveau_upper = niveau.upper()
        
        # Mettre à jour la source de données
        preferences['default_data_sources'][niveau_upper] = file_path
        
        # Sauvegarder (recharge automatiquement le serveur)
        save_preferences(preferences)
        
        return json.dumps({
            "status": "success",
            "message": f"Source de données mise à jour pour {niveau}: {file_path}",
            "niveau": niveau_upper,
            "file_path": file_path
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Erreur dans update_data_source: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

@mcp.tool()
def add_data_source(niveau: str, file_path: str) -> str:
    """
    Ajoute une nouvelle source de données pour un niveau.
    
    Args:
        niveau: Niveau scolaire (ex: SECONDE, PREMIERE, etc.)
        file_path: Chemin vers le fichier de progression
    
    Returns:
        JSON string avec le résultat de l'opération
    """
    return update_data_source(niveau, file_path)  # Même logique

@mcp.tool()
def remove_data_source(niveau: str) -> str:
    """
    Supprime la source de données pour un niveau.
    
    Args:
        niveau: Niveau scolaire à supprimer
    
    Returns:
        JSON string avec le résultat de l'opération
    """
    try:
        preferences = load_preferences()
        niveau_upper = niveau.upper()
        
        if niveau_upper in preferences['default_data_sources']:
            del preferences['default_data_sources'][niveau_upper]
            save_preferences(preferences)  # Recharge le serveur
            
            return json.dumps({
                "status": "success",
                "message": f"Source de données supprimée pour {niveau}",
                "niveau": niveau_upper
            }, ensure_ascii=False, indent=2)
        else:
            return json.dumps({
                "status": "warning",
                "message": f"Aucune source de données configurée pour {niveau}",
                "niveau": niveau_upper
            }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Erreur dans remove_data_source: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

@mcp.tool()
def reset_preferences() -> str:
    """
    Remet les préférences aux valeurs par défaut.
    
    Returns:
        JSON string avec le résultat de l'opération
    """
    try:
        default_preferences = {
            "default_data_sources": {},
            "fallback_behavior": "show_error_message",
            "last_updated": "2025-09-11T00:00:00Z"
        }
        
        save_preferences(default_preferences)  # Recharge le serveur
        
        return json.dumps({
            "status": "success",
            "message": "Préférences remises à zéro",
            "preferences": default_preferences
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Erreur dans reset_preferences: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

@mcp.tool()
def list_configured_niveaux() -> str:
    """
    Liste tous les niveaux qui ont une source de données configurée.
    
    Returns:
        JSON string avec la liste des niveaux configurés
    """
    try:
        preferences = load_preferences()
        configured_niveaux = list(preferences.get('default_data_sources', {}).keys())
        
        return json.dumps({
            "status": "success",
            "niveaux_configures": configured_niveaux,
            "total": len(configured_niveaux)
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        logger.error(f"Erreur dans list_configured_niveaux: {e}")
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

# Modifier les fonctions existantes pour gérer les erreurs de manière plus explicite
@mcp.tool()
def search_progressions(niveau: str, query: str = "") -> str:
    """
    Recherche des entrées de progression par texte libre.
    
    Args:
        niveau: Niveau scolaire (SIXIEME, CINQUIEME, etc.)
        query: Terme de recherche optionnel (nom, description, thème, objectifs)
    
    Returns:
        JSON string avec les résultats de la recherche
    """
    try:
        if progression_server is None:
            return json.dumps({
                "success": False,
                "error": "Serveur de progression non initialisé"
            }, ensure_ascii=False, indent=2)
            
        results = progression_server.search_progressions(niveau, query)
        
        # Vérifier si aucun résultat à cause d'un niveau non configuré
        if not results and niveau.upper() not in progression_server._progression_cache:
            return json.dumps({
                "success": False,
                "niveau": niveau,
                "query": query,
                "count": 0,
                "results": [],
                "message": f"Aucune source de données configurée pour le niveau {niveau}. Utilisez 'add_data_source' pour ajouter un fichier de progression."
            }, ensure_ascii=False, indent=2)
        
        return json.dumps({
            "success": True,
            "niveau": niveau,
            "query": query,
            "count": len(results),
            "results": results
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": str(e)
        }, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # Initialisation avec préférences
    logger.info("Chargement des préférences utilisateur...")
    preferences = load_preferences()
    
    logger.info("Initialisation du serveur de progression avec préférences...")
    progression_server = ProgressionServer(DATA_DIR, preferences)
    
    logger.info("Serveur MCP Progression amélioré prêt")
    
    # Démarrage du serveur MCP
    mcp.run()