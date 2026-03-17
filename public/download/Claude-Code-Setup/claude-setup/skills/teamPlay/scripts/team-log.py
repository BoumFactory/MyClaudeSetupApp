#!/usr/bin/env python3
"""
Script de logging pour les agents TeamPlay.
Chaque agent logue son activite via ce script ultra-court.

Usage:
  team-log.py task <agent> <task-id> <label> [detail]     # ajoute une tache
  team-log.py start <agent> <task-id>                      # marque en_cours
  team-log.py done <agent> <task-id> "description du fix"  # marque termine
  team-log.py fail <agent> <task-id> "raison"              # marque erreur
  team-log.py log <agent> "message"                         # ajoute un log
  team-log.py file <agent> <filepath> "action"              # logue un fichier modifie
"""
import json
import sys
import os
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEV_DIR = PROJECT_ROOT / ".dev"
TEAM_JSON = DEV_DIR / "team-live.json"

MAX_LOGS = 50
MAX_FILES = 100


def load():
    if not TEAM_JSON.exists():
        print("ERREUR: team-live.json introuvable. Lancer team-dashboard.py init d'abord.")
        sys.exit(1)
    with open(TEAM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save(data):
    data["last_updated"] = datetime.now().isoformat()
    with open(TEAM_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def _get_agent(data, agent_name):
    if agent_name not in data["agents"]:
        print(f"ERREUR: agent '{agent_name}' inconnu. Agents: {', '.join(data['agents'].keys())}")
        sys.exit(1)
    return data["agents"][agent_name]


def _update_agent_status(agent):
    """Met a jour le status de l'agent selon ses taches."""
    tasks = agent["tasks"]
    if not tasks:
        agent["status"] = "idle"
        return
    statuses = [t["status"] for t in tasks]
    if any(s == "working" for s in statuses):
        agent["status"] = "working"
    elif all(s == "done" for s in statuses):
        agent["status"] = "done"
    elif any(s == "error" for s in statuses) and not any(s == "working" for s in statuses):
        agent["status"] = "error"
    else:
        agent["status"] = "idle"


def _add_global_log(data, message):
    data["global_log"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message,
    })
    data["global_log"] = data["global_log"][-100:]


def cmd_task(args):
    """Ajoute une tache: team-log.py task <agent> <task-id> <label> [detail]"""
    if len(args) < 3:
        print("Usage: task <agent> <task-id> <label> [detail]")
        return
    data = load()
    agent = _get_agent(data, args[0])

    # Verifier doublon
    for t in agent["tasks"]:
        if t["id"] == args[1]:
            print(f"Tache {args[1]} existe deja pour {args[0]}")
            return

    task = {
        "id": args[1],
        "label": args[2],
        "status": "pending",
        "detail": args[3] if len(args) > 3 else "",
        "created": datetime.now().strftime("%H:%M:%S"),
    }
    agent["tasks"].append(task)
    _update_agent_status(agent)
    _add_global_log(data, f"[{args[0]}] Tache ajoutee: {args[2]}")
    save(data)
    print(f"Tache {args[1]} ajoutee pour {args[0]}")


def cmd_start(args):
    """Marque une tache en cours: team-log.py start <agent> <task-id>"""
    if len(args) < 2:
        print("Usage: start <agent> <task-id>")
        return
    data = load()
    agent = _get_agent(data, args[0])

    for t in agent["tasks"]:
        if t["id"] == args[1]:
            t["status"] = "working"
            t["started"] = datetime.now().strftime("%H:%M:%S")
            _update_agent_status(agent)
            _add_global_log(data, f"[{args[0]}] Demarre: {t['label']}")
            save(data)
            print(f"{args[0]}/{args[1]} -> working")
            return

    print(f"Tache {args[1]} non trouvee pour {args[0]}")


def cmd_done(args):
    """Marque une tache terminee: team-log.py done <agent> <task-id> 'description'"""
    if len(args) < 2:
        print("Usage: done <agent> <task-id> [description]")
        return
    data = load()
    agent = _get_agent(data, args[0])

    for t in agent["tasks"]:
        if t["id"] == args[1]:
            t["status"] = "done"
            t["finished"] = datetime.now().strftime("%H:%M:%S")
            if len(args) > 2:
                t["detail"] = args[2]
            _update_agent_status(agent)

            # Log agent
            agent["log"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": f"[OK] {t['label']}",
            })
            agent["log"] = agent["log"][-MAX_LOGS:]

            _add_global_log(data, f"[{args[0]}] Termine: {t['label']}")
            save(data)
            print(f"{args[0]}/{args[1]} -> done")
            return

    print(f"Tache {args[1]} non trouvee pour {args[0]}")


def cmd_fail(args):
    """Marque une tache en erreur: team-log.py fail <agent> <task-id> 'raison'"""
    if len(args) < 2:
        print("Usage: fail <agent> <task-id> [raison]")
        return
    data = load()
    agent = _get_agent(data, args[0])

    for t in agent["tasks"]:
        if t["id"] == args[1]:
            t["status"] = "error"
            if len(args) > 2:
                t["detail"] = args[2]
            _update_agent_status(agent)

            agent["log"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": f"[FAIL] {t['label']}: {args[2] if len(args) > 2 else 'erreur'}",
            })
            agent["log"] = agent["log"][-MAX_LOGS:]

            _add_global_log(data, f"[{args[0]}] ECHEC: {t['label']}")
            save(data)
            print(f"{args[0]}/{args[1]} -> error")
            return

    print(f"Tache {args[1]} non trouvee pour {args[0]}")


def cmd_log(args):
    """Ajoute un log: team-log.py log <agent> 'message'"""
    if len(args) < 2:
        print("Usage: log <agent> <message>")
        return
    data = load()
    agent = _get_agent(data, args[0])

    agent["log"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": args[1],
    })
    agent["log"] = agent["log"][-MAX_LOGS:]

    _add_global_log(data, f"[{args[0]}] {args[1]}")
    save(data)
    print(f"Log {args[0]}: {args[1][:50]}")


def cmd_file(args):
    """Logue un fichier modifie: team-log.py file <agent> <filepath> 'action'"""
    if len(args) < 3:
        print("Usage: file <agent> <filepath> <action>")
        return
    data = load()
    agent = _get_agent(data, args[0])

    agent["files_modified"].append({
        "path": args[1],
        "action": args[2],
        "time": datetime.now().strftime("%H:%M:%S"),
    })
    agent["files_modified"] = agent["files_modified"][-MAX_FILES:]

    save(data)
    print(f"Fichier {args[0]}: {args[1]} ({args[2]})")


COMMANDS = {
    "task": cmd_task,
    "start": cmd_start,
    "done": cmd_done,
    "fail": cmd_fail,
    "log": cmd_log,
    "file": cmd_file,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Commands: task, start, done, fail, log, file")
        print("Examples:")
        print('  team-log.py task frontend btn-delete "Creer bouton suppression"')
        print("  team-log.py start frontend btn-delete")
        print('  team-log.py done frontend btn-delete "Bouton cree avec handler"')
        print('  team-log.py fail frontend btn-delete "CSS casse"')
        print('  team-log.py log frontend "Debut implementation du panel"')
        print('  team-log.py file frontend "ui/js/modules/panel.js" "modified"')
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
