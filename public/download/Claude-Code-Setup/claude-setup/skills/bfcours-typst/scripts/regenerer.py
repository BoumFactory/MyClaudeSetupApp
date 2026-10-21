"""Met le skill bfcours-typst à jour, en une commande, quand un paquet (Typst ou LaTeX) a changé.

Étapes (chacune est sautée proprement si sa source manque sur le poste) :

a. relance le générateur d'index de la suite, s'il est présent : réécrit `tools/index/index.json`
   (signatures, docstrings, équivalents LaTeX, exemples) ;
b. copie cet index dans `scripts/donnees/index.json` : l'instantané livré avec le skill, lu chez un
   collègue qui n'a que les paquets installés ;
c. relit les fiches `#fonction(…)` des guides (`docs/*.typ`) → `scripts/donnees/cles-guides.json` ;
d. relit la table de renommage de la suite, si elle est présente → `scripts/donnees/renommage.json` ;
e. relit les `.sty` de bfcours, rdexo, rdcrep, rdmcq (dossiers trouvés par `kpsewhich`) →
   `scripts/donnees/signatures-latex.json` (arguments des commandes LaTeX, pour le convertisseur) ;
f. régénère `references/paquets/<paquet>.md` (une fiche par paquet) et `references/paquets/INDEX.md` ;
g. lance le banc du convertisseur (`verifier_convertisseur.py`) et affiche son bilan.

Les fiches et les fichiers de `donnees/` sont GÉNÉRÉS : ne jamais les éditer à la main (une correction se fait
dans la docstring ou le guide du paquet, puis on relance ce script).

Usage (avec PYTHONIOENCODING=utf-8 ; chemin du script relatif au dossier du skill) :
    python scripts/regenerer.py
    python scripts/regenerer.py --sans-sigs     # index de la suite déjà à jour
    python scripts/regenerer.py --sans-latex    # ne relit pas les .sty
    python scripts/regenerer.py --sans-banc     # ne lance pas le banc du convertisseur
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import commun  # noqa: E402
import localiser  # noqa: E402
from tex2typ import signatures  # noqa: E402

IMPORT_SEPARE = set()  # paquets que le méta-paquet ne réexporte pas
STY_LATEX = ("bfcours.sty", "rdexo.sty", "rdcrep.sty", "rdmcq.sty")


def relancer_sigs():
    """(a) Régénère l'index de la suite ; sauté si la suite (ou sigs.py) est absente."""
    sigs = localiser.outil("sigs.py")
    if not sigs:
        print("(a) sigs.py introuvable (suite source absente) : index de la suite non régénéré.")
        return
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, str(sigs)], cwd=str(sigs.parent), env=env, capture_output=True,
                       text=True, encoding="utf-8", timeout=600)
    if r.returncode != 0:
        print(r.stdout.strip())
        print(r.stderr.strip())
        raise SystemExit("sigs.py a échoué : index non régénéré.")
    derniere = [l for l in r.stdout.strip().splitlines() if l.strip()]
    print(f"(a) index de la suite régénéré par {sigs.name}" + (f" — {derniere[-1].strip()}" if derniere else ""))


def maj_kebab():
    """(a bis) Copie de la table des noms kebab-case de la suite, si elle est présente."""
    import kebab
    try:
        kebab.maj()
    except SystemExit:
        print("(a bis) table-finale.json introuvable (suite absente) : donnees/kebab.json gardé tel quel.")


def copier_index():
    """(b) Instantané de l'index dans le skill."""
    source = localiser.outil("index/index.json")
    if not source:
        print("(b) pas d'index dans la suite : l'instantané scripts/donnees/index.json est gardé tel quel.")
        return
    commun.DONNEES.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, commun.INDEX_LIVRE)
    data = json.loads(commun.INDEX_LIVRE.read_text(encoding="utf-8"))
    print(f"(b) index copié dans {commun.INDEX_LIVRE.name} : {len(data['fonctions'])} fonctions, "
          f"{len(data['paquets'])} paquets (généré le {data.get('genere', '?')}).")


def ecrire_guides():
    """(c) Clés des guides ; un résultat vide ne remplace pas un fichier existant."""
    guides = commun.extraire_guides()
    if not guides:
        print("(c) aucun guide docs/*.typ trouvé : cles-guides.json gardé tel quel.")
        return commun.lire_cles_guides()
    commun.CLES_GUIDES.write_text(json.dumps(guides, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"(c) clés des guides : {len(guides)} fonctions → {commun.CLES_GUIDES.name}.")
    return guides


def ecrire_renommage():
    """(d) Instantané de la table de renommage."""
    chemin = commun.fichier_renommage()
    if not chemin:
        print("(d) table de renommage introuvable : renommage.json gardé tel quel.")
        return
    segments = commun.extraire_renommage()
    data = {"source": "table de renommage de la suite", "genere": date.today().isoformat(),
            "segments": [{"paquet": p, "texte": t} for p, t in segments]}
    commun.RENOMMAGE_LIVRE.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"(d) table de renommage : {len(segments)} segments → {commun.RENOMMAGE_LIVRE.name}.")


def ecrire_signatures_latex():
    """(e) Signatures des commandes LaTeX, lues dans les dossiers des .sty installés."""
    kpse = shutil.which("kpsewhich")
    if not kpse:
        print("(e) kpsewhich introuvable (LaTeX absent) : signatures-latex.json gardé tel quel.")
        return
    dossiers = []
    for sty in STY_LATEX:
        try:
            r = subprocess.run([kpse, sty], capture_output=True, text=True, encoding="utf-8", timeout=60)
        except (OSError, subprocess.TimeoutExpired):
            continue
        chemin = r.stdout.strip()
        if r.returncode == 0 and chemin and Path(chemin).is_file():
            d = Path(chemin).parent
            if d not in dossiers:
                dossiers.append(d)
    if not dossiers:
        print("(e) aucun des paquets " + ", ".join(STY_LATEX) + " trouvé par kpsewhich : signatures gardées.")
        return
    r = signatures.extraire(dossiers)
    signatures.DONNEES.mkdir(parents=True, exist_ok=True)
    signatures.FICHIER.write_text(json.dumps(r, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"(e) signatures LaTeX : {len(r['commandes'])} commandes, {len(r['environnements'])} environnements "
          f"(dossiers : {', '.join(d.name for d in dossiers)}) → {signatures.FICHIER.name}.")


def lancer_banc():
    """(g) Banc du convertisseur ; renvoie son code de sortie."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    sys.stdout.flush()  # sinon, sortie redirigée, le bilan du banc s'afficherait avant les étapes a à f
    try:
        r = subprocess.run([sys.executable, str(ICI / "verifier_convertisseur.py")], env=env, timeout=1800)
    except subprocess.TimeoutExpired:
        print("(g) banc interrompu (plus de 30 minutes).")
        return 1
    return r.returncode


def _cellule(t):
    return (t or "").replace("|", "\\|").replace("\n", " ").strip()


def _tronquer(t, n=220):
    t = _cellule(t)
    return t if len(t) <= n else t[: n - 1] + "…"


def fiche(paquet, fonctions, guides, infos, version):
    """Texte Markdown de la fiche d'un paquet."""
    setters = [f["appel"] for f in fonctions if f["appel"].split(".")[-1].startswith("set")]
    l = [f"# {paquet}", "",
         f"Fiche générée par `scripts/regenerer.py` le {date.today().strftime('%d/%m/%Y')} depuis l'index "
         f"des fonctions et les guides des paquets. **Ne pas éditer à la main.**", ""]
    if paquet in IMPORT_SEPARE:
        l.append(f"- Import (NON réexporté par le méta-paquet) : `{localiser.import_suite(version)}` puis, APRÈS lui, "
                 f"`#import \"@local/{paquet}:{version}\": *`.")
    elif localiser.PUBLIE:
        l.append(f"- Import : `{localiser.import_suite(version)}` (toute la suite) ou, pour cette partie seule, "
                 f"{localiser.import_partie_md(paquet, version)}.")
    else:
        l.append(f"- Import : `{localiser.import_suite(version)}` (méta-paquet) ou {localiser.import_partie_md(paquet, version)}.")
    if setters:
        l.append(f"- Réglage : {', '.join('`' + s + '`' for s in setters)} (signature commune `set…(pour:, definir:, reinitialiser:, ..clés)`).")
    l.append(f"- Guide complet : `docs/{paquet}.pdf` du dépôt (sources : `docs/guide.typ` du paquet `{paquet}`).")
    l += ["", "## Sommaire", ""]
    for f in fonctions:
        l.append(f"- `{f['appel']}` — {_tronquer(f['resume'], 140)}")
    # Clés partagées (même nom, même rôle) par au moins trois fonctions : décrites une fois, en tête.
    compte = {}
    for f in fonctions:
        for p in f["parametres"]:
            if not p["variadique"] and not p["positionnel"]:
                compte.setdefault((p["nom"], p["description"]), []).append(f["appel"])
    communes = {k: v for k, v in compte.items() if len(v) >= 3}
    if communes:
        l += ["", "## Clés communes", "",
              "Clés de même nom et de même rôle acceptées par plusieurs fonctions du paquet (défaut : `auto` = "
              "réglage du setter, sinon défaut du paquet).", "",
              "| Clé | Rôle | Option LaTeX | Fonctions |", "|---|---|---|---|"]
        latex_cle = {}
        for f in fonctions:
            for p in f["parametres"]:
                if p.get("latex"):
                    latex_cle.setdefault(p["nom"], p["latex"])
        for (nom, desc), qui in communes.items():
            l.append(f"| `{nom}` | {_tronquer(desc)} | {_cellule(latex_cle.get(nom, ''))} | "
                     f"{len(qui)} : {', '.join('`' + q + '`' for q in qui[:8])}{' …' if len(qui) > 8 else ''} |")
    for f in fonctions:
        l += ["", f"## {f['appel']}", ""]
        l.append(f"```typ\n{f['signature']}\n```")
        if f["description"]:
            l += ["", f["description"].strip()]
        if f["latex"]:
            l += ["", "LaTeX : " + ", ".join(f"`\\{x}`" for x in f["latex"])]
        tous = [p for p in f["parametres"] if not p["variadique"]]
        params = [p for p in tous if (p["nom"], p["description"]) not in communes]
        partagees = [p["nom"] for p in tous if (p["nom"], p["description"]) in communes]
        if partagees:
            l += ["", "Clés communes acceptées (voir en tête) : " + ", ".join(f"`{n}`" for n in partagees) + "."]
        if params:
            l += ["", "| Clé | Défaut | Type | Rôle | Option LaTeX |", "|---|---|---|---|---|"]
            for p in params:
                defaut = "(positionnel)" if p["positionnel"] else f"`{p['defaut']}`"
                l.append(f"| `{p['nom']}` | {defaut} | {_cellule(p['type'])} | {_tronquer(p['description'])} "
                         f"| {_cellule(p.get('latex', ''))} |")
        g = guides.get(f["appel"]) or guides.get(f["nom"])
        noms_index = {p["nom"] for p in tous}
        if g:
            sup = [p for p in g["params"] if p["nom"] not in noms_index]
            if sup:
                l += ["", f"Clés documentées dans le guide (`{g['fichier']}`) :", "",
                      "| Clé | Défaut | Type | Valeurs | Rôle |", "|---|---|---|---|---|"]
                for p in sup:
                    defaut = "(positionnel)" if p["positionnel"] else (f"`{p['defaut']}`" if p["defaut"] else "")
                    l.append(f"| `{p['nom']}` | {defaut} | {_cellule(p['type'])} | "
                             f"{', '.join('`' + o + '`' for o in p['options'])} | {_tronquer(p['description'])} |")
            for v in g.get("variantes", []):
                l += ["", f"Variante `{v['appel']}` : {_tronquer(v['resume'], 300)}"]
                for p in v["params"]:
                    l.append(f"- `{p['nom']}`" + (f" (défaut `{p['defaut']}`)" if p["defaut"] else "")
                             + (f", valeurs {', '.join('`' + o + '`' for o in p['options'])}" if p["options"] else "")
                             + f" : {_tronquer(p['description'], 160)}")
        for i, ex in enumerate(f["exemples"][:2]):
            l += ["", "Exemple :" if i == 0 else "Autre exemple :", "", f"```typ\n{ex.strip()}\n```"]
    return "\n".join(l) + "\n"


def ecrire_fiches(data, guides):
    """(f) Une fiche Markdown par paquet, et leur index."""
    version = localiser.version_suite() or localiser.VERSION_PAR_DEFAUT
    commun.FICHES.mkdir(parents=True, exist_ok=True)
    par_paquet = {}
    for f in data["fonctions"]:
        par_paquet.setdefault(f["paquet"], []).append(f)
    lignes = ["# Fiches des paquets", "",
              f"Générées par `scripts/regenerer.py` le {date.today().strftime('%d/%m/%Y')} (index du "
              f"{data.get('genere', '?')}). Ne pas éditer à la main.", "",
              "| Paquet | Fonctions | Fiche |", "|---|---|---|"]
    for paquet in sorted(par_paquet):
        if paquet == "farfadet-docs":
            continue  # outil de rédaction de guides, hors documents de cours
        texte = fiche(paquet, par_paquet[paquet], guides, data["paquets"].get(paquet, {}), version)
        (commun.FICHES / f"{paquet}.md").write_text(texte, encoding="utf-8")
        lignes.append(f"| `{paquet}` | {len(par_paquet[paquet])} | [{paquet}.md]({paquet}.md) |")
    (commun.FICHES / "INDEX.md").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"(f) fiches : {len(par_paquet) - ('farfadet-docs' in par_paquet)} paquets → references/paquets/.")


def main():
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    a = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    a.add_argument("--sans-sigs", action="store_true", help="ne relance pas le générateur d'index")
    a.add_argument("--sans-latex", action="store_true", help="ne relit pas les .sty LaTeX")
    a.add_argument("--sans-banc", action="store_true", help="ne lance pas le banc du convertisseur")
    args = a.parse_args()
    if not args.sans_sigs:
        relancer_sigs()
    commun.DONNEES.mkdir(parents=True, exist_ok=True)
    maj_kebab()
    copier_index()
    data = commun.lire_index()
    guides = ecrire_guides()
    ecrire_renommage()
    if args.sans_latex:
        print("(e) relecture des .sty sautée (--sans-latex).")
    else:
        ecrire_signatures_latex()
    ecrire_fiches(data, guides)
    if args.sans_banc:
        print("(g) banc sauté (--sans-banc).")
        return 0
    print("(g) banc du convertisseur :\n")
    code = lancer_banc()
    if code:
        print("\nLe banc signale des échecs : corriger tex2typ/regles.py (ou le convertisseur), puis relancer "
              "verifier_convertisseur.py.")
    return code


if __name__ == "__main__":
    sys.exit(main())
