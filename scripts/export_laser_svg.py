#!/usr/bin/env python3
"""Export PUA artwork as binary monochrome SVG for bamboo laser workflows."""

from __future__ import annotations

import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def export_one(source: Path, target: Path) -> None:
    root = ET.parse(source).getroot()
    root.set("data-castalia-output", "laser-monochrome-v1")
    root.attrib.pop("data-ink-animation", None)
    root.attrib.pop("data-ink-path-units", None)
    for node in root.iter():
        node.attrib.pop("opacity", None)
        node.attrib.pop("class", None)
        fill = node.get("fill")
        stroke = node.get("stroke")
        if fill and fill.lower() != "none":
            node.set("fill", "#000000")
        if stroke and stroke.lower() != "none":
            node.set("stroke", "#000000")
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
    parser.add_argument("--source", type=Path, default=Path("assets/pua"))
    parser.add_argument("--output", type=Path, default=Path("build/laser-pua"))
    args = parser.parse_args()
    if args.output.exists():
        shutil.rmtree(args.output)
    count = 0
    for source in sorted(args.source.rglob("*.svg")):
        if source.parent.name == "references":
            continue
        export_one(source, args.output / source.relative_to(args.source))
        count += 1
    print(f"exported {count} monochrome laser SVGs to {args.output}")


if __name__ == "__main__":
    main()
