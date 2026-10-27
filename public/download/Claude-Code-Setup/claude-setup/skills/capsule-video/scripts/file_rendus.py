"""Fournée : file d'attente des rendus, UNE capsule à la fois, dès qu'elle est contrôlée.

Une capsule est prête quand son dossier contient le fichier vide « PRET-RENDU » (posé après le
regard sur la planche) et pas encore la vidéo de sortie ; elle est rendue par rendre_canvas.py. La file scrute le
dossier toutes les 30 s ; elle s'arrête quand toutes les capsules attendues sont rendues, ou
quand le fichier <dossier>/STOP-RENDUS existe. Journal : <dossier>/rendus.log.

Usage (depuis la racine du projet, en arrière-plan) :
    python file_rendus.py <dossier_fournee> [--qualite envoi|540|projection] [--total 23]

--qualite : défaut = qualite_rendu de config.json, sinon envoi (720p).

--total : nombre de capsules attendues (défaut : nombre de sous-dossiers contenant un script.md
au lancement, recalculé à chaque tour).
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys
import time
from datetime import datetime

ICI = pathlib.Path(__file__).resolve().parent
SORTIES = {"540": "capsule-540p.mp4", "envoi": "capsule-envoi.mp4", "projection": "capsule.mp4"}


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("--qualite", default=None, choices=list(SORTIES))
    ap.add_argument("--total", type=int, default=None)
    a = ap.parse_args()
    if a.qualite is None:
        try:
            q = json.loads((ICI.parent / "config.json").read_text(encoding="utf-8-sig")).get("qualite_rendu")
        except (OSError, ValueError):
            q = None
        a.qualite = q if q in SORTIES else "envoi"
    racine = pathlib.Path(a.dossier)
    journal = racine / "rendus.log"
    sortie = SORTIES[a.qualite]

    def noter(texte):
        ligne = f"{datetime.now():%H:%M:%S}  {texte}"
        print(ligne, flush=True)
        with open(journal, "a", encoding="utf-8") as f:
            f.write(ligne + "\n")

    noter(f"File de rendus démarrée ({a.qualite})")
    echecs, perimes = set(), set()
    while not (racine / "STOP-RENDUS").exists():
        toutes = sorted(d for d in racine.iterdir() if d.is_dir() and (d / "script.md").exists())
        attendues = a.total or len(toutes)
        rendues = [d for d in toutes if (d / sortie).exists()]
        if len(rendues) >= attendues:
            noter(f"Terminé : {len(rendues)} capsules rendues")
            return
        pretes = []
        for d in toutes:
            if not (d / "PRET-RENDU").exists() or (d / sortie).exists() or d.name in echecs:
                continue
            voix = d / "data" / "temps-forts.json"
            if voix.exists() and voix.stat().st_mtime > (d / "PRET-RENDU").stat().st_mtime:
                # voix refaite APRÈS le contrôle : les ancres n'ont peut-être pas été raccrochées
                if d.name not in perimes:
                    noter(f"  ignorée : {d.name} (PRET-RENDU antérieur à la dernière voix, à reposer après contrôle)")
                    perimes.add(d.name)
                continue
            perimes.discard(d.name)
            pretes.append(d)
        if not pretes:
            time.sleep(30)
            continue
        d = pretes[0]
        noter(f"Rendu de {d.name}")
        t0 = time.time()
        if not (d / "spec.js").exists():
            echecs.add(d.name)
            noter(f"  ÉCHEC {d.name} : pas de spec.js (une capsule à scenes.js se rend avec le skill capsule-video-html)")
            continue
        r = subprocess.run([sys.executable, str(ICI / "rendre_canvas.py"), str(d), "--qualite", a.qualite],
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=5400)
        lignes = (r.stdout + r.stderr).strip().splitlines()
        if r.returncode == 0 and (d / sortie).exists():
            noter(f"  OK {d.name} : {(d / sortie).stat().st_size / 1e6:.1f} Mo en {time.time() - t0:.0f} s")
        else:
            echecs.add(d.name)  # pas de nouvelle tentative : corriger, puis relancer la file
            noter(f"  ÉCHEC {d.name} (code {r.returncode}) : " + " | ".join(lignes[-6:]))
    noter("Arrêt demandé (STOP-RENDUS)")


if __name__ == "__main__":
    main()
