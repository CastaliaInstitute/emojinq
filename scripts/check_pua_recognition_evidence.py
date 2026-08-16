#!/usr/bin/env python3
"""Release gate for real, label-blind PUA recognition evidence."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
LEDGER = ROOT / "assets" / "pua-recognition-review.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
REQUIRED_EVIDENCE_FIELDS = (
    "reviewer", "reviewed_at", "ink_recognized_as", "color_recognized_as", "evidence",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        source = item["source"]
        ink_path = ROOT / "assets" / "pua" / source
        explicit_color = ROOT / "assets" / "pua-color" / source
        color_path = explicit_color if explicit_color.exists() else ink_path
        age = item.get("observer_age_months")
        protocol_ok = (
            isinstance(age, int)
            and 12 <= age <= 47
            and item.get("label_hidden") is True
            and item.get("choice_free") is True
            and item.get("review_scale_css_px") == 32
        )
        hashes_ok = (
            item.get("ink_sha256") == digest(ink_path)
            and item.get("color_sha256") == digest(color_path)
        )
        expected_color_mode = "familiar-color" if explicit_color.exists() else "ink-fallback"
        color_scope_ok = item.get("color_mode") == expected_color_mode
        if item.get("status") != "approved" or missing or not protocol_ok or not hashes_ok or not color_scope_ok:
            if not protocol_ok:
                missing.append("toddler_label_blind_protocol")
            if not hashes_ok:
                missing.append("current_asset_hashes")
            if not color_scope_ok:
                missing.append("color_scope")
            incomplete.append((item["source"], item.get("status", "missing"), missing))
    if incomplete:
        sample = "; ".join(
            f"{source} [{status}; missing {','.join(missing) or 'none'}]"
            for source, status, missing in incomplete[:8]
        )
        raise SystemExit(
            f"label-blind recognition evidence incomplete for {len(incomplete)}/{len(items)} candidates: {sample}"
        )
    print(f"recognition evidence checked: {len(items)} hash-bound toddler label-blind ink/color approvals")


if __name__ == "__main__":
    main()
