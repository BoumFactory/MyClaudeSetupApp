#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
integrate_feedback.py — Intégration des remarques collègue dans un preplan H5P.

Ce script lit un preplan JSON et un fichier de feedback exporté par le
visualiseur standalone (build_standalone.py), puis ANNOTE les nœuds concernés
en ajoutant une clé "_review_remarks" contenant les commentaires du collègue.

Il n'est PAS un agent IA : il ne réécrit pas le contenu pédagogique. Les
annotations servent de guide pour qu'un agent applique ensuite les corrections.

Usage :
    python integrate_feedback.py \\
        --preplan preplan_fixed.json \\
        --feedback feedback.json \\
        --output preplan_revised.json

Format du feedback accepté (plusieurs variantes détectées automatiquement) :

    Variante A (clés "node_N") :
    {
        "node_5":  {"content": "Le texte est trop long, réduire de 50%",
                    "priority": "medium"},
        "node_12": {"content": "Question ambiguë", "priority": "high"}
    }

    Variante B (clés entières sous forme de string) :
    { "5": {"content": "...", "priority": "..."} }

    Variante C (liste d'objets) :
    [
        {"node": 5,  "content": "...", "priority": "high"},
        {"node": 12, "content": "...", "priority": "medium"}
    ]

La sortie est écrite dans --output (le fichier --preplan n'est JAMAIS modifié).
"""

import argparse
import copy
import json
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def charger_json(chemin: Path) -> dict | list:
    """Charge un fichier JSON en UTF-8."""
    with open(chemin, encoding="utf-8") as f:
        return json.load(f)


def ecrire_json(chemin: Path, donnees: dict | list) -> None:
    """Écrit un objet Python en JSON UTF-8 indenté."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(donnees, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Normalisation du feedback
# ---------------------------------------------------------------------------

def normaliser_feedback(donnees: dict | list) -> list[dict]:
    """
    Normalise le feedback quelle que soit sa variante d'entrée.

    Retourne une liste de dicts uniformes :
    [
        {"index": int, "comment": str, "priority": str},
        ...
    ]
    """
    remarques = []

    if isinstance(donnees, list):
        # Variante C : liste d'objets {"node": N, "content": "...", ...}
        for item in donnees:
            index = item.get("node")
            if index is None:
                print(
                    f"  ATTENTION : entrée de feedback sans clé \"node\" "
                    f"ignorée : {item}",
                    file=sys.stderr,
                )
                continue
            try:
                index = int(index)
            except (TypeError, ValueError):
                print(
                    f"  ATTENTION : index de nœud invalide \"{index}\" "
                    f"ignoré.",
                    file=sys.stderr,
                )
                continue
            remarques.append({
                "index": index,
                "comment": str(item.get("content", item.get("comment", ""))),
                "priority": str(item.get("priority", "medium")),
            })

    elif isinstance(donnees, dict):
        for cle, valeur in donnees.items():
            # Variante A : "node_N"  Variante B : "N"
            cle_nettoyee = cle.strip()
            if cle_nettoyee.startswith("node_"):
                cle_nettoyee = cle_nettoyee[len("node_"):]
            try:
                index = int(cle_nettoyee)
            except ValueError:
                print(
                    f"  ATTENTION : clé de feedback \"{cle}\" non reconnue "
                    f"(ne correspond pas à un index de nœud). Ignorée.",
                    file=sys.stderr,
                )
                continue

            if isinstance(valeur, dict):
                commentaire = str(
                    valeur.get("content", valeur.get("comment", ""))
                )
                priorite = str(valeur.get("priority", "medium"))
            else:
                # Valeur simple (chaîne de commentaire)
                commentaire = str(valeur)
                priorite = "medium"

            remarques.append({
                "index": index,
                "comment": commentaire,
                "priority": priorite,
            })
    else:
        print(
            "ERREUR : format du fichier feedback non reconnu "
            f"(type : {type(donnees).__name__}).",
            file=sys.stderr,
        )

    return remarques


# ---------------------------------------------------------------------------
# Intégration des remarques dans le preplan
# ---------------------------------------------------------------------------

def integrer_remarques(preplan: dict, remarques: list[dict]) -> tuple[dict, list]:
    """
    Ajoute les annotations "_review_remarks" dans les nœuds du preplan.

    Retourne :
      - preplan annoté (copie profonde)
      - liste des remarques effectivement intégrées
    """
    preplan_annote = copy.deepcopy(preplan)
    noeuds = preplan_annote.get("nodes", [])
    nb_noeuds = len(noeuds)

    integrees = []

    for remarque in remarques:
        idx = remarque["index"]
        if idx < 0 or idx >= nb_noeuds:
            print(
                f"  ATTENTION : index {idx} hors bornes "
                f"(le preplan contient {nb_noeuds} nœuds, index 0 à "
                f"{nb_noeuds - 1}). Remarque ignorée.",
                file=sys.stderr,
            )
            continue

        noeud = noeuds[idx]
        if "_review_remarks" not in noeud:
            noeud["_review_remarks"] = []

        noeud["_review_remarks"].append({
            "comment": remarque["comment"],
            "priority": remarque["priority"],
        })
        integrees.append({
            "index": idx,
            "title": noeud.get("title", f"Nœud {idx}"),
            "comment": remarque["comment"],
            "priority": remarque["priority"],
        })

    return preplan_annote, integrees


# ---------------------------------------------------------------------------
# Affichage du résumé
# ---------------------------------------------------------------------------

ORDRE_PRIORITE = {"high": 0, "medium": 1, "low": 2}


def afficher_resume(remarques_integrees: list[dict], nb_total: int) -> None:
    """Affiche un résumé lisible trié par priorité décroissante."""
    print("\n" + "=" * 60)
    print("Résumé de l'intégration des remarques")
    print("=" * 60)
    print(f"  Remarques fournies : {nb_total}")
    print(f"  Remarques intégrées : {len(remarques_integrees)}")

    if not remarques_integrees:
        print("  (aucune remarque intégrée)")
        return

    # Nœuds concernés
    indices_concernes = sorted({r["index"] for r in remarques_integrees})
    print(f"  Nœuds concernés    : {indices_concernes}")

    # Classement par priorité
    triees = sorted(
        remarques_integrees,
        key=lambda r: ORDRE_PRIORITE.get(r["priority"].lower(), 99),
    )

    print("\n  Détail par priorité (high en premier) :")
    print("  " + "-" * 56)
    for r in triees:
        priorite_aff = r["priority"].upper().ljust(6)
        titre_aff = r["title"][:30].ljust(30)
        commentaire_court = r["comment"][:60]
        if len(r["comment"]) > 60:
            commentaire_court += "…"
        print(
            f"  [{priorite_aff}] Nœud {r['index']:3d} — {titre_aff} | "
            f"{commentaire_court}"
        )


# ---------------------------------------------------------------------------
# Fonction main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Intègre les remarques d'un collègue (fichier feedback.json) dans "
            "un preplan H5P Branching Scenario en annotant les nœuds ciblés "
            "avec une clé \"_review_remarks\"."
        )
    )
    parser.add_argument(
        "--preplan",
        type=Path,
        required=True,
        help="Preplan JSON source (non modifié, lecture seule).",
    )
    parser.add_argument(
        "--feedback",
        type=Path,
        required=True,
        help="Fichier JSON de feedback exporté par le visualiseur.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Chemin du preplan annoté à produire (≠ du fichier --preplan).",
    )
    args = parser.parse_args()

    # Vérifications d'existence
    for chemin, label in [(args.preplan, "--preplan"), (args.feedback, "--feedback")]:
        if not chemin.exists():
            print(
                f"ERREUR : fichier {label} introuvable : {chemin}",
                file=sys.stderr,
            )
            return 1

    # Chargement
    print("=" * 60)
    print("Intégration des remarques collègue dans le preplan H5P")
    print("=" * 60)
    print(f"  Preplan source : {args.preplan}")
    print(f"  Feedback       : {args.feedback}")
    print(f"  Sortie         : {args.output}")

    preplan = charger_json(args.preplan)
    if not isinstance(preplan, dict):
        print(
            "ERREUR : le fichier --preplan doit être un objet JSON (dict).",
            file=sys.stderr,
        )
        return 1

    feedback_brut = charger_json(args.feedback)

    # Normalisation du feedback
    remarques = normaliser_feedback(feedback_brut)
    if not remarques:
        print(
            "ATTENTION : aucune remarque valide trouvée dans le fichier "
            "feedback. Le preplan est copié sans modification.",
            file=sys.stderr,
        )

    # Intégration
    preplan_annote, integrees = integrer_remarques(preplan, remarques)

    # Écriture
    ecrire_json(args.output, preplan_annote)
    print(f"\n  Preplan annoté écrit : {args.output}")

    # Résumé
    afficher_resume(integrees, nb_total=len(remarques))

    return 0


if __name__ == "__main__":
    sys.exit(main())
