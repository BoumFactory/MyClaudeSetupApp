"""Aide des installeurs (installer.ps1 et installer.sh) : écrit config.json et essaie chaque brique. Bibliothèque standard seule.

Usage :
    python aide_installation.py copier  --source <skill> --cible <skill de destination>      (installer.sh)
    python aide_installation.py ffmpeg  --archive <fichier.tar.xz> --dest <dossier bin>      (installer.sh)
    python aide_installation.py config  --skill <skill> --valeurs <fichier.json>
    python aide_installation.py essai   --skill <skill> --travail <dossier> [--bilan <fichier.json>]
    python aide_installation.py poids   <dossier> [...]

config : fusionne les valeurs dans <skill>/config.json SANS toucher aux clés personnelles déjà présentes
         (voix_clonees, voix_pocket_defaut, premier_usage_fait, mfa écrite par installer_mfa.py…).
essai  : capsule d'une phrase dans <travail> : voix Pocket (+ contrôle Parakeet), horodatage MFA, une image
         rendue ; Whisper sur la même phrase s'il est installé. Bilan lisible + JSON (OK / problème + solution).
"""
import argparse
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PERSONNELLES = {"voix_clonees", "voix_pocket_defaut", "premier_usage_fait", "qualite_rendu", "modele_pocket"}


def cmd_config(a):
    chemin = pathlib.Path(a.skill) / "config.json"
    conf = json.loads(chemin.read_text(encoding="utf-8")) if chemin.exists() else {}
    neuves = json.loads(pathlib.Path(a.valeurs).read_text(encoding="utf-8-sig"))
    for k, v in neuves.items():
        if k in PERSONNELLES and k in conf:
            continue
        conf[k] = v
    chemin.write_text(json.dumps(conf, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"config.json écrit : {chemin}")


def poids(p):
    p = pathlib.Path(p)
    if p.is_file():
        return p.stat().st_size
    total = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try:
                total += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return total


def cmd_copier(a):
    """Copie le skill dans le dossier de base (installer.sh) : sans config.json ni preferences.md (propres à chaque
    utilisateur), sans __pycache__ ni *.bak.js ; ce qui existe déjà à destination est mis à jour."""
    ignore = shutil.ignore_patterns("config.json", "preferences.md", "*.bak.js", "__pycache__")
    shutil.copytree(a.source, a.cible, ignore=ignore, dirs_exist_ok=True)
    print(f"skill copié : {a.cible}")


def cmd_ffmpeg(a):
    """Extrait ffmpeg et ffprobe d'une archive tar (.tar.xz de builds statiques Linux) dans <dest>."""
    import tarfile
    dest = pathlib.Path(a.dest)
    dest.mkdir(parents=True, exist_ok=True)
    trouves = set()
    with tarfile.open(a.archive) as t:
        for m in t.getmembers():
            nom = pathlib.PurePosixPath(m.name).name
            if m.isfile() and nom in ("ffmpeg", "ffprobe"):
                f = t.extractfile(m)
                (dest / nom).write_bytes(f.read())
                (dest / nom).chmod(0o755)
                trouves.add(nom)
    if trouves != {"ffmpeg", "ffprobe"}:
        sys.exit(f"ffmpeg ou ffprobe absent de l'archive (trouvé : {sorted(trouves)})")
    print(f"ffmpeg et ffprobe extraits dans {dest}")


def cmd_precharger(a):
    """Télécharge les poids dans HF_HOME (à lancer avec le Python du moteur concerné)."""
    t = time.time()
    if a.quoi == "pocket":
        from pocket_tts import TTSModel
        m = TTSModel.load_model(language="french_24l")
        m.get_state_for_audio_prompt("estelle")
    elif a.quoi == "parakeet":
        import onnx_asr
        onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3", quantization="int8")
        onnx_asr.load_vad("silero")
    elif a.quoi == "whisper":
        from faster_whisper.utils import download_model
        download_model(a.modele or "medium")
    print(f"{a.quoi} prêt en {time.time() - t:.0f} s")


def cmd_poids(a):
    for d in a.dossiers:
        print(f"{poids(d) / 1e9:.2f}")


SCRIPT = """# Capsule d'essai de l'installeur

## b01 [pause 0.3]
Bonjour ! Cette petite capsule vérifie que la voix, le contrôle et le rendu fonctionnent.
"""

SPEC = """CAPSULE({
  titre: "Essai de l'installation",
  audio: 'audio.wav', theme: 'nuit', mention: 'Voix de synthèse',
  scenes: [
    { id: 's-titre', gabarit: 'titre', debut: 0,
      haut: [ { titre: 'Installation [réussie]{.grad}', id: 't-titre', ecrit: '@b01+0.2' } ],
      centre: [ { carte: 'Voix, contrôle, horodatage et rendu : $x^2 + 1 = 2$', couleur: 'vert', id: 't-obj',
                  taille: 44, montre: '@b01~"rendu"' } ] },
  ],
  gestes(C) {},
});
"""


class Bilan:
    def __init__(self):
        self.lignes = []

    def note(self, brique, ok, detail, solution=""):
        self.lignes.append({"brique": brique, "ok": ok, "detail": detail, "solution": "" if ok else solution})
        etat = "OK      " if ok else "PROBLÈME"
        print(f"  [{etat}] {brique} : {detail}" + ("" if ok else f"\n             → {solution}"), flush=True)


def lancer(cmd, travail, nom, timeout=1800):
    t = time.time()
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=timeout)
    (pathlib.Path(travail) / f"journal-{nom}.txt").write_text(r.stdout + "\n--- stderr ---\n" + r.stderr, encoding="utf-8")
    return r, time.time() - t


def dernieres(r, n=3):
    lignes = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
    return " | ".join(lignes[-n:])[:300]


def cmd_essai(a):
    skill = pathlib.Path(a.skill).resolve()
    S = skill / "scripts"
    conf = json.loads((skill / "config.json").read_text(encoding="utf-8"))
    py = conf["python_rendu"]
    d = pathlib.Path(a.travail).resolve()
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir(parents=True)
    (d / "script.md").write_text(SCRIPT, encoding="utf-8")
    b = Bilan()
    journal = f"journaux détaillés : {d}"

    # 1. Voix Pocket + contrôle Parakeet
    r, t = lancer([py, str(S / "voix_pocket.py"), str(d)], d, "voix")
    fid = d / "data" / "fidelite-voix.json"
    voix_ok = r.returncode == 0 and (d / "audio.wav").exists()
    b.note("Voix de synthèse (Pocket TTS)", voix_ok,
           f"une phrase en {t:.0f} s (chargement compris)" if voix_ok else dernieres(r),
           f"relancer l'installeur ; {journal} (journal-voix.txt)")
    if voix_ok:
        try:
            info = json.loads(fid.read_text(encoding="utf-8"))
            moteur = str(info.get("controle") or "")
            ok_p = moteur.startswith("parakeet")
            b.note("Contrôle de fidélité (Parakeet)", ok_p,
                   f"phrase réécoutée et comparée ({info.get('sans_erreur', '?')}/1 sans écart)" if ok_p
                   else f"contrôle fait par un autre moteur ({moteur or 'inconnu'})",
                   "vérifier python_parakeet dans config.json ; relancer l'installeur")
        except Exception as e:  # noqa: BLE001
            b.note("Contrôle de fidélité (Parakeet)", False, f"bilan illisible ({e})", "relancer l'installeur")
    else:
        b.note("Contrôle de fidélité (Parakeet)", False, "non essayé (pas de voix)", "corriger d'abord la voix")

    # 2. Capsule + horodatage MFA
    mfa_ok = False
    if voix_ok:
        r, t = lancer([py, str(S / "nouvelle_capsule.py"), str(d), str(d / "audio.wav"), "--titre", "Essai"], d, "capsule")
        (d / "spec.js").write_text(SPEC, encoding="utf-8")
        r, t = lancer([py, str(S / "transcrire.py"), str(d / "audio.wav"), str(d)], d, "horodatage")
        sortie = r.stdout + r.stderr
        mfa_ok = r.returncode == 0 and "Horodatage MFA" in sortie
        b.note("Horodatage au mot (MFA)", mfa_ok,
               f"mots posés sur la voix en {t:.0f} s (≈ 45 s de lancement fixe)" if mfa_ok
               else ("repli sur Whisper : MFA absent ou en échec" if r.returncode == 0 else dernieres(r)),
               f"relancer l'installeur (étape MFA) ; {journal} (journal-horodatage.txt)")
    else:
        b.note("Horodatage au mot (MFA)", False, "non essayé (pas de voix)", "corriger d'abord la voix")

    # 3. Image rendue (Chromium + moteur canvas)
    if voix_ok and (d / "data").exists():
        r, t = lancer([py, str(S / "rendre_canvas.py"), str(d), "--images", "2.5"], d, "rendu")
        pngs = sorted((d / "planches").glob("*.png")) if (d / "planches").exists() else []
        mode = next((l.strip() for l in (r.stdout + r.stderr).splitlines() if "rendu graphique" in l), "")
        b.note("Rendu d'une image (Chromium)", r.returncode == 0 and bool(pngs),
               f"{pngs[0]} en {t:.0f} s {mode}" if pngs else dernieres(r),
               f"vérifier Chromium (navigateurs) et ffmpeg ; {journal} (journal-rendu.txt)")
    else:
        b.note("Rendu d'une image (Chromium)", False, "non essayé (pas de capsule)", "corriger d'abord la voix")

    # 4. Whisper (facultatif)
    pyw = conf.get("python_asr")
    if pyw:
        code = ("import sys; sys.path.insert(0, r'%s'); import asr_whisper; "
                "m, dev = asr_whisper.charger(sys.argv[2]); "
                "segs, _ = m.transcribe(sys.argv[1], language='fr'); "
                "print('@@', dev, ' '.join(s.text.strip() for s in segs))") % str(S)
        if (d / "audio.wav").exists():
            r, t = lancer([pyw, "-X", "utf8", "-c", code, str(d / "audio.wav"), conf.get("modele_asr", "medium")], d, "whisper")
            ligne = next((l for l in r.stdout.splitlines() if l.startswith("@@")), "")
            b.note("Transcription des enregistrements (Whisper)", bool(ligne),
                   f"{ligne[3:120]}… en {t:.0f} s" if ligne else dernieres(r),
                   f"relancer l'installeur en répondant oui ; {journal} (journal-whisper.txt)")
        else:
            b.note("Transcription des enregistrements (Whisper)", False, "non essayé (pas d'audio)", "corriger d'abord la voix")

    ok = all(l["ok"] for l in b.lignes)
    if a.bilan:
        pathlib.Path(a.bilan).write_text(json.dumps({"ok": ok, "date": time.strftime("%Y-%m-%d %H:%M"),
                                                     "briques": b.lignes}, ensure_ascii=False, indent=1), encoding="utf-8")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("config")
    c.add_argument("--skill", required=True)
    c.add_argument("--valeurs", required=True)
    e = sp.add_parser("essai")
    e.add_argument("--skill", required=True)
    e.add_argument("--travail", required=True)
    e.add_argument("--bilan")
    p = sp.add_parser("poids")
    p.add_argument("dossiers", nargs="+")
    cp = sp.add_parser("copier")
    cp.add_argument("--source", required=True)
    cp.add_argument("--cible", required=True)
    ff = sp.add_parser("ffmpeg")
    ff.add_argument("--archive", required=True)
    ff.add_argument("--dest", required=True)
    q = sp.add_parser("precharger")
    q.add_argument("quoi", choices=("pocket", "parakeet", "whisper"))
    q.add_argument("modele", nargs="?")
    a = ap.parse_args()
    {"config": cmd_config, "essai": cmd_essai, "poids": cmd_poids, "precharger": cmd_precharger,
     "copier": cmd_copier, "ffmpeg": cmd_ffmpeg}[a.cmd](a)


if __name__ == "__main__":
    main()
