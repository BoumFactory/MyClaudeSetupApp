"""Tests de validate_progression.py."""

from __future__ import annotations

import pytest

from validate_progression import (
    codes_from_v2_json,
    Report,
    validate,
)


def test_codes_5E_contient_competences_et_automatismes():
    codes = codes_from_v2_json("5E")
    # 110 compétences + 53 automatismes côté JSON v2 (état 2026-05-21).
    assert len(codes) >= 160
    # Quelques codes attendus.
    assert any(c.startswith("5E-GEO-") for c in codes)
    assert any(c.startswith("5E-NB-") for c in codes)
    # Codes d'automatismes au format 🅰5E🛠N.
    assert any("🅰5E🛠" in c for c in codes)


def test_codes_inconnu_leve_erreur():
    valid = {"5E-GEO-001", "5E-GEO-002"}
    prog = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": [
                {"type": "objectif", "code": "5E-GEO-001"},
                {"type": "objectif", "code": "5E-XX-999"},
            ]}
        ]
    }
    r = Report()
    validate(prog, valid, r)
    assert r.has_errors()
    assert any("5E-XX-999" in e for e in r.errors)


def test_doublon_genere_warning_pas_erreur():
    valid = {"5E-GEO-001"}
    prog = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": [
                {"type": "objectif", "code": "5E-GEO-001"},
                {"type": "objectif", "code": "5E-GEO-001"},
            ]}
        ]
    }
    r = Report()
    validate(prog, valid, r)
    assert not r.has_errors()
    assert any("doublon" in w.lower() for w in r.warnings)


def test_type_invalide_leve_erreur():
    valid = {"5E-GEO-001"}
    prog = {
        "niveau": "5E",
        "elements": [
            {"type": "foobar"},  # type racine invalide
            {"type": "sequence", "titre": "S1", "contenu": [
                {"type": "machin"},  # type contenu invalide
            ]},
        ]
    }
    r = Report()
    validate(prog, valid, r)
    assert r.has_errors()
    # Deux erreurs distinctes.
    assert len(r.errors) >= 2


def test_niveau_invalide_leve_erreur():
    prog = {"niveau": "XYZ", "elements": []}
    r = Report()
    validate(prog, set(), r)
    assert r.has_errors()


def test_objectif_sans_code_leve_erreur():
    valid = {"5E-GEO-001"}
    prog = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": [
                {"type": "objectif"},  # pas de "code"
            ]},
        ]
    }
    r = Report()
    validate(prog, valid, r)
    assert r.has_errors()
    assert any("code" in e and "manquant" in e for e in r.errors)


def test_progression_minimaliste_valide():
    valid = {"5E-GEO-001"}
    prog = {
        "niveau": "5E",
        "elements": [
            {"type": "sequence", "titre": "S1", "contenu": [
                {"type": "objectif", "code": "5E-GEO-001"},
            ]},
            {"type": "vacances", "label": "Toussaint"},
        ]
    }
    r = Report()
    validate(prog, valid, r)
    assert not r.has_errors()
    assert r.stats["sequences"] == 1
    assert r.stats["vacances"] == 1
    assert r.stats["objectifs_places"] == 1
