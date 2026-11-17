# Memory Graph — SQLite store for structured life/entity facts

The reference tier below an agent runtime's injected memory. When the small
always-injected memory tier runs short, the agent queries this store instead
of reconstructing facts from prose notes or primary data.

Schema discipline is adapted from
[helo](https://github.com/jordanmrash/helo) (identity lock, evidence triggers,
sha256-verified payloads, agent isolation); the entity/relation/fact graph and
FTS5 recall layer are this construct's addition.

## Layout

| File | What it is |
|---|---|
| `schema.sql` | The store: `identity` (agent lock), `evidence` (sha256 payloads), `memories` / `lessons` (helo pattern, triggers reject non-`hermes:` evidence), `entities` / `relations` / `facts` (the graph), `mem_fts` (plain FTS5 — contentless FTS5 returns NULL on column selects) |
| `memq.py` | CLI: read-only `search` / `entity` / `neighbors` / `facts` / `stats`, and write commands `add-fact` / `add-entity` / `add-relation` that always create their own `hermes:` evidence row. `MEMQ_DB` env var overrides the default path (used by the self-test) |
| `seed_example.py` | **Example-data-only** seeder + verification battery (11 checks). Run it: `python3 seed_example.py` → builds a temp DB, exercises the full loop (init, idempotent seed, FTS, trigger rejection, read-only path, CLI smoke), cleans up, exits 0/1 |

## The tiering (adopting instance)

```
MEMORY.md (~2 KB, injected every turn)          pointers only
  -> deep-memory.md sections                    prose digests
    -> this SQLite graph                        structured facts (this directory)
      -> raw primary data (scans, era files)    verification tier
```

One home per fact: a fact lives in exactly one tier; other tiers link to it.

## Doctrine (non-negotiable)

- **No production data in this directory in a published repo.** The live
  `hermes-memory.sqlite3` is machine-specific and stays on the adopting
  machine (see repo SECURITY.md). `seed_example.py` uses labeled placeholder
  data only.
- **Evidence or it doesn't go in.** Triggers abort inserts whose
  `evidence_ref` is not `hermes:<id>`; the identity CHECK aborts any other
  agent. Fix the data, never bypass the trigger.
- **Append-only.** A changed relationship gets a new row with the new
  `valid_from`/`valid_to` window plus the old row's `valid_to` set. Rows are
  never deleted.
- **Confidence key is load-bearing.** `measured` / `reported` / `inferred` —
  citing a fact without its confidence and evidence reference is a citation
  failure, not a style one.

## Adoption

1. Copy this directory plus `skills/memory-graph/` into the agent's
   governance home.
2. Run `python3 seed_example.py` — all 11 checks must pass on the target host.
3. Write your own `seed_graph.py` from the example's shape (idempotent,
   evidence-keyed) and seed from the instance's durable records.
4. Point the agent's memory tiering at the store (the skill carries the
   trigger conditions).
