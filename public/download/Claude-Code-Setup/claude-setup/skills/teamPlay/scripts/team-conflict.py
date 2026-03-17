#!/usr/bin/env python3
"""
Gestion des conflits inter-agents pour TeamPlay.

Usage:
  team-conflict.py signal <reporter> <against> "description"
  team-conflict.py resolve <conflict-id> "resolution" [winner]
  team-conflict.py list
  team-conflict.py apply-resolutions
"""
import json
import sys
import os
import glob
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent
DEV_DIR = PROJECT_ROOT / ".dev"
TEAM_JSON = DEV_DIR / "team-live.json"

# Priorite par defaut : settings > backend > frontend > tests > reviewer
PRIORITY = {"settings": 1, "backend": 2, "frontend": 3, "tests": 4, "reviewer": 5}


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


def _next_conflict_id(data):
    conflicts = data.get("conflicts", [])
    if not conflicts:
        return "conflict-001"
    max_id = 0
    for c in conflicts:
        try:
            num = int(c["id"].split("-")[1])
            if num > max_id:
                max_id = num
        except (IndexError, ValueError):
            pass
    return f"conflict-{max_id + 1:03d}"


def _determine_winner(reporter, against):
    """Determine le gagnant par priorite par defaut."""
    r_prio = PRIORITY.get(reporter, 99)
    a_prio = PRIORITY.get(against, 99)
    return reporter if r_prio <= a_prio else against


def cmd_signal(args):
    """Signale un conflit: team-conflict.py signal <reporter> <against> 'description'"""
    if len(args) < 3:
        print("Usage: signal <reporter> <against> <description>")
        return
    data = load()
    reporter = args[0]
    against = args[1]
    description = args[2]

    conflict_id = _next_conflict_id(data)
    conflict = {
        "id": conflict_id,
        "reporter": reporter,
        "against": against,
        "description": description,
        "status": "open",
        "time": datetime.now().strftime("%H:%M:%S"),
        "resolution": None,
        "winner": None,
        "instruction_for_loser": None,
    }
    data["conflicts"].append(conflict)

    # Log global
    data["global_log"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": f"CONFLIT {conflict_id}: {reporter} vs {against} - {description}",
    })
    data["global_log"] = data["global_log"][-100:]

    save(data)
    print(f"Conflit signale: {conflict_id} ({reporter} vs {against})")


def cmd_resolve(args):
    """Resout un conflit: team-conflict.py resolve <conflict-id> 'resolution' [winner]"""
    if len(args) < 2:
        print("Usage: resolve <conflict-id> <resolution> [winner]")
        return
    data = load()
    conflict_id = args[0]
    resolution = args[1]
    winner = args[2] if len(args) > 2 else None

    for c in data["conflicts"]:
        if c["id"] == conflict_id:
            if c["status"] == "resolved":
                print(f"Conflit {conflict_id} deja resolu")
                return

            # Determiner le gagnant
            if not winner:
                winner = _determine_winner(c["reporter"], c["against"])

            loser = c["against"] if winner == c["reporter"] else c["reporter"]

            c["status"] = "resolved"
            c["resolution"] = resolution
            c["winner"] = winner
            c["instruction_for_loser"] = resolution
            c["resolved_at"] = datetime.now().strftime("%H:%M:%S")

            # Log global
            data["global_log"].append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "message": f"RESOLU {conflict_id}: gagnant={winner}, {loser} doit appliquer: {resolution[:80]}",
            })
            data["global_log"] = data["global_log"][-100:]

            save(data)
            print(f"Conflit {conflict_id} resolu. Gagnant: {winner}. Instruction pour {loser}: {resolution[:80]}")
            return

    print(f"Conflit {conflict_id} non trouve")


def cmd_list(args):
    """Liste les conflits."""
    data = load()
    conflicts = data.get("conflicts", [])

    if not conflicts:
        print("Aucun conflit")
        return

    for c in conflicts:
        status_icon = "!" if c["status"] == "open" else "v"
        print(f"  [{status_icon}] {c['id']} ({c['status']})")
        print(f"      {c['reporter']} vs {c['against']}: {c['description']}")
        if c["status"] == "resolved":
            print(f"      Gagnant: {c['winner']} | Resolution: {c['resolution'][:80]}")


def cmd_apply_resolutions(args):
    """Lit les fichiers de resolution du dashboard HTML et les applique."""
    data = load()
    pattern = str(DEV_DIR / "conflict-resolution-*.json")
    resolution_files = glob.glob(pattern)

    if not resolution_files:
        print("Aucun fichier de resolution a appliquer")
        return

    applied = 0
    for filepath in resolution_files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                res = json.load(f)

            conflict_id = res.get("conflict_id")
            winner = res.get("winner")
            resolution = res.get("resolution", "")

            # Trouver et resoudre le conflit
            for c in data["conflicts"]:
                if c["id"] == conflict_id and c["status"] == "open":
                    loser = c["against"] if winner == c["reporter"] else c["reporter"]
                    c["status"] = "resolved"
                    c["resolution"] = resolution
                    c["winner"] = winner
                    c["instruction_for_loser"] = resolution
                    c["resolved_at"] = datetime.now().strftime("%H:%M:%S")

                    data["global_log"].append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "message": f"RESOLU (dashboard) {conflict_id}: gagnant={winner}, instruction pour {loser}",
                    })
                    applied += 1
                    break

            # Supprimer le fichier de resolution traite
            os.remove(filepath)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Erreur lecture {filepath}: {e}")

    if applied > 0:
        data["global_log"] = data["global_log"][-100:]
        save(data)

    print(f"{applied} resolution(s) appliquee(s) depuis le dashboard")


COMMANDS = {
    "signal": cmd_signal,
    "resolve": cmd_resolve,
    "list": cmd_list,
    "apply-resolutions": cmd_apply_resolutions,
}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print("Commands: signal, resolve, list, apply-resolutions")
        print("Examples:")
        print('  team-conflict.py signal frontend backend "Both modifying /api/questions"')
        print('  team-conflict.py resolve conflict-001 "Backend owns the endpoint" backend')
        print("  team-conflict.py list")
        print("  team-conflict.py apply-resolutions")
        sys.exit(0)

    cmd = sys.argv[1]
    COMMANDS[cmd](sys.argv[2:])
