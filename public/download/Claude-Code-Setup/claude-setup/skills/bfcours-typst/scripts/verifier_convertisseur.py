"""Banc de vérification du convertisseur LaTeX bfcours → Typst (convertir.py + tex2typ/).

Procédure « le paquet a changé » (Typst ou LaTeX) :
  1. `python scripts/regenerer.py` : index des fonctions, clés des guides, table de renommage, signatures
     LaTeX et fiches des paquets remis à jour ; ce script lance ensuite le banc ;
  2. le banc (ce script) convertit chaque cas de `banc/cas/`, compile les versions professeur et élève, et
     vérifie les attentes de `banc/attentes.json` ;
  3. un cas en échec : corriger la règle concernée dans `tex2typ/regles.py` (renommages, clés des arguments
     sans nom…) ou, si le défaut est général, le module de `tex2typ/` en cause ; ne jamais affaiblir une
     attente pour faire passer un cas.

Attentes d'un cas (`attentes.json`, clé = nom du .tex sans extension) :
  - `compile` (vrai par défaut) : les deux versions compilent ;
  - `contient` : motifs (expressions régulières) qui doivent apparaître dans le .typ ;
  - `absent` : motifs interdits ; ceux de `_defauts` s'y ajoutent (sauf `"sans_defauts": true`) ;
  - `replis_max` (0 par défaut) : nombre de nœuds que la réparation a le droit de replier ;
  - `fichiers` : fichiers que la conversion doit produire à côté du .typ (images copiées).

Usage (avec PYTHONIOENCODING=utf-8 ; chemin du script relatif au dossier du skill) :
    python scripts/verifier_convertisseur.py                    # tous les cas
    python scripts/verifier_convertisseur.py --cas tcfillcrep-formule
    python scripts/verifier_convertisseur.py --corpus "<dossier>"   # en plus : tous les maîtres .tex du dossier
    python scripts/verifier_convertisseur.py --garder           # garde le dossier temporaire et l'affiche
Code de sortie : 1 si un cas (ou un maître du corpus) échoue, 0 sinon.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

import localiser  # noqa: E402

BANC = ICI / "banc"
CAS = BANC / "cas"
ATTENTES = BANC / "attentes.json"
MAITRE = re.compile(r"^[ \t]*\\documentclass", re.M)
MARQUE = "@@resultat@@"
DELAI = 900  # secondes par document


def message_erreur(erreur) -> str:
    texte = (getattr(erreur, "message", "") or str(erreur)).strip()
    return texte.splitlines()[0][:160] if texte else "?"


def convertir_un(source: Path, dossier: Path, cat, polices) -> dict:
    """Convertit `source` dans `dossier` (réparation comprise), puis compile les deux versions."""
    from convertir import Pilote
    from tex2typ.lecture import lire_document
    from tex2typ.reparation import compiler_versions
    dossier.mkdir(parents=True, exist_ok=True)
    sortie = dossier / (source.stem + ".typ")
    pilote = Pilote(lire_document(source), cat, sortie, polices)
    _, rapport = pilote.reparer()
    erreur = compiler_versions(sortie, polices, dossier)
    return {"sortie": str(sortie), "erreur": message_erreur(erreur) if erreur is not None else None,
            "replis": len(pilote.notes), "notes": pilote.notes, "extraits": len(rapport.extraits),
            "a_reprendre": len(rapport.a_reprendre)}


def travailleur(source: str, dossier: str) -> int:
    """Mode interne : une conversion par processus (la mémoire de Typst est rendue à la fin, et un plantage
    du compilateur ne fait échouer que ce document)."""
    from tex2typ.catalogue import Catalogue
    polices = [str(localiser.polices())] if localiser.polices() else []
    try:
        r = convertir_un(Path(source), Path(dossier), Catalogue(), polices)
    except Exception:
        r = {"plantage": traceback.format_exc().strip()}
    print(MARQUE + json.dumps(r, ensure_ascii=False))
    return 0


def convertir_isole(source: Path, dossier: Path) -> dict:
    """Lance `travailleur` dans un sous-processus ; renvoie son résultat, avec le texte Typst écrit."""
    debut = time.perf_counter()
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    sortie = dossier / (source.stem + ".typ")
    for essai in range(2):  # un processus tué (mémoire du poste saturée…) a droit à une seconde chance
        try:
            p = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--travailleur", str(source),
                                str(dossier)], capture_output=True, text=True, encoding="utf-8", errors="replace",
                               env=env, timeout=DELAI)
        except subprocess.TimeoutExpired:
            r = {"plantage": f"conversion interrompue après {DELAI} s"}
            break
        lignes = [l for l in p.stdout.splitlines() if l.startswith(MARQUE)]
        if lignes:
            r = json.loads(lignes[-1][len(MARQUE):])
            break
        dernier = (p.stderr.strip().splitlines() or ["(aucun message)"])[-2:]
        r = {"plantage": f"processus de conversion arrêté (code {p.returncode}, {essai + 1} essai(s)) : "
                         + " / ".join(dernier)}
    r["duree"] = time.perf_counter() - debut
    r["sortie"] = sortie
    r["texte"] = sortie.read_text(encoding="utf-8") if sortie.exists() else ""
    if "plantage" in r:
        r.update(erreur=r["plantage"].splitlines()[-1][:200], replis=0, notes=[], extraits=0, a_reprendre=0)
    return r


def verifier_cas(nom: str, attente: dict, defauts: dict, r: dict) -> list:
    """Liste des attentes non tenues (vide si le cas passe)."""
    echecs = []
    texte = r["texte"]
    if "plantage" in r:
        return ["plantage du convertisseur :\n      " + r["plantage"].replace("\n", "\n      ")]
    if attente.get("compile", True) and r["erreur"] is not None:
        echecs.append("ne compile pas : " + r["erreur"])
    for motif in attente.get("contient", []):
        if not re.search(motif, texte, re.M):
            echecs.append(f"motif attendu absent : {motif}")
    absents = list(attente.get("absent", []))
    if not attente.get("sans_defauts"):
        absents += defauts.get("absent", [])
    # les motifs interdits portent sur le Typst écrit : ni les extraits ```latex``` ni les commentaires
    hors_brut = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), texte, flags=re.S)
    hors_brut = re.sub(r"^\s*//.*$", "", hors_brut, flags=re.M)
    for motif in absents:
        m = re.search(motif, hors_brut, re.M)
        if m:
            ligne = hors_brut[: m.start()].count("\n") + 1
            echecs.append(f"motif interdit présent (ligne {ligne}) : {motif} → « {m.group(0)[:60]} »")
    plafond = attente.get("replis_max", defauts.get("replis_max", 0))
    if r["replis"] > plafond:
        echecs.append(f"{r['replis']} nœud(s) replié(s) par la réparation (au plus {plafond}) : "
                      + " ; ".join(n[:100] for n in r["notes"][:3]))
    for f in attente.get("fichiers", []):
        if not (r["sortie"].parent / f).exists():
            echecs.append(f"fichier attendu non produit : {f}")
    return echecs


def nettoyer(dossier: Path) -> None:
    """Supprime le dossier temporaire fichier par fichier, puis ses dossiers vides (jamais shutil.rmtree)."""
    for racine, sous, fichiers in os.walk(dossier, topdown=False):
        for f in fichiers:
            try:
                os.remove(os.path.join(racine, f))
            except OSError:
                pass
        for d in sous:
            try:
                os.rmdir(os.path.join(racine, d))
            except OSError:
                pass
    try:
        os.rmdir(dossier)
    except OSError:
        pass


def lancer_banc(tmp: Path, seul: str | None) -> tuple[int, int]:
    data = json.loads(ATTENTES.read_text(encoding="utf-8"))
    defauts = data.get("_defauts", {})
    noms = sorted(k for k in data if not k.startswith("_"))
    sources = {p.stem: p for p in CAS.glob("*.tex")}
    orphelins = sorted(set(sources) - set(noms))
    if seul:
        if seul not in data:
            sys.exit(f"Cas inconnu : {seul}. Cas disponibles : {', '.join(noms)}")
        noms = [seul]
    print(f"Banc du convertisseur : {len(noms)} cas ({CAS})\n")
    print(f"{'cas':32} {'état':6} {'durée':>6}  détail")
    details, reussis = [], 0
    for nom in noms:
        source = sources.get(nom)
        if source is None:
            print(f"{nom:32} {'ÉCHEC':6} {'':>6}  fichier {nom}.tex absent de banc/cas/")
            details.append((nom, [f"fichier {nom}.tex absent de banc/cas/"], None))
            continue
        r = convertir_isole(source, tmp / nom)  # un plantage est un échec du cas, pas du banc
        echecs = verifier_cas(nom, data[nom], defauts, r)
        duree = f"{r['duree']:.1f}s"
        if echecs:
            details.append((nom, echecs, r))
            print(f"{nom:32} {'ÉCHEC':6} {duree:>6}  {len(echecs)} attente(s) non tenue(s)", flush=True)
        else:
            reussis += 1
            print(f"{nom:32} {'OK':6} {duree:>6}  {data[nom].get('description', '')[:70]}", flush=True)
    print(f"\nBilan du banc : {reussis}/{len(noms)} cas réussis.")
    if orphelins and not seul:
        print("Cas sans attentes (ignorés) : " + ", ".join(orphelins))
    for nom, echecs, r in details:
        print(f"\n— {nom}" + (f" ({r['sortie']})" if r else ""))
        for e in echecs:
            print("    · " + e)
    return reussis, len(noms)


def maitres(dossier: Path) -> list:
    sortie = []
    for f in sorted(dossier.rglob("*.tex")):
        if "archives" in f.parts:
            continue
        try:
            debut = f.read_text(encoding="utf-8", errors="replace")[:20000]
        except OSError:
            continue
        if MAITRE.search(debut):
            sortie.append(f)
    return sortie


def lancer_corpus(dossier: Path, tmp: Path) -> tuple[int, int]:
    liste = maitres(dossier)
    print(f"\nCorpus : {len(liste)} maîtres dans {dossier}\n")
    print(f"{'maître':58} {'compile':8} {'replis':>6} {'extraits':>8} {'à reprendre':>11} {'durée':>6}")
    ok, erreurs, replis = 0, [], []
    for k, source in enumerate(liste, 1):
        rel = source.relative_to(dossier).as_posix()
        r = convertir_isole(source, tmp / "corpus" / f"{k:02d}-{source.stem}")
        etat = "PLANTE" if "plantage" in r else "OK" if r["erreur"] is None else "ÉCHEC"
        ok += r["erreur"] is None
        if r["erreur"] is not None:
            erreurs.append((rel, r["erreur"]))
        replis += [(rel, n) for n in r["notes"]]
        print(f"{rel[:58]:58} {etat:8} {r['replis']:>6} {r['extraits']:>8} {r['a_reprendre']:>11} "
              f"{r['duree']:>5.1f}s", flush=True)
    print(f"\nBilan du corpus : {ok}/{len(liste)} maîtres compilent en version professeur et élève.")
    for rel, e in erreurs:
        print(f"    · {rel} : {e}")
    if replis:
        print("Nœuds repliés par la réparation (refusés par Typst, rendus en extrait LaTeX ou en orange) :")
        for rel, n in replis:
            print(f"    · {rel} : {n[:150]}")
    return ok, len(liste)


def main() -> int:
    for flux in (sys.stdout, sys.stderr):
        if hasattr(flux, "reconfigure"):
            flux.reconfigure(encoding="utf-8", errors="replace")
    p = argparse.ArgumentParser(description="Banc de vérification du convertisseur LaTeX bfcours → Typst.")
    p.add_argument("--cas", help="un seul cas (nom du .tex sans extension)")
    p.add_argument("--corpus", help="dossier de documents réels : convertit et compile tous ses maîtres .tex")
    p.add_argument("--garder", action="store_true", help="ne supprime pas le dossier temporaire")
    p.add_argument("--travailleur", nargs=2, metavar=("SOURCE", "DOSSIER"), help=argparse.SUPPRESS)
    a = p.parse_args()
    if a.travailleur:
        return travailleur(*a.travailleur)
    localiser.verifier_ou_quitter(besoin_typst=True)
    tmp = Path(tempfile.mkdtemp(prefix="banc-tex2typ-"))
    try:
        reussis, total = lancer_banc(tmp, a.cas)
        echec = reussis < total
        if a.corpus:
            ok, n = lancer_corpus(Path(a.corpus).resolve(), tmp)
            echec = echec or ok < n
    finally:
        if a.garder:
            print(f"\nDossier conservé : {tmp}")
        else:
            nettoyer(tmp)
    return 1 if echec else 0


if __name__ == "__main__":
    sys.exit(main())
