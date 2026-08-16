#!/usr/bin/env python3
"""Release gate for real, label-blind PUA recognition evidence."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
LEDGER = ROOT / "assets" / "pua-recognition-review.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
REQUIRED_EVIDENCE_FIELDS = (
    "reviewer", "reviewed_at", "ink_recognized_as", "color_recognized_as", "evidence",
)


def main() -> None:
    developmental = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    expected = {
        entry["source"]
        for entry in developmental["entries"]
        if entry.get("family") == "pua" and entry.get("track") in CANDIDATE_TRACKS
    }
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = ledger.get("items", [])
    actual = {item.get("source") for item in items}
    if actual != expected or len(items) != len(expected):
        raise SystemExit(
            f"recognition ledger scope mismatch: expected {len(expected)} unique candidates, found {len(actual)}"
        )
    incomplete = []
    for item in items:
        missing = [field for field in REQUIRED_EVIDENCE_FIELDS if not str(item.get(field, "")).strip()]
        if item.get("status") != "approved" or missing:
            incomplete.append((item["source"], item.get("status", "missing"), missing))
    if incomplete:
        sample = "; ".join(
            f"{source} [{status}; missing {','.join(missing) or 'none'}]"
            for source, status, missing in incomplete[:8]
        )
        raise SystemExit(
            f"label-blind recognition evidence incomplete for {len(incomplete)}/{len(items)} candidates: {sample}"
        )
    print(f"recognition evidence checked: {len(items)} label-blind ink/color approvals")


if __name__ == "__main__":
    main()
