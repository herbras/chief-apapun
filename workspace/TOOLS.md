# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Linear

- Linear MCP is configured via `mcporter` in `config/mcporter.json` as server `linear`.
- Auth header uses `Authorization: Bearer ${LINEAR_API_KEY}` and expects `LINEAR_API_KEY` in `~/.openclaw/.env`.
- For ad hoc calls, prefix shell commands with `set -a; source ~/.openclaw/.env; set +a;` so header substitution works.
- Common call pattern:
  - `mcporter call linear.save_issue --args '{"title":"...","team":"{{BUSINESS_NAME}}","description":"..."}'`

## Outreach tracking

- For {{OWNER_NAME}}'s outreach / lead-tracking work, the Google Sheet is the only source of truth.
- Do not treat local `.md` or `.csv` prospect files as the live outreach list unless {{OWNER_NAME}} explicitly asks for an export or backup.
- If a lead is added or updated, update the Google Sheet rather than only changing workspace files.
- On this Mac, prefer the local `gog` CLI for Google Sheets work when available; `{{ASSISTANT_EMAIL}}` is already authenticated with Sheets access.
- More broadly for Google Workspace tasks (Sheets/Gmail/Calendar/Docs), prefer `gog` on this machine rather than browser automation when `gog` can do the job.
- For LinkedIn investigation / outreach browser work, prefer the OpenClaw-managed browser profile (`openclaw`) now that {{OWNER_NAME}} has logged LinkedIn into it. Treat personal Chrome attach (`profile=user`) as fallback-only when {{OWNER_NAME}} is physically present and explicitly wants reuse of his live browser session.

## Email / Gmail

- The founder's default work email / cc for chief-of-staff communication is `{{PRIMARY_WORK_EMAIL}}`.
- Use `{{PERSONAL_EMAIL}}` only for personal matters.
- For outbound outreach sent via `gog gmail send`, keep emails in plain text unless rich formatting is specifically needed.
- `gog gmail send` plain text is sent as normal `text/plain`; if a mobile client looks awkward, the fix is usually shorter paragraphs and cleaner bulleting, not HTML.
- For plain-text outreach, prefer:
  - one short sentence per paragraph when possible
  - short bullet lists
  - fewer long compound sentences
  - cleaner spacing so mobile wrap looks natural
- When mentioning {{BUSINESS_NAME}} for the first time in an outbound email, write `{{BUSINESS_URL}}` so the recipient's client auto-links it; don't bother with `https://`.
- In first-contact outreach, skip the self-introduction fluff and get to the point. Preferred pattern: a simple greeting, then "I'm on the team at {{BUSINESS_URL}}..." rather than "I'm {{ASSISTANT_NAME}}, {{OWNER_NAME}}'s assistant..."
- Use this default signature for outbound {{BUSINESS_NAME}} emails unless {{OWNER_NAME}} specifies otherwise:

  [farewell greeting],
  {{ASSISTANT_NAME}}

  AI Assistant to {{OWNER_NAME}} (Founder)
  {{BUSINESS_URL}} - replace this line with your business one-liner.
- In scheduling and follow-up threads, read the full thread context before asking for contact details or next-step info. If a person was already copied or identified earlier in the thread, use that context instead of asking {{OWNER_NAME}} to repeat it.
- When replying to an email thread where copied recipients matter, do not assume `--thread-id ... --reply-all` will preserve earlier recipients. Prefer replying against the original message id with `--reply-to-message-id ... --reply-all`, or otherwise verify recipients before sending.
- For outbound {{BUSINESS_NAME}} work email sent by {{ASSISTANT_NAME}}, cc {{OWNER_NAME}} by default unless he says otherwise. Use `{{PRIMARY_WORK_EMAIL}}` as the default cc address.
- Do not write email language that implies {{ASSISTANT_NAME}} is human or personally attended an interaction. Avoid lines like `nice to meet you`, `great seeing you`, or `I enjoyed speaking today` unless the sentence is explicitly about {{OWNER_NAME}}'s experience rather than mine. Prefer neutral phrasing like `Thanks for meeting with {{OWNER_NAME}} today`.

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
