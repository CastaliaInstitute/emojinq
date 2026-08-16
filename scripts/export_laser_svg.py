#!/usr/bin/env python3
"""Export artwork as grayscale SVG for bamboo laser depth workflows.

The grayscale value is intentional production data: black is the deepest
engraving pass, white is the lightest/pass-through value, and intermediate
neutral grays are calibrated depth steps.  The SVG remains pure vector art so
the same geometry can be sent to a power-modulated laser or rasterized for a
display/font build.
"""

from __future__ import annotations

import argparse
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
HEX = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def grayscale(value: str) -> str:
    """Convert paint to an explicit neutral gray while preserving luminance."""
    match = HEX.match(value.strip())
    if not match:
        return "#000000"
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(ch * 2 for ch in digits)
    r, g, b = (int(digits[index:index + 2], 16) for index in (0, 2, 4))
    y = round(0.2126 * r + 0.7152 * g + 0.0722 * b)
    return f"#{y:02x}{y:02x}{y:02x}"


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def export_one(source: Path, target: Path) -> None:
    root = ET.parse(source).getroot()
    root.set("data-castalia-output", "laser-grayscale-v1")
    root.set("data-laser-depth-encoding", "neutral-luminance-linear-v1")
    root.set("data-laser-black", "deepest")
    root.set("data-laser-white", "lightest")
    root.set("data-laser-calibrate", "required")
    root.attrib.pop("data-ink-animation", None)
    root.attrib.pop("data-ink-path-units", None)
    for node in root.iter():
        node.attrib.pop("opacity", None)
        fill_opacity = node.attrib.pop("fill-opacity", None)
        stroke_opacity = node.attrib.pop("stroke-opacity", None)
        node.attrib.pop("class", None)
        fill = node.get("fill")
        stroke = node.get("stroke")
        if fill_opacity == "0":
            node.set("fill", "none")
            fill = "none"
        if stroke_opacity == "0":
            node.set("stroke", "none")
            stroke = "none"
        if fill and fill.lower() != "none":
            node.set("fill", grayscale(fill))
        if stroke and stroke.lower() != "none":
            node.set("stroke", grayscale(stroke))
        if local(node.tag) in {"path", "circle", "ellipse", "line", "polyline", "polygon", "rect"}:
            if node.get("stroke-width"):
                try:
                    width = float(node.get("stroke-width"))
                except ValueError:
                    width = 1.0
                node.set("stroke-width", f"{max(1.0, width):g}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(ET.tostring(root, encoding="unicode") + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("--output", type=Path, default=Path("build/laser-standard"))
    args = parser.parse_args()
    if args.output.exists():
        shutil.rmtree(args.output)
    count = 0
    for source in sorted(args.source.rglob("*.svg")):
        if source.parent.name == "references":
            continue
        export_one(source, args.output / source.relative_to(args.source))
        count += 1
    print(f"exported {count} grayscale laser SVGs to {args.output}")


if __name__ == "__main__":
    main()
