"""Conversion de l'arbre LaTeX en Typst bfcours-typst, lisible et indenté.

Principes :
- une commande bfcours garde son nom (règle R1 de la suite) ; ses options deviennent des clés validées
  contre l'index (`catalogue.py`) ; une clé inconnue est écartée et notée, jamais devinée ;
- les largeurs relatives restent relatives : `0.45\\linewidth` → `45%`, colonnes de minipages → `largeurs:` ;
- ce qui n'a pas d'équivalent (figure TikZ, environnement inconnu) devient un extrait `#latex[…]`, rendu
  par LaTeX à la compilation : fidèle, et marqué pour que l'agent décide de le redessiner ou non ;
- chaque nœud « repliable » est entouré de marqueurs invisibles ; si Typst refuse une ligne, la réparation
  (reparation.py) retrouve le nœud fautif et le replie (extrait LaTeX, ou marqueur orange en ligne).
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

import localiser
from . import maths, regles
from .analyse import Analyseur, Arg, Car, Cmd, Env, Groupe, Maths, Noeud, Par, Si, Texte
from .catalogue import Catalogue, Fonction
from .lecture import Document
from .signatures import definitions
from .traductions import Traductions

from .ecriture import (FER, INDENT, OUV, SEP, chaine, cle_id as _cle_id, construire_appel, crochets,
                       fin_groupe as _fin_groupe, ident as _ident, indenter, num as _num,
                       sans_marqueurs as _sans_marqueurs, texte_simple as _texte_simple, virgule as _vir)

ACCENTS_TEXTE = {
    ("'", "e"): "é", ("'", "E"): "É", ("`", "e"): "è", ("`", "E"): "È", ("^", "e"): "ê", ("^", "E"): "Ê",
    ('"', "e"): "ë", ("`", "a"): "à", ("`", "A"): "À", ("^", "a"): "â", ("^", "A"): "Â", ("^", "i"): "î",
    ("^", "\\i"): "î", ('"', "i"): "ï", ('"', "\\i"): "ï", ("^", "o"): "ô", ("^", "O"): "Ô", ("`", "u"): "ù",
    ("^", "u"): "û", ('"', "u"): "ü", ("c", "c"): "ç", ("c", "C"): "Ç", ("'", "a"): "á", ("'", "o"): "ó",
    ("'", "i"): "í", ("'", "u"): "ú", ("~", "n"): "ñ", ('"', "o"): "ö", ('"', "a"): "ä",
}
SYMBOLES_TEXTE = {
    "oe": "#oe", "OE": "#oe-maj", "ae": "æ", "AE": "Æ", "euro": "#euro", "officialeuro": "#euro", "EUR": "#euro",
    "degres": "°",
    "textdegree": "°", "degree": "°", "ldots": "…", "dots": "…", "textbullet": "•", "S": "§", "P": "¶",
    "LaTeX": "LaTeX", "TeX": "TeX", "textasciitilde": "\\~", "textbackslash": "\\\\", "copyright": "©",
    "textregistered": "®", "texttrademark": "™", "dag": "†", "textendash": "–", "textemdash": "—",
    "guillemotleft": "«", "guillemotright": "»", "og": "«~", "fg": "~»", "i": "ı", "ss": "ß", "o": "ø",
    "checkmark": "✓", "textquotesingle": "'", "quad": "#h(1em)", "qquad": "#h(2em)", ",": "#h(0.17em)",
    " ": " ", "@": "", "/": "", "-": "", "&": "&", "%": "%", "$": "\\$", "#": "\\#", "_": "\\_", "{": "{",
    "}": "}", "textunderscore": "\\_", "pourcent": "%", "nombre": "", "texteuro": "#euro", "eurologo": "#euro",
    "textperthousand": "‰", "textonehalf": "½", "texttimes": "×", "textdiv": "÷", "textpm": "±",
    "textless": "\\<", "textgreater": ">", "textbar": "|", "textsection": "§", "textellipsis": "…",
    "ier": "#super[er]", "iere": "#super[re]", "ieme": "#super[e]",
}


@dataclass
class Rapport:
    a_reprendre: List[str] = field(default_factory=list)
    extraits: List[str] = field(default_factory=list)
    cles_ecartees: List[str] = field(default_factory=list)
    ignorees: Dict[str, int] = field(default_factory=dict)
    inconnues: Dict[str, int] = field(default_factory=dict)
    images: List[str] = field(default_factory=list)
    replis: List[str] = field(default_factory=list)
    extraits_codes: List[str] = field(default_factory=list)

    def compter(self, table: Dict[str, int], nom: str):
        table[nom] = table.get(nom, 0) + 1


@dataclass
class Region:
    cle: Tuple
    mode: str  # "bloc" (extrait LaTeX) | "ligne" (marqueur orange) | "supprimer"
    source: str
    description: str


class Conversion(Traductions):
    def __init__(self, doc: Document, cat: Catalogue, signatures, sortie: Path, replis: Optional[Set] = None,
                 nom: str = "document"):
        self.doc = doc
        self.cat = cat
        self.sig = signatures
        self.sortie = sortie
        self.dossier_source = doc.maitre.parent
        self.nom = nom
        self.replis_demandes: Set = set(replis or ())
        self.rapport = Rapport()
        self.regions: Dict[int, Region] = {}
        self.compteur = 0
        self.texte = ""  # texte en cours d'analyse (corps, ou corps d'une macro dépliée)
        self.pile_textes: List[Tuple[str, str]] = []
        self.contexte = "corps"
        self.niveau = 0  # profondeur de contenant (0 : niveau du document)
        self.dans_exo = False
        self.dans_si = False
        self.zones_maths: List[str] = []  # zones de réponse rencontrées dans les formules
        self.paquets_latex: Set[str] = set()
        self.bfcours_latex = False
        self.utilise_extraits = False
        self.utilise_reprendre = False
        self.modele: Dict[str, str] = {}
        self.premier_bandeau = True
        self.reglages_tete: List[str] = []
        defs = definitions(doc.preambule)
        self.macros: Dict[str, dict] = defs["corps"]
        self.preambule_latex: List[str] = []
        self._lire_preambule()
        corps_defs = definitions(doc.corps)
        for k, v in corps_defs["corps"].items():
            self.macros.setdefault(k, v)
        for k, v in corps_defs["commandes"].items():
            self.sig["commandes"].setdefault(k, v)
        for k, v in corps_defs["environnements"].items():
            self.sig["environnements"].setdefault(k, v)

    # ===================================================================== préambule
    def _lire_preambule(self):
        p = self.doc.preambule
        d = definitions(p)
        for k, v in d["commandes"].items():
            self.sig["commandes"].setdefault(k, v)
        for k, v in d["environnements"].items():
            self.sig["environnements"].setdefault(k, v)
        # marges
        m = re.search(r"\\usepackage\s*\[([^\]]*)\]\s*\{geometry\}", p) or re.search(r"\\geometry\s*\{([^}]*)\}", p)
        if m:
            marges = []
            for k, v in self._options(m.group(1)):
                if k in ("left", "right", "top", "bottom") and v:
                    marges.append(f"{k}: {self._longueur(v)}")
                elif k == "margin" and v:
                    marges = [f"{c}: {self._longueur(v)}" for c in ("left", "right", "top", "bottom")]
            if marges:
                self.modele["marges"] = "(" + ", ".join(marges) + ")"
        opts = self.doc.classe_options
        mt = re.search(r"(\d+)pt", opts)
        if mt and mt.group(1) not in ("12",):
            pass  # bfcours-fonts impose 12 pt : la taille de classe est sans effet
        if "fleqn" not in opts and "\\documentclass" in p:
            self.modele["fleqn"] = "false"
        if re.search(r"\\usepackage\{bfcours-fonts-dys\}", p):
            self.modele["dys"] = "true"
        # lignes reprises dans le préambule des extraits LaTeX
        for motif in (r"\\usetikzlibrary\s*\{[^}]*\}", r"\\usepgfplotslibrary\s*\{[^}]*\}", r"\\pgfplotsset\s*\{",
                      r"\\tikzset\s*\{", r"\\definecolor\s*\{[^}]*\}\s*\{[^}]*\}\s*\{[^}]*\}",
                      r"\\colorlet\s*\{[^}]*\}\s*\{[^}]*\}"):
            for mm in re.finditer(motif, p):
                debut = mm.start()
                fin = mm.end()
                if p[fin - 1] == "{":
                    fin = _fin_groupe(p, fin - 1)
                self.preambule_latex.append(p[debut:fin])
        # réglages bfcours du préambule : repris après #show: modele(…)
        an = Analyseur(p, self.sig)
        self.texte = p
        for n in an.analyser():
            if isinstance(n, Cmd) and n.nom in ("setrdexo", "setrdcrep", "displayitempointstrue",
                                                 "displayitempointsfalse", "setrdmcq", "sisetup"):
                r = self._cmd(n, [n], 0)[0]
                if r and r.strip():
                    self.reglages_tete.append(_sans_marqueurs(r))
            elif isinstance(n, Cmd) and n.nom == "def" and False:
                pass
        m = re.search(r"\\def\\rdifficulty\{([^}]*)\}", p)
        if m:
            self.reglages_tete.append(f"#rdifficulty({self._nombre(m.group(1)) or 1})")

    # ===================================================================== outils
    def _options(self, brut: str) -> List[Tuple[str, Optional[str]]]:
        """« a=1, b={x,y}, c » → [("a", "1"), ("b", "x,y"), ("c", None)] (virgules de premier niveau)."""
        sortie, prof, cour = [], 0, ""
        for c in brut + ",":
            if c in "{[(":
                prof += 1
            elif c in "}])":
                prof -= 1
            if c == "," and prof == 0:
                if cour.strip():
                    if "=" in cour:
                        k, v = cour.split("=", 1)
                        v = v.strip()
                        if v.startswith("{") and v.endswith("}") and _fin_groupe(v, 0) == len(v):
                            v = v[1:-1]
                        sortie.append((k.strip(), v))
                    else:
                        sortie.append((cour.strip(), None))
                cour = ""
            else:
                cour += c
        return sortie

    def _est_cles(self, brut: str, f: Optional[Fonction] = None) -> bool:
        b = re.sub(r"\$[^$]*\$|\{[^{}]*\}", "", brut)
        if "=" in b:
            return True
        if f is not None:
            items = [k for k, _ in self._options(brut)]
            return bool(items) and all(self.cat.cle(f, k) for k in items)
        return False

    def developper(self, brut: str) -> str:
        """Remplace les variables du document (`\\def\\largeur{3}`, macros sans argument) par leur valeur."""
        for _ in range(6):
            nouveau = re.sub(r"\\([A-Za-z@]+)",
                             lambda m: self.macros[m.group(1)]["corps"]
                             if m.group(1) in self.macros and not self.macros[m.group(1)].get("n") else m.group(0),
                             brut)
            if nouveau == brut:
                break
            brut = nouveau
        return brut

    def _nombre(self, v: str) -> Optional[str]:
        v = self.developper(v)
        v = v.strip().replace("{,}", ".").replace(",", ".")
        return v if re.fullmatch(r"-?\d+(\.\d+)?", v) else None

    def _longueur(self, v: str, relative: bool = True) -> str:
        """Longueur LaTeX → Typst : relatif en % (largeur de ligne), unités gardées, ex → em, bp → pt."""
        v = self.developper(v).strip().replace(" ", "")
        m = re.fullmatch(r"(-?[\d.]*)\\(linewidth|textwidth|columnwidth|hsize|paperwidth|textheight)", v)
        if m:
            k = float(m.group(1)) if m.group(1) not in ("", "-") else (-1.0 if m.group(1) == "-" else 1.0)
            if m.group(2) == "textheight":
                return f"{_num(k * 25)}cm"
            return f"{_num(k * 100)}%"
        m = re.fullmatch(r"(-?[\d.]*)\\baselineskip", v)
        if m:
            k = float(m.group(1)) if m.group(1) not in ("", "-") else 1.0
            return f"{_num(k * 1.2)}em"
        m = re.fullmatch(r"(-?\d*\.?\d+)(pt|cm|mm|em|in|bp|ex|pc|sp|dd)?", v)
        if m:
            n, u = m.group(1), m.group(2) or "pt"
            if n.startswith("."):
                n = "0" + n
            if n.startswith("-."):
                n = "-0" + n[1:]
            if u == "ex":
                return f"{_num(float(n) * 0.5)}em"
            if u in ("bp", "dd", "pc", "sp"):
                return f"{n}pt"
            return n + u
        if v in ("\\fill", "\\stretch{1}"):
            return "1fr"
        return chaine(v)

    def _valeur(self, f: Optional[Fonction], cle: str, v: Optional[str]) -> str:
        """Valeur d'une option LaTeX → expression Typst."""
        if v is None or v == "":
            return "true"
        v = v.strip()
        if v in ("true", "false"):
            return v
        if v == "none":
            return "none"
        n = self._nombre(v)
        if n is not None:
            return n
        if re.fullmatch(r"-?[\d.]+\s*(pt|cm|mm|em|ex|in|bp)|-?[\d.]*\\(linewidth|textwidth|baselineskip)", v):
            return self._longueur(v)
        if v.startswith("{") and "}{" in v:  # R6 : {a}{b} → tableau
            parts = re.findall(r"\{([^{}]*)\}", v)
            return "(" + ", ".join(self._valeur(f, cle, p) for p in parts) + ")"
        if "=" in re.sub(r"\{[^{}]*\}", "", v):  # clés imbriquées (R5)
            return "(" + ", ".join(f"{_cle_id(k)}: {self._valeur(None, k, w)}" for k, w in self._options(v)) + ")"
        if v.startswith("\\") or "$" in v:
            return chaine(v)
        return chaine(v)

    def cles(self, f: Optional[Fonction], brut: str, quoi: str) -> List[str]:
        """Options LaTeX → « clé: valeur » validées contre l'index ; les autres sont notées."""
        sortie, ecartees = [], []
        for k, v in self._options(brut):
            if k in regles.CLES_IGNOREES:
                ecartees.append(f"{k} ({regles.CLES_IGNOREES[k]})")
                continue
            if "/" in k:  # sous-chemin pgf → dictionnaire (R5)
                tete, reste = k.split("/", 1)
                cle_t = self.cat.cle(f, tete) if f else tete
                if cle_t:
                    sortie.append(f"{_cle_id(cle_t)}: ({_cle_id(re.sub(r'[ ]+', '-', reste))}: {self._valeur(None, reste, v)})")
                else:
                    ecartees.append(k)
                continue
            cle_t = self.cat.cle(f, k) if f else re.sub(r"\s+", "-", k)
            if cle_t is None and f is not None and self.cat.accepte_tout(f):
                cle_t = re.sub(r"\s+", "-", k)
            if cle_t is None:
                ecartees.append(k + ("=" + v if v else ""))
                continue
            sortie.append(f"{_cle_id(cle_t)}: {self._valeur(f, cle_t, v)}")
        if ecartees:
            self.rapport.cles_ecartees.append(f"{quoi} : " + ", ".join(ecartees))
        return sortie

    # ===================================================================== marqueurs
    def _cle_noeud(self, n: Noeud) -> Tuple:
        return (self.contexte, type(n).__name__, n.debut, n.fin)

    def region(self, n: Noeud, texte: str, mode: str, description: str = "") -> str:
        self.compteur += 1
        i = self.compteur
        self.regions[i] = Region(self._cle_noeud(n), mode, self.texte[n.debut:n.fin], description)
        return f"{OUV}{i}{SEP}{texte}{FER}{i}{SEP}"

    def replie(self, n: Noeud) -> bool:
        return self._cle_noeud(n) in self.replis_demandes

    # ===================================================================== extraits LaTeX
    def extrait(self, code: str, raison: str, env: str = "") -> str:
        """Extrait LaTeX rendu à la compilation (bloc). Deux versions si le code dépend de la correction."""
        self.utilise_extraits = True
        code = code.strip("\n")
        code = self._deplier_tikzinclude(code)
        # `baseline=…` place la figure sur la ligne de texte LaTeX ; rendue seule (standalone), la partie
        # sous la ligne de base est rognée : la clé ne sert à rien dans un extrait, on la retire
        code = re.sub(r"(\\begin\{tikzpicture\}\s*\[[^\]]*?)\s*,?\s*baseline\s*(=\s*(\([^)]*\)|\{[^}]*\}|[^,\]]*))?",
                      r"\1", code)
        code = re.sub(r"\\begin\{tikzpicture\}\s*\[\s*,", r"\\begin{tikzpicture}[", code)
        code = re.sub(r"\\begin\{tikzpicture\}\s*\[\s*\]", r"\\begin{tikzpicture}", code)
        for p in regles.EXTRAITS.get(env, ()):
            self.paquets_latex.add(p)
        for nom, paquets in regles.COMMANDES_EXTRAITS.items():
            if "\\" + nom in code:
                self.paquets_latex.update(paquets)
        if "tkzTab" in code:
            self.paquets_latex.add("tkz-tab")
        if "\\begin{axis}" in code or "\\addplot" in code:
            self.paquets_latex.add("pgfplots")
        if "tkzDef" in code or "tkzDraw" in code:
            self.paquets_latex.add("tkz-euclide")
        if "\\begin{tikzpicture}" in code or "\\tikz" in code:
            self.paquets_latex.add("tikz")
        # le document LaTeX charge bfcours : ses extraits aussi (couleurs, styles, macros comme \ifcorrection)
        if any(mq in code for mq in regles.MARQUEURS_BFCOURS) or re.search(r"\\usepackage(\[[^\]]*\])?\{bfcours\}",
                                                                           self.doc.preambule):
            self.bfcours_latex = True
        moteur = regles.MOTEURS.get(env)
        tete = f'#latex(moteur: "{moteur}")' if moteur else "#latex"
        self.rapport.extraits.append(raison)
        self.rapport.extraits_codes.append(code)
        if re.search(r"\\ifcorrection|tccrep|\\crep\b|begin\{crep\}|tcfillcrep|repsim", code + self._corps_cites(code)):
            self.bfcours_latex = True
            prof = tete + "[```latex\n\\setrdcrep{correction=true}\n" + code + "\n```]"
            eleve = tete + "[```latex\n\\setrdcrep{correction=false}\n" + code + "\n```]"
            return "#ifcorrection[\n" + indenter(prof) + "\n][\n" + indenter(eleve) + "\n]"
        return tete + "[```latex\n" + code + "\n```]"

    def _corps_cites(self, code: str) -> str:
        """Corps des macros du document appelées (directement ou non) par un code LaTeX."""
        vus, a_voir, corps = set(), set(re.findall(r"\\([A-Za-z@]+)", code)), []
        while a_voir:
            nom = a_voir.pop()
            if nom in vus or nom not in self.macros:
                continue
            vus.add(nom)
            corps.append(self.macros[nom]["corps"])
            a_voir |= set(re.findall(r"\\([A-Za-z@]+)", self.macros[nom]["corps"]))
        return "\n".join(corps)

    def _deplier_tikzinclude(self, code: str) -> str:
        def rempl(m):
            d = self.macros.get("tikzfig" + m.group(1))
            return d["corps"] if d else m.group(0)
        for _ in range(3):
            code = re.sub(r"\\tikzinclude\s*\{([^}]*)\}", rempl, code)
        return code

    def a_reprendre(self, source: str, raison: str) -> str:
        self.utilise_reprendre = True
        self.rapport.a_reprendre.append(f"{raison} : {source[:90]}")
        return "#a-reprendre(" + chaine(source.strip()) + ")"

    # ===================================================================== séquences
    def sequence(self, noeuds: Sequence[Noeud]) -> str:
        """Suite de nœuds → balisage Typst (plusieurs lignes possibles)."""
        sortie: List[str] = []  # morceaux ; "\n\n" = paragraphe
        i = 0
        noeuds = list(noeuds)
        while i < len(noeuds):
            n = noeuds[i]
            texte, bloc, j = self.noeud(noeuds, i)
            i = j
            if texte is None:
                continue
            if bloc:
                if sortie and not sortie[-1].endswith("\n"):
                    sortie.append("\n")
                sortie.append(texte.strip("\n") + "\n")
            else:
                if isinstance(n, Par):
                    if sortie and not "".join(sortie[-2:]).endswith("\n\n"):
                        sortie.append("\n\n" if not sortie[-1].endswith("\n") else "\n")
                    continue
                # « #h(1em)(avec » prolongerait l'appel, « #num(3).Suite » lirait un champ, « #oeur » serait un
                # autre nom : un « ; » ferme l'expression (Typst le consomme, il ne s'affiche pas)
                if sortie and texte:
                    avant, apres = _sans_marqueurs(sortie[-1]), _sans_marqueurs(texte)
                    if (re.match(r"\(|\.\w", apres) and re.search(r"#[\w.\-]+(\([^()]*\)|\[[^\[\]]*\])+$", avant)) \
                            or (re.match(r"[\w\-(.\[]", apres) and re.search(r"#[A-Za-z][\w\-]*$", avant)):
                        texte = ";" + texte
                sortie.append(texte)
        texte = "".join(sortie)
        texte = re.sub(r"[ \t]+\n", "\n", texte)
        texte = re.sub(r"\n{3,}", "\n\n", texte)
        return texte.strip("\n ")

    def noeud(self, noeuds: Sequence[Noeud], i: int) -> Tuple[Optional[str], bool, int]:
        """Convertit noeuds[i] (et parfois les suivants). Renvoie (texte, est_bloc, indice suivant)."""
        n = noeuds[i]
        if isinstance(n, Texte):
            return self.texte_brut(n.s), False, i + 1
        if isinstance(n, Par):
            return "", False, i + 1
        if isinstance(n, Car):
            return ("~" if n.c == "~" else "\\&"), False, i + 1
        if isinstance(n, Groupe):
            return self.groupe(n), False, i + 1
        if isinstance(n, Maths):
            if self.replie(n):
                if n.mode == "inline":
                    return self.a_reprendre("$" + n.source + "$", "formule refusée par Typst"), False, i + 1
                return self.extrait(self.texte[n.debut:n.fin], "formule refusée par Typst"), True, i + 1
            t, bloc = self.formule(n)
            return self.region(n, t, "ligne" if not bloc else "bloc", "formule"), bloc, i + 1
        if isinstance(n, Si):
            return self.conditionnelle(n), True, i + 1
        if isinstance(n, Env):
            groupe = getattr(self, "s_" + _ident(n.nom), None)  # environnements qui regroupent leurs voisins
            if groupe is not None:
                t, j = groupe(noeuds, i)
                pseudo = Env(n.debut, noeuds[j - 1].fin, n.nom)
                if self.replie(pseudo):
                    return self.extrait(self.texte[pseudo.debut:pseudo.fin], f"{n.nom} refusé par Typst", n.nom), True, j
                return self.region(pseudo, t, "bloc", n.nom), True, j
            if self.replie(n):
                return self.extrait(self.texte[n.debut:n.fin], f"environnement {n.nom} refusé par Typst", n.nom), True, i + 1
            t = self.environnement(n)
            return self.region(n, t, "bloc", n.nom), True, i + 1
        if isinstance(n, Cmd):
            if self.replie(n):
                src = self.texte[n.debut:n.fin]
                return self.a_reprendre(src, f"\\{n.nom} refusé par Typst"), False, i + 1
            texte, bloc, j = self._cmd(n, noeuds, i)
            if texte is None:
                return None, False, j
            if n.args or bloc:
                texte = self.region(n, texte, "bloc" if bloc else "ligne", "\\" + n.nom)
            return texte, bloc, j
        return None, False, i + 1

    # ===================================================================== texte
    def texte_brut(self, s: str) -> str:
        """Texte LaTeX sans commande → balisage Typst (caractères spéciaux échappés)."""
        s = re.sub(r"\n[ \t]+", "\n", s)
        s = re.sub(r"[ \t]{2,}", " ", s)
        s = s.replace("``", "“").replace("''", "”").replace("<<", "«").replace(">>", "»")
        s = re.sub(r"([\\#*_@<`\[\]$])", r"\\\1", s)
        s = re.sub(r"/(?=[/*])", r"\\/", s)
        # début de ligne : =, -, +, 1. seraient lus comme titre ou liste
        s = re.sub(r"(^|\n)(\s*)([=+\-]|/ |\d+\.)(?=\s)", lambda m: m.group(1) + m.group(2) + "\\" + m.group(3), s)
        return s

    def groupe(self, n: Groupe) -> str:
        """{…} : groupe ; les déclarations qu'il contient (\\small, \\bfseries, \\color) ne valent que dedans."""
        return self.sequence(n.enfants)

    def contenu(self, noeuds: Sequence[Noeud]) -> str:
        """Contenu d'un argument : « [ … ] » en ligne, ou en bloc indenté s'il tient sur plusieurs lignes."""
        self.niveau += 1
        try:
            t = self.sequence(noeuds)
        finally:
            self.niveau -= 1
        return crochets(t)

    def contenu_arg(self, a: Optional[Arg]) -> str:
        return self.contenu(a.enfants if a and a.present else [])

    # ===================================================================== formules
    def macros_maths(self):
        conv = self

        def texte_dans_maths(c: maths.Convertisseur, brut: str) -> str:
            return conv.markup_depuis(brut)

        def vecteur(c):
            return "vect(" + c.arg() + ")"

        def coordonnees(c):
            nom = c._optionnel_brut()
            x, y = c.arg(), c.arg()
            extra = ""
            # 3e coordonnée éventuelle (espace)
            return "coordonnees(" + _vir(x) + ", " + _vir(y) + extra + (", nom: " + c.sous(nom) if nom else "") + ")"

        def intervalle(c):
            forme = c._optionnel_brut()
            a, b = c.arg(), c.arg()
            return "intervalle(" + _vir(a) + ", " + _vir(b) + (f', forme: "{forme.strip()}"' if forme else "") + ")"

        def crochet(cote):
            def f(c):
                taille = c._optionnel_brut()
                t = f'taille: "{taille.strip().lstrip(chr(92))}"' if taille else ""
                return f"crochet{cote.lower()}(" + t + ")"
            return f

        def zone(nom):
            """Zone de réponse (ou mise en valeur) DANS une formule : comme rdcrep, son contenu est une formule."""
            def f(c):
                opt = c._optionnel_brut()
                nb = {"tccrep": 2, "tcfraccrep": 2}.get(nom, 1)
                bruts = [c._groupe_brut() for _ in range(nb)]
                formules = ["[$" + c.sous(b).strip() + "$]" if b.strip() else "[]" for b in bruts]
                cible = {"tcautocrep": "tccrep"}.get(nom, nom)
                f_t = conv.cat.fonction(cible)
                nommes = []
                if opt is not None and opt.strip():
                    if conv._est_cles(opt, f_t):
                        nommes = conv.cles(f_t, opt, "\\" + nom)
                    elif nom == "repsim":
                        nommes = [f"largeur: {conv._longueur(opt)}"]
                    elif nom in ("acc", "surligner"):
                        nommes = [f'couleur: "{opt.strip()}"']
                pos = formules
                if nom == "tccrep":
                    largeur = conv._longueur(bruts[0])
                    pos = [largeur if not largeur.startswith('"') else "auto", formules[1]]
                elif nom == "tcautocrep":
                    pos = ["auto"] + formules
                appel = "#" + construire_appel(cible, pos, nommes, diese=False)
                # dans la formule, un repère : formule() sortira la zone de la formule (comme en LaTeX, où
                # la boîte est posée au niveau du texte ; dans le $…$ de Typst, la zone casserait la ligne)
                conv.zones_maths.append(appel)
                return f"\x11{len(conv.zones_maths) - 1}\x12"
            return f

        def encadrer(c):
            couleur = c._optionnel_brut()
            corps = c.arg()
            return "encadrer(" + corps + (f', couleur: "{couleur}"' if couleur else "") + ")"

        def ensemble(lettre):
            return lambda c: maths.ENSEMBLES[lettre]

        table = {"Vecteur": vecteur, "vv": vecteur, "Coordonnees": coordonnees, "intervalle": intervalle,
                 "CrochetG": crochet("G"), "CrochetD": crochet("D"), "encadrer": encadrer}
        for nom in ("tccrep", "tcfillcrep", "repsim", "tcautocrep", "tcfraccrep", "acc", "voc", "surligner"):
            table[nom] = zone(nom)
        for l in ("R", "N", "Z", "Q", "C", "D"):
            if l not in self.macros:
                table[l] = ensemble(l)
        table["__texte__"] = texte_dans_maths
        return table

    def formule(self, n: Maths) -> Tuple[str, bool]:
        display = n.mode != "inline"
        r = maths.convertir(n.source, display=display, macros=self.macros_maths(), macros_utilisateur=self.macros)
        t = r.texte.strip()
        for inc in r.inconnues:
            self.rapport.compter(self.rapport.inconnues, inc)
        if r.inconnues:
            self.rapport.a_reprendre.append("formule à vérifier (" + ", ".join(sorted(set(r.inconnues))) + ") : $"
                                            + n.source.strip()[:70] + "$")
        if t.startswith(("^", "_")):  # « cm$^2$ » : exposant sans base
            t = '""' + t
        if "\x11" in t:
            morceaux = re.split(r"\x11(\d+)\x12", t)
            # une zone DANS une fraction ou une parenthèse (« \dfrac{1}{\repsim{z}} ») ne peut pas sortir
            # de la formule sans la couper en deux : elle y reste, comme en mode display
            profondeur, imbriquee = 0, False
            for k, m in enumerate(morceaux):
                if k % 2:
                    imbriquee = imbriquee or profondeur > 0
                else:
                    sans_chaines = re.sub(r'"(?:[^"\\]|\\.)*"', "", m)
                    profondeur += sans_chaines.count("(") - sans_chaines.count(")")
            if not display and not imbriquee:  # « $f_1 = \tcfillcrep{…}$ » → « $f_1 =$ #tcfillcrep[…] »
                sortie = []
                for k, m in enumerate(morceaux):
                    if k % 2:
                        sortie.append(self.zones_maths[int(m)])
                    elif m.strip():
                        sortie.append("$" + m.strip().replace("\n", " ") + "$")
                return " ".join(sortie), False
            t = "".join(self.zones_maths[int(m)] if k % 2 else m for k, m in enumerate(morceaux))
        if not display:
            return "$" + t.replace("\n", " ") + "$", False
        lignes = t.split("\n")
        if len(lignes) == 1 and len(t) < 70:
            return "$ " + t + " $", True
        return "$\n" + indenter("\n".join(l.strip() for l in lignes)) + "\n$", True

    def markup_depuis(self, source: str, en_ligne: bool = False) -> str:
        """Convertit un fragment LaTeX (texte) écrit ailleurs (macro, argument de \\text dans une formule)."""
        an = Analyseur(source, self.sig)
        noeuds = an.analyser()
        self.pile_textes.append((self.texte, self.contexte))
        self.texte, self.contexte = source, self.contexte + "›frag"
        try:
            t = self.sequence(noeuds)
        finally:
            self.texte, self.contexte = self.pile_textes.pop()
        t = _sans_marqueurs(t)
        return t if not en_ligne else t.replace("\n", " ")

    # ===================================================================== conditionnelle
    def conditionnelle(self, n: Si) -> str:
        if n.nom != "ifcorrection":
            self.rapport.a_reprendre.append(f"\\{n.nom} : seule la branche « vrai » est gardée")
            return self.sequence(n.alors)
        # #ifcorrection rend son contenu dans le flux : au niveau du document, un saut de page y reste permis
        increment = 1 if self.niveau > 0 else 0
        self.niveau += increment
        ancien, self.dans_si = self.dans_si, True
        try:
            alors = self.sequence(n.alors)
            sinon = self.sequence(n.sinon) if n.sinon is not None else None
        finally:
            self.niveau -= increment
            self.dans_si = ancien
        alors = self.proteger(alors)
        if sinon is None:
            return "#ifcorrection" + crochets(alors)
        return "#ifcorrection" + crochets(alors) + crochets(self.proteger(sinon))

    # ===================================================================== commandes
    def _cmd(self, n: Cmd, noeuds: Sequence[Noeud], i: int) -> Tuple[Optional[str], bool, int]:
        nom = n.nom
        suivant = i + 1
        methode = getattr(self, "c_" + _ident(nom), None)
        if methode is not None:
            r = methode(n, noeuds, i)
            if isinstance(r, tuple):
                return r
            return r, False, suivant
        if nom in regles.IGNOREES:
            self.rapport.compter(self.rapport.ignorees, "\\" + nom)
            return None, False, suivant
        if nom in SYMBOLES_TEXTE:
            return SYMBOLES_TEXTE[nom], False, suivant
        if nom in regles.TAILLES or nom in regles.GRAISSES or nom in ("color", "centering"):
            return self.declaration(n, noeuds, i)
        if nom in regles.ESPACES_V:
            return f"#v({regles.ESPACES_V[nom]})", True, suivant
        if len(nom) == 1 and nom in "'`^\"~c" and n.args == [] and suivant < len(noeuds):
            pass
        if nom in self.macros and nom not in ("tikzinclude",):
            return self.deplier(n, noeuds, i)
        if nom in regles.COMMANDES_EXTRAITS:
            return self.extrait(self.texte[n.debut:n.fin], f"\\{nom}"), True, suivant
        f, imposees = self.cat.pour_latex(nom)
        if f is not None:
            return self.appel(f, n.args, None, imposees, quoi="\\" + nom, etoile=n.etoile), self._est_bloc_f(f), suivant
        # inconnue
        self.rapport.compter(self.rapport.inconnues, "\\" + nom)
        if not n.args:
            return None, False, suivant
        return self.a_reprendre(self.texte[n.debut:n.fin], f"commande inconnue \\{nom}"), False, suivant

    def _est_bloc_f(self, f: Fonction) -> bool:
        return f.paquet in ("farfadet-didactique", "farfadet-exo", "farfadet-qcm", "farfadet-enum",
                            "farfadet-tableaux", "rdboites", "farfadet-modele") and f.nom not in (
            "itempoint", "voc", "vocref", "competence", "liencontent", "coloredsquare", "thetags", "thelabel")

    def deplier(self, n: Cmd, noeuds, i):
        """Macro du document : dépliée (ses arguments substitués), puis convertie."""
        d = self.macros[n.nom]
        corps = d["corps"]
        valeurs = [a.brut for a in n.args if a.present]
        nb = d.get("n", 0)
        if len(valeurs) < nb:  # macro définie avec des arguments mais lue sans signature
            j = i + 1
            while len(valeurs) < nb and j < len(noeuds):
                if isinstance(noeuds[j], Groupe):
                    valeurs.append(self.texte[noeuds[j].debut + 1:noeuds[j].fin - 1])
                    j += 1
                elif isinstance(noeuds[j], Texte) and not noeuds[j].s.strip():
                    j += 1
                else:
                    break
            i = j - 1
        if d.get("defaut") is not None and (not n.args or not n.args[0].present or n.args[0].genre != "o"):
            valeurs = [d["defaut"]] + valeurs
        for k, v in enumerate(valeurs, 1):
            corps = corps.replace("#" + str(k), v)
        if "\\begin{tikzpicture}" in corps or "\\tikz" in corps:
            return self.extrait(corps, f"figure (macro \\{n.nom})", "tikzpicture"), True, i + 1
        profondeur = self.contexte.count("›")
        if profondeur > 6:
            return None, False, i + 1
        an = Analyseur(corps, self.sig)
        self.pile_textes.append((self.texte, self.contexte))
        self.texte, self.contexte = corps, self.contexte + "›" + n.nom
        try:
            noeuds_m = an.analyser()
            t = self.sequence(noeuds_m)
            bloc = any(isinstance(x, (Env, Si)) for x in noeuds_m) or "\n" in t
        finally:
            self.texte, self.contexte = self.pile_textes.pop()
        return (t if t.strip() else None), bloc, i + 1

    def declaration(self, n: Cmd, noeuds, i):
        """\\small, \\bfseries, \\color{…}, \\centering : enveloppent la suite du groupe courant."""
        reste = list(noeuds[i + 1:])
        corps = self.sequence(reste)
        nom = n.nom
        if not corps.strip():
            return None, False, len(noeuds)
        if nom in regles.TAILLES:
            t = f"#text(size: {regles.TAILLES[nom]})" + crochets(corps)
        elif nom in regles.GRAISSES:
            g = regles.GRAISSES[nom]
            t = (f"#{g}" + crochets(corps)) if g else corps
        elif nom == "color":
            c = n.arg("m")
            t = f"#textcolor({chaine(c.brut.strip() if c else 'black')})" + crochets(corps)
        else:  # centering
            t = "#align(center)" + crochets(corps)
        return t, "\n" in corps, len(noeuds)

    # --- appel générique ------------------------------------------------------------------------
    def appel(self, f: Fonction, args: List[Arg], corps: Optional[List[Noeud]], imposees: Dict[str, str],
              quoi: str, etoile: bool = False, extra_pos: Optional[List[str]] = None,
              extra_nommes: Optional[List[str]] = None) -> str:
        """Appel Typst générique : options → clés, arguments → positionnels typés, corps en dernier."""
        positionnels, nommes = self._arguments(f, args, imposees, quoi, etoile, extra_pos, extra_nommes)
        if corps is not None:
            positionnels.append(self.contenu(corps))
        return construire_appel(f.nom, positionnels, nommes, valeur=(f.genre == "valeur"))

    def appel_env(self, f: Fonction, args: List[Arg], corps: Optional[List[Noeud]], imposees: Dict[str, str],
                  quoi: str, extra_pos: Optional[List[str]] = None, extra_nommes: Optional[List[str]] = None) -> str:
        """Syntaxe environnement : `#begin(F, clés)[blocs fixes]`, corps indenté, `#end(F)`."""
        positionnels, nommes = self._arguments(f, args, imposees, quoi, False, extra_pos, extra_nommes)
        return self.begin_end(f.nom, positionnels, nommes, self.corps_env(corps or []))

    def corps_env(self, noeuds: Sequence[Noeud]) -> str:
        """Corps d'un environnement : balisage Typst non entouré de crochets (indenté par `begin_end`)."""
        self.niveau += 1
        try:
            return self.sequence(noeuds)
        finally:
            self.niveau -= 1

    @staticmethod
    def begin_end(nom: str, positionnels: List[str], nommes: List[str], corps: str) -> str:
        """`#begin(nom, positionnels en code, clés)[blocs fixes]`, corps indenté de 2 espaces, `#end(nom)`."""
        tete = construire_appel("begin", [nom] + list(positionnels), list(nommes))
        corps = corps.strip("\n")
        if not _sans_marqueurs(corps).strip():
            return tete + "\n#end(" + nom + ")"
        return tete + "\n" + indenter(corps) + "\n#end(" + nom + ")"

    def proteger(self, t: str) -> str:
        """Contenu placé dans un élément opaque (conditionnelle, align, bloc, cellule) : un begin/end qu'il
        contient n'y serait pas regroupé, d'où `#environnements[…]` autour."""
        if "#begin(" in _sans_marqueurs(t):
            return "#environnements" + crochets(t)
        return t

    def _arguments(self, f: Fonction, args: List[Arg], imposees: Dict[str, str], quoi: str, etoile: bool = False,
                   extra_pos: Optional[List[str]] = None,
                   extra_nommes: Optional[List[str]] = None) -> Tuple[List[str], List[str]]:
        """Arguments LaTeX d'une commande ou d'un environnement → (positionnels, clés) Typst."""
        nommes = [f"{_cle_id(k)}: {v}" for k, v in imposees.items()]
        positionnels: List[str] = list(extra_pos or [])
        noms_opt = list(regles.OPTIONNELS_NOMMES.get(f.nom, regles.OPTIONNELS_NOMMES.get(quoi.lstrip("\\"), [])))
        noms_obl = list(regles.OBLIGATOIRES_NOMMES.get(f.nom, []))
        rang_opt = 0
        rang_obl = 0
        rang_pos = len(positionnels)
        for a in args:
            if a.genre == "s":
                if a.present and "etoile" in f.cles:
                    nommes.append("etoile: true")
                continue
            if a.genre == "o":
                if not a.present:
                    rang_opt += 1
                    continue
                if self._est_cles(a.brut, f):
                    nommes += self.cles(f, a.brut, quoi)
                elif rang_opt < len(noms_opt):
                    cle = noms_opt[rang_opt]
                    if cle:
                        conv = regles.VALEURS_OPTIONNELS.get((f.nom, cle), {})
                        brut = a.brut.strip()
                        v = conv.get(brut) or self._valeur_positionnelle(cle, brut)
                        nommes.append(f"{_cle_id(cle)}: {v}")
                else:
                    positionnels.append(self.contenu(a.enfants))
                rang_opt += 1
                continue
            if a.genre in ("m", "v"):
                if not a.present:
                    continue
                cle = noms_obl[rang_obl] if rang_obl < len(noms_obl) else None
                rang_obl += 1
                if cle:
                    if (f.nom, cle) in regles.CLES_CHAINES:
                        if a.brut.strip():
                            nommes.append(f"{_cle_id(cle)}: {chaine(_texte_simple(a.brut))}")
                    elif a.brut.strip():
                        nommes.append(f"{_cle_id(cle)}: {self.contenu(a.enfants)}")
                    continue
                type_p = f.type_positionnel(rang_pos)
                rang_pos += 1
                positionnels.append(self._positionnel(a, type_p))
        nommes += list(extra_nommes or [])
        return positionnels, nommes

    def _valeur_positionnelle(self, cle: str, brut: str) -> str:
        if cle in ("couleur", "forme", "format", "code", "taille", "nom"):
            if cle == "nom":
                return "[" + self.markup_depuis(brut, True) + "]"
            return chaine(brut.lstrip("\\"))
        n = self._nombre(brut)
        if n is not None:
            return n
        if re.match(r"-?[\d.]+\s*[a-z]{2}|\\", brut):
            return self._longueur(brut)
        return chaine(brut)

    def _positionnel(self, a: Arg, type_p: str) -> str:
        brut = a.brut.strip()
        t = type_p.lower()
        if "content" in t or not t:
            if not t and self._nombre(brut) is not None and not a.enfants or (not t and False):
                return self._nombre(brut)
            return self.contenu(a.enfants)
        if ("length" in t or "ratio" in t) and brut:
            if brut == "auto":
                return "auto"
            return self._longueur(brut)
        if "int" in t or "float" in t:
            n = self._nombre(brut)
            if n is not None:
                return n
        if "str" in t:
            return chaine(_texte_simple(brut))
        if "bool" in t:
            return "true" if brut in ("true", "") else "false"
        return self.contenu(a.enfants)

    # ===================================================================== environnements
    def environnement(self, n: Env) -> str:
        methode = getattr(self, "e_" + _ident(n.nom), None)
        if methode is not None:
            return methode(n)
        if n.nom in regles.EXTRAITS or n.nom in ("tikzpicture",):
            return self.extrait(self.texte[n.debut:n.fin], f"figure ({n.nom})", n.nom)
        f, imposees = self.cat.pour_latex(n.nom)
        if f is not None and f.genre == "fonction":
            if f.nom in regles.FORME_ENVIRONNEMENT:
                return self.appel_env(f, n.args, n.enfants, imposees, quoi=n.nom)
            return self.appel(f, n.args, n.enfants, imposees, quoi=n.nom)
        self.rapport.compter(self.rapport.inconnues, "\\begin{" + n.nom + "}")
        return self.extrait(self.texte[n.debut:n.fin], f"environnement {n.nom} sans équivalent", n.nom)

    # ===================================================================== document complet
    def convertir(self) -> str:
        """Typst complet, AVEC les marqueurs de régions (retirés par `regions_et_texte`)."""
        self.texte, self.contexte = self.doc.corps, "corps"
        noeuds = Analyseur(self.doc.corps, self.sig).analyser()
        noeuds = self._solutions_prof(noeuds)
        corps = self.sequence(noeuds)
        return self.assembler(corps)

    def _solutions_prof(self, noeuds: List[Noeud]) -> List[Noeud]:
        """Partie « Solutions » de fin (\\newpage \\chapitre{…}{Solutions :} … \\rdexocorrection) hors
        \\ifcorrection : enveloppée dans une conditionnelle, sinon l'élève verrait la page des corrigés."""
        for k, x in enumerate(noeuds):
            if isinstance(x, Cmd) and x.nom == "chapitre" and x.args and \
                    re.search(r"solution|correction|corrig", x.args[-1].brut, re.I):
                debut = k
                j = k - 1
                while j >= 0 and (isinstance(noeuds[j], (Par,)) or (isinstance(noeuds[j], Texte) and not noeuds[j].s.strip())
                                  or isinstance(noeuds[j], Cmd) and noeuds[j].nom in ("newpage", "clearpage", "setcounter")):
                    if isinstance(noeuds[j], Cmd) and noeuds[j].nom in ("newpage", "clearpage"):
                        debut = j
                    j -= 1
                fin = max((m for m, y in enumerate(noeuds) if isinstance(y, Cmd) and y.nom == "rdexocorrection"),
                          default=-1)
                if fin > k:
                    si = Si(noeuds[debut].debut, noeuds[fin].fin, "ifcorrection", list(noeuds[debut:fin + 1]), None)
                    self.rapport.a_reprendre.append("partie « Solutions » réservée à la version professeur "
                                                    "(enveloppée dans #ifcorrection)")
                    return noeuds[:debut] + [si] + noeuds[fin + 1:]
        return noeuds

    def assembler(self, corps: str) -> str:
        import datetime
        lignes = [
            f"// {self.nom}.typ — préconverti depuis {self.doc.maitre.name} par le skill bfcours-typst "
            f"(convertir.py), le {datetime.date.today():%d/%m/%Y}.",
            "// Versions professeur et élève : compiler.py du skill (ou Ctrl+Maj+B avec l'extension VS Code bfcours-typst ; Ctrl+S ouvre l'aperçu).",
            localiser.import_suite(self.cat.version),
            "",
        ]
        cles = []
        for cle in ("niveau", "theme", "type-document", "cycle", "etablissement", "zone-droite", "fleqn", "dys",
                    "marges"):
            if cle in self.modele:
                cles.append(f"{cle}: {_sans_marqueurs(self.modele[cle])}")
        lignes.append(construire_appel("show: modele", ['"cours"'], cles).replace("#show: modele", "#show: modele"))
        lignes.append("")
        if self.utilise_extraits:
            paquets = ["bfcours"] if self.bfcours_latex else sorted(self.paquets_latex)
            # mêmes polices que le document LaTeX : sinon les étiquettes des figures changent de taille
            for police in ("bfcours-fonts-dys", "bfcours-fonts"):
                if re.search(r"\\usepackage(\[[^\]]*\])?\{" + police + r"\}", self.doc.preambule):
                    paquets.append(police)
                    break
            pre = []
            if "tikz" in self.paquets_latex and not self.bfcours_latex:
                pre.append("\\usetikzlibrary{" + ",".join(regles.BIBLIOTHEQUES_TIKZ) + "}")
            pre += self.preambule_latex
            pre += self._definitions_pour_extraits()
            reglage = [f"paquets: ({', '.join(chaine(p) for p in paquets)}{',' if len(paquets) == 1 else ''})"]
            if pre:
                reglage.append("preambule: ```latex\n" + "\n".join(pre) + "\n```")
            # `lire` : l'aperçu Tinymist montre les extraits déjà rendus (rendus-tex/), sans rien lancer.
            reglage.append("lire: p => read(p, encoding: none)")
            lignes.append("// Extraits LaTeX (figures, constructions sans équivalent) : rendus par LaTeX au Ctrl+Maj+B ;")
            lignes.append("// `lire` les montre aussi dans l'aperçu (Ctrl+S) une fois rendus.")
            lignes.append("#setbflatex(\n" + ",\n".join(indenter(r) for r in reglage) + ",\n)")
            lignes.append("")
        if self.utilise_reprendre:
            lignes.append("// À reprendre à la main : ce que le convertisseur n'a pas su traduire (en orange dans le PDF).")
            lignes.append("#let a-reprendre(code) = box(fill: orange.lighten(60%), inset: 2pt, raw(code))")
            lignes.append("")
        if self.reglages_tete:
            lignes += self.reglages_tete
            lignes.append("")
        return "\n".join(lignes) + corps.strip("\n") + "\n"

    def _definitions_pour_extraits(self) -> List[str]:
        """Macros du document citées par les extraits LaTeX (variables \\def, \\newcommand) : reprises dans
        le préambule des extraits, sinon LaTeX ne les connaîtrait pas."""
        sortie, vues = [], set()
        codes = "\n".join(self.rapport.extraits_codes) if hasattr(self.rapport, "extraits_codes") else ""
        a_voir = set(re.findall(r"\\([A-Za-z@]+)", codes))
        while a_voir:
            nom = a_voir.pop()
            if nom in vues or nom not in self.macros or nom.startswith("tikzfig"):
                continue
            vues.add(nom)
            d = self.macros[nom]
            n = d.get("n", 0)
            if n:
                sortie.append(f"\\providecommand{{\\{nom}}}[{n}]{'[' + d['defaut'] + ']' if d.get('defaut') is not None else ''}{{{d['corps']}}}")
            else:
                sortie.append(f"\\def\\{nom}{{{d['corps']}}}")
            a_voir |= set(re.findall(r"\\([A-Za-z@]+)", d["corps"]))
        return sorted(sortie)
