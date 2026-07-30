#!/usr/bin/env python3
"""Validate the complete card-ready tapered SVG corpus."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, default=Path("assets/gray-all"))
    args = parser.parse_args()
    root = args.source_dir
    items = json.loads((root / "manifest.json").read_text())
    files = [root / item["source"] for item in items]
    missing = [str(path) for path in files if not path.exists()]
    bad_style = []
    bad_system = []
    bad_markers = []
    upstream_empty = []
    for path in files:
        text = path.read_text(errors="replace")
        if 'data-castalia-style="sumi-e-ink-wash-v1"' not in text:
            bad_style.append(path.name)
        if 'data-ink-stroke-system="tapered-v1"' not in text:
            bad_system.append(path.name)
        if any(token in text for token in ("<marker", "marker-start", "marker-end")):
            bad_markers.append(path.name)
        if 'data-ink-coverage="upstream-empty"' in text:
            upstream_empty.append(path.name)
    if missing or bad_style or bad_system or bad_markers:
        raise SystemExit({
            "missing": missing[:10],
            "bad_style": bad_style[:10],
            "bad_system": bad_system[:10],
            "bad_markers": bad_markers[:10],
        })
    print(f"SVG set checked: {len(files)} complete tapered card glyphs")
    if upstream_empty:
        print(f"upstream-empty glyphs preserved: {len(upstream_empty)} ({', '.join(upstream_empty)})")


if __name__ == "__main__":
    main()
