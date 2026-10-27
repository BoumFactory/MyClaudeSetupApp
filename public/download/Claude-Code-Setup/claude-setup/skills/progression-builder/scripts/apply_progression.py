"""Applique un JSON de progression à une fiche HTML (gabarit v2).

Usage :
    python apply_progression.py --html out/progression_5E_vierge.html \
                                --progression ma_progression.json \
                                --output out/progression_5E_remplie.html

Principe
--------
Dans le gabarit v2 (`assets/reference_v2.html`), rien n'est statique : la
colonne gauche est construite en JS au chargement à partir de l'objet `DATA`,
puis `App.init(snapshot)` restaure l'état enregistré dans la balise

    <!-- __SNAPSHOT_START__ -->
    <script type="application/json" id="__snapshot__">…</script>
    <!-- __SNAPSHOT_END__ -->

C'est exactement le mécanisme du bouton « Enregistrer » de la fiche
(`exportHTML()`), qui réécrit cette balise. Le script fait donc la même chose
côté Python : il convertit le JSON de progression (schéma de
`references/format_progression_json.md`) en snapshot et l'écrit dans la balise.
À l'ouverture, la fiche déplace elle-même chaque objectif de la colonne gauche
vers sa séquence (même code que l'import manuel) : la fiche est autonome,
toutes ses fonctions sont conservées (exports, impression, double-clic,
lien vers le PDF du BO, nouvel enregistrement…).

Correspondances
---------------
  - séquence            → séquence (titre, objectifs dans l'ordre, commentaires)
  - vacances            → séparateur doré entre deux séquences
  - separateur (racine) → séparateur (label, couleur facultative) — format
                          produit par le bouton « JSON » de la fiche
  - commentaire         → commentaire ouvert (titre + texte ; URL rendues
                          cliquables, retours à la ligne conservés)
  - separateur dans une séquence → le gabarit v2 n'a pas de séparateur
                          interne : il devient un commentaire « 🛠 label »
                          qui indique le premier objectif de la phase.
  - conserver_intro     → sans effet (le gabarit v2 n'a pas de séquence d'intro).

Les codes absents du référentiel de la fiche sont signalés en [WARN] et ignorés.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import (  # noqa: E402
    SNAPSHOT_RE,
    html_escape,
    iter_data_items,
    read_data,
    read_snapshot,
)

VACANCES_COLOR = "#c8a200"   # « Doré », première couleur de SEP_COLORS du gabarit
URL_RE = re.compile(r"https?://[^\s<>\"']+")


# ---------------------------------------------------------------------------
#  Index des compétences de la fiche
# ---------------------------------------------------------------------------

def build_objectifs_index(html_text: str) -> dict[str, dict[str, str]]:
    """Index code → {text, theme, subtheme, type, page, bo_ref, bo_url}.

    Lu dans le référentiel DATA embarqué (ou dans le snapshot s'il en contient
    un), c'est-à-dire la source même de la colonne gauche de la fiche.
    """
    index: dict[str, dict[str, str]] = {}
    for theme, sub, item in iter_data_items(read_data(html_text)):
        code = item.get("code")
        if not code:
            continue
        index[code] = {
            "text": item.get("text", ""),
            "theme": theme,
            "subtheme": sub,
            "type": item.get("type", ""),
            "page": str(item.get("page", "") or ""),
            "bo_ref": item.get("boRef", ""),
            "bo_url": item.get("boUrl", ""),
        }
    return index


def print_coverage_stats(objectifs_index: dict[str, dict[str, str]],
                          placed_codes: set[str]) -> None:
    """Affiche un récap placé / total par domaine après injection."""
    by_theme_total: dict[str, int] = {}
    by_theme_placed: dict[str, int] = {}
    for code, data in objectifs_index.items():
        theme = data.get("theme") or "—"
        by_theme_total[theme] = by_theme_total.get(theme, 0) + 1
        if code in placed_codes:
            by_theme_placed[theme] = by_theme_placed.get(theme, 0) + 1

    total = len(objectifs_index)
    placed = len(placed_codes & set(objectifs_index.keys()))
    pct = (placed / total * 100) if total else 0.0
    print(f"\nCouverture : {placed}/{total} compétences placées ({pct:.1f} %)")

    width = max((len(t) for t in by_theme_total), default=10)
    for theme in by_theme_total:
        t = by_theme_total[theme]
        p = by_theme_placed.get(theme, 0)
        bar_n = int(round((p / t) * 20)) if t else 0
        bar = "█" * bar_n + "·" * (20 - bar_n)
        print(f"  {theme:<{width}}  {p:>3}/{t:<3}  {bar}")

    missing_codes = [c for c in objectifs_index if c not in placed_codes]
    if missing_codes:
        sample = ", ".join(missing_codes[:8])
        more = f" (+{len(missing_codes)-8} autres)" if len(missing_codes) > 8 else ""
        print(f"\n{len(missing_codes)} code(s) non placé(s). Exemples : {sample}{more}")


# ---------------------------------------------------------------------------
#  Progression JSON → snapshot de la fiche
# ---------------------------------------------------------------------------

def texte_to_html(texte: str) -> str:
    """Texte brut → HTML du corps de commentaire (échappé, liens, <br>)."""
    out: list[str] = []
    pos = 0
    for m in URL_RE.finditer(texte):
        out.append(html_escape(texte[pos:m.start()]))
        url = html_escape(m.group(0))
        out.append(f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>')
        pos = m.end()
    out.append(html_escape(texte[pos:]))
    return "".join(out).replace("\n", "<br>")


def _comment(item: dict) -> dict:
    label = item.get("titre") or item.get("label") or "Commentaire / Ressource"
    if item.get("html") is not None:          # format exporté par la fiche
        body = item["html"]
    else:
        body = texte_to_html(item.get("texte", "") or "")
    return {"label": label, "html": body, "open": True}


def _sequence(entry: dict, index: dict, placed: set[str],
              missing: list[str]) -> dict:
    items: list[dict] = []
    comments: list[dict] = []
    contenu = entry.get("contenu", []) or []
    for pos, item in enumerate(contenu):
        kind = item.get("type", "objectif")
        if kind == "objectif":
            code = item.get("code", "")
            data = index.get(code)
            if data is None:
                missing.append(code)
                continue
            if code in placed:
                # La fiche ne peut placer un objectif qu'une fois (il est
                # déplacé depuis la colonne gauche) : on garde la 1re place.
                print(f"[WARN] Code en doublon ignoré : {code}", file=sys.stderr)
                continue
            placed.add(code)
            items.append({
                "code": code,
                "text": data["text"],
                "theme": data["theme"],
                "subtheme": data["subtheme"],
                "type": data["type"],
            })
        elif kind == "commentaire":
            comments.append(_comment(item))
        elif kind == "separateur":
            label = item.get("label") or "Exos / RdP / Auto"
            suivant = next((c.get("code") for c in contenu[pos + 1:]
                            if c.get("type", "objectif") == "objectif"
                            and c.get("code") in index), None)
            body = (f"Phase qui commence à l'objectif {html_escape(suivant)}."
                    if suivant else "Phase en fin de séquence.")
            comments.append({"label": f"🛠 {label}", "html": body, "open": True})
        else:
            print(f"[WARN] Type d'item inconnu : {kind}", file=sys.stderr)
    return {
        "type": "sequence",
        "title": entry.get("titre") or "Séquence",
        "collapsed": bool(entry.get("replie", False)),
        "headerColor": None,
        "bodyColor": None,
        "items": items,
        "comments": comments,
    }


def build_snapshot(progression: dict, index: dict[str, dict[str, str]],
                   base: dict | None = None) -> tuple[dict, set[str], list[str]]:
    """Construit le snapshot lu par `App.init()`.

    `base` : snapshot déjà présent dans la fiche (fiche réenregistrée) ; son
    référentiel (`data`) et sa configuration (`config`) sont conservés, ses
    séquences sont remplacées.
    """
    placed: set[str] = set()
    missing: list[str] = []
    sequences: list[dict] = []
    for entry in progression.get("elements", []):
        kind = entry.get("type")
        if kind == "sequence":
            sequences.append(_sequence(entry, index, placed, missing))
        elif kind == "vacances":
            sequences.append({"type": "separateur",
                              "text": entry.get("label") or "Vacances",
                              "color": entry.get("couleur") or VACANCES_COLOR})
        elif kind == "separateur":
            sequences.append({"type": "separateur",
                              "text": entry.get("label") or entry.get("text") or "",
                              "color": entry.get("color") or entry.get("couleur")
                              or VACANCES_COLOR})
        else:
            print(f"[WARN] Type d'élément racine inconnu : {kind}", file=sys.stderr)

    snapshot: dict = {}
    if base:
        for key in ("title", "sousTitre", "config", "data"):
            if key in base:
                snapshot[key] = base[key]
    if progression.get("titre"):
        snapshot["title"] = progression["titre"]
    if progression.get("sous_titre") is not None:
        snapshot["sousTitre"] = progression["sous_titre"]
    snapshot["sequences"] = sequences
    return snapshot, placed, missing


def inject_snapshot(html_text: str, snapshot: dict) -> str:
    """Écrit le snapshot dans la balise __snapshot__ (comme exportHTML())."""
    if not SNAPSHOT_RE.search(html_text):
        raise ValueError("Balise __snapshot__ introuvable : la fiche ne provient "
                         "pas du gabarit v2 (relancer generate_vierge.py).")
    payload = json.dumps(snapshot, ensure_ascii=False).replace("</", "<\\/")
    return SNAPSHOT_RE.sub(lambda m: m.group(1) + payload + m.group(3),
                           html_text, count=1)


def apply_progression(html_text: str, progression: dict,
                       show_stats: bool = True) -> str:
    index = build_objectifs_index(html_text)
    snapshot, placed, missing = build_snapshot(
        progression, index, base=read_snapshot(html_text))
    out = inject_snapshot(html_text, snapshot)

    if missing:
        print(
            f"[WARN] {len(missing)} code(s) absent(s) du référentiel de la fiche, "
            "non placé(s) : " + ", ".join(missing[:8]) + ("…" if len(missing) > 8 else ""),
            file=sys.stderr,
        )
    if show_stats:
        print_coverage_stats(index, placed)
    return out


# ---------------------------------------------------------------------------
#  CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Applique un JSON de progression à une fiche HTML (gabarit v2).")
    parser.add_argument("--html", required=True, help="Fiche HTML en entrée (vierge ou déjà remplie)")
    parser.add_argument("--progression", required=True, help="JSON décrivant la progression")
    parser.add_argument("--output", required=True, help="Fiche HTML remplie en sortie")
    parser.add_argument("--no-stats", action="store_true",
                        help="N'affiche pas le récap de couverture par domaine.")
    args = parser.parse_args()

    html_text = Path(args.html).read_text(encoding="utf-8")
    progression = json.loads(Path(args.progression).read_text(encoding="utf-8"))

    out = apply_progression(html_text, progression, show_stats=not args.no_stats)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print(f"[OK] Progression appliquée → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
