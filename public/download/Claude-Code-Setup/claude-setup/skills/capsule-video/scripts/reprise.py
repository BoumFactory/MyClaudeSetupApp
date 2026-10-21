"""Reprise de capsules dont le script a changé (après un retour du professeur).

Pour chaque capsule : sauvegarde dans version-N/ (spec.js, index.html, script.md,
temps-forts.json, vidéos), retrait des vidéos et de PRET-RENDU, relecture de rigueur
(relire_script.py), puis voix.py --modifies et transcrire.py. Il reste ensuite à faire
raccrocher les ancres par l'animateur, contrôler, et reposer PRET-RENDU.

Usage (depuis la racine du projet) :
    python reprise.py <capsule> [<capsule> ...] [--forcer]
"""
import os
import pathlib
import shutil
import subprocess
import sys

ICI = pathlib.Path(__file__).resolve().parent
VIDEOS = ("capsule-540p.mp4", "capsule-envoi.mp4", "capsule.mp4")


def lancer(args):
    r = subprocess.run([sys.executable] + args, env=dict(os.environ, PYTHONIOENCODING="utf-8"),
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    lignes = (r.stdout + r.stderr).strip().splitlines()
    print("   " + (lignes[-1] if lignes else "(rien)"), flush=True)
    return r.returncode, lignes


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    forcer = "--forcer" in sys.argv
    for arg in [a for a in sys.argv[1:] if a != "--forcer"]:
        d = pathlib.Path(arg)
        code, lignes = lancer([str(ICI / "relire_script.py"), str(d)])
        if code and not forcer:
            print("\n".join(lignes))
            sys.exit(f"{d.name} : alertes de rigueur à corriger avant la reprise (ou --forcer).")
        n = 1
        while (d / f"version-{n}").exists():
            n += 1
        sauvegarde = d / f"version-{n}"
        sauvegarde.mkdir()
        for nom in ("spec.js", "index.html", "script.md", "data/temps-forts.json") + VIDEOS:
            if (d / nom).exists():
                shutil.copy2(d / nom, sauvegarde / pathlib.Path(nom).name)
        for nom in VIDEOS + ("PRET-RENDU",):
            (d / nom).unlink(missing_ok=True)
        print(f"=== {d.name} (ancienne version dans {sauvegarde.name}/)", flush=True)
        for etape in ([str(ICI / "voix.py"), str(d), "--modifies"],
                      [str(ICI / "transcrire.py"), str(d / "audio.wav"), str(d)]):
            code, lignes = lancer(etape)
            if code:
                sys.exit("Échec : " + " ".join(etape) + "\n" + "\n".join(lignes[-10:]))


if __name__ == "__main__":
    main()
