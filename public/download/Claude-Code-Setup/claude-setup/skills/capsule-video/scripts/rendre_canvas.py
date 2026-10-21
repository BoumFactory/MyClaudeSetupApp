"""Rendu d'une capsule « moteur canvas » (spec.js) : Chromium dessine et encode en H.264 lui-même.

Usage :
    python rendre_canvas.py <dossier_capsule> [--qualite 540|envoi|projection] [--workers 0] [--gpu auto]
                            [--accel materiel|logiciel] [--debit 160] [--debut 0] [--fin X]
                            [--finition auto|aucune|x264]
                            [--allegees 370,220] [--fenetre] [--sortie fichier.mp4]

Chaîne : un petit serveur HTTP local (port libre) sert la capsule (/) et le moteur (/moteur-canvas/) ;
Chromium (Playwright, profil temporaire, carte graphique) ouvre moteur-canvas/rendu.html, qui prépare
la scène (MathJax → chemins, mise en page) puis répartit les images entre des workers. Chaque worker
dessine sur un OffscreenCanvas, encode en H.264 (WebCodecs) et renvoie les morceaux encodés au fil de
l'eau (POST /flux). Python écrit les flux, puis ffmpeg assemble vidéo et audio SANS réencoder la vidéo.

Chromium n'est lancé que par Playwright et fermé par browser.close() : aucune interaction avec le
Chrome de l'utilisateur, aucune fermeture par nom de processus.
"""
import argparse
import asyncio
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

import commun  # noqa: F401  (emplacement des navigateurs, avant playwright)
import gpu
from barre import Barre
from playwright.async_api import async_playwright

MOTEUR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "moteur-canvas"
# drapeaux communs ; ceux du rendu graphique (Vulkan, Direct3D 11 ou logiciel) sont choisis par gpu.lancer()
DRAPEAUX = ["--autoplay-policy=no-user-gesture-required"]


def workers_auto():
    """2 workers dès qu'il y a 4 cœurs et 2 Go libres, sinon 1. Mesuré le 09/10/2026 (540p, 2 min 05) : mémoire de
    pointe de tout le rendu (Python + Chromium + ffmpeg) 0,6 Go avec 2 workers, 0,5 Go avec 1 : sobre pour un PC de 4 Go."""
    coeurs, _, libre = gpu.ressources()
    return 2 if coeurs >= 4 and libre >= 2.0 else 1
# hauteur, débit vidéo par défaut (kb/s), débit audio, nom du fichier.
# Encodeur LOGICIEL par défaut (mesuré le 09/10/2026 sur 2 min 05) : plus rapide que le matériel (561 contre
# 467 images/s) et il respecte le débit visé ; le matériel (NVENC via Media Foundation) l'ignore (5,3 Mo
# pour une consigne de 120 kb/s). 540p à 220 kb/s : 4,6 Mo, dégradés aussi lisses que l'ancien x264.
# Capsule de captures d'écran (20/10/2026) : 220 kb/s en 540p laissait l'image floue plus d'une seconde après
# chaque zoom ; 500 kb/s corrigeait. Débits 720p et 1080p relevés d'autant (proportionnels aux pixels).
QUALITES = {"540": (540, 500, "80k", "capsule-540p.mp4"),
            "envoi": (720, 900, "96k", "capsule-envoi.mp4"),
            "projection": (1080, 2000, "160k", "capsule.mp4")}
TYPES = {".js": "text/javascript", ".woff2": "font/woff2", ".html": "text/html", ".json": "application/json",
         ".wav": "audio/wav", ".mp3": "audio/mpeg", ".m4a": "audio/mp4", ".png": "image/png", ".jpg": "image/jpeg",
         ".svg": "image/svg+xml", ".css": "text/css"}


class Serveur:
    """Serveur HTTP local : / → dossier de la capsule ; /moteur-canvas/ → copie locale du moteur, sinon celui du skill."""

    def __init__(self, capsule):
        self.capsule = capsule
        local = capsule / "moteur-canvas"
        self.moteur = local if (local / "rendu.html").exists() else MOTEUR
        self.flux = {}
        self.images = capsule / "planches"
        srv = self

        class Gestion(SimpleHTTPRequestHandler):
            extensions_map = TYPES

            def translate_path(self, path):
                p = unquote(urlparse(path).path)
                if p.startswith("/moteur-canvas/"):
                    return str(srv.moteur / p[len("/moteur-canvas/"):])
                return str(srv.capsule / p.lstrip("/"))

            def do_POST(self):
                u = urlparse(self.path)
                q = parse_qs(u.query)
                donnees = self.rfile.read(int(self.headers["Content-Length"]))
                if u.path == "/image":   # mode --images : une PNG par instant
                    srv.images.mkdir(parents=True, exist_ok=True)
                    (srv.images / f"canvas-{float(q['t'][0]):07.2f}.png").write_bytes(donnees)
                else:
                    srv.flux.setdefault(int(q["tranche"][0]), {})[int(q["n"][0])] = donnees
                self.send_response(200)
                self.send_header("Content-Length", "0")
                self.end_headers()

            def end_headers(self):
                self.send_header("Cache-Control", "no-store")
                super().end_headers()

            def log_message(self, *a):
                pass

        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), Gestion)
        self.port = self.httpd.server_address[1]
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def fermer(self):
        self.httpd.shutdown()
        self.httpd.server_close()


def utilise_trois(dossier):
    """Vrai si la capsule charge le plugin trois (three.js) dans son spec.js."""
    texte = (dossier / "spec.js").read_text(encoding="utf-8")
    return bool(re.search(r"three\.min\.js|plugins-canvas/trois|C\.trois\s*\(", texte))


def finition_x264(brut, sortie, debit_k):
    """Deux passes x264 fast/animation au débit vidéo visé, audio copié ; journaux de passe dans le dossier de sortie."""
    journaux = sortie.with_name("ffmpeg2pass-" + sortie.stem)
    base = ["ffmpeg", "-y", "-v", "error", "-i", str(brut), "-c:v", "libx264", "-preset", "fast", "-tune", "animation",
            "-b:v", f"{debit_k}k", "-pix_fmt", "yuv420p", "-passlogfile", str(journaux)]
    try:
        subprocess.run(base + ["-pass", "1", "-an", "-f", "null", os.devnull], check=True, timeout=1800)
        subprocess.run(base + ["-pass", "2", "-c:a", "copy", "-movflags", "+faststart", str(sortie)], check=True, timeout=1800)
    finally:
        for f in sortie.parent.glob(journaux.name + "*"):
            f.unlink(missing_ok=True)


async def rendre(a):
    t0 = time.time()
    dossier = pathlib.Path(a.dossier).resolve()
    if not (dossier / "spec.js").exists():
        sys.exit(f"spec.js introuvable dans {dossier}")
    trois = utilise_trois(dossier)
    if a.qualite is None:
        a.qualite = "envoi" if trois else (commun.CONF.get("qualite_rendu") if commun.CONF.get("qualite_rendu") in QUALITES else "540")
    finition = a.finition == "x264" or (a.finition == "auto" and trois)
    hauteur, debit_def, debit_audio, nom = QUALITES[a.qualite]
    debit_final = a.debit or debit_def
    debit_rendu = round(6000 * (hauteur / 720) ** 2) if finition else debit_final
    if not a.workers:
        a.workers = workers_auto()
    serveur = Serveur(dossier)
    memoire = gpu.Memoire()
    params = {"hauteur": hauteur, "fps": a.fps, "workers": a.workers, "debit": debit_rendu * 1000,
              "accel": "prefer-software" if a.accel == "logiciel" else "prefer-hardware", "gop": a.gop}
    if a.debut:
        params["debut"] = a.debut
    if a.fin:
        params["fin"] = a.fin
    if a.images:
        params["images"] = a.images
    url = f"http://127.0.0.1:{serveur.port}/moteur-canvas/rendu.html?" + "&".join(f"{k}={v}" for k, v in params.items())
    console = []
    # l'audio s'encode en AAC PENDANT le rendu (l'assemblage final n'est plus qu'une copie)
    m = re.search(r"""audio\s*:\s*['"]([^'"]+)['"]""", (dossier / "spec.js").read_text(encoding="utf-8"))
    audio = dossier / (m.group(1) if m else "audio.wav")
    sortie = pathlib.Path(a.sortie) if a.sortie else dossier / nom
    aac = sortie.with_suffix(".audio.m4a")
    proc_audio = None
    if audio.exists() and not a.images:
        coupe = (["-ss", f"{a.debut:.3f}"] if a.debut else []) + (["-to", f"{a.fin:.3f}"] if a.fin else [])
        proc_audio = subprocess.Popen(["ffmpeg", "-y", "-v", "error", *coupe, "-i", str(audio), "-vn", "-c:a", "aac",
                                       "-b:a", debit_audio, str(aac)])
    try:
        async with async_playwright() as p:
            browser, mode_gpu, carte = await gpu.lancer(p, a.gpu, DRAPEAUX)
            t_lance = time.time()
            if not a.images:
                print(f"Rendu graphique : {mode_gpu} — {carte} ; {a.workers} worker(s)")
            try:
                page = await browser.new_page()
                page.on("console", lambda m: console.append(m.text) if m.type in ("error", "warning") else None)
                page.on("pageerror", lambda e: console.append(str(e)))
                await page.goto(url)
                barre = None
                while True:
                    etat = await page.evaluate("window.etat || null")
                    if etat and etat.get("total") and barre is None:
                        barre = Barre(f"Rendu canvas « {etat.get('titre') or dossier.name} » — {hauteur}p, "
                                      f"{a.workers} workers", etat["total"])
                    if barre and etat:
                        barre.maj(etat["faites"])
                    memoire.echantillon()
                    if etat and etat.get("fini"):
                        break
                    if time.time() - t0 > a.delai:
                        raise SystemExit(f"Délai dépassé ({a.delai} s) : rendu interrompu")
                    await asyncio.sleep(0.25)
            finally:
                await browser.close()
    finally:
        serveur.fermer()
    if etat.get("erreurs"):
        raise SystemExit("Erreurs dans la capsule :\n" + "\n".join(etat["erreurs"] + console[:10]))
    for r in etat.get("rapport", []):
        print("  mise en page :", r)
    if a.images:
        print(f"Images fixes écrites dans {serveur.images} ({time.time() - t0:.1f} s)")
        return None

    # flux H.264 (Annex B) : les tranches commencent toutes par une image clé, on les met bout à bout
    brut = sortie.with_suffix(".h264")
    with open(brut, "wb") as f:
        for i in sorted(serveur.flux):
            for n in sorted(serveur.flux[i]):
                f.write(serveur.flux[i][n])
    debut = a.debut or 0.0
    fin = min(a.fin, etat["duree"]) if a.fin else etat["duree"]
    t_ff = time.time()
    cmd = ["ffmpeg", "-y", "-v", "error", "-fflags", "+genpts", "-r", str(a.fps), "-f", "h264", "-i", str(brut)]
    if proc_audio and proc_audio.wait(timeout=300) == 0:
        cmd += ["-i", str(aac), "-map", "0:v", "-map", "1:a", "-c:a", "copy", "-t", f"{fin - debut:.3f}"]
    else:
        print(f"ATTENTION : audio introuvable ou illisible ({audio}), vidéo muette")
    inter = sortie.with_name(sortie.stem + "-intermediaire-haut-debit.mp4") if finition else sortie
    cmd += ["-c:v", "copy", "-movflags", "+faststart", str(inter)]
    t_fin = 0.0
    try:
        subprocess.run(cmd, check=True, timeout=300)
        if finition:
            t_x = time.time()
            finition_x264(inter, sortie, debit_final)
            t_fin = time.time() - t_x
    finally:
        brut.unlink(missing_ok=True)
        aac.unlink(missing_ok=True)
        if finition:
            inter.unlink(missing_ok=True)
    t_total = time.time() - t0

    w = [x for x in etat.get("workers", []) if x]
    n = etat["total"]
    print(f"OK {sortie} ({sortie.stat().st_size / 1e6:.2f} Mo) — {n} images, {fin - debut:.1f} s de vidéo")
    print(f"  total {t_total:.1f} s ({n / t_total:.0f} images/s de bout en bout) ; "
          f"rendu pur {etat['temps'].get('rendu', 0) / 1000:.1f} s ({n / max(0.001, etat['temps'].get('rendu', 1) / 1000):.0f} images/s cumulées)")
    print(f"  détail : lancement Chromium {t_lance - t0:.1f} s · préparation page (MathJax, polices, mise en page) "
          f"{etat['temps'].get('prep_page', 0) / 1000:.1f} s · rendu {etat['temps'].get('rendu', 0) / 1000:.1f} s · "
          f"assemblage ffmpeg {time.time() - t_ff - t_fin:.1f} s")
    if finition:
        print(f"  finition x264 : {t_fin:.0f} s (rendu intermédiaire à {debit_rendu} kb/s, sortie à {debit_final} kb/s)")
    for i, x in enumerate(w):
        print(f"  worker {i} : {x['images']} images, {x['accel']} {x['codec']} {x['debit'] // 1000} kb/s — prépa {x['t_prep']} ms, "
              f"dessin {x['t_dessin']} ms, VideoFrame+encode {x['t_image']} ms, attente encodeur {x['t_attente_encodeur']} ms, "
              f"vidage {x['t_vidage']} ms")
    print(f"  rendu graphique : {mode_gpu} ({carte}) ; mémoire de pointe (Python + Chromium + ffmpeg) : {memoire.texte()}")
    if a.json:
        pathlib.Path(a.json).write_text(json.dumps({"total_s": t_total, "lancement_s": t_lance - t0, "etat": etat,
                                                    "mode_gpu": mode_gpu, "carte": carte, "memoire_go": memoire.pointe,
                                                    "taille_octets": sortie.stat().st_size}, ensure_ascii=False, indent=1),
                                        encoding="utf-8")
    return sortie


REGLAGES_ALLEGES = {370: (28, 64), 360: (28, 64), 240: (30, 48), 220: (30, 48)}


def reduire(mp4, hauteur, crf, audio_k, sortie):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp4), "-vf", f"scale=-2:{hauteur}:flags=lanczos",
                    "-c:v", "libx264", "-preset", "slow", "-crf", str(crf), "-tune", "animation", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", f"{audio_k}k", "-movflags", "+faststart", str(sortie)], check=True, timeout=900)
    print(f"Version allégée {hauteur}p : {sortie} ({sortie.stat().st_size / 1e6:.1f} Mo)")


def relancer_en_fenetre():
    args = [x for x in sys.argv[1:] if x != "--fenetre"] + ["--pause-fin"]
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.Popen([sys.executable, str(pathlib.Path(__file__).resolve())] + args,
                            creationflags=subprocess.CREATE_NEW_CONSOLE, env=env)
    sys.exit(proc.wait())


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Rendu d'une capsule spec.js par le moteur canvas (WebCodecs).")
    ap.add_argument("dossier")
    ap.add_argument("--qualite", choices=list(QUALITES), default=None,
                    help="défaut : envoi (720p) pour une capsule 3D, sinon qualite_rendu de la config (envoi)")
    ap.add_argument("--finition", choices=["auto", "aucune", "x264"], default="auto",
                    help="x264 = rendu intermédiaire à haut débit puis deux passes x264 fast ; auto = x264 si la capsule utilise le plugin trois")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--workers", type=int, default=0, help="0 = selon la machine (2 si 4 cœurs et 2 Go libres, sinon 1)")
    ap.add_argument("--gpu", choices=["auto", "vulkan", "d3d11", "intel", "metal", "logiciel"], default="auto",
                    help="rendu graphique : auto = Vulkan, puis Direct3D 11, puis logiciel (Linux : Vulkan puis logiciel ; "
                         "macOS : Metal puis logiciel) ; intel = puce intégrée (essai, Windows)")
    ap.add_argument("--accel", choices=["materiel", "logiciel"], default="logiciel",
                    help="encodeur H.264 de Chromium : matériel (carte graphique) ou logiciel ; repli automatique")
    ap.add_argument("--debit", type=int, default=0, help="débit vidéo visé en kb/s (défaut selon la qualité)")
    ap.add_argument("--gop", type=float, default=10, help="secondes entre deux images clés")
    ap.add_argument("--debut", type=float, default=0.0)
    ap.add_argument("--fin", type=float, default=None)
    ap.add_argument("--sortie", default=None)
    ap.add_argument("--allegees", default=",".join(str(h) for h in commun.CONF.get("versions_allegees", [])))
    ap.add_argument("--delai", type=float, default=900, help="durée maximale du rendu en secondes")
    ap.add_argument("--json", default=None, help="écrit les mesures dans ce fichier")
    ap.add_argument("--images", default=None, help="instants (s) séparés par des virgules : PNG dans planches/, sans vidéo")
    ap.add_argument("--fenetre", action="store_true", help="Windows : rendu dans une console visible")
    ap.add_argument("--pause-fin", action="store_true", help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.fenetre and sys.platform == "win32":
        relancer_en_fenetre()
    code = 0
    try:
        principale = asyncio.run(rendre(args))
        for h in [] if principale is None else sorted({int(x) for x in args.allegees.split(",") if x.strip()}, reverse=True):
            crf, ak = REGLAGES_ALLEGES.get(h, (28, 64))
            reduire(principale, h, crf, ak, principale.with_name(f"capsule-{h}p.mp4"))
    except BaseException:  # noqa: BLE001
        code = 1
        if not args.pause_fin:
            raise
        import traceback
        traceback.print_exc()
    if args.pause_fin:
        print(("\nTerminé !" if code == 0 else "\nÉCHEC du rendu (voir ci-dessus).") + " Fermeture de la fenêtre dans 60 s.")
        time.sleep(60)
    sys.exit(code)
