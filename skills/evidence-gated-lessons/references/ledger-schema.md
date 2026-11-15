# Verification Ledger — format

File: `~/.hermes/agent-governance/verification-ledger.json` — a JSON array of entries.
Each entry records that a specific rule was TESTED against a real case WITH A CONTROL
ARM, and what the measured verdict was. This is what separates "the rule works" from
"the rule sounds right."

## Entry shape

```json
{
  "key": "<pattern-key the verdict belongs to>",
  "date": "<ISO timestamp of the judgment>",
  "case_fingerprint": "<sha256 of the exact rule text being judged, first 16 hex>",
  "passes": 3,
  "control_passed": false,
  "control_kind": "proxy",
  "verdict": "EFFECTIVE",
  "runs": [
    { "passed": true, "evidence": "<what was actually observed, verbatim where possible>" }
  ],
  "control": {
    "passed": false,
    "evidence": "<what the control arm did without the rule>"
  }
}
```

## Rules of the ledger

1. **A control arm is mandatory for EFFECTIVE.** The control runs the SAME task, judged
   by the SAME criterion, differing in exactly ONE variable: whether the rule under test
   is available to the agent doing the work. Carried arms pass + control fails ⇒
   EFFECTIVE. If the control also passes, the rule adds nothing measurable ⇒ UNRELIABLE
   (or the case is too weak — fix the case, don't force the verdict).
2. **Fingerprint discipline.** `case_fingerprint` is computed over the exact rule text
   (and the case's trap description). When the rule text is later sharpened, the old
   entry's fingerprint no longer matches: keep the old entry, flag it
   `"_superseded": "<why the old text no longer exists>"`, and judge the amended rule
   as a NEW entry. Never edit a stored verdict.
3. **Evidence is observation, not narration.** Each run's evidence says what the agent
   actually did on its first attempt and what output was read. A run where the agent
   pre-empted the trap because it knew the rule scores PASS; a run where it fired the
   trap on the first call scores FAIL even if it recovered — an uninstructed agent
   recovers the same way.
4. **`passes`** counts test runs that passed; the verdict requires the passes the case
   demands (typically all) AND a failing control.
5. **REFUSED is a valid outcome.** If a judge re-runs recorded runs against changed
   text, it refuses: the stored verdict no longer applies. That refusal is the harness
   working as designed — re-record the runs against the current text.
6. **Ledger entries are never deleted.** History of corrections is the point.

## Worked example (from agent-of-record, abridged)

Key `bridge-8934-evaluate-rejects-safe-navigation` had TWO entries: the first judged an
early version of the rule and came out UNRELIABLE — the un-instructed control discovered
a second trap the rule had missed. The entry was kept and flagged `_superseded`; the
amended rule (naming both traps) was judged as a new entry: 3/3 carried runs pre-empted,
control fired the trap on its first call, verdict EFFECTIVE. The superseded entry is what
proves the rule was corrected by measurement rather than declared corrected.
