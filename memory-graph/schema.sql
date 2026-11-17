-- Hermes memory graph — adapted from helo (jordanmrash/helo, memory/helo_memory.py)
-- Attribution: schema discipline (identity lock, evidence triggers, sha256 evidence,
-- failure suspension) created by Jordan Rash, Director, Tax Transformation & Automation.
-- Host adaptation by Hermes 2026-11-16: agent='hermes', evidence ns 'hermes:',
-- plus entity/relation/fact graph + FTS5 for life-fact recall.
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS identity (
  agent TEXT PRIMARY KEY CHECK(agent='hermes'),
  schema_version INTEGER NOT NULL
);

-- evidence: sha256-verified payloads (helo pattern)
CREATE TABLE IF NOT EXISTS evidence (
  id INTEGER PRIMARY KEY,
  agent TEXT NOT NULL CHECK(agent='hermes'),
  source TEXT NOT NULL,            -- hermes_runtime | deep_dive_2026_11_15 | user_statement
  outcome TEXT NOT NULL,           -- measured | reported | inference_unverified
  payload TEXT NOT NULL,
  payload_sha256 TEXT NOT NULL
);

-- memories: bounded durable facts (helo pattern)
CREATE TABLE IF NOT EXISTS memories (
  id INTEGER PRIMARY KEY,
  agent TEXT NOT NULL CHECK(agent='hermes'),
  content TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(agent) REFERENCES identity(agent)
);

-- lessons: evidence-gated, suspend after 2 verified failures (helo pattern)
CREATE TABLE IF NOT EXISTS lessons (
  id INTEGER PRIMARY KEY,
  agent TEXT NOT NULL CHECK(agent='hermes'),
  content TEXT NOT NULL,
  evidence_ref TEXT NOT NULL,
  status TEXT NOT NULL CHECK(status IN ('active','suspended')),
  failures INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL,
  FOREIGN KEY(agent) REFERENCES identity(agent)
);

CREATE TRIGGER IF NOT EXISTS no_import_memories BEFORE INSERT ON memories
  WHEN NEW.evidence_ref NOT LIKE 'hermes:%'
  BEGIN SELECT RAISE(ABORT,'hermes: evidence required'); END;

CREATE TRIGGER IF NOT EXISTS no_import_lessons BEFORE INSERT ON lessons
  WHEN NEW.evidence_ref NOT LIKE 'hermes:%'
  BEGIN SELECT RAISE(ABORT,'hermes: evidence required'); END;

-- ── graph layer ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS entities (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL CHECK(kind IN ('person','org','place','event','project','account','device')),
  name TEXT NOT NULL,
  canonical_key TEXT NOT NULL UNIQUE,   -- lowercase, dot-form: 'a.doe'
  attributes TEXT NOT NULL DEFAULT '{}', -- JSON
  first_seen TEXT, last_seen TEXT,
  source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS relations (
  id INTEGER PRIMARY KEY,
  from_id INTEGER NOT NULL REFERENCES entities(id),
  to_id INTEGER NOT NULL REFERENCES entities(id),
  rel_type TEXT NOT NULL,               -- spouse_of, parent_of, works_at, lives_at, friend_of,
                                        -- treats, agent_of, located_in, hired_by, member_of,
                                        -- built_by, part_of, searches_for, uses, paid_to ...
  attributes TEXT NOT NULL DEFAULT '{}', -- JSON (titles, dates, notes)
  valid_from TEXT, valid_to TEXT,        -- time-aware: valid_to NULL = current
  source TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rel_from ON relations(from_id);
CREATE INDEX IF NOT EXISTS idx_rel_to ON relations(to_id);
CREATE INDEX IF NOT EXISTS idx_rel_type ON relations(rel_type);

CREATE TABLE IF NOT EXISTS facts (
  id INTEGER PRIMARY KEY,
  entity_id INTEGER REFERENCES entities(id),  -- NULL = global fact
  content TEXT NOT NULL,
  confidence TEXT NOT NULL CHECK(confidence IN ('measured','reported','inferred')),
  evidence_ref TEXT NOT NULL,
  created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_facts_entity ON facts(entity_id);

-- FTS5 over entities + facts for fuzzy recall (plain table: contentless tables
-- return NULL on column selects)
CREATE VIRTUAL TABLE IF NOT EXISTS mem_fts USING fts5(
  doc_id, kind, text
);
