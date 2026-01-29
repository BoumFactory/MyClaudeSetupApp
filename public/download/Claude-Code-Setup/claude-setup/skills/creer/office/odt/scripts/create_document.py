#!/usr/bin/env python3
"""
Cree un document ODT avec les styles Sesamath.
Usage: python create_document.py <fichier_sortie.odt> [--template <modele.odt>]

Ce script permet de creer un nouveau document ODT avec les styles educatifs
Sesamath pre-configures pour les cahiers d'exercices mathematiques.
"""
import sys
import os
import argparse
from copy import deepcopy

try:
    from odf.opendocument import OpenDocumentText, load
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.style import TableProperties, TableColumnProperties, TableCellProperties
    from odf.text import P, Span, H, List, ListItem
    from odf.table import Table, TableColumn, TableRow, TableCell
except ImportError:
    print("Erreur: odfpy n'est pas installe. Executez: pip install odfpy")
    sys.exit(1)


def create_sesamath_styles(doc):
    """Ajoute les styles Sesamath de base au document."""

    # Style _Paragraphe
    style = Style(name="_5f_Paragraphe", displayname="_Paragraphe", family="paragraph")
    style.addElement(ParagraphProperties(
        marginleft="0cm",
        marginright="0.101cm",
        margintop="0.101cm",
        marginbottom="0.101cm",
        textalign="start"
    ))
    style.addElement(TextProperties(
        fontsize="11pt",
        fontname="Bitstream Vera Sans"
    ))
    doc.styles.addElement(style)

    # Style _Paragraphe_Reponse_Eleve
    style = Style(name="_5f_Paragraphe_5f_Reponse_5f_Eleve",
                  displayname="_Paragraphe_Reponse_Eleve",
                  family="paragraph")
    style.addElement(ParagraphProperties(
        lineheight="0.7cm",
        textalign="start"
    ))
    style.addElement(TextProperties(
        color="#b3b3b3"
    ))
    doc.styles.addElement(style)

    # Style _Paragraphe_Reponse_Pointilles_Grises
    style = Style(name="_5f_Paragraphe_5f_Reponse_5f_Pointilles_5f_Grises",
                  displayname="_Paragraphe_Reponse_Pointilles_Grises",
                  family="paragraph")
    style.addElement(ParagraphProperties(
        textalign="end"
    ))
    style.addElement(TextProperties(
        color="#b3b3b3"
    ))
    doc.styles.addElement(style)

    # Style _Titre_Exercices_avec_Titre
    style = Style(name="_5f_Titre_5f_Exercices_5f_avec_5f_Titre",
                  displayname="_Titre_Exercices_avec_Titre",
                  family="paragraph")
    style.addElement(ParagraphProperties(
        margintop="0.3cm",
        marginbottom="0.101cm",
        textalign="justify"
    ))
    style.addElement(TextProperties(
        fontsize="12pt",
        fontweight="bold"
    ))
    doc.styles.addElement(style)

    # Style _Caracteres_gras
    style = Style(name="_5f_Caracteres_5f_gras",
                  displayname="_Caracteres_gras",
                  family="text")
    style.addElement(TextProperties(fontweight="bold"))
    doc.styles.addElement(style)

    # Style _Caracteres_correction
    style = Style(name="_5f_Caracteres_5f_correction",
                  displayname="_Caracteres_correction",
                  family="text")
    style.addElement(TextProperties(color="#FF0000", fontweight="bold"))
    doc.styles.addElement(style)

    # Style _Tableau_Centre
    style = Style(name="_5f_Tableau_5f_Centre",
                  displayname="_Tableau_Centre",
                  family="paragraph")
    style.addElement(ParagraphProperties(textalign="center"))
    doc.styles.addElement(style)

    # Style _Tableau_Gauche
    style = Style(name="_5f_Tableau_5f_Gauche",
                  displayname="_Tableau_Gauche",
                  family="paragraph")
    style.addElement(ParagraphProperties(textalign="start"))
    doc.styles.addElement(style)

    print("Styles Sesamath de base ajoutes")


def create_document_from_template(template_path: str, output_path: str):
    """Cree un nouveau document en copiant les styles d'un modele."""
    template = load(template_path)
    doc = OpenDocumentText()

    # Copier les styles du modele
    for style in template.styles.childNodes:
        doc.styles.addElement(deepcopy(style))

    # Copier les styles automatiques
    for style in template.automaticstyles.childNodes:
        doc.automaticstyles.addElement(deepcopy(style))

    print(f"Styles copies depuis {template_path}")
    return doc


def create_new_document():
    """Cree un nouveau document avec les styles Sesamath."""
    doc = OpenDocumentText()
    create_sesamath_styles(doc)
    return doc


def add_exercise(doc, numero: int, titre: str = None, questions: list = None):
    """Ajoute un exercice au document.

    Args:
        doc: Le document ODT
        numero: Numero de l'exercice
        titre: Titre optionnel de l'exercice
        questions: Liste de questions (strings)
    """
    # Titre de l'exercice
    if titre:
        titre_text = f"Exercice {numero} : {titre}"
    else:
        titre_text = f"Exercice {numero}"

    p = P(stylename="_5f_Titre_5f_Exercices_5f_avec_5f_Titre", text=titre_text)
    doc.text.addElement(p)

    # Questions
    if questions:
        for i, q in enumerate(questions, 1):
            p = P(stylename="_5f_Paragraphe", text=f"{i}. {q}")
            doc.text.addElement(p)

            # Zone de reponse
            p = P(stylename="_5f_Paragraphe_5f_Reponse_5f_Eleve")
            doc.text.addElement(p)


def add_response_lines(doc, count: int = 3):
    """Ajoute des lignes de reponse pointillees."""
    for _ in range(count):
        p = P(stylename="_5f_Paragraphe_5f_Reponse_5f_Pointilles_5f_Grises")
        # Ajouter des espaces pour creer les pointilles
        p.addText("." * 80)
        doc.text.addElement(p)


def main():
    parser = argparse.ArgumentParser(description="Creer un document ODT avec styles Sesamath")
    parser.add_argument("output", help="Fichier ODT de sortie")
    parser.add_argument("--template", "-t", help="Fichier ODT modele pour copier les styles")
    parser.add_argument("--demo", action="store_true", help="Creer un document de demonstration")

    args = parser.parse_args()

    # Creer le document
    if args.template and os.path.exists(args.template):
        doc = create_document_from_template(args.template, args.output)
    else:
        doc = create_new_document()

    # Mode demo: ajouter du contenu exemple
    if args.demo:
        # Titre
        h = H(outlinelevel=1, text="Fiche d'exercices - Mathematiques")
        doc.text.addElement(h)

        # Exercice 1
        add_exercise(doc, 1, "Calculs de base", [
            "Calculer 25 + 17 =",
            "Calculer 42 - 19 =",
            "Calculer 8 x 7 ="
        ])

        # Exercice 2
        add_exercise(doc, 2, "Probleme", [
            "Marie a 24 billes. Elle en donne 8 a Pierre. Combien lui en reste-t-il ?"
        ])
        add_response_lines(doc, 4)

        print("Document de demonstration cree")

    # Sauvegarder
    doc.save(args.output)
    size = os.path.getsize(args.output)
    print(f"Document sauvegarde: {args.output} ({size} octets)")


if __name__ == "__main__":
    main()
