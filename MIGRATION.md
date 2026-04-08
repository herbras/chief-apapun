# Migration To v3

`v3.0.0` is the first public release of the revised clawchief architecture.

If you are coming from the public `v2` release, this is not a drop-in patch.

## What changed

Three major things changed:

1. canonical live task state moved from markdown files to Todoist
2. Google workflows moved from raw `gog` guidance to `gws`-backed helper scripts
3. the public pack now depends on a shared task-system contract, helper scripts, deterministic cron wording, and tests

## Breaking changes

### Tasks

Old model:

- `clawchief/tasks.md`
- `clawchief/tasks-completed.md`

New model:

- Todoist is the only live task system
- `clawchief/task-system-acceptance.md` is the audit index
- `skills/task-system-contract/SKILL.md` is the shared runtime contract
- `clawchief/scripts/todoist_cli.py` is the stable local command surface

What this means:

- do not keep running the old markdown task workflow
- do not recreate `clawchief/tasks.md` as a shadow live database
- bootstrap Todoist before relying on recurring task flows

### Google workflows

Old model:

- `SETUP-GOG.md`
- skills that referenced raw `gog` commands directly

New model:

- `SETUP-GWS.md`
- helper scripts in `clawchief/scripts/`
- skills that call those helpers instead of assuming raw one-off Google commands

What this means:

- re-auth your Google environment around the `gws` profiles the helper scripts use
- verify Gmail, Calendar, and Sheets through the helper scripts, not just by testing the underlying CLI in isolation

### Cron behavior

Old model:

- thinner cron examples, less explicit trigger language

New model:

- short but deterministic cron prompts
- explicit ownership boundaries
- Todoist-only daily task prep
- EA and BD sweeps framed as bounded recurring triggers

What this means:

- update your cron jobs from `cron/jobs.template.json`
- do not keep old task-prep prompts that rebuild markdown task files

## Recommended upgrade path

1. Back up your current OpenClaw workspace and cron config.
2. Install the new `skills/task-system-contract`.
3. Copy over the revised `clawchief/` files and `clawchief/scripts/`.
4. Set up `gws` using `SETUP-GWS.md`.
5. Add `TODOIST_API_TOKEN` to your environment or `~/.openclaw/.env`.
6. Run:

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py bootstrap
```

7. Replace old cron jobs with the templates from `cron/jobs.template.json`.
8. Run the install checklist.

## If you have old markdown task data

If you still have task history in the older markdown format, treat it as migration input only.

The helper includes import commands for that transition:

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py import-markdown
python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py import-markdown --apply
```

After migration, Todoist should become the only live task system.

## Sanity checks after upgrade

Make sure all of these are true:

- `python3 ~/.openclaw/workspace/clawchief/scripts/ea_gmail.py search ...` works
- `python3 ~/.openclaw/workspace/clawchief/scripts/ea_calendar.py calendars` works
- `python3 ~/.openclaw/workspace/clawchief/scripts/sheet_helper.py read ...` works
- `python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py list-tasks --owner ryan --due-today` works
- your daily task prep is operating on Todoist only
- no active workflow still treats `clawchief/tasks.md` as canonical
