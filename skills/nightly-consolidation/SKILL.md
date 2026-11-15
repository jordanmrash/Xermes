---
name: nightly-consolidation
description: Nightly memory/skills consolidation; proposes, never edits.
version: 1.0.0
author: "Hermes Agent (adapted from agent-of-record dream-cycle; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, memory, consolidation]
    related_skills: [evidence-gated-lessons, session-bookend]
---

# Nightly Consolidation (dream cycle)

> Adapted 2026-11-14 by Hermes Agent from `agent-of-record`'s dream-cycle skill
> (nightly consolidation pass over the knowledge base). Original author: Jordan Rash,
> Director, Tax Transformation and Automation. Attribution kept intact per the
> source's integrity rule.

A periodic sweep across ALL durable knowledge — Hermes memory, this profile's skills,
the lessons corpus, and recent session history — that PROPOSES changes in a dated
report. It never edits, deletes, or modifies anything: every change waits for the
user's approval. The user can pause this entirely by saying "turn off consolidation"
(cron job `nightly-consolidation` → paused) or remove it with "get rid of it".

## When to Use (triggers)

- The scheduled cron job `nightly-consolidation` fires (daily, 2:00 America/Chicago).
- The user says "run the dream cycle", "nightly review", "consolidate my lessons",
  "clean up my memory", "what should be retired", "is my memory still accurate".

NOT for: logging one lesson (use `evidence-gated-lessons`), saving one memory
(use the `memory` tool), or the session bookend (use `session-bookend`). This is the
periodic sweep across all of them.

## The pass (one run, in order)

1. **Inventory.** Read Hermes memory (the two stores), this profile's skill list
   (names + descriptions), the deep-tier file `~/.hermes/agent-governance/deep-memory.md`, the
   lessons corpus `~/.hermes/agent-governance/lessons.md` (Pattern-Keys + statuses), and
   recent sessions (session_search) for corrections, repeated
   mistakes, and new standing facts.
2. **Find the deltas.** Look for:
   - **Merges** — the same fact in two places (memory + skill, or two lessons) that
     should have one home.
   - **Retirements** — memories/skills/lessons that are stale (superseded facts, dead
     machines, finished one-offs).
   - **Contradictions** — two stored statements that disagree; name both and which the
     evidence favors (a file/measured evidence beats a remembered claim).
   - **Reachability gaps** — a lesson or rule that is stored where no session that
     needs it would load it (the seeded corpus lives in a skill; a rule about terminal
     work that only sits in memory is a gap).
   - **Budget pressure** — memory stores over ~80% of their character budget.
3. **Write the report** to `~/.hermes/agent-governance/reports/consolidation-YYYY-MM-DD.md`
   (the date is the run date): a table of proposals, each with: id, kind
   (merge/retire/contradiction/reachability/budget), the exact current text, the
   proposed change, the evidence for it, and the risk of doing it.
4. **Deliver the summary.** The final response is SHORT (2-4 lines): run status,
   proposal count by kind, and the report path. No prose replay of the proposals.

## Hard rules

- **Propose, never edit.** The report is the only output. Approval happens the next
  time the user speaks; a user saying "apply 3 and 7" authorizes exactly those.
- **Never delete a lesson or ledger entry** — only propose supersede (the corpus's own
  rule: a ledger that deleted its own history could not show that a rule was corrected).
- **Attribution integrity** — if a skill's attribution block (Jordan Rash, author of
  record) is missing or altered, say so in the report; never silently rewrite it.
- **Idempotent.** Re-running the same day overwrites that day's report with the same
  proposals, not a duplicate file.
