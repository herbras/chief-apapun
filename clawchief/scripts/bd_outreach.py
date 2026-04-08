#!/usr/bin/env python3

"""Business-development outreach helper.

Renders and sends the approved initial outreach templates from Ryan's mailbox.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timedelta
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo


SCRIPT_DIR = Path(__file__).resolve().parent
EA_GMAIL_PATH = SCRIPT_DIR / "ea_gmail.py"
TODOIST_CLI_PATH = SCRIPT_DIR / "todoist_cli.py"
RYAN_FROM = "ryan@ryancarson.com"
R2_CC = "r2@untangle.us"
DEFAULT_SECTION = "Business development partnerships"
DEFAULT_PROGRAM = "Business development partnerships"
DEFAULT_TZ = ZoneInfo("America/New_York")


@dataclass(frozen=True)
class OutreachTemplate:
    kind: str
    subject: str
    default_cc: str


COACH_THERAPIST_TEMPLATE = OutreachTemplate(
    kind="coach_therapist",
    subject="Saw your work",
    default_cc=R2_CC,
)

ATTORNEY_TEMPLATE = OutreachTemplate(
    kind="attorney",
    subject="New divorce assistant for CT residents just launched",
    default_cc=R2_CC,
)


def detect_kind(role: str) -> str | None:
    lowered = role.lower()
    attorney_markers = ("attorney", "lawyer", "family law", "esq", "esquire", "law office", "law offices")
    coach_markers = ("coach", "therap", "counsel", "lmft", "lcsw", "psycholog", "marriage")
    if any(marker in lowered for marker in attorney_markers):
        return ATTORNEY_TEMPLATE.kind
    if any(marker in lowered for marker in coach_markers):
        return COACH_THERAPIST_TEMPLATE.kind
    return None


def normalize_kind(kind: str, role: str) -> str:
    if kind:
        return kind
    detected = detect_kind(role)
    if detected:
        return detected
    raise ValueError("Unable to determine outreach template kind; provide --kind explicitly.")


def template_for_kind(kind: str) -> OutreachTemplate:
    if kind == COACH_THERAPIST_TEMPLATE.kind:
        return COACH_THERAPIST_TEMPLATE
    if kind == ATTORNEY_TEMPLATE.kind:
        return ATTORNEY_TEMPLATE
    raise ValueError(f"Unsupported outreach template kind: {kind}")


def coach_therapist_plain(first_name: str) -> str:
    return "\n\n".join(
        [
            f"Hi {first_name},",
            "I'm Ryan, the founder of Untangle. My assistant came across your work and thought we should connect.",
            "Untangle helps CT residents getting divorced who can't afford an attorney, or who have an attorney but would like to reduce costs.",
            "I built Untangle because I saw my two sisters go through really tough divorces, and I wanted to do something about it. Untangle.us answers divorce questions, correctly fills out all divorce forms, and helps clients move forward with confidence.",
            "I've copied my assistant here in case you'd be open to a quick phone call sometime. No pressure at all - I'm not trying to sell you anything. Just thought it would be good to connect and see if we can collaborate.",
            "All the best,\nRyan\n\nFounder, Untangle",
        ]
    )


def coach_therapist_html(first_name: str) -> str:
    safe_name = escape(first_name)
    return "".join(
        [
            f"<p>Hi {safe_name},</p>",
            "<p>I'm Ryan, the founder of Untangle. My assistant came across your work and thought we should connect.</p>",
            "<p>Untangle helps CT residents getting divorced who can't afford an attorney, or who have an attorney but would like to reduce costs.</p>",
            "<p>I built Untangle because I saw my two sisters go through really tough divorces, and I wanted to do something about it. Untangle.us answers divorce questions, correctly fills out all divorce forms, and helps clients move forward with confidence.</p>",
            "<p>I've copied my assistant here in case you'd be open to a quick phone call sometime. No pressure at all - I'm not trying to sell you anything. Just thought it would be good to connect and see if we can collaborate.</p>",
            '<p>All the best,<br>Ryan</p><p>Founder, <a href="https://untangle.us">Untangle</a></p>',
        ]
    )


def attorney_plain(first_name: str) -> str:
    return "\n\n".join(
        [
            f"Hi {first_name},",
            "I'm Ryan, the founder of Untangle. I noticed you practice family law in CT and wanted to reach out.",
            "I built Untangle because I watched my two sisters go through really tough divorces. It helps CT residents answer non-legal divorce questions and correctly fill out all their court forms - which can be a big time-saver for attorneys whose clients need help with paperwork.",
            "Would you be open to a quick 10-minute call? I'd love to hear how you're handling form prep now and whether Untangle could be useful for your clients.",
            "All the best,\nRyan\n\nFounder, Untangle",
        ]
    )


def attorney_html(first_name: str) -> str:
    safe_name = escape(first_name)
    return "".join(
        [
            f"<p>Hi {safe_name},</p>",
            "<p>I'm Ryan, the founder of Untangle. I noticed you practice family law in CT and wanted to reach out.</p>",
            "<p>I built Untangle because I watched my two sisters go through really tough divorces. It helps CT residents answer non-legal divorce questions and correctly fill out all their court forms - which can be a big time-saver for attorneys whose clients need help with paperwork.</p>",
            "<p>Would you be open to a quick 10-minute call? I'd love to hear how you're handling form prep now and whether Untangle could be useful for your clients.</p>",
            '<p>All the best,<br>Ryan</p><p>Founder, <a href="https://untangle.us">Untangle</a></p>',
        ]
    )


def render_template(kind: str, first_name: str) -> dict[str, str]:
    template = template_for_kind(kind)
    if kind == COACH_THERAPIST_TEMPLATE.kind:
        body_text = coach_therapist_plain(first_name)
        body_html = coach_therapist_html(first_name)
    elif kind == ATTORNEY_TEMPLATE.kind:
        body_text = attorney_plain(first_name)
        body_html = attorney_html(first_name)
    else:
        raise ValueError(f"Unsupported outreach template kind: {kind}")
    return {
        "kind": template.kind,
        "subject": template.subject,
        "body_text": body_text,
        "body_html": body_html,
        "from_addr": RYAN_FROM,
        "default_cc": template.default_cc,
    }


def render(args: argparse.Namespace) -> dict[str, str]:
    kind = normalize_kind(args.kind, args.role)
    return render_template(kind, args.first_name)


def slugify(value: str) -> str:
    lowered = value.lower()
    chars = [char if char.isalnum() else "-" for char in lowered]
    slug = "".join(chars).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "contact"


def followup_due_date() -> str:
    return (datetime.now(DEFAULT_TZ).date() + timedelta(days=3)).isoformat()


def build_followup_task_payload(*, first_name: str, to_email: str) -> dict[str, str]:
    slug_source = slugify(f"{first_name}-{to_email}")
    return {
        "content": f"Follow up with {first_name} about Untangle outreach",
        "owner": "ryan",
        "section": DEFAULT_SECTION,
        "priority": "2",
        "due_date": followup_due_date(),
        "metadata_key": f"bd-initial-followup-{slug_source}",
        "meta_program": DEFAULT_PROGRAM,
        "meta_source": "initial_outreach",
        "meta_kind": "bd_initial_followup",
        "meta_contact_email": to_email,
    }


def upsert_followup_task(*, first_name: str, to_email: str) -> dict[str, object]:
    payload = build_followup_task_payload(first_name=first_name, to_email=to_email)
    command = [
        "python3",
        str(TODOIST_CLI_PATH),
        "upsert-task",
        "--content",
        payload["content"],
        "--owner",
        payload["owner"],
        "--section",
        payload["section"],
        "--priority",
        payload["priority"],
        "--due-date",
        payload["due_date"],
        "--metadata-key",
        payload["metadata_key"],
        "--meta",
        f'program={payload["meta_program"]}',
        "--meta",
        f'source={payload["meta_source"]}',
        "--meta",
        f'kind={payload["meta_kind"]}',
        "--meta",
        f'contact_email={payload["meta_contact_email"]}',
    ]
    proc = subprocess.run(command, capture_output=True, text=True)
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or "Failed to create follow-up task"
        raise RuntimeError(message)
    return json.loads(proc.stdout)


def send(args: argparse.Namespace) -> dict[str, object]:
    rendered = render(args)
    cc = "" if args.no_default_cc else rendered["default_cc"]
    if args.cc:
        cc = args.cc
    if args.dry_run:
        followup = build_followup_task_payload(first_name=args.first_name, to_email=args.to)
        return {
            "dry_run": True,
            "kind": rendered["kind"],
            "subject": rendered["subject"],
            "to": args.to,
            "cc": cc,
            "from_addr": rendered["from_addr"],
            "body_html": rendered["body_html"],
            "followup_task": followup,
        }
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as handle:
        body_path = Path(handle.name)
        handle.write(rendered["body_html"])
    command = [
        "python3",
        str(EA_GMAIL_PATH),
        "--account",
        rendered["from_addr"],
        "send",
        "--to",
        args.to,
        "--subject",
        rendered["subject"],
        "--body-file",
        str(body_path),
        "--from",
        rendered["from_addr"],
        "--html",
    ]
    if cc:
        command.extend(["--cc", cc])
    try:
        proc = subprocess.run(command, capture_output=True, text=True)
    finally:
        body_path.unlink(missing_ok=True)
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or "Failed to send outreach email"
        raise RuntimeError(message)
    payload = json.loads(proc.stdout)
    payload["kind"] = rendered["kind"]
    payload["subject"] = rendered["subject"]
    payload["to"] = args.to
    payload["cc"] = cc
    payload["from_addr"] = rendered["from_addr"]
    payload["followup_task"] = upsert_followup_task(first_name=args.first_name, to_email=args.to)
    return payload


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Business-development outreach helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    render_parser = subparsers.add_parser("render")
    render_parser.add_argument("--kind", choices=[COACH_THERAPIST_TEMPLATE.kind, ATTORNEY_TEMPLATE.kind], default="")
    render_parser.add_argument("--role", default="")
    render_parser.add_argument("--first-name", required=True)

    send_parser = subparsers.add_parser("send")
    send_parser.add_argument("--kind", choices=[COACH_THERAPIST_TEMPLATE.kind, ATTORNEY_TEMPLATE.kind], default="")
    send_parser.add_argument("--role", default="")
    send_parser.add_argument("--first-name", required=True)
    send_parser.add_argument("--to", required=True)
    send_parser.add_argument("--cc", default="")
    send_parser.add_argument("--no-default-cc", action="store_true")
    send_parser.add_argument("--dry-run", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "render":
            result = render(args)
        elif args.command == "send":
            result = send(args)
        else:
            raise AssertionError(f"Unhandled command: {args.command}")
    except (RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
