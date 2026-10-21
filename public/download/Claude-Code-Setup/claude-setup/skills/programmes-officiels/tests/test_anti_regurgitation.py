"""Tests de la directive anti-régurgitation.

Vérifie que toutes les compétences ont été générées par le pipeline mécanique
(extraction_method == 'mechanical_from_bullets'). Aucune compétence ne doit
porter une trace de génération LLM sur le champ formulation_bo.
"""
import json
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"


def _load():
    return json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]


def test_extraction_method_est_mecanique():
    """Anti-régurgitation : aucune compétence ne doit avoir été générée par LLM."""
    comps = _load()
    suspects = []
    for c in comps:
        em = c.get("extraction_meta", {})
        method = em.get("extraction_method")
        if method != "mechanical_from_bullets":
            suspects.append((c["code"], method))
    assert not suspects, (
        f"{len(suspects)} compétences avec extraction_method != 'mechanical_from_bullets' "
        f"(5 premières : {suspects[:5]})"
    )


def test_formulation_bo_jamais_vide():
    comps = _load()
    vides = [c["code"] for c in comps if not (c.get("formulation_bo") or "").strip()]
    assert not vides, f"{len(vides)} compétences avec formulation_bo vide : {vides[:5]}"


def test_intitule_egal_formulation_bo():
    """Vérification corollaire : l'intitulé d'une compétence mécanique est le bullet BO verbatim."""
    comps = _load()
    diffs = [c["code"] for c in comps if c.get("intitule", "") != c.get("formulation_bo", "")]
    assert not diffs, (
        f"{len(diffs)} compétences où intitule != formulation_bo (suggère retouche LLM) : "
        f"{diffs[:5]}"
    )
