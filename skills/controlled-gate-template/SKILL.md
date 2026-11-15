---
name: controlled-gate-template
description: Auditable automation with gates, named gaps, control arms.
version: 1.0.0
author: "Hermes Agent (adapted from agent-of-record synthetic control loop; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, verification, automation]
    related_skills: [evidence-gated-lessons]
---

# Controlled Gate Template

> Adapted 2026-11-14 by Hermes Agent from `agent-of-record`
> (examples/synthetic-control-loop: validate_manifest.py, run.py, verification-case,
> recorded runs). Original author: Jordan Rash, Director, Tax Transformation and
> Automation. Attribution kept intact per the source's integrity rule.

Pattern for work a person signs their name to: a deterministic gate in front of every
deliverable, and a harness that proves the gate actually works. Measured, not assumed.

## When to Use (triggers)

Building or reviewing any auditable automation where a missing or bad input must never
become a plausible-looking output: tax workpapers, provision inputs, manifest-driven
batch jobs, deliverable bundles, migration bundles, anything with required components.

## The contract (do not relax)

1. **The gate is deterministic code, not a prompt.** It reads a manifest that names
   every required segment/component, checks presence AND non-emptiness, and reports
   each one by name.
2. **A missing required segment is a HARD STOP that names what is missing** and
   **produces no partial output.** A complete-looking deliverable must not be buildable
   from incomplete inputs by accident.
3. **Three-valued exit codes:** `0` complete (downstream may run), `3` a required
   segment is missing or empty (named), `2` could not run (manifest unreadable, bad
   usage). `2` is NEVER a rule failure — it means the check itself could not execute.
4. **Downstream steps check the gate's exit code** before running. No code path skips
   the gate "because the inputs look fine."

## The harness (prove the gate works)

The gate is not trusted because it looks right; it is trusted because a recorded
control loop shows it behaving exactly as the lesson prescribes:

1. **Positive arm:** complete input set → gate exits 0.
2. **Negative arm:** the set missing a required segment → gate exits 3, names the
   segment, and produced nothing.
3. **Control arm:** the same task WITHOUT the gate/rule, judged by the same criterion —
   it must fail (or produce the wrong output). A control that passes means the gate
   adds nothing measurable.
4. **Verdict:** carried arms pass + control fails ⇒ `EFFECTIVE`; otherwise
   `UNRELIABLE` — fix the gate or the case and re-record. Verdicts go into
   `~/.hermes/agent-governance/verification-ledger.json` (format in the
   `evidence-gated-lessons` skill's `references/ledger-schema.md`).
5. **Re-run the loop after any change to the gate or the rule text.** A refactored gate
   must be shown to still refuse the exact negative case; "it compiles" is not evidence.

## Building one

1. Copy `references/gate_template.py` next to the workflow. It is a generalized port
   of the proven AoR gate: manifest-driven, three-valued exit codes, named gaps, no
   partial output, CSV row counts where the segments are tabular.
2. Write the `manifest.json` for the real workpaper: workpaper name +
   `required_segments` (id, file, description). Every component that must exist for
   the deliverable to be signable goes in the manifest — if it is not in the manifest,
   it is not required.
3. Add a `--check` runner (see `references/controlled-gate-example.md` for the AoR
   run.py structure) that executes the three arms and prints one line per step; this
   is what CI or a pre-delivery step calls.
4. Record the runs (verdicts + evidence) in the verification ledger.

## Anti-patterns (from the seeded lessons corpus)

- A check that skips the thing that can fail is not a check
  (`install-check-skipped-handshake-hides-dead-bridge`).
- A verification that cannot fail on the thing you fear is not a verification
  (`verification-scoped-away-from-the-risk`).
- A check that warns on a proxy trains you to ignore the real ones
  (`verifier-warns-on-proxy-not-the-defect`).
- Never read the gate's exit code through a pipe — a pipeline reports the LAST
  command's status (`verifier-pipe-masks-the-exit-code`).
