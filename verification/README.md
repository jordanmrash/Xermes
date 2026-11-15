# Verification ledger

`verification-ledger.json` records that a specific rule was TESTED against a
real case **with a control arm**, and what the measured verdict was. This is
what separates "the rule works" from "the rule sounds right."

- **Format:** see
  [`skills/evidence-gated-lessons/references/ledger-schema.md`](../skills/evidence-gated-lessons/references/ledger-schema.md)
  — entry shape, the mandatory control arm, fingerprint discipline, and the
  worked example.
- **Verdicts:** `EFFECTIVE` (carried arms pass AND the control fails) or
  `UNRELIABLE`. Superseded entries are flagged `_superseded`, never deleted.
- **State of this file:** intentionally empty in the public repo. Ledger
  entries reference local test runs; the live ledger lives on the machine and
  is not committed (see SECURITY.md). The schema and the worked example in the
  reference file are the publishable content.
