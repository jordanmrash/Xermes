---
name: session-bookend
description: Session open/close bookend; context, lessons, handoff notes.
version: 1.0.0
author: "Hermes Agent (adapted from agent-of-record gamma-tango; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, session, workflow]
    related_skills: [evidence-gated-lessons, nightly-consolidation]
---

# Session Bookend (open / close)

> Adapted 2026-11-14 by Hermes Agent from `agent-of-record`'s gamma-tango skill
> (the operator's session bookend command). Original author: Jordan Rash, Director,
> Tax Transformation and Automation. Attribution kept intact per the source's
> integrity rule.

A three-part routine (memory, lessons, state) that runs at task start and task end so
no session burns turns rediscovering what a previous one paid for, and no session ends
with the next one cold.

## When to Use (triggers)

- The user says "bookend this", "open the session", "close the session" (the gamma-
  tango phrasing), or asks for the start-of-task context load / end-of-task wrap-up.
- If the phrase arrives with no mode word: infer OPEN when no real work has been done
  yet in the session, CLOSE when it has; say which mode was chosen.

Do NOT use for a plain memory request ("save this") or a plain lesson request ("log
that") — do those directly with the right tool/skill.

## OPEN (start of a task)

1. **Standing context.** Confirm the memory stores and user profile are loaded (they
   are injected automatically — do not re-read them, just note anything task-relevant).
   Then read `~/.hermes/agent-governance/handoff.md` if it exists — it carries open
   threads from prior sessions (work it, mark items `[x]` with a date as they close).
2. **Lesson scan.** Grep `~/.hermes/agent-governance/lessons.md` for subsystem prefixes
   and key phrases of the task. Report any matching Pattern-Keys in ONE line each
   (Rule only; the full entry is read when the situation actually matches).
3. **Baseline.** If the task touches a repository, run `git status --short` and report
   it as the pre-work baseline (seeded lesson: read the ACTUAL git status before
   describing repo state — never narrate from memory of what was changed).

## CLOSE (end of a task)

1. **Log lessons.** For each non-obvious failure, trap, or user correction from the
   session, log an entry per `evidence-gated-lessons` (or sharpen an existing
   Pattern-Key). Honest evidence key: `measured` only if a check's output was read.
2. **Handoff note.** Record what the NEXT session needs: open threads, things left
   half-done, constraints discovered. Write or update
   `~/.hermes/agent-governance/handoff.md` (the standing handoff file — mark done items
   `[x]` with a date, keep open ones); for short tasks one or two lines in the reply
   also suffice.
3. **Propose a commit.** If work happened in a repository, show the diff summary and
   PROPOSE the commit message; run the commit only on the user's yes (or per the
   auto-approval scope in `~/.hermes/repo-adoption-review.md` — commits to the user's
   own working repo are pre-approved; pushes are not).

## Hard rules

- **Test every exit code; never echo one** (seeded lesson
  `cowork-close-reports-ok-on-failed-commit`): a close that prints success without
  checking the underlying operation is the exact failure this bookend exists to catch.
- **No destructive close steps without approval.** The close never force-pushes,
  deletes branches, or sends anything.
- **Close a handoff item by splitting, not by leaving it half-open.** When an item is
  only partly done because the remainder is a hard stop (push, send, delete, spend),
  mark the completed part `[x]` with a date and its concrete handle (commit hash,
  file path, message id), and carve the gated remainder into a NEW open item named
  for the gate. A single `[ ]` item that is really "done except approval" hides the one
  thing the next session must act on.
