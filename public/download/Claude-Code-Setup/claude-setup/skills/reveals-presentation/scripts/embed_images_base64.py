#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script généralisé pour convertir toutes les images d'un fichier HTML en base64.
Crée une version "embedded" autonome et portable du HTML.

IMPORTANT: Utiliser uniquement pour partager le document une fois TOUTES les modifications terminées.
La version embedded sera plus lourde mais entièrement portable (pas de dossier images externe).

Usage:
    python embed_images_base64.py <fichier_html> [--output <fichier_sortie>] [--suffix <suffixe>]

Arguments:
    fichier_html : Fichier HTML contenant des balises <img> avec src locale
    --output : Nom du fichier de sortie (défaut: <nom>_embedded.html)
    --suffix : Suffixe pour le fichier de sortie (défaut: _embedded)
"""

import re
import base64
import os
import argparse
import sys
from pathlib import Path

def get_image_mime_type(image_path):
    """Détermine le type MIME d'une image selon son extension."""
    ext = image_path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.ico': 'image/x-icon'
    }
    return mime_types.get(ext, 'image/png')

def image_to_base64(image_path):
    """Convertit une image en chaîne base64."""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"  ERREUR lors de la lecture de {image_path}: {e}")
        return None

def convert_html_images_to_base64(html_file_path, output_file_path=None, suffix="_embedded"):
    """
    Convertit toutes les images locales d'un fichier HTML en base64.

    Args:
        html_file_path: Chemin vers le fichier HTML source
        output_file_path: Chemin vers le fichier HTML de sortie (optionnel)
        suffix: Suffixe à ajouter au nom du fichier si output_file_path n'est pas spécifié

    Returns:
        Path vers le fichier créé
    """
    html_path = Path(html_file_path)

    if not html_path.exists():
        raise FileNotFoundError(f"Le fichier {html_file_path} n'existe pas")

    # Déterminer le fichier de sortie
    if output_file_path:
        output_path = Path(output_file_path)
    else:
        output_path = html_path.parent / f"{html_path.stem}{suffix}{html_path.suffix}"

    # Lire le contenu HTML
    print(f"Lecture du fichier {html_path.name}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Trouver toutes les balises img avec src
    # Pattern pour capturer les guillemets simples ou doubles
    img_pattern = r'<img\s+([^>]*\s+)?src=(["\'])([^"\']+)\2([^>]*)>'
    matches = list(re.finditer(img_pattern, html_content))

    print(f"  -> {len(matches)} balise(s) <img> trouvee(s)\n")

    # Compter les images converties
    converted_count = 0
    skipped_count = 0
    total_size_kb = 0

    # Parcourir toutes les correspondances
    for i, match in enumerate(matches, 1):
        full_tag = match.group(0)
        quote_char = match.group(2)  # Mémoriser le type de guillemet utilisé
        src_value = match.group(3)

        # Ignorer les URLs externes et les images déjà en base64
        if src_value.startswith(('http://', 'https://', 'data:', '//', 'mailto:')):
            print(f"[{i}/{len(matches)}] Ignoré (externe/base64): {src_value[:50]}...")
            skipped_count += 1
            continue

        # Construire le chemin complet vers l'image
        image_path = html_path.parent / src_value

        if not image_path.exists():
            print(f"[{i}/{len(matches)}] Image introuvable: {src_value}")
            print(f"  Chemin recherché: {image_path}")
            skipped_count += 1
            continue

        # Convertir l'image en base64
        print(f"[{i}/{len(matches)}] Conversion: {src_value}...")
        base64_data = image_to_base64(image_path)

        if base64_data is None:
            skipped_count += 1
            continue

        # Déterminer le type MIME
        mime_type = get_image_mime_type(image_path)

        # Créer le data URI
        data_uri = f"data:{mime_type};base64,{base64_data}"

        # Créer la nouvelle balise img avec data URI (en conservant le type de guillemet)
        new_tag = full_tag.replace(f'src={quote_char}{src_value}{quote_char}', f'src={quote_char}{data_uri}{quote_char}')

        # Remplacer dans le HTML
        html_content = html_content.replace(full_tag, new_tag)
        converted_count += 1

        # Afficher la taille de l'image
        size_kb = len(base64_data) * 3 / 4 / 1024  # Approximation de la taille
        total_size_kb += size_kb
        print(f"  OK ({size_kb:.1f} KB)")

    # Écrire le nouveau fichier HTML
    print(f"\nEcriture du fichier {output_path.name}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Statistiques
    original_size_kb = html_path.stat().st_size / 1024
    new_size_kb = output_path.stat().st_size / 1024

    print("\n" + "=" * 60)
    print("Conversion terminee !")
    print(f"  - {converted_count} image(s) convertie(s) en base64")
    print(f"  - {skipped_count} image(s) ignoree(s)")
    print(f"  - Taille totale des images: {total_size_kb:.1f} KB")
    print(f"\nTailles des fichiers:")
    print(f"  - Original: {original_size_kb:.1f} KB")
    print(f"  - Embedded: {new_size_kb:.1f} KB")
    print(f"  - Augmentation: +{new_size_kb - original_size_kb:.1f} KB")
    print(f"\nFichier cree: {output_path.absolute()}")
    print("=" * 60)

    return output_path

def main():
    parser = argparse.ArgumentParser(
        description="Convertit les images d'un fichier HTML en base64 pour créer une version portable",
        epilog="IMPORTANT: Utiliser uniquement pour partager le document une fois TOUTES les modifications terminées."
    )
    parser.add_argument(
        "html_file",
        help="Fichier HTML à traiter"
    )
    parser.add_argument(
        "--output",
        help="Nom du fichier de sortie (défaut: <nom>_embedded.html)"
    )
    parser.add_argument(
        "--suffix",
        default="_embedded",
        help="Suffixe pour le fichier de sortie si --output n'est pas spécifié (défaut: _embedded)"
    )

    args = parser.parse_args()

    try:
        output_path = convert_html_images_to_base64(
            args.html_file,
            args.output,
            args.suffix
        )

        print(f"\nLe fichier embedded est pret pour le partage:")
        print(f"  {output_path.name}")
        print("\nCe fichier est totalement autonome et ne necessite aucun fichier externe.")

    except FileNotFoundError as e:
        print(f"ERREUR: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERREUR inattendue: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
