"""Retrouve, sur n'importe quel poste, ce dont le skill a besoin : paquets `@local/farfadet-*`, version
installée, polices, outils de la suite (bfwatch, index des fonctions), outil de rendu des extraits LaTeX.

Aucun chemin propre à un poste n'est écrit en dur. Ordre de recherche :

1. variables d'environnement (facultatives) : `BFCOURS_TYPST_SUITE` (dossier de la suite ou du dépôt),
   `BFCOURS_TYPST_POLICES` (dossier des polices) ;
2. le dossier des paquets locaux de Typst (`%APPDATA%/typst/packages/local` sous Windows,
   `~/Library/Application Support/typst/packages/local` sous macOS, `$XDG_DATA_HOME/typst/packages/local`
   ou `~/.local/share/typst/packages/local` ailleurs) : quand `farfadet-socle` y est un
   lien, sa cible mène au dépôt, donc aux polices et aux outils ;
3. le fichier `chemin-suite.txt` du skill (écrit par `installer.py --skill`), qui note le dépôt de la suite ;
4. les dossiers parents du skill et du dossier courant : le dépôt (le skill est dans `tools/skill/`).

Usage en ligne de commande (diagnostic) :
    python localiser.py            # ce qui a été trouvé, et ce qui manque
    python localiser.py --json     # même chose, en JSON
"""
from __future__ import annotations

import json
import os
import platform
import re
import sys
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional

SKILL = Path(__file__).resolve().parent.parent
DONNEES = SKILL / "scripts" / "donnees"
POLICE_TEMOIN = "BfcoursMaths-Regular.otf"

# Forme des imports écrits par le skill. En développement, la suite est le méta-paquet `@local/farfadet` (un paquet
# `@local/farfadet-*` par partie). Dans le dépôt publié, l'exporteur passe PUBLIE à True : la suite est alors le paquet
# aplati `@preview/farfadet` (Typst Universe, ou sa copie posée dans le cache de Typst par l'installateur), dont chaque
# partie est un module (`exercices`, `zones-reponse`…). Le reste du skill passe par les fonctions ci-dessous.
PUBLIE = True
VERSION_PAR_DEFAUT = "0.2.0"
NOM_PREVIEW = "farfadet"
ANCIEN_NOM_PREVIEW = "bfcours"      # nom du paquet avant le renommage du 21/10/2026 : reconnu, jamais écrit
MODULES = {
    "farfadet-socle": "socle", "farfadet-didactique": "didactique", "farfadet-enum": "enumerations",
    "farfadet-tableaux": "tableaux", "farfadet-crep": "zones-reponse", "farfadet-exo": "exercices", "farfadet-qcm": "qcm",
    "farfadet-maths": "maths", "farfadet-modele": "modeles", "farfadet-extras": "extras", "farfadet-latex": "extraits-latex",
    "farfadet-tabvar": "variations", "farfadet-geom": "geom", "rdboites": "rd-boites", "rdtime": "rd-time",
    "rdratio": "rd-ratio", "rdgrid": "rd-grid", "rdarithm": "rd-arithm", "rdconv": "rd-conv", "rdopp": "rd-opp",
    "rdsheet": "rd-sheet", "rdtabnum": "rd-tabnum",
}


def ref_suite(version: str) -> str:
    """Référence du paquet qui porte toute la suite : `@local/farfadet:V` ou `@preview/farfadet:V`."""
    return f"@preview/{NOM_PREVIEW}:{version}" if PUBLIE else f"@local/farfadet:{version}"


def import_suite(version: str) -> str:
    """Ligne d'import de toute la suite."""
    return f'#import "{ref_suite(version)}": *'


def import_partie_md(paquet: str, version: str) -> str:
    """Phrase Markdown (avec ses codes) qui donne l'import d'une partie de la suite seule."""
    if PUBLIE and paquet in MODULES:
        m = MODULES[paquet]
        return f'`#import "{ref_suite(version)}": {m}` puis `#import {m}: *`'
    return f'`#import "@local/{paquet}:{version}": *`'


def dossier_cache_preview() -> Path:
    """Dossier `preview/` du cache de paquets de Typst (`TYPST_PACKAGE_CACHE_PATH` désigne son parent, comme pour la
    ligne de commande de Typst : `%LOCALAPPDATA%/typst/packages` sous Windows, `~/Library/Caches/typst/packages` sous
    macOS, `$XDG_CACHE_HOME/typst/packages` ou `~/.cache/typst/packages` ailleurs)."""
    env = os.environ.get("TYPST_PACKAGE_CACHE_PATH")
    if env:
        return Path(env) / "preview"
    systeme = platform.system()
    if systeme == "Windows":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(base) / "typst" / "packages" / "preview"
    if systeme == "Darwin":
        return Path.home() / "Library" / "Caches" / "typst" / "packages" / "preview"
    base = os.environ.get("XDG_CACHE_HOME") or str(Path.home() / ".cache")
    return Path(base) / "typst" / "packages" / "preview"


def options_paquets() -> Dict[str, str]:
    """Arguments `package_path` / `package_cache_path` du module typst, d'après les variables d'environnement de la
    ligne de commande de Typst (`TYPST_PACKAGE_PATH`, `TYPST_PACKAGE_CACHE_PATH`). Vide si elles ne sont pas définies."""
    options = {}
    if os.environ.get("TYPST_PACKAGE_PATH"):
        options["package_path"] = os.environ["TYPST_PACKAGE_PATH"]
    if os.environ.get("TYPST_PACKAGE_CACHE_PATH"):
        options["package_cache_path"] = os.environ["TYPST_PACKAGE_CACHE_PATH"]
    return options


def dossier_paquets_locaux() -> Path:
    """Dossier `typst/packages/local` du poste (même règle que Typst ; `TYPST_PACKAGE_PATH` l'emporte,
    comme pour la ligne de commande de Typst : il désigne le dossier qui contient `local/`)."""
    env = os.environ.get("TYPST_PACKAGE_PATH")
    if env:
        return Path(env) / "local"
    systeme = platform.system()
    if systeme == "Windows":
        base = os.environ.get("APPDATA") or str(Path.home() / "AppData" / "Roaming")
        return Path(base) / "typst" / "packages" / "local"
    if systeme == "Darwin":
        return Path.home() / "Library" / "Application Support" / "typst" / "packages" / "local"
    base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
    return Path(base) / "typst" / "packages" / "local"


def _cle_version(v: str):
    return tuple(int(x) if x.isdigit() else 0 for x in re.split(r"[.\-]", v))


def versions_installees(nom: str) -> List[str]:
    dossier = dossier_paquets_locaux() / nom
    if not dossier.is_dir():
        return []
    return sorted((d.name for d in dossier.iterdir() if (d / "typst.toml").exists()), key=_cle_version)


def versions_en_cache(nom: str = NOM_PREVIEW) -> List[str]:
    """Versions d'un paquet `@preview` présentes dans le cache de Typst."""
    dossier = dossier_cache_preview() / nom
    if not dossier.is_dir():
        return []
    return sorted((d.name for d in dossier.iterdir() if (d / "typst.toml").exists()), key=_cle_version)


@lru_cache(maxsize=None)
def version_suite() -> Optional[str]:
    """Version installée de la suite (la plus récente), ou None : méta-paquet `@local/farfadet` en développement,
    paquet `@preview/farfadet` du cache de Typst dans le dépôt publié."""
    v = versions_en_cache() if PUBLIE else versions_installees("farfadet")
    return v[-1] if v else None


def dossier_paquet(nom: str) -> Optional[Path]:
    """Dossier réel (lien résolu) d'un paquet local, version la plus récente."""
    v = versions_installees(nom)
    if not v:
        return None
    return (dossier_paquets_locaux() / nom / v[-1]).resolve()


def _est_suite(d: Path) -> bool:
    """Un dossier qui contient les paquets ou les polices de la suite."""
    return d.is_dir() and ((d / "polices" / POLICE_TEMOIN).exists() or (d / "farfadet-socle" / "typst.toml").exists()
                           or (d / "packages" / "local").is_dir())


@lru_cache(maxsize=None)
def suite() -> Optional[Path]:
    """Dossier du dépôt de la suite : celui qui porte `polices/` et les outils."""
    env = os.environ.get("BFCOURS_TYPST_SUITE")
    if env and _est_suite(Path(env)):
        return Path(env).resolve()
    socle = dossier_paquet("farfadet-socle")
    if socle:
        for d in [socle, *socle.parents][:6]:
            if (d / "polices" / POLICE_TEMOIN).exists() or (d / "outils" / "bfwatch.py").exists() \
                    or (d / "tools" / "bfwatch.py").exists():
                return d
    note = SKILL / "chemin-suite.txt"      # écrit par `installer.py --skill` : où est le dépôt de la suite
    if note.is_file():
        lu = note.read_text(encoding="utf-8").strip()
        if lu and _est_suite(Path(lu)):
            return Path(lu).resolve()
    for depart in (SKILL, Path.cwd()):
        for d in [depart, *depart.parents]:
            # d lui-même : le dépôt (skill rangé dans tools/skill/)
            for cand in (d, d / "bfcours-typst"):
                if _est_suite(cand):
                    return cand.resolve()
    return None


def _premier(*chemins: Optional[Path]) -> Optional[Path]:
    for c in chemins:
        if c and c.exists():
            return c
    return None


@lru_cache(maxsize=None)
def polices() -> Optional[Path]:
    """Dossier des polices de la suite, ou None si elles sont installées dans le système (ou absentes)."""
    env = os.environ.get("BFCOURS_TYPST_POLICES")
    if env and (Path(env) / POLICE_TEMOIN).exists():
        return Path(env).resolve()
    s = suite()
    if s and (s / "polices" / POLICE_TEMOIN).exists():
        return s / "polices"
    for nom in ("farfadet", "farfadet-socle"):
        p = dossier_paquet(nom)
        if p and (p / "polices" / POLICE_TEMOIN).exists():
            return p / "polices"
    return None


def outil(nom: str) -> Optional[Path]:
    """Un outil de la suite : `tools/<nom>`."""
    s = suite()
    if not s:
        return None
    return _premier(s / "outils" / nom, s / "tools" / nom)


def bfwatch() -> Optional[Path]:
    return outil("bfwatch.py")


def rendus_tex() -> Optional[Path]:
    """Script de rendu des extraits LaTeX, livré dans le paquet farfadet-latex."""
    p = dossier_paquet("farfadet-latex")
    s = suite()
    return _premier(p / "outils" / "rendus_tex" / "rendus_tex.py" if p else None,
                    s / "farfadet-latex" / "outils" / "rendus_tex" / "rendus_tex.py" if s else None)


def index_fonctions() -> Optional[Path]:
    """Index des fonctions : celui de la suite s'il existe (toujours à jour), sinon la copie du skill."""
    return _premier(outil("index/index.json"), DONNEES / "index.json")


def module_typst() -> Optional[str]:
    try:
        import typst  # noqa: F401
        return getattr(typst, "__version__", "?")
    except ImportError:
        return None


def module_fitz() -> bool:
    try:
        import fitz  # noqa: F401
        return True
    except ImportError:
        return False


def latex_disponible() -> Optional[str]:
    import shutil
    for moteur in ("lualatex", "pdflatex", "xelatex"):
        chemin = shutil.which(moteur)
        if chemin:
            return chemin
    return None


def bilan() -> Dict[str, object]:
    return {
        "python": sys.executable,
        "module_typst": module_typst(),
        "pymupdf": module_fitz(),
        "paquets_locaux": str(dossier_cache_preview() if PUBLIE else dossier_paquets_locaux()),
        "version_suite": version_suite(),
        "suite": str(suite()) if suite() else None,
        "polices": str(polices()) if polices() else None,
        "bfwatch": str(bfwatch()) if bfwatch() else None,
        "installer": str(outil("installer.py")) if outil("installer.py") else None,
        "rendus_tex": str(rendus_tex()) if rendus_tex() else None,
        "index": str(index_fonctions()) if index_fonctions() else None,
        "latex": latex_disponible(),
    }


def verifier_ou_quitter(besoin_typst: bool = True) -> None:
    """Arrête le script avec une consigne claire si l'essentiel manque."""
    manques = []
    if besoin_typst and not module_typst():
        manques.append(f"module Python « typst » absent de {sys.executable} : pip install typst")
    if not version_suite():
        if PUBLIE:
            ancien = (f" ; l'ancien paquet @preview/{ANCIEN_NOM_PREVIEW} est présent mais ne suffit plus : relancer la "
                      "commande d'installation" if versions_en_cache(ANCIEN_NOM_PREVIEW) else "")
            manques.append(f"paquet @preview/{NOM_PREVIEW} introuvable dans {dossier_cache_preview()} : installer la "
                           "suite (installer.ps1 / installer.sh à la racine du dépôt) ; Typst le télécharge aussi tout "
                           "seul à la première compilation quand il est sur Typst Universe" + ancien)
        else:
            manques.append(f"paquet @local/farfadet introuvable dans {dossier_paquets_locaux()} : installer la "
                           "suite (installer.ps1 / installer.sh à la racine du dépôt publié)")
    if manques:
        sys.exit("Installation incomplète :\n- " + "\n- ".join(manques))


def main() -> None:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    b = bilan()
    if "--json" in sys.argv:
        print(json.dumps(b, ensure_ascii=False, indent=2))
        return
    libelles = {
        "python": "Python", "module_typst": "module typst", "pymupdf": "PyMuPDF (images de contrôle)",
        "paquets_locaux": "cache @preview" if PUBLIE else "paquets locaux",
        "version_suite": "version de farfadet" if PUBLIE else "version de farfadet", "suite": "suite / dépôt",
        "polices": "polices", "bfwatch": "bfwatch (prof + élève + LaTeX)", "installer": "installer.py (extension, skill…)", "rendus_tex": "rendu des extraits LaTeX",
        "index": "index des fonctions", "latex": "LaTeX (extraits)",
    }
    for cle, valeur in b.items():
        etat = valeur if valeur not in (None, False) else "INTROUVABLE"
        print(f"{libelles[cle]:34} {etat}")
    if not b["polices"]:
        print("\nPolices : pas de dossier trouvé (facultatif). Typst utilisera ses polices intégrées ; pour le rendu "
              "Erewhon, définir BFCOURS_TYPST_POLICES.")


if __name__ == "__main__":
    main()
