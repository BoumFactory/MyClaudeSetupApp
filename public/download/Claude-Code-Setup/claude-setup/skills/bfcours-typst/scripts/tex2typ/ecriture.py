"""Écriture du Typst : crochets, appels, indentation, marqueurs de régions. Rien de propre à bfcours ici."""
from __future__ import annotations

import re
from typing import List

OUV, SEP, FER = "\ue000", "\ue001", "\ue002"
INDENT = "  "
LARGEUR = 90  # au-delà, un appel s'écrit sur plusieurs lignes


def sans_marqueurs(t: str) -> str:
    return re.sub(OUV + r"\d+" + SEP + "|" + FER + r"\d+" + SEP, "", t)


def indenter(texte: str, prefixe: str = INDENT) -> str:
    """Indente chaque ligne non vide, sauf l'intérieur des blocs bruts ``` (code, extraits LaTeX)."""
    sortie, dans_brut = [], False
    for ligne in texte.split("\n"):
        nue = sans_marqueurs(ligne)
        if dans_brut:
            sortie.append(ligne)
        else:
            sortie.append(prefixe + ligne if nue.strip() else ligne)
        if nue.count("```") % 2 == 1:
            dans_brut = not dans_brut
    return "\n".join(sortie)


def chaine(t: str) -> str:
    return '"' + t.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'


def crochets(t: str) -> str:
    """Contenu Typst : « [court] » sur la ligne, « [\\n  long\\n] » s'il occupe plusieurs lignes."""
    nu = sans_marqueurs(t)
    if "\n" in nu.strip("\n") or len(nu) > LARGEUR:
        if "\n" not in nu.strip("\n") and "```" not in nu:
            return "[" + t.strip() + "]"
        return "[\n" + indenter(t.strip("\n")) + "\n]"
    if nu.endswith("\\") and not nu.endswith("\\\\"):
        t += " "
    return "[" + t + "]"


def construire_appel(nom: str, positionnels: List[str], nommes: List[str], valeur: bool = False,
                     diese: bool = True) -> str:
    """`#nom(clés)[contenu][contenu]` ; arguments en code dans les parenthèses, contenus en crochets à la suite.

    Les contenus en crochets ne peuvent venir qu'APRÈS les arguments en code : un positionnel en code placé
    après un contenu force l'écriture de tous les arguments dans les parenthèses."""
    tete = ("#" if diese else "") + nom
    if valeur and not positionnels and not nommes:
        return tete
    code: List[str] = []
    contenus: List[str] = []
    for p in positionnels:
        nu = sans_marqueurs(p)
        if nu.startswith("[") and nu.endswith("]"):
            contenus.append(p)
        else:
            if contenus:  # code après contenu : tout passe entre parenthèses
                code += contenus
                contenus = []
            code.append(p)
    args = code + nommes
    longueur = sum(len(sans_marqueurs(a)) for a in args)
    multi = any("\n" in sans_marqueurs(a) for a in args)
    if not args:
        parenth = "()" if not contenus else ""
    elif multi or longueur > LARGEUR:
        parenth = "(\n" + ",\n".join(indenter(a) for a in args) + ",\n)"
    else:
        parenth = "(" + ", ".join(args) + ")"
    return tete + parenth + "".join(contenus)


def fin_groupe(t: str, i: int) -> int:
    """t[i] == '{' : indice qui suit l'accolade fermante correspondante."""
    prof = 0
    while i < len(t):
        c = t[i]
        if c == "\\":
            i += 2
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return i + 1
        i += 1
    return len(t)


def num(x: float) -> str:
    s = f"{x:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("-0", "") else "0"


def cle_id(k: str) -> str:
    """Nom de clé Typst valide (sinon entre guillemets, dans un dictionnaire)."""
    k = k.strip()
    return k if re.fullmatch(r"[A-Za-z_][\w-]*", k) else chaine(k)


def ident(nom: str) -> str:
    """Nom de commande LaTeX → suffixe de méthode Python (`tcbtab*` → `tcbtab_etoile`, `\\'` → `car_39`)."""
    if len(nom) == 1 and not nom.isalnum():
        return "car_" + str(ord(nom))
    if nom == "\\\\":
        return "saut"
    return re.sub(r"\W", "_", nom.replace("*", "_etoile"))


def virgule(t: str) -> str:
    """Formule placée dans un argument d'appel : entre parenthèses si elle contient une virgule."""
    return "(" + t + ")" if "," in t and not re.fullmatch(r"[\w.]+\(.*\)", t) else t


def texte_simple(brut: str) -> str:
    """Texte LaTeX nettoyé de ses commandes de mise en forme (pour une chaîne : étiquettes, niveau…)."""
    t = re.sub(r"\\(?:textbf|textit|emph|mathbf|text|mathrm|textsuperscript|ensuremath)\s*", "", brut)
    t = re.sub(r"[{}$^~]", "", t)
    t = re.sub(r"\\[A-Za-z]+\s*", "", t)
    return re.sub(r"\s+", " ", t).strip()
