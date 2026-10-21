#!/usr/bin/env python3
"""
Diff visuel page-à-page entre deux dossiers de captures PNG.

Pour chaque paire de pages (alignées par index) :
    - pixels sombres présents AVANT et APRÈS : gris clair (inchangé)
    - pixels sombres présents UNIQUEMENT APRÈS : rouge (ajouté par les optimisations)
    - pixels sombres présents UNIQUEMENT AVANT : bleu (supprimé)
    - pixels clairs (fond) : blanc

Si l'un des dossiers a plus de pages que l'autre :
    - pages présentes seulement dans AVANT  → page entière teintée bleue (« PAGE SUPPRIMÉE »)
    - pages présentes seulement dans APRÈS  → page entière teintée rouge (« PAGE AJOUTÉE »)

Usage:
    python diff_pages.py --before <dir_v0_captures> --after <dir_v4_captures> --output <dir_diff>
                         [--threshold 200] [--strict]

Options:
    --threshold N : luminance < N est considérée comme « contenu » (défaut : 200)
    --strict      : ne tolère aucun pixel de décalage entre les deux images (sinon, redim automatique)

Sortie:
    <dir_diff>/diff_001.png ... diff_NNN.png
    summary.json avec statistiques par page
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont


DARK_THRESHOLD_DEFAULT = 200  # < 200 = pixel "encré"


def load_gray(path: Path) -> np.ndarray:
    """Charge une image en niveaux de gris (uint8)."""
    return np.array(Image.open(path).convert("L"))


def align_shapes(a: np.ndarray, b: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Si tailles différentes, redimensionne A sur la taille de B (Lanczos)."""
    if a.shape == b.shape:
        return a, b
    target = (b.shape[1], b.shape[0])  # (width, height)
    a_resized = np.array(Image.fromarray(a).resize(target, Image.LANCZOS))
    return a_resized, b


def diff_pair(before: np.ndarray, after: np.ndarray, threshold: int) -> tuple[Image.Image, dict]:
    """Construit l'image de diff + stats.

    Renvoie (image RGB, stats dict).
    """
    a_dark = before < threshold
    b_dark = after < threshold

    same = a_dark & b_dark
    added = b_dark & ~a_dark
    removed = a_dark & ~b_dark

    h, w = after.shape
    rgb = np.full((h, w, 3), 255, dtype=np.uint8)  # fond blanc

    # Gris clair pour pixels inchangés (intensité ~ pixel d'origine, atténuée)
    # On garde la nuance d'origine du PDF "après" pour le contenu inchangé.
    gray_value = np.where(same, after, 255)  # garder l'intensité d'origine sinon blanc
    # Appliquer gray_value sur les 3 canaux (fond blanc + gris où same)
    same_mask3 = np.stack([same, same, same], axis=-1)
    rgb_same = np.stack([gray_value, gray_value, gray_value], axis=-1)
    rgb = np.where(same_mask3, rgb_same, rgb)

    # Rouge pour pixels ajoutés (apparu en v_après)
    rgb[added] = [220, 30, 30]

    # Bleu pour pixels supprimés (étaient en v_avant)
    rgb[removed] = [30, 60, 220]

    stats = {
        "pixels_total": int(h * w),
        "pixels_same": int(same.sum()),
        "pixels_added": int(added.sum()),
        "pixels_removed": int(removed.sum()),
        "ratio_added": round(float(added.sum()) / (h * w), 5),
        "ratio_removed": round(float(removed.sum()) / (h * w), 5),
        "ratio_changed": round(float((added.sum() + removed.sum())) / (h * w), 5),
    }
    return Image.fromarray(rgb), stats


def label_full_page(source_path: Path, color: tuple[int, int, int], text: str) -> Image.Image:
    """Crée une image en teintant la page d'origine avec la couleur indiquée."""
    src = Image.open(source_path).convert("L")
    arr = np.array(src)
    h, w = arr.shape
    # Inverser pour avoir un masque sur le contenu
    dark = arr < DARK_THRESHOLD_DEFAULT
    rgb = np.full((h, w, 3), 255, dtype=np.uint8)
    rgb[dark] = color
    img = Image.fromarray(rgb)
    # Apposer un label centré
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except (OSError, IOError):
        font = ImageFont.load_default()
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    except AttributeError:
        tw, th = font.getsize(text)
    draw.rectangle([(w // 2 - tw // 2 - 20, h // 2 - th // 2 - 10),
                    (w // 2 + tw // 2 + 20, h // 2 + th // 2 + 10)],
                   fill=(255, 255, 255), outline=color, width=3)
    draw.text((w // 2 - tw // 2, h // 2 - th // 2), text, fill=color, font=font)
    return img


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diff visuel page-à-page entre deux dossiers de captures PNG."
    )
    parser.add_argument("--before", required=True, help="Dossier des PNG avant (v0)")
    parser.add_argument("--after", required=True, help="Dossier des PNG après (vN)")
    parser.add_argument("--output", required=True, help="Dossier de sortie pour les diffs")
    parser.add_argument(
        "--threshold",
        type=int,
        default=DARK_THRESHOLD_DEFAULT,
        help=f"Seuil de noirceur (défaut : {DARK_THRESHOLD_DEFAULT})",
    )
    args = parser.parse_args()

    before_dir = Path(args.before)
    after_dir = Path(args.after)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    files_before = sorted(before_dir.glob("page_*.png"))
    files_after = sorted(after_dir.glob("page_*.png"))

    if not files_before or not files_after:
        print(json.dumps({"status": "error", "message": "Aucun PNG trouvé dans l'un des dossiers"}), file=sys.stderr)
        return 1

    n_b = len(files_before)
    n_a = len(files_after)
    n_max = max(n_b, n_a)
    per_page_stats = []

    for i in range(n_max):
        out_file = out_dir / f"diff_{i + 1:03d}.png"
        if i < n_b and i < n_a:
            arr_b = load_gray(files_before[i])
            arr_a = load_gray(files_after[i])
            arr_b, arr_a = align_shapes(arr_b, arr_a)
            img, stats = diff_pair(arr_b, arr_a, args.threshold)
            stats["page"] = i + 1
            stats["status"] = "compared"
        elif i < n_b:
            img = label_full_page(files_before[i], (30, 60, 220), f"PAGE {i+1} SUPPRIMEE")
            stats = {"page": i + 1, "status": "removed_only_in_before"}
        else:
            img = label_full_page(files_after[i], (220, 30, 30), f"PAGE {i+1} AJOUTEE")
            stats = {"page": i + 1, "status": "added_only_in_after"}
        img.save(out_file)
        per_page_stats.append(stats)

    summary = {
        "status": "ok",
        "before_pages": n_b,
        "after_pages": n_a,
        "diff_pages": n_max,
        "output_dir": str(out_dir.resolve()),
        "pages": per_page_stats,
    }
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
