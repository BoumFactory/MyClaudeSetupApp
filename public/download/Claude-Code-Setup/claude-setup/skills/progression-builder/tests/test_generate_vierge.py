"""Tests de generate_vierge.py (architecture v2 : template reference_v2.html,
DATA/CONFIG injectés entre marqueurs, panneau gauche rendu par JS au load).

On régénère pour chaque niveau et on vérifie sur l'objet DATA injecté :
  - DATA parse correctement (injection OK),
  - nombre d'items = compétences + automatismes du JSON,
  - codes uniques,
  - titre contenant le label du niveau,
  - garde anti-régression : aucun grand domaine « Analyse » au collège,
  - cycle 3 (CM1/CM2/6E) : présence du grand domaine « Grandeurs et mesures » si GM.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from generate_vierge import rebuild_html
from _utils import NIVEAU_LABEL, COLLEGE_NIVEAUX, CYCLE3_NIVEAUX

ROOT = Path(__file__).resolve().parent.parent
V2_JSON_DIR = ROOT.parents[0] / "programmes-officiels" / "data" / "json"
REFERENCE = ROOT / "assets" / "reference_v2.html"

NIVEAUX = ["CM1", "CM2", "6E", "5E", "4E", "3E",
           "2GT", "1SPE", "1ENS", "1TEC", "TSPE", "TCOMP", "TTEC"]


@pytest.fixture(scope="module")
def reference_html() -> str:
    return REFERENCE.read_text(encoding="utf-8")


def _level_data(niveau: str) -> dict:
    return json.loads((V2_JSON_DIR / f"{niveau}.json").read_text(encoding="utf-8"))


def _parse_data(html: str) -> dict:
    m = re.search(r"/\* __DATA_START__ \*/\s*let DATA = (\{.*?\});\s*/\* __DATA_END__ \*/",
                  html, re.DOTALL)
    assert m, "objet DATA introuvable dans le HTML généré"
    return json.loads(m.group(1))


def _items(data: dict):
    n, codes = 0, []
    for blk in data.values():
        for v in blk.get("themes", {}).values():
            lst = v if isinstance(v, list) else v.get("items", [])
            for it in lst:
                n += 1
                if it.get("code"):
                    codes.append(it["code"])
    return n, codes


@pytest.mark.parametrize("niveau", NIVEAUX)
def test_nombre_items(niveau: str, reference_html: str):
    data = _level_data(niveau)
    html = rebuild_html(reference_html, data, niveau)
    n, _ = _items(_parse_data(html))
    attendu = data["meta"]["total_competences"] + len(data.get("automatismes", []))
    assert n == attendu, f"{niveau}: {n} items dans DATA, attendu {attendu}"


@pytest.mark.parametrize("niveau", NIVEAUX)
def test_codes_uniques(niveau: str, reference_html: str):
    data = _level_data(niveau)
    html = rebuild_html(reference_html, data, niveau)
    _, codes = _items(_parse_data(html))
    doublons = [c for c in set(codes) if codes.count(c) > 1]
    assert not doublons, f"{niveau}: codes en doublon : {doublons[:5]}"


@pytest.mark.parametrize("niveau", NIVEAUX)
def test_titre_label(niveau: str, reference_html: str):
    data = _level_data(niveau)
    html = rebuild_html(reference_html, data, niveau)
    label = NIVEAU_LABEL[niveau]
    assert label in html or label.replace("'", "&#39;") in html, \
        f"{niveau}: label '{label}' absent du HTML"


@pytest.mark.parametrize("niveau", [n for n in NIVEAUX if n in COLLEGE_NIVEAUX])
def test_pas_d_analyse_au_college(niveau: str, reference_html: str):
    data = _level_data(niveau)
    html = rebuild_html(reference_html, data, niveau)
    keys = list(_parse_data(html).keys())
    assert not any("Analyse" in k for k in keys), \
        f"{niveau}: grand domaine « Analyse » présent au collège : {keys}"


@pytest.mark.parametrize("niveau", [n for n in NIVEAUX if n in CYCLE3_NIVEAUX])
def test_grandeurs_et_mesures_cycle3(niveau: str, reference_html: str):
    """Au cycle 3, GM doit former le grand domaine « Grandeurs et mesures »."""
    data = _level_data(niveau)
    if "GM" not in data["stats"].get("by_domaine", {}):
        pytest.skip(f"{niveau} sans domaine GM")
    html = rebuild_html(reference_html, data, niveau)
    keys = list(_parse_data(html).keys())
    assert any("Grandeurs et mesures" in k for k in keys), \
        f"{niveau}: « Grandeurs et mesures » attendu comme grand domaine : {keys}"
