#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
monolithize_didactic.py
=======================

Opération inverse de `atomize_didactic.py` : résout récursivement tous les
`\\input{sections/...}` (ou tout `\\input{chemin_relatif}` ciblé) d'un
`enonce.tex` pour produire un fichier monolithique unique.

Utile pour :
- Partager un cours dans une archive auto-suffisante.
- Re-monolithiser avant fork / refactor majeur.
- Garantir l'idempotence atomize → monolithize → atomize → identique.

Sécurité
--------
- Par défaut, écrit le résultat dans `<enonce>.monolith.tex` (à côté de l'original).
- `--inplace` : écrase `enonce.tex` après backup horodaté.
- `--cleanup` : après écriture, supprime les fichiers `sections/<Type>/*.tex`
  qui ont été inlinés (et le dossier `sections/` si vide). Backup conservé.
- Ne touche jamais à `enonce_figures.tex` ni aux annexes : seul le pattern
  `\\input{sections/...}` ou `\\input{...}` ciblé est résolu.

Comportement
------------
- Résolution récursive : un fichier inliné peut lui-même contenir des `\\input`.
- Protection anti-cycle (suivi des chemins déjà inlinés).
- Skip les `\\input` commentés (`%\\input{...}`).
- Préserve les fins de ligne et l'indentation autour du `\\input`.

Usage
-----
    python monolithize_didactic.py --enonce path/to/enonce.tex [options]

Options principales :
    --enonce <path>      Chemin du enonce.tex à monolithiser (obligatoire)
    --inplace            Écrase le fichier source après backup
    --output <path>      Chemin de sortie (défaut : <enonce>.monolith.tex)
    --pattern <glob>     Pattern des inputs à résoudre (défaut : sections/*)
                         Ex : "*" pour tout résoudre, "sections/Definition/*" pour cibler.
    --cleanup            Supprime les fichiers inlinés après écriture (avec --inplace)
    --verbose            Détail des résolutions
"""

from __future__ import annotations

import argparse
import fnmatch
import re
import shutil
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Détection des \input
# ---------------------------------------------------------------------------

# \input{chemin} avec gestion ad-hoc :
#  - tolère espaces : \input {sections/...}
#  - ignore si commenté (on filtre par ligne ensuite)
INPUT_RE = re.compile(r"\\input\s*\{([^}]+)\}")
COMMENT_RE = re.compile(r"(?<!\\)%")


def is_commented(line_before_match: str) -> bool:
    """Vrai si un `%` non échappé précède la position courante sur la ligne."""
    return bool(COMMENT_RE.search(line_before_match))


def resolve_input_path(base_dir: Path, raw_path: str) -> Path:
    """Résout un chemin d'argument `\\input{...}` relativement au fichier appelant.

    LaTeX accepte les chemins sans extension `.tex`. On essaie les deux.
    """
    p = Path(raw_path)
    if not p.is_absolute():
        p = base_dir / p
    if p.exists():
        return p
    p_tex = p.with_suffix(".tex") if not p.suffix else p
    if p_tex.exists():
        return p_tex
    # Dernier essai : .tex ajouté brut
    p_brut = Path(str(p) + ".tex")
    if p_brut.exists():
        return p_brut
    return p  # n'existera pas mais on rendra l'info pour le warning


# ---------------------------------------------------------------------------
# Résolution récursive
# ---------------------------------------------------------------------------

def inline_text(
    text: str,
    base_dir: Path,
    pattern: str,
    *,
    visited: set[Path],
    inlined_files: set[Path],
    verbose: bool = False,
) -> str:
    """Résout les `\\input{<motif>}` dans `text`.

    `pattern` est un motif glob/fnmatch appliqué sur le chemin brut tel
    qu'écrit dans `\\input{...}` (avant résolution). Permet de cibler
    `sections/*` pour ne pas toucher aux figures.

    `visited` = ensemble de Path absolus déjà visités (anti-cycle).
    `inlined_files` = collecte des fichiers inlinés (pour --cleanup).
    """
    out_pieces: list[str] = []
    cursor = 0

    for match in INPUT_RE.finditer(text):
        start, end = match.start(), match.end()
        # Vérifier si commenté : recherche du début de ligne
        nl = text.rfind("\n", 0, start)
        line_start = nl + 1 if nl != -1 else 0
        line_prefix = text[line_start:start]
        if is_commented(line_prefix):
            continue
        raw_path = match.group(1).strip()
        # Filtrage par pattern
        if not fnmatch.fnmatchcase(raw_path, pattern):
            # Aussi essayer avec extension .tex retirée
            stripped = raw_path[:-4] if raw_path.endswith(".tex") else raw_path
            if not fnmatch.fnmatchcase(stripped, pattern):
                continue
        resolved = resolve_input_path(base_dir, raw_path)
        if not resolved.is_file():
            print(f"[WARN] \\input{{{raw_path}}} non résolu (cherché : {resolved})",
                  file=sys.stderr)
            continue
        abs_path = resolved.resolve()
        if abs_path in visited:
            print(f"[WARN] cycle détecté sur {abs_path}, ignoré.", file=sys.stderr)
            continue
        # Pré-bloc inchangé
        out_pieces.append(text[cursor:start])
        # Récursion sur le contenu inliné
        visited.add(abs_path)
        sub_text = resolved.read_text(encoding="utf-8")
        sub_text = inline_text(
            sub_text, resolved.parent, pattern,
            visited=visited, inlined_files=inlined_files, verbose=verbose,
        )
        # Retire un éventuel newline final pour ne pas casser le flux ;
        # le contexte autour du \input gère déjà sa propre mise en page.
        if sub_text.endswith("\r\n"):
            sub_text = sub_text[:-2]
        elif sub_text.endswith("\n"):
            sub_text = sub_text[:-1]
        out_pieces.append(sub_text)
        inlined_files.add(abs_path)
        if verbose:
            print(f"  [+] inline {resolved}")
        cursor = end

    out_pieces.append(text[cursor:])
    return "".join(out_pieces)


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------

def monolithize(
    enonce_path: Path,
    *,
    pattern: str = "sections/*",
    inplace: bool = False,
    output: Path | None = None,
    cleanup: bool = False,
    verbose: bool = False,
) -> Path:
    if not enonce_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {enonce_path}")

    source_text = enonce_path.read_text(encoding="utf-8")
    inlined_files: set[Path] = set()
    visited: set[Path] = {enonce_path.resolve()}

    new_text = inline_text(
        source_text, enonce_path.parent, pattern,
        visited=visited, inlined_files=inlined_files, verbose=verbose,
    )

    if inplace:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup = enonce_path.with_suffix(enonce_path.suffix + f".bak.{timestamp}")
        shutil.copy2(enonce_path, backup)
        print(f"[BACKUP] {backup}")
        out_path = enonce_path
    else:
        out_path = output if output else enonce_path.with_suffix(".monolith.tex")

    out_path.write_text(new_text, encoding="utf-8")
    n_lines = new_text.count("\n") + (0 if new_text.endswith("\n") else 1)
    print(f"[OK] {out_path} ({n_lines} lignes, {len(inlined_files)} fichier(s) inliné(s))")

    if cleanup:
        if not inplace:
            print("[INFO] --cleanup ignoré (sans --inplace, on garde les fichiers source).")
        else:
            for f in inlined_files:
                try:
                    f.unlink()
                    if verbose:
                        print(f"  [-] supprime {f}")
                except OSError as e:
                    print(f"[WARN] impossible de supprimer {f} : {e}", file=sys.stderr)
            # Tentative de suppression des dossiers vides
            for type_dir in {f.parent for f in inlined_files}:
                try:
                    if type_dir.exists() and not any(type_dir.iterdir()):
                        type_dir.rmdir()
                except OSError:
                    pass
            sections_dir = enonce_path.parent / "sections"
            try:
                if sections_dir.exists() and not any(sections_dir.iterdir()):
                    sections_dir.rmdir()
            except OSError:
                pass
    return out_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Résout les \\input{sections/...} d'un enonce.tex bfcours "
                    "vers un fichier monolithique.",
    )
    parser.add_argument("--enonce", required=True)
    parser.add_argument("--inplace", action="store_true",
                        help="Écrase le fichier source (avec backup).")
    parser.add_argument("--output", default="",
                        help="Chemin de sortie (défaut : <enonce>.monolith.tex).")
    parser.add_argument("--pattern", default="sections/*",
                        help="Motif glob des inputs à résoudre (défaut : sections/*). "
                             "Utiliser '*' pour tout résoudre.")
    parser.add_argument("--cleanup", action="store_true",
                        help="Supprime les fichiers inlinés (nécessite --inplace).")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    out = monolithize(
        Path(args.enonce),
        pattern=args.pattern,
        inplace=args.inplace,
        output=Path(args.output) if args.output else None,
        cleanup=args.cleanup,
        verbose=args.verbose,
    )
    return 0 if out.exists() else 1


if __name__ == "__main__":
    sys.exit(main())
