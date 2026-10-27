"""Point d'entrée unique du skill capsule-video : une commande courte par étape, lançable par un collègue
sans connaître les scripts (d'après une idée d'un collègue, rd ; réécrit sur la chaîne actuelle).

    python capsule.py nouvelle <capsule> [--audio fichier] [--titre "..."] [--formules grandes|compactes]
    python capsule.py relire   <capsule> [--appliquer]          # rigueur + forme orale des notations
    python capsule.py voix     <capsule> [--voix estelle] [--modifies | --seulement b03,b07] [--piper [siwis]]
    python capsule.py caler    <capsule> [--vocab "mots rares"] # mots horodatés (MFA sur le texte connu)
    python capsule.py planche  <capsule> [--images 2.5,10]      # À LA DEMANDE : PNG dans planches/ ; défaut : milieu de chaque temps fort
    python capsule.py rendu    <capsule> [--qualite 540|envoi|projection] [--finition auto|aucune|x264]
                                         [--debut X --fin Y] [--brouillon] [--fenetre]
    python capsule.py tout     <capsule> [--voix X | --piper] [--planche] [--rendu] [--qualite 540|envoi|projection]

<capsule> : un chemin, ou un nom cherché dans « dossier_capsules » de config.json.
`tout` enchaîne relire → voix → caler, puis s'arrête (écrire spec.js) ; --planche ajoute la planche de contrôle
(à la demande seulement), --rendu rend aussi la vidéo. `voix --controle` force le contrôle de fidélité. Chaque commande appelle le script du dossier scripts/ (options
complètes : python scripts/<script>.py --help). Marche depuis n'importe quel dossier.
Une capsule à scenes.js (ancien moteur HTML) se traite avec le skill capsule-video-html.
"""
import argparse
import json
import os
import pathlib
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent
SCRIPTS = RACINE / "scripts"
sys.path.insert(0, str(SCRIPTS))
from commun import CONF, python_de  # noqa: E402  (config.json facultatif)


def trouver_python():
    """python_rendu (chemin absolu, ou relatif au dossier courant ou à un parent du skill), puis python (ancienne
    clé), puis un .venv voisin, puis l'interpréteur courant."""
    bases = [pathlib.Path.cwd()] + list(RACINE.parents)[:5]
    for cle in ("python_rendu", "python"):
        v = CONF.get(cle)
        if not v:
            continue
        p = pathlib.Path(v)
        for c in ([p] if p.is_absolute() else [b / p for b in bases]):
            if c.exists():
                return str(c)
    for b in [RACINE] + bases:
        for v in (b / ".venv" / "Scripts" / "python.exe", b / "venv" / "Scripts" / "python.exe",
                  b / ".venv" / "bin" / "python", b / "venv" / "bin" / "python"):  # Windows, puis Linux / macOS
            if v.exists():
                return str(v)
    return sys.executable


PY = trouver_python()


def lancer(script, args, arreter=True):
    cmd = [PY, "-X", "utf8", str(SCRIPTS / script)] + [str(a) for a in args]
    print("→ " + " ".join(f'"{c}"' if " " in c else c for c in cmd[3:]), flush=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    code = subprocess.call(cmd, env=env)
    if code and arreter:
        sys.exit(f"Échec de {script} (code {code}).")
    return code


def capsule(nom, creer=False):
    p = pathlib.Path(nom)
    if not p.exists() and not p.is_absolute() and CONF.get("dossier_capsules"):
        q = pathlib.Path(CONF["dossier_capsules"]) / nom
        if q.exists() or creer:
            p = q
    if not creer:
        if not p.exists():
            sys.exit(f"Capsule introuvable : {nom} (ni chemin, ni dossier dans dossier_capsules).")
        if (p / "scenes.js").exists() and not (p / "spec.js").exists():
            sys.exit(f"{p} est une capsule du moteur HTML (scenes.js) : utiliser le skill capsule-video-html.")
    return p.resolve()


def audio_de(d):
    for nom in ("audio.wav", "audio.mp3", "audio.m4a", "audio.flac", "audio.ogg"):
        if (d / nom).exists():
            return d / nom
    sys.exit(f"Pas d'audio dans {d} : lancer d'abord « capsule.py voix » (ou poser l'enregistrement en audio.xxx).")


def instants_planche(d):
    """Milieu de chaque temps fort (data/temps-forts.json) ; à défaut, 5 instants répartis sur l'audio."""
    tf = d / "data" / "temps-forts.json"
    if tf.exists():
        blocs = json.loads(tf.read_text(encoding="utf-8"))
        t = [round((b["debut"] + b["fin"]) / 2, 2) for b in blocs if "debut" in b and "fin" in b]
        if t:
            return t
    tr = d / "data" / "transcript.json"
    duree = json.loads(tr.read_text(encoding="utf-8")).get("duree", 60) if tr.exists() else 60
    return [round(duree * k / 6, 2) for k in range(1, 6)]


# ---------------------------------------------------------------- commandes
def c_nouvelle(a):
    d = capsule(a.capsule, creer=True)
    args = [d] + ([a.audio] if a.audio else []) + ["--titre", a.titre or d.name]
    if a.formules:
        args += ["--formules", a.formules]
    lancer("nouvelle_capsule.py", args)
    if not (d / "script.md").exists() and not a.audio:
        print("Étape suivante : écrire script.md (temps forts ## b01 …), puis « capsule.py tout " + d.name + " ».")


def c_relire(a):
    lancer("relire_script.py", [capsule(a.capsule)] + (["--appliquer"] if a.appliquer else []))


def c_voix(a):
    d = capsule(a.capsule)
    sel = (["--modifies"] if a.modifies else []) + (["--seulement", a.seulement] if a.seulement else [])
    if a.piper:
        lancer("voix.py", [d, "--voix-piper", a.piper] + sel)
        return
    if not python_de("pocket"):
        sys.exit("Pocket TTS n'est pas installé (clé python_pocket de config.json) : relancer "
                 "installation/installer.ps1, ou utiliser la voix de secours : capsule.py voix " + d.name + " --piper")
    lancer("voix_pocket.py", [d] + (["--voix", a.voix] if a.voix else []) + (["--controle"] if getattr(a, "controle", False) else []) + sel)


def c_caler(a):
    d = capsule(a.capsule)
    lancer("transcrire.py", [audio_de(d), d] + (["--vocab", a.vocab] if a.vocab else []))


def c_planche(a):
    d = capsule(a.capsule)
    images = a.images or ",".join(str(t) for t in instants_planche(d))
    lancer("rendre_canvas.py", [d, "--images", images])
    print(f"Planche : {d / 'planches'}")


def c_rendu(a):
    d = capsule(a.capsule)
    args = [d]
    if a.brouillon:
        args += ["--qualite", "540", "--sortie",
                 d / f"essai-{a.debut or 0:g}-{a.fin if a.fin is not None else 'fin'}.mp4"]
    elif a.qualite:
        args += ["--qualite", a.qualite]
    if a.finition:
        args += ["--finition", a.finition]
    if a.debut:
        args += ["--debut", a.debut]
    if a.fin is not None:
        args += ["--fin", a.fin]
    if a.fenetre:
        args += ["--fenetre"]
    lancer("rendre_canvas.py", args)


def c_tout(a):
    d = capsule(a.capsule)
    if lancer("relire_script.py", [d], arreter=False):
        sys.exit("Alertes de relecture : corriger script.md (ou « capsule.py relire --appliquer »), puis relancer.")
    a.modifies, a.seulement = True, ""
    c_voix(a)
    a.vocab = ""
    c_caler(a)
    if a.planche:
        a.images = None
        c_planche(a)
    if a.rendu:
        a.brouillon, a.finition, a.debut, a.fin, a.fenetre = False, None, 0, None, False
        c_rendu(a)
    else:
        print("Voix et calage prêts : écrire spec.js, puis « capsule.py rendu " + d.name + " ».")


def main():
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Capsules vidéo animées : une commande par étape.")
    sp = ap.add_subparsers(dest="commande", required=True)

    p = sp.add_parser("nouvelle", help="crée le dossier (moteur, aperçu, spec.js)")
    p.add_argument("capsule"); p.add_argument("--audio"); p.add_argument("--titre")
    p.add_argument("--formules", choices=["grandes", "compactes"])
    p.set_defaults(f=c_nouvelle)

    p = sp.add_parser("relire", help="relecture de rigueur et forme orale des notations")
    p.add_argument("capsule"); p.add_argument("--appliquer", action="store_true")
    p.set_defaults(f=c_relire)

    def opts_voix(p):
        p.add_argument("--voix", help="voix Pocket par défaut des temps forts sans étiquette")
        p.add_argument("--piper", nargs="?", const="siwis", default=None, help="voix de secours Piper (siwis, tom, upmc)")

    p = sp.add_parser("voix", help="voix de synthèse (Pocket TTS ; contrôle de fidélité Parakeet avec --controle)")
    p.add_argument("capsule"); opts_voix(p)
    p.add_argument("--controle", action="store_true", help="force le contrôle de fidélité (à la demande)")
    p.add_argument("--modifies", action="store_true"); p.add_argument("--seulement", default="")
    p.set_defaults(f=c_voix)

    p = sp.add_parser("caler", help="mots horodatés (MFA, sinon Whisper)")
    p.add_argument("capsule"); p.add_argument("--vocab", default="")
    p.set_defaults(f=c_caler)

    p = sp.add_parser("planche", help="images fixes dans planches/")
    p.add_argument("capsule"); p.add_argument("--images")
    p.set_defaults(f=c_planche)

    p = sp.add_parser("rendu", help="vidéo MP4")
    p.add_argument("capsule"); p.add_argument("--qualite", choices=["540", "envoi", "projection"])
    p.add_argument("--finition", choices=["auto", "aucune", "x264"])
    p.add_argument("--debut", type=float, default=0); p.add_argument("--fin", type=float)
    p.add_argument("--brouillon", action="store_true", help="extrait 540p dans essai-<début>-<fin>.mp4")
    p.add_argument("--fenetre", action="store_true")
    p.set_defaults(f=c_rendu)

    p = sp.add_parser("tout", help="relire → voix → caler (→ planche avec --planche, → rendu avec --rendu)")
    p.add_argument("capsule"); opts_voix(p)
    p.add_argument("--planche", action="store_true", help="ajoute la planche de contrôle (à la demande seulement)")
    p.add_argument("--rendu", action="store_true"); p.add_argument("--qualite", choices=["540", "envoi", "projection"])
    p.set_defaults(f=c_tout)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
