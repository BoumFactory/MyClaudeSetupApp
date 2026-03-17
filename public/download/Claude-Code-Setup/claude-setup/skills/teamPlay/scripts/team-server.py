#!/usr/bin/env python3
"""
Serveur HTTP custom pour le TeamPlay Dashboard.
Remplace SimpleHTTPServer pour supporter les endpoints API :
  - GET  /*              : fichiers statiques depuis .dev/
  - POST /api/feedback   : envoie un message a un agent (ecrit dans .dev/team-inbox-{agent}.txt)
  - GET  /api/inbox-status : retourne quels agents ont des messages en attente

Usage:
  python team-server.py [--port 8766]
"""
import json
import os
import sys
import urllib.parse
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEV_DIR = PROJECT_ROOT / ".dev"
DEFAULT_PORT = 8766


class TeamPlayHandler(SimpleHTTPRequestHandler):
    """Handler HTTP custom : sert les fichiers statiques + endpoints API."""

    def __init__(self, *args, **kwargs):
        # Servir les fichiers depuis .dev/
        super().__init__(*args, directory=str(DEV_DIR), **kwargs)

    def do_POST(self):
        """Gere les requetes POST."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/feedback":
            self._handle_feedback()
        else:
            self.send_error(404, "Endpoint non trouve")

    def do_GET(self):
        """Gere les requetes GET (statiques + API)."""
        parsed = urllib.parse.urlparse(self.path)

        if parsed.path == "/api/inbox-status":
            self._handle_inbox_status()
        else:
            # Servir les fichiers statiques normalement
            super().do_GET()

    def _handle_feedback(self):
        """POST /api/feedback - Recoit un message et l'ecrit dans le fichier inbox de l'agent."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._send_json(400, {"error": "Corps de requete vide"})
                return

            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))

            agent = data.get("agent", "").strip()
            message = data.get("message", "").strip()

            if not agent or not message:
                self._send_json(400, {"error": "Champs 'agent' et 'message' requis"})
                return

            # Securite : empecher l'injection de chemin
            if "/" in agent or "\\" in agent or ".." in agent:
                self._send_json(400, {"error": "Nom d'agent invalide"})
                return

            # Ecrire dans le fichier inbox
            inbox_file = DEV_DIR / f"team-inbox-{agent}.txt"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] {message}\n"

            with open(inbox_file, "a", encoding="utf-8") as f:
                f.write(line)

            self._send_json(200, {
                "status": "ok",
                "agent": agent,
                "message": message,
                "timestamp": timestamp
            })

        except json.JSONDecodeError:
            self._send_json(400, {"error": "JSON invalide"})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_inbox_status(self):
        """GET /api/inbox-status - Retourne quels agents ont des messages en attente."""
        try:
            status = {}
            for f in DEV_DIR.glob("team-inbox-*.txt"):
                agent_name = f.stem.replace("team-inbox-", "")
                # Verifier que le fichier n'est pas vide
                if f.stat().st_size > 0:
                    status[agent_name] = True

            self._send_json(200, status)
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _send_json(self, code, data):
        """Envoie une reponse JSON."""
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Gere les requetes CORS preflight."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Reduit la verbosete des logs (ignorer les requetes de polling)."""
        msg = format % args
        # Ne pas logger les requetes de polling frequentes
        if "team-live.json" in msg or "inbox-status" in msg:
            return
        sys.stderr.write(f"[TeamPlay] {msg}\n")


def main():
    port = DEFAULT_PORT

    # Parser --port
    for i, arg in enumerate(sys.argv):
        if arg == "--port" and i + 1 < len(sys.argv):
            port = int(sys.argv[i + 1])

    # Verifier que .dev/ existe
    if not DEV_DIR.exists():
        print(f"ERREUR: repertoire {DEV_DIR} introuvable")
        sys.exit(1)

    server = HTTPServer(("", port), TeamPlayHandler)
    print(f"TeamPlay server demarre sur http://localhost:{port}")
    print(f"Fichiers servis depuis: {DEV_DIR}")
    print(f"API endpoints:")
    print(f"  POST /api/feedback      - Envoyer un message a un agent")
    print(f"  GET  /api/inbox-status  - Statut des boites de reception")
    print()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServeur arrete.")
        server.server_close()


if __name__ == "__main__":
    main()
