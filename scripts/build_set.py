#!/usr/bin/env python3
"""Apply the Castalia pen treatment to a manifest of Noto SVG inputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from import_noto_svg import convert


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("assets/manifest.json"))
    parser.add_argument("--source-dir", type=Path, default=Path("assets/source"))
    parser.add_argument("--output-dir", type=Path, default=Path("assets/generated"))
    args = parser.parse_args()

    entries = json.loads(args.manifest.read_text())
    for entry in entries:
        convert(
            args.source_dir / entry["source"],
            args.output_dir / f"{entry['name']}.svg",
            entry["name"],
        )


if __name__ == "__main__":
    main()
