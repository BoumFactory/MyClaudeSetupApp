#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
atomize_didactic.py
===================

Extrait les environnements didactiques top-level d'un `enonce.tex` bfcours
vers des fichiers individuels dans `sections/<Type>/<nom>.tex`, et remplace
chaque bloc extrait par un `\\input{sections/<Type>/<nom>.tex}` dans le
fichier source.

Pourquoi
--------
Les `enonce.tex` de cours longs (typiquement >1000 lignes) deviennent
difficiles à éditer par l'IA (latence Read/Edit, perte de contexte).
L'atomisation conserve une vue d'orchestration (sections, sous-sections,
EXO, inputs) dans `enonce.tex` et déporte chaque concept atomique dans
son propre fichier réutilisable et partageable.

Convention bfcours observée
---------------------------
- Les `\\section{}` / `\\subsection{}` restent dans `enonce.tex`.
- Les EXO restent inline par défaut (énoncé + correction couplés).
- Les environnements didactiques (Definition, Propriete, Theoreme, Demonstration,
  Exemple, Remarque, Notation, Activite, Methode, Theoreme, Histoire, Graphique...)
  sont extraits chacun dans `sections/<Type>/<préfixe><NN>_<slug>.tex`.
- Le tracking gère les environnements imbriqués (MultiColonnes, tcbenumerate,
  tcbtab, center, crep, minipage...) : seul le bloc didactique top-level
  est extrait, avec son contenu interne intact.

Sécurité
--------
- Backup automatique de `enonce.tex` en `enonce.tex.bak.<timestamp>`.
- Mode `--dry-run` : affiche le plan sans toucher au système de fichiers.
- Refuse d'écraser un fichier existant : ajoute un suffixe `_v2`, `_v3`...
- Conserve l'encodage UTF-8 et les fins de ligne d'origine.

Usage
-----
    python atomize_didactic.py --enonce path/to/enonce.tex [options]

Options principales :
    --enonce <path>      Chemin vers le fichier à atomiser (obligatoire)
    --dry-run            Affiche le plan, ne modifie rien
    --threshold N        Refuse l'atomisation si le fichier fait moins de N lignes
                         (défaut : 1000 ; --force pour bypasser)
    --force              Bypass du threshold
    --exclude-exo        Ne pas atomiser les EXO (par défaut : ils sont atomisés)
    --types T1,T2,...    Liste explicite des types à atomiser
    --verbose            Affiche le détail des blocs détectés

Cas particulier des EXO
-----------------------
Les `EXO` sont typiquement précédés d'une ligne `\\def\\rdifficulty{N}` qui
en fait sémantiquement partie (elle fixe la difficulté affichée sur la
coche). Le script absorbe automatiquement cette ligne dans le bloc atomisé
ET en extrait la valeur pour le nom de fichier.

Le nom d'un EXO atomisé intègre dans l'ordre :
  exo<NN>_d<difficulty>_<code_competence>_<slug>.tex

Exemples :
  exo01_d1_1sp22_tirage_d_une_boule_numerotee.tex
        ^^ difficulty=1
           ^^^^^ code compétence (2e arg de \\begin{EXO}{...}{...})

  exo15_d2-5_1sl19_duree_avant_la_premiere_panne.tex
        ^^^^ difficulty=2.5 (le `.` est remplacé par `-`)

  exo03_1sp24_titre.tex        (pas de \\def\\rdifficulty → token d<X> omis)

Le script est idempotent : ré-exécuté sur un fichier déjà atomisé, il ne
fait rien (les `\\input` existants sont préservés).
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Types didactiques par défaut (ordre observé dans le projet)
DEFAULT_TYPES = (
    "Definition",
    "Propriete",
    "Theoreme",
    "Lemme",
    "Corollaire",
    "Demonstration",
    "Exemple",
    "Methode",
    "Remarque",
    "Notation",
    "Activite",
    "Histoire",
    "Graphique",
    "Conjecture",
    "Algorithme",
    "EXO",
)

# Regex pour reconnaître une ligne \def\rdifficulty{...} précédant un EXO.
# Cette ligne fait sémantiquement partie du bloc EXO et doit être absorbée.
RDIFFICULTY_LINE_RE = re.compile(r"\\def\s*\\rdifficulty\s*\{[^}]*\}\s*$")

# Capture la valeur de difficulté pour l'intégrer au nom de fichier.
RDIFFICULTY_VALUE_RE = re.compile(r"\\def\s*\\rdifficulty\s*\{([^}]*)\}")

# Préfixes courts pour les noms de fichiers (sinon : type.lower())
TYPE_PREFIX = {
    "Definition": "def",
    "Propriete": "prop",
    "Theoreme": "theo",
    "Lemme": "lem",
    "Corollaire": "cor",
    "Demonstration": "demo",
    "Exemple": "exemple",
    "Methode": "meth",
    "Remarque": "rem",
    "Notation": "not",
    "Activite": "act",
    "Histoire": "hist",
    "Graphique": "graph",
    "Conjecture": "conj",
    "Algorithme": "algo",
    "EXO": "exo",
}

MAX_SLUG_LEN = 40


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def strip_accents(s: str) -> str:
    """Convertit en ASCII en supprimant les diacritiques."""
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def slugify(title: str) -> str:
    """Slugifie un titre : ASCII, minuscules, _, max 40 chars."""
    if not title:
        return ""
    # Retire les commandes LaTeX simples (\textbf{...}, \emph{...}, $...$, etc.)
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^}]*\})?", " ", title)
    s = re.sub(r"\$[^$]*\$", " ", s)  # supprime les morceaux math
    s = strip_accents(s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    s = s.strip("_")
    if len(s) > MAX_SLUG_LEN:
        s = s[:MAX_SLUG_LEN].rstrip("_")
    return s


def line_of_offset(text: str, offset: int) -> int:
    """Numéro de ligne (1-based) correspondant à un offset dans `text`."""
    return text.count("\n", 0, offset) + 1


# ---------------------------------------------------------------------------
# Tokenisation : suit \begin / \end en ignorant les commentaires
# ---------------------------------------------------------------------------

# Token \begin{Name} ou \end{Name} -- on capture le nom de l'environnement.
ENV_TOKEN_RE = re.compile(r"\\(begin|end)\s*\{([A-Za-z@*]+)\}")
# Caractère % non échappé débutant un commentaire LaTeX
COMMENT_RE = re.compile(r"(?<!\\)%")


def _line_starts_at(text: str, offset: int) -> int:
    """Retourne l'offset du début de la ligne contenant `offset`."""
    nl = text.rfind("\n", 0, offset)
    return nl + 1 if nl != -1 else 0


def _is_in_comment(text: str, offset: int) -> bool:
    """Vrai si `offset` se situe après un `%` non échappé sur sa ligne."""
    line_start = _line_starts_at(text, offset)
    line_prefix = text[line_start:offset]
    return bool(COMMENT_RE.search(line_prefix))


@dataclass
class EnvBlock:
    """Un environnement didactique top-level repéré dans le source."""
    env_type: str
    begin_offset: int  # offset de '\' dans \begin{...}
    end_offset: int    # offset après le '}' de \end{...}
    title: str = ""
    code: str = ""     # 2e argument obligatoire (utilisé surtout pour EXO : code compétence)
    difficulty: str = ""  # valeur de \def\rdifficulty{...} pour EXO (ex: "1", "1.5", "2.5")
    counter: int = 0
    filename: str = ""  # rempli plus tard

    @property
    def begin_line(self) -> int:
        return -1  # rempli dynamiquement via line_of_offset

    @property
    def end_line(self) -> int:
        return -1


def find_optional_argument(text: str, start: int) -> tuple[str, int]:
    """Si text[start:] commence par '[arg]', retourne (arg, position_après_]).

    Sinon retourne ("", start).
    Gère les crochets imbriqués élémentaires (1 niveau).
    """
    if start >= len(text) or text[start] != "[":
        return "", start
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return "", start  # crochet mal fermé : ignore


def find_brace_argument(text: str, start: int) -> tuple[str, int]:
    """Si text[start:] commence par '{arg}', retourne (arg, position_après_}).

    Sinon retourne ("", start). Gère les accolades imbriquées.
    """
    if start >= len(text) or text[start] != "{":
        return "", start
    depth = 0
    i = start
    while i < len(text):
        c = text[i]
        if c == "\\":
            i += 2  # skip the escaped char
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
        i += 1
    return "", start


def extract_title_and_code(text: str, after_begin_offset: int) -> tuple[str, str]:
    """Extrait le titre et le 2e argument juste après \\begin{Env}.

    Pour les environnements didactiques classiques, le titre est en
    argument optionnel [..]. Certains (Propriete{...}, EXO{...}{...}) ont
    le titre en argument obligatoire {...}. EXO en a deux : titre + code.
    On retourne (titre, code) — code vide si absent.
    """
    i = after_begin_offset
    while i < len(text) and text[i] in " \t":
        i += 1
    if i >= len(text):
        return "", ""
    title = ""
    if text[i] == "[":
        title, i = find_optional_argument(text, i)
        title = title.strip()
        return title, ""  # pour les types à [opt], pas de 2e arg pertinent
    if text[i] == "{":
        title, i = find_brace_argument(text, i)
        title = title.strip()
        # Tenter un 2e argument {...} (cas EXO)
        while i < len(text) and text[i] in " \t":
            i += 1
        if i < len(text) and text[i] == "{":
            code, _ = find_brace_argument(text, i)
            return title, code.strip()
        return title, ""
    return "", ""


def extend_backward_for_exo(text: str, begin_offset: int) -> tuple[int, str]:
    """Pour un bloc EXO, étend `begin_offset` vers l'arrière pour absorber
    une éventuelle ligne `\\def\\rdifficulty{...}` qui le précède
    immédiatement (séparée par 0+ lignes vides).

    Retourne (nouvel_offset, valeur_difficulty). Si rien à absorber :
    (begin_offset, "").
    """
    # Reculer sur whitespace/newlines
    i = begin_offset
    while i > 0 and text[i - 1] in " \t\r\n":
        i -= 1
    # i pointe juste après le dernier caractère non-blanc de la ligne
    # précédente (ou == 0 si on a tout consommé). Identifier cette ligne.
    line_end = i  # exclusif
    line_start = text.rfind("\n", 0, line_end) + 1  # 0 si pas trouvé
    line_content = text[line_start:line_end]
    if RDIFFICULTY_LINE_RE.match(line_content):
        m = RDIFFICULTY_VALUE_RE.search(line_content)
        difficulty = m.group(1).strip() if m else ""
        return line_start, difficulty
    return begin_offset, ""


def iter_env_tokens(text: str) -> Iterable[tuple[str, str, int, int]]:
    """Itère sur les \\begin / \\end hors commentaires.

    Yield (kind, name, start_offset, end_offset)
    avec kind ∈ {"begin", "end"}.
    """
    for m in ENV_TOKEN_RE.finditer(text):
        if _is_in_comment(text, m.start()):
            continue
        yield m.group(1), m.group(2), m.start(), m.end()


# ---------------------------------------------------------------------------
# Détection des blocs didactiques top-level
# ---------------------------------------------------------------------------

def find_didactic_blocks(text: str, types: set[str]) -> list[EnvBlock]:
    """Retourne la liste ordonnée des blocs didactiques top-level.

    Top-level = pile vide au moment du \\begin (i.e. on n'est dans aucun
    autre environnement). On suit la pile sur TOUS les \\begin/\\end pour
    gérer correctement les imbrications (MultiColonnes, tcbenumerate,
    center, crep, etc.).
    """
    blocks: list[EnvBlock] = []
    stack: list[tuple[str, int]] = []  # (env_name, begin_offset)
    pending_block: EnvBlock | None = None

    for kind, name, start, end in iter_env_tokens(text):
        if kind == "begin":
            if not stack and name in types:
                # Top-level didactique : on démarre un bloc à enregistrer.
                title, code = extract_title_and_code(text, end)
                effective_start = start
                difficulty = ""
                if name == "EXO":
                    # Absorber le \def\rdifficulty{...} qui précède s'il existe,
                    # et en récupérer la valeur pour le nom de fichier.
                    effective_start, difficulty = extend_backward_for_exo(text, start)
                pending_block = EnvBlock(
                    env_type=name,
                    begin_offset=effective_start,
                    end_offset=-1,
                    title=title,
                    code=code,
                    difficulty=difficulty,
                )
            stack.append((name, start))
        else:  # end
            if not stack:
                # \end sans \begin : source mal formé ; on ignore et continue.
                continue
            top_name, _ = stack.pop()
            if top_name != name:
                # Mismatch : LaTeX ne compilerait pas. On reset le pending.
                pending_block = None
                continue
            if not stack and pending_block is not None and name == pending_block.env_type:
                pending_block.end_offset = end
                blocks.append(pending_block)
                pending_block = None
    return blocks


# ---------------------------------------------------------------------------
# Génération des noms de fichiers
# ---------------------------------------------------------------------------

def format_difficulty_for_filename(value: str) -> str:
    """Convertit une valeur de \\rdifficulty en token de nom de fichier.

    Le `.` est remplacé par `-` pour préserver la glob-ability et la
    lisibilité ("1.5" -> "d1-5"). Tout caractère non-alphanumérique
    devient `-`. Retourne "" si la valeur est vide.
    """
    if not value:
        return ""
    cleaned = re.sub(r"[^A-Za-z0-9]", "-", value).strip("-")
    if not cleaned:
        return ""
    return f"d{cleaned}"


def assign_filenames(blocks: list[EnvBlock], sections_dir: Path) -> None:
    """Assigne un nom de fichier à chaque bloc selon la convention
    `<prefix><NN>[_<d-token>][_<code>][_<slug>].tex` (NN cumulatif par
    type, 2 chiffres).

    Pour les EXO, on intercale après le compteur un token de difficulté
    `d<X>` (ex: `d1`, `d2-5` pour difficulty=2.5) suivi du code compétence.
    L'ordre choisi (difficulté avant compétence) place la difficulté
    immédiatement visible, ce qui facilite les filtrages par niveau
    (`ls exo*_d1_*` = tous les exos faciles, tous codes compétence
    confondus).

    Pour les autres types didactiques, le code et la difficulté sont
    ignorés.
    """
    counter_by_type: dict[str, int] = {}
    used_names: set[str] = set()
    for block in blocks:
        counter_by_type[block.env_type] = counter_by_type.get(block.env_type, 0) + 1
        block.counter = counter_by_type[block.env_type]
        prefix = TYPE_PREFIX.get(block.env_type, block.env_type.lower())
        slug = slugify(block.title)
        base = f"{prefix}{block.counter:02d}"
        if block.env_type == "EXO":
            d_token = format_difficulty_for_filename(block.difficulty)
            if d_token:
                base = f"{base}_{d_token}"
            if block.code:
                code_slug = slugify(block.code)
                if code_slug:
                    base = f"{base}_{code_slug}"
        if slug:
            base = f"{base}_{slug}"
        # Collision : si le fichier existe déjà OU si déjà attribué dans ce run.
        type_dir = sections_dir / block.env_type
        candidate = f"{base}.tex"
        version = 1
        while (type_dir / candidate).exists() or candidate in used_names:
            version += 1
            candidate = f"{base}_v{version}.tex"
        used_names.add(candidate)
        block.filename = candidate


# ---------------------------------------------------------------------------
# Application : extraction + remplacement
# ---------------------------------------------------------------------------

def detect_eol(text: str) -> str:
    """Détecte la convention de fin de ligne dominante."""
    if "\r\n" in text:
        return "\r\n"
    return "\n"


def atomize(
    enonce_path: Path,
    types: set[str],
    *,
    dry_run: bool = False,
    threshold: int = 1000,
    force: bool = False,
    verbose: bool = False,
) -> int:
    """Atomise les environnements didactiques d'`enonce_path`.

    Retourne le nombre de blocs extraits.
    """
    if not enonce_path.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {enonce_path}")

    text = enonce_path.read_text(encoding="utf-8")
    n_lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    eol = detect_eol(text)

    if n_lines < threshold and not force and not dry_run:
        print(
            f"[INFO] {enonce_path.name} a {n_lines} lignes (seuil = {threshold}). "
            f"Atomisation non recommandée. Utiliser --force pour forcer.",
        )
        return 0

    blocks = find_didactic_blocks(text, types)
    if not blocks:
        print(f"[INFO] Aucun environnement didactique top-level détecté dans {enonce_path.name}.")
        return 0

    sections_dir = enonce_path.parent / "sections"
    assign_filenames(blocks, sections_dir)

    # Plan d'action
    print(f"[PLAN] {len(blocks)} bloc(s) didactique(s) top-level détecté(s) "
          f"({n_lines} lignes dans {enonce_path.name})")
    for b in blocks:
        line_b = line_of_offset(text, b.begin_offset)
        line_e = line_of_offset(text, b.end_offset)
        title_view = f' "{b.title}"' if b.title else ""
        target = f"sections/{b.env_type}/{b.filename}"
        print(f"  * L{line_b:>4}-{line_e:<4} {b.env_type:<13}{title_view:<45}  ->  {target}")

    if dry_run:
        print("\n[DRY-RUN] Aucune modification effectuée.")
        return len(blocks)

    # Backup
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = enonce_path.with_suffix(enonce_path.suffix + f".bak.{timestamp}")
    shutil.copy2(enonce_path, backup_path)
    print(f"\n[BACKUP] {backup_path}")

    # Écriture des fichiers atomisés + construction du nouveau enonce
    # On parcourt les blocs dans l'ordre et on assemble le nouveau texte.
    pieces: list[str] = []
    cursor = 0
    for block in blocks:
        # Texte avant le bloc
        pieces.append(text[cursor:block.begin_offset])
        # Contenu extrait (bloc complet, begin...end inclus)
        block_text = text[block.begin_offset:block.end_offset]
        # Écriture du fichier atomisé
        type_dir = sections_dir / block.env_type
        type_dir.mkdir(parents=True, exist_ok=True)
        out_file = type_dir / block.filename
        # Le fichier atomisé reçoit le bloc tel quel + un newline final.
        atom_content = block_text.rstrip() + eol
        out_file.write_text(atom_content, encoding="utf-8")
        if verbose:
            print(f"  [+] ecrit {out_file}")
        # Remplacement par \input dans enonce
        pieces.append(f"\\input{{sections/{block.env_type}/{block.filename}}}")
        cursor = block.end_offset
    pieces.append(text[cursor:])
    new_text = "".join(pieces)

    enonce_path.write_text(new_text, encoding="utf-8")
    new_lines = new_text.count("\n") + (0 if new_text.endswith("\n") else 1)
    print(f"\n[OK] {enonce_path.name} : {n_lines} -> {new_lines} lignes "
          f"({len(blocks)} bloc(s) extrait(s)).")
    return len(blocks)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Atomise les environnements didactiques d'un enonce.tex bfcours.",
    )
    parser.add_argument("--enonce", required=True, help="Chemin vers le enonce.tex à atomiser.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Affiche le plan sans rien modifier.")
    parser.add_argument("--threshold", type=int, default=1000,
                        help="Seuil de lignes au-delà duquel l'atomisation est recommandée "
                             "(défaut: 1000).")
    parser.add_argument("--force", action="store_true",
                        help="Force l'atomisation sous le seuil.")
    parser.add_argument("--exclude-exo", action="store_true",
                        help="N'atomise PAS les EXO (par défaut, ils sont atomisés).")
    parser.add_argument("--include-exo", action="store_true",
                        help="[OBSOLÈTE] Compatibilité ; sans effet (EXO atomisé par défaut).")
    parser.add_argument("--types", default="",
                        help="Liste explicite (CSV) des types à atomiser. "
                             "Remplace la liste par défaut.")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    if args.types:
        types = {t.strip() for t in args.types.split(",") if t.strip()}
    else:
        types = set(DEFAULT_TYPES)
        if args.exclude_exo:
            types.discard("EXO")

    n = atomize(
        Path(args.enonce),
        types,
        dry_run=args.dry_run,
        threshold=args.threshold,
        force=args.force,
        verbose=args.verbose,
    )
    return 0 if n >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
