# Xermes

Governance patterns for agent runtimes, extracted from the Cowork-era repos
[agent-of-record](https://github.com/jordanmrash/agent-of-record),
[agent-construct-lab](https://github.com/jordanmrash/agent-construct-lab), and
[helo](https://github.com/jordanmrash/helo), and adopted into **Hermes Agent**
(Nous Research) on macOS. This repository documents the specific configuration
changes made to a Hermes instance to add a governance layer — and proves the
layer is host-agnostic: the same patterns run on a Windows/Copilot-Cowork stack
*and* a macOS/Hermes stack, with the evidence recorded for each.

The discipline throughout is *measured, not assumed*: every rule carries an
evidence key, every gate is verified against a control arm, and any failure
becomes a hard stop that names what is missing.

## The gap these patterns fill

An agent runtime's capability layer (terminal, browser, files, scheduling) is
commodity — Hermes provides all of it natively. The governance layer is not:

| Concern | Without governance | With these patterns |
|---|---|---|
| Lessons from failures | Logged and trusted at face value | Every rule carries a `measured` / `reported` / `inference unverified` evidence key; dedupe by Pattern-Key; a rule suspended after two verified failures |
| Rules that do work | "Sounds right" | A verification ledger with a **control arm**: carried arms pass **and** the control fails ⇒ `EFFECTIVE`; anything else `UNRELIABLE` |
| Memory over time | Grows, or is pruned by hand | A nightly consolidation sweep that **proposes** merges, retirements, contradictions, and reachability gaps — and never auto-edits |
| Structured facts below the injected tier | Prose notes only; no queryable home for people/orgs/places/timelines | A **SQLite entity/relation/fact graph** (helo discipline: identity lock, evidence triggers, sha256 payloads) with FTS recall, confidence keys, and time-aware relations — referenced when the injected memory runs short |
| Session lifecycle | Each session starts cold, ends with implicit knowledge | A bookend: OPEN (standing context + lesson scan + git baseline) / CLOSE (lessons logged + handoff note + commit proposal) |
| Auditable deliverables | "The inputs look fine" | A deterministic gate: manifest-driven required segments, exit codes `0` / `3` (named missing segment) / `2` (could not run), no partial output — and the gate itself is proven by a three-arm harness |
| Agent constructs | Wired into a platform, then discovered malformed | A schema-validated publish gate with non-optional governance, memory, and evaluation fields |

## What was changed in the Hermes instance

The concrete configuration changes, in one record: [`docs/repo-adoption-review.md`](docs/repo-adoption-review.md).
It lists what was adopted (seven items, with source and destination), what was
deliberately *not* adopted (the host-specific machinery and why), what needed
correction in the source repos, and the operating agreement between user and
agent (auto-approval scope, hard stops, pause/remove conventions).

**Update 2026-11-16:** the memory-graph construct (`memory-graph/` +
`skills/memory-graph/`) was added — the helo SQLite runtime, previously adopted
only as doctrine, now runs on this host as the structured-fact reference tier.
Proven by `memory-graph/seed_example.py` (11 checks, example data only).

## Repository layout

```
skills/                       # the six governance skills (procedural memory)
  evidence-gated-lessons/     # lesson format, evidence key, Pattern-Key dedupe, suspension
    references/ledger-schema.md
  controlled-gate-template/   # deterministic gate + control-arm harness
    references/gate_template.py          # copy-and-adapt gate (exit 0/2/3, named gaps)
    references/controlled-gate-example.md
  nightly-consolidation/      # the dream cycle: propose, never edit
  session-bookend/            # OPEN / CLOSE routines
  construct-publish-gate/     # pre-ship schema validation for agent constructs
    references/agent-construct.schema.json
  memory-graph/               # SQLite life-fact graph: when + how (added 2026-11-16)
memory-graph/                 # the graph construct (added 2026-11-16)
  schema.sql                  # helo core + entities/relations/facts + FTS5
  memq.py                     # read-only query + evidence-gated write CLI
  seed_example.py             # example-data seeder + 11-check verification battery
  README.md
lessons/lessons.md            # the lessons corpus (49 entries, host-agnostic)
verification/                 # the verification ledger (rules measured, not assumed)
reports/                      # consolidation reports are generated locally, never committed
docs/repo-adoption-review.md  # the adoption record (the specific config changes)
```

Each skill is written for a Hermes `skills/` directory as-is: copy a folder in
and the agent loads it. The skills are also readable standalone — each
`SKILL.md` states its triggers, the format contract, and its hard rules.

## How the evidence works (the short version)

- **Evidence key.** `measured` = verified by a check whose output was actually
  read. `reported` = a tool claimed success and nothing confirmed it — a
  hypothesis, not a fact.
- **Control arm.** A rule is only `EFFECTIVE` if the instructed agent passes the
  case *and* the same task, same criterion, rule unavailable, fails. If the
  control passes, the rule adds nothing measurable.
- **Suspension, not deletion.** A rule that fails twice is marked `suspended`;
  a superseded rule is marked with its replacement key. A ledger that deleted
  its own history could not show that a rule was corrected.

Full formats: [`skills/evidence-gated-lessons/references/ledger-schema.md`](skills/evidence-gated-lessons/references/ledger-schema.md).

## What is intentionally NOT included

Machine-specific state is excluded by doctrine, not by accident — see
[SECURITY.md](SECURITY.md): the live memory stores, session transcripts, chat
history, credentials, browser state, and local machine paths. The repository
holds patterns, formats, the sanitized corpus, and the adoption record —
nothing that identifies a machine or a person beyond the author's public
professional identity.

## Attribution

Original author: **Jordan Rash**, Director, Tax Transformation and Automation.
The patterns derive from his agent-of-record / agent-construct-lab / helo
projects; the adaptation into Hermes Agent was performed by the Hermes agent
itself under the operating agreement recorded in the adoption review.
Attribution blocks inside the skills are load-bearing — do not remove them
(see the adoption record, item 3).

## License

MIT — see [LICENSE](LICENSE).
