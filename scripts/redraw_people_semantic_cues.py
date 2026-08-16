#!/usr/bin/env python3
"""Add unmistakable semantic cues to near-duplicate people glyphs."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522"):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=.25), fill=color)


def add(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/people" / f"{name}.svg"
    text = target.read_text()
    if "data-semantic-cue" in text:
        return
    text = text.replace(
        f'aria-label="people / {name}"',
        f'aria-label="people / {name}" data-semantic-cue="distinctive-mark-v1"',
        1,
    )
    text = text.replace("</svg>", "".join(marks) + "</svg>")
    target.write_text(text)


# Nurse: a cap and a compact medical cross on the torso.
add("nurse", [
    ribbon([(30, 17, .2), (34, 14, .75), (40, 15, 1.0), (43, 18, .22)], 1.5, "nurse-cap"),
    ribbon([(36, 47, .2), (36, 54, .85)], 1.35, "nurse-cross-vertical"),
    ribbon([(32, 50, .2), (40, 50, .85)], 1.35, "nurse-cross-horizontal"),
])

# Healer: a sprig held forward, separating the role from a clinical nurse.
add("healer", [
    ribbon([(28, 52, .2), (25, 47, .7), (22, 42, .25)], 1.2, "healer-stem", "#4a4943"),
    ribbon([(24, 45, .2), (20, 43, .72), (18, 45, .25)], 1.15, "healer-leaf-left", "#3c3b36"),
    ribbon([(25, 47, .2), (29, 44, .72), (31, 45, .25)], 1.15, "healer-leaf-right", "#3c3b36"),
])

# Sage: a walking staff gives the quiet elder figure a clear role cue.
add("sage", [
    ribbon([(51, 31, .2), (52, 42, .65), (51, 54, 1.0), (52, 59, .2)], 1.45, "sage-staff", "#3c3b36"),
    ribbon([(51, 31, .2), (54, 29, .75), (56, 31, .2)], 1.05, "sage-staff-hook", "#77746a"),
])

# Seeker: a small lantern held out in front, with a single glow mark.
add("seeker", [
    ribbon([(47, 43, .2), (51, 47, .65), (55, 50, .22)], 1.1, "seeker-lantern-handle", "#3c3b36"),
    '<path data-semantic-cue="distinctive-mark-v1" class="ink-wash" fill="#4a4943" d="M 52 49 C 55 48 58 49 59 51 L 58 56 C 56 58 53 58 51 56 Z"/>',
    ribbon([(55, 45, .2), (58, 43, .7), (61, 44, .2)], .9, "seeker-glow", "#77746a"),
])

print("distinguished nurse, healer, sage, and seeker with semantic brush cues")
