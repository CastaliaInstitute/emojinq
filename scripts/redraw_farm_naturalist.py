#!/usr/bin/env python3
"""Author readable farm subjects as sparse sumi-e brush studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.3):
    role = "ink-dry" if color == "#77746a" else "ink-wash"
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color, class_name=role)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/farm" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="farm / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>farm / {name} — naturalist sumi-e study</title>{''.join(marks)}</svg>
''')


# Bee: a rounded abdomen, clear wings, antennae, and two brush stripes.
write("bee", [
    ribbon([(27, 35, .15), (31, 29, .72), (40, 28, 1.0), (48, 34, .72), (45, 41, .55), (35, 42, .72), (27, 35, .15)], 1.65, "bee-abdomen", "#4a4943", .34),
    '<ellipse class="ink-wash" cx="26" cy="35" rx="3.7" ry="3.8" fill="#262522"/>',
    '<path class="ink-wash" fill="#77746a" d="M 33 30 C 27 22 21 22 20 27 C 22 31 28 33 34 33 Z M 40 30 C 46 22 53 22 54 27 C 52 31 46 33 40 33 Z"/>',
    ribbon([(34, 30, .2), (35, 35, .7), (34, 40, .2)], 1.05, "bee-stripe-one", "#262522"),
    ribbon([(40, 30, .2), (41, 35, .7), (40, 40, .2)], 1.05, "bee-stripe-two", "#262522"),
    ribbon([(25, 32, .2), (21, 28, .7), (19, 25, .2)], .8, "bee-antenna-left", "#77746a"),
    ribbon([(27, 32, .2), (24, 27, .7), (24, 24, .2)], .8, "bee-antenna-right", "#77746a"),
])

# Carrot: a tapered root with leafy crown and a few soil marks.
write("carrot", [
    ribbon([(31, 28, .95), (35, 36, 1.0), (37, 45, .62), (36, 56, .08)], 7.2, "carrot-root", "#4a4943", .3),
    ribbon([(30, 29, .15), (36, 27, .8), (43, 29, .15)], .9, "carrot-shoulder", "#262522", .32),
    ribbon([(36, 29, .2), (32, 22, .7), (29, 15, .2)], 1.6, "carrot-leaf-left", "#262522", .34),
    ribbon([(37, 28, .2), (37, 20, .7), (38, 12, .2)], 1.7, "carrot-leaf-center", "#4a4943", .34),
    ribbon([(39, 29, .2), (44, 22, .7), (49, 17, .2)], 1.5, "carrot-leaf-right", "#77746a", .34),
    ribbon([(31, 57, .2), (38, 58, .7), (45, 57, .2)], .95, "carrot-soil", "#77746a"),
])

# Chicken: a compact body, lifted head, beak, comb, and two grounded legs.
write("chicken", [
    ribbon([(20, 38, .15), (24, 30, .72), (34, 28, 1.0), (43, 31, .8), (53, 36, .55), (49, 44, .72), (38, 48, 1.0), (27, 46, .65), (20, 38, .15)], 1.8, "chicken-body", "#4a4943", .36),
    '<ellipse class="ink-wash" cx="43" cy="25" rx="6.0" ry="5.5" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#262522" d="M 40 20 C 41 15 44 14 46 19 C 49 15 52 17 50 21 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 49 25 L 58 28 L 49 30 Z"/>',
    ribbon([(31, 36, .2), (36, 39, .7), (41, 36, .2)], 1.0, "chicken-wing", "#77746a"),
    ribbon([(31, 45, .2), (30, 53, .7), (27, 57, .2)], 1.2, "chicken-leg-left"),
    ribbon([(44, 45, .2), (45, 53, .7), (49, 57, .2)], 1.2, "chicken-leg-right"),
])

# Corn: an ear with overlapping husk leaves and a few visible kernels.
write("corn", [
    ribbon([(30, 19, .15), (37, 16, .75), (44, 20, 1.0), (47, 30, .72), (44, 47, .62), (37, 54, .8), (29, 48, .55), (27, 31, .72), (30, 19, .15)], 1.8, "corn-ear", "#4a4943", .34),
    '<path class="ink-wash" fill="#77746a" d="M30 51 C23 47 18 39 20 28 C26 33 31 40 34 50 Z"/>',
    '<path class="ink-dry" fill="#bcb9af" d="M41 51 C49 46 54 39 53 28 C47 34 43 41 38 50 Z"/>',
    '<ellipse class="ink-wash" cx="35" cy="27" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="41" cy="28" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="34" cy="34" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="41" cy="36" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="36" cy="42" rx="1.5" ry="1.3" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="40" cy="45" rx="1.4" ry="1.2" fill="#4a4943"/>',
    '<ellipse class="ink-wash" cx="35" cy="20" rx="1.3" ry="1.1" fill="#4a4943"/>',
])

# Cow: a low, heavy body with horns, muzzle, udder, and four short legs.
write("cow", [
    ribbon([(18, 34, .15), (24, 27, .72), (35, 25, 1.0), (48, 28, .78), (57, 34, .55), (55, 42, .72), (44, 47, 1.0), (30, 46, .72), (19, 41, .15)], 2.0, "cow-body", "#4a4943", .36),
    ribbon([(20, 31, .15), (15, 29, .72), (10, 33, 1.0), (12, 40, .62), (19, 39, .15)], 1.7, "cow-head", "#3c3b36", .34),
    ribbon([(14, 31, .2), (11, 27, .7), (8, 28, .2)], 1.1, "cow-horn-left", "#262522"),
    ribbon([(18, 31, .2), (20, 27, .7), (23, 28, .2)], 1.1, "cow-horn-right", "#262522"),
    ribbon([(27, 43, .2), (26, 53, .7), (24, 57, .2)], 1.45, "cow-leg-one"),
    ribbon([(36, 44, .2), (36, 53, .7), (34, 57, .2)], 1.45, "cow-leg-two"),
    ribbon([(46, 43, .2), (48, 53, .7), (50, 57, .2)], 1.45, "cow-leg-three"),
    ribbon([(52, 41, .2), (55, 50, .7), (57, 55, .2)], 1.45, "cow-leg-four"),
    '<ellipse class="ink-wash" cx="17" cy="37" rx="2.0" ry="1.5" fill="#77746a"/>',
])

# Egg: an asymmetrical shell with a soft grounded shadow and a tiny wash seam.
write("egg", [
    ribbon([(36, 15, .15), (29, 18, .65), (25, 28, 1.0), (24, 40, .78), (29, 51, .65), (36, 55, .15)], 2.0, "egg-left", "#262522", .34),
    ribbon([(36, 55, .15), (44, 51, .65), (49, 41, 1.0), (48, 28, .72), (42, 18, .55), (36, 15, .15)], 1.35, "egg-right", "#77746a", .34),
    ribbon([(33, 28, .2), (36, 31, .7), (39, 29, .2)], .8, "egg-wash-seam", "#77746a"),
    ribbon([(26, 57, .2), (35, 58, .7), (46, 57, .2)], 1.0, "egg-ground", "#77746a"),
])

# Flour: a tied cloth sack with a soft, weighted base.
write("flour", [
    ribbon([(28, 27, .15), (32, 22, .72), (40, 22, 1.0), (45, 27, .15)], 1.9, "flour-neck", "#262522", .34),
    ribbon([(28, 27, .15), (23, 37, .72), (20, 49, .15)], 1.45, "flour-left", "#4a4943", .34),
    ribbon([(45, 27, .15), (50, 38, .72), (53, 49, .15)], 1.25, "flour-right", "#77746a", .34),
    ribbon([(20, 49, .15), (30, 55, .72), (43, 55, 1.0), (53, 49, .15)], 1.55, "flour-base", "#4a4943", .36),
    ribbon([(27, 27, .2), (35, 29, .7), (46, 27, .2)], 1.45, "flour-tie", "#262522", .34),
    ribbon([(36, 47, .2), (36, 39, .7), (36, 33, .2)], 1.0, "flour-wheat-stem", "#4a4943"),
    ribbon([(36, 38, .2), (31, 35, .7), (28, 35, .2)], 1.0, "flour-grain-left-a", "#77746a"),
    ribbon([(36, 42, .2), (41, 38, .7), (44, 37, .2)], .9, "flour-grain-right-a", "#77746a"),
    ribbon([(36, 46, .2), (31, 43, .7), (28, 43, .2)], .8, "flour-grain-left-b", "#bcb9af"),
])

# Greenhouse: an arched glass frame enclosing a small crop bed.
write("greenhouse", [
    ribbon([(13, 52, .2), (14, 31, .7), (21, 20, 1.0), (35, 14, .7), (50, 20, .2), (59, 31, .7), (59, 52, .2)], 1.7, "greenhouse-frame", "#4a4943", .32),
    ribbon([(35, 15, .2), (35, 52, .7)], 1.1, "greenhouse-ridge", "#77746a"),
    ribbon([(14, 34, .2), (35, 32, .7), (59, 34, .2)], .9, "greenhouse-crossbeam", "#77746a"),
    ribbon([(27, 52, .2), (27, 39, .7), (44, 39, .2), (44, 52, .2)], 1.1, "greenhouse-door", "#262522"),
    ribbon([(23, 52, .2), (23, 27, .7)], .75, "greenhouse-pane-left", "#bcb9af"),
    ribbon([(48, 52, .2), (48, 27, .7)], .75, "greenhouse-pane-right", "#bcb9af"),
    ribbon([(18, 53, .2), (35, 51, .7), (55, 53, .2)], 1.0, "greenhouse-bed", "#4a4943"),
    ribbon([(21, 51, .2), (24, 43, .7), (28, 50, .2)], 1.35, "greenhouse-plant-left", "#262522"),
    ribbon([(43, 51, .2), (47, 41, .7), (52, 50, .2)], 1.35, "greenhouse-plant-right", "#262522"),
])

# Honey: a squat jar with a lid, warm dark wash, and one slow drip.
write("honey", [
    ribbon([(24, 29, .15), (34, 26, .72), (48, 29, .15)], 1.8, "honey-rim", "#262522", .34),
    ribbon([(24, 30, .15), (23, 40, .72), (25, 49, .15)], 1.35, "honey-left", "#4a4943", .34),
    ribbon([(48, 30, .15), (51, 40, .72), (49, 49, .15)], 1.25, "honey-right", "#77746a", .34),
    ribbon([(25, 49, .15), (36, 54, .8), (49, 49, .15)], 1.4, "honey-base", "#4a4943", .34),
    ribbon([(27, 27, .2), (35, 25, .7), (46, 27, .2)], 1.6, "honey-lid", "#262522", .3),
    ribbon([(29, 35, .2), (37, 37, .7), (45, 35, .2)], .9, "honey-glass-mark", "#77746a"),
    ribbon([(47, 27, .2), (51, 23, .7), (53, 19, .2)], 1.1, "honey-drip", "#77746a", .33),
    '<ellipse class="ink-wash" cx="35" cy="21" rx="2.4" ry="1.7" fill="#262522"/>',
])

# Meat: an irregular cut with a bone end and a few grain marks.
write("meat", [
    ribbon([(20, 28, .15), (29, 23, .72), (41, 25, 1.0), (50, 31, .72), (53, 41, .6), (47, 49, .72), (35, 52, 1.0), (23, 47, .72), (18, 38, .5), (20, 28, .15)], 1.9, "meat-cut", "#4a4943", .38),
    ribbon([(46, 28, .15), (53, 24, .72), (59, 28, 1.0), (54, 33, .15)], 1.25, "meat-bone", "#77746a", .34),
    ribbon([(28, 31, .2), (34, 35, .7), (42, 33, .2)], .9, "meat-grain-one", "#262522"),
    ribbon([(26, 40, .2), (34, 43, .7), (43, 41, .2)], .8, "meat-grain-two", "#77746a"),
])

# Milk: a handled pitcher with a wide lip and a quiet highlight.
write("milk", [
    ribbon([(26, 25, .15), (35, 22, .75), (47, 25, .15)], 1.8, "milk-rim", "#262522", .34),
    ribbon([(26, 26, .15), (24, 38, .72), (25, 50, .15)], 1.4, "milk-left", "#4a4943", .34),
    ribbon([(47, 26, .15), (49, 38, .72), (48, 50, .15)], 1.2, "milk-right", "#77746a", .34),
    ribbon([(25, 50, .15), (36, 55, .8), (48, 50, .15)], 1.4, "milk-base", "#4a4943", .34),
    ribbon([(27, 25, .2), (36, 23, .7), (46, 25, .2)], 1.6, "milk-lip", "#262522", .3),
    ribbon([(46, 30, .2), (55, 28, .7), (58, 34, .2)], 1.5, "milk-handle", "#262522", .32),
    ribbon([(31, 33, .2), (35, 35, .7), (39, 34, .2)], .8, "milk-highlight", "#77746a"),
])

# Pig: a low rounded body, snout, ear, curly tail, and short legs.
write("pig", [
    ribbon([(18, 35, .15), (25, 28, .72), (37, 27, 1.0), (50, 30, .78), (57, 36, .55), (54, 43, .72), (43, 48, 1.0), (29, 47, .72), (19, 42, .15)], 2.0, "pig-body", "#4a4943", .36),
    ribbon([(20, 34, .15), (15, 32, .72), (10, 36, 1.0), (12, 42, .62), (19, 39, .15)], 1.7, "pig-head", "#3c3b36", .34),
    ribbon([(22, 31, .2), (19, 26, .7), (22, 24, .2)], 1.2, "pig-ear", "#262522"),
    ribbon([(54, 34, .2), (61, 30, .7), (62, 35, .2), (59, 38, .7), (62, 40, .2)], 1.1, "pig-tail", "#77746a", .36),
    ribbon([(28, 44, .2), (27, 53, .7), (25, 57, .2)], 1.35, "pig-leg-left"),
    ribbon([(45, 44, .2), (46, 53, .7), (48, 57, .2)], 1.35, "pig-leg-right"),
    '<ellipse class="ink-wash" cx="14" cy="38" rx="2.0" ry="1.4" fill="#77746a"/>',
])

# Strawberry: a heart-shaped berry with seeds, leafy calyx, and a ground mark.
write("strawberry", [
    ribbon([(36, 25, .15), (29, 21, .72), (22, 26, 1.0), (22, 36, .72), (28, 48, .62), (36, 56, .15)], 1.9, "strawberry-left", "#4a4943", .36),
    ribbon([(36, 56, .15), (45, 48, .72), (51, 36, 1.0), (50, 26, .65), (43, 21, .55), (36, 25, .15)], 1.35, "strawberry-right", "#77746a", .36),
    '<path class="ink-wash" fill="#77746a" d="M 36 27 C 31 22 26 22 23 25 C 28 26 31 29 36 31 C 41 27 45 25 49 25 C 45 22 40 22 36 27 Z"/>',
    '<ellipse class="ink-wash" cx="29" cy="34" rx="1.1" ry="1.7" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="37" cy="38" rx="1.1" ry="1.7" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="44" cy="33" rx="1.1" ry="1.7" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="33" cy="46" rx="1.1" ry="1.7" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="41" cy="47" rx="1.1" ry="1.7" fill="#262522"/>',
])

# Tomato: a round fruit with a star-shaped calyx and a slight shoulder.
write("tomato", [
    ribbon([(36, 24, .15), (27, 21, .72), (20, 29, 1.0), (19, 40, .75), (26, 51, .62), (36, 55, .15)], 2.0, "tomato-left", "#4a4943", .36),
    ribbon([(36, 55, .15), (46, 51, .72), (53, 41, 1.0), (52, 30, .72), (45, 22, .55), (36, 24, .15)], 1.4, "tomato-right", "#77746a", .36),
    '<path class="ink-wash" fill="#77746a" d="M 36 26 L 32 20 L 36 22 L 40 18 L 40 24 L 46 22 L 42 28 Z"/>',
    ribbon([(26, 35, .2), (30, 33, .7), (34, 34, .2)], .8, "tomato-highlight", "#77746a"),
])

# Wheat: a long stalk with alternating grains and a loose awn at the top.
write("wheat", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 17, .2)], 1.45, "wheat-stem", "#4a4943", .34),
    ribbon([(36, 28, .2), (30, 25, .7), (26, 21, .2)], 1.0, "wheat-grain-left-one", "#262522"),
    ribbon([(36, 34, .2), (43, 31, .7), (47, 27, .2)], 1.0, "wheat-grain-right-one", "#262522"),
    ribbon([(36, 40, .2), (29, 37, .7), (25, 33, .2)], 1.0, "wheat-grain-left-two", "#77746a"),
    ribbon([(35, 46, .2), (42, 43, .7), (47, 39, .2)], 1.0, "wheat-grain-right-two", "#77746a"),
    ribbon([(36, 19, .2), (32, 14, .7), (31, 10, .2)], .85, "wheat-awn-left", "#77746a"),
    ribbon([(36, 19, .2), (40, 14, .7), (42, 10, .2)], .85, "wheat-awn-right", "#77746a"),
])

print("redrew all 15 farm glyphs as authored sumi-e studies")
