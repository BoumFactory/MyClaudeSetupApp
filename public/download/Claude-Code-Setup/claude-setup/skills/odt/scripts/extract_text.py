#!/usr/bin/env python3
"""
Extrait le texte brut d'un fichier ODT.
Usage: python extract_text.py <fichier.odt>
"""
import zipfile
import sys
from xml.etree import ElementTree as ET

def extract_text(odt_path: str) -> str:
    """Extrait le texte brut d'un fichier ODT."""
    TEXT_NS = '{urn:oasis:names:tc:opendocument:xmlns:text:1.0}'

    with zipfile.ZipFile(odt_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    paragraphs = []

    for p in root.iter(f'{TEXT_NS}p'):
        text = ''.join(p.itertext())
        if text.strip():
            paragraphs.append(text)

    return '\n'.join(paragraphs)

def extract_styles(odt_path: str) -> list:
    """Liste les styles utilises dans un fichier ODT."""
    STYLE_NS = '{urn:oasis:names:tc:opendocument:xmlns:style:1.0}'

    with zipfile.ZipFile(odt_path, 'r') as z:
        styles_content = z.read('styles.xml').decode('utf-8')

    root = ET.fromstring(styles_content)
    styles = []

    for style in root.iter(f'{STYLE_NS}style'):
        name = style.get(f'{STYLE_NS}name', '')
        display_name = style.get(f'{STYLE_NS}display-name', name)
        family = style.get(f'{STYLE_NS}family', '')
        if display_name.startswith('_'):
            styles.append({'name': name, 'display_name': display_name, 'family': family})

    return styles

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_text.py <fichier.odt> [--styles]")
        sys.exit(1)

    odt_path = sys.argv[1]

    if '--styles' in sys.argv:
        styles = extract_styles(odt_path)
        print("Styles personnalises:")
        for s in styles:
            print(f"  {s['display_name']} ({s['family']})")
    else:
        text = extract_text(odt_path)
        print(text)
