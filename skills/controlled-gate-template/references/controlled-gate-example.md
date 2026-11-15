# Worked example — the AoR synthetic control loop

Source: `agent-of-record/examples/synthetic-control-loop/` (verified by running on this
machine 2026-11-14: gate refused the incomplete set with exit 3 naming Segment D, harness
judged EFFECTIVE, control failed).

## Anatomy

```
synthetic-control-loop/
  validate_manifest.py      # the gate (exit 0 / 2 / 3)
  run.py                    # the three-arm runner with --check
  verification-case.json    # the recorded test case (prompt + traps + criterion)
  lesson.md                 # the rule under test, exact text (fingerprinted)
  recorded-runs.json        # the carried-arm transcripts (what the agent did)
  inputs/complete/          # all 4 segments + manifest  -> gate exit 0
  inputs/incomplete/        # segment D absent          -> gate exit 3, names D
```

## What run.py checks (one line per step under --check)

1. `gate accepts the complete input set (exit 0)` — rc == 0.
2. `gate refuses the set missing Segment D, names it, produces nothing (exit 3)` —
   rc == 3 AND output contains `HARD STOP`, the segment id, and `No workpaper was
   produced`.
3. `harness judges the recorded arms EFFECTIVE (3 carried pass, control fails)` — the
   judge (AoR's verify_delivery.py) re-judges the recorded transcripts against the
   CURRENT rule text and case; it REFUSES if the text drifted since recording.

All three pass ⇒ `CONTROL_LOOP: OK - a missing input became a hard stop, and the
delivered rule is measured, not assumed.` Exit 0. Any miss ⇒ `CONTROL_LOOP: FAIL`,
exit 1. Judge missing ⇒ `COULD NOT RUN`, exit 2.

## Adapting it

- Replace the four synthetic segments with the real required components of your
  deliverable (e.g. provision: trial balance, subledger extract, adjustments, prior
  year comparative).
- Keep the manifest as the single source of truth for "required": adding a component
  to the deliverable means adding it to the manifest in the same change.
- Keep `--check` callable from CI / a pre-delivery step, and re-run it after every
  gate or rule edit (seeded lesson `enforcer-encodes-the-superseded-rule`).
- Record the runs and verdict in `~/.hermes/agent-governance/verification-ledger.json`.
