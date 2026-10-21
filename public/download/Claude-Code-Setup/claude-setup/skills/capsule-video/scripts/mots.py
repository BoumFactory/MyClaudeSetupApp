"""Affiche les mots indexés et horodatés d'une capsule, segment par segment.
C'est la table de référence pour ancrer les gestes ('#147' = mot 147).

Usage : python mots.py <dossier_capsule> [--de 0] [--a 9999]
"""
import argparse
import json
import pathlib
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
ap = argparse.ArgumentParser()
ap.add_argument("dossier")
ap.add_argument("--de", type=float, default=0)
ap.add_argument("--a", type=float, default=1e9)
a = ap.parse_args()
d = json.loads((pathlib.Path(a.dossier) / "data" / "transcript.json").read_text(encoding="utf-8"))
for s in d["segments"]:
    if s["fin"] < a.de or s["debut"] > a.a:
        continue
    print(f"--- [{s['debut']:.2f}–{s['fin']:.2f}]")
    print("  " + " ".join(f"{m['i']}:{m['mot']}@{m['debut']:.2f}" for m in s["mots"]))
