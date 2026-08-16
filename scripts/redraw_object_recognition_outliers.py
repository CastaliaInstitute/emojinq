#!/usr/bin/env python3
"""Disambiguate concrete object glyphs that cannot share a stock silhouette."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/pua/objects"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(points, width, seed, color="#262421", wobble=.2):
    class_name = "ink-dry" if color in {"#77746a", "#bcb9af"} else "ink-wash"
    return svg_path(
        stroke_path(p(*points), width=width, seed=seed, wobble=wobble),
        fill=color,
        class_name=class_name,
    )


def mass(d: str, color="#262421") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{color}" data-ink-brush-pass="loaded-mass-v2"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    cp = re.search(r'data-pua="[^"]+"', target.read_text(encoding="utf-8"))
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="objects / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="draw-v1" data-naturalist-construction="toddler-anatomy-v1">
<title>objects / {name} — toddler-readable anatomical sumi-e study</title>{''.join(marks)}</svg>
''', encoding="utf-8")


# A small gallery wall: three unmistakable frames with different pictures.
write("gallery", [
    ribbon([(8, 24, .12), (27, 23, .85), (27, 46, .75), (8, 46, .85), (8, 24, .12)], 1.5, "gallery-left-frame"),
    ribbon([(31, 14, .12), (63, 15, .85), (62, 39, .75), (31, 38, .85), (31, 14, .12)], 1.7, "gallery-main-frame"),
    ribbon([(37, 45, .12), (62, 46, .85), (61, 61, .75), (37, 60, .85), (37, 45, .12)], 1.45, "gallery-right-frame"),
    ribbon([(11, 40, .12), (17, 33, .8), (23, 40, .12)], .85, "gallery-left-picture", "#77746a"),
    ribbon([(35, 33, .12), (43, 25, .8), (50, 31, .65), (58, 23, .12)], 1.0, "gallery-main-picture", "#4a4943"),
    ribbon([(40, 56, .12), (47, 50, .8), (56, 56, .12)], .8, "gallery-right-picture", "#77746a"),
    '<circle class="ink-wash" cx="54" cy="21" r="2" fill="#262421"/>',
])


# A front-facing oven: cooktop, knobs, glazed door, handle, and feet.
write("oven", [
    ribbon([(17, 14, .12), (55, 14, .9), (56, 59, .75), (16, 59, .9), (17, 14, .12)], 1.9, "oven-case"),
    ribbon([(17, 26, .12), (55, 26, .9)], 1.15, "oven-control-divider", "#4a4943"),
    ribbon([(23, 35, .12), (49, 35, .9), (49, 54, .75), (23, 54, .9), (23, 35, .12)], 1.45, "oven-door"),
    ribbon([(27, 31, .12), (45, 31, .9)], 1.5, "oven-handle"),
    ribbon([(22, 59, .12), (21, 63, .8)], 1.3, "oven-foot-left"),
    ribbon([(50, 59, .12), (51, 63, .8)], 1.3, "oven-foot-right"),
    '<circle class="ink-wash" cx="25" cy="20" r="2" fill="#262421"/><circle class="ink-wash" cx="36" cy="20" r="2" fill="#4a4943"/><circle class="ink-wash" cx="47" cy="20" r="2" fill="#262421"/>',
    ribbon([(27, 48, .12), (32, 42, .75), (38, 49, .9), (45, 41, .12)], .8, "oven-window-glint", "#77746a"),
])


# A physical doorway containing the universal running-person and right-arrow
# cues.  Open brush contours keep the exit readable without turning the whole
# door into a dense sign block.
write("exit", [
    ribbon([(11, 65, .12), (11, 9, .82), (60, 9, .9), (60, 65, .12)], 2.8, "exit-door-frame"),
    ribbon([(10, 65, .12), (35, 64, .85), (62, 65, .08)], 1.7, "exit-threshold", "#77746a"),
    ribbon([(18, 17, .12), (54, 17, .85), (54, 43, .78), (18, 43, .85), (18, 17, .12)], 1.5, "exit-sign-panel", "#77746a"),
    '<circle class="ink-wash" cx="29" cy="23" r="3.0" fill="#262421" data-ink-brush-pass="loaded-dab-v1"/>',
    ribbon([(29, 27, .12), (30, 33, .82), (27, 38, .08)], 2.2, "exit-runner-body"),
    ribbon([(30, 30, .12), (24, 33, .72), (20, 37, .08)], 1.35, "exit-runner-arm-back"),
    ribbon([(31, 30, .12), (36, 33, .72), (40, 34, .08)], 1.2, "exit-runner-arm-forward", "#4a4943"),
    ribbon([(28, 37, .12), (23, 41, .72), (19, 43, .08)], 1.55, "exit-runner-leg-back"),
    ribbon([(29, 37, .12), (35, 40, .72), (39, 43, .08)], 1.45, "exit-runner-leg-forward", "#4a4943"),
    ribbon([(39, 33, .12), (48, 33, .85), (56, 33, .08)], 2.0, "exit-arrow-shaft"),
    mass("M50 26 L61 33 L50 41 C52 37 53 35 56 33 C53 31 52 29 50 26 Z"),
    ribbon([(46, 53, .12), (54, 53, .82), (58, 51, .08)], 1.7, "exit-door-lever", "#4a4943"),
])

print("redrew exit, gallery, and oven as distinct concrete objects")
