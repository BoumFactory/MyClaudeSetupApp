#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
assemble_modules.py — Assemblage de modules H5P Branching Scenario parallèles.

Concatène plusieurs fichiers JSON « modules » (chacun contenant une liste de
nœuds ou un preplan partiel avec une clé "nodes") en un seul preplan valide,
en recalculant les index globaux des nextContentId.

Usage :
    python assemble_modules.py \\
        --config allocation.json \\
        --input module_a.json module_b.json module_c.json \\
        --output preplan_assembled.json

Format du fichier --config (optionnel) :
    {
        "title": "Mon parcours",
        "scoring": "static-end-score",
        "enableBackwardsNavigation": true,
        "startScreen": {"title": "...", "subtitle": "..."},
        "endScreens": [...],
        "modules": [
            {"file": "module_a.json", "start": 0, "count": 5},
            {"file": "module_b.json", "start": 5, "count": 3}
        ],
        "symbols": {
            "$MODULE_B_START": 5,
            "$BILAN": 8
        }
    }

Si --config est absent, les modules sont concaténés dans l'ordre donné par
--input, chaque module démarrant à l'offset = somme des tailles précédentes.

Logique de décalage d'index :
    - nextContentId >= 0 : LOCAL à l'intérieur du module → décalé de l'offset
    - nextContentId == -1 : terminal → inchangé
    - nextContentId de type str commençant par "$" : référence symbolique
      → résolue via la map "symbols" du fichier config
"""

import argparse
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def charger_json(chemin: Path) -> dict | list:
    """Charge un fichier JSON en UTF-8."""
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def extraire_noeuds(donnees: dict | list) -> list:
    """
    Extrait la liste de nœuds depuis un module.
    Accepte :
      (a) une liste de nœuds directement,
      (b) un dict avec une clé "nodes".
    """
    if isinstance(donnees, list):
        return donnees
    if isinstance(donnees, dict):
        if "nodes" in donnees:
            return donnees["nodes"]
        raise ValueError(
            "Le module est un dict mais ne contient pas de clé \"nodes\"."
        )
    raise ValueError(
        f"Format de module non reconnu : {type(donnees).__name__}"
    )


def decaler_refs(noeud: dict, offset: int, symboles: dict) -> None:
    """
    Modifie en place un nœud pour décaler ses références nextContentId.

    Règles :
      - int >= 0  → ajout de l'offset (référence locale → globale)
      - int == -1 → inchangé (nœud terminal)
      - str débutant par "$" → résolution via la map symboles
      - str quelconque → laissé tel quel (log d'avertissement)
    """
    def transformer(valeur):
        if isinstance(valeur, int):
            return valeur if valeur == -1 else valeur + offset
        if isinstance(valeur, str) and valeur.startswith("$"):
            if valeur in symboles:
                return symboles[valeur]
            print(
                f"  ATTENTION : symbole \"{valeur}\" non résolu "
                f"(absent de la map symbols).",
                file=sys.stderr,
            )
            return valeur
        return valeur

    # nextContentId de niveau nœud
    if "nextContentId" in noeud:
        noeud["nextContentId"] = transformer(noeud["nextContentId"])

    # nextContentId dans les alternatives (branching_question)
    for alt in noeud.get("alternatives", []):
        if "nextContentId" in alt:
            alt["nextContentId"] = transformer(alt["nextContentId"])

    # nextContentId dans les slides > interactions (si présent)
    for slide in noeud.get("slides", []):
        for interaction in slide.get("interactions", []):
            if "nextContentId" in interaction:
                interaction["nextContentId"] = transformer(
                    interaction["nextContentId"]
                )


# ---------------------------------------------------------------------------
# Logique principale
# ---------------------------------------------------------------------------

def construire_plan_allocation(
    fichiers_input: list[Path],
    config: dict,
) -> list[dict]:
    """
    Construit le plan d'allocation : liste de dicts
    {"fichier": Path, "offset": int, "count_attendu": int | None}.
    """
    modules_config = config.get("modules", [])
    plan = []

    if modules_config:
        # Allocation explicite depuis le fichier config
        fichiers_par_nom = {f.name: f for f in fichiers_input}
        offset_courant = 0

        for entree in modules_config:
            nom = entree.get("file", "")
            # Cherche d'abord par nom exact, sinon par correspondance partielle
            chemin = fichiers_par_nom.get(nom)
            if chemin is None:
                # Cherche dans les fichiers_input par correspondance partielle
                candidats = [f for f in fichiers_input if f.name == nom or str(f) == nom]
                if candidats:
                    chemin = candidats[0]
                else:
                    # Tente de résoudre comme chemin direct
                    p = Path(nom)
                    chemin = p if p.exists() else None

            if chemin is None:
                print(
                    f"  ATTENTION : fichier \"{nom}\" non trouvé parmi les "
                    f"fichiers --input. Module ignoré.",
                    file=sys.stderr,
                )
                continue

            offset = entree.get("start", offset_courant)
            count_attendu = entree.get("count", None)
            plan.append({
                "fichier": chemin,
                "offset": offset,
                "count_attendu": count_attendu,
            })
            offset_courant = offset + (count_attendu or 0)
    else:
        # Pas de config modules → concaténation dans l'ordre, offsets calculés
        offset_courant = 0
        for f in fichiers_input:
            plan.append({
                "fichier": f,
                "offset": offset_courant,
                "count_attendu": None,
            })
            # On ne connaît pas encore le count ; on le mettra à jour après
            # le chargement. Pour l'instant on ne peut pas calculer l'offset
            # suivant sans charger le fichier.
            # → on chargera les fichiers séquentiellement dans assemble().

    return plan


def assembler(
    fichiers_input: list[Path],
    config: dict,
) -> list:
    """
    Charge les modules, décale leurs références et les concatène.
    Retourne la liste globale de nœuds.
    """
    symboles = config.get("symbols", {})
    modules_config = config.get("modules", [])
    noeuds_globaux = []
    offset_courant = 0

    if modules_config:
        # Plan explicite : les offsets sont déjà dans la config
        fichiers_par_nom = {f.name: f for f in fichiers_input}

        for i, entree in enumerate(modules_config):
            nom = entree.get("file", "")
            chemin = fichiers_par_nom.get(nom)
            if chemin is None:
                candidats = [f for f in fichiers_input if str(f).endswith(nom)]
                chemin = candidats[0] if candidats else Path(nom)

            offset = entree.get("start", offset_courant)
            count_attendu = entree.get("count", None)

            print(f"\n  Module {i + 1} : {chemin.name}")
            print(f"    Offset global : {offset}")

            donnees = charger_json(chemin)
            noeuds = extraire_noeuds(donnees)
            count_reel = len(noeuds)
            print(f"    Nœuds trouvés : {count_reel}")

            if count_attendu is not None and count_reel != count_attendu:
                print(
                    f"    ATTENTION : {count_reel} nœuds trouvés, "
                    f"{count_attendu} attendus d'après la config.",
                    file=sys.stderr,
                )

            # Décalage des références
            for noeud in noeuds:
                decaler_refs(noeud, offset, symboles)

            noeuds_globaux.extend(noeuds)
            offset_courant = offset + count_reel

    else:
        # Concaténation séquentielle sans config explicite
        for i, chemin in enumerate(fichiers_input):
            offset = offset_courant
            print(f"\n  Module {i + 1} : {chemin.name}")
            print(f"    Offset global : {offset}")

            donnees = charger_json(chemin)
            noeuds = extraire_noeuds(donnees)
            count_reel = len(noeuds)
            print(f"    Nœuds trouvés : {count_reel}")

            for noeud in noeuds:
                decaler_refs(noeud, offset, symboles)

            noeuds_globaux.extend(noeuds)
            offset_courant += count_reel

    return noeuds_globaux


def construire_preplan(noeuds: list, config: dict) -> dict:
    """
    Assemble le preplan final avec les métadonnées issues du config (ou
    des valeurs par défaut raisonnables).
    """
    preplan = {
        "title": config.get("title", "Parcours H5P assemblé"),
        "scoring": config.get("scoring", "static-end-score"),
        "enableBackwardsNavigation": config.get(
            "enableBackwardsNavigation", False
        ),
        "startScreen": config.get(
            "startScreen",
            {"title": "Parcours H5P", "subtitle": ""},
        ),
        "nodes": noeuds,
        "endScreens": config.get(
            "endScreens",
            [
                {
                    "title": "Parcours terminé",
                    "subtitle": "Merci de votre participation.",
                    "score": 100,
                }
            ],
        ),
    }

    # Propager randomizeBranchingQuestions si présent dans la config
    if "randomizeBranchingQuestions" in config:
        preplan["randomizeBranchingQuestions"] = config[
            "randomizeBranchingQuestions"
        ]

    return preplan


# ---------------------------------------------------------------------------
# Fonction main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Assemble plusieurs modules JSON de nœuds H5P Branching Scenario "
            "en un seul preplan, en recalculant les index globaux des "
            "nextContentId."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help=(
            "Fichier JSON décrivant l'allocation d'index et les métadonnées "
            "du preplan assemblé (optionnel)."
        ),
    )
    parser.add_argument(
        "--input",
        nargs="+",
        type=Path,
        required=True,
        help="Un ou plusieurs fichiers JSON de modules à assembler.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Chemin du fichier preplan assemblé à produire.",
    )
    args = parser.parse_args()

    # Charger la config (ou dict vide si absente)
    config: dict = {}
    if args.config is not None:
        if not args.config.exists():
            print(
                f"ERREUR : fichier de config introuvable : {args.config}",
                file=sys.stderr,
            )
            return 1
        config = charger_json(args.config)
        # La config peut être une liste d'offsets simples (format minimal)
        if isinstance(config, list):
            config = {"modules": [{"start": o} for o in config]}

    # Vérifier que les fichiers d'entrée existent
    for f in args.input:
        if not f.exists():
            print(
                f"ERREUR : fichier d'entrée introuvable : {f}",
                file=sys.stderr,
            )
            return 1

    print("=" * 60)
    print("Assemblage des modules H5P Branching Scenario")
    print("=" * 60)
    print(f"  Fichiers d'entrée : {[str(f) for f in args.input]}")
    print(f"  Config            : {args.config or '(aucune)'}")
    print(f"  Sortie            : {args.output}")

    # Assemblage
    noeuds = assembler(args.input, config)
    preplan = construire_preplan(noeuds, config)

    # Écriture du preplan assemblé
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(preplan, f, ensure_ascii=False, indent=2)

    # Résumé final
    print("\n" + "=" * 60)
    print("Résumé de l'assemblage")
    print("=" * 60)
    print(f"  Modules assemblés : {len(args.input)}")
    print(f"  Total nœuds       : {len(noeuds)}")
    print(f"  Preplan écrit     : {args.output}")

    # Compter les types de nœuds
    types: dict[str, int] = {}
    for n in noeuds:
        t = n.get("type", "inconnu")
        types[t] = types.get(t, 0) + 1
    if types:
        print("  Types de nœuds :")
        for t, c in sorted(types.items()):
            print(f"    {t:30s} : {c}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
