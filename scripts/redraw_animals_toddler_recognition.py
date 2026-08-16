#!/usr/bin/env python3
"""Draw the animal PUA set as bold, toddler-readable sumi-e studies.

The earlier anatomy-derived line drawings became pale diagrams at 32px.  This
pass makes each referent depend on the animal cue a young child is most likely
to name: cow muzzle and udder, lamb wool, wolf ears and tail, rabbit ears and
haunch, squirrel tail, bee stripes, flying wings, and repeated herd/pack forms.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "animals"

# Preserve the full identifying silhouettes while keeping the ink field below
# the family's 20% negative-space ceiling.  Dense subjects receive slightly
# more breathing room than the naturally sparse group-flight studies.
COMPOSITION_SCALE = {
    "calf": .88,
    "herd": .90,
    "lamb": .90,
    "pack": .90,
    "predator": .87,
    "prey": .90,
    "squirrel": .80,
}


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", wobble=.28, dry=False) -> str:
    return svg_path(
        stroke_path(points(*values), width=max(width, 1.15), seed=seed, wobble=wobble),
        fill=color,
        class_name="ink-dry" if dry else "ink-wash",
    )


def mass(d: str, color="#3f3e39", role="ink-wash") -> str:
    return f'<path class="{role}" fill="{color}" d="{d}" data-ink-brush-pass="loaded-mass-v2"/>'


def dab(cx: float, cy: float, rx: float, ry: float, color="#262522", role="ink-wash") -> str:
    return (
        f'<ellipse class="{role}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" '
        f'fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'
    )


def group(transform: str, marks: list[str]) -> str:
    return f'<g transform="{transform}">{"".join(marks)}</g>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text(encoding="utf-8")
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    artwork = ''.join(marks)
    if name in COMPOSITION_SCALE:
        scale = COMPOSITION_SCALE[name]
        artwork = f'<g transform="translate(36 36) scale({scale}) translate(-36 -36)">{artwork}</g>'
    target.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="animals / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>animals / {name} — recognizable naturalist sumi-e study</title>{artwork}</svg>
''',
        encoding="utf-8",
    )


GROUND = ribbon([(8, 62, .08), (25, 60, .72), (45, 62, .58), (65, 59, .08)], 1.3, "animals-ground", "#77746a", .35, True)


def cow_marks() -> list[str]:
    return [
        mass("M 17 29 C 24 25 40 25 49 29 C 53 33 52 42 47 46 C 37 49 24 48 17 43 C 13 39 13 33 17 29 Z", "#4a4943"),
        mass("M 47 28 C 52 24 59 25 62 29 L 64 37 C 61 42 53 43 48 39 Z", "#262522"),
        mass("M 49 27 L 47 20 L 53 25 Z M 59 26 L 64 21 L 63 29 Z", "#262522"),
        mass("M 53 35 C 56 33 61 34 64 36 C 63 40 58 41 54 39 Z", "#77746a", "ink-dry"),
        mass("M 18 43 L 23 43 L 22 58 L 17 58 Z M 31 46 L 36 46 L 36 59 L 31 59 Z M 43 44 L 48 43 L 50 58 L 45 58 Z", "#3a3935"),
        mass("M 27 45 C 31 43 37 44 40 47 C 39 51 36 53 33 51 C 31 53 28 51 27 48 Z", "#77746a", "ink-dry"),
        ribbon([(17, 31, .10), (11, 27, .75), (9, 21, .08)], 1.7, "calf-tail", "#262522", .32),
        dab(9, 20, 1.8, 2.0, "#262522"),
        dab(58, 30, 1.1, 1.1, "#f3f0e6", "ink-dry"),
        mass("M 25 29 C 29 27 34 28 36 31 C 34 35 29 36 25 33 Z", "#77746a", "ink-dry"),
    ]


write("calf", cow_marks() + [GROUND])


write("lamb", [
    mass("M 17 34 C 14 28 20 23 26 25 C 29 19 37 21 39 25 C 45 21 51 26 49 32 C 55 35 52 43 47 44 C 44 51 35 50 32 46 C 26 51 18 47 19 42 C 14 41 13 37 17 34 Z", "#77746a", "ink-dry"),
    mass("M 47 29 C 53 26 60 29 61 35 C 62 41 57 45 51 43 L 46 39 Z", "#262522"),
    mass("M 49 29 L 48 23 L 54 28 Z M 57 29 L 63 26 L 60 33 Z", "#262522"),
    mass("M 23 44 L 28 44 L 27 59 L 22 59 Z M 40 45 L 45 44 L 47 59 L 42 59 Z", "#3f3e39"),
    dab(56, 34, 1.1, 1.1, "#f3f0e6", "ink-dry"),
    ribbon([(18, 35, .10), (13, 32, .72), (11, 29, .08)], 1.8, "lamb-tail", "#4a4943", .32),
    GROUND,
])


write("predator", [
    mass("M 14 35 C 22 28 36 27 47 32 C 53 35 55 42 50 46 C 40 50 25 49 17 44 C 13 42 11 38 14 35 Z", "#3f3e39"),
    mass("M 45 31 C 49 25 56 23 62 27 L 67 33 L 62 38 L 52 38 Z", "#262522"),
    mass("M 49 27 L 48 18 L 56 24 Z M 57 24 L 63 18 L 63 28 Z", "#262522"),
    mass("M 62 31 L 69 33 L 62 36 Z", "#77746a", "ink-dry"),
    mass("M 18 43 L 24 44 L 22 59 L 17 59 Z M 32 46 L 38 46 L 38 59 L 32 59 Z M 46 44 L 51 42 L 54 57 L 49 58 Z", "#262522"),
    ribbon([(15, 36, .10), (9, 29, .75), (8, 20, .90), (13, 15, .08)], 3.3, "wolf-tail", "#4a4943", .40),
    dab(59, 28, 1.0, 1.0, "#f3f0e6", "ink-dry"),
    ribbon([(24, 33, .10), (34, 31, .75), (45, 34, .08)], 1.2, "wolf-back-light", "#77746a", .26, True),
    GROUND,
])


write("prey", [
    mass("M 24 39 C 28 30 41 28 50 35 C 57 41 55 51 47 55 C 37 60 24 55 21 48 C 19 44 20 41 24 39 Z", "#4a4943"),
    mass("M 18 35 C 17 29 21 25 27 25 C 33 26 35 31 32 37 L 25 41 Z", "#262522"),
    mass("M 20 27 C 15 20 15 10 19 8 C 23 13 25 21 24 27 Z M 25 26 C 23 18 27 9 31 8 C 33 15 31 23 29 28 Z", "#3f3e39"),
    dab(54, 40, 4.0, 4.0, "#77746a", "ink-dry"),
    dab(25, 29, 1.0, 1.0, "#f3f0e6", "ink-dry"),
    mass("M 31 50 C 38 48 47 50 51 55 C 45 58 37 59 31 56 Z", "#262522"),
    ribbon([(23, 57, .10), (37, 59, .72), (52, 57, .08)], 1.4, "rabbit-ground", "#77746a", .30, True),
])


write("squirrel", [
    mass("M 21 39 C 24 30 35 27 44 32 C 52 37 51 49 43 55 C 34 60 22 55 19 48 C 17 44 18 41 21 39 Z", "#4a4943"),
    mass("M 15 37 C 11 33 13 27 18 25 C 23 23 29 26 30 31 C 29 36 23 39 17 40 Z", "#262522"),
    mass("M 19 25 L 22 18 L 26 27 Z", "#262522"),
    mass("M 42 40 C 49 38 56 32 56 25 C 56 20 52 17 49 18 C 46 20 49 24 52 27 C 51 32 46 35 41 36 C 35 32 36 24 42 18 C 49 10 60 14 63 23 C 67 36 57 48 46 51 Z", "#77746a", "ink-dry"),
    mass("M 27 37 C 31 35 35 37 36 40 C 34 44 31 46 28 44 Z", "#262522"),
    mass("M 24 51 C 29 49 35 51 38 56 C 33 59 26 59 22 56 Z", "#262522"),
    dab(21, 29, 1.0, 1.0, "#f3f0e6", "ink-dry"),
    ribbon([(48, 19, .12), (56, 24, .78), (55, 34, .58), (48, 41, .08)], 1.3, "squirrel-tail-fold", "#4a4943", .34, True),
    GROUND,
])


def bee(transform: str) -> str:
    return group(transform, [
        dab(0, 0, 7.2, 4.0, "#3f3e39"),
        mass("M -3 -2 C -10 -10 -15 -7 -11 -1 C -8 2 -5 2 -2 1 Z M 2 -2 C 7 -10 14 -7 11 -1 C 8 2 5 2 2 1 Z", "#77746a", "ink-dry"),
        mass("M -3 -4 L -1 4 L 1 4 L -1 -4 Z M 2 -4 L 4 3 L 6 2 L 4 -4 Z", "#262522"),
        mass("M 7 -1 L 12 -3 L 9 1 L 12 3 L 7 1 Z", "#262522"),
    ])


write("colony", [
    mass("M 9 47 C 10 38 17 32 26 32 C 35 32 42 39 42 48 L 39 58 L 12 58 Z", "#77746a", "ink-dry"),
    ribbon([(12, 42, .12), (25, 39, .80), (39, 43, .08)], 1.4, "hive-ring-one", "#4a4943", .24),
    ribbon([(11, 49, .12), (25, 47, .80), (40, 50, .08)], 1.4, "hive-ring-two", "#4a4943", .24),
    bee("translate(24 20) scale(.70) rotate(-12)"),
    bee("translate(48 25) scale(.62) rotate(14)"),
    bee("translate(55 43) scale(.52) rotate(-8)"),
    GROUND,
])


def flying_bird(transform: str, shade="#3f3e39") -> str:
    return group(transform, [
        mass("M -2 0 C -10 -10 -18 -10 -22 -5 C -15 -4 -9 0 -4 5 C -2 3 -1 2 0 1 C 6 -5 13 -7 20 -4 C 14 -1 9 4 5 9 C 2 6 0 3 -2 0 Z", shade),
        mass("M 3 0 C 8 -1 12 0 15 2 L 21 3 L 15 5 C 10 5 6 4 3 2 Z", "#262522"),
    ])


write("flock", [
    flying_bird("translate(28 27) scale(.72) rotate(-8)"),
    flying_bird("translate(48 42) scale(.58) rotate(7)", "#4a4943"),
    flying_bird("translate(18 48) scale(.46) rotate(-5)", "#77746a"),
    ribbon([(8, 58, .08), (26, 53, .70), (48, 51, .45), (65, 45, .08)], 1.2, "flock-air", "#77746a", .38, True),
])


write("migration", [
    flying_bird("translate(36 18) scale(.48)"),
    flying_bird("translate(24 30) scale(.43) rotate(-5)", "#4a4943"),
    flying_bird("translate(49 31) scale(.43) rotate(5)", "#4a4943"),
    flying_bird("translate(14 43) scale(.36) rotate(-7)", "#77746a"),
    flying_bird("translate(59 44) scale(.36) rotate(7)", "#77746a"),
    ribbon([(8, 56, .08), (28, 50, .68), (47, 52, .46), (65, 48, .08)], 1.2, "migration-wind", "#77746a", .36, True),
])


mini_cow = cow_marks()[:-3]
write("herd", [
    group("translate(-2 18) scale(.68)", mini_cow),
    group("translate(27 6) scale(.68)", mini_cow),
    ribbon([(7, 62, .08), (29, 59, .72), (51, 61, .48), (66, 58, .08)], 1.4, "herd-ground", "#77746a", .34, True),
])


def wolf_face(transform: str, shade="#3f3e39") -> str:
    return group(transform, [
        mass("M -10 -5 L -9 -17 L -2 -10 C 3 -12 8 -9 10 -5 L 17 0 L 10 7 C 7 13 -5 14 -11 8 C -16 4 -16 -1 -10 -5 Z", shade),
        mass("M 1 -10 L 8 -18 L 10 -5 Z", "#262522"),
        mass("M 7 0 L 18 1 L 10 6 L 4 5 Z", "#77746a", "ink-dry"),
        dab(4, -4, 1.2, 1.2, "#f3f0e6", "ink-dry"),
    ])


write("pack", [
    wolf_face("translate(19 42) scale(.78)", "#4a4943"),
    wolf_face("translate(39 28) scale(.92)", "#262522"),
    wolf_face("translate(56 45) scale(.66)", "#77746a"),
    GROUND,
])


print("redrew 10 animal glyphs for toddler recognition")
