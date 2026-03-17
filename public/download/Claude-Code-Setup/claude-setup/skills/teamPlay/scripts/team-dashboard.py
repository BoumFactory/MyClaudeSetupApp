#!/usr/bin/env python3
"""
Dashboard TeamPlay pour QF-Studio.
Gere le dashboard team sur le meme serveur HTTP port 8766.

Usage:
  team-dashboard.py init "Nom de la team" [--agents frontend,backend,settings,tests,reviewer]
  team-dashboard.py stop
  team-dashboard.py status
"""
import json
import sys
import os
import subprocess
import socket
import shutil
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEV_DIR = PROJECT_ROOT / ".dev"
TEAM_JSON = DEV_DIR / "team-live.json"
TEAM_HTML_SRC = DEV_DIR / "team-live.html"
PORT = 8766

DEFAULT_AGENTS = ["frontend", "backend", "settings", "tests", "reviewer"]


def load():
    if not TEAM_JSON.exists():
        return None
    with open(TEAM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(TEAM_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _start_server():
    """Lance le serveur HTTP custom en background si pas deja actif."""
    if _is_port_in_use(PORT):
        print(f"Serveur deja actif sur port {PORT}")
        return

    # Utiliser team-server.py (serveur custom avec support API)
    server_script = SCRIPT_DIR / "team-server.py"

    if sys.platform == "win32":
        subprocess.Popen(
            [sys.executable, str(server_script), "--port", str(PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW,
        )
    else:
        subprocess.Popen(
            [sys.executable, str(server_script), "--port", str(PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

    import time
    for _ in range(20):
        time.sleep(0.25)
        if _is_port_in_use(PORT):
            print(f"Serveur HTTP demarre sur port {PORT}")
            return
    print("WARN: serveur pas demarre apres 5s")


def cmd_init(args):
    """Initialise le dashboard team."""
    team_name = args[0] if args else "TeamPlay"

    # Parser --agents
    agents = DEFAULT_AGENTS[:]
    for i, arg in enumerate(args):
        if arg == "--agents" and i + 1 < len(args):
            agents = [a.strip() for a in args[i + 1].split(",") if a.strip()]
            break

    data = {
        "mode": "team",
        "team_name": team_name,
        "title": f"TeamPlay - {team_name}",
        "started": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "agents": {},
        "conflicts": [],
        "global_log": [],
    }

    for agent in agents:
        data["agents"][agent] = {
            "status": "idle",
            "tasks": [],
            "log": [],
            "files_modified": [],
        }

    save(data)

    # Copier le template HTML
    html_template = SCRIPT_DIR.parent / "templates" / "team-live.html"
    if html_template.exists():
        shutil.copy2(html_template, TEAM_HTML_SRC)
    # Sinon le HTML est deja dans .dev/ (cree manuellement)

    # Lancer le serveur HTTP
    _start_server()

    url = f"http://localhost:{PORT}/team-live.html"
    print(f"Team dashboard initialise: {url}")
    print(f"Agents: {', '.join(agents)}")

    # Ouvrir dans le navigateur
    if sys.platform == "win32":
        os.system(f'start "" "{url}"')
    elif sys.platform == "darwin":
        os.system(f'open "{url}"')
    else:
        os.system(f'xdg-open "{url}" 2>/dev/null &')


def cmd_stop(args):
    """Arrete la session team (marque comme terminee)."""
    data = load()
    if not data:
        print("Pas de session team active")
        return

    data["stopped"] = datetime.now().isoformat()
    data["global_log"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": "Session team arretee",
    })
    save(data)
    print("Session team arretee")


def cmd_status(args):
    """Affiche le statut de la session team."""
    data = load()
    if not data:
        print("Pas de session team active")
        return

    print(f"Team: {data['team_name']}")
    print(f"Demarre: {data['started']}")
    print()

    total_tasks = 0
    done_tasks = 0

    for name, agent in data["agents"].items():
        tasks = agent["tasks"]
        total = len(tasks)
        done = sum(1 for t in tasks if t["status"] == "done")
        active = sum(1 for t in tasks if t["status"] == "working")
        total_tasks += total
        done_tasks += done

        status_icon = {
            "idle": " ",
            "working": "~",
            "done": "v",
            "error": "x",
        }.get(agent["status"], "?")

        print(f"  [{status_icon}] {name}: {done}/{total} taches ({active} en cours)")
        for t in tasks:
            t_icon = {
                "pending": " ",
                "working": "~",
                "done": "v",
                "error": "x",
            }.get(t["status"], "?")
            print(f"      [{t_icon}] {t['id']}: {t['label'][:60]}")

    pct = int(done_tasks / total_tasks * 100) if total_tasks else 0
    print(f"\nProgression globale: {done_tasks}/{total_tasks} ({pct}%)")

    open_conflicts = sum(1 for c in data.get("conflicts", []) if c["status"] == "open")
    if open_conflicts:
        print(f"Conflits ouverts: {open_conflicts}")


COMMANDS = {
    "init": cmd_init,
    "stop": cmd_stop,
    "status": cmd_status,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Commands: init, stop, status")
        print("Examples:")
        print('  team-dashboard.py init "Feature X"')
        print("  team-dashboard.py init \"Feature X\" --agents frontend,backend,tests")
        print("  team-dashboard.py status")
        print("  team-dashboard.py stop")
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
