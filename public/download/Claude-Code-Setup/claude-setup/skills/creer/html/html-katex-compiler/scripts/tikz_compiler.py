#!/usr/bin/env python3
"""
Compilateur TikZ vers SVG base64 pour les cours HTML/KaTeX.

Workflow:
1. Lit un fichier figures.tikz contenant plusieurs figures nommées
2. Compile chaque figure individuellement dans un dossier temporaire
3. Convertit PDF → SVG via dvisvgm ou pdf2svg
4. Encode en base64 pour insertion inline dans le HTML

Format du fichier figures.tikz:
```
%% FIGURE: nom-de-la-figure
\begin{tikzpicture}
  ...
\end{tikzpicture}

%% FIGURE: autre-figure
\begin{tikzpicture}
  ...
\end{tikzpicture}
```
"""

import os
import re
import sys
import base64
import tempfile
import subprocess
import shutil
from pathlib import Path
from typing import Dict, Optional

# Préambule LaTeX standard pour les figures
TIKZ_PREAMBLE = r"""
\documentclass[tikz,border=2pt]{standalone}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{amsmath,amssymb}
\usepackage{tikz}
\usetikzlibrary{calc,angles,quotes,arrows.meta,decorations.markings,patterns,positioning}

% Styles personnalisés pour la géométrie
\tikzset{
    % Points
    point/.style={circle, fill, inner sep=1.5pt},
    point label/.style={font=\small},
    % Segments et droites
    ligne/.style={thick},
    droite/.style={thick, shorten <=-1cm, shorten >=-1cm},
    demi-droite/.style={thick, shorten >=-1cm},
    % Vecteurs
    vecteur/.style={-{Stealth[length=8pt]}, thick},
    % Angles
    angle droit/.style={draw, fill=none},
    arc angle/.style={draw, ->, thick},
    % Cercles
    cercle/.style={thick},
    % Codages
    mark segment/.style={postaction={decorate, decoration={markings,
        mark=at position 0.5 with {\draw (-2pt,-2pt) -- (2pt,2pt);}}}},
    mark segment double/.style={postaction={decorate, decoration={markings,
        mark=at position 0.5 with {
            \draw (-2pt,-2pt) -- (2pt,2pt);
            \draw ([xshift=2pt]-2pt,-2pt) -- ([xshift=2pt]2pt,2pt);
        }}}},
    % Axes
    axe/.style={-{Stealth[length=6pt]}, thick},
    grille/.style={very thin, gray!30},
    % Couleurs thématiques
    couleur1/.style={blue!70!black},
    couleur2/.style={red!70!black},
    couleur3/.style={green!60!black},
    couleur4/.style={orange!80!black},
}

\begin{document}
"""

TIKZ_POSTAMBLE = r"""
\end{document}
"""


def parse_tikz_file(tikz_path: Path) -> Dict[str, str]:
    """
    Parse un fichier .tikz et extrait les figures nommées.

    Returns:
        Dict[nom_figure, code_tikz]
    """
    if not tikz_path.exists():
        return {}

    content = tikz_path.read_text(encoding='utf-8')
    figures = {}

    # Pattern pour extraire les figures: %% FIGURE: nom suivi du code jusqu'au prochain %% FIGURE ou fin
    pattern = r'%%\s*FIGURE:\s*([a-zA-Z0-9_-]+)\s*\n(.*?)(?=%%\s*FIGURE:|$)'
    matches = re.findall(pattern, content, re.DOTALL)

    for name, code in matches:
        # Nettoyer le code (enlever espaces vides au début/fin)
        code = code.strip()
        if code:
            figures[name.strip()] = code

    return figures


def compile_tikz_to_svg(tikz_code: str, figure_name: str, temp_dir: Path) -> Optional[str]:
    """
    Compile un code TikZ en SVG et retourne le contenu SVG.

    Args:
        tikz_code: Code TikZ de la figure
        figure_name: Nom de la figure (pour les fichiers temporaires)
        temp_dir: Dossier temporaire pour la compilation

    Returns:
        Contenu SVG ou None si échec
    """
    tex_file = temp_dir / f"{figure_name}.tex"
    pdf_file = temp_dir / f"{figure_name}.pdf"
    svg_file = temp_dir / f"{figure_name}.svg"

    # Écrire le fichier .tex complet
    full_tex = TIKZ_PREAMBLE + tikz_code + TIKZ_POSTAMBLE
    tex_file.write_text(full_tex, encoding='utf-8')

    # Compiler avec pdflatex
    try:
        result = subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex_file.name],
            cwd=temp_dir,
            capture_output=True,
            timeout=30
        )

        if not pdf_file.exists():
            print(f"  [ERREUR] Compilation échouée pour {figure_name}")
            print(f"  Log: {result.stdout.decode('utf-8', errors='ignore')[-500:]}")
            return None

    except subprocess.TimeoutExpired:
        print(f"  [ERREUR] Timeout lors de la compilation de {figure_name}")
        return None
    except FileNotFoundError:
        print(f"  [ERREUR] pdflatex non trouvé. Installez MiKTeX ou TeX Live.")
        return None

    # Convertir PDF → SVG avec dvisvgm ou pdf2svg
    try:
        # Essayer dvisvgm d'abord (meilleure qualité)
        result = subprocess.run(
            ['dvisvgm', '--pdf', '--no-fonts', '-o', svg_file.name, pdf_file.name],
            cwd=temp_dir,
            capture_output=True,
            timeout=30
        )

        if not svg_file.exists():
            # Fallback: essayer pdf2svg
            subprocess.run(
                ['pdf2svg', pdf_file.name, svg_file.name],
                cwd=temp_dir,
                capture_output=True,
                timeout=30
            )
    except FileNotFoundError:
        # Essayer pdf2svg directement
        try:
            subprocess.run(
                ['pdf2svg', pdf_file.name, svg_file.name],
                cwd=temp_dir,
                capture_output=True,
                timeout=30
            )
        except FileNotFoundError:
            print(f"  [ERREUR] Ni dvisvgm ni pdf2svg trouvé.")
            return None

    if svg_file.exists():
        return svg_file.read_text(encoding='utf-8')

    return None


def svg_to_base64_img(svg_content: str, figure_name: str) -> str:
    """
    Convertit un SVG en balise <img> avec data URI base64.
    """
    # Encoder en base64
    svg_bytes = svg_content.encode('utf-8')
    b64 = base64.b64encode(svg_bytes).decode('ascii')

    # Créer la balise img
    return f'<img src="data:image/svg+xml;base64,{b64}" alt="{figure_name}" class="tikz-figure" style="max-width: 100%; height: auto;" />'


def svg_to_inline(svg_content: str, figure_name: str) -> str:
    """
    Nettoie le SVG pour insertion inline (sans balise img).
    Ajoute une classe pour le styling.
    """
    # Ajouter une classe au SVG
    svg_content = re.sub(
        r'<svg\s',
        f'<svg class="tikz-figure tikz-{figure_name}" ',
        svg_content,
        count=1
    )
    return svg_content


def compile_all_figures(tikz_path: Path, use_base64: bool = True) -> Dict[str, str]:
    """
    Compile toutes les figures d'un fichier .tikz.

    Args:
        tikz_path: Chemin vers le fichier figures.tikz
        use_base64: Si True, retourne des <img> base64, sinon SVG inline

    Returns:
        Dict[nom_figure, html_code]
    """
    figures = parse_tikz_file(tikz_path)

    if not figures:
        return {}

    print(f"  Figures TikZ: {len(figures)} trouvées")

    compiled = {}

    # Créer un dossier temporaire pour les compilations
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        for name, code in figures.items():
            print(f"    Compilation: {name}...", end=" ")

            svg_content = compile_tikz_to_svg(code, name, temp_path)

            if svg_content:
                if use_base64:
                    compiled[name] = svg_to_base64_img(svg_content, name)
                else:
                    compiled[name] = svg_to_inline(svg_content, name)
                print("OK")
            else:
                # Placeholder en cas d'échec
                compiled[name] = f'<div class="tikz-error">[Figure {name} : erreur de compilation]</div>'
                print("ERREUR")

    return compiled


def replace_placeholders(html_content: str, figures: Dict[str, str]) -> str:
    """
    Remplace les placeholders {{tikz:nom}} par le code HTML des figures.
    """
    def replacer(match):
        name = match.group(1)
        if name in figures:
            return figures[name]
        else:
            return f'<div class="tikz-missing">[Figure {name} non trouvée]</div>'

    return re.sub(r'\{\{tikz:([a-zA-Z0-9_-]+)\}\}', replacer, html_content)


# === Point d'entrée CLI ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tikz_compiler.py <fichier.tikz> [--inline]")
        print("  --inline : SVG inline au lieu de base64 (défaut: base64)")
        sys.exit(1)

    tikz_file = Path(sys.argv[1])
    use_base64 = "--inline" not in sys.argv

    if not tikz_file.exists():
        print(f"Fichier non trouvé: {tikz_file}")
        sys.exit(1)

    figures = compile_all_figures(tikz_file, use_base64)

    print(f"\nFigures compilées: {len(figures)}")
    for name in figures:
        print(f"  - {name}")
