#!/usr/bin/env python3
"""
Script de génération d'infographies via l'API Google Gemini 3 Pro.
Version optimisée pour les infographies éducatives riches en contenu.

Utilise le modèle gemini-3-pro-image-preview qui accepte des prompts
très détaillés avec beaucoup de contexte.
"""

import json
import os
import sys
import argparse
import time
import base64
import threading
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv
import requests

# Charger les variables d'environnement
load_dotenv()


class ProgressIndicator:
    """Indicateur de progression pendant la génération."""

    def __init__(self, message: str = "Generation en cours"):
        self.message = message
        self.running = False
        self.thread = None
        self.start_time = None
        self.symbols = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def _run(self):
        """Boucle d'affichage du spinner."""
        idx = 0
        while self.running:
            elapsed = int(time.time() - self.start_time)
            symbol = self.symbols[idx % len(self.symbols)]
            # Afficher le temps écoulé pour que l'utilisateur sache que ça avance
            sys.stdout.write(f"\r  {symbol} {self.message}... ({elapsed}s)")
            sys.stdout.flush()
            time.sleep(0.1)
            idx += 1

    def start(self):
        """Démarre l'indicateur."""
        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self, success: bool = True):
        """Arrête l'indicateur."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        status = "OK" if success else "ERREUR"
        sys.stdout.write(f"\r  {status} {self.message} ({elapsed}s)          \n")
        sys.stdout.flush()


class GeminiInfographyAPI:
    """Client pour l'API Google Gemini 3 Pro (génération d'infographies)."""

    # IMPORTANT: Modèle exact à utiliser
    MODEL = "gemini-3-pro-image-preview"

    # Timeout pour les infographies (peut être long)
    TIMEOUT = 240  # 4 minutes

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialise le client API Gemini 3 Pro.

        Args:
            api_key: Clé API Google (si None, charge depuis .env)
        """
        self.api_key = api_key or os.getenv("NANOBANANA_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

        if not self.api_key:
            print("\nERREUR: Cle API Google non trouvee!")
            print("   Veuillez configurer NANOBANANA_API_KEY dans le fichier .env")
            print("   Exemple: NANOBANANA_API_KEY=\"votre-cle-api\"\n")
            sys.exit(1)

        print(f"API Google Gemini 3 Pro initialisee pour infographies")
        print(f"Modele: {self.MODEL}")
        print(f"Timeout: {self.TIMEOUT}s (les infographies complexes prennent du temps)")

    def generate_infography(
        self,
        prompt: str,
        context: str = "",
        style_instructions: str = "",
        timeout: Optional[int] = None
    ) -> Optional[bytes]:
        """
        Génère une infographie via l'API Google Gemini 3 Pro.

        Ce modèle est optimisé pour les prompts longs et détaillés,
        parfait pour les infographies éducatives complexes.

        Args:
            prompt: Description détaillée de l'infographie
            context: Contexte éducatif additionnel
            style_instructions: Instructions de style visuel
            timeout: Timeout personnalisé (défaut: TIMEOUT)

        Returns:
            Données de l'image en bytes, ou None si erreur
        """
        actual_timeout = timeout or self.TIMEOUT

        # Construction du prompt enrichi
        full_prompt = self._build_infography_prompt(prompt, context, style_instructions)
        print(f"  Longueur du prompt: {len(full_prompt)} caracteres")

        payload = {
            "contents": [{
                "parts": [{"text": full_prompt}]
            }],
            "generationConfig": {
                "response_modalities": ["image"]
            }
        }

        url = f"{self.base_url}/models/{self.MODEL}:generateContent?key={self.api_key}"

        # Démarrer l'indicateur de progression
        progress = ProgressIndicator(f"Gemini 3 Pro genere l'infographie (max {actual_timeout}s)")
        progress.start()

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=actual_timeout
            )
            progress.stop(success=(response.status_code == 200))

            if response.status_code == 200:
                result = response.json()

                # Extraire l'image en base64
                if "candidates" in result and len(result["candidates"]) > 0:
                    candidate = result["candidates"][0]

                    # Vérifier s'il y a un blocage de contenu
                    if "finishReason" in candidate:
                        reason = candidate["finishReason"]
                        if reason == "SAFETY":
                            print("  BLOCAGE: Contenu refuse par les filtres de securite")
                            return None
                        elif reason == "RECITATION":
                            print("  BLOCAGE: Contenu trop proche d'une source existante")
                            return None
                        elif reason != "STOP":
                            print(f"  AVERTISSEMENT: finishReason = {reason}")

                    if "content" in candidate:
                        content = candidate["content"]

                        if "parts" in content:
                            for part in content["parts"]:
                                if "inlineData" in part:
                                    inline = part["inlineData"]
                                    if "data" in inline:
                                        image_data = base64.b64decode(inline["data"])
                                        print(f"  Infographie generee avec succes!")
                                        return image_data

                # Pas d'image trouvée
                print("  AVERTISSEMENT: Pas d'image dans la reponse")
                print(f"  DEBUG: Structure de reponse:")
                self._debug_response(result)
                return None

            else:
                self._handle_error(response)
                return None

        except requests.exceptions.Timeout:
            progress.stop(success=False)
            print(f"\n  TIMEOUT: La requete a depasse {actual_timeout}s")
            print("  Cela peut signifier:")
            print("    - L'API est surchargee -> reessayer plus tard")
            print("    - Le prompt est trop complexe -> simplifier")
            print("    - Probleme reseau -> verifier connexion")
            print(f"\n  Conseil: reessayer avec --timeout {actual_timeout + 60}")
            return None

        except requests.exceptions.ConnectionError as e:
            progress.stop(success=False)
            print(f"\n  ERREUR CONNEXION: {str(e)[:100]}")
            print("  Verifiez votre connexion internet.")
            return None

        except requests.exceptions.RequestException as e:
            progress.stop(success=False)
            print(f"\n  ERREUR REQUETE: {str(e)[:200]}")
            return None

        except Exception as e:
            progress.stop(success=False)
            print(f"\n  ERREUR INATTENDUE: {type(e).__name__}: {str(e)[:200]}")
            return None

    def _handle_error(self, response):
        """Gère les erreurs HTTP de l'API."""
        print(f"\n  ERREUR HTTP {response.status_code}")

        try:
            error_data = response.json()
            if "error" in error_data:
                error = error_data["error"]
                print(f"  Message: {error.get('message', 'N/A')[:300]}")
                if "status" in error:
                    print(f"  Status: {error['status']}")
        except:
            print(f"  Corps: {response.text[:300]}")

        # Conseils spécifiques selon le code
        if response.status_code == 400:
            print("\n  Causes possibles:")
            print("    - Prompt trop long ou mal formé")
            print("    - Contenu non autorisé dans le prompt")
            print("    - Paramètres invalides")
        elif response.status_code == 401:
            print("\n  Verifiez votre cle API (NANOBANANA_API_KEY)")
        elif response.status_code == 403:
            print("\n  Acces refuse. Verifiez:")
            print("    - Quota API")
            print("    - Permissions du projet Google Cloud")
        elif response.status_code == 429:
            print("\n  Limite de requetes atteinte!")
            print("  Attendez quelques minutes avant de reessayer.")
        elif response.status_code == 500:
            print("\n  Erreur serveur Google. Reessayez plus tard.")
        elif response.status_code == 503:
            print("\n  Service temporairement indisponible.")
            print("  L'API est peut-être surchargée.")

    def _debug_response(self, result: dict, indent: int = 4):
        """Affiche la structure de la réponse pour debug."""
        def show_structure(obj, prefix=""):
            if isinstance(obj, dict):
                for key, val in obj.items():
                    if isinstance(val, (dict, list)):
                        print(f"{prefix}{key}: ({type(val).__name__})")
                        show_structure(val, prefix + "  ")
                    elif isinstance(val, str) and len(val) > 50:
                        print(f"{prefix}{key}: \"{val[:50]}...\" ({len(val)} chars)")
                    else:
                        print(f"{prefix}{key}: {val}")
            elif isinstance(obj, list):
                print(f"{prefix}[{len(obj)} items]")
                if obj:
                    show_structure(obj[0], prefix + "  ")

        show_structure(result, "    ")

    def _build_infography_prompt(
        self,
        main_prompt: str,
        context: str,
        style_instructions: str
    ) -> str:
        """
        Construit un prompt optimisé pour la génération d'infographies.

        Args:
            main_prompt: Description principale
            context: Contexte éducatif
            style_instructions: Instructions de style

        Returns:
            Prompt complet formaté
        """
        parts = []

        # Instruction de base pour infographie
        parts.append("""Generate an educational INFOGRAPHIC image. This is NOT a simple illustration - it must be a structured visual composition with:
- Multiple labeled zones/sections
- Text annotations and titles
- Arrows, connectors, and visual hierarchy
- Diagrams, schemas, or flowcharts where appropriate
- Clear visual organization of information

CRITICAL: The image must contain readable text labels and annotations.""")

        # Prompt principal
        parts.append(f"\n## Main Content\n{main_prompt}")

        # Contexte si fourni
        if context:
            parts.append(f"\n## Educational Context\n{context}")

        # Instructions de style
        if style_instructions:
            parts.append(f"\n## Visual Style\n{style_instructions}")
        else:
            # Style par défaut pour infographies éducatives
            parts.append("""
## Visual Style (Default)
- Clean, professional educational infographic style
- White or light background for clarity
- Clear visual hierarchy with numbered sections
- Sans-serif fonts for readability
- Color-coded sections with consistent palette
- Icons and symbols to reinforce concepts
- Sufficient white space between elements""")

        return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(
        description="Génère des infographies éducatives via Google Gemini 3 Pro"
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Description détaillée de l'infographie (peut être très long)"
    )

    parser.add_argument(
        "--context", "-c",
        default="",
        help="Contexte éducatif additionnel"
    )

    parser.add_argument(
        "--style", "-s",
        default="",
        help="Instructions de style visuel"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Chemin complet du fichier de sortie (ex: output/infographie.png)"
    )

    parser.add_argument(
        "--prompt-file", "-f",
        help="Fichier JSON contenant le prompt détaillé (alternative à --prompt)"
    )

    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=GeminiInfographyAPI.TIMEOUT,
        help=f"Timeout en secondes (défaut: {GeminiInfographyAPI.TIMEOUT})"
    )

    args = parser.parse_args()

    # Charger le prompt depuis un fichier si spécifié
    prompt = args.prompt
    context = args.context
    style = args.style

    if args.prompt_file:
        prompt_path = Path(args.prompt_file)
        if prompt_path.exists():
            with open(prompt_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                prompt = data.get('prompt', prompt)
                context = data.get('context', context)
                style = data.get('style', style)
            print(f"Prompt charge depuis: {args.prompt_file}")
        else:
            print(f"AVERTISSEMENT: Fichier de prompt non trouve: {args.prompt_file}")

    # Créer le répertoire de sortie si nécessaire
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Initialiser le client API
    api_client = GeminiInfographyAPI()

    # Afficher les informations
    print(f"\n{'='*60}")
    print(f"GÉNÉRATION D'INFOGRAPHIE - Gemini 3 Pro")
    print(f"{'='*60}")
    print(f"Sortie : {args.output}")
    print(f"Longueur prompt : {len(prompt)} caracteres")
    if context:
        print(f"Contexte : {len(context)} caracteres")
    if style:
        print(f"Style : {len(style)} caracteres")
    print(f"Timeout : {args.timeout}s")
    print(f"{'='*60}\n")

    # Générer l'infographie
    image_data = api_client.generate_infography(
        prompt=prompt,
        context=context,
        style_instructions=style,
        timeout=args.timeout
    )

    if image_data:
        # Sauvegarder l'image
        with open(output_path, 'wb') as f:
            f.write(image_data)

        print(f"\n{'='*60}")
        print(f"SUCCES!")
        print(f"{'='*60}")
        print(f"Infographie sauvegardee : {output_path}")
        print(f"Taille : {len(image_data) / 1024:.1f} Ko")
        print(f"{'='*60}\n")

        # Sauvegarder les métadonnées
        metadata = {
            "generation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": GeminiInfographyAPI.MODEL,
            "prompt_length": len(prompt),
            "context_length": len(context),
            "style_length": len(style),
            "output_file": str(output_path),
            "file_size_kb": len(image_data) / 1024,
            "timeout_used": args.timeout
        }

        metadata_file = output_path.with_suffix('.json')
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        print(f"Metadonnees : {metadata_file}\n")

    else:
        print(f"\n{'='*60}")
        print(f"ECHEC DE LA GENERATION")
        print(f"{'='*60}")
        print("Verifiez les messages d'erreur ci-dessus.")
        print("Suggestions:")
        print("  - Verifier la cle API")
        print("  - Simplifier le prompt si trop complexe")
        print("  - Augmenter le timeout avec --timeout 300")
        print("  - Reessayer dans quelques minutes")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
