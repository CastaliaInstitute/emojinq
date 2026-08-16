#!/usr/bin/env python3
"""Make quantity/operator concepts read as intentional sumi-e symbols."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.25):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/science" / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 9 63 C 23 61 42 64 63 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>science / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("add", [
    ribbon([(36, 15, .18), (35, 25, .7), (36, 36, 1.0), (35, 47, .25)], 2.3, "add-vertical", wobble=.24),
    ribbon([(18, 36, .18), (28, 35, .7), (36, 36, 1.0), (45, 35, .72), (55, 36, .2)], 2.3, "add-horizontal", wobble=.24),
])

write("divide", [
    ribbon([(16, 36, .2), (27, 35, .72), (38, 36, 1.0), (49, 35, .72), (57, 36, .2)], 2.0, "divide-bar", wobble=.25),
    '<ellipse class="ink-wash" cx="36" cy="25" rx="2.7" ry="2.4" fill="#3c3b36"/>',
    '<ellipse class="ink-wash" cx="36" cy="47" rx="2.7" ry="2.4" fill="#3c3b36"/>',
])

write("equal", [
    ribbon([(17, 30, .18), (27, 29, .7), (38, 30, 1.0), (49, 29, .72), (57, 30, .2)], 2.1, "equal-upper", wobble=.25),
    ribbon([(17, 42, .18), (28, 41, .72), (39, 42, 1.0), (50, 41, .7), (57, 42, .2)], 2.1, "equal-lower", wobble=.25),
])

write("count", [
    ribbon([(15, 42, .2), (24, 37, .68), (33, 33, 1.0), (42, 28, .7), (51, 24, .2)], 1.45, "count-tally", "#4a4943", .28),
    '<ellipse class="ink-wash" cx="17" cy="25" rx="2.3" ry="2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="26" cy="25" rx="2.3" ry="2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="35" cy="25" rx="2.3" ry="2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="44" cy="25" rx="2.3" ry="2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="53" cy="25" rx="2.3" ry="2" fill="#262522"/>',
])

write("one", [
    ribbon([(36, 15, .16), (35, 25, .7), (36, 36, 1.0), (35, 48, .7), (36, 57, .18)], 3.0, "one-stroke", wobble=.3),
])

write("none", [
    ribbon([(26, 22, .2), (20, 27, .7), (19, 36, 1.0), (23, 45, .72), (32, 50, .28), (42, 49, .2), (51, 44, .68), (55, 36, .94), (52, 27, .5), (45, 22, .2)], 1.8, "none-open-ring", "#4a4943", .3),
    ribbon([(28, 36, .18), (36, 34, .7), (44, 36, .22)], 1.1, "none-empty-mark", "#77746a", .27),
])

print("redrew add, divide, equal, count, one, and none")
