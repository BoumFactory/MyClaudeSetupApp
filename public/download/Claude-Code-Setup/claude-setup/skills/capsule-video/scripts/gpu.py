"""Rendu graphique de Chromium sur n'importe quel PC (Windows, Linux, macOS) : détection avec repli, ressources, mémoire.

Ordre d'essai (mode « auto »), sous Windows (Linux : Vulkan puis logiciel ; macOS : Metal puis logiciel) :
  1. vulkan   : ANGLE Vulkan + GPU haute performance (carte dédiée NVIDIA/AMD : le plus rapide) ;
  2. d3d11    : ANGLE Direct3D 11, sans forcer le GPU haute performance (puce Intel/AMD intégrée, pilotes anciens) ;
  3. logiciel : --disable-gpu (aucune carte utilisable) : ça marche, plus lentement, avec un avertissement.
Un mode est refusé si le lancement échoue ou si WebGL rapporte un moteur logiciel (SwiftShader…).
Mode « intel » : d3d11 sur la puce économe (--force_low_power_gpu), pour simuler un PC sans carte dédiée.

Chromium n'est lancé que par Playwright (profil temporaire) et fermé par browser.close().
Fichier identique dans capsule-video et capsule-video-html (les deux skills sont autonomes).
"""
import ctypes
import os
import sys

MODES = {
    "vulkan": ["--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=vulkan", "--force_high_performance_gpu",
               "--enable-gpu-rasterization"],
    "d3d11": ["--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=d3d11", "--enable-gpu-rasterization"],
    "intel": ["--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=d3d11", "--force_low_power_gpu",
              "--enable-gpu-rasterization"],
    # macOS : ANGLE Metal (non testé) ; Direct3D 11 n'existe que sous Windows
    "metal": ["--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=metal", "--enable-gpu-rasterization"],
    "logiciel": ["--disable-gpu"],
}


def ordre_auto():
    """Modes essayés dans l'ordre selon le système : Windows Vulkan > Direct3D 11 ; macOS Metal ; Linux Vulkan ; puis logiciel."""
    if sys.platform == "win32":
        return ["vulkan", "d3d11", "logiciel"]
    if sys.platform == "darwin":
        return ["metal", "logiciel"]
    return ["vulkan", "logiciel"]
LOGICIELS = ("swiftshader", "llvmpipe", "microsoft basic render", "warp", "software")
JS_CARTE = """(() => { const c = document.createElement('canvas').getContext('webgl');
  const d = c && c.getExtension('WEBGL_debug_renderer_info');
  return c ? (d ? c.getParameter(d.UNMASKED_RENDERER_WEBGL) : 'WebGL sans nom de carte') : 'pas de WebGL'; })()"""


def est_logiciel(carte):
    c = (carte or "").lower()
    return any(x in c for x in LOGICIELS) or c in ("pas de webgl", "")


async def carte_graphique(browser):
    page = await browser.new_page()
    try:
        return await page.evaluate(JS_CARTE)
    finally:
        await page.close()


async def lancer(p, mode="auto", base=(), afficher=print):
    """Lance Chromium dans le meilleur mode disponible ; renvoie (browser, mode, nom de la carte)."""
    ordre = ordre_auto() if mode == "auto" else [mode]
    notes = []
    for m in ordre:
        try:
            b = await p.chromium.launch(args=list(base) + MODES[m], timeout=60000)
        except Exception as e:  # noqa: BLE001  (pilote absent, GPU refusé…)
            notes.append(f"{m} : lancement impossible ({str(e).splitlines()[0][:120]})")
            continue
        carte = await carte_graphique(b)
        if m not in ("logiciel",) and est_logiciel(carte):
            notes.append(f"{m} : pas de carte utilisable ({carte})")
            await b.close()
            continue
        for n in notes:
            afficher("  rendu graphique — essai écarté : " + n)
        if m == "logiciel":
            afficher("ATTENTION : aucune carte graphique utilisable, rendu entièrement logiciel. Ça marche, "
                     "mais plus lentement (mesuré sur 12 cœurs : 1,4 fois le temps avec carte graphique pour le moteur "
                     "canvas, 4 fois pour le moteur HTML ; davantage sur un petit processeur).")
        return b, m, carte
    raise SystemExit("Chromium ne démarre dans aucun mode graphique :\n  " + "\n  ".join(notes))


def ressources():
    """(cœurs logiques, mémoire vive totale en Go, mémoire libre en Go)."""
    coeurs = os.cpu_count() or 2
    try:
        import psutil
        vm = psutil.virtual_memory()
        return coeurs, vm.total / 2 ** 30, vm.available / 2 ** 30
    except ImportError:
        pass
    if sys.platform == "win32":
        class MEM(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        m = MEM()
        m.dwLength = ctypes.sizeof(MEM)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            return coeurs, m.ullTotalPhys / 2 ** 30, m.ullAvailPhys / 2 ** 30
    return coeurs, 8.0, 4.0


class Memoire:
    """Mémoire de pointe de ce processus et de tous ses descendants (Chromium, ffmpeg) ; échantillonnée à la demande."""

    def __init__(self):
        try:
            import psutil
            self.moi = psutil.Process()
        except ImportError:
            self.moi = None
        self.pointe = 0.0

    def echantillon(self):
        if not self.moi:
            return
        total = 0
        try:
            for p in [self.moi] + self.moi.children(recursive=True):
                try:
                    total += p.memory_info().rss
                except Exception:  # noqa: BLE001  (processus terminé entre-temps)
                    pass
        except Exception:  # noqa: BLE001
            return
        self.pointe = max(self.pointe, total / 2 ** 30)

    def texte(self):
        return f"{self.pointe:.2f} Go" if self.moi else "non mesurée (psutil absent)"
