import importlib.util
import sys
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "sheet_helper.py"
SPEC = importlib.util.spec_from_file_location("sheet_helper", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
sheet_helper = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sheet_helper
SPEC.loader.exec_module(sheet_helper)


class SheetHelperTest(unittest.TestCase):
    def make_sheet(self, *rows: list[str]) -> dict[str, list[list[str]]]:
        return {"values": [sheet_helper.LEADS_HEADERS, *rows]}

    def test_profile_account_for_email_defaults_to_r2(self) -> None:
        self.assertEqual(sheet_helper.profile_account_for_email("r2@untangle.us"), sheet_helper.DEFAULT_ACCOUNT)
        self.assertEqual(sheet_helper.profile_account_for_email("ryan@ryancarson.com"), "ryan@ryancarson.com")

    def test_read_values_arg_prefers_file_when_present(self) -> None:
        with patch.object(sheet_helper.Path, "read_text", return_value='[["a"]]') as read_mock:
            result = sheet_helper.read_values_arg("", "/tmp/values.json")

        self.assertEqual(result, '[["a"]]')
        read_mock.assert_called_once()

    def test_main_requires_values_for_update_and_append(self) -> None:
        with patch.object(sys, "argv", ["sheet_helper.py", "update", "--spreadsheet", "id", "--range", "A1"]):
            self.assertEqual(sheet_helper.main(), 2)

        with patch.object(sys, "argv", ["sheet_helper.py", "append", "--spreadsheet", "id", "--range", "A1"]):
            self.assertEqual(sheet_helper.main(), 2)

    def test_main_read_uses_gws_path(self) -> None:
        with (
            patch.object(sheet_helper, "gws_read", return_value={"range": "Leads!A:R"}) as gws_mock,
            patch.object(sys, "argv", ["sheet_helper.py", "read", "--spreadsheet", "sheet-1", "--range", "Leads!A:R"]),
            patch("builtins.print"),
        ):
            exit_code = sheet_helper.main()

        self.assertEqual(exit_code, 0)
        gws_mock.assert_called_once_with("sheet-1", "Leads!A:R", profile_account=sheet_helper.DEFAULT_ACCOUNT)

    def test_lead_upsert_create_dry_run_sets_date_added_and_note(self) -> None:
        args = Namespace(
            spreadsheet="sheet-1",
            field=[
                "Full name=Jane Doe",
                "First=Jane",
                "Last=Doe",
                "Email=jane@example.com",
                "Role=Marriage counselor",
            ],
            match_field=[],
            clear_field=[],
            append_r2_note="2026-04-07: initial outreach sent from Ryan.",
            append_ryan_note="",
            mode="upsert",
            allow_identity_overwrite=False,
            dry_run=True,
            account=sheet_helper.DEFAULT_ACCOUNT,
        )
        with patch.object(sheet_helper, "gws_read", return_value=self.make_sheet()):
            result = sheet_helper.lead_upsert(args)

        self.assertEqual(result["action"], "create")
        self.assertTrue(result["record"]["Date added"])
        self.assertEqual(result["record"]["Email"], "jane@example.com")
        self.assertEqual(result["record"]["R2's Notes"], "2026-04-07: initial outreach sent from Ryan.")

    def test_lead_upsert_update_preserves_existing_fields_and_appends_note(self) -> None:
        existing = [
            "Jane Doe",
            "Jane",
            "Doe",
            "Marriage counselor",
            "https://example.com",
            "jane@example.com",
            "555-0100",
            "Hartford, CT",
            "No",
            "No",
            "No",
            "No",
            "",
            "Ryan note",
            "2026-04-06: existing note",
            "2026-04-06",
            "untangle.us/team/jane",
            "Ready for Ryan outreach",
        ]
        args = Namespace(
            spreadsheet="sheet-1",
            field=[
                "Email sent=Yes",
                "Status=Waiting for reply",
                "Email=jane@example.com",
            ],
            match_field=[],
            clear_field=[],
            append_r2_note="2026-04-07: outreach sent with coach_therapist template.",
            append_ryan_note="",
            mode="upsert",
            allow_identity_overwrite=False,
            dry_run=False,
            account=sheet_helper.DEFAULT_ACCOUNT,
        )
        with (
            patch.object(sheet_helper, "gws_read", return_value=self.make_sheet(existing)),
            patch.object(sheet_helper, "gws_update", return_value={"updatedRange": "Leads!A2:R2"}) as update_mock,
        ):
            result = sheet_helper.lead_upsert(args)

        self.assertEqual(result["action"], "update")
        write_args = update_mock.call_args[0][0]
        written = sheet_helper.json.loads(write_args.values_json)[0]
        record = {column: written[index] for index, column in enumerate(sheet_helper.LEADS_HEADERS)}
        self.assertEqual(record["Phone"], "555-0100")
        self.assertEqual(record["Partner link"], "untangle.us/team/jane")
        self.assertEqual(record["Ryan's Notes"], "Ryan note")
        self.assertIn("2026-04-06: existing note", record["R2's Notes"])
        self.assertIn("2026-04-07: outreach sent with coach_therapist template.", record["R2's Notes"])
        self.assertEqual(record["Email sent"], "Yes")
        self.assertEqual(record["Status"], "Waiting for reply")

    def test_lead_upsert_refuses_ambiguous_duplicate_match(self) -> None:
        duplicate_a = [
            "Jane Doe",
            "Jane",
            "Doe",
            "",
            "https://example.com",
            "jane@example.com",
            "",
            "",
            "No",
            "No",
            "No",
            "No",
            "",
            "",
            "",
            "2026-04-06",
            "",
            "Ready for Ryan outreach",
        ]
        duplicate_b = list(duplicate_a)
        duplicate_b[14] = "2026-04-07: duplicate row"
        args = Namespace(
            spreadsheet="sheet-1",
            field=["Email=jane@example.com", "Status=Waiting for reply"],
            match_field=[],
            clear_field=[],
            append_r2_note="",
            append_ryan_note="",
            mode="upsert",
            allow_identity_overwrite=False,
            dry_run=True,
            account=sheet_helper.DEFAULT_ACCOUNT,
        )
        with patch.object(sheet_helper, "gws_read", return_value=self.make_sheet(duplicate_a, duplicate_b)):
            with self.assertRaises(sheet_helper.LeadSheetError):
                sheet_helper.lead_upsert(args)

    def test_lead_upsert_refuses_overwriting_non_empty_identity_fields(self) -> None:
        existing = [
            "Jane Doe",
            "Jane",
            "Doe",
            "",
            "https://example.com",
            "jane@old.example.com",
            "",
            "",
            "No",
            "No",
            "No",
            "No",
            "",
            "",
            "",
            "2026-04-06",
            "",
            "Ready for Ryan outreach",
        ]
        args = Namespace(
            spreadsheet="sheet-1",
            field=[
                "Website=https://example.com",
                "Email=jane@new.example.com",
                "Status=Waiting for reply",
            ],
            match_field=[],
            clear_field=[],
            append_r2_note="",
            append_ryan_note="",
            mode="upsert",
            allow_identity_overwrite=False,
            dry_run=True,
            account=sheet_helper.DEFAULT_ACCOUNT,
        )
        with patch.object(sheet_helper, "gws_read", return_value=self.make_sheet(existing)):
            with self.assertRaises(sheet_helper.LeadSheetError):
                sheet_helper.lead_upsert(args)


if __name__ == "__main__":
    unittest.main()
