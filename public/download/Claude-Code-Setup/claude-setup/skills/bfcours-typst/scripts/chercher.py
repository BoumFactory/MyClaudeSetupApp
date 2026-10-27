"""Recherche dans l'index des fonctions bfcours-typst (toutes les fonctions publiques des paquets). Sortie compacte.

Usage (avec PYTHONIOENCODING=utf-8 ; chemin du script relatif au dossier du skill) :
    python scripts/chercher.py "conversion d'unités"    # je veux faire X
    python scripts/chercher.py --latex tcbtabc           # équivalent d'une commande LaTeX
    python scripts/chercher.py --paquet rdopp            # fonctions d'un paquet
    python scripts/chercher.py --fiche exo               # tout sur une fonction : clés, exemple
    (les anciens noms marchent encore : « EXO », « MultiColonnes », « Vecteur » trouvent exo, multi-colonnes, vect)
    python scripts/chercher.py --cle position            # quelles fonctions acceptent cette clé
    options : -n 15 (nombre de résultats)

Sources (voir commun.py) : l'index de la suite quand elle est présente, sinon `scripts/donnees/index.json` ;
les clés des guides `scripts/donnees/cles-guides.json` ; la table de renommage (`scripts/donnees/renommage.json`). Tout se régénère par `regenerer.py`.
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import commun  # noqa: E402
import kebab  # noqa: E402
from tex2typ import regles  # noqa: E402

VIDES = {"de", "des", "du", "la", "le", "les", "un", "une", "et", "ou", "a", "au", "aux", "en", "d", "l", "pour",
         "je", "veux", "faire", "avec", "dans", "sur", "par", "qui", "que", "comment", "mon", "ma", "mes", "the"}


def _mots(texte):
    mots = []
    for m in re.findall(r"[\w\\-]+", commun.plier(texte)):
        m = m.lstrip("\\")
        if m in VIDES or len(m) < 2:
            continue
        mots.append(m[:-1] if len(m) > 4 and m.endswith(("s", "x")) else m)
    return mots


def _noms_recherche(r):
    """Nom kebab-case, sa forme sans tirets et les anciens noms (alias : « MultiColonnes » trouve multi-colonnes)."""
    nom = commun.plier(r["nom"])
    anciens = [commun.plier(a) for a in kebab.anciens(r["nom"].rpartition(".")[2])]
    return " ".join([nom, str(nom).replace("-", "")] + anciens)


def _court(texte, n):
    """Texte coupé à n caractères, avec « … » s'il a été coupé."""
    return texte if len(texte) <= n else texte[: n - 1].rstrip() + "…"


def _ligne(r, guides):
    nb = len([p for p in r["parametres"] if not p["variadique"]])
    g = guides.get(r["appel"]) or guides.get(r["nom"])
    if nb == 0 and g:
        nb = len(g["params"])
    latex = f"  [LaTeX : {', '.join(chr(92) + x for x in r['latex'])}]" if r["latex"] else ""
    return f"{r['appel']:<24} {r['paquet']:<19} {_court(r['resume'], 110)}{latex}"


def chercher(data, guides, requete, n):
    mots = _mots(requete)
    if not mots:
        return []
    notes = []
    for r in data["fonctions"]:
        g = guides.get(r["appel"]) or guides.get(r["nom"]) or {}
        champs = [
            (_noms_recherche(r), 8),
            (commun.plier(" ".join(r["latex"])), 6),
            (commun.plier(r["resume"]), 3),
            (commun.plier(r["description"]), 1),
            (commun.plier(" ".join(p["nom"] + " " + (p["description"] or "") for p in r["parametres"])), 1),
            (commun.plier(" ".join(p["nom"] + " " + p["description"] for p in g.get("params", []))), 1),
        ]
        s = 0
        couverts = 0
        for mot in mots:
            trouve = False
            for i, (texte, poids) in enumerate(champs):
                # nom et LaTeX : sous-chaîne (« colonnes » trouve MultiColonnes) ; textes : début de mot
                if (mot in texte) if i < 2 else re.search(r"(?<![\w])" + re.escape(mot), texte):
                    s += poids
                    trouve = True
            couverts += trouve
        if s:
            notes.append((couverts, s, r))
    notes.sort(key=lambda x: (-x[0], -x[1]))
    return [r for _, _, r in notes[:n]]


# Noms LaTeX qui ne sont pas des fonctions en Typst (clés, syntaxe) : réponse directe.
ALIAS_LATEX = {
    "exocorrection": "marqueur `#exocorrection` (sans parenthèses) dans le corps d'`exo`/`exo-eval` : `#exo[Titre][énoncé #exocorrection correction]`",
    "tcblower": "marqueur `#tcblower` (sans parenthèses) dans le corps d'`exo`/`exo-eval`, avant `#exocorrection` : `#exo[Titre][énoncé #tcblower réponse #exocorrection correction]`",
    "overlay": "pas d'équivalent ; pour les étiquettes tournées dans la marge : `setrdexo(display-tags: true | \"correction\")`",
    "tcbitem": "`tcbitem(clés)[contenu]`, passé ENTRE les parenthèses de multi-colonnes/tcbenumerate/tcbraster ; sans clé, un simple bloc `[…]`",
    "Needspace": "`#needspace(13em)` (farfadet-maths)",
    "ifcorrection": "`#ifcorrection[prof][élève]`, `#ifcorrection[prof]`, `context ifcorrection()`",
    "displayitempointstrue": "`#displayitempoints(true)`",
    "displayitempointsfalse": "`#displayitempoints(false)`",
    "newpage": "`#pagebreak()`",
    "input": "`#include \"fichier.typ\"` ou tout réunir dans un seul .typ",
    "tikzinclude": "redessiner la figure en cetz (skill typst, references/cetz.md)",
    "tcbset": "le setter du paquet concerné (`setrdexo`, `setrdcrep`, `setbfenvironments`…) ; `correction style` → clé `correction-style` de `setrdexo`",
}


def par_latex(data, nom):
    nom = nom.lstrip("\\")
    typst = kebab.nom_typst(nom) if kebab.est_ancien(nom) else nom  # nom LaTeX → nom Typst actuel
    if nom in regles.RENOMMAGES:                                    # commande LaTeX renommée (Colonnes, exo, Theo…)
        typst = regles.RENOMMAGES[nom][0]
    trouves = [r for r in data["fonctions"]
               if nom in r["latex"] or r["nom"] in (nom, typst) or nom.lower() in (x.lower() for x in r["latex"])]
    if not trouves:
        trouves = [r for r in data["fonctions"] if r["nom"].lower() in (nom.lower(), typst.lower())]
    segments = [s for s in commun.segments_renommage() if re.search(r"`\\?" + re.escape(nom) + r"`", s[1])]
    return trouves, segments


def fiche(data, guides, nom):
    nom = kebab.nom_typst(nom)   # un ancien nom (EXO, MultiColonnes…) désigne la fonction renommée
    rs = [r for r in data["fonctions"] if r["appel"] == nom or r["nom"] == nom]
    if not rs:
        rs = [r for r in data["fonctions"] if r["appel"].lower() == nom.lower() or r["nom"].lower() == nom.lower()]
    if not rs:
        print(f"Aucune fonction « {nom} ». Essayer : chercher.py \"{nom}\"")
        return
    for r in rs:
        print(f"{r['appel']}  ({r['paquet']}, {r['fichier']})")
        print(f"  {r['signature']}")
        print()
        print("  " + str(r["description"]).replace("\n", "\n  "))
        if r["latex"]:
            print("  LaTeX : " + ", ".join("\\" + x for x in r["latex"]))
        params = [p for p in r["parametres"] if not p["variadique"]]
        if params:
            print("\n  Clés (index) :")
            for p in params:
                d = "positionnel" if p["positionnel"] else f"défaut {p['defaut']}"
                lt = f" [LaTeX : {p['latex']}]" if p.get("latex") else ""
                print(f"    {p['nom']} ({d}) : {p['description'] or ''}{lt}")
        g = guides.get(r["appel"]) or guides.get(r["nom"])
        if g:
            connus = {p["nom"] for p in params}
            sup = [p for p in g["params"] if p["nom"] not in connus]
            if sup:
                print(f"\n  Clés (guide {g['fichier']}) :")
                for p in sup:
                    d = "positionnel" if p["positionnel"] else f"défaut {p['defaut']}"
                    o = f" ; valeurs {', '.join(p['options'])}" if p["options"] else ""
                    print(f"    {p['nom']} ({d}{o}) : {p['description']}")
            for v in g.get("variantes", []):
                print(f"\n  Variante {v['appel']} : {v['resume']}")
        for ex in r["exemples"][:3]:
            print("\n  Exemple :\n    " + str(ex.strip()).replace("\n", "\n    "))
        print()
        if r["appel"] == "modele":  # les clés de modele("cours", …) sont celles de bfcours
            print("Clés de modele(\"cours\", …) = clés de farfadet :\n")
            fiche(data, guides, "farfadet")


def par_cle(data, guides, cle):
    vus = []
    for r in data["fonctions"]:
        noms = {p["nom"] for p in r["parametres"]}
        g = guides.get(r["appel"]) or guides.get(r["nom"]) or {}
        noms |= {p["nom"] for p in g.get("params", [])}
        if cle in noms:
            vus.append(r)
    return vus


def main():
    # Console Windows en cp1252 : sans cela, « → » ou « … » d'un résultat arrêtent le script
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    a = argparse.ArgumentParser(description="Recherche dans l'index bfcours-typst.")
    a.add_argument("requete", nargs="?", help="besoin en mots (« tableau de conversion », « zone de réponse »)")
    a.add_argument("--latex", help="nom d'une commande ou d'un environnement LaTeX bfcours (avec ou sans \\)")
    a.add_argument("--paquet", help="liste les fonctions d'un paquet")
    a.add_argument("--fiche", help="détail d'une fonction : signature, clés, LaTeX, exemples")
    a.add_argument("--cle", help="fonctions qui acceptent cette clé")
    a.add_argument("-n", type=int, default=12)
    args = a.parse_args()
    data = commun.lire_index()
    guides = commun.lire_cles_guides()
    if args.fiche:
        fiche(data, guides, args.fiche)
    elif args.latex:
        trouves, segments = par_latex(data, args.latex)
        alias = ALIAS_LATEX.get(args.latex.lstrip("\\"))
        if alias:
            print(f"\\{args.latex.lstrip(chr(92))} : {alias}")
        for r in trouves:
            print(_ligne(r, guides))
        for paquet, s in segments:
            s = re.sub(r"\s*\((?:soir du |matin du )?\d\d/\d\d/\d{4}\)", "", s)   # dates de journal : bruit
            print(f"renommage{' (' + paquet + ')' if paquet else ''} : {s}")
        if not trouves and not segments and not alias:
            print(f"Rien pour \\{args.latex.lstrip(chr(92))} : chercher par le besoin (chercher.py \"…\"), "
                  "ou c'est une commande LaTeX standard (skill typst, references/latex-vers-typst.md).")
        elif trouves:
            print(f"\nDétail : chercher.py --fiche {trouves[0]['appel']}")
    elif args.paquet:
        rs = [r for r in data["fonctions"] if r["paquet"] == args.paquet]
        if not rs:
            print("Paquets : " + ", ".join(sorted(data["paquets"])))
        for r in rs:
            print(_ligne(r, guides))
    elif args.cle:
        for r in par_cle(data, guides, args.cle):
            print(_ligne(r, guides))
    elif args.requete:
        rs = chercher(data, guides, args.requete, args.n)
        for r in rs:
            print(_ligne(r, guides))
        if rs:
            print(f"\nDétail : chercher.py --fiche {rs[0]['appel']}")
        else:
            print("Aucun résultat : reformuler (mots du métier : « tableau », « réponse », « exercice »…).")
    else:
        a.print_help()


if __name__ == "__main__":
    main()
