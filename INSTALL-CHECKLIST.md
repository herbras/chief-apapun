# Install Checklist

The install is good only if every item below passes.

## GOG

- [ ] `gog auth list` shows the correct operating account
- [ ] Gmail **message search** works
- [ ] Calendar list/read works
- [ ] Sheets metadata read works

## Skills

- [ ] `executive-assistant` is installed in `~/.openclaw/skills/`
- [ ] `business-development` is installed in `~/.openclaw/skills/`
- [ ] `daily-task-manager` is installed in `~/.openclaw/skills/`
- [ ] `daily-task-prep` is installed in `~/.openclaw/skills/`

## Workspace

- [ ] `HEARTBEAT.md` is installed
- [ ] `TOOLS.md` is installed
- [ ] `tasks/current.md` is installed
- [ ] private workspace files have been authored if your setup depends on them
- [ ] all placeholders are replaced

## Behavior

- [ ] heartbeat reads `tasks/current.md`
- [ ] proactive updates route to the intended channel + target
- [ ] inbox sweeps use **message-level** Gmail search
- [ ] scheduling checks all relevant calendars before booking
- [ ] business-development work treats the Google Sheet as the live source of truth
- [ ] daily task prep promotes due-today items into `## Today`
- [ ] LinkedIn work prefers an agent-controlled browser profile by default

## Cron

- [ ] executive assistant sweep exists
- [ ] daily task prep exists
- [ ] daily business-development sourcing exists
- [ ] optional nightly backup is configured only if desired
- [ ] optional self-update is enabled only if explicitly desired

If any box is unchecked, the install is not done.
