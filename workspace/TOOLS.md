# TOOLS.md - Local Notes

Skills define how workflows should operate. This file is for your machine-specific setup.

## What goes here

Use this file for things like:

- Google account / profile notes
- browser profile choices
- camera names and locations
- SSH hosts and aliases
- device nicknames
- room names
- local auth state

## Clawchief boundary

- Keep workflow policy in `skills/` and `clawchief/*.md`.
- Keep `TOOLS.md` for local environment notes, account details, auth state, browser/profile choices, and machine-specific setup.

## Communication defaults

- Principal name: `{{OWNER_NAME}}`
- Assistant name: `{{ASSISTANT_NAME}}`
- Primary assistant email: `{{ASSISTANT_EMAIL}}`
- Primary work email / calendar: `{{PRIMARY_WORK_EMAIL}}`
- Personal email: `{{PERSONAL_EMAIL}}`
- Time zone: `{{TIMEZONE}}`
- Primary proactive update route: `{{PRIMARY_UPDATE_CHANNEL}} -> {{PRIMARY_UPDATE_TARGET}}`

## `gws` profile notes

Document the profile directories, credential files, and account mappings your helper scripts should use.

Example:

- assistant profile config dir: `~/.config/gws-r2`
- principal profile config dir: `~/.config/gws-owner`
- credential files, if you pin them explicitly
- any account-specific calendar write restrictions or read-only calendars

## Todoist

- canonical project name: `Clawchief`
- token source: environment variable or `~/.openclaw/.env`
- document any local conventions or owner aliases you want to preserve

## Calendars to check

List the calendars that should be treated as real availability constraints.

Example:

- `{{PRIMARY_WORK_EMAIL}}`
- `{{PERSONAL_EMAIL}}`
- additional work calendars
- Family calendar or equivalent hard-conflict calendar

## Outreach tracker

- live tracker / sheet id: `{{GOOGLE_SHEET_ID}}`
- treat this as the source of truth for outreach / CRM state
- document the current expected columns here if your sheet is customized

## Business-development playbook

Document your default sourcing motion here.

Suggested knobs:

- target geography
- primary target segment
- optional secondary target segment
- default daily batch size
- verification requirements
- follow-up cadence overrides
- any outreach tone or compliance rules unique to your environment
