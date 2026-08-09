#!/usr/bin/env python3
"""Verify that PUA SVG brush marks can be animated without changing their artwork."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    args = parser.parse_args()
    failures = []
    count = 0
    for svg in sorted(args.root.rglob("*.svg")):
        if svg.parent.name == "references":
            continue
        count += 1
        root = ET.parse(svg).getroot()
        if root.get("data-ink-animation") not in {"draw-v1", "wash-v1"}:
            failures.append(f"{svg}: missing draw-v1/wash-v1 animation contract")
        strokes = [
            node for node in root.iter()
            if local(node.tag) == "path" and node.get("class", "").split().__contains__("ink-stroke")
        ]
        for node in strokes:
            if node.get("pathLength") != "1":
                failures.append(f"{svg}: ink stroke missing pathLength=1")
        if not strokes and root.get("data-ink-animation") != "wash-v1":
            failures.append(f"{svg}: no animatable strokes but not marked wash-v1")
    if failures:
        raise SystemExit("\n".join(failures[:30]) + ("\n..." if len(failures) > 30 else ""))
    print(f"SVG animation checked: {count} PUA glyphs with normalized draw/wash contracts")


if __name__ == "__main__":
    main()
