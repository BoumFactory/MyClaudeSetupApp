#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble le rapport HTML d'audit d'accessibilité.

Lit dans le dossier d'audit : constats.json (rédigé par l'agent), captures.json
(capturer_zones.py) et mesures.json (preparer_eval.py). Écrit rapport.html, qui
référence les images par chemins relatifs (captures/...) : le dossier d'audit
doit rester entier pour que le rapport s'affiche.

Usage :
  python generer_rapport.py --dossier "<dossier_audit>" [--ouvrir]
Code de sortie 1 si constats.json contient des erreurs bloquantes.
"""
import argparse
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
GABARIT = SKILL_DIR / "assets" / "rapport_template.html"
DIMENSIONS = {"mise_en_forme", "ancrages_linguistiques", "sequencage", "non_verbal", "materiel",
              "repetition", "appartenance", "autonomie", "reussite"}
GRAVITES = {"bloquant", "important", "confort"}
NIVEAUX = {"aucun", "partiel", "avance", "non_applicable"}
MOMENTS = {"avant", "pendant", "apres"}


def valider(d):
    erreurs, alertes = [], []
    ev = d.get("evaluation") or {}
    for k in ("titre", "fichier_source"):
        if not ev.get(k):
            erreurs.append(f"evaluation.{k} manquant")
    if not d.get("objectifs"):
        erreurs.append("objectifs vide : chaque exercice doit avoir son objectif et ses critères de réussite")
    for o in d.get("objectifs", []):
        if not o.get("criteres_reussite"):
            alertes.append(f"{o.get('exercice')} : aucun critère de réussite")
    ids = set()
    for c in d.get("constats", []):
        cid = c.get("id", "?")
        if cid in ids:
            erreurs.append(f"identifiant en double : {cid}")
        ids.add(cid)
        if c.get("dimension") not in DIMENSIONS:
            erreurs.append(f"{cid} : dimension inconnue « {c.get('dimension')} »")
        if c.get("gravite") not in GRAVITES:
            erreurs.append(f"{cid} : gravité inconnue « {c.get('gravite')} » (bloquant, important, confort)")
        for champ in ("titre", "observation", "pourquoi"):
            if not c.get(champ):
                erreurs.append(f"{cid} : champ « {champ} » vide")
        if not c.get("pistes"):
            erreurs.append(f"{cid} : aucune piste")
        else:
            reco = [p for p in c["pistes"] if p.get("recommandee")]
            if len(reco) != 1:
                erreurs.append(f"{cid} : {len(reco)} piste(s) « recommandee » — il en faut exactement une")
            elif not reco[0].get("pourquoi_recommandee"):
                alertes.append(f"{cid} : piste recommandée sans « pourquoi_recommandee »")
        if not isinstance(c.get("a_retenir"), bool):
            erreurs.append(f"{cid} : « a_retenir » doit valoir true ou false (présélection de l'agent)")
        if not c.get("preserve"):
            alertes.append(f"{cid} : « preserve » vide (dire ce que la piste ne touche pas)")
        if not c.get("source"):
            alertes.append(f"{cid} : pas de source Éduscol citée")
        if not c.get("zones"):
            alertes.append(f"{cid} : aucune zone (pas de capture) — normal seulement pour un constat global")
    dims_grille = {g.get("dimension") for g in d.get("grille", [])}
    for g in d.get("grille", []):
        if g.get("niveau") not in NIVEAUX:
            erreurs.append(f"grille {g.get('dimension')} : niveau « {g.get('niveau')} » invalide")
        for r in g.get("constats", []):
            if r not in ids:
                alertes.append(f"grille {g.get('dimension')} : renvoie à {r}, absent des constats")
    manquantes = DIMENSIONS - dims_grille
    if manquantes:
        erreurs.append(f"grille incomplète, dimensions absentes : {sorted(manquantes)}")
    for p in d.get("passation", []):
        if p.get("moment") not in MOMENTS:
            erreurs.append(f"passation {p.get('id')} : moment « {p.get('moment')} » (avant, pendant, apres)")
        if not isinstance(p.get("a_retenir"), bool):
            erreurs.append(f"passation {p.get('id')} : « a_retenir » doit valoir true ou false")
    for p in (d.get("synthese") or {}).get("priorites", []):
        if isinstance(p, dict):
            for r in p.get("constats", []):
                if r not in ids:
                    alertes.append(f"priorité renvoyant à {r}, absent des constats")
    return erreurs, alertes


def noter(d):
    """Note d'accessibilité : indice de grille sur 100 et obstacles restants.

    Indice = moyenne des dimensions applicables (aucun 0, partiel 1, avancé 2), ramenée sur 100.
    Le maximum est atteint avec un indice de 100, zéro bloquant et zéro important ; les
    constats « confort » restants sont signalés sans faire baisser la note.
    """
    valeurs = {"aucun": 0, "partiel": 1, "avance": 2}
    cotes = [valeurs[g["niveau"]] for g in d.get("grille", []) if g.get("niveau") in valeurs]
    indice = round(100 * sum(cotes) / (2 * len(cotes))) if cotes else None
    compte = {g: sum(1 for c in d.get("constats", []) if c.get("gravite") == g)
              for g in ("bloquant", "important", "confort")}
    maximum = indice == 100 and compte["bloquant"] == 0 and compte["important"] == 0
    return {"indice": indice, **compte, "maximum": maximum}


def score_precedent(dossier):
    """Note de l'audit daté précédent du même sujet (dossiers frères), pour l'avant / après."""
    freres = sorted(p for p in dossier.parent.iterdir()
                    if p.is_dir() and p.name < dossier.name and (p / "constats.json").exists())
    if not freres:
        return None
    try:
        prec = json.loads((freres[-1] / "constats.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return {**noter(prec), "dossier": freres[-1].name}


def main():
    ap = argparse.ArgumentParser(description="Générer le rapport HTML d'audit d'accessibilité")
    ap.add_argument("--dossier", required=True, help="Dossier d'audit")
    ap.add_argument("--ouvrir", action="store_true", help="Ouvrir le rapport dans le navigateur")
    args = ap.parse_args()

    dossier = Path(args.dossier).resolve()
    d = json.loads((dossier / "constats.json").read_text(encoding="utf-8"))
    erreurs, alertes = valider(d)
    for a in alertes:
        print("alerte : " + a)
    if erreurs:
        print("ERREURS dans constats.json :")
        for e in erreurs:
            print("  - " + e)
        sys.exit(1)

    for nom, cle in (("captures.json", "captures"), ("mesures.json", "mesures")):
        f = dossier / nom
        d[cle] = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    if not d["captures"]:
        print("alerte : captures.json absent — lancer capturer_zones.py avant")
    d["dossier_audit"] = str(dossier)
    d.setdefault("id", f"{d['evaluation'].get('fichier_source')}|{d['evaluation'].get('date_analyse', '')}")
    if not d["evaluation"].get("fichier_pdf"):
        d["evaluation"]["fichier_pdf"] = d["mesures"].get("fichier_pdf")
    d["note"] = noter(d)
    d["note_precedente"] = score_precedent(dossier)

    charge = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    titre = d["evaluation"]["titre"].replace("<", "&lt;")
    html = GABARIT.read_text(encoding="utf-8").replace("__DATA__", charge).replace("__TITRE__", titre)
    sortie = dossier / "rapport.html"
    sortie.write_text(html, encoding="utf-8")
    print(f"Rapport : {sortie}")
    print(f"{len(d.get('constats', []))} constat(s), {len(d.get('passation', []))} action(s) de passation")
    n = d["note"]
    print(f"NOTE : indice de grille {n['indice']}/100 · {n['bloquant']} bloquant(s), {n['important']} important(s), "
          f"{n['confort']} confort · {'MAXIMUM ATTEINT' if n['maximum'] else 'maximum non atteint'}")
    if d["note_precedente"]:
        p = d["note_precedente"]
        print(f"Audit précédent ({p['dossier']}) : indice {p['indice']}/100 · {p['bloquant']} bloquant(s), "
              f"{p['important']} important(s), {p['confort']} confort")
    if args.ouvrir and os.name == "nt":
        os.startfile(str(sortie))  # navigateur par défaut, sans toucher aux processus existants


if __name__ == "__main__":
    main()
