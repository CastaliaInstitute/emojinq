#!/usr/bin/env python3
"""Author irregular weather phenomena as sparse sumi-e brush studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.3):
    role = "ink-dry" if color == "#77746a" else "ink-wash"
    if color == "#77746a":
        color = "#5f5c55"
    # Weather gestures must remain visible at the 32 px toddler-review size.
    # Preserve pressure variation while keeping the lightest lift-off from
    # collapsing into a one-pixel hairline.
    width = max(width * 1.32, 1.15)
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color, class_name=role)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/weather_sky" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="weather_sky / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>weather_sky / {name} — naturalist sumi-e study</title>{''.join(marks)}</svg>
''')


# Frost: a crooked ice fern with uneven side growth, not a perfect snowflake.
write("frost", [
    '<path class="ink-wash" fill="#4a4943" d="M 35 14 L 40 25 L 36 36 L 30 26 Z"/>',
    ribbon([(35, 59, .2), (35, 47, .7), (36, 35, 1.0), (34, 20, .2)], 2.8, "frost-spine", "#4a4943", .35),
    ribbon([(35, 45, .2), (27, 40, .7), (19, 32, .2)], 2.15, "frost-branch-left-low", "#262522"),
    ribbon([(35, 38, .2), (44, 34, .7), (53, 26, .2)], 2.2, "frost-branch-right-mid", "#262522"),
    ribbon([(35, 38, .2), (27, 34, .7), (20, 27, .2)], 1.8, "frost-branch-left-mid", "#4a4943"),
    ribbon([(35, 45, .2), (44, 42, .7), (52, 36, .2)], 1.75, "frost-branch-right-low", "#4a4943"),
    ribbon([(35, 31, .2), (29, 27, .7), (26, 23, .2)], 1.0, "frost-branch-left-high", "#77746a"),
    ribbon([(34, 25, .2), (40, 21, .7), (42, 17, .2)], .95, "frost-branch-right-high", "#77746a"),
    ribbon([(26, 34, .2), (24, 29, .7), (21, 27, .2)], .8, "frost-needle-left", "#77746a"),
    ribbon([(48, 29, .2), (51, 25, .7), (54, 24, .2)], .8, "frost-needle-right", "#77746a"),
    '<path class="ink-wash" fill="#77746a" d="M 31 28 L 28 24 L 30 20 L 33 25 Z M 42 37 L 46 33 L 50 34 L 46 38 Z M 28 44 L 24 41 L 22 43 L 26 47 Z"/>',
])

# Storm: a low cloud feeding a rotating descending wind column.
write("storm", [
    '<path class="ink-wash" fill="#4a4943" d="M 13 27 C 14 22 20 19 26 21 C 29 16 38 16 42 21 C 49 18 57 21 59 27 C 56 31 48 31 42 30 C 34 33 24 31 18 32 C 15 31 13 29 13 27 Z"/>',
    ribbon([(17, 32, .2), (25, 30, .7), (36, 32, 1.0), (48, 30, .7), (56, 33, .2)], 1.6, "storm-wind-one", "#262522", .34),
    ribbon([(22, 39, .2), (31, 37, .7), (41, 39, 1.0), (50, 37, .2)], 1.45, "storm-wind-two", "#4a4943", .34),
    ribbon([(28, 46, .2), (35, 44, .7), (42, 46, .2)], 1.2, "storm-funnel", "#77746a", .34),
    ribbon([(35, 49, .2), (36, 54, .7), (35, 58, .2)], .8, "storm-tail", "#77746a", .34),
])

# Puddle: an irregular shallow pool with a falling drop and concentric ripples.
write("puddle", [
    '<path class="ink-wash" fill="#4a4943" d="M 14 45 C 20 39 32 40 39 43 C 47 39 59 42 61 47 C 56 54 44 55 35 53 C 25 56 16 52 14 45 Z"/>',
    ribbon([(21, 47, .2), (29, 45, .7), (38, 47, 1.0), (48, 45, .7), (56, 47, .2)], 1.05, "puddle-ripple-one", "#77746a", .32),
    ribbon([(27, 52, .2), (34, 50, .7), (42, 52, .2)], .85, "puddle-ripple-two", "#77746a", .32),
    '<path class="ink-wash" fill="#262522" d="M 36 17 C 32 22 32 27 36 31 C 40 27 40 22 36 17 Z"/>',
    ribbon([(36, 31, .2), (36, 36, .7), (35, 40, .2)], .8, "puddle-drop-trail", "#77746a", .3),
])

# Lightning: a soft cloud body with one irregular fork descending from it.
write("lightning", [
    '<path class="ink-wash" fill="#4a4943" d="M 13 28 C 15 23 21 21 27 23 C 30 18 38 18 42 23 C 49 20 56 23 58 28 C 55 32 47 32 41 31 C 34 34 24 32 18 33 C 15 32 13 30 13 28 Z"/>',
    ribbon([(36, 25, .2), (32, 33, .7), (37, 32, 1.0), (31, 43, .7), (40, 37, .2)], 2.45, "lightning-fork", "#262522", .34),
    ribbon([(19, 34, .2), (22, 39, .7), (21, 44, .2)], .85, "lightning-rain-left", "#77746a"),
    ribbon([(50, 34, .2), (53, 39, .7), (52, 44, .2)], .85, "lightning-rain-right", "#77746a"),
    '<path class="ink-wash" fill="#262522" d="M 35 27 L 27 42 L 35 41 L 29 57 L 47 36 L 39 38 L 44 27 Z"/>',
])

# Breeze: three unequal, open passes cross the square without enclosing it.
write("breeze", [
    ribbon([(8, 25, .15), (19, 19, .65), (31, 21, 1.0), (41, 27, .58), (52, 26, .2)], 1.75, "breeze-high", "#262522", .38),
    ribbon([(13, 38, .18), (24, 33, .68), (35, 36, 1.0), (45, 41, .58), (58, 38, .18)], 1.5, "breeze-middle", "#4a4943", .4),
    ribbon([(22, 50, .18), (31, 47, .72), (41, 49, 1.0), (49, 53, .2)], 1.05, "breeze-low", "#77746a", .42),
    ribbon([(52, 25, .2), (58, 20, .8), (64, 21, .3), (60, 27, .18)], .9, "breeze-leaf", "#77746a", .32),
    '<path class="ink-wash" fill="#4a4943" d="M 54 20 C 58 14 65 15 66 20 C 63 25 58 27 54 24 Z"/>',
])

# Drizzle: a low wash carries a sparse curtain of separate, tilted drops.
write("drizzle", [
    '<path class="ink-wash" fill="#77746a" d="M 13 30 C 15 24 22 22 28 24 C 32 18 41 19 45 24 C 52 22 58 25 59 30 C 53 34 20 34 13 30 Z"/>',
    ribbon([(13, 30, .18), (19, 24, .7), (27, 25, 1.0), (33, 20, .72), (42, 21, .9), (48, 27, .65), (57, 28, .2)], 3.05, "drizzle-cloud", "#4a4943", .36),
    ribbon([(20, 36, .2), (18, 43, .85), (16, 49, .2)], .85, "drizzle-one", "#77746a", .3),
    ribbon([(31, 35, .2), (29, 44, .9), (27, 51, .2)], .9, "drizzle-two", "#262522", .3),
    ribbon([(43, 36, .2), (41, 43, .8), (39, 49, .2)], .82, "drizzle-three", "#77746a", .32),
    ribbon([(54, 35, .2), (52, 42, .82), (50, 47, .2)], .78, "drizzle-four", "#4a4943", .32),
    '<path class="ink-wash" fill="#4a4943" d="M 19 36 C 16 41 16 46 19 49 C 23 46 23 41 19 36 Z M 34 36 C 31 42 31 48 34 51 C 38 47 38 42 34 36 Z M 49 35 C 46 40 46 45 49 48 C 53 44 53 40 49 35 Z"/>',
])

# Heat: the empty center is the glare; wavering vertical marks carry the air.
write("heat", [
    '<path class="ink-wash" fill="#4a4943" d="M 36 12 C 42 12 47 17 47 23 C 47 29 42 34 36 34 C 30 34 25 29 25 23 C 25 17 30 12 36 12 Z"/>',
    ribbon([(36, 10, .2), (36, 7, .7), (36, 5, .2)], 1.2, "heat-ray-top", "#262522"),
    ribbon([(21, 13, .2), (17, 9, .7), (14, 7, .2)], 1.1, "heat-ray-left", "#77746a"),
    ribbon([(51, 13, .2), (55, 9, .7), (58, 7, .2)], 1.1, "heat-ray-right", "#77746a"),
    ribbon([(14, 51, .2), (26, 48, .65), (38, 51, 1.0), (49, 49, .55), (59, 51, .2)], 1.05, "heat-horizon", "#77746a", .36),
    ribbon([(21, 43, .2), (18, 38, .75), (23, 33, 1.0), (20, 27, .7), (23, 20, .2)], 1.55, "heat-left", "#4a4943", .4),
    ribbon([(36, 44, .2), (32, 38, .72), (37, 32, 1.0), (34, 26, .7), (38, 18, .2)], 1.85, "heat-host", "#262522", .42),
    ribbon([(51, 42, .2), (48, 37, .7), (52, 31, .95), (49, 25, .62), (52, 21, .2)], 1.3, "heat-right", "#77746a", .4),
])

# Ice: one leaning shard, described by unequal edge and fracture gestures.
write("ice", [
    ribbon([(17, 48, .2), (24, 30, .72), (35, 15, 1.0), (45, 27, .58), (55, 46, .2)], 2.05, "ice-ridge", "#262522", .31),
    ribbon([(17, 48, .2), (31, 55, .75), (47, 52, 1.0), (55, 46, .2)], 1.45, "ice-foot", "#4a4943", .3),
    ribbon([(24, 31, .2), (37, 34, .85), (49, 28, .2)], 1.05, "ice-fracture-high", "#77746a", .34),
    ribbon([(36, 16, .2), (36, 34, .8), (32, 53, .2)], 1.0, "ice-fracture-long", "#4a4943", .3),
    ribbon([(37, 34, .2), (47, 51, .85), (55, 46, .2)], .8, "ice-fracture-low", "#77746a", .34),
])

# Shade: an off-center parasol holds a generous field of unpainted shelter.
write("shade", [
    ribbon([(9, 33, .15), (17, 23, .65), (29, 18, 1.0), (43, 20, .78), (57, 29, .42), (63, 34, .15)], 2.45, "shade-canopy", "#262522", .34),
    ribbon([(11, 34, .2), (24, 32, .68), (38, 35, 1.0), (51, 32, .62), (62, 34, .2)], 1.2, "shade-eave", "#4a4943", .36),
    ribbon([(36, 34, .2), (35, 45, .72), (36, 57, .25)], 1.75, "shade-post", "#4a4943", .3),
    ribbon([(36, 57, .2), (40, 60, .8), (44, 58, .2)], .85, "shade-hook", "#77746a", .31),
    ribbon([(18, 38, .2), (24, 42, .75), (30, 40, .2)], .72, "shade-shadow", "#77746a", .38),
])

# Sky: a small host cloud and distant guest sun leave most of the field open.
write("sky", [
    '<path class="ink-wash" fill="#77746a" d="M 12 41 C 14 35 21 33 27 36 C 31 30 40 31 44 36 C 51 33 59 36 61 42 C 54 46 20 47 12 41 Z"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 18 15 C 23 12 29 14 32 19 C 33 24 30 29 25 31 C 20 31 16 27 15 22 C 15 19 16 17 18 15 Z"/>',
    ribbon([(10, 42, .18), (19, 36, .68), (28, 38, 1.0), (36, 34, .72), (44, 37, .9), (54, 36, .5), (62, 41, .18)], 1.75, "sky-cloud-host", "#4a4943", .4),
    ribbon([(15, 47, .18), (27, 44, .7), (39, 47, 1.0), (51, 45, .5), (59, 47, .18)], 1.05, "sky-cloud-underside", "#77746a", .38),
    ribbon([(18, 24, .2), (20, 18, .72), (26, 15, 1.0), (32, 18, .62), (34, 23, .2)], 1.25, "sky-sun-arc", "#262522", .31),
    ribbon([(48, 23, .2), (51, 20, .72), (54, 23, .2)], .72, "sky-bird-one", "#77746a", .34),
    ribbon([(56, 27, .2), (59, 25, .7), (62, 27, .2)], .62, "sky-bird-two", "#77746a", .34),
])

# Thunder: a charged cloud, a short strike, and two broken sound gestures.
write("thunder", [
    ribbon([(12, 29, .18), (20, 22, .68), (29, 24, 1.0), (37, 19, .76), (47, 23, .9), (58, 28, .18)], 3.15, "thunder-cloud", "#3c3b36", .37),
    ribbon([(38, 28, .2), (32, 38, .72), (38, 37, 1.0), (31, 49, .72), (43, 42, .2)], 2.15, "thunder-strike", "#262522", .35),
    ribbon([(14, 39, .2), (10, 43, .8), (14, 47, .2)], .82, "thunder-rumble-left", "#77746a", .4),
    ribbon([(54, 38, .2), (61, 42, .8), (56, 47, .2)], .9, "thunder-rumble-right", "#4a4943", .4),
    ribbon([(20, 51, .2), (25, 54, .72), (30, 52, .2)], .7, "thunder-echo", "#77746a", .4),
    '<path class="ink-wash" fill="#262522" d="M 37 27 L 28 43 L 36 42 L 30 58 L 48 36 L 40 39 L 45 27 Z"/>',
])

print("redrew 11 weather and sky phenomena as authored sumi-e studies")
