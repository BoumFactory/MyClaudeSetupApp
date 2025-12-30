#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestion des formules mathematiques dans les documents ODT.

Les formules dans LibreOffice Writer peuvent etre:
1. Des objets embarques (Object 1, Object 2...) au format ODF Formula
2. Du MathML inline (moins courant)

Ce module fournit des fonctions pour:
- Creer des formules en StarMath (syntaxe LibreOffice Math)
- Convertir LaTeX vers StarMath
- Inserer des formules dans un document ODT

Syntaxe StarMath courante:
- Fraction: {a} over {b}
- Racine carree: sqrt{x}
- Puissance: x^{2}
- Indice: x_{i}
- Somme: sum from{i=1} to{n} x_i
- Integrale: int from{a} to{b} f(x) dx
- Infini: infinity
- Plus ou moins: +-
- Multiplication: times ou cdot
- Division: div
- Different: <>
- Inferieur ou egal: <=
- Superieur ou egal: >=
- Fleche: rightarrow ou ->
- Grec: %alpha, %beta, %gamma, %pi, %theta, etc.

Usage:
    from math_formulas import create_math_object, latex_to_starmath

    # Creer une fraction
    formula = create_math_object("{3} over {4}")

    # Convertir du LaTeX
    starmath = latex_to_starmath(r"\\frac{a}{b}")
"""

import os
import re
import zipfile
import tempfile
import shutil
from typing import Optional, Tuple


# Mapping LaTeX -> StarMath (partiel mais couvre les cas courants)
LATEX_TO_STARMATH = {
    # Fractions
    r'\\frac{([^}]+)}{([^}]+)}': r'{{\\1} over {\\2}}',

    # Racines
    r'\\sqrt{([^}]+)}': r'sqrt{\\1}',
    r'\\sqrt\[([^\]]+)\]{([^}]+)}': r'nroot{\\1}{\\2}',

    # Puissances et indices
    r'\^{([^}]+)}': r'^{\\1}',
    r'_{([^}]+)}': r'_{\\1}',
    r'\^(\d)': r'^\\1',
    r'_(\d)': r'_\\1',

    # Operateurs
    r'\\times': 'times',
    r'\\cdot': 'cdot',
    r'\\div': 'div',
    r'\\pm': '+-',
    r'\\mp': '-+',
    r'\\leq': '<=',
    r'\\geq': '>=',
    r'\\neq': '<>',
    r'\\approx': 'approx',
    r'\\equiv': 'equiv',

    # Fleches
    r'\\rightarrow': 'rightarrow',
    r'\\leftarrow': 'leftarrow',
    r'\\leftrightarrow': 'leftrightarrow',
    r'\\Rightarrow': 'drarrow',
    r'\\Leftarrow': 'dlarrow',

    # Sommes, produits, integrales
    r'\\sum_{([^}]+)}\^{([^}]+)}': r'sum from{\\1} to{\\2}',
    r'\\sum': 'sum',
    r'\\prod_{([^}]+)}\^{([^}]+)}': r'prod from{\\1} to{\\2}',
    r'\\prod': 'prod',
    r'\\int_{([^}]+)}\^{([^}]+)}': r'int from{\\1} to{\\2}',
    r'\\int': 'int',

    # Limites
    r'\\lim_{([^}]+)}': r'lim from{\\1}',

    # Lettres grecques
    r'\\alpha': '%alpha',
    r'\\beta': '%beta',
    r'\\gamma': '%gamma',
    r'\\delta': '%delta',
    r'\\epsilon': '%epsilon',
    r'\\zeta': '%zeta',
    r'\\eta': '%eta',
    r'\\theta': '%theta',
    r'\\iota': '%iota',
    r'\\kappa': '%kappa',
    r'\\lambda': '%lambda',
    r'\\mu': '%mu',
    r'\\nu': '%nu',
    r'\\xi': '%xi',
    r'\\pi': '%pi',
    r'\\rho': '%rho',
    r'\\sigma': '%sigma',
    r'\\tau': '%tau',
    r'\\upsilon': '%upsilon',
    r'\\phi': '%phi',
    r'\\chi': '%chi',
    r'\\psi': '%psi',
    r'\\omega': '%omega',

    # Majuscules grecques
    r'\\Gamma': '%GAMMA',
    r'\\Delta': '%DELTA',
    r'\\Theta': '%THETA',
    r'\\Lambda': '%LAMBDA',
    r'\\Xi': '%XI',
    r'\\Pi': '%PI',
    r'\\Sigma': '%SIGMA',
    r'\\Phi': '%PHI',
    r'\\Psi': '%PSI',
    r'\\Omega': '%OMEGA',

    # Symboles speciaux
    r'\\infty': 'infinity',
    r'\\partial': 'partial',
    r'\\forall': 'forall',
    r'\\exists': 'exists',
    r'\\emptyset': 'emptyset',
    r'\\in': 'in',
    r'\\notin': 'notin',
    r'\\subset': 'subset',
    r'\\supset': 'supset',
    r'\\cup': 'union',
    r'\\cap': 'intersection',

    # Fonctions
    r'\\sin': 'sin',
    r'\\cos': 'cos',
    r'\\tan': 'tan',
    r'\\log': 'log',
    r'\\ln': 'ln',
    r'\\exp': 'exp',

    # Parentheses et accolades
    r'\\left\(': 'left(',
    r'\\right\)': 'right)',
    r'\\left\[': 'left[',
    r'\\right\]': 'right]',
    r'\\left\\{': 'left lbrace',
    r'\\right\\}': 'right rbrace',
    r'\\lbrace': 'lbrace',
    r'\\rbrace': 'rbrace',

    # Espaces
    r'\\,': '`',
    r'\\;': '~',
    r'\\quad': '~~',
    r'\\qquad': '~~~~',

    # Texte
    r'\\text{([^}]+)}': r'"\\1"',
    r'\\mathrm{([^}]+)}': r'\\1',
}


def latex_to_starmath(latex: str) -> str:
    """
    Convertit une formule LaTeX en syntaxe StarMath.

    Args:
        latex: Formule en syntaxe LaTeX

    Returns:
        Formule en syntaxe StarMath

    Exemple:
        >>> latex_to_starmath(r"\\frac{a+b}{c}")
        '{a+b} over {c}'
    """
    result = latex

    # Appliquer les conversions dans l'ordre
    for pattern, replacement in LATEX_TO_STARMATH.items():
        result = re.sub(pattern, replacement, result)

    # Nettoyer les accolades LaTeX restantes
    # (en StarMath, les accolades groupent, pas besoin de les echapper)

    return result


def starmath_to_mathml(starmath: str, font_size: str = "10pt", font_family: str = "sans-serif") -> str:
    """
    Convertit une formule StarMath en MathML.

    Note: Cette conversion est simplifiee. Pour une conversion complete,
    utiliser LibreOffice en mode headless.

    Args:
        starmath: Formule en syntaxe StarMath
        font_size: Taille de police
        font_family: Famille de police

    Returns:
        Code MathML
    """
    # Template MathML de base
    mathml_template = '''<?xml version="1.0" encoding="UTF-8"?>
<math xmlns="http://www.w3.org/1998/Math/MathML" display="block">
  <semantics>
    <mstyle mathsize="{font_size}">
      <mstyle mathvariant="{font_family}">
        {content}
      </mstyle>
    </mstyle>
    <annotation encoding="StarMath 5.0">{starmath}</annotation>
  </semantics>
</math>'''

    # Conversion simplifiee StarMath -> MathML
    content = convert_starmath_to_mathml_content(starmath)

    return mathml_template.format(
        font_size=font_size,
        font_family=font_family,
        content=content,
        starmath=starmath
    )


def convert_starmath_to_mathml_content(starmath: str) -> str:
    """
    Convertit le contenu StarMath en elements MathML.

    Conversion simplifiee pour les cas courants.
    """
    # Fractions: {a} over {b}
    fraction_pattern = r'\{([^}]+)\}\s*over\s*\{([^}]+)\}'
    match = re.search(fraction_pattern, starmath)
    if match:
        num, den = match.groups()
        return f'<mfrac><mrow><mn>{num}</mn></mrow><mn>{den}</mn></mfrac>'

    # Nombres simples
    if re.match(r'^\d+$', starmath.strip()):
        return f'<mn>{starmath.strip()}</mn>'

    # Variables simples
    if re.match(r'^[a-zA-Z]$', starmath.strip()):
        return f'<mi>{starmath.strip()}</mi>'

    # Par defaut, retourner comme texte
    return f'<mtext>{starmath}</mtext>'


def create_formula_object(starmath: str, object_name: str = "Object 1") -> dict:
    """
    Cree les fichiers necessaires pour un objet formule ODF.

    Args:
        starmath: Formule en syntaxe StarMath
        object_name: Nom du dossier objet (ex: "Object 1")

    Returns:
        Dictionnaire avec les fichiers a creer:
        {
            'content.xml': contenu MathML,
            'settings.xml': parametres,
        }
    """
    # Generer le MathML
    mathml = starmath_to_mathml(starmath)

    # Settings minimal
    settings = '''<?xml version="1.0" encoding="UTF-8"?>
<office:document-settings xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:config="urn:oasis:names:tc:opendocument:xmlns:config:1.0"
    office:version="1.3">
  <office:settings>
    <config:config-item-set config:name="ooo:configuration-settings">
    </config:config-item-set>
  </office:settings>
</office:document-settings>'''

    return {
        'content.xml': mathml,
        'settings.xml': settings,
    }


def add_formula_to_odt(odt_path: str, starmath: str, output_path: str = None) -> str:
    """
    Ajoute une formule mathematique a un document ODT existant.

    Args:
        odt_path: Chemin vers le document ODT
        starmath: Formule en syntaxe StarMath
        output_path: Chemin de sortie (si None, modifie le fichier original)

    Returns:
        Chemin du fichier modifie

    Note: Cette fonction ajoute la formule a la fin du document.
    Pour un placement plus precis, utiliser insert_formula_at_position().
    """
    if output_path is None:
        output_path = odt_path

    temp_dir = tempfile.mkdtemp(prefix="odt_math_")

    try:
        # Extraire l'ODT
        with zipfile.ZipFile(odt_path, 'r') as z:
            z.extractall(temp_dir)

        # Trouver le prochain numero d'objet disponible
        object_num = 1
        while os.path.exists(os.path.join(temp_dir, f"Object {object_num}")):
            object_num += 1

        object_name = f"Object {object_num}"
        object_dir = os.path.join(temp_dir, object_name)
        os.makedirs(object_dir)

        # Creer les fichiers de l'objet formule
        formula_files = create_formula_object(starmath, object_name)
        for filename, content in formula_files.items():
            filepath = os.path.join(object_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

        # Creer le sous-dossier Configurations2
        os.makedirs(os.path.join(object_dir, "Configurations2"), exist_ok=True)

        # Mettre a jour le manifest.xml
        manifest_path = os.path.join(temp_dir, "META-INF", "manifest.xml")
        update_manifest_for_formula(manifest_path, object_name)

        # Mettre a jour content.xml pour referencer la formule
        content_path = os.path.join(temp_dir, "content.xml")
        add_formula_reference_to_content(content_path, object_name)

        # Rezipper
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            # mimetype en premier, non compresse
            mimetype_path = os.path.join(temp_dir, "mimetype")
            if os.path.exists(mimetype_path):
                zout.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)

            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file == "mimetype":
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zout.write(file_path, arcname)

        return output_path

    finally:
        shutil.rmtree(temp_dir)


def update_manifest_for_formula(manifest_path: str, object_name: str):
    """Met a jour le manifest.xml pour inclure un nouvel objet formule."""
    with open(manifest_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trouver la position avant </manifest:manifest>
    insert_pos = content.rfind('</manifest:manifest>')

    # Nouvelles entrees pour l'objet formule
    new_entries = f'''
 <manifest:file-entry manifest:full-path="{object_name}/Configurations2/" manifest:media-type="application/vnd.sun.xml.ui.configuration"/>
 <manifest:file-entry manifest:full-path="{object_name}/content.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="{object_name}/settings.xml" manifest:media-type="text/xml"/>
 <manifest:file-entry manifest:full-path="{object_name}/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.formula"/>
'''

    content = content[:insert_pos] + new_entries + content[insert_pos:]

    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(content)


def add_formula_reference_to_content(content_path: str, object_name: str):
    """Ajoute une reference a la formule dans content.xml."""
    with open(content_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Creer l'element draw:frame avec la formule
    formula_frame = f'''
<text:p text:style-name="Standard">
  <draw:frame draw:style-name="fr1" draw:name="{object_name}" text:anchor-type="as-char" svg:width="2cm" svg:height="0.8cm" draw:z-index="0">
    <draw:object xlink:href="./{object_name}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>
  </draw:frame>
</text:p>
'''

    # Trouver la position avant </office:text>
    insert_pos = content.rfind('</office:text>')
    if insert_pos == -1:
        print("[AVERTISSEMENT] </office:text> non trouve")
        return

    content = content[:insert_pos] + formula_frame + content[insert_pos:]

    with open(content_path, 'w', encoding='utf-8') as f:
        f.write(content)


# ============================================================================
# EXEMPLES DE FORMULES COURANTES EN STARMATH
# ============================================================================

STARMATH_EXAMPLES = {
    # Fractions
    'fraction_simple': '{a} over {b}',
    'fraction_composee': '{{a+b} over {c}} over {{d} over {e}}',

    # Operations
    'addition': 'a + b',
    'soustraction': 'a - b',
    'multiplication': 'a times b',
    'division': 'a div b',

    # Puissances et racines
    'puissance': 'x^{2}',
    'racine_carree': 'sqrt{x}',
    'racine_n': 'nroot{3}{x}',

    # Fractions decimales
    'fraction_decimale': '{134`587} over {100}',

    # Egalites
    'egalite': 'a = b',
    'different': 'a <> b',
    'inferieur': 'a < b',
    'superieur': 'a > b',
    'inf_egal': 'a <= b',
    'sup_egal': 'a >= b',

    # Sommes et produits
    'somme': 'sum from{i=1} to{n} x_i',
    'produit': 'prod from{i=1} to{n} x_i',

    # Integrales
    'integrale_definie': 'int from{a} to{b} f(x) dx',
    'integrale_indefinie': 'int f(x) dx',

    # Limites
    'limite': 'lim from{x -> infinity} f(x)',

    # Equations
    'equation_second_degre': 'x = {-b +- sqrt{b^2 - 4ac}} over {2a}',

    # Geometrie
    'pythagore': 'a^2 + b^2 = c^2',
    'aire_cercle': 'A = %pi r^2',
    'perimetre_cercle': 'P = 2 %pi r',

    # Trigonometrie
    'identite_trigo': 'sin^2(x) + cos^2(x) = 1',
}


def print_starmath_examples():
    """Affiche des exemples de formules StarMath."""
    print("=== EXEMPLES DE FORMULES STARMATH ===\n")
    for name, formula in STARMATH_EXAMPLES.items():
        print(f"{name}:")
        print(f"  StarMath: {formula}")
        print()


if __name__ == "__main__":
    print_starmath_examples()

    # Test de conversion LaTeX -> StarMath
    print("\n=== TEST CONVERSION LATEX -> STARMATH ===\n")
    latex_examples = [
        r"\frac{a}{b}",
        r"\sqrt{x^2 + y^2}",
        r"\sum_{i=1}^{n} x_i",
        r"\int_{0}^{\infty} e^{-x} dx",
        r"\alpha + \beta = \gamma",
    ]

    for latex in latex_examples:
        starmath = latex_to_starmath(latex)
        print(f"LaTeX:    {latex}")
        print(f"StarMath: {starmath}")
        print()
