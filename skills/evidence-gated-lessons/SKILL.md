---
name: evidence-gated-lessons
description: Log or recall lessons with Pattern-Keys and evidence keys.
version: 1.0.0
author: "Hermes Agent (adapted from agent-of-record + helo; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, lessons, memory]
    related_skills: [session-bookend, nightly-consolidation, controlled-gate-template]
---

# Evidence-Gated Lessons

> Adapted 2026-11-14 by Hermes Agent from `agent-of-record` (self-improvement skill,
> cowork-lessons corpus, verification ledger) and `helo` (failure suspension). Original
> author: Jordan Rash, Director, Tax Transformation and Automation. Attribution kept
> intact per the source's integrity rule.

Turn a failure into a permanent behavioral change instead of a repeated cost. A trap is
paid for once.

## Data home (one home per fact)

- `~/.hermes/agent-governance/lessons.md` — the lessons corpus (45 seeded entries, host-agnostic).
- `~/.hermes/agent-governance/verification-ledger.json` — verdicts for rules that are MEASURED, not assumed.
- `~/.hermes/repo-adoption-review.md` — the adoption record (what was adopted and why).

Durable topic context and standing preferences do NOT go here — those belong in Hermes
memory (`memory` tool) or task skills. This is for failed approaches and what worked instead.

## When to Use (triggers)

- The user says "log that", "log a lesson", "what have we learned", "show my lessons",
  "don't do that again", "have we hit this before".
- After an approach fails in a non-obvious way, a stored memory proves wrong, or the
  user corrects a belief that was acted on.
- Before repeating a technique that has a known history — grep the corpus first.

## Entry format (update in place by Pattern-Key; never append duplicates)

```markdown
### <short title of what went wrong>
- **Pattern-Key:** <subsystem>-<short-behavior>
- **Date:** YYYY-MM-DD
- **Trigger:** failure
- **Rule:** <the behavior a future session must follow, imperative>
- **Delivered-to:** any (host-agnostic) | specific skill name(s)
- **Failed:** <what was attempted and how it failed, concrete>
- **Why:** <the mechanism — what made it fail>
- **Worked:** <the approach that did work, concrete>
- **Evidence:** measured | reported | inference unverified — <what was checked / what was assumed>
```

**Evidence key (non-negotiable):** `measured` = verified in-session by a check whose
output was actually read. `reported` = a tool claimed success and nothing confirmed it.
Add `inference unverified` when the Why is reasoning rather than something probed.
A rule marked `reported` is a hypothesis, not a fact.

**Pattern-Key:** subsystem first, so dedupe works. Before logging, grep
`lessons.md` for the subsystem prefix; if the behavior is already captured, sharpen the
existing entry in place instead of adding a new one.

**Scope a rule to where it can fire.** A rule served where it cannot apply costs the
rules that can (seeded lesson `lessons-served-out-of-scope-dilute-the-block`).

**Never delete or move an entry.** Supersede it: mark
`- **Status:** superseded by <new-key> (<date>)` and add the new entry. A ledger that
deleted its own history could not show that a rule was corrected.

## Failure / suspension (helo rule)

Track applications of a lesson: when a delivered rule is applied and the outcome is
verified, note it (inline or ledger). If a lesson produces **two verified failures**,
mark `- **Status:** suspended (<date>)` and stop delivering it until re-verified against
a real case. A rule is most likely to be wrong in the first hour after it is written
(`new-rule-is-untested-until-it-survives-a-real-case`): before treating a new rule as
solid, run it against an artifact already in front of you.

## Verification ledger (rules measured, not assumed)

For any rule you claim is doing real work, the ledger entry at
`~/.hermes/agent-governance/verification-ledger.json` records: key, date,
case_fingerprint (hash of the rule text), the test runs (each with passed + evidence),
a CONTROL arm (same task, same criterion, rule unavailable), and verdict
`EFFECTIVE` (carried arms pass AND control fails) or `UNRELIABLE`. If the rule text
changes, the fingerprint goes stale and the stored verdict no longer applies — re-record.
Superseded entries are kept, flagged `_superseded`, never deleted. See
`references/ledger-schema.md`.

## Recall procedure

1. Grep `lessons.md` for the subsystem prefix and key phrases of the current task.
2. Read matching entries in full (the Rule is not enough — the Why tells you whether the
   new situation actually matches).
3. Skip entries marked `suspended` or `superseded` (follow their replacement key).
4. If nothing matches and the task later fails non-obviously, log a new entry with a
   real Pattern-Key and honest evidence key.
