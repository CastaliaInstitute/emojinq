#!/usr/bin/env python3
"""Clarify bench and ceiling as simple, readable sumi-e studies."""
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
    target = ROOT / "assets/pua/locations" / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 9 63 C 24 61 42 64 63 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="locations / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>locations / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("bench", [
    '<path class="ink-wash" fill="#4a4943" d="M 13 37 C 24 34 47 35 60 38 L 59 43 C 45 45 27 44 14 42 Z"/>',
    ribbon([(13, 39, .2), (25, 37, .7), (39, 39, 1.0), (53, 37, .7), (60, 39, .2)], 2.6, "bench-seat", wobble=.28),
    ribbon([(18, 42, .2), (20, 51, .8), (19, 57, .2)], 1.75, "bench-leg-left", "#4a4943", .27),
    ribbon([(54, 42, .2), (52, 51, .8), (53, 57, .2)], 1.75, "bench-leg-right", "#4a4943", .27),
    ribbon([(17, 31, .2), (27, 29, .75), (39, 30, 1.0), (52, 29, .65), (55, 31, .2)], 1.55, "bench-back", "#77746a", .26),
])

write("ceiling", [
    '<path class="ink-wash" fill="#4a4943" d="M 10 15 C 24 13 48 14 62 16 L 61 20 C 44 19 27 19 11 19 Z"/>',
    ribbon([(10, 16, .2), (23, 15, .72), (37, 16, 1.0), (51, 15, .7), (62, 16, .2)], 2.0, "ceiling-beam", wobble=.25),
    ribbon([(36, 17, .2), (36, 25, .8), (35, 31, .2)], 1.45, "ceiling-cord", "#4a4943", .24),
    ribbon([(29, 32, .2), (32, 35, .72), (36, 36, 1.0), (41, 35, .72), (44, 32, .2)], 1.75, "ceiling-lamp", "#262522", .27),
    ribbon([(32, 40, .2), (29, 45, .7), (27, 51, .25)], .9, "ceiling-light-left", "#77746a", .28),
    ribbon([(40, 40, .2), (43, 45, .7), (45, 51, .25)], .9, "ceiling-light-right", "#77746a", .28),
    '<path class="ink-wash" fill="#4a4943" d="M 29 34 C 32 31 40 31 44 34 C 42 39 32 39 29 34 Z"/>',
])

write("graph", [
    ribbon([(14, 54, .2), (14, 42, .7), (15, 29, 1.0), (14, 18, .2)], 1.65, "graph-axis-y", "#4a4943", .3),
    ribbon([(13, 54, .2), (26, 54, .7), (40, 53, 1.0), (55, 54, .7), (62, 53, .2)], 1.65, "graph-axis-x", "#4a4943", .3),
    ribbon([(18, 47, .2), (25, 44, .7), (32, 45, 1.0), (39, 38, .7), (46, 39, .2), (54, 27, .7), (60, 24, .2)], 2.0, "graph-curve", "#262522", .34),
    '<ellipse class="ink-wash" cx="25" cy="44" rx="1.8" ry="1.6" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="39" cy="38" rx="1.8" ry="1.6" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="54" cy="27" rx="1.8" ry="1.6" fill="#77746a"/>',
])

write("post", [
    '<path class="ink-wash" fill="#4a4943" d="M 14 21 C 23 18 48 19 58 22 L 57 39 C 46 42 25 41 14 38 Z"/>',
    ribbon([(36, 39, .2), (36, 49, .7), (35, 59, .2)], 2.0, "post-stem", "#262522", .3),
    ribbon([(29, 29, .2), (36, 27, .7), (48, 29, .2)], .9, "post-letter-one", "#77746a"),
    ribbon([(25, 34, .2), (35, 32, .7), (48, 34, .2)], .9, "post-letter-two", "#77746a"),
    ribbon([(27, 59, .2), (35, 57, .7), (44, 59, .2)], 1.2, "post-foot", "#77746a"),
])

write("net", [
    ribbon([(14, 22, .2), (14, 45, .7), (15, 57, .2)], 1.8, "net-pole-left", "#4a4943", .3),
    ribbon([(58, 22, .2), (58, 45, .7), (57, 57, .2)], 1.8, "net-pole-right", "#4a4943", .3),
    ribbon([(14, 30, .2), (25, 34, .7), (36, 37, 1.0), (47, 34, .7), (58, 30, .2)], 1.25, "net-top", "#262522", .34),
    ribbon([(14, 37, .2), (25, 41, .7), (36, 44, 1.0), (47, 41, .7), (58, 37, .2)], 1.0, "net-middle", "#77746a", .34),
    ribbon([(14, 44, .2), (25, 48, .7), (36, 51, 1.0), (47, 48, .7), (58, 44, .2)], .9, "net-bottom", "#77746a", .34),
    ribbon([(22, 33, .2), (25, 41, .7), (27, 48, .2)], .75, "net-weave-one", "#77746a", .34),
    ribbon([(33, 36, .2), (36, 44, .7), (39, 50, .2)], .75, "net-weave-two", "#77746a", .34),
    ribbon([(45, 34, .2), (47, 41, .7), (49, 48, .2)], .75, "net-weave-three", "#77746a", .34),
])

print("redrew bench and ceiling with explicit semantic silhouettes")
