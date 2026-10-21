#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
05_competences_from_bullets.py — Transforme les bullets extraits en JSON niveau.

Phase 5 du pipeline (révisée). AUCUNE intervention LLM dans ce script.

Pipeline :
  1. Lit data/bullets/{folder}/page_*.json
  2. Pour chaque bullet sous une section connue (Contenus / Capacités attendues /
     Démonstrations / Exemples d'algorithme / Approfondissements possibles),
     classifie le domaine via un mapping sous_domaine → domaine.
  3. Génère code, fingerprint, source mécaniquement.
  4. Construit data/json/{NIVEAU}.json (structure meta + stats + competences_by_theme).

Les bullets « implicites » (orphelins, hors section bullet canonique — souvent
automatismes ou préambule) sont collectés dans le champ `automatismes` ou ignorés
selon leur sous-domaine.

Usage :
    python scripts/build/05_competences_from_bullets.py             # tous niveaux mono
    python scripts/build/05_competences_from_bullets.py 1SPE
    python scripts/build/05_competences_from_bullets.py --force
"""

import io
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
BULLETS_DIR = DATA_DIR / "bullets"
JSON_DIR = DATA_DIR / "json"
MAPPING_FILE = PDF_DIR / "_mapping.json"

# Folder → niveau code (mono-niveau seulement ; cycle4 traité à part)
FOLDER_TO_NIVEAU = {
    "2GT": "2GT", "1SPE": "1SPE", "1ENS": "1ENS", "1TEC": "1TEC",
    "TSPE": "TSPE", "TCOMP": "TCOMP", "TTEC": "TTEC"
}

# Nom long du niveau (depuis _mapping.json original_name simplifié)
NIVEAU_NOM = {
    "2GT": "Seconde générale et technologique",
    "1SPE": "Première générale — enseignement de spécialité mathématiques",
    "1ENS": "Première générale — mathématiques intégrées à l'enseignement scientifique",
    "1TEC": "Première — voie technologique",
    "TSPE": "Terminale générale — enseignement de spécialité mathématiques",
    "TCOMP": "Terminale générale — mathématiques complémentaires",
    "TTEC": "Terminale — voie technologique",
    "5E": "Cinquième",
    "4E": "Quatrième",
    "3E": "Troisième",
    "CM1": "Cours moyen première année",
    "CM2": "Cours moyen deuxième année",
    "6E": "Sixième",
}

CYCLE_OF_NIVEAU = {
    "CM1": "C3", "CM2": "C3", "6E": "C3",
    "5E": "C4", "4E": "C4", "3E": "C4",
    "2GT": "Lycée", "1SPE": "Lycée", "1ENS": "Lycée", "1TEC": "Lycée",
    "TSPE": "Lycée", "TCOMP": "Lycée", "TTEC": "Lycée"
}

# Mapping sous_domaine (texte BO normalisé) → domaine (code)
# Le texte est comparé après normalisation (lowercase, sans accents, alphanum+_).
DOMAINE_BY_SOUSDOMAINE = {
    # Cycle 4 (BO mars 2026) — sous-domaines spécifiques
    "nombres_et_calculs": "NB",
    "nombres_et_organisations": "NB",
    "racine_carree": "NB",
    "nombres_rationnels": "NB",
    "puissances": "NB",
    "ecriture_scientifique": "NB",
    "fractions": "NB",
    "nombres_decimaux_relatifs": "NB",
    "nombres_relatifs": "NB",
    "ensembles_de_nombres": "NB",
    "arithmetique_collège": "NB",
    "calcul_litteral": "AL",
    "calcul_litteral_et_algebrique": "AL",
    "calcul_litteral_et_fonctions": "AL",
    "equations": "AL",
    "inequations": "AL",
    "fonctions_lineaires": "AL",
    "fonctions_affines": "AL",
    "proportionnalite": "AL",
    "pourcentages": "AL",
    "espace_et_geometrie": "GEO",
    "geometrie_plane": "GEO",
    "transformations": "GEO",
    "symetries": "GEO",
    "rotations": "GEO",
    "translations": "GEO",
    "homotheties": "GEO",
    "angles": "GEO",
    "triangles": "GEO",
    "polygones": "GEO",
    "cercles": "GEO",
    "configurations_planes": "GEO",
    "espace": "GEO",
    "solides": "GEO",
    "reperage_sur_une_droite_et_dans_le_plan": "GEO",
    "theoreme_de_pythagore": "GEO",
    "theoreme_de_thales": "GEO",
    "trigonometrie_dans_le_triangle_rectangle": "TRG",
    "grandeurs_et_mesures": "GM",
    "longueurs": "GM",
    "aires": "GM",
    "volumes": "GM",
    "perimetres": "GM",
    "vitesses": "GM",
    "donnees_et_statistiques": "STA",
    "statistiques_collège": "STA",
    "moyenne": "STA",
    "mediane": "STA",
    "etendue": "STA",
    "probabilites_collège": "PR",
    "evenements": "PR",
    "organisation_et_gestion_de_donnees": "OGD",
    "algorithmique_au_college": "ALGO",
    "scratch": "ALGO",
    "programmes_scratch": "ALGO",
    # Lycée transversal
    "vocabulaire_ensembliste_et_logique": "LOG",
    "variables_et_instructions_elementaires": "ALGO",
    "notion_de_fonction": "ALGO",
    "notion_de_liste": "ALGO",
    "algorithmique_et_programmation": "ALGO",
    # Lycée — Nombres
    "arithmetique": "NB",
    "nombres_reels": "NB",
    # Lycée — Algèbre
    "algebre": "AL",
    "calcul_algebrique": "AL",
    "equations_et_inequations": "AL",
    "equations_fonctions_polynomes_du_second_degre": "AL",
    "suites_numeriques_modeles_discrets": "AL",
    # Lycée — Géométrie
    "vecteurs": "GEO",
    "vecteurs_et_problemes_de_geometrie": "GEO",
    "droites_du_plan": "GEO",
    "calcul_vectoriel_et_produit_scalaire": "GEO",
    "geometrie_repere": "GEO",
    "geometrie_reperee": "GEO",
    "geometrie": "GEO",
    # Lycée — Analyse
    "fonctions": "AN",
    "representation_algebrique_et_graphique_des_fonctions": "AN",
    "variations_et_extremums": "AN",
    "variations_et_extremums_d_une_fonction": "AN",
    "variations_et_courbes_representatives_des_fonctions": "AN",
    "derivation": "AN",
    "fonction_exponentielle": "AN",
    "fonctions_exponentielles": "AN",
    "modelisation_quadratique": "AN",
    "variation_lineaire": "AN",
    "variation_exponentielle": "AN",
    "variation_lineaire_suites_arithmetiques_et_fonctions_affines": "AN",
    "variation_exponentielle_suites_geometriques_et_fonctions_exponentielles": "AN",
    # Lycée — Trigonométrie
    "trigonometrie": "TRG",
    # Lycée — Stats / Probas
    "information_chiffree_et_statistique_descriptive": "STA",
    "croisement_de_deux_variables_qualitatives": "STA",
    "statistiques": "STA",
    "analyse_de_l_information_chiffree": "STA",
    "statistique_bivariee_caracteres_qualitatifs": "STA",
    "statistique_bivariee_caracteres_quantitatifs": "STA",
    "probabilites": "PR",
    "phenomenes_aleatoires": "PR",
    "probabilites_conditionnelles": "PR",
    "probabilites_conditionnelles_et_independance": "PR",
    "variables_aleatoires_reelles": "PR",
    "experimentations": "PR",
    "probabilites_et_statistiques": "PR",
    # TSPE — sous-domaines spécifiques (ajoutés session 4)
    "combinatoire_et_denombrement": "PR",
    "concentration_loi_des_grands_nombres": "PR",
    "succession_d_epreuves_independantes_schema_de_bernoulli": "PR",
    "loi_binomiale": "PR",
    "sommes_de_variables_aleatoires": "PR",
    "compléments_sur_la_derivation": "AN",
    "complements_sur_la_derivation": "AN",
    "continuite_des_fonctions_d_une_variable_reelle": "AN",
    "limites_des_fonctions": "AN",
    "fonction_logarithme": "AN",
    "fonctions_sinus_et_cosinus": "AN",
    "primitives_equations_differentielles": "AN",
    "primitives": "AN",
    "equations_differentielles": "AN",
    "calcul_integral": "AN",
    "integration": "AN",
    "convexite": "AN",
    "suites": "AN",
    "limites_de_suites": "AN",
    "manipulation_des_vecteurs_des_droites_et_des_plans_de_l_espace": "GEO",
    "orthogonalite_et_distances_dans_l_espace": "GEO",
    "representations_parametriques_et_equations_cartesiennes": "GEO",
    "produit_scalaire_dans_l_espace": "GEO",
    # TCOMP / TTEC sous-domaines spécifiques
    "modeles_definis_par_une_fonction_d_une_variable": "AN",
    "modeles_definis_par_une_relation_de_recurrence": "AN",
    "loi_de_probabilite_a_densite": "PR",
    "loi_exponentielle": "PR",
    "loi_normale": "PR",
    "echantillonnage": "PR",
    "estimation": "PR",
    "lois_discretes": "PR",
    "lois_a_densite": "PR",
    "loi_geometrique": "PR",
    "loi_uniforme": "PR",
    "inference_bayesienne": "PR",
    "temps_d_attente": "PR",
    "fonctions_convexes": "AN",
    "convexite": "AN",
    "modeles_d_evolution": "AN",
    "calculs_d_aires": "AN",
    "approche_historique_de_la_fonction_logarithme": "AN",
    "fonction_logarithme": "AN",
    "correlation_et_causalite": "STA",
    "repartition_des_richesses_inegalites": "STA",
    "themes_d_etude": "STA",
    "analyse": "AN",
    "probabilites_et_statistique": "PR",
    # 1TEC / TTEC — sous-domaines spécifiques voie technologique (ajoutés session 6)
    "suites_arithmetiques": "AN",
    "suites_geometriques": "AN",
    "suites_numeriques": "AN",
    "fonctions_polynomes_de_degre_2": "AN",
    "fonctions_de_la_variable_reelle": "AN",
    "fonction_inverse": "AN",
    "point_de_vue_local": "AN",
    "point_de_vue_global": "AN",
    "variables_aleatoires": "PR",
    "variable_aleatoire": "PR",
    "probabilites_conditionnelles_independance": "PR",
    "statistique_et_probabilites": "STA",
    "statistiques_et_probabilites": "STA",
    "selection_de_donnees": "STA",
    "figures_regulieres": "GEO",
    "solides": "GEO",
    "coniques": "GEO",
    "perspective_centrale": "GEO",
    "perspective_cavaliere": "GEO",
    "geometrie_dans_l_espace": "GEO",
    "geometrie_plane": "GEO",
    "repérage": "GEO",
    "reperage": "GEO",
    "situations_algorithmiques": "ALGO",
    "listes": "ALGO",
    "variables": "ALGO",
    "activites_algorithmiques_et_numeriques": "ALGO",
    "evolutions_et_variations": "STA",
    "proportions_et_pourcentages": "STA",
    # Cycle 3 (BO 2026) — sous-domaines CM1 / CM2 / 6e
    # Nombres et calculs
    "les_nombres_entiers": "NB",
    "les_nombres_decimaux": "NB",
    "les_nombres_entiers_et_decimaux": "NB",
    "nombres_calcul_et_resolution_de_problemes": "NB",
    "les_fractions": "NB",
    "comparer_des_fractions": "NB",
    "additionner_et_soustraire_des_fractions": "NB",
    "effectuer_des_operations_sur_les_fractions": "NB",
    "resoudre_des_problemes_mettant_en_jeu_des_fractions": "NB",
    "inventer_des_problemes_mettant_en_jeu_des_fractions": "NB",
    "savoir_que_la_fraction": "NB",
    "additionner_et_soustraire_des_nombres_decimaux": "NB",
    "controler_les_resultats_a_l_aide_d_ordres_de_grandeur": "NB",
    "les_quatre_operations": "NB",
    "le_calcul_mental": "NB",
    "memoriser_des_faits_numeriques": "NB",
    "connaitre_des_faits_numeriques_usuels_avec_des_entiers": "NB",
    "connaitre_la_moitie_des_nombres_impairs_jusqu_a_15": "NB",
    "apprendre_des_procedures_de_calcul_mental": "NB",
    "multiplier_un_nombre_decimal_par_10": "NB",
    "diviser_un_nombre_decimal_par_10": "NB",
    "multiplier_un_nombre_decimal_par_5": "NB",
    "multiplier_un_nombre_decimal_par_50": "NB",
    "multiplier_un_nombre_entier_par_5": "NB",
    "comparer_et_denombrer_des_collections_en_les_organisant": "NB",
    "construire_des_collections_de_cardinal_donne": "NB",
    "la_resolution_de_problemes": "NB",
    "resoudre_des_problemes_de_comparaison_multiplicative": "NB",
    "resoudre_des_problemes_de_denombrement": "NB",
    "resoudre_des_problemes_d_optimisation": "NB",
    # Algèbre cycle 3 (initiation à la pensée algébrique)
    "resoudre_des_problemes_algebriques": "AL",
    "completer_des_egalites_a_trous_multiplicatives": "AL",
    "resoudre_des_problemes_mettant_en_jeu_des_nombres_inconnus": "AL",
    # Grandeurs et mesures cycle 3
    "les_longueurs": "GM",
    "les_masses": "GM",
    "les_contenances": "GM",
    "les_aires": "GM",
    "les_angles": "GM",
    "les_volumes": "GM",
    "le_reperage_dans_le_temps_et_les_durees": "GM",
    "convertir_des_durees": "GM",
    "effectuer_des_conversions_d_aire": "GM",
    "determiner_des_aires": "GM",
    "calculer_des_perimetres_de_figures_composees": "GM",
    "resoudre_des_problemes_impliquant_des_longueurs": "GM",
    # Géométrie cycle 3
    "la_geometrie_plane": "GEO",
    "les_solides": "GEO",
    "le_reperage_dans_l_espace": "GEO",
    "espace_et_geometrie": "GEO",
    "deplacements_dans_l_espace": "GEO",
    "etude_de_configurations_planes": "GEO",
    "distances": "GEO",
    "cercles_et_disques": "GEO",
    "triangles": "GEO",
    "construire_des_triangles": "GEO",
    "symetrie_axiale": "GEO",
    "la_vision_dans_l_espace": "GEO",
    "voir_dans_l_espace_des_assemblages_de_cubes": "GEO",
    "comprendre_et_utiliser_les_notations_des_angles": "GEO",
    "comparer_des_angles": "GEO",
    "connaitre_la_definition_de_la_mediatrice_d_un_segment": "GEO",
    "reconnaitre_et_utiliser_la_notion_de_perpendicularite": "GEO",
    "reconnaitre_et_utiliser_la_notion_de_parallelisme": "GEO",
    # Organisation et gestion de données / probabilités cycle 3
    "organisation_et_gestion_de_donnees_et_probabilites": "OGD",
    "les_probabilites": "PR",
    "identifier_des_experiences_aleatoires": "PR",
    "reconnaitre_des_situations_d_equiprobabilite": "PR",
    "comparer_des_probabilites_dans_des_cas_simples": "PR",
    # Proportionnalité (cycle 3 : champ transversal, classé NB par convention)
    "la_proportionnalite": "NB",
    "s_initier_a_la_resolution_de_problemes_d_echelles": "NB",
    # Pensée informatique cycle 3
    "initiation_a_la_pensee_informatique": "ALGO",
    # ─── Mapping enrichi cycle 4 (session 9 — 2026-05-21) ───
    "operations": "NB",
    "operations_sur_les_nombres_relatifs": "NB",
    "nombres_relatifs": "NB",
    "nombres_rationnels": "NB",
    "puissances": "NB",
    "racine_carree": "NB",
    "multiples_et_diviseurs": "NB",
    "calcul_litteral_et_algebrique": "AL",
    "proportionnalite_fonctions": "AL",
    "fonctions": "AN",
    "parallelogrammes": "GEO",
    "parallelogrammes_et_translations": "GEO",
    "translations_et_vecteurs": "GEO",
    "transformations": "GEO",
    "representation_de_l_espace": "GEO",
    "reperage_sur_une_droite_et_dans_le_plan": "GEO",
    "espace_et_geometrie": "GEO",
    "statistiques": "STA",
    "probabilites": "PR",
    "la_pensee_informatique": "ALGO",
    "pensee_informatique": "ALGO",
    "angles": "GEO",  # en cycle 4, les angles sont en GEO (et non GM comme en cycle 3)
    "fraction": "NB",  # match substring : 'Le sens quotient d\'une fraction', 'La fraction comme opérateur multiplicatif' (cycle 3 6E)
    # ─── Mapping enrichi 1ENS (session 9 — 2026-05-21) ───
    # Le BO 1ENS a une structure [sous-domaine] + [bullets] sans titre de section
    # explicite. Les bullets sont remontés en section "unknown" par le parser ; la
    # règle de promotion `unknown → capacite` (cf. collect_bullets) leur attribue
    # le statut de compétence à condition que le sous-domaine soit ici classifié.
    "evolutions_et_variations": "AN",     # taux d'évolution, fonctions
    "calcul_numerique_et_algebrique": "AL",
    "fonctions_et_representations": "AN",
    "phenomenes_aleatoires": "PR",
    "variation_exponentielle": "AN",
    "cas_particulier_de_l_exposant": "AN",
    # Sous-domaines "situations et problèmes" du BO 1ENS : pas des compétences à
    # proprement parler, on les ignore en les mappant à un domaine OGD (organisation
    # / contextualisation) pour rester traçable mais qu'ils ne polluent pas les
    # compétences phares. Si non souhaité, retirer ces lignes pour que ces bullets
    # restent en automatismes.
    "theorie_des_jeux": "OGD",
    "sciences_de_la_terre": "OGD",
    "modele_simple_de_fiscalite": "OGD",
    "economie": "OGD",
    "enseignement_moral_et_civique": "OGD",
}

# Domaine code → label kebab pour génération du code compétence (XX-DOM-NNN)
DOMAINE_CODE_LABEL = {
    "NB": "NB", "AL": "AL", "AN": "AN", "GEO": "GEO", "GM": "GM",
    "STA": "STA", "PR": "PR", "OGD": "OGD", "ALGO": "ALGO", "TRG": "TRG", "LOG": "LOG"
}


def norm(s: str) -> str:
    s = s or ""
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def slug(s: str, max_len: int = 50) -> str:
    out = norm(s)
    return out[:max_len].rstrip("_")


def classify_domaine(sous_domaine: str | None) -> str | None:
    if not sous_domaine:
        return None
    n = norm(sous_domaine)
    # Match exact prioritaire
    if n in DOMAINE_BY_SOUSDOMAINE:
        return DOMAINE_BY_SOUSDOMAINE[n]
    # Heuristique substring AVEC FRONTIÈRES DE MOT (session 9, 2026-05-21) :
    # 'commentaires' ne doit pas matcher 'aires' (faux positif TTEC vu en session 8).
    # On exige que la clé soit délimitée par début/fin de chaîne ou par '_' dans la
    # version normalisée. La clé la plus longue gagne (specificity over generality).
    candidates = []
    for key, dom in DOMAINE_BY_SOUSDOMAINE.items():
        if "_" in key:
            # Clés composées : matching substring OK (ex: "suites_arithmetiques")
            if key in n:
                candidates.append((key, dom))
        else:
            # Mots simples : exiger un match en frontière de mot
            if n == key or n.startswith(key + "_") or n.endswith("_" + key) or ("_" + key + "_") in n:
                candidates.append((key, dom))
    if not candidates:
        return None
    candidates.sort(key=lambda kd: -len(kd[0]))
    return candidates[0][1]


def load_mapping() -> dict:
    return json.load(open(MAPPING_FILE, encoding='utf-8'))


def collect_bullets_for_folder(folder: str) -> list[dict]:
    """Charge tous les bullets de tous les page_*.json d'un dossier, dans l'ordre."""
    out_bullets = []
    bullets_folder = BULLETS_DIR / folder
    if not bullets_folder.exists():
        return []
    for page_file in sorted(bullets_folder.glob("page_*.json")):
        data = json.load(open(page_file, encoding='utf-8'))
        for sec in data["page_data"]["sections"]:
            sec_type = sec["type"]
            sec_title = sec["title"]
            sous_domaine = sec["sous_domaine"]
            niveau_sec = sec.get("niveau_assigne")
            # Promotion (session 9, 2026-05-21) : une section "unknown" (== "(implicite)")
            # dont le sous-domaine est un VRAI domaine mathématique classifiable est traitée
            # comme une section "capacite" (compétence). Sinon, les bullets de préambule
            # (sous-domaines "Objectifs majeurs", "La résolution de problèmes", etc.) restent
            # en automatismes via le filtre original. Cette règle débloque 1ENS dont le BO
            # n'utilise pas de titre de section explicite après les sous-domaines.
            if sec_type == "unknown" and sous_domaine and classify_domaine(sous_domaine):
                sec_type_effective = "capacite"
            else:
                sec_type_effective = sec_type
            for b in sec["bullets"]:
                out_bullets.append({
                    "formulation_bo": b["formulation_bo"],
                    "section_title": sec_title,
                    "section_type": sec_type_effective,
                    "sous_domaine": sous_domaine,
                    "niveau_assigne": b.get("niveau_assigne") or niveau_sec,
                    "source": b["source"]
                })
    return out_bullets


def build_competence(niveau: str, bullet: dict, code: str) -> dict:
    fp = slug(bullet["formulation_bo"], 50)
    if not fp:
        fp = slug(bullet["sous_domaine"] or "competence", 40) + "_x"

    comp = {
        "code": code,
        "intitule": bullet["formulation_bo"],
        "fingerprint": fp,
        "niveau": niveau,
        "domaine": classify_domaine(bullet["sous_domaine"]) or "AL",
        "sous_domaine": bullet["sous_domaine"] or "(à classer)",
        "type": bullet["section_type"],
        "formulation_bo": bullet["formulation_bo"],
        "source": bullet["source"],
        "tags": [bullet["section_type"]],
        "extraction_meta": {
            "date": datetime.now(timezone.utc).isoformat(timespec='seconds'),
            "agent_version": "v2.0-mechanical",
            "confidence": 0.9 if classify_domaine(bullet["sous_domaine"]) else 0.7,
            "verified": False,
            "extraction_method": "mechanical_from_bullets"
        }
    }
    return comp


def build_level_json(niveau: str, folder: str, mapping_entry: dict, filter_niveau: str | None = None) -> dict:
    """Construit le JSON d'un niveau.

    Si `filter_niveau` est fourni (ex : '5E' pour cycle4), ne conserve que les
    bullets avec `niveau_assigne == filter_niveau`.
    """
    raw_bullets = collect_bullets_for_folder(folder)

    if filter_niveau:
        raw_bullets = [b for b in raw_bullets if b.get("niveau_assigne") == filter_niveau]

    # Filtrer par type :
    #  - "contenu/capacite/demonstration/algorithme/approfondissement" → competences_by_theme
    #  - "automatisme" → automatismes[] (champ string array du JSON niveau)
    #  - "unknown" (orphelins) → automatismes[] si ils ont un sous_domaine, sinon ignoré
    canonical_types = {"contenu", "capacite", "demonstration", "algorithme", "approfondissement"}
    competences_bullets = [b for b in raw_bullets if b["section_type"] in canonical_types]
    automatismes_bullets = [b for b in raw_bullets if b["section_type"] in ("automatisme", "unknown") and b["sous_domaine"]]

    # Génération codes : compteur par domaine
    domain_counters = {}
    competences_by_theme = {}

    for bullet in competences_bullets:
        domaine = classify_domaine(bullet["sous_domaine"]) or "AL"
        domain_counters[domaine] = domain_counters.get(domaine, 0) + 1
        code = f"{niveau}-{DOMAINE_CODE_LABEL[domaine]}-{domain_counters[domaine]:03d}"
        comp = build_competence(niveau, bullet, code)
        sous_dom = bullet["sous_domaine"] or "(à classer)"
        competences_by_theme.setdefault(domaine, {}).setdefault(sous_dom, []).append(comp)

    # Stats
    by_domaine = {dom: sum(len(comps) for comps in themes.values()) for dom, themes in competences_by_theme.items()}
    by_type = {}
    for dom, themes in competences_by_theme.items():
        for theme, comps in themes.items():
            for c in comps:
                by_type[c["type"]] = by_type.get(c["type"], 0) + 1

    # Automatismes : on garde la formulation_bo de chaque bullet implicite (texte verbatim BO).
    # Format `automatismes` reste en list[str] pour compat avec les consommateurs
    # historiques. On exporte EN PLUS `automatismes_detailed` avec source + domaine
    # — utilisé par progression-builder pour afficher la page BO et colorer chaque
    # automatisme par son domaine d'origine plutôt qu'en gris uniforme.
    automatismes_list = [b["formulation_bo"] for b in automatismes_bullets]
    automatismes_detailed = []
    for b in automatismes_bullets:
        sous_dom = b.get("sous_domaine") or ""
        domaine = classify_domaine(sous_dom) or "AL"
        automatismes_detailed.append({
            "text": b["formulation_bo"],
            "sous_domaine": sous_dom,
            "domaine": domaine,
            "source": b.get("source", {}),
        })

    bo_ref = mapping_entry.get("bo_reference", "")
    bo_url = mapping_entry.get("bo_url", "")
    pdf = next(k for k, v in load_mapping()["files"].items() if v["page_folder"] == folder)

    level = {
        "meta": {
            "niveau": niveau,
            "nom": NIVEAU_NOM.get(niveau, niveau),
            "cycle": CYCLE_OF_NIVEAU.get(niveau, "Lycée"),
            "bo_reference": bo_ref,
            "bo_url": bo_url,
            "pdf": pdf,
            "applicable_a_partir_de": "Rentrée 2026",
            "generated": datetime.now(timezone.utc).isoformat(timespec='seconds'),
            "agent_version": "v2.0-mechanical",
            "total_competences": sum(by_domaine.values()),
            "status": "mechanical_extraction",
            "_note_status": "Extraction mécanique depuis bullets BO (script 05_competences_from_bullets.py). Aucune régurgitation LLM. Champ formulation_bo strictement issu du PDF."
        },
        "stats": {"by_domaine": by_domaine, "by_type": by_type},
        "objectifs": f"Programme officiel du niveau {niveau} ({NIVEAU_NOM.get(niveau, niveau)}), {bo_ref}. Voir le PDF source ({pdf}) pour les objectifs détaillés dans le préambule.",
        "automatismes": automatismes_list,
        "automatismes_detailed": automatismes_detailed,
        "competences_by_theme": competences_by_theme
    }
    return level


def build_cycle4_levels(mapping_entry: dict, force: bool = False) -> list[tuple[str, int, int]]:
    """Produit 5E.json, 4E.json, 3E.json depuis le dossier 'cycle4'."""
    results = []
    for niveau in ("5E", "4E", "3E"):
        level = build_level_json(niveau, "cycle4", mapping_entry, filter_niveau=niveau)
        out_path = JSON_DIR / f"{niveau}.json"
        if out_path.exists() and not force:
            print(f"  [SKIP] {niveau}.json existe (--force pour écraser)")
            continue
        out_path.write_text(json.dumps(level, ensure_ascii=False, indent=2),
                            encoding='utf-8', newline='\n')
        n = level["meta"]["total_competences"]
        n_auto = len(level["automatismes"])
        doms = ", ".join(f"{d}:{c}" for d, c in level["stats"]["by_domaine"].items())
        print(f"  {niveau}.json : {n} compétences ({doms}), {n_auto} automatismes")
        results.append((niveau, n, n_auto))
    return results


def build_cycle3_levels(mapping_entry: dict, force: bool = False) -> list[tuple[str, int, int]]:
    """Produit CM1.json, CM2.json, 6E.json depuis le dossier 'cycle3'."""
    results = []
    for niveau in ("CM1", "CM2", "6E"):
        level = build_level_json(niveau, "cycle3", mapping_entry, filter_niveau=niveau)
        out_path = JSON_DIR / f"{niveau}.json"
        if out_path.exists() and not force:
            print(f"  [SKIP] {niveau}.json existe (--force pour écraser)")
            continue
        out_path.write_text(json.dumps(level, ensure_ascii=False, indent=2),
                            encoding='utf-8', newline='\n')
        n = level["meta"]["total_competences"]
        n_auto = len(level["automatismes"])
        doms = ", ".join(f"{d}:{c}" for d, c in level["stats"]["by_domaine"].items())
        print(f"  {niveau}.json : {n} compétences ({doms}), {n_auto} automatismes")
        results.append((niveau, n, n_auto))
    return results


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__); return
    force = "--force" in args
    if force:
        args.remove("--force")

    mapping = load_mapping()
    folders_to_niveau = FOLDER_TO_NIVEAU.copy()

    targets = []
    if args:
        target = args[0]
        if target in ("cycle4", "cycle3"):
            targets = [target]
        elif target in folders_to_niveau:
            targets = [target]
        else:
            print(f"Folder inconnu : {target}. Disponibles : {list(folders_to_niveau)} + cycle4 + cycle3")
            sys.exit(2)
    else:
        targets = list(folders_to_niveau.keys()) + ["cycle4", "cycle3"]

    grand_total = 0
    for folder in targets:
        mapping_entry = next(v for v in mapping["files"].values() if v["page_folder"] == folder)
        if folder == "cycle4":
            results = build_cycle4_levels(mapping_entry, force=force)
            for _, n, _ in results:
                grand_total += n
            continue
        if folder == "cycle3":
            results = build_cycle3_levels(mapping_entry, force=force)
            for _, n, _ in results:
                grand_total += n
            continue
        niveau = folders_to_niveau[folder]
        level = build_level_json(niveau, folder, mapping_entry)
        out_path = JSON_DIR / f"{niveau}.json"
        if out_path.exists() and not force:
            print(f"  [SKIP] {niveau}.json existe (--force pour écraser)")
            continue
        out_path.write_text(json.dumps(level, ensure_ascii=False, indent=2),
                            encoding='utf-8', newline='\n')
        n = level["meta"]["total_competences"]
        n_auto = len(level["automatismes"])
        grand_total += n
        doms = ", ".join(f"{d}:{c}" for d, c in level["stats"]["by_domaine"].items())
        print(f"  {niveau}.json : {n} compétences ({doms}), {n_auto} automatismes")

    print(f"\nTotal : {grand_total} compétences générées mécaniquement")


if __name__ == "__main__":
    main()
