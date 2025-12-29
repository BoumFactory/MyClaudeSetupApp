#!/usr/bin/env python3
"""
Script de génération d'images via l'API Nano Banana (Google Imagen).
Version simplifiée utilisant juste une clé API.
"""

import json
import os
import sys
import argparse
import time
import base64
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement
load_dotenv()


class NanoBananaAPI:
    """Client pour l'API Nano Banana."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le client API Nano Banana.

        Args:
            api_key: Clé API Nano Banana (si None, charge depuis .env)
        """
        self.api_key = api_key or os.getenv("NANOBANANA_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

        if not self.api_key:
            print("\nERREUR: Cle API Google non trouvee!")
            print("   Veuillez configurer NANOBANANA_API_KEY dans le fichier .env")
            print("   Exemple: NANOBANANA_API_KEY=\"votre-cle-api\"\n")
            sys.exit(1)

        print(f"API Google Gemini initialisee (Nano Banana)")

    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        number_of_images: int = 1,
        model: str = "imagen-4.0-fast"
    ) -> Optional[List[bytes]]:
        """
        Génère une ou plusieurs images via l'API Google Gemini.

        Args:
            prompt: Description de l'image
            negative_prompt: Éléments à éviter
            number_of_images: Nombre d'images à générer
            model: ignoré (Gemini utilise gemini-2.5-flash-image-preview)

        Returns:
            Liste de données d'images en bytes, ou None si erreur
        """
        try:
            print(f"  Generation en cours avec Gemini 2.5 Flash Image...")

            # Format de requête pour l'API Gemini
            full_prompt = prompt
            if negative_prompt:
                full_prompt += f"\n\nNegative prompt (elements to avoid): {negative_prompt}"

            image_bytes_list = []

            # Générer les images une par une (Gemini ne supporte pas number_of_images)
            for i in range(number_of_images):
                payload = {
                    "contents": [{
                        "parts": [{"text": full_prompt}]
                    }],
                    "generationConfig": {
                        "response_modalities": ["image"]
                    }
                }

                url = f"{self.base_url}/models/gemini-2.5-flash-image-preview:generateContent?key={self.api_key}"

                response = requests.post(
                    url,
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    print(f"  DEBUG: Response structure: {list(result.keys())}")

                    # Extraire l'image en base64
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        print(f"  DEBUG: Candidate keys: {list(candidate.keys())}")

                        if "content" in candidate:
                            content = candidate["content"]
                            print(f"  DEBUG: Content keys: {list(content.keys())}")

                            if "parts" in content:
                                parts = content["parts"]
                                print(f"  DEBUG: Number of parts: {len(parts)}")

                                for idx, part in enumerate(parts):
                                    print(f"  DEBUG: Part {idx} keys: {list(part.keys())}")

                                    # Note: l'API utilise "inlineData" (camelCase) et non "inline_data"
                                    if "inlineData" in part:
                                        inline = part["inlineData"]
                                        print(f"  DEBUG: inlineData keys: {list(inline.keys())}")

                                        if "data" in inline:
                                            image_data = base64.b64decode(inline["data"])
                                            image_bytes_list.append(image_data)
                                            print(f"  Image {i+1} extraite avec succes")
                                            break
                    else:
                        print(f"  DEBUG: No candidates in response")
                else:
                    error_msg = response.text
                    print(f"\nERREUR {response.status_code}:")
                    print(error_msg)

                    if response.status_code == 401:
                        print("   Verifiez votre cle API Google")
                    elif response.status_code == 429:
                        print("   Limite de requetes atteinte. Attendez quelques minutes.")

                    return None

                # Pause entre les images
                if i < number_of_images - 1:
                    time.sleep(0.5)

            if image_bytes_list:
                print(f"  {len(image_bytes_list)} image(s) generee(s) avec succes")
            return image_bytes_list if image_bytes_list else None

        except requests.exceptions.Timeout:
            print("\nERREUR: Delai d'attente depasse")
            return None
        except Exception as e:
            print(f"\nERREUR lors de la generation: {str(e)}")
            return None


def generate_variations(
    api_client: NanoBananaAPI,
    prompt_data: Dict,
    num_variations: int,
    output_dir: Path,
    image_id: int,
    model: str = "imagen-4.0-fast"
) -> List[Path]:
    """
    Génère plusieurs variations d'une image.

    Args:
        api_client: Client API initialisé
        prompt_data: Données du prompt
        num_variations: Nombre de variations à générer
        output_dir: Répertoire de sortie
        image_id: ID de l'image
        model: Nom du modèle

    Returns:
        Liste des chemins des images générées
    """
    generated_paths = []

    print(f"\nImage {image_id}: {prompt_data['context']}")
    print(f"Génération de {num_variations} variation(s)...")

    # Générer toutes les variations d'un coup
    image_bytes_list = api_client.generate_image(
        prompt=prompt_data['prompt'],
        negative_prompt=prompt_data.get('negative_prompt', ''),
        number_of_images=num_variations,
        model=model
    )

    if image_bytes_list:
        for variation, image_data in enumerate(image_bytes_list, 1):
            # Sauvegarder l'image
            filename = f"image_{image_id:03d}_var_{variation}.png"
            filepath = output_dir / filename

            with open(filepath, 'wb') as f:
                f.write(image_data)

            generated_paths.append(filepath)
            print(f"  Sauvegardée : {filename}")
    else:
        print(f"  Échec de la génération")

    return generated_paths


def main():
    parser = argparse.ArgumentParser(
        description="Génère des images via l'API Nano Banana (Google Imagen)"
    )

    parser.add_argument(
        "--prompt_file", "-p",
        required=True,
        help="Fichier JSON contenant les prompts"
    )

    parser.add_argument(
        "--output_dir", "-o",
        required=True,
        help="Répertoire de sortie pour les images"
    )

    parser.add_argument(
        "--num_variations", "-n",
        type=int,
        default=2,
        help="Nombre de variations par prompt (défaut: 2)"
    )

    parser.add_argument(
        "--model",
        default="imagen-4.0-fast",
        choices=["imagen-4.0-fast", "imagen-4.0-standard", "imagen-4.0-ultra"],
        help="Modèle Imagen à utiliser (défaut: imagen-4.0-fast)"
    )

    args = parser.parse_args()

    # Charger le fichier de prompts
    prompt_file = Path(args.prompt_file)
    if not prompt_file.exists():
        print(f"ERREUR: Fichier de prompts introuvable : {args.prompt_file}")
        sys.exit(1)

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompts_data = json.load(f)

    # Créer le répertoire de sortie
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Initialiser le client API
    api_client = NanoBananaAPI()

    # Générer les images
    print(f"\n{'='*60}")
    print(f"GÉNÉRATION D'IMAGES - Nano Banana API (Google Imagen)")
    print(f"{'='*60}")
    print(f"Fichier de prompts : {args.prompt_file}")
    print(f"Répertoire de sortie : {args.output_dir}")
    print(f"Nombre d'images : {prompts_data['metadata']['num_images']}")
    print(f"Variations par image : {args.num_variations}")
    print(f"Modèle : {args.model}")
    print(f"Style : {prompts_data['metadata']['style']}")
    print(f"Thème : {prompts_data['metadata']['theme']}")
    print(f"{'='*60}\n")

    all_generated = []
    success_count = 0
    total_count = prompts_data['metadata']['num_images']

    for prompt_data in prompts_data['prompts']:
        image_id = prompt_data['id']

        paths = generate_variations(
            api_client,
            prompt_data,
            args.num_variations,
            output_dir,
            image_id,
            args.model
        )

        all_generated.extend(paths)

        if paths:
            success_count += 1

        # Petite pause entre les groupes d'images pour éviter le rate limiting
        if image_id < total_count:
            time.sleep(1)

    # Résumé
    print(f"\n{'='*60}")
    print(f"RÉSUMÉ")
    print(f"{'='*60}")
    print(f"Images générées avec succès : {success_count}/{total_count}")
    print(f"Fichiers créés : {len(all_generated)}")
    print(f"Répertoire : {output_dir}")
    print(f"{'='*60}\n")

    # Sauvegarder un fichier de métadonnées
    metadata = {
        "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "prompt_file": str(prompt_file),
        "num_variations": args.num_variations,
        "model": args.model,
        "api": "nanobanana",
        "success_count": success_count,
        "total_count": total_count,
        "generated_files": [str(p) for p in all_generated],
        "style": prompts_data['metadata']['style'],
        "theme": prompts_data['metadata']['theme']
    }

    metadata_file = output_dir / "generation_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Métadonnées sauvegardées : {metadata_file}\n")

    if success_count < total_count:
        print("Certaines images n'ont pas pu être générées.")
        print("   Vérifiez les messages d'erreur ci-dessus.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
