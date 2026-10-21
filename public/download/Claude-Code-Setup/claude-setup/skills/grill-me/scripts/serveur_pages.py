#!/usr/bin/env python
"""Petit serveur HTTP local pour les pages grill-me.

Sert uniquement %TEMP%/grill-me-pages/, lié à 127.0.0.1, sur un port fixe
(47821, surchargeable par GRILL_ME_PORT) afin que l'autorisation du micro
soit mémorisée par le navigateur. S'arrête seul après 3 h sans requête.
"""
import os
import sys
import tempfile
import threading
import time
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT = int(os.environ.get("GRILL_ME_PORT", "47821"))
DOSSIER = Path(tempfile.gettempdir()) / "grill-me-pages"
INACTIVITE_MAX = 3 * 3600

derniere_requete = time.time()


class Gestionnaire(SimpleHTTPRequestHandler):
    def _toucher(self):
        global derniere_requete
        derniere_requete = time.time()

    def do_GET(self):
        self._toucher()
        if self.path.split("?", 1)[0] == "/__ping":
            corps = b"grill-me"
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        super().do_GET()

    def do_HEAD(self):
        self._toucher()
        super().do_HEAD()

    def list_directory(self, path):
        self.send_error(404, "Not found")
        return None

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args):
        pass


def surveiller(serveur):
    while True:
        time.sleep(30)
        if time.time() - derniere_requete > INACTIVITE_MAX:
            serveur.shutdown()
            return


def main():
    DOSSIER.mkdir(parents=True, exist_ok=True)
    try:
        serveur = ThreadingHTTPServer(("127.0.0.1", PORT), partial(Gestionnaire, directory=str(DOSSIER)))
    except OSError as e:
        print(f"Port {PORT} indisponible : {e}", file=sys.stderr)
        return 1
    serveur.daemon_threads = True
    threading.Thread(target=surveiller, args=(serveur,), daemon=True).start()
    try:
        serveur.serve_forever()
    finally:
        serveur.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
