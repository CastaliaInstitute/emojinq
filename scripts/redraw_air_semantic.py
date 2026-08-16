#!/usr/bin/env python3
"""Make breeze and breath read as air movement rather than cloud faces."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.3):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(category: str, name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua" / category / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {category}/{name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 9 63 C 23 61 42 64 63 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="{category} / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>{category} / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("weather_sky", "breeze", [
    ribbon([(10, 28, .2), (18, 25, .7), (28, 26, 1.0), (38, 23, .6), (51, 25, .22)], 1.9, "breeze-upper"),
    ribbon([(10, 36, .18), (20, 34, .6), (31, 36, 1.0), (43, 33, .62), (59, 35, .18)], 2.25, "breeze-middle"),
    ribbon([(14, 45, .18), (23, 43, .6), (33, 45, .92), (43, 42, .55), (53, 43, .2)], 1.45, "breeze-lower", "#4a4943"),
    ribbon([(51, 24, .18), (56, 22, .7), (61, 24, .25)], 1.0, "breeze-tail", "#77746a"),
])

write("body", "breath", [
    ribbon([(19, 39, .2), (25, 36, .72), (31, 37, 1.0), (35, 40, .22)], 2.0, "breath-mouth"),
    ribbon([(36, 31, .18), (42, 28, .62), (50, 29, .95), (58, 26, .22)], 1.45, "breath-upper", "#4a4943"),
    ribbon([(38, 39, .18), (45, 37, .6), (53, 39, 1.0), (62, 36, .2)], 1.85, "breath-middle"),
    ribbon([(41, 47, .18), (48, 45, .6), (56, 47, 1.0), (63, 44, .2)], 1.25, "breath-lower", "#77746a"),
])

print("redrew breeze and breath as directional air brush studies")
