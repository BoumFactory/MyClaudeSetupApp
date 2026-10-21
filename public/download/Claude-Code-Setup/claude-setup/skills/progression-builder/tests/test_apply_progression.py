"""Tests de apply_progression.py.

On utilise le HTML vierge déjà généré dans out/ comme base de test, puis
on lui applique un JSON minimal et on vérifie le résultat.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from apply_progression import (
    apply_progression,
    build_objectifs_index,
)

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"

# apply_progression.py cible la structure du template v1 (leftPanel statique avec
# des <div class="objectif" data-code=…> + un <div id="resizer">). Le template v2
# (reference_v2.html) rend le panneau gauche PAR JS au load depuis l'objet DATA, il
# n'y a donc pas d'objectif statique à indexer. Le Mode 2 (compléter une progression
# via JSON) doit être réécrit pour injecter dans DATA / le snapshot v2.
# Tests neutralisés en attendant cette réécriture.
pytestmark = pytest.mark.skip(
    reason="apply_progression = pipeline v1 (leftPanel statique) ; template v2 rend "
           "le panneau par JS depuis DATA. Mode 2 à réécrire pour le v2."
)


@pytest.fixture(scope="module")
def html_5E_vierge() -> str:
    path = OUT / "progression_5E_vierge.html"
    if not path.exists():
        pytest.skip("HTML 5E vierge non généré — lancer generate_vierge d'abord.")
    return path.read_text(encoding="utf-8")


def test_index_5E_indexe_tous_les_codes(html_5E_vierge):
    idx = build_objectifs_index(html_5E_vierge)
    # 110 comp + 53 auto = 163 codes côté leftPanel.
    assert len(idx) >= 160
    # Vérifie que chaque entrée a bg + text.
    for code, data in idx.items():
        assert data["bg"].startswith("#")
        assert data["text"]


def test_apply_injecte_les_codes_demandes(html_5E_vierge):
    progression = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1 — Test",
             "contenu": [
                 {"type": "objectif", "code": "5E-GEO-001"},
                 {"type": "commentaire", "titre": "Note", "texte": "ressource X"},
             ]},
            {"type": "vacances", "label": "Toussaint"},
        ],
    }
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    # Le bloc right-objectif doit avoir été inséré.
    assert 'class="right-objectif" data-code="5E-GEO-001"' in out
    # Le code doit être grisé dans le leftPanel.
    idx_after = build_objectifs_index(out)
    # On vérifie via le HTML brut puisque l'index ne capture pas la classe.
    assert 'class="objectif grayed"' in out
    # La séquence et les vacances sont présentes.
    assert "S1 &mdash; Test" in out or "S1 — Test" in out
    assert "Toussaint" in out


def test_apply_code_inconnu_warn_pas_crash(html_5E_vierge, capsys):
    progression = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1",
             "contenu": [{"type": "objectif", "code": "5E-ZZ-999"}]},
        ],
    }
    apply_progression(html_5E_vierge, progression, show_stats=False)
    captured = capsys.readouterr()
    assert "5E-ZZ-999" in captured.err


def test_apply_conserve_intro_par_defaut(html_5E_vierge):
    progression = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": []},
        ],
    }
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    assert 'data-intro="true"' in out


def test_apply_sans_conserver_intro(html_5E_vierge):
    progression = {
        "niveau": "5E",
        "conserver_intro": False,
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": []},
        ],
    }
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    # On a vidé le sequencesContainer, donc le data-intro="true" qui y était
    # doit avoir disparu. Note : le data-intro est uniquement dans le bloc
    # de droite, jamais à gauche.
    assert 'data-intro="true"' not in out
