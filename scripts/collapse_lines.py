#!/usr/bin/env python3
"""Convert reviewed area-style SVGs into scalable line-only artwork."""

from __future__ import annotations

import argparse
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "circle", "ellipse", "rect", "polygon", "polyline", "line"}
ECHO_CLASSES = {"ink-echo", "ink-echo-two", "ink-pencil"}
TOKEN_RE = re.compile(r"[AaCcHhLlMmQqSsTtVvZz]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
ARITY = {"M": 2, "L": 2, "T": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "A": 7}
ET.register_namespace("", SVG_NS)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def roughen_path(d: str, seed: int, amount: float = 0.32) -> str:
    """Add deterministic sub-pixel hand wobble to path coordinates."""
    tokens = TOKEN_RE.findall(d)
    command = None
    parameter = 0
    result = []
    for index, token in enumerate(tokens):
        if token.isalpha():
            command = token
            parameter = 0
            result.append(token)
            continue
        value = float(token)
        upper = command.upper() if command else ""
        arity = ARITY.get(upper, 0)
        slot = parameter % arity if arity else -1
        eligible = upper not in {"A"} or slot in {5, 6}
        if arity and eligible:
            phase = math.sin((seed + index * 17.0) * 12.9898) * 43758.5453
            wobble = (phase - math.floor(phase) - 0.5) * 2.0 * amount
            value += wobble
        result.append(f"{value:.3f}".rstrip("0").rstrip("."))
        parameter += 1
    return " ".join(result)


def collapse(root: ET.Element) -> None:
    root.set("data-castalia-style", "davinci-line-v2")
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
                        if float(element.get("stroke-width", "1")) < 0.7 and len(element.get("d", "")) < 100:
                            parent.remove(element)
                            continue
                    except ValueError:
                        pass
                element.set("fill", "none")
                try:
                    base_width = float(element.get("stroke-width", "0.95"))
                except ValueError:
                    base_width = 0.95
                if not element.get("stroke-width"):
                    base_width = 0.95
                variation = 0.72 + ((weight_index * 13) % 7) * 0.075
                element.set("stroke-width", f"{base_width * variation:.2f}")
                element.set("stroke-linecap", "round")
                element.set("stroke-linejoin", "round")
                if element.get("d"):
                    element.set("d", roughen_path(element.get("d", ""), weight_index))
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
