"""Reconnaissance vocale Parakeet TDT 0.6B v3 (ONNX int8, onnx-asr) sur processeur : ni CUDA, ni PyTorch.

Sert au contrôle de fidélité des voix de synthèse (controle_fidelite.py) et, en repli explicite, à la
transcription d'un enregistrement (transcrire.py / nettoyer_audio.py --asr parakeet).
À n'importer que dans le Python de la clé « python_parakeet » de config.json (onnx-asr, soundfile, num2words).

Pièges (banc du 20/10/2026) :
- un appel de plus de ≈ 6 min plante (erreur ONNX de longueur d'attention) : au-delà de LIMITE_S, découpage
  aux silences par le VAD Silero fourni avec onnx-asr ;
- pas de vocabulaire à injecter (pas d'équivalent à --vocab) ; les « euh » et les mots répétés à la suite
  (« mais mais ») sont effacés ;
- horodatage par pas de 80 ms : à affiner par MFA (aligner_mfa.py) ;
- modèle de 640 Mo téléchargé au premier chargement dans HF_HOME (cache_modeles), 3,5 s à chaud.
"""
import os
import wave

import commun  # noqa: F401  (HF_HOME = cache des modèles)

MODELE = "nemo-parakeet-tdt-0.6b-v3"
LIMITE_S = 300.0
os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


def charger():
    import onnx_asr
    print("Parakeet TDT 0.6B v3 (ONNX int8) sur processeur", flush=True)
    return onnx_asr.load_model(MODELE, quantization="int8", providers=["CPUExecutionProvider"])


def duree(chemin):
    try:
        with wave.open(str(chemin), "rb") as w:
            return w.getnframes() / w.getframerate()
    except (wave.Error, EOFError):
        return 0.0


def _lire_16k(chemin):
    """Tableau float32 mono 16 kHz (le VAD l'exige) ; ffmpeg si le fichier n'est pas déjà à 16 kHz."""
    import subprocess
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(chemin), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, dtype="float32")


def texte(model, chemin):
    """Texte reconnu d'un fichier (temps fort court : un seul appel ; long : découpé par le VAD)."""
    if duree(chemin) <= LIMITE_S:
        r = model.recognize(str(chemin))
        return (r if isinstance(r, str) else getattr(r, "text", str(r))).strip()
    mots_, _ = mots(model, chemin)
    return " ".join(m["mot"] for m in mots_)


def mots(model, chemin):
    """Mots horodatés {mot, debut, fin} et segments [(debut, fin, texte)] d'un enregistrement de toute longueur."""
    import onnx_asr
    x = _lire_16k(chemin)
    vad = onnx_asr.load_vad("silero", providers=["CPUExecutionProvider"])
    m = model.with_vad(vad, max_speech_duration_s=20, min_silence_duration_ms=300).with_timestamps()
    res, segments = [], []
    for seg in m.recognize(x, sample_rate=16000):
        cur = None
        for tok, ts in zip(seg.tokens, seg.timestamps):
            t = round(float(ts) + seg.start, 3)
            if tok.startswith(" ") or cur is None:  # un jeton qui commence par une espace ouvre un mot
                if cur and cur["mot"].strip():
                    res.append(cur)
                cur = {"mot": tok.strip(), "debut": t, "fin": round(t + 0.08, 3)}
            else:
                cur["mot"] += tok
                cur["fin"] = round(t + 0.08, 3)
        if cur and cur["mot"].strip():
            res.append(cur)
        segments.append((round(seg.start, 3), round(seg.end, 3), seg.text.strip()))
    return res, segments
