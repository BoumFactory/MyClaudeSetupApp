#!/usr/bin/env python3
"""
Compile un projet cours HTML/KaTeX en fichier unique autonome.
Usage: python compile_project.py <chemin_projet> [--output nom_fichier.html] [--no-vocabulary] [--no-theme-switcher]

Le script :
1. Lit config.json (niveau, theme, univers, parts_order)
2. Assemble le CSS: base + niveau + theme + TOUS les univers
3. Assemble toutes les parties HTML
4. Injecte KaTeX (CSS avec fonts base64 + JS)
5. Injecte le système de vocabulaire avec infobulles
6. Injecte le theme switcher (univers + light/dark)
7. Génère le fichier unique dans output/
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Import du compilateur TikZ
try:
    from tikz_compiler import compile_all_figures, replace_placeholders
    TIKZ_AVAILABLE = True
except ImportError:
    TIKZ_AVAILABLE = False

# Chemins vers les ressources du skill
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "assets"
STYLES_DIR = SKILL_DIR / "styles"

# Valeurs par défaut
DEFAULT_NIVEAU = "2nde"
DEFAULT_THEME = "geometrie"
DEFAULT_UNIVERS = "standard"

# Liste de tous les univers disponibles
ALL_UNIVERSES = ["standard", "minimal", "paper", "nature", "retro", "manga", "futuriste", "gaming"]

def read_file(path: Path) -> str:
    """Lit un fichier et retourne son contenu."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_style(category: str, name: str) -> str:
    """Charge un fichier CSS de style."""
    style_path = STYLES_DIR / category / f"{name}.css"
    if style_path.exists():
        return read_file(style_path)
    else:
        print(f"ATTENTION: Style non trouvé: {category}/{name}.css")
        return ""

def load_vocabulary(project_path: Path = None) -> dict:
    """
    Charge le vocabulaire.
    Priorité: 1. vocabulary.json du projet, 2. vocabulary.json global du skill
    """
    if project_path:
        project_vocab = project_path / "vocabulary.json"
        if project_vocab.exists():
            with open(project_vocab, "r", encoding="utf-8") as f:
                return json.load(f)

    global_vocab = ASSETS_DIR / "vocabulary.json"
    if global_vocab.exists():
        with open(global_vocab, "r", encoding="utf-8") as f:
            return json.load(f)

    return None

def filter_vocabulary_by_niveau(vocabulary: dict, niveau: str) -> dict:
    """Filtre le vocabulaire pour ne garder que les termes du niveau approprié."""
    if not vocabulary or "terms" not in vocabulary:
        return vocabulary

    niveau_order = ["6eme", "5eme", "4eme", "3eme", "2nde", "1ere", "tle", "sup"]
    niveau_index = niveau_order.index(niveau) if niveau in niveau_order else len(niveau_order)

    filtered_terms = {}
    for term, data in vocabulary["terms"].items():
        term_niveaux = data.get("niveau", [])
        for n in term_niveaux:
            if n in niveau_order:
                n_index = niveau_order.index(n)
                if n_index <= niveau_index:
                    filtered_terms[term] = data
                    break

    return {
        "meta": vocabulary.get("meta", {}),
        "terms": filtered_terms
    }

def compile_project(project_path: str, output_name: str = None,
                   enable_vocabulary: bool = True, enable_theme_switcher: bool = True):
    """Compile le projet en fichier HTML unique."""

    project = Path(project_path)

    if not project.exists():
        print(f"ERREUR: Le projet n'existe pas: {project_path}")
        sys.exit(1)

    config_path = project / "config.json"
    if not config_path.exists():
        print(f"ERREUR: config.json manquant dans {project_path}")
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    titre = config.get("titre", "Cours")
    niveau_label = config.get("niveau_label", config.get("niveau", ""))
    parts_order = config.get("parts_order", [])

    niveau = config.get("niveau", DEFAULT_NIVEAU)
    theme = config.get("theme", DEFAULT_THEME)
    default_univers = config.get("univers", DEFAULT_UNIVERS)

    enable_vocabulary = config.get("vocabulary", enable_vocabulary)
    enable_theme_switcher = config.get("theme_switcher", enable_theme_switcher)

    print(f"Configuration: niveau={niveau}, theme={theme}, univers_defaut={default_univers}")
    print(f"  Options: vocabulary={enable_vocabulary}, theme_switcher={enable_theme_switcher}")

    # Charger les assets KaTeX
    katex_css = read_file(ASSETS_DIR / "katex-inline.css")
    katex_js = read_file(ASSETS_DIR / "katex.min.js")
    autorender_js = read_file(ASSETS_DIR / "auto-render.min.js")

    # Charger le vocabulaire si activé
    vocabulary_data = ""
    vocabulary_js = ""
    if enable_vocabulary:
        vocab = load_vocabulary(project)
        if vocab:
            vocab_filtered = filter_vocabulary_by_niveau(vocab, niveau)
            vocabulary_data = f"window.VOCABULARY_DATA = {json.dumps(vocab_filtered, ensure_ascii=False)};"
            vocab_js_path = ASSETS_DIR / "vocabulary-tooltips.js"
            if vocab_js_path.exists():
                vocabulary_js = read_file(vocab_js_path)
                print(f"  Vocabulaire: {len(vocab_filtered['terms'])} termes chargés")

    # Charger le theme switcher si activé
    theme_switcher_js = ""
    if enable_theme_switcher:
        theme_switcher_path = ASSETS_DIR / "theme-switcher.js"
        if theme_switcher_path.exists():
            theme_switcher_js = read_file(theme_switcher_path)

    # === STYLES ===
    # CSS de forçage light/dark mode
    theme_override_css = """
/* === FORÇAGE LIGHT/DARK MODE === */
/* Quand data-theme="light", on force le mode clair */
[data-theme="light"] {
    color-scheme: light;
}

/* Override des media queries pour forcer le light mode */
@media (prefers-color-scheme: dark) {
    [data-theme="light"] body,
    [data-theme="light"] .cours-container,
    [data-theme="light"] .definition,
    [data-theme="light"] .theoreme,
    [data-theme="light"] .propriete,
    [data-theme="light"] .exemple,
    [data-theme="light"] .methode,
    [data-theme="light"] .remarque,
    [data-theme="light"] .exercice {
        /* Les variables CSS sont redéfinies dans chaque univers */
    }
}

/* Quand data-theme="dark", on force le mode sombre */
[data-theme="dark"] {
    color-scheme: dark;
}
"""

    # Base + niveau + theme
    styles_parts = []

    base_css = read_file(STYLES_DIR / "base.css")
    styles_parts.append(f"/* === BASE === */\n{base_css}")

    niveau_css = load_style("niveaux", niveau)
    if niveau_css:
        styles_parts.append(f"/* === NIVEAU: {niveau} === */\n{niveau_css}")

    theme_css = load_style("themes", theme)
    if theme_css:
        styles_parts.append(f"/* === THEME: {theme} === */\n{theme_css}")

    styles_parts.append(theme_override_css)

    base_styles = "\n\n".join(styles_parts)

    # Charger TOUS les univers
    universe_styles = []
    for univ in ALL_UNIVERSES:
        univ_css = load_style("univers", univ)
        if univ_css:
            # Ajouter le CSS avec un wrapper qui sera géré par JS
            disabled = "disabled" if univ != default_univers else ""
            universe_styles.append(f'<style data-universe="{univ}" {disabled}>\n{univ_css}\n</style>')

    universe_styles_html = "\n".join(universe_styles)
    print(f"  Univers: {len(ALL_UNIVERSES)} styles inclus (défaut: {default_univers})")

    # === COMPILATION TikZ ===
    # Cherche figures.tikz dans parts/ (prioritaire) ou à la racine du projet
    tikz_figures = {}
    tikz_file = project / "parts" / "figures.tikz"
    if not tikz_file.exists():
        tikz_file = project / "figures.tikz"  # fallback racine

    if tikz_file.exists() and TIKZ_AVAILABLE:
        print(f"  TikZ: Compilation des figures depuis {tikz_file.relative_to(project)}...")
        tikz_figures = compile_all_figures(tikz_file, use_base64=True)
        print(f"  TikZ: {len(tikz_figures)} figures compilées")
    elif tikz_file.exists() and not TIKZ_AVAILABLE:
        print(f"  TikZ: ATTENTION - fichier figures.tikz trouvé mais tikz_compiler non disponible")

    # Assembler les parties HTML
    parts_content = ""
    for part_name in parts_order:
        part_file = project / "parts" / f"{part_name}.html"
        if part_file.exists():
            parts_content += read_file(part_file) + "\n\n"
        else:
            print(f"ATTENTION: Partie non trouvée: {part_file}")

    if not parts_order:
        parts_dir = project / "parts"
        if parts_dir.exists():
            for part_file in sorted(parts_dir.glob("*.html")):
                parts_content += read_file(part_file) + "\n\n"

    # Remplacer les placeholders TikZ {{tikz:nom-figure}}
    if tikz_figures and TIKZ_AVAILABLE:
        parts_content = replace_placeholders(parts_content, tikz_figures)

    # Script de vocabulaire
    vocabulary_script = ""
    if enable_vocabulary and vocabulary_js:
        vocabulary_script = f"""
<script>
{vocabulary_data}
</script>
<script>
{vocabulary_js}
</script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    setTimeout(function() {{
        if (window.VocabularyTooltips && window.VOCABULARY_DATA) {{
            VocabularyTooltips.init(window.VOCABULARY_DATA);
        }}
    }}, 500);
}});
</script>
"""

    # Script du theme switcher
    theme_switcher_script = ""
    if enable_theme_switcher and theme_switcher_js:
        theme_switcher_script = f"""
<script>
// Univers par défaut
window.DEFAULT_UNIVERSE = '{default_univers}';
</script>
<script>
{theme_switcher_js}
</script>
"""

    # Générer le HTML final
    html_output = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titre}</title>
    <style>
{katex_css}
    </style>
    <style>
{base_styles}
    </style>
    <!-- Styles des univers (un seul actif à la fois) -->
    {universe_styles_html}
</head>
<body data-universe="{default_univers}">

<div class="cours-container">
    <h1>{titre}</h1>
    <p class="niveau-label"><em>{niveau_label}</em></p>

    {parts_content}

    <div class="footer">
        Document généré avec KaTeX - Fonctionne 100% hors ligne
    </div>
</div>

<script>
{katex_js}
</script>
<script>
{autorender_js}
</script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}},
            {{left: '\\\\(', right: '\\\\)', display: false}},
            {{left: '\\\\[', right: '\\\\]', display: true}}
        ],
        throwOnError: false
    }});

    const observer = new IntersectionObserver((entries) => {{
        entries.forEach(entry => {{
            if (entry.isIntersecting) {{
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }}
        }});
    }}, {{ threshold: 0.1 }});

    document.querySelectorAll('.definition, .theoreme, .propriete, .exemple, .methode, .remarque, .exercice').forEach(el => {{
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    }});
}});
</script>
{vocabulary_script}
{theme_switcher_script}
</body>
</html>
'''

    # Nom de sortie
    if not output_name:
        safe_name = titre.lower().replace(" ", "-").replace("'", "")
        output_name = f"{safe_name}-ONEFILE.html"

    output_dir = project / "output"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / output_name
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_output)

    size_kb = output_path.stat().st_size / 1024
    size_mb = size_kb / 1024

    print(f"\nCompilation réussie !")
    print(f"  Fichier: {output_path}")
    print(f"  Taille: {size_mb:.2f} MB ({size_kb:.0f} KB)")
    print(f"  Parties: {len(parts_order) if parts_order else 'auto'}")
    print(f"  Style: {niveau} + {theme}")
    if enable_vocabulary:
        print(f"  Vocabulaire: active")
    if enable_theme_switcher:
        print(f"  Theme Switcher: active (bouton en haut a droite)")

    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description="Compile un projet cours HTML/KaTeX")
    parser.add_argument("project_path", help="Chemin du projet à compiler")
    parser.add_argument("--output", "-o", help="Nom du fichier de sortie")
    parser.add_argument("--no-vocabulary", action="store_true", help="Désactiver les infobulles de vocabulaire")
    parser.add_argument("--no-theme-switcher", action="store_true", help="Désactiver le sélecteur de thème")

    args = parser.parse_args()

    compile_project(
        args.project_path,
        args.output,
        not args.no_vocabulary,
        not args.no_theme_switcher
    )

if __name__ == "__main__":
    main()
