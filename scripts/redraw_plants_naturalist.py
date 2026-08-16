#!/usr/bin/env python3
"""Author a compact set of readable botanical sumi-e studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.3):
    role = "ink-dry" if color == "#77746a" else "ink-wash"
    color = {"#bcb9af": "#716e67", "#77746a": "#5d5a54"}.get(color.lower(), color)
    width = max(width * 1.30, 1.20)
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color, class_name=role)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/plants" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="plants / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>plants / {name} — botanical sumi-e study</title>{''.join(marks)}</svg>
''')


# Pine: an asymmetrical conifer with a tapered trunk and irregular branch tiers.
write("pine", [
    ribbon([(36, 18, .14), (30, 24, .92), (23, 30, .08)], 5.2, "pine-loaded-top-left", "#4a4943", .38),
    ribbon([(36, 19, .14), (42, 24, .92), (49, 31, .08)], 4.7, "pine-loaded-top-right", "#5d5a54", .38),
    ribbon([(36, 32, .14), (28, 38, .96), (18, 45, .08)], 6.0, "pine-loaded-mid-left", "#5d5a54", .40),
    ribbon([(36, 33, .14), (45, 39, .96), (55, 46, .08)], 5.4, "pine-loaded-mid-right", "#4a4943", .40),
    ribbon([(36, 57, .2), (36, 46, .7), (35, 34, 1.0), (36, 22, .2)], 2.0, "pine-trunk", "#4a4943", .32),
    ribbon([(36, 27, .2), (29, 29, .7), (24, 33, .2)], 1.45, "pine-branch-left-one"),
    ribbon([(36, 32, .2), (43, 34, .7), (49, 38, .2)], 1.5, "pine-branch-right-one"),
    ribbon([(35, 38, .2), (28, 40, .7), (21, 44, .2)], 1.65, "pine-branch-left-two"),
    ribbon([(36, 43, .2), (45, 45, .7), (53, 49, .2)], 1.65, "pine-branch-right-two"),
    ribbon([(35, 48, .2), (28, 51, .7), (22, 53, .2)], 1.75, "pine-branch-left-three"),
    ribbon([(36, 52, .2), (45, 54, .7), (55, 56, .2)], 1.75, "pine-branch-right-three"),
    ribbon([(27, 29, .2), (25, 26, .7), (24, 24, .2)], .75, "pine-needles-upper-left", "#77746a"),
    ribbon([(43, 34, .2), (45, 31, .7), (47, 30, .2)], .75, "pine-needles-upper-right", "#77746a"),
    ribbon([(25, 40, .2), (22, 37, .7), (20, 36, .2)], .8, "pine-needles-middle-left", "#77746a"),
    ribbon([(46, 45, .2), (50, 42, .7), (53, 41, .2)], .8, "pine-needles-middle-right", "#77746a"),
    ribbon([(25, 51, .2), (21, 49, .7), (18, 49, .2)], .85, "pine-needles-low-left", "#77746a"),
    ribbon([(47, 54, .2), (52, 52, .7), (56, 52, .2)], .85, "pine-needles-low-right", "#77746a"),
    ribbon([(35, 20, .2), (32, 17, .7), (31, 14, .2)], 1.0, "pine-crown-left", "#77746a"),
    ribbon([(37, 21, .2), (40, 17, .7), (41, 13, .2)], 1.0, "pine-crown-right", "#77746a"),
])

# Root: a short plant crown separating into visibly spreading roots.
write("root", [
    ribbon([(36, 16, .2), (35, 25, .7), (36, 35, 1.0), (35, 42, .2)], 2.3, "root-stem", "#4a4943", .32),
    ribbon([(35, 40, .2), (29, 47, .7), (21, 54, 1.0), (14, 57, .2)], 2.0, "root-left", "#262522", .34),
    ribbon([(36, 40, .2), (38, 48, .7), (39, 56, .2)], 2.0, "root-center", "#262522", .34),
    ribbon([(37, 40, .2), (45, 46, .7), (55, 53, 1.0), (61, 55, .2)], 2.0, "root-right", "#262522", .34),
    ribbon([(25, 50, .2), (21, 52, .7), (18, 52, .2)], .8, "root-fine-left", "#77746a"),
    ribbon([(47, 48, .2), (52, 49, .7), (56, 48, .2)], .8, "root-fine-right", "#77746a"),
])

# Seed: a single organic seed with a seam and a small ground shadow.
write("seed", [
    ribbon([(31, 49, .2), (25, 43, .7), (24, 34, 1.0), (28, 26, .7), (36, 21, .2), (43, 24, .5), (46, 31, .9), (44, 40, .7), (38, 47, .2)], 2.1, "seed-outline", "#3c3b36", .34),
    ribbon([(30, 45, .2), (34, 38, .7), (38, 31, 1.0), (41, 25, .2)], .95, "seed-seam", "#77746a", .34),
    ribbon([(22, 53, .2), (30, 55, .7), (41, 54, 1.0), (50, 55, .2)], 1.1, "seed-ground", "#77746a"),
])

# Stem: a curved stalk with leaves at different heights and directions.
write("stem", [
    ribbon([(35, 57, .2), (34, 46, .7), (36, 35, 1.0), (34, 23, .2)], 1.9, "stem-main", "#4a4943", .35),
    ribbon([(35, 42, .2), (27, 39, .7), (21, 35, .2)], 1.25, "stem-leaf-left", "#262522"),
    ribbon([(35, 36, .2), (43, 31, .7), (49, 26, .2)], 1.25, "stem-leaf-right", "#262522"),
    ribbon([(35, 48, .2), (43, 45, .7), (49, 43, .2)], 1.15, "stem-leaf-low", "#262522"),
    ribbon([(21, 35, .2), (25, 32, .7), (29, 33, .2)], .85, "stem-leaf-vein-left", "#77746a"),
    ribbon([(49, 26, .2), (45, 29, .7), (42, 30, .2)], .85, "stem-leaf-vein-right", "#77746a"),
])

# Watering: a small tilted can with a spout and separate falling drops.
write("watering", [
    '<path class="ink-wash" fill="#716e67" d="M 21 31 C 27 27 38 28 44 32 L 45 46 C 40 52 27 52 22 47 C 20 42 20 36 21 31 Z"/>',
    ribbon([(22, 31, .15), (32, 28, .75), (43, 32, .15)], 1.8, "watering-rim", "#4a4943", .34),
    ribbon([(22, 32, .15), (21, 40, .72), (24, 47, .15)], 1.35, "watering-left", "#77746a", .34),
    ribbon([(43, 32, .15), (45, 40, .72), (42, 48, .15)], 1.45, "watering-right", "#262522", .34),
    ribbon([(24, 47, .15), (33, 51, .78), (42, 48, .15)], 1.3, "watering-base", "#4a4943", .34),
    ribbon([(25, 31, .2), (26, 25, .7), (31, 22, 1.0), (36, 24, .2)], 1.5, "watering-handle", "#262522", .32),
    ribbon([(42, 36, .2), (49, 34, .7), (57, 29, 1.0)], 2.0, "watering-spout", "#262522", .34),
    ribbon([(57, 29, .2), (60, 28, .7), (62, 30, .2)], 1.1, "watering-spout-tip", "#77746a"),
    '<ellipse class="ink-wash" cx="53" cy="39" rx="1.7" ry="2.4" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="57" cy="45" rx="1.5" ry="2.1" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="61" cy="51" rx="1.3" ry="1.8" fill="#77746a"/>',
])

# Bloom: an open five-petal flower with a curved stem and two leaves.
write("bloom", [
    ribbon([(36, 58, .2), (35, 46, .7), (36, 34, 1.0), (36, 24, .2)], 1.7, "bloom-stem", "#4a4943", .34),
    '<path class="ink-wash" fill="#4a4943" d="M 36 24 C 29 24 25 20 27 16 C 29 13 34 16 36 20 C 37 14 42 13 44 16 C 46 20 41 23 36 24 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 36 24 C 31 28 26 27 25 24 C 25 21 30 20 36 22 C 41 19 46 21 46 24 C 45 28 40 28 36 24 Z"/>',
    '<ellipse class="ink-wash" cx="36" cy="23" rx="2.5" ry="2.3" fill="#262522"/>',
    ribbon([(35, 43, .2), (28, 40, .7), (22, 36, .2)], 1.15, "bloom-leaf-left", "#262522"),
    ribbon([(36, 38, .2), (43, 35, .7), (50, 31, .2)], 1.15, "bloom-leaf-right", "#262522"),
])

# Bud: a closed flower swelling at the end of a bent stem.
write("bud", [
    ribbon([(36, 58, .2), (35, 46, .7), (37, 35, 1.0), (39, 25, .2)], 1.7, "bud-stem", "#4a4943", .34),
    '<path class="ink-wash" fill="#4a4943" d="M 39 26 C 34 22 34 16 39 12 C 44 16 44 22 39 26 Z"/>',
    ribbon([(36, 43, .2), (29, 39, .7), (23, 35, .2)], 1.1, "bud-leaf-left", "#262522"),
    ribbon([(37, 37, .2), (44, 33, .7), (50, 28, .2)], 1.1, "bud-leaf-right", "#77746a"),
    ribbon([(39, 20, .2), (40, 17, .7), (39, 14, .2)], .75, "bud-seam", "#77746a"),
])

# Fruit: a weighted round fruit with a stem, leaf, and a subtle wash highlight.
write("fruit", [
    ribbon([(35, 22, .15), (27, 21, .65), (21, 29, 1.0), (20, 40, .82), (26, 51, .55), (36, 56, .15)], 2.6, "fruit-host-side", "#262522", .36),
    ribbon([(36, 56, .15), (46, 53, .65), (52, 44, 1.0), (52, 32, .72), (44, 23, .15)], 1.75, "fruit-guest-side", "#4a4943", .36),
    ribbon([(28, 51, .15), (36, 54, .78), (44, 52, .15)], .9, "fruit-base", "#77746a", .34),
    ribbon([(36, 23, .2), (37, 18, .7), (40, 14, .2)], 1.5, "fruit-stem", "#262522", .3),
    ribbon([(39, 17, .2), (45, 15, .7), (51, 17, .2)], 1.3, "fruit-leaf", "#77746a", .32),
    ribbon([(28, 30, .2), (25, 36, .7), (27, 42, .2)], .75, "fruit-highlight", "#77746a", .3),
])

# Moss: a low, damp cushion with short tufted fronds rather than parallel arcs.
write("moss", [
    '<path class="ink-wash" fill="#716e67" d="M 11 51 C 14 43 22 40 29 44 C 34 37 43 39 47 44 C 54 41 61 45 61 51 C 54 57 20 58 11 51 Z"/>',
    ribbon([(11, 51, .15), (20, 45, .72), (29, 49, 1.0), (37, 46, .72), (46, 49, 1.0), (60, 47, .15)], 2.9, "moss-cushion", "#4a4943", .42),
    ribbon([(15, 55, .15), (28, 52, .7), (40, 55, 1.0), (55, 52, .15)], 1.0, "moss-dry-edge", "#77746a", .4),
    ribbon([(19, 48, .2), (18, 41, .7), (20, 37, .2)], 1.25, "moss-tuft-one", "#262522", .34),
    ribbon([(26, 49, .2), (27, 41, .7), (30, 36, .2)], 1.25, "moss-tuft-two", "#262522", .34),
    ribbon([(43, 48, .2), (44, 40, .7), (47, 35, .2)], 1.25, "moss-tuft-three", "#262522", .34),
    ribbon([(51, 49, .2), (54, 43, .7), (57, 40, .2)], 1.25, "moss-tuft-four", "#77746a", .34),
])

# Stream: a winding water ribbon with an irregular bank and a few reflected
# brush marks, retaining the sense of flow without a closed cartoon shape.
write("stream", [
    ribbon([(11, 48, .2), (20, 43, .7), (30, 44, 1.0), (39, 49, .72), (50, 49, .35), (60, 44, .2)], 2.6, "stream-bank", "#4a4943", .36),
    ribbon([(12, 54, .2), (23, 51, .7), (34, 53, 1.0), (45, 55, .7), (57, 52, .2)], 1.65, "stream-water-one", "#77746a", .34),
    ribbon([(17, 38, .2), (25, 35, .7), (34, 37, .2)], 1.0, "stream-water-two", "#262522", .34),
    ribbon([(42, 41, .2), (50, 38, .7), (58, 39, .2)], .9, "stream-water-three", "#77746a", .34),
])

# Compost: an uneven heap with visible scraps and a small warm center.
write("compost", [
    ribbon([(12, 51, .15), (20, 43, .65), (31, 45, 1.0), (40, 40, .75), (51, 44, .9), (60, 50, .15)], 2.75, "compost-heap", "#4a4943", .4),
    ribbon([(15, 54, .15), (27, 51, .72), (40, 54, 1.0), (56, 51, .15)], 1.0, "compost-lower-edge", "#77746a", .4),
    ribbon([(21, 47, .2), (26, 44, .7), (32, 46, .2)], 1.0, "compost-scrap-one", "#77746a"),
    ribbon([(37, 45, .2), (42, 42, .7), (48, 45, .2)], 1.0, "compost-scrap-two", "#77746a"),
    ribbon([(27, 51, .2), (34, 49, .7), (41, 51, .2)], .9, "compost-layer", "#262522"),
    ribbon([(33, 42, .15), (36, 38, .8), (40, 42, .15)], .8, "compost-warm-center", "#77746a", .34),
])

# Dirt: loose clods spread across a low ground line.
write("dirt", [
    ribbon([(11, 51, .15), (20, 47, .7), (28, 50, 1.0), (37, 46, .72), (46, 50, .95), (61, 49, .15)], 2.35, "dirt-clods", "#4a4943", .42),
    '<ellipse class="ink-wash" cx="22" cy="43" rx="3.4" ry="2.1" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="39" cy="42" rx="3.0" ry="1.8" fill="#77746a"/>',
    '<ellipse class="ink-wash" cx="52" cy="44" rx="3.8" ry="2.0" fill="#77746a"/>',
    ribbon([(16, 56, .2), (29, 57, .7), (43, 56, 1.0), (57, 57, .2)], 1.0, "dirt-ground", "#77746a"),
])

# Log: a horizontal fallen trunk with bark ridges and a visible cut end.
write("log", [
    ribbon([(13, 32, .15), (27, 28, .72), (42, 31, 1.0), (57, 32, .15)], 2.5, "log-upper-bark", "#262522", .38),
    ribbon([(14, 47, .15), (28, 50, .72), (43, 47, 1.0), (57, 47, .15)], 1.7, "log-lower-bark", "#4a4943", .38),
    ribbon([(14, 33, .15), (13, 40, .72), (14, 47, .15)], 1.2, "log-cut-left", "#77746a", .34),
    ribbon([(57, 32, .15), (62, 36, .72), (61, 43, 1.0), (57, 47, .15)], 1.25, "log-cut-end", "#77746a", .36),
    ribbon([(19, 34, .2), (29, 37, .7), (42, 35, .2)], 1.0, "log-bark-one", "#262522"),
    ribbon([(18, 41, .2), (30, 43, .7), (45, 41, .2)], .95, "log-bark-two", "#77746a"),
    ribbon([(57, 36, .2), (60, 38, .7), (58, 42, .2)], .8, "log-ring", "#262522"),
    ribbon([(56, 40, .2), (60, 41, .7), (58, 44, .2)], .7, "log-ring-two", "#262522"),
])

# Oak: a broad irregular crown, thick trunk, and two visible limbs.
write("oak", [
    '<path class="ink-wash" fill="#5d5a54" d="M 14 34 C 14 27 21 22 29 24 C 33 17 42 17 46 24 C 54 21 60 27 58 35 C 55 41 47 41 40 38 C 32 43 22 41 17 37 C 15 36 14 35 14 34 Z"/>',
    ribbon([(14, 35, .15), (20, 27, .72), (29, 29, 1.0), (35, 23, .15)], 4.0, "oak-crown-left", "#4a4943", .42),
    ribbon([(27, 27, .15), (35, 18, .8), (44, 23, .15)], 4.4, "oak-crown-host", "#262522", .4),
    ribbon([(39, 25, .15), (48, 20, .72), (57, 28, 1.0), (59, 35, .15)], 3.5, "oak-crown-right", "#4a4943", .42),
    ribbon([(17, 38, .15), (30, 35, .72), (43, 39, 1.0), (57, 35, .15)], 1.2, "oak-crown-dry", "#77746a", .42),
    ribbon([(36, 40, .2), (35, 48, .7), (36, 58, .2)], 3.0, "oak-trunk", "#262522", .32),
    ribbon([(35, 46, .2), (27, 41, .7), (21, 36, .2)], 1.8, "oak-limb-left", "#262522", .32),
    ribbon([(37, 46, .2), (45, 40, .7), (52, 34, .2)], 1.8, "oak-limb-right", "#262522", .32),
    ribbon([(22, 29, .2), (29, 27, .7), (36, 29, .2)], .8, "oak-crown-mark", "#77746a"),
])

# Soil: an exposed cross-section with a darker upper layer and fine roots.
write("soil", [
    ribbon([(11, 39, .15), (22, 35, .72), (35, 39, 1.0), (47, 36, .72), (61, 40, .15)], 2.45, "soil-surface", "#262522", .4),
    ribbon([(14, 48, .15), (27, 45, .72), (40, 49, 1.0), (57, 46, .15)], 1.15, "soil-layer", "#77746a", .4),
    ribbon([(36, 39, .2), (33, 46, .7), (29, 53, .2)], 1.0, "soil-root-left", "#77746a"),
    ribbon([(37, 40, .2), (40, 47, .7), (45, 53, .2)], 1.0, "soil-root-right", "#77746a"),
    ribbon([(30, 48, .2), (25, 49, .7), (21, 48, .2)], .75, "soil-fine-root", "#77746a"),
])

# Sprout: two tender leaves lifting from a small soil cradle.
write("sprout", [
    ribbon([(36, 56, .2), (35, 45, .7), (36, 34, .2)], 1.65, "sprout-stem", "#4a4943", .34),
    '<path class="ink-wash" fill="#4a4943" d="M 35 36 C 27 35 22 30 24 26 C 29 25 34 29 36 34 Z"/>',
    '<path class="ink-wash" fill="#77746a" d="M 36 34 C 39 27 46 24 51 26 C 51 32 44 36 36 36 Z"/>',
    ribbon([(21, 54, .15), (30, 50, .7), (39, 53, 1.0), (49, 50, .7), (57, 54, .15)], 1.75, "sprout-soil", "#4a4943", .4),
    ribbon([(29, 55, .2), (36, 53, .7), (44, 55, .2)], .8, "sprout-soil-mark", "#77746a"),
])

# Nest: a low woven cradle made from crossing loaded and broken passes.
write("nest", [
    ribbon([(12, 39, .15), (23, 47, .68), (37, 50, 1.0), (52, 46, .7), (61, 37, .15)], 2.35, "nest-cradle", "#4a4943", .38),
    ribbon([(15, 35, .15), (27, 40, .7), (40, 41, 1.0), (56, 34, .15)], 1.45, "nest-rim", "#262522", .4),
    ribbon([(18, 44, .15), (29, 37, .72), (44, 47, .9), (57, 40, .15)], .95, "nest-weave-one", "#77746a", .42),
    ribbon([(20, 49, .15), (34, 42, .72), (49, 49, .15)], .82, "nest-weave-two", "#77746a", .4),
    '<ellipse class="ink-wash" cx="31" cy="34" rx="3.1" ry="4.2" fill="#4a4943"/>',
    '<ellipse class="ink-wash" cx="40" cy="33" rx="3" ry="4.1" fill="#77746a"/>',
])

# Tool: a hand trowel held diagonally, with one dark handle and a dry blade.
write("tool", [
    ribbon([(20, 55, .15), (28, 47, .7), (37, 38, 1.0), (45, 29, .15)], 2.25, "tool-shaft", "#262522", .32),
    ribbon([(43, 31, .15), (48, 26, .75), (53, 21, .15)], 3.4, "tool-handle", "#4a4943", .3),
    ribbon([(19, 55, .15), (14, 49, .7), (13, 42, 1.0), (20, 45, .7), (27, 49, .15)], 1.7, "tool-blade", "#77746a", .38),
    ribbon([(17, 50, .15), (21, 48, .75), (25, 49, .15)], .72, "tool-blade-ridge", "#4a4943", .34),
    ribbon([(46, 28, .15), (50, 30, .75), (54, 27, .15)], .68, "tool-grip-mark", "#77746a", .36),
])

print("redrew all 18 plant glyphs as authored botanical sumi-e studies")
