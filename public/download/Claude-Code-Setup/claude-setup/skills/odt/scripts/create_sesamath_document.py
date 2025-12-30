#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creation de documents ODT avec styles Sesamath complets.

Ce script cree des documents pedagogiques avec:
- Les environnements didactiques (Definition, Propriete, Methode, Remarque, Exemple)
  avec titres encadres colores (texte blanc sur fond colore)
- Les en-tetes et pieds de page configures selon le domaine mathematique
- Les formules mathematiques en mode objets ODF
- Les exercices avec zones de reponse

Architecture des environnements Sesamath:
=========================================

Un environnement Sesamath se compose de:

1. PARAGRAPHE TITRE (style paragraphe _Titre_xxx):
   - Contient un SPAN avec style caractere _Caracteres_Titre_xxx
   - Le Span a: fond colore, texte blanc, bordure noire, padding

2. PARAGRAPHE(S) CORPS (style paragraphe _Paragraphe_xxx):
   - Bordure gauche coloree (4.51pt solid #couleur)
   - Padding 0.25cm

Couleurs par environnement:
- Definition/Vocabulaire: vert #77bc65 (bordure), #00a933 (fond titre)
- Propriete: rose #ec9ba4 (bordure), #bf0041 (fond titre)
- Methode: bleu #729fcf (bordure), #2a6099 (fond titre)
- Remarque: turquoise #78bbb2 (bordure), #50938a (fond titre)
- Exemple: gris #eeeeee (fond), noir #000000 (bordure)

Usage:
    from create_sesamath_document import SesamathDocument

    doc = SesamathDocument("mon_cours.odt", chapitre="Les fractions", niveau="6e", domaine="numerique")
    doc.add_definition("Definition", "Une fraction est...")
    doc.add_propriete("Propriete fondamentale", "On ne change pas la valeur...")
    doc.add_methode("Simplifier une fraction", ["Etape 1...", "Etape 2..."])
    doc.add_exercice("Simplifier", "Simplifie les fractions suivantes:", questions=["3/6", "4/8"])
    doc.add_formula("{3} over {4}")  # Formule StarMath
    doc.save()
"""

import os
import sys
import zipfile
import tempfile
import shutil
import re
import uuid
from pathlib import Path
from typing import List, Optional, Union

# Chemin vers le skill ODT
SKILL_PATH = Path(__file__).parent.parent
TEMPLATE_PATH = SKILL_PATH / "assets" / "template_sesamath_complet.odt"

try:
    from odf.opendocument import load
    from odf.text import P, H, Span, List as OdfList, ListItem, S
    from odf.draw import Frame, Object
    from odf.style import Style, ParagraphProperties, TableColumnProperties, TableCellProperties, TableProperties, TextProperties
    from odf.table import Table, TableColumn, TableRow, TableCell
    from odf import dc
except ImportError:
    print("Erreur: odfpy n'est pas installe. Executez: pip install odfpy")
    sys.exit(1)


# =============================================================================
# STYLES SESAMATH - Noms exacts avec accents
# =============================================================================

STYLES = {
    # --- Paragraphes de base ---
    'paragraphe': '_5f_Paragraphe',

    # --- VOCABULAIRE (vert #77bc65) ---
    'titre_vocabulaire': '_5f_Titre_5f_Vocabulaire',
    'para_vocabulaire': '_5f_Paragraphe_5f_Vocabulaire',
    'para_vocabulaire_bullet': '_5f_Paragraphe_5f_Vocabulaire_5f_bullet',
    'car_titre_vocabulaire': '_5f_Caractères_5f_Titre_5f_Vocabulaire',

    # --- DEFINITION (vert #77bc65) ---
    'titre_definition': '_5f_Titre_5f_Définition',
    'para_definition': '_5f_Paragraphe_5f_Définition',
    'para_definition_bullet': '_5f_Paragraphe_5f_Définition_5f_bullet',
    'car_titre_definition': '_5f_Caractères_5f_Titre_5f_Définition',

    # --- PROPRIETE (rose #ec9ba4) ---
    'titre_propriete': '_5f_Titre_5f_Propriété',
    'para_propriete': '_5f_Paragraphe_5f_Propriété',
    'para_propriete_bullet': '_5f_Paragraphe_5f_Propriété_5f_bullet',
    'car_titre_propriete': '_5f_Caractères_5f_Titre_5f_Propriété',

    # --- METHODE (bleu #729fcf) ---
    'titre_methode': '_5f_Titre_5f_Méthode',
    'para_methode': '_5f_Paragraphe_5f_Méthode',
    'para_methode_bullet': '_5f_Paragraphe_5f_Méthode_5f_Bullet',
    'car_titre_methode': '_5f_Caractères_5f_Titre_5f_Méthode',

    # --- REMARQUE (turquoise #78bbb2) ---
    'titre_remarque': '_5f_Titre_5f_Remarque',
    'para_remarque': '_5f_Paragraphe_5f_Remarque',
    'para_remarque_bullet': '_5f_Paragraphe_5f_Remarque_5f_bullet',
    'car_titre_remarque': '_5f_Caractères_5f_Titre_5f_Remarque',

    # --- EXEMPLE (gris #eeeeee) ---
    'titre_exemple': '_5f_Titre_5f_Exemple',
    'para_exemple': '_5f_Paragraphe_5f_Exemple',
    'para_exemple_bullet': '_5f_Paragraphe_5f_Exemple_5f_bullet',
    'para_exemple_avec_titre': '_5f_Paragraphe_5f_Exemple_5f_avec_5f_Titre',
    'para_exemple_sans_titre': '_5f_Paragraphe_5f_Exemple_5f_sans_5f_Titre',
    'car_titre_exemple': '_5f_Caractères_5f_Titre_5f_Exemple',

    # --- EXERCICES ---
    'titre_exercice_avec_titre': '_5f_Titre_5f_Exercices_5f_avec_5f_Titre',
    'titre_exercice_sans_titre': '_5f_Titre_5f_Exercices_5f_sans_5f_Titre',
    'premier_titre_exercice': '_5f_Premier_5f_Titre_5f_Exercices_5f_avec_5f_Num_5f_Exo_5f_sans_5f_Titre',
    'para_num_question': '_5f_Paragraphe_5f_avec_5f_Num_5f_Question',
    'car_numero_exercice': '_5f_Numéros_20_exercices',

    # --- REPONSES ELEVE ---
    'para_reponse_eleve': '_5f_Paragraphe_5f_Réponse_5f_Elève',
    'para_reponse_eleve_bullet': '_5f_Paragraphe_5f_Réponse_5f_Elève_5f_Bullet',
    'para_reponse_pointilles': '_5f_Paragraphe_5f_Réponse_5f_Pointillés_5f_Grisés',
    'para_reponse_fraction': '_5f_Paragraphe_5f_Réponse_5f_Elève_5f_Fraction',

    # --- TABLEAUX ---
    'tableau_centre': '_5f_Tableau_5f_Centré',
    'tableau_gauche': '_5f_Tableau_20_Gauche',
    'tableau_centre_gras': '_5f_Tableau_5f_Centré_5f_Gras',

    # --- CARACTERES ---
    'car_gras': '_5f_Caractères_5f_gras',
    'car_gras_blanc': '_5f_Caractères_5f_gras_5f_Blanc',
    'car_correction': '_5f_Caractères_5f_correction',
    'car_encadre': '_5f_Caractères_5f_encadré',
    'car_indice': '_5f_Caractères_5f_indice',
    'car_exposant': '_5f_Caractères_5f_exposant',
    'pointilles_gris': '_5f_pointillés_20_gris',
}

# =============================================================================
# MOTS-CLES AUTOMATIQUES - Mise en valeur automatique dans les environnements
# =============================================================================

# Liste des mots-cles a mettre en valeur automatiquement
# Classes en gras avec la couleur de l'environnement
KEYWORDS = {
    # Verbes d'action mathematiques
    'verbes_action': [
        'calculer', 'calcule', 'calculez', 'calculons',
        'simplifier', 'simplifie', 'simplifiez', 'simplifions',
        'demontrer', 'demontre', 'demontrez', 'demontrons',
        'démontrer', 'démontre', 'démontrez', 'démontrons',
        'prouver', 'prouve', 'prouvez', 'prouvons',
        'tracer', 'trace', 'tracez', 'tracons',
        'construire', 'construis', 'construisez', 'construisons',
        'determiner', 'determine', 'determinez', 'determinons',
        'déterminer', 'détermine', 'déterminez', 'déterminons',
        'resoudre', 'resous', 'resolvez', 'resolvons',
        'résoudre', 'résous', 'résolvez', 'résolvons',
        'factoriser', 'factorise', 'factorisez', 'factorisons',
        'developper', 'developpe', 'developpez', 'developpons',
        'développer', 'développe', 'développez', 'développons',
        'reduire', 'reduis', 'reduisez', 'reduisons',
        'réduire', 'réduis', 'réduisez', 'réduisons',
        'exprimer', 'exprime', 'exprimez', 'exprimons',
        'convertir', 'convertis', 'convertissez', 'convertissons',
        'comparer', 'compare', 'comparez', 'comparons',
        'ordonner', 'ordonne', 'ordonnez', 'ordonnons',
        'classer', 'classe', 'classez', 'classons',
        'representer', 'represente', 'representez', 'representons',
        'représenter', 'représente', 'représentez', 'représentons',
        'placer', 'place', 'placez', 'placons',
        'identifier', 'identifie', 'identifiez', 'identifions',
        'verifier', 'verifie', 'verifiez', 'verifions',
        'vérifier', 'vérifie', 'vérifiez', 'vérifions',
        'justifier', 'justifie', 'justifiez', 'justifions',
        'expliquer', 'explique', 'expliquez', 'expliquons',
        'deduire', 'deduis', 'deduisez', 'deduisons',
        'déduire', 'déduis', 'déduisez', 'déduisons',
        'appliquer', 'applique', 'appliquez', 'appliquons',
        'utiliser', 'utilise', 'utilisez', 'utilisons',
        'montrer', 'montre', 'montrez', 'montrons',
        'trouver', 'trouve', 'trouvez', 'trouvons',
        'donner', 'donne', 'donnez', 'donnons',
        'ecrire', 'ecris', 'ecrivez', 'ecrivons',
        'écrire', 'écris', 'écrivez', 'écrivons',
        'lire', 'lis', 'lisez', 'lisons',
        'mesurer', 'mesure', 'mesurez', 'mesurons',
        'arrondir', 'arrondis', 'arrondissez', 'arrondissons',
        'encadrer', 'encadre', 'encadrez', 'encadrons',
        'estimer', 'estime', 'estimez', 'estimons',
    ],

    # Mots de vocabulaire mathematique
    'vocabulaire': [
        'numerateur', 'numérateur',
        'denominateur', 'dénominateur',
        'quotient', 'dividende', 'diviseur', 'reste',
        'somme', 'difference', 'différence', 'produit',
        'facteur', 'terme', 'coefficient', 'exposant',
        'puissance', 'racine', 'carré', 'carre', 'cube',
        'inverse', 'oppose', 'opposé', 'valeur absolue',
        'fraction', 'pourcentage', 'proportion',
        'equation', 'équation', 'inéquation', 'inequation',
        'variable', 'inconnue', 'parametre', 'paramètre',
        'fonction', 'image', 'antecedent', 'antécédent',
        'ensemble', 'intervalle', 'union', 'intersection',
        'droite', 'segment', 'demi-droite',
        'angle', 'sommet', 'cote', 'côté',
        'triangle', 'rectangle', 'carre', 'carré', 'losange',
        'parallelogramme', 'parallélogramme', 'trapeze', 'trapèze',
        'cercle', 'rayon', 'diametre', 'diamètre', 'corde', 'arc',
        'perimetre', 'périmètre', 'aire', 'surface', 'volume',
        'mediane', 'médiane', 'bissectrice', 'hauteur', 'mediatrice', 'médiatrice',
        'parallele', 'parallèle', 'perpendiculaire', 'secante', 'sécante',
        'symetrie', 'symétrie', 'rotation', 'translation', 'homothetie', 'homothétie',
        'vecteur', 'norme', 'coordonnees', 'coordonnées', 'abscisse', 'ordonnee', 'ordonnée',
        'repere', 'repère', 'origine', 'axe',
        'probabilite', 'probabilité', 'frequence', 'fréquence', 'moyenne', 'mediane', 'médiane',
        'ecart-type', 'écart-type', 'variance', 'effectif',
    ],

    # Mots logiques et structurants
    'logique': [
        'donc', 'ainsi', 'par consequent', 'par conséquent',
        'car', 'parce que', 'puisque',
        'si', 'alors', 'sinon',
        'soit', 'posons', 'notons', 'appelons',
        'or', 'mais', 'cependant', 'toutefois',
        'de plus', 'en outre', 'egalement', 'également',
        'en effet', 'en particulier', 'notamment',
        'c\'est-a-dire', 'c\'est-à-dire', 'autrement dit',
        'par exemple', 'par definition', 'par définition',
        'reciproquement', 'réciproquement', 'inversement',
        'attention', 'remarque', 'noter que', 'notons que',
    ],

    # Expressions mathematiques importantes
    'expressions': [
        'est egal a', 'est égal à', 'est equivalent a', 'est équivalent à',
        'est inferieur a', 'est inférieur à', 'est superieur a', 'est supérieur à',
        'est proportionnel a', 'est proportionnel à',
        'est perpendiculaire a', 'est perpendiculaire à',
        'est parallele a', 'est parallèle à',
        'est symetrique de', 'est symétrique de',
        'appartient a', 'appartient à', 'n\'appartient pas a', 'n\'appartient pas à',
        'divise', 'est divisible par', 'est multiple de',
        'est un diviseur de', 'est un multiple de',
        'si et seulement si', 'est defini par', 'est défini par',
    ],
}

# Couleurs par type d'environnement (pour le texte des mots-cles)
ENVIRONMENT_COLORS = {
    'definition': '#00a933',   # Vert
    'vocabulaire': '#00a933',  # Vert
    'propriete': '#bf0041',    # Rose
    'methode': '#2a6099',      # Bleu
    'remarque': '#50938a',     # Turquoise
    'exemple': '#333333',      # Gris fonce
    'exercice': '#2a6099',     # Bleu (comme methode)
}

# Master pages par domaine mathematique
MASTER_PAGES = {
    'geometrie': 'INTRO_5f_GEOMETRIE_5f_CLR_5f_1ca2b8',
    'numerique': 'INTRO_5f_NUMERIQUE_5f_CLR_5f_d7e12c',
    'mesures': 'INTRO_5f_MESURES_5f_CLR_5f_7fb241',
    'gestion_donnees': 'INTRO_5f_DONNEES_5f_CLR_5f_9d0f89',
    'problemes': 'INTRO_5f_PROBLEMES_5f_CLR_5f_d62e4e',
    'standard': 'Standard',
}

# Master pages SERIE (pour exercices, 1 ou 2 colonnes)
MASTER_PAGES_SERIE = {
    'geometrie_1col': 'SERIE_5f_GEOMETRIE_5f_CLR_5f_1ca2b8_5f_1COL',
    'geometrie_2col': 'SERIE_5f_GEOMETRIE_5f_CLR_5f_1ca2b8_5f_2COL',
    'numerique_1col': 'SERIE_5f_NUMERIQUE_5f_CLR_5f_d7e12c_5f_1COL',
    'numerique_2col': 'SERIE_5f_NUMERIQUE_5f_CLR_5f_d7e12c_5f_2COL',
    'mesures_1col': 'SERIE_5f_MESURES_5f_CLR_5f_7fb241_5f_1COL',
    'mesures_2col': 'SERIE_5f_MESURES_5f_CLR_5f_7fb241_5f_2COL',
    'gestion_donnees_1col': 'SERIE_5f_GESTION_5f_DE_5f_DONNEES_5f_CLR_5f_9d0f89_5f_1COL',
    'gestion_donnees_2col': 'SERIE_5f_GESTION_5f_DE_5f_DONNEES_5f_CLR_5f_9d0f89_5f_2COL',
    'problemes_1col': 'SERIE_5f_PROBLEMES_5f_CLR_5f_d62e4e_5f_1COL',
    'problemes_2col': 'SERIE_5f_PROBLEMES_5f_CLR_5f_d62e4e_5f_2COL',
}


class SesamathDocument:
    """
    Classe pour creer des documents ODT avec les styles Sesamath.

    Exemple:
        doc = SesamathDocument("cours.odt", chapitre="Fractions", niveau="6e")
        doc.add_definition("Definition", "Une fraction est un nombre...")
        doc.add_propriete("Propriete", "On ne change pas la valeur...")
        doc.save()
    """

    def __init__(self, output_path: str, chapitre: str = None,
                 niveau: str = None, domaine: str = None,
                 titre_dans_contenu: bool = False):
        """
        Initialise un nouveau document Sesamath.

        Args:
            output_path: Chemin du fichier de sortie
            chapitre: Nom du chapitre - sera injecte dans les en-tetes de page
            niveau: Niveau scolaire (6e, 5e, 4e, 3e, 2nde, 1ere, tle)
            domaine: Domaine mathematique (numerique, geometrie, mesures, etc.)
            titre_dans_contenu: Si True, ajoute aussi le titre comme H1 dans le contenu
                               Par defaut False: le titre apparait SEULEMENT dans les en-tetes
        """
        self.output_path = output_path
        self.chapitre = chapitre
        self.niveau = niveau
        self.domaine = domaine
        self.titre_dans_contenu = titre_dans_contenu
        self.exercice_counter = 0
        self.formula_counter = 0
        self.formulas_to_insert = []  # Liste des formules a inserer en post-traitement
        self.master_page_set = False
        self.corrections = []  # Liste des corrections pour page separee
        self.in_columns = False  # Indique si on est dans une section multicolonne
        self.column_count = 1  # Nombre de colonnes actuel
        self._page_margins = None  # Marges de page personnalisées

        # Charger le template
        if not TEMPLATE_PATH.exists():
            raise FileNotFoundError(f"Template non trouve: {TEMPLATE_PATH}")

        self.doc = load(str(TEMPLATE_PATH))

        # Effacer le contenu existant
        for child in list(self.doc.text.childNodes):
            self.doc.text.removeChild(child)

        # Configurer la master page selon le domaine
        if domaine and domaine in MASTER_PAGES:
            self._set_master_page(MASTER_PAGES[domaine])

        # Nom du style de numero de question (pour reference dans add_exercice)
        self._question_number_style_name = "QuestionNumberStyle"

        # Creer le style pour les numeros de questions (petit cadre bleu)
        self._create_question_number_style()

        # Ajouter le titre du chapitre dans le CONTENU seulement si demande
        # Note: Le titre est TOUJOURS injecte dans les en-tetes via _inject_header_title()
        if chapitre and titre_dans_contenu:
            self._add_chapter_title()

    def _set_master_page(self, master_page_name: str):
        """
        Configure la master page pour le document.

        La master page definit les en-tetes et pieds de page avec les couleurs
        du domaine mathematique.

        Args:
            master_page_name: Nom de la master page (ex: 'INTRO_5f_NUMERIQUE_5f_CLR_5f_d7e12c')
        """
        # Creer un style automatique qui reference la master page
        # Ce style sera applique au premier paragraphe du document
        style_name = f"MP_Auto_{uuid.uuid4().hex[:8]}"

        # On va stocker cette info pour le post-traitement
        # car odfpy ne permet pas facilement de creer des styles avec master-page-name
        self._master_page_style = {
            'name': style_name,
            'master_page': master_page_name
        }
        self.master_page_set = True

    def _add_chapter_title(self):
        """Ajoute le titre du chapitre avec infos niveau/domaine."""
        h = H(outlinelevel=1, text=self.chapitre)
        self.doc.text.addElement(h)

        if self.niveau or self.domaine:
            info_parts = []
            if self.niveau:
                info_parts.append(f"Niveau : {self.niveau}")
            if self.domaine:
                info_parts.append(f"Domaine : {self.domaine.replace('_', ' ').title()}")
            p = P(stylename=STYLES['paragraphe'], text=" - ".join(info_parts))
            self.doc.text.addElement(p)

        # Ligne vide
        self.add_empty_line()

    def _create_question_number_style(self):
        """
        Cree un style de caractere pour les numeros de questions.

        Le style a un petit cadre decoratif bleu clair pour differencier
        visuellement les numeros de questions des donnees de l'exercice.

        Caracteristiques:
        - Fond bleu tres clair (#e8f0fa)
        - Bordure fine bleu fonce (#2a6099)
        - Texte gras bleu fonce
        - Leger padding
        """
        # Creer le style de caractere dans automatic-styles
        style = Style(name=self._question_number_style_name, family="text")

        # Proprietes du texte: gras, couleur bleue, avec fond et bordure
        text_props = TextProperties(
            fontweight="bold",
            fontweightasian="bold",
            fontweightcomplex="bold",
            color="#2a6099",
            backgroundcolor="#e8f0fa"
        )
        # Note: Les bordures de caracteres ne sont pas bien supportees par odfpy
        # On va ajouter le style via post-processing XML pour avoir la bordure
        style.addElement(text_props)

        self.doc.automaticstyles.addElement(style)

        # Marquer qu'on a besoin du post-processing pour la bordure
        self._question_style_needs_border = True

    def _get_or_create_keyword_style(self, env_type: str) -> str:
        """
        Obtient ou cree un style de caractere pour les mots-cles d'un environnement.

        Args:
            env_type: Type d'environnement (definition, propriete, methode, etc.)

        Returns:
            Nom du style de caractere
        """
        style_name = f"Keyword_{env_type}"

        # Verifier si le style existe deja
        if not hasattr(self, '_keyword_styles'):
            self._keyword_styles = {}

        if style_name in self._keyword_styles:
            return style_name

        # Creer le style
        color = ENVIRONMENT_COLORS.get(env_type, '#2a6099')

        style = Style(name=style_name, family="text")
        text_props = TextProperties(
            fontweight="bold",
            fontweightasian="bold",
            fontweightcomplex="bold",
            color=color
        )
        style.addElement(text_props)
        self.doc.automaticstyles.addElement(style)

        self._keyword_styles[style_name] = color
        return style_name

    def _add_text_with_keywords(self, parent_element, text: str, env_type: str):
        """
        Ajoute du texte a un element en mettant en valeur les mots-cles.

        Les mots-cles detectes sont mis en gras avec la couleur de l'environnement.

        Args:
            parent_element: Element parent (P ou autre)
            text: Texte a traiter
            env_type: Type d'environnement pour la couleur
        """
        # Compiler tous les mots-cles en une seule liste
        all_keywords = []
        for category in KEYWORDS.values():
            all_keywords.extend(category)

        # Trier par longueur decroissante pour matcher les expressions longues d'abord
        all_keywords = sorted(set(all_keywords), key=len, reverse=True)

        # Creer une regex qui matche tous les mots-cles (insensible a la casse)
        # Utiliser des word boundaries pour eviter les faux positifs
        if not all_keywords:
            parent_element.addText(text)
            return

        # Construire le pattern avec echappement et word boundaries
        pattern_parts = [rf'\b{re.escape(kw)}\b' for kw in all_keywords]
        pattern = '|'.join(pattern_parts)

        # Obtenir le style pour cet environnement
        style_name = self._get_or_create_keyword_style(env_type)

        # Parser le texte et creer les spans
        last_end = 0
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            # Ajouter le texte avant le match
            if match.start() > last_end:
                parent_element.addText(text[last_end:match.start()])

            # Ajouter le mot-cle en gras colore
            span = Span(stylename=style_name, text=match.group())
            parent_element.addElement(span)

            last_end = match.end()

        # Ajouter le texte restant
        if last_end < len(text):
            parent_element.addText(text[last_end:])

    def add_empty_line(self):
        """Ajoute une ligne vide."""
        p = P(stylename=STYLES['paragraphe'])
        self.doc.text.addElement(p)

    def add_paragraph(self, text: str, style: str = 'paragraphe'):
        """Ajoute un paragraphe simple."""
        p = P(stylename=STYLES.get(style, STYLES['paragraphe']), text=text)
        self.doc.text.addElement(p)

    def add_heading(self, text: str, level: int = 2):
        """
        Ajoute un titre de niveau specifie.

        Les titres H1 sont mis en valeur (gras, plus grand, souligne).
        """
        # Utiliser le style Heading correspondant au niveau
        style_name = f"Heading_20_{level}"
        h = H(outlinelevel=level, stylename=style_name, text=text)
        self.doc.text.addElement(h)

        # Marquer qu'on utilise des H1 personnalises
        if level == 1:
            if not hasattr(self, '_custom_h1_needed'):
                self._custom_h1_needed = True

    # =========================================================================
    # ENVIRONNEMENTS DIDACTIQUES
    # =========================================================================

    def _add_environnement(self, env_type: str, titre: str, contenu: Union[str, List[str]],
                           formule: str = None, sous_titre: str = None):
        """
        Ajoute un environnement didactique complet.

        Args:
            env_type: Type d'environnement (definition, propriete, methode, remarque, exemple, vocabulaire)
            titre: Texte du titre (sera affiche dans un encadre colore)
            contenu: Texte ou liste de textes pour le contenu
            formule: Formule StarMath optionnelle à intégrer dans le contenu
            sous_titre: Sous-titre optionnel (ex: "fraction" pour "Définition : fraction")
                       Seul le titre principal est encadré, le sous-titre est en texte normal

        Exemple:
            # "Définition : Fraction" avec seulement "Définition" encadré
            _add_environnement('definition', 'Définition', contenu, sous_titre='Fraction')
        """
        # Creer le paragraphe titre avec le Span encadre colore
        p_titre = P(stylename=STYLES[f'titre_{env_type}'])

        # Ajouter le Span avec le style de caractere (fond colore, texte blanc)
        span_titre = Span(stylename=STYLES[f'car_titre_{env_type}'], text=f" {titre} ")
        p_titre.addElement(span_titre)

        # Ajouter le sous-titre si present (en texte normal, non encadre)
        if sous_titre:
            p_titre.addText(f" : {sous_titre}")

        self.doc.text.addElement(p_titre)

        # Ajouter le contenu avec mise en valeur automatique des mots-cles
        if isinstance(contenu, str):
            # Si une formule est fournie, on l'intègre dans le paragraphe
            if formule:
                self.formula_counter += 1
                placeholder_id = f"__FORMULA_{self.formula_counter}__"
                self.formulas_to_insert.append({
                    'id': placeholder_id,
                    'starmath': formule,
                    'inline': True
                })
                p_contenu = P(stylename=STYLES[f'para_{env_type}'])
                # Mise en valeur des mots-cles dans le texte
                self._add_text_with_keywords(p_contenu, contenu, env_type)
                p_contenu.addText(f"  {placeholder_id}")
            else:
                p_contenu = P(stylename=STYLES[f'para_{env_type}'])
                # Mise en valeur des mots-cles
                self._add_text_with_keywords(p_contenu, contenu, env_type)
            self.doc.text.addElement(p_contenu)
        else:
            # Liste de contenus (avec puces) - mise en valeur des mots-cles
            for item in contenu:
                p_item = P(stylename=STYLES[f'para_{env_type}_bullet'])
                p_item.addText("• ")
                self._add_text_with_keywords(p_item, item, env_type)
                self.doc.text.addElement(p_item)

    def add_definition(self, titre: str, contenu: Union[str, List[str]], formule: str = None):
        """
        Ajoute un bloc Definition.

        Le titre apparait dans un encadre vert (#00a933) avec texte blanc.
        Le contenu a une bordure gauche verte (#77bc65).

        Args:
            titre: Texte du titre (ex: "Definition")
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle (ex: "{a} over {b}")
        """
        self._add_environnement('definition', titre, contenu, formule)

    def add_vocabulaire(self, titre: str, contenu: Union[str, List[str]], formule: str = None):
        """
        Ajoute un bloc Vocabulaire.

        Memes couleurs que Definition (vert).

        Args:
            titre: Texte du titre
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle
        """
        self._add_environnement('vocabulaire', titre, contenu, formule)

    def add_propriete(self, titre: str, contenu: Union[str, List[str]], formule: str = None):
        """
        Ajoute un bloc Propriete.

        Le titre apparait dans un encadre rose (#bf0041) avec texte blanc.
        Le contenu a une bordure gauche rose (#ec9ba4).

        Args:
            titre: Texte du titre
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle
        """
        self._add_environnement('propriete', titre, contenu, formule)

    def add_methode(self, titre: str, contenu: Union[str, List[str]], formule: str = None):
        """
        Ajoute un bloc Methode.

        Le titre apparait dans un encadre bleu (#2a6099) avec texte blanc.
        Le contenu a une bordure gauche bleue (#729fcf).

        Args:
            titre: Texte du titre
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle
        """
        self._add_environnement('methode', titre, contenu, formule)

    def add_remarque(self, titre: str, contenu: Union[str, List[str]], formule: str = None):
        """
        Ajoute un bloc Remarque.

        Le titre apparait dans un encadre turquoise (#50938a) avec texte blanc.
        Le contenu a une bordure gauche turquoise (#78bbb2).

        Args:
            titre: Texte du titre
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle
        """
        self._add_environnement('remarque', titre, contenu, formule)

    def add_exemple(self, titre: str = None, contenu: Union[str, List[str]] = None, formule: str = None):
        """
        Ajoute un bloc Exemple.

        Si titre est fourni: utilise le style avec titre (fond gris, bordure)
        Sinon: utilise le style simple

        Args:
            titre: Texte du titre (optionnel)
            contenu: Texte ou liste de textes
            formule: Formule StarMath optionnelle
        """
        if titre:
            self._add_environnement('exemple', titre, contenu, formule)
        else:
            # Exemple sans titre
            if isinstance(contenu, str):
                p = P(stylename=STYLES['para_exemple_sans_titre'], text=contenu)
                self.doc.text.addElement(p)
            else:
                for item in contenu:
                    p = P(stylename=STYLES['para_exemple_bullet'], text=f"• {item}")
                    self.doc.text.addElement(p)

    # =========================================================================
    # MULTICOLONNE
    # =========================================================================

    def start_columns(self, num_columns: int = 2, gap: str = "0.5cm", separator: bool = True):
        """
        Demarre une section multicolonne.

        Args:
            num_columns: Nombre de colonnes (2, 3 ou 4)
            gap: Espacement entre les colonnes (defaut: 0.5cm)
            separator: Afficher une ligne verticale entre les colonnes (defaut: True)

        Exemple:
            doc.start_columns(2, gap="1cm")
            doc.add_paragraph("Texte en colonne 1")
            doc.column_break()
            doc.add_paragraph("Texte en colonne 2")
            doc.end_columns()
        """
        self.in_columns = True
        self.column_count = num_columns
        self._column_gap = gap
        self._column_item_counter = 0  # Compteur d'elements dans la section multicolonne

        # Ajouter un placeholder pour le debut de section
        # Le post-traitement ajoutera le style de section avec colonnes
        self._section_counter = getattr(self, '_section_counter', 0) + 1
        section_id = f"__SECTION_START_{self._section_counter}__"
        self._current_section_id = section_id
        self._sections_to_process = getattr(self, '_sections_to_process', [])
        self._sections_to_process.append({
            'start_id': section_id,
            'end_id': None,
            'columns': num_columns,
            'gap': gap,
            'separator': separator
        })

        p = P(stylename=STYLES['paragraphe'], text=section_id)
        self.doc.text.addElement(p)

    def end_columns(self):
        """Termine la section multicolonne et revient a une seule colonne."""
        if not self.in_columns:
            return

        self.in_columns = False
        self.column_count = 1
        self._column_item_counter = 0  # Reset du compteur

        # Ajouter un placeholder pour la fin de section
        end_id = f"__SECTION_END_{self._section_counter}__"
        self._sections_to_process[-1]['end_id'] = end_id

        p = P(stylename=STYLES['paragraphe'], text=end_id)
        self.doc.text.addElement(p)

    def column_break(self):
        """Insere un saut de colonne (passe a la colonne suivante)."""
        # Placeholder pour saut de colonne
        break_id = f"__COLUMN_BREAK_{uuid.uuid4().hex[:8]}__"
        if not hasattr(self, '_column_breaks'):
            self._column_breaks = []
        self._column_breaks.append(break_id)

        p = P(stylename=STYLES['paragraphe'], text=break_id)
        self.doc.text.addElement(p)

    # =========================================================================
    # GRILLE D'EXERCICES (TABLEAU)
    # =========================================================================

    def start_exercise_grid(self, columns: int = 2):
        """
        Demarre une grille d'exercices sous forme de tableau invisible.

        RECOMMANDE pour disposer les exercices en grille 2x2, 3x3, etc.
        Contrairement a start_columns(), les exercices sont places dans
        des cellules de tableau, garantissant un alignement parfait.

        Args:
            columns: Nombre de colonnes (defaut: 2)

        Exemple:
            doc.start_exercise_grid(2)  # Grille 2 colonnes
            doc.add_exercice("Exo 1", ...)  # Cellule 1,1
            doc.add_exercice("Exo 2", ...)  # Cellule 1,2
            doc.add_exercice("Exo 3", ...)  # Cellule 2,1
            doc.add_exercice("Exo 4", ...)  # Cellule 2,2
            doc.end_exercise_grid()
        """
        self.in_grid = True
        self.grid_columns = columns
        self._grid_exercises = []  # Stocke les exercices pour construction du tableau
        self._grid_cell_content = []  # Contenu de la cellule courante

    def end_exercise_grid(self):
        """
        Termine la grille d'exercices et construit le tableau.

        Le tableau est cree avec des bordures invisibles et des cellules
        de largeur egale.
        """
        if not getattr(self, 'in_grid', False):
            return

        # Finaliser la derniere cellule si elle a du contenu
        if self._grid_cell_content:
            self._grid_exercises.append(self._grid_cell_content)
            self._grid_cell_content = []

        if not self._grid_exercises:
            self.in_grid = False
            return

        # Creer les styles de tableau
        table_name = f"ExerciseGrid_{uuid.uuid4().hex[:6]}"

        # Style de tableau (largeur 100%, sans bordure)
        table_style = Style(name=f"{table_name}_style", family="table")
        table_style.addElement(TableProperties(width="100%", align="margins"))
        self.doc.automaticstyles.addElement(table_style)

        # Style de colonne
        col_style = Style(name=f"{table_name}_col", family="table-column")
        col_width = f"{17 / self.grid_columns:.2f}cm"  # ~17cm disponible
        col_style.addElement(TableColumnProperties(columnwidth=col_width))
        self.doc.automaticstyles.addElement(col_style)

        # Style de cellule (sans bordure, padding)
        cell_style = Style(name=f"{table_name}_cell", family="table-cell")
        cell_style.addElement(TableCellProperties(
            padding="0.2cm",
            verticalalign="top"
        ))
        self.doc.automaticstyles.addElement(cell_style)

        # Creer le tableau
        table = Table(name=table_name)

        # Ajouter les colonnes
        for _ in range(self.grid_columns):
            table.addElement(TableColumn(stylename=f"{table_name}_col"))

        # Remplir les lignes
        num_exercises = len(self._grid_exercises)
        num_rows = (num_exercises + self.grid_columns - 1) // self.grid_columns

        for row_idx in range(num_rows):
            row = TableRow()

            for col_idx in range(self.grid_columns):
                cell = TableCell(stylename=f"{table_name}_cell")
                exo_idx = row_idx * self.grid_columns + col_idx

                if exo_idx < num_exercises:
                    # Ajouter le contenu de l'exercice
                    for element in self._grid_exercises[exo_idx]:
                        cell.addElement(element)
                else:
                    # Cellule vide
                    cell.addElement(P(text=""))

                row.addElement(cell)

            table.addElement(row)

        self.doc.text.addElement(table)

        # Reset
        self.in_grid = False
        self._grid_exercises = []
        self._grid_cell_content = []

    def _add_to_grid_cell(self, element):
        """Ajoute un element a la cellule courante de la grille."""
        if getattr(self, 'in_grid', False):
            self._grid_cell_content.append(element)
        else:
            self.doc.text.addElement(element)

    def _finalize_grid_cell(self):
        """Finalise la cellule courante et passe a la suivante."""
        if getattr(self, 'in_grid', False) and self._grid_cell_content:
            self._grid_exercises.append(self._grid_cell_content)
            self._grid_cell_content = []

    # =========================================================================
    # EXERCICES
    # =========================================================================

    def add_exercice(self, titre: str, enonce: str = None,
                     questions: List[str] = None, lignes_reponse: int = 3,
                     correction: Union[str, List[str]] = None):
        """
        Ajoute un exercice complet avec correction optionnelle.

        Si appele dans une grille (start_exercise_grid), l'exercice est
        ajoute dans une cellule du tableau.

        Args:
            titre: Titre de l'exercice (ex: "Simplifier les fractions")
            enonce: Texte d'enonce (optionnel)
            questions: Liste de questions numerotees (optionnel)
            lignes_reponse: Nombre de lignes de reponse par question
            correction: Correction de l'exercice (str ou liste).
                        Si fournie, sera ajoutee sur la page de corrections.
        """
        self.exercice_counter += 1
        current_exo_num = self.exercice_counter

        # Fonction d'ajout (grille ou document direct)
        def add_element(el):
            if getattr(self, 'in_grid', False):
                self._grid_cell_content.append(el)
            else:
                self.doc.text.addElement(el)

        # Titre de l'exercice avec numero
        p_titre = P(stylename=STYLES['titre_exercice_avec_titre'])
        span_num = Span(stylename=STYLES['car_numero_exercice'], text=f" {current_exo_num} ")
        p_titre.addElement(span_num)
        p_titre.addText(f"  {titre}")
        add_element(p_titre)

        # Enonce avec mise en valeur des mots-cles
        if enonce:
            p_enonce = P(stylename=STYLES['paragraphe'])
            self._add_text_with_keywords(p_enonce, enonce, 'exercice')
            add_element(p_enonce)

        # Questions avec mise en valeur des mots-cles
        if questions:
            for i, question in enumerate(questions, 1):
                # Question numerotee avec numero encadre
                p_q = P(stylename=STYLES['para_num_question'])
                # Numero dans un span avec style decoratif (espaces pour aeration)
                span_num = Span(stylename=self._question_number_style_name, text=f" {i}. ")
                p_q.addElement(span_num)
                # Espaces apres le cadre (S avec c=3 pour 3 espaces)
                space_element = S()
                space_element.setAttribute('c', '3')
                p_q.addElement(space_element)
                # Mise en valeur des mots-cles dans la question
                self._add_text_with_keywords(p_q, question, 'exercice')
                add_element(p_q)

                # Lignes de reponse
                for _ in range(lignes_reponse):
                    p_rep = P(stylename=STYLES['para_reponse_pointilles'])
                    add_element(p_rep)

        # Stocker la correction pour la page separee
        if correction:
            self.corrections.append({
                'exercice_num': current_exo_num,
                'titre': titre,
                'correction': correction,
                'is_formula': False
            })

        # GRILLE TABLEAU: finaliser la cellule pour passer a la suivante
        if getattr(self, 'in_grid', False):
            self._finalize_grid_cell()
        # MULTICOLONNE (ancien systeme): saut de colonne
        elif self.in_columns:
            self._column_item_counter += 1
            if self._column_item_counter % self.column_count != 0:
                self.column_break()

    def add_exercice_math(self, titre: str, enonce: str = None,
                          questions_formulas: List[str] = None, lignes_reponse: int = 1,
                          corrections_formulas: List[str] = None):
        """
        Ajoute un exercice avec des questions et corrections en mode formule StarMath.

        Args:
            titre: Titre de l'exercice
            enonce: Texte d'enonce (optionnel)
            questions_formulas: Liste de formules StarMath pour les questions
            lignes_reponse: Nombre de lignes de reponse par question
            corrections_formulas: Liste de formules StarMath pour les corrections
        """
        self.exercice_counter += 1
        current_exo_num = self.exercice_counter

        # Titre de l'exercice avec numero
        p_titre = P(stylename=STYLES['titre_exercice_avec_titre'])
        span_num = Span(stylename=STYLES['car_numero_exercice'], text=f" {current_exo_num} ")
        p_titre.addElement(span_num)
        p_titre.addText(f"  {titre}")
        self.doc.text.addElement(p_titre)

        # Enonce avec mise en valeur des mots-cles
        if enonce:
            p_enonce = P(stylename=STYLES['paragraphe'])
            self._add_text_with_keywords(p_enonce, enonce, 'exercice')
            self.doc.text.addElement(p_enonce)

        # Questions en formules
        if questions_formulas:
            for i, formula in enumerate(questions_formulas, 1):
                # Numero de question en gras + formule
                self.add_formula_inline(f"{i}. ", formula, "",
                                        style='para_num_question', bold_prefix=True)

                # Lignes de reponse
                for _ in range(lignes_reponse):
                    p_rep = P(stylename=STYLES['para_reponse_pointilles'])
                    self.doc.text.addElement(p_rep)

        # Stocker les corrections en mode formule
        if corrections_formulas:
            self.corrections.append({
                'exercice_num': current_exo_num,
                'titre': titre,
                'correction': corrections_formulas,
                'is_formula': True
            })

        # GRILLE AUTO: saut de colonne pour remplir la grille
        if self.in_columns:
            self._column_item_counter += 1
            if self._column_item_counter % self.column_count != 0:
                self.column_break()

    def add_zone_reponse(self, lignes: int = 3, style: str = 'pointilles'):
        """
        Ajoute une zone de reponse eleve.

        Args:
            lignes: Nombre de lignes
            style: 'pointilles' ou 'vide'
        """
        style_name = STYLES['para_reponse_pointilles'] if style == 'pointilles' else STYLES['para_reponse_eleve']
        for _ in range(lignes):
            p = P(stylename=style_name)
            self.doc.text.addElement(p)

    def page_break(self):
        """Insere un saut de page."""
        # Placeholder pour saut de page
        break_id = f"__PAGE_BREAK_{uuid.uuid4().hex[:8]}__"
        if not hasattr(self, '_page_breaks'):
            self._page_breaks = []
        self._page_breaks.append(break_id)

        p = P(stylename=STYLES['paragraphe'], text=break_id)
        self.doc.text.addElement(p)

    def set_page_margins(self, left: str = None, right: str = None,
                         top: str = None, bottom: str = None):
        """
        Definit les marges de page du document.

        Modifie UNIQUEMENT les marges du page-layout (pas les styles de paragraphe).
        Utile pour ajuster l'espace avec la bande coloree Sesamath.

        Args:
            left: Marge gauche (ex: "2.5cm")
            right: Marge droite (ex: "2cm")
            top: Marge haute (ex: "2cm")
            bottom: Marge basse (ex: "2cm")
        """
        self._page_margins = {
            'left': left,
            'right': right,
            'top': top,
            'bottom': bottom
        }

    def add_corrections_page(self, titre: str = None, columns: int = 2):
        """
        Ajoute une page dediee aux corrections des exercices.

        Cette methode insere automatiquement:
        - Un saut de page avec la meme master page
        - Un titre "[chapitre] - Solutions"
        - Toutes les corrections stockees via add_exercice(correction=...)
        - Le tout en multicolonne pour economiser de la place

        Args:
            titre: Titre de la page de corrections (defaut: "[chapitre] - Solutions")
            columns: Nombre de colonnes (defaut: 2)

        Exemple:
            doc.add_exercice("Ex 1", correction="a) 3/4  b) 1/2")
            doc.add_exercice("Ex 2", correction=["1. x = 5", "2. y = 3"])
            doc.add_corrections_page()  # Genere automatiquement la page
        """
        if not self.corrections:
            return  # Pas de corrections a afficher

        # Saut de page - on va forcer la master page via placeholder
        self._corrections_page_break_id = f"__CORRECTIONS_PAGE_BREAK_{uuid.uuid4().hex[:8]}__"
        if not hasattr(self, '_corrections_breaks'):
            self._corrections_breaks = []
        self._corrections_breaks.append(self._corrections_page_break_id)

        p = P(stylename=STYLES['paragraphe'], text=self._corrections_page_break_id)
        self.doc.text.addElement(p)

        # Titre des corrections (coherent avec le chapitre)
        if titre is None:
            if self.chapitre:
                titre = f"{self.chapitre} - Solutions"
            else:
                titre = "Solutions"

        self.add_heading(titre, level=1)
        self.add_empty_line()

        # Demarrer le multicolonne
        if columns > 1:
            self.start_columns(columns)

        # Afficher chaque correction
        for corr in self.corrections:
            exo_num = corr['exercice_num']
            exo_titre = corr['titre']
            correction = corr['correction']

            # Titre de l'exercice en gras
            p_titre = P(stylename=STYLES['paragraphe'])
            span = Span(stylename=STYLES['car_gras'], text=f"Exercice {exo_num}")
            p_titre.addElement(span)
            if exo_titre:
                p_titre.addText(f" - {exo_titre}")
            self.doc.text.addElement(p_titre)

            # Contenu de la correction
            is_formula = corr.get('is_formula', False)

            if is_formula:
                # Corrections en mode formule (sans surlignage, format maths)
                if isinstance(correction, list):
                    for i, formula in enumerate(correction, 1):
                        # Numero en gras + formule
                        self.add_formula_inline(f"{i}. ", formula, "",
                                                style='paragraphe', bold_prefix=True)
                else:
                    self.add_formula(correction)
            else:
                # Corrections en texte rouge
                if isinstance(correction, str):
                    p_corr = P(stylename=STYLES['paragraphe'])
                    span_corr = Span(stylename=STYLES['car_correction'], text=correction)
                    p_corr.addElement(span_corr)
                    self.doc.text.addElement(p_corr)
                else:
                    # Liste de corrections
                    for item in correction:
                        p_item = P(stylename=STYLES['paragraphe'])
                        span_item = Span(stylename=STYLES['car_correction'], text=f"  {item}")
                        p_item.addElement(span_item)
                        self.doc.text.addElement(p_item)

            self.add_empty_line()

        # Terminer le multicolonne
        if columns > 1:
            self.end_columns()

    # =========================================================================
    # FORMULES MATHEMATIQUES
    # =========================================================================

    def add_formula(self, starmath: str, inline: bool = False):
        """
        Ajoute une formule mathematique.

        Args:
            starmath: Formule en syntaxe StarMath (ex: "{3} over {4}")
            inline: Si True, insere dans le texte courant

        Syntaxe StarMath courante:
            Fraction: {a} over {b}
            Racine: sqrt{x}
            Puissance: x^{2}
            Indice: x_{i}
            Multiplication: times ou cdot
            Pi: %pi
            Somme: sum from{i=1} to{n}
        """
        self.formula_counter += 1
        placeholder_id = f"__FORMULA_{self.formula_counter}__"

        # Stocker la formule pour post-traitement
        self.formulas_to_insert.append({
            'id': placeholder_id,
            'starmath': starmath,
            'inline': inline
        })

        # Ajouter un placeholder qui sera remplace en post-traitement
        p = P(stylename=STYLES['paragraphe'], text=placeholder_id)
        self.doc.text.addElement(p)

    def add_formula_inline(self, text_before: str, starmath: str, text_after: str = "",
                            style: str = 'paragraphe', bold_prefix: bool = False):
        """
        Ajoute du texte avec une formule inline.

        Args:
            text_before: Texte avant la formule
            starmath: Formule StarMath
            text_after: Texte apres la formule
            style: Style de paragraphe (defaut: 'paragraphe')
            bold_prefix: Si True, le texte avant la formule est en gras (pour numeros)
        """
        self.formula_counter += 1
        placeholder_id = f"__FORMULA_{self.formula_counter}__"

        # Stocker la formule pour post-traitement
        self.formulas_to_insert.append({
            'id': placeholder_id,
            'starmath': starmath,
            'inline': True,
            'text_before': text_before,
            'text_after': text_after
        })

        p = P(stylename=STYLES.get(style, STYLES['paragraphe']))
        if bold_prefix and text_before:
            span = Span(stylename=STYLES['car_gras'], text=text_before)
            p.addElement(span)
        else:
            p.addText(text_before)
        p.addText(f" {placeholder_id} ")
        if text_after:
            p.addText(text_after)
        self.doc.text.addElement(p)

    # =========================================================================
    # STYLES SPECIAUX ET ACCENTUATION
    # =========================================================================

    def add_text_gras(self, text: str):
        """Ajoute du texte en gras."""
        p = P(stylename=STYLES['paragraphe'])
        span = Span(stylename=STYLES['car_gras'], text=text)
        p.addElement(span)
        self.doc.text.addElement(p)

    def add_correction(self, text: str):
        """Ajoute un texte de correction (rouge gras)."""
        p = P(stylename=STYLES['paragraphe'])
        span = Span(stylename=STYLES['car_correction'], text=text)
        p.addElement(span)
        self.doc.text.addElement(p)

    def add_paragraph_with_emphasis(self, text: str, emphasized_words: List[str],
                                     style: str = 'paragraphe'):
        """
        Ajoute un paragraphe avec des mots en gras (verbes d'action, mots clés).

        Args:
            text: Le texte complet
            emphasized_words: Liste des mots à mettre en gras
            style: Style de paragraphe (defaut: 'paragraphe')

        Exemple:
            doc.add_paragraph_with_emphasis(
                "Calculer la somme puis simplifier le résultat.",
                ["Calculer", "simplifier"]
            )
        """
        p = P(stylename=STYLES.get(style, STYLES['paragraphe']))

        # Construire une regex pour trouver les mots à accentuer (insensible à la casse)
        remaining = text
        for word in emphasized_words:
            parts = re.split(f'({re.escape(word)})', remaining, flags=re.IGNORECASE)
            remaining = ""
            for i, part in enumerate(parts):
                if part.lower() == word.lower():
                    # Mot trouvé: on flush le texte accumulé puis on ajoute le span
                    if remaining:
                        p.addText(remaining)
                        remaining = ""
                    span = Span(stylename=STYLES['car_gras'], text=part)
                    p.addElement(span)
                else:
                    remaining += part

        # Ajouter le texte restant
        if remaining:
            p.addText(remaining)

        self.doc.text.addElement(p)

    def add_vocabulary_entry(self, term: str, definition: str, add_to_index: bool = True):
        """
        Ajoute une entrée de vocabulaire avec le terme en gras et optionnellement indexé.

        Args:
            term: Le terme de vocabulaire (sera en gras)
            definition: La définition du terme
            add_to_index: Si True, ajoute le terme à l'index automatique

        Exemple:
            doc.add_vocabulary_entry("Numérateur", "Nombre au-dessus de la barre de fraction")
        """
        from odf.text import IndexMark, IndexEntrySpan

        p = P(stylename=STYLES['para_vocabulaire'])

        # Terme en gras
        span_term = Span(stylename=STYLES['car_gras'], text=term)
        p.addElement(span_term)

        # Ajouter à l'index si demandé (via placeholder pour post-traitement)
        if add_to_index:
            # On stocke l'entrée d'index pour post-traitement
            if not hasattr(self, 'index_entries'):
                self.index_entries = []
            self.index_entries.append(term)

        # Définition
        p.addText(f" : {definition}")

        self.doc.text.addElement(p)

    # =========================================================================
    # TITRES ET SOUS-TITRES
    # =========================================================================

    def add_section_title(self, title: str, level: int = 1, numbered: bool = True):
        """
        Ajoute un titre de section (I, II, III... ou 1, 2, 3...).

        Args:
            title: Texte du titre
            level: Niveau (1=partie principale, 2=sous-partie, 3=paragraphe)
            numbered: Si True, ajoute une numérotation automatique
        """
        h = H(outlinelevel=level, text=title)
        self.doc.text.addElement(h)

    def add_activity_title(self, title: str, activity_num: int = None):
        """
        Ajoute un titre d'activité.

        Args:
            title: Titre de l'activité
            activity_num: Numéro de l'activité (optionnel, auto-incrémenté si None)
        """
        if not hasattr(self, 'activity_counter'):
            self.activity_counter = 0

        if activity_num is None:
            self.activity_counter += 1
            activity_num = self.activity_counter

        h = H(outlinelevel=2, text=f"Activité {activity_num} : {title}")
        self.doc.text.addElement(h)

    # =========================================================================
    # SAUVEGARDE
    # =========================================================================

    def save(self):
        """Sauvegarde le document avec post-traitement pour master pages, formules et titre."""
        # Sauvegarder d'abord avec odfpy
        self.doc.save(self.output_path)

        # Post-traitement pour master page, formules, multicolonne, sauts et titre chapitre
        needs_postprocess = (
            self.master_page_set
            or self.formulas_to_insert
            or self.chapitre  # IMPORTANT: injecter le titre dans les en-tetes
            or hasattr(self, '_sections_to_process') and self._sections_to_process
            or hasattr(self, '_page_breaks') and self._page_breaks
            or hasattr(self, '_column_breaks') and self._column_breaks
            or hasattr(self, '_corrections_breaks') and self._corrections_breaks
            or getattr(self, '_question_style_needs_border', False)
        )
        if needs_postprocess:
            self._postprocess_odt()

        size = os.path.getsize(self.output_path)

        print(f"\n[OK] Document Sesamath cree avec succes!")
        print(f"     Fichier: {self.output_path}")
        print(f"     Taille: {size:,} octets")

        if self.chapitre:
            print(f"     Chapitre: {self.chapitre}")
        if self.niveau:
            print(f"     Niveau: {self.niveau}")
        if self.domaine:
            print(f"     Domaine: {self.domaine}")
        if self.master_page_set:
            print(f"     Master page: {self._master_page_style['master_page']}")

        print(f"     Exercices: {self.exercice_counter}")
        print(f"     Formules: {self.formula_counter}")

        return self.output_path

    def _postprocess_odt(self):
        """
        Post-traitement du fichier ODT pour:
        1. Ajouter le style automatique avec master-page-name
        2. Inserer les formules mathematiques comme objets ODF
        3. Traiter les sections multicolonnes
        4. Traiter les sauts de page et de colonne
        5. Corriger les pieds de page avec double numero
        """
        temp_dir = tempfile.mkdtemp(prefix="sesamath_odt_")

        try:
            # Extraire le fichier ODT
            with zipfile.ZipFile(self.output_path, 'r') as z:
                z.extractall(temp_dir)

            # Modifier content.xml
            content_path = os.path.join(temp_dir, 'content.xml')
            with open(content_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 1. Ajouter le style automatique pour master page
            if self.master_page_set:
                content = self._inject_master_page_style(content)

            # 2. Traiter les formules (remplacer les placeholders)
            if self.formulas_to_insert:
                content, manifest_entries, formula_objects = self._process_formulas(content, temp_dir)

                # Mettre a jour le manifest.xml
                if formula_objects:
                    manifest_path = os.path.join(temp_dir, 'META-INF', 'manifest.xml')
                    self._update_manifest(manifest_path, manifest_entries)

            # 3. Traiter les sections multicolonnes
            if hasattr(self, '_sections_to_process') and self._sections_to_process:
                content = self._process_multicolumn_sections(content)

            # 4. Traiter les sauts de page
            if hasattr(self, '_page_breaks') and self._page_breaks:
                content = self._process_page_breaks(content)

            # 5. Traiter les sauts de colonne
            if hasattr(self, '_column_breaks') and self._column_breaks:
                content = self._process_column_breaks(content)

            # 5b. Traiter les sauts de page des corrections (avec master page forcée)
            if hasattr(self, '_corrections_breaks') and self._corrections_breaks:
                content = self._process_corrections_page_breaks(content)

            # 6. Ameliorer le style des numeros de questions (ajouter bordure)
            if getattr(self, '_question_style_needs_border', False):
                content = self._enhance_question_number_style(content)

            # Sauvegarder content.xml modifie
            with open(content_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # 6. Modifier styles.xml
            styles_path = os.path.join(temp_dir, 'styles.xml')
            if os.path.exists(styles_path):
                # Corriger les pieds de page avec double numero
                self._fix_duplicate_page_numbers(styles_path)
                # Injecter le titre du chapitre dans les en-têtes
                if self.chapitre:
                    self._inject_header_title(styles_path)
                # Personnaliser les styles de titres H1
                self._customize_heading_styles(styles_path)
                # Modifier les marges de page si demandé
                if self._page_margins:
                    self._apply_page_margins(styles_path)

            # Rezipper le fichier ODT
            self._rezip_odt(temp_dir, self.output_path)

        finally:
            shutil.rmtree(temp_dir)

    def _process_multicolumn_sections(self, content: str) -> str:
        """
        Traite les sections multicolonnes.

        Remplace les placeholders par des balises text:section avec le style
        de colonnes approprie, avec optionnellement une ligne de separation.
        """
        for i, section in enumerate(self._sections_to_process, 1):
            start_id = section['start_id']
            end_id = section['end_id']
            columns = section['columns']
            gap = section['gap']
            separator = section.get('separator', True)

            # Creer le style de section dans office:automatic-styles
            section_style_name = f"Sect{i}"
            section_style = f'''<style:style style:name="{section_style_name}" style:family="section">
  <style:section-properties style:editable="false" fo:margin-left="0cm" fo:margin-right="0cm">
    <style:columns fo:column-count="{columns}" fo:column-gap="{gap}">
'''
            # Ajouter la ligne de separation si demandee
            if separator and columns > 1:
                section_style += '      <style:column-sep style:width="0.5pt" style:color="#cccccc" style:height="100%" style:vertical-align="middle"/>\n'

            # Ajouter les colonnes avec largeur egale
            col_width = f"{10/columns:.2f}*"
            for _ in range(columns):
                section_style += f'      <style:column style:rel-width="{col_width}" fo:start-indent="0cm" fo:end-indent="0cm"/>\n'

            section_style += '''    </style:columns>
  </style:section-properties>
</style:style>'''

            # Injecter le style dans office:automatic-styles
            auto_styles_end = content.find('</office:automatic-styles>')
            if auto_styles_end > 0:
                content = content[:auto_styles_end] + section_style + '\n' + content[auto_styles_end:]

            # Remplacer le placeholder de debut par l'ouverture de section
            # On doit remplacer tout le paragraphe contenant le placeholder
            content = re.sub(
                rf'<text:p[^>]*>{start_id}</text:p>',
                f'<text:section text:style-name="{section_style_name}" text:name="Section{i}">',
                content
            )

            # Remplacer le placeholder de fin par la fermeture de section
            if end_id:
                content = re.sub(
                    rf'<text:p[^>]*>{end_id}</text:p>',
                    '</text:section>',
                    content
                )

        return content

    def _process_page_breaks(self, content: str) -> str:
        """
        Traite les sauts de page.

        Remplace les placeholders par un paragraphe avec style de saut de page.
        """
        # Creer un style de paragraphe avec saut de page
        page_break_style = '''<style:style style:name="PageBreakStyle" style:family="paragraph" style:parent-style-name="Standard">
  <style:paragraph-properties fo:break-before="page"/>
</style:style>'''

        # Injecter le style si des sauts de page existent
        if self._page_breaks:
            auto_styles_end = content.find('</office:automatic-styles>')
            if auto_styles_end > 0:
                content = content[:auto_styles_end] + page_break_style + '\n' + content[auto_styles_end:]

        # Remplacer chaque placeholder
        for break_id in self._page_breaks:
            content = re.sub(
                rf'<text:p[^>]*>{break_id}</text:p>',
                '<text:p text:style-name="PageBreakStyle"/>',
                content
            )

        return content

    def _process_column_breaks(self, content: str) -> str:
        """
        Traite les sauts de colonne.

        Remplace les placeholders par un vrai saut de colonne ODF
        utilisant un style avec fo:break-before="column".
        """
        if not self._column_breaks:
            return content

        # Creer le style de saut de colonne
        column_break_style = '''<style:style style:name="ColumnBreakStyle" style:family="paragraph" style:parent-style-name="Standard">
  <style:paragraph-properties fo:break-before="column"/>
</style:style>'''

        # Injecter le style dans office:automatic-styles
        auto_styles_end = content.find('</office:automatic-styles>')
        if auto_styles_end > 0:
            content = content[:auto_styles_end] + column_break_style + '\n' + content[auto_styles_end:]

        # Remplacer chaque placeholder par un paragraphe avec le style de saut
        for break_id in self._column_breaks:
            content = re.sub(
                rf'<text:p[^>]*>{break_id}</text:p>',
                '<text:p text:style-name="ColumnBreakStyle"/>',
                content
            )

        return content

    def _process_corrections_page_breaks(self, content: str) -> str:
        """
        Traite les sauts de page des corrections avec master page forcée.

        Crée un style de paragraphe avec break-before="page" ET master-page-name
        pour forcer la même master page que le reste du document.
        """
        if not self.master_page_set:
            # Si pas de master page définie, utiliser un saut simple
            for break_id in self._corrections_breaks:
                content = re.sub(
                    rf'<text:p[^>]*>{break_id}</text:p>',
                    '<text:p text:style-name="PageBreakStyle"/>',
                    content
                )
            return content

        master_page = self._master_page_style['master_page']

        # Créer un style avec saut de page ET master page
        corrections_break_style = f'''<style:style style:name="CorrectionsPageBreak" style:family="paragraph" style:parent-style-name="Standard" style:master-page-name="{master_page}">
  <style:paragraph-properties fo:break-before="page" style:page-number="auto"/>
</style:style>'''

        # Injecter le style
        auto_styles_end = content.find('</office:automatic-styles>')
        if auto_styles_end > 0:
            content = content[:auto_styles_end] + corrections_break_style + '\n' + content[auto_styles_end:]

        # Remplacer les placeholders
        for break_id in self._corrections_breaks:
            content = re.sub(
                rf'<text:p[^>]*>{break_id}</text:p>',
                '<text:p text:style-name="CorrectionsPageBreak"/>',
                content
            )

        return content

    def _enhance_question_number_style(self, content: str) -> str:
        """
        Ameliore le style des numeros de questions avec une bordure.

        odfpy ne permet pas facilement d'ajouter des bordures aux styles
        de caracteres, donc on le fait en post-traitement XML.

        Ajoute:
        - fo:border: bordure fine bleue
        - fo:padding: espace interieur
        """
        style_name = self._question_number_style_name

        # Chercher le style dans content.xml et ajouter les attributs de bordure
        # Pattern: <style:style style:name="QuestionNumberStyle" style:family="text">
        #            <style:text-properties .../>
        #          </style:style>

        def enhance_style(match):
            style_xml = match.group(0)

            # Ajouter les attributs de bordure au text-properties
            # On remplace /> par les nouveaux attributs + />
            # Attention: [^>]* capture aussi / donc on utilise une approche differente
            style_xml = re.sub(
                r'(<style:text-properties[^/]*?)(\s*/>)',
                r'\1 fo:border="0.5pt solid #2a6099" fo:padding="1pt"\2',
                style_xml
            )

            return style_xml

        content = re.sub(
            rf'<style:style[^>]*style:name="{style_name}"[^>]*>.*?</style:style>',
            enhance_style,
            content,
            flags=re.DOTALL
        )

        return content

    def _inject_master_page_style(self, content: str) -> str:
        """Injecte le style automatique pour la master page dans content.xml."""
        style_name = self._master_page_style['name']
        master_page = self._master_page_style['master_page']

        # Creer le style automatique - paragraphe invisible pour appliquer la master page
        # Marges et hauteur a 0 pour ne pas prendre d'espace
        auto_style = f'''<style:style style:name="{style_name}" style:family="paragraph" style:parent-style-name="Standard" style:master-page-name="{master_page}">
  <style:paragraph-properties style:page-number="auto" fo:margin-top="0cm" fo:margin-bottom="0cm" fo:line-height="0pt"/>
  <style:text-properties fo:font-size="1pt"/>
</style:style>'''

        # Cas 1: office:automatic-styles avec contenu (balise fermante)
        auto_styles_end = content.find('</office:automatic-styles>')
        if auto_styles_end > 0:
            content = content[:auto_styles_end] + auto_style + '\n' + content[auto_styles_end:]
        else:
            # Cas 2: office:automatic-styles auto-fermante (vide)
            auto_styles_empty = content.find('office:automatic-styles/>')
            if auto_styles_empty > 0:
                # Remplacer par une balise ouvrante + style + balise fermante
                content = content.replace(
                    'office:automatic-styles/>',
                    f'office:automatic-styles>{auto_style}</office:automatic-styles>'
                )

        # INSERER un paragraphe vide avec le style MP_Auto au debut du document
        # Cela applique la master page sans modifier le style des autres elements
        # Le paragraphe vide n'occupe pas d'espace visible
        content = re.sub(
            r'(<office:text[^>]*>)',
            f'\\1<text:p text:style-name="{style_name}"/>',
            content,
            count=1
        )

        return content

    def _process_formulas(self, content: str, temp_dir: str):
        """Traite les formules et cree les objets ODF."""
        manifest_entries = []
        formula_objects = []

        for formula in self.formulas_to_insert:
            placeholder = formula['id']
            starmath = formula['starmath']
            object_num = len(formula_objects) + 1
            object_name = f"Object {object_num}"

            # Creer le dossier de l'objet formule
            object_dir = os.path.join(temp_dir, object_name)
            os.makedirs(object_dir, exist_ok=True)

            # Creer content.xml pour la formule (MathML)
            formula_content = self._create_mathml(starmath)
            with open(os.path.join(object_dir, 'content.xml'), 'w', encoding='utf-8') as f:
                f.write(formula_content)

            # Entrees pour le manifest
            manifest_entries.append(f'<manifest:file-entry manifest:full-path="{object_name}/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.formula"/>')
            manifest_entries.append(f'<manifest:file-entry manifest:full-path="{object_name}/content.xml" manifest:media-type="text/xml"/>')

            formula_objects.append(object_name)

            # Remplacer le placeholder par la reference a l'objet
            frame_xml = f'''<draw:frame draw:style-name="fr1" draw:name="{object_name}" text:anchor-type="as-char" svg:width="1.5cm" svg:height="0.6cm" draw:z-index="0">
  <draw:object xlink:href="./{object_name}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
</draw:frame>'''

            content = content.replace(placeholder, frame_xml)

        return content, manifest_entries, formula_objects

    def _normalize_starmath(self, starmath: str) -> str:
        """
        Normalise une formule StarMath.

        Note: La taille et police sont gerees manuellement par l'utilisateur
        dans LibreOffice pour eviter les bugs de rendu.
        """
        return starmath.strip()

    def _create_mathml(self, starmath: str) -> str:
        """
        Cree le contenu MathML pour une formule StarMath.

        Format simple MathML avec annotation StarMath.
        L'utilisateur active manuellement les formules dans LibreOffice.
        """
        clean_formula = starmath.strip()

        # Format MathML simple - LibreOffice interprete l'annotation StarMath
        return f'''<?xml version="1.0" encoding="UTF-8"?>
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <semantics>
    <annotation encoding="StarMath 5.0">{clean_formula}</annotation>
  </semantics>
</math>'''

    def _inject_header_title(self, styles_path: str):
        """
        Injecte le titre du chapitre dans les en-têtes ET pieds de page.

        - En-tête ligne 1 : titre du chapitre
        - En-tête ligne 2 : niveau et méta-infos
        - Pied de page : titre du chapitre (remplace textes par défaut)
        """
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles = f.read()

        # Construire la ligne de méta-infos
        meta_parts = []
        if self.niveau:
            meta_parts.append(f"Niveau {self.niveau}")
        if self.domaine:
            domaine_label = self.domaine.replace('_', ' ').title()
            meta_parts.append(domaine_label)
        meta_line = " | ".join(meta_parts) if meta_parts else ""

        # === EN-TÊTE LIGNE 1 : Titre principal ===
        title_patterns = [
            r'>A compléter<',
            r'>À compléter<',
            r'>A Compléter<',
            r'>À Compléter<',
            r'>A completer<',
            r'>A Completer<',
            r'>Nombres entiers et décimaux<',
            r'>Nombres entiers et d[ée]cimaux<',
        ]

        for pattern in title_patterns:
            styles = re.sub(pattern, f'>{self.chapitre}<', styles, flags=re.IGNORECASE)

        # === EN-TÊTE LIGNE 2 : Méta-infos ===
        subtitle_patterns = [
            r'>Résumé de cours<',
            r'>Resume de cours<',
            r'>R[ée]sum[ée] de cours<',
        ]

        replacement = f'>{meta_line}<' if meta_line else '><'
        for pattern in subtitle_patterns:
            styles = re.sub(pattern, replacement, styles, flags=re.IGNORECASE)

        # === PIED DE PAGE : Remplacer les textes par défaut ===
        # Patterns pour les différentes master pages (footer)
        footer_patterns = [
            r'>Entiers et décimaux : Numération<',
            r'>Entiers et d[ée]cimaux[^<]*<',
            r'>E</text:span><text:span[^>]*>ntiers et d[ée]cimaux[^<]*<',
            r'>Géométrie[^<]*<',
            r'>G[ée]om[ée]trie[^<]*<',
            r'>Gestion de donn[ée]es[^<]*<',
            r'>Mesures[^<]*<',
            r'>Probl[èe]mes[^<]*<',
        ]

        for pattern in footer_patterns:
            styles = re.sub(pattern, f'>{self.chapitre}<', styles, flags=re.IGNORECASE)

        with open(styles_path, 'w', encoding='utf-8') as f:
            f.write(styles)

    def _fix_duplicate_page_numbers(self, styles_path: str):
        """
        Corrige les pieds de page ayant un double numero de page.

        Le template Sesamath a un bug: dans <style:footer>, il y a deux <text:h>
        contenant chacun un <text:page-number>. On supprime le premier (MP61)
        pour ne garder que celui avec le fond colore (MP63).
        """
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles = f.read()

        # Le probleme specifique: dans le footer, on a:
        # <text:h style="MP61">...<text:page-number>...</text:h>
        # <text:h style="MP63">...<draw:g>...<text:page-number>...</text:h>
        #
        # On veut supprimer le premier text:h (MP61) qui contient page-number
        # mais PAS le draw:g avec le fond colore

        # Pattern pour matcher le premier text:h avec MP61 contenant page-number
        # On doit etre prudent car text:h peut contenir d'autres text:h imbriques
        # Solution: supprimer tout le bloc <text:h text:style-name="MP61"...>...</text:h>
        # qui contient directement un page-number (pas via un draw:text-box)

        def fix_footer(match):
            footer = match.group(0)

            # Compter les text:page-number directs dans le footer
            page_count = len(re.findall(r'<text:page-number', footer))

            if page_count >= 2:
                # Supprimer le text:h avec MP61 qui contient page-number directement
                # Pattern: <text:h text:style-name="MP61"...>...<text:page-number>...</text:h>
                # Suivi immediatement par <text:h text:style-name="MP63"
                footer = re.sub(
                    r'(<style:footer>)'
                    r'<text:h text:style-name="MP61"[^>]*>'
                    r'(?:(?!</text:h>).)*?'  # Contenu jusqu'au premier </text:h>
                    r'<text:page-number[^>]*>[^<]*</text:page-number>'
                    r'(?:(?!</text:h>).)*?'
                    r'</text:h>'
                    r'(<text:h text:style-name="MP63")',
                    r'\1\2',
                    footer,
                    flags=re.DOTALL
                )

            return footer

        # Appliquer la correction aux footers
        styles = re.sub(
            r'<style:footer>.*?</style:footer>',
            fix_footer,
            styles,
            flags=re.DOTALL
        )

        with open(styles_path, 'w', encoding='utf-8') as f:
            f.write(styles)

    def _apply_page_margins(self, styles_path: str):
        """
        Applique les marges de page personnalisées au page-layout.

        Modifie UNIQUEMENT les attributs fo:margin-* dans les balises
        style:page-layout-properties, pas les styles de paragraphe.
        """
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles = f.read()

        def update_page_layout(match):
            props = match.group(0)
            margins = self._page_margins

            if margins.get('left'):
                props = re.sub(r'fo:margin-left="[^"]*"',
                              f'fo:margin-left="{margins["left"]}"', props)
            if margins.get('right'):
                props = re.sub(r'fo:margin-right="[^"]*"',
                              f'fo:margin-right="{margins["right"]}"', props)
            if margins.get('top'):
                props = re.sub(r'fo:margin-top="[^"]*"',
                              f'fo:margin-top="{margins["top"]}"', props)
            if margins.get('bottom'):
                props = re.sub(r'fo:margin-bottom="[^"]*"',
                              f'fo:margin-bottom="{margins["bottom"]}"', props)

            return props

        # Modifier uniquement les page-layout-properties (pas les paragraph-properties)
        styles = re.sub(
            r'<style:page-layout-properties[^>]*>',
            update_page_layout,
            styles
        )

        with open(styles_path, 'w', encoding='utf-8') as f:
            f.write(styles)

    def _customize_heading_styles(self, styles_path: str):
        """
        Personnalise les styles de titres pour les rendre plus visibles.

        - H1 (Heading_20_1): gras, plus grand, souligné, couleur, espacement réduit
        """
        with open(styles_path, 'r', encoding='utf-8') as f:
            styles = f.read()

        # Modifier le style Heading_20_1 pour ajouter soulignement et couleur
        def enhance_h1(match):
            style = match.group(0)

            # Ajouter les propriétés de soulignement si pas présentes
            if 'text-underline' not in style:
                # Insérer avant la fermeture de style:text-properties
                style = re.sub(
                    r'(fo:font-weight="bold")',
                    r'\1 style:text-underline-style="solid" style:text-underline-width="auto" style:text-underline-color="#2a6099"',
                    style
                )

            # Ajouter une couleur de texte
            if 'fo:color' not in style:
                style = re.sub(
                    r'(fo:font-size="[^"]*")',
                    r'\1 fo:color="#2a6099"',
                    style,
                    count=1
                )

            # Ajouter style:paragraph-properties si absent (pour override les marges du parent)
            if 'style:paragraph-properties' not in style:
                # Inserer juste apres la balise ouvrante du style
                style = re.sub(
                    r'(<style:style[^>]*>)',
                    r'\1<style:paragraph-properties fo:margin-top="0.1cm" fo:margin-bottom="0.1cm"/>',
                    style
                )
            else:
                # Modifier les marges existantes
                style = re.sub(
                    r'fo:margin-top="[^"]*"',
                    'fo:margin-top="0.1cm"',
                    style
                )
                style = re.sub(
                    r'fo:margin-bottom="[^"]*"',
                    'fo:margin-bottom="0.1cm"',
                    style
                )

            return style

        styles = re.sub(
            r'<style:style[^>]*style:name="Heading_20_1"[^>]*>.*?</style:style>',
            enhance_h1,
            styles,
            flags=re.DOTALL
        )

        with open(styles_path, 'w', encoding='utf-8') as f:
            f.write(styles)

    def _update_manifest(self, manifest_path: str, entries: list):
        """Met a jour le manifest.xml avec les nouvelles entrees."""
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = f.read()

        # Trouver la position avant </manifest:manifest>
        insert_pos = manifest.rfind('</manifest:manifest>')
        if insert_pos > 0:
            new_entries = '\n'.join(entries)
            manifest = manifest[:insert_pos] + new_entries + '\n' + manifest[insert_pos:]

        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(manifest)

    def _rezip_odt(self, temp_dir: str, output_path: str):
        """Rezippe le dossier en fichier ODT."""
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            # mimetype en premier, non compresse
            mimetype_path = os.path.join(temp_dir, 'mimetype')
            if os.path.exists(mimetype_path):
                zout.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)

            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file == 'mimetype':
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zout.write(file_path, arcname)


# =============================================================================
# FONCTION UTILITAIRE
# =============================================================================

def create_sample_document(output_path: str):
    """
    Crée un document de démonstration avec tous les types d'environnements.
    Les formules mathématiques sont intégrées directement dans les environnements.
    """
    doc = SesamathDocument(
        output_path,
        chapitre="Les Fractions",
        niveau="6e",
        domaine="numerique"
    )

    # Introduction
    doc.add_paragraph(
        "Ce chapitre présente les fractions et leurs propriétés fondamentales."
    )
    doc.add_empty_line()

    # Vocabulaire
    doc.add_vocabulaire("Vocabulaire", [
        "Le numérateur est le nombre au-dessus de la barre de fraction.",
        "Le dénominateur est le nombre en-dessous de la barre de fraction.",
        "La barre de fraction signifie « divisé par »."
    ])
    doc.add_empty_line()

    # Définition avec formule intégrée
    doc.add_definition(
        "Définition",
        "Une fraction est un nombre qui s'écrit sous la forme",
        formule="{a} over {b}"
    )
    doc.add_paragraph(
        "où a et b sont des nombres entiers et b est différent de zéro."
    )
    doc.add_empty_line()

    # Exemples - formules avec add_formula_inline pour un meilleur rendu
    doc.add_exemple("Exemples", "Voici quelques fractions courantes :")
    doc.add_formula_inline("", "{3} over {4}", " représente 3 parts sur 4 parts égales.")
    doc.add_formula_inline("", "{1} over {2}", " représente la moitié d'un tout.")
    doc.add_formula_inline("", "{5} over {5} = 1", " (un tout entier).")
    doc.add_empty_line()

    # Propriété avec formule intégrée
    doc.add_propriete(
        "Propriété fondamentale",
        "On ne change pas la valeur d'une fraction en multipliant (ou divisant) "
        "le numérateur et le dénominateur par un même nombre non nul.",
        formule="{a} over {b} = {a times k} over {b times k}"
    )
    doc.add_formula_inline("Exemple : ", "{2} over {4} = {1} over {2}", " (on divise par 2)")
    doc.add_empty_line()

    # Méthode
    doc.add_methode("Méthode : Simplifier une fraction", [
        "Chercher un diviseur commun au numérateur et au dénominateur.",
        "Diviser le numérateur et le dénominateur par ce diviseur.",
        "Recommencer jusqu'à obtenir une fraction irréductible."
    ])
    doc.add_empty_line()

    # Remarque avec formule
    doc.add_remarque(
        "Remarque",
        "Une fraction est dite irréductible lorsqu'on ne peut plus la simplifier. "
        "Par exemple, la fraction suivante est irréductible :",
        formule="{3} over {7}"
    )
    doc.add_empty_line()

    # Exercice 1
    doc.add_exercice(
        "Simplifier les fractions",
        "Simplifie les fractions suivantes en trouvant un diviseur commun :",
        questions=["4/8 = ", "6/9 = ", "10/15 = ", "12/16 = "],
        lignes_reponse=1
    )
    doc.add_empty_line()

    # Exercice 2
    doc.add_exercice(
        "Problème",
        "Marie a mangé 3/8 d'une pizza. Pierre a mangé 2/8 de la même pizza.",
        questions=[
            "Quelle fraction de la pizza ont-ils mangée ensemble ?",
            "Quelle fraction de la pizza reste-t-il ?"
        ],
        lignes_reponse=3
    )

    doc.save()
    return output_path


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Cree un document ODT avec les styles Sesamath"
    )
    parser.add_argument("output", nargs='?', default="test_sesamath_complet.odt",
                        help="Fichier de sortie")
    parser.add_argument("--demo", action="store_true",
                        help="Creer un document de demonstration")

    args = parser.parse_args()

    if args.demo or True:  # Toujours creer le demo pour le test
        create_sample_document(args.output)
