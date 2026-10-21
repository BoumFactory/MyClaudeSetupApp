"""Tests d'idempotence et de complétude du miroir markdown.

Spec §2.2bis : re-exécuter `06_export_markdown.py` ne doit modifier aucun fichier
si les JSON source n'ont pas bougé. R-10 : le markdown est un dérivé pur des
JSON niveau, jamais édité à la main.

Trois invariants :
1. Chaque compétence du `all_flat.json` a son `.md` miroir.
2. Aucun `.md` orphelin (code disparu) ne traîne dans `data/markdown/`.
3. Re-générer tous les `.md` ne modifie aucun fichier (hash global stable).

Le test 3 invoque le script en subprocess car celui-ci réécrit `sys.stdout`
au chargement (UTF-8 forcing), ce qui casse la capture pytest si on l'importait.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parent.parent
ALL_FLAT = SKILL_DIR / "data" / "json" / "all_flat.json"
MD_DIR = SKILL_DIR / "data" / "markdown"
EXPORT_SCRIPT = SKILL_DIR / "scripts" / "build" / "06_export_markdown.py"

DOMAIN_KEBAB = {
    "NB": "nombres", "AL": "algebre", "AN": "analyse",
    "GEO": "geometrie", "GM": "grandeurs-mesures",
    "STA": "statistiques", "PR": "probabilites",
    "OGD": "organisation-gestion-donnees",
    "ALGO": "algorithmique", "TRG": "trigonometrie", "LOG": "logique",
}
CYCLE_OF_NIVEAU = {
    "CM1": "ecole/cycle3", "CM2": "ecole/cycle3", "6E": "ecole/cycle3",
    "5E": "college/cycle4", "4E": "college/cycle4", "3E": "college/cycle4",
    "2GT": "lycee", "1SPE": "lycee", "1ENS": "lycee", "1TEC": "lycee",
    "TSPE": "lycee", "TCOMP": "lycee", "TTEC": "lycee",
}


def _md_path_for(c: dict) -> Path:
    cycle = CYCLE_OF_NIVEAU[c["niveau"]]
    dom_k = DOMAIN_KEBAB.get(c["domaine"], c["domaine"].lower())
    return MD_DIR / cycle / c["niveau"] / dom_k / f"{c['code']}.md"


def _load_all_comps():
    return json.load(open(ALL_FLAT, encoding="utf-8"))["competences"]


def _snapshot_md_tree() -> dict[str, str]:
    """Retourne {chemin_relatif: sha256} pour tous les .md sous data/markdown/."""
    out: dict[str, str] = {}
    for md in MD_DIR.rglob("*.md"):
        h = hashlib.sha256(md.read_bytes()).hexdigest()
        out[str(md.relative_to(MD_DIR)).replace("\\", "/")] = h
    return out


def test_chaque_competence_a_son_md():
    """Tout code listé dans all_flat doit avoir un .md miroir."""
    manquants = []
    for c in _load_all_comps():
        if not _md_path_for(c).exists():
            manquants.append(c["code"])
    assert not manquants, (
        f"{len(manquants)} fichier(s) .md manquant(s) (5 premiers : {manquants[:5]})"
    )


def test_pas_de_md_orphelin():
    """Aucun .md miroir ne doit subsister sans compétence correspondante.

    Détecte les codes supprimés/renommés dont le .md n'a pas été nettoyé.
    Seuls les fichiers nommés comme un code de compétence sont contrôlés.
    """
    codes_valides = {c["code"] for c in _load_all_comps()}
    orphelins = []
    for md in MD_DIR.rglob("*.md"):
        code = md.stem
        if "-" not in code or code.count("-") < 2:
            continue
        if code not in codes_valides:
            orphelins.append(str(md.relative_to(MD_DIR)))
    assert not orphelins, (
        f"{len(orphelins)} .md orphelin(s) (5 premiers : {orphelins[:5]})"
    )


def test_export_markdown_est_idempotent():
    """Spec §2.2bis : re-générer le markdown ne doit modifier aucun fichier."""
    before = _snapshot_md_tree()
    assert before, "Aucun .md trouvé sous data/markdown/ — rien à vérifier."

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        [sys.executable, str(EXPORT_SCRIPT)],
        cwd=str(SKILL_DIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, (
        f"Échec du script 06_export_markdown.py "
        f"(stdout={result.stdout!r}, stderr={result.stderr!r})"
    )

    after = _snapshot_md_tree()

    nouveaux = set(after) - set(before)
    disparus = set(before) - set(after)
    modifies = [p for p in after.keys() & before.keys() if after[p] != before[p]]

    msg = []
    if nouveaux:
        msg.append(f"{len(nouveaux)} nouveau(x) (5 : {sorted(nouveaux)[:5]})")
    if disparus:
        msg.append(f"{len(disparus)} disparu(s) (5 : {sorted(disparus)[:5]})")
    if modifies:
        msg.append(f"{len(modifies)} modifié(s) (5 : {modifies[:5]})")
    assert not (nouveaux or disparus or modifies), (
        "Export markdown non idempotent : " + " | ".join(msg)
    )
