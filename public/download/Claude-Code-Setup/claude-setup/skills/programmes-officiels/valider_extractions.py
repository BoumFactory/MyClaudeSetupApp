#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de validation et scoring des extractions de programmes officiels
Compare les JSON extraits avec les PDFs sources du BO
Attribue un score de conformité de 0 à 100%
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
import PyPDF2
import re


class ValidateurExtraction:
    """Valide une extraction de programme officiel"""

    def __init__(self, fichier_json: str, fichier_pdf: str):
        """
        Initialise le validateur

        Args:
            fichier_json: Chemin vers le fichier JSON extrait
            fichier_pdf: Chemin vers le PDF source du BO
        """
        self.fichier_json = Path(fichier_json)
        self.fichier_pdf = Path(fichier_pdf)
        self.json_data = None
        self.pdf_text = None
        self.rapport = {
            "fichier": str(self.fichier_json.name),
            "score_global": 0,
            "scores_details": {},
            "erreurs": [],
            "avertissements": [],
            "statistiques": {}
        }

    def charger_donnees(self) -> bool:
        """Charge les données JSON et PDF"""
        try:
            # Charger JSON
            with open(self.fichier_json, 'r', encoding='utf-8') as f:
                self.json_data = json.load(f)

            # Charger PDF
            with open(self.fichier_pdf, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                self.pdf_text = ""
                for page in pdf_reader.pages:
                    self.pdf_text += page.extract_text() + "\n"

            return True

        except Exception as e:
            self.rapport["erreurs"].append(f"Erreur de chargement : {e}")
            return False

    def valider_structure(self) -> int:
        """
        Valide la structure du JSON
        Retourne un score de 0 à 100
        """
        score = 0
        points_structure = {
            "niveau": 10,
            "reference_bo": 5,
            "domaines": 15,
            "competences_existantes": 20
        }

        # Vérifier champ 'niveau'
        if "niveau" in self.json_data:
            score += points_structure["niveau"]
        else:
            self.rapport["erreurs"].append("Champ 'niveau' manquant")

        # Vérifier référence BO
        if "reference_bo" in self.json_data or "bo_reference" in self.json_data:
            score += points_structure["reference_bo"]
        else:
            self.rapport["avertissements"].append("Référence BO manquante")

        # Vérifier domaines
        if "domaines" in self.json_data:
            score += points_structure["domaines"]

            # Vérifier que chaque domaine a des compétences
            nb_domaines_avec_comp = 0
            for domaine in self.json_data["domaines"]:
                if "competences" in domaine and len(domaine["competences"]) > 0:
                    nb_domaines_avec_comp += 1

            if nb_domaines_avec_comp == len(self.json_data["domaines"]):
                score += points_structure["competences_existantes"]
            else:
                score += (nb_domaines_avec_comp / len(self.json_data["domaines"])) * points_structure["competences_existantes"]
                self.rapport["avertissements"].append(
                    f"{nb_domaines_avec_comp}/{len(self.json_data['domaines'])} domaines ont des compétences"
                )
        else:
            self.rapport["erreurs"].append("Champ 'domaines' manquant")

        self.rapport["scores_details"]["structure"] = score
        return int(score)

    def valider_codes_uniques(self) -> int:
        """
        Vérifie que tous les codes de compétences sont uniques
        Retourne un score de 0 à 100
        """
        if "domaines" not in self.json_data:
            return 0

        codes = []
        codes_dupliques = []

        for domaine in self.json_data["domaines"]:
            if "competences" not in domaine:
                continue

            for comp in domaine["competences"]:
                code = comp.get("code")
                if code:
                    if code in codes:
                        codes_dupliques.append(code)
                    codes.append(code)

        if not codes:
            self.rapport["erreurs"].append("Aucun code de compétence trouvé")
            return 0

        if codes_dupliques:
            score = max(0, 100 - len(codes_dupliques) * 10)
            self.rapport["erreurs"].append(f"Codes dupliqués : {', '.join(codes_dupliques)}")
        else:
            score = 100

        self.rapport["scores_details"]["codes_uniques"] = score
        return score

    def valider_completude_competences(self) -> int:
        """
        Vérifie que chaque compétence a tous les champs requis
        Retourne un score de 0 à 100
        """
        if "domaines" not in self.json_data:
            return 0

        champs_requis = ["code", "intitule"]
        champs_optionnels = ["capacites", "connaissances", "attendus"]

        nb_total = 0
        nb_completes = 0
        nb_avec_optionnels = 0

        for domaine in self.json_data["domaines"]:
            if "competences" not in domaine:
                continue

            for comp in domaine["competences"]:
                nb_total += 1

                # Vérifier champs requis
                if all(champ in comp for champ in champs_requis):
                    nb_completes += 1

                # Vérifier champs optionnels
                nb_opt = sum(1 for champ in champs_optionnels if champ in comp and comp[champ])
                if nb_opt >= 2:  # Au moins 2 champs optionnels remplis
                    nb_avec_optionnels += 1

        if nb_total == 0:
            return 0

        score_requis = (nb_completes / nb_total) * 60
        score_optionnels = (nb_avec_optionnels / nb_total) * 40
        score = int(score_requis + score_optionnels)

        self.rapport["statistiques"]["nb_competences_total"] = nb_total
        self.rapport["statistiques"]["nb_competences_completes"] = nb_completes

        if score < 100:
            self.rapport["avertissements"].append(
                f"{nb_completes}/{nb_total} compétences ont tous les champs requis"
            )

        self.rapport["scores_details"]["completude"] = score
        return score

    def valider_correspondance_bo(self) -> int:
        """
        Vérifie que les compétences correspondent au BO
        Recherche les intitulés dans le PDF source
        Retourne un score de 0 à 100
        """
        if not self.pdf_text or "domaines" not in self.json_data:
            return 0

        # Normaliser le texte du PDF
        pdf_normalise = self._normaliser_texte(self.pdf_text)

        nb_total = 0
        nb_trouvees = 0
        nb_partielles = 0

        for domaine in self.json_data["domaines"]:
            if "competences" not in domaine:
                continue

            for comp in domaine["competences"]:
                nb_total += 1
                intitule = comp.get("intitule", "")

                if not intitule:
                    continue

                # Normaliser l'intitulé
                intitule_normalise = self._normaliser_texte(intitule)

                # Recherche exacte (au moins 80% de l'intitulé)
                mots_intitule = intitule_normalise.split()
                if len(mots_intitule) >= 3:
                    # Chercher les 3 premiers mots significatifs
                    debut_intitule = " ".join(mots_intitule[:3])

                    if debut_intitule in pdf_normalise:
                        nb_trouvees += 1
                    else:
                        # Recherche partielle (au moins 2 mots trouvés)
                        mots_trouves = sum(1 for mot in mots_intitule if mot in pdf_normalise and len(mot) > 3)
                        if mots_trouves >= 2:
                            nb_partielles += 1

        if nb_total == 0:
            return 0

        # Score : 100% si tout trouvé exactement, 50% si partiel
        score = int((nb_trouvees * 100 + nb_partielles * 50) / nb_total)
        score = min(100, score)  # Plafonner à 100

        self.rapport["statistiques"]["nb_correspondances_exactes"] = nb_trouvees
        self.rapport["statistiques"]["nb_correspondances_partielles"] = nb_partielles

        if score < 80:
            self.rapport["avertissements"].append(
                f"Seulement {nb_trouvees}/{nb_total} correspondances exactes avec le BO"
            )

        self.rapport["scores_details"]["correspondance_bo"] = score
        return score

    def calculer_score_global(self) -> int:
        """
        Calcule le score global pondéré
        Retourne un score de 0 à 100
        """
        ponderations = {
            "structure": 0.15,
            "codes_uniques": 0.15,
            "completude": 0.30,
            "correspondance_bo": 0.40
        }

        score = 0
        for critere, poids in ponderations.items():
            if critere in self.rapport["scores_details"]:
                score += self.rapport["scores_details"][critere] * poids

        return int(score)

    def valider(self) -> Dict:
        """
        Lance toutes les validations et retourne le rapport
        """
        if not self.charger_donnees():
            self.rapport["score_global"] = 0
            return self.rapport

        # Exécuter toutes les validations
        self.valider_structure()
        self.valider_codes_uniques()
        self.valider_completude_competences()
        self.valider_correspondance_bo()

        # Calculer score global
        self.rapport["score_global"] = self.calculer_score_global()

        # Déterminer le niveau de qualité
        score = self.rapport["score_global"]
        if score >= 90:
            self.rapport["qualite"] = "Excellente [OK]"
        elif score >= 75:
            self.rapport["qualite"] = "Bonne [+]"
        elif score >= 60:
            self.rapport["qualite"] = "Acceptable [!]"
        else:
            self.rapport["qualite"] = "A ameliorer [-]"

        return self.rapport

    @staticmethod
    def _normaliser_texte(texte: str) -> str:
        """Normalise un texte pour comparaison"""
        # Minuscules
        texte = texte.lower()

        # Supprimer accents
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

        # Supprimer ponctuation excessive
        texte = re.sub(r'[^\w\s]', ' ', texte)
        texte = re.sub(r'\s+', ' ', texte)

        return texte.strip()


def valider_tous_les_programmes():
    """Valide tous les programmes disponibles"""
    dossier_data = Path(__file__).parent / "data"
    dossier_pdf = Path(__file__).parent / "pdf"

    correspondances = {
        "cycle3.json": "cycle3_v2.pdf",
        "seconde.json": "seconde.pdf",
        "premiere_spe.json": "premiere_spe_v2.pdf",
        "terminale_spe.json": "terminale_spe.pdf",
        "premiere_ens_sci.json": "premiere_ens_sci.pdf",
        "terminale_ens_sci.json": "terminale_ens_sci.pdf"
    }

    print("\n" + "="*80)
    print("VALIDATION DES EXTRACTIONS DE PROGRAMMES OFFICIELS")
    print("="*80 + "\n")

    rapports = []

    for json_file, pdf_file in correspondances.items():
        chemin_json = dossier_data / json_file
        chemin_pdf = dossier_pdf / pdf_file

        if not chemin_json.exists():
            print(f"[-] {json_file} : Fichier non trouve, passage au suivant")
            continue

        if not chemin_pdf.exists():
            print(f"[!] {json_file} : PDF source manquant ({pdf_file})")
            continue

        print(f"[*] Validation de {json_file}...")

        validateur = ValidateurExtraction(chemin_json, chemin_pdf)
        rapport = validateur.valider()
        rapports.append(rapport)

        # Afficher résumé
        print(f"   Score global : {rapport['score_global']}% - {rapport['qualite']}")
        print(f"   |-- Structure : {rapport['scores_details'].get('structure', 0)}%")
        print(f"   |-- Codes uniques : {rapport['scores_details'].get('codes_uniques', 0)}%")
        print(f"   |-- Completude : {rapport['scores_details'].get('completude', 0)}%")
        print(f"   |-- Correspondance BO : {rapport['scores_details'].get('correspondance_bo', 0)}%")

        if rapport["erreurs"]:
            print(f"   [!] Erreurs : {len(rapport['erreurs'])}")
            for erreur in rapport["erreurs"][:3]:
                print(f"      - {erreur}")

        if rapport["avertissements"]:
            print(f"   [!] Avertissements : {len(rapport['avertissements'])}")

        print()

    # Synthèse globale
    if rapports:
        score_moyen = sum(r["score_global"] for r in rapports) / len(rapports)
        print("="*80)
        print(f"SYNTHESE GLOBALE")
        print("="*80)
        print(f"   Fichiers valides : {len(rapports)}")
        print(f"   Score moyen : {int(score_moyen)}%")
        print()

        # Compter par niveau de qualité
        nb_excellent = sum(1 for r in rapports if r["score_global"] >= 90)
        nb_bon = sum(1 for r in rapports if 75 <= r["score_global"] < 90)
        nb_acceptable = sum(1 for r in rapports if 60 <= r["score_global"] < 75)
        nb_ameliorer = sum(1 for r in rapports if r["score_global"] < 60)

        print(f"   [OK] Excellents (>=90%) : {nb_excellent}")
        print(f"   [+]  Bons (75-89%) : {nb_bon}")
        print(f"   [!]  Acceptables (60-74%) : {nb_acceptable}")
        print(f"   [-]  A ameliorer (<60%) : {nb_ameliorer}")
        print()

    # Sauvegarder rapport complet
    rapport_complet = {
        "date_validation": str(Path(__file__).stat().st_mtime),
        "score_moyen": int(score_moyen) if rapports else 0,
        "rapports": rapports
    }

    chemin_rapport = dossier_data.parent / "rapport_validation.json"
    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        json.dump(rapport_complet, f, ensure_ascii=False, indent=2)

    print(f"[*] Rapport complet sauvegarde : {chemin_rapport}")
    print()


if __name__ == "__main__":
    valider_tous_les_programmes()
