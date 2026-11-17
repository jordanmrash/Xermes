#!/usr/bin/env python3
"""seed_example.py — build a throwaway example DB and run the verification
battery against it.

This is the repository's "proves it runs" artifact (helo/ACL doctrine): it
demonstrates the full loop — schema init, idempotent seeding, FTS recall,
evidence-trigger rejection (foreign evidence AND foreign agent), read-only
query path, and integrity — using ONLY clearly-labeled example data.

No production data lives in this repository. The live memory store of an
adoption is machine-specific and stays on the adopting machine.

Usage:
  python3 seed_example.py            # temp DB, self-test, cleaned up
  python3 seed_example.py --db PATH  # build at PATH instead
Exit code 0 = all checks passed, 1 = any check failed.
"""
import sqlite3, json, hashlib, pathlib, datetime, sys, tempfile, os, subprocess

HERE = pathlib.Path(__file__).resolve().parent
TODAY = datetime.date.today().isoformat()

def sha(s): return hashlib.sha256(s.encode()).hexdigest()

def connect(path):
    c = sqlite3.connect(str(path)); c.execute("PRAGMA foreign_keys=ON"); return c

def init(path):
    c = connect(path)
    if not c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='identity'").fetchone():
        c.executescript((HERE / "schema.sql").read_text().replace("PRAGMA foreign_keys=ON;", ""))
        c.execute("INSERT INTO identity VALUES ('hermes', 1)")
    c.commit()
    return c

def ev(c, source, outcome, payload):
    row = c.execute("SELECT id FROM evidence WHERE source=? AND payload=? AND agent='hermes'",
                    (source, payload)).fetchone()
    if row: return row[0]
    c.execute("INSERT INTO evidence(agent,source,outcome,payload,payload_sha256) VALUES('hermes',?,?,?,?)",
              (source, outcome, payload, sha(payload)))
    return c.execute("SELECT last_insert_rowid()").fetchone()[0]

# ── EXAMPLE DATA ONLY ──────────────────────────────────────────────────────
# Generic placeholder entities demonstrating each kind and the evidence
# pattern. Replace with your own seeder on an adopting machine.
EXAMPLE_ENTS = [
    ("person", "A. Doe", "a.doe",
     {"role": "example person", "email": "a.doe@example.com"}, "example-doc"),
    ("org", "Acme Corp", "acme.corp",
     {"role": "example employer"}, "example-doc"),
    ("place", "12 Main St", "12.main.st",
     {"role": "example residence; purchased 2020-05"}, "example-doc"),
    ("project", "proj-alpha", "proj.alpha",
     {"role": "example agent project"}, "example-statement-2026-01-01"),
]
EXAMPLE_RELS = [
    ("a.doe", "acme.corp", "works_at", {"title": "example role"}, "2020", None),
    ("a.doe", "12.main.st", "lives_at", {"since": "2020-05"}, None, None),
    ("proj.alpha", "a.doe", "built_by", {}, None, None),
]
EXAMPLE_FACTS = [
    ("a.doe", "Example measured fact: verified in primary data", "measured", "example-doc"),
    ("a.doe", "Example inferred fact: deduced, labeled as such", "inferred", "example-doc"),
    (None, "Example global fact: tiering note", "measured", "example-statement-2026-01-01"),
]

def seed(c):
    n = {"ent": 0, "rel": 0, "fac": 0}
    ids = {}
    for kind, name, key, attrs, source in EXAMPLE_ENTS:
        row = c.execute("SELECT id FROM entities WHERE canonical_key=?", (key,)).fetchone()
        if row:
            ids[key] = row[0]; continue
        e = ev(c, source, "measured", f"example entity {key}")
        c.execute("INSERT INTO entities(kind,name,canonical_key,attributes,first_seen,last_seen,source) VALUES(?,?,?,?,?,?,?)",
                  (kind, name, key, json.dumps(attrs), TODAY, TODAY, f"hermes:{e}"))
        ids[key] = c.execute("SELECT last_insert_rowid()").fetchone()[0]
        n["ent"] += 1
    for fk, tk, rt, attrs, vf, vt in EXAMPLE_RELS:
        ex = c.execute("SELECT 1 FROM relations WHERE from_id=? AND to_id=? AND rel_type=? AND valid_from IS ? AND valid_to IS ?",
                       (ids[fk], ids[tk], rt, vf, vt)).fetchone()
        if ex: continue
        e = ev(c, "example-doc", "measured", f"{fk} {rt} {tk}")
        c.execute("INSERT INTO relations(from_id,to_id,rel_type,attributes,valid_from,valid_to,source) VALUES(?,?,?,?,?,?,?)",
                  (ids[fk], ids[tk], rt, json.dumps(attrs), vf, vt, f"hermes:{e}"))
        n["rel"] += 1
    for ek, content, conf, source in EXAMPLE_FACTS:
        if c.execute("SELECT 1 FROM facts WHERE content=?", (content,)).fetchone(): continue
        e = ev(c, source, conf, content)
        eid = ids.get(ek)
        c.execute("INSERT INTO facts(entity_id,content,confidence,evidence_ref,created_at) VALUES(?,?,?,?,?)",
                  (eid, content, conf, f"hermes:{e}", TODAY))
        n["fac"] += 1
    c.execute("INSERT INTO mem_fts(doc_id,kind,text) SELECT 'e'||id,'entity',name||' '||attributes FROM entities")
    c.execute("INSERT INTO mem_fts(doc_id,kind,text) SELECT 'f'||id,'fact',content FROM facts")
    c.execute("INSERT INTO mem_fts(doc_id,kind,text) SELECT 'r'||id,'relation',rel_type||' ' FROM relations")
    c.commit()
    return n

def main():
    args = sys.argv[1:]
    db_path = args[args.index("--db") + 1] if "--db" in args else os.path.join(tempfile.mkdtemp(prefix="xermes-mg-"), "example.sqlite3")
    init(pathlib.Path(db_path))
    c = connect(db_path)
    first = seed(c)
    checks = []
    def ck(name, ok, detail=""):
        checks.append((name, ok, detail))

    ck("seed counts", first == {"ent": 4, "rel": 3, "fac": 3}, str(first))
    ck("idempotent re-seed", seed(c) == {"ent": 0, "rel": 0, "fac": 0})
    ck("integrity", c.execute("PRAGMA integrity_check").fetchone()[0] == "ok")
    try:
        c.execute("INSERT INTO memories(agent,content,evidence_ref,created_at) VALUES('hermes','x','external:rogue','x')")
        ck("trigger: foreign evidence rejected", False, "insert was accepted")
    except sqlite3.IntegrityError:
        ck("trigger: foreign evidence rejected", True)
    try:
        c.execute("INSERT INTO memories(agent,content,evidence_ref,created_at) VALUES('other','x','hermes:1','x')")
        ck("trigger: foreign agent rejected", False, "insert was accepted")
    except sqlite3.IntegrityError:
        ck("trigger: foreign agent rejected", True)
    # read-only query path (helo pattern)
    uri = "file:" + pathlib.Path(db_path).resolve().as_posix() + "?mode=ro"
    with sqlite3.connect(uri, uri=True) as ro:
        ro.execute("PRAGMA query_only=ON")
        n_ents = ro.execute("SELECT count(*) FROM entities").fetchone()[0]
        ck("read-only entity count", n_ents == 4, str(n_ents))
        hits = ro.execute("SELECT count(*) FROM mem_fts WHERE mem_fts MATCH '\"acme\"'").fetchone()[0]
        ck("FTS recall (acme)", hits >= 1, str(hits))
        row = ro.execute("SELECT name FROM entities WHERE canonical_key='12.main.st'").fetchone()
        ck("entity resolution", row is not None and row[0] == "12 Main St")
        rel = ro.execute("""SELECT r.rel_type FROM relations r
                            JOIN entities e ON e.id=r.to_id WHERE e.canonical_key='12.main.st'""").fetchone()
        ck("relation traversal", rel is not None and rel[0] == "lives_at")
    # memq CLI smoke test (env override -> no live DB needed)
    out = subprocess.run([sys.executable, str(HERE / "memq.py"), "search", "acme"],
                         capture_output=True, text=True,
                         env={**os.environ, "MEMQ_DB": str(db_path)})
    ck("memq CLI search", out.returncode == 0 and "acme" in out.stdout.lower(),
       (out.stderr or out.stdout)[:120])
    out2 = subprocess.run([sys.executable, str(HERE / "memq.py"), "entity", "12.main.st"],
                          capture_output=True, text=True,
                          env={**os.environ, "MEMQ_DB": str(db_path)})
    ck("memq CLI entity", out2.returncode == 0 and "lives_at" in out2.stdout,
       (out2.stderr or out2.stdout)[:120])

    c.close()
    failed = [c for c in checks if not c[1]]
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not pathlib.Path(db_path).parent.name.startswith("xermes-mg-"):
        print(f"example DB left at: {db_path}")
    else:
        os.remove(db_path); os.rmdir(pathlib.Path(db_path).parent)
    print(f"\n{len(checks) - len(failed)}/{len(checks)} checks passed")
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
