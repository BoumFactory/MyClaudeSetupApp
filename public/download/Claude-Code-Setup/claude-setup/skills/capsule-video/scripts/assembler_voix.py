"""Assemble une capsule à VOIX MIXTES : voix enregistrée du professeur + voix de synthèse Piper (« tom »).

Usage :
    python assembler_voix.py <dossier_capsule> [--script script.md] [--prof-blocs <sortie de nettoyer_audio.py>]
                             [--debit 1.1] [--cible -16] [--sans-transcription]

Entrée : <capsule>/script.md au format de script_mixte.py :
    ## b01 [prof]      → segment du professeur (fichier <prof-blocs>/b01.wav, produit par
                         nettoyer_audio.py --bloc, ou à défaut <capsule>/prof/b01.wav)
    ## b02 [tom]       → synthétisé par Piper « tom » (ou [siwis], [upmc] : voix de secours) ; débit réglable
    ## b03 [estelle]   → synthétisé par Pocket TTS (voix du catalogue, ou alias de voix clonée de config.json, ex. [ma-voix]) :
                         voix_pocket.py --brut-seulement dans le Python « python_pocket », contrôle de fidélité compris
    Les lignes « > visuel : … » sont ignorées.

Traitement : les blocs tom sont synthétisés (mêmes règles de prononciation que voix.py : nombres en mots,
lettres, prononciation.json), tous les blocs sont mis en mono 44,1 kHz, puis NIVELÉS PAR VOIX à la même sonie
(EBU R128, --cible -16 LUFS, limiteur −1 dB) pour qu'on ne règle pas le volume entre deux phrases.

Sorties (mêmes noms que voix.py : tout le reste du skill fonctionne tel quel, ancres '@b05~"mot"' comprises) :
    <capsule>/audio.wav                    voix assemblée, silences compris
    <capsule>/voix/<id>.wav                un fichier par bloc (niveaux appliqués)
    <capsule>/data/temps-forts.json|js     {id, texte, voix, debut, fin, mots:[{mot, debut, fin, source, bloc, voix}]}
    <capsule>/data/transcript.json|js|txt  transcription mot à mot UNIFIÉE (chaque mot porte son bloc et sa voix)
    <capsule>/data/voix-intervalles.json|js  plages de chaque voix : badge « Voix de synthèse » seulement pendant tom
    (horodatage par transcrire.py : MFA sur le texte dit, « texte_reconnu » de prof-blocs.json pour les blocs [prof] ;
     --sans-transcription estime les mots au prorata des lettres)

Si Piper manque dans l'interpréteur courant, le script se relance avec "python_tts" de config.json.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess
import sys
import wave

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from commun import CONF  # noqa: E402
from script_mixte import VOIX_SYNTHESE, est_pocket, lire_script_mixte  # noqa: E402


def relancer_si_besoin(blocs):
    """Piper n'est requis (et le script ne se relance) que s'il y a des blocs [tom]/[siwis]/[upmc] ; Pocket tourne à part."""
    if not any(b["voix"] in VOIX_SYNTHESE for b in blocs):
        return
    try:
        __import__("piper")
        return
    except ImportError:
        pass
    py = CONF.get("python_voix") or CONF.get("python_tts")
    if not py or not os.path.exists(py) or os.path.abspath(py) == os.path.abspath(sys.executable):
        sys.exit("piper introuvable : l'installer, ou renseigner son Python dans config.json")
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    sys.exit(subprocess.call([py, str(pathlib.Path(__file__).resolve())] + sys.argv[1:], env=env))


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *args], check=True)


def vers_44k(entree, sortie, filtre=None):
    cmd = ["-i", str(entree)]
    if filtre:
        cmd += ["-af", filtre]
    ffmpeg(*cmd, "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(sortie))


def duree_wav(chemin):
    with wave.open(str(chemin), "rb") as w:
        return w.getnframes() / w.getframerate()


def sonie(fichiers):
    """Sonie intégrée (LUFS) de la mise bout à bout des fichiers (tous en mono 44,1 kHz)."""
    if not fichiers:
        return None
    entrees = []
    for f in fichiers:
        entrees += ["-i", str(f)]
    chaine = "".join(f"[{k}:a]" for k in range(len(fichiers))) + f"concat=n={len(fichiers)}:v=0:a=1,ebur128=framelog=quiet"
    r = subprocess.run(["ffmpeg", "-v", "info", *entrees, "-filter_complex", chaine, "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    trouves = re.findall(r"I:\s+(-?[\d.]+)\s+LUFS", r.stderr)
    return float(trouves[-1]) if trouves else None


def synthetiser_pocket(blocs, dossier, a):
    """Blocs à voix Pocket TTS (catalogue ou voix clonée) : voix_pocket.py --brut-seulement dans le Python de Pocket
    (python_pocket), avec contrôle Whisper et jusqu'à 3 essais ; l'assemblage et le nivellement restent ici."""
    if not any(est_pocket(b["voix"]) for b in blocs):
        return
    py = CONF.get("python_pocket")
    if not py or not os.path.exists(py):
        sys.exit("Blocs à voix Pocket TTS mais python_pocket est absent de config.json (voir installation/LISEZMOI.md).")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    cmd = [py, "-X", "utf8", str(ICI / "voix_pocket.py"), str(dossier), "--script", a.script, "--brut-seulement", "--modifies"]
    if subprocess.call(cmd, env=env) != 0:
        sys.exit("voix_pocket.py a échoué")
    bruts = json.loads((dossier / "voix-brut" / "pocket-bruts.json").read_text(encoding="utf-8"))
    for b in blocs:
        if est_pocket(b["voix"]):
            b["texte_dit"] = bruts[b["id"]]["texte_dit"]
            b["brut"] = pathlib.Path(bruts[b["id"]]["fichier"])
            print(f"  {b['id']} [{b['voix']}] {duree_wav(b['brut']):5.1f} s | {b['texte_dit'][:70]}")


def synthetiser(blocs, dossier, a):
    synthetiser_pocket(blocs, dossier, a)
    if not any(b["voix"] in VOIX_SYNTHESE for b in blocs):
        return
    import voix  # noqa: PLC0415  (voix.py du skill, inchangé : pour_l_oreille, Piper)
    dico_f = dossier / "prononciation.json"
    dico = json.loads(dico_f.read_text(encoding="utf-8")) if dico_f.exists() else {}
    moteurs = {}
    brut = dossier / "voix-brut"
    brut.mkdir(exist_ok=True)
    ns = argparse.Namespace(debit=a.debit, silence_phrase=a.silence_phrase)
    for b in blocs:
        if b["voix"] not in VOIX_SYNTHESE:
            continue
        b["texte_dit"] = voix.pour_l_oreille(b["texte"], dico)
        if b["voix"] not in moteurs:
            moteurs[b["voix"]] = voix.Piper(b["voix"])
        sortie = brut / f"{b['id']}.wav"
        moteurs[b["voix"]].dire(b["texte_dit"], sortie, ns, b["lent"])
        print(f"  {b['id']} [{b['voix']}] {duree_wav(sortie):5.1f} s | {b['texte_dit'][:70]}")
        b["brut"] = sortie


def trouver_prof(blocs, dossier, a):
    meta = {}
    racine = pathlib.Path(a.prof_blocs) if a.prof_blocs else None
    if racine and (racine / "prof-blocs.json").exists():
        meta = json.loads((racine / "prof-blocs.json").read_text(encoding="utf-8"))
    brut = dossier / "voix-brut"
    brut.mkdir(exist_ok=True)
    manquants = []
    for b in blocs:
        if b["voix"] != "prof":
            continue
        candidats = []
        if b["id"] in meta:
            candidats.append(racine / meta[b["id"]]["fichier"])
        candidats += [racine / "prof-blocs" / f"{b['id']}.wav"] if racine else []
        candidats += [dossier / "prof" / f"{b['id']}.wav"]
        src = next((c for c in candidats if c.exists()), None)
        if not src:
            manquants.append(b["id"])
            continue
        b["brut"] = brut / f"{b['id']}.wav"
        vers_44k(src, b["brut"])
        b["texte_dit"] = b["texte"]
        if meta.get(b["id"], {}).get("texte_reconnu"):
            b["texte_reconnu"] = meta[b["id"]]["texte_reconnu"]  # ce que le prof a dit : MFA aligne ce texte
    if manquants:
        sys.exit(f"Segments prof introuvables : {', '.join(manquants)}. Les produire avec "
                 f"nettoyer_audio.py applique <sortie> --bloc script.md, puis --prof-blocs <sortie>.")


def niveler(blocs, dossier, a):
    dv = dossier / "voix"
    dv.mkdir(exist_ok=True)
    # chaque voix (prof, tom, estelle, ma-voix…) est nivelée séparément : la voix brute de Pocket sort à -33 LUFS,
    # celle de Piper plus haut ; les blocs de synthèse sont d'abord mis à 44,1 kHz avant la mesure
    for b in blocs:
        if b["voix"] == "prof":
            b["brut44"] = b["brut"]
        else:
            tmp = dossier / "voix-brut" / f"{b['id']}-44k.wav"
            vers_44k(b["brut"], tmp)
            b["brut44"] = tmp
    gains = {}
    for voix in sorted({b["voix"] for b in blocs}):
        i = sonie([b["brut44"] for b in blocs if b["voix"] == voix])
        gains[voix] = (a.cible - i) if i is not None else 0.0
        if i is not None:
            print(f"Sonie {voix} : {i:.1f} LUFS → gain {gains[voix]:+.1f} dB (cible {a.cible} LUFS)")
    for b in blocs:
        g = gains[b["voix"]]
        d = duree_wav(b["brut44"])
        fd = min(0.006, d / 4)
        filtre = f"volume={g:.2f}dB,alimiter=limit=0.89:level=disabled,afade=t=in:st=0:d={fd:.4f},afade=t=out:st={max(0.0, d - fd):.4f}:d={fd:.4f}"
        vers_44k(b["brut44"], dv / f"{b['id']}.wav", filtre)
    return gains


def assembler(blocs, dossier, a):
    dv = dossier / "voix"
    morceaux, t = [], 0.0

    def silence(s):
        return b"\x00" * (int(round(s * 44100)) * 2)

    morceaux.append(silence(0.25))
    t = 0.25
    for b in blocs:
        with wave.open(str(dv / f"{b['id']}.wav"), "rb") as w:
            morceaux.append(w.readframes(w.getnframes()))
            b["debut"] = round(t, 3)
            t += w.getnframes() / w.getframerate()
            b["fin"] = round(t, 3)
        pause = b["pause"] + a.pause_en_plus
        morceaux.append(silence(pause))
        t += pause
    with wave.open(str(dossier / "audio.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes(b"".join(morceaux))
    return t


def ecrire_temps_forts(blocs, dossier):
    champs = ("id", "texte", "texte_dit", "texte_reconnu", "lent", "voix", "debut", "fin")
    tf = [{k: b[k] for k in champs if k in b} | ({"mots": b["mots"]} if "mots" in b else {}) for b in blocs]
    d = dossier / "data"
    (d / "temps-forts.json").write_text(json.dumps(tf, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "temps-forts.js").write_text("window.TEMPS_FORTS = " + json.dumps(tf, ensure_ascii=False) + ";\n", encoding="utf-8")
    return tf


def mots_estimes(b):
    """Sans reconnaissance vocale : mots répartis au prorata de leurs lettres dans la durée du bloc."""
    mots = [m for m in re.split(r"[\s]+", b["texte"]) if re.search(r"\w", m)]
    poids = [len(re.sub(r"\W", "", m)) + 1 for m in mots]
    total, t, res = sum(poids), b["debut"], []
    for m, p in zip(mots, poids):
        d = (b["fin"] - b["debut"]) * p / total
        res.append({"mot": m, "debut": round(t, 3), "fin": round(t + d, 3), "source": "estime"})
        t += d
    return res


def unifier(blocs, dossier, duree_totale, estime):
    d = dossier / "data"
    if estime:
        for b in blocs:
            b["mots"] = mots_estimes(b)
        unifies = [dict(m, bloc=b["id"], voix=b["voix"]) for b in blocs for m in b["mots"]]
        for i, m in enumerate(unifies):
            m["i"] = i
        tr = {"duree": round(duree_totale, 3), "texte": " ".join(b["texte"] for b in blocs),
              "segments": [{"debut": b["debut"], "fin": b["fin"], "texte": b["texte"], "mots": []} for b in blocs],
              "mots": unifies}
    else:
        tr = json.loads((d / "transcript.json").read_text(encoding="utf-8"))
        tf = json.loads((d / "temps-forts.json").read_text(encoding="utf-8"))
        par_id = {b["id"]: b for b in tf}
        for b in blocs:
            b["mots"] = par_id[b["id"]].get("mots", [])
        for m in tr["mots"]:
            b = next((x for x in blocs if x["debut"] - 0.2 <= m["debut"] < x["fin"] + 0.2), None)
            if b:
                m["bloc"], m["voix"] = b["id"], b["voix"]
        for s in tr["segments"]:
            b = next((x for x in blocs if x["debut"] - 0.2 <= s["debut"] < x["fin"] + 0.2), None)
            if b:
                s["bloc"], s["voix"] = b["id"], b["voix"]
    for b in blocs:
        for m in b.get("mots", []):
            m["bloc"], m["voix"] = b["id"], b["voix"]
    tr["blocs"] = [{"id": b["id"], "voix": b["voix"], "debut": b["debut"], "fin": b["fin"]} for b in blocs]
    (d / "transcript.json").write_text(json.dumps(tr, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "transcript.js").write_text("window.TRANSCRIPT = " + json.dumps(tr, ensure_ascii=False) + ";\n", encoding="utf-8")
    with open(d / "transcript.txt", "w", encoding="utf-8") as f:
        for s in tr["segments"]:
            f.write(f"[{s['debut']:7.2f}] ({s.get('voix', '?'):<5}) {s['texte']}\n")
    ecrire_temps_forts(blocs, dossier)
    inter = {"duree": round(duree_totale, 3), "blocs": tr["blocs"]}
    for v in sorted({b["voix"] for b in blocs}):
        inter[v] = [[b["debut"], b["fin"]] for b in blocs if b["voix"] == v]
    (d / "voix-intervalles.json").write_text(json.dumps(inter, ensure_ascii=False, indent=1), encoding="utf-8")
    (d / "voix-intervalles.js").write_text("window.VOIX_INTERVALLES = " + json.dumps(inter, ensure_ascii=False) + ";\n", encoding="utf-8")
    return tr, inter


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("dossier")
    ap.add_argument("--script", default="script.md")
    ap.add_argument("--prof-blocs", default=None, help="dossier de sortie de nettoyer_audio.py (prof-blocs.json)")
    ap.add_argument("--debit", type=float, default=1.1, help="ralentissement Piper (length_scale) : 1.0 = débit naturel")
    ap.add_argument("--silence-phrase", type=float, default=0.45)
    ap.add_argument("--pause-en-plus", type=float, default=0.2, help="ajouté à chaque [pause] entre blocs (s)")
    ap.add_argument("--cible", type=float, default=-16.0, help="sonie visée de chaque voix (LUFS)")
    ap.add_argument("--sans-transcription", action="store_true",
                    help="n'appelle pas Whisper : mots estimés au prorata des lettres (ancres moins précises)")
    a = ap.parse_args()
    d = pathlib.Path(a.dossier)
    (d / "data").mkdir(parents=True, exist_ok=True)
    blocs = lire_script_mixte(d / a.script)
    relancer_si_besoin(blocs)
    n_tom = sum(b["voix"] != "prof" for b in blocs)
    print(f"{len(blocs)} blocs : {len(blocs) - n_tom} prof, {n_tom} synthèse")
    trouver_prof(blocs, d, a)
    synthetiser(blocs, d, a)
    niveler(blocs, d, a)
    total = assembler(blocs, d, a)
    ecrire_temps_forts(blocs, d)
    print(f"audio.wav : {total:.1f} s")

    if not a.sans_transcription:
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        # transcrire.py : horodatage MFA de chaque bloc sur son texte dit (texte_reconnu pour un bloc [prof]),
        # Whisper si MFA manque ; puis aligne les mots exacts du script.
        if subprocess.call([sys.executable, str(ICI / "transcrire.py"), str(d / "audio.wav"), str(d)], env=env) != 0:
            sys.exit("transcrire.py a échoué (relancer avec --sans-transcription pour des mots estimés)")
    tr, inter = unifier(blocs, d, total, a.sans_transcription)
    mesure = sonie([d / "audio.wav"])
    print(f"\nTranscription unifiée : {len(tr['mots'])} mots, {len(tr['blocs'])} blocs "
          f"(sonie du mélange : {mesure:.1f} LUFS)" if mesure else "")
    for v in sorted(k for k in inter if k not in ("duree", "blocs")):
        print(f"  voix {v} : " + ", ".join(f"{x:.1f}–{y:.1f}" for x, y in inter[v]))
    print("Badge « Voix de synthèse » : C.badgeVoix({ voix: 'tom' }) (plugin blocs) ou data/voix-intervalles.json")


if __name__ == "__main__":
    main()
