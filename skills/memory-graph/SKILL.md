---
name: memory-graph
description: Query the SQLite life-fact graph when memory runs short.
version: 1.0.0
author: "Hermes Agent (schema adapted from helo; original author Jordan Rash, Director, Tax Transformation and Automation)"
license: MIT
metadata:
  hermes:
    tags: [governance, memory, sqlite]
    related_skills: [evidence-gated-lessons, nightly-consolidation]
---

# Memory Graph (SQLite life-fact graph)

> Adapted 2026-11-16 by Hermes Agent from the schema discipline of `helo`
> (jordanmrash/helo): identity lock, evidence triggers, sha256-verified payloads,
> agent isolation. The graph layer (entities / relations / facts / FTS5) is a
> host adaptation for a Hermes instance. Original author: Jordan Rash, Director,
> Tax Transformation and Automation. Attribution kept intact per the source's
> integrity rule.

## When to Use (triggers)

- The user asks a question about **structured life or entity facts** — people,
  orgs, places, projects, events, relationships, timelines — and the injected
  memory tier (MEMORY.md, a few KB) does not carry the answer.
- A new durable fact appears (user statement or verified document) and needs a
  permanent, queryable home below the injected tier.
- NOT for: procedural lessons (evidence-gated-lessons owns those), prose digests
  (deep-memory sections), raw primary data (era files / scans).

## Location

`~/.hermes/agent-governance/memory-graph/`
- `hermes-memory.sqlite3` — the store
- `schema.sql`, `seed_graph.py` (idempotent), `memq.py` (CLI)

## Commands (all via `python3`)

```bash
M=~/.hermes/agent-governance/memory-graph
python3 $M/memq.py stats                    # counts, integrity
python3 $M/memq.py search "<terms>"         # FTS over entities/facts/relations
python3 $M/memq.py entity <key-or-name>     # entity + attrs + facts + relations
python3 $M/memq.py neighbors <key>          # all relations both directions
python3 $M/memq.py facts [key]              # facts for one entity or all
```

Entity keys are dot-form (`person.name`, `org.acme`, `12.main.st`). `entity`
also matches by display name.

## Reading discipline

- The DB opens **read-only** for queries (helo pattern). Never write with a raw
  connection for reads.
- Every fact row carries `confidence` (`measured` / `reported` / `inferred`) and
  an `evidence_ref` (`hermes:<evidence-id>` → evidence table, sha256-verified
  payload naming the source doc). **Cite both when using a fact in an answer** —
  especially for inferred ones (label them as inferred).
- Relations are time-aware: `valid_from` / `valid_to`; `valid_to = NULL` means
  current.

## Writing discipline (via `memq.py` only)

```bash
python3 $M/memq.py add-fact <entity|global> <measured|reported|inferred> <source> <content...>
python3 $M/memq.py add-entity <kind> <name> <key> <source> [attrs-json]
python3 $M/memq.py add-relation <from> <to> <type> <source> [attrs-json] [valid_from] [valid_to]
```

- `source` = the document that proves it (e.g. a dated report filename) or
  `user-statement-YYYY-MM-DD` for what the user said. **No source, no write.**
- Confidence: `measured` = verified in primary data; `reported` = user or a doc
  states it; `inferred` = deduced (say so).
- **One home per fact.** This graph is the home for structured facts;
  deep-memory sections hold prose digests; MEMORY.md holds pointers only. Link,
  don't copy.
- A changed relationship (job, move, status): insert a new relation row with the
  new window and set the old row's `valid_to`. **Never delete rows** — the graph
  is append-only history (helo doctrine).
- DB triggers reject inserts without `hermes:` evidence and reject any agent
  other than `hermes` (identity lock). If a write fails, the trigger caught
  something wrong — fix the data; do not bypass the trigger.
- FTS is updated automatically by `memq.py` after writes.

## Hard rules

- **Sanitized publication.** The live DB is a machine-specific store and is never
  committed to a repo (see SECURITY.md of the publishing repo). Only schema,
  tooling, and a clearly-labeled example seeder are published.
- **No inferred fact goes in as measured.** The confidence key is load-bearing;
  inflating it corrupts every downstream citation.
- **Verify after writing.** Read the row back (`memq.py entity`) before telling
  the user the fact was recorded.

## Pitfalls

- FTS must be a **plain** FTS5 table, not contentless — contentless FTS5 returns
  NULL on column selects.
- Re-running `seed_graph.py` is safe (idempotent) and never touches rows added
  via `memq.py`.
- For anything not in the graph, check the deep-memory sections first, then the
  raw era files — don't guess.
