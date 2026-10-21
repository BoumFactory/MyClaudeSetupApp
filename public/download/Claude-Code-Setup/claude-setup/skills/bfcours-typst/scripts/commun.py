"""Outils communs aux scripts du skill bfcours-typst : lecture de l'index, clés des guides, table de
renommage LaTeX.

Aucun chemin propre à un poste : tout passe par `localiser.py`. Deux situations sont prévues.

- **Suite source présente** (dépôt de la suite, trouvé par `localiser.suite()`) : l'index est celui de
  `tools/index/index.json` (toujours à jour), les guides sont lus dans les `docs/*.typ` des paquets, la table de renommage dans l'instantané `scripts/donnees/renommage.json`.
- **Paquets installés seuls** (poste d'un collègue) : on lit les instantanés livrés avec le skill dans
  `scripts/donnees/` — `index.json`, `cles-guides.json`, `renommage.json` — que `regenerer.py` recopie ou
  régénère à chaque mise à jour.

Les clés documentées dans les guides (fiches `#fonction(…, params: (p(…)…))`) complètent l'index pour les
fonctions à arguments variadiques comme `EXO`, `tcbenumerate`, `setrdexo`.
"""
import json
import re
import unicodedata
from pathlib import Path

import kebab
import localiser

SKILL = localiser.SKILL
DONNEES = localiser.DONNEES
INDEX_LIVRE = DONNEES / "index.json"
CLES_GUIDES = DONNEES / "cles-guides.json"
RENOMMAGE_LIVRE = DONNEES / "renommage.json"
FICHES = SKILL / "references" / "paquets"


def lire_index():
    chemin = localiser.index_fonctions()
    if not chemin:
        raise SystemExit("Index des fonctions introuvable (ni dans la suite, ni dans scripts/donnees/index.json) : "
                         "lancer scripts/regenerer.py, ou réinstaller le skill.")
    # un index produit avant le passage au kebab-case est mis à niveau (idempotent)
    return kebab.normaliser_index(json.loads(Path(chemin).read_text(encoding="utf-8")))


def dossiers_paquets():
    """[(nom du paquet, dossier)] des paquets qui portent un guide (`docs/*.typ`) : ceux de la suite si elle
    est présente, sinon ceux des paquets installés (quand l'installation a gardé leurs `docs/`)."""
    s = localiser.suite()
    if s:
        return [(p.name, p) for p in sorted(s.iterdir()) if (p / "docs").is_dir()]
    racine = localiser.dossier_paquets_locaux()
    if not racine.is_dir():
        return []
    sortie = []
    for d in sorted(racine.iterdir()):
        p = localiser.dossier_paquet(d.name)
        if p and (p / "docs").is_dir():
            sortie.append((d.name, p))
    return sortie


def fichier_renommage():
    """`_eclatement/RENOMMAGE.md` du chantier (à côté de la suite ou dedans), ou None."""
    s = localiser.suite()
    if not s:
        return None
    for c in (s.parent / "_eclatement" / "RENOMMAGE.md", s / "_eclatement" / "RENOMMAGE.md"):
        if c.exists():
            return c
    return None


def lire_cles_guides():
    """{appel: {"paquet", "fichier", "resume", "params": [{nom, type, defaut, options, description}]}}."""
    if not CLES_GUIDES.exists():
        return {}
    guides = json.loads(CLES_GUIDES.read_text(encoding="utf-8"))
    return {kebab.nom_typst(k): v for k, v in guides.items()}  # clés = noms kebab-case


def plier(texte):
    """Minuscules sans accents, pour comparer des mots."""
    t = unicodedata.normalize("NFD", texte.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


# ---------------------------------------------------------------------------
# Lecture des fiches `#fonction(…)` des guides
# ---------------------------------------------------------------------------

def _fermante(texte, debut):
    """Indice du délimiteur fermant celui de texte[debut] ; saute chaînes, blocs bruts et commentaires."""
    ouvrant = texte[debut]
    fermant = {"(": ")", "[": "]", "{": "}"}[ouvrant]
    pile = [fermant]
    i, n = debut + 1, len(texte)
    while i < n:
        c = texte[i]
        if c == '"' and pile[-1] != "]":
            i += 1
            while i < n and texte[i] != '"':
                i += 2 if texte[i] == "\\" else 1
        elif c == "`":
            m = re.match(r"`+", texte[i:])
            k = len(m.group(0))
            fin = texte.find("`" * k, i + k)
            if fin < 0:
                return -1
            i = fin + k
            continue
        elif c == "\\" and pile[-1] == "]":
            i += 2
            continue
        elif c in "([{":
            pile.append({"(": ")", "[": "]", "{": "}"}[c])
        elif c in ")]}":
            if c != pile[-1]:
                return -1
            pile.pop()
            if not pile:
                return i
        i += 1
    return -1


def _chaine(texte, i):
    """Lit une chaîne Typst à texte[i] == '"' ; renvoie (valeur, indice après)."""
    j = i + 1
    out = []
    while j < len(texte) and texte[j] != '"':
        if texte[j] == "\\" and j + 1 < len(texte):
            out.append(texte[j + 1])
            j += 2
            continue
        out.append(texte[j])
        j += 1
    return "".join(out), j + 1


def _nettoyer(contenu):
    """Contenu Typst d'une description -> texte lisible sur une ligne."""
    t = re.sub(r"#raw\(\"((?:[^\"\\]|\\.)*)\"\)", lambda m: "`" + m.group(1) + "`", contenu)
    t = re.sub(r"\s+", " ", t)
    return t.strip()


def _params(corps):
    """Paramètres `p("nom", "types", defaut: "…", options: (…))[description]` d'une liste `params: (…)`."""
    sortie = []
    for m in re.finditer(r'(?<![\w.-])(?:p|param)\(\s*"', corps):
        debut = corps.rfind("(", 0, m.end())
        fin = _fermante(corps, debut)
        if fin < 0:
            continue
        appel = corps[debut + 1 : fin]
        nom, k = _chaine(appel, appel.index('"'))
        reste = appel[k:]
        mt = re.match(r'\s*,\s*"', reste)
        types = ""
        if mt:
            types, k2 = _chaine(reste, mt.end() - 1)
            reste = reste[k2:]
        defaut = None
        md = re.search(r'defaut:\s*"', reste)
        if md:
            defaut, _ = _chaine(reste, md.end() - 1)
        options = []
        mo = re.search(r"options:\s*\(", reste)
        if mo:
            fo = _fermante(reste, mo.end() - 1)
            bloc = reste[mo.end() : fo] if fo > 0 else ""
            niveau, i = 0, 0
            while i < len(bloc):  # clés de premier niveau du dictionnaire d'options
                c = bloc[i]
                if c in "([{":
                    f = _fermante(bloc, i)
                    i = f + 1 if f > 0 else i + 1
                    continue
                mk = re.match(r'\s*,?\s*("((?:[^"\\]|\\.)*)"|[\w-]+)\s*:', bloc[i:])
                if mk:
                    val = mk.group(2) if mk.group(2) is not None else mk.group(1)
                    options.append(re.sub(r'\\?"', "", val))
                    i += mk.end()
                    continue
                i += 1
        positionnel = bool(re.search(r"positionnel:\s*true", reste))
        description = ""
        if fin + 1 < len(corps) and corps[fin + 1] == "[":
            fd = _fermante(corps, fin + 1)
            if fd > 0:
                description = _nettoyer(corps[fin + 2 : fd])
        sortie.append(dict(nom=nom, type=types, defaut=defaut, options=options, positionnel=positionnel,
                           description=description))
    return sortie


def extraire_guides():
    """Lit les `#fonction("nom", …, params: (…))[résumé]` de tous les `docs/*.typ` des paquets."""
    res = {}
    for nom_paquet, paquet in dossiers_paquets():
        for f in sorted((paquet / "docs").glob("*.typ")):
            texte = f.read_text(encoding="utf-8")
            for m in re.finditer(r'#fonction\(\s*"', texte):
                debut = m.end() - 1
                nom, apres = _chaine(texte, debut)
                ouv = texte.rfind("(", 0, m.end())
                fin = _fermante(texte, ouv)
                if fin < 0:
                    continue
                appel = texte[ouv + 1 : fin]
                mp = re.search(r"params:\s*\(", appel)
                params = []
                if mp:
                    fp = _fermante(appel, mp.end() - 1)
                    if fp > 0:
                        params = _params(appel[mp.end() - 1 : fp + 1])
                resume = ""
                if fin + 1 < len(texte) and texte[fin + 1] == "[":
                    fr = _fermante(texte, fin + 1)
                    if fr > 0:
                        resume = _nettoyer(texte[fin + 2 : fr])
                cle = nom.split("(")[0].strip()
                variante = nom if "(" in nom else None
                entree = res.setdefault(cle, dict(paquet=nom_paquet, fichier=f"{nom_paquet}/docs/{f.name}",
                                                   resume=resume, params=[], variantes=[]))
                if variante:
                    entree["variantes"].append(dict(appel=variante, resume=resume, params=params))
                    continue
                connus = {p["nom"] for p in entree["params"]}
                entree["params"] += [p for p in params if p["nom"] not in connus]
                if not entree["resume"]:
                    entree["resume"] = resume
    return res


# ---------------------------------------------------------------------------
# Table de renommage (section « Épurage »)
# ---------------------------------------------------------------------------

def segments_renommage():
    """Segments (paquet, « ancien → nouveau ») : lus dans l'instantané `donnees/renommage.json`."""
    if fichier_renommage():
        return extraire_renommage()
    if RENOMMAGE_LIVRE.exists():
        data = json.loads(RENOMMAGE_LIVRE.read_text(encoding="utf-8"))
        return [(s["paquet"], s["texte"]) for s in data.get("segments", [])]
    return []


def extraire_renommage():
    """Segments « ancien → nouveau » de la table de renommage, avec leur paquet."""
    chemin = fichier_renommage()
    if not chemin:
        return []
    texte = chemin.read_text(encoding="utf-8")
    debut = texte.find("## Épurage")
    fin = texte.find("\n## ", debut + 5)
    section = texte[debut : fin if fin > 0 else len(texte)]
    sortie = []
    for ligne in section.splitlines():
        if not ligne.startswith("|"):
            if ligne.startswith("- ") and "→" in ligne:
                sortie.append(("", ligne[2:].strip()))
            continue
        cases = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cases) < 2 or cases[0] in ("Paquet", "---") or set(cases[0]) <= {"-"}:
            continue
        for case in cases[1:]:
            for morceau in re.split(r" ; |\. (?=[A-Z`])", case):
                if "→" in morceau or "fusionn" in morceau or "supprim" in morceau.lower():
                    sortie.append((cases[0], morceau.strip()))
    return sortie
