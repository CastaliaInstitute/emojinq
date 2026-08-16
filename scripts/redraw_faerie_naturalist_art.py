#!/usr/bin/env python3
"""Redraw faerie PUA glyphs as distinct pose-led sumi-e figures."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "faerie"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", *, dry=False) -> str:
    d = stroke_path(
        points(*values), width=width, seed=seed, wobble=.25,
        taper_start=.10, taper_end=.08,
    )
    class_name = "ink-dry" if dry else "ink-wash"
    brush_pass = "dry-edge-v2" if dry else "loaded-ribbon-v2"
    return (
        f'<path class="{class_name}" d="{d}" fill="{color}" '
        f'data-ink-brush-pass="{brush_pass}"/>'
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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="faerie / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>faerie / {name} — naturalist sumi-e gesture study</title>{''.join(marks)}</svg>
''')


# Hover: a suspended vertical body, wide beating wings, and feet that do not
# meet the ground.  The unequal wing loads prevent heraldic symmetry.
write("hover", [
    dab(36, 18, 3.0, 3.2),
    ribbon([(36, 22, .10), (35, 31, .84), (37, 42, 1.0), (36, 50, .08)], 3.4, "hover-body", "#4a4943"),
    ribbon([(34, 28, .10), (24, 20, .74), (11, 17, .08)], 2.6, "hover-wing-upper-left"),
    ribbon([(38, 29, .10), (49, 22, .72), (63, 20, .08)], 1.8, "hover-wing-upper-right", "#77746a", dry=True),
    ribbon([(34, 34, .10), (23, 39, .72), (12, 47, .08)], 1.9, "hover-wing-lower-left", "#4a4943"),
    ribbon([(38, 35, .10), (49, 40, .72), (61, 47, .08)], 1.15, "hover-wing-lower-right", "#77746a", dry=True),
    ribbon([(34, 48, .10), (31, 56, .72), (28, 62, .08)], 1.25, "hover-leg-left"),
    ribbon([(38, 48, .10), (42, 56, .72), (44, 62, .08)], .90, "hover-leg-right", "#bcb9af", dry=True),
])


# Reach: the whole figure leans into one long lifted arm; wings counterbalance
# behind rather than repeating the hover silhouette.
write("reach", [
    dab(30, 24, 2.8, 3.0),
    ribbon([(31, 27, .10), (36, 35, .84), (43, 43, .08)], 3.1, "reach-body", "#4a4943"),
    ribbon([(34, 31, .10), (45, 26, .72), (57, 18, .94), (65, 12, .08)], 1.8, "reach-arm"),
    ribbon([(30, 31, .10), (19, 25, .72), (8, 23, .08)], 2.5, "reach-wing-upper"),
    ribbon([(33, 35, .10), (21, 39, .72), (10, 47, .08)], 1.35, "reach-wing-lower", "#77746a", dry=True),
    ribbon([(42, 42, .10), (47, 51, .72), (54, 57, .08)], 1.5, "reach-leg-forward"),
    ribbon([(39, 43, .10), (36, 53, .72), (33, 61, .08)], 1.05, "reach-leg-back", "#77746a", dry=True),
    ribbon([(64, 12, .10), (67, 9, .72), (69, 8, .08)], .65, "reach-tip", "#bcb9af", dry=True),
])


# Dart: a horizontal body and swept-back wings make speed intrinsic to the
# silhouette.  A pair of dry wake marks replaces an arrow symbol.
write("dart", [
    dab(51, 32, 2.8, 2.7),
    ribbon([(48, 34, .10), (39, 35, .82), (29, 38, 1.0), (20, 41, .08)], 3.5, "dart-body", "#4a4943"),
    ribbon([(38, 35, .10), (27, 25, .72), (15, 18, .08)], 2.3, "dart-wing-upper"),
    ribbon([(35, 38, .10), (24, 44, .72), (12, 51, .08)], 1.65, "dart-wing-lower", "#77746a", dry=True),
    ribbon([(50, 34, .10), (59, 36, .72), (66, 34, .08)], 1.25, "dart-arm"),
    ribbon([(22, 41, .10), (14, 45, .72), (8, 48, .08)], 1.2, "dart-leg", "#4a4943"),
    ribbon([(11, 31, .10), (18, 32, .72), (24, 33, .08)], .72, "dart-wake-high", "#bcb9af", dry=True),
    ribbon([(7, 57, .10), (15, 53, .72), (22, 50, .08)], .65, "dart-wake-low", "#77746a", dry=True),
])


# Alight: a steep descending body, high braking wings, and one foot meeting a
# branch distinguish landing from hovering.
write("alight", [
    dab(40, 22, 2.8, 3.0),
    ribbon([(39, 25, .10), (35, 34, .82), (31, 45, 1.0), (27, 54, .08)], 3.2, "alight-body", "#4a4943"),
    ribbon([(37, 30, .10), (27, 21, .72), (16, 12, .08)], 2.4, "alight-wing-left"),
    ribbon([(40, 30, .10), (49, 19, .72), (57, 10, .08)], 1.55, "alight-wing-right", "#77746a", dry=True),
    ribbon([(30, 49, .10), (25, 57, .72), (22, 62, .08)], 1.5, "alight-leg-touch"),
    ribbon([(32, 47, .10), (37, 54, .72), (42, 57, .08)], 1.0, "alight-leg-lift", "#77746a", dry=True),
    ribbon([(12, 63, .10), (25, 62, .82), (40, 64, .08)], 1.25, "alight-branch"),
    ribbon([(35, 32, .10), (29, 36, .72), (23, 39, .08)], .72, "alight-wing-edge", "#bcb9af", dry=True),
])


# Dance: an upright S-curve, one lifted knee, and opposing arms.  Wings are
# short guests so the human movement remains the host.
write("dance", [
    dab(35, 15, 2.8, 3.0),
    ribbon([(35, 18, .10), (31, 28, .80), (36, 38, 1.0), (33, 47, .08)], 3.0, "dance-body", "#4a4943"),
    ribbon([(32, 27, .10), (23, 24, .72), (16, 18, .08)], 1.45, "dance-arm-left"),
    ribbon([(36, 27, .10), (45, 21, .72), (52, 14, .08)], 1.75, "dance-arm-right"),
    ribbon([(32, 31, .10), (23, 34, .72), (15, 41, .08)], 1.5, "dance-wing-left", "#77746a", dry=True),
    ribbon([(37, 32, .10), (47, 34, .72), (57, 39, .08)], 1.15, "dance-wing-right", "#bcb9af", dry=True),
    ribbon([(33, 46, .10), (27, 55, .72), (22, 62, .08)], 1.5, "dance-leg-ground"),
    ribbon([(35, 46, .10), (43, 49, .82), (51, 45, .08)], 1.65, "dance-leg-lift"),
    ribbon([(10, 63, .10), (21, 61, .72), (31, 62, .08)], .65, "dance-ground", "#77746a", dry=True),
])


# Bow: head and torso fold forward while wings close vertically behind.  Both
# legs remain grounded, giving it a compact, unmistakably deferential stance.
write("bow", [
    dab(46, 31, 2.8, 2.8),
    ribbon([(44, 32, .10), (36, 34, .80), (29, 40, 1.0), (27, 49, .08)], 3.2, "bow-body", "#4a4943"),
    ribbon([(34, 35, .10), (29, 22, .72), (27, 10, .08)], 2.2, "bow-wing-high"),
    ribbon([(31, 37, .10), (22, 28, .72), (15, 19, .08)], 1.35, "bow-wing-low", "#77746a", dry=True),
    ribbon([(42, 34, .10), (51, 38, .72), (58, 43, .08)], 1.25, "bow-arm"),
    ribbon([(27, 47, .10), (23, 56, .72), (20, 62, .08)], 1.5, "bow-leg-left"),
    ribbon([(30, 48, .10), (35, 56, .72), (40, 61, .08)], 1.1, "bow-leg-right", "#77746a", dry=True),
    ribbon([(15, 63, .10), (28, 62, .72), (43, 63, .08)], .65, "bow-ground", "#bcb9af", dry=True),
])


# Carry: two arms cradle a visible seed while the body rises diagonally.  The
# rear wing is dry, making the carried object the second visual weight.
write("carry", [
    dab(30, 20, 2.8, 3.0),
    ribbon([(31, 23, .10), (35, 32, .82), (40, 42, 1.0), (45, 51, .08)], 3.2, "carry-body", "#4a4943"),
    ribbon([(33, 30, .10), (42, 28, .72), (49, 31, .08)], 1.45, "carry-arm-upper"),
    ribbon([(35, 34, .10), (43, 37, .72), (50, 33, .08)], 1.2, "carry-arm-lower", "#77746a", dry=True),
    dab(52, 32, 3.1, 2.6, "#262522"),
    ribbon([(32, 30, .10), (21, 22, .72), (10, 18, .08)], 2.4, "carry-wing-upper"),
    ribbon([(35, 35, .10), (23, 39, .72), (13, 47, .08)], 1.35, "carry-wing-lower", "#77746a", dry=True),
    ribbon([(44, 49, .10), (39, 57, .72), (35, 63, .08)], 1.35, "carry-leg-a"),
    ribbon([(46, 49, .10), (52, 55, .72), (58, 58, .08)], .9, "carry-leg-b", "#bcb9af", dry=True),
])


# Spin: a compact turning body sits inside one incomplete circular sweep; wings
# and limbs radiate at different angles rather than forming another standing pose.
write("spin", [
    dab(36, 26, 2.8, 2.8),
    ribbon([(36, 29, .10), (40, 36, .82), (36, 44, 1.0), (31, 49, .08)], 3.1, "spin-body", "#4a4943"),
    ribbon([(35, 32, .10), (24, 29, .72), (13, 23, .08)], 2.1, "spin-wing-a"),
    ribbon([(39, 33, .10), (49, 28, .72), (59, 23, .08)], 1.4, "spin-wing-b", "#77746a", dry=True),
    ribbon([(34, 40, .10), (23, 44, .72), (14, 51, .08)], 1.2, "spin-leg-a"),
    ribbon([(38, 42, .10), (48, 46, .72), (58, 51, .08)], 1.5, "spin-leg-b"),
    ribbon([(14, 55, .10), (8, 43, .66), (10, 29, .86), (20, 17, .78), (34, 11, .90), (50, 15, .72), (62, 27, .08)], 1.1, "spin-orbit", "#77746a", dry=True),
    ribbon([(58, 17, .10), (63, 23, .72), (64, 30, .08)], .65, "spin-orbit-lift", "#bcb9af", dry=True),
])


# Spring: a low kneeling figure tends a new shoot.  Wings echo opening leaves.
write("season-spring", [
    dab(28, 27, 2.7, 2.8),
    ribbon([(29, 30, .10), (34, 37, .82), (39, 44, .08)], 3.0, "spring-body", "#4a4943"),
    ribbon([(31, 34, .10), (22, 29, .72), (14, 24, .08)], 2.0, "spring-wing-leaf-a"),
    ribbon([(34, 36, .10), (25, 40, .72), (17, 47, .08)], 1.25, "spring-wing-leaf-b", "#77746a", dry=True),
    ribbon([(38, 42, .10), (32, 49, .72), (25, 52, .08)], 1.4, "spring-kneel"),
    ribbon([(36, 37, .10), (45, 40, .72), (52, 45, .08)], 1.15, "spring-arm", "#77746a", dry=True),
    ribbon([(55, 56, .10), (55, 48, .72), (55, 41, .08)], 1.15, "spring-stem"),
    ribbon([(55, 46, .10), (49, 43, .72), (45, 44, .08)], 1.7, "spring-leaf-left", "#4a4943"),
    ribbon([(55, 48, .10), (61, 44, .72), (65, 45, .08)], 1.3, "spring-leaf-right", "#77746a", dry=True),
])


# Summer: an open, rising pose answers a small sun.  Wings point upward like
# heated air rather than using the horizontal hover arrangement.
write("season-summer", [
    dab(34, 26, 2.8, 3.0),
    ribbon([(34, 29, .10), (36, 38, .82), (34, 49, .08)], 3.1, "summer-body", "#4a4943"),
    ribbon([(33, 33, .10), (25, 23, .72), (20, 13, .08)], 2.1, "summer-wing-left"),
    ribbon([(37, 33, .10), (45, 22, .72), (49, 12, .08)], 1.4, "summer-wing-right", "#77746a", dry=True),
    ribbon([(36, 34, .10), (45, 31, .72), (53, 25, .08)], 1.55, "summer-arm"),
    dab(59, 19, 3.0, 3.0, "#262522"),
    ribbon([(33, 48, .10), (28, 57, .72), (24, 63, .08)], 1.4, "summer-leg-a"),
    ribbon([(36, 48, .10), (42, 56, .72), (47, 61, .08)], .95, "summer-leg-b", "#bcb9af", dry=True),
    ribbon([(58, 13, .10), (58, 9, .72), (58, 6, .08)], .65, "summer-ray", "#77746a", dry=True),
])


# Autumn: the pose pitches with wind while one hand releases a falling leaf.
# Long rear wings share the leaf's downward diagonal.
write("season-autumn", [
    dab(38, 23, 2.8, 2.9),
    ribbon([(37, 26, .10), (32, 35, .82), (27, 45, .08)], 3.1, "autumn-body", "#4a4943"),
    ribbon([(35, 31, .10), (24, 24, .72), (12, 20, .08)], 2.3, "autumn-wing-upper"),
    ribbon([(32, 36, .10), (21, 42, .72), (10, 50, .08)], 1.4, "autumn-wing-lower", "#77746a", dry=True),
    ribbon([(36, 31, .10), (46, 35, .72), (55, 40, .08)], 1.35, "autumn-arm"),
    ribbon([(27, 44, .10), (22, 53, .72), (18, 60, .08)], 1.35, "autumn-leg-a"),
    ribbon([(29, 44, .10), (35, 52, .72), (42, 57, .08)], .95, "autumn-leg-b", "#bcb9af", dry=True),
    ribbon([(58, 42, .10), (63, 46, .82), (59, 51, .08)], 2.0, "autumn-leaf", "#4a4943"),
    ribbon([(57, 54, .10), (60, 58, .72), (58, 62, .08)], .65, "autumn-leaf-fall", "#77746a", dry=True),
])


# Winter: a curled body and folded wings conserve warmth; three dry flakes hold
# the cold field around it without turning the figure into a snowflake icon.
write("season-winter", [
    dab(37, 25, 2.8, 2.9),
    ribbon([(36, 28, .10), (31, 35, .82), (33, 43, 1.0), (40, 47, .08)], 3.2, "winter-curled-body", "#4a4943"),
    ribbon([(34, 32, .10), (25, 27, .72), (17, 20, .08)], 1.8, "winter-folded-wing-a"),
    ribbon([(33, 36, .10), (24, 39, .72), (16, 45, .08)], 1.2, "winter-folded-wing-b", "#77746a", dry=True),
    ribbon([(39, 46, .10), (46, 50, .72), (52, 50, .08)], 1.3, "winter-knees"),
    ribbon([(40, 31, .10), (46, 36, .72), (49, 42, .08)], .95, "winter-arm", "#bcb9af", dry=True),
    ribbon([(56, 18, .10), (61, 18, .72), (65, 18, .08)], .72, "winter-flake-a", "#77746a", dry=True),
    ribbon([(61, 13, .10), (61, 18, .72), (61, 23, .08)], .72, "winter-flake-b", "#77746a", dry=True),
    ribbon([(12, 55, .10), (17, 57, .72), (22, 56, .08)], .65, "winter-drift", "#bcb9af", dry=True),
])


# Dew drop: a compact teardrop outline with a broad paper highlight.  Keeping
# the point, rounded water weight, and reflected-light crescent legible at 32px
# matters more than making the drop a single heavy ink mass.
write("dew-drop", [
    '<path class="ink-wash" d="M36 10 C32 19 23 30 23 43 C23 53 28 60 36 62 C44 60 49 53 49 43 C49 31 41 20 36 10 Z" fill="#4a4943" data-ink-brush-pass="loaded-mass-v1"/>',
    '<path class="ink-dry" d="M30 32 C27 39 27 48 32 53 C34 55 35 53 33 51 C30 46 30 39 33 34 C35 30 32 28 30 32 Z" fill="#eeeeea" opacity=".9" data-ink-brush-pass="reserved-paper-v1"/>',
    '<path class="ink-dry" d="M43 39 C45 47 42 54 37 57" fill="none" stroke="#77746a" stroke-width="1.5" stroke-linecap="round" opacity=".68" data-ink-brush-pass="dry-edge-v2"/>',
])


print("redrew 12 faerie gestures and the dew-drop as distinct naturalist brush studies")
