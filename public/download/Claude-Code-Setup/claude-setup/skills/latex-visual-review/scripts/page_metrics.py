#!/usr/bin/env python3
"""
Extraction de métriques objectives par page d'un PDF, pour diagnostiquer la
qualité de disposition (densité, blancs perdus, déséquilibres haut/bas).

Usage:
    python page_metrics.py --pdf <chemin.pdf> [--json <fichier>] [--dpi 100]

Métriques par page (clé `pages`, liste d'objets) :
    - index            : numéro de page (1-based)
    - text_length      : longueur du texte extrait (caractères)
    - blocks           : nombre de blocs de texte détectés
    - fill_ratio       : ratio global de pixels non blancs (densité visuelle)
    - top_fill         : ratio sur la bande supérieure (0-15% de la hauteur)
    - bottom_fill      : ratio sur la bande inférieure (85-100% de la hauteur)
    - bottom_half_fill : ratio sur la moitié basse (50-100%)
    - widow_hint       : True si la bande haute (15-25%) est isolée (texte minuscule)
    - orphan_hint      : True si seule la dernière bande (75-85%) contient du texte
    - is_sparse        : True si fill_ratio < 0.10
    - is_dense         : True si fill_ratio > 0.55

Métriques globales (racine du JSON) :
    - pages_total
    - fill_mean, fill_std
    - last_page_fill_ratio       : utile pour détecter dernière page quasi vide
    - last_page_bottom_half_fill : encore plus discriminant
    - empty_pages_count          : pages avec fill_ratio < 0.05
    - sparse_tail                : True si la dernière page a fill_ratio < 0.20
    - density_imbalance          : écart-type relatif (std/mean), > 0.4 = mise en page hétérogène
    - low_dpi_images             : liste des images raster (PNG/JPEG) imprimées sous le
                                    seuil --dpi-threshold à leur taille finale (cf. D7 dans
                                    references/figures-et-defauts.md). Calculé directement depuis les
                                    images embarquées dans le PDF (taille pixel native vs boîte
                                    de placement réelle sur la page) : ne détecte QUE le raster,
                                    les figures vectorielles (TikZ, PDF, EPS) ne sont jamais des
                                    "images" au sens PDF et ne sont donc jamais signalées.
    - low_dpi_images_count       : nombre d'occurrences dans low_dpi_images

Sortie : JSON sur stdout, ou écrit dans --json si fourni.

Notes :
    - Le rendu pour métriques se fait en GRAY (1 octet/pixel) pour gagner du temps.
    - Le DPI par défaut est 100 (suffisant pour des métriques de remplissage).
    - numpy est utilisé si disponible, sinon fallback Python pur sur memoryview.
"""
import argparse
import json
import math
import sys
from pathlib import Path

import fitz  # PyMuPDF

try:
    import numpy as np

    HAS_NUMPY = True
except ImportError:  # pragma: no cover
    HAS_NUMPY = False


WHITE_THRESHOLD = 240  # pixels avec luminance >= 240 considérés blancs


def fill_ratio_gray(pix: "fitz.Pixmap", threshold: int = WHITE_THRESHOLD) -> float:
    """Ratio global de pixels non blancs sur un pixmap GRAY."""
    n = pix.width * pix.height
    if n == 0:
        return 0.0
    data = pix.samples  # bytes, 1 octet/pixel en GRAY
    if HAS_NUMPY:
        arr = np.frombuffer(data, dtype=np.uint8)
        return float((arr < threshold).mean())
    # Fallback Python pur
    return sum(1 for b in data if b < threshold) / n


def band_fill_gray(
    pix: "fitz.Pixmap", y_start: float, y_end: float, threshold: int = WHITE_THRESHOLD
) -> float:
    """Ratio de pixels non blancs sur une bande horizontale [y_start, y_end] (ratios 0-1)."""
    h, w = pix.height, pix.width
    rs = max(0, int(h * y_start))
    re = min(h, int(h * y_end))
    if re <= rs or w == 0:
        return 0.0
    data = pix.samples
    if HAS_NUMPY:
        arr = np.frombuffer(data, dtype=np.uint8).reshape((h, w))
        band = arr[rs:re]
        return float((band < threshold).mean())
    # Fallback Python pur
    total = (re - rs) * w
    non_white = 0
    for row in range(rs, re):
        base = row * w
        chunk = data[base : base + w]
        non_white += sum(1 for b in chunk if b < threshold)
    return non_white / total if total else 0.0


def measure_page(page: "fitz.Page", dpi: int) -> dict:
    """Calcule toutes les métriques d'une page."""
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=matrix, colorspace=fitz.csGRAY, alpha=False)

    fill = fill_ratio_gray(pix)
    top_fill = band_fill_gray(pix, 0.00, 0.15)
    bottom_fill = band_fill_gray(pix, 0.85, 1.00)
    bottom_half_fill = band_fill_gray(pix, 0.50, 1.00)
    upper_band = band_fill_gray(pix, 0.15, 0.25)
    lower_band = band_fill_gray(pix, 0.75, 0.85)

    text = page.get_text() or ""
    blocks = page.get_text("blocks") or []

    # Heuristiques widow/orphan : présence isolée de texte dans une seule bande
    widow_hint = upper_band > 0.02 and bottom_half_fill < 0.05
    orphan_hint = lower_band > 0.02 and band_fill_gray(pix, 0.00, 0.75) < 0.05

    return {
        "index": page.number + 1,
        "text_length": len(text),
        "blocks": len(blocks),
        "fill_ratio": round(fill, 4),
        "top_fill": round(top_fill, 4),
        "bottom_fill": round(bottom_fill, 4),
        "bottom_half_fill": round(bottom_half_fill, 4),
        "widow_hint": bool(widow_hint),
        "orphan_hint": bool(orphan_hint),
        "is_sparse": bool(fill < 0.10),
        "is_dense": bool(fill > 0.55),
    }


def detect_low_dpi_images(doc: "fitz.Document", threshold: float) -> list:
    """Repère les images raster (PNG/JPEG) imprimées sous `threshold` dpi.

    Pour chaque image embarquée dans le PDF, compare sa résolution pixel native
    à la taille de sa boîte de placement réelle sur la page (en points) pour en
    déduire le dpi effectif à l'impression. Les figures vectorielles (TikZ, PDF,
    EPS) ne sont pas des "images" au sens PDF (ce sont des opérateurs de dessin)
    et ne sont donc jamais candidates ici — seul le raster est concerné.
    """
    findings = []
    for page_index in range(doc.page_count):
        page = doc.load_page(page_index)
        for img in page.get_images(full=True):
            xref = img[0]
            try:
                base = doc.extract_image(xref)
            except Exception:  # pragma: no cover
                continue
            px_w, px_h = base.get("width", 0), base.get("height", 0)
            if not px_w or not px_h:
                continue
            try:
                rects = page.get_image_rects(xref)
            except Exception:  # pragma: no cover
                rects = []
            for rect in rects:
                width_in = rect.width / 72.0
                height_in = rect.height / 72.0
                if width_in <= 0 or height_in <= 0:
                    continue
                dpi_effective = min(px_w / width_in, px_h / height_in)
                if dpi_effective < threshold:
                    findings.append(
                        {
                            "page": page_index + 1,
                            "xref": xref,
                            "pixel_size": [px_w, px_h],
                            "printed_size_cm": [
                                round(rect.width / 28.3465, 2),
                                round(rect.height / 28.3465, 2),
                            ],
                            "dpi_effective": round(dpi_effective, 1),
                        }
                    )
    return findings


def aggregate(pages: list) -> dict:
    """Calcule les métriques globales à partir des métriques par page."""
    n = len(pages)
    if n == 0:
        return {
            "pages_total": 0,
            "fill_mean": 0.0,
            "fill_std": 0.0,
            "last_page_fill_ratio": 0.0,
            "last_page_bottom_half_fill": 0.0,
            "empty_pages_count": 0,
            "sparse_tail": False,
            "density_imbalance": 0.0,
        }
    fills = [p["fill_ratio"] for p in pages]
    mean = sum(fills) / n
    var = sum((f - mean) ** 2 for f in fills) / n
    std = math.sqrt(var)
    last = pages[-1]
    return {
        "pages_total": n,
        "fill_mean": round(mean, 4),
        "fill_std": round(std, 4),
        "last_page_fill_ratio": last["fill_ratio"],
        "last_page_bottom_half_fill": last["bottom_half_fill"],
        "empty_pages_count": sum(1 for f in fills if f < 0.05),
        "sparse_tail": bool(last["fill_ratio"] < 0.20),
        "density_imbalance": round(std / mean, 4) if mean > 0 else 0.0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extrait des métriques de mise en page d'un PDF (densité, blancs perdus, déséquilibres)."
    )
    parser.add_argument("--pdf", required=True, help="Chemin du PDF source")
    parser.add_argument(
        "--json",
        default=None,
        help="Fichier de sortie JSON (sinon, JSON sur stdout)",
    )
    parser.add_argument("--dpi", type=int, default=100, help="Résolution pour les métriques (défaut : 100)")
    parser.add_argument(
        "--dpi-threshold",
        type=float,
        default=150.0,
        help="Seuil d'alerte dpi effectif pour les images raster imprimées (défaut : 150)",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    if not pdf_path.is_file():
        print(
            json.dumps({"status": "error", "message": f"PDF introuvable : {pdf_path}"}),
            file=sys.stderr,
        )
        return 1

    try:
        doc = fitz.open(str(pdf_path))
    except Exception as exc:
        print(
            json.dumps({"status": "error", "message": f"PDF illisible : {exc}"}),
            file=sys.stderr,
        )
        return 1

    pages_metrics = [measure_page(doc.load_page(i), args.dpi) for i in range(doc.page_count)]
    low_dpi_images = detect_low_dpi_images(doc, args.dpi_threshold)
    doc.close()

    result = {
        "status": "ok",
        "pdf": str(pdf_path),
        "dpi": args.dpi,
        "numpy_available": HAS_NUMPY,
        **aggregate(pages_metrics),
        "low_dpi_images": low_dpi_images,
        "low_dpi_images_count": len(low_dpi_images),
        "dpi_threshold": args.dpi_threshold,
        "pages": pages_metrics,
    }

    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        Path(args.json).write_text(payload, encoding="utf-8")
        print(json.dumps({"status": "ok", "json_written": args.json}, ensure_ascii=False))
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
