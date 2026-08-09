#!/usr/bin/env python3
"""Verify that every PUA category is present in source, manifest, and review sheets."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"
SHEETS = ROOT / "build" / "pua-contact-sheets"

asset_categories = {
    path.name
    for path in PUA.iterdir()
    if path.is_dir() and path.name != "references"
}
manifest = json.loads((PUA / "manifest.json").read_text())
manifest_categories = {entry["source"].split("/", 1)[0] for entry in manifest}
missing_from_manifest = sorted(asset_categories - manifest_categories)
missing_assets = sorted(manifest_categories - asset_categories)
missing_sheets = sorted(
    category for category in asset_categories
    if not (SHEETS / f"{category}.jpg").exists()
)
empty_categories = sorted(
    category for category in asset_categories
    if not list((PUA / category).glob("*.svg"))
)

if missing_from_manifest or missing_assets or missing_sheets or empty_categories:
    raise SystemExit(
        json.dumps(
            {
                "missing_from_manifest": missing_from_manifest,
                "missing_assets": missing_assets,
                "missing_sheets": missing_sheets,
                "empty_categories": empty_categories,
            },
            indent=2,
        )
    )

print(
    f"PUA coverage checked: {len(asset_categories)} categories, "
    f"{len(manifest)} manifest entries, contact sheets present"
)
