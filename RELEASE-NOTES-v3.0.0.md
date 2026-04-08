# v3.0.0

This is a breaking architectural release of `clawchief`.

## Breaking changes

- Todoist is now the only canonical live task system.
- The old markdown task model built around `clawchief/tasks.md` and `clawchief/tasks-completed.md` is no longer the public operating model.
- Google workflows now run through `gws`-backed helper scripts instead of the older raw `gog`-first guidance.
- The public pack now includes a shared task-system contract, helper scripts, and tests as part of the core architecture.

## What's new

- Added a Todoist-backed task architecture with:
  - `skills/task-system-contract/SKILL.md`
  - `clawchief/task-system-acceptance.md`
  - `clawchief/scripts/todoist_cli.py`
- Added `gws`-backed helper scripts for:
  - Gmail
  - Calendar
  - Sheets
  - outbound outreach
- Added new source-of-truth files for:
  - location-aware task/actionability rules
  - knowledge compilation / linting behavior
  - thin task-system audit governance
- Updated the EA, BD, daily-task-manager, and daily-task-prep skills to match the revised live system
- Replaced the old cron template wording with deterministic trigger prompts
- Added a public test suite to keep the pack aligned with the revised behavior

## Upgrade notes

- Read `MIGRATION.md` before upgrading from `v2`
- Use `SETUP-GWS.md` instead of the older `SETUP-GOG.md`
- bootstrap Todoist before relying on recurring task workflows

## Verification

- public test suite passes: `43` tests
