#!/usr/bin/env python3
"""Enforce the source-level decisions from the manual PUA semantic audit."""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

from mark_intentional_pua_components import REVIEWED
from rank_developmental_vocabulary import PUA_CONTEXTUAL_REVIEW
from redraw_pua_semantic_audit_batch import ART


ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"
DEVELOPMENTAL = ROOT / "assets" / "developmental-vocabulary.json"


def main() -> None:
    entries = {
        entry["source"]: entry
        for entry in json.loads(DEVELOPMENTAL.read_text(encoding="utf-8"))["entries"]
        if entry.get("family") == "pua"
    }
    failures: list[str] = []

    for category, stems in PUA_CONTEXTUAL_REVIEW.items():
        for stem in stems:
            source = f"{category}/{stem}.svg"
            entry = entries.get(source)
            if not entry or entry.get("track") != "context" or not entry.get("reason", "").startswith("manual audit:"):
                failures.append(f"{source}: manual contextual classification missing")

    material_entries = [entry for source, entry in entries.items() if source.startswith("materials/")]
    if not material_entries or any(entry.get("track") != "context" for entry in material_entries):
        failures.append("materials: every substance must remain outside the single-object queue")

    for source in ART:
        relative = f"{source}.svg"
        root = ET.parse(PUA / relative).getroot()
        if root.get("data-semantic-audit") != "label-independent-defining-parts-v1":
            failures.append(f"{relative}: reviewed defining-parts construction missing")
        if entries.get(relative, {}).get("track") != "referent":
            failures.append(f"{relative}: manually redrawn whole object left the referent queue")

    for source, expected_class in REVIEWED.items():
        root = ET.parse(PUA / source).getroot()
        if root.get("data-intentional-components") != expected_class:
            failures.append(f"{source}: reviewed component classification missing")
        if root.get("data-component-review") != "severity-contact-sheet-2026-08-v1":
            failures.append(f"{source}: component review provenance missing")

    if failures:
        raise SystemExit("\n".join(failures))
    print(
        f"PUA semantic audit checked: {sum(map(len, PUA_CONTEXTUAL_REVIEW.values()))} "
        f"source-level contextual decisions, {len(material_entries)} materials, "
        f"{len(ART)} defining-part redraws, {len(REVIEWED)} reviewed multi-part layouts"
    )


if __name__ == "__main__":
    main()
