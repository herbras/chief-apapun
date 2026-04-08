import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CLAWCHIEF_ROOT = REPO_ROOT / "clawchief"
SKILLS_ROOT = REPO_ROOT / "skills"
CRON_PATH = REPO_ROOT / "cron" / "jobs.template.json"


class TaskSystemContractTest(unittest.TestCase):
    def test_acceptance_doc_is_a_thin_audit_index(self) -> None:
        text = (CLAWCHIEF_ROOT / "task-system-acceptance.md").read_text()
        self.assertIn("audit index", text)
        self.assertIn("~/.openclaw/skills/task-system-contract/SKILL.md", text)
        self.assertIn("Keep this file as an index and audit map, not a second runtime policy document.", text)
        self.assertIn("Todoist is the only live task system", text)

    def test_shared_task_contract_skill_lists_core_criteria(self) -> None:
        text = (SKILLS_ROOT / "task-system-contract" / "SKILL.md").read_text()
        required_phrases = [
            "Todoist is the only live task system for clawchief",
            "When Ryan assigns R2 a task with a due date or a clear time horizon",
            "When work depends on an external reply, delivery, approval, or later check-in",
            "Use stable metadata keys for automation-created Todoist tasks",
            "Potential partner email",
            "Ryan-to-R2 assignment",
            "Waiting on external reply",
            "Meeting-note ingestion",
            "Default prospecting batch",
            "Follow up with <FirstName> about Untangle outreach",
            "Daily prep",
            "Blockers and delivery resilience",
            "Gemini doc is visible from calendar/thread context but access is denied",
            "Never update or recreate `clawchief/tasks.md`",
        ]
        for phrase in required_phrases:
            self.assertIn(phrase, text)

    def test_daily_task_manager_is_todoist_only(self) -> None:
        text = (SKILLS_ROOT / "daily-task-manager" / "SKILL.md").read_text()
        self.assertIn("~/.openclaw/skills/task-system-contract/SKILL.md", text)
        self.assertIn("Todoist is the only live task sink", text)
        self.assertIn("create a separate Todoist follow-up task", text)
        self.assertIn("stable metadata key", text)

    def test_daily_task_prep_surfaces_partner_and_ea_followups(self) -> None:
        text = (SKILLS_ROOT / "daily-task-prep" / "SKILL.md").read_text()
        self.assertIn("~/.openclaw/skills/task-system-contract/SKILL.md", text)
        self.assertIn("Do not rebuild or recreate a live `clawchief/tasks.md`", text)
        self.assertIn("Business development partnerships and Executive assistant sections", text)
        self.assertIn("partner or EA follow-up is due today or overdue", text)

    def test_executive_assistant_references_shared_contract_and_keeps_role_rules(self) -> None:
        text = (SKILLS_ROOT / "executive-assistant" / "SKILL.md").read_text()
        self.assertIn("priority-map.md", text)
        self.assertIn("~/.openclaw/skills/task-system-contract/SKILL.md", text)
        self.assertIn("update the Untangle outreach tracker", text)
        self.assertIn("Family calendar", text)
        self.assertIn("ea_gmail.py", text)
        self.assertIn("ea_calendar.py", text)
        self.assertIn("gws gmail +reply", text)
        self.assertIn("ea_calendar.py agenda", text)
        self.assertIn("outbound action path before sending", text)
        self.assertIn("Do **not** use `--thread-id` as the reply mechanism", text)
        self.assertIn("If Ryan emails R2 directly from one of Ryan's own addresses", text)
        self.assertIn("A direct human email from Ryan to `r2@untangle.us` should always receive a reply", text)
        self.assertNotIn("do **not** pass `--subject`", text)
        self.assertNotIn("omit `--subject` entirely", text)
        self.assertNotIn("--reply-to-message-id=MESSAGE_ID --reply-all --cc='hello@untangle.us' --subject=", text)

    def test_business_development_references_shared_contract_and_keeps_tracker_rules(self) -> None:
        text = (SKILLS_ROOT / "business-development" / "SKILL.md").read_text()
        self.assertIn("~/.openclaw/skills/task-system-contract/SKILL.md", text)
        self.assertIn("Todoist follow-through", text)
        self.assertIn("create or update the Todoist follow-up task", text)
        self.assertIn("sheet_helper.py", text)
        self.assertIn("lead-upsert", text)
        self.assertIn("through `gws`", text)
        self.assertIn("Do not perform LinkedIn activity as R2", text)
        self.assertIn("bd_outreach.py", text)
        self.assertIn("Follow up with Jane about Untangle outreach", text)
        self.assertIn("bd-blocker-", text)
        self.assertIn("header row cannot be verified", text)
        self.assertIn("Treat this workflow as a CRM operating system", text)
        self.assertNotIn("send the LinkedIn connection request note", text)
        self.assertNotIn("Prefer a dedicated agent-controlled browser profile", text)

    def test_cron_prompts_enforce_todoist_contract(self) -> None:
        jobs = json.loads(CRON_PATH.read_text())["jobs"]
        by_name = {job["name"]: job for job in jobs}

        ea_message = by_name["Executive assistant sweep"]["payload"]["message"]
        self.assertIn("Use the existing executive-assistant skill", ea_message)
        self.assertIn("This cron is the dependable trigger for recurring EA work", ea_message)
        self.assertIn("Rely on the existing skill for the detailed sweep procedure", ea_message)
        self.assertIn("also apply the existing business-development skill", ea_message)
        self.assertEqual(by_name["Executive assistant sweep"]["payload"]["timeoutSeconds"], 900)

        bd_message = by_name["Untangle daily prospecting"]["payload"]["message"]
        self.assertIn("Use the existing business-development skill", bd_message)
        self.assertIn("Rely on the existing skill for the detailed procedure", bd_message)

        prep_message = by_name["Daily task prep"]["payload"]["message"]
        self.assertIn("Use the existing daily-task-prep skill", prep_message)
        self.assertIn("This cron is the dependable trigger for morning task curation", prep_message)


if __name__ == "__main__":
    unittest.main()
