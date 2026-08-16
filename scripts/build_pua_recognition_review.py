#!/usr/bin/env python3
"""Create or refresh the label-blind concrete-glyph recognition ledger."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"
OUTPUT = ROOT / "assets" / "pua-recognition-review.json"
CANDIDATE_TRACKS = {"concrete", "referent"}
CANDIDATE_FAMILIES = {"gray-all", "pua"}
PRESERVED = {
    "status", "reviewer", "reviewed_at", "ink_recognized_as",
    "color_recognized_as", "evidence", "notes", "observer_age_months",
    "label_hidden", "choice_free", "review_scale_css_px",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key_for(family: str, source: str) -> str:
    return f"{family}:{source}"


def asset_paths(family: str, source: str) -> tuple[Path, Path, str]:
    if family == "gray-all":
        return (
            ROOT / "assets" / "gray-all" / source,
            ROOT / "assets" / "color-all" / source,
            "familiar-color",
        )
    ink = ROOT / "assets" / "pua" / source
    explicit_color = ROOT / "assets" / "pua-color" / source
    return ink, explicit_color if explicit_color.exists() else ink, (
        "familiar-color" if explicit_color.exists() else "ink-fallback"
    )


def main() -> None:
    developmental = json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))
    existing: dict[str, dict] = {}
    if OUTPUT.exists():
        existing = {}
        for item in json.loads(OUTPUT.read_text(encoding="utf-8")).get("items", []):
            family = item.get("family", "pua")
            existing[key_for(family, item["source"])] = item
    candidates = sorted(
        (
            entry for entry in developmental["entries"]
            if entry.get("family") in CANDIDATE_FAMILIES and entry.get("track") in CANDIDATE_TRACKS
        ),
        key=lambda entry: (entry["family"], entry["source"]),
    )
    items = []
    for entry in candidates:
        family = entry["family"]
        source = entry["source"]
        item_id = key_for(family, source)
        old = existing.get(item_id, {})
        ink_path, color_path, color_mode = asset_paths(family, source)
        ink_sha256 = digest(ink_path)
        color_sha256 = digest(color_path)
        item = {
            "id": item_id,
            "family": family,
            "source": source,
            "group": entry.get("group") or source.split("/", 1)[0],
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
            "color_mode": color_mode,
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
        "version": 2,
        "method": "label-blind-object-scale-review",
        "instructions": (
            "Show every concrete standard and PUA ink/color or explicit fallback at 32 CSS pixels "
            "to a 12–47 month-old observer, "
            "without a label, hint, or answer choices. Record the observer's words verbatim. "
            "Approval requires recognizable identity in both presentations and evidence bound to these asset hashes."
        ),
        "items": items,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"recognition ledger refreshed: {len(items)} candidates")


if __name__ == "__main__":
    main()
