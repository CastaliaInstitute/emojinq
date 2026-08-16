#!/usr/bin/env python3
"""Author recognizable culinary and medicinal herbs as sparse sumi-e studies."""
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
    target = ROOT / "assets/pua/herbs" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 42 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="herbs / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>herbs / {name} — botanical sumi-e study</title>{''.join(marks)}</svg>
''')


# Aloe: a low rosette of thick, pointed leaves.
write("aloe", [
    ribbon([(36, 57, .2), (33, 47, .7), (27, 33, 1.0), (22, 23, .2)], 2.0, "aloe-left", "#4a4943", .34),
    ribbon([(36, 57, .2), (35, 45, .7), (35, 29, 1.0), (36, 16, .2)], 2.25, "aloe-center", "#262522", .34),
    ribbon([(37, 57, .2), (41, 47, .7), (48, 34, 1.0), (55, 25, .2)], 2.0, "aloe-right", "#4a4943", .34),
    ribbon([(34, 53, .2), (27, 46, .7), (18, 42, .2)], 1.8, "aloe-low-left", "#77746a", .34),
    ribbon([(39, 53, .2), (47, 47, .7), (57, 43, .2)], 1.8, "aloe-low-right", "#77746a", .34),
])

# Basil: a branching stalk with broad paired leaves and a small flowering tip.
write("basil", [
    ribbon([(36, 57, .2), (35, 45, .7), (36, 33, 1.0), (35, 21, .2)], 1.8, "basil-stem", "#4a4943", .32),
    ribbon([(35, 39, .2), (28, 36, .7), (21, 31, .2)], 1.35, "basil-leaf-left-low"),
    ribbon([(36, 35, .2), (43, 32, .7), (50, 27, .2)], 1.35, "basil-leaf-right-low"),
    ribbon([(35, 29, .2), (29, 26, .7), (24, 22, .2)], 1.15, "basil-leaf-left-high", "#4a4943"),
    ribbon([(36, 26, .2), (42, 23, .7), (47, 19, .2)], 1.15, "basil-leaf-right-high", "#4a4943"),
    '<ellipse class="ink-wash" cx="35" cy="17" rx="2.0" ry="2.2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="40" cy="17" rx="1.5" ry="1.7" fill="#77746a"/>',
])

# Lavender: a single slender stalk ending in a tapered cluster of blooms.
write("lavender", [
    ribbon([(35, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 18, .2)], 1.45, "lavender-stem", "#4a4943", .32),
    ribbon([(35, 47, .2), (29, 44, .7), (25, 40, .2)], .95, "lavender-leaf-left", "#77746a"),
    ribbon([(36, 42, .2), (42, 39, .7), (46, 35, .2)], .95, "lavender-leaf-right", "#77746a"),
    '<path class="ink-wash" fill="#262522" d="M 32 28 C 31 23 33 16 36 12 C 40 17 41 23 39 29 Z"/>',
    '<ellipse class="ink-wash" cx="34" cy="20" rx="1.7" ry="1.3" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="38" cy="23" rx="1.7" ry="1.3" fill="#77746a"/>',
])

# Mint: a low, spreading stem with paired rounded leaves.
write("mint", [
    ribbon([(36, 58, .2), (35, 47, .7), (36, 36, 1.0), (35, 25, .2)], 1.8, "mint-stem", "#4a4943", .35),
    ribbon([(35, 44, .2), (27, 42, .7), (19, 37, .2)], 1.35, "mint-leaf-left-low"),
    ribbon([(36, 39, .2), (44, 36, .7), (52, 31, .2)], 1.35, "mint-leaf-right-low"),
    ribbon([(35, 32, .2), (29, 29, .7), (24, 25, .2)], 1.15, "mint-leaf-left-high", "#4a4943"),
    ribbon([(36, 28, .2), (42, 24, .7), (47, 20, .2)], 1.15, "mint-leaf-right-high", "#4a4943"),
    ribbon([(21, 37, .2), (25, 35, .7), (28, 35, .2)], .75, "mint-vein-left", "#77746a"),
    ribbon([(50, 31, .2), (46, 30, .7), (43, 30, .2)], .75, "mint-vein-right", "#77746a"),
])

# Sage: two broad, slightly bowed leaves on a short woody stem.
write("sage", [
    ribbon([(36, 57, .2), (35, 46, .7), (36, 35, 1.0), (36, 25, .2)], 1.9, "sage-stem", "#4a4943", .34),
    '<path class="ink-wash" fill="#4a4943" d="M 35 39 C 28 31 19 31 14 36 C 20 43 28 45 35 42 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 37 35 C 43 27 52 26 58 31 C 54 38 45 40 37 38 Z"/>',
    ribbon([(17, 37, .2), (24, 38, .7), (32, 40, .2)], .8, "sage-leaf-vein-left", "#262522"),
    ribbon([(40, 35, .2), (47, 33, .7), (55, 32, .2)], .8, "sage-leaf-vein-right", "#262522"),
])

# Calendula: a single open daisy-like flower with a dark center and long stem.
write("calendula", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 23, .2)], 1.65, "calendula-stem", "#4a4943", .32),
    '<path class="ink-wash" fill="#4a4943" d="M 36 22 C 29 22 25 18 28 15 C 30 12 34 15 36 18 C 38 13 42 12 44 15 C 46 18 41 21 36 22 Z"/>',
    '<ellipse class="ink-wash" cx="36" cy="18" rx="2.6" ry="2.4" fill="#262522"/>',
    ribbon([(35, 43, .2), (28, 39, .7), (23, 36, .2)], 1.0, "calendula-leaf-left", "#77746a"),
    ribbon([(36, 38, .2), (43, 35, .7), (48, 31, .2)], 1.0, "calendula-leaf-right", "#77746a"),
])

# Chamomile: two small white-petal flowers on wiry branching stems.
write("chamomile", [
    ribbon([(34, 58, .2), (34, 45, .7), (31, 33, 1.0), (29, 23, .2)], 1.35, "chamomile-stem-left", "#4a4943", .34),
    ribbon([(35, 46, .2), (43, 36, .7), (47, 26, .2)], 1.2, "chamomile-stem-right", "#4a4943", .34),
    '<path class="ink-wash" fill="#77746a" d="M 29 23 C 24 21 23 18 26 17 C 29 17 30 19 29 23 C 29 18 32 16 34 18 C 35 20 32 22 29 23 Z"/>',
    '<ellipse class="ink-wash" cx="29" cy="20" rx="1.8" ry="1.8" fill="#262522"/>',
    '<path class="ink-wash" fill="#77746a" d="M 47 26 C 42 24 42 21 45 20 C 48 20 49 22 47 26 C 48 21 51 20 52 22 C 53 24 50 26 47 26 Z"/>',
    '<ellipse class="ink-wash" cx="47" cy="23" rx="1.7" ry="1.7" fill="#262522"/>',
])

# Echinacea: a drooping cone surrounded by narrow petals.
write("echinacea", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 23, .2)], 1.6, "echinacea-stem", "#4a4943", .33),
    '<path class="ink-wash" fill="#4a4943" d="M 36 20 C 30 18 26 15 27 13 C 31 14 34 16 36 18 C 38 13 42 11 44 12 C 43 16 40 19 36 20 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 30 22 C 25 20 22 18 21 16 C 25 16 29 18 32 21 M 42 21 C 46 17 50 16 52 17 C 49 20 45 22 42 22 M 32 25 C 28 25 24 24 22 22 C 26 21 30 22 33 24 M 40 24 C 44 22 48 22 51 24 C 48 26 44 26 40 25 Z"/>',
    '<ellipse class="ink-wash" cx="36" cy="21" rx="3.0" ry="3.4" fill="#262522"/>',
])

# Rosemary: a woody upright sprig with many narrow needle leaves.
write("rosemary", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 19, .2)], 1.85, "rosemary-stem", "#4a4943", .34),
    ribbon([(35, 43, .2), (29, 39, .7), (24, 34, .2)], 1.0, "rosemary-left-low", "#262522"),
    ribbon([(36, 39, .2), (43, 35, .7), (48, 30, .2)], 1.0, "rosemary-right-low", "#262522"),
    ribbon([(35, 32, .2), (29, 28, .7), (25, 24, .2)], .95, "rosemary-left-high", "#262522"),
    ribbon([(36, 28, .2), (42, 24, .7), (46, 20, .2)], .95, "rosemary-right-high", "#262522"),
    ribbon([(35, 48, .2), (29, 46, .7), (25, 43, .2)], .8, "rosemary-needle-left", "#77746a"),
    ribbon([(37, 47, .2), (43, 44, .7), (48, 41, .2)], .8, "rosemary-needle-right", "#77746a"),
])

# Yarrow: a feathery stem topped with a broad, loose flower head.
write("yarrow", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 22, .2)], 1.45, "yarrow-stem", "#4a4943", .34),
    ribbon([(35, 44, .2), (28, 41, .7), (23, 38, .2)], .95, "yarrow-leaf-left", "#262522"),
    ribbon([(36, 38, .2), (43, 35, .7), (49, 31, .2)], .95, "yarrow-leaf-right", "#262522"),
    '<path class="ink-wash" fill="#4a4943" d="M 28 22 C 28 18 31 15 36 14 C 41 15 44 18 44 22 C 40 25 32 25 28 22 Z"/>',
    '<ellipse class="ink-wash" cx="31" cy="20" rx="1.4" ry="1.2" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="36" cy="18" rx="1.4" ry="1.2" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="41" cy="20" rx="1.4" ry="1.2" fill="#77746a"/>',
])

print("redrew aloe, basil, lavender, mint, and sage as herb studies")
