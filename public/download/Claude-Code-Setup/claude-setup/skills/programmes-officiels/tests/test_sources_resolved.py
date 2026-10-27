"""Tests d'intégrité : chaque source.page_image pointe vers un dossier de pages dont le PDF source existe.

Les PNG ne sont pas fournis : ils se régénèrent par scripts/regenerer_pages.py."""
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = SKILL_DIR / "data" / "json"


def _all_comps():
    out = []
    for f in JSON_DIR.glob("*.json"):
        if f.name in ("schema.json", "all_flat.json"):
            continue
        data = json.load(open(f, encoding="utf-8"))
        for dom, themes in data.get("competences_by_theme", {}).items():
            for theme, comps in themes.items():
                out.extend(comps)
    return out


def test_toutes_sources_resolvent_vers_un_pdf():
    mapping = json.load(open(SKILL_DIR / "data" / "pdf" / "_mapping.json", encoding="utf-8"))["files"]
    missing = []
    for c in _all_comps():
        rel = c.get("source", {}).get("page_image")
        assert rel, f"Compétence {c['code']} sans page_image"
        folder = Path(rel).parent.name
        if not any(e["page_folder"] == folder and (SKILL_DIR / "data" / "pdf" / pdf).exists()
                   for pdf, e in mapping.items()):
            missing.append((c["code"], rel))
    assert not missing, f"{len(missing)} sources sans PDF (5 premières : {missing[:5]})"


def test_source_page_strictement_positive():
    for c in _all_comps():
        page = c.get("source", {}).get("page")
        assert isinstance(page, int) and page >= 1, f"{c['code']} : page invalide ({page})"
