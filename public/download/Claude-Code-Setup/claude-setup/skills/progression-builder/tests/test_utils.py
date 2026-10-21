"""Tests des utilitaires de _utils.py."""

from __future__ import annotations

import _utils as U


def test_palette_couvre_tous_les_domaines():
    attendus = {"NB", "AL", "AN", "GEO", "GM", "STA", "PR", "OGD", "ALGO", "TRG", "LOG"}
    assert attendus.issubset(U.DOMAINE_INFO.keys())
    for k, info in U.DOMAINE_INFO.items():
        assert {"label", "color", "emoji"}.issubset(info.keys())
        assert info["color"].startswith("#")
        assert len(info["color"]) == 7


def test_niveau_label_couvre_les_13_niveaux():
    attendus = {"CM1", "CM2", "6E", "5E", "4E", "3E",
                "2GT", "1SPE", "1ENS", "1TEC", "TSPE", "TCOMP", "TTEC"}
    assert attendus == set(U.NIVEAU_LABEL.keys())


def test_shade_color_eclaircit():
    base = "#a30f33"
    s0 = U.shade_color(base, 0)
    s2 = U.shade_color(base, 2)
    # step=0 doit redonner ~la même couleur (à l'arrondi près).
    assert s0.lower() == base.lower() or s0.lower().startswith("#a")
    # step=2 doit être plus clair → composante R plus haute.
    assert int(s2[1:3], 16) > int(base[1:3], 16) or int(s2[3:5], 16) > int(base[3:5], 16)


def test_html_escape_basique():
    assert U.html_escape("<a>&\"'") == "&lt;a&gt;&amp;&quot;&#39;"


def test_slugify_supprime_accents():
    assert U.slugify("Géométrie & co !") == "geometrie-co"
    assert U.slugify("") == "x"
