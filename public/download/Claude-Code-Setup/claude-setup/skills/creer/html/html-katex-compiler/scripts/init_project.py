#!/usr/bin/env python3
"""
Initialise un projet de cours HTML/KaTeX modulaire.
Usage: python init_project.py <chemin_projet> [options]

Options:
  --titre "Titre du cours"
  --niveau 2nde|1ere|tle|6eme|5eme|4eme|3eme|sup
  --niveau-label "Seconde" (texte affiché)
  --theme geometrie|analyse|algebre|probabilites|statistiques|arithmetique|trigonometrie|complexes|suites|vecteurs
  --univers standard|manga|futuriste|nature|retro|minimal|gaming|paper
"""

import os
import sys
import json
import argparse

# Valeurs disponibles
NIVEAUX = ["6eme", "5eme", "4eme", "3eme", "2nde", "1ere", "tle", "sup"]
THEMES = ["geometrie", "analyse", "algebre", "probabilites", "statistiques",
          "arithmetique", "trigonometrie", "complexes", "suites", "vecteurs"]
UNIVERS = ["standard", "manga", "futuriste", "nature", "retro", "minimal", "gaming", "paper"]

# Labels par défaut pour les niveaux
NIVEAU_LABELS = {
    "6eme": "Sixième",
    "5eme": "Cinquième",
    "4eme": "Quatrième",
    "3eme": "Troisième",
    "2nde": "Seconde",
    "1ere": "Première",
    "tle": "Terminale",
    "sup": "Supérieur"
}

def create_structure(project_path: str, titre: str, niveau: str, niveau_label: str,
                     theme: str, univers: str):
    """Crée la structure de dossiers et fichiers template."""

    # Créer les dossiers (sans styles/)
    os.makedirs(os.path.join(project_path, "parts"), exist_ok=True)
    os.makedirs(os.path.join(project_path, "output"), exist_ok=True)

    # Déterminer le label du niveau
    if not niveau_label:
        niveau_label = NIVEAU_LABELS.get(niveau, niveau)

    # Créer config.json
    config = {
        "titre": titre,
        "niveau": niveau,
        "niveau_label": niveau_label,
        "theme": theme,
        "univers": univers,
        "auteur": "",
        "parts_order": ["01-introduction"]
    }
    with open(os.path.join(project_path, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # Créer une partie template
    intro_content = """<!-- Introduction du cours -->
<h2>1. Introduction</h2>

<div class="definition">
    <strong>Définition à compléter</strong><br>
    Texte de la définition avec formule : $x^2 + y^2 = r^2$
</div>

<div class="propriete">
    Une propriété importante :
    $$\\vec{AB} + \\vec{BC} = \\vec{AC}$$
</div>

<div class="exemple">
    Exemple d'application :
    $$\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}$$
</div>

<div class="theoreme">
    <strong>Théorème fondamental</strong><br>
    Énoncé du théorème avec une formule inline $\\sqrt{a^2 + b^2}$.
</div>

<div class="methode">
    <strong>Comment résoudre ce type de problème :</strong>
    <ol>
        <li>Première étape</li>
        <li>Deuxième étape</li>
        <li>Conclusion</li>
    </ol>
</div>
"""
    with open(os.path.join(project_path, "parts", "01-introduction.html"), "w", encoding="utf-8") as f:
        f.write(intro_content)

    print(f"Projet créé : {project_path}")
    print(f"")
    print(f"  Configuration:")
    print(f"    - Niveau: {niveau} ({niveau_label})")
    print(f"    - Thème: {theme}")
    print(f"    - Univers: {univers}")
    print(f"")
    print(f"  Fichiers:")
    print(f"    - config.json")
    print(f"    - parts/01-introduction.html (template)")
    print(f"    - output/ (pour le fichier compilé)")
    print(f"")
    print(f"  Pour compiler:")
    print(f'    python ".claude/skills/html-katex-compiler/scripts/compile_project.py" "{project_path}"')

def main():
    parser = argparse.ArgumentParser(
        description="Initialise un projet cours HTML/KaTeX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Valeurs disponibles:
  --niveau: {', '.join(NIVEAUX)}
  --theme: {', '.join(THEMES)}
  --univers: {', '.join(UNIVERS)}

Exemples:
  python init_project.py mon-cours --titre "Les Vecteurs" --niveau 2nde --theme vecteurs
  python init_project.py mon-cours --titre "Probabilités" --niveau 3eme --theme probabilites --univers gaming
  python init_project.py mon-cours --titre "Analyse" --niveau tle --theme analyse --univers futuriste
"""
    )
    parser.add_argument("project_path", help="Chemin du projet à créer")
    parser.add_argument("--titre", default="Cours de Mathématiques", help="Titre du cours")
    parser.add_argument("--niveau", default="2nde", choices=NIVEAUX, help="Niveau scolaire (défaut: 2nde)")
    parser.add_argument("--niveau-label", dest="niveau_label", default="", help="Texte affiché pour le niveau")
    parser.add_argument("--theme", default="geometrie", choices=THEMES, help="Thème mathématique (défaut: geometrie)")
    parser.add_argument("--univers", default="standard", choices=UNIVERS, help="Univers graphique (défaut: standard)")

    args = parser.parse_args()

    create_structure(
        args.project_path,
        args.titre,
        args.niveau,
        args.niveau_label,
        args.theme,
        args.univers
    )

if __name__ == "__main__":
    main()
