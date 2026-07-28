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
    for parent in root.iter():
        for element in list(parent):
            class_names = set(element.get("class", "").split())
            is_echo = bool(class_names & ECHO_CLASSES) or element.get("stroke-dasharray")
            if is_echo:
                parent.remove(element)
                continue
            if local(element.tag) in SHAPES:
                element.set("fill", "none")


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
