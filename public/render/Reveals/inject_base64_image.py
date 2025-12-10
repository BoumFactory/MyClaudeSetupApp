#!/usr/bin/env python3
"""
Script pour injecter une image en base64 dans un fichier HTML.
Remplace un placeholder <!-- BASE64_IMAGE_PLACEHOLDER:id --> par l'image encodée.

Usage:
    python inject_base64_image.py <html_file> <image_file> [--id <placeholder_id>]

Exemple:
    python inject_base64_image.py infography-generator-skill.html gaia.png --id infography-example
"""

import argparse
import base64
import sys
from pathlib import Path


def get_mime_type(image_path: Path) -> str:
    """Retourne le type MIME basé sur l'extension."""
    ext = image_path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
    }
    return mime_types.get(ext, 'image/png')


def encode_image_to_base64(image_path: Path) -> str:
    """Encode une image en base64 avec le préfixe data URI."""
    with open(image_path, 'rb') as f:
        image_data = f.read()

    b64_data = base64.b64encode(image_data).decode('utf-8')
    mime_type = get_mime_type(image_path)

    return f"data:{mime_type};base64,{b64_data}"


def inject_image(html_path: Path, image_path: Path, placeholder_id: str = "default") -> bool:
    """Injecte l'image base64 dans le fichier HTML."""

    # Lire le fichier HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Placeholder à chercher
    placeholder = f"<!-- BASE64_IMAGE_PLACEHOLDER:{placeholder_id} -->"

    if placeholder not in html_content:
        print(f"Erreur: Placeholder '{placeholder}' non trouve dans {html_path}")
        return False

    # Encoder l'image
    print(f"Encodage de {image_path}...")
    base64_data = encode_image_to_base64(image_path)
    print(f"Taille base64: {len(base64_data):,} caracteres")

    # Remplacer le placeholder
    html_content = html_content.replace(placeholder, base64_data)

    # Ecrire le fichier
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Image injectee avec succes dans {html_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Injecte une image en base64 dans un fichier HTML"
    )
    parser.add_argument('html_file', help="Fichier HTML cible")
    parser.add_argument('image_file', help="Fichier image a encoder")
    parser.add_argument('--id', default='default', help="ID du placeholder (defaut: default)")

    args = parser.parse_args()

    html_path = Path(args.html_file)
    image_path = Path(args.image_file)

    if not html_path.exists():
        print(f"Erreur: Fichier HTML non trouve: {html_path}")
        sys.exit(1)

    if not image_path.exists():
        print(f"Erreur: Fichier image non trouve: {image_path}")
        sys.exit(1)

    success = inject_image(html_path, image_path, args.id)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
