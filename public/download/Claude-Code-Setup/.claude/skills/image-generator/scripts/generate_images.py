#!/usr/bin/env python3
"""
Script pour générer des images avec l'API Google Imagen.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, List
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Charger les variables d'environnement
load_dotenv()

# Modèles disponibles
MODELS = {
    "fast": "imagen-4.0-fast-generate-001",
    "standard": "imagen-4.0-generate-001",
    "ultra": "imagen-4.0-ultra-generate-001",
    "imagen3": "imagen-3.0-generate-002"
}

# Formats d'image disponibles
ASPECT_RATIOS = {
    "square": "1:1",
    "fullscreen": "4:3",
    "fullscreen_portrait": "3:4",
    "widescreen": "16:9",
    "portrait": "9:16"
}


def generate_images(
    prompt: str,
    output_dir: str,
    model: str = "standard",
    num_images: int = 4,
    aspect_ratio: str = "square",
    image_size: str = "1K",
    person_generation: str = "allow_adult",
    base_filename: str = "generated_image"
) -> List[str]:
    """
    Génère des images avec l'API Google Imagen.

    Args:
        prompt: Texte de description pour générer l'image
        output_dir: Répertoire où sauvegarder les images
        model: Modèle à utiliser (fast, standard, ultra, imagen3)
        num_images: Nombre d'images à générer (1-4)
        aspect_ratio: Format de l'image (square, fullscreen, etc.)
        image_size: Taille de l'image (1K ou 2K, uniquement pour standard/ultra)
        person_generation: Autorisation de générer des personnes
        base_filename: Nom de base pour les fichiers générés

    Returns:
        Liste des chemins des fichiers générés
    """
    # Récupérer la clé API
    api_key = os.getenv("NANOBANANA_API_KEY")
    if not api_key:
        raise ValueError("NANOBANANA_API_KEY non trouvée dans .env")

    # Créer le client
    client = genai.Client(api_key=api_key)

    # Sélectionner le modèle
    model_id = MODELS.get(model, MODELS["standard"])

    # Configuration de la génération
    config_params = {
        "number_of_images": num_images,
        "aspect_ratio": ASPECT_RATIOS.get(aspect_ratio, "1:1"),
        "person_generation": person_generation
    }

    # Ajouter image_size seulement pour standard/ultra
    if model in ["standard", "ultra"]:
        config_params["image_size"] = image_size

    config = types.GenerateImagesConfig(**config_params)

    # Générer les images
    print(f"Génération de {num_images} image(s) avec le modèle {model}...")
    print(f"Prompt: {prompt}")

    response = client.models.generate_images(
        model=model_id,
        prompt=prompt,
        config=config
    )

    # Créer le répertoire de sortie s'il n'existe pas
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Sauvegarder les images
    saved_files = []
    for i, generated_image in enumerate(response.generated_images):
        filename = f"{base_filename}_{i+1}.png"
        filepath = output_path / filename

        # Sauvegarder l'image
        generated_image.image.save(str(filepath))
        saved_files.append(str(filepath))
        print(f"Image sauvegardée: {filepath}")

    return saved_files


def main():
    parser = argparse.ArgumentParser(
        description="Générer des images avec l'API Google Imagen"
    )
    parser.add_argument(
        "prompt",
        type=str,
        help="Description textuelle pour générer l'image"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        required=True,
        help="Répertoire de sortie pour les images"
    )
    parser.add_argument(
        "-m", "--model",
        type=str,
        choices=["fast", "standard", "ultra", "imagen3"],
        default="standard",
        help="Modèle à utiliser (défaut: standard)"
    )
    parser.add_argument(
        "-n", "--num-images",
        type=int,
        default=4,
        choices=[1, 2, 3, 4],
        help="Nombre d'images à générer (1-4, défaut: 4)"
    )
    parser.add_argument(
        "-a", "--aspect-ratio",
        type=str,
        choices=list(ASPECT_RATIOS.keys()),
        default="square",
        help="Format de l'image (défaut: square)"
    )
    parser.add_argument(
        "-s", "--image-size",
        type=str,
        choices=["1K", "2K"],
        default="1K",
        help="Taille de l'image (1K ou 2K, défaut: 1K)"
    )
    parser.add_argument(
        "-p", "--person-generation",
        type=str,
        choices=["dont_allow", "allow_adult", "allow_all"],
        default="allow_adult",
        help="Autorisation de générer des personnes (défaut: allow_adult)"
    )
    parser.add_argument(
        "-f", "--filename",
        type=str,
        default="generated_image",
        help="Nom de base pour les fichiers (défaut: generated_image)"
    )

    args = parser.parse_args()

    try:
        saved_files = generate_images(
            prompt=args.prompt,
            output_dir=args.output_dir,
            model=args.model,
            num_images=args.num_images,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            person_generation=args.person_generation,
            base_filename=args.filename
        )

        print(f"\nSuccès! {len(saved_files)} image(s) générée(s):")
        for file in saved_files:
            print(f"  - {file}")

    except Exception as e:
        print(f"Erreur: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
