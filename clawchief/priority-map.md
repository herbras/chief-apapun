# Priority Map

Purpose: define who and what should matter enough to interrupt Ryan, trigger R2 action, or be safely ignored.

This file is the canonical "people + programs" layer for OpenClaw prioritization.

## Ownership boundary

This file owns:
- people importance
- program importance
- urgency level
- routing/action mode

This file does not own:
- task storage mechanics
- reply wording
- meeting-note ingestion procedure
- cron timing or retries

## How to use this file

When a new signal arrives from Slack, email, calendar, tasks, meeting notes, docs, or notes:

1. Map it to zero or more *people*
2. Map it to zero or more *programs*
3. Assign an urgency level
4. Choose the action mode

If a signal maps to no important people and no important programs, it should usually be ignored or batched and then archived.

## Urgency levels

- **P0 — interrupt now**
  - time-sensitive, high-stakes, or blocking
  - appropriate to put in front of Ryan quickly
- **P1 — same day**
  - important enough to surface today
  - may require Ryan or R2 action today
- **P2 — digest / batched**
  - worth tracking, but not worth interrupting Ryan for immediately
- **P3 — ignore / archive**
  - low-value noise, duplicative context, or non-actionable chatter

## Action modes

- **Interrupt Ryan now** — surface directly in Slack as a short, clear alert
- **Handle and summarize** — R2 acts, then gives Ryan a concise update if helpful
- **Queue for digest** — hold for next structured summary / heartbeat if still relevant
- **Ignore** — no user-facing message needed

## Task grouping convention

Todoist labels and section choices should connect back to this file's program/person grouping when there is a clear match.

Preferred pattern:

- owner assignment: `ryan` or `r2`
- one program section when there is a clear match
- due date or deadline to express when the next action should happen
- labels only for secondary context when they add real value

Rules:
- Use the exact program names from this file when choosing Todoist sections whenever there is a clear match.
- If a task does not clearly map to a program or person here, leave it unlabeled rather than inventing a noisy label.
- Do not use workflow-state sections like `Today`, `Next`, `Waiting`, or `Scheduled`; due dates should carry timing/state instead.
- Preserve stable program grouping unless Ryan explicitly wants a regroup.

## People

People are not only important because they are operationally relevant.
They are also important because they matter emotionally to Ryan.
The system should treat love, family, loyalty, and relationship depth as real prioritization signals — not just logistics.

### Ryan Carson
- Why he matters:
  - he is the principal, the decision-maker, and the person this whole system exists to help
- Watch for:
  - direct asks
  - approvals needed
  - decisions only Ryan can make
  - anything that affects his calendar, travel, or revenue priorities
- Escalate to P0 when:
  - there is a hard deadline within 24 hours
  - there is a meeting conflict or urgent scheduling issue
  - a prospect / partner / investor / board item is blocked on him
- Default action:
  - usually interrupt Ryan now or handle and summarize

## Core family

### Gillian Carson
- Why she matters:
  - she is Ryan's wife
  - they have been married since 2004-04-04
  - Ryan said he loves her with all his heart
  - she is central to his life, not just a scheduling variable
- Watch for:
  - family logistics that affect Ryan's schedule
  - Ryan shares a calendar with Gill called "Family" attached to the ryan@ryancarson.com Google account
  - messages or situations where Gill needs support, coordination, or a response
  - board-related context where Gill is directly involved
  - anything important to Gill that Ryan would want surfaced promptly
- Escalate to P0 when:
  - same-day family logistics affect Ryan's time or commitments
  - Gill needs something time-sensitive from Ryan
- Default action:
  - handle and summarize unless immediate attention is clearly warranted

### Jackson Carson
- Why he matters:
  - he is Ryan's son
  - family matters involving Jackson are intrinsically important, not merely administrative
- Watch for:
  - scheduling, school, travel, family coordination, health, or other time-sensitive needs
- Escalate to P0 when:
  - there is same-day schedule impact, urgency, or something Ryan would strongly want to know quickly
- Default action:
  - handle and summarize, escalating when time-sensitive

### Devon Carson
- Why he matters:
  - he is Ryan's son
  - family matters involving Devon are intrinsically important, not merely administrative
- Watch for:
  - scheduling, school, travel, family coordination, health, or other time-sensitive needs
- Escalate to P0 when:
  - there is same-day schedule impact, urgency, or something Ryan would strongly want to know quickly
- Default action:
  - handle and summarize, escalating when time-sensitive

### Marta
- Why she matters:
  - she is Ryan's mom
  - Ryan calls her every Sunday
  - family communication with Marta should be treated as emotionally meaningful, not background noise
- Watch for:
  - calls, reminders, family updates, health changes, travel, or anything that may matter to Ryan emotionally
- Escalate to P0 when:
  - there is important family news, health news, or time-sensitive coordination
- Default action:
  - handle and summarize unless urgent

### Chance
- Why he matters:
  - he is Ryan's dad
  - family communication with Chance matters on a personal, not just logistical, level
- Watch for:
  - reminders, birthday / check-in timing, health, travel, or family updates
- Escalate to P0 when:
  - there is important family news, health news, or time-sensitive coordination
- Default action:
  - handle and summarize unless urgent

### Kerri Foster
- Why she matters:
  - she is Ryan's sister
  - sibling / family developments should count as real priority signals when relevant
- Watch for:
  - meaningful family updates, moves, coordination, birthdays, or requests that would matter to Ryan
- Escalate to P1 when:
  - there is important family news or a time-sensitive ask
- Default action:
  - queue or handle and summarize depending on urgency

### Kristen Semmens
- Why she matters:
  - she is Ryan's sister
  - sibling / family developments should count as real priority signals when relevant
- Watch for:
  - meaningful family updates, coordination, birthdays, or requests that would matter to Ryan
- Escalate to P1 when:
  - there is important family news or a time-sensitive ask
- Default action:
  - queue or handle and summarize depending on urgency

### Jessica Carson
- Why she matters:
  - she is Ryan's sister
  - sibling / family developments should count as real priority signals when relevant
- Watch for:
  - meaningful family updates, coordination, birthdays, or requests that would matter to Ryan
- Escalate to P1 when:
  - there is important family news or a time-sensitive ask
- Default action:
  - queue or handle and summarize depending on urgency

## Pets

### Brinkley
- Why he matters:
  - he is part of Ryan's family life and recurring care for him should be treated as a real responsibility, not generic admin
- Watch for:
  - care reminders Ryan explicitly wants tracked
  - time-sensitive pet logistics that affect Ryan's day or travel
- Escalate to P1 when:
  - same-day care or travel coordination could be missed
- Default action:
  - queue or handle and summarize depending on urgency

## Friends

### Banning Jones
- Why they matter:
  - Banning is Ryan's friend and son of Bill Jones
  - this relationship matters personally, not just because of OpenClaw or operator learning
  - it also has strategic value because of the OpenClaw / operator overlap
- Watch for:
  - relationship-building opportunities
  - operator / OpenClaw insight exchange
  - direct asks or collaboration opportunities
- Escalate to P1 when:
  - there is a clear reply opportunity or useful follow-up that should not sit
- Default action:
  - handle and summarize; do not over-interrupt Ryan unless strategically relevant

## Important work / strategic relationships

### Linda Douglas
- Why she matters:
  - she is a key trusted operator for Untangle - our Chief Legal Officer
  - legal, policy, standards, and sensitive operating judgment run through her
- Watch for:
  - legal/compliance questions
  - policy claims that should not be answered casually
  - anything involving partner standards, referral structure, disclosures, or legal risk
- Escalate to P0 when:
  - a live thread needs a legal or policy answer to keep moving
  - a risky outbound response is about to be sent without approved guidance
- Default action:
  - handle and summarize, or interrupt Ryan if Linda input is blocking an important thread

### Phil Schwarz
- Why he matters:
  - he is on the Untangle board, representing Corazon Capital who own's 15% of Untangle, and is a high-trust strategic relationship
  - communication involving Phil can affect Ryan's strategic accountability and support structure
- Watch for:
  - board updates
  - investor communications
  - requests that affect financing, reporting, or strategic accountability
- Escalate to P0 when:
  - there is a near-term board/investor deadline or a sensitive strategic issue
- Default action:
  - handle and summarize unless Ryan decision is required soon

## Dynamic people groups

### Warm prospects / referral partners
- Listed in the live outreach sheet / CRM configured for this install.
- Why they matter:
  - direct path to early customers and channel leverage
- Watch for:
  - replies, objections, scheduling, interest signals, referrals, pilot discussions
- Escalate to P0 when:
  - a hot lead or warm partner reply is waiting and timing matters
- Default action:
  - handle and summarize

### Untangle Angel Investors
- Why they matter:
  - high-signal strategic communication
- Watch for:
  - requests for updates, metrics, materials, meetings, or decisions
- Escalate to P0 when:
  - response timing or message quality matters materially
- Default action:
  - handle and summarize, escalating when sensitive or strategic

## Programs

### First 10 paying customers
- Why it matters:
  - Ryan said this is the immediate top company priority
- Q2 target ladder:
  - 2026-04-30: 10 total customers
  - 2026-05-31: 20 total customers
  - 2026-06-30: 30 total customers
  - Current: 0
- Watch for:
  - anything that can directly create customers, learn from prospects, unblock acquisition, or improve conversion
- Examples:
  - partner introductions
  - prospect replies
  - customer objections
  - offers, pilots, pricing reactions, conversion bottlenecks
- Escalate to P0 when:
  - a near-term revenue opportunity is blocked on Ryan
  - there is a hot prospect / partner thread needing same-day action
- Default action:
  - handle and summarize or interrupt Ryan if his action is required today
- Ignore / downgrade:
  - vague marketing ideas with no clear next step

### Instagram content
- Why it matters:
  - this is a specific GTM program Ryan is actively using
  - it supports authority, reach, and customer acquisition
- Watch for:
  - recording videos with Linda or partners, editing, posting, scheduling, distribution, and follow-up needs
- Escalate to P1 when:
  - a recording window, publishing deadline, or blocker could stall momentum
- Default action:
  - handle and summarize unless same-day action is needed

### AEO / SEO
- Why it matters:
  - compounding acquisition channel
  - improves discoverability for people actively searching for divorce help
- Watch for:
  - rankings, content opportunities, technical issues, and search-performance changes
- Escalate to P1 when:
  - there is a concrete change that can materially improve discoverability or fix a meaningful issue
- Default action:
  - queue for digest unless action is clearly time-sensitive

### Meta Ads
- Why it matters:
  - paid acquisition channel with direct customer-growth implications
- Watch for:
  - campaign launches, account issues, creative needs, performance shifts, and blocking setup problems
- Escalate to P1 when:
  - spend, delivery, or setup problems are blocking acquisition
- Default action:
  - handle and summarize, escalating when Ryan decision is needed

### Google Ads
- Why it matters:
  - paid acquisition channel tied to search intent and conversion
- Watch for:
  - campaign launches, keyword / landing-page issues, performance changes, and setup blockers
- Escalate to P1 when:
  - a change materially affects traffic, lead flow, or spend efficiency
- Default action:
  - handle and summarize, escalating when Ryan decision is needed

### Fresh Start Registry partnership with Olivia
- Why it matters:
  - named partnership program with direct distribution and credibility implications
- Watch for:
  - communication with Olivia
  - partnership tasks
  - dashboard / listing work
  - magazine / expert / feature opportunities
- Escalate to P1 when:
  - the partnership is blocked, an opportunity is live, or Ryan input is needed to keep momentum
- Default action:
  - handle and summarize

### Business development partnerships
- Why it matters:
  - this is the live BD motion for building partnerships with attorneys, divorce coaches, and marriage counselors
- Watch for:
  - outreach replies
  - follow-up gaps
  - meetings
  - partner questions
  - objections
  - pilot opportunities
- Escalate to P0 when:
  - a strong reply or meeting opportunity is waiting and timing matters
- Default action:
  - handle and summarize

### Executive assistant: inbox, calendar, travel, schedule integrity
- Why it matters:
  - this is the operating system for Ryan's day-to-day execution capacity
  - inbox, scheduling, travel, and coordination tasks can create immediate drag or unblock important work
- Watch for:
  - scheduling follow-ups
  - travel constraints
  - inbox cleanup or reply obligations
  - meeting prep
  - calendar integrity issues
- Escalate to P1 when:
  - a scheduling issue, travel constraint, or inbox follow-up could disrupt the next few days
- Default action:
  - handle and summarize

### Out-of-home advertising
- Why it matters:
  - active awareness channel with real spend and coordination attached
- Watch for:
  - proposals
  - creative
  - placements
  - pricing
  - deadlines
  - vendor coordination
- Escalate to P1 when:
  - a decision, asset, or approval is blocking execution
- Default action:
  - handle and summarize

### 121G venture fund wind-down
- Why it matters:
  - Ryan runs a small venture fund called 121G
  - it is expected to wind down at the end of 2026
  - it still creates real investor, admin, and communication obligations that should not get lost
- Watch for:
  - inbox follow-up
  - investor updates
  - admin or communication tasks that still require attention
  - wind-down obligations, deadlines, or cleanup tasks tied to 2026
- Escalate to P1 when:
  - an investor-facing or time-sensitive 121G item is waiting
  - a wind-down deadline or obligation needs action
- Default action:
  - handle and summarize

### Board / investor communication
- Why it matters:
  - board and investor communication affects Ryan's strategic accountability, financing context, and external trust
- Watch for:
  - investor updates
  - board reports
  - materials due to Phil or investors
  - recurring reporting obligations
- Escalate to P1 when:
  - a board or investor deliverable is due soon
  - a strategic response needs Ryan input or careful wording
- Default action:
  - handle and summarize

### Family / personal logistics
- Why it matters:
  - family and personal obligations are real priorities, not background admin
  - they affect Ryan's life directly and often affect his capacity for work too
- Watch for:
  - birthdays
  - anniversaries
  - family check-ins
  - personal reminders
  - family coordination
- Escalate to P1 when:
  - a family obligation is time-sensitive or emotionally important enough that Ryan would want it surfaced promptly
- Default action:
  - handle and summarize

### Health / medical
- Why it matters:
  - medical follow-ups and preventive care are high-value long-horizon responsibilities that should not fall through the cracks
- Watch for:
  - annual exams
  - blood tests
  - checkups
  - specialist follow-ups
  - recurring health reminders
- Escalate to P1 when:
  - a medical task is time-sensitive, overdue, or tied to a real appointment / test deadline
- Default action:
  - handle and summarize

### Home / household
- Why it matters:
  - the house, car, boat, and recurring maintenance tasks create real operational load and can become expensive or disruptive if missed
- Watch for:
  - service scheduling
  - maintenance reminders
  - seasonal house work
  - vehicle upkeep
  - home systems that need recurring attention
- Escalate to P1 when:
  - a maintenance issue becomes urgent, seasonal, or costly if delayed
- Default action:
  - handle and summarize

### Essex Yacht Club Communications Chair
- Why it matters:
  - Ryan is chair of the Communications Committee at Essex Yacht Club
  - this is a named recurring role / program, not generic admin
  - EYC work is a real recurring commitment and should not disappear into generic admin noise
- Watch for:
  - Newsworthy
  - Spyglass
  - committee communications
  - scheduling or content obligations tied to EYC
- Escalate to P1 when:
  - a publication, deadline, or committee obligation is time-sensitive
- Default action:
  - handle and summarize

### clawchief improvement
- Why it matters:
  - compounds R2 effectiveness over time
- Watch for:
  - operator patterns worth copying
  - setup changes that improve autonomy, prioritization, or execution
  - concrete opportunities to improve the system Ryan uses daily
  - new OpenClaw capabilities that can be turned into better clawchief workflows
- Escalate to P1 when:
  - Ryan explicitly asks for system improvement work or a change is clearly high leverage
- Default action:
  - convert into a concrete task, proposal, or direct internal update pass instead of leaving it as a vague idea
- Ignore / downgrade:
  - theoretical AI chatter without a concrete operational implication

## Default routing rules

Use these deterministic routing defaults unless a clearer instruction overrides them:

- general inbox, scheduling, travel, calendar integrity, or operational coordination -> `executive-assistant`
- partner / referral / prospect pipeline, outreach tracker, lead verification, or prospecting batch work -> `business-development`
- direct task CRUD, reprioritization, completion, or current-task review -> `daily-task-manager`
- morning due-date retuning and daily actionability prep -> `daily-task-prep`
- meeting notes enter through `executive-assistant`, then route into `business-development` too if the note changes outreach / partner state
- cross-cutting Todoist follow-up / blocker rules come from `~/.openclaw/skills/task-system-contract/SKILL.md`, not from this file

If a signal maps to more than one route, choose the workflow that owns the live source of truth being changed.

## Things that should usually be ignored or batched

- casual chatter with no action
- repeated notifications that add no new information
- documents or messages with no connection to a priority person or program
- speculative ideas without owner, deadline, or next step
- low-stakes activity already captured in the task list

## Review cadence

Review this file when:
- Ryan says priorities changed
- a new person becomes important
- a new recurring program appears
- summaries feel noisy or are missing important things
