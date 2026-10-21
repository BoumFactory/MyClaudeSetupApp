"""Crée un dossier de capsule (moteur canvas) à partir du gabarit et y copie l'audio.

Usage :
    python nouvelle_capsule.py <dossier_capsule> [<audio>] [--titre "..."] [--formules grandes|compactes]

<audio> est facultatif (voie B : la capsule peut être créée avant la voix ; spec.js vise alors audio.wav).
--formules : préréglage de taille des formules écrit dans spec.js (défaut : clé « formules » de config.json,
sinon « grandes »). Voir references/moteur-canvas.md, § Taille des formules.

Copie assets/moteur-canvas/ (moteur, MathJax, GSAP et polices vendorisés) et le gabarit (index.html = aperçu,
spec.js = contenu à écrire). Le dossier est portable : il s'ouvre hors ligne et se rend sur n'importe quel poste
avec Playwright + ffmpeg. Un spec.js existant n'est jamais écrasé.
Pour une capsule à scenes.js (moteur HTML), utiliser le skill capsule-video-html.
"""
import argparse
import pathlib
import shutil
import sys

from commun import CONF

ICI = pathlib.Path(__file__).resolve().parent
ASSETS = ICI.parent / "assets"
GABARIT = ASSETS / "gabarit-canvas"
MOTEUR = ASSETS / "moteur-canvas"


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("dossier")
    ap.add_argument("audio", nargs="?", default=None, help="facultatif : audio.wav visé par défaut")
    ap.add_argument("--titre", default="Capsule")
    ap.add_argument("--formules", choices=["grandes", "compactes"], default=None,
                    help="taille des formules (défaut : config.json « formules », sinon grandes)")
    a = ap.parse_args()
    formules = a.formules or CONF.get("formules") or "grandes"
    if formules not in ("grandes", "compactes"):
        sys.exit(f"config.json : « formules » vaut {formules!r} ; valeurs possibles : grandes, compactes.")

    d = pathlib.Path(a.dossier)
    d.mkdir(parents=True, exist_ok=True)
    if (d / "scenes.js").exists():
        sys.exit(f"{d} contient scenes.js (moteur HTML) : utiliser le skill capsule-video-html, ou un autre dossier.")
    shutil.copytree(MOTEUR, d / "moteur-canvas", dirs_exist_ok=True)
    spec_neuf = not (d / "spec.js").exists()
    for nom in ("index.html", "spec.js"):
        if not (d / nom).exists():
            shutil.copy2(GABARIT / nom, d / nom)
    if a.audio:
        if not pathlib.Path(a.audio).exists():
            sys.exit(f"Audio introuvable : {a.audio}")
        ext = pathlib.Path(a.audio).suffix.lower()
        cible = d / f"audio{ext}"
        if pathlib.Path(a.audio).resolve() != cible.resolve():
            shutil.copy2(a.audio, cible)
    else:   # voie B : la voix sera générée plus tard dans audio.wav
        ext = ".wav"
        cible = d / "audio.wav"
    html = (d / "index.html").read_text(encoding="utf-8")
    (d / "index.html").write_text(html.replace("<title>Capsule — aperçu</title>", f"<title>{a.titre} — aperçu</title>"),
                                  encoding="utf-8")
    if spec_neuf:
        sp = (d / "spec.js").read_text(encoding="utf-8")
        sp = sp.replace("titre: 'Titre de la capsule',", f"titre: {a.titre!r},", 1)
        sp = sp.replace("audio: 'audio.wav'", f"audio: 'audio{ext}'", 1)
        sp = sp.replace("formules: 'grandes',", f"formules: '{formules}',", 1)
        (d / "spec.js").write_text(sp, encoding="utf-8")
    present = "" if cible.exists() else ", à produire"
    print(f"Capsule prête : {d}  (audio : {cible.name}{present} ; formules : {formules if spec_neuf else 'spec.js existant conservé'})")


if __name__ == "__main__":
    main()
