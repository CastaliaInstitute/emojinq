#!/usr/bin/env python3
"""Convert grayscale vector wash contours into stroke-only SVG studies.

This is an authoring conversion for detailed reference art.  It preserves the
traced vector contours while replacing filled grayscale masses with rounded,
tone-mapped strokes, so the output can be animated and inspected as SVG line
work without embedding the source raster.
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


def luminance(paint: str) -> int:
    match = re.fullmatch(r"#?([0-9a-fA-F]{6})", paint.strip())
    if not match:
        return 128
    value = match.group(1)
    red, green, blue = (int(value[i:i + 2], 16) for i in (0, 2, 4))
    return round(0.2126 * red + 0.7152 * green + 0.0722 * blue)


def stroke_width(paint: str) -> float:
    # Darker traced washes carry a loaded nib; pale contours remain hairline
    # detail.  Keep all weights usable at 72-unit glyph scale.
    tone = luminance(paint)
    return max(0.18, min(1.22, 1.24 - tone / 255.0))


def convert(source: Path, target: Path) -> int:
    tree = ET.parse(source)
    root = tree.getroot()
    root.set("data-castalia-style", "sumi-e-naturalist-v2")
    root.set("data-ink-stroke-system", "tone-mapped-contour-v1")
    root.set("data-ink-animation", "draw-v1")
    root.set("data-ink-path-units", "normalized")
    root.set("data-ink-coverage", "complete")
    count = 0
    for element in root.iter():
        if local(element.tag) != "path" or not element.get("d"):
            continue
        paint = element.get("fill", "#4a4943")
        element.set("class", "ink-stroke")
        element.set("data-ink-stroke", "tapered")
        element.set("data-ink-role", "vector-wash-contour")
        element.set("data-ink-index", str(count))
        element.set("pathLength", "1")
        element.set("fill", "none")
        element.set("stroke", paint)
        element.set("stroke-width", f"{stroke_width(paint):.2f}")
        element.set("stroke-linecap", "round")
        element.set("stroke-linejoin", "round")
        count += 1
    target.parent.mkdir(parents=True, exist_ok=True)
    tree.write(target, encoding="utf-8", xml_declaration=True)
    return count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    count = convert(args.input, args.output)
    print(f"converted {count} vector wash contours to strokes: {args.output}")


if __name__ == "__main__":
    main()
