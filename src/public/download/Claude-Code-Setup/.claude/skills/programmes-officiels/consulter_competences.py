#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Programme de consultation des programmes officiels de mathématiques
Permet de rechercher et afficher les compétences par niveau, thème ou mots-clés
"""

import json
from pathlib import Path
from typing import List, Dict, Optional, Union
import re


class ConsulteurProgrammes:
    """Classe pour consulter les programmes officiels de mathématiques"""

    def __init__(self, chemin_data: Optional[str] = None):
        """
        Initialise le consulteur

        Args:
            chemin_data: Chemin vers le dossier data (par défaut : ./data)
        """
        if chemin_data is None:
            self.chemin_data = Path(__file__).parent / "data"
        else:
            self.chemin_data = Path(chemin_data)

        self.programmes = {}
        self._charger_programmes()

    def _charger_programmes(self):
        """Charge tous les programmes disponibles"""
        fichiers_json = self.chemin_data.glob("*.json")

        for fichier in fichiers_json:
            if fichier.name == "references_bo.json":
                continue

            niveau = fichier.stem
            try:
                with open(fichier, 'r', encoding='utf-8') as f:
                    self.programmes[niveau] = json.load(f)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de {fichier}: {e}")

    def lister_niveaux_disponibles(self) -> List[str]:
        """Retourne la liste des niveaux disponibles"""
        return sorted(self.programmes.keys())

    def chercher_competence(self, code: str) -> Optional[Dict]:
        """
        Recherche une compétence par son code unique

        Args:
            code: Code de la compétence (ex: "6-NC-001", "1SPE-ANA-018")

        Returns:
            Dictionnaire de la compétence ou None si non trouvée
        """
        for niveau, programme in self.programmes.items():
            if "domaines" not in programme:
                continue

            for domaine in programme["domaines"]:
                if "competences" not in domaine:
                    continue

                for competence in domaine["competences"]:
                    if competence.get("code") == code:
                        return {
                            **competence,
                            "niveau": niveau,
                            "domaine": domaine.get("nom"),
                            "domaine_code": domaine.get("code")
                        }

        return None

    def lister_competences_niveau(self, niveau: str, domaine: Optional[str] = None) -> List[Dict]:
        """
        Liste toutes les compétences d'un niveau

        Args:
            niveau: Niveau (ex: "6eme", "seconde", "premiere_spe")
            domaine: Optionnel - Code du domaine pour filtrer (ex: "NC", "ALG")

        Returns:
            Liste des compétences
        """
        if niveau not in self.programmes:
            return []

        programme = self.programmes[niveau]
        competences = []

        if "domaines" not in programme:
            return []

        for dom in programme["domaines"]:
            # Filtrer par domaine si spécifié
            if domaine and dom.get("code") != domaine:
                continue

            if "competences" not in dom:
                continue

            for comp in dom["competences"]:
                competences.append({
                    **comp,
                    "niveau": niveau,
                    "domaine": dom.get("nom"),
                    "domaine_code": dom.get("code")
                })

        return competences

    def chercher_mots_cles(self, mots_cles: Union[str, List[str]],
                          niveau: Optional[str] = None) -> List[Dict]:
        """
        Recherche des compétences contenant certains mots-clés

        Args:
            mots_cles: Mot-clé ou liste de mots-clés à rechercher
            niveau: Optionnel - Limite la recherche à un niveau

        Returns:
            Liste des compétences correspondantes
        """
        if isinstance(mots_cles, str):
            mots_cles = [mots_cles]

        # Normaliser les mots-clés (minuscules, sans accents)
        mots_cles_normalises = [self._normaliser_texte(mc) for mc in mots_cles]

        resultats = []
        programmes_a_chercher = {niveau: self.programmes[niveau]} if niveau else self.programmes

        for niv, programme in programmes_a_chercher.items():
            if "domaines" not in programme:
                continue

            for domaine in programme["domaines"]:
                if "competences" not in domaine:
                    continue

                for competence in domaine["competences"]:
                    # Rechercher dans l'intitulé, les capacités et les connaissances
                    texte_a_chercher = " ".join([
                        competence.get("intitule", ""),
                        " ".join(competence.get("capacites", [])),
                        " ".join(competence.get("connaissances", []))
                    ])

                    texte_normalise = self._normaliser_texte(texte_a_chercher)

                    # Vérifier si tous les mots-clés sont présents
                    if all(mc in texte_normalise for mc in mots_cles_normalises):
                        resultats.append({
                            **competence,
                            "niveau": niv,
                            "domaine": domaine.get("nom"),
                            "domaine_code": domaine.get("code")
                        })

        return resultats

    def chercher_par_theme(self, niveau: str, theme: str) -> List[Dict]:
        """
        Recherche des compétences liées à un thème

        Args:
            niveau: Niveau à consulter
            theme: Thème à rechercher (ex: "fractions", "dérivée", "pythagore")

        Returns:
            Liste des compétences du thème
        """
        return self.chercher_mots_cles(theme, niveau)

    def afficher_competence(self, competence: Dict, detaille: bool = True):
        """
        Affiche une compétence de manière formatée

        Args:
            competence: Dictionnaire de la compétence
            detaille: Si True, affiche tous les détails
        """
        print(f"\n{'='*80}")
        print(f"[{competence['code']}] {competence['intitule']}")
        print(f"{'='*80}")
        print(f"Niveau : {competence.get('niveau', 'N/A')}")
        print(f"Domaine : {competence.get('domaine', 'N/A')} ({competence.get('domaine_code', 'N/A')})")

        if detaille:
            if competence.get("capacites"):
                print(f"\n📌 Capacités attendues :")
                for cap in competence["capacites"]:
                    print(f"  • {cap}")

            if competence.get("connaissances"):
                print(f"\n📚 Connaissances :")
                for conn in competence["connaissances"]:
                    print(f"  • {conn}")

            if competence.get("attendus"):
                print(f"\n🎯 Attendus : {competence['attendus']}")

            if competence.get("commentaires"):
                print(f"\n💬 Commentaires : {competence['commentaires']}")

        print(f"{'='*80}\n")

    def statistiques_niveau(self, niveau: str) -> Dict:
        """
        Calcule les statistiques d'un niveau

        Args:
            niveau: Niveau à analyser

        Returns:
            Dictionnaire avec les statistiques
        """
        if niveau not in self.programmes:
            return {}

        programme = self.programmes[niveau]
        stats = {
            "niveau": niveau,
            "nb_domaines": len(programme.get("domaines", [])),
            "nb_competences_total": 0,
            "par_domaine": {}
        }

        for domaine in programme.get("domaines", []):
            nb_comp = len(domaine.get("competences", []))
            stats["nb_competences_total"] += nb_comp
            stats["par_domaine"][domaine.get("nom")] = nb_comp

        return stats

    @staticmethod
    def _normaliser_texte(texte: str) -> str:
        """Normalise un texte pour la recherche (minuscules, sans accents)"""
        # Minuscules
        texte = texte.lower()

        # Supprimer les accents
        accents = {
            'à': 'a', 'â': 'a', 'ä': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'î': 'i', 'ï': 'i',
            'ô': 'o', 'ö': 'o',
            'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c'
        }
        for accent, sans_accent in accents.items():
            texte = texte.replace(accent, sans_accent)

        return texte


# ==================== Fonctions utilitaires ====================

def chercher_competence(code: str) -> Optional[Dict]:
    """Recherche une compétence par code"""
    consulteur = ConsulteurProgrammes()
    return consulteur.chercher_competence(code)


def lister_competences_niveau(niveau: str, domaine: Optional[str] = None) -> List[Dict]:
    """Liste les compétences d'un niveau"""
    consulteur = ConsulteurProgrammes()
    return consulteur.lister_competences_niveau(niveau, domaine)


def chercher_mots_cles(mots_cles: Union[str, List[str]],
                       niveau: Optional[str] = None) -> List[Dict]:
    """Recherche par mots-clés"""
    consulteur = ConsulteurProgrammes()
    return consulteur.chercher_mots_cles(mots_cles, niveau)


def chercher_par_theme(niveau: str, theme: str) -> List[Dict]:
    """Recherche par thème"""
    consulteur = ConsulteurProgrammes()
    return consulteur.chercher_par_theme(niveau, theme)


# ==================== Interface en ligne de commande ====================

def main():
    """Interface en ligne de commande"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Consulter les programmes officiels de mathématiques"
    )

    subparsers = parser.add_subparsers(dest="commande", help="Commande à exécuter")

    # Commande: lister les niveaux
    subparsers.add_parser("niveaux", help="Lister les niveaux disponibles")

    # Commande: chercher une compétence
    parser_code = subparsers.add_parser("code", help="Chercher une compétence par code")
    parser_code.add_argument("code", help="Code de la compétence (ex: 6-NC-001)")

    # Commande: lister les compétences d'un niveau
    parser_niveau = subparsers.add_parser("niveau", help="Lister les compétences d'un niveau")
    parser_niveau.add_argument("niveau", help="Niveau (ex: 6eme, seconde)")
    parser_niveau.add_argument("--domaine", help="Filtrer par domaine (ex: NC, ALG)")

    # Commande: recherche par mots-clés
    parser_recherche = subparsers.add_parser("recherche", help="Rechercher par mots-clés")
    parser_recherche.add_argument("mots_cles", nargs="+", help="Mots-clés à rechercher")
    parser_recherche.add_argument("--niveau", help="Limiter à un niveau")

    # Commande: statistiques
    parser_stats = subparsers.add_parser("stats", help="Statistiques d'un niveau")
    parser_stats.add_argument("niveau", help="Niveau à analyser")

    args = parser.parse_args()

    consulteur = ConsulteurProgrammes()

    # Exécution des commandes
    if args.commande == "niveaux":
        print("\n📚 Niveaux disponibles :")
        for niveau in consulteur.lister_niveaux_disponibles():
            stats = consulteur.statistiques_niveau(niveau)
            print(f"  • {niveau} ({stats['nb_competences_total']} compétences)")

    elif args.commande == "code":
        comp = consulteur.chercher_competence(args.code)
        if comp:
            consulteur.afficher_competence(comp)
        else:
            print(f"❌ Compétence {args.code} non trouvée")

    elif args.commande == "niveau":
        competences = consulteur.lister_competences_niveau(args.niveau, args.domaine)
        print(f"\n📋 {len(competences)} compétences trouvées pour {args.niveau}")
        if args.domaine:
            print(f"   (domaine : {args.domaine})")

        for comp in competences:
            consulteur.afficher_competence(comp, detaille=False)

    elif args.commande == "recherche":
        competences = consulteur.chercher_mots_cles(args.mots_cles, args.niveau)
        print(f"\n🔍 {len(competences)} compétences trouvées")

        for comp in competences:
            consulteur.afficher_competence(comp, detaille=False)

    elif args.commande == "stats":
        stats = consulteur.statistiques_niveau(args.niveau)
        if stats:
            print(f"\n📊 Statistiques pour {args.niveau}")
            print(f"  Nombre de domaines : {stats['nb_domaines']}")
            print(f"  Nombre total de compétences : {stats['nb_competences_total']}")
            print(f"\n  Répartition par domaine :")
            for domaine, nb in stats['par_domaine'].items():
                print(f"    • {domaine} : {nb} compétences")
        else:
            print(f"❌ Niveau {args.niveau} non trouvé")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
