import importlib.util
import io
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "todoist_cli.py"
SPEC = importlib.util.spec_from_file_location("todoist_cli", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
todoist_cli = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = todoist_cli
SPEC.loader.exec_module(todoist_cli)


class FakeResponse:
    def __init__(self, status: int, body: bytes) -> None:
        self.status = status
        self._body = body

    def read(self) -> bytes:
        return self._body

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False


def make_http_error(url: str, code: int, payload: bytes) -> urllib.error.HTTPError:
    return urllib.error.HTTPError(url, code, "boom", {}, io.BytesIO(payload))


class TodoistCliRetryTest(unittest.TestCase):
    def test_request_retries_transient_http_errors(self) -> None:
        client = todoist_cli.TodoistClient(token="test-token")
        transient = make_http_error("https://api.todoist.com/api/v1/projects", 503, b'{"error":"bad gateway"}')
        success = FakeResponse(200, b'{"ok": true}')

        with (
            patch.object(todoist_cli.urllib.request, "urlopen", side_effect=[transient, success]),
            patch.object(todoist_cli.time, "sleep") as sleep_mock,
        ):
            result = client.request("GET", "/projects")

        self.assertEqual(result, {"ok": True})
        sleep_mock.assert_called_once()

    def test_sync_retries_transient_http_errors(self) -> None:
        client = todoist_cli.TodoistClient(token="test-token")
        transient = make_http_error("https://api.todoist.com/api/v1/sync", 502, b'{"error":"bad gateway"}')
        success = FakeResponse(200, b'{"sync_status": {}}')

        with (
            patch.object(todoist_cli.urllib.request, "urlopen", side_effect=[transient, success]),
            patch.object(todoist_cli.time, "sleep") as sleep_mock,
        ):
            result = client.sync(resource_types=["user"])

        self.assertEqual(result, {"sync_status": {}})
        sleep_mock.assert_called_once()

    def test_non_transient_http_error_still_raises(self) -> None:
        client = todoist_cli.TodoistClient(token="test-token")
        fatal = make_http_error("https://api.todoist.com/api/v1/projects", 400, b'{"error":"bad request"}')

        with patch.object(todoist_cli.urllib.request, "urlopen", side_effect=[fatal]):
            with self.assertRaises(todoist_cli.TodoistError):
                client.request("GET", "/projects")


class TodoistCliMetadataRegressionTest(unittest.TestCase):
    def test_split_description_and_metadata_parses_metadata_only_block(self) -> None:
        human, metadata = todoist_cli.split_description_and_metadata(
            "---\nkey: partner-followup-charlene-lynton-scheduling\nkind: partner_followup"
        )

        self.assertEqual(human, "")
        self.assertEqual(
            metadata,
            {
                "key": "partner-followup-charlene-lynton-scheduling",
                "kind": "partner_followup",
            },
        )

    def test_upsert_task_matches_existing_metadata_only_description(self) -> None:
        class FakeClient:
            def tasks(self, _filters):
                return [
                    {
                        "id": "existing-task",
                        "content": "Follow up on Charlene Lynton scheduling reply",
                        "description": "---\nkey: partner-followup-charlene-lynton-scheduling\nkind: partner_followup",
                        "section_id": "bd-section",
                        "labels": [],
                        "due": {"date": "2026-04-08"},
                    }
                ]

        with (
            patch.object(todoist_cli, "resolve_project_name", return_value={"id": "project-1"}),
            patch.object(todoist_cli, "resolve_section_id", return_value="bd-section"),
            patch.object(todoist_cli, "resolve_assignee_id", return_value=None),
        ):
            result = todoist_cli.upsert_task(
                FakeClient(),
                project_name="Clawchief",
                content="Follow up with Charlene Lynton on rescheduled meeting time",
                owner="r2",
                section_name="Business development partnerships",
                labels=[],
                priority=2,
                description="Thread: waiting on Charlene to confirm a replacement slot.",
                metadata={"key": "partner-followup-charlene-lynton-scheduling"},
                due={"date": "2026-04-08"},
                deadline=None,
                dry_run=True,
            )

        self.assertEqual(result["action"], "update")
        self.assertEqual(result["task_id"], "existing-task")

    def test_upsert_task_closes_duplicate_metadata_matches(self) -> None:
        class FakeClient:
            def __init__(self) -> None:
                self.closed_ids: list[str] = []

            def tasks(self, _filters):
                return [
                    {
                        "id": "keep-me",
                        "content": "Follow up with Charlene Lynton on rescheduled meeting time",
                        "description": "Thread: waiting on Charlene.\n\n---\nkey: partner-followup-charlene-lynton-scheduling",
                        "section_id": "bd-section",
                        "labels": [],
                        "due": {"date": "2026-04-08"},
                        "updated_at": "2026-04-07T16:07:25.460569Z",
                    },
                    {
                        "id": "old-1",
                        "content": "Follow up on Charlene Lynton scheduling reply",
                        "description": "---\nkey: partner-followup-charlene-lynton-scheduling\nkind: partner_followup",
                        "section_id": "bd-section",
                        "labels": [],
                        "due": {"date": "2026-04-08"},
                        "updated_at": "2026-04-07T15:58:00.000000Z",
                    },
                    {
                        "id": "old-2",
                        "content": "Check Charlene Lynton scheduling reply and finalize a valid time",
                        "description": "---\nkey: partner-followup-charlene-lynton-scheduling\nkind: partner_followup",
                        "section_id": "bd-section",
                        "labels": [],
                        "due": {"date": "2026-04-09"},
                        "updated_at": "2026-04-07T16:01:05.000000Z",
                    },
                ]

            def close_task(self, task_id: str) -> None:
                self.closed_ids.append(task_id)

        client = FakeClient()
        with (
            patch.object(todoist_cli, "resolve_project_name", return_value={"id": "project-1"}),
            patch.object(todoist_cli, "resolve_section_id", return_value="bd-section"),
            patch.object(todoist_cli, "resolve_assignee_id", return_value=None),
            patch.object(todoist_cli, "apply_task_changes", return_value={"id": "keep-me"}),
        ):
            result = todoist_cli.upsert_task(
                client,
                project_name="Clawchief",
                content="Follow up with Charlene Lynton on rescheduled meeting time",
                owner="r2",
                section_name="Business development partnerships",
                labels=[],
                priority=2,
                description="Thread: waiting on Charlene to confirm a replacement slot.",
                metadata={"key": "partner-followup-charlene-lynton-scheduling"},
                due={"date": "2026-04-08"},
                deadline=None,
                dry_run=False,
            )

        self.assertEqual(result["action"], "update")
        self.assertEqual(sorted(client.closed_ids), ["old-1", "old-2"])


if __name__ == "__main__":
    unittest.main()
