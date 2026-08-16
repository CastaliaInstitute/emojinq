#!/usr/bin/env python3
"""Create or refresh the label-blind PUA recognition review ledger."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
OUTPUT = ROOT / "assets" / "pua-recognition-review.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
PRESERVED = {
    "status", "reviewer", "reviewed_at", "ink_recognized_as",
    "color_recognized_as", "evidence", "notes",
}


def main() -> None:
    developmental = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    existing: dict[str, dict] = {}
    if OUTPUT.exists():
        existing = {
            item["source"]: item
            for item in json.loads(OUTPUT.read_text(encoding="utf-8")).get("items", [])
        }
    candidates = sorted(
        (
            entry for entry in developmental["entries"]
            if entry.get("family") == "pua" and entry.get("track") in CANDIDATE_TRACKS
        ),
        key=lambda entry: entry["source"],
    )
    items = []
    for entry in candidates:
        old = existing.get(entry["source"], {})
        item = {
            "source": entry["source"],
            "expected": entry["name"],
            "codepoints": entry["codepoints"],
            "status": "pending",
            "reviewer": "",
            "reviewed_at": "",
            "ink_recognized_as": "",
            "color_recognized_as": "",
            "evidence": "",
            "notes": "",
        }
        item.update({key: old[key] for key in PRESERVED if key in old})
        items.append(item)
    payload = {
        "version": 1,
        "method": "label-blind-object-scale-review",
        "instructions": (
            "Show ink and color variants without a label at toddler viewing size. "
            "Record the observer's words verbatim; approval requires recognizable identity in both variants."
        ),
        "items": items,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recognition ledger refreshed: {len(items)} candidates")


if __name__ == "__main__":
    main()
