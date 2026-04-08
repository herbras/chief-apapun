# GWS Setup

This is a hard prerequisite for the revised Google workflows.

The current clawchief pack uses `gws` through helper scripts, not raw `gog` commands.

## 1. Install `gws`

Install the Google Workspace CLI on the machine and make sure this works:

```bash
gws --help
```

## 2. Create the Google OAuth credentials you need

You need desktop-client OAuth credentials for the Google account(s) the helper scripts will use.

Enable the APIs you need:

- Gmail API
- Google Calendar API
- Google Sheets API
- Google Drive API
- Google Docs API

## 3. Decide your profile layout

The helper scripts assume `gws` may run under more than one profile.

A common pattern is:

- one assistant profile for the assistant mailbox
- one principal profile for principal-owned outbound mailboxes/calendars when needed

Document your chosen profile directories in `workspace/TOOLS.md`.

## 4. Authenticate the accounts you need

Authenticate the Google accounts your workflows depend on:

- assistant mailbox
- any principal/work mailbox you send from directly
- any calendar-only account the EA workflow must read

## 5. Verify Gmail through the helper layer

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/ea_gmail.py search --query 'in:inbox newer_than:7d' --max 5
```

## 6. Verify Calendar through the helper layer

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/ea_calendar.py calendars
python3 ~/.openclaw/workspace/clawchief/scripts/ea_calendar.py agenda --days 2
```

## 7. Verify Sheets through the helper layer

```bash
python3 ~/.openclaw/workspace/clawchief/scripts/sheet_helper.py read --spreadsheet {{GOOGLE_SHEET_ID}} --range 'Leads!A:R'
```

## 8. Verify Docs access if meeting-note ingestion is enabled

If you plan to ingest meeting notes, make sure the operating account can access the shared docs the workflow will inspect.

## Stop conditions

Stop and fix setup if:

- `gws --help` fails
- the wrong Google account is authenticated
- Gmail works but Calendar or Sheets does not
- the tracker sheet is not shared to the authenticated account
- meeting-note docs are visible from calendar/thread context but the operating account cannot open them
