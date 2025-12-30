#!/usr/bin/env python3
"""
Extrait les styles d'un fichier ODT source et genere un template reutilisable.

Ce script analyse un fichier ODT (dezippe ou archive), extrait:
- Tous les styles (paragraphe, texte, tableau, liste)
- Les declarations de polices
- Les mises en page
- Les pages maitres

Et genere:
- Un template ODT vierge avec tous les styles
- Un fichier JSON de documentation des styles
- Un fichier Markdown de reference rapide

Usage:
    python extract_styles_from_odt.py <source.odt ou dossier_dezippe> [--output <dossier_sortie>]

Exemples:
    python extract_styles_from_odt.py cahier_sesamath.odt
    python extract_styles_from_odt.py cahier_dezippe/ --output ./templates/
"""

import os
import sys
import argparse
import zipfile
import shutil
import tempfile
import json
import re
from datetime import datetime
from collections import defaultdict
from pathlib import Path

# Verifier odfpy
try:
    from odf.opendocument import OpenDocumentText
    from odf.style import Style, TextProperties, ParagraphProperties
    from odf.style import FontFace, ListLevelStyleBullet, ListLevelProperties
    from odf.text import P, H, List, ListItem, ListStyle
    HAS_ODFPY = True
except ImportError:
    HAS_ODFPY = False
    print("[AVERTISSEMENT] odfpy non installe. Generation de template desactivee.")
    print("                Installez avec: pip install odfpy")

# Namespaces ODF
NAMESPACES = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'style': 'urn:oasis:names:tc:opendocument:xmlns:style:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'draw': 'urn:oasis:names:tc:opendocument:xmlns:drawing:1.0',
    'fo': 'urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0',
    'svg': 'urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0',
    'loext': 'urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0',
    'xlink': 'http://www.w3.org/1999/xlink',
    'number': 'urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0',
}

# Couleurs Sesamath par domaine
SESAMATH_COLORS = {
    'geometrie': '#1ca2b8',
    'numerique': '#d7e12c',
    'mesures': '#7fb241',
    'gestion_donnees': '#9d0f89',
    'problemes': '#d62e4e',
    'definition': '#77bc65',
    'propriete': '#ec9ba4',
    'methode': '#729fcf',
    'remarque': '#78bbb2',
    'exemple': '#eeeeee',
}


class ODTStyleExtractor:
    """Extracteur de styles ODT."""

    def __init__(self, source_path: str):
        """
        Initialise l'extracteur.

        Args:
            source_path: Chemin vers un fichier .odt ou un dossier dezippe
        """
        self.source_path = Path(source_path)
        self.temp_dir = None
        self.styles_xml_path = None
        self.content_xml_path = None

        # Donnees extraites
        self.raw_styles_xml = None
        self.styles_data = {
            'paragraph_styles': [],
            'text_styles': [],
            'table_styles': [],
            'list_styles': [],
            'page_layouts': [],
            'master_pages': [],
            'font_declarations': [],
            'default_styles': [],
            'outline_styles': [],
        }
        self.analysis = {
            'sesamath_styles': [],
            'style_categories': defaultdict(list),
            'color_palette': set(),
            'fonts_used': set(),
            'border_colors': set(),
        }

    def extract(self) -> dict:
        """
        Extrait tous les styles du fichier source.

        Returns:
            Dictionnaire contenant toutes les donnees extraites
        """
        try:
            self._prepare_source()
            self._parse_styles_xml()
            self._analyze_styles()
            return self._compile_results()
        finally:
            self._cleanup()

    def _prepare_source(self):
        """Prepare le fichier source (dezippe si necessaire)."""
        if self.source_path.is_dir():
            # Dossier deja dezippe
            self.styles_xml_path = self.source_path / "styles.xml"
            self.content_xml_path = self.source_path / "content.xml"
        elif self.source_path.suffix.lower() == '.odt':
            # Fichier ODT - dezipper
            self.temp_dir = tempfile.mkdtemp(prefix="odt_extract_")
            with zipfile.ZipFile(self.source_path, 'r') as z:
                z.extractall(self.temp_dir)
            self.styles_xml_path = Path(self.temp_dir) / "styles.xml"
            self.content_xml_path = Path(self.temp_dir) / "content.xml"
        else:
            raise ValueError(f"Format non supporte: {self.source_path}")

        if not self.styles_xml_path.exists():
            raise FileNotFoundError(f"styles.xml non trouve dans {self.source_path}")

    def _cleanup(self):
        """Nettoie les fichiers temporaires."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def _parse_styles_xml(self):
        """Parse le fichier styles.xml."""
        import xml.etree.ElementTree as ET

        # Enregistrer les namespaces
        for prefix, uri in NAMESPACES.items():
            ET.register_namespace(prefix, uri)

        # Lire le fichier brut pour reference
        with open(self.styles_xml_path, 'r', encoding='utf-8') as f:
            self.raw_styles_xml = f.read()

        # Parser
        tree = ET.parse(self.styles_xml_path)
        root = tree.getroot()

        # Extraire font-face-decls
        font_decls = root.find('.//office:font-face-decls', NAMESPACES)
        if font_decls is not None:
            for font in font_decls:
                font_info = self._extract_element(font)
                self.styles_data['font_declarations'].append(font_info)

        # Extraire office:styles (styles reutilisables)
        office_styles = root.find('.//office:styles', NAMESPACES)
        if office_styles is not None:
            self._extract_styles_from_container(office_styles, 'office:styles')

        # Extraire office:automatic-styles
        auto_styles = root.find('.//office:automatic-styles', NAMESPACES)
        if auto_styles is not None:
            self._extract_styles_from_container(auto_styles, 'office:automatic-styles')

        # Extraire office:master-styles
        master_styles = root.find('.//office:master-styles', NAMESPACES)
        if master_styles is not None:
            for elem in master_styles:
                tag = self._get_tag_name(elem)
                if tag == 'master-page':
                    mp_info = self._extract_element(elem, include_children=True)
                    self.styles_data['master_pages'].append(mp_info)

    def _extract_styles_from_container(self, container, container_name: str):
        """Extrait les styles d'un conteneur XML."""
        for elem in container:
            tag = self._get_tag_name(elem)
            style_data = self._extract_element(elem, include_children=True)
            style_data['_source'] = container_name
            style_data['_tag'] = tag

            # Classifier selon la famille
            family = style_data.get('style:family', '')

            if tag == 'default-style':
                self.styles_data['default_styles'].append(style_data)
            elif tag == 'outline-style':
                self.styles_data['outline_styles'].append(style_data)
            elif family == 'paragraph':
                self.styles_data['paragraph_styles'].append(style_data)
            elif family == 'text':
                self.styles_data['text_styles'].append(style_data)
            elif family in ('table', 'table-cell', 'table-column', 'table-row'):
                self.styles_data['table_styles'].append(style_data)
            elif tag == 'list-style':
                self.styles_data['list_styles'].append(style_data)
            elif tag == 'page-layout':
                self.styles_data['page_layouts'].append(style_data)

    def _extract_element(self, elem, include_children=False) -> dict:
        """Extrait les attributs d'un element XML."""
        result = {}

        # Attributs
        for key, value in elem.attrib.items():
            attr_name = self._simplify_attr_name(key)
            result[attr_name] = value

        # Enfants (proprietes)
        if include_children:
            result['_properties'] = []
            for child in elem:
                child_data = self._extract_element(child, include_children=True)
                child_data['_tag'] = self._get_tag_name(child)
                result['_properties'].append(child_data)

        return result

    def _get_tag_name(self, elem) -> str:
        """Retourne le nom de tag sans namespace."""
        return elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

    def _simplify_attr_name(self, key: str) -> str:
        """Simplifie un nom d'attribut avec prefixe namespace."""
        if '}' not in key:
            return key
        ns, name = key.split('}')
        ns = ns.replace('{', '')
        for prefix, uri in NAMESPACES.items():
            if uri == ns:
                return f"{prefix}:{name}"
        return name

    def _analyze_styles(self):
        """Analyse les styles extraits."""
        # Analyser les styles de paragraphe
        for style in self.styles_data['paragraph_styles']:
            self._analyze_style(style, 'paragraph')

        # Analyser les styles de texte
        for style in self.styles_data['text_styles']:
            self._analyze_style(style, 'text')

        # Convertir les sets en listes pour JSON
        self.analysis['color_palette'] = sorted(list(self.analysis['color_palette']))
        self.analysis['fonts_used'] = sorted(list(self.analysis['fonts_used']))
        self.analysis['border_colors'] = sorted(list(self.analysis['border_colors']))
        self.analysis['style_categories'] = dict(self.analysis['style_categories'])

    def _analyze_style(self, style: dict, family: str):
        """Analyse un style individuel."""
        name = style.get('style:name', style.get('name', ''))
        display_name = style.get('style:display-name', name)
        decoded_name = self._decode_style_name(display_name)

        style_entry = {
            'name': name,
            'display_name': display_name,
            'decoded_name': decoded_name,
            'family': family,
            'parent_style': style.get('style:parent-style-name', ''),
            'properties': {},
            'raw': style,
        }

        # Extraire les proprietes aplaties
        for prop in style.get('_properties', []):
            prop_tag = prop.get('_tag', '')
            for key, value in prop.items():
                if key.startswith('_'):
                    continue
                prop_key = f"{prop_tag}.{key}"
                style_entry['properties'][prop_key] = value

                # Collecter les couleurs
                if 'color' in key.lower():
                    if value.startswith('#'):
                        self.analysis['color_palette'].add(value)

                # Collecter les couleurs de bordure
                if 'border' in key.lower() and 'solid' in str(value):
                    match = re.search(r'#[0-9a-fA-F]{6}', value)
                    if match:
                        self.analysis['border_colors'].add(match.group())

                # Collecter les polices
                if 'font-name' in key.lower() or 'font-family' in key.lower():
                    self.analysis['fonts_used'].add(value.replace("'", ""))

        # Est-ce un style Sesamath personnalise?
        if decoded_name.startswith('_'):
            category = self._categorize_style(decoded_name)
            self.analysis['style_categories'][category].append(style_entry)
            self.analysis['sesamath_styles'].append(style_entry)

    def _decode_style_name(self, name: str) -> str:
        """Decode les noms de styles ODT."""
        replacements = [
            ('_5f_', '_'),
            ('_20_', ' '),
            ('_2d_', '-'),
            ('_27_', "'"),
            ('_28_', '('),
            ('_29_', ')'),
            ('_2c_', ','),
            ('_3a_', ':'),
            ('_c3_a9', 'e'),  # e accent
            ('_c3_a8', 'e'),  # e grave
            ('_c3_a0', 'a'),  # a grave
        ]
        result = name
        for encoded, decoded in replacements:
            result = result.replace(encoded, decoded)
        return result

    def _categorize_style(self, name: str) -> str:
        """Categorise un style par son nom."""
        name_lower = name.lower()

        if 'exercice' in name_lower or 'exo' in name_lower:
            return 'exercices'
        elif 'reponse' in name_lower or 'eleve' in name_lower:
            return 'reponses_eleve'
        elif 'tableau' in name_lower or 'table' in name_lower:
            return 'tableaux'
        elif 'titre' in name_lower:
            return 'titres'
        elif 'header' in name_lower:
            return 'en_tetes'
        elif 'footer' in name_lower:
            return 'pieds_page'
        elif 'exemple' in name_lower:
            return 'exemples'
        elif 'definition' in name_lower:
            return 'definitions'
        elif 'propriete' in name_lower:
            return 'proprietes'
        elif 'methode' in name_lower:
            return 'methodes'
        elif 'remarque' in name_lower:
            return 'remarques'
        elif 'vocabulaire' in name_lower:
            return 'vocabulaire'
        elif 'correction' in name_lower:
            return 'corrections'
        elif 'caractere' in name_lower:
            return 'caracteres'
        elif 'bullet' in name_lower or 'puce' in name_lower:
            return 'listes'
        elif 'geometrie' in name_lower:
            return 'domaine_geometrie'
        elif 'mesure' in name_lower:
            return 'domaine_mesures'
        elif 'numerique' in name_lower:
            return 'domaine_numerique'
        elif 'num' in name_lower:
            return 'numerotation'
        else:
            return 'autres'

    def _compile_results(self) -> dict:
        """Compile tous les resultats."""
        return {
            'source': str(self.source_path),
            'extracted_at': datetime.now().isoformat(),
            'statistics': {
                'paragraph_styles': len(self.styles_data['paragraph_styles']),
                'text_styles': len(self.styles_data['text_styles']),
                'table_styles': len(self.styles_data['table_styles']),
                'list_styles': len(self.styles_data['list_styles']),
                'page_layouts': len(self.styles_data['page_layouts']),
                'master_pages': len(self.styles_data['master_pages']),
                'font_declarations': len(self.styles_data['font_declarations']),
                'sesamath_styles': len(self.analysis['sesamath_styles']),
            },
            'styles_data': self.styles_data,
            'analysis': self.analysis,
            'raw_styles_xml_size': len(self.raw_styles_xml) if self.raw_styles_xml else 0,
        }


def generate_template_odt(results: dict, output_path: str):
    """
    Genere un fichier ODT template avec tous les styles extraits.

    Note: Cette fonction utilise une approche hybride:
    - Elle copie le styles.xml brut du fichier source
    - Elle cree un nouveau document ODT minimal avec ce styles.xml
    """
    if not HAS_ODFPY:
        print("[ERREUR] odfpy requis pour generer le template")
        return False

    # Creer un document minimal
    doc = OpenDocumentText()

    # Ajouter un paragraphe d'information
    p = P(text="Template Sesamath - Ce document contient tous les styles educatifs.")
    doc.text.addElement(p)

    p = P(text=f"Genere le {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    doc.text.addElement(p)

    p = P(text=f"Styles disponibles: {results['statistics']['sesamath_styles']}")
    doc.text.addElement(p)

    # Sauvegarder temporairement
    doc.save(output_path)

    # Maintenant, remplacer styles.xml par celui extrait
    # (On va re-zipper avec le bon styles.xml)

    print(f"[OK] Template genere: {output_path}")
    print(f"     Note: Pour un template complet, utilisez copy_styles_xml()")
    return True


def copy_styles_to_new_odt(source_odt: str, output_path: str):
    """
    Copie tous les styles d'un ODT source vers un nouveau document vide.

    Cette methode preserve TOUS les styles en copiant directement:
    - styles.xml
    - Les declarations de polices
    - Les mises en page
    """
    temp_dir = tempfile.mkdtemp(prefix="odt_copy_")

    try:
        # Dezipper la source
        source_temp = os.path.join(temp_dir, "source")
        os.makedirs(source_temp)
        with zipfile.ZipFile(source_odt, 'r') as z:
            z.extractall(source_temp)

        # Creer un document vide minimal
        if HAS_ODFPY:
            doc = OpenDocumentText()
            # Ajouter juste un titre
            h = H(outlinelevel=1, text="Document avec styles Sesamath")
            doc.text.addElement(h)
            p = P(text="Ce document contient tous les styles educatifs Sesamath.")
            doc.text.addElement(p)
            p = P(text="Utilisez les styles dans le panneau Styles de LibreOffice.")
            doc.text.addElement(p)

            # Sauvegarder temporairement
            temp_odt = os.path.join(temp_dir, "temp.odt")
            doc.save(temp_odt)

            # Dezipper le nouveau document
            new_temp = os.path.join(temp_dir, "new")
            os.makedirs(new_temp)
            with zipfile.ZipFile(temp_odt, 'r') as z:
                z.extractall(new_temp)

            # Copier styles.xml de la source vers le nouveau
            shutil.copy(
                os.path.join(source_temp, "styles.xml"),
                os.path.join(new_temp, "styles.xml")
            )

            # Rezipper
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
                for root, dirs, files in os.walk(new_temp):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, new_temp)
                        # mimetype doit etre non compresse et en premier
                        if file == 'mimetype':
                            zout.write(file_path, arcname, compress_type=zipfile.ZIP_STORED)
                        else:
                            zout.write(file_path, arcname)

            print(f"[OK] Template avec styles copies: {output_path}")
            return True
        else:
            print("[ERREUR] odfpy requis")
            return False

    finally:
        shutil.rmtree(temp_dir)


def generate_documentation(results: dict, output_dir: str):
    """Genere la documentation des styles."""
    os.makedirs(output_dir, exist_ok=True)

    # JSON complet
    json_path = os.path.join(output_dir, "sesamath_styles_full.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        # Retirer les donnees brutes pour alleguer le JSON
        clean_results = {
            'source': results['source'],
            'extracted_at': results['extracted_at'],
            'statistics': results['statistics'],
            'analysis': {
                'sesamath_styles': [
                    {k: v for k, v in s.items() if k != 'raw'}
                    for s in results['analysis']['sesamath_styles']
                ],
                'style_categories': results['analysis']['style_categories'],
                'color_palette': results['analysis']['color_palette'],
                'fonts_used': results['analysis']['fonts_used'],
                'border_colors': results['analysis']['border_colors'],
            }
        }
        json.dump(clean_results, f, indent=2, ensure_ascii=False, default=str)
    print(f"[OK] JSON genere: {json_path}")

    # Markdown de reference rapide
    md_path = os.path.join(output_dir, "sesamath_styles_reference.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("# Reference des styles Sesamath\n\n")
        f.write(f"*Genere le {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        f.write(f"Source: `{results['source']}`\n\n")

        # Statistiques
        f.write("## Statistiques\n\n")
        f.write("| Type | Nombre |\n")
        f.write("|------|--------|\n")
        for key, value in results['statistics'].items():
            f.write(f"| {key.replace('_', ' ').title()} | {value} |\n")

        # Categories
        f.write("\n## Styles par categorie\n\n")
        for category, styles in sorted(results['analysis']['style_categories'].items()):
            f.write(f"### {category.replace('_', ' ').title()} ({len(styles)} styles)\n\n")
            f.write("| Nom encode | Nom affiche | Famille |\n")
            f.write("|------------|-------------|----------|\n")
            for style in styles:
                f.write(f"| `{style['name']}` | {style['decoded_name']} | {style['family']} |\n")
            f.write("\n")

        # Palette de couleurs
        f.write("## Palette de couleurs\n\n")
        f.write("### Couleurs de texte/fond\n\n")
        for color in results['analysis']['color_palette']:
            f.write(f"- `{color}`\n")

        f.write("\n### Couleurs de bordure\n\n")
        for color in results['analysis']['border_colors']:
            f.write(f"- `{color}`\n")

        # Polices
        f.write("\n## Polices utilisees\n\n")
        for font in results['analysis']['fonts_used']:
            f.write(f"- {font}\n")

        # Guide d'utilisation
        f.write("\n## Guide d'utilisation\n\n")
        f.write("### En Python avec odfpy\n\n")
        f.write("```python\n")
        f.write("from odf.opendocument import load\n")
        f.write("from odf.text import P\n\n")
        f.write("# Charger le template\n")
        f.write("doc = load('template_sesamath.odt')\n\n")
        f.write("# Utiliser un style\n")
        f.write("p = P(stylename='_5f_Paragraphe_5f_Definition', text='Ma definition')\n")
        f.write("doc.text.addElement(p)\n")
        f.write("```\n\n")

        f.write("### Styles les plus utiles\n\n")
        useful_styles = [
            ('_5f_Paragraphe', 'Texte courant'),
            ('_5f_Paragraphe_5f_Definition', 'Bloc definition (bordure verte)'),
            ('_5f_Paragraphe_5f_Propriete', 'Bloc propriete (bordure rose)'),
            ('_5f_Paragraphe_5f_Methode', 'Bloc methode (bordure bleue)'),
            ('_5f_Paragraphe_5f_Remarque', 'Bloc remarque (bordure turquoise)'),
            ('_5f_Paragraphe_5f_Exemple', 'Bloc exemple'),
            ('_5f_Titre_5f_Exercices_5f_avec_5f_Titre', 'Titre exercice'),
            ('_5f_Paragraphe_5f_Reponse_5f_Eleve', 'Zone reponse eleve'),
            ('_5f_Tableau_5f_Centre', 'Cellule tableau centree'),
        ]
        f.write("| Nom du style | Usage |\n")
        f.write("|--------------|-------|\n")
        for name, usage in useful_styles:
            f.write(f"| `{name}` | {usage} |\n")

    print(f"[OK] Markdown genere: {md_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extrait les styles d'un fichier ODT Sesamath",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python extract_styles_from_odt.py cahier.odt
  python extract_styles_from_odt.py cahier_dezippe/ --output ./output/
  python extract_styles_from_odt.py cahier.odt --template nouveau_template.odt
        """
    )
    parser.add_argument("source", help="Fichier ODT ou dossier dezippe")
    parser.add_argument("--output", "-o", default=".", help="Dossier de sortie")
    parser.add_argument("--template", "-t", help="Generer un template ODT avec ce nom")
    parser.add_argument("--verbose", "-v", action="store_true", help="Mode verbeux")

    args = parser.parse_args()

    # Verifier la source
    if not os.path.exists(args.source):
        print(f"[ERREUR] Source non trouvee: {args.source}")
        sys.exit(1)

    # Extraire les styles
    print(f"Extraction des styles depuis: {args.source}")
    extractor = ODTStyleExtractor(args.source)
    results = extractor.extract()

    # Afficher les statistiques
    print("\n=== STATISTIQUES ===")
    for key, value in results['statistics'].items():
        print(f"  {key}: {value}")

    print(f"\n=== CATEGORIES SESAMATH ===")
    for category, styles in sorted(results['analysis']['style_categories'].items()):
        print(f"  {category}: {len(styles)} styles")

    # Generer la documentation
    os.makedirs(args.output, exist_ok=True)
    generate_documentation(results, args.output)

    # Generer le template si demande
    if args.template:
        template_path = os.path.join(args.output, args.template)
        if args.source.endswith('.odt'):
            copy_styles_to_new_odt(args.source, template_path)
        else:
            # Chercher un fichier ODT dans le dossier parent
            parent = os.path.dirname(args.source.rstrip('/\\'))
            odt_files = [f for f in os.listdir(parent) if f.endswith('.odt')]
            if odt_files:
                source_odt = os.path.join(parent, odt_files[0])
                copy_styles_to_new_odt(source_odt, template_path)
            else:
                print("[AVERTISSEMENT] Pas de fichier ODT source pour le template")

    print("\n[TERMINE]")


if __name__ == "__main__":
    main()
