"""Valide un JSON de progression avant injection.

Vérifie en amont d'`apply_progression.py` :

  - structure (types acceptés au niveau racine et dans les séquences),
  - existence des codes (croisés avec le JSON v2 du niveau, ou avec un
    HTML vierge si on veut valider contre une fiche déjà customisée),
  - doublons (un même code placé plusieurs fois — autorisé mais signalé),
  - cohérence du champ `niveau`,
  - champs requis présents (titre de séquence, code d'objectif).

Usage :

    python validate_progression.py --progression out/my_prog.json
    python validate_progression.py --progression out/my_prog.json --html out/progression_5E_vierge.html
    python validate_progression.py --progression out/my_prog.json --strict

Sortie : rapport stdout. Exit code 0 si OK, 1 si au moins une erreur,
2 si erreurs *non bloquantes* mais signalées en mode `--strict`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_V2_JSON_DIR = (
    Path(__file__).resolve().parents[2] / "programmes-officiels" / "data" / "json"
)

VALID_ROOT_TYPES = {"sequence", "vacances"}
VALID_CONTENT_TYPES = {"objectif", "commentaire", "separateur"}
VALID_NIVEAUX = {"CM1", "CM2", "6E", "5E", "4E", "3E",
                 "2GT", "1SPE", "1ENS", "1TEC", "TSPE", "TCOMP", "TTEC"}


# ---------------------------------------------------------------------------
#  Chargement des codes valides pour un niveau
# ---------------------------------------------------------------------------

def codes_from_v2_json(niveau: str) -> set[str]:
    """Lit le JSON v2 et renvoie l'ensemble des codes attendus dans le HTML.

    Les compétences ont un `code` explicite dans le JSON. Les automatismes
    sont stockés comme strings ; leurs codes sont synthétisés par
    `generate_vierge.py` sous la forme `🅰{NIV}🛠{i}` (i démarre à 1).
    On reconstruit la même règle ici pour pouvoir les valider.
    """
    json_path = DEFAULT_V2_JSON_DIR / f"{niveau}.json"
    if not json_path.exists():
        raise FileNotFoundError(f"JSON v2 introuvable : {json_path}")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    codes: set[str] = set()
    for domaine_dict in data.get("competences_by_theme", {}).values():
        for sous_dom_list in domaine_dict.values():
            for comp in sous_dom_list:
                code = comp.get("code")
                if code:
                    codes.add(code)
    for i, _auto in enumerate(data.get("automatismes", []), start=1):
        codes.add(f"🅰{niveau}🛠{i}")
    return codes


def codes_from_html(html_path: Path) -> set[str]:
    """Extrait les data-code présents dans le HTML vierge."""
    html_text = html_path.read_text(encoding="utf-8")
    return set(re.findall(r'data-code="([^"]+)"', html_text))


# ---------------------------------------------------------------------------
#  Validation
# ---------------------------------------------------------------------------

class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.stats: dict[str, int] = {}

    def err(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)

    def has_errors(self) -> bool:
        return bool(self.errors)


def validate(progression: dict, valid_codes: set[str], report: Report) -> None:
    # Champ niveau
    niveau = progression.get("niveau")
    if niveau is None:
        report.warn('Champ "niveau" absent (informatif mais recommandé).')
    elif niveau not in VALID_NIVEAUX:
        report.err(f'Champ "niveau" invalide : "{niveau}". '
                   f'Attendu : un parmi {sorted(VALID_NIVEAUX)}.')

    # Champ elements
    elements = progression.get("elements")
    if elements is None:
        report.err('Champ "elements" manquant — rien à appliquer.')
        return
    if not isinstance(elements, list):
        report.err('"elements" doit être une liste.')
        return

    placed_codes: list[str] = []
    nb_sequences = 0
    nb_vacances = 0
    nb_commentaires = 0
    nb_separateurs = 0

    for idx, elem in enumerate(elements):
        if not isinstance(elem, dict):
            report.err(f'elements[{idx}] doit être un objet, pas {type(elem).__name__}.')
            continue
        kind = elem.get("type")
        if kind not in VALID_ROOT_TYPES:
            report.err(f'elements[{idx}].type "{kind}" invalide. '
                       f'Attendu : {sorted(VALID_ROOT_TYPES)}.')
            continue

        if kind == "vacances":
            nb_vacances += 1
            continue

        # Séquence
        nb_sequences += 1
        titre = elem.get("titre")
        if not titre:
            report.warn(f'elements[{idx}] (sequence) : titre vide ou absent.')
        contenu = elem.get("contenu", [])
        if not isinstance(contenu, list):
            report.err(f'elements[{idx}].contenu doit être une liste.')
            continue
        for cidx, item in enumerate(contenu):
            if not isinstance(item, dict):
                report.err(f'elements[{idx}].contenu[{cidx}] doit être un objet.')
                continue
            ctype = item.get("type", "objectif")
            if ctype not in VALID_CONTENT_TYPES:
                report.err(f'elements[{idx}].contenu[{cidx}].type "{ctype}" invalide. '
                           f'Attendu : {sorted(VALID_CONTENT_TYPES)}.')
                continue
            if ctype == "objectif":
                code = item.get("code")
                if not code:
                    report.err(f'elements[{idx}].contenu[{cidx}] (objectif) : '
                               f'champ "code" manquant.')
                    continue
                if code not in valid_codes:
                    report.err(f'Code inconnu : "{code}" '
                               f'(elements[{idx}].contenu[{cidx}]). '
                               f'Vérifier le BO ou la casse du code.')
                else:
                    placed_codes.append(code)
            elif ctype == "commentaire":
                nb_commentaires += 1
            elif ctype == "separateur":
                nb_separateurs += 1

    # Doublons
    seen: dict[str, int] = {}
    for c in placed_codes:
        seen[c] = seen.get(c, 0) + 1
    duplicates = {c: n for c, n in seen.items() if n > 1}
    if duplicates:
        report.warn(
            f'{len(duplicates)} code(s) en doublon : '
            + ", ".join(f"{c}×{n}" for c, n in sorted(duplicates.items()))
        )

    # Stats
    report.stats = {
        "sequences": nb_sequences,
        "vacances": nb_vacances,
        "commentaires": nb_commentaires,
        "separateurs": nb_separateurs,
        "objectifs_places": len(placed_codes),
        "objectifs_uniques": len(set(placed_codes)),
        "objectifs_disponibles": len(valid_codes),
    }


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valide un JSON de progression avant injection."
    )
    parser.add_argument("--progression", required=True,
                        help="JSON de progression à valider")
    parser.add_argument("--html",
                        help="HTML vierge à utiliser comme source de codes valides "
                             "(prioritaire sur le JSON v2 si fourni)")
    parser.add_argument("--niveau",
                        help="Niveau à utiliser pour charger le JSON v2 "
                             "(par défaut : champ \"niveau\" du JSON de progression)")
    parser.add_argument("--strict", action="store_true",
                        help="Considère les warnings comme bloquants (exit code 2).")
    args = parser.parse_args()

    progression = json.loads(Path(args.progression).read_text(encoding="utf-8"))

    if args.html:
        valid_codes = codes_from_html(Path(args.html))
        source = f"HTML {args.html}"
    else:
        niveau = args.niveau or progression.get("niveau")
        if not niveau:
            print('[ERR] Impossible de déterminer le niveau : ni --niveau, '
                  'ni --html, ni champ "niveau" dans le JSON.', file=sys.stderr)
            return 1
        try:
            valid_codes = codes_from_v2_json(niveau)
        except FileNotFoundError as e:
            print(f"[ERR] {e}", file=sys.stderr)
            return 1
        source = f"JSON v2 niveau {niveau}"

    report = Report()
    validate(progression, valid_codes, report)

    # Affichage
    print(f"Source des codes valides : {source}")
    print(f"Codes disponibles : {len(valid_codes)}")
    if report.stats:
        s = report.stats
        print(f"Structure : {s['sequences']} séquence(s), {s['vacances']} vacances, "
              f"{s['commentaires']} commentaire(s), {s['separateurs']} séparateur(s).")
        print(f"Objectifs placés : {s['objectifs_places']} "
              f"(dont {s['objectifs_uniques']} uniques) "
              f"sur {s['objectifs_disponibles']} disponibles.")

    if report.warnings:
        print(f"\n[WARN] {len(report.warnings)} avertissement(s) :")
        for w in report.warnings:
            print(f"  - {w}")
    if report.errors:
        print(f"\n[ERR] {len(report.errors)} erreur(s) :")
        for e in report.errors:
            print(f"  - {e}")
        return 1

    if args.strict and report.warnings:
        print("\n[STRICT] Avertissement(s) considéré(s) comme bloquant(s).")
        return 2

    print("\n[OK] Progression valide.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
