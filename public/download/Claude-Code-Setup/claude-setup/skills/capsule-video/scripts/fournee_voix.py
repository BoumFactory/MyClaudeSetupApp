"""Fournée : prépare la matière première de plusieurs capsules d'un dossier, une après l'autre.

Pour chaque sous-dossier contenant un script.md (et pas encore data/temps-forts.json) :
voix.py → nouvelle_capsule.py → transcrire.py. Aucun rendu vidéo : léger, compatible avec un
rendu qui tourne à côté.

Usage (depuis la racine du projet) :
    python fournee_voix.py <dossier_fournee> [--prefixes F2,F3] [--voix-piper siwis]
                           [--titre "Fiche {fiche} - Exercice {exo}"]

Le titre peut utiliser {nom} (nom du dossier) et, pour des dossiers nommés « F2-E5-… »,
{fiche} et {exo}.
"""
import argparse
import os
import pathlib
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent


def lancer(args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable] + args, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=1800)
    lignes = (r.stdout + r.stderr).strip().splitlines()
    print("   " + (lignes[-1] if lignes else "(rien)"), flush=True)
    if r.returncode:
        sys.exit(f"Échec ({r.returncode}) : {' '.join(args)}\n" + "\n".join(lignes[-15:]))


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("--prefixes", default="", help="ne traiter que les dossiers commençant par ces préfixes")
    ap.add_argument("--voix-piper", default=None)
    ap.add_argument("--titre", default="{nom}")
    ap.add_argument("--forcer", action="store_true", help="synthétiser même si relire_script.py signale des alertes")
    a = ap.parse_args()
    # Rigueur d'abord (references/rigueur.md) : aucune voix n'est synthétisée sur un script fautif.
    relu = subprocess.run([sys.executable, str(ICI / "relire_script.py"), a.dossier],
                          env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    if relu.returncode and not a.forcer:
        sys.exit("Fournée arrêtée : corriger les alertes de relire_script.py (ou --forcer si ce sont de faux positifs).")
    prefixes = [p for p in a.prefixes.split(",") if p]
    for d in sorted(pathlib.Path(a.dossier).iterdir()):
        if not d.is_dir() or (prefixes and not any(d.name.startswith(p) for p in prefixes)):
            continue
        if not (d / "script.md").exists() or (d / "data/temps-forts.json").exists():
            continue
        morceaux = d.name.split("-")
        champs = {"nom": d.name,
                  "fiche": morceaux[0][1:] if len(morceaux) > 1 else "",
                  "exo": morceaux[1][1:] if len(morceaux) > 1 else ""}
        print(f"=== {d.name}", flush=True)
        voix = [str(ICI / "voix.py"), str(d)] + (["--voix-piper", a.voix_piper] if a.voix_piper else [])
        lancer(voix)
        lancer([str(ICI / "nouvelle_capsule.py"), str(d), str(d / "audio.wav"), "--titre", a.titre.format(**champs)])
        lancer([str(ICI / "transcrire.py"), str(d / "audio.wav"), str(d)])


if __name__ == "__main__":
    main()
