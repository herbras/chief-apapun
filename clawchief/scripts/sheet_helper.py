#!/usr/bin/env python3

"""Clawchief Sheets helper.

This wrapper gives skills one stable Google Sheets command surface built on `gws`.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any
from types import SimpleNamespace
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo


DEFAULT_ACCOUNT = "r2@untangle.us"
RYAN_PROFILE_ACCOUNT = "ryan@ryancarson.com"
PROFILE_CONFIG_DIRS = {
    DEFAULT_ACCOUNT: Path.home() / ".config" / "gws-r2",
    RYAN_PROFILE_ACCOUNT: Path.home() / ".config" / "gws-ryan",
}
PROFILE_CREDENTIAL_FILES = {
    account: config_dir / "credentials.json" for account, config_dir in PROFILE_CONFIG_DIRS.items()
}
DEFAULT_TZ = ZoneInfo("America/New_York")
LEADS_SHEET_RANGE = "Leads!A:R"
LEADS_HEADERS = [
    "Full name",
    "First",
    "Last",
    "Role",
    "Website",
    "Email",
    "Phone",
    "Location",
    "Email sent",
    "LI sent",
    "LI accepted",
    "Meeting booked",
    "LinkedIn",
    "Ryan's Notes",
    "R2's Notes",
    "Date added",
    "Partner link",
    "Status",
]
NOTE_COLUMNS = {"Ryan's Notes", "R2's Notes"}
IDENTITY_COLUMNS = {"Full name", "First", "Last", "Website", "Email", "LinkedIn"}
YES_NO_COLUMNS = {"Email sent", "LI sent", "LI accepted", "Meeting booked"}


class LeadSheetError(Exception):
    """Raised when a lead upsert cannot be completed safely."""


@dataclass
class CommandFailure(Exception):
    command: list[str]
    returncode: int
    stdout: str
    stderr: str

    def combined_output(self) -> str:
        return "\n".join(part for part in (self.stdout.strip(), self.stderr.strip()) if part)


def profile_account_for_email(email: str) -> str:
    normalized = email.strip().lower()
    if normalized == RYAN_PROFILE_ACCOUNT:
        return RYAN_PROFILE_ACCOUNT
    return DEFAULT_ACCOUNT


def gws_env(profile_account: str) -> dict[str, str]:
    env = os.environ.copy()
    config_dir = PROFILE_CONFIG_DIRS.get(profile_account, PROFILE_CONFIG_DIRS[DEFAULT_ACCOUNT])
    env["GOOGLE_WORKSPACE_CLI_CONFIG_DIR"] = str(config_dir)
    env["GOOGLE_WORKSPACE_CLI_KEYRING_BACKEND"] = "file"
    credentials_file = PROFILE_CREDENTIAL_FILES.get(profile_account)
    if credentials_file and credentials_file.exists():
        env["GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE"] = str(credentials_file)
    return env


def run(command: list[str], *, expect_json: bool = False, profile_account: str = DEFAULT_ACCOUNT) -> Any:
    proc = subprocess.run(command, capture_output=True, text=True, env=gws_env(profile_account))
    if proc.returncode != 0:
        raise CommandFailure(command, proc.returncode, proc.stdout, proc.stderr)
    if not expect_json:
        return proc.stdout
    text = proc.stdout.strip()
    if not text:
        return {}
    return json.loads(text)


def read_values_arg(values_json: str, values_file: str) -> str:
    if values_file:
        return Path(values_file).read_text()
    return values_json


def simplify_column_name(value: str) -> str:
    return "".join(char for char in value.lower() if char.isalnum())


COLUMN_ALIASES = {simplify_column_name(column): column for column in LEADS_HEADERS}


def canonical_column_name(name: str) -> str:
    normalized = name.strip()
    if normalized in LEADS_HEADERS:
        return normalized
    simplified = simplify_column_name(normalized)
    if simplified in COLUMN_ALIASES:
        return COLUMN_ALIASES[simplified]
    raise LeadSheetError(f"Unknown lead column: {name}")


def parse_assignments(raw_pairs: list[str] | None) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw in raw_pairs or []:
        if "=" not in raw:
            raise LeadSheetError(f"Expected Column=Value assignment, got: {raw}")
        key, value = raw.split("=", 1)
        column = canonical_column_name(key)
        if column in parsed:
            raise LeadSheetError(f"Duplicate assignment for column: {column}")
        parsed[column] = value
    return parsed


def parse_clear_fields(raw_fields: list[str] | None) -> set[str]:
    return {canonical_column_name(value) for value in (raw_fields or [])}


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_url(value: str) -> str:
    raw = value.strip()
    if not raw:
        return ""
    candidate = raw if "://" in raw else f"https://{raw}"
    parts = urlsplit(candidate)
    host = parts.netloc.lower().lstrip()
    if host.startswith("www."):
        host = host[4:]
    path = parts.path.rstrip("/")
    return f"{host}{path}".rstrip("/")


def normalize_name_piece(value: str) -> str:
    cleaned = value.split(",", 1)[0].strip().lower()
    tokens = []
    current = []
    for char in cleaned:
        if char.isalnum():
            current.append(char)
        elif current:
            tokens.append("".join(current))
            current = []
    if current:
        tokens.append("".join(current))
    return " ".join(tokens)


def normalize_yes_no(value: str) -> str:
    lowered = value.strip().lower()
    if lowered in {"yes", "y", "true"}:
        return "Yes"
    if lowered in {"no", "n", "false"}:
        return "No"
    return value


def canonical_person_name(row: dict[str, str]) -> str:
    first = normalize_name_piece(row.get("First", ""))
    last = normalize_name_piece(row.get("Last", ""))
    if first or last:
        return " ".join(part for part in (first, last) if part).strip()
    return normalize_name_piece(row.get("Full name", ""))


def validate_leads_header(values: list[list[str]]) -> list[list[str]]:
    if not values:
        raise LeadSheetError("Leads sheet is empty; cannot verify schema.")
    header = values[0]
    if header != LEADS_HEADERS:
        raise LeadSheetError(
            "Leads header mismatch. Refusing blind write.\n"
            f"Expected: {LEADS_HEADERS}\n"
            f"Found: {header}"
        )
    return values[1:]


def row_to_record(row: list[str]) -> dict[str, str]:
    padded = list(row) + [""] * max(0, len(LEADS_HEADERS) - len(row))
    return {column: str(padded[index]) for index, column in enumerate(LEADS_HEADERS)}


def derive_match_hints(fields: dict[str, str], explicit: dict[str, str]) -> dict[str, str]:
    hints = dict(explicit)
    for column in IDENTITY_COLUMNS:
        if column not in hints and fields.get(column):
            hints[column] = fields[column]
    return hints


def row_match_score(row: dict[str, str], hints: dict[str, str]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    if hints.get("Email") and normalize_email(row.get("Email", "")) == normalize_email(hints["Email"]):
        score += 100
        reasons.append("Email")
    if hints.get("Website") and normalize_url(row.get("Website", "")) == normalize_url(hints["Website"]):
        score += 80
        reasons.append("Website")
    if hints.get("LinkedIn") and normalize_url(row.get("LinkedIn", "")) == normalize_url(hints["LinkedIn"]):
        score += 70
        reasons.append("LinkedIn")

    row_name = canonical_person_name(row)
    hint_name = canonical_person_name(hints)
    if row_name and hint_name and row_name == hint_name:
        score += 30
        reasons.append("Name")
    return score, reasons


def find_matching_row(rows: list[list[str]], hints: dict[str, str]) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=2):
        record = row_to_record(row)
        score, reasons = row_match_score(record, hints)
        if score > 0:
            candidates.append(
                {
                    "row_number": index,
                    "record": record,
                    "score": score,
                    "reasons": reasons,
                }
            )
    if not candidates:
        return None
    candidates.sort(key=lambda item: (-item["score"], item["row_number"]))
    if len(candidates) == 1:
        return candidates[0]
    if candidates[0]["score"] > candidates[1]["score"] and candidates[0]["score"] >= 80:
        return candidates[0]
    lines = [
        f"row {candidate['row_number']}: matched by {', '.join(candidate['reasons'])}; "
        f"Email={candidate['record'].get('Email', '')!r}; Website={candidate['record'].get('Website', '')!r}; "
        f"Name={candidate['record'].get('Full name', '')!r}; Status={candidate['record'].get('Status', '')!r}"
        for candidate in candidates
    ]
    raise LeadSheetError("Ambiguous lead match; refusing write.\n" + "\n".join(lines))


def ensure_identity_is_safe(
    existing: dict[str, str],
    fields: dict[str, str],
    *,
    allow_identity_overwrite: bool,
) -> None:
    if allow_identity_overwrite:
        return
    for column in ("Email", "Website", "LinkedIn"):
        incoming = fields.get(column, "").strip()
        current = existing.get(column, "").strip()
        if not incoming or not current:
            continue
        normalizer = normalize_email if column == "Email" else normalize_url
        if normalizer(incoming) != normalizer(current):
            raise LeadSheetError(
                f"Refusing to overwrite non-empty identity field {column!r}: "
                f"existing={current!r}, incoming={incoming!r}"
            )

    incoming_name = canonical_person_name(fields)
    existing_name = canonical_person_name(existing)
    if incoming_name and existing_name and incoming_name != existing_name:
        raise LeadSheetError(
            f"Refusing to overwrite non-empty identity field 'Name': existing={existing_name!r}, incoming={incoming_name!r}"
        )


def append_note(existing: str, new_note: str) -> str:
    note = new_note.strip()
    if not note:
        return existing
    lines = [line for line in existing.splitlines() if line.strip()]
    if note in lines:
        return existing
    lines.append(note)
    return "\n".join(lines)


def merge_lead_record(
    base: dict[str, str],
    fields: dict[str, str],
    *,
    clear_fields: set[str],
    append_r2_note: str,
    append_ryan_note: str,
    is_create: bool,
) -> dict[str, str]:
    merged = dict(base)
    for column in clear_fields:
        merged[column] = ""
    for column, value in fields.items():
        if value == "":
            continue
        merged[column] = normalize_yes_no(value) if column in YES_NO_COLUMNS else value
    if append_ryan_note:
        merged["Ryan's Notes"] = append_note(merged.get("Ryan's Notes", ""), append_ryan_note)
    if append_r2_note:
        merged["R2's Notes"] = append_note(merged.get("R2's Notes", ""), append_r2_note)
    if is_create and not merged.get("Date added", "").strip():
        merged["Date added"] = datetime.now(DEFAULT_TZ).date().isoformat()
    return merged


def namespace_for_write(*, spreadsheet: str, cell_range: str, values: list[list[str]], account: str) -> SimpleNamespace:
    return SimpleNamespace(
        spreadsheet=spreadsheet,
        range=cell_range,
        values_json=json.dumps(values),
        values_file="",
        value_input_option="USER_ENTERED",
        insert_data_option="INSERT_ROWS",
        account=account,
    )


def lead_upsert(args: argparse.Namespace) -> Any:
    if not args.field and not args.clear_field and not args.append_r2_note and not args.append_ryan_note:
        raise LeadSheetError("Provide at least one field change or note append for lead-upsert.")

    fields = parse_assignments(args.field)
    match_fields = parse_assignments(args.match_field)
    clear_fields = parse_clear_fields(args.clear_field)
    hints = derive_match_hints(fields, match_fields)
    if not hints:
        raise LeadSheetError(
            "lead-upsert requires at least one identity hint via --field or --match-field "
            "(Email, Website, LinkedIn, Full name, or First/Last)."
        )

    sheet = gws_read(args.spreadsheet, LEADS_SHEET_RANGE, profile_account=profile_account_for_email(args.account))
    rows = validate_leads_header(sheet.get("values", []))
    match = find_matching_row(rows, hints)
    if args.mode == "create-only" and match is not None:
        raise LeadSheetError(f"Lead already exists at row {match['row_number']}; refusing create-only write.")
    if args.mode == "update-only" and match is None:
        raise LeadSheetError("No existing lead matched the provided identity hints.")

    if match is None:
        base = {column: "" for column in LEADS_HEADERS}
        action = "create"
        row_number = None
    else:
        base = match["record"]
        ensure_identity_is_safe(
            base,
            fields,
            allow_identity_overwrite=args.allow_identity_overwrite,
        )
        action = "update"
        row_number = match["row_number"]

    merged = merge_lead_record(
        base,
        fields,
        clear_fields=clear_fields,
        append_r2_note=args.append_r2_note,
        append_ryan_note=args.append_ryan_note,
        is_create=match is None,
    )
    row_values = [[merged[column] for column in LEADS_HEADERS]]
    response: dict[str, Any] = {
        "action": action,
        "row_number": row_number,
        "matched_by": [] if match is None else match["reasons"],
        "record": merged,
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        return response

    if action == "create":
        write_result = gws_append(namespace_for_write(
            spreadsheet=args.spreadsheet,
            cell_range=LEADS_SHEET_RANGE,
            values=row_values,
            account=args.account,
        ))
    else:
        write_result = gws_update(namespace_for_write(
            spreadsheet=args.spreadsheet,
            cell_range=f"Leads!A{row_number}:R{row_number}",
            values=row_values,
            account=args.account,
        ))
    response["write_result"] = write_result
    return response


def gws_read(spreadsheet_id: str, cell_range: str, *, profile_account: str) -> Any:
    return run(
        [
            "gws",
            "sheets",
            "spreadsheets",
            "values",
            "get",
            "--params",
            json.dumps({"spreadsheetId": spreadsheet_id, "range": cell_range}),
            "--format",
            "json",
        ],
        expect_json=True,
        profile_account=profile_account,
    )


def gws_update(args: argparse.Namespace) -> Any:
    values = json.loads(read_values_arg(args.values_json, args.values_file))
    return run(
        [
            "gws",
            "sheets",
            "spreadsheets",
            "values",
            "update",
            "--params",
            json.dumps(
                {
                    "spreadsheetId": args.spreadsheet,
                    "range": args.range,
                    "valueInputOption": args.value_input_option,
                    "includeValuesInResponse": True,
                }
            ),
            "--json",
            json.dumps({"values": values}),
            "--format",
            "json",
        ],
        expect_json=True,
        profile_account=profile_account_for_email(args.account),
    )


def gws_append(args: argparse.Namespace) -> Any:
    values = json.loads(read_values_arg(args.values_json, args.values_file))
    return run(
        [
            "gws",
            "sheets",
            "spreadsheets",
            "values",
            "append",
            "--params",
            json.dumps(
                {
                    "spreadsheetId": args.spreadsheet,
                    "range": args.range,
                    "valueInputOption": args.value_input_option,
                    "insertDataOption": args.insert_data_option,
                    "includeValuesInResponse": True,
                }
            ),
            "--json",
            json.dumps({"values": values}),
            "--format",
            "json",
        ],
        expect_json=True,
        profile_account=profile_account_for_email(args.account),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Clawchief Sheets helper")
    parser.add_argument("--account", default=DEFAULT_ACCOUNT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("--spreadsheet", required=True)
    read_parser.add_argument("--range", required=True)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--spreadsheet", required=True)
    update_parser.add_argument("--range", required=True)
    update_parser.add_argument("--values-json", default="")
    update_parser.add_argument("--values-file", default="")
    update_parser.add_argument("--value-input-option", default="USER_ENTERED")

    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("--spreadsheet", required=True)
    append_parser.add_argument("--range", required=True)
    append_parser.add_argument("--values-json", default="")
    append_parser.add_argument("--values-file", default="")
    append_parser.add_argument("--value-input-option", default="USER_ENTERED")
    append_parser.add_argument("--insert-data-option", default="INSERT_ROWS")

    lead_upsert_parser = subparsers.add_parser("lead-upsert")
    lead_upsert_parser.add_argument("--spreadsheet", required=True)
    lead_upsert_parser.add_argument("--field", action="append", default=[])
    lead_upsert_parser.add_argument("--match-field", action="append", default=[])
    lead_upsert_parser.add_argument("--clear-field", action="append", default=[])
    lead_upsert_parser.add_argument("--append-r2-note", default="")
    lead_upsert_parser.add_argument("--append-ryan-note", default="")
    lead_upsert_parser.add_argument("--mode", choices=["upsert", "update-only", "create-only"], default="upsert")
    lead_upsert_parser.add_argument("--allow-identity-overwrite", action="store_true")
    lead_upsert_parser.add_argument("--dry-run", action="store_true")

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command in {"update", "append"} and not args.values_json and not args.values_file:
        print("Provide either --values-json or --values-file", file=sys.stderr)
        return 2
    try:
        if args.command == "read":
            result = gws_read(
                args.spreadsheet,
                args.range,
                profile_account=profile_account_for_email(args.account),
            )
        elif args.command == "update":
            result = gws_update(args)
        elif args.command == "append":
            result = gws_append(args)
        elif args.command == "lead-upsert":
            result = lead_upsert(args)
        else:
            raise AssertionError(f"Unhandled command: {args.command}")
    except CommandFailure as exc:
        print(exc.combined_output() or f"Command failed: {' '.join(exc.command)}", file=sys.stderr)
        return exc.returncode
    except LeadSheetError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
