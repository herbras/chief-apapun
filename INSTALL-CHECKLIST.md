# Install Checklist

The install is good only if every item below passes.

## `gws` + helper layer

- [ ] `gws --help` works on the machine
- [ ] the intended Google accounts are authenticated in the `gws` profiles the helper scripts use
- [ ] Gmail search works through `clawchief/scripts/ea_gmail.py`
- [ ] Calendar list / agenda works through `clawchief/scripts/ea_calendar.py`
- [ ] Sheets read works through `clawchief/scripts/sheet_helper.py`
- [ ] Google Docs access works if meeting-notes ingestion is enabled

## Todoist

- [ ] `TODOIST_API_TOKEN` is present in the environment or `~/.openclaw/.env`
- [ ] `python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py bootstrap` succeeds in the target account
- [ ] the `Clawchief` project exists in Todoist
- [ ] the expected program sections were created from `clawchief/priority-map.md`

## Skills

- [ ] `task-system-contract` is installed in `~/.openclaw/skills/`
- [ ] `executive-assistant` is installed in `~/.openclaw/skills/`
- [ ] `business-development` is installed in `~/.openclaw/skills/`
- [ ] `daily-task-manager` is installed in `~/.openclaw/skills/`
- [ ] `daily-task-prep` is installed in `~/.openclaw/skills/`

## Workspace

- [ ] `clawchief/priority-map.md` is installed
- [ ] `clawchief/auto-resolver.md` is installed
- [ ] `clawchief/meeting-notes.md` is installed
- [ ] `clawchief/location-awareness.md` is installed
- [ ] `clawchief/knowledge-compiler.md` is installed
- [ ] `clawchief/task-system-acceptance.md` is installed
- [ ] `clawchief/scripts/` is installed
- [ ] `workspace/HEARTBEAT.md` is installed
- [ ] `workspace/TOOLS.md` is installed
- [ ] `workspace/memory/meeting-notes-state.json` is installed
- [ ] private workspace files have been authored if your setup depends on them
- [ ] all placeholders are replaced

## Behavior

- [ ] heartbeat reads source-of-truth files and helper-backed live state instead of duplicating workflow logic
- [ ] proactive updates route to the intended channel and target
- [ ] inbox sweeps use message-level Gmail search
- [ ] scheduling checks all relevant calendars before booking
- [ ] Todoist is the only live task system
- [ ] meeting notes are treated as a live signal source if enabled
- [ ] business-development work treats the outreach sheet as the live CRM source of truth
- [ ] daily task prep operates on Todoist only and does not rebuild `clawchief/tasks.md`

## Cron

- [ ] Executive assistant sweep exists
- [ ] Daily task prep exists
- [ ] Untangle daily prospecting exists
- [ ] optional nightly backup is configured only if desired
- [ ] optional self-update is enabled only if explicitly desired
- [ ] recurring cron prompts use the deterministic trigger wording from `cron/jobs.template.json`

If any box is unchecked, the install is not done.
