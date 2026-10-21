"""Signatures des commandes et environnements LaTeX : combien d'arguments, lesquels sont facultatifs.

Le convertisseur doit savoir que `\\tccrep[opts]{3cm}{réponse}` prend un argument facultatif puis deux
obligatoires : sinon il ne sait pas où s'arrête la commande. Les signatures viennent de trois sources,
par priorité croissante :

1. `donnees/signatures-latex.json`, livré avec le skill (lu dans les `.sty` de bfcours, rdexo, rdcrep…
   par `python -m tex2typ.signatures --extraire <dossiers>`) ;
2. une table de commandes LaTeX courantes (ci-dessous) ;
3. les définitions du document lui-même (`\\newcommand`, `\\NewDocumentCommand`, `\\newtcolorbox`,
   `\\def\\nom#1#2`…), lues dans son préambule et dans ses `.sty` locaux.

Une signature est une chaîne au format xparse simplifié : `m` obligatoire, `o` facultatif entre crochets,
`O` facultatif avec défaut, `s` étoile, `t<c>` jeton facultatif, `d<>` délimiteurs facultatifs, `v` verbatim.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable

DONNEES = Path(__file__).resolve().parent.parent / "donnees"
FICHIER = DONNEES / "signatures-latex.json"

# Commandes LaTeX standard (et paquets très courants) dont le convertisseur doit connaître les arguments.
STANDARD: Dict[str, str] = {
    "textbf": "m", "textit": "m", "emph": "m", "underline": "m", "textsc": "m", "texttt": "m", "textsf": "m",
    "textrm": "m", "textup": "m", "textnormal": "m", "uline": "m", "sout": "m",
    "textcolor": "om m", "color": "om", "colorbox": "om m", "fcolorbox": "om m m", "highlight": "m",
    "section": "s o m", "subsection": "s o m", "subsubsection": "s o m", "paragraph": "s o m",
    "chapter": "s o m", "part": "s o m",
    "label": "m", "ref": "m", "eqref": "m", "pageref": "m", "cite": "o m", "footnote": "o m",
    "href": "m m", "url": "v", "nolinkurl": "v",
    "includegraphics": "s o m", "input": "m", "include": "m", "subfile": "m", "import": "m m",
    "vspace": "s m", "hspace": "s m", "vskip": "", "hskip": "",
    "newpage": "", "clearpage": "", "pagebreak": "o", "newline": "", "linebreak": "o",
    "medskip": "", "bigskip": "", "smallskip": "", "noindent": "", "indent": "", "par": "",
    "hfill": "", "vfill": "", "centering": "", "raggedright": "", "raggedleft": "",
    "item": "o", "multicolumn": "m m m", "multirow": "o m o m", "cline": "m", "hline": "",
    "cellcolor": "o m", "rowcolor": "o m", "arraybackslash": "",
    "makebox": "o o m", "mbox": "m", "fbox": "m", "framebox": "o o m", "parbox": "o o o m m",
    "raisebox": "m o o m", "resizebox": "s m m m", "scalebox": "m o m", "rotatebox": "o m m",
    "phantom": "m", "hphantom": "m", "vphantom": "m",
    "setlength": "m m", "addtolength": "m m", "setcounter": "m m", "addtocounter": "m m",
    "stepcounter": "m", "refstepcounter": "m",
    "renewcommand": "s m o o m", "newcommand": "s m o o m", "providecommand": "s m o o m",
    "def": "", "tikz": "o m", "tikzset": "m", "pgfplotsset": "m", "usetikzlibrary": "m",
    "usepackage": "o m", "RequirePackage": "o m", "documentclass": "o m", "geometry": "m",
    "hypersetup": "m", "title": "m", "author": "m", "date": "m", "maketitle": "",
    "tableofcontents": "", "today": "", "LaTeX": "", "TeX": "",
    "num": "o m", "SI": "o m m", "si": "o m", "qty": "o m m", "unit": "o m", "ang": "o m",
    "numlist": "o m", "numrange": "o m m", "np": "o m",
    "footnotesize": "", "small": "", "normalsize": "", "large": "", "Large": "", "LARGE": "", "huge": "",
    "Huge": "", "tiny": "", "scriptsize": "", "bfseries": "", "itshape": "", "mdseries": "", "upshape": "",
    "sffamily": "", "rmfamily": "", "ttfamily": "", "normalfont": "", "scshape": "",
    "Needspace": "s m", "needspace": "m", "enlargethispage": "s m",
    "qrcode": "o m", "faIcon": "o m", "textbullet": "", "dots": "", "ldots": "", "og": "", "fg": "",
    "frquote": "m", "enquote": "m", "oe": "", "OE": "", "ae": "", "AE": "", "euro": "", "degres": "",
    "ifcorrection": "", "else": "", "fi": "",
}

# Environnements standard : signature des arguments qui suivent \begin{nom}.
STANDARD_ENV: Dict[str, str] = {
    "itemize": "o", "enumerate": "o", "description": "o", "center": "", "flushleft": "", "flushright": "",
    "minipage": "o o o m", "tabular": "o m", "tabular*": "m o m", "tabularx": "m m", "array": "o m",
    "table": "o", "figure": "o", "multicols": "m", "multicols*": "m", "tikzpicture": "o",
    "align": "", "align*": "", "equation": "", "equation*": "", "gather": "", "gather*": "",
    "cases": "", "verbatim": "", "lstlisting": "o", "minted": "o m", "quote": "", "quotation": "",
    "tcolorbox": "o", "tcbraster": "o", "adjustbox": "m", "spacing": "m", "wrapfigure": "o m o m",
}


def lire_specification(spec: str) -> str:
    """Spécification xparse (`O{}mm`, `s o m`, `>{\\SplitList{;}}m`…) → suite de lettres `s o m…`."""
    sortie, i = [], 0
    while i < len(spec):
        c = spec[i]
        if c in " \t\n+!":
            i += 1
            continue
        if c == ">" or c == "=":  # processeur d'argument : >{…}
            i += 1
            if i < len(spec) and spec[i] == "{":
                i = _fin_groupe(spec, i)
            continue
        if c == "b":  # corps de l'environnement : pas un argument
            i += 1
        elif c in "mvls":
            sortie.append({"m": "m", "v": "v", "l": "m", "s": "s"}[c])
            i += 1
        elif c == "o":
            sortie.append("o")
            i += 1
        elif c == "O":
            sortie.append("o")
            i += 1
            if i < len(spec) and spec[i] == "{":
                i = _fin_groupe(spec, i)
        elif c == "t":
            sortie.append("t" + spec[i + 1: i + 2])
            i += 2
        elif c in "dr":
            sortie.append(("d" if c == "d" else "r") + spec[i + 1: i + 3])
            i += 3
        elif c in "DR":
            sortie.append(("d" if c == "D" else "r") + spec[i + 1: i + 3])
            i += 3
            if i < len(spec) and spec[i] == "{":
                i = _fin_groupe(spec, i)
        elif c in "eE":
            i += 1
            for _ in range(1 if c == "e" else 2):
                if i < len(spec) and spec[i] == "{":
                    i = _fin_groupe(spec, i)
        else:
            i += 1
    return " ".join(sortie)


def _fin_groupe(texte: str, i: int) -> int:
    """Indice qui suit le groupe {…} ouvert en texte[i]."""
    profondeur = 0
    while i < len(texte):
        c = texte[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            profondeur += 1
        elif c == "}":
            profondeur -= 1
            if profondeur == 0:
                return i + 1
        i += 1
    return i


def _arg(texte: str, i: int):
    """Lit un argument {…} ou \\nom à partir de i (espaces sautés). Renvoie (contenu, fin) ou (None, i)."""
    while i < len(texte) and texte[i] in " \t\n":
        i += 1
    if i >= len(texte):
        return None, i
    if texte[i] == "{":
        fin = _fin_groupe(texte, i)
        return texte[i + 1: fin - 1], fin
    if texte[i] == "\\":
        m = re.match(r"\\([A-Za-z@]+\*?|.)", texte[i:])
        return m.group(0), i + m.end()
    return None, i


def _opt(texte: str, i: int):
    j = i
    while j < len(texte) and texte[j] in " \t\n":
        j += 1
    if j < len(texte) and texte[j] == "[":
        profondeur, k = 0, j
        while k < len(texte):
            if texte[k] == "{":
                profondeur += 1
            elif texte[k] == "}":
                profondeur -= 1
            elif texte[k] == "]" and profondeur == 0:
                return texte[j + 1: k], k + 1
            k += 1
    return None, i


def definitions(texte: str) -> Dict[str, Dict[str, str]]:
    """Commandes et environnements définis dans un texte LaTeX : {"commandes": {nom: sig}, "environnements": …}.

    Chaque commande garde aussi, dans "corps", le texte de sa définition quand elle est simple (pour
    l'expansion des macros de l'utilisateur)."""
    cmds: Dict[str, str] = {}
    envs: Dict[str, str] = {}
    corps: Dict[str, Dict[str, object]] = {}
    texte = re.sub(r"(?<!\\)%.*", "", texte)
    for m in re.finditer(r"\\(newcommand|renewcommand|providecommand|DeclareRobustCommand)\*?", texte):
        nom, i = _arg(texte, m.end())
        if not nom or not nom.startswith("\\"):
            continue
        n, i2 = _opt(texte, i)
        defaut, i3 = _opt(texte, i2)
        corps_def, fin = _arg(texte, i3)
        nb = int(n) if n and n.strip().isdigit() else 0
        sig = (["o"] if defaut is not None else []) + ["m"] * (nb - (1 if defaut is not None else 0))
        cmds[nom[1:]] = " ".join(sig)
        if corps_def is not None:
            corps[nom[1:]] = {"n": nb, "defaut": defaut, "corps": corps_def}
    for m in re.finditer(r"\\(NewDocumentCommand|DeclareDocumentCommand|RenewDocumentCommand|ProvideDocumentCommand"
                         r"|NewExpandableDocumentCommand|DeclareExpandableDocumentCommand)", texte):
        nom, i = _arg(texte, m.end())
        spec, _ = _arg(texte, i)
        if nom and nom.startswith("\\") and spec is not None:
            cmds[nom[1:]] = lire_specification(spec)
    for m in re.finditer(r"\\bfdNewSemanticEnv\s*\{([^}]+)\}", texte):  # bfcours : environnement « O{} +b »
        envs[m.group(1).strip()] = "o"
    for m in re.finditer(r"\\(NewDocumentEnvironment|DeclareDocumentEnvironment|RenewDocumentEnvironment"
                         r"|NewTColorBox|DeclareTColorBox|RenewTColorBox|ProvideTColorBox|bfdDeclareEnv)\b", texte):
        _, i = _opt(texte, m.end())
        nom, i = _arg(texte, i)
        spec, _ = _arg(texte, i)
        if nom and spec is not None:
            envs[nom.strip()] = lire_specification(spec)
    for m in re.finditer(r"\\(DeclareTotalTColorBox|NewTotalTColorBox|NewTotalTCBox|DeclareTotalTCBox|RenewTotalTCBox|NewTCBox|DeclareTCBox|newtcbox|DeclareTColorBoxCmd)", texte):
        _, i = _opt(texte, m.end())
        nom, i = _arg(texte, i)
        spec, _ = _arg(texte, i)
        if nom and nom.startswith("\\") and spec is not None:
            cmds[nom[1:]] = lire_specification(spec)
    for m in re.finditer(r"\\(newenvironment|renewenvironment)\*?", texte):
        nom, i = _arg(texte, m.end())
        n, i2 = _opt(texte, i)
        defaut, _ = _opt(texte, i2)
        if nom:
            nb = int(n) if n and n.strip().isdigit() else 0
            envs[nom.strip()] = " ".join((["o"] if defaut is not None else []) + ["m"] * (nb - (1 if defaut is not None else 0)))
    for m in re.finditer(r"\\(newtcolorbox|renewtcolorbox|newtcbtheorem)", texte):
        _, i = _opt(texte, m.end())
        nom, i = _arg(texte, i)
        n, i2 = _opt(texte, i)
        defaut, _ = _opt(texte, i2)
        if nom:
            nb = int(n) if n and n.strip().isdigit() else 0
            envs[nom.strip()] = " ".join((["o"] if defaut is not None else []) + ["m"] * (nb - (1 if defaut is not None else 0)))
    for m in re.finditer(r"\\(?:g|e|x)?def\s*\\([A-Za-z@]+)((?:#\d)*)\s*\{", texte):
        nom, params = m.group(1), m.group(2)
        nb = len(params) // 2
        cmds.setdefault(nom, " ".join(["m"] * nb))
        debut = m.end() - 1
        fin = _fin_groupe(texte, debut)
        corps.setdefault(nom, {"n": nb, "defaut": None, "corps": texte[debut + 1: fin - 1]})
    return {"commandes": cmds, "environnements": envs, "corps": corps}


def extraire(dossiers: Iterable[Path]) -> Dict[str, Dict[str, str]]:
    cmds: Dict[str, str] = {}
    envs: Dict[str, str] = {}
    for d in dossiers:
        for f in sorted(Path(d).rglob("*.sty")):
            if "archives" in f.parts:
                continue
            texte = f.read_text(encoding="utf-8", errors="replace")
            r = definitions(texte)
            for k, v in r["commandes"].items():
                cmds.setdefault(k, v)
            for k, v in r["environnements"].items():
                envs.setdefault(k, v)
    return {"commandes": dict(sorted(cmds.items())), "environnements": dict(sorted(envs.items()))}


def charger() -> Dict[str, Dict[str, str]]:
    """Signatures connues : fichier livré, puis table standard (prioritaire)."""
    base = {"commandes": {}, "environnements": {}}
    if FICHIER.exists():
        base = json.loads(FICHIER.read_text(encoding="utf-8"))
    base["commandes"].update(STANDARD)
    base["environnements"].update(STANDARD_ENV)
    return base


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--extraire":
        r = extraire(Path(x) for x in sys.argv[2:])
        DONNEES.mkdir(parents=True, exist_ok=True)
        FICHIER.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(r['commandes'])} commandes, {len(r['environnements'])} environnements → {FICHIER}")
    else:
        print(__doc__)
