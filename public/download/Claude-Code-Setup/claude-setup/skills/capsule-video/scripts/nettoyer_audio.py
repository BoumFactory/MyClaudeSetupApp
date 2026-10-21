"""Nettoyage d'un enregistrement du professeur : blancs longs, hésitations, reprises.

Trois temps, validables à la main :

    python nettoyer_audio.py analyse <audio> <sortie> [--seuil-db -35] [--blanc-min 0.8] [--garder 0.3]
    (éditer <sortie>/coupes.json : "actif": false pour garder une coupe, ou ajouter une coupe "manuel")
    python nettoyer_audio.py applique <sortie> [--bloc script.md]
    python nettoyer_audio.py tout <audio> <sortie> [--bloc script.md]         # sans validation

Détections (toutes réglables, toutes listées dans coupes.json et coupes.txt) :
  - blancs longs : ffmpeg silencedetect (seuil en dB, durée minimale) ; on ne garde que --garder secondes
    de silence (≈ 0,3 s) au lieu du blanc entier ;
  - hésitations « euh », « hum » : faster-whisper configuré pour les CONSERVER (initial_prompt qui en contient,
    suppression de jetons désactivée, pas de filtre VAD, horodatage au mot) ;
  - reprises : phrase recommencée (n-gramme de mots répété peu après) → on garde la DERNIÈRE prise.
Reconnaissance : Whisper (défaut, carte graphique si disponible, sinon processeur). --asr parakeet : repli sur
processeur, 10 fois plus rapide que Whisper sur processeur, mais il efface les « euh » et les mots répétés à la
suite (hésitations et bégaiements non détectés ; reprises de phrases entières et blancs, oui).

Application : coupes jointes par des micro-fondus (--fondu, 10 ms) : pas de clic. Puis nouvelle
transcription de l'audio nettoyé (transcrire.py : reconnaissance, puis horodatage MFA du texte reconnu) dans
<sortie>/data/.

Option --bloc script.md (format script_mixte.py : « ## b01 [prof] » / « ## b02 [tom] ») : les blocs [prof] du
script lu sont alignés sur l'audio nettoyé ; chaque bloc est découpé dans <sortie>/prof-blocs/bNN.wav
(+ prof-blocs.json), prêt pour assembler_voix.py.

Sorties dans <sortie>/ : mots-bruts.json, coupes.json, coupes.txt, audio-nettoye.wav, data/transcript.*,
prof-blocs/, prof-blocs.json, alignement-blocs.txt.

prof-blocs.json donne aussi, par bloc, « texte_reconnu » (ce que le prof a réellement dit) : MFA l'aligne.
Le script se relance seul avec le Python du moteur (python_asr pour Whisper, python_parakeet).
"""
import argparse
import difflib
import json
import os
import pathlib
import re
import subprocess
import sys
import unicodedata

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))

PROMPT_HESITATIONS = ("Euh, alors euh... hum, bon, euh, voilà. Hmm, donc euh, on va, euh, regarder ça. "
                      "Heu, ben, hum, euh.")
FILLER = re.compile(r"^(e+u+h+|h?e+u+h*|heum+|hum+|hmm+|hm+|mmh+|mh+|hem+|euhh+|ehh+|eh|ah+)$")
MOTS_OUTILS = {"le", "la", "les", "de", "du", "des", "un", "une", "je", "on", "il", "elle", "et", "a", "que", "qui",
               "ce", "ca", "donc", "alors", "ben", "en", "se", "ne", "est", "y"}


def moteur_asr(a):
    import commun
    return getattr(a, "asr", None) or commun.CONF.get("asr_enregistrements") or "whisper"


def relancer_si_besoin(a):
    """Relance dans le Python du moteur de reconnaissance (python_asr pour Whisper, python_parakeet)."""
    import commun
    commun.relancer_pour(moteur_asr(a), pathlib.Path(__file__).resolve(), sys.argv[1:])


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


EXTRA = set()   # formes que Whisper prend pour des hésitations (« heure » pour « euh »), ajoutées par --hesitation-extra


def est_hesitation(mot):
    n = norm(mot)
    return bool(FILLER.match(n)) or n in EXTRA


def duree_audio(chemin):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(chemin)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def fmt(t):
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


# ---------------------------------------------------------------- blancs
def detecter_blancs(audio, seuil_db, blanc_min, duree):
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(audio), "-af", f"silencedetect=noise={seuil_db}dB:d={blanc_min}",
                        "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    blancs, debut = [], None
    for ligne in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", ligne)
        if m:
            debut = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end:\s*([\d.]+)", ligne)
        if m and debut is not None:
            blancs.append((debut, float(m.group(1))))
            debut = None
    if debut is not None:
        blancs.append((debut, duree))
    return blancs


# ---------------------------------------------------------------- reconnaissance
def mots_parakeet(audio_16k):
    """Repli sans Whisper : Parakeet ONNX sur processeur, découpé par le VAD. ATTENTION : Parakeet efface les « euh »
    et les mots répétés à la suite (« mais mais ») : hésitations et bégaiements ne sont pas détectés."""
    import asr_parakeet
    print("Reconnaissance Parakeet (--asr parakeet) : « euh » et mots répétés NON détectés, --vocab sans effet")
    mots, _ = asr_parakeet.mots(asr_parakeet.charger(), audio_16k)
    return [m for m in mots if norm(m["mot"])]


def mots_whisper(audio_16k, args):
    import asr_whisper
    model, _ = asr_whisper.charger(args.modele, cpu=args.cpu)
    prompt = PROMPT_HESITATIONS + (" " + args.vocab if args.vocab else "")
    segs, _ = model.transcribe(
        str(audio_16k), language="fr", word_timestamps=True, vad_filter=False, initial_prompt=prompt,
        suppress_tokens=[], suppress_blank=False, condition_on_previous_text=False, beam_size=5, temperature=0.0)
    mots = []
    for s in segs:
        for w in s.words or []:
            mot = w.word.strip()
            if norm(mot):
                mots.append({"mot": mot, "debut": round(w.start, 3), "fin": round(w.end, 3)})
    return mots


# ---------------------------------------------------------------- détection des coupes
def coupes_blancs(blancs, garder, duree):
    res = []
    for d, f in blancs:
        reste = min(garder, f - d)
        debut_coupe = d + (0.1 if d <= 0.01 else reste / 2)       # début de fichier : 0,1 s de pièce vide
        fin_coupe = f - (0.1 if f >= duree - 0.01 else reste / 2)   # fin de fichier idem
        if fin_coupe - debut_coupe >= 0.15:
            res.append({"type": "blanc", "debut": round(debut_coupe, 3), "fin": round(fin_coupe, 3),
                        "texte": f"blanc de {f - d:.1f} s réduit à {garder:.1f} s"})
    return res


def coupes_hesitations(mots):
    res = []
    for i, w in enumerate(mots):
        if not est_hesitation(w["mot"]):
            continue
        prec_fin = mots[i - 1]["fin"] if i else 0.0
        suiv_debut = mots[i + 1]["debut"] if i + 1 < len(mots) else w["fin"] + 0.1
        d = max(w["debut"] - 0.04, (prec_fin + w["debut"]) / 2)
        f = min(w["fin"] + 0.04, (w["fin"] + suiv_debut) / 2)
        res.append({"type": "hésitation", "debut": round(d, 3), "fin": round(f, 3), "texte": w["mot"]})
    return res


def coupes_reprises(mots, min_n, max_ecart_mots, max_ecart_s):
    """Phrase recommencée : le même n-gramme de mots reparaît peu après → on coupe la prise précédente."""
    flux = [(norm(w["mot"]), k) for k, w in enumerate(mots) if norm(w["mot"]) and not est_hesitation(w["mot"])]
    normes = [n for n, _ in flux]
    res, i = [], 0
    while i < len(flux):
        trouve = None
        for n in range(min(12, len(flux) - i), 0, -1):
            if n < min_n and not (n == 1):
                continue
            graine = normes[i:i + n]
            for j in range(i + 1, min(len(flux) - n + 1, i + max_ecart_mots + 1)):
                if n == 1 and j != i + 1:
                    continue
                if normes[j:j + n] == graine and mots[flux[j][1]]["debut"] - mots[flux[i][1]]["debut"] <= max_ecart_s:
                    trouve = (n, j)
                    break
            if trouve:
                break
        if not trouve:
            i += 1
            continue
        n, j = trouve
        ki, kj = flux[i][1], flux[j][1]
        immediat = (j == i + n)
        if n == 1:
            actif = normes[i] in MOTS_OUTILS
            note = "mot répété à la suite : à vérifier" if not actif else "bégaiement"
        elif n >= 4 or immediat:
            actif, note = True, "phrase recommencée" if not immediat else "bégaiement"
        else:
            actif, note = False, "répétition courte (3 mots) : peut être voulue, à valider"
        prec_fin = mots[ki - 1]["fin"] if ki else 0.0
        d = max(mots[ki]["debut"] - 0.05, (prec_fin + mots[ki]["debut"]) / 2)
        f = max(d + 0.05, mots[kj]["debut"] - 0.05)
        retire = " ".join(w["mot"] for w in mots[ki:kj])
        garde = " ".join(w["mot"] for w in mots[kj:kj + n + 3])
        res.append({"type": "reprise", "debut": round(d, 3), "fin": round(f, 3), "actif": actif,
                    "texte": retire, "garde": garde, "note": note})
        i = j
    return res


def fusionner(coupes):
    """Union des coupes ACTIVES, triées ; deux coupes à moins de 40 ms l'une de l'autre sont jointes."""
    iv = sorted((c["debut"], c["fin"]) for c in coupes if c.get("actif", True) and c["fin"] > c["debut"])
    res = []
    for d, f in iv:
        if res and d <= res[-1][1] + 0.04:
            res[-1][1] = max(res[-1][1], f)
        else:
            res.append([d, f])
    return res


def ecrire_resume(sortie, donnees):
    lignes = [f"Coupes proposées pour {donnees['audio']} ({donnees['duree']:.1f} s)", ""]
    total = 0.0
    for c in donnees["coupes"]:
        etat = "actif  " if c.get("actif", True) else "inactif"
        dur = c["fin"] - c["debut"]
        if c.get("actif", True):
            total += dur
        extra = f"  → garde « {c['garde']} »" if c.get("garde") else ""
        note = f"  ({c['note']})" if c.get("note") else ""
        lignes.append(f"{c['id']}  {etat}  {c['type']:<10} {fmt(c['debut'])} → {fmt(c['fin'])}  ({dur:4.2f} s)  "
                      f"« {c['texte']} »{extra}{note}")
    par_type = {}
    for c in donnees["coupes"]:
        if c.get("actif", True):
            par_type[c["type"]] = par_type.get(c["type"], 0) + (c["fin"] - c["debut"])
    lignes += ["", "Temps retiré (coupes actives) : " + ", ".join(f"{k} {v:.1f} s" for k, v in par_type.items())
               + f" — total {total:.1f} s sur {donnees['duree']:.1f} s"]
    lignes += ["", "Pour valider : éditer coupes.json (\"actif\": false pour garder, debut/fin pour ajuster, ou une coupe",
               "{\"type\": \"manuel\", \"debut\": 12.3, \"fin\": 13.0, \"texte\": \"toux\"}), puis : nettoyer_audio.py applique <sortie>"]
    (sortie / "coupes.txt").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print("\n".join(lignes))


# ---------------------------------------------------------------- analyse
def analyser(a):
    relancer_si_besoin(a)
    EXTRA.update(norm(x) for x in a.hesitation_extra.split(",") if norm(x))
    import commun  # noqa: F401
    audio = pathlib.Path(a.audio).resolve()
    sortie = pathlib.Path(a.sortie)
    sortie.mkdir(parents=True, exist_ok=True)
    duree = duree_audio(audio)
    w16 = sortie / "audio-16k.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(audio), "-ac", "1", "-ar", "16000", str(w16)], check=True)

    blancs = detecter_blancs(w16, a.seuil_db, a.blanc_min, duree)
    print(f"{len(blancs)} blanc(s) de {a.blanc_min} s ou plus (seuil {a.seuil_db} dB)")
    mots = mots_parakeet(w16) if moteur_asr(a) == "parakeet" else mots_whisper(w16, a)
    # Whisper hallucine parfois dans les longs silences : un mot entièrement dans un blanc est écarté
    avant = len(mots)
    def dans_silence(w):
        # marge de 0,25 s : Whisper étire souvent l'horodatage du premier mot après un blanc vers l'arrière
        return any(d + 0.25 <= w["debut"] and w["fin"] <= f - 0.25 for d, f in blancs if f - d >= 1.0)
    ecartes = [w for w in mots if dans_silence(w)]
    mots = [w for w in mots if not dans_silence(w)]
    if ecartes:
        print(f"{avant - len(mots)} mot(s) reconnus dans un silence écartés (hallucination probable) : "
              + ", ".join(f"« {w['mot']} » {w['debut']:.1f} s" for w in ecartes))
    (sortie / "mots-bruts.json").write_text(json.dumps(mots, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(mots)} mots reconnus (hésitations conservées)")

    coupes = []
    if not a.sans_blancs:
        coupes += coupes_blancs(blancs, a.garder, duree)
    if not a.sans_hesitations:
        coupes += coupes_hesitations(mots)
    if not a.sans_reprises:
        coupes += coupes_reprises(mots, a.min_reprise, a.ecart_mots, a.ecart_s)
    coupes.sort(key=lambda c: c["debut"])
    for k, c in enumerate(coupes, 1):
        c["id"] = f"c{k:02d}"
        c.setdefault("actif", True)
    donnees = {"audio": str(audio), "duree": round(duree, 3),
               "reglages": {k: getattr(a, k) for k in ("seuil_db", "blanc_min", "garder", "min_reprise", "ecart_mots", "ecart_s")},
               "coupes": coupes}
    (sortie / "coupes.json").write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
    ecrire_resume(sortie, donnees)
    return donnees


# ---------------------------------------------------------------- application
def appliquer(a):
    sortie = pathlib.Path(a.sortie)
    donnees = json.loads((sortie / "coupes.json").read_text(encoding="utf-8"))
    audio, duree = pathlib.Path(donnees["audio"]), donnees["duree"]
    coupes = fusionner(donnees["coupes"])
    garde, t = [], 0.0
    for d, f in coupes:
        if d - t >= 0.05:
            garde.append((t, min(d, duree)))
        t = max(t, f)
    if duree - t >= 0.05:
        garde.append((t, duree))
    if not garde:
        sys.exit("Toutes les coupes retirent l'audio entier : rien à garder.")
    fondu = a.fondu
    filtres, noms = [], []
    for k, (d, f) in enumerate(garde):
        ch = f"atrim=start={d:.4f}:end={f:.4f},asetpts=PTS-STARTPTS"
        L = f - d
        fd = min(fondu, L / 3)
        if d > 0.001:
            ch += f",afade=t=in:st=0:d={fd:.4f}"
        if f < duree - 0.001:
            ch += f",afade=t=out:st={L - fd:.4f}:d={fd:.4f}"
        filtres.append(f"[0:a]{ch}[s{k}]")
        noms.append(f"[s{k}]")
    filtres.append("".join(noms) + f"concat=n={len(garde)}:v=0:a=1[sortie]")
    script = sortie / "filtre-coupes.txt"
    script.write_text(";\n".join(filtres), encoding="utf-8")
    nettoye = sortie / "audio-nettoye.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(audio), "-filter_complex_script", str(script),
                    "-map", "[sortie]", "-c:a", "pcm_s16le", str(nettoye)], check=True)
    nouvelle = duree_audio(nettoye)
    print(f"Audio nettoyé : {nettoye} ({duree:.1f} s → {nouvelle:.1f} s, {len(coupes)} coupe(s) jointes, "
          f"{len(garde)} morceaux gardés, fondu {fondu * 1000:.0f} ms)")

    # nouvelle transcription de l'audio nettoyé (transcrire.py : reconnaissance, puis horodatage MFA sur ce texte)
    if not a.sans_transcription:
        cmd = [sys.executable, str(ICI / "transcrire.py"), str(nettoye), str(sortie), "--asr", moteur_asr(a)]
        if a.vocab:
            cmd += ["--vocab", a.vocab]
        env = dict(os.environ, PYTHONIOENCODING="utf-8")
        if subprocess.call(cmd, env=env) != 0:
            sys.exit("transcrire.py a échoué")
    if a.bloc:
        if a.sans_transcription:
            sys.exit("--bloc exige la transcription (retirer --sans-transcription)")
        decouper_blocs(sortie, nettoye, pathlib.Path(a.bloc))


# ---------------------------------------------------------------- alignement des blocs [prof]
def decouper_blocs(sortie, nettoye, script):
    import aligner
    from script_mixte import lire_script_mixte
    blocs = [b for b in lire_script_mixte(script) if b["voix"] == "prof"]
    if not blocs:
        sys.exit("Le script ne contient aucun bloc [prof].")
    tr = json.loads((sortie / "data" / "transcript.json").read_text(encoding="utf-8"))
    reconnus = []
    for m in tr["mots"]:
        for morceau in re.split(r"['’]+", m["mot"]):
            if aligner.norm(morceau):
                reconnus.append({"n": aligner.norm(morceau), "debut": m["debut"], "fin": m["fin"]})
    jetons, proprio = [], []
    for k, b in enumerate(blocs):
        for _, n in aligner.jetons(b["texte"]):
            jetons.append(n)
            proprio.append(k)
    sm = difflib.SequenceMatcher(a=jetons, b=[r["n"] for r in reconnus], autojunk=False)
    paires = {}   # bloc → indices des mots reconnus appariés
    for bloc in sm.get_matching_blocks():
        for i in range(bloc.size):
            paires.setdefault(proprio[bloc.a + i], []).append(bloc.b + i)
    duree = duree_audio(nettoye)
    rapport, cov, premiers, derniers = [], [], [], []
    for k, b in enumerate(blocs):
        total = sum(1 for p in proprio if p == k)
        ap = paires.get(k, [])
        if not ap:
            sys.exit(f"Bloc {b['id']} introuvable dans l'enregistrement nettoyé (aucun mot en commun). "
                     f"Vérifier le texte du script ou l'enregistrement.")
        cov.append(len(ap) / total)
        premiers.append(min(ap))
        derniers.append(max(ap))
    for k in range(1, len(blocs)):   # les blocs se suivent dans l'enregistrement
        premiers[k] = max(premiers[k], derniers[k - 1] + 1)
    # frontière entre deux blocs : le plus grand silence entre deux mots, entre le dernier mot apparié de l'un
    # et le premier de l'autre (les mots non appariés, mal reconnus, restent ainsi avec leur bloc)
    debuts, fins = [], []
    for k in range(len(blocs)):
        d_mot = reconnus[premiers[k]]["debut"]
        f_mot = reconnus[derniers[k]]["fin"]
        debuts.append(max(0.0, d_mot - 0.25) if k == 0 else d_mot)
        fins.append(f_mot)
    for k in range(len(blocs) - 1):
        j0, j1 = derniers[k], premiers[k + 1]
        meilleur = (-1.0, reconnus[j0]["fin"], reconnus[j1]["debut"])
        for j in range(j0, j1):
            g = reconnus[j + 1]["debut"] - reconnus[j]["fin"]
            if g > meilleur[0]:
                meilleur = (g, reconnus[j]["fin"], reconnus[j + 1]["debut"])
        g, a_fin, b_debut = meilleur
        fins[k] = a_fin + min(0.30, max(0.0, g) / 2)
        debuts[k + 1] = b_debut - min(0.25, max(0.0, g) / 2)
    fins[-1] = min(duree, fins[-1] + 0.30)
    sortie_b = sortie / "prof-blocs"
    sortie_b.mkdir(exist_ok=True)
    meta = {}
    for k, b in enumerate(blocs):
        d0, f0 = debuts[k], fins[k]
        cov_k = cov[k]
        fd = 0.008
        fichier = sortie_b / f"{b['id']}.wav"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{d0:.3f}", "-to", f"{f0:.3f}", "-i", str(nettoye),
                        "-af", f"afade=t=in:st=0:d={fd},afade=t=out:st={max(0.0, f0 - d0 - fd):.3f}:d={fd}",
                        "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(fichier)], check=True)
        # texte réellement dit dans ce bloc (transcription) : assembler_voix.py le transmet, et MFA aligne ce texte-là
        # (et non le script, dont le prof a pu s'écarter)
        dits = [m["mot"] for m in tr["mots"] if d0 - 0.02 <= m["debut"] and m["fin"] <= f0 + 0.02]
        meta[b["id"]] = {"fichier": f"prof-blocs/{b['id']}.wav", "debut": round(d0, 3), "fin": round(f0, 3),
                         "texte": b["texte"], "texte_reconnu": " ".join(dits), "couverture": round(cov_k, 2)}
        alerte = "  ⚠ couverture faible : l'enregistrement s'écarte du script" if cov_k < 0.6 else ""
        rapport.append(f"{b['id']}  {fmt(d0)} → {fmt(f0)}  couverture {cov_k:.0%}{alerte}  « {b['texte'][:60]} »")
    (sortie / "prof-blocs.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    (sortie / "alignement-blocs.txt").write_text("\n".join(rapport) + "\n", encoding="utf-8")
    print("\nBlocs [prof] alignés sur l'audio nettoyé :\n" + "\n".join(rapport))


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)

    def reglages_analyse(p):
        p.add_argument("--seuil-db", type=float, default=-35.0, help="niveau sous lequel c'est un silence (dB)")
        p.add_argument("--blanc-min", type=float, default=0.8, help="durée minimale d'un blanc à réduire (s)")
        p.add_argument("--garder", type=float, default=0.3, help="silence conservé à la place du blanc (s)")
        p.add_argument("--min-reprise", type=int, default=3, help="longueur minimale d'un n-gramme répété (mots)")
        p.add_argument("--ecart-mots", type=int, default=40, help="distance maximale entre deux prises (mots)")
        p.add_argument("--ecart-s", type=float, default=20.0, help="distance maximale entre deux prises (s)")
        p.add_argument("--hesitation-extra", default="", help="mots que Whisper confond avec « euh » (ex. heure), coupés aussi")
        p.add_argument("--sans-blancs", action="store_true")
        p.add_argument("--sans-hesitations", action="store_true")
        p.add_argument("--sans-reprises", action="store_true")
        p.add_argument("--modele", default="large-v3")
        p.add_argument("--cpu", action="store_true")
        p.add_argument("--vocab", default="", help="notations et mots rares attendus (injectés dans le prompt)")
        p.add_argument("--asr", choices=("whisper", "parakeet"), default=None,
                       help="reconnaissance : whisper (défaut, asr_enregistrements de config.json) | parakeet (repli "
                            "processeur : ni « euh » ni mots répétés détectés)")

    def reglages_applique(p):
        p.add_argument("--fondu", type=float, default=0.010, help="micro-fondu à chaque jonction (s)")
        p.add_argument("--bloc", default=None, help="script.md à blocs [prof]/[tom] : découpe l'audio en blocs")
        p.add_argument("--sans-transcription", action="store_true")
        p.add_argument("--vocab", default=argparse.SUPPRESS)
        p.add_argument("--asr", choices=("whisper", "parakeet"), default=None)

    p1 = sp.add_parser("analyse", help="détecte les coupes (écrit coupes.json et coupes.txt)")
    p1.add_argument("audio"); p1.add_argument("sortie")
    reglages_analyse(p1)
    p2 = sp.add_parser("applique", help="applique coupes.json, retranscrit, découpe les blocs")
    p2.add_argument("sortie")
    reglages_applique(p2)
    p3 = sp.add_parser("tout", help="analyse puis applique, sans validation")
    p3.add_argument("audio"); p3.add_argument("sortie")
    reglages_analyse(p3)
    p3.add_argument("--fondu", type=float, default=0.010)
    p3.add_argument("--bloc", default=None)
    p3.add_argument("--sans-transcription", action="store_true")
    a = ap.parse_args()
    if not hasattr(a, "vocab"):
        a.vocab = ""
    if a.cmd == "analyse":
        analyser(a)
    elif a.cmd == "applique":
        appliquer(a)
    else:
        analyser(a)
        appliquer(a)


if __name__ == "__main__":
    main()
