#!/usr/bin/env python3
"""Validate animation companion coverage without altering static artwork."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
manifest = ROOT / "assets/animations/manifest.json"
data = json.loads(manifest.read_text(encoding="utf-8"))
errors = []
for item in data["companions"]:
    companion = ROOT / "assets" / item["source"]
    static = ROOT / "assets" / item["static"]
    if not companion.exists(): errors.append(f"missing companion: {item['source']}")
    if not static.exists(): errors.append(f"missing static source: {item['static']}")
    if companion.exists():
        text = companion.read_text(encoding="utf-8")
        for required in ("data-emoji-animation=", "prefers-reduced-motion", "xlink:href="):
            if required not in text: errors.append(f"{item['source']}: missing {required}")
if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"validated {len(data['companions'])} animation companions and static pairings")
