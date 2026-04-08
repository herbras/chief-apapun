import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "ea_gmail.py"
SPEC = importlib.util.spec_from_file_location("ea_gmail", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ea_gmail = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ea_gmail
SPEC.loader.exec_module(ea_gmail)


class EaGmailWrapperTest(unittest.TestCase):
    def test_profile_account_for_email_routes_ryan_owned_addresses(self) -> None:
        self.assertEqual(ea_gmail.profile_account_for_email("ryan@ryancarson.com"), "ryan@ryancarson.com")
        self.assertEqual(ea_gmail.profile_account_for_email("hello@untangle.us"), "ryan@ryancarson.com")
        self.assertEqual(ea_gmail.profile_account_for_email("r2@untangle.us"), ea_gmail.DEFAULT_ACCOUNT)

    def test_reply_with_gws_builds_reply_all_command(self) -> None:
        with patch.object(ea_gmail, "run", return_value={"id": "sent-1"}) as run_mock:
            result = ea_gmail.reply_with_gws(
                message_id="19d698676770653a",
                body="Yep — reply works.",
                reply_all=True,
                profile_account=ea_gmail.DEFAULT_ACCOUNT,
                cc="hello@untangle.us",
            )

        self.assertEqual(result, {"id": "sent-1"})
        run_mock.assert_called_once_with(
            [
                "gws",
                "gmail",
                "+reply-all",
                "--message-id",
                "19d698676770653a",
                "--body",
                "Yep — reply works.",
                "--cc",
                "hello@untangle.us",
            ],
            expect_json=True,
            profile_account=ea_gmail.DEFAULT_ACCOUNT,
        )

    def test_send_with_gws_supports_html(self) -> None:
        with patch.object(ea_gmail, "run", return_value={"id": "sent-1"}) as run_mock:
            result = ea_gmail.send_with_gws(
                to="jane@example.com",
                subject="Hello",
                body="<p>Hi</p>",
                profile_account="ryan@ryancarson.com",
                html=True,
                from_addr="ryan@ryancarson.com",
            )

        self.assertEqual(result, {"id": "sent-1"})
        run_mock.assert_called_once_with(
            [
                "gws",
                "gmail",
                "+send",
                "--to",
                "jane@example.com",
                "--subject",
                "Hello",
                "--body",
                "<p>Hi</p>",
                "--html",
                "--from",
                "ryan@ryancarson.com",
            ],
            expect_json=True,
            profile_account="ryan@ryancarson.com",
        )

    def test_normalize_search_result_accepts_gws_message_envelope(self) -> None:
        self.assertEqual(
            ea_gmail.normalize_search_result({"messages": [{"id": "m1"}, {"id": "m2"}]}),
            [{"id": "m1"}, {"id": "m2"}],
        )

    def test_main_thread_uses_gws_path(self) -> None:
        with (
            patch.object(ea_gmail, "gws_thread", return_value={"id": "thread-1"}) as gws_thread_mock,
            patch.object(sys, "argv", ["ea_gmail.py", "thread", "--thread-id", "thread-1"]),
            patch("builtins.print"),
        ):
            exit_code = ea_gmail.main()

        self.assertEqual(exit_code, 0)
        gws_thread_mock.assert_called_once_with("thread-1", profile_account=ea_gmail.DEFAULT_ACCOUNT)


if __name__ == "__main__":
    unittest.main()
