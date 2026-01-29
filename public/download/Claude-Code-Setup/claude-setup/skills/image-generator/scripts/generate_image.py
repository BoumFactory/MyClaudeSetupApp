#!/usr/bin/env python3
"""
Script de generation d'images via l'API Google Imagen 4.0.
Utilise le modele imagen-4.0-generate-001 pour generer des images de haute qualite.
"""

import argparse
import os
import sys
from pathlib import Path

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv

# Trouver le fichier .env a la racine du projet
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent.parent.parent  # Remonter de scripts -> image-generator -> skills -> .claude -> racine
env_path = project_root / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    # Essayer aussi le repertoire courant
    load_dotenv()

from google import genai
from google.genai import types


def generate_image(
    prompt: str,
    output_path: str,
    filename: str = "generated_image",
    width: int = 1920,
    height: int = 1080,
    number_of_images: int = 1,
    model: str = "imagen-4.0-generate-001"
):
    """
    Genere une image avec l'API Google Imagen 4.0.

    Args:
        prompt: Description de l'image a generer (en anglais)
        output_path: Dossier de sortie
        filename: Nom du fichier (sans extension)
        width: Largeur de l'image
        height: Hauteur de l'image
        number_of_images: Nombre d'images a generer
        model: Modele a utiliser (imagen-4.0-generate-001, imagen-4.0-fast-generate-001, imagen-4.0-ultra-generate-001)
    """
    # Recuperer la cle API
    api_key = os.getenv("NANOBANANA_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ERREUR: Aucune cle API trouvee.")
        print("Definissez NANOBANANA_API_KEY, GOOGLE_API_KEY ou GEMINI_API_KEY dans le fichier .env")
        sys.exit(1)

    # Initialiser le client
    client = genai.Client(api_key=api_key)

    # Creer le dossier de sortie si necessaire
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    aspect_ratio = get_aspect_ratio(width, height)
    print(f"Generation de {number_of_images} image(s)...")
    print(f"Modele: {model}")
    print(f"Prompt: {prompt}")
    print(f"Dimensions cibles: {width}x{height} (ratio: {aspect_ratio})")

    try:
        # Generer l'image avec Imagen 4.0
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=number_of_images,
                aspect_ratio=aspect_ratio,
                safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            )
        )

        # Sauvegarder les images
        generated_files = []
        for i, image in enumerate(response.generated_images):
            if number_of_images == 1:
                file_path = output_dir / f"{filename}.png"
            else:
                file_path = output_dir / f"{filename}_{i+1}.png"

            # Sauvegarder l'image
            image.image.save(str(file_path))
            generated_files.append(str(file_path))
            print(f"Image sauvegardee: {file_path}")

        return generated_files

    except Exception as e:
        print(f"ERREUR lors de la generation: {e}")
        sys.exit(1)


def get_aspect_ratio(width: int, height: int) -> str:
    """
    Determine le ratio d'aspect le plus proche parmi ceux supportes par Imagen.
    Ratios supportes: 1:1, 3:4, 4:3, 9:16, 16:9
    """
    ratio = width / height

    ratios = {
        "1:1": 1.0,
        "4:3": 4/3,
        "3:4": 3/4,
        "16:9": 16/9,
        "9:16": 9/16
    }

    # Trouver le ratio le plus proche
    closest = min(ratios.keys(), key=lambda k: abs(ratios[k] - ratio))
    return closest


def main():
    parser = argparse.ArgumentParser(
        description="Genere des images avec l'API Google Imagen 4.0"
    )
    parser.add_argument(
        "prompt",
        help="Description de l'image a generer (en anglais)"
    )
    parser.add_argument(
        "-o", "--output",
        default=".",
        help="Dossier de sortie (defaut: dossier courant)"
    )
    parser.add_argument(
        "-f", "--filename",
        default="generated_image",
        help="Nom du fichier sans extension (defaut: generated_image)"
    )
    parser.add_argument(
        "-W", "--width",
        type=int,
        default=1920,
        help="Largeur de l'image (defaut: 1920)"
    )
    parser.add_argument(
        "-H", "--height",
        type=int,
        default=1080,
        help="Hauteur de l'image (defaut: 1080)"
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        default=1,
        choices=[1, 2, 3, 4],
        help="Nombre d'images a generer (1-4, defaut: 1)"
    )
    parser.add_argument(
        "-m", "--model",
        default="imagen-4.0-generate-001",
        choices=["imagen-4.0-generate-001", "imagen-4.0-fast-generate-001", "imagen-4.0-ultra-generate-001"],
        help="Modele a utiliser (defaut: imagen-4.0-generate-001)"
    )

    args = parser.parse_args()

    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        filename=args.filename,
        width=args.width,
        height=args.height,
        number_of_images=args.number,
        model=args.model
    )


if __name__ == "__main__":
    main()
