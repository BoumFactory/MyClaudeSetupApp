"""Tests de apply_progression.py (gabarit v2 : injection dans le snapshot).

On part de la fiche vierge 5E déjà générée dans out/, on lui applique un JSON
minimal et on relit le snapshot écrit dans la balise __snapshot__.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from _utils import read_snapshot
from apply_progression import (
    apply_progression,
    build_objectifs_index,
    texte_to_html,
)
from validate_progression import Report, codes_from_html, validate

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
EXEMPLE = ROOT / "assets" / "exemple_progression.json"


@pytest.fixture(scope="module")
def html_5E_vierge() -> str:
    path = OUT / "progression_5E_vierge.html"
    if not path.exists():
        pytest.skip("HTML 5E vierge non généré — lancer generate_vierge d'abord.")
    return path.read_text(encoding="utf-8")


def test_index_5E_indexe_tous_les_codes(html_5E_vierge):
    idx = build_objectifs_index(html_5E_vierge)
    # 121 compétences + 47 automatismes (état 2026-05-21).
    assert len(idx) >= 160
    for code, data in idx.items():
        assert data["text"]
        assert data["theme"]
        assert data["subtheme"]


def test_apply_injecte_les_codes_demandes(html_5E_vierge):
    progression = {
        "niveau": "5E",
        "titre": "Ma progression de 5e",
        "elements": [
            {"type": "sequence", "titre": "S1 — Test",
             "contenu": [
                 {"type": "objectif", "code": "5E-GEO-001"},
                 {"type": "commentaire", "titre": "Note",
                  "texte": "ressource <X>\nvoir https://eduscol.education.fr/"},
             ]},
            {"type": "vacances", "label": "Toussaint"},
        ],
    }
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    snap = read_snapshot(out)
    assert snap["title"] == "Ma progression de 5e"
    seq, vac = snap["sequences"]
    assert seq["type"] == "sequence" and seq["title"] == "S1 — Test"
    assert [i["code"] for i in seq["items"]] == ["5E-GEO-001"]
    # Les champs lus par _restoreSequences() sont présents.
    assert {"text", "theme", "subtheme"} <= set(seq["items"][0])
    com = seq["comments"][0]
    assert com["label"] == "Note" and com["open"] is True
    assert "&lt;X&gt;<br>" in com["html"]
    assert '<a href="https://eduscol.education.fr/"' in com["html"]
    assert vac == {"type": "separateur", "text": "Toussaint", "color": "#c8a200"}
    # Le reste de la fiche (JS, DATA, PDF embarqué) est intact.
    assert out.count("/* __DATA_START__ */") == 1
    assert len(out) > len(html_5E_vierge)


def test_apply_snapshot_ne_ferme_pas_la_balise(html_5E_vierge):
    progression = {"niveau": "5E", "elements": [
        {"type": "sequence", "titre": "Piège </script> dans un titre", "contenu": []}]}
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    assert read_snapshot(out)["sequences"][0]["title"] == "Piège </script> dans un titre"


def test_apply_code_inconnu_warn_pas_crash(html_5E_vierge, capsys):
    progression = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1",
             "contenu": [{"type": "objectif", "code": "5E-ZZ-999"}]},
        ],
    }
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    captured = capsys.readouterr()
    assert "5E-ZZ-999" in captured.err
    assert read_snapshot(out)["sequences"][0]["items"] == []


def test_apply_doublon_garde_la_premiere_place(html_5E_vierge, capsys):
    progression = {"niveau": "5E", "elements": [
        {"type": "sequence", "titre": "S1", "contenu": [{"code": "5E-GEO-001"}]},
        {"type": "sequence", "titre": "S2", "contenu": [{"code": "5E-GEO-001"}]},
    ]}
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    s1, s2 = read_snapshot(out)["sequences"]
    assert len(s1["items"]) == 1 and s2["items"] == []
    assert "doublon" in capsys.readouterr().err


def test_apply_separateur_interne_devient_commentaire(html_5E_vierge):
    progression = {"niveau": "5E", "elements": [
        {"type": "sequence", "titre": "S1", "contenu": [
            {"type": "objectif", "code": "5E-GEO-001"},
            {"type": "separateur", "label": "Exos / RdP"},
            {"type": "objectif", "code": "5E-GEO-002"},
        ]}]}
    seq = read_snapshot(apply_progression(html_5E_vierge, progression,
                                          show_stats=False))["sequences"][0]
    assert len(seq["items"]) == 2
    assert seq["comments"][0]["label"] == "🛠 Exos / RdP"
    assert "5E-GEO-002" in seq["comments"][0]["html"]


def test_apply_conserver_intro_sans_effet(html_5E_vierge):
    # Le gabarit v2 n'a pas de séquence d'intro : la clé est acceptée, ignorée.
    for keep in (True, False):
        progression = {"niveau": "5E", "conserver_intro": keep, "elements": [
            {"type": "sequence", "titre": "S1", "contenu": []}]}
        out = apply_progression(html_5E_vierge, progression, show_stats=False)
        assert [s["title"] for s in read_snapshot(out)["sequences"]] == ["S1"]


def test_apply_sur_fiche_deja_remplie_remplace(html_5E_vierge):
    p1 = {"niveau": "5E", "elements": [{"type": "sequence", "titre": "A", "contenu": []}]}
    p2 = {"niveau": "5E", "elements": [{"type": "sequence", "titre": "B", "contenu": []}]}
    once = apply_progression(html_5E_vierge, p1, show_stats=False)
    twice = apply_progression(once, p2, show_stats=False)
    assert [s["title"] for s in read_snapshot(twice)["sequences"]] == ["B"]
    assert twice.count("__SNAPSHOT_START__ -->") == html_5E_vierge.count("__SNAPSHOT_START__ -->")


def test_texte_to_html_echappe_et_lie():
    assert texte_to_html("a & b") == "a &amp; b"
    assert texte_to_html("x\ny") == "x<br>y"
    assert "<a href=" in texte_to_html("voir https://example.org/page")


def test_exemple_valide_puis_applique(html_5E_vierge, tmp_path):
    progression = json.loads(EXEMPLE.read_text(encoding="utf-8"))
    html_path = OUT / "progression_5E_vierge.html"
    report = Report()
    validate(progression, codes_from_html(html_path), report)
    assert not report.has_errors(), report.errors
    out = apply_progression(html_5E_vierge, progression, show_stats=False)
    seqs = read_snapshot(out)["sequences"]
    assert sum(1 for s in seqs if s["type"] == "sequence") == 3
    assert sum(1 for s in seqs if s["type"] == "separateur") == 2


def test_codes_from_html_lit_le_referentiel(html_5E_vierge):
    codes = codes_from_html(OUT / "progression_5E_vierge.html")
    assert len(codes) >= 160
    assert "5E-GEO-001" in codes
