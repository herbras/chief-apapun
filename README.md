# clawchief

`clawchief` is a public OpenClaw starter kit for turning OpenClaw into a founder / chief-of-staff operating system.

It is opinionated about the architecture of the workflow, but meant to be customized for your own people, programs, calendars, inboxes, trackers, and recurring routines.

## Breaking Changes In v3

`v3.0.0` is a breaking architectural release.

If you installed or learned `clawchief` from the earlier public `v2` release, read [MIGRATION.md](/Users/r2/.openclaw/workspace/clawchief-github/MIGRATION.md) before upgrading.

The important changes are:

- live task state now lives in Todoist, not `clawchief/tasks.md`
- Google workflows now run through `gws`-backed helper scripts, not raw `gog` instructions
- the public pack now includes a shared task-system contract, helper scripts, and tests as part of the core architecture

## Launch post

If you want the original public context for `clawchief`, here is the launch post from Ryan Carson's real-world rollout:

- <https://x.com/ryancarson/status/2039786704731541903>

## What this repo gives you

A portable operating model with:

- a source-of-truth `clawchief/` layer for priorities, resolution policy, meeting-note policy, location-aware task curation, and knowledge compilation
- a Todoist-backed live task system with a shared task contract
- `gws`-backed helper scripts for Gmail, Calendar, Sheets, outreach, and Todoist workflows
- executive-assistant, business-development, daily-task-manager, daily-task-prep, and task-system-contract skills
- deterministic cron templates with short trigger prompts
- tests that keep the public pack aligned with the revised behavior

## Revised architecture

The current pack has three important shifts from the original public version:

1. live task state now lives in Todoist, not `clawchief/tasks.md`
2. Google workflows now run through `gws`-backed helper scripts, not raw `gog` commands
3. recurring behavior is encoded through a shared task contract, thin source-of-truth files, helper scripts, and deterministic cron triggers

## Repo layout

### Source-of-truth files

- `clawchief/priority-map.md`
- `clawchief/auto-resolver.md`
- `clawchief/meeting-notes.md`
- `clawchief/location-awareness.md`
- `clawchief/knowledge-compiler.md`
- `clawchief/task-system-acceptance.md`
- `clawchief/archive/README.md`

### Helper scripts

- `clawchief/scripts/todoist_cli.py`
- `clawchief/scripts/ea_gmail.py`
- `clawchief/scripts/ea_calendar.py`
- `clawchief/scripts/sheet_helper.py`
- `clawchief/scripts/bd_outreach.py`

### Skills

- `skills/task-system-contract`
- `skills/executive-assistant`
- `skills/business-development`
- `skills/daily-task-manager`
- `skills/daily-task-prep`

### Tests

- `clawchief/tests/`

### Workspace templates

- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/memory/meeting-notes-state.json`
- `workspace/tasks/current.md` as a deprecation pointer for older installs

### Setup docs

- `INSTALL-WITH-OPENCLAW.md`
- `SETUP-GWS.md`
- `INSTALL-CHECKLIST.md`
- `CHANNELS.md`
- `cron/jobs.template.json`

## The design pattern

The system works best when you separate:

1. prioritization -> `clawchief/priority-map.md`
2. resolution policy -> `clawchief/auto-resolver.md`
3. meeting-note ingestion policy -> `clawchief/meeting-notes.md`
4. place-based actionability -> `clawchief/location-awareness.md`
5. system compilation / linting policy -> `clawchief/knowledge-compiler.md`
6. live tasks -> Todoist via `clawchief/scripts/todoist_cli.py`
7. shared task-system rules -> `skills/task-system-contract/SKILL.md`
8. local environment details -> `workspace/TOOLS.md`
9. recurring orchestration -> `workspace/HEARTBEAT.md` plus cron jobs

That separation is the main thing this repo is trying to teach.

## Install order

1. Read `INSTALL-WITH-OPENCLAW.md`
2. Complete `SETUP-GWS.md`
3. Copy the skills into `~/.openclaw/skills/`
4. Copy `clawchief/` and `workspace/` into `~/.openclaw/workspace/`
5. Replace placeholders and customize `workspace/TOOLS.md`
6. Add `TODOIST_API_TOKEN` to your environment or `~/.openclaw/.env`
7. Create cron jobs from `cron/jobs.template.json`
8. Run `INSTALL-CHECKLIST.md`

## Good customization targets

Customize these first:

- `workspace/TOOLS.md`
- `clawchief/priority-map.md`
- `skills/business-development/resources/partners.md`
- `cron/jobs.template.json`
- any Ryan / Untangle specific helper defaults you want to convert into your own environment

## Core operating lessons baked into this repo

- use Gmail message-level search, not thread-only search
- check all relevant calendars before booking
- keep one canonical live task system, and let Todoist own it
- use helper scripts as the stable command surface for Google workflows
- keep cron prompts short and let skills hold workflow logic
- use a policy layer for prioritization and a separate policy layer for auto-resolution
- treat meeting notes as a live signal source, not passive documents
- keep heartbeat thin and let deterministic cron jobs own recurring work
- compile durable lessons back into source-of-truth files instead of leaving them stranded in chat

## Legacy note

The older public repo used `clawchief/tasks.md` and `clawchief/tasks-completed.md` as live task files.

That is no longer the canonical model.

Archived markdown task files may still exist for migration reference, but the revised pack uses Todoist as the only live task system.

## Private local files you probably still want

You may still want your own private workspace files such as:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`
- `memory/`

Those are intentionally not part of this public repo.
