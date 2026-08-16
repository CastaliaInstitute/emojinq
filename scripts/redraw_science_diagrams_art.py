#!/usr/bin/env python3
"""Turn rigid science diagrams into readable sumi-e object studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.28):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/science" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 40 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>science / {name} — authored sumi-e study</title>{''.join(marks)}</svg>
''')


# Code: an open scroll with handwritten syntax marks, rather than a regular
# rounded rectangle that reads as a blank screen.
write("code", [
    ribbon([(17, 19, .2), (25, 16, .7), (39, 17, 1.0), (53, 19, .7), (58, 25, .2), (57, 46, .3), (51, 52, .8), (37, 54, 1.0), (23, 52, .55), (16, 46, .2), (17, 19, .2)], 1.55, "code-scroll", "#4a4943", .34),
    ribbon([(27, 30, .2), (23, 35, .7), (27, 40, .2)], 1.9, "code-angle-left", wobble=.32),
    ribbon([(43, 30, .2), (47, 35, .7), (43, 40, .2)], 1.9, "code-angle-right", wobble=.32),
    ribbon([(39, 28, .2), (36, 35, .7), (33, 42, .2)], 1.55, "code-slash", "#3c3b36", .32),
    ribbon([(29, 24, .2), (35, 23, .7), (41, 24, .2)], .9, "code-line-one", "#77746a"),
    ribbon([(28, 47, .2), (34, 46, .7), (40, 47, .2)], .9, "code-line-two", "#77746a"),
])

# Sequence: three distinct stations joined by a winding continuous stroke;
# no arrowheads, so the direction comes from spacing and gesture.
write("sequence", [
    ribbon([(12, 36, .18), (20, 33, .7), (28, 36, 1.0), (35, 40, .7), (42, 36, .2), (50, 31, .7), (60, 35, .2)], 1.35, "sequence-thread", "#4a4943", .34),
    '<ellipse class="ink-wash" cx="15" cy="36" rx="4.0" ry="3.5" fill="#3c3b36"/>',
    '<ellipse class="ink-wash" cx="36" cy="40" rx="4.0" ry="3.5" fill="#4a4943"/>',
    '<ellipse class="ink-wash" cx="57" cy="34" rx="4.0" ry="3.5" fill="#3c3b36"/>',
    ribbon([(13, 25, .2), (20, 23, .7), (27, 25, .2)], .9, "sequence-top-mark", "#77746a"),
])

# Server: a small stack of uneven equipment drawers with indicator dabs.
write("server", [
    '<path class="ink-wash" fill="#4a4943" d="M 18 18 C 25 16 46 17 54 20 L 53 31 C 44 33 27 32 18 30 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 17 34 C 26 32 47 33 55 36 L 54 47 C 43 49 27 48 17 46 Z"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 19 50 C 28 48 46 49 52 51 L 51 57 C 41 59 28 58 19 56 Z"/>',
    ribbon([(24, 22, .2), (32, 21, .7), (40, 22, .2)], .9, "server-slot-one", "#262522"),
    ribbon([(24, 38, .2), (33, 37, .7), (41, 38, .2)], .9, "server-slot-two", "#262522"),
    '<ellipse class="ink-wash" cx="47" cy="23" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="48" cy="39" rx="1.5" ry="1.3" fill="#262522"/>',
    ribbon([(22, 20, .2), (22, 29, .7), (22, 39, .2)], .8, "server-rack-edge", "#77746a"),
    ribbon([(50, 20, .2), (50, 29, .7), (50, 39, .2)], .8, "server-rack-edge-right", "#77746a"),
])

print("redrew code, sequence, and server as brush studies")
