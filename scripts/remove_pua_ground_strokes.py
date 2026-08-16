#!/usr/bin/env python3
"""Remove the old non-semantic baseline strokes from PUA artwork.

Earlier PUA generators appended a lightly curved line near y=60 as a visual
ground.  It is not part of the glyph and reads as a UI baseline/shadow.  This
script removes only the known dry-brush baseline geometry, leaving meaningful
waves, roots, horizons, and landscape marks untouched.
"""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def is_ground(node: ET.Element) -> bool:
    if local(node.tag) != "path":
        return False
    classes = set(node.get("class", "").split())
    if not (
        "ink-dry" in classes
        or "ink-stroke" in classes
        or node.get("data-ink-contour") == "naturalist-line-v3"
        or node.get("data-ink-ribbon-pass") == "v2"
    ):
        return False
    d = re.sub(r"\s+", " ", node.get("d", "").strip())
    # Some early passes wrote a simple cubic sweep; later naturalist passes
    # converted that same sweep into a closed ribbon.  Both remain shallow,
    # wide, and isolated at the bottom of the viewBox.
    values = [float(value) for value in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", d)]
    if len(values) < 8:
        return False
    xs = values[0::2]
    ys = values[1::2]
    return (
        min(ys) >= 56
        and max(ys) <= 68
        and max(ys) - min(ys) <= 8
        and max(xs) - min(xs) >= 35
        and len(values) >= 8
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    args = parser.parse_args()
    removed = 0
    files = 0
    for path in sorted(args.root.rglob("*.svg")):
        if path.parent.name == "references":
            continue
        tree = ET.parse(path)
        root = tree.getroot()
        count = 0
        for parent in root.iter():
            for child in list(parent):
                if is_ground(child):
                    parent.remove(child)
                    count += 1
        if count:
            tree.write(path, encoding="utf-8", xml_declaration=True)
            removed += count
            files += 1
    print(f"removed {removed} non-semantic PUA ground strokes from {files} SVGs")


if __name__ == "__main__":
    main()
