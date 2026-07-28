#!/usr/bin/env python3
"""Convert reviewed area-style SVGs into scalable line-only artwork."""

from __future__ import annotations

import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
ECHO_CLASSES = {"ink-echo", "ink-echo-two", "ink-pencil"}
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def collapse(root: ET.Element) -> None:
    root.set("data-castalia-style", "naturalist-line-v1")
    weight_index = 0
    for parent in root.iter():
        for element in list(parent):
            class_names = set(element.get("class", "").split())
            is_echo = bool(class_names & ECHO_CLASSES) or element.get("stroke-dasharray")
            if is_echo:
                parent.remove(element)
                continue
            if local(element.tag) in SHAPES:
                # Short, thin unmarked paths are usually decorative arcs from
                # the area illustration rather than semantic line structure.
                # Keep thicker/explicit geometry such as veins, text, steam,
                # windows, and mechanical details.
                if element.get("fill") == "none" and element.get("stroke-width"):
                    try:
                        if float(element.get("stroke-width", "1")) < 0.7 and element.get("data-ink-keep") != "true":
                            parent.remove(element)
                            continue
                    except ValueError:
                        pass
                element.set("fill", "none")
                if local(element.tag) == "path" and element.get("d"):
                    try:
                        base_width = float(element.get("stroke-width", "1.0"))
                    except ValueError:
                        base_width = 1.0
                    weighted = ET.fromstring(ET.tostring(element, encoding="unicode"))
                    weighted.set("fill", "none")
                    weighted.set("stroke", "#262522")
                    weighted.set("stroke-width", f"{base_width * 1.55:.2f}")
                    weighted.set("stroke-dasharray", "31 5 12 7 24 4 9 6")
                    weighted.set("stroke-dashoffset", str((weight_index * 7) % 23))
                    weighted.set("opacity", ".78")
                    rotation = ((weight_index % 5) - 2) * 0.16
                    weighted.set("transform", f"translate(.18 .12) rotate({rotation:.2f} 64 64)")
                    parent.insert(list(parent).index(element) + 1, weighted)
                    weight_index += 1


def convert(source: Path, output: Path) -> None:
    tree = ET.parse(source)
    root = tree.getroot()
    collapse(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("assets/canonical"))
    parser.add_argument("--output-dir", type=Path, default=Path("assets/line"))
    args = parser.parse_args()
    for source in sorted(args.input_dir.glob("*.svg")):
        convert(source, args.output_dir / source.name)


if __name__ == "__main__":
    main()
