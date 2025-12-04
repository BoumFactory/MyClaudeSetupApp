"""
Scraper HTML pour extraire les liens de téléchargement des fiches problème
Configuration facilement modifiable via scraper_config.json
"""

import requests
from bs4 import BeautifulSoup
import json
import time
from pathlib import Path
from typing import Dict, Optional, List
from urllib.parse import urljoin


class ProblemathequeHTMLScraper:
    """Scraper HTML pour extraire les liens de téléchargement"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialise le scraper

        Args:
            config_path: Chemin vers le fichier de configuration JSON
        """
        if config_path is None:
            config_path = Path(__file__).parent / "scraper_config.json"

        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.base_url = self.config['base_url']
        self.selectors = self.config['html_selectors']
        self.user_agent = self.config['user_agent']
        self.timeout = self.config['timeout_seconds']

        # Rate limiting
        self.last_request_time = 0
        self.min_interval = 1.0 / self.config['rate_limiting']['requests_per_second']

    def _rate_limit(self):
        """Applique le rate limiting"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()

    def _fetch_html(self, url: str) -> BeautifulSoup:
        """
        Récupère et parse le HTML d'une page

        Args:
            url: URL de la page

        Returns:
            Objet BeautifulSoup
        """
        self._rate_limit()

        headers = {'User-Agent': self.user_agent}

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')

        except requests.exceptions.RequestException as e:
            raise Exception(f"❌ Erreur fetch HTML: {e}")

    def _extract_link(self, soup: BeautifulSoup, selector_config: Dict) -> Optional[str]:
        """
        Extrait un lien depuis le HTML avec un sélecteur

        Args:
            soup: Objet BeautifulSoup
            selector_config: Configuration du sélecteur (selector, attribute)

        Returns:
            URL du lien ou None
        """
        selector = selector_config['selector']
        attribute = selector_config.get('attribute', 'href')

        # Tester tous les sélecteurs (séparés par virgule)
        for sel in selector.split(','):
            sel = sel.strip()
            element = soup.select_one(sel)

            if element:
                link = element.get(attribute)
                if link:
                    # Convertir en URL absolue si nécessaire
                    return urljoin(self.base_url, link)

        return None

    def extract_download_links(self, fiche_url: str) -> Dict[str, Optional[str]]:
        """
        Extrait tous les liens de téléchargement d'une fiche

        Args:
            fiche_url: URL de la fiche problème

        Returns:
            Dictionnaire des liens de téléchargement par format
            {
                'pdf_enseignant': 'https://...',
                'docx_enseignant': 'https://...',
                'odt_enseignant': 'https://...',
                'pdf_eleve': 'https://...'
            }
        """
        try:
            soup = self._fetch_html(fiche_url)

            links = {}
            download_selectors = self.selectors['download_links']

            for format_name, selector_config in download_selectors.items():
                link = self._extract_link(soup, selector_config)
                links[format_name] = link

            # Si aucun lien trouvé, essayer le fallback
            if not any(links.values()):
                print(f"⚠️  Aucun lien trouvé avec sélecteurs principaux, essai fallback...")
                links = self._fallback_extraction(soup)

            return links

        except Exception as e:
            print(f"❌ Erreur extraction liens: {e}")
            return {
                'pdf_enseignant': None,
                'docx_enseignant': None,
                'odt_enseignant': None,
                'pdf_eleve': None
            }

    def _fallback_extraction(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        """
        Méthode de secours pour extraire les liens

        Args:
            soup: Objet BeautifulSoup

        Returns:
            Dictionnaire des liens trouvés
        """
        links = {
            'pdf_enseignant': None,
            'docx_enseignant': None,
            'odt_enseignant': None,
            'pdf_eleve': None
        }

        fallback_selector = self.selectors['fallback']['all_download_links']
        all_links = soup.select(fallback_selector)

        for link_elem in all_links:
            href = link_elem.get('href', '')
            full_url = urljoin(self.base_url, href)

            # Déterminer le type
            if 'enseignant' in href.lower():
                if href.endswith('.pdf'):
                    links['pdf_enseignant'] = full_url
                elif href.endswith('.docx'):
                    links['docx_enseignant'] = full_url
                elif href.endswith('.odt'):
                    links['odt_enseignant'] = full_url

            elif 'eleve' in href.lower() or 'élève' in href.lower():
                if href.endswith('.pdf'):
                    links['pdf_eleve'] = full_url

        return links

    def get_download_links_summary(self, links: Dict[str, Optional[str]]) -> str:
        """
        Formate un résumé des liens de téléchargement

        Args:
            links: Dictionnaire des liens

        Returns:
            Résumé formaté
        """
        summary_lines = ["💾 Formats disponibles :"]

        format_labels = {
            'pdf_enseignant': '  📄 PDF Enseignant',
            'docx_enseignant': '  📝 DOCX Enseignant',
            'odt_enseignant': '  📝 ODT Enseignant',
            'pdf_eleve': '  📄 PDF Élève'
        }

        for format_key, label in format_labels.items():
            if links.get(format_key):
                summary_lines.append(f"{label} : ✅")
            else:
                summary_lines.append(f"{label} : ❌")

        return '\n'.join(summary_lines)

    def download_file(self, url: str, output_path: Path) -> bool:
        """
        Télécharge un fichier

        Args:
            url: URL du fichier
            output_path: Chemin de destination

        Returns:
            True si succès, False sinon
        """
        try:
            self._rate_limit()

            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout, stream=True)
            response.raise_for_status()

            # Créer le dossier parent si nécessaire
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Télécharger
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Téléchargé : {output_path.name}")
            return True

        except Exception as e:
            print(f"❌ Erreur téléchargement: {e}")
            return False


class DownloadLinkCache:
    """Cache persistant pour les liens de téléchargement"""

    def __init__(self, cache_file: Optional[Path] = None):
        """
        Initialise le cache

        Args:
            cache_file: Chemin du fichier de cache
        """
        if cache_file is None:
            cache_file = Path(__file__).parent / "download_links_cache.json"

        self.cache_file = cache_file
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        """Charge le cache depuis le fichier"""
        if not self.cache_file.exists():
            return {}

        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Erreur chargement cache téléchargements: {e}")
            return {}

    def _save_cache(self):
        """Sauvegarde le cache"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Erreur sauvegarde cache téléchargements: {e}")

    def get(self, fiche_slug: str) -> Optional[Dict]:
        """
        Récupère les liens depuis le cache

        Args:
            fiche_slug: Slug de la fiche

        Returns:
            Dictionnaire des liens ou None
        """
        return self.cache.get(fiche_slug)

    def set(self, fiche_slug: str, links: Dict):
        """
        Stocke les liens dans le cache

        Args:
            fiche_slug: Slug de la fiche
            links: Dictionnaire des liens
        """
        self.cache[fiche_slug] = {
            'links': links,
            'cached_at': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        self._save_cache()


if __name__ == "__main__":
    # Exemple d'utilisation
    scraper = ProblemathequeHTMLScraper()
    cache = DownloadLinkCache()

    print("=== Test Scraper HTML Problémathèque ===\n")

    # Test sur une fiche
    test_url = "https://www.problematheque-csen.fr/fiche-probleme/la-cigale-et-la-fourmi/"
    test_slug = "la-cigale-et-la-fourmi"

    print(f"🔍 Test extraction : {test_url}\n")

    # Vérifier cache
    cached_links = cache.get(test_slug)
    if cached_links:
        print(f"📦 Liens trouvés dans le cache (mis à jour : {cached_links['cached_at']})")
        links = cached_links['links']
    else:
        print("🌐 Extraction depuis le site...")
        links = scraper.extract_download_links(test_url)
        cache.set(test_slug, links)

    print(f"\n{scraper.get_download_links_summary(links)}\n")

    # Afficher les URLs
    for format_name, url in links.items():
        if url:
            print(f"  {format_name}: {url}")

    print(f"\n✅ Test terminé")
