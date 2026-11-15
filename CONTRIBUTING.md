# Contributing

This repository holds governance patterns that an agent loads and acts on. A
change here changes agent behavior, so the bar for editing is the bar the
patterns themselves set: evidence, not assertion.

## Adding a lesson

1. Grep `lessons/lessons.md` for the subsystem prefix first — if the behavior
   is already captured, sharpen the existing entry in place (update by
   Pattern-Key, never append duplicates).
2. Follow the entry format exactly (title, Pattern-Key, Date, Trigger, Rule,
   Delivered-to, Failed, Why, Worked, Evidence).
3. The **Evidence key is non-negotiable**: `measured` only if a check's output
   was actually read; `reported` if a tool claimed success; add
   `inference unverified` when the Why is reasoning rather than something probed.
4. Scan the diff for anything personal or machine-specific (see SECURITY.md)
   before pushing.
5. Never delete or move an entry — supersede it (`- **Status:** superseded by
   <key> (<date>)`).

## Adding or changing a skill

1. A skill is a rule that a future session must follow, loaded by trigger.
   Write it as an imperative rule plus the why; one rule per lesson.
2. Keep the attribution block intact — it is load-bearing (see the adoption
   record, item 3).
3. If the skill encodes a *measured* claim, the claim needs a verification
   ledger entry (control arm included) in `verification/` — or the claim is a
   hypothesis and should be written as one.
4. Re-run the controlled gate / selftests after any change to a gate or rule
   text; "it compiles" is not evidence.

## What does not belong here

Anything that identifies a machine or a person beyond the author's public
professional identity (see SECURITY.md). Patterns yes; state no.
