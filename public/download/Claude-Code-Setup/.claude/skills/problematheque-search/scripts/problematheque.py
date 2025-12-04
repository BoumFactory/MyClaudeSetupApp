#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script principal pour rechercher et télécharger des problèmes de la Problémathèque CSEN
Utilise le client API REST et le scraper HTML
"""

import argparse
import json
import sys
import io
from pathlib import Path
from typing import List, Dict, Optional

# Configurer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Ajouter le dossier scripts au path
sys.path.insert(0, str(Path(__file__).parent))

from api_client import ProblemathequeAPIClient
from html_scraper import ProblemathequeHTMLScraper, DownloadLinkCache


class ProblemathequeSearch:
    """Interface principale pour rechercher des problèmes"""

    def __init__(self):
        self.api_client = ProblemathequeAPIClient()
        self.html_scraper = ProblemathequeHTMLScraper()
        self.download_cache = DownloadLinkCache()

    def search(
        self,
        query: Optional[str] = None,
        cycles: Optional[List[str]] = None,
        domaines: Optional[List[str]] = None,
        keywords: Optional[List[str]] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Recherche des problèmes avec critères

        Args:
            query: Recherche textuelle
            cycles: Liste de cycles (ex: ['cycle-3', 'cycle-4'] ou ['3', '4'])
            domaines: Liste de domaines (slugs ou noms partiels)
            keywords: Liste de mots-clés
            limit: Nombre maximum de résultats

        Returns:
            Liste des fiches problème enrichies
        """
        # Résoudre les IDs de taxonomies
        cycle_ids = self._resolve_cycle_ids(cycles) if cycles else None
        domaine_ids = self._resolve_domaine_ids(domaines) if domaines else None
        keyword_ids = self._resolve_keyword_ids(keywords) if keywords else None

        # Rechercher
        results = self.api_client.search_fiches(
            search=query,
            cycle_ids=cycle_ids,
            domaine_ids=domaine_ids,
            mot_cle_ids=keyword_ids,
            per_page=limit
        )

        # Enrichir avec les noms de taxonomies
        enriched_results = []
        for fiche in results:
            enriched = self.api_client.resolve_taxonomy_names(fiche)
            enriched_results.append(enriched)

        return enriched_results

    def _resolve_cycle_ids(self, cycle_slugs: List[str]) -> List[int]:
        """Résout les slugs de cycles en IDs"""
        all_cycles = self.api_client.get_cycles()

        ids = []
        for slug in cycle_slugs:
            # Normaliser : '3' -> 'cycle-3', 'Cycle 3' -> 'cycle-3'
            normalized = slug.lower().strip()
            if normalized.isdigit():
                normalized = f"cycle-{normalized}"
            elif not normalized.startswith('cycle'):
                normalized = f"cycle-{normalized}"

            # Trouver l'ID
            for cycle in all_cycles:
                if cycle['slug'] == normalized or str(cycle['id']) == slug:
                    ids.append(cycle['id'])
                    break

        return ids

    def _resolve_domaine_ids(self, domaine_slugs: List[str]) -> List[int]:
        """Résout les slugs de domaines en IDs"""
        all_domaines = self.api_client.get_domaines()

        ids = []
        for slug in domaine_slugs:
            normalized = slug.lower().strip()

            # Recherche exacte par slug ou partielle par nom
            for domaine in all_domaines:
                if (domaine['slug'] == normalized or
                    normalized in domaine['name'].lower() or
                    str(domaine['id']) == slug):
                    ids.append(domaine['id'])
                    break

        return ids

    def _resolve_keyword_ids(self, keyword_slugs: List[str]) -> List[int]:
        """Résout les slugs de mots-clés en IDs"""
        all_keywords = self.api_client.get_mots_cles()

        ids = []
        for slug in keyword_slugs:
            normalized = slug.lower().strip()

            for keyword in all_keywords:
                if (keyword['slug'] == normalized or
                    normalized in keyword['name'].lower() or
                    str(keyword['id']) == slug):
                    ids.append(keyword['id'])
                    break

        return ids

    def get_download_links(self, fiche_slug: str) -> Dict[str, Optional[str]]:
        """
        Récupère les liens de téléchargement d'une fiche

        Args:
            fiche_slug: Slug de la fiche

        Returns:
            Dictionnaire des liens de téléchargement
        """
        # Vérifier le cache
        cached = self.download_cache.get(fiche_slug)
        if cached:
            return cached['links']

        # Récupérer la fiche pour avoir l'URL
        fiche = self.api_client.get_fiche_by_slug(fiche_slug)
        if not fiche:
            raise ValueError(f"❌ Fiche '{fiche_slug}' non trouvée")

        fiche_url = fiche['link']

        # Extraire les liens
        links = self.html_scraper.extract_download_links(fiche_url)

        # Mettre en cache
        self.download_cache.set(fiche_slug, links)

        return links

    def download_fiche(
        self,
        fiche_slug: str,
        format_type: str = 'pdf_enseignant',
        output_dir: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Télécharge une fiche

        Args:
            fiche_slug: Slug de la fiche
            format_type: Type de format (pdf_enseignant, docx_enseignant, etc.)
            output_dir: Dossier de destination

        Returns:
            Chemin du fichier téléchargé ou None
        """
        if output_dir is None:
            output_dir = Path.cwd() / "ressources-problematheque"

        # Récupérer les liens
        links = self.get_download_links(fiche_slug)

        download_url = links.get(format_type)
        if not download_url:
            print(f"❌ Format '{format_type}' non disponible pour '{fiche_slug}'")
            return None

        # Déterminer le nom de fichier
        extension = format_type.split('_')[0]  # pdf, docx, odt
        filename = f"{fiche_slug}-{format_type}.{extension}"
        output_path = output_dir / filename

        # Télécharger
        success = self.html_scraper.download_file(download_url, output_path)

        return output_path if success else None

    def format_results(self, results: List[Dict], include_links: bool = False) -> str:
        """
        Formate les résultats de recherche

        Args:
            results: Liste des fiches
            include_links: Inclure les liens de téléchargement

        Returns:
            Texte formaté
        """
        if not results:
            return "❌ Aucun problème trouvé"

        output = [f"📚 {len(results)} problème(s) trouvé(s) :\n"]

        for i, fiche in enumerate(results, 1):
            title = fiche.get('title', {}).get('rendered', 'Sans titre')
            cycles = ', '.join(fiche.get('cycle_names', []))
            domaines = ', '.join(fiche.get('domaine_names', []))
            mots_cles = ', '.join(fiche.get('mot_cle_names', [])[:5])
            url = fiche.get('link', '')
            slug = fiche.get('slug', '')

            output.append(f"{i}. {title}")
            output.append(f"   📖 Cycles : {cycles}")
            output.append(f"   🔢 Domaines : {domaines}")
            output.append(f"   🏷️  Mots-clés : {mots_cles}")
            output.append(f"   🔗 URL : {url}")

            if include_links:
                # Récupérer les liens de téléchargement
                try:
                    links = self.get_download_links(slug)
                    output.append("   💾 Téléchargements :")
                    if links.get('pdf_enseignant'):
                        output.append("      📄 PDF Enseignant ✅")
                    if links.get('docx_enseignant'):
                        output.append("      📝 DOCX Enseignant ✅")
                except Exception as e:
                    output.append(f"   ⚠️  Erreur liens: {e}")

            output.append("")

        return '\n'.join(output)


def main():
    """Point d'entrée CLI"""
    parser = argparse.ArgumentParser(
        description="Recherche de problèmes dans la Problémathèque CSEN"
    )

    parser.add_argument('query', nargs='?', help="Recherche textuelle")
    parser.add_argument('--cycles', '-c', nargs='+', help="Cycles (ex: 3 4 lycee)")
    parser.add_argument('--domaines', '-d', nargs='+', help="Domaines (ex: geometrie algebre)")
    parser.add_argument('--keywords', '-k', nargs='+', help="Mots-clés")
    parser.add_argument('--limit', '-l', type=int, default=10, help="Nombre de résultats")
    parser.add_argument('--json', action='store_true', help="Sortie JSON")
    parser.add_argument('--download', help="Télécharger une fiche (slug)")
    parser.add_argument('--format', default='pdf_enseignant',
                       choices=['pdf_enseignant', 'docx_enseignant', 'odt_enseignant', 'pdf_eleve'],
                       help="Format de téléchargement")
    parser.add_argument('--output', '-o', type=Path, help="Dossier de téléchargement")
    parser.add_argument('--links', action='store_true', help="Inclure les liens de téléchargement")

    args = parser.parse_args()

    searcher = ProblemathequeSearch()

    # Mode téléchargement
    if args.download:
        output_path = searcher.download_fiche(
            args.download,
            format_type=args.format,
            output_dir=args.output
        )
        if output_path:
            print(f"✅ Téléchargé : {output_path}")
        sys.exit(0 if output_path else 1)

    # Mode recherche
    results = searcher.search(
        query=args.query,
        cycles=args.cycles,
        domaines=args.domaines,
        keywords=args.keywords,
        limit=args.limit
    )

    if args.json:
        # Sortie JSON
        output = []
        for fiche in results:
            output.append({
                'slug': fiche['slug'],
                'title': fiche['title']['rendered'],
                'url': fiche['link'],
                'cycles': fiche['cycle_names'],
                'domaines': fiche['domaine_names'],
                'mots_cles': fiche['mot_cle_names']
            })
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # Sortie texte formatée
        print(searcher.format_results(results, include_links=args.links))


if __name__ == "__main__":
    main()
