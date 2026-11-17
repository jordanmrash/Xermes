#!/usr/bin/env python3
"""memq — query/write CLI for the hermes memory graph (helo-adapted SQLite store).
Usage:
  memq.py stats
  memq.py search <text...>                 FTS over entities/facts/relations
  memq.py entity <key-or-name>             entity + attributes + facts + relations
  memq.py neighbors <key>                  all relations (both directions) resolved
  memq.py facts [key]                      facts for entity (or all)
  memq.py add-fact <entity|global> <measured|reported|inferred> <source> <content...>
  memq.py add-entity <kind> <name> <key> <source> [attrs-json]
  memq.py add-relation <from> <to> <type> <source> [attrs-json] [valid_from] [valid_to]
Read-only commands open the DB read-only (helo pattern). Writes always create a
hermes: evidence row — the no-import trigger rejects anything else.
"""
import sqlite3, json, hashlib, pathlib, datetime, sys, os

ROOT = pathlib.Path(__file__).resolve().parent
DB = pathlib.Path(os.environ.get("MEMQ_DB") or (ROOT / "hermes-memory.sqlite3"))

def ro():
    uri = "file:" + DB.resolve().as_posix() + "?mode=ro"
    c = sqlite3.connect(uri, uri=True, timeout=5)
    c.execute("PRAGMA query_only=ON")
    return c

def rw():
    c = sqlite3.connect(str(DB)); c.execute("PRAGMA foreign_keys=ON"); return c

def ev(c, source, outcome, payload):
    row = c.execute("SELECT id FROM evidence WHERE source=? AND payload=? AND agent='hermes'",
                    (source, payload)).fetchone()
    if row: return row[0]
    c.execute("INSERT INTO evidence(agent,source,outcome,payload,payload_sha256) VALUES('hermes',?,?,?,?)",
              (source, outcome, payload, hashlib.sha256(payload.encode()).hexdigest()))
    return c.execute("SELECT last_insert_rowid()").fetchone()[0]

def resolve(c, key_or_name):
    row = c.execute("SELECT id, kind, name, canonical_key, attributes, first_seen, last_seen, source FROM entities WHERE canonical_key=? OR lower(name)=lower(?)",
                    (key_or_name, key_or_name)).fetchone()
    return row

def print_entity(r):
    eid, kind, name, key, attrs, fs, ls, src = r
    print(f"{kind} | {name} | key={key} | {fs}->{ls} | src={src}")
    print(f"  attrs: {json.dumps(json.loads(attrs))}")
    print("  facts:")
    for f in ro().execute("SELECT id, confidence, content FROM facts WHERE entity_id=?", (eid,)).fetchall():
        print(f"    [{f[1]}] (#{f[0]}) {f[2]}")
    print("  relations:")
    for fr, to, rt, attrs, vf, vt in ro().execute("""
        SELECT CASE WHEN r.from_id=? THEN e1.name ELSE e2.name END,
               CASE WHEN r.from_id=? THEN e2.name ELSE e1.name END,
               r.rel_type, r.attributes, r.valid_from, r.valid_to
        FROM relations r JOIN entities e1 ON e1.id=r.from_id JOIN entities e2 ON e2.id=r.to_id
        WHERE r.from_id=? OR r.to_id=?""", (eid, eid, eid, eid)).fetchall():
        a = json.loads(attrs) if attrs != "{}" else ""
        span = f" ({vf or '—'}→{vt or 'now'})"
        other = fr if fr != name else to
        d = "→" if fr != name else "←"
        print(f"    {d} {other} [{rt}] {a}{span}")

def main():
    a = sys.argv[1:]
    if not a: print(__doc__); return
    cmd = a[0]
    if cmd == "stats":
        with ro() as c:
            print(json.dumps({
                "entities": c.execute("SELECT count(*) FROM entities").fetchone()[0],
                "relations": c.execute("SELECT count(*) FROM relations").fetchone()[0],
                "facts": c.execute("SELECT count(*) FROM facts").fetchone()[0],
                "evidence": c.execute("SELECT count(*) FROM evidence").fetchone()[0],
                "by_kind": dict(c.execute("SELECT kind, count(*) FROM entities GROUP BY kind")),
                "integrity": c.execute("PRAGMA integrity_check").fetchone()[0],
            }, indent=1))
    elif cmd == "search":
        q = " ".join(a[1:])
        try:
            with ro() as c:
                for doc, kind, text in c.execute(
                    "SELECT doc_id, kind, snippet(mem_fts, 2, '>>','<<','…',12) FROM mem_fts WHERE mem_fts MATCH ? LIMIT 15",
                    (f'"{q}" OR ' + " OR ".join(f'"{w}"' for w in q.split()),)):
                    print(f"[{doc}] {text}")
        except sqlite3.OperationalError:
            print("no FTS match")
    elif cmd == "entity":
        r = resolve(ro(), a[1])
        if not r: print(f"entity not found: {a[1]}"); return
        print_entity(r)
    elif cmd == "neighbors":
        r = resolve(ro(), a[1])
        if not r: print(f"entity not found: {a[1]}"); return
        eid = r[0]
        with ro() as c:
            for fr, to, rt, attrs, vf, vt in c.execute("""
                SELECT CASE WHEN r.from_id=? THEN e1.name ELSE e2.name END,
                       CASE WHEN r.from_id=? THEN e2.name ELSE e1.name END,
                       r.rel_type, r.attributes, r.valid_from, r.valid_to
                FROM relations r JOIN entities e1 ON e1.id=r.from_id JOIN entities e2 ON e2.id=r.to_id
                WHERE r.from_id=? OR r.to_id=? ORDER BY rel_type""", (eid, eid, eid, eid)).fetchall():
                a2 = json.loads(attrs) if attrs != "{}" else ""
                d = "→" if fr != r[2] else "←"
                print(f"{d} {fr} [{rt}] {a2} ({vf or '—'}→{vt or 'now'})")
    elif cmd == "facts":
        with ro() as c:
            if len(a) > 1:
                r = resolve(c, a[1])
                if not r: print("entity not found"); return
                rows = c.execute("SELECT id, confidence, content, created_at FROM facts WHERE entity_id=? ORDER BY created_at", (r[0],)).fetchall()
            else:
                rows = c.execute("SELECT id, confidence, content, created_at FROM facts ORDER BY created_at").fetchall()
            for i, conf, content, created in rows:
                print(f"[{conf}] (#{i}, {created}) {content}")
    elif cmd == "add-fact":
        target, conf, source, content = a[1], a[2], a[3], " ".join(a[4:])
        with rw() as c:
            if target == "global":
                eid = None
            else:
                r = resolve(c, target)
                if not r: sys.exit(f"entity not found: {target}")
                eid = r[0]
            e = ev(c, source, conf, content)
            c.execute("INSERT INTO facts(entity_id,content,confidence,evidence_ref,created_at) VALUES(?,?,?,?,?)",
                      (eid, content, conf, f"hermes:{e}", datetime.date.today().isoformat()))
            c.execute("INSERT INTO mem_fts(doc_id,kind,text) VALUES('f'||last_insert_rowid(),'fact',?)", (content,))
            c.commit()
            print(f"fact #{c.execute('SELECT last_insert_rowid()').fetchone()[0]} added (evidence hermes:{e})")
    elif cmd == "add-entity":
        kind, name, key, source = a[1], a[2], a[3], a[4]
        attrs = json.loads(a[5]) if len(a) > 5 else {}
        with rw() as c:
            if c.execute("SELECT 1 FROM entities WHERE canonical_key=?", (key,)).fetchone():
                sys.exit(f"entity exists: {key}")
            e = ev(c, source, "measured", f"entity {key} {name}")
            c.execute("INSERT INTO entities(kind,name,canonical_key,attributes,first_seen,last_seen,source) VALUES(?,?,?,?,?,?,?)",
                      (kind, name, key, json.dumps(attrs), datetime.date.today().isoformat(), datetime.date.today().isoformat(), f"hermes:{e}"))
            c.execute("INSERT INTO mem_fts(doc_id,kind,text) VALUES('e'||last_insert_rowid(),'entity',?)", (name + " " + json.dumps(attrs),))
            c.commit()
            print(f"entity {key} added")
    elif cmd == "add-relation":
        fkey, tkey, rtype, source = a[1], a[2], a[3], a[4]
        attrs = json.loads(a[5]) if len(a) > 5 and a[5] != "{}" else {}
        vf = a[6] if len(a) > 6 else None
        vt = a[7] if len(a) > 7 else None
        with rw() as c:
            rf, rt = resolve(c, fkey), resolve(c, tkey)
            if not rf or not rt: sys.exit("entity not found")
            e = ev(c, source, "measured", f"{fkey} {rtype} {tkey}")
            c.execute("INSERT INTO relations(from_id,to_id,rel_type,attributes,valid_from,valid_to,source) VALUES(?,?,?,?,?,?,?)",
                      (rf[0], rt[0], rtype, json.dumps(attrs), vf, vt, f"hermes:{e}"))
            c.commit()
            print(f"relation {fkey} -> {tkey} [{rtype}] added")
    else:
        print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
