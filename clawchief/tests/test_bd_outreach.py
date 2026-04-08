import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "bd_outreach.py"
SPEC = importlib.util.spec_from_file_location("bd_outreach", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
bd_outreach = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = bd_outreach
SPEC.loader.exec_module(bd_outreach)


class BdOutreachTest(unittest.TestCase):
    def test_detect_kind_prefers_attorney_for_legal_roles(self) -> None:
        self.assertEqual(bd_outreach.detect_kind("Family law attorney"), "attorney")
        self.assertEqual(bd_outreach.detect_kind("Marriage counselor"), "coach_therapist")

    def test_render_coach_template_includes_linked_signature_and_default_cc(self) -> None:
        result = bd_outreach.render_template("coach_therapist", "Jane")
        self.assertEqual(result["subject"], "Saw your work")
        self.assertEqual(result["default_cc"], "r2@untangle.us")
        self.assertIn('href="https://untangle.us"', result["body_html"])
        self.assertIn("I've copied my assistant here", result["body_text"])

    def test_render_attorney_template_has_expected_subject(self) -> None:
        result = bd_outreach.render_template("attorney", "Jane")
        self.assertEqual(result["subject"], "New divorce assistant for CT residents just launched")
        self.assertEqual(result["default_cc"], "r2@untangle.us")

    def test_send_dry_run_uses_template_defaults(self) -> None:
        args = bd_outreach.build_parser().parse_args(
            ["send", "--role", "Marriage counselor", "--first-name", "Jane", "--to", "jane@example.com", "--dry-run"]
        )
        result = bd_outreach.send(args)
        self.assertEqual(result["kind"], "coach_therapist")
        self.assertEqual(result["cc"], "r2@untangle.us")
        self.assertIn('href="https://untangle.us"', result["body_html"])
        self.assertEqual(result["followup_task"]["owner"], "ryan")
        self.assertEqual(result["followup_task"]["content"], "Follow up with Jane about Untangle outreach")

    def test_build_followup_task_payload_uses_three_day_due_date(self) -> None:
        with patch.object(bd_outreach, "followup_due_date", return_value="2026-04-10"):
            payload = bd_outreach.build_followup_task_payload(first_name="Jane", to_email="jane@example.com")
        self.assertEqual(payload["owner"], "ryan")
        self.assertEqual(payload["due_date"], "2026-04-10")
        self.assertEqual(payload["metadata_key"], "bd-initial-followup-jane-jane-example-com")


if __name__ == "__main__":
    unittest.main()
