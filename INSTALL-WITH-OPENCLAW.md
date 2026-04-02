# Install With OpenClaw

Follow this in order.

## 0. Get GOG working

Complete `SETUP-GOG.md` first.

Do not continue until these all work:

- Gmail message search
- Calendar list / event read
- Sheets metadata read

## 1. Gather install values

Collect these before writing files:

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
- `{{REPO_ROOT}}`

## 2. Install the skills

Copy these directories into `~/.openclaw/skills/`:

- `skills/executive-assistant`
- `skills/business-development`
- `skills/daily-task-manager`
- `skills/daily-task-prep`

## 3. Install the workspace files

Copy these into `~/.openclaw/workspace/`:

- `workspace/HEARTBEAT.md`
- `workspace/TOOLS.md`
- `workspace/tasks/current.md`

Merge carefully if you already have live files.

## 4. Add your private workspace files

This public pack does **not** ship personal context files.

Create your own versions of these in the workspace if you use them:

- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`
- `memory/`

## 5. Replace placeholders

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
- `{{REPO_ROOT}}`

## 6. Create the cron jobs

Use `cron/jobs.template.json` as the pattern.

Recommended starting jobs:

1. executive assistant sweep
2. daily task prep
3. daily business-development sourcing

Optional jobs:

4. nightly backup
5. self-update

Notes:
- backup should stay disabled until the remote repo and allowlist are correct
- self-update should stay disabled unless you explicitly want that behavior

## 7. Validate the install

Run `INSTALL-CHECKLIST.md`.
