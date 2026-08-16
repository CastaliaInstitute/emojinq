#!/usr/bin/env python3
"""Clarify a few abstract science concepts with readable brush metaphors."""
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
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 9 63 C 24 61 42 64 63 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="science / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>science / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


# Compare: two different forms held against a shared measuring line.
write("compare", [
    ribbon([(14, 48, .2), (25, 47, .75), (36, 48, 1.0), (48, 47, .68), (59, 48, .2)], 1.45, "compare-baseline"),
    ribbon([(22, 46, .2), (20, 40, .72), (22, 34, 1.0), (28, 31, .7), (33, 34, .25), (32, 41, .2), (28, 46, .7)], 1.9, "compare-left", "#4a4943"),
    ribbon([(43, 46, .2), (42, 37, .72), (46, 28, 1.0), (53, 30, .7), (56, 37, .25), (54, 45, .2)], 2.15, "compare-right"),
    ribbon([(36, 25, .2), (36, 39, .8), (36, 48, .2)], .9, "compare-divider", "#77746a"),
])

# Hypothesis: a question held over a small experimental seed/idea.
write("hypothesis", [
    ribbon([(25, 47, .2), (30, 43, .7), (36, 42, 1.0), (42, 43, .7), (47, 47, .2)], 1.55, "hypothesis-ground", "#4a4943"),
    ribbon([(36, 42, .18), (36, 35, .7), (34, 31, 1.0), (31, 29, .5), (30, 26, .2)], 1.5, "hypothesis-stem", "#3c3b36"),
    ribbon([(30, 27, .2), (34, 24, .7), (38, 26, 1.0), (39, 29, .25)], 1.35, "hypothesis-leaf", "#262522"),
    ribbon([(46, 20, .2), (49, 17, .68), (54, 18, 1.0), (57, 22, .65), (56, 26, .25), (52, 29, .6), (52, 34, .2)], 1.7, "hypothesis-question", "#262522"),
    '<ellipse class="ink-wash" cx="52" cy="40" rx="1.8" ry="1.7" fill="#262522"/>',
])

# Theory: an open book supporting a connected explanatory structure.
write("theory", [
    ribbon([(12, 47, .2), (19, 43, .7), (28, 45, 1.0), (35, 49, .55), (36, 53, .2)], 1.7, "theory-book-left", "#4a4943"),
    ribbon([(60, 47, .2), (53, 43, .7), (44, 45, 1.0), (37, 49, .55), (36, 53, .2)], 1.7, "theory-book-right", "#4a4943"),
    ribbon([(24, 39, .2), (29, 33, .68), (36, 36, 1.0), (43, 30, .68), (49, 35, .2)], 1.35, "theory-structure", "#262522"),
    '<ellipse class="ink-wash" cx="24" cy="39" rx="2" ry="1.8" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="36" cy="36" rx="2" ry="1.8" fill="#4a4943"/>',
    '<ellipse class="ink-wash" cx="49" cy="35" rx="2" ry="1.8" fill="#262522"/>',
])

# Translation: two facing speech forms joined by a flowing exchange mark.
write("translation", [
    ribbon([(12, 30, .2), (17, 25, .7), (25, 24, 1.0), (31, 28, .7), (30, 34, .25), (25, 37, .2), (20, 36, .6), (17, 40, .2)], 1.8, "translation-left"),
    ribbon([(60, 42, .2), (55, 47, .7), (47, 48, 1.0), (41, 44, .7), (42, 38, .25), (47, 35, .2), (52, 36, .6), (55, 32, .2)], 1.8, "translation-right", "#4a4943"),
    ribbon([(31, 29, .18), (36, 32, .7), (41, 31, .25)], 1.15, "translation-forward", "#262522"),
    ribbon([(41, 44, .18), (36, 41, .7), (31, 42, .25)], 1.15, "translation-return", "#77746a"),
])

print("redrew compare, hypothesis, theory, and translation")
