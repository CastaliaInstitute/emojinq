#!/usr/bin/env python3
"""Bring weak people concepts up to the catalog's dense naturalist plate style."""

from __future__ import annotations

import copy
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/pua/people"
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522") -> str:
    return svg_path(stroke_path(p(*values), width=width, seed=seed, wobble=.2), fill=color)


def source_path(name: str) -> str:
    root = ET.parse(OUT / f"{name}.svg").getroot()
    for element in root.iter():
        if element.tag.rsplit("}", 1)[-1] == "path" and element.get("d"):
            item = copy.deepcopy(element)
            item.set("fill", "#262522")
            item.set("class", "ink-wash")
            item.set("data-ink-brush-pass", "naturalist-plate-v1")
            for key in ("opacity", "fill-opacity", "stroke-opacity", "stroke", "stroke-width", "style"):
                item.attrib.pop(key, None)
            return ET.tostring(item, encoding="unicode")
    raise SystemExit(f"no vector plate path found in {name}")


def write(target: str, source: str, marks: list[str], description: str) -> None:
    path = OUT / f"{target}.svg"
    original = path.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', original)
    if not codepoint:
        raise SystemExit(f"missing PUA codepoint in {path}")
    body = source_path(source) + "\n  " + "\n  ".join(marks)
    path.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="{NS}" viewBox="0 0 72 72" role="img" aria-label="people / {target}" {codepoint.group(0)} data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1" data-ink-animation="wash-v1" data-ink-path-units="normalized">
  <title>people / {target} — {description}</title>
  {body}
</svg>
'''
    )


write("alliance", "friend", [
    ribbon([(25, 40, .2), (31, 37, .72), (36, 39, 1.0), (41, 37, .72), (47, 40, .2)], 1.8, "alliance-linked-hands", "#4a4943"),
    ribbon([(31, 42, .2), (36, 45, .75), (41, 42, .2)], 1.0, "alliance-shared-bond", "#77746a"),
], "dense companion study with linked hands")

write("compassion", "empathy", [
    ribbon([(29, 28, .2), (34, 32, .72), (39, 37, 1.0), (45, 40, .2)], 2.2, "compassion-resting-hand", "#4a4943"),
    ribbon([(20, 50, .2), (30, 54, .7), (41, 53, .2)], .9, "compassion-ground", "#77746a"),
], "dense naturalist study of a steadying hand")

write("conflict", "cousin", [
    ribbon([(13, 35, .2), (22, 33, .68), (31, 38, 1.0), (36, 42, .2)], 2.2, "conflict-left-gesture", "#262522"),
    ribbon([(59, 35, .2), (50, 33, .68), (41, 38, 1.0), (36, 42, .2)], 2.2, "conflict-right-gesture", "#4a4943"),
    ribbon([(27, 45, .2), (34, 42, .72), (41, 45, .2)], 1.1, "conflict-tension", "#77746a"),
], "dense naturalist study of opposing figures")

write("cooperation", "community", [
    ribbon([(16, 41, .2), (28, 38, .72), (40, 41, 1.0), (54, 38, .2)], 2.0, "cooperation-shared-work", "#4a4943"),
    ribbon([(28, 43, .2), (36, 46, .72), (44, 43, .2)], 1.0, "cooperation-common-ground", "#77746a"),
], "dense group study with a shared burden")

write("help", "offering", [
    ribbon([(28, 47, .2), (35, 42, .72), (42, 35, 1.0), (49, 31, .2)], 2.25, "help-lifting-arm", "#4a4943"),
    ribbon([(43, 35, .2), (47, 32, .7), (51, 34, .2)], .95, "help-open-hand", "#77746a"),
], "dense figure study of an offered hand")

write("choice", "pilgrimage", [
    ribbon([(36, 51, .2), (29, 46, .68), (23, 42, 1.0), (16, 41, .2)], 1.6, "choice-left-path", "#4a4943"),
    ribbon([(36, 51, .2), (43, 46, .68), (50, 42, 1.0), (58, 41, .2)], 1.25, "choice-right-path", "#77746a"),
], "dense traveler study at a forked path")

write("humility", "offering", [
    ribbon([(29, 43, .2), (35, 47, .72), (42, 45, 1.0), (49, 40, .2)], 1.6, "humility-lowered-offering", "#4a4943"),
    ribbon([(46, 38, .2), (51, 34, .7), (54, 29, .2)], 1.0, "humility-sprig", "#77746a"),
], "dense bowed figure with a quiet offering")

write("mentor", "legacy", [
    ribbon([(26, 41, .2), (32, 37, .72), (38, 34, 1.0), (45, 31, .2)], 1.8, "mentor-pointing-hand", "#4a4943"),
    ribbon([(32, 47, .2), (39, 49, .7), (47, 47, .2)], 1.0, "mentor-open-book", "#77746a"),
], "dense elder and learner study with an open book")

write("welcome", "service", [
    ribbon([(16, 42, .2), (25, 36, .72), (35, 34, 1.0), (47, 36, .6), (57, 42, .2)], 1.8, "welcome-open-gesture", "#4a4943"),
    ribbon([(22, 53, .2), (36, 55, .7), (51, 53, .2)], .9, "welcome-threshold", "#77746a"),
], "dense host study with an open threshold")

write("work", "repair", [
    ribbon([(24, 40, .2), (33, 43, .7), (42, 40, 1.0), (51, 35, .2)], 2.0, "work-tool-hand", "#4a4943"),
    ribbon([(38, 43, .2), (45, 49, .7), (55, 49, .2)], 1.3, "work-bench-edge", "#77746a"),
], "dense craftsperson study at a workbench")

print("replaced ten sparse people concepts with dense vector naturalist plates")
