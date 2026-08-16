#!/usr/bin/env python3
"""Turn the abstract pattern/colour PUA family into hand-loaded brush marks."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "patterns"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*v) for v in values]


def ribbon(values, width, seed, color="#262522", dry=False) -> str:
    d = stroke_path(p(*values), width=width, seed=seed, wobble=.25, taper_start=.12, taper_end=.10)
    cls = "ink-dry" if dry else "ink-wash"
    return f'<path class="{cls}" d="{d}" fill="{color}" data-ink-brush-pass="{"dry-edge-v1" if dry else "loaded-ribbon-v2"}"/>'


def dry(values, width, seed, color="#77746a") -> list[str]:
    return [
        f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>'
        for d in dry_brush_paths(p(*values), width=width, seed=seed, breaks=2)
    ]


def mass(d, fill="#bcb9af") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{fill}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx, cy, rx, ry, fill="#4a4943") -> str:
    return f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    cp = re.search(r'data-pua="([^"]+)"', source)
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="patterns / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>patterns / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


# Pigment names are represented by distinct value/mark, not literal colour.
for name, fill, seed, marks in [
    ("black", "#262522", "black", [
        ribbon([(13, 43, .10), (22, 32, .70), (35, 27, 1.0), (49, 30, .82), (59, 39, .10)], 5.6, "black-loaded", "#262522"),
        ribbon([(18, 49, .10), (30, 44, .72), (43, 45, .96), (55, 41, .08)], .9, "black-dry", "#77746a", True),
    ]),
    ("gray", "#77746a", "gray", [
        ribbon([(12, 34, .10), (23, 28, .70), (36, 31, 1.0), (48, 27, .72), (59, 33, .08)], 3.1, "gray-mist-high", "#77746a"),
        ribbon([(17, 44, .10), (29, 39, .72), (41, 42, .94), (54, 38, .08)], 1.3, "gray-mist-low", "#bcb9af", True),
    ]),
    ("white", "#dedbd4", "white", [
        ribbon([(36, 16, .08), (47, 18, .72), (55, 27, .96), (57, 39, .84), (50, 50, .72), (38, 56, .92), (25, 53, .72), (17, 44, .84), (16, 31, .72), (24, 21, .70), (36, 16, .08)], 1.7, "white-empty-field", "#77746a"),
        ribbon([(25, 25, .10), (32, 21, .72), (41, 21, .08)], .65, "white-paper-edge", "#dedbd4", True),
    ]),
    ("brown", "#4a4943", "brown", [
        ribbon([(13, 47, .10), (23, 39, .72), (35, 41, 1.0), (47, 36, .72), (59, 43, .08)], 3.4, "brown-earth-host", "#4a4943"),
        ribbon([(18, 52, .10), (29, 47, .72), (42, 49, .94), (55, 45, .08)], 1.1, "brown-earth-dry", "#77746a", True),
        dab(31, 37, 1.3, .9, "#262522"),
    ]),
    ("blue", "#77746a", "blue", [
        ribbon([(13, 41, .08), (22, 31, .72), (32, 28, .96), (42, 34, .92), (53, 28, .08)], 3.8, "blue-sweep"),
        ribbon([(18, 49, .08), (29, 42, .72), (41, 43, .96), (54, 37, .08)], 1.0, "blue-dry", "#bcb9af", True),
    ]),
    ("green", "#4a4943", "green", [
        ribbon([(36, 57, .08), (34, 46, .72), (36, 34, .96), (42, 25, .08)], 2.0, "green-stem"),
        ribbon([(35, 40, .08), (28, 34, .72), (19, 31, .08)], 3.0, "green-leaf-l", "#77746a"),
        ribbon([(37, 37, .08), (45, 31, .72), (54, 29, .08)], 3.0, "green-leaf-r", "#262522"),
    ]),
    ("purple", "#77746a", "purple", [
        ribbon([(36, 56, .08), (36, 43, .72), (36, 29, .08)], 1.35, "purple-stem", "#262522"),
        ribbon([(36, 34, .08), (28, 28, .72), (20, 27, .08)], 3.2, "purple-petal-l", "#77746a"),
        ribbon([(36, 34, .08), (44, 28, .72), (52, 27, .08)], 3.2, "purple-petal-r", "#bcb9af"),
        dab(36, 25, 3.0, 2.5, "#262522"),
    ]),
    ("red", "#262522", "red", [
        ribbon([(36, 57, .08), (36, 44, .72), (36, 31, .08)], 1.4, "red-stem", "#77746a"),
        ribbon([(36, 34, .08), (29, 27, .72), (24, 22, .08)], 3.6, "red-petal-l"),
        ribbon([(36, 34, .08), (43, 27, .72), (48, 22, .08)], 3.6, "red-petal-r", "#4a4943"),
        dab(36, 35, 2.4, 2.1, "#262522"),
    ]),
    ("yellow", "#4a4943", "yellow", [
        ribbon([(36, 57, .08), (36, 44, .72), (36, 31, .08)], 1.3, "yellow-stem", "#77746a"),
        ribbon([(36, 34, .08), (28, 29, .72), (20, 30, .08)], 3.0, "yellow-petal-l", "#262522"),
        ribbon([(36, 34, .08), (44, 29, .72), (52, 30, .08)], 3.0, "yellow-petal-r", "#77746a"),
        ribbon([(36, 34, .08), (36, 26, .72), (36, 19, .08)], 2.8, "yellow-petal-top", "#bcb9af"),
    ]),
    ("orange", "#4a4943", "orange", [
        ribbon([(15, 41, .10), (20, 29, .65), (32, 22, .96), (45, 24, .88), (53, 33, .72), (51, 44, .92), (41, 51, .82), (29, 49, .72), (24, 41, .65), (29, 33, .72), (38, 31, .92), (44, 36, .08)], 2.7, "orange-peel", "#4a4943"),
        ribbon([(20, 51, .10), (30, 54, .72), (41, 52, .08)], .72, "orange-peel-dry", "#77746a", True),
    ]),
    ("silver", "#bcb9af", "silver", [
        ribbon([(36, 57, .08), (32, 47, .72), (29, 37, .96), (33, 26, .08)], 3.2, "silver-drop", "#77746a"),
        ribbon([(40, 52, .08), (46, 43, .72), (49, 34, .08)], 1.0, "silver-edge", "#262522", True),
    ]),
]:
    write(name, marks)


write("circle", [
    ribbon([(36, 10, .08), (47, 12, .72), (57, 20, .96), (62, 31, .94), (60, 44, .88), (51, 55, .72), (39, 61, .96), (25, 58, .72), (15, 50, .90), (10, 38, .78), (13, 26, .84), (22, 16, .70), (36, 10, .08)], 3.0, "circle-contour"),
    *dry([(23, 18, .10), (31, 15, .72), (42, 16, .94), (51, 21, .08)], .8, "circle-dry"),
])
write("oval", [
    ribbon([(18, 36, .08), (25, 27, .72), (38, 24, .96), (52, 27, .90), (58, 36, .82), (52, 45, .72), (38, 49, .96), (24, 45, .72), (18, 36, .08)], 3.0, "oval-contour"),
    ribbon([(25, 35, .10), (34, 31, .72), (45, 32, .08)], .75, "oval-dry", "#77746a", True),
])
write("square", [
    ribbon([(19, 18, .08), (34, 17, .72), (52, 18, .92), (54, 34, .90), (53, 53, .84), (35, 55, .92), (18, 53, .78), (18, 35, .90), (19, 18, .08)], 2.9, "square-contour"),
    ribbon([(25, 24, .10), (36, 23, .72), (47, 24, .08)], .75, "square-dry", "#77746a", True),
])
write("triangle", [
    ribbon([(36, 12, .08), (28, 28, .72), (20, 46, .96), (17, 53, .88), (35, 54, .94), (54, 53, .80), (47, 37, .72), (36, 12, .08)], 3.0, "triangle-contour"),
    ribbon([(29, 47, .10), (36, 45, .72), (44, 47, .08)], .75, "triangle-dry", "#77746a", True),
])
write("corner", [
    ribbon([(19, 17, .08), (20, 36, .72), (20, 54, .94), (39, 54, .88), (56, 54, .08)], 2.6, "corner-mark"),
    ribbon([(25, 20, .08), (26, 37, .72), (26, 48, .08)], .62, "corner-inner", "#77746a", True),
])
write("line", [
    ribbon([(13, 38, .08), (27, 36, .72), (41, 37, .96), (58, 35, .08)], 2.1, "line-mark"),
    ribbon([(18, 43, .08), (29, 41, .72), (42, 42, .96), (52, 40, .08)], .65, "line-dry", "#77746a", True),
])
write("curve", [
    ribbon([(16, 49, .08), (20, 37, .72), (28, 26, .94), (39, 20, .86), (53, 18, .08)], 2.6, "curve-mark"),
    ribbon([(19, 53, .08), (26, 42, .72), (35, 35, .08)], .72, "curve-dry", "#77746a", True),
])
write("edge", [ribbon([(15, 52, .08), (21, 40, .72), (29, 28, .94), (39, 19, .08)], 3.2, "edge-loaded"), ribbon([(22, 51, .08), (28, 40, .72), (36, 29, .08)], .7, "edge-dry", "#77746a", True)])
write("gold", [
    dab(36, 35, 3.0, 2.7, "#262522"),
    ribbon([(36, 31, .08), (36, 22, .72), (37, 13, .08)], 1.9, "gold-ray-top", "#4a4943"),
    ribbon([(32, 33, .08), (25, 27, .72), (18, 22, .08)], 1.45, "gold-ray-left", "#77746a", True),
    ribbon([(40, 33, .08), (48, 27, .72), (56, 23, .08)], 1.7, "gold-ray-right", "#4a4943"),
    ribbon([(33, 38, .08), (26, 44, .72), (20, 51, .08)], 1.35, "gold-ray-low-left", "#4a4943"),
    ribbon([(40, 38, .08), (47, 45, .72), (53, 52, .08)], 1.1, "gold-ray-low-right", "#77746a", True),
])
write("sphere", [
    ribbon([(36, 12, .08), (48, 14, .72), (57, 24, .96), (60, 37, .82), (54, 50, .72), (42, 58, .92), (28, 57, .72), (17, 48, .84), (13, 35, .72), (19, 22, .72), (36, 12, .08)], 3.0, "sphere-contour"),
    ribbon([(18, 35, .08), (29, 31, .72), (42, 32, .96), (57, 37, .08)], 1.6, "sphere-latitude", "#77746a", True),
    ribbon([(36, 15, .08), (31, 26, .72), (31, 39, .96), (36, 56, .08)], 1.4, "sphere-meridian", "#4a4943"),
])
write("cube", [
    ribbon([(36, 13, .08), (48, 18, .72), (57, 24, .08)], 2.7, "cube-top-right", "#262522"),
    ribbon([(36, 13, .08), (25, 18, .72), (15, 24, .08)], 2.1, "cube-top-left", "#77746a", True),
    ribbon([(15, 24, .08), (25, 30, .72), (36, 36, .08)], 2.35, "cube-mid-left", "#4a4943"),
    ribbon([(57, 24, .08), (47, 30, .72), (36, 36, .08)], 1.9, "cube-mid-right", "#77746a", True),
    ribbon([(15, 24, .08), (15, 36, .72), (16, 47, .08)], 2.0, "cube-left-edge", "#4a4943"),
    ribbon([(57, 24, .08), (57, 36, .72), (56, 47, .08)], 2.4, "cube-right-edge", "#262522"),
    ribbon([(16, 47, .08), (26, 54, .72), (36, 59, .08)], 1.8, "cube-low-left", "#77746a", True),
    ribbon([(56, 47, .08), (47, 54, .72), (36, 59, .08)], 2.2, "cube-low-right", "#4a4943"),
    ribbon([(36, 36, .08), (36, 48, .72), (36, 59, .08)], 1.7, "cube-center-edge", "#262522"),
])
write("pattern", [
    ribbon([(19, 53, .08), (24, 43, .72), (31, 36, .96), (39, 31, .82), (47, 22, .08)], 2.4, "pattern-host"),
    ribbon([(19, 24, .08), (27, 29, .72), (34, 37, .96), (41, 45, .82), (52, 51, .08)], 1.8, "pattern-guest", "#4a4943"),
    ribbon([(24, 55, .08), (34, 49, .72), (44, 51, .08)], .72, "pattern-dry", "#77746a", True),
])

print("redrew all 23 pattern and pigment PUA glyphs as vector brush studies")
