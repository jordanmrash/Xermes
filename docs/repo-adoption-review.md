# Repo Adoption Review — AoR / Helo / ACL → Hermes
**Date:** 2026-11-14 · **Performed by:** Hermes Agent (Qwen 3.8 via oMLX) · **Source repos:** `jordanmrash/agent-of-record`, `jordanmrash/agent-construct-lab`, `jordanmrash/helo` (cloned to scratch 2026-11-14, depth 1)

## 1. Review of the repos

### agent-of-record (v0.3.5, MIT, 4.0 MB)
A governed foundation for AI agents doing work a person signs their name to, built in
public accounting. Contains: a two-tier memory, a **120-entry lessons corpus**
(`CoworkConfig/cowork-memory/cowork-lessons.md`) with an evidence key
(`measured` / `reported` / `inference unverified`), a **verification ledger**
(`verification-ledger.json`) that grades rules `EFFECTIVE`/`UNRELIABLE` against a
**control arm** (un-instructed agent, same task, same criterion), 10 skills
(self-improvement, dream-cycle, gamma-tango, persistent-memory, not-a-robot,
command/git/local-file/playwright bridges, skill-menu), a **synthetic control loop**
(deterministic gate + three-arm harness), and clean-room publication tooling
(facts_check, public_scan, release_check, m365/Copilot personalizers).
**Verified by running:** `validate_manifest.py` on the incomplete input → exit 3,
names Segment D, "No workpaper was produced"; `run.py --check` → all three arms OK,
harness verdict `EFFECTIVE` (3 carried pass, control fails).

### helo (reference implementation, 192 KB)
Lean, evidence-gated memory + procedural-lessons core for an M365 declarative agent.
Single SQLite store with agent isolation (CHECK constraints + triggers that block
imported memories), 6-field **exact** retrieval (agent_id, scope, problem_signature,
compatibility_contract, applicability, exceptions), sha256-verified evidence payloads,
**duplicate/replay/foreign-identity rejection**, failure counting with
**auto-suspension at 2 verified failures**, and hard-blocked production writes.
**Verified by running:** `tests/test_lean_workflow.py` → PASS (isolated write,
retrieval, duplicate rejection, foreign identity rejection, feedback, suspension,
replay rejection; production remains blank). Note: requires Python ≥3.12
(tempfile.ignore_cleanup_errors); fails on the Mac's system Python 3.9.

### agent-construct-lab (release4, 360 KB)
Governed workspace automation for constructing, validating, and testing **portable
agent constructs** and platform adapters. JSON schemas (agent-construct,
platform-adapter, component-registry, platform-evidence), a certified reference
construct, five platform adapters (microsoft-365, claude, chatgpt, gemini,
open-runtime), and Node validation/scoring utilities.
**Verified by running:** `scoring-engine-selftest.js` → PASS (7/7).
`adapter-contract-selftest.js` → FAILS on a default clone (hardcoded directory name).

## 2. Conclusions

1. The capability layer this Hermes instance needs (terminal, browser, files,
   orchestration, image gen) is already native — Hermes does not need the repos'
   MCP bridges or Windows job infrastructure.
2. The **governance layer** is the real gap: evidence discipline on lessons,
   measurement of rules against a control, consolidation of memory, session
   bookends, and a publish gate for constructs. The repos are a proven, running
   reference for exactly that layer.
3. Hermes' own architecture (small pointer-tier memory + procedural skills +
   session search + cron) maps 1:1 onto the repos' two-tier design — the adoption
   slots in cleanly rather than fighting the host.
4. The 120-entry corpus splits: ~45 entries are host-agnostic behavioral lessons
   (transferable as-is); the rest describe Cowork/Windows/OneDrive/bridge machinery
   this instance does not run (not transferable).

## 3. What was adopted

| # | Adopted item | Where it lives now | Source |
|---|---|---|---|
| 1 | **Evidence-gated lessons** skill (format, evidence key, dedupe-by-Pattern-Key, supersede-don't-delete, 2-failure suspension) | skill `evidence-gated-lessons` + `references/ledger-schema.md` | AoR self-improvement + cowork-lessons + verification ledger; helo suspension rule |
| 2 | **Seeded lessons corpus** — 45 host-agnostic entries, full Failed/Why/Worked blocks, attribution header | `~/.hermes/agent-governance/lessons.md` | AoR cowork-lessons.md (45 of 120) |
| 3 | **Verification ledger** (empty, format + worked example documented) | `~/.hermes/agent-governance/verification-ledger.json` | AoR verification-ledger.json |
| 4 | **Controlled-gate template** skill (gate contract: exit 0/2/3, named gaps, no partial output; harness: positive/negative/control arms, EFFECTIVE verdict, re-run after change) + generalized gate script + worked example | skill `controlled-gate-template` + `references/gate_template.py`, `references/controlled-gate-example.md` | AoR examples/synthetic-control-loop |
| 5 | **Nightly consolidation** (dream cycle) — sweep memory/skills/lessons/sessions → dated proposal report (merges, retirements, contradictions, reachability gaps, budget); **proposes, never edits** | skill `nightly-consolidation` + reports dir `~/.hermes/agent-governance/reports/` + cron job `nightly-consolidation` (daily 02:00 America/Chicago, report lands as a note in this chat) | AoR dream-cycle skill |
| 6 | **Session bookend** (gamma tango) — OPEN: standing context + lesson scan + git baseline; CLOSE: log lessons + handoff note + propose commit | skill `session-bookend` | AoR gamma-tango skill |
| 7 | **Construct publish gate** — ACL Release 4 schema as a hard pre-ship validation (governance/memory/evaluation fields non-optional) + scoring reference | skill `construct-publish-gate` + `references/agent-construct.schema.json` | ACL release4 |

## 4. What was NOT adopted (non-applicable to this instance)

- **Four MCP bridges (8931 playwright / 8932 filesystem / 8933 command / 8934 Power
  Automate), dev tunnel + supergateway, Windows watchdog (Task Scheduler), OneDrive
  delivery surface, CommandJobs `.bat` infrastructure, `.plugin`/`.mcpb` build
  pipeline, Copilot personalizers, m365 adapter.** Rationale: Hermes natively provides
  terminal, browser control, file access, and scheduling; those bridges exist because
  Claude Cowork lacks those capabilities. Porting them would duplicate the host.
- **The ~75 bridge-specific lesson entries** (Cowork MCP bridges, Windows batch/
  schtask, OneDrive placeholder behavior, Power Automate evaluate_expression traps,
  `.plugin` install mechanics, save_memory 512-char cap). Rationale: the machinery
  they describe does not exist here; a rule served where it cannot apply costs the
  rules that can (their own seeded lesson). They remain in the repo for the Cowork
  route.
- **helo's SQLite runtime as a live service.** Rationale: its governance invariants
  (evidence gating, exact retrieval, failure suspension, production-write block) were
  adopted as doctrine into skills #1/#4; the runtime itself targets his M365 agent,
  not this host.
- **AoR's Windows install contract** (AGENTS.md steps for the tunnel route). Rationale:
  host-specific.

## 5. What needs correction (in the source repos)

**Status 2026-11-15:** items 1–2 were fixed on fresh clones in `~/repos/`, verified by
running (helo test PASS on CPython 3.9.6 and 3.13.18; ACL selftests PASS 12/12, 7/7,
plus both Claude validators), and committed locally: helo `3ee0cfc`, ACL `f5272a1`.
The ACL fix covered seven release4 scripts sharing the same hardcoded-folder defect,
not just the selftest. Push to GitHub pending user approval (hard stop).

1. **helo:** `tests/test_lean_workflow.py` uses `tempfile.TemporaryDirectory(ignore_cleanup_errors=...)`,
   which requires Python ≥3.12. The README says to run it with plain `python`; on a
   3.9–3.11 default it crashes at import. Fix: pin ≥3.12 in CI/docs or drop the kwarg
   with a fallback. (Workaround used here: ran with the 3.13 venv Python.)
2. **ACL:** `release4/adapter-contract-selftest.js` hardcodes a directory named
   `AgentConstructLab`, so it fails on a default `agent-construct-lab` clone (case
   mismatch in the resolved path). Fix: derive the repo root from `__dirname`.
3. **Attribution (not a bug, a rule):** adapted skills keep the source's attribution
   block ("Created by Jordan Rash, Director, Tax Transformation and Automation") and
   its integrity check. All five adopted skills carry it.

## 6. How the adopted pieces enhance existing Hermes configuration

| Existing Hermes capability | Gap before | Enhancement after |
|---|---|---|
| `skill_manage` / skills (procedural memory) | Accepts lessons at face value; no evidence discipline | `evidence-gated-lessons`: every rule carries `measured`/`reported` evidence, dedupes by Pattern-Key, suspends after 2 verified failures, never deletes history |
| Persistent memory (MEMORY.md / user profile) | Grows or manually prunes; no periodic review | `nightly-consolidation` cron: daily proposal report (merges/retirements/contradictions/reachability/budget) with zero auto-edits; user approves what to apply |
| Terminal / automation | No reusable auditable-deliverable pattern | `controlled-gate-template`: deterministic gate (named gaps, exit 0/2/3, no partial output) + control-arm harness → deliverables that are signable, with the gate itself measured |
| Session lifecycle | Each session starts cold, ends with implicit knowledge | `session-bookend`: explicit OPEN (context + lesson scan + baseline) / CLOSE (lessons logged + handoff + commit proposal) |
| Agent construction (he builds Helo, Cowork clone, MCP agents) | No formal publish gate | `construct-publish-gate`: schema-validated construct definitions with mandatory governance/memory/evaluation fields before any platform wiring |
| Hermes memory's own one-home-per-fact rule | Ad-hoc | The governance home `~/.hermes/agent-governance/` is the single home for lessons + ledger + reports; memory stays a pointer to it |

## 7. Operating agreement (per user instruction 2026-11-14)

**Auto-approval scope.** Routine, reversible, local actions are pre-approved without
per-step confirmation: creating/editing skills and governance files, running test
suites, cloning public repos (read-only), reading/writing under the user's home and
scratch, scheduling/pausing Hermes cron jobs, committing to the user's own working
repositories.

**Hard stops (confirmation always required).** Irreversible or externally visible
actions: pushing commits to the public GitHub repos, sending emails or messages to
anyone, deleting data or repos, changing system security settings (FDA, firewall,
default browser), spending money, and anything the user's own governance doctrine
marks `explicit-per-action`.

**Toggle convention (applies to every adopted feature, all time):**
- "turn off <feature>" → feature PAUSED until the user says otherwise (no auto-resume).
  For the nightly consolidation: cron job `nightly-consolidation` → paused; skills
  remain for manual "run the dream cycle" use.
- "get rid of <feature>" → feature REMOVED: skill deleted, cron job removed, its data
  archived (moved, not deleted) into `~/.hermes/agent-governance/archive/`, then
  removed from memory. Say what was removed.
- "turn on <feature>" / "resume <feature>" → restore.
