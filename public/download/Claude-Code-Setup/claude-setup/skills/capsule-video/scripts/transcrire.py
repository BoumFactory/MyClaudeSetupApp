"""Transcription horodatée au mot d'une capsule (local, gratuit, processeur suffisant).

Usage :
    python transcrire.py <audio> <dossier_capsule> [--vocab "mot1, mot2"] [--asr whisper|parakeet]
                         [--horodatage mfa|whisper] [--modele large-v3] [--cpu]

Deux cas :
  • Voix de synthèse (data/temps-forts.json existe : voix_pocket.py, voix.py, assembler_voix.py) : le texte dit
    est CONNU. Horodatage par MFA (alignement forcé, clé « horodatage » de config.json, défaut si installé) sur
    chaque voix/<id>.wav, sans aucune reconnaissance vocale ; à défaut, Whisper transcrit chaque temps fort avec
    son texte en indice (ancienne méthode, plus lente et moins précise). Puis aligner.py recolle les mots
    exacts du script sur ces horodatages.
  • Enregistrement du professeur (pas de temps-forts.json) : le texte est d'abord reconnu (clé
    « asr_enregistrements », option --asr : whisper par défaut, carte graphique si disponible sinon processeur ;
    parakeet en repli sur processeur, sans --vocab et moins bon sur le jargon), puis MFA refait les temps de
    chaque mot sur le texte reconnu.

Produit dans <dossier_capsule>/data/ :
    transcript.json  {"duree", "texte", "segments":[{debut,fin,texte,mots:[{i,mot,debut,fin}]}], "mots":[...],
                      "horodatage": "mfa" | absent (Whisper)}
    transcript.txt   une ligne par segment, préfixée [mm:ss.cc] et les index de mots
    transcript.js    window.TRANSCRIPT = {...}  (chargeable en file:// par la page)
    sous-titres.srt

Le script se relance seul avec le Python du moteur de reconnaissance (python_asr, python_parakeet) quand il
en faut un ; l'horodatage MFA seul n'en demande aucun.
"""
import argparse
import json
import os
import subprocess
import sys
import time

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import aligner_mfa  # noqa: E402
import commun  # noqa: E402  (cache des modèles sur le lecteur choisi)


def lire_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio")
    ap.add_argument("dossier")
    ap.add_argument("--vocab", default="", help="vocabulaire attendu, injecté en initial_prompt (Whisper seulement)")
    ap.add_argument("--modele", default=commun.CONF.get("modele_asr", "large-v3"))
    ap.add_argument("--langue", default="fr")
    ap.add_argument("--cpu", action="store_true", help="Whisper sur processeur même si une carte NVIDIA est là")
    ap.add_argument("--asr", choices=("whisper", "parakeet"), default=None,
                    help="reconnaissance d'un enregistrement (défaut : asr_enregistrements de config.json, whisper)")
    ap.add_argument("--horodatage", choices=("mfa", "whisper"), default=None,
                    help="défaut : horodatage de config.json (mfa), Whisper si MFA n'est pas installé")
    return ap.parse_args()


def ffprobe_duree(chemin):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", chemin],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def segments_whisper(segs, mots, segments, decalage=0.0):
    for s in segs:
        ms = []
        for w in s.words or []:
            m = {"i": len(mots), "mot": w.word.strip(),
                 "debut": round(w.start + decalage, 3), "fin": round(w.end + decalage, 3)}
            mots.append(m)
            ms.append(m)
        segments.append({"debut": round(s.start + decalage, 3), "fin": round(s.end + decalage, 3),
                         "texte": s.text.strip(), "mots": ms})
        print(f"[{aligner_mfa.ts(s.start + decalage)}] {s.text.strip()}")


def finir(a, res, t0, synthese):
    aligner_mfa.ecrire(a.dossier, res)
    print(f"\n{len(res['mots'])} mots, {len(res['segments'])} segments, {res['duree']:.1f} s d'audio, "
          f"traité en {time.time() - t0:.1f} s → {os.path.join(a.dossier, 'data')}")


def main():
    a = lire_args()
    synthese = os.path.exists(os.path.join(a.dossier, "data", "temps-forts.json"))
    horo = a.horodatage or commun.CONF.get("horodatage") or "mfa"
    if horo == "mfa" and not aligner_mfa.disponible():
        print("MFA non installé (clé « mfa » de config.json) : horodatage par Whisper")
        horo = "whisper"
    t0 = time.time()

    if synthese and horo == "mfa":
        # Voix de synthèse : texte connu, aucune reconnaissance vocale
        try:
            stats = aligner_mfa.transcript_temps_forts(a.dossier, a.audio)
        except RuntimeError as e:
            print(f"Échec de MFA ({e}) : repli sur Whisper")
            env = dict(os.environ, PYTHONIOENCODING="utf-8")
            sys.exit(subprocess.call([sys.executable, os.path.abspath(__file__)] + sys.argv[1:] + ["--horodatage", "whisper"],
                                     env=env))
        print(aligner_mfa.resume(stats))
        print(f"Horodatage MFA en {time.time() - t0:.1f} s")
        import aligner
        aligner.aligner(a.dossier)
        return

    asr = "whisper" if synthese else (a.asr or commun.CONF.get("asr_enregistrements") or "whisper")
    commun.relancer_pour(asr, os.path.abspath(__file__), sys.argv[1:])

    data = os.path.join(a.dossier, "data")
    os.makedirs(data, exist_ok=True)
    # Audio 16 kHz mono : entrée la plus fiable pour la reconnaissance et pour MFA
    wav = os.path.join(data, "audio-16k.wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", a.audio, "-ac", "1", "-ar", "16000", wav], check=True)
    segments, mots = [], []

    if asr == "parakeet":
        import asr_parakeet
        print("Reconnaissance Parakeet (repli) : pas de --vocab, jargon moins bien reconnu, « euh » et mots "
              "répétés effacés")
        model = asr_parakeet.charger()
        mp, segs = asr_parakeet.mots(model, wav)
        k = 0
        for d0, f0, texte in segs:
            ms = []
            while k < len(mp) and mp[k]["debut"] < f0 + 0.05:
                m = dict(mp[k], i=len(mots))
                mots.append(m)
                ms.append(m)
                k += 1
            segments.append({"debut": d0, "fin": f0, "texte": texte, "mots": ms})
            print(f"[{aligner_mfa.ts(d0)}] {texte}")
        duree = ffprobe_duree(a.audio)
    else:
        import asr_whisper
        model, _ = asr_whisper.charger(a.modele, cpu=a.cpu)
        if synthese:
            # Ancienne méthode (MFA absent) : un temps fort à la fois, son texte exact en indice
            for b in json.load(open(os.path.join(data, "temps-forts.json"), encoding="utf-8")):
                segs, _ = model.transcribe(
                    os.path.join(a.dossier, "voix", b["id"] + ".wav"), language=a.langue,
                    word_timestamps=True, vad_filter=False, initial_prompt=b["texte"],
                    beam_size=5, condition_on_previous_text=False)
                segments_whisper(segs, mots, segments, b["debut"])
            duree = ffprobe_duree(a.audio)
        else:
            segs, info = model.transcribe(
                wav, language=a.langue, word_timestamps=True, vad_filter=True,
                vad_parameters={"min_silence_duration_ms": 400},
                initial_prompt=a.vocab or None, beam_size=5, condition_on_previous_text=False)
            segments_whisper(segs, mots, segments)
            duree = info.duration

    res = {"duree": round(duree, 3), "texte": " ".join(s["texte"] for s in segments), "segments": segments, "mots": mots}
    finir(a, res, t0, synthese)
    if synthese:
        import aligner
        aligner.aligner(a.dossier)
    elif horo == "mfa":
        t1 = time.time()
        try:
            stats = aligner_mfa.affiner_enregistrement(a.dossier, wav)
            print(aligner_mfa.resume(stats) + f" ; {stats.get('mots_temps_asr', 0)} mot(s) gardent le temps de {asr} "
                  f"(horodatage affiné en {time.time() - t1:.1f} s)")
        except RuntimeError as e:
            print(f"MFA a échoué ({e}) : les temps de {asr} sont gardés")


if __name__ == "__main__":
    main()
