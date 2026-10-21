"""Chargement de Whisper (faster-whisper), partagé par transcrire.py, nettoyer_audio.py et controle_fidelite.py.

Le périphérique suit la clé « whisper_device » de config.json : auto (carte NVIDIA si elle répond, sinon
processeur), cuda (erreur si la carte manque) ou cpu. Sur processeur, large-v3 est très lent : medium est
pris à sa place, sauf modèle explicite.
À n'importer que dans le Python qui a faster-whisper (clé « python_asr »).
"""
import commun


def charger(modele="large-v3", cpu=False):
    """Renvoie (modèle chargé, "cuda" | "cpu")."""
    commun.dll_nvidia()
    import numpy as np
    from faster_whisper import WhisperModel as _WM

    def WhisperModel(nom, **kw):  # noqa: N802
        # cache local d'abord : sinon faster-whisper interroge Hugging Face à chaque chargement (≈ 30 s perdues
        # derrière un proxy qui casse le SSL, mesuré le 20/10/2026) ; en ligne seulement si le modèle manque
        try:
            return _WM(nom, local_files_only=True, **kw)
        except Exception:  # noqa: BLE001
            return _WM(nom, **kw)
    voulu = "cpu" if cpu else (commun.CONF.get("whisper_device") or "auto")
    if voulu in ("auto", "cuda"):
        try:
            m = WhisperModel(modele, device="cuda", compute_type="float16")
            # les erreurs de DLL CUDA n'apparaissent qu'au premier calcul : on le force sur 1 s de silence
            list(m.transcribe(np.zeros(16000, dtype="float32"), language="fr")[0])
            print(f"Whisper {modele} sur carte graphique", flush=True)
            return m, "cuda"
        except Exception as e:  # noqa: BLE001  (pas de carte NVIDIA, DLL absentes…)
            if voulu == "cuda":
                raise
            print(f"Carte graphique indisponible ({str(e)[:100]}) : repli processeur", flush=True)
    nom = modele if modele != "large-v3" else "medium"
    print(f"Whisper {nom} sur processeur (int8)", flush=True)
    return WhisperModel(nom, device="cpu", compute_type="int8"), "cpu"
