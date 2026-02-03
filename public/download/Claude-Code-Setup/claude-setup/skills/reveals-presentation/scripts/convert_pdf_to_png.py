#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script généralisé pour convertir des fichiers PDF en PNG.

Usage:
    python convert_pdf_to_png.py <dossier_ou_fichier> [--dpi <resolution>] [--pattern <glob>]

Arguments:
    dossier_ou_fichier : Dossier contenant les PDF ou fichier PDF unique
    --dpi : Résolution DPI pour les PNG (défaut: 300)
    --pattern : Pattern glob pour filtrer les fichiers (défaut: *.pdf)
"""

import os
import subprocess
import glob
import argparse
import sys
from pathlib import Path

def convert_pdf_to_png(pdf_file, png_file, dpi=300):
    """
    Convertit un fichier PDF en PNG avec plusieurs méthodes de fallback.

    Args:
        pdf_file: Chemin vers le fichier PDF source
        png_file: Chemin vers le fichier PNG de sortie
        dpi: Résolution DPI (défaut: 300)

    Returns:
        (success, method_name): Tuple avec succès et nom de la méthode utilisée
    """
    converters = [
        # Méthode 1: pdftoppm (souvent la plus fiable sur Windows)
        (
            ["pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf_file, png_file.replace(".png", "")],
            "pdftoppm"
        ),
        # Méthode 2: Ghostscript 64-bit
        (
            ["gswin64c", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", f"-r{dpi}", f"-sOutputFile={png_file}", pdf_file],
            "Ghostscript 64-bit"
        ),
        # Méthode 3: Ghostscript 32-bit
        (
            ["gswin32c", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", f"-r{dpi}", f"-sOutputFile={png_file}", pdf_file],
            "Ghostscript 32-bit"
        ),
        # Méthode 4: ImageMagick (magick)
        (
            ["magick", "-density", str(dpi), pdf_file, "-quality", "100", png_file],
            "ImageMagick (magick)"
        ),
        # Méthode 5: ImageMagick (convert)
        (
            ["convert", "-density", str(dpi), pdf_file, "-quality", "100", png_file],
            "ImageMagick (convert)"
        ),
    ]

    for cmd, method_name in converters:
        try:
            subprocess.run(
                cmd,
                check=True,
                timeout=30,
                capture_output=True,
                text=True
            )
            return True, method_name
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            continue

    return False, "Aucune méthode de conversion disponible"

def main():
    parser = argparse.ArgumentParser(
        description="Convertit des fichiers PDF en PNG avec haute résolution"
    )
    parser.add_argument(
        "path",
        help="Dossier contenant les PDF ou fichier PDF unique"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Résolution DPI pour les PNG (défaut: 300)"
    )
    parser.add_argument(
        "--pattern",
        default="*.pdf",
        help="Pattern glob pour filtrer les fichiers dans un dossier (défaut: *.pdf)"
    )
    parser.add_argument(
        "--output-dir",
        help="Dossier de sortie (défaut: même dossier que le PDF source)"
    )

    args = parser.parse_args()

    # Déterminer si c'est un fichier ou un dossier
    input_path = Path(args.path)

    if not input_path.exists():
        print(f"ERREUR: Le chemin {args.path} n'existe pas")
        sys.exit(1)

    # Collecter les fichiers PDF à traiter
    if input_path.is_file():
        if input_path.suffix.lower() != '.pdf':
            print(f"ERREUR: {args.path} n'est pas un fichier PDF")
            sys.exit(1)
        pdf_files = [input_path]
        work_dir = input_path.parent
    else:
        # C'est un dossier
        work_dir = input_path
        pattern_path = work_dir / args.pattern
        pdf_files = sorted(work_dir.glob(args.pattern))

    if not pdf_files:
        print(f"Aucun fichier PDF trouvé avec le pattern '{args.pattern}' dans {work_dir}")
        sys.exit(0)

    # Déterminer le dossier de sortie
    if args.output_dir:
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = work_dir

    print(f"Conversion de {len(pdf_files)} fichier(s) PDF...")
    print(f"  Résolution: {args.dpi} DPI")
    print(f"  Dossier de sortie: {output_dir.absolute()}\n")

    # Traiter chaque fichier
    success_count = 0
    error_count = 0
    methods_used = {}

    for i, pdf_file in enumerate(pdf_files, 1):
        png_file = output_dir / pdf_file.name.replace(".pdf", ".png")

        print(f"[{i}/{len(pdf_files)}] {pdf_file.name}...")

        success, method = convert_pdf_to_png(str(pdf_file), str(png_file), args.dpi)

        if success:
            file_size = png_file.stat().st_size / 1024
            print(f"  ✓ Conversion réussie ({method}, {file_size:.1f} KB)")
            success_count += 1

            # Compter les méthodes utilisées
            methods_used[method] = methods_used.get(method, 0) + 1
        else:
            print(f"  ✗ Échec: {method}")
            error_count += 1

    # Résumé
    print("\n" + "=" * 60)
    print("Conversion terminée !")
    print(f"  ✓ {success_count} fichier(s) converti(s)")
    if error_count > 0:
        print(f"  ✗ {error_count} erreur(s)")

    if methods_used:
        print("\n  Méthodes utilisées:")
        for method, count in methods_used.items():
            print(f"    - {method}: {count} fichier(s)")

    print(f"\n  → PNG dans: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
