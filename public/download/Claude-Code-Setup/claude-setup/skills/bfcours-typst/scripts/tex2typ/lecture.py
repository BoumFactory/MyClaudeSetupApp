"""Lecture d'un document LaTeX : encodage, commentaires, fichiers inclus, préambule et corps.

Le document converti est « aplati » : chaque `\\input{…}` / `\\include{…}` / `\\subfile{…}` est remplacé par
le contenu du fichier, encadré de deux marqueurs `\\bfFichier{chemin}` / `\\bfFinFichier` que le
convertisseur transforme en commentaires Typst (on retrouve ainsi l'origine de chaque bloc).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

INCLUSION = re.compile(r"\\(input|include|subfile|subfileinclude)\s*\{([^}]+)\}|\\input\s+([^\s{}\\]+)")
IMPORT = re.compile(r"\\(?:sub)?import\*?\s*\{([^}]*)\}\s*\{([^}]+)\}")


@dataclass
class Document:
    maitre: Path
    preambule: str = ""
    corps: str = ""
    classe_options: str = ""
    fichiers: List[Path] = field(default_factory=list)
    illisibles: Dict[str, int] = field(default_factory=dict)  # fichier → nombre de caractères U+FFFD
    introuvables: List[str] = field(default_factory=list)


def lire_texte(chemin: Path, document: Optional[Document] = None) -> str:
    """UTF-8 si possible, sinon cp1252 (anciens fichiers Windows), sinon latin-1."""
    brut = chemin.read_bytes()
    for codage in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            texte = brut.decode(codage)
            break
        except UnicodeDecodeError:
            continue
    else:
        texte = brut.decode("utf-8", errors="replace")
    if document is not None and "\ufffd" in texte:
        document.illisibles[str(chemin)] = texte.count("\ufffd")
    return texte.replace("\r\n", "\n").replace("\r", "\n")


def retirer_commentaires(texte: str) -> str:
    """Retire les commentaires `% …` (pas `\\%`), en gardant les sauts de ligne.

    Un commentaire en fin de ligne mange aussi le saut de ligne et les espaces du début de la ligne
    suivante, comme en LaTeX ; une ligne qui n'était qu'un commentaire disparaît sans créer de paragraphe.
    """
    sortie = []
    for ligne in texte.split("\n"):
        i, coupe = 0, None
        while i < len(ligne):
            c = ligne[i]
            if c == "\\":
                i += 2
                continue
            if c == "%":
                coupe = i
                break
            i += 1
        if coupe is None:
            sortie.append(ligne + "\n")
        else:
            avant = ligne[:coupe]
            if avant.strip() == "":
                sortie.append("")  # ligne entièrement commentée : disparaît
            else:
                sortie.append(avant)  # « %» final : la ligne suivante est collée
    return "".join(sortie)


def _resoudre(nom: str, dossier: Path, extensions=(".tex", "")) -> Optional[Path]:
    nom = nom.strip()
    for ext in extensions:
        p = (dossier / (nom + ext)) if not nom.endswith(ext) or not ext else dossier / nom
        if p.is_file():
            return p
    return None


def _corps_si_document(texte: str) -> str:
    """Un fichier inclus qui est lui-même un document complet : on ne garde que son corps."""
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", texte, re.S)
    return m.group(1) if m and "\\documentclass" in texte[: m.start()] else texte


def deplier(texte: str, dossier: Path, document: Document, profondeur: int = 0) -> str:
    if profondeur > 12:
        return texte

    def remplacer(m: re.Match) -> str:
        nom = m.group(2) or m.group(3)
        if m.group(1) in ("subfile", "subfileinclude") or nom is None:
            pass
        cible = _resoudre(nom, dossier)
        if cible is None:
            document.introuvables.append(nom)
            return m.group(0)
        document.fichiers.append(cible)
        contenu = _corps_si_document(retirer_commentaires(lire_texte(cible, document)))
        contenu = deplier(contenu, cible.parent, document, profondeur + 1)
        rel = cible.name if cible.parent == document.maitre.parent else str(cible.relative_to(document.maitre.parent)) \
            if _sous(cible, document.maitre.parent) else str(cible)
        return "\\bfFichier{" + rel.replace("\\", "/") + "}\n" + contenu + "\n\\bfFinFichier{}"

    def remplacer_import(m: re.Match) -> str:
        sous = dossier / m.group(1)
        cible = _resoudre(m.group(2), sous)
        if cible is None:
            document.introuvables.append(m.group(1) + m.group(2))
            return m.group(0)
        document.fichiers.append(cible)
        contenu = _corps_si_document(retirer_commentaires(lire_texte(cible, document)))
        return "\\bfFichier{" + cible.name + "}\n" + deplier(contenu, cible.parent, document, profondeur + 1) \
            + "\n\\bfFinFichier{}"

    texte = IMPORT.sub(remplacer_import, texte)
    return INCLUSION.sub(remplacer, texte)


def _sous(p: Path, d: Path) -> bool:
    try:
        p.resolve().relative_to(d.resolve())
        return True
    except ValueError:
        return False


def lire_document(maitre: Path) -> Document:
    maitre = maitre.resolve()
    doc = Document(maitre=maitre)
    texte = retirer_commentaires(lire_texte(maitre, doc))
    m = re.search(r"\\begin\{document\}", texte)
    if m:
        preambule, reste = texte[: m.start()], texte[m.end():]
        fin = re.search(r"\\end\{document\}", reste)
        corps = reste[: fin.start()] if fin else reste
    else:  # fragment sans préambule (un exercice isolé) : tout est corps
        preambule, corps = "", texte
    mc = re.search(r"\\documentclass\s*(?:\[([^\]]*)\])?", preambule)
    doc.classe_options = (mc.group(1) or "") if mc else ""
    doc.preambule = deplier(preambule, maitre.parent, doc)
    doc.corps = deplier(corps, maitre.parent, doc)
    return doc
