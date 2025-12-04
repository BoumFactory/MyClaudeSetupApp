"""
Client API REST pour la Problémathèque CSEN
Gère les requêtes vers l'API WordPress pour rechercher et filtrer les fiches problème.
"""

import requests
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta


class ProblemathequeAPIClient:
    """Client pour l'API REST de la Problémathèque CSEN"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise le client API

        Args:
            config_path: Chemin vers le fichier de configuration JSON
        """
        if config_path is None:
            config_path = Path(__file__).parent / "scraper_config.json"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.base_url = self.config['base_url']
        self.api_base = f"{self.base_url}{self.config['api']['base']}"
        self.endpoints = self.config['api']['endpoints']
        self.user_agent = self.config['user_agent']
        self.timeout = self.config['timeout_seconds']

        # Rate limiting
        self.last_request_time = 0
        self.min_interval = 1.0 / self.config['rate_limiting']['requests_per_second']

        # Cache
        self.cache_enabled = self.config['cache']['enabled']
        self.cache_ttl = timedelta(seconds=self.config['cache']['ttl_seconds'])
        self.cache_file = Path(__file__).parent / self.config['cache']['file']
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Charge le cache depuis le fichier JSON"""
        if not self.cache_enabled or not self.cache_file.exists():
            return {}

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
                # Nettoyer les entrées expirées
                now = datetime.now().isoformat()
                return {k: v for k, v in cache.items()
                       if datetime.fromisoformat(v.get('cached_at', '2000-01-01')) + self.cache_ttl > datetime.now()}
        except Exception as e:
            print(f"⚠️  Erreur chargement cache: {e}")
            return {}

    def _save_cache(self):
        """Sauvegarde le cache dans le fichier JSON"""
        if not self.cache_enabled:
            return

        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde cache: {e}")

    def _rate_limit(self):
        """Applique le rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Optional[Dict] = None, use_cache: bool = True) -> Dict:
        """
        Effectue une requête HTTP vers l'API

        Args:
            endpoint: Endpoint de l'API
            params: Paramètres de requête
            use_cache: Utiliser le cache si disponible

        Returns:
            Réponse JSON
        """
        url = f"{self.api_base}{endpoint}"
        cache_key = f"{url}:{json.dumps(params, sort_keys=True)}"

        # Vérifier le cache
        if use_cache and cache_key in self.cache:
            return self.cache[cache_key]['data']

        # Effectuer la requête
        self._rate_limit()

        headers = {'User-Agent': self.user_agent}

        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # Mettre en cache
            if use_cache:
                self.cache[cache_key] = {
                    'data': data,
                    'cached_at': datetime.now().isoformat()
                }
                self._save_cache()

            return data

        except requests.exceptions.RequestException as e:
            raise Exception(f"❌ Erreur requête API: {e}")

    def get_cycles(self) -> List[Dict]:
        """
        Récupère la liste des cycles scolaires

        Returns:
            Liste des cycles avec ID, nom, slug, count
        """
        return self._make_request(self.endpoints['cycles'])

    def get_domaines(self) -> List[Dict]:
        """
        Récupère la liste des domaines mathématiques

        Returns:
            Liste des domaines avec ID, nom, slug, count
        """
        return self._make_request(self.endpoints['domaines'])

    def get_mots_cles(self) -> List[Dict]:
        """
        Récupère la liste des mots-clés disponibles

        Returns:
            Liste des mots-clés avec ID, nom, slug, count
        """
        return self._make_request(self.endpoints['mots_cles'])

    def search_fiches(
        self,
        search: Optional[str] = None,
        cycle_ids: Optional[List[int]] = None,
        domaine_ids: Optional[List[int]] = None,
        mot_cle_ids: Optional[List[int]] = None,
        per_page: int = 20,
        page: int = 1,
        orderby: str = 'date',
        order: str = 'desc'
    ) -> List[Dict]:
        """
        Recherche des fiches problème avec filtres

        Args:
            search: Recherche textuelle
            cycle_ids: IDs des cycles (ex: [10, 12] pour Cycle 3 et 4)
            domaine_ids: IDs des domaines
            mot_cle_ids: IDs des mots-clés
            per_page: Nombre de résultats par page
            page: Numéro de page
            orderby: Tri (date, title, relevance)
            order: Ordre (asc, desc)

        Returns:
            Liste des fiches problème
        """
        params = {
            'per_page': per_page,
            'page': page,
            'orderby': orderby,
            'order': order
        }

        if search:
            params['search'] = search

        if cycle_ids:
            params['cycle'] = ','.join(map(str, cycle_ids))

        if domaine_ids:
            params['domaine'] = ','.join(map(str, domaine_ids))

        if mot_cle_ids:
            params['mot-cle'] = ','.join(map(str, mot_cle_ids))

        return self._make_request(self.endpoints['fiches'], params)

    def get_fiche_by_slug(self, slug: str) -> Optional[Dict]:
        """
        Récupère une fiche par son slug

        Args:
            slug: Slug de la fiche (ex: "la-cigale-et-la-fourmi")

        Returns:
            Données de la fiche ou None si non trouvée
        """
        params = {'slug': slug}
        results = self._make_request(self.endpoints['fiches'], params)

        return results[0] if results else None

    def get_fiche_by_id(self, fiche_id: int) -> Dict:
        """
        Récupère une fiche par son ID

        Args:
            fiche_id: ID de la fiche

        Returns:
            Données de la fiche
        """
        endpoint = f"{self.endpoints['fiches']}/{fiche_id}"
        return self._make_request(endpoint)

    def resolve_taxonomy_names(self, fiche: Dict) -> Dict:
        """
        Résout les noms des taxonomies (cycles, domaines, mots-clés) d'une fiche

        Args:
            fiche: Données de la fiche avec IDs de taxonomies

        Returns:
            Fiche enrichie avec noms des taxonomies
        """
        # Récupérer les mappings
        cycles = {c['id']: c['name'] for c in self.get_cycles()}
        domaines = {d['id']: d['name'] for d in self.get_domaines()}
        mots_cles = {m['id']: m['name'] for m in self.get_mots_cles()}

        # Résoudre les noms
        fiche['cycle_names'] = [cycles.get(cid, f"Cycle {cid}") for cid in fiche.get('cycle', [])]
        fiche['domaine_names'] = [domaines.get(did, f"Domaine {did}") for did in fiche.get('domaine', [])]
        fiche['mot_cle_names'] = [mots_cles.get(mid, f"Tag {mid}") for mid in fiche.get('mot-cle', [])]

        return fiche

    def format_fiche_summary(self, fiche: Dict) -> str:
        """
        Formate un résumé textuel d'une fiche

        Args:
            fiche: Données de la fiche (enrichie avec taxonomies)

        Returns:
            Résumé formaté en texte
        """
        title = fiche.get('title', {}).get('rendered', 'Sans titre')
        cycles = ', '.join(fiche.get('cycle_names', []))
        domaines = ', '.join(fiche.get('domaine_names', []))
        mots_cles = ', '.join(fiche.get('mot_cle_names', [])[:5])  # Max 5 mots-clés
        url = fiche.get('link', '')

        summary = f"""
📚 {title}

📖 Cycles : {cycles}
🔢 Domaines : {domaines}
🏷️  Mots-clés : {mots_cles}
🔗 URL : {url}
""".strip()

        return summary


if __name__ == "__main__":
    # Exemple d'utilisation
    client = ProblemathequeAPIClient()

    print("=== Test Client API Problémathèque ===\n")

    # Lister les cycles
    print("📚 Cycles disponibles:")
    cycles = client.get_cycles()
    for cycle in cycles:
        print(f"  - {cycle['name']} (ID: {cycle['id']}, {cycle['count']} problèmes)")

    print("\n🔢 Domaines disponibles:")
    domaines = client.get_domaines()
    for domaine in domaines[:5]:  # Afficher 5 premiers
        print(f"  - {domaine['name']} (ID: {domaine['id']}, {domaine['count']} problèmes)")

    # Recherche
    print("\n🔍 Recherche 'fraction' :")
    results = client.search_fiches(search="fraction", per_page=3)
    for fiche in results:
        fiche_enrichie = client.resolve_taxonomy_names(fiche)
        print(f"\n{client.format_fiche_summary(fiche_enrichie)}")

    print(f"\n✅ Test terminé")
