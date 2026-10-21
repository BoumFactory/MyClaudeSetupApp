# -*- coding: utf-8 -*-
"""Socle commun aux methodes d'extraction de resource-to-skill.

Une "methode" = un module Python capable de transformer un type de ressource
(PDF, video, page web, dossier de code...) en un workspace normalise que Claude
peut lire sans deviner ou fouiller.

Contrat d'un module methode:

    NAME      : str   identifiant, doit correspondre a la cle du registry.json
    VERSION   : str
    MATURITY  : "full" | "partial" | "stub"
    GAPS      : list[str]  lacunes connues -> declenche la voie "ameliorer la methode"
    extract(source: str, ws: Workspace, opts: dict) -> dict

`extract` remplit le workspace et renvoie un dict fusionne dans le manifeste
(cles libres: title, coverage, stats, ...).

Le workspace produit:

    <out>/
      manifest.json    carte de l'extraction (type, methode, couverture, artefacts)
      content.md       le texte extrait, structure, avec ancres (page/timecode)
      assets/          images destinees a etre regardees (frames, planches, figures)
      raw/             fichiers bruts conserves pour verification (vtt, html, json)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Statuts de couverture utilises dans manifest["coverage"].
# ok      : dimension entierement captee
# sampled : captee par echantillonnage (frames, extraits) -> Claude peut vouloir plus
# partial : captee de facon incomplete -> candidat a l'amelioration de la methode
# missing : non captee alors qu'elle existe dans la ressource -> a signaler
# n/a     : la ressource ne possede pas cette dimension
COVERAGE_VALUES = ("ok", "sampled", "partial", "missing", "n/a")


class ExtractionError(RuntimeError):
    """Echec bloquant d'une methode: le routeur le transforme en rapport propre."""


class Workspace:
    """Dossier de sortie normalise. Toutes les ecritures passent par ici."""

    def __init__(self, root: Path):
        self.root = Path(root)
        self.assets_dir = self.root / "assets"
        self.raw_dir = self.root / "raw"
        for d in (self.root, self.assets_dir, self.raw_dir):
            d.mkdir(parents=True, exist_ok=True)
        self.warnings: list[str] = []
        self.next_steps: list[str] = []
        self._assets: list[str] = []
        self._raw: list[str] = []

    # -- ecritures -----------------------------------------------------------
    def write_content(self, text: str) -> Path:
        p = self.root / "content.md"
        p.write_text(text, encoding="utf-8")
        return p

    def add_asset(self, path: Path, label: str = "") -> str:
        """Copie une image externe dans assets/ et renvoie son chemin relatif."""
        path = Path(path)
        dest = self.assets_dir / path.name
        if path.resolve() != dest.resolve():
            shutil.copy2(path, dest)
        rel = f"assets/{dest.name}"
        if rel not in self._assets:
            self._assets.append(rel)
        return rel

    def register_asset(self, rel_name: str) -> str:
        """Enregistre un fichier deja ecrit directement dans assets/."""
        rel = f"assets/{rel_name}"
        self._assets.append(rel)
        return rel

    def add_raw(self, name: str, data: str | bytes) -> Path:
        p = self.raw_dir / name
        if isinstance(data, bytes):
            p.write_bytes(data)
        else:
            p.write_text(data, encoding="utf-8")
        self._raw.append(f"raw/{name}")
        return p

    def raw_path(self, name: str) -> Path:
        return self.raw_dir / name

    def claim_raw(self, name: str) -> str:
        self._raw.append(f"raw/{name}")
        return f"raw/{name}"

    # -- signalement ---------------------------------------------------------
    def warn(self, message: str) -> None:
        """Ce qui n'a pas pu etre extrait. Remonte tel quel dans le manifeste."""
        self.warnings.append(message)

    def suggest(self, message: str) -> None:
        """Action concrete proposee a Claude apres lecture du manifeste."""
        self.next_steps.append(message)

    @property
    def assets(self) -> list[str]:
        return list(self._assets)

    @property
    def raw(self) -> list[str]:
        return list(self._raw)


def run(cmd: list[str], timeout: int = 900, check: bool = True, cwd: Path | None = None):
    """Execute une commande externe en neutralisant les surprises d'encodage Windows."""
    env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
        cwd=str(cwd) if cwd else None,
    )
    if check and proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-8:]
        raise ExtractionError(
            f"Echec de `{cmd[0]}` (code {proc.returncode}):\n" + "\n".join(tail)
        )
    return proc


def which(name: str) -> str | None:
    """Localise un executable, en essayant aussi les variantes Windows."""
    for candidate in (name, f"{name}.exe", f"{name}.cmd", f"{name}.bat"):
        found = shutil.which(candidate)
        if found:
            return found
    return None


def require(name: str, hint: str) -> str:
    exe = which(name)
    if not exe:
        raise ExtractionError(f"`{name}` est introuvable dans le PATH. {hint}")
    return exe


def has_module(module: str) -> bool:
    import importlib.util

    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ValueError):
        return False


def pip_install(package: str) -> bool:
    """Installe un paquet a la demande. Renvoie True si l'import devient possible.

    Le poste a un certificat auto-signe dans la chaine TLS: sans --trusted-host,
    pip echoue en SSLError. On tente d'abord normalement, puis avec les hotes de
    confiance, pour ne pas dependre d'une config locale.
    """
    base = [sys.executable, "-m", "pip", "install", "--quiet", package]
    trusted = base + [
        "--trusted-host", "pypi.org",
        "--trusted-host", "files.pythonhosted.org",
        "--trusted-host", "pypi.python.org",
    ]
    for cmd in (base, trusted):
        try:
            if subprocess.run(cmd, capture_output=True, timeout=900).returncode == 0:
                return True
        except (subprocess.TimeoutExpired, OSError):
            continue
    return False


def clip(text: str, limit: int = 400) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"
