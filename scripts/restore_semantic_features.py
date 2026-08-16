#!/usr/bin/env python3
"""Restore tiny semantic marks lost by generic centerline tracing."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)

# Coordinates are in the normalized 72-unit recovered viewBox. These are
# deliberately open, slightly irregular almond strokes—not filled dots—so the
# repair obeys the stroke-only source rule while remaining legible at card size.
FEATURES = {
    "1F436.svg": [(28.2, 29.5, 1.25, 0.88, 0.08), (44.7, 29.5, 1.25, 0.88, -0.06)],
    "1F98A.svg": [(25.0, 40.4, 1.35, 0.96, 0.12), (47.0, 40.4, 1.35, 0.96, -0.10)],
}


def eye(cx: float, cy: float, rx: float, ry: float, lean: float) -> ET.Element:
    # Two restrained curves make an open brush almond. The slight lean and
    # unequal control points avoid the sterile, typeset oval produced by a
    # generic ellipse while keeping the mark recognizable at 16–32 px.
    left_x = cx - rx
    right_x = cx + rx
    upper_y = cy - ry * (0.72 + lean)
    lower_y = cy + ry * (0.58 - lean)
    d = (
        f"M {left_x:.2f} {cy + ry * 0.06:.2f} "
        f"C {cx - rx * 0.62:.2f} {upper_y:.2f} {cx + rx * 0.50:.2f} {upper_y - ry * 0.10:.2f} {right_x:.2f} {cy - ry * 0.04:.2f} "
        f"M {right_x:.2f} {cy - ry * 0.04:.2f} "
        f"C {cx + rx * 0.54:.2f} {lower_y:.2f} {cx - rx * 0.52:.2f} {lower_y + ry * 0.12:.2f} {left_x:.2f} {cy + ry * 0.06:.2f}"
    )
    return ET.Element(f"{{{SVG_NS}}}path", {
        "class": "ink-stroke",
        "data-ink-stroke": "tapered",
        "data-ink-role": "semantic-eye",
        "pathLength": "1",
        "d": d,
        "fill": "none",
        "stroke": "#262421",
        "stroke-width": "0.66",
        "stroke-linecap": "round",
        "stroke-linejoin": "round",
    })


def remove_old_eye_traces(group: ET.Element, cx: float, cy: float) -> None:
    """Remove recovered fragments wholly inside one tiny eye region."""
    for node in list(group):
        if node.tag.rsplit("}", 1)[-1] != "path":
            continue
        if node.get("data-ink-role") != "centerline-recovered":
            continue
        values = [float(value) for value in re.findall(r"[-+]?(?:\d+\.\d+|\d+|\.\d+)", node.get("d", ""))]
        if len(values) < 4:
            continue
        xs = values[0::2]
        ys = values[1::2]
        if min(xs) >= cx - 4.2 and max(xs) <= cx + 4.2 and min(ys) >= cy - 4.2 and max(ys) <= cy + 4.2:
            group.remove(node)


def repair(root: Path, filename: str) -> None:
    target = root / filename
    tree = ET.parse(target)
    svg = tree.getroot()
    group = next((node for node in svg if node.tag.rsplit("}", 1)[-1] == "g"), svg)
    for node in list(group):
        if node.get("data-ink-role") == "semantic-eye":
            group.remove(node)
    for cx, cy, rx, ry, lean in FEATURES[filename]:
        remove_old_eye_traces(group, cx, cy)
        group.append(eye(cx, cy, rx, ry, lean))
    tree.write(target, encoding="utf-8", xml_declaration=True)
    print(f"restored {len(FEATURES[filename])} semantic eye strokes in {target}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("assets/gray-all"))
    parser.add_argument("filenames", nargs="*", default=list(FEATURES))
    args = parser.parse_args()
    for filename in args.filenames:
        if filename not in FEATURES:
            raise SystemExit(f"no reviewed feature recipe for {filename}")
        repair(args.root, filename)


if __name__ == "__main__":
    main()
