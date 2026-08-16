#!/usr/bin/env python3
"""Validate complete Emojinq ontology coverage and orientation contracts."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY = json.loads((ROOT / "assets/ontology.json").read_text())
ALIGNMENTS = {"fixed", "profile-upright", "full-heading"}
ENVIRONMENTS = {"land", "air", "water-surface", "underwater", "subterranean", "space", "none"}
expected = set()
for relative in ("gray-all/manifest.json", "alpha-ink/manifest.json", "divination/manifest.json", "pua/manifest.json"):
    for item in json.loads((ROOT / "assets" / relative).read_text()):
        codepoints = item.get("codepoints") or []
        expected.add("-".join(f"{int(cp):X}" for cp in codepoints) or f"missing:{item.get('name')}")
entries = ONTOLOGY.get("entries", {})
missing = sorted(expected - set(entries))
if missing:
    raise SystemExit(f"ontology missing {len(missing)} glyphs; first: {missing[:5]}")
for key, entry in entries.items():
    orientation = entry.get("orientation", {})
    if orientation.get("travelAlignment") not in ALIGNMENTS:
        raise SystemExit(f"{key}: invalid travelAlignment")
    vector = orientation.get("vector")
    if not isinstance(vector, list) or len(vector) != 2:
        raise SystemExit(f"{key}: facing vector must have two components")
    if entry.get("embodiment", {}).get("mobility") != "fixed" and orientation.get("travelAlignment") != "fixed" and vector == [0, 0]:
        raise SystemExit(f"{key}: mobile travel-aligned glyph needs a facing vector")
    embodiment = entry.get("embodiment", {})
    environments = embodiment.get("environments")
    if not isinstance(environments, list) or not environments or not set(environments) <= ENVIRONMENTS:
        raise SystemExit(f"{key}: invalid environments")
    if embodiment.get("degreesOfFreedom") == 3 and environments[0] not in {"air", "underwater", "space"}:
        raise SystemExit(f"{key}: three-axis motion requires a volume environment")
print(f"ontology covers and orients all {len(expected)} unique Emojinq glyph sequences")
