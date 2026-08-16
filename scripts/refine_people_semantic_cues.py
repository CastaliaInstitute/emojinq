#!/usr/bin/env python3
"""Strengthen the nurse/healer distinction at small glyph sizes."""
from __future__ import annotations

from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522"):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=.24), fill=color)


def append(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/people" / f"{name}.svg"
    text = target.read_text()
    if "semantic-cue-v2" in text:
        return
    target.write_text(text.replace("</svg>", ''.join(marks) + "</svg>")
        .replace('data-semantic-cue="distinctive-mark-v1"', 'data-semantic-cue="distinctive-mark-v2"', 1))


append("nurse", [
    ribbon([(36, 43, .2), (36, 49, .8), (36, 55, .2)], 1.85, "nurse-cross-v2"),
    ribbon([(31, 49, .2), (36, 49, .85), (41, 49, .2)], 1.85, "nurse-cross-bar-v2"),
])

append("healer", [
    ribbon([(43, 53, .18), (46, 46, .62), (50, 39, .94), (53, 31, .2)], 1.45, "healer-sprig-v2", "#3c3b36"),
    ribbon([(49, 41, .18), (44, 37, .76), (41, 38, .2)], 1.35, "healer-leaf-a-v2", "#262522"),
    ribbon([(50, 39, .18), (55, 35, .76), (58, 36, .2)], 1.35, "healer-leaf-b-v2", "#262522"),
    ribbon([(46, 47, .18), (41, 44, .76), (38, 45, .2)], 1.15, "healer-leaf-c-v2", "#4a4943"),
])

print("refined nurse cross and healer herb sprig")
