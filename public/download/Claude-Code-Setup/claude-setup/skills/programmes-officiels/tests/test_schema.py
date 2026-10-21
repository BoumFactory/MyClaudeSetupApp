"""Tests structurels : tous les JSON niveau valident le JSON Schema."""
import json
from pathlib import Path

import jsonschema
import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = SKILL_DIR / "data" / "json"
SCHEMA = json.load(open(JSON_DIR / "schema.json", encoding="utf-8"))

NIVEAU_FILES = sorted(
    p for p in JSON_DIR.glob("*.json")
    if p.name not in ("schema.json", "all_flat.json")
)


@pytest.mark.parametrize("path", NIVEAU_FILES, ids=lambda p: p.stem)
def test_niveau_valide_schema(path: Path):
    data = json.load(open(path, encoding="utf-8"))
    jsonschema.validate(data, SCHEMA)


def test_au_moins_10_niveaux():
    """Cible 2026 : 10 niveaux extraits (5E, 4E, 3E, 2GT, 1SPE, 1ENS, 1TEC, TSPE, TCOMP, TTEC)."""
    assert len(NIVEAU_FILES) >= 10
