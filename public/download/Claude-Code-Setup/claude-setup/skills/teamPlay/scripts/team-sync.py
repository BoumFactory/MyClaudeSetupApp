#!/usr/bin/env python3
"""
Script de synchronisation pour le coordinateur TeamPlay.
Permet au coordinateur de pousser les donnees directement dans team-live.json.

Usage:
  team-sync.py tasks '<json_array>'      # Sync la liste de taches complete
  team-sync.py agent <name> <status>      # Met a jour le status d'un agent
  team-sync.py message <agent> '<text>'   # Ajoute un message au log d'un agent
  team-sync.py plan '<json_plan>'         # Injecte le plan global
  team-sync.py check-inbox               # Verifie les fichiers inbox utilisateur
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
MAX_GLOBAL_LOGS = 100

# Mapping des statuts Claude TaskList -> statuts TeamPlay
STATUS_MAP = {
    "pending": "pending",
    "in_progress": "working",
    "completed": "done",
    "cancelled": "error",
    "blocked": "pending",
}


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


def _ensure_agent(data, agent_name):
    """Retourne l'agent, le cree avec structure vide s'il n'existe pas."""
    if agent_name not in data["agents"]:
        data["agents"][agent_name] = {
            "status": "idle",
            "tasks": [],
            "log": [],
            "files_modified": [],
        }
    return data["agents"][agent_name]


def _update_agent_status(agent):
    """Met a jour le status global de l'agent selon ses taches."""
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
    data["global_log"] = data["global_log"][-MAX_GLOBAL_LOGS:]


def cmd_tasks(args):
    """Sync la liste de taches complete depuis un JSON array Claude TaskList.

    team-sync.py tasks '<json_array>'
    Format attendu :
    [{"id":"1","subject":"...","status":"pending|in_progress|completed","owner":"frontend","blockedBy":[]},...]
    """
    if not args:
        print("Usage: tasks '<json_array>'")
        sys.exit(1)

    try:
        task_list = json.loads(args[0])
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide: {e}")
        sys.exit(1)

    if not isinstance(task_list, list):
        print("ERREUR: le JSON doit etre un array de taches")
        sys.exit(1)

    data = load()
    now_hms = datetime.now().strftime("%H:%M:%S")
    updated_count = 0
    created_count = 0

    for task in task_list:
        task_id = str(task.get("id", ""))
        subject = task.get("subject", task.get("label", f"Tache {task_id}"))
        raw_status = task.get("status", "pending")
        tp_status = STATUS_MAP.get(raw_status, "pending")
        owner = task.get("owner", "")

        if not owner or not task_id:
            continue

        agent = _ensure_agent(data, owner)

        # Chercher si la tache existe deja
        existing = None
        for t in agent["tasks"]:
            if t["id"] == task_id:
                existing = t
                break

        if existing:
            old_status = existing["status"]
            existing["label"] = subject
            existing["status"] = tp_status
            if tp_status == "working" and "started" not in existing:
                existing["started"] = now_hms
            if tp_status in ("done", "error"):
                existing["finished"] = now_hms
            if old_status != tp_status:
                _add_global_log(data, f"[{owner}] Tache {task_id} : {old_status} -> {tp_status} ({subject})")
            updated_count += 1
        else:
            new_task = {
                "id": task_id,
                "label": subject,
                "status": tp_status,
                "detail": "",
                "created": now_hms,
            }
            if tp_status == "working":
                new_task["started"] = now_hms
            if tp_status in ("done", "error"):
                new_task["finished"] = now_hms
            agent["tasks"].append(new_task)
            _add_global_log(data, f"[{owner}] Tache ajoutee: {subject} ({tp_status})")
            created_count += 1

        _update_agent_status(agent)

    save(data)
    print(f"Taches synchronisees: {created_count} creees, {updated_count} mises a jour")


def cmd_agent(args):
    """Met a jour le status d'un agent.

    team-sync.py agent <name> <status>
    Status valides: idle, working, done, error
    """
    if len(args) < 2:
        print("Usage: agent <name> <status>")
        print("Status valides: idle, working, done, error")
        sys.exit(1)

    name = args[0]
    status = args[1]

    valid_statuses = {"idle", "working", "done", "error"}
    if status not in valid_statuses:
        print(f"ERREUR: status invalide '{status}'. Valides: {', '.join(sorted(valid_statuses))}")
        sys.exit(1)

    data = load()
    agent = _ensure_agent(data, name)
    old_status = agent["status"]
    agent["status"] = status

    if old_status != status:
        _add_global_log(data, f"[{name}] Status: {old_status} -> {status}")

    save(data)
    print(f"Agent '{name}' status -> {status}")


def cmd_message(args):
    """Ajoute un message au log d'un agent et au global_log.

    team-sync.py message <agent> '<text>'
    """
    if len(args) < 2:
        print("Usage: message <agent> '<text>'")
        sys.exit(1)

    agent_name = args[0]
    text = args[1]
    now_hms = datetime.now().strftime("%H:%M:%S")

    data = load()
    agent = _ensure_agent(data, agent_name)

    agent["log"].append({
        "time": now_hms,
        "message": text,
    })
    agent["log"] = agent["log"][-MAX_LOGS:]

    _add_global_log(data, f"[{agent_name}] {text}")
    save(data)
    print(f"Message ajoute pour '{agent_name}': {text[:80]}")


def cmd_plan(args):
    """Injecte le plan global dans team-live.json.

    team-sync.py plan '<json_plan>'
    Format attendu :
    {
      "tasks": [{"id":"1","subject":"...","owner":"frontend","status":"pending","blockedBy":["3"]}],
      "last_updated": "ISO"
    }
    Ou directement un array de taches (sera encapsule automatiquement).
    """
    if not args:
        print("Usage: plan '<json_plan>'")
        sys.exit(1)

    try:
        plan_data = json.loads(args[0])
    except json.JSONDecodeError as e:
        print(f"ERREUR: JSON invalide: {e}")
        sys.exit(1)

    # Normaliser : si c'est un array, l'encapsuler
    if isinstance(plan_data, list):
        plan_obj = {
            "tasks": plan_data,
            "last_updated": datetime.now().isoformat(),
        }
    elif isinstance(plan_data, dict):
        plan_obj = plan_data
        plan_obj["last_updated"] = datetime.now().isoformat()
    else:
        print("ERREUR: le JSON doit etre un objet ou un array de taches")
        sys.exit(1)

    data = load()
    data["plan"] = plan_obj

    task_count = len(plan_obj.get("tasks", []))
    _add_global_log(data, f"[coordinateur] Plan injecte: {task_count} taches")
    save(data)
    print(f"Plan injecte: {task_count} taches")


def cmd_check_inbox(args):
    """Verifie les fichiers inbox utilisateur dans .dev/team-inbox-*.txt.

    Lit chaque fichier, extrait l'agent depuis le nom, supprime le fichier.
    Retourne un JSON array : [{"agent": "frontend", "message": "..."}, ...]
    """
    inbox_files = list(DEV_DIR.glob("team-inbox-*.txt"))

    if not inbox_files:
        print("[]")
        return

    messages = []
    for inbox_file in inbox_files:
        # Extraire le nom de l'agent depuis le filename
        # team-inbox-frontend.txt -> frontend
        stem = inbox_file.stem  # "team-inbox-frontend"
        prefix = "team-inbox-"
        if stem.startswith(prefix):
            agent_name = stem[len(prefix):]
        else:
            agent_name = stem

        try:
            content = inbox_file.read_text(encoding="utf-8").strip()
            messages.append({
                "agent": agent_name,
                "message": content,
            })
            inbox_file.unlink()
        except Exception as e:
            messages.append({
                "agent": agent_name,
                "message": f"ERREUR lecture: {e}",
            })

    print(json.dumps(messages, ensure_ascii=False, indent=2))


COMMANDS = {
    "tasks": cmd_tasks,
    "agent": cmd_agent,
    "message": cmd_message,
    "plan": cmd_plan,
    "check-inbox": cmd_check_inbox,
}


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Commands: tasks, agent, message, plan, check-inbox")
        print()
        print("Examples:")
        print('  team-sync.py tasks \'[{"id":"1","subject":"Fix bug","status":"in_progress","owner":"frontend","blockedBy":[]}]\'')
        print("  team-sync.py agent frontend working")
        print('  team-sync.py message backend "Compilation Rust terminee"')
        print('  team-sync.py plan \'{"tasks":[{"id":"1","subject":"Tache 1","owner":"frontend","status":"pending","blockedBy":[]}]}\'')
        print("  team-sync.py check-inbox")
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
