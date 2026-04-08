import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ea_calendar.py"
SPEC = importlib.util.spec_from_file_location("ea_calendar", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ea_calendar = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ea_calendar
SPEC.loader.exec_module(ea_calendar)


class EaCalendarWrapperTest(unittest.TestCase):
    def test_profile_account_for_email_routes_ryan_owned_addresses(self) -> None:
        self.assertEqual(ea_calendar.profile_account_for_email("ryan@ryancarson.com"), "ryan@ryancarson.com")
        self.assertEqual(ea_calendar.profile_account_for_email("hello@untangle.us"), "ryan@ryancarson.com")
        self.assertEqual(ea_calendar.profile_account_for_email("r2@untangle.us"), ea_calendar.DEFAULT_ACCOUNT)

    def test_build_event_body_adds_attendees_and_meet(self) -> None:
        body, conference_version = ea_calendar.build_event_body(
            summary="Ryan Carson <> Colleen ONeil",
            start="2026-04-08T13:00:00-04:00",
            end="2026-04-08T13:30:00-04:00",
            description="Intro call",
            location="",
            attendees=["colleen@example.com", "r2@untangle.us"],
            meet=True,
        )

        self.assertEqual(conference_version, 1)
        self.assertEqual(body["summary"], "Ryan Carson <> Colleen ONeil")
        self.assertEqual(body["attendees"], [{"email": "colleen@example.com"}, {"email": "r2@untangle.us"}])
        self.assertIn("conferenceData", body)

    def test_build_patch_body_merges_additional_attendees(self) -> None:
        body = ea_calendar.build_patch_body(
            summary=None,
            start="",
            end="",
            description=None,
            location=None,
            attendees=[],
            add_attendees=["r2@untangle.us"],
            current_event={"attendees": [{"email": "colleen@example.com"}]},
        )

        self.assertEqual(
            body["attendees"],
            [{"email": "colleen@example.com"}, {"email": "r2@untangle.us"}],
        )

    def test_build_patch_body_requires_start_and_end_together(self) -> None:
        with self.assertRaises(ValueError):
            ea_calendar.build_patch_body(
                summary=None,
                start="2026-04-08T13:00:00-04:00",
                end="",
                description=None,
                location=None,
                attendees=[],
                add_attendees=[],
                current_event=None,
            )

    def test_normalize_items_unwraps_gws_item_envelope(self) -> None:
        self.assertEqual(
            ea_calendar.normalize_items({"items": [{"id": "cal-1"}]}),
            [{"id": "cal-1"}],
        )

    def test_main_calendars_uses_gws_path(self) -> None:
        with (
            patch.object(ea_calendar, "gws_calendars", return_value=[{"id": "cal-1"}]) as gws_mock,
            patch.object(sys, "argv", ["ea_calendar.py", "calendars"]),
            patch("builtins.print"),
        ):
            exit_code = ea_calendar.main()

        self.assertEqual(exit_code, 0)
        gws_mock.assert_called_once_with(100, "reader", profile_account=ea_calendar.DEFAULT_ACCOUNT)


if __name__ == "__main__":
    unittest.main()
