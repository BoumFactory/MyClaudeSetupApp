"""Analyse d'un corps LaTeX en arbre de nœuds, chaque nœud gardant sa position dans le source.

La position (`debut`, `fin`) permet de retrouver le LaTeX exact d'un nœud : c'est ce texte qui part dans un
extrait `#latex[…]` quand un nœud n'a pas d'équivalent Typst ou que sa traduction ne compile pas.

Nœuds :
  Texte(s)              texte ordinaire (espaces et sauts de ligne simples compris)
  Par()                 ligne vide : nouveau paragraphe
  Groupe(enfants)       { … }
  Cmd(nom, etoile, args)    \\nom*[…]{…} ; args : liste d'Arg(genre « o » | « m » | « v », enfants, brut)
  Env(nom, args, enfants)   \\begin{nom}…\\end{nom} ; `brut_corps` pour les environnements verbatim
  Maths(source, mode)   $…$, \\(…\\), \\[…\\], $$…$$, align, equation… (source LaTeX brute)
  Si(nom, alors, sinon) \\ifcorrection … \\else … \\fi
  Car(c)                caractère spécial : « ~ », « & »
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

ENV_MATHS = {"align", "align*", "equation", "equation*", "gather", "gather*", "multline", "multline*",
             "eqnarray", "eqnarray*", "displaymath", "math", "flalign", "flalign*", "alignat", "alignat*"}
ENV_BRUTS = {"verbatim", "verbatim*", "lstlisting", "minted", "tikzpicture", "pspicture", "pspicture*",
             "pgfpicture", "tikzcd", "circuitikz", "forest", "asy", "axis", "comment", "filecontents",
             "filecontents*", "scratch", "Verbatim", "BVerbatim", "pythoncode", "python", "pycode",
             "tkzexample", "luacode", "luacode*", "sagesilent", "tcblisting", "codePython", "BFCodePython",
             "Tableur", "tabvar", "variations"}
IFS_NEUTRES = {"ifx", "ifnum", "ifdim", "ifcase", "ifodd", "ifthenelse", "ifdefined", "ifcsname", "iftrue",
               "iffalse", "ifmmode", "ifvmode", "ifhmode", "ifinner", "ifcat", "ifvoid", "ifeof"}


@dataclass
class Noeud:
    debut: int = 0
    fin: int = 0


@dataclass
class Texte(Noeud):
    s: str = ""


@dataclass
class Par(Noeud):
    pass


@dataclass
class Car(Noeud):
    c: str = ""


@dataclass
class Groupe(Noeud):
    enfants: List[Noeud] = field(default_factory=list)


@dataclass
class Arg:
    genre: str  # "o", "m", "v", "s", "t"
    enfants: List[Noeud] = field(default_factory=list)
    brut: str = ""
    debut: int = 0
    fin: int = 0
    present: bool = True


@dataclass
class Cmd(Noeud):
    nom: str = ""
    etoile: bool = False
    args: List[Arg] = field(default_factory=list)

    def arg(self, genre: str, rang: int = 0) -> Optional[Arg]:
        trouves = [a for a in self.args if a.genre == genre and a.present]
        return trouves[rang] if rang < len(trouves) else None


@dataclass
class Env(Noeud):
    nom: str = ""
    args: List[Arg] = field(default_factory=list)
    enfants: List[Noeud] = field(default_factory=list)
    brut_corps: str = ""
    corps_debut: int = 0
    corps_fin: int = 0

    def arg(self, genre: str, rang: int = 0) -> Optional[Arg]:
        trouves = [a for a in self.args if a.genre == genre and a.present]
        return trouves[rang] if rang < len(trouves) else None


@dataclass
class Maths(Noeud):
    source: str = ""
    mode: str = "inline"  # "inline" | "display" | nom d'environnement (align*, equation…)


@dataclass
class Si(Noeud):
    nom: str = ""
    alors: List[Noeud] = field(default_factory=list)
    sinon: Optional[List[Noeud]] = None


class Analyseur:
    def __init__(self, texte: str, signatures: Dict[str, Dict[str, str]]):
        self.t = texte
        self.n = len(texte)
        self.cmds = signatures.get("commandes", {})
        self.envs = signatures.get("environnements", {})

    # ------------------------------------------------------------------ utilitaires
    def _espaces(self, i: int, sauts: bool = True) -> int:
        """Saute les espaces (et un seul saut de ligne si `sauts`, jamais une ligne vide)."""
        nl = 0
        while i < self.n and self.t[i] in " \t\n":
            if self.t[i] == "\n":
                nl += 1
                if not sauts or nl > 1:
                    break
            i += 1
        return i

    def _fin_groupe(self, i: int) -> int:
        """t[i] == '{' : indice du '}' correspondant."""
        prof = 0
        while i < self.n:
            c = self.t[i]
            if c == "\\":
                i += 2
                continue
            if c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
                if prof == 0:
                    return i
            i += 1
        return self.n - 1

    def _fin_crochet(self, i: int) -> int:
        """t[i] == '[' : indice du ']' fermant, hors groupes {…}."""
        prof = 0
        j = i + 1
        while j < self.n:
            c = self.t[j]
            if c == "\\":
                j += 2
                continue
            if c == "{":
                prof += 1
            elif c == "}":
                prof -= 1
            elif c == "]" and prof == 0:
                return j
            elif c == "\n" and self.t[j + 1: j + 2] == "\n" and prof == 0:
                return -1  # pas de ligne vide dans un argument facultatif
            j += 1
        return -1

    # ------------------------------------------------------------------ arguments
    def lire_args(self, i: int, sig: str, nom: str = "") -> (List[Arg], int):
        args: List[Arg] = []
        elements = sig.split()
        for k, e in enumerate(elements):
            dernier = k == len(elements) - 1
            if e == "s":
                if i < self.n and self.t[i] == "*":
                    args.append(Arg("s", brut="*", debut=i, fin=i + 1))
                    i += 1
                else:
                    args.append(Arg("s", present=False))
                continue
            if e.startswith("t"):
                c = e[1:2]
                j = self._espaces(i, sauts=False)
                if self.t[j: j + 1] == c:
                    args.append(Arg("t", brut=c, debut=j, fin=j + 1))
                    i = j + 1
                else:
                    args.append(Arg("t", present=False))
                continue
            if e == "o" or e.startswith("d"):
                ouvrant = "[" if e == "o" else e[1:2]
                j = self._espaces(i, sauts=not dernier)
                if self.t[j: j + 1] == ouvrant:
                    fin = self._fin_crochet(j) if ouvrant == "[" else self.t.find(e[2:3], j + 1)
                    if fin > 0:
                        brut = self.t[j + 1: fin]
                        args.append(Arg("o", self.analyser(j + 1, fin), brut, j, fin + 1))
                        i = fin + 1
                        continue
                args.append(Arg("o", present=False))
                continue
            if e == "v":
                j = self._espaces(i)
                if j < self.n:
                    delim = self.t[j]
                    fermant = "}" if delim == "{" else delim
                    fin = self._fin_groupe(j) if delim == "{" else self.t.find(fermant, j + 1)
                    args.append(Arg("v", brut=self.t[j + 1: fin], debut=j, fin=fin + 1))
                    i = fin + 1
                continue
            # obligatoire
            j = self._espaces(i)
            if j >= self.n:
                args.append(Arg("m", present=False))
                continue
            c = self.t[j]
            if c == "{":
                fin = self._fin_groupe(j)
                args.append(Arg("m", self.analyser(j + 1, fin), self.t[j + 1: fin], j, fin + 1))
                i = fin + 1
            elif c == "\\":
                m = re.match(r"\\([A-Za-z@]+|.)", self.t[j:])
                args.append(Arg("m", self.analyser(j, j + m.end()), m.group(0), j, j + m.end()))
                i = j + m.end()
            elif c in "}]":
                args.append(Arg("m", present=False))
            else:
                args.append(Arg("m", [Texte(j, j + 1, c)], c, j, j + 1))
                i = j + 1
        return args, i

    def _args_inconnus(self, i: int) -> (List[Arg], int):
        """Commande sans signature : arguments collés à la commande ([…] puis {…} sans espace)."""
        args: List[Arg] = []
        while i < self.n and self.t[i] in "[{":
            if self.t[i] == "[":
                fin = self._fin_crochet(i)
                if fin < 0:
                    break
                args.append(Arg("o", self.analyser(i + 1, fin), self.t[i + 1: fin], i, fin + 1))
                i = fin + 1
            else:
                fin = self._fin_groupe(i)
                args.append(Arg("m", self.analyser(i + 1, fin), self.t[i + 1: fin], i, fin + 1))
                i = fin + 1
        return args, i

    # ------------------------------------------------------------------ maths
    def _fin_maths(self, i: int, fermant: str) -> int:
        j = i
        while j < self.n:
            if self.t[j] == "\\":
                if self.t.startswith(fermant, j) and fermant.startswith("\\"):
                    return j
                j += 2
                continue
            if self.t.startswith(fermant, j):
                return j
            j += 1
        return -1

    def _fin_env(self, nom: str, i: int) -> (int, int):
        """Début et fin de \\end{nom} correspondant (imbrication du même nom comptée)."""
        motif = re.compile(r"\\(begin|end)\s*\{" + re.escape(nom) + r"\}")
        prof = 1
        for m in motif.finditer(self.t, i):
            prof += 1 if m.group(1) == "begin" else -1
            if prof == 0:
                return m.start(), m.end()
        return self.n, self.n

    # ------------------------------------------------------------------ analyse
    def analyser(self, debut: int = 0, fin: Optional[int] = None) -> List[Noeud]:
        fin = self.n if fin is None else fin
        noeuds, _ = self._suite(debut, fin, arrets=())
        return noeuds

    def _suite(self, i: int, fin: int, arrets) -> (List[Noeud], int):
        """Lit une suite de nœuds jusqu'à `fin`, ou jusqu'à une commande de `arrets` (\\else, \\fi)."""
        noeuds: List[Noeud] = []
        tampon_debut = i

        def vider(j):
            nonlocal tampon_debut
            if j > tampon_debut:
                morceau = self.t[tampon_debut:j]
                # lignes vides → Par
                pos = tampon_debut
                for partie in re.split(r"(\n[ \t]*\n\s*)", morceau):
                    if not partie:
                        continue
                    if re.fullmatch(r"\n[ \t]*\n\s*", partie):
                        noeuds.append(Par(pos, pos + len(partie)))
                    else:
                        noeuds.append(Texte(pos, pos + len(partie), partie))
                    pos += len(partie)
            tampon_debut = j

        while i < fin:
            c = self.t[i]
            if c == "\\":
                m = re.match(r"\\([A-Za-z@]+)(\*?)|\\(.)", self.t[i:fin], re.S)
                if not m:
                    i += 1
                    continue
                if m.group(3) is not None:  # \X : symbole
                    s = m.group(3)
                    if s in "([":
                        vider(i)
                        fermant = "\\)" if s == "(" else "\\]"
                        j = self._fin_maths(i + 2, fermant)
                        if j < 0:
                            j = fin
                        noeuds.append(Maths(i, j + 2, self.t[i + 2: j], "inline" if s == "(" else "display"))
                        i = j + 2
                        tampon_debut = i
                        continue
                    vider(i)
                    if s == "\\":
                        args, k = self.lire_args(i + 2, "s o")
                        noeuds.append(Cmd(i, k, "\\\\", False, args))
                        i = k
                    else:
                        noeuds.append(Cmd(i, i + 2, s, False, []))
                        i += 2
                    tampon_debut = i
                    continue
                nom = m.group(1)
                if nom in arrets:
                    vider(i)
                    return noeuds, i
                vider(i)
                debut_cmd = i
                i += len(nom) + 1
                if nom == "begin":
                    noeud, i = self._environnement(debut_cmd, i, fin)
                    noeuds.append(noeud)
                    tampon_debut = i
                    continue
                if nom == "end":  # \end orphelin : on l'ignore
                    _, i = self._args_inconnus(i)
                    tampon_debut = i
                    continue
                if nom.startswith("if") and nom not in IFS_NEUTRES and nom != "if":
                    noeud, i = self._conditionnelle(debut_cmd, nom, i, fin)
                    noeuds.append(noeud)
                    tampon_debut = i
                    continue
                etoile = False
                sig = self.cmds.get(nom + "*") if m.group(2) else None
                if sig is None:
                    sig = self.cmds.get(nom)
                    if m.group(2):
                        if sig is not None and sig.startswith("s"):
                            pass  # l'étoile sera lue par la signature
                        else:
                            etoile = True
                            i += 1
                if sig is None:
                    args, i = self._args_inconnus(i)
                else:
                    if not sig.startswith("s") and m.group(2) and not etoile:
                        i += 1
                        etoile = True
                    args, i = self.lire_args(i, sig, nom)
                    if any(a.genre == "s" and a.present for a in args):
                        etoile = True
                noeuds.append(Cmd(debut_cmd, i, nom, etoile, args))
                # LaTeX mange l'espace qui suit une commande sans argument : on fait de même
                if not args and i < fin and self.t[i] in " \t":
                    i += 1
                tampon_debut = i
                continue
            if c == "$":
                vider(i)
                double = self.t.startswith("$$", i)
                fermant = "$$" if double else "$"
                j = self._fin_maths(i + len(fermant), fermant)
                if j < 0:
                    j = fin
                noeuds.append(Maths(i, j + len(fermant), self.t[i + len(fermant): j], "display" if double else "inline"))
                i = j + len(fermant)
                tampon_debut = i
                continue
            if c == "{":
                vider(i)
                j = self._fin_groupe(i)
                noeuds.append(Groupe(i, j + 1, self.analyser(i + 1, j)))
                i = j + 1
                tampon_debut = i
                continue
            if c in "~&":
                vider(i)
                noeuds.append(Car(i, i + 1, c))
                i += 1
                tampon_debut = i
                continue
            if c == "}":  # accolade orpheline
                vider(i)
                i += 1
                tampon_debut = i
                continue
            i += 1
        vider(min(i, fin))
        return noeuds, i

    def _environnement(self, debut: int, i: int, fin: int):
        m = re.match(r"\s*\{([^}]+)\}", self.t[i:])
        if not m:
            return Texte(debut, i, ""), i
        nom = m.group(1).strip()
        i += m.end()
        corps_debut_brut = i
        if nom in ENV_MATHS:
            d, f = self._fin_env(nom, i)
            return Maths(debut, f, self.t[i:d], nom), f
        sig = self.envs.get(nom, "")
        args, i = self.lire_args(i, sig, nom) if sig else ([], i)
        d, f = self._fin_env(nom, i)
        env = Env(debut, f, nom, args, [], self.t[i:d], i, d)
        if nom not in ENV_BRUTS:
            env.enfants = self.analyser(i, d)
        del corps_debut_brut
        return env, f

    def _conditionnelle(self, debut: int, nom: str, i: int, fin: int):
        """\\ifnom … [\\else …] \\fi, avec les \\if imbriqués."""
        alors, j = self._suite_si(i, fin)
        sinon = None
        if self.t.startswith("\\else", j):
            sinon, j = self._suite_si(j + len("\\else"), fin)
        if self.t.startswith("\\fi", j):
            j += len("\\fi")
        return Si(debut, j, nom, alors, sinon), j

    def _suite_si(self, i: int, fin: int):
        """Nœuds jusqu'au \\else ou \\fi de même niveau."""
        # on cherche d'abord l'étendue en comptant les \if…
        prof = 0
        j = i
        motif = re.compile(r"\\(if[A-Za-z@]*|else|fi)(?![A-Za-z@])")
        while True:
            m = motif.search(self.t, j, fin)
            if not m:
                break
            mot = m.group(1)
            if mot.startswith("if") and mot != "if" or mot == "if":
                if mot not in ("ifx",) or True:
                    prof += 1
            elif mot == "fi":
                if prof == 0:
                    return self.analyser(i, m.start()), m.start()
                prof -= 1
            elif mot == "else" and prof == 0:
                return self.analyser(i, m.start()), m.start()
            j = m.end()
        return self.analyser(i, fin), fin
