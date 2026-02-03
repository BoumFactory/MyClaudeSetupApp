#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
TEMPLATE DE GENERATION DE DOCUMENT ODT SESAMATH
=============================================================================

INSTRUCTIONS POUR L'AGENT:
--------------------------
1. COPIER ce fichier vers le dossier de destination du document
2. RENOMMER le fichier (ex: generate_fractions.py)
3. MODIFIER les sections marquees [AGENT: ...]
4. EXECUTER le script pour generer l'ODT

NE PAS MODIFIER:
- Les imports
- La classe SesamathDocument
- La structure generale du script

A MODIFIER:
- Les metadonnees (OUTPUT_FILE, CHAPITRE, NIVEAU, DOMAINE)
- Le contenu dans la fonction build_document()
"""

import sys
from pathlib import Path

# Ajouter le chemin vers les scripts du skill ODT
SKILL_ODT_PATH = Path(r"C:\Users\Utilisateur\Documents\Professionnel\1. Reims 2025 - 2026\.claude\skills\odt\scripts")
sys.path.insert(0, str(SKILL_ODT_PATH))

from create_sesamath_document import SesamathDocument

# =============================================================================
# [AGENT: MODIFIER CES METADONNEES]
# =============================================================================

OUTPUT_FILE = "document.odt"  # [AGENT: Nom du fichier de sortie]
CHAPITRE = "Titre du chapitre"  # [AGENT: Titre du chapitre]
NIVEAU = "6e"  # [AGENT: 6e, 5e, 4e, 3e, 2nde, 1ere, tle]
DOMAINE = "numerique"  # [AGENT: numerique, geometrie, mesures, gestion_donnees, problemes]


# =============================================================================
# CONSTRUCTION DU DOCUMENT
# =============================================================================

def build_document():
    """
    Construit le document ODT avec le contenu pedagogique.

    [AGENT: Modifier cette fonction pour ajouter le contenu demande]
    """

    # Creer le document avec les metadonnees
    # Note: Le chapitre est automatiquement injecte dans les EN-TETES de page
    #       Pour l'avoir aussi en H1 dans le contenu, ajouter titre_dans_contenu=True
    doc = SesamathDocument(
        OUTPUT_FILE,
        chapitre=CHAPITRE,
        niveau=NIVEAU,
        domaine=DOMAINE,
        titre_dans_contenu=False  # [AGENT: True pour avoir aussi un H1 dans le contenu]
    )

    # =========================================================================
    # [AGENT: AJOUTER LE CONTENU ICI]
    # =========================================================================

    # --- Introduction ---
    # doc.add_paragraph("Introduction du chapitre...")
    # doc.add_empty_line()

    # --- Vocabulaire ---
    # doc.add_vocabulaire("Vocabulaire", [
    #     "Terme 1 : definition...",
    #     "Terme 2 : definition...",
    # ])
    # doc.add_empty_line()

    # --- Definition ---
    # doc.add_definition("Definition", "Contenu de la definition...")
    # # Ou avec formule integree:
    # doc.add_definition("Definition", "Texte avant la formule", formule="{a} over {b}")
    # doc.add_empty_line()

    # --- Propriete ---
    # doc.add_propriete("Propriete", "Contenu de la propriete...")
    # doc.add_empty_line()

    # --- Methode ---
    # doc.add_methode("Methode", [
    #     "Etape 1...",
    #     "Etape 2...",
    #     "Etape 3...",
    # ])
    # doc.add_empty_line()

    # --- Remarque ---
    # doc.add_remarque("Remarque", "Contenu de la remarque...")
    # doc.add_empty_line()

    # --- Exemple ---
    # doc.add_exemple("Exemple", "Contenu de l'exemple...")
    # # Ou avec formule inline:
    # doc.add_formula_inline("Exemple: ", "{3} over {4}", " = 0.75")
    # doc.add_empty_line()

    # --- Exercice ---
    # doc.add_exercice(
    #     "Titre de l'exercice",
    #     "Enonce de l'exercice...",
    #     questions=["Question 1", "Question 2"],
    #     lignes_reponse=2,
    #     correction=["Reponse 1", "Reponse 2"]  # Optionnel
    # )
    # doc.add_empty_line()

    # --- Formules mathematiques ---
    # doc.add_formula("{a} over {b}")  # Fraction seule
    # doc.add_formula_inline("L'aire vaut ", "%pi r^{2}", " unites.")

    # --- Mise en page ---
    # doc.page_break()  # Saut de page
    # doc.start_columns(2)  # Debut multicolonne
    # doc.end_columns()  # Fin multicolonne

    # --- Page de corrections ---
    # doc.add_corrections_page()  # Genere automatiquement depuis les exercices

    # =========================================================================
    # FIN DU CONTENU
    # =========================================================================

    # Sauvegarder le document
    doc.save()

    return OUTPUT_FILE


# =============================================================================
# EXECUTION
# =============================================================================

if __name__ == "__main__":
    print(f"Generation du document: {OUTPUT_FILE}")
    print(f"Chapitre: {CHAPITRE}")
    print(f"Niveau: {NIVEAU}")
    print(f"Domaine: {DOMAINE}")
    print("-" * 50)

    output = build_document()

    print("-" * 50)
    print(f"Document genere: {output}")
