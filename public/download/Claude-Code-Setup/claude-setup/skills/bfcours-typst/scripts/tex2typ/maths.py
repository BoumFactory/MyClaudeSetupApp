"""Formules LaTeX → mode mathématique de Typst, écrit pour être relu par un humain.

    convertir("\\dfrac{x+1}{2} \\leqslant \\sqrt{3}")  →  "display((x + 1)/2) lt.eq.slant sqrt(3)"

Choix d'écriture :
- lettres séparées par des espaces (`AB` → `A B`) : en Typst, `AB` serait une variable inconnue ;
- `3{,}5` → `3.5` : le modèle bfcours affiche la virgule décimale française dans les formules ;
- `\\frac{a}{b}` → `a/b` (parenthèses seulement si nécessaire), `\\dfrac` → `display(a/b)` en ligne ;
- commandes de bfcours : `\\Vecteur{AB}` → `vect(A B)`, `\\Coordonnees[A]{x}{y}` → `coordonnees(x, y, nom: A)`.

Une commande inconnue ne fait pas échouer la conversion : elle est notée dans `inconnues` et la formule
est signalée (le convertisseur la replie alors en extrait LaTeX, fidèle).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Tuple

SYMBOLES: Dict[str, str] = {
    # grec
    **{g: g for g in ("alpha", "beta", "gamma", "delta", "zeta", "eta", "theta", "iota", "kappa", "lambda", "mu",
                      "nu", "xi", "pi", "rho", "sigma", "tau", "upsilon", "chi", "psi", "omega", "Gamma", "Delta",
                      "Theta", "Lambda", "Xi", "Pi", "Sigma", "Upsilon", "Phi", "Psi", "Omega")},
    "epsilon": "epsilon.alt", "varepsilon": "epsilon", "phi": "phi.alt", "varphi": "phi", "vartheta": "theta.alt",
    "varpi": "pi.alt", "varrho": "rho.alt", "varsigma": "sigma.alt", "varkappa": "kappa.alt",
    # opérations
    "times": "times", "div": "div", "cdot": "dot", "pm": "plus.minus", "mp": "minus.plus", "ast": "ast",
    "star": "star", "circ": "compose", "bullet": "bullet", "oplus": "plus.circle", "otimes": "times.circle",
    "cup": "union", "cap": "inter", "bigcup": "union.big", "bigcap": "inter.big", "setminus": "without",
    "backslash": "backslash", "wedge": "and", "land": "and", "vee": "or", "lor": "or", "neg": "not", "lnot": "not",
    # relations
    "leq": "<=", "le": "<=", "geq": ">=", "ge": ">=", "leqslant": "lt.eq.slant", "geqslant": "gt.eq.slant",
    "neq": "!=", "ne": "!=", "approx": "approx", "simeq": "tilde.eq", "sim": "tilde.op", "cong": "tilde.equiv",
    "equiv": "equiv", "propto": "prop", "ll": "<<", "gg": ">>", "in": "in", "notin": "in.not", "ni": "in.rev",
    "subset": "subset", "subseteq": "subset.eq", "supset": "supset", "supseteq": "supset.eq",
    "not\\subset": "subset.not", "nsubseteq": "subset.eq.not", "parallel": "parallel", "perp": "perp",
    "mid": "divides", "nmid": "divides.not", "models": "models", "vdash": "tack.r",
    # flèches
    "to": "->", "rightarrow": "->", "longrightarrow": "-->", "leftarrow": "<-", "longleftarrow": "<--",
    "Rightarrow": "=>", "Longrightarrow": "==>", "Leftarrow": "arrow.l.double", "Longleftarrow": "<==",
    "Leftrightarrow": "<=>", "Longleftrightarrow": "<==>", "iff": "<==>", "implies": "==>", "impliedby": "<==",
    "leftrightarrow": "<->", "mapsto": "|->", "longmapsto": "|-->", "uparrow": "arrow.t", "downarrow": "arrow.b",
    "nearrow": "arrow.tr", "searrow": "arrow.br", "nRightarrow": "arrow.r.double.not",
    # divers
    "infty": "oo", "partial": "diff", "nabla": "nabla", "forall": "forall", "exists": "exists",
    "nexists": "exists.not", "emptyset": "emptyset", "varnothing": "emptyset", "angle": "angle",
    "measuredangle": "angle.arc", "triangle": "triangle.stroked.t", "square": "square.stroked", "ell": "ell",
    "hbar": "planck.reduce", "Re": "Re", "Im": "Im", "aleph": "aleph", "prime": "prime", "degree": "degree",
    "ldots": "...", "dots": "...", "cdots": "dots.c", "vdots": "dots.v", "ddots": "dots.down", "dotsc": "...",
    "dotsb": "dots.c", "colon": "colon", "lbrace": "{", "rbrace": "}", "langle": "angle.l", "rangle": "angle.r",
    "lfloor": "floor.l", "rfloor": "floor.r", "lceil": "ceil.l", "rceil": "ceil.r", "vert": "|", "lvert": "|",
    "rvert": "|", "Vert": "||", "lVert": "||", "rVert": "||", "|": "||", "top": "top", "bot": "bot",
    "checkmark": "checkmark", "dagger": "dagger", "S": "section", "P": "pilcrow", "euro": "euro", "%": "%",
    "#": "\\#", "&": "\\&", "_": "\\_", "$": "\\$", "{": "{", "}": "}", "textdegree": "degree", "degres": "degree",
    "cdotp": "dot.c", "intercal": "top", "complement": "complement", "Box": "square.stroked",
    "blacksquare": "square.filled", "lozenge": "lozenge.stroked", "sharp": "sharp", "flat": "flat",
    "heartsuit": "suit.heart.stroked", "spadesuit": "suit.spade", "clubsuit": "suit.club", "diamond": "diamond",
}
GROS_OPERATEURS = {"sum": "sum", "prod": "product", "coprod": "product.co", "int": "integral",
                   "iint": "integral.double", "iiint": "integral.triple", "oint": "integral.cont",
                   "bigoplus": "plus.circle.big", "bigotimes": "times.circle.big", "bigsqcup": "union.sq.big"}
FONCTIONS = {f: f for f in ("sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos", "arctan", "sinh", "cosh",
                            "tanh", "coth", "ln", "log", "lg", "exp", "lim", "liminf", "limsup", "max", "min", "sup",
                            "inf", "det", "dim", "gcd", "arg", "deg", "ker", "hom", "mod", "Pr")}
FONCTIONS.update({"limsup": "limsup", "liminf": "liminf", "bmod": "mod", "pmod": "mod"})
ESPACES = {",": "thin", ":": "med", ";": "thick", ">": "med", "!": "", " ": "space", "quad": "quad",
           "qquad": "wide", "thinspace": "thin", "medspace": "med", "thickspace": "thick", "enspace": "space.en",
           "negthinspace": "", "hfill": "", "hspace": "", "nobreak": "", "displaystyle": "", "textstyle": "",
           "scriptstyle": "", "limits": "", "nolimits": "", "left.": "", "right.": "", "relax": "", "strut": "",
           "mathstrut": "", "big": "", "Big": "", "bigg": "", "Bigg": "", "bigl": "", "bigr": "", "Bigl": "",
           "Bigr": "", "biggl": "", "biggr": "", "middle": "", "allowbreak": "", "label": "", "nonumber": "",
           "notag": "", "noindent": "", "boldmath": "", "unboldmath": "", "phantom": ""}
ACCENTS = {"vec": "arrow", "overrightarrow": "arrow", "overleftarrow": "arrow.l", "hat": "hat", "widehat": "hat",
           "bar": "overline", "overline": "overline", "underline": "underline", "tilde": "tilde",
           "widetilde": "tilde", "dot": "dot", "ddot": "dot.double", "check": "caron", "breve": "breve",
           "acute": "acute", "grave": "grave", "mathring": "circle", "overleftrightarrow": "arrow.l.r"}
POLICES = {"mathbf": "bold", "boldsymbol": "bold", "bm": "bold", "mathit": "italic", "mathcal": "cal",
           "mathscr": "scr", "mathfrak": "frak", "mathsf": "sans", "mathtt": "mono", "mathbb": "bb",
           "mathrm": "upright", "textup": "upright", "mathnormal": ""}
ENSEMBLES = {"R": "RR", "N": "NN", "Z": "ZZ", "Q": "QQ", "C": "CC", "D": "dd", "K": "KK", "P": "PP"}
TEXTE = {"text", "textrm", "textnormal", "mbox", "textit", "textbf", "emph", "textsf", "texttt", "hbox", "mathrm*",
         "operatorname", "operatorname*"}
DELIMS = {"(": "(", ")": ")", "[": "[", "]": "]", "\\{": "{", "\\}": "}", "|": "|", "\\|": "||", ".": "",
          "\\langle": "angle.l", "\\rangle": "angle.r", "\\lfloor": "floor.l", "\\rfloor": "floor.r",
          "\\lceil": "ceil.l", "\\rceil": "ceil.r", "\\vert": "|", "\\Vert": "||", "\\lvert": "|", "\\rvert": "|",
          "\\lbrace": "{", "\\rbrace": "}", "/": "/", "\\lVert": "||", "\\rVert": "||", "<": "angle.l",
          ">": "angle.r"}
MATRICES = {"pmatrix": '"("', "bmatrix": '"["', "Bmatrix": '"{"', "vmatrix": '"|"', "Vmatrix": '"||"',
            "matrix": "#none", "smallmatrix": "#none", "array": "#none"}  # en maths, `none` seul = variable


@dataclass
class Resultat:
    texte: str
    inconnues: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.inconnues


class Convertisseur:
    """Une instance par formule. `macros` : fonctions supplémentaires (commandes bfcours, macros du document)."""

    def __init__(self, source: str, macros: Optional[Dict[str, Callable]] = None, display: bool = False,
                 macros_utilisateur: Optional[Dict[str, dict]] = None):
        self.s = source
        self.i = 0
        self.n = len(source)
        self.inconnues: List[str] = []
        self.macros = macros or {}
        self.utilisateur = macros_utilisateur or {}
        self.display = display
        self.profondeur_expansion = 0

    # -------------------------------------------------------------- lecture
    def _espaces(self):
        while self.i < self.n and self.s[self.i] in " \t\n":
            self.i += 1

    def _groupe_brut(self) -> str:
        """Lit un argument {…} (ou un seul jeton) et renvoie son source LaTeX."""
        self._espaces()
        if self.i >= self.n:
            return ""
        c = self.s[self.i]
        if c == "{":
            prof, j = 0, self.i
            while j < self.n:
                if self.s[j] == "\\":
                    j += 2
                    continue
                if self.s[j] == "{":
                    prof += 1
                elif self.s[j] == "}":
                    prof -= 1
                    if prof == 0:
                        break
                j += 1
            brut = self.s[self.i + 1: j]
            self.i = j + 1
            return brut
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", self.s[self.i:])
            self.i += m.end()
            return m.group(0)
        self.i += 1
        return c

    def _optionnel_brut(self) -> Optional[str]:
        j = self.i
        while j < self.n and self.s[j] in " \t":
            j += 1
        if j < self.n and self.s[j] == "[":
            prof, k = 0, j + 1
            while k < self.n:
                if self.s[k] == "{":
                    prof += 1
                elif self.s[k] == "}":
                    prof -= 1
                elif self.s[k] == "]" and prof == 0:
                    self.i = k + 1
                    return self.s[j + 1: k]
                k += 1
        return None

    def sous(self, source: str) -> str:
        c = Convertisseur(source, self.macros, self.display, self.utilisateur)
        c.profondeur_expansion = self.profondeur_expansion
        r = c.convertir()
        self.inconnues += c.inconnues
        return r

    def arg(self) -> str:
        return self.sous(self._groupe_brut())

    # -------------------------------------------------------------- conversion
    def convertir(self) -> str:
        morceaux: List[str] = []
        while self.i < self.n:
            m = self._element()
            if m is None:
                continue
            morceaux.append(m)
        return joindre(morceaux)

    def _element(self) -> Optional[str]:
        s, i = self.s, self.i
        c = s[i]
        if c in " \t\n":
            self.i += 1
            return None
        if c == "\\":
            return self._commande()
        if c == "{":
            contenu = self.sous(self._groupe_brut())
            return contenu if _atome(contenu) else "(" + contenu + ")" if contenu else '""'
        if c in "^_":
            self.i += 1
            self._espaces()
            if self.i < self.n and self.s[self.i] == "\\" and re.match(r"\\prime", self.s[self.i:]):
                self.i += 6
                return "'"
            contenu = self.arg()
            if c == "^" and contenu.strip() in ("compose", "circle.stroked.small"):
                return "°"  # 90^\circ : degré
            return c + _parentheser(contenu, indice=True)
        if c == "'":
            j = i
            while j < self.n and s[j] == "'":
                j += 1
            self.i = j
            return "'" * (j - i)
        if c.isdigit() or (c == "." and i + 1 < self.n and s[i + 1].isdigit()):
            m = re.match(r"\d+(?:(?:\.|\{,\}|\{\.\}|,(?=\d))\d+)*", s[i:])
            nombre = m.group(0)
            self.i += m.end()
            nombre = nombre.replace("{,}", ".").replace("{.}", ".")
            nombre = re.sub(r",(?=\d)", ".", nombre)
            return nombre
        if c.isalpha():
            self.i += 1
            if c in "ACDEFGHIJKLMNOPQRSTUVWXYZBabcdefghijklmnopqrstuvwxyz":
                return c
            return c  # lettre accentuée : acceptée telle quelle
        if c == "&":
            self.i += 1
            return "&"
        if c == '"':
            self.i += 1
            return '\\"'
        if c == "~":  # espace insécable : inutile autour du « ; » (espacé par le modèle), gardée devant « % »
            self.i += 1
            if re.match(r"\s*\\%", s[self.i:]):
                return "space"
            return None
        if c == "#":
            self.i += 1
            return "\\#"
        if c == "$":
            self.i += 1
            return None
        self.i += 1
        if c == "<" and s[i + 1: i + 2] == "=":
            return "< ="
        if c == "-" and s[i + 1: i + 2] == ">":
            return "- >"
        if c == "*":
            return "*"
        if c == "/":
            return "slash"
        return c

    def _commande(self) -> Optional[str]:
        s = self.s
        m = re.match(r"\\([A-Za-z]+\*?|.)", s[self.i:])
        nom = m.group(1)
        self.i += m.end()
        if nom.endswith("*") and nom not in ("operatorname*",):
            nom = nom[:-1]
        if nom == "\\":
            self._optionnel_brut()
            return "\\\n"
        if nom in ESPACES:
            if nom in ("hspace", "phantom", "label"):
                self._groupe_brut()
                return "space" if nom == "hspace" else None
            return ESPACES[nom] or None
        if nom in ("left", "right"):
            self._espaces()
            mm = re.match(r"\\[A-Za-z]+|\\.|.", s[self.i:])
            d = mm.group(0)
            self.i += mm.end()
            return DELIMS.get(d, d) or None
        if nom in self.macros:
            return self.macros[nom](self)
        if nom in self.utilisateur and self.profondeur_expansion < 8:
            return self._expansion(nom)
        if nom in SYMBOLES:
            return SYMBOLES[nom]
        if nom in FONCTIONS:
            return FONCTIONS[nom]
        if nom in GROS_OPERATEURS:
            return GROS_OPERATEURS[nom]
        if nom in ("frac", "dfrac", "tfrac", "cfrac"):
            a, b = self.arg(), self.arg()
            den = _parentheser(b)
            if den.startswith("-"):  # « 10/-6 » : Typst coupe la fraction sur le signe
                den = "(" + den + ")"
            f = _parentheser(a) + "/" + den
            if nom == "dfrac" and not self.display:
                return "display(" + f + ")"
            if nom == "tfrac" and self.display:
                return "inline(" + f + ")"
            return f
        if nom in ("binom", "dbinom", "tbinom"):
            return "binom(" + self.arg() + ", " + self.arg() + ")"
        if nom == "sqrt":
            indice = self._optionnel_brut()
            corps = self.arg()
            return "sqrt(" + corps + ")" if indice is None else "root(" + self.sous(indice) + ", " + corps + ")"
        if nom in ACCENTS:
            return ACCENTS[nom] + "(" + self.arg() + ")"
        if nom in ("overbrace", "underbrace"):
            corps = self.arg()
            self._espaces()
            note = ""
            if self.i < self.n and self.s[self.i] in "^_":
                self.i += 1
                note = ", " + self.arg()
            return nom + "(" + corps + note + ")"
        if nom in ("overset", "stackrel"):
            haut, bas = self.arg(), self.arg()
            return "limits(" + bas + ")^" + _parentheser(haut)
        if nom == "underset":
            dessous, base = self.arg(), self.arg()
            return "limits(" + base + ")_" + _parentheser(dessous)
        if nom in ("cancel", "bcancel", "xcancel", "sout"):
            return "cancel(" + self.arg() + ")"
        if nom in ("boxed", "fbox"):
            return "#box(stroke: 0.5pt, inset: 3pt, $" + self.arg() + "$)"
        if nom == "mathbb":
            brut = self._groupe_brut().strip()
            if brut in ENSEMBLES:
                return ENSEMBLES[brut]
            return "bb(" + self.sous(brut) + ")"
        if nom in POLICES:
            brut = self._groupe_brut()
            contenu = self.sous(brut)
            if POLICES[nom] == "upright" and re.fullmatch(r"[A-Za-zÀ-ÿ]{2,}", brut.strip()):
                return 'upright("' + brut.strip() + '")'
            if not POLICES[nom]:
                return contenu
            return POLICES[nom] + "(" + contenu + ")"
        if nom in ("operatorname", "operatorname*"):
            brut = self._groupe_brut().strip()
            return 'op("' + _texte_brut(brut) + '"' + (", limits: #true" if nom.endswith("*") else "") + ")"
        if nom in TEXTE:
            brut = self._groupe_brut()
            return self._texte(brut, nom)
        if nom in ("color", "textcolor"):
            modele = self._optionnel_brut()  # \color[HTML]{f15929} : modèle de couleur, puis code
            couleur = self._groupe_brut()
            if nom == "textcolor":
                if modele and modele.strip().lower() == "html" and re.fullmatch(r"[0-9A-Fa-f]{6}", couleur.strip()):
                    return '#text(fill: rgb("#' + couleur.strip() + '"))[$' + self.arg() + '$]'
                return '#text(fill: xcolor("' + couleur + '"))[$' + self.arg() + '$]'
            return None
        if nom == "not":
            suite = self._element()
            return (suite + ".not") if suite and re.fullmatch(r"[a-z.]+", suite) else "cancel(" + (suite or "") + ")"
        if nom == "begin":
            return self._environnement()
        if nom in ("pmod",):
            return "(mod " + self.arg() + ")"
        if nom in ("ensuremath", "mathord", "mathbin", "mathrel", "mathop", "displaystyle"):
            return self.arg()
        if nom in ("num", "np", "nombre"):
            self._optionnel_brut()
            return self.sous(self._groupe_brut())
        if nom in ("SI", "qty", "SIunit"):
            self._optionnel_brut()
            valeur = self.sous(self._groupe_brut())
            unite = self._groupe_brut()
            return valeur + ' "' + _unite(unite) + '"'
        if nom in ("si", "unit"):
            self._optionnel_brut()
            return '"' + _unite(self._groupe_brut()) + '"'
        if nom == "ang":
            self._optionnel_brut()
            return self.sous(self._groupe_brut()) + "degree"
        if nom == "pourcent":
            return "%"
        if nom == "parallele":
            return "parallel"
        self.inconnues.append("\\" + nom)
        return '"?' + nom + '"'

    def _expansion(self, nom: str) -> str:
        d = self.utilisateur[nom]
        n = d.get("n", 0)
        valeurs = []
        if d.get("defaut") is not None:
            opt = self._optionnel_brut()
            valeurs.append(opt if opt is not None else d["defaut"])
            n -= 1
        for _ in range(max(n, 0)):
            valeurs.append(self._groupe_brut())
        corps = d["corps"]
        for k, v in enumerate(valeurs, 1):
            corps = corps.replace("#" + str(k), v)
        c = Convertisseur(corps, self.macros, self.display, self.utilisateur)
        c.profondeur_expansion = self.profondeur_expansion + 1
        r = c.convertir()
        self.inconnues += c.inconnues
        return r if _atome(r) else "(" + r + ")" if " " in r.strip() and False else r

    def _texte(self, brut: str, nom: str) -> str:
        rappel = self.macros.get("__texte__")
        if rappel and ("$" in brut or re.search(r"\\[A-Za-z]", brut)):
            # texte balisé (\acc, \tccrep, formule…) : converti par le convertisseur de texte
            return "#[" + rappel(self, brut).replace("\n", " ") + "]"
        if "$" in brut or "\\" in brut.replace("\\ ", "").replace("\\,", ""):
            # texte avec formule ou commande : contenu Typst
            interieur = re.sub(r"\$([^$]*)\$", lambda m: "$" + self.sous(m.group(1)) + "$", brut)
            interieur = interieur.replace("\\,", " ").replace("\\ ", " ").replace("~", " ")
            interieur = re.sub(r"\\(textbf|textit|emph)\{([^{}]*)\}", lambda m: ("*" if m.group(1) == "textbf" else "_") + m.group(2) + ("*" if m.group(1) == "textbf" else "_"), interieur)
            if re.search(r"\\[A-Za-z]", re.sub(r"\$[^$]*\$", "", interieur)):
                self.inconnues.append("\\" + nom + "{…}")
            return "#[" + interieur + "]"
        t = _texte_brut(brut)
        if nom == "textbf":
            return 'bold(upright("' + t + '"))'
        if nom in ("textit", "emph"):
            return 'italic("' + t + '")'
        return '"' + t + '"'

    def _environnement(self) -> str:
        nom = self._groupe_brut().strip()
        etoile = nom.endswith("*")
        base = nom.rstrip("*")
        if base == "array" or base == "tabular":
            self._groupe_brut()  # spécification de colonnes
        fin = re.search(r"\\end\s*\{" + re.escape(nom) + r"\}", self.s[self.i:])
        if not fin:
            self.inconnues.append("\\begin{" + nom + "}")
            return ""
        corps = self.s[self.i: self.i + fin.start()]
        self.i += fin.end()
        lignes = [l for l in re.split(r"\\\\(?:\[[^\]]*\])?", corps)]
        while lignes and not lignes[-1].strip():
            lignes.pop()
        if base in ("cases", "dcases", "rcases"):
            elements = [self.sous(l.strip()) for l in lignes]
            return "cases(" + ("reverse: #true, " if base == "rcases" else "") + ", ".join(elements) + ")"
        if base in MATRICES:
            rangees = []
            for l in lignes:
                cellules = [self.sous(c.strip()) or '""' for c in _couper_esperluettes(l)]
                rangees.append(", ".join(cellules))
            delim = MATRICES[base]
            return "mat(delim: " + delim + ", " + "; ".join(rangees) + ")"
        if base in ("aligned", "align", "split", "gathered", "alignedat", "eqnarray"):
            return " \\\n".join(self.sous(l.strip()) for l in lignes)
        self.inconnues.append("\\begin{" + nom + "}")
        del etoile
        return ""


def _couper_esperluettes(ligne: str) -> List[str]:
    parts, prof, cour = [], 0, ""
    i = 0
    while i < len(ligne):
        c = ligne[i]
        if c == "\\" and i + 1 < len(ligne):
            cour += ligne[i: i + 2]
            i += 2
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
        if c == "&" and prof == 0:
            parts.append(cour)
            cour = ""
        else:
            cour += c
        i += 1
    parts.append(cour)
    return parts


def _texte_brut(t: str) -> str:
    t = t.replace("\\,", " ").replace("\\ ", " ").replace("~", " ").replace("\\;", " ").replace("{", "").replace("}", "")
    t = t.replace("\\%", "%").replace("\\&", "&").replace("\\_", "_")
    return t.replace("\\", "\\\\").replace('"', '\\"')


def _unite(u: str) -> str:
    u = u.replace("\\per", "/").replace("\\square", "²").replace("\\cubic", "³")
    u = re.sub(r"\\(kilo|centi|milli|mega|micro)", lambda m: {"kilo": "k", "centi": "c", "milli": "m", "mega": "M", "micro": "µ"}[m.group(1)], u)
    u = re.sub(r"\\(metre|meter|gram|second|litre|liter|hour|minute|euro|percent|degreeCelsius|celsius)",
               lambda m: {"metre": "m", "meter": "m", "gram": "g", "second": "s", "litre": "L", "liter": "L",
                          "hour": "h", "minute": "min", "euro": "€", "percent": "%", "degreeCelsius": "°C",
                          "celsius": "°C"}[m.group(1)], u)
    u = u.replace("^2", "²").replace("^3", "³").replace("^{2}", "²").replace("^{3}", "³").replace(".", "⋅")
    return _texte_brut(u).strip()


def _atome(t: str, indice: bool = False) -> bool:
    """Un seul jeton pour Typst : nombre, lettre, symbole nommé, appel `nom(…)` complet, chaîne.

    `f(x)` n'en est PAS un : une lettre seule suivie de parenthèses fait deux unités en Typst, donc
    `n(n+1)/2` rendrait n × (n+1)/2. Un appel ne compte que pour un nom d'au moins deux lettres.
    Pour un exposant (`indice`), `-1` n'est pas un jeton : `x^-1` doit s'écrire `x^(-1)`."""
    t = t.strip()
    if not t:
        return True
    if re.fullmatch((r"\d+(\.\d+)?" if indice else r"-?\d+(\.\d+)?") + r"|[A-Za-zÀ-ÿ°]|[A-Za-z][A-Za-z.]*|\"[^\"]*\"|'+", t):
        return True
    m = re.fullmatch(r"[A-Za-z][A-Za-z.]+\((.*)\)", t, re.S)
    if m and _equilibre(m.group(1)):
        return True
    if t[0] in "([{" and _ferme_au_bout(t):
        return True
    return False


def _equilibre(t: str) -> bool:
    prof = 0
    for c in t:
        if c in "([{":
            prof += 1
        elif c in ")]}":
            prof -= 1
            if prof < 0:
                return False
    return prof == 0


def _ferme_au_bout(t: str) -> bool:
    prof = 0
    for k, c in enumerate(t):
        if c in "([{":
            prof += 1
        elif c in ")]}":
            prof -= 1
            if prof == 0 and k != len(t) - 1:
                return False
    return prof == 0


def _parentheser(t: str, indice: bool = False) -> str:
    """Parenthèses (invisibles en Typst) autour d'un numérateur, d'un dénominateur ou d'un exposant."""
    t = t.strip()
    if not t:
        return '""'
    if _atome(t, indice):
        return t
    return "(" + t + ")"


SANS_ESPACE_AVANT = ("^", "_", "'", ")", ",", "!", "°")
SANS_ESPACE_APRES = ("(",)


def _normes(morceaux: List[str]) -> List[str]:
    """`|| u ||` (\\| … \\|) → `norm(u)`, quand les deux barres doubles se répondent."""
    sortie: List[str] = []
    i = 0
    while i < len(morceaux):
        if morceaux[i] == "||":
            try:
                j = morceaux.index("||", i + 1)
            except ValueError:
                j = -1
            if j > i + 1:
                sortie.append("norm(" + joindre(morceaux[i + 1: j]) + ")")
                i = j + 1
                continue
        sortie.append(morceaux[i])
        i += 1
    return sortie


def joindre(morceaux: List[str]) -> str:
    """Assemble les morceaux en mettant un espace là où Typst en a besoin (et là où il aide à lire)."""
    morceaux = _normes(morceaux)
    sortie = ""
    for m in morceaux:
        if not sortie:
            sortie = m
            continue
        if m.startswith(SANS_ESPACE_AVANT) or sortie.endswith(SANS_ESPACE_APRES) or sortie.endswith("\n"):
            sortie += m
            continue
        a, b = sortie[-1], m[0]
        if b == "(" and re.search(r"[_^][A-Za-z0-9]+$", sortie):
            # « P_A(B) » : collé, Typst lirait A(B) comme UNE unité et la mettrait toute en indice
            sortie += " " + m
            continue
        if b == "(" and (a.isalnum() or a == "'"):
            # f(x), x^2(…) : pas d'espace avant une parenthèse qui suit une lettre
            sortie += m
            continue
        if b in "+-=<>" or a in "+-=<>":
            sortie += " " + m
            continue
        if (a.isalnum() or a in "\"')]}.") and (b.isalnum() or b in "\"#("):
            sortie += " " + m
            continue
        if a in "|" and b.isalnum() or b == "|" and a.isalnum():
            sortie += m
            continue
        sortie += " " + m
    sortie = re.sub(r" {2,}", " ", sortie)
    # signe unaire en tête, après une parenthèse, un crochet ou un séparateur : « -3 », « +oo »
    sortie = re.sub(r"(^|[(\[\],;&{]) ?([-+]) (?=\d|[A-Za-z(])",
                    lambda mm: mm.group(1) + (" " if mm.group(1) in "];,{" and mm.group(1) else "") + mm.group(2),
                    sortie)
    # après une relation ou un opérateur : « = -1 », « < -2 », « in -3 »
    sortie = re.sub(r"((?:[=<>:]|<=|>=|!=|\bin|\bunion|\binter|\btimes|\bdiv|\bapprox|\bslant|=>|->) )([-+]) (?=\d|[A-Za-z(])",
                    r"\1\2", sortie)
    return sortie.strip(" ")


def convertir(source: str, display: bool = False, macros: Optional[Dict[str, Callable]] = None,
              macros_utilisateur: Optional[Dict[str, dict]] = None) -> Resultat:
    c = Convertisseur(source, macros, display, macros_utilisateur)
    texte = c.convertir()
    return Resultat(texte, c.inconnues)
