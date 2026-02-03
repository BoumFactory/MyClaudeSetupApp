#!/usr/bin/env python3
"""
Script de comparaison et s\u00e9lection des meilleures images.
Analyse les variations g\u00e9n\u00e9r\u00e9es et aide \u00e0 choisir les meilleures.
"""

import json
import os
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("\u274c ERREUR: Biblioth\u00e8ques manquantes")
    print("   Installez avec: pip install Pillow numpy")
    sys.exit(1)


def analyze_image_colors(image_path: Path) -> Dict:
    """
    Analyse les couleurs d'une image.

    Args:
        image_path: Chemin vers l'image

    Returns:
        Dict avec statistiques couleurs
    """
    img = Image.open(image_path)
    img_array = np.array(img)

    # Convertir en RGB si n\u00e9cessaire
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = img_array[:, :, :3]

    # Calculer le nombre de couleurs uniques
    pixels = img_array.reshape(-1, img_array.shape[-1])
    unique_colors = len(np.unique(pixels, axis=0))

    # Calculer la proportion de blanc (pour les fonds)
    white_threshold = 240
    white_pixels = np.all(img_array >= white_threshold, axis=-1)
    white_ratio = np.sum(white_pixels) / white_pixels.size

    # Calculer le contraste moyen
    grayscale = np.mean(img_array, axis=-1)
    contrast = np.std(grayscale)

    return {
        "unique_colors": unique_colors,
        "white_ratio": white_ratio,
        "contrast": contrast
    }


def score_image(
    image_path: Path,
    criteria: List[str],
    color_stats: Dict
) -> float:
    """
    Calcule un score pour une image selon les crit\u00e8res.

    Args:
        image_path: Chemin vers l'image
        criteria: Liste des crit\u00e8res
        color_stats: Statistiques couleurs de l'image

    Returns:
        Score entre 0 et 1
    """
    scores = []

    if "printability" in criteria:
        # Meilleur score = peu de couleurs + fond blanc + bon contraste
        color_score = max(0, 1 - (color_stats["unique_colors"] / 10000))
        white_score = color_stats["white_ratio"]
        contrast_score = min(1, color_stats["contrast"] / 100)

        printability = (color_score * 0.4 + white_score * 0.3 + contrast_score * 0.3)
        scores.append(printability)

    if "clarity" in criteria:
        # Meilleur score = bon contraste
        clarity = min(1, color_stats["contrast"] / 100)
        scores.append(clarity)

    if "simplicity" in criteria:
        # Meilleur score = peu de couleurs
        simplicity = max(0, 1 - (color_stats["unique_colors"] / 5000))
        scores.append(simplicity)

    # Score moyen
    return sum(scores) / len(scores) if scores else 0.5


def group_variations(image_dir: Path) -> Dict[int, List[Path]]:
    """
    Groupe les images par ID (variations du m\u00eame prompt).

    Args:
        image_dir: R\u00e9pertoire contenant les images

    Returns:
        Dict {image_id: [paths]}
    """
    groups = defaultdict(list)

    for image_file in sorted(image_dir.glob("image_*.png")):
        # Extraire l'ID de l'image depuis le nom de fichier
        # Format: image_001_var_1.png
        parts = image_file.stem.split("_")
        if len(parts) >= 2:
            try:
                image_id = int(parts[1])
                groups[image_id].append(image_file)
            except ValueError:
                continue

    return dict(groups)


def display_comparison(
    image_id: int,
    variations: List[Tuple[Path, float, Dict]]
) -> None:
    """
    Affiche une comparaison des variations.

    Args:
        image_id: ID de l'image
        variations: Liste de (path, score, stats)
    """
    print(f"\n{'='*60}")
    print(f"Image {image_id} - {len(variations)} variation(s)")
    print(f"{'='*60}")

    for i, (path, score, stats) in enumerate(variations, 1):
        print(f"\n  Variation {i}: {path.name}")
        print(f"    Score: {score:.3f}")
        print(f"    Couleurs uniques: {stats['unique_colors']}")
        print(f"    Fond blanc: {stats['white_ratio']:.1%}")
        print(f"    Contraste: {stats['contrast']:.1f}")


def interactive_selection(
    image_id: int,
    variations: List[Tuple[Path, float, Dict]]
) -> int:
    """
    Permet \u00e0 l'utilisateur de s\u00e9lectionner la meilleure variation.

    Args:
        image_id: ID de l'image
        variations: Liste de (path, score, stats)

    Returns:
        Index de la variation s\u00e9lectionn\u00e9e (0-based)
    """
    # Trouver l'index du meilleur score
    best_idx = max(range(len(variations)), key=lambda i: variations[i][1])

    print(f"\n  Recommandation: Variation {best_idx + 1} (meilleur score)")
    print(f"\n  Options:")
    print(f"    1-{len(variations)}: Choisir une variation sp\u00e9cifique")
    print(f"    A: Accepter la recommandation")
    print(f"    K: Garder toutes les variations")

    while True:
        choice = input(f"\n  Votre choix pour l'image {image_id}: ").strip().upper()

        if choice == "A":
            return best_idx
        elif choice == "K":
            return -1  # Code sp\u00e9cial pour garder tout
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(variations):
                    return idx
                else:
                    print(f"  \u274c Veuillez entrer un nombre entre 1 et {len(variations)}")
            except ValueError:
                print(f"  \u274c Entr\u00e9e invalide")


def cleanup_unselected(
    variations: List[Tuple[Path, float, Dict]],
    selected_idx: int
) -> None:
    """
    Supprime les variations non s\u00e9lectionn\u00e9es.

    Args:
        variations: Liste de (path, score, stats)
        selected_idx: Index de la variation \u00e0 garder
    """
    for i, (path, _, _) in enumerate(variations):
        if i != selected_idx:
            try:
                path.unlink()
                print(f"  \u2717 Supprim\u00e9: {path.name}")
            except Exception as e:
                print(f"  \u274c Erreur lors de la suppression de {path.name}: {e}")


def rename_selected(selected_path: Path, image_id: int) -> Path:
    """
    Renomme l'image s\u00e9lectionn\u00e9e pour retirer le suffixe de variation.

    Args:
        selected_path: Chemin de l'image s\u00e9lectionn\u00e9e
        image_id: ID de l'image

    Returns:
        Nouveau chemin
    """
    new_name = f"image_{image_id:03d}.png"
    new_path = selected_path.parent / new_name

    try:
        selected_path.rename(new_path)
        print(f"  \u2713 Renomm\u00e9 en: {new_name}")
        return new_path
    except Exception as e:
        print(f"  \u274c Erreur lors du renommage: {e}")
        return selected_path


def main():
    parser = argparse.ArgumentParser(
        description="Compare et s\u00e9lectionne les meilleures images"
    )

    parser.add_argument(
        "--input_dir", "-i",
        required=True,
        help="R\u00e9pertoire contenant les images g\u00e9n\u00e9r\u00e9es"
    )

    parser.add_argument(
        "--selection_criteria", "-c",
        default="printability,clarity,simplicity",
        help="Crit\u00e8res de s\u00e9lection s\u00e9par\u00e9s par des virgules"
    )

    parser.add_argument(
        "--auto", "-a",
        action="store_true",
        help="S\u00e9lection automatique (sans interaction)"
    )

    parser.add_argument(
        "--keep_all",
        action="store_true",
        help="Garder toutes les variations (pas de suppression)"
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    if not input_dir.exists():
        print(f"\u274c ERREUR: R\u00e9pertoire introuvable : {args.input_dir}")
        sys.exit(1)

    criteria = [c.strip() for c in args.selection_criteria.split(",")]

    print(f"\n{'='*60}")
    print(f"COMPARAISON ET S\u00c9LECTION D'IMAGES")
    print(f"{'='*60}")
    print(f"R\u00e9pertoire : {args.input_dir}")
    print(f"Crit\u00e8res : {', '.join(criteria)}")
    print(f"Mode : {'Automatique' if args.auto else 'Interactif'}")
    print(f"{'='*60}\n")

    # Grouper les variations
    groups = group_variations(input_dir)

    if not groups:
        print("\u274c Aucune image trouv\u00e9e dans le r\u00e9pertoire")
        sys.exit(1)

    print(f"Trouv\u00e9 {len(groups)} groupe(s) d'images\n")

    # Analyser et s\u00e9lectionner
    selections = {}

    for image_id in sorted(groups.keys()):
        paths = groups[image_id]

        # Analyser chaque variation
        variations = []
        for path in paths:
            stats = analyze_image_colors(path)
            score = score_image(path, criteria, stats)
            variations.append((path, score, stats))

        # Trier par score d\u00e9croissant
        variations.sort(key=lambda x: x[1], reverse=True)

        # Afficher la comparaison
        display_comparison(image_id, variations)

        # S\u00e9lection
        if args.keep_all:
            print(f"\n  \u2713 Toutes les variations conserv\u00e9es")
            selected_idx = -1
        elif args.auto or len(variations) == 1:
            selected_idx = 0
            print(f"\n  \u2713 S\u00e9lection automatique: Variation 1 (score: {variations[0][1]:.3f})")
        else:
            selected_idx = interactive_selection(image_id, variations)

        selections[image_id] = {
            "selected_idx": selected_idx,
            "variations": variations
        }

    # Confirmation avant nettoyage
    if not args.keep_all and not args.auto:
        print(f"\n{'='*60}")
        print(f"CONFIRMATION")
        print(f"{'='*60}")
        confirm = input("\nSupprimer les variations non s\u00e9lectionn\u00e9es ? (o/N): ").strip().lower()

        if confirm != 'o':
            print("\n\u274c Op\u00e9ration annul\u00e9e. Toutes les images conserv\u00e9es.")
            return

    # Nettoyer et renommer
    if not args.keep_all:
        print(f"\n{'='*60}")
        print(f"NETTOYAGE")
        print(f"{'='*60}\n")

        for image_id, selection_data in selections.items():
            selected_idx = selection_data["selected_idx"]

            if selected_idx == -1:
                continue

            variations = selection_data["variations"]

            print(f"Image {image_id}:")

            # Supprimer les non-s\u00e9lectionn\u00e9es
            cleanup_unselected(variations, selected_idx)

            # Renommer la s\u00e9lectionn\u00e9e
            selected_path = variations[selected_idx][0]
            rename_selected(selected_path, image_id)

    print(f"\n{'='*60}")
    print(f"\u2713 Traitement termin\u00e9")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
