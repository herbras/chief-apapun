# HEARTBEAT.md

Canonical sources:

- `clawchief/priority-map.md`
- `clawchief/auto-resolver.md`
- `clawchief/meeting-notes.md`
- `clawchief/knowledge-compiler.md`
- Todoist task state
- `clawchief/scripts/todoist_cli.py`
- `memory/meeting-notes-state.json`
- `executive-assistant` skill
- `business-development` skill
- `daily-task-manager` skill

Heartbeat role:

- run the relevant skill-driven operational sweep
- prefer EA by default, switch to business-development when the signal is pipeline / outreach state
- treat the outreach sheet as a live CRM queue, not just a historical tracker
- use Todoist as live task state, not chat memory
- use the local Todoist helper, not ad hoc manual task-state guesses
- use at most one compiler / lint pass when no higher-value operational work is pending
- do not perform daily task prep here
- if nothing matters, reply `HEARTBEAT_OK`

Rules:

- keep this file thin
- let the skills own the procedures
- keep heartbeat passes small
- when doing BD/EA sweeps, bias toward checking whether CRM rows changed state and need a sheet update
- do not send repeated or near-identical nudges unless something materially changed
