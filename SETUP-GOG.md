# GOG Setup

This is a hard prerequisite.

## 1. Install GOG

```bash
brew install steipete/tap/gogcli
gog --help
```

## 2. Create a Google OAuth client

You need a Google OAuth desktop-client credentials JSON before `gog auth credentials ...` will work.

Create it in Google Cloud Console:

1. Create or choose a project
2. Open **APIs & Services**
3. Enable the APIs you need:
   - Gmail API
   - Google Calendar API
   - Google Sheets API
   - Google Drive API
   - Google Docs API
   - People API
4. Configure the **OAuth consent screen** if prompted
5. Add the operating Google account as a test user if required
6. Open **Credentials**
7. Click **Create Credentials** -> **OAuth client ID**
8. Choose **Desktop app**
9. Download the JSON file
10. Save it somewhere safe on the machine doing the install

## 3. Load the OAuth client credentials

```bash
gog auth credentials /path/to/client_secret.json
```

## 4. Add the operating account

```bash
gog auth add {{ASSISTANT_EMAIL}} --services gmail,calendar,drive,contacts,docs,sheets
```

## 5. Verify the account

```bash
gog auth list
```

## 6. Verify Gmail message search

```bash
gog gmail messages search -a {{ASSISTANT_EMAIL}} 'in:inbox newer_than:7d' --max=5 --json --results-only
```

Important: use **message-level** Gmail search for inbox sweeps. Do not rely on thread-only search.

## 7. Verify Calendar

```bash
gog calendar calendars -a {{ASSISTANT_EMAIL}} --json --results-only
gog calendar events --all -a {{ASSISTANT_EMAIL}} --days=2 --max=20 --json --results-only
```

## 8. Verify Sheets

```bash
gog sheets metadata {{GOOGLE_SHEET_ID}} -a {{ASSISTANT_EMAIL}} --json --results-only
```

## Stop conditions

Stop and fix setup if:

- the OAuth client JSON was never created or downloaded
- the wrong Google account is authenticated
- Gmail works but Calendar or Sheets does not
- the tracker sheet is not shared to the authenticated account
- someone uses thread-only search where message search is required
