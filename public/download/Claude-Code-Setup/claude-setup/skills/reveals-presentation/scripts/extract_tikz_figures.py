#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script généralisé pour extraire les graphiques TikZ d'un fichier LaTeX et les compiler en images PNG.

Usage:
    python extract_tikz_figures.py <fichier_tex> [--output-dir <dossier>] [--latex-template <fichier>]

Arguments:
    fichier_tex : Fichier LaTeX source contenant les codes TikZ
    --output-dir : Dossier de sortie pour les images (défaut: images_graphiques)
    --latex-template : Fichier template LaTeX personnalisé (optionnel)
"""

import re
import os
import subprocess
import sys
import argparse
from pathlib import Path

# Template LaTeX standalone par défaut avec styles TikZ complets
DEFAULT_LATEX_TEMPLATE = r"""\documentclass[tikz,border=2mm]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{decorations.markings}
\usetikzlibrary{shapes.misc}

% Définitions des commandes TikZ personnalisées
\tikzset{
    quadrillage/.style={help lines, gray!40},
    epais/.style={thick, line width=1.2pt},
    axe/.style={->, >=stealth, thick, black},
    % Points avec croix droites visibles
    point/.style={cross out, draw, minimum size=5pt, line width=0.8pt, inner sep=0pt},
    point correction/.style={cross out, draw, minimum size=5pt, line width=1.2pt, inner sep=0pt,red},
    % Segments standard
    segment/.style={thick},
    % Vecteurs avec flèches
    vecteur/.style={->, >=stealth, thick},
    % Couleurs standard pour différencier
    couleur1/.style={blue},
    couleur2/.style={red},
    couleur3/.style={green!60!black},
    prop/.style={blue!60!cyan},
    defi/.style={green!60!black},
    % Labels de points
    label point/.style={font=\normalsize},
    % Style général qui regroupe tout
    general/.style={point, segment, couleur1}
}

% Commandes personnalisées
\newcommand{\XAxe}[3]{
    \draw[->, thick] (#1-0.5,0) -- (#2+0.5,0) node[right] {$x$};
    \foreach \x in {#3} {
        \draw (\x,0.1) -- (\x,-0.1) node[below] {$\x$};
    }
}
\newcommand{\YAxe}[3]{
    \draw[->, thick] (0,#1-0.5) -- (0,#2+0.5) node[above] {$y$};
    \foreach \y in {#3} {
        \draw (0.1,\y) -- (-0.1,\y) node[left] {$\y$};
    }
}
\newcommand{\origine}{
    \fill (0,0) circle (2pt) node[below left] {O};
}
\newcommand{\pointC}[4]{
    \node[point] at (#1,#2) {};
    \node[label point,#4] at (#1,#2) {#3};
}
\newcommand{\pointCorrection}[4]{
    \node[point correction] at (#1,#2) {};
    \node[label point,#4] at (#1,#2) {#3};
}
\newcommand{\Coordonnees}[3][]{$#1(#2~;~#3)$}

\begin{document}
%TIKZ_CODE%
\end{document}
"""

def extract_tikz_from_file(tex_file_path):
    """Extrait tous les blocs TikZ d'un fichier LaTeX."""
    with open(tex_file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern pour capturer les environnements tikzpicture
    tikz_pattern = r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}'
    tikz_blocks = re.findall(tikz_pattern, content, re.DOTALL)

    return tikz_blocks

def compile_tikz_to_pdf(tikz_code, output_tex_file, latex_template):
    """Compile un code TikZ en PDF."""
    # Créer le fichier LaTeX complet
    latex_content = latex_template.replace("%TIKZ_CODE%", tikz_code)

    with open(output_tex_file, "w", encoding="utf-8") as f:
        f.write(latex_content)

    # Compiler avec lualatex
    output_dir = os.path.dirname(output_tex_file)
    try:
        result = subprocess.run(
            ["lualatex", "-interaction=nonstopmode", f"-output-directory={output_dir}", output_tex_file],
            capture_output=True,
            text=True,
            timeout=30
        )

        return result.returncode == 0, result.stderr
    except subprocess.TimeoutExpired:
        return False, "Timeout lors de la compilation"
    except Exception as e:
        return False, str(e)

def convert_pdf_to_png(pdf_file, png_file, dpi=300):
    """Convertit un PDF en PNG avec plusieurs méthodes de fallback."""
    converters = [
        # Méthode 1: ImageMagick (magick)
        (["magick", "-density", str(dpi), pdf_file, "-quality", "100", png_file], "ImageMagick (magick)"),
        # Méthode 2: ImageMagick (convert)
        (["convert", "-density", str(dpi), pdf_file, "-quality", "100", png_file], "ImageMagick (convert)"),
        # Méthode 3: pdftoppm
        (["pdftoppm", "-png", "-r", str(dpi), "-singlefile", pdf_file, png_file.replace(".png", "")], "pdftoppm"),
        # Méthode 4: Ghostscript 64-bit
        (["gswin64c", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", f"-r{dpi}", f"-sOutputFile={png_file}", pdf_file], "Ghostscript 64-bit"),
        # Méthode 5: Ghostscript 32-bit
        (["gswin32c", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", f"-r{dpi}", f"-sOutputFile={png_file}", pdf_file], "Ghostscript 32-bit"),
    ]

    for cmd, method_name in converters:
        try:
            subprocess.run(cmd, check=True, timeout=10, capture_output=True)
            return True, method_name
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue

    return False, "Aucune méthode de conversion disponible"

def main():
    parser = argparse.ArgumentParser(
        description="Extrait et compile les graphiques TikZ d'un fichier LaTeX en images PNG"
    )
    parser.add_argument("tex_file", help="Fichier LaTeX source contenant les codes TikZ")
    parser.add_argument("--output-dir", default="images_graphiques", help="Dossier de sortie pour les images")
    parser.add_argument("--latex-template", help="Fichier template LaTeX personnalisé (optionnel)")
    parser.add_argument("--prefix", default="graph", help="Préfixe pour les noms de fichiers (défaut: graph)")
    parser.add_argument("--dpi", type=int, default=300, help="Résolution DPI pour les PNG (défaut: 300)")

    args = parser.parse_args()

    # Vérifier que le fichier source existe
    tex_path = Path(args.tex_file)
    if not tex_path.exists():
        print(f"ERREUR: Le fichier {args.tex_file} n'existe pas")
        sys.exit(1)

    # Créer le dossier de sortie
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    # Charger le template LaTeX
    if args.latex_template:
        template_path = Path(args.latex_template)
        if not template_path.exists():
            print(f"ERREUR: Le fichier template {args.latex_template} n'existe pas")
            sys.exit(1)
        with open(template_path, "r", encoding="utf-8") as f:
            latex_template = f.read()
    else:
        latex_template = DEFAULT_LATEX_TEMPLATE

    # Extraire les codes TikZ
    print(f"Extraction des codes TikZ depuis {tex_path.name}...")
    tikz_blocks = extract_tikz_from_file(tex_path)
    print(f"  → {len(tikz_blocks)} graphique(s) TikZ trouvé(s)\n")

    if not tikz_blocks:
        print("Aucun graphique TikZ trouvé dans le fichier.")
        sys.exit(0)

    # Traiter chaque graphique
    success_count = 0
    error_count = 0

    for i, tikz_code in enumerate(tikz_blocks, 1):
        print(f"[{i}/{len(tikz_blocks)}] Traitement de {args.prefix}_{i:02d}...")

        # Noms de fichiers
        tex_file = output_dir / f"{args.prefix}_{i:02d}.tex"
        pdf_file = output_dir / f"{args.prefix}_{i:02d}.pdf"
        png_file = output_dir / f"{args.prefix}_{i:02d}.png"

        # Compilation LaTeX → PDF
        success, error_msg = compile_tikz_to_pdf(tikz_code, str(tex_file), latex_template)

        if not success:
            print(f"  ✗ Compilation échouée: {error_msg[:200]}")
            error_count += 1
            continue

        print(f"  ✓ Compilation PDF réussie")

        # Conversion PDF → PNG
        success, method = convert_pdf_to_png(str(pdf_file), str(png_file), args.dpi)

        if not success:
            print(f"  ✗ Conversion PNG échouée: {method}")
            error_count += 1
            continue

        print(f"  ✓ Conversion PNG réussie ({method})")

        # Afficher la taille du fichier
        file_size = png_file.stat().st_size / 1024
        print(f"    Taille: {file_size:.1f} KB\n")

        success_count += 1

    # Résumé
    print("=" * 60)
    print(f"Traitement terminé !")
    print(f"  ✓ {success_count} graphique(s) converti(s) avec succès")
    if error_count > 0:
        print(f"  ✗ {error_count} erreur(s)")
    print(f"  → Images dans: {output_dir.absolute()}")
    print("=" * 60)

if __name__ == "__main__":
    main()
