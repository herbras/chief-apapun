# clawchief

clawchief is a working OpenClaw setup to add Chief of Staff abilities to OpenClaw.

Use this repo if you want OpenClaw to help run day-to-day operations like:

- inbox triage
- scheduling and calendar checks
- a canonical markdown task list
- outreach tracking in Google Sheets
- recurring cron-driven routines

## What is in this repo

### Skills

- `executive-assistant`
- `business-development`
- `daily-task-manager`
- `daily-task-prep`

### Workspace files

- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/tasks/current.md`

### Setup docs

- `INSTALL-WITH-OPENCLAW.md`
- `SETUP-GOG.md`
- `INSTALL-CHECKLIST.md`
- `CHANNELS.md`
- `cron/jobs.template.json`

## What this setup expects

This setup expects:

- OpenClaw is already installed
- `gog` works for Gmail, Calendar, and Sheets
- you are willing to edit placeholders for your own name, email addresses, business, target market, geography, and sheet IDs

If `gog` is not working, stop and fix that first.

## Install order

1. Read `INSTALL-WITH-OPENCLAW.md`
2. Complete `SETUP-GOG.md`
3. Copy the skills into `~/.openclaw/skills/`
4. Copy the workspace files into `~/.openclaw/workspace/`
5. Replace placeholders
6. Create cron jobs from `cron/jobs.template.json`
7. Run `INSTALL-CHECKLIST.md`

## What makes this repo useful

The files in this repo are meant to be used by OpenClaw as working instructions, not as abstract examples.

The important behavior is:

- use Gmail **message-level search**, not thread-only search
- check **all relevant calendars** before booking
- keep one canonical `tasks/current.md`
- remove backlog duplicates when promoting tasks into `## Today`
- update the outreach tracker before treating a reply as handled
- keep cron prompts short and let the skill hold the workflow logic

## Private files not included here

The live setup also uses private workspace files like:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`
- `memory/`

Create your own local versions of those.
