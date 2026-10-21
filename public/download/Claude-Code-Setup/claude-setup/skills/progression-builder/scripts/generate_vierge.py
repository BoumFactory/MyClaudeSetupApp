"""Génère une fiche HTML de progression VIERGE pour un niveau donné.

Usage :
    python generate_vierge.py --niveau 5E --output out/progression_5E_vierge.html

Le script (v2) :
  1. Lit le JSON du niveau cible dans le skill `programmes-officiels`
     (data/json/{NIVEAU}.json).
  2. Charge le squelette HTML v2 (assets/reference_v2.html) — architecture
     App namespace avec CONFIG/DATA dynamiques, snapshot/restore, config panel.
  3. Convertit le JSON v2 en objet DATA au format attendu par le gabarit (code, type,
     page, boRef, boUrl) et l'injecte entre les marqueurs __DATA_START__ et
     __DATA_END__.
  4. Injecte le CONFIG avec les couleurs de nos domaines.
  5. Met à jour le <title>, le titre h2 et le sous-titre.
  6. Embarque le PDF du programme en base64.
  7. Écrit le HTML autonome final.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import (  # noqa: E402
    AUTOMATISMES_INFO,
    COLLEGE_NIVEAUX,
    DOMAINE_INFO,
    MACRO_INFO,
    NIVEAU_LABEL,
    html_escape,
    macro_for_college,
    macro_order_for,
)

SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REFERENCE = SKILL_ROOT / "assets" / "reference_v2.html"
DEFAULT_V2_JSON_DIR = (
    SKILL_ROOT.parents[0] / "programmes-officiels" / "data" / "json"
)
DEFAULT_V2_PDF_DIR = (
    SKILL_ROOT.parents[0] / "programmes-officiels" / "data" / "pdf"
)


def _v2_to_data(level_data: dict, niveau_code: str) -> dict:
    """Convertit un JSON v2 en objet DATA au format attendu par le template.

    Format de sortie :
    {
      "Nombres et calculs": {
        "color": "NB",
        "themes": {
          "Opérations": [
            {"text": "Additionner...", "code": "5E-NB-001", "type": "capacite",
             "page": 7, "boRef": "BO...", "boUrl": "https://..."}
          ]
        }
      },
      "Automatismes": {
        "color": "AUTO",
        "themes": {
          "Opérations": {
            "color": "NB",
            "items": [...]
          }
        }
      }
    }
    """
    competences_by_theme = level_data.get("competences_by_theme", {})
    meta = level_data.get("meta", {})
    niveau_bo_ref = meta.get("bo_reference", "")
    niveau_bo_url = meta.get("bo_url", "")

    data = {}

    def _items(comps: list) -> list:
        out = []
        for comp in comps:
            src = comp.get("source", {}) or {}
            out.append({
                "text": comp.get("intitule", ""),
                "code": comp.get("code", ""),
                "type": comp.get("type", "capacite"),
                "page": src.get("page", ""),
                "boRef": src.get("bo_reference", "") or niveau_bo_ref,
                "boUrl": src.get("bo_url", "") or niveau_bo_url,
            })
        return out

    if niveau_code in COLLEGE_NIVEAUX:
        # --- Collège : regroupement par GRAND DOMAINE BO (en-têtes réels) ---
        buckets: dict = {}  # macro -> {sous_dom -> items}
        for domaine, sous_themes in competences_by_theme.items():
            if not sous_themes:
                continue
            for sous_dom, comps in sous_themes.items():
                if not comps:
                    continue
                macro = macro_for_college(domaine, sous_dom, niveau_code)
                buckets.setdefault(macro, {}).setdefault(sous_dom, []).extend(_items(comps))
        for macro in macro_order_for(niveau_code):
            if macro not in buckets:
                continue
            info = MACRO_INFO[macro]
            data[f"{info['emoji']} {macro}"] = {
                "color": info["color_code"], "themes": buckets[macro],
            }
        for macro, themes in buckets.items():  # filet de sécurité
            if macro not in macro_order_for(niveau_code):
                data[f"❓ {macro}"] = {"color": "NB", "themes": themes}
    else:
        # --- Lycée : taxonomie fine inchangée ---
        domaines_presents = [d for d in DOMAINE_INFO if d in competences_by_theme]
        for d in competences_by_theme:
            if d not in domaines_presents and d in DOMAINE_INFO:
                domaines_presents.append(d)

        for domaine in domaines_presents:
            info = DOMAINE_INFO[domaine]
            sous_themes = competences_by_theme[domaine]
            if not sous_themes:
                continue

            theme_label = f"{info['emoji']} {info['label']}"
            themes_dict: dict = {}
            for sous_dom, comps in sous_themes.items():
                themes_dict[sous_dom] = _items(comps)

            data[theme_label] = {"color": domaine, "themes": themes_dict}

    # Automatismes
    automatismes_d = level_data.get("automatismes_detailed") or []
    automatismes_s = level_data.get("automatismes", [])

    if automatismes_d or automatismes_s:
        a_info = AUTOMATISMES_INFO
        auto_themes: dict = {}

        if automatismes_d:
            by_sous_dom: dict[str, list] = {}
            for auto in automatismes_d:
                sd = auto.get("sous_domaine", "Automatismes") or "Automatismes"
                by_sous_dom.setdefault(sd, []).append(auto)

            global_idx = 0
            for sd, autos in by_sous_dom.items():
                items = []
                for auto in autos:
                    global_idx += 1
                    src = auto.get("source", {}) or {}
                    items.append({
                        "text": auto.get("text", ""),
                        "code": f"\U0001f170{niveau_code}\U0001f6e0{global_idx}",
                        "type": "automatisme",
                        "page": src.get("page", ""),
                        "boRef": src.get("bo_reference", "") or niveau_bo_ref,
                        "boUrl": src.get("bo_url", "") or niveau_bo_url,
                    })
                dom_code = autos[0].get("domaine", "AUTO") if autos else "AUTO"
                auto_themes[sd] = {"color": dom_code, "items": items}
        else:
            items = []
            for i, text in enumerate(automatismes_s, start=1):
                items.append({
                    "text": text,
                    "code": f"\U0001f170{niveau_code}\U0001f6e0{i}",
                    "type": "automatisme",
                })
            auto_themes["Automatismes du niveau"] = items

        data[f"{a_info['emoji']} {a_info['label']}"] = {
            "color": "AUTO",
            "themes": auto_themes,
        }

    return data


def _build_config(level_data: dict) -> dict:
    """Construit le CONFIG pour un niveau donné."""
    colors = {}
    for code, info in DOMAINE_INFO.items():
        colors[code] = info["color"]
    colors["AUTO"] = AUTOMATISMES_INFO["color"]

    return {
        "colors": colors,
        "comment": {"border": "#c8a200", "header": "#fdf7cc", "body": "#fffde8"},
        "sequence": {"headerBg": "#e5e5e5", "bodyBg": "#f5f5f5"},
        "pdf": {"showNumbers": False, "showDate": False, "fontFamily": "sans-serif"},
    }


def rebuild_html(reference_html: str, level_data: dict, niveau_code: str) -> str:
    """Reconstruit le HTML en injectant DATA et CONFIG."""

    titre_niveau = NIVEAU_LABEL.get(niveau_code, niveau_code)
    meta = level_data.get("meta", {})
    bo_ref = meta.get("bo_reference", "")
    bo_url = meta.get("bo_url", "")

    # ---- 1) Injecter DATA ----
    data_obj = _v2_to_data(level_data, niveau_code)
    data_json = json.dumps(data_obj, ensure_ascii=False, indent=2)
    # Échapper </script> dans le JSON pour la sécurité HTML
    data_json = data_json.replace("</script>", "<\\/script>")

    data_start = "/* __DATA_START__ */"
    data_end = "/* __DATA_END__ */"
    ds_pos = reference_html.find(data_start)
    de_pos = reference_html.find(data_end)
    if ds_pos == -1 or de_pos == -1:
        raise ValueError("Marqueurs __DATA_START__/__DATA_END__ introuvables")
    reference_html = (
        reference_html[: ds_pos + len(data_start)]
        + f"\n  let DATA = {data_json};\n  "
        + reference_html[de_pos:]
    )

    # ---- 2) Injecter CONFIG ----
    config_obj = _build_config(level_data)
    config_json = json.dumps(config_obj, ensure_ascii=False, indent=2)
    # Indenter pour alignement dans le JS
    config_json = config_json.replace("\n", "\n  ")

    config_start = "/* __CONFIG_START__ */"
    config_end = "/* __CONFIG_END__ */"
    # Re-chercher les positions car le HTML a changé
    cs_pos = reference_html.find(config_start)
    ce_pos = reference_html.find(config_end)
    if cs_pos != -1 and ce_pos != -1:
        reference_html = (
            reference_html[: cs_pos + len(config_start)]
            + f"\n  let CONFIG = {config_json};\n  "
            + reference_html[ce_pos:]
        )

    # ---- 3) <title> ----
    new_title = f"<title>Progression — {html_escape(titre_niveau)} ({niveau_code})</title>"
    reference_html = re.sub(
        r"<title>[^<]*</title>", new_title, reference_html, count=1
    )

    # ---- 4) Titre H2 et sous-titre ----
    reference_html = re.sub(
        r'id="progressionTitle">[^<]*</h2>',
        f'id="progressionTitle">Progression de {html_escape(titre_niveau)} ({html_escape(niveau_code)}) en mathématiques</h2>',
        reference_html,
        count=1,
    )

    sous_titre = f"Programme officiel — {html_escape(bo_ref)}" if bo_ref else "Programme officiel"
    reference_html = re.sub(
        r'id="sous-titre"[^>]*>[^<]*</div>',
        f'id="sous-titre" contenteditable="true" style="font-size:1em; color:#444; margin-top:4px; font-style:italic; outline:none;">{sous_titre}</div>',
        reference_html,
        count=1,
    )

    # ---- 5) Titre panneau gauche ----
    reference_html = reference_html.replace(
        "Liste des objectifs et \U0001f6e0 Automatismes",
        f"Objectifs et \U0001f6e0 Automatismes — {html_escape(titre_niveau)} ({html_escape(niveau_code)})",
        1,
    )

    # ---- 6) PDF embarqué en base64 ----
    pdf_filename = meta.get("pdf", "")
    sentinel = '<script type="text/plain" id="embeddedPdfB64"'
    if pdf_filename and sentinel not in reference_html:
        pdf_path = DEFAULT_V2_PDF_DIR / pdf_filename
        if pdf_path.exists():
            b64 = base64.b64encode(pdf_path.read_bytes()).decode("ascii")
            script_pdf = (
                f'{sentinel} '
                f'data-pdf-name="{html_escape(pdf_filename)}">{b64}<'
                f'/script>'
            )
            # Insérer avant le DERNIER </body> (pas le premier, qui est
            # dans un template JS de exportPDF)
            last_body = reference_html.rfind("</body>")
            if last_body != -1:
                reference_html = (
                    reference_html[:last_body]
                    + script_pdf + "\n"
                    + reference_html[last_body:]
                )
        else:
            print(f"[WARN] PDF embarqué introuvable : {pdf_path}", flush=True)

    return reference_html


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Génère une fiche HTML de progression vierge (template v2)."
    )
    parser.add_argument("--niveau", required=True, help="Code du niveau (CM1, 5E, TSPE, …)")
    parser.add_argument(
        "--json-dir",
        default=str(DEFAULT_V2_JSON_DIR),
        help="Dossier contenant les {NIVEAU}.json (skill)",
    )
    parser.add_argument(
        "--reference",
        default=str(DEFAULT_REFERENCE),
        help="Fiche HTML de référence (squelette v2)",
    )
    parser.add_argument("--output", required=True, help="Chemin de sortie du HTML généré")
    args = parser.parse_args()

    niveau = args.niveau.upper()
    if niveau not in NIVEAU_LABEL:
        print(
            f"[ERREUR] Niveau inconnu : {niveau}. Valeurs valides : {', '.join(NIVEAU_LABEL)}",
            file=sys.stderr,
        )
        return 2

    json_path = Path(args.json_dir) / f"{niveau}.json"
    if not json_path.exists():
        print(f"[ERREUR] JSON introuvable : {json_path}", file=sys.stderr)
        return 2

    ref_path = Path(args.reference)
    if not ref_path.exists():
        print(f"[ERREUR] Référence introuvable : {ref_path}", file=sys.stderr)
        return 2

    level_data = json.loads(json_path.read_text(encoding="utf-8"))
    reference_html = ref_path.read_text(encoding="utf-8")

    out_html = rebuild_html(reference_html, level_data, niveau)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out_html, encoding="utf-8")

    n_competences = level_data.get("meta", {}).get("total_competences", "?")
    n_automatismes = len(level_data.get("automatismes_detailed", []) or level_data.get("automatismes", []))
    print(
        f"[OK] {niveau} → {out_path}  "
        f"(compétences: {n_competences} ; automatismes: {n_automatismes})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
