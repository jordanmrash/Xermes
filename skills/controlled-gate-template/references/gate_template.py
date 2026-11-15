#!/usr/bin/env python3
"""Deterministic input gate — generalized from agent-of-record's validate_manifest.py.

The manifest names the required segments; nothing downstream runs until every one is
present and non-empty. A missing segment is a hard stop that names what is missing.
The gate produces no partial output, so a complete-looking deliverable cannot be built
from incomplete inputs by accident.

Exit codes: 0 complete, 3 a required segment is missing or empty, 2 could not run.

usage: gate_template.py <input-folder>

manifest.json (in the input folder):
{
  "workpaper": "<name of the deliverable>",
  "required_segments": [
    { "id": "A", "file": "segment-a.csv", "description": "<what it is>" },
    ...
  ]
}

CSV segments get a row count in the report; other files are presence/non-empty checks.
"""
import csv
import json
import os
import sys


def main(argv):
    if len(argv) != 1:
        print("usage: gate_template.py <input-folder>")
        return 2
    folder = argv[0]
    manifest_path = os.path.join(folder, "manifest.json")
    try:
        with open(manifest_path, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (OSError, ValueError) as exc:
        print("COULD NOT RUN: %s" % exc)
        return 2

    missing, present = [], []
    for seg in manifest["required_segments"]:
        path = os.path.join(folder, seg["file"])
        if not os.path.isfile(path) or os.path.getsize(path) == 0:
            missing.append(seg)
            continue
        detail = ""
        if path.lower().endswith(".csv"):
            try:
                with open(path, encoding="utf-8", newline="") as fh:
                    rows = list(csv.DictReader(fh))
                if not rows:
                    missing.append(seg)
                    continue
                detail = "%d rows" % len(rows)
            except (OSError, csv.Error) as exc:
                print("COULD NOT RUN: %s: %s" % (seg["file"], exc))
                return 2
        present.append((seg, detail))

    print("workpaper : %s" % manifest["workpaper"])
    for seg, detail in present:
        print("  present  %s  %-16s %s  %s" % (seg["id"], seg["file"], detail or "ok", seg["description"]))
    for seg in missing:
        print("  MISSING  %s  %-16s         %s" % (seg["id"], seg["file"], seg["description"]))

    if missing:
        ids = ", ".join(s["id"] for s in missing)
        print("HARD STOP: required segment(s) %s absent. No deliverable was produced." % ids)
        return 3

    print("complete  : %d of %d required segments present; downstream steps may run"
          % (len(present), len(manifest["required_segments"])))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
