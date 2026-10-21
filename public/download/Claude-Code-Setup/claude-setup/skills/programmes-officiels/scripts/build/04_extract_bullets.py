#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
04_extract_bullets.py — Extraction MÉCANIQUE des bullets du BO depuis pages_txt/.

Phase 5a du pipeline (révisée).

Principe : aucune intervention LLM. Le script lit le texte brut PyMuPDF de
chaque page, identifie les sections canoniques du BO ("Contenus", "Capacités
attendues", "Démonstrations", "Exemples d'algorithme", "Approfondissements
possibles"), et extrait les bullets (lignes commençant par −, -, •, *).

Chaque bullet devient un `formulation_bo` candidat strictement issu du PDF —
aucune régurgitation par LLM. La phase 5b (enrichissement par analyse) ne
reçoit que les bullets isolés pour produire les métadonnées (domaine, type
final, code, fingerprint, prerequis, liens, tags).

Sortie : data/bullets/{folder}/page_NNN.json

Usage :
    python scripts/build/04_extract_bullets.py             # tous niveaux
    python scripts/build/04_extract_bullets.py 1SPE        # un niveau
    python scripts/build/04_extract_bullets.py --force     # réécrit
"""

import io
import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = SKILL_DIR / "data"
PDF_DIR = DATA_DIR / "pdf"
PAGES_TXT_DIR = DATA_DIR / "pages_txt"
BULLETS_DIR = DATA_DIR / "bullets"
MAPPING_FILE = PDF_DIR / "_mapping.json"

# Titres canoniques de sections du BO (insensible casse, tolère pluriels et apostrophes)
SECTION_TITLES = {
    # Lycée
    "contenus": "contenu",
    "contenu": "contenu",
    "contenus_associes": "contenu",
    "contenu_associe": "contenu",
    "capacites": "capacite",
    "capacite": "capacite",
    "capacites_attendues": "capacite",
    "capacite_attendue": "capacite",
    "demonstration": "demonstration",
    "demonstrations": "demonstration",
    "demonstration_possible": "demonstration",
    "demonstrations_possibles": "demonstration",
    "demonstrations_exigibles": "demonstration",
    "exemple_d_algorithme": "algorithme",
    "exemples_d_algorithme": "algorithme",
    "exemples_d_algorithmes": "algorithme",
    "exemple_d_algorithmes": "algorithme",
    "approfondissement_possible": "approfondissement",
    "approfondissements_possibles": "approfondissement",
    # Cycle 4 (BO mars 2026) — structures spécifiques
    "objectifs_d_apprentissage": "capacite",
    "automatismes": "automatisme",
    "prolongements_possibles_mises_en_perspective_historiques_et_culturelles": "approfondissement",
    "prolongements_possibles": "approfondissement",
    # Cycle 3 (BO 2026) — variante du titre approfondissement
    "mises_en_perspective_historiques_et_culturelles": "approfondissement",
}

# Titres "context-only" : marquent un sous-domaine mais pas une section bullet
CONTEXT_TITLES_LOWER = {
    "objectifs", "histoire_des_mathematiques", "situations_et_problemes",
    "contenus_mathematiques", "preambule", "introduction", "vocabulaire_ensembliste_et_logique",
    "algorithmique_et_programmation",
    # Cycle 3 : encadré générique précédant "Objectifs d'apprentissage" — à ignorer
    "connaissances_et_capacites_attendues",
    # NB : "automatismes" retiré de CONTEXT car cycle4 l'utilise comme titre de section bullet
    # ─── Faux positifs cycle 4 (session 9 — 2026-05-21) ───
    # Page 18 contient un exemple de tableau "élection des délégués" :
    # noms d'élèves (cellules de tableau) détectés par erreur comme sous-domaines.
    "total", "alexis", "chloe", "salma", "djibril",
    # Titres de section générique du BO lycée qui ne sont pas des sous-domaines
    # mathématiques (vus en 1TEC/TTEC/TSPE/TCOMP). Sans cet ajout, ces titres
    # captent les bullets et faussent la classification (chute en AL par fallback).
    "commentaires", "programme", "problemes_possibles",
    "organisation_du_programme", "descriptif",
}

# Titres de niveau (cycle 4) : "Cinquième", "Quatrième", "Troisième"
# Et cycle 3 : "Cours moyen première année" (CM1), "Cours moyen deuxième année" (CM2), "Sixième" (6E)
NIVEAU_TITLES_LOWER = {
    "cinquieme": "5E",
    "quatrieme": "4E",
    "troisieme": "3E",
    "cours_moyen_premiere_annee": "CM1",
    "cours_moyen_deuxieme_annee": "CM2",
    "sixieme": "6E",
}

# Dossiers où chaque ligne sous une section bullet canonique doit être traitée comme un bullet
# implicite (cas du BO cycle 3 : les "Objectifs d'apprentissage" listent les compétences sans
# caractère de puce, une compétence par ligne).
#
# Cycle 4 (ajouté session 9 — 2026-05-21) : même structure que cycle 3 pour les
# "Objectifs d'apprentissage" (lignes capitales sans puce). Les "Automatismes" et
# "Prolongements possibles" gardent leurs puces explicites, qui restent prioritaires.
BULLETLESS_FOLDERS = {"cycle3", "cycle4"}

# Pages "sommaire" : ne pas propager le current_niveau qu'elles ont fait dériver (le sommaire
# liste tous les niveaux successivement et finit donc avec le dernier — typiquement "Troisième" —
# ce qui contamine ensuite les pages 2..N qui sont en réalité du préambule, puis du cycle 5e).
# On reset à None après le traitement de la page si elle contient "Sommaire" comme sous-domaine.
SOMMAIRE_RESET_FOLDERS = {"cycle4", "cycle3"}

BULLET_CHARS = ("−", "–", "—", "-", "•", "●", "*", "·")


def normalize_title(s: str) -> str:
    """Normalise un titre pour matching : lowercase, sans accents, sans ponctuation."""
    s = s.strip().rstrip(":.").strip()
    s = s.lower()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def is_bullet_line(line: str) -> bool:
    """Vrai si la ligne (déjà strippée) commence par un caractère de puce BO."""
    if not line:
        return False
    # Caractères de puce possibles, suivi d'un espace ou ponctuation
    return line[0] in BULLET_CHARS and (len(line) == 1 or line[1] in (" ", "\t"))


def strip_bullet(line: str) -> str:
    """Enlève la puce et les espaces de tête."""
    return line[1:].lstrip()


def is_section_title(line: str) -> tuple[bool, str | None]:
    """Renvoie (True, type_canonique) si la ligne est un titre de section bullet."""
    norm = normalize_title(line)
    if norm in SECTION_TITLES:
        return True, SECTION_TITLES[norm]
    return False, None


def is_context_title(line: str) -> bool:
    norm = normalize_title(line)
    return norm in CONTEXT_TITLES_LOWER


def is_niveau_title(line: str) -> tuple[bool, str | None]:
    """Détecte 'Cinquième' / 'Quatrième' / 'Troisième' → renvoie (True, code)."""
    norm = normalize_title(line)
    if norm in NIVEAU_TITLES_LOWER:
        return True, NIVEAU_TITLES_LOWER[norm]
    return False, None


def is_potential_subdomaine(line: str) -> bool:
    """Détecte un titre H2/H3 candidat de sous-domaine.

    Heuristiques durcies (session 5) pour éviter les faux positifs :
      - Longueur 5–55 chars, ≤ 8 mots
      - Commence par majuscule
      - Pas de bullet, pas de titre de section/contexte/niveau
      - Pas de caractères mathématiques italiques (𝑥𝑛𝑎ƒ etc. U+1D400..U+1D7FF, U+0192)
      - Pas finir par : , . ; ou caractère suggérant une phrase tronquée
      - Parenthèses équilibrées
      - Pas plus de 2 caractères de ponctuation interne (,;-) → rejette les phrases
      - Au moins 50 % des mots commencent par majuscule OU c'est un seul mot capitalisé
    """
    s = line.strip()
    if not s or len(s) > 55 or len(s) < 5:
        return False
    if is_bullet_line(s):
        return False
    if is_section_title(s)[0] or is_context_title(s):
        return False
    if is_niveau_title(s)[0]:
        return False
    # Fin de phrase ou fragment
    if s.endswith((":", ".", ";", ",")):
        return False
    # Caractères mathématiques exotiques : U+1D400–U+1D7FF (italic math), U+0192 (ƒ), symboles
    if any(0x1D400 <= ord(c) <= 0x1D7FF for c in s):
        return False
    if any(c in s for c in ("ƒ", "∫", "∑", "∏", "√", "∞", "∂", "≤", "≥", "↦", "Ω", "∩", "∪", "→")):
        return False
    # Pas de parenthèses du tout (rejette les notations mathématiques : Card(A), P(B), V(X), etc.)
    if "(" in s or ")" in s:
        return False
    # Pas d'opérateurs mathématiques typiques
    if any(op in s for op in (" = ", " + ", " – ", " × ", " ÷ ")):
        return False
    # Pas plus de 2 virgules ou points-virgules (limite les phrases longues)
    if s.count(",") + s.count(";") > 2:
        return False
    # Nombre de mots raisonnable
    words = s.split()
    if len(words) > 8:
        return False
    # Première lettre majuscule (accents inclus)
    first = words[0][0] if words and words[0] else ""
    if not first or (not first.isupper() and first not in ("É", "È", "Ê", "À", "Ô", "Ç", "Î", "Ï", "Ù", "Û", "Ü")):
        return False
    # Heuristique de "vrai titre" : pas trop de mots minuscules (signale une phrase).
    # EXCEPTION : si le 1er mot est un déterminant/article ou un nom thématique connu
    # (ex. "Les nombres entiers et décimaux", "Le repérage dans le temps et les durées"),
    # on accepte sans appliquer cette règle, sinon on rejette à tort les titres BO cycle 3.
    if is_subdomaine_opener(s):
        return True
    lowercase_words = sum(1 for w in words if w and w[0].islower() and w not in ("de", "du", "des", "d'", "le", "la", "les", "et", "ou", "à", "au", "aux", "en", "par", "pour", "sur", "dans", "avec", "sans"))
    if lowercase_words > len(words) // 2:
        return False
    return True


def merge_continuation_lines(lines: list[str]) -> list[str]:
    """Recolle les lignes de continuation d'un bullet wrap-text.

    Logique :
      - Une ligne commençant par une puce (−, -, •, ...) démarre un nouveau bullet.
      - Une ligne qui est un titre de section / contexte / sous-domaine ferme le bullet en cours.
      - Toute autre ligne non vide est concaténée au bullet en cours (continuation).
      - Une ligne vide ferme aussi le bullet en cours.
    """
    out = []
    pending = None  # bullet en cours d'accumulation
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            if pending is not None:
                out.append(pending)
                pending = None
            out.append("")
            continue
        s = stripped.lstrip()

        if is_bullet_line(s):
            # Flush bullet précédent et commence un nouveau
            if pending is not None:
                out.append(pending)
            pending = s
            continue

        # Pas un bullet : si c'est un titre/contexte/sous-domaine/niveau, on ferme le bullet et on garde
        if is_section_title(s)[0] or is_context_title(s) or is_potential_subdomaine(s) or is_niveau_title(s)[0]:
            if pending is not None:
                out.append(pending)
                pending = None
            out.append(s)
            continue

        # Sinon : continuation du bullet en cours (wrap-text)
        if pending is not None:
            pending = pending.rstrip() + " " + s
        else:
            out.append(s)

    if pending is not None:
        out.append(pending)
    return out


UPPER_ACCENTS = ("É", "È", "Ê", "Ë", "À", "Â", "Ô", "Ö", "Ç", "Î", "Ï", "Ù", "Û", "Ü")

# Types de section où, en mode bulletless, chaque ligne devient un bullet implicite.
BULLETLESS_BULLET_TYPES = {"contenu", "capacite", "algorithme"}

# Mots-ouvreurs valides pour un sous-domaine cycle 3 : déterminants/articles
# + noms communs courants des thèmes mathématiques. En mode bulletless, à
# l'intérieur d'une section bullet déjà ouverte avec des bullets accumulés,
# une nouvelle ligne n'est traitée comme sous-domaine QUE si son 1er mot
# est dans cette liste — sinon c'est un bullet implicite (verbe à l'infinitif
# par défaut dans le BO cycle 3).
SUBDOMAINE_OPENER_WORDS = {
    # Déterminants / articles
    "le", "la", "les", "l", "un", "une", "des", "du", "de",
    "ce", "cet", "cette", "ces",
    # Noms thématiques courants (sans accent, comparaison via norm)
    "algebre", "geometrie", "trigonometrie", "arithmetique", "logique",
    "pourcentages", "angles", "distances", "cercles", "triangles",
    "symetrie", "numeration", "espace", "grandeurs", "calcul",
    "fractions", "longueurs", "masses", "aires", "volumes",
    "contenances", "solides", "deplacements", "vision", "resolution",
    "organisation", "probabilites", "proportionnalite", "etude",
    "initiation", "cours", "mises", "prolongements", "objectifs",
    "principes", "sommaire", "evolutions", "variations",
    "nombres", "fonctions", "suites", "vecteurs", "statistiques",
    "perspective", "configurations", "histoire",
    # Ajout (session 10) — sous-domaines BO cycle 4 dont le premier mot
    # n'était pas dans la liste, ce qui les faisait router comme bullets
    # implicites en mode bulletless. Voir bug "Puissances 5E/4E", "Racine
    # carrée 4E", "Translations et vecteurs 3E", etc.
    "puissances", "racine", "multiples", "transformations", "translations",
    "representation", "reperage", "parallelogrammes", "operations",
}


def starts_with_upper(s: str) -> bool:
    """Vrai si la première lettre est une majuscule (latin de base ou accentuée)."""
    if not s:
        return False
    c = s[0]
    return c.isupper() or c in UPPER_ACCENTS


def is_subdomaine_opener(s: str) -> bool:
    """Vrai si le 1er mot de la ligne est un ouvreur valide de sous-domaine (cycle 3)."""
    words = s.split()
    if not words:
        return False
    first = words[0].lower().rstrip("'’.,;:")
    first_norm = ''.join(c for c in unicodedata.normalize('NFD', first)
                        if unicodedata.category(c) != 'Mn')
    return first_norm in SUBDOMAINE_OPENER_WORDS


def extract_bullets_from_page(text: str, page_num: int, state: dict | None = None,
                              bulletless: bool = False) -> dict:
    """Parse le texte d'une page et extrait les bullets par section.

    Le paramètre `state` est un dict mutable {state["current_subdomaine"]: str|None}
    qui PERSISTE entre les pages d'un même dossier. Cela permet de propager
    le sous-domaine introduit en fin de page N aux sections orphelines en
    début de page N+1 (cas fréquent dans les BO multipage).

    Si `bulletless=True` (cas cycle 3) : sous une section dont le type est dans
    BULLETLESS_BULLET_TYPES, chaque ligne commençant par une majuscule ouvre
    un nouveau bullet, une ligne en minuscule continue le bullet précédent.
    Les bullets explicites (− • etc.) restent prioritaires partout.
    """
    raw_lines = text.splitlines()
    lines = [ln.rstrip() for ln in raw_lines]
    if not bulletless:
        # En mode bulletless on ne fusionne PAS les continuations en amont :
        # la logique bullet-par-ligne dans la boucle gère elle-même les wraps.
        lines = merge_continuation_lines(lines)

    result = {
        "page": page_num,
        "sections": [],
        "raw_subdomaines_detected": [],
    }

    if state is None:
        state = {"current_subdomaine": None, "current_niveau": None}
    state.setdefault("current_niveau", None)

    current_section = None  # dict {title, type, sous_domaine, niveau_assigne, bullets}
    pending_implicit = None  # bullet implicite (mode bulletless) en cours d'accumulation

    def flush_section():
        if current_section is not None and current_section["bullets"]:
            result["sections"].append(current_section)

    def flush_pending_implicit():
        nonlocal pending_implicit
        if pending_implicit is not None and current_section is not None:
            current_section["bullets"].append({
                "formulation_bo": pending_implicit.strip(),
                "type_hint": current_section["type"],
                "sous_domaine_hint": state["current_subdomaine"],
                "niveau_assigne": state["current_niveau"]
            })
        pending_implicit = None

    for line in lines:
        s = line.strip()
        if not s:
            if bulletless:
                flush_pending_implicit()
            continue

        # Détection titre de niveau (cycle 4 / cycle 3)
        is_niv, niv_code = is_niveau_title(s)
        if is_niv:
            flush_pending_implicit()
            flush_section()
            current_section = None
            state["current_niveau"] = niv_code
            continue

        # Détection bullet explicite (prioritaire dans tous les modes)
        if is_bullet_line(s):
            flush_pending_implicit()
            text_bullet = strip_bullet(s).strip()
            if current_section is None:
                current_section = {
                    "title": "(implicite)",
                    "type": "unknown",
                    "sous_domaine": state["current_subdomaine"],
                    "niveau_assigne": state["current_niveau"],
                    "bullets": []
                }
            current_section["bullets"].append({
                "formulation_bo": text_bullet,
                "type_hint": current_section["type"],
                "sous_domaine_hint": state["current_subdomaine"],
                "niveau_assigne": state["current_niveau"]
            })
            continue

        # Détection section bullet
        is_sec, sec_type = is_section_title(s)
        if is_sec:
            flush_pending_implicit()
            flush_section()
            current_section = {
                "title": s,
                "type": sec_type,
                "sous_domaine": state["current_subdomaine"],
                "niveau_assigne": state["current_niveau"],
                "bullets": []
            }
            continue

        # Détection titre de contexte
        if is_context_title(s):
            flush_pending_implicit()
            flush_section()
            current_section = None
            continue

        # Détection sous-domaine candidat
        if is_potential_subdomaine(s):
            # En mode bulletless, à l'intérieur d'une section bullet capacite/contenu/algorithme,
            # ne considérer comme NOUVEAU sous-domaine que les lignes commençant par un ouvreur
            # valide (déterminant ou nom thématique). Les autres lignes — typiquement des
            # compétences à verbe initial qui passent les heuristiques de longueur — sont
            # routées vers bullet implicite.
            if bulletless and current_section is not None \
                    and current_section["type"] in BULLETLESS_BULLET_TYPES \
                    and not is_subdomaine_opener(s):
                if starts_with_upper(s):
                    flush_pending_implicit()
                    pending_implicit = s
                else:
                    if pending_implicit is not None:
                        pending_implicit = pending_implicit.rstrip() + " " + s
                continue
            flush_pending_implicit()
            flush_section()
            current_section = None
            state["current_subdomaine"] = s
            result["raw_subdomaines_detected"].append(s)
            continue

        # Mode bulletless : ligne dans une section capacite/contenu/algorithme
        # → bullet implicite (majuscule = nouveau, minuscule = continuation).
        if bulletless and current_section is not None \
                and current_section["type"] in BULLETLESS_BULLET_TYPES:
            if starts_with_upper(s):
                flush_pending_implicit()
                pending_implicit = s
            else:
                if pending_implicit is not None:
                    pending_implicit = pending_implicit.rstrip() + " " + s
                # sinon : prose de bas de page, ignorée
            continue

        # Sinon : ligne de prose, ignorée

    if bulletless:
        flush_pending_implicit()
    flush_section()
    return result


def process_folder(folder: str, mapping_entry: dict, force: bool = False) -> dict:
    txt_dir = PAGES_TXT_DIR / folder
    out_dir = BULLETS_DIR / folder
    out_dir.mkdir(parents=True, exist_ok=True)

    bo_ref = mapping_entry.get("bo_reference", "")
    bo_url = mapping_entry.get("bo_url", "")
    pdf = next((k for k, v in load_mapping()["files"].items() if v["page_folder"] == folder),
               f"{folder.lower()}.pdf")

    summary = {
        "page_folder": folder,
        "extracted_at": datetime.now(timezone.utc).isoformat(timespec='seconds'),
        "extractor": "04_extract_bullets.py mechanical",
        "pages": []
    }

    bulletless = folder in BULLETLESS_FOLDERS
    txt_files = sorted(txt_dir.glob("page_*.txt"))
    total_bullets = 0
    # State persistant entre pages : propage le sous-domaine introduit page N à la page N+1
    folder_state = {"current_subdomaine": None}
    for txt in txt_files:
        page_num = int(txt.stem.split("_")[-1])
        out_path = out_dir / f"page_{page_num:03d}.json"
        if out_path.exists() and not force:
            with open(out_path, encoding='utf-8') as f:
                existing = json.load(f)
            n = sum(len(s["bullets"]) for s in existing["page_data"]["sections"])
            total_bullets += n
            summary["pages"].append({"page": page_num, "bullets": n, "skipped": True})
            continue

        text = txt.read_text(encoding='utf-8')
        page_data = extract_bullets_from_page(text, page_num, state=folder_state, bulletless=bulletless)

        # Sommaire : la page d'index liste tous les niveaux à la suite, le state termine
        # contaminé par le dernier titre rencontré (typiquement "Troisième" → 3E). Reset.
        if folder in SOMMAIRE_RESET_FOLDERS:
            if any(sd.lower().startswith("sommaire") for sd in page_data["raw_subdomaines_detected"]):
                folder_state["current_niveau"] = None

        # Enrichir chaque bullet avec source canonique
        for sec in page_data["sections"]:
            for b in sec["bullets"]:
                b["source"] = {
                    "pdf": pdf,
                    "page": page_num,
                    "bo_reference": bo_ref,
                    "bo_url": bo_url,
                    "page_image": f"../pages/{folder}/page_{page_num:03d}.png"
                }

        payload = {
            "meta": {
                "page_folder": folder,
                "page": page_num,
                "pdf": pdf,
                "bo_reference": bo_ref,
                "extracted_at": summary["extracted_at"],
                "extractor": "04_extract_bullets.py mechanical"
            },
            "page_data": page_data
        }
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                            encoding='utf-8', newline='\n')

        n = sum(len(s["bullets"]) for s in page_data["sections"])
        total_bullets += n
        summary["pages"].append({
            "page": page_num,
            "bullets": n,
            "sections": [s["title"] for s in page_data["sections"]],
            "sous_domaines": page_data["raw_subdomaines_detected"][:10]
        })

    summary["total_bullets"] = total_bullets

    (out_dir / "_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding='utf-8', newline='\n'
    )
    return summary


_mapping = None
def load_mapping() -> dict:
    global _mapping
    if _mapping is None:
        with open(MAPPING_FILE, encoding='utf-8') as f:
            _mapping = json.load(f)
    return _mapping


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print(__doc__); return
    force = "--force" in args
    if force:
        args.remove("--force")

    mapping = load_mapping()
    folders_map = {v["page_folder"]: v for v in mapping["files"].values()}

    targets = [args[0]] if args else list(folders_map.keys())
    grand_total = 0
    for folder in targets:
        if folder not in folders_map:
            print(f"Folder inconnu : {folder}")
            continue
        print(f"\nExtraction bullets — {folder}/")
        s = process_folder(folder, folders_map[folder], force=force)
        n = s["total_bullets"]
        grand_total += n
        print(f"   {n} bullets extraits sur {len(s['pages'])} pages")
        for p in s["pages"]:
            if p.get("bullets", 0) > 0 and not p.get("skipped"):
                secs = ",".join(p.get("sections", []))[:80]
                print(f"     page {p['page']:3} : {p['bullets']:3} bullets  [{secs}]")
    print(f"\nTotal global : {grand_total} bullets extraits ({len(targets)} dossier(s))")


if __name__ == "__main__":
    main()
