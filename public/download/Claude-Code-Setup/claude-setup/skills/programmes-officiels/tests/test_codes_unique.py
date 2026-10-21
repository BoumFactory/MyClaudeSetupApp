"""Tests d'unicité des codes de compétence sur l'ensemble des niveaux."""
import json
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"
CODE_RE = re.compile(r"^[A-Z0-9]+-[A-Z]{2,4}-[0-9]{3}$")


def _load():
    return json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]


def test_codes_uniques_globalement():
    comps = _load()
    codes = [c["code"] for c in comps]
    assert len(codes) == len(set(codes)), f"Doublons : {sorted(set(c for c in codes if codes.count(c) > 1))}"


def test_codes_format_canonique():
    comps = _load()
    invalides = [c["code"] for c in comps if not CODE_RE.match(c["code"])]
    assert not invalides, f"Codes au format invalide : {invalides[:5]}"


def test_au_moins_500_competences():
    """Cible 2026 : au moins 500 compétences extraites mécaniquement."""
    comps = _load()
    assert len(comps) >= 500
