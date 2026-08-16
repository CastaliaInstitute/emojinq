#!/usr/bin/env python3
"""Redraw the rocket PUA family as economical sumi-e machine studies.

The subjects are modern hardware, but the drawing logic is the same as the
book-derived naturalist families: a loaded host gesture establishes weight and
direction, a few guest marks identify the machine, and dry edges leave the
paper active.  Closed diagrammatic outlines are deliberately avoided.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "rockets"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(
    values: list[tuple[float, float, float]],
    width: float,
    seed: str,
    color: str = "#262522",
    *,
    dry: bool = False,
) -> str:
    d = stroke_path(
        points(*values),
        width=width,
        seed=seed,
        wobble=.24,
        taper_start=.10,
        taper_end=.08,
    )
    class_name = "ink-dry" if dry else "ink-wash"
    brush_pass = "dry-edge-v2" if dry else "loaded-ribbon-v2"
    return (
        f'<path class="{class_name}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{brush_pass}"/>'
    )


def mass(d: str, color: str = "#4a4943") -> str:
    return (
        f'<path class="ink-wash" d="{d}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
    )


def dab(cx: float, cy: float, rx: float, ry: float, color: str = "#262522") -> str:
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="rockets / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>rockets / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


# A small research rocket: one loaded ascent, an offset edge, two fins, and a
# broken exhaust.  The body is a brush gesture rather than a traced hull.
write("sounding-rocket", [
    ribbon([(36, 59, .08), (35, 48, .66), (36, 34, 1.0), (35, 20, .78), (38, 10, .08)], 5.0, "sounding-body"),
    ribbon([(38, 12, .10), (42, 20, .68), (42, 35, .84), (40, 48, .08)], 1.05, "sounding-dry-edge", "#77746a", dry=True),
    ribbon([(34, 48, .10), (28, 54, .78), (25, 58, .08)], 2.0, "sounding-fin-left", "#4a4943"),
    ribbon([(38, 49, .10), (43, 54, .72), (46, 56, .08)], 1.35, "sounding-fin-right", "#77746a", dry=True),
    ribbon([(36, 59, .10), (34, 64, .76), (35, 68, .08)], 1.15, "sounding-exhaust", "#4a4943", dry=True),
])


# The orbital vehicle is heavier and already in flight.  A slanted body axis,
# stage collars, and long exhaust separate it from the sounding rocket.
write("orbital-rocket", [
    ribbon([(25, 56, .08), (30, 46, .72), (37, 34, 1.0), (45, 22, .82), (53, 13, .08)], 6.0, "orbital-body"),
    ribbon([(51, 14, .10), (55, 19, .68), (51, 28, .08)], 1.05, "orbital-nose-edge", "#77746a", dry=True),
    ribbon([(31, 45, .12), (39, 48, .80), (45, 47, .08)], 1.15, "orbital-stage-band", "#bcb9af", dry=True),
    ribbon([(28, 48, .10), (20, 49, .72), (15, 54, .08)], 2.0, "orbital-fin-host", "#4a4943"),
    ribbon([(25, 55, .10), (18, 61, .72), (11, 65, .08)], 1.55, "orbital-flame-a", "#4a4943", dry=True),
    ribbon([(29, 57, .10), (25, 63, .72), (22, 67, .08)], .72, "orbital-flame-b", "#77746a", dry=True),
])


# Three imperfect vertical loads make the clustered booster readable without
# outlining three cylinders.  The center core is host; side cores are guests.
write("booster", [
    ribbon([(36, 58, .08), (35, 45, .72), (36, 29, 1.0), (37, 14, .08)], 5.6, "booster-core"),
    ribbon([(25, 56, .08), (24, 43, .70), (25, 28, .94), (27, 18, .08)], 3.4, "booster-left", "#4a4943"),
    ribbon([(47, 56, .08), (48, 43, .68), (47, 29, .90), (45, 19, .08)], 2.5, "booster-right-dry", "#77746a", dry=True),
    ribbon([(23, 53, .10), (18, 58, .72), (16, 62, .08)], 1.4, "booster-left-fin", "#4a4943"),
    ribbon([(49, 53, .10), (54, 58, .72), (56, 61, .08)], 1.0, "booster-right-fin", "#77746a", dry=True),
    ribbon([(35, 59, .10), (36, 64, .74), (34, 68, .08)], 1.2, "booster-exhaust", "#4a4943", dry=True),
])


# Launch is an event, not a vehicle portrait: the dark rising axis dominates,
# while broken ground, flame, and smoke activate the lower empty field.
write("launch", [
    ribbon([(29, 48, .08), (32, 39, .72), (37, 29, 1.0), (43, 19, .78), (49, 12, .08)], 5.0, "launch-ascent"),
    ribbon([(47, 13, .10), (51, 18, .70), (48, 25, .08)], .95, "launch-hull-edge", "#77746a", dry=True),
    ribbon([(31, 46, .10), (25, 49, .72), (21, 54, .08)], 1.65, "launch-fin"),
    ribbon([(29, 49, .10), (27, 57, .74), (23, 64, .08)], 2.0, "launch-flame", "#4a4943"),
    ribbon([(12, 59, .10), (22, 56, .62), (31, 60, .88), (42, 57, .72), (57, 61, .08)], 1.6, "launch-smoke", "#77746a", dry=True),
    ribbon([(9, 64, .10), (20, 62, .72), (32, 65, .08)], .72, "launch-ground", "#bcb9af", dry=True),
])


# A blunt re-entry capsule uses a compact wash, an open dry rim, and a heavy
# heat shield.  Its empty shoulder space keeps the mass from becoming a badge.
write("capsule", [
    mass("M 36 14 C 30 17 25 27 24 38 C 23 47 27 55 35 58 C 43 57 48 50 48 41 C 48 30 43 19 36 14 Z", "#bcb9af"),
    ribbon([(36, 15, .10), (29, 22, .72), (26, 35, .90), (28, 47, .08)], 1.55, "capsule-left-rim", "#262522"),
    ribbon([(38, 16, .10), (44, 25, .70), (46, 38, .86), (43, 49, .08)], .95, "capsule-right-dry", "#77746a", dry=True),
    ribbon([(28, 50, .10), (36, 55, 1.0), (44, 50, .08)], 2.4, "capsule-heat-shield", "#262522"),
    dab(37, 32, 2.4, 2.0, "#4a4943"),
    ribbon([(34, 29, .10), (38, 27, .72), (41, 30, .08)], .65, "capsule-window-glint", "#dedbd4", dry=True),
])


# The lander balances a dense cabin against spidery, unequal legs and a small
# antenna; the broken horizon gives scale without enclosing the subject.
write("lunar-lander", [
    mass("M 29 27 C 33 23 42 23 46 28 L 48 39 C 44 44 29 45 25 39 L 27 30 Z", "#4a4943"),
    ribbon([(29, 38, .12), (23, 47, .76), (16, 56, .08)], 1.8, "lander-leg-left"),
    ribbon([(44, 39, .12), (50, 48, .72), (57, 54, .08)], 1.35, "lander-leg-right", "#77746a", dry=True),
    ribbon([(16, 56, .10), (11, 57, .72), (8, 58, .08)], 1.2, "lander-foot-left"),
    ribbon([(56, 54, .10), (62, 56, .72), (65, 56, .08)], .9, "lander-foot-right", "#77746a", dry=True),
    ribbon([(36, 25, .10), (35, 17, .72), (40, 13, .08)], 1.15, "lander-antenna"),
    ribbon([(9, 62, .10), (21, 60, .70), (35, 62, .92), (51, 59, .72), (63, 61, .08)], .72, "lander-horizon", "#bcb9af", dry=True),
])


# A satellite is read by its compact bus, unequal solar wings, and antenna.
# The diagonal wing axis keeps the composition from becoming a heraldic icon.
write("satellite", [
    mass("M 33 27 L 43 30 L 46 38 L 39 46 L 29 42 L 27 34 Z", "#4a4943"),
    ribbon([(29, 34, .10), (21, 29, .74), (12, 23, .92), (7, 20, .08)], 3.0, "satellite-wing-left", "#262522"),
    ribbon([(28, 39, .10), (20, 35, .72), (11, 29, .08)], 1.05, "satellite-wing-left-dry", "#77746a", dry=True),
    ribbon([(44, 39, .10), (52, 45, .72), (62, 51, .08)], 2.1, "satellite-wing-right", "#77746a", dry=True),
    ribbon([(42, 34, .10), (51, 39, .72), (61, 44, .08)], 1.25, "satellite-wing-right-loaded", "#262522"),
    ribbon([(37, 28, .10), (39, 20, .72), (45, 15, .08)], 1.1, "satellite-antenna"),
    ribbon([(44, 15, .10), (49, 13, .72), (53, 14, .08)], .72, "satellite-dish", "#77746a", dry=True),
    ribbon([(16, 25, .10), (20, 31, .72), (22, 36, .08)], .65, "satellite-panel-rib", "#bcb9af", dry=True),
])


# The station is a long assembled habitat: a decisive truss, offset modules,
# and broad panel gestures.  No single closed outline pretends it is a capsule.
write("space-station", [
    ribbon([(11, 39, .08), (25, 37, .72), (40, 39, 1.0), (57, 36, .08)], 2.6, "station-truss"),
    ribbon([(31, 38, .10), (34, 29, .72), (36, 21, .08)], 4.4, "station-module-host", "#4a4943"),
    ribbon([(43, 38, .10), (46, 46, .72), (50, 53, .08)], 3.0, "station-module-guest", "#77746a", dry=True),
    ribbon([(22, 36, .10), (15, 28, .72), (8, 23, .08)], 3.1, "station-panel-upper", "#262522"),
    ribbon([(22, 40, .10), (15, 48, .72), (8, 54, .08)], 2.0, "station-panel-lower", "#77746a", dry=True),
    ribbon([(54, 36, .10), (61, 29, .72), (66, 26, .08)], 1.55, "station-panel-right", "#4a4943"),
    ribbon([(36, 22, .10), (41, 17, .72), (46, 17, .08)], .72, "station-docking-edge", "#bcb9af", dry=True),
])


# Rover: low chassis, three weight-bearing wheel dabs, mast, and one reaching
# arm.  Unequal wheels and a sloping ground line resist mechanical symmetry.
write("rover", [
    ribbon([(16, 43, .10), (27, 39, .76), (40, 41, 1.0), (52, 38, .08)], 5.0, "rover-chassis", "#4a4943"),
    dab(21, 51, 3.8, 3.5, "#262522"),
    dab(38, 51, 3.2, 3.0, "#4a4943"),
    dab(53, 48, 2.7, 2.6, "#77746a"),
    ribbon([(32, 39, .10), (33, 29, .72), (31, 20, .08)], 1.6, "rover-mast"),
    ribbon([(29, 20, .10), (35, 17, .72), (41, 19, .08)], 1.4, "rover-camera", "#262522"),
    ribbon([(49, 39, .10), (58, 31, .72), (64, 29, .08)], 1.25, "rover-arm", "#77746a", dry=True),
    ribbon([(10, 57, .10), (23, 55, .72), (39, 57, .90), (58, 53, .08)], .72, "rover-ground", "#bcb9af", dry=True),
])


# Mission control is human work rather than another spacecraft: a sweeping
# console hosts three uneven figures and a dry trajectory rises behind them.
write("mission-control", [
    ribbon([(10, 49, .10), (23, 44, .72), (38, 46, 1.0), (55, 42, .08)], 4.2, "control-console", "#4a4943"),
    dab(22, 33, 2.7, 2.9, "#262522"),
    ribbon([(22, 36, .10), (21, 42, .72), (23, 46, .08)], 2.0, "control-person-left"),
    dab(37, 30, 2.4, 2.6, "#4a4943"),
    ribbon([(37, 33, .10), (38, 39, .72), (38, 45, .08)], 1.65, "control-person-center", "#4a4943"),
    dab(51, 34, 2.1, 2.3, "#77746a"),
    ribbon([(51, 36, .10), (50, 40, .72), (51, 43, .08)], 1.2, "control-person-right", "#77746a", dry=True),
    ribbon([(14, 22, .10), (27, 16, .68), (40, 18, .90), (51, 12, .08)], 1.15, "control-trajectory", "#77746a", dry=True),
    ribbon([(48, 12, .10), (55, 11, .72), (59, 15, .08)], .72, "control-target", "#bcb9af", dry=True),
])


print("redrew all 10 rocket PUA glyphs as naturalist sumi-e machine studies")
