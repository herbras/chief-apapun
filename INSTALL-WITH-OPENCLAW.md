# Install With OpenClaw

Follow this in order.

## 0. Get `gws` working

Complete `SETUP-GWS.md` first.

Do not continue until these all work through the helper layer:

- Gmail search / read
- Calendar list / agenda
- Sheets read
- Google Docs access if you plan to use meeting-notes ingestion

## 1. Gather install values

Collect these before editing files:

- `{{OWNER_NAME}}`
- `{{ASSISTANT_NAME}}`
- `{{ASSISTANT_EMAIL}}`
- `{{PRIMARY_WORK_EMAIL}}`
- `{{PERSONAL_EMAIL}}`
- `{{BUSINESS_NAME}}`
- `{{BUSINESS_URL}}`
- `{{TIMEZONE}}`
- `{{PRIMARY_UPDATE_CHANNEL}}`
- `{{PRIMARY_UPDATE_TARGET}}`
- `{{GOOGLE_SHEET_ID}}`
- `{{TARGET_MARKET}}`
- `{{TARGET_GEOGRAPHY}}`

Also gather:

- your Todoist API token for `TODOIST_API_TOKEN`
- any additional calendar addresses you need the EA workflow to inspect
- any `gws` profile/config directories you want the helper scripts to use

## 2. Install the skills

Copy these directories into `~/.openclaw/skills/`:

- `skills/task-system-contract`
- `skills/executive-assistant`
- `skills/business-development`
- `skills/daily-task-manager`
- `skills/daily-task-prep`

## 3. Install the workspace files

Copy these into `~/.openclaw/workspace/`:

- `clawchief/`
- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/memory/meeting-notes-state.json`

Notes:

- `workspace/tasks/current.md` is included only as a deprecation note for older installs
- live task state now lives in Todoist, not `clawchief/tasks.md`

## 4. Add your private workspace files

This public pack does not ship personal context files.

Create your own versions of these if your setup depends on them:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`
- `memory/`

## 5. Replace placeholders and local defaults

Replace every placeholder token before testing.

Minimum search list:

- `{{OWNER_NAME}}`
- `{{ASSISTANT_NAME}}`
- `{{ASSISTANT_EMAIL}}`
- `{{PRIMARY_WORK_EMAIL}}`
- `{{PERSONAL_EMAIL}}`
- `{{BUSINESS_NAME}}`
- `{{BUSINESS_URL}}`
- `{{TIMEZONE}}`
- `{{PRIMARY_UPDATE_CHANNEL}}`
- `{{PRIMARY_UPDATE_TARGET}}`
- `{{GOOGLE_SHEET_ID}}`
- `{{TARGET_MARKET}}`
- `{{TARGET_GEOGRAPHY}}`

Then customize these first:

- `workspace/TOOLS.md`
- `clawchief/priority-map.md`
- `skills/business-development/resources/partners.md`
- `cron/jobs.template.json`

## 6. Configure auth and runtime env

At minimum:

- ensure your `gws` profiles are authenticated for the accounts the helper scripts need
- add `TODOIST_API_TOKEN` to your environment or `~/.openclaw/.env`
- if you use non-default `gws` profile directories, document them in `workspace/TOOLS.md`

## 7. Bootstrap Todoist

Before you rely on the task flows in a new Todoist account, run:

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/todoist_cli.py bootstrap
```

That creates the expected project / section shape for the current priority map.

## 8. Create the cron jobs

Use `cron/jobs.template.json` as the starting pattern.

Recommended starting jobs:

1. Executive assistant sweep
2. Daily task prep
3. Untangle daily prospecting

Optional jobs:

4. Nightly OpenClaw backup
5. Optional OpenClaw self-update

Notes:

- keep prompts short and let the skill carry the workflow details
- keep recurring jobs deterministic and bounded
- let Todoist own live task state
- let the helper scripts own the command surface for Gmail, Calendar, and Sheets

## 9. Validate the install

Run `INSTALL-CHECKLIST.md`.
