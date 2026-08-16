#!/usr/bin/env python3
"""Author material concepts as tangible sumi-e object studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.3):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/materials" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 42 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="materials / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>materials / {name} — material sumi-e study</title>{''.join(marks)}</svg>
''')


# Cloth: a folded, soft-edged drape with a few hanging folds.
write("cloth", [
    '<path class="ink-wash" fill="#4a4943" d="M 14 28 C 20 24 29 27 36 25 C 43 22 51 26 57 30 L 54 45 C 45 50 27 50 18 45 Z"/>',
    ribbon([(18, 31, .2), (25, 35, .7), (34, 33, .2)], 1.1, "cloth-fold-one", "#77746a"),
    ribbon([(27, 45, .2), (31, 39, .7), (34, 33, .2)], .9, "cloth-fold-two", "#262522"),
    ribbon([(40, 46, .2), (43, 39, .7), (44, 29, .2)], .9, "cloth-fold-three", "#77746a"),
    ribbon([(48, 46, .2), (51, 40, .7), (52, 31, .2)], .8, "cloth-fold-four", "#77746a"),
])

# Fiber: a loose ball of interlaced strands with one trailing end.
write("fiber", [
    '<path class="ink-wash" fill="#4a4943" d="M 16 38 C 18 27 27 21 38 22 C 49 20 57 27 57 38 C 55 49 47 54 36 53 C 25 55 17 48 16 38 Z"/>',
    ribbon([(19, 35, .2), (28, 28, .7), (40, 29, 1.0), (52, 38, .2)], 1.0, "fiber-strand-one", "#77746a", .34),
    ribbon([(20, 44, .2), (30, 35, .7), (42, 36, 1.0), (53, 29, .2)], .9, "fiber-strand-two", "#262522", .34),
    ribbon([(25, 49, .2), (34, 41, .7), (46, 44, .2)], .85, "fiber-strand-three", "#77746a", .34),
    ribbon([(48, 48, .2), (57, 52, .7), (62, 49, .2)], 1.0, "fiber-tail", "#262522", .34),
])

# Glass: a thin tumbler with a wavering rim and translucent inner wash.
write("glass", [
    ribbon([(20, 22, .2), (29, 20, .7), (42, 21, 1.0), (52, 23, .2)], 1.35, "glass-rim", "#262522", .28),
    ribbon([(20, 23, .2), (22, 39, .7), (26, 52, 1.0), (46, 53, .7), (51, 40, .2)], 1.35, "glass-body", "#4a4943", .3),
    ribbon([(25, 28, .2), (28, 40, .7), (31, 49, .2)], .75, "glass-highlight", "#77746a", .32),
    ribbon([(27, 46, .2), (35, 48, .7), (44, 47, .2)], .8, "glass-reflection", "#77746a"),
])

# Leather: a worn satchel with flap, seam, and strap.
write("leather", [
    '<path class="ink-wash" fill="#4a4943" d="M 20 29 C 26 25 45 25 51 29 L 53 50 C 46 55 27 55 19 50 Z"/>',
    ribbon([(20, 30, .2), (29, 34, .7), (40, 33, 1.0), (51, 30, .2)], 1.35, "leather-flap", "#262522", .31),
    ribbon([(17, 27, .2), (14, 21, .7), (18, 17, .2), (23, 25, .2)], 1.35, "leather-strap", "#77746a", .34),
    ribbon([(27, 41, .2), (35, 43, .7), (44, 41, .2)], .8, "leather-stitch", "#77746a"),
])

# Metal: a worn circular washer/gear-like plate with an uneven center and
# sparse teeth, avoiding a rigid engineering diagram.
write("metal", [
    '<path class="ink-wash" fill="#4a4943" d="M 36 16 L 42 19 L 49 18 L 51 25 L 57 30 L 54 36 L 56 43 L 50 47 L 48 54 L 41 52 L 35 56 L 30 51 L 23 53 L 21 46 L 15 42 L 18 35 L 15 29 L 21 24 L 22 17 L 29 19 Z"/>',
    '<ellipse class="ink-wash" cx="36" cy="36" rx="10" ry="10" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="36" cy="36" rx="4" ry="4" fill="#262522"/>',
    ribbon([(28, 36, .2), (36, 29, .7), (44, 36, .2)], .8, "metal-wear", "#77746a"),
])

# Paper: a torn-edged sheet with a folded corner and handwritten lines.
write("paper", [
    '<path class="ink-wash" fill="#4a4943" d="M 18 17 L 50 18 L 55 25 L 53 53 L 19 52 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 43 18 L 52 25 L 43 26 Z"/>',
    ribbon([(25, 31, .2), (33, 29, .7), (45, 31, .2)], .85, "paper-line-one", "#262522"),
    ribbon([(25, 38, .2), (34, 36, .7), (46, 38, .2)], .85, "paper-line-two", "#77746a"),
    ribbon([(25, 45, .2), (32, 43, .7), (40, 45, .2)], .8, "paper-line-three", "#77746a"),
])

# Plastic: a light bottle with a cap, shoulder, and a single reflective mark.
write("plastic", [
    '<path class="ink-wash" fill="#4a4943" d="M 29 22 L 29 28 C 24 31 23 36 24 49 C 28 54 44 54 48 49 C 49 36 48 31 43 28 L 43 22 Z"/>',
    ribbon([(30, 21, .2), (35, 20, .7), (42, 21, .2)], 1.5, "plastic-cap", "#262522"),
    ribbon([(29, 37, .2), (36, 39, .7), (43, 37, .2)], .9, "plastic-label", "#77746a"),
    ribbon([(28, 32, .2), (30, 36, .7), (30, 42, .2)], .75, "plastic-highlight", "#77746a"),
])

# Sand: a wind-shaped dune with a few loose grains and a rippled face.
write("sand", [
    '<path class="ink-wash" fill="#4a4943" d="M 12 51 C 20 45 25 35 34 32 C 43 29 48 36 60 42 C 54 51 42 55 29 54 C 22 55 16 54 12 51 Z"/>',
    ribbon([(21, 47, .2), (31, 44, .7), (42, 45, .2)], .85, "sand-ripple-one", "#77746a"),
    ribbon([(26, 50, .2), (36, 48, .7), (48, 49, .2)], .8, "sand-ripple-two", "#77746a"),
    '<ellipse class="ink-wash" cx="18" cy="39" rx="1.4" ry="1.0" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="54" cy="34" rx="1.2" ry=".9" fill="#77746a"/>',
])

# Stone: an irregular faceted rock with a dark underside and a single plane.
write("stone", [
    '<path class="ink-wash" fill="#4a4943" d="M 15 47 L 20 28 L 34 20 L 51 24 L 58 40 L 48 52 L 27 55 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 20 28 L 34 20 L 39 34 L 27 40 Z"/>',
    '<path class="ink-wash" fill="#262522" d="M 27 40 L 39 34 L 58 40 L 48 52 L 27 55 Z"/>',
    ribbon([(25, 46, .2), (35, 48, .7), (46, 45, .2)], .8, "stone-wear", "#77746a"),
])

# Thread: a loose spool with a trailing, irregular strand.
write("thread", [
    '<path class="ink-wash" fill="#4a4943" d="M 26 27 C 31 23 44 23 49 27 L 48 49 C 43 54 31 54 26 49 Z"/>',
    ribbon([(26, 28, .2), (35, 31, .7), (48, 28, .2)], 1.25, "thread-spool-top", "#262522"),
    ribbon([(29, 35, .2), (37, 38, .7), (46, 35, .2)], .85, "thread-wrap-one", "#77746a"),
    ribbon([(29, 42, .2), (37, 45, .7), (46, 42, .2)], .85, "thread-wrap-two", "#77746a"),
    ribbon([(46, 29, .2), (54, 26, .7), (60, 30, .2), (56, 35, .7), (61, 39, .2)], 1.0, "thread-loose-end", "#262522", .36),
])

print("redrew cloth, fiber, glass, leather, metal, paper, plastic, sand, stone, and thread")
