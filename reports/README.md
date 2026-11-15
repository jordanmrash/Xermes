# Reports

Consolidation reports (the nightly dream-cycle output) are generated **locally**
at runtime — one dated file per run — and are intentionally **never committed**:
they quote session detail and live machine state.

This directory exists so the layout matches the skill contract
(`nightly-consolidation` writes to the governance home's `reports/`). If you are
adapting these patterns to your own runtime, keep the same invariant: the
proposer writes a dated report; a human reads it and approves; nothing is
edited until someone says so.
