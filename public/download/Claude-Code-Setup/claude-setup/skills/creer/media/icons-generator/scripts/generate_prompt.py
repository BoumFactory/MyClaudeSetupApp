#!/usr/bin/env python3
"""
Script de g\u00e9n\u00e9ration de fichiers de prompts pour Nano Banana API.
G\u00e9n\u00e8re des prompts optimis\u00e9s selon le style et le contexte \u00e9ducatif.
"""

import json
import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional


# Styles pr\u00e9d\u00e9finis avec leurs modificateurs de prompt
STYLE_MODIFIERS = {
    "minimal_color_print": {
        "suffix": ", simple line art, minimal colors (2-3 colors max), high contrast, clean lines, white background, suitable for economical printing",
        "negative": "gradient, photorealistic, detailed textures, many colors, dark background",
        "max_colors": 3
    },
    "moderate_color_classroom": {
        "suffix": ", colorful illustration, 4-6 vibrant colors, medium detail, engaging and fun, educational style, clear and readable",
        "negative": "photorealistic, overly complex, too many details, dark or muddy colors",
        "max_colors": 6
    },
    "educational_illustration": {
        "suffix": ", clean educational diagram, didactic style, clear labels possible, maximum clarity, instructional design, simple and understandable",
        "negative": "artistic, abstract, decorative, photorealistic",
        "max_colors": 4
    },
    "flat_design": {
        "suffix": ", flat design, geometric shapes, simple composition, bold colors, modern minimalist style",
        "negative": "3D, shadows, gradients, realistic",
        "max_colors": 4
    },
    "cartoon_simple": {
        "suffix": ", simple cartoon style, friendly characters, basic shapes, approachable and fun, suitable for young students",
        "negative": "realistic, complex, detailed shading, photographic",
        "max_colors": 5
    }
}


# Th\u00e8mes pr\u00e9d\u00e9finis avec leurs modificateurs
THEME_MODIFIERS = {
    "escape_game_medieval": "medieval theme, castle elements, ancient artifacts, mysterious atmosphere",
    "escape_game_scifi": "science fiction theme, futuristic elements, space technology, modern mystery",
    "escape_game_detective": "detective investigation theme, crime scene elements, mystery solving, clues and evidence",
    "mathematics": "mathematical context, geometric elements, numbers and symbols, academic setting",
    "science_physics": "physics concepts, scientific equipment, laboratory setting, educational science",
    "science_biology": "biology concepts, nature elements, living organisms, scientific illustration",
    "history": "historical context, period-appropriate elements, educational history illustration",
    "geography": "geographical elements, maps, landscapes, world exploration",
    "literature": "literary theme, books, reading, storytelling elements",
    "adventure": "adventure theme, exploration, discovery, exciting journey",
    "neutral_educational": "neutral educational context, versatile, general learning environment"
}


def build_prompt(context: str, style: str, theme: str, custom_modifiers: Optional[str] = None) -> Dict[str, str]:
    """
    Construit un prompt complet \u00e0 partir du contexte, style et th\u00e8me.

    Args:
        context: Description de l'image souhait\u00e9e
        style: Cl\u00e9 du style dans STYLE_MODIFIERS
        theme: Cl\u00e9 du th\u00e8me dans THEME_MODIFIERS
        custom_modifiers: Modificateurs personnalis\u00e9s optionnels

    Returns:
        Dict avec 'prompt' et 'negative_prompt'
    """
    # R\u00e9cup\u00e9rer les modificateurs
    style_mod = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["minimal_color_print"])
    theme_mod = THEME_MODIFIERS.get(theme, "")

    # Construire le prompt principal
    prompt_parts = [context]

    if theme_mod:
        prompt_parts.append(theme_mod)

    prompt_parts.append(style_mod["suffix"])

    if custom_modifiers:
        prompt_parts.append(custom_modifiers)

    full_prompt = ", ".join(prompt_parts)

    return {
        "prompt": full_prompt,
        "negative_prompt": style_mod["negative"],
        "max_colors": style_mod["max_colors"]
    }


def generate_prompt_file(
    output: str,
    style: str,
    theme: str,
    num_images: int,
    contexts: List[str],
    custom_modifiers: Optional[str] = None
) -> None:
    """
    G\u00e9n\u00e8re un fichier JSON contenant tous les prompts.

    Args:
        output: Chemin du fichier de sortie
        style: Style visuel
        theme: Th\u00e8me global
        num_images: Nombre d'images \u00e0 g\u00e9n\u00e9rer
        contexts: Liste des contextes pour chaque image
        custom_modifiers: Modificateurs personnalis\u00e9s optionnels
    """
    if len(contexts) != num_images:
        print(f"ERREUR: Le nombre de contextes ({len(contexts)}) ne correspond pas au nombre d'images ({num_images})")
        sys.exit(1)

    # G\u00e9n\u00e9rer les prompts
    prompts_data = {
        "metadata": {
            "style": style,
            "theme": theme,
            "num_images": num_images,
            "custom_modifiers": custom_modifiers
        },
        "prompts": []
    }

    for i, context in enumerate(contexts, 1):
        prompt_data = build_prompt(context, style, theme, custom_modifiers)
        prompt_data["id"] = i
        prompt_data["context"] = context
        prompts_data["prompts"].append(prompt_data)

    # Cr\u00e9er le r\u00e9pertoire si n\u00e9cessaire
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # \u00c9crire le fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(prompts_data, f, indent=2, ensure_ascii=False)

    print(f"\u2713 Fichier de prompts g\u00e9n\u00e9r\u00e9 : {output}")
    print(f"  - Nombre d'images : {num_images}")
    print(f"  - Style : {style}")
    print(f"  - Th\u00e8me : {theme}")


def create_default_config() -> None:
    """Cr\u00e9e un fichier de configuration par d\u00e9faut."""
    config_dir = Path(__file__).parent.parent / "config"
    config_dir.mkdir(parents=True, exist_ok=True)

    default_config = {
        "style": "minimal_color_print",
        "theme": "neutral_educational",
        "custom_modifiers": "",
        "num_variations": 3,
        "output_format": "png",
        "resolution": {
            "width": 1024,
            "height": 1024
        }
    }

    config_path = config_dir / "default_config.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2, ensure_ascii=False)

    print(f"\u2713 Configuration par d\u00e9faut cr\u00e9\u00e9e : {config_path}")


def list_available_options() -> None:
    """Affiche les styles et th\u00e8mes disponibles."""
    print("\n=== STYLES DISPONIBLES ===")
    for style_name, style_data in STYLE_MODIFIERS.items():
        print(f"\n  {style_name}")
        print(f"    Couleurs max: {style_data['max_colors']}")
        print(f"    Modificateur: {style_data['suffix'][:80]}...")

    print("\n\n=== TH\u00c8MES DISPONIBLES ===")
    for theme_name, theme_desc in THEME_MODIFIERS.items():
        print(f"\n  {theme_name}")
        print(f"    {theme_desc}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="G\u00e9n\u00e8re des fichiers de prompts pour l'API Nano Banana"
    )

    parser.add_argument(
        "--output", "-o",
        help="Chemin du fichier de sortie (JSON)"
    )

    parser.add_argument(
        "--style", "-s",
        default="minimal_color_print",
        help="Style visuel (d\u00e9faut: minimal_color_print)"
    )

    parser.add_argument(
        "--theme", "-t",
        default="neutral_educational",
        help="Th\u00e8me global (d\u00e9faut: neutral_educational)"
    )

    parser.add_argument(
        "--num_images", "-n",
        type=int,
        help="Nombre d'images \u00e0 g\u00e9n\u00e9rer"
    )

    parser.add_argument(
        "--contexts", "-c",
        help="Contextes s\u00e9par\u00e9s par des virgules"
    )

    parser.add_argument(
        "--custom_modifiers", "-m",
        help="Modificateurs personnalis\u00e9s optionnels"
    )

    parser.add_argument(
        "--create_config",
        action="store_true",
        help="Cr\u00e9er un fichier de configuration par d\u00e9faut"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="Lister les styles et th\u00e8mes disponibles"
    )

    parser.add_argument(
        "--config",
        help="Charger des param\u00e8tres depuis un fichier de config"
    )

    args = parser.parse_args()

    # Actions sp\u00e9ciales
    if args.create_config:
        create_default_config()
        return

    if args.list:
        list_available_options()
        return

    # Charger config si sp\u00e9cifi\u00e9
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        args.style = config.get("style", args.style)
        args.theme = config.get("theme", args.theme)
        args.custom_modifiers = config.get("custom_modifiers", args.custom_modifiers)

    # Validation
    if not args.output:
        print("ERREUR: --output est requis")
        parser.print_help()
        sys.exit(1)

    if not args.num_images:
        print("ERREUR: --num_images est requis")
        parser.print_help()
        sys.exit(1)

    if not args.contexts:
        print("ERREUR: --contexts est requis")
        parser.print_help()
        sys.exit(1)

    # Parser les contextes
    contexts = [c.strip() for c in args.contexts.split(",")]

    # G\u00e9n\u00e9rer le fichier
    generate_prompt_file(
        args.output,
        args.style,
        args.theme,
        args.num_images,
        contexts,
        args.custom_modifiers
    )


if __name__ == "__main__":
    main()
