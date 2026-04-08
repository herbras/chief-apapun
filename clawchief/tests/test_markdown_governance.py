import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLAWCHIEF_ROOT = REPO_ROOT / "clawchief"
CRON_PATH = REPO_ROOT / "cron" / "jobs.template.json"


class MarkdownGovernanceTest(unittest.TestCase):
    def test_priority_map_owns_routing_not_task_mechanics(self) -> None:
        text = (CLAWCHIEF_ROOT / "priority-map.md").read_text()
        self.assertIn("## Ownership boundary", text)
        self.assertIn("This file owns:", text)
        self.assertIn("This file does not own:", text)
        self.assertIn("task storage mechanics", text)
        self.assertIn("general inbox, scheduling, travel, calendar integrity, or operational coordination -> `executive-assistant`", text)
        self.assertIn("partner / referral / prospect pipeline, outreach tracker, lead verification, or prospecting batch work -> `business-development`", text)
        self.assertNotIn("## Default routing rules\n\nTBD", text)

    def test_auto_resolver_stays_scoped_to_action_mode(self) -> None:
        text = (CLAWCHIEF_ROOT / "auto-resolver.md").read_text()
        self.assertIn("## Ownership boundary", text)
        self.assertIn("action mode selection after classification", text)
        self.assertIn("This file does not own:", text)
        self.assertIn("cron trigger timing", text)
        self.assertIn("task schema or Todoist field conventions", text)

    def test_location_awareness_stays_scoped_to_place_constraints(self) -> None:
        text = (CLAWCHIEF_ROOT / "location-awareness.md").read_text()
        self.assertIn("## Ownership boundary", text)
        self.assertIn("place-based actionability", text)
        self.assertIn("This file does not own:", text)
        self.assertIn("urgency ranking", text)
        self.assertIn("The executive-assistant workflow should use this rule before offering times", text)

    def test_meeting_notes_uses_cron_as_primary_trigger(self) -> None:
        text = (CLAWCHIEF_ROOT / "meeting-notes.md").read_text()
        self.assertIn("The recurring executive-assistant sweep cron is the canonical dependable trigger", text)
        self.assertIn("reliability must not depend on heartbeats", text)
        self.assertIn("## Ownership boundary", text)
        self.assertIn("## Trigger rule", text)
        self.assertIn("Primary trigger:", text)
        self.assertIn("~/.openclaw/cron/jobs.json", text)

    def test_knowledge_compiler_defines_trigger_hierarchy_and_cron_determinism(self) -> None:
        text = (CLAWCHIEF_ROOT / "knowledge-compiler.md").read_text()
        self.assertIn("## Trigger hierarchy", text)
        self.assertIn("Scheduled crons are the dependable triggers for recurring behavior.", text)
        self.assertIn("heartbeat / opportunistic runs for bonus maintenance or extra coverage", text)
        self.assertIn("## Cron determinism", text)
        self.assertIn("let the cron be the dependable trigger", text)
        self.assertIn("prefer deterministic sweeps over open-ended exploration", text)
        self.assertIn("use the existing owning skill", text)

    def test_crons_encode_deterministic_trigger_language(self) -> None:
        jobs = json.loads(CRON_PATH.read_text())["jobs"]
        by_name = {job["name"]: job for job in jobs}

        ea_message = by_name["Executive assistant sweep"]["payload"]["message"]
        self.assertIn("Use the existing executive-assistant skill", ea_message)
        self.assertIn("This cron is the dependable trigger for recurring EA work", ea_message)
        self.assertIn("Rely on the existing skill for the detailed sweep procedure", ea_message)
        self.assertIn("Keep the run bounded and deterministic", ea_message)

        bd_message = by_name["Untangle daily prospecting"]["payload"]["message"]
        self.assertIn("Use the existing business-development skill", bd_message)
        self.assertIn("This cron is the dependable trigger for the recurring BD batch", bd_message)
        self.assertIn("Rely on the existing skill for the detailed procedure", bd_message)
        self.assertIn("Keep the run bounded and deterministic", bd_message)

        prep_job = by_name["Daily task prep"]
        prep_message = prep_job["payload"]["message"]
        self.assertIn("Use the existing daily-task-prep skill", prep_message)
        self.assertIn("This cron is the dependable trigger for morning task curation", prep_message)
        self.assertIn("Rely on the existing skill for the detailed procedure", prep_message)
        self.assertEqual(prep_job["payload"]["timeoutSeconds"], 900)


if __name__ == "__main__":
    unittest.main()
