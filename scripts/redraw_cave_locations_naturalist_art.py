#!/usr/bin/env python3
"""Redraw Colossal Cave locations as atmospheric sumi-e place studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "cave_locations"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", *, dry=False) -> str:
    d = stroke_path(
        points(*values), width=width, seed=seed, wobble=.26,
        taper_start=.10, taper_end=.08,
    )
    class_name = "ink-dry" if dry else "ink-wash"
    brush_pass = "dry-edge-v2" if dry else "loaded-ribbon-v2"
    return (
        f'<path class="{class_name}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{brush_pass}"/>'
    )


def mass(d: str, color="#4a4943") -> str:
    return (
        f'<path class="ink-wash" d="{d}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
    )


def dab(cx, cy, rx, ry, color="#262522") -> str:
    return (
        f'<ellipse class="ink-wash" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'
    )


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="cave locations / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>cave locations / {name} — naturalist sumi-e place study</title>{''.join(marks)}</svg>
''')


# The road enters from the lower-left and spends itself at a small building.
# Unequal verges and a distant roof make the location legible without a map pin.
write("end-of-road", [
    ribbon([(7, 59, .10), (18, 53, .70), (29, 45, .94), (39, 36, .08)], 3.0, "road-host", "#4a4943"),
    ribbon([(11, 63, .10), (23, 57, .72), (33, 48, .84), (41, 40, .08)], .85, "road-dry-verge", "#77746a", dry=True),
    ribbon([(38, 36, .10), (47, 27, .76), (57, 33, .08)], 2.0, "road-house-roof"),
    ribbon([(42, 34, .10), (42, 47, .72), (43, 53, .08)], 1.25, "road-house-left", "#4a4943"),
    ribbon([(56, 34, .10), (56, 45, .72), (55, 51, .08)], .95, "road-house-right", "#77746a", dry=True),
    ribbon([(43, 52, .10), (49, 50, .72), (56, 51, .08)], 1.4, "road-house-base"),
    ribbon([(5, 51, .10), (13, 48, .72), (20, 50, .08)], .72, "road-stream", "#bcb9af", dry=True),
])


# The grate sits in sloping earth.  Three bars are enough; a grass guest mark
# and broken horizon prevent it from becoming a generic grid icon.
write("outside-grate", [
    ribbon([(9, 31, .10), (23, 25, .72), (39, 26, .92), (57, 31, .08)], 2.1, "grate-bank"),
    ribbon([(17, 35, .10), (28, 33, .72), (42, 35, .92), (54, 33, .08)], 2.0, "grate-top"),
    ribbon([(18, 36, .10), (20, 47, .72), (23, 56, .08)], 1.45, "grate-left"),
    ribbon([(53, 35, .10), (50, 46, .72), (48, 54, .08)], 1.05, "grate-right", "#77746a", dry=True),
    ribbon([(27, 34, .10), (28, 44, .72), (29, 53, .08)], 1.15, "grate-bar-a", "#4a4943"),
    ribbon([(39, 35, .10), (39, 44, .72), (39, 53, .08)], .85, "grate-bar-b", "#77746a", dry=True),
    ribbon([(22, 45, .10), (34, 43, .72), (49, 44, .08)], .72, "grate-crossbar", "#bcb9af", dry=True),
    ribbon([(57, 30, .10), (61, 24, .72), (65, 22, .08)], .85, "grate-grass", "#4a4943", dry=True),
])


# A loaded ceiling gesture presses down on a scattered rubble field.  The
# detached stones are intentional place evidence, not decorative confetti.
write("debris-room", [
    ribbon([(8, 53, .10), (12, 33, .70), (24, 19, .94), (39, 15, .86), (55, 23, .72), (64, 43, .08)], 2.6, "debris-cavern"),
    ribbon([(13, 55, .10), (24, 48, .72), (34, 55, .08)], 3.0, "debris-ridge-a", "#4a4943"),
    ribbon([(31, 55, .10), (40, 44, .72), (48, 55, .08)], 2.3, "debris-ridge-b"),
    ribbon([(47, 55, .10), (55, 49, .72), (62, 56, .08)], 1.45, "debris-ridge-c", "#77746a", dry=True),
    dab(20, 58, 2.4, 1.5, "#262522"),
    dab(42, 59, 1.8, 1.2, "#77746a"),
    ribbon([(27, 31, .10), (36, 29, .72), (45, 32, .08)], .72, "debris-ceiling-crack", "#bcb9af", dry=True),
])


# The bird chamber gives the small bird a cavern-sized host and a stone perch.
write("bird-chamber", [
    ribbon([(8, 58, .10), (11, 37, .68), (22, 20, .94), (37, 14, .84), (54, 22, .72), (64, 48, .08)], 2.5, "bird-cavern"),
    ribbon([(20, 51, .10), (32, 47, .72), (46, 49, .08)], 1.7, "bird-perch", "#4a4943"),
    ribbon([(29, 39, .10), (35, 34, .78), (42, 36, .94), (47, 40, .08)], 3.6, "chamber-bird-body", "#4a4943"),
    dab(47, 34, 2.7, 2.4, "#262522"),
    ribbon([(49, 34, .10), (54, 33, .72), (58, 35, .08)], .95, "chamber-bird-beak"),
    ribbon([(31, 39, .10), (25, 36, .72), (21, 33, .08)], 1.2, "chamber-bird-tail", "#77746a", dry=True),
    ribbon([(15, 57, .10), (27, 55, .72), (39, 57, .08)], .72, "bird-floor", "#bcb9af", dry=True),
])


# The hall is vertical and nearly empty; mist crosses it in three lifted bands.
write("hall-of-mists", [
    ribbon([(10, 61, .10), (11, 40, .68), (18, 22, .92), (29, 11, .08)], 2.6, "mist-hall-left"),
    ribbon([(62, 60, .10), (59, 40, .68), (52, 23, .90), (43, 13, .08)], 1.75, "mist-hall-right", "#77746a", dry=True),
    ribbon([(17, 31, .10), (28, 27, .72), (40, 30, .90), (55, 26, .08)], 1.25, "mist-band-high", "#bcb9af", dry=True),
    ribbon([(12, 43, .10), (25, 39, .72), (39, 43, .90), (59, 38, .08)], 1.6, "mist-band-mid", "#77746a", dry=True),
    ribbon([(17, 55, .10), (31, 51, .72), (44, 54, .90), (57, 50, .08)], .85, "mist-band-low", "#bcb9af", dry=True),
    ribbon([(30, 12, .10), (35, 18, .72), (38, 27, .08)], .72, "mist-stalactite", "#4a4943", dry=True),
])


# The Plover Room is identified by the emerald held inside a broad cave arch.
# Only four facet strokes are needed at this scale.
write("plover-room", [
    ribbon([(8, 59, .10), (11, 38, .68), (22, 20, .94), (37, 13, .86), (53, 21, .72), (64, 51, .08)], 2.6, "plover-cavern"),
    ribbon([(36, 27, .10), (45, 37, .72), (36, 52, .08)], 2.0, "plover-gem-right"),
    ribbon([(36, 27, .10), (27, 37, .72), (36, 52, .08)], 1.45, "plover-gem-left", "#77746a", dry=True),
    ribbon([(27, 37, .10), (36, 40, .92), (45, 37, .08)], 1.05, "plover-gem-cross"),
    ribbon([(36, 28, .10), (36, 40, .72), (36, 51, .08)], .80, "plover-gem-spine", "#4a4943"),
    ribbon([(14, 58, .10), (27, 55, .72), (42, 57, .08)], .72, "plover-floor", "#bcb9af", dry=True),
])


# Castalia's rook is a brush-built tower carrying a living central flame.  The
# battlements are separate guest marks so the silhouette stays open and airy.
write("castalia-rook-flame", [
    ribbon([(22, 57, .10), (23, 44, .72), (22, 30, .08)], 3.0, "rook-left"),
    ribbon([(50, 57, .10), (49, 44, .72), (50, 30, .08)], 2.1, "rook-right", "#77746a", dry=True),
    ribbon([(21, 57, .10), (34, 59, .86), (51, 57, .08)], 2.7, "rook-base", "#262522"),
    ribbon([(22, 31, .10), (29, 28, .72), (35, 31, .08)], 1.65, "rook-battlement-left"),
    ribbon([(37, 31, .10), (43, 27, .72), (50, 30, .08)], 1.15, "rook-battlement-right", "#77746a", dry=True),
    ribbon([(22, 30, .10), (22, 23, .72), (29, 23, .90), (29, 28, .72), (36, 28, .90), (36, 23, .72), (43, 23, .90), (43, 29, .72), (50, 29, .08)], 1.15, "rook-crenellation", "#262522"),
    ribbon([(27, 46, .10), (36, 43, .84), (46, 46, .08)], 1.05, "rook-crossbar", "#bcb9af", dry=True),
    ribbon([(36, 46, .10), (32, 39, .72), (36, 33, .92), (34, 25, .72), (39, 17, .08)], 2.5, "rook-flame-host", "#4a4943"),
    ribbon([(38, 34, .10), (43, 29, .72), (42, 23, .08)], 1.0, "rook-flame-guest", "#77746a", dry=True),
])


print("redrew all 7 cave-location PUA glyphs as atmospheric sumi-e studies")
