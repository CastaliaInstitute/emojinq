#!/usr/bin/env python3
"""Create or refresh the label-blind PUA recognition review ledger."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
OUTPUT = ROOT / "assets" / "pua-recognition-review.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
PRESERVED = {
    "status", "reviewer", "reviewed_at", "ink_recognized_as",
    "color_recognized_as", "evidence", "notes", "observer_age_months",
    "label_hidden", "choice_free", "review_scale_css_px",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        ink_path = ROOT / "assets" / "pua" / entry["source"]
        explicit_color = ROOT / "assets" / "pua-color" / entry["source"]
        color_path = explicit_color if explicit_color.exists() else ink_path
        ink_sha256 = digest(ink_path)
        color_sha256 = digest(color_path)
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
            "observer_age_months": None,
            "label_hidden": False,
            "choice_free": False,
            "review_scale_css_px": 32,
            "ink_sha256": ink_sha256,
            "color_sha256": color_sha256,
            "color_mode": "familiar-color" if explicit_color.exists() else "ink-fallback",
        }
        same_art = (
            old.get("ink_sha256") == ink_sha256
            and old.get("color_sha256") == color_sha256
        )
        if same_art:
            item.update({key: old[key] for key in PRESERVED if key in old})
        elif old.get("status") == "approved":
            item["notes"] = "Approval reset because the reviewed art changed."
        items.append(item)
    payload = {
        "version": 1,
        "method": "label-blind-object-scale-review",
        "instructions": (
            "Show ink and color/fallback variants at 32 CSS pixels to a 12–47 month-old observer, "
            "without a label, hint, or answer choices. Record the observer's words verbatim. "
            "Approval requires recognizable identity in both presentations and evidence bound to these asset hashes."
        ),
        "items": items,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recognition ledger refreshed: {len(items)} candidates")


if __name__ == "__main__":
    main()
