---
name: construct-publish-gate
description: Validate agent constructs against the ACL schema pre-ship.
version: 1.0.0
author: "Hermes Agent (adapted from agent-construct-lab release4 schemas; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, agent-constructs, validation]
    related_skills: [evidence-gated-lessons, controlled-gate-template]
---

# Construct Publish Gate

> Adapted 2026-11-14 by Hermes Agent from `agent-construct-lab` (release4 schemas and
> scoring). Original author: Jordan Rash, Director, Tax Transformation and
> Automation. Attribution kept intact per the source's integrity rule.

Before a new agent construct ships (Helo v2, the Copilot Cowork clone, any new MCP-
backed agent), validate its definition against the ACL Release 4 schema and require
the governance fields the schema makes non-optional.

## When to Use (triggers)

- The user says "certify this construct", "validate the construct", "is this ready to
  ship/publish", or designs a new agent and asks whether it is well-formed.
- Before wiring a new agent construct into any platform (M365, Claude, ChatGPT,
  Gemini, open-runtime).

## The gate

1. **Schema validation.** The construct JSON must validate against
   `references/agent-construct.schema.json` (schema_version 1.0.0). Required fields:
   id (lowercase slug), name, purpose (>=10 chars), capabilities, components,
   governance, memory, evaluation, targets.
2. **Governance fields are non-negotiable** (the schema requires all four):
   - `approval_policy`: `read-only` | `explicit-for-state-change` | `explicit-per-action`
   - `prohibited_actions`: explicit list (never empty by omission — an empty list is a
     statement; make it a deliberate one with a reason).
   - `evidence_required`: true for anything the user signs their name to.
   - `rollback_required`: true if the construct mutates state.
3. **Memory fields:** `durable`, `incident_learning`, and `promotion_requires_review`
   — a construct that promotes lessons without review is exactly the failure the
   `evidence-gated-lessons` ledger exists to catch.
4. **Evaluation fields:** `shared_suite` (name of the behavioral suite) and
   `minimum_score` (0-100). A construct without a shared suite cannot be compared
   across platforms — that is the point of ACL's behavioral equivalence matrix.
5. **Targets** are the five platforms: `microsoft-365`, `claude`, `chatgpt`, `gemini`,
   `open-runtime`. Each target needs a matching adapter in the ACL repo
   (`release4/*.adapter.json`) or a new one built from `platform-adapter.schema.json`.

## How to run it

The schema lives in the ACL repo; the validated reference construct
(`certified-workspace-agent.construct.json`) is the worked example. To validate:

```bash
pip install jsonschema
python -c "import jsonschema, json, pathlib;
jsonschema.validate(json.loads(pathlib.Path('<construct>.json').read_text()),
  json.loads(pathlib.Path('<agent-construct.schema.json>').read_text()))
print('CONSTRUCT: VALID')"
```

A failing validation is a HARD STOP for the publish (three-valued contract from the
`controlled-gate-template` skill: valid / invalid-named / could-not-run).

## Scoring (optional, for equivalence)

The ACL repo's `release4/score-platform-evidence.js` (verified PASS 7/7 on this machine
2026-11-14) scores platform evidence against the construct's expectations. Use it when
claiming a new platform adapter is behaviorally equivalent to a certified one. Note:
its sibling `adapter-contract-selftest.js` hardcodes a directory name (`AgentConstructLab`)
and fails on a default clone — see the adoption review doc before relying on it.

## Security boundary (from ACL SECURITY.md)

Do not commit secrets, credentials, browser state, machine-specific paths, private
workspace logs, or internal-only status artifacts into a construct definition or its
evidence. Machine-specific state is INTENTIONALLY excluded from the public schema —
keep it that way.
