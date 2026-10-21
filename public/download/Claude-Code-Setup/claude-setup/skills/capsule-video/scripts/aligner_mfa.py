"""Horodatage au mot par alignement forcé (Montreal Forced Aligner, MFA 3, modèles french_mfa, processeur seul).

Quand le texte dit est connu, MFA pose chaque mot sur l'audio à ≈ 20 ms près (médiane) sans jamais en sauter
un ; Whisper, lui, en saute ou en étire (banc du 20/10/2026, 805/805 mots alignés en 48 s
pour 5 min 21 de voix, 0 recalage manuel contre 4 pour Whisper).

Usages (transcrire.py appelle ces fonctions ; la ligne de commande sert au diagnostic) :
    python aligner_mfa.py <capsule>                         # voix de synthèse : voix/<id>.wav + texte dit
    python aligner_mfa.py <capsule> --enregistrement <wav>  # enregistrement : affine data/transcript.json (texte
                                                            #   déjà transcrit par Whisper ou Parakeet)

Mode voix de synthèse : un fichier par temps fort (voix/<id>.wav) et son texte : « texte_reconnu » (bloc [prof]
d'une capsule mixte, texte réellement dit d'après la transcription de nettoyer_audio.py), sinon « texte_dit ».
Écrit data/transcript.json au format de transcrire.py (un segment par temps fort, mots du texte dit, temps
absolus), que aligner.py recolle ensuite sur les mots du script.
Mode enregistrement : l'audio est découpé aux silences entre segments (morceaux de 20 à 40 s), chaque morceau
est aligné sur les mots déjà transcrits ; seuls les temps changent (mots, ponctuation et index gardés).

Python : n'importe lequel (bibliothèque standard + ffmpeg) ; mfa.exe tourne dans son propre environnement.
Les nombres en chiffres (« 240 ») sont dits en mots pour MFA via num2words, pris dans un autre Python du
skill (python_parakeet, python_pocket ou python_tts) si celui-ci ne l'a pas.
Mots absents du dictionnaire : prononciation générée à la volée (--g2p_model_path french_mfa), jamais bloquant.

Pièges réglés ici (voir references/outils-audio.md) : DLL libsndfile introuvable si <env>, <env>/Scripts et
<env>/Library/bin ne sont pas dans le PATH du processus ; « unable to open database file » (sqlite) si TEMP
n'existe pas ; dossier de travail propre à chaque appel (deux capsules alignées en même temps ne se gênent pas),
supprimé à la fin.
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import wave

ICI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import commun  # noqa: E402

MODELE = "french_mfa"


# ------------------------------------------------------------------ installation
def config():
    """{"exe", "env", "modeles", "root"} si MFA est installé et ses modèles présents, sinon None."""
    c = commun.CONF.get("mfa") or {}
    env = c.get("env")
    if not env:
        return None
    exe = pathlib.Path(env) / ("Scripts" if sys.platform == "win32" else "bin") / ("mfa.exe" if sys.platform == "win32" else "mfa")
    modeles = pathlib.Path(c.get("modeles") or pathlib.Path(env).parent / "mfa-modeles")
    pm = modeles / "pretrained_models"
    if not exe.exists() or not (pm / "acoustic" / f"{MODELE}.zip").exists() \
            or not (pm / "dictionary" / f"{MODELE}.dict").exists():
        return None
    return {"exe": str(exe), "env": str(env), "modeles": str(modeles), "root": c.get("root"),
            "g2p": (pm / "g2p" / f"{MODELE}.zip").exists()}


def disponible():
    return config() is not None


def _environnement(cfg, tmp):
    env = pathlib.Path(cfg["env"])
    e = dict(os.environ, PYTHONIOENCODING="utf-8", MFA_ROOT_DIR=cfg["modeles"], TEMP=str(tmp), TMP=str(tmp), TMPDIR=str(tmp))
    if cfg.get("root"):
        e["MAMBA_ROOT_PREFIX"] = cfg["root"]
    for k in ("CONDA_PREFIX", "CONDA_DEFAULT_ENV", "PYTHONHOME", "PYTHONPATH", "VIRTUAL_ENV"):
        e.pop(k, None)
    garde = [p for p in e.get("PATH", "").split(os.pathsep) if "anaconda" not in p.lower() and "miniconda" not in p.lower()]
    dossiers = [str(env), str(env / "Scripts"), str(env / "Library" / "bin")] if sys.platform == "win32" else [str(env / "bin")]
    e["PATH"] = os.pathsep.join(dossiers + garde)
    return e


# ------------------------------------------------------------------ texte
def n(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", s)


def nettoyer_jeton(m):
    """Ponctuation de bord retirée ; apostrophes et tirets internes gardés (MFA connaît « l'exercice »)."""
    return re.sub(r"^[^\w]+|[^\w]+$", "", m.replace("’", "'"))


def vers_oral(textes):
    """Liste de textes → mêmes textes, nombres dits en mots (pour_l_oreille de voix.py, sans les rustines Piper)."""
    if not any(re.search(r"\d", t) for t in textes):
        return list(textes)
    if commun.module_present("num2words"):
        import voix  # noqa: PLC0415
        return [voix.pour_l_oreille(t, None, piper=False) if re.search(r"\d", t) else t for t in textes]
    for cle in ("python_parakeet", "python_pocket", "python_tts", "python_voix"):
        py = commun.CONF.get(cle)
        if py and os.path.exists(py) and os.path.abspath(py) != os.path.abspath(sys.executable):
            r = subprocess.run([py, "-X", "utf8", str(ICI / "aligner_mfa.py"), "--oral"], input=json.dumps(textes),
                               capture_output=True, text=True, encoding="utf-8",
                               env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1"))
            if r.returncode == 0:
                return json.loads(r.stdout.strip().splitlines()[-1])
    print("  num2words introuvable : nombres en chiffres laissés au g2p de MFA (horodatage moins sûr)")
    return list(textes)


def unites(mots):
    """Mots d'origine → unités pour MFA : [(indices d'origine, texte lab)]. « J » + « 'ajoute » (Whisper coupe
    l'élision) forment une seule unité « J'ajoute »."""
    res = []
    for i, m in enumerate(mots):
        brut = m.replace("’", "'").strip()
        if res and (brut.startswith("'") or res[-1][2].endswith("'")):
            idx, txt, b = res[-1]
            res[-1] = (idx + [i], txt + brut, b + brut)
        else:
            res.append(([i], brut, brut))
    oral = vers_oral([t for _, t, _ in res])
    sortie = []
    for (idx, _, _), o in zip(res, oral):
        lab = " ".join(x for x in (nettoyer_jeton(t) for t in o.split()) if x)
        sortie.append((idx, lab))
    return sortie


# ------------------------------------------------------------------ MFA
def _lire_sortie(chemin_json, chemin_tg):
    """Mots MFA [(debut, fin, mot, oov)] depuis la sortie json (ou TextGrid à défaut)."""
    if chemin_json.exists():
        d = json.loads(chemin_json.read_text(encoding="utf-8"))
        tiers = d.get("tiers", {})
        mots = [(float(a), float(b), c) for a, b, c in tiers.get("words", {}).get("entries", []) if str(c).strip()]
        phones = [(float(a), float(b), c) for a, b, c in tiers.get("phones", {}).get("entries", [])]
    elif chemin_tg.exists():
        txt = chemin_tg.read_text(encoding="utf-8")
        tiers = {}
        for t in re.split(r"item \[\d+\]:", txt)[1:]:
            nom = re.search(r'name = "([^"]*)"', t).group(1)
            tiers[nom] = [(float(a), float(b), c) for a, b, c in re.findall(
                r'xmin = ([\d.eE+-]+)\s*\n\s*xmax = ([\d.eE+-]+)\s*\n\s*text = "([^"]*)"', t)]
        mots = [x for x in tiers.get("words", []) if x[2].strip()]
        phones = tiers.get("phones", [])
    else:
        return None
    return [(a, b, c, any(p[2] == "spn" and p[0] >= a - 1e-6 and p[1] <= b + 1e-6 for p in phones)) for a, b, c in mots]


def aligner(paires, jobs=None, large=False):
    """paires : [{"id", "wav", "unites": [(indices, lab)]}] → ({id: {indice d'origine: (debut, fin, oov)}}, stats).
    Temps relatifs au fichier de chaque paire."""
    cfg = config()
    if not cfg:
        raise RuntimeError("MFA n'est pas installé (clé « mfa » de config.json, scripts/installer_mfa.py)")
    base = pathlib.Path(cfg["modeles"]).parent / "tmp-mfa"
    base.mkdir(parents=True, exist_ok=True)
    travail = pathlib.Path(tempfile.mkdtemp(prefix="aligne-", dir=str(base)))
    corpus, sortie, tmp = travail / "corpus", travail / "sortie", travail / "tmp"
    for d in (corpus, sortie, tmp):
        d.mkdir()
    stats = {"unites": 0, "alignees": 0, "oov": [], "non_recollees": [], "sans_sortie": [], "duree_mfa_s": 0.0}
    try:
        vides = set()
        for p in paires:
            lab = " ".join(u for _, u in p["unites"] if u)
            if not lab:
                vides.add(p["id"])
                continue
            shutil.copyfile(p["wav"], corpus / f"{p['id']}.wav")
            (corpus / f"{p['id']}.lab").write_text(lab + "\n", encoding="utf-8")
        jobs = jobs or max(1, min((os.cpu_count() or 4) // 2, len(paires) - len(vides), 6))
        cmd = [cfg["exe"], "align", str(corpus), MODELE, MODELE, str(sortie), "--clean", "--single_speaker",
               "--output_format", "json", "-t", str(tmp), "-j", str(jobs)]
        if cfg["g2p"]:
            cmd += ["--g2p_model_path", MODELE]
        if large:  # parole spontanée, texte reconnu imparfait : faisceau élargi (défauts MFA : 10 et 40)
            cmd += ["--beam", "100", "--retry_beam", "400"]
        t0 = time.time()
        r = subprocess.run(cmd, env=_environnement(cfg, tmp), capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=3600)
        stats["duree_mfa_s"] = round(time.time() - t0, 1)
        if r.returncode != 0:
            raise RuntimeError("mfa align a échoué :\n" + "\n".join((r.stdout + r.stderr).strip().splitlines()[-15:]))
        res = {}
        for p in paires:
            if p["id"] in vides:
                res[p["id"]] = {}
                continue
            mfa = _lire_sortie(sortie / f"{p['id']}.json", sortie / f"{p['id']}.TextGrid")
            if mfa is None:  # MFA renonce à un fichier dont le texte ne colle pas à l'audio (même avec retry_beam)
                stats["sans_sortie"].append(p["id"])
                res[p["id"]] = {}
                continue
            res[p["id"]] = recoller(p, mfa, stats)
        if len(stats["sans_sortie"]) == len(paires):
            raise RuntimeError("MFA n'a rien aligné :\n" + "\n".join((r.stdout + r.stderr).strip().splitlines()[-15:]))
        return res, stats
    finally:
        shutil.rmtree(travail, ignore_errors=True)


def recoller(p, mfa, stats):
    """Recolle les mots MFA (minuscules, parfois coupés au tiret) sur les unités, par accumulation de lettres.
    Un décalage (mot que MFA aurait écrit autrement) arrête le recollage de ce fichier : les mots restants
    gardent leurs anciens temps (ou sont interpolés par aligner.py)."""
    k, temps = 0, {}
    for idx, lab in p["unites"]:
        if not n(lab):
            continue
        stats["unites"] += 1
        cible, acc, grp = n(lab), "", []
        while k < len(mfa) and len(acc) < len(cible):
            acc += n(mfa[k][2])
            grp.append(mfa[k])
            k += 1
        if not grp or acc != cible:
            stats["non_recollees"].append(f"{p['id']}:{lab}")
            break
        oov = any(g[3] for g in grp)
        if oov:
            stats["oov"].append(lab)
        stats["alignees"] += 1
        d0, f0 = grp[0][0], grp[-1][1]
        if len(idx) == 1:
            temps[idx[0]] = (d0, f0, oov)
        else:  # élision recollée (« J'ajoute ») : partage au prorata des lettres
            longueurs = [max(1, len(n(x))) for x in p["origine"][idx[0]: idx[-1] + 1]] if "origine" in p else [1] * len(idx)
            tot, t = sum(longueurs), d0
            for i, L in zip(idx, longueurs):
                dt = (f0 - d0) * L / tot
                temps[i] = (t, t + dt, oov)
                t += dt
    return temps


# ------------------------------------------------------------------ sorties au format de transcrire.py
def _duree(chemin):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(chemin)],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def transcript_temps_forts(dossier, audio=None):
    """Voix de synthèse : MFA sur chaque voix/<id>.wav avec son texte ; écrit data/transcript.json. Renvoie stats."""
    d = pathlib.Path(dossier)
    tf = json.loads((d / "data" / "temps-forts.json").read_text(encoding="utf-8"))
    paires = []
    for b in tf:
        texte = b.get("texte_reconnu") or b.get("texte_dit") or b["texte"]
        origine = [m for m in texte.split() if nettoyer_jeton(m)]
        paires.append({"id": b["id"], "wav": str(d / "voix" / f"{b['id']}.wav"), "origine": origine,
                       "unites": unites(origine), "debut": b["debut"]})
        if b.get("voix") == "prof" and not b.get("texte_reconnu"):
            print(f"  {b['id']} [prof] sans texte reconnu : aligné sur le texte du script (vérifier ses ancres)")
    res, stats = aligner(paires)
    segments, mots = [], []
    for p in paires:
        ms = []
        for i, mot in enumerate(p["origine"]):
            t = res[p["id"]].get(i)
            if not t:
                continue
            m = {"i": len(mots), "mot": mot, "debut": round(t[0] + p["debut"], 3), "fin": round(t[1] + p["debut"], 3)}
            if t[2]:
                m["oov"] = True
            mots.append(m)
            ms.append(m)
        if ms:
            segments.append({"debut": ms[0]["debut"], "fin": ms[-1]["fin"], "texte": " ".join(x["mot"] for x in ms),
                             "mots": ms, "bloc": p["id"]})
    duree = _duree(audio or d / "audio.wav")
    ecrire(d, {"duree": round(duree, 3), "texte": " ".join(s["texte"] for s in segments), "segments": segments,
               "mots": mots, "horodatage": "mfa"})
    return stats


def decouper(mots, duree, cible=20.0, maxi=40.0):
    """Morceaux [(debut, fin, [indices])] coupés au milieu d'un silence entre deux mots (≥ 0,3 s après cible s,
    le plus grand silence disponible au-delà de maxi s)."""
    morceaux, courant, debut = [], [], 0.0
    for i, m in enumerate(mots):
        if courant:
            prec = mots[courant[-1]]
            ecart = m["debut"] - prec["fin"]
            long_ = m["debut"] - debut
            if (long_ >= cible and ecart >= 0.3) or ecart >= 1.5 or long_ >= maxi:
                if long_ >= maxi and ecart < 0.3:
                    # pas de silence : couper au plus grand écart de la seconde moitié du morceau (dans la première,
                    # on ne retirerait qu'un mot à la fois)
                    possibles = [q for q in range(1, len(courant)) if mots[courant[q]]["debut"] - debut >= cible / 2]
                    j = max(possibles, key=lambda q: (mots[courant[q]]["debut"] - mots[courant[q - 1]]["fin"], q),
                            default=None)
                    if j:
                        coupe = (mots[courant[j - 1]]["fin"] + mots[courant[j]]["debut"]) / 2
                        morceaux.append((debut, coupe, courant[:j]))
                        courant, debut = courant[j:], coupe
                        courant.append(i)
                        continue
                coupe = (prec["fin"] + m["debut"]) / 2
                morceaux.append((debut, coupe, courant))
                courant, debut = [], coupe
        courant.append(i)
    if courant:
        morceaux.append((debut, duree, courant))
    return morceaux


def affiner_enregistrement(dossier, wav16k):
    """Enregistrement transcrit (data/transcript.json) : temps des mots refaits par MFA sur le texte transcrit."""
    d = pathlib.Path(dossier)
    tr = json.loads((d / "data" / "transcript.json").read_text(encoding="utf-8"))
    mots = tr["mots"]
    if not mots:
        return {"unites": 0, "alignees": 0, "oov": [], "non_recollees": [], "sans_sortie": [], "duree_mfa_s": 0}
    with wave.open(str(wav16k), "rb") as w:
        sr, nch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth()
        brut = w.readframes(w.getnframes())
        duree = w.getnframes() / sr
    morceaux = decouper(mots, duree)
    travail = pathlib.Path(tempfile.mkdtemp(prefix="morceaux-", dir=str(d / "data")))
    try:
        paires = []
        for k, (a, b, idx) in enumerate(morceaux):
            f = travail / f"m{k:04d}.wav"
            with wave.open(str(f), "wb") as w:
                w.setnchannels(nch); w.setsampwidth(sw); w.setframerate(sr)
                w.writeframes(brut[int(a * sr) * nch * sw: int(b * sr) * nch * sw])
            origine = [mots[i]["mot"] for i in idx]
            paires.append({"id": f"m{k:04d}", "wav": str(f), "origine": origine, "unites": unites(origine),
                           "debut": a, "idx": idx})
        res, stats = aligner(paires, large=True)
    finally:
        shutil.rmtree(travail, ignore_errors=True)
    gardes = 0
    for p in paires:
        for j, i in enumerate(p["idx"]):
            t = res[p["id"]].get(j)
            if t:
                mots[i]["debut"], mots[i]["fin"] = round(t[0] + p["debut"], 3), round(t[1] + p["debut"], 3)
                if t[2]:
                    mots[i]["oov"] = True
            else:
                gardes += 1
                mots[i]["horodatage"] = "asr"
    stats["mots_temps_asr"] = gardes
    for s in tr["segments"]:
        if s.get("mots"):
            s["debut"], s["fin"] = s["mots"][0]["debut"], s["mots"][-1]["fin"]
    tr["horodatage"] = "mfa"
    ecrire(d, tr)
    return stats


def ts(t):
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def srt_ts(t):
    h, r = divmod(t, 3600)
    m, s = divmod(r, 60)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"


def ecrire(d, res):
    data = pathlib.Path(d) / "data"
    data.mkdir(exist_ok=True)
    (data / "transcript.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    (data / "transcript.js").write_text("window.TRANSCRIPT = " + json.dumps(res, ensure_ascii=False) + ";\n", encoding="utf-8")
    with open(data / "transcript.txt", "w", encoding="utf-8") as f:
        for s in res["segments"]:
            idx = f"#{s['mots'][0]['i']}-{s['mots'][-1]['i']}" if s["mots"] else ""
            f.write(f"[{ts(s['debut'])} → {ts(s['fin'])}] {idx} {s['texte']}\n")
    with open(data / "sous-titres.srt", "w", encoding="utf-8") as f:
        for k, s in enumerate(res["segments"], 1):
            f.write(f"{k}\n{srt_ts(s['debut'])} --> {srt_ts(s['fin'])}\n{s['texte']}\n\n")


def resume(stats):
    oov = len(stats["oov"])
    nr = stats["non_recollees"]
    return (f"MFA : {stats['alignees']}/{stats['unites']} mots posés en {stats['duree_mfa_s']:.0f} s"
            + (f", {oov} hors dictionnaire (prononciation générée)" if oov else "")
            + (f", recollage interrompu : {', '.join(nr[:5])}" if nr else "")
            + (f", fichiers non alignés (texte trop éloigné de l'audio) : {', '.join(stats['sans_sortie'])}"
               if stats.get("sans_sortie") else ""))


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--oral":
        print(json.dumps(vers_oral(json.loads(sys.stdin.read())), ensure_ascii=False))
        return
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capsule")
    ap.add_argument("--enregistrement", default=None, help="wav 16 kHz de l'enregistrement déjà transcrit")
    a = ap.parse_args()
    if not disponible():
        sys.exit("MFA n'est pas installé ou ses modèles manquent (clé « mfa » de config.json).")
    stats = affiner_enregistrement(a.capsule, a.enregistrement) if a.enregistrement else transcript_temps_forts(a.capsule)
    print(resume(stats))


if __name__ == "__main__":
    main()
