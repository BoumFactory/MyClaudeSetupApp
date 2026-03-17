#!/usr/bin/env python3
"""
Lecteur de logs inter-agents pour TeamPlay.
Permet a chaque agent de lire les logs de tous les autres.

Usage:
  team-read.py logs [agent]           # tous les logs, ou logs d'un agent
  team-read.py tasks [agent]          # etat des taches (tous ou un agent)
  team-read.py files [agent]          # fichiers modifies (tous ou un agent)
  team-read.py conflicts              # conflits ouverts
  team-read.py instructions <agent>   # instructions/resolutions pour cet agent
"""
import json
import sys
import os
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEV_DIR = PROJECT_ROOT / ".dev"
TEAM_JSON = DEV_DIR / "team-live.json"


def load():
    if not TEAM_JSON.exists():
        print("ERREUR: team-live.json introuvable. Lancer team-dashboard.py init d'abord.")
        sys.exit(1)
    with open(TEAM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_logs(args):
    """Affiche les logs. Sans argument: tous les agents tries par timestamp."""
    data = load()
    agent_filter = args[0] if args else None

    if agent_filter:
        if agent_filter not in data["agents"]:
            print(f"Agent '{agent_filter}' inconnu. Agents: {', '.join(data['agents'].keys())}")
            return
        logs = data["agents"][agent_filter].get("log", [])
        for entry in logs:
            print(f"  [{entry['time']}] {entry['message']}")
        if not logs:
            print(f"Aucun log pour {agent_filter}")
    else:
        # Collecter tous les logs avec le nom de l'agent
        all_logs = []
        for name, agent in data["agents"].items():
            for entry in agent.get("log", []):
                all_logs.append({
                    "agent": name,
                    "time": entry["time"],
                    "message": entry["message"],
                })
        # Trier par timestamp
        all_logs.sort(key=lambda x: x["time"])
        for entry in all_logs:
            print(f"  [{entry['time']}] [{entry['agent']}] {entry['message']}")
        if not all_logs:
            print("Aucun log")


def cmd_tasks(args):
    """Affiche l'etat des taches."""
    data = load()
    agent_filter = args[0] if args else None

    agents_to_show = {}
    if agent_filter:
        if agent_filter not in data["agents"]:
            print(f"Agent '{agent_filter}' inconnu.")
            return
        agents_to_show[agent_filter] = data["agents"][agent_filter]
    else:
        agents_to_show = data["agents"]

    for name, agent in agents_to_show.items():
        status_icon = {"idle": " ", "working": "~", "done": "v", "error": "x"}.get(agent["status"], "?")
        print(f"[{status_icon}] {name} ({agent['status']})")
        for t in agent["tasks"]:
            t_icon = {"pending": " ", "working": "~", "done": "v", "error": "x"}.get(t["status"], "?")
            detail = f" - {t['detail']}" if t.get("detail") else ""
            print(f"    [{t_icon}] {t['id']}: {t['label']}{detail}")
        if not agent["tasks"]:
            print("    (aucune tache)")


def cmd_files(args):
    """Affiche les fichiers modifies."""
    data = load()
    agent_filter = args[0] if args else None

    agents_to_show = {}
    if agent_filter:
        if agent_filter not in data["agents"]:
            print(f"Agent '{agent_filter}' inconnu.")
            return
        agents_to_show[agent_filter] = data["agents"][agent_filter]
    else:
        agents_to_show = data["agents"]

    for name, agent in agents_to_show.items():
        files = agent.get("files_modified", [])
        if files:
            print(f"[{name}]")
            for f in files:
                print(f"  [{f['time']}] {f['action']:10s} {f['path']}")
        elif not agent_filter:
            print(f"[{name}] (aucun fichier)")

    if agent_filter and not agents_to_show.get(agent_filter, {}).get("files_modified"):
        print(f"Aucun fichier modifie par {agent_filter}")


def cmd_conflicts(args):
    """Affiche les conflits ouverts."""
    data = load()
    conflicts = [c for c in data.get("conflicts", []) if c["status"] == "open"]

    if not conflicts:
        print("Aucun conflit ouvert")
        return

    for c in conflicts:
        print(f"  [{c['id']}] {c['reporter']} vs {c['against']}: {c['description']}")
        print(f"           Status: {c['status']} | Signale a {c['time']}")


def cmd_instructions(args):
    """Affiche les instructions de resolution pour un agent."""
    if not args:
        print("Usage: instructions <agent>")
        return

    data = load()
    agent_name = args[0]

    # Chercher les conflits resolus qui concernent cet agent comme "perdant"
    instructions = []
    for c in data.get("conflicts", []):
        if c["status"] != "resolved":
            continue
        if c.get("winner") and c["winner"] != agent_name:
            # Cet agent est le perdant si il est l'autre partie
            if agent_name in (c["reporter"], c["against"]):
                instructions.append({
                    "conflict_id": c["id"],
                    "instruction": c.get("instruction_for_loser", ""),
                    "winner": c["winner"],
                    "description": c["description"],
                })

    if not instructions:
        print(f"Aucune instruction pour {agent_name}")
        return

    for inst in instructions:
        print(f"  Conflit {inst['conflict_id']} (gagnant: {inst['winner']}):")
        print(f"    Sujet: {inst['description']}")
        print(f"    Instruction: {inst['instruction']}")


COMMANDS = {
    "logs": cmd_logs,
    "tasks": cmd_tasks,
    "files": cmd_files,
    "conflicts": cmd_conflicts,
    "instructions": cmd_instructions,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Commands: logs, tasks, files, conflicts, instructions")
        print("Examples:")
        print("  team-read.py logs")
        print("  team-read.py logs frontend")
        print("  team-read.py tasks")
        print("  team-read.py tasks backend")
        print("  team-read.py files")
        print("  team-read.py conflicts")
        print("  team-read.py instructions frontend")
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
