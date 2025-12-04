#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUILD MONOLITH
==============
Génère un fichier HTML unique (monolithique) à partir des fichiers modulaires.
Ce fichier peut être partagé facilement avec les élèves.

Usage:
    python build_monolith.py                    # Génère animation.html dans le dossier courant
    python build_monolith.py output.html        # Génère avec un nom personnalisé
    python build_monolith.py -m                 # Minifie le code
    python build_monolith.py --watch            # Surveille les changements et rebuild

Options:
    -m, --minify     Minifie le CSS et JS (retire commentaires, espaces inutiles)
    -w, --watch      Mode surveillance: rebuild automatique si fichier modifié
    -o, --output     Chemin du fichier de sortie
    -h, --help       Affiche cette aide
"""

import os
import sys
import re
import time
import argparse
from pathlib import Path
from datetime import datetime


def read_file(filepath: Path) -> str:
    """Lit un fichier avec gestion de l'encodage."""
    try:
        return filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[ERREUR] Impossible de lire {filepath}: {e}")
        return ""


def minify_css(css: str) -> str:
    """Minifie le CSS en retirant commentaires et espaces inutiles."""
    # Retirer les commentaires
    css = re.sub(r'/\*[\s\S]*?\*/', '', css)
    # Retirer les espaces multiples
    css = re.sub(r'\s+', ' ', css)
    # Retirer les espaces autour des caractères spéciaux
    css = re.sub(r'\s*([{};:,>+~])\s*', r'\1', css)
    # Retirer les espaces en début/fin
    css = css.strip()
    return css


def minify_js(js: str) -> str:
    """
    Minification légère du JS (conserve la lisibilité pour debug).
    Ne supprime que les commentaires sur une ligne et les espaces multiples.
    """
    # Retirer les commentaires // (mais pas dans les strings)
    lines = []
    for line in js.split('\n'):
        # Simple heuristique: retirer // si pas dans une string
        if '//' in line and '"' not in line.split('//')[0] and "'" not in line.split('//')[0]:
            line = line.split('//')[0]
        lines.append(line.rstrip())
    js = '\n'.join(lines)

    # Retirer les lignes vides multiples
    js = re.sub(r'\n\s*\n\s*\n', '\n\n', js)

    return js


def collect_css_files(base_path: Path) -> list:
    """Collecte tous les fichiers CSS dans l'ordre."""
    css_dir = base_path / 'css'
    if not css_dir.exists():
        return []

    # Ordre de chargement important
    order = ['main.css', 'controls.css', 'scenarios.css']
    files = []

    for name in order:
        filepath = css_dir / name
        if filepath.exists():
            files.append(filepath)

    # Ajouter les autres fichiers CSS
    for filepath in sorted(css_dir.glob('*.css')):
        if filepath not in files:
            files.append(filepath)

    return files


def collect_js_files(base_path: Path) -> list:
    """Collecte tous les fichiers JS dans l'ordre de dépendances."""
    js_dir = base_path / 'js'
    if not js_dir.exists():
        return []

    files = []

    # 1. Fichiers core (ordre de dependance)
    core_order = [
        'math-utils.js',
        'canvas-renderer.js',
        'animation-core.js',
        'timeline.js',
        'controls.js',
        'render-helpers.js',
        'animation-logic.js',
    ]

    for name in core_order:
        filepath = js_dir / name
        if filepath.exists():
            files.append(filepath)

    # 2. Fichiers scenarios/ (dans l'ordre alphabétique)
    scenarios_dir = js_dir / 'scenarios'
    if scenarios_dir.exists():
        # D'abord index.js (définit le registre et helpers)
        index_file = scenarios_dir / 'index.js'
        if index_file.exists():
            files.append(index_file)

        # Ensuite les scènes dans l'ordre alphabétique (01-, 02-, ...)
        for filepath in sorted(scenarios_dir.glob('*.js')):
            if filepath.name != 'index.js' and filepath not in files:
                files.append(filepath)

    # 3. Fichier scenes.js (récupère du registre)
    scenes_file = js_dir / 'scenes.js'
    if scenes_file.exists():
        files.append(scenes_file)

    # 4. Fichier main.js (point d'entrée)
    main_file = js_dir / 'main.js'
    if main_file.exists():
        files.append(main_file)

    # 5. Autres fichiers JS non listés
    for filepath in sorted(js_dir.glob('*.js')):
        if filepath not in files:
            files.append(filepath)

    return files


def extract_html_body(html_content: str) -> dict:
    """
    Extrait les differentes parties du HTML:
    - head_meta: meta tags, title
    - body: contenu du body
    - head_scripts: scripts inline du head (MathJax config, etc.)
    - external_scripts: scripts externes (CDN)
    """
    result = {
        'title': 'Animation Interactive',
        'body': '',
        'head_scripts': '',
        'external_scripts': ''
    }

    # Extraire le titre
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if title_match:
        result['title'] = title_match.group(1)

    # Extraire les scripts inline du head (comme la config MathJax)
    head_match = re.search(r'<head[^>]*>([\s\S]*?)</head>', html_content, re.IGNORECASE)
    if head_match:
        head_content = head_match.group(1)
        # Trouver les scripts inline dans le head
        inline_scripts = re.findall(r'<script>[\s\S]*?</script>', head_content, re.IGNORECASE)
        result['head_scripts'] = '\n'.join(inline_scripts)
        # Trouver les scripts externes (CDN) dans le head
        external_scripts = re.findall(r'<script[^>]*src="https?://[^"]*"[^>]*></script>', head_content, re.IGNORECASE)
        result['external_scripts'] = '\n    '.join(external_scripts)

    # Extraire le body
    body_match = re.search(r'<body[^>]*>([\s\S]*?)</body>', html_content, re.IGNORECASE)
    if body_match:
        body = body_match.group(1)
        # Retirer les balises script (on les inline nous-memes)
        body = re.sub(r'<script[^>]*src=[^>]*></script>\s*', '', body)
        result['body'] = body.strip()

    return result


def build_monolith(base_path: Path, output_path: Path, minify: bool = False) -> bool:
    """
    Construit le fichier HTML monolithique.

    Args:
        base_path: Chemin vers le dossier de l'animation
        output_path: Chemin du fichier de sortie
        minify: Si True, minifie le CSS et JS

    Returns:
        True si succès, False sinon
    """
    print(f"\n{'='*60}")
    print(f"BUILD MONOLITH - {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")
    print(f"Source: {base_path}")
    print(f"Output: {output_path}")
    print(f"Minify: {'Oui' if minify else 'Non'}")
    print()

    # Vérifier que index.html existe
    index_path = base_path / 'index.html'
    if not index_path.exists():
        print(f"[ERREUR] index.html non trouvé dans {base_path}")
        return False

    # Lire index.html
    index_html = read_file(index_path)
    html_parts = extract_html_body(index_html)

    # Collecter les CSS
    css_files = collect_css_files(base_path)
    print(f"[CSS] {len(css_files)} fichier(s) trouvé(s)")

    css_content = []
    for filepath in css_files:
        content = read_file(filepath)
        if content:
            css_content.append(f"/* === {filepath.name} === */")
            css_content.append(minify_css(content) if minify else content)
            print(f"  + {filepath.name}")

    all_css = '\n\n'.join(css_content)

    # Collecter les JS
    js_files = collect_js_files(base_path)
    print(f"\n[JS] {len(js_files)} fichier(s) trouvé(s)")

    js_content = []
    for filepath in js_files:
        content = read_file(filepath)
        if content:
            js_content.append(f"// === {filepath.name} ===")
            js_content.append(minify_js(content) if minify else content)
            print(f"  + {filepath.name}")

    all_js = '\n\n'.join(js_content)

    # Construire le HTML final avec support MathJax
    head_scripts = html_parts.get('head_scripts', '')
    external_scripts = html_parts.get('external_scripts', '')

    html_output = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_parts['title']}</title>
    {head_scripts}
    {external_scripts}
    <style>
{all_css}
    </style>
</head>
<body>
{html_parts['body']}
    <script>
{all_js}
    </script>
</body>
</html>
'''

    # Écrire le fichier de sortie
    try:
        output_path.write_text(html_output, encoding='utf-8')
        file_size = output_path.stat().st_size
        print(f"\n[SUCCÈS] Fichier généré: {output_path}")
        print(f"         Taille: {file_size / 1024:.1f} Ko")
        return True
    except Exception as e:
        print(f"\n[ERREUR] Impossible d'écrire {output_path}: {e}")
        return False


def watch_mode(base_path: Path, output_path: Path, minify: bool = False):
    """
    Mode surveillance: rebuild automatique quand un fichier change.
    """
    print("\n[WATCH] Mode surveillance activé. Ctrl+C pour arrêter.")

    last_mtime = 0

    while True:
        try:
            # Collecter tous les fichiers à surveiller
            files_to_watch = [base_path / 'index.html']
            files_to_watch.extend(collect_css_files(base_path))
            files_to_watch.extend(collect_js_files(base_path))

            # Trouver le plus récent
            current_mtime = 0
            for f in files_to_watch:
                if f.exists():
                    mtime = f.stat().st_mtime
                    if mtime > current_mtime:
                        current_mtime = mtime

            # Rebuild si changement
            if current_mtime > last_mtime:
                last_mtime = current_mtime
                build_monolith(base_path, output_path, minify)

            time.sleep(1)

        except KeyboardInterrupt:
            print("\n[WATCH] Arrêt de la surveillance.")
            break


def main():
    parser = argparse.ArgumentParser(
        description='Génère un fichier HTML monolithique à partir des fichiers modulaires.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
    python build_monolith.py
    python build_monolith.py -o animation.html
    python build_monolith.py -m -o animation.min.html
    python build_monolith.py --watch
        """
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='animation.html',
        help='Nom du fichier de sortie (défaut: animation.html)'
    )

    parser.add_argument(
        '-m', '--minify',
        action='store_true',
        help='Minifie le CSS et JS'
    )

    parser.add_argument(
        '-w', '--watch',
        action='store_true',
        help='Mode surveillance: rebuild automatique'
    )

    parser.add_argument(
        'path',
        nargs='?',
        type=str,
        default='.',
        help='Chemin du dossier source (défaut: dossier courant)'
    )

    args = parser.parse_args()

    # Déterminer les chemins
    base_path = Path(args.path).resolve()
    output_path = base_path / args.output

    # Vérifier que le dossier existe
    if not base_path.exists():
        print(f"[ERREUR] Le dossier {base_path} n'existe pas.")
        sys.exit(1)

    # Exécuter
    if args.watch:
        watch_mode(base_path, output_path, args.minify)
    else:
        success = build_monolith(base_path, output_path, args.minify)
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
