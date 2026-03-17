# Agent Team Tools Reference

Quick reference for all tools used in agent team orchestration.

## TeamCreate

Creates a new team with a shared task list.

Parameters:
- `team_name` (required): short, lowercase, hyphenated name
- `description` (optional): purpose of the team

Creates:
- Team config at `~/.claude/teams/{team-name}/config.json`
- Task list at `~/.claude/tasks/{team-name}/`

## Task (spawning teammates)

Spawn a teammate by including `team_name` and `name` parameters.

Key parameters:
- `team_name`: must match the created team
- `name`: human-readable role name (e.g., "backend-dev")
- `subagent_type`: agent type ("general-purpose" for code work, "Explore" for research, "Plan" for architecture)
- `model`: "sonnet" (default, cost-effective) or "opus" (complex work) or "haiku" (simple tasks)
- `mode`: "bypassPermissions", "plan" (requires approval), "default", "delegate"
- `prompt`: detailed instructions — teammates do NOT inherit conversation history

## TaskCreate

Create a task in the shared task list.

Parameters:
- `subject`: imperative title (e.g., "Implement auth middleware")
- `description`: detailed description with acceptance criteria
- `activeForm`: present continuous form for spinner (e.g., "Implementing auth middleware")

## TaskUpdate

Update task status, ownership, or dependencies.

Parameters:
- `taskId` (required): task ID
- `status`: "pending", "in_progress", "completed", "deleted"
- `owner`: teammate name to assign
- `addBlockedBy`: array of task IDs that must complete first
- `addBlocks`: array of task IDs this task blocks

## TaskList

List all tasks with summary info. No parameters.

## TaskGet

Get full details of a specific task by ID.

## SendMessage

Communication between agents.

Types:
- `message`: DM to one teammate (recipient required)
- `broadcast`: send to ALL teammates (costly, use sparingly)
- `shutdown_request`: ask teammate to shut down gracefully
- `shutdown_response`: teammate responds to shutdown request
- `plan_approval_response`: approve/reject a teammate's plan

## TeamDelete

Remove team and task directories. Fails if teammates are still active — shut them down first.
