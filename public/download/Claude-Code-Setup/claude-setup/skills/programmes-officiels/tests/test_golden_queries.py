"""Tests des golden queries : 30+ requêtes de référence figées contre l'index FTS5.

Chaque requête est lue depuis tests/fixtures/golden_queries.json et exécutée
contre data/search_index.sqlite. La même logique de filtrage que scripts/search.py
est appliquée (FTS5 puis filtres structurels niveau/domaine/type via all_flat.json).

Toute évolution de l'extraction qui casse une attente sera capturée ici.
"""
import json
import sqlite3
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "golden_queries.json"
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"
FTS = SKILL_DIR / "data" / "search_index.sqlite"


def _load_queries():
    return json.load(open(FIXTURES, encoding="utf-8"))["queries"]


def _load_competences_by_code():
    flat = json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]
    return {c["code"]: c for c in flat}


def _run_fts_competences(keyword: str) -> list[str]:
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    cur.execute(
        "SELECT code FROM competences_fts WHERE competences_fts MATCH ? ORDER BY rank LIMIT 500",
        (keyword,),
    )
    rows = [r[0] for r in cur.fetchall()]
    con.close()
    return rows


def _run_fts_automatismes(keyword: str, niveau: str | None) -> list[dict]:
    con = sqlite3.connect(str(FTS))
    cur = con.cursor()
    sql = "SELECT auto_id, niveau FROM automatismes_fts WHERE automatismes_fts MATCH ?"
    params: list = [keyword]
    if niveau:
        sql += " AND niveau = ?"
        params.append(niveau)
    sql += " ORDER BY rank LIMIT 500"
    cur.execute(sql, params)
    rows = [{"auto_id": r[0], "niveau": r[1]} for r in cur.fetchall()]
    con.close()
    return rows


def _apply_structural_filters(comps: list[dict], q: dict) -> list[dict]:
    out = comps
    if q.get("niveau"):
        out = [c for c in out if c["niveau"] == q["niveau"]]
    if q.get("domaine"):
        out = [c for c in out if c["domaine"] == q["domaine"]]
    if q.get("type"):
        out = [c for c in out if c["type"] == q["type"]]
    return out


def _execute(q: dict, by_code: dict) -> tuple[list[dict], list[dict]]:
    """Retourne (compétences, automatismes) selon la query.

    - Si keyword fourni : FTS5 puis filtres structurels.
    - Sinon : balayage de all_flat avec filtres structurels uniquement.
    - scope='automatismes' : ne renvoie que la liste automatismes (compétences vides).
    """
    scope = q.get("scope", "competences")
    keyword = q.get("keyword")

    if scope == "automatismes":
        if not keyword:
            return [], []
        return [], _run_fts_automatismes(keyword, q.get("niveau"))

    if keyword:
        codes = _run_fts_competences(keyword)
        comps = [by_code[c] for c in codes if c in by_code]
    else:
        comps = list(by_code.values())

    comps = _apply_structural_filters(comps, q)
    return comps, []


def _gq_id(gq):
    return gq["id"]


QUERIES = _load_queries()


def test_au_moins_30_golden_queries():
    """Spec : viser au minimum 30 requêtes couvrant niveaux × types × domaines."""
    assert len(QUERIES) >= 30, f"Seulement {len(QUERIES)} golden queries (cible : 30)"


@pytest.mark.parametrize("gq", QUERIES, ids=_gq_id)
def test_golden_query(gq):
    by_code = _load_competences_by_code()
    comps, autos = _execute(gq["query"], by_code)
    expect = gq.get("expect", {})

    # Codes effectivement retournés (compétences) ou ids (automatismes)
    codes_set = {c["code"] for c in comps}
    n_comps = len(comps)
    n_autos = len(autos)
    n_total = n_comps if gq["query"].get("scope", "competences") != "automatismes" else n_autos

    # must_contain_codes (compétences)
    for code in expect.get("must_contain_codes", []):
        assert code in codes_set, (
            f"{gq['id']} : code attendu '{code}' absent — résultats ({n_comps}) : "
            f"{sorted(codes_set)[:10]}…"
        )

    # must_contain_one_of (compétences)
    one_of = expect.get("must_contain_one_of")
    if one_of:
        intersection = codes_set.intersection(one_of)
        assert intersection, (
            f"{gq['id']} : aucun des codes attendus {one_of} trouvé — "
            f"résultats ({n_comps}) : {sorted(codes_set)[:10]}…"
        )

    # must_not_contain_codes
    for code in expect.get("must_not_contain_codes", []):
        assert code not in codes_set, (
            f"{gq['id']} : code interdit '{code}' présent dans les résultats"
        )

    # min_results
    if "min_results" in expect:
        assert n_total >= expect["min_results"], (
            f"{gq['id']} : {n_total} résultats < min {expect['min_results']}"
        )

    # max_results
    if "max_results" in expect:
        assert n_total <= expect["max_results"], (
            f"{gq['id']} : {n_total} résultats > max {expect['max_results']}"
        )

    # all_niveau_in
    if "all_niveau_in" in expect and comps:
        bad = [(c["code"], c["niveau"]) for c in comps if c["niveau"] not in expect["all_niveau_in"]]
        assert not bad, (
            f"{gq['id']} : niveaux hors {expect['all_niveau_in']} : {bad[:5]}"
        )

    # all_type_in
    if "all_type_in" in expect and comps:
        bad = [(c["code"], c["type"]) for c in comps if c["type"] not in expect["all_type_in"]]
        assert not bad, (
            f"{gq['id']} : types hors {expect['all_type_in']} : {bad[:5]}"
        )
