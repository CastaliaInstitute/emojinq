#!/usr/bin/env python3
"""Reject stale developmental metadata or falsely asserted PUA review evidence."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from rank_developmental_vocabulary import load_entries


ROOT = Path(__file__).resolve().parents[1]
PUA_ROOT = ROOT / "assets" / "pua"
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
CANDIDATE_MARKER = "pua-object-scale-candidate-v2"
RETIRED_REVIEW_MARKER = "pua-concrete-referents-complete-v1"


def main() -> None:
    payload = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    actual = payload.get("entries", [])
    expected = load_entries()
    if actual != expected:
        actual_by_id = {entry["id"]: entry for entry in actual}
        expected_by_id = {entry["id"]: entry for entry in expected}
        changed = [
            key for key in sorted(actual_by_id.keys() | expected_by_id.keys())
            if actual_by_id.get(key) != expected_by_id.get(key)
        ]
        sample = ", ".join(changed[:8])
        raise SystemExit(
            f"developmental metadata is stale for {len(changed)} records"
            + (f" (first: {sample})" if sample else "")
        )

    pua_entries = [entry for entry in actual if entry.get("family") == "pua"]
    unresolved = [entry["source"] for entry in pua_entries if entry.get("track") == "unreviewed-referent"]
    if unresolved:
        raise SystemExit(f"PUA taxonomy contains {len(unresolved)} unreviewed referents")
    expected_candidates = {
        entry["source"] for entry in pua_entries if entry.get("track") in CANDIDATE_TRACKS
    }
    marked_candidates: set[str] = set()
    retired_claims: list[str] = []
    for path in sorted(PUA_ROOT.rglob("*.svg")):
        root = ET.parse(path).getroot()
        source = path.relative_to(PUA_ROOT).as_posix()
        if root.get("data-object-scale-candidate") == CANDIDATE_MARKER:
            marked_candidates.add(source)
        if root.get("data-toddler-review") == RETIRED_REVIEW_MARKER:
            retired_claims.append(source)
    if marked_candidates != expected_candidates:
        missing = sorted(expected_candidates - marked_candidates)
        extra = sorted(marked_candidates - expected_candidates)
        raise SystemExit(
            f"PUA candidate markers disagree with taxonomy: {len(missing)} missing, {len(extra)} extra"
        )
    if retired_claims:
        raise SystemExit(f"retired automatic toddler-review claim remains on {len(retired_claims)} SVGs")
    print(
        f"developmental metadata checked: {len(actual)} records, "
        f"{len(expected_candidates)} PUA object-scale candidates, 0 unreviewed PUA referents"
    )


if __name__ == "__main__":
    main()
