#!/usr/bin/env python3
"""Author a small set of object glyphs as restrained sumi-e brush studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.26):
    # Make familiar silhouettes readable at 32px while retaining taper and
    # irregular pressure.  Fine descriptive marks remain lighter by color.
    width = max(width * 1.35, 1.2)
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/objects" / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 9 63 C 24 61 42 64 63 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="objects / {name}" {match.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>objects / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


# A bowl: an uneven rim, one continuous vessel stroke, and a quiet wash inside.
write("bowl", [
    ribbon([(14, 25, .2), (20, 21, .62), (30, 20, 1.0), (42, 21, .78), (54, 24, .35), (58, 27, .2)], 2.2, "bowl-rim", wobble=.3),
    ribbon([(14, 26, .18), (16, 36, .62), (20, 45, .94), (28, 50, 1.0), (39, 51, .8), (50, 47, .45), (56, 39, .2)], 2.3, "bowl-body", "#3c3b36", .3),
    ribbon([(19, 31, .2), (29, 34, .65), (41, 34, 1.0), (52, 31, .24)], 1.05, "bowl-inner", "#77746a", .28),
    ribbon([(27, 50, .2), (28, 56, .7), (37, 57, 1.0), (45, 55, .2)], 1.25, "bowl-foot", "#4a4943", .28),
    ribbon([(24, 39, .2), (31, 42, .7), (41, 42, .2)], .8, "bowl-wash-mark", "#77746a", .31),
])


# Fork: a single tapered handle with four separated, calligraphic tines.
write("fork", [
    ribbon([(18, 57, .2), (25, 49, .65), (34, 40, 1.0), (43, 30, .7), (51, 20, .2)], 2.35, "fork-handle", wobble=.28),
    ribbon([(42, 30, .18), (39, 20, .72), (38, 14, .25)], 1.35, "fork-tine-1", wobble=.26),
    ribbon([(45, 29, .18), (44, 19, .72), (44, 13, .25)], 1.35, "fork-tine-2", wobble=.26),
    ribbon([(48, 28, .18), (49, 18, .72), (50, 13, .25)], 1.35, "fork-tine-3", wobble=.26),
    ribbon([(51, 28, .18), (54, 19, .72), (56, 15, .25)], 1.35, "fork-tine-4", wobble=.26),
])


# Nail: broad irregular head, tapering shaft, and a dry edge at the point.
write("nail", [
    ribbon([(27, 17, .25), (33, 15, .8), (41, 16, 1.0), (47, 19, .28)], 3.6, "nail-head", "#3c3b36", .3),
    ribbon([(37, 19, .2), (37, 30, .72), (36, 43, 1.0), (35, 56, .22)], 2.3, "nail-shaft", wobble=.25),
    ribbon([(33, 55, .2), (35, 60, .8), (37, 55, .2)], 1.1, "nail-point", "#77746a", .28),
])


# Roof: a low, asymmetrical house roof with one supporting wash.
write("roof", [
    ribbon([(10, 33, .2), (22, 24, .72), (35, 15, 1.0), (48, 24, .72), (61, 34, .2)], 2.35, "roof-ridge", wobble=.3),
    ribbon([(17, 34, .2), (20, 47, .7), (21, 55, .25)], 1.45, "roof-left-wall", "#4a4943", .3),
    ribbon([(53, 34, .2), (51, 46, .7), (50, 55, .25)], 1.45, "roof-right-wall", "#4a4943", .3),
    ribbon([(21, 55, .2), (34, 56, .7), (50, 55, .2)], 1.55, "roof-ground", "#3c3b36", .28),
    ribbon([(31, 55, .2), (31, 47, .7), (39, 47, 1.0), (39, 55, .2)], 1.1, "roof-door", "#77746a", .25),
    ribbon([(17, 35, .2), (25, 37, .7), (35, 36, 1.0), (46, 37, .7), (54, 35, .2)], .85, "roof-eave", "#77746a", .3),
    ribbon([(25, 27, .2), (28, 24, .7), (31, 23, .2)], .8, "roof-tile-left", "#77746a", .3),
    ribbon([(40, 23, .2), (44, 25, .7), (47, 28, .2)], .8, "roof-tile-right", "#77746a", .3),
])


# Rope: one long coiled brush ribbon, not a geometric double outline.
write("rope", [
    ribbon([(18, 47, .2), (14, 41, .55), (16, 32, .95), (23, 25, 1.0), (34, 22, .78), (46, 24, .45), (54, 30, .2), (56, 37, .5), (52, 43, .92), (44, 46, .75), (35, 44, .42), (30, 39, .2), (31, 34, .55), (36, 32, .9), (42, 33, .3)], 2.25, "rope-coil", "#3c3b36", .31),
    ribbon([(18, 48, .2), (25, 53, .7), (36, 55, 1.0), (49, 53, .3)], 1.2, "rope-tail", "#77746a", .28),
    ribbon([(42, 33, .2), (48, 29, .7), (53, 31, .2)], 1.0, "rope-loose-end", "#262522", .34),
    ribbon([(48, 29, .2), (53, 27, .7), (57, 29, .2)], .75, "rope-fiber", "#77746a", .34),
])


# Sign: a worn board and post, with the silhouette doing most of the work.
write("sign", [
    ribbon([(15, 25, .2), (27, 23, .7), (42, 24, 1.0), (57, 22, .6), (61, 25, .2), (60, 37, .35), (46, 39, .8), (30, 37, 1.0), (15, 39, .2), (15, 25, .2)], 2.1, "sign-board", "#3c3b36", .3),
    ribbon([(36, 38, .2), (36, 48, .8), (35, 59, .25)], 2.0, "sign-post", wobble=.27),
    ribbon([(28, 59, .2), (36, 57, .78), (44, 59, .2)], 1.3, "sign-foot", "#77746a", .28),
    ribbon([(23, 31, .2), (30, 29, .7), (38, 31, .2)], .8, "sign-letter-one", "#77746a", .3),
    ribbon([(26, 35, .2), (35, 33, .7), (46, 35, .2)], .8, "sign-letter-two", "#77746a", .3),
])


# Axle: two imperfect wheel dabs joined by a single axle stroke.
write("axle", [
    ribbon([(17, 36, .2), (27, 36, .7), (38, 37, 1.0), (49, 36, .7), (57, 36, .2)], 2.0, "axle-bar", wobble=.25),
    ribbon([(23, 25, .2), (18, 29, .72), (17, 37, 1.0), (21, 45, .72), (28, 48, .25), (33, 44, .2), (34, 35, .7), (30, 28, .25), (23, 25, .2)], 1.75, "axle-wheel-left", "#4a4943", .29),
    ribbon([(47, 25, .2), (42, 30, .72), (42, 38, 1.0), (46, 46, .72), (53, 48, .25), (58, 44, .2), (59, 35, .7), (54, 28, .25), (47, 25, .2)], 1.75, "axle-wheel-right", "#4a4943", .29),
    ribbon([(23, 30, .2), (24, 36, .8), (27, 42, .25)], .9, "axle-spoke-left", "#77746a", .25),
    ribbon([(28, 36, .2), (23, 36, .8), (19, 39, .25)], .9, "axle-spoke-left-cross", "#77746a", .25),
    ribbon([(48, 30, .2), (49, 36, .8), (53, 42, .25)], .9, "axle-spoke-right", "#77746a", .25),
    ribbon([(53, 36, .2), (48, 36, .8), (44, 39, .25)], .9, "axle-spoke-right-cross", "#77746a", .25),
    '<ellipse class="ink-wash" cx="24" cy="36" rx="2.2" ry="2" fill="#262522"/>',
    '<ellipse class="ink-wash" cx="48" cy="36" rx="2.2" ry="2" fill="#262522"/>',
])


# Drum: a rounded body, rim, and a few loose vertical lacing marks.
write("drum", [
    ribbon([(23, 22, .2), (30, 18, .7), (42, 18, 1.0), (50, 22, .3)], 2.25, "drum-rim", wobble=.28),
    ribbon([(23, 23, .2), (22, 35, .65), (24, 49, 1.0), (31, 55, .7), (42, 56, .3), (50, 50, .2), (51, 36, .65), (50, 23, .2)], 2.2, "drum-body", "#4a4943", .3),
    ribbon([(26, 29, .2), (35, 33, .68), (46, 30, .25)], 1.05, "drum-skin", "#77746a", .3),
    ribbon([(27, 27, .2), (28, 40, .8), (29, 51, .25)], .9, "drum-lace-left", "#77746a", .25),
    ribbon([(47, 27, .2), (46, 40, .8), (45, 51, .25)], .9, "drum-lace-right", "#77746a", .25),
    ribbon([(25, 22, .2), (20, 17, .72), (16, 13, .25)], 1.1, "drumstick-left", "#262522", .28),
    ribbon([(49, 22, .2), (54, 17, .72), (58, 13, .25)], 1.1, "drumstick-right", "#262522", .28),
    '<ellipse class="ink-wash" cx="36" cy="23" rx="11" ry="3.4" fill="#77746a"/>',
    ribbon([(27, 23, .2), (36, 25, .7), (46, 23, .2)], .85, "drumhead-mark", "#262522", .28),
    ribbon([(25, 34, .2), (29, 36, .7), (31, 47, .2)], .8, "drum-lace-extra-left", "#262522", .3),
    ribbon([(47, 34, .2), (43, 36, .7), (41, 47, .2)], .8, "drum-lace-extra-right", "#262522", .3),
])


# Arch: one stone-like brush arch, with the opening left as negative space.
write("arch", [
    ribbon([(13, 55, .2), (14, 40, .55), (18, 27, .9), (26, 19, 1.0), (37, 16, .76), (48, 19, .5), (56, 28, .2), (59, 40, .55), (59, 55, .2)], 2.6, "arch-outer", "#3c3b36", .3),
    ribbon([(24, 55, .2), (24, 42, .58), (27, 32, .9), (34, 27, 1.0), (42, 29, .66), (48, 36, .3), (49, 55, .2)], 1.35, "arch-inner", "#77746a", .28),
    ribbon([(16, 38, .2), (21, 37, .7), (25, 39, .2)], .8, "arch-masonry-left", "#77746a", .3),
    ribbon([(48, 39, .2), (53, 37, .7), (57, 39, .2)], .8, "arch-masonry-right", "#77746a", .3),
    ribbon([(29, 20, .2), (34, 19, .7), (39, 20, .2)], .8, "arch-keystone", "#77746a", .28),
])

print("redrew bowl, fork, nail, roof, rope, sign, axle, drum, and arch")
