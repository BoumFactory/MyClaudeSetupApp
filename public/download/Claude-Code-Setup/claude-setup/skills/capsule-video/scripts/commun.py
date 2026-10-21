"""Réglages communs aux scripts du skill : lecture de config.json et emplacements des caches.

À importer AVANT playwright, faster_whisper, torch… : les variables d'environnement
(HF_HOME, PLAYWRIGHT_BROWSERS_PATH) décident où sont lus les modèles et les navigateurs.
L'installeur (installation/installer.ps1) remplit config.json ; tout est sur le lecteur choisi.
"""
import json
import os
import pathlib
import sys

ICI = pathlib.Path(__file__).resolve().parent
# config.json facultatif (collègue sans installeur, fichier incomplet) : {} plutôt qu'un plantage à l'import.
# Une clé indispensable se lit par conf_requise(), qui explique quoi faire.
_FICHIER_CONF = ICI.parent / "config.json"
try:
    CONF = json.loads(_FICHIER_CONF.read_text(encoding="utf-8")) if _FICHIER_CONF.exists() else {}
except json.JSONDecodeError as e:
    sys.exit(f"config.json illisible ({e}) : corriger le fichier ou relancer installation/installer.ps1.")

# caches : seulement si le dossier existe (sinon on laisse les emplacements par défaut)
if CONF.get("cache_modeles") and os.path.isdir(CONF["cache_modeles"]):
    os.environ.setdefault("HF_HOME", CONF["cache_modeles"])
if CONF.get("navigateurs") and os.path.isdir(CONF["navigateurs"]):
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", CONF["navigateurs"])


def conf_requise(cle, usage=""):
    """Valeur d'une clé indispensable de config.json, ou arrêt avec un message clair (pas de KeyError)."""
    v = CONF.get(cle)
    if v in (None, ""):
        sys.exit(f"Clé « {cle} » absente de config.json{' (' + usage + ')' if usage else ''} : "
                 f"lancer installation/installer.ps1 ou renseigner la clé à la main.")
    return v
# ffmpeg portable installé par l'installeur (<base>/outils/ffmpeg/bin) : ajouté au PATH du seul processus
if CONF.get("dossier_ffmpeg") and os.path.isdir(CONF["dossier_ffmpeg"]):
    os.environ["PATH"] = CONF["dossier_ffmpeg"] + os.pathsep + os.environ.get("PATH", "")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


PYTHON_DE = {"whisper": "python_asr", "parakeet": "python_parakeet", "pocket": "python_pocket"}
MODULE_DE = {"whisper": "faster_whisper", "parakeet": "onnx_asr", "pocket": "pocket_tts"}


def python_de(moteur):
    """Chemin du Python d'un moteur (« whisper », « parakeet », « pocket ») s'il existe, sinon None."""
    py = CONF.get(PYTHON_DE[moteur])
    return py if py and os.path.exists(py) else None


def module_present(nom):
    import importlib.util
    return importlib.util.find_spec(nom) is not None


def relancer_pour(moteur, script, args):
    """Si le module du moteur manque dans l'interpréteur courant, relance script avec le Python du moteur
    (UTF-8) et termine ; sinon ne fait rien."""
    import subprocess
    if module_present(MODULE_DE[moteur]):
        return
    py = python_de(moteur)
    if not py or os.path.abspath(py) == os.path.abspath(sys.executable):
        sys.exit(f"{MODULE_DE[moteur]} introuvable : renseigner la clé {PYTHON_DE[moteur]} de config.json "
                 f"(voir references/outils-audio.md).")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    sys.exit(subprocess.call([py, "-X", "utf8", str(script)] + list(args), env=env))


def dll_nvidia():
    """Rend visibles les DLL CUDA installées par pip (nvidia-cublas-cu12, nvidia-cudnn-cu12)."""
    if sys.platform != "win32":
        # Linux : bibliothèques .so de pip (nvidia/*/lib), chargées à l'avance (LD_LIBRARY_PATH est lu trop tard)
        import ctypes
        import glob
        for so in sorted(glob.glob(os.path.join(sys.prefix, "lib", "python3*", "site-packages", "nvidia", "*", "lib", "lib*.so*"))):
            try:
                ctypes.CDLL(so, mode=ctypes.RTLD_GLOBAL)
            except OSError:
                pass
        return
    base = pathlib.Path(sys.prefix) / "Lib" / "site-packages" / "nvidia"
    if not base.exists():
        return
    for bin_ in base.glob("*/bin"):
        try:
            os.add_dll_directory(str(bin_))
        except (AttributeError, OSError):
            pass
        os.environ["PATH"] = str(bin_) + os.pathsep + os.environ.get("PATH", "")
