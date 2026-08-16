#!/usr/bin/env python3
"""Author recognizable flora as sparse botanical sumi-e studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.32):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/flora" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 42 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="flora / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>flora / {name} — botanical sumi-e study</title>{''.join(marks)}</svg>
''')


# Berry bush: an open branching shrub with clustered berries.
write("berrybush", [
    ribbon([(36, 57, .2), (34, 46, .7), (35, 36, 1.0), (36, 25, .2)], 1.8, "berrybush-trunk", "#4a4943"),
    ribbon([(35, 43, .2), (27, 36, .7), (20, 29, .2)], 1.25, "berrybush-left", "#262522"),
    ribbon([(35, 39, .2), (44, 32, .7), (51, 24, .2)], 1.25, "berrybush-right", "#262522"),
    ribbon([(35, 48, .2), (26, 45, .7), (19, 40, .2)], 1.1, "berrybush-low-left", "#77746a"),
    '<ellipse class="ink-wash" cx="19" cy="28" rx="2.2" ry="2.0" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="24" cy="31" rx="2.2" ry="2.0" fill="#4a4943"/>',
    '<ellipse class="ink-wash" cx="51" cy="24" rx="2.2" ry="2.0" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="47" cy="28" rx="2.2" ry="2.0" fill="#4a4943"/>',
    ribbon([(27, 37, .2), (31, 34, .7), (35, 35, .2)], .8, "berrybush-leaf-left", "#77746a"),
])

# Fern: a single arcing frond with paired leaflets along the rachis.
write("fern", [
    ribbon([(24, 58, .2), (29, 47, .7), (36, 35, 1.0), (45, 21, .2)], 1.55, "fern-rachis", "#4a4943", .36),
    ribbon([(31, 45, .2), (25, 42, .7), (21, 38, .2)], 1.0, "fern-leaf-left-one", "#262522"),
    ribbon([(34, 40, .2), (28, 37, .7), (24, 33, .2)], 1.0, "fern-leaf-left-two", "#262522"),
    ribbon([(37, 35, .2), (33, 31, .7), (30, 27, .2)], .95, "fern-leaf-left-three", "#77746a"),
    ribbon([(30, 46, .2), (37, 44, .7), (43, 40, .2)], 1.0, "fern-leaf-right-one", "#262522"),
    ribbon([(34, 39, .2), (41, 37, .7), (47, 32, .2)], 1.0, "fern-leaf-right-two", "#262522"),
    ribbon([(39, 32, .2), (45, 29, .7), (50, 24, .2)], .95, "fern-leaf-right-three", "#77746a"),
])

# Grass: a low fan of bent blades with varied sweep and negative space.
write("grass", [
    ribbon([(36, 58, .2), (33, 46, .7), (27, 34, .2)], 1.45, "grass-blade-left", "#4a4943", .36),
    ribbon([(37, 58, .2), (36, 45, .7), (37, 30, .2)], 1.7, "grass-blade-center", "#262522", .36),
    ribbon([(38, 58, .2), (43, 45, .7), (51, 35, .2)], 1.45, "grass-blade-right", "#4a4943", .36),
    ribbon([(35, 57, .2), (27, 50, .7), (20, 47, .2)], 1.15, "grass-blade-low-left", "#77746a", .36),
    ribbon([(39, 57, .2), (48, 51, .7), (57, 48, .2)], 1.15, "grass-blade-low-right", "#77746a", .36),
])

# Maple: a single characteristic palmate leaf on a stem.
write("maple", [
    ribbon([(36, 58, .2), (36, 46, .7), (36, 34, .2)], 1.55, "maple-stem", "#4a4943"),
    '<path class="ink-wash" fill="#4a4943" d="M 36 35 L 31 27 L 27 31 L 24 24 L 32 26 L 31 18 L 36 25 L 41 18 L 40 26 L 48 24 L 45 31 L 41 27 Z"/>',
    ribbon([(36, 35, .2), (36, 27, .7), (36, 20, .2)], .8, "maple-vein", "#77746a"),
    ribbon([(35, 34, .2), (30, 29, .7), (26, 26, .2)], .75, "maple-vein-left", "#77746a"),
    ribbon([(37, 34, .2), (42, 29, .7), (46, 26, .2)], .75, "maple-vein-right", "#77746a"),
])

# Palm: a leaning trunk and long feathered fronds.
write("palm", [
    ribbon([(35, 58, .2), (33, 47, .7), (35, 35, 1.0), (39, 25, .2)], 2.0, "palm-trunk", "#4a4943", .35),
    ribbon([(39, 25, .2), (30, 18, .7), (22, 16, .2)], 1.35, "palm-frond-left", "#262522", .36),
    ribbon([(39, 25, .2), (39, 15, .7), (38, 10, .2)], 1.35, "palm-frond-center", "#262522", .36),
    ribbon([(39, 25, .2), (48, 18, .7), (56, 16, .2)], 1.35, "palm-frond-right", "#262522", .36),
    ribbon([(35, 26, .2), (29, 22, .7), (24, 21, .2)], .8, "palm-leaf-left", "#77746a"),
    ribbon([(43, 24, .2), (49, 21, .7), (54, 21, .2)], .8, "palm-leaf-right", "#77746a"),
])

# Willow: a rounded crown with many long, falling branch strokes.
write("willow", [
    '<path class="ink-wash" fill="#4a4943" d="M 16 30 C 18 21 27 18 34 21 C 40 16 50 19 53 26 C 59 25 63 30 60 36 C 55 41 22 42 16 36 Z"/>',
    ribbon([(36, 38, .2), (35, 48, .7), (36, 58, .2)], 2.4, "willow-trunk", "#262522", .34),
    ribbon([(25, 36, .2), (23, 47, .7), (22, 57, .2)], 1.15, "willow-hang-left", "#77746a", .36),
    ribbon([(31, 38, .2), (30, 49, .7), (29, 59, .2)], 1.15, "willow-hang-mid-left", "#262522", .36),
    ribbon([(42, 38, .2), (44, 49, .7), (46, 59, .2)], 1.15, "willow-hang-mid-right", "#77746a", .36),
    ribbon([(49, 37, .2), (52, 47, .7), (54, 56, .2)], 1.15, "willow-hang-right", "#262522", .36),
])

# Birch: a light, crooked trunk with sparse branching and bark marks.
write("birch", [
    ribbon([(35, 58, .2), (34, 46, .7), (36, 34, 1.0), (34, 20, .2)], 2.25, "birch-trunk", "#4a4943", .36),
    ribbon([(35, 35, .2), (27, 28, .7), (22, 21, .2)], 1.2, "birch-branch-left", "#262522"),
    ribbon([(35, 30, .2), (43, 25, .7), (49, 18, .2)], 1.2, "birch-branch-right", "#262522"),
    ribbon([(35, 43, .2), (28, 39, .7), (22, 34, .2)], 1.0, "birch-low-left", "#77746a"),
    ribbon([(33, 27, .2), (36, 25, .7), (39, 26, .2)], .75, "birch-bark-mark-one", "#77746a"),
    ribbon([(33, 36, .2), (36, 34, .7), (39, 35, .2)], .75, "birch-bark-mark-two", "#77746a"),
])

# Bush: a low, rounded shrub made from several overlapping masses and twigs.
write("bush", [
    '<path class="ink-wash" fill="#4a4943" d="M 13 45 C 14 37 20 33 27 35 C 29 29 38 28 42 34 C 49 30 58 34 59 42 C 62 46 56 52 50 52 C 41 55 22 54 14 50 Z"/>',
    ribbon([(28, 50, .2), (28, 43, .7), (25, 37, .2)], 1.15, "bush-twig-left", "#262522"),
    ribbon([(38, 51, .2), (39, 43, .7), (43, 35, .2)], 1.15, "bush-twig-right", "#262522"),
    ribbon([(45, 49, .2), (50, 44, .7), (55, 40, .2)], .9, "bush-twig-far", "#77746a"),
])

# Pine: a narrow conifer with an uneven central leader and tiered boughs.
write("pine", [
    ribbon([(36, 58, .2), (36, 45, .7), (35, 33, 1.0), (36, 18, .2)], 1.8, "flora-pine-trunk", "#4a4943", .34),
    ribbon([(35, 28, .2), (28, 31, .7), (23, 35, .2)], 1.25, "flora-pine-left-one"),
    ribbon([(36, 34, .2), (44, 37, .7), (50, 41, .2)], 1.25, "flora-pine-right-one"),
    ribbon([(35, 40, .2), (27, 44, .7), (20, 48, .2)], 1.45, "flora-pine-left-two"),
    ribbon([(36, 45, .2), (45, 49, .7), (54, 53, .2)], 1.45, "flora-pine-right-two"),
    ribbon([(35, 25, .2), (31, 21, .7), (30, 17, .2)], .85, "flora-pine-needle-left", "#77746a"),
    ribbon([(37, 26, .2), (41, 22, .7), (42, 18, .2)], .85, "flora-pine-needle-right", "#77746a"),
])

# Poplar: a tall, narrow crown on a straight trunk with a few vertical tufts.
write("poplar", [
    ribbon([(36, 58, .2), (36, 46, .7), (36, 34, 1.0), (36, 18, .2)], 2.0, "poplar-trunk", "#4a4943", .32),
    '<path class="ink-wash" fill="#4a4943" d="M 30 39 C 29 30 30 21 36 14 C 42 21 43 30 42 39 C 39 43 33 43 30 39 Z"/>',
    ribbon([(32, 31, .2), (28, 27, .7), (26, 23, .2)], .75, "poplar-side-left", "#77746a"),
    ribbon([(40, 31, .2), (44, 27, .7), (46, 22, .2)], .75, "poplar-side-right", "#77746a"),
])

# Reed: three hollow stalks with separate brushy seed heads.
write("reed", [
    ribbon([(27, 58, .2), (28, 45, .7), (27, 27, .2)], 1.25, "reed-left", "#4a4943", .34),
    ribbon([(36, 58, .2), (36, 44, .7), (37, 24, .2)], 1.35, "reed-center", "#262522", .34),
    ribbon([(45, 58, .2), (44, 45, .7), (46, 29, .2)], 1.25, "reed-right", "#4a4943", .34),
    '<path class="ink-wash" fill="#4a4943" d="M 24 27 C 24 22 28 20 31 22 L 30 28 Z M 34 24 C 34 19 38 17 40 20 L 39 25 Z M 43 29 C 43 24 47 22 49 25 L 48 30 Z"/>',
])

# Snag: a dead trunk with broken limbs and a few rough bark scars.
write("snag", [
    ribbon([(36, 58, .2), (35, 47, .7), (36, 34, 1.0), (34, 19, .2)], 2.7, "snag-trunk", "#4a4943", .38),
    ribbon([(35, 35, .2), (27, 28, .7), (21, 20, .2)], 1.7, "snag-left-limb", "#262522", .38),
    ribbon([(36, 31, .2), (44, 25, .7), (51, 19, .2)], 1.6, "snag-right-limb", "#262522", .38),
    ribbon([(34, 43, .2), (29, 40, .7), (25, 37, .2)], .9, "snag-bark-one", "#77746a"),
    ribbon([(38, 48, .2), (43, 45, .7), (47, 43, .2)], .9, "snag-bark-two", "#77746a"),
])

# Spruce: a fuller, drooping conifer with layered boughs.
write("spruce", [
    ribbon([(36, 58, .2), (36, 45, .7), (35, 31, 1.0), (36, 17, .2)], 1.8, "spruce-trunk", "#4a4943", .34),
    ribbon([(35, 26, .2), (30, 29, .7), (24, 33, .2)], 1.4, "spruce-left-high"),
    ribbon([(36, 31, .2), (43, 34, .7), (49, 38, .2)], 1.4, "spruce-right-high"),
    ribbon([(35, 38, .2), (27, 42, .7), (19, 46, .2)], 1.65, "spruce-left-low"),
    ribbon([(36, 44, .2), (45, 49, .7), (54, 53, .2)], 1.65, "spruce-right-low"),
    ribbon([(29, 29, .2), (26, 26, .7), (24, 24, .2)], .8, "spruce-needles-left", "#77746a"),
    ribbon([(44, 34, .2), (47, 31, .7), (50, 30, .2)], .8, "spruce-needles-right", "#77746a"),
])

# Stump: a low cut trunk with an elliptical top, bark sides, and rings.
write("stump", [
    '<path class="ink-wash" fill="#4a4943" d="M 22 28 C 28 24 44 24 51 28 L 50 52 C 44 56 29 56 22 52 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 22 28 C 28 23 45 23 51 28 C 46 33 28 33 22 28 Z"/>',
    ribbon([(28, 27, .2), (34, 26, .7), (40, 28, .2)], .8, "stump-ring-one", "#262522"),
    ribbon([(31, 29, .2), (36, 28, .7), (42, 29, .2)], .7, "stump-ring-two", "#262522"),
    ribbon([(25, 36, .2), (31, 38, .7), (39, 37, .2)], .8, "stump-bark-one", "#77746a"),
])

print("redrew berrybush, fern, grass, maple, palm, and willow as flora studies")
