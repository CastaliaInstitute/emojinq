#!/usr/bin/env python3
"""Redraw the four small story-world PUA families for 32px recognition."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"

COMPOSITION_SCALE = {
    ("adventure", "emerald"): .78,
    ("adventure", "gold-nugget"): .90,
    ("adventure", "silver-chest"): .70,
    ("brc", "art-car"): .90,
    ("brc", "temple"): .70,
    ("castalia", "judy-torso"): .82,
    ("castalia", "maker-seal"): .94,
    ("castalia", "mermaid-guide"): .88,
    ("castalia", "pirate-ship"): .90,
    ("castalia", "police-box"): .68,
    ("castalia", "punch-torso"): .82,
    ("castalia", "puppet-left-hand"): .89,
    ("castalia", "puppet-right-hand"): .89,
    ("castalia", "puppet-shoe"): .88,
    ("castalia", "research-submarine"): .80,
    ("castalia", "rook-flame"): .86,
    ("cave_locations", "bird-chamber"): .91,
    ("cave_locations", "castalia-rook-flame"): .96,
    ("cave_locations", "debris-room"): .94,
    ("cave_locations", "outside-grate"): .84,
    ("cave_locations", "plover-room"): .90,
}

# Two rooms lean toward their landmark, avoiding a row of mechanically centered
# cave badges while retaining safe margins.
COMPOSITION_OFFSET = {
    ("cave_locations", "debris-room"): 3,
    ("cave_locations", "plover-room"): -3,
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


def contour(d: str, color="#77746a", width=1.6) -> str:
    return (
        f'<path class="ink-dry" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" d="{d}" data-ink-brush-pass="dry-contour-v2"/>'
    )


def dab(cx, cy, rx, ry, color="#262522", role="ink-wash") -> str:
    return f'<ellipse class="{role}" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def group(transform: str, marks: list[str]) -> str:
    return f'<g transform="{transform}">{"".join(marks)}</g>'


def write(category: str, name: str, marks: list[str]) -> None:
    target = PUA / category / f"{name}.svg"
    source = target.read_text(encoding="utf-8")
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    artwork = ''.join(marks)
    key = (category, name)
    scale = COMPOSITION_SCALE.get(key, 1.0)
    offset = COMPOSITION_OFFSET.get(key, 0)
    if scale != 1.0 or offset:
        artwork = f'<g transform="translate({offset} 0) translate(36 36) scale({scale}) translate(-36 -36)">{artwork}</g>'
    target.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="{category} / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>{category} / {name} — recognizable sumi-e story study</title>{artwork}</svg>
''', encoding="utf-8")


GROUND = contour("M 8 62 C 24 59 43 63 65 59", "#77746a", 1.2)


# Adventure objects ---------------------------------------------------------
write("adventure", "black-rod", [
    ribbon([(13, 58, .08), (27, 44, .72), (43, 29, .98), (59, 13, .08)], 4.0, "black-rod-host", "#262522", .32),
    ribbon([(18, 56, .10), (33, 42, .72), (50, 25, .08)], 1.2, "black-rod-dry", "#77746a", .30, True),
    dab(60, 12, 3.0, 3.0, "#262522"),
])

write("adventure", "brass-lamp", [
    mass("M 19 39 C 26 34 42 34 49 39 C 48 48 42 54 33 54 C 25 54 20 49 19 39 Z", "#4a4943"),
    mass("M 47 38 C 53 36 59 31 65 27 C 62 36 55 43 47 45 Z", "#262522"),
    contour("M 21 40 C 11 35 9 48 17 51 C 22 53 25 49 25 46", "#77746a", 2.4),
    ribbon([(28, 34, .10), (35, 28, .72), (45, 29, .08)], 2.0, "lamp-lid", "#262522", .28),
    dab(36, 27, 2.0, 1.4, "#262522"),
    ribbon([(25, 55, .10), (34, 57, .74), (45, 54, .08)], 2.0, "lamp-foot", "#77746a", .28, True),
])

write("adventure", "emerald", [
    mass("M 36 9 L 58 27 L 52 53 L 36 64 L 19 52 L 14 27 Z", "#77746a", "ink-dry"),
    contour("M 36 9 L 44 28 L 36 64 M 14 27 L 44 28 L 52 53 M 58 27 L 28 29 L 19 52", "#262522", 1.8),
    mass("M 28 29 L 44 28 L 36 58 Z", "#4a4943"),
])

write("adventure", "gold-nugget", [
    mass("M 14 43 C 13 33 22 27 30 29 C 35 21 47 25 48 32 C 59 32 63 44 56 51 C 47 58 25 57 17 51 Z", "#4a4943"),
    mass("M 23 34 C 28 28 37 29 39 34 C 35 39 27 41 22 38 Z M 43 38 C 48 34 54 37 55 42 C 51 46 45 46 42 43 Z", "#77746a", "ink-dry"),
    GROUND,
])

write("adventure", "keys", [
    contour("M 21 16 C 12 16 9 27 15 33 C 21 39 32 34 32 25 C 32 19 27 16 21 16 Z", "#262522", 3.0),
    ribbon([(28, 32, .10), (39, 43, .78), (55, 58, .08)], 3.2, "key-one-shaft", "#262522", .25),
    mass("M 50 52 L 59 52 L 59 58 L 55 58 L 55 63 L 49 58 Z", "#262522"),
    contour("M 49 15 C 41 15 38 24 43 29 C 48 34 57 31 58 24 C 58 18 54 15 49 15 Z", "#77746a", 2.6),
    ribbon([(46, 30, .10), (39, 41, .72), (31, 55, .08)], 2.4, "key-two-shaft", "#77746a", .25, True),
    mass("M 27 52 L 35 52 L 34 58 L 30 58 L 30 62 L 25 58 Z", "#77746a", "ink-dry"),
])

write("adventure", "little-bird", [
    mass("M 18 39 C 22 29 35 26 44 31 C 51 35 51 45 44 50 C 35 56 22 52 18 44 Z", "#4a4943"),
    mass("M 39 31 C 44 25 52 25 56 30 C 59 34 57 39 52 41 L 44 39 Z", "#262522"),
    mass("M 56 31 L 66 34 L 56 37 Z", "#77746a", "ink-dry"),
    mass("M 24 38 C 31 32 40 35 43 41 C 37 47 29 48 23 44 Z", "#77746a", "ink-dry"),
    ribbon([(20, 43, .10), (13, 39, .72), (8, 36, .08)], 2.2, "bird-tail", "#262522", .30),
    dab(51, 30, 1.1, 1.1, "#f3f0e6", "ink-dry"),
    contour("M 31 51 L 29 59 M 38 51 L 40 59", "#262522", 1.5),
    GROUND,
])

write("adventure", "silver-chest", [
    mass("M 13 28 C 18 16 53 16 59 28 L 59 35 L 13 35 Z", "#77746a", "ink-dry"),
    mass("M 11 34 L 61 34 L 58 59 L 14 59 Z", "#4a4943"),
    contour("M 14 37 L 59 37 M 23 34 L 21 58 M 50 34 L 52 58", "#b2afa6", 1.4),
    mass("M 31 39 L 42 39 L 42 49 L 38 49 L 38 55 L 34 55 L 34 49 L 31 49 Z", "#262522"),
    GROUND,
])


# BRC referents -------------------------------------------------------------
write("brc", "art-car", [
    mass("M 12 38 C 20 30 47 29 57 38 L 62 49 L 9 49 Z", "#4a4943"),
    mass("M 25 28 C 30 21 42 21 48 29 Z", "#77746a", "ink-dry"),
    dab(20, 52, 5.5, 5.5, "#262522"), dab(51, 52, 5.5, 5.5, "#262522"),
    ribbon([(35, 24, .10), (33, 15, .72), (27, 9, .08)], 1.5, "art-car-flag-mast", "#262522", .28),
    mass("M 27 8 L 44 12 L 29 18 Z", "#77746a", "ink-dry"),
    contour("M 14 41 C 27 35 44 37 58 42", "#b2afa6", 1.2),
    GROUND,
])

write("brc", "man", [
    dab(36, 15, 6.0, 6.3, "#262522"),
    mass("M 29 23 C 33 20 40 21 43 24 L 45 43 C 41 48 32 48 28 43 Z", "#4a4943"),
    ribbon([(30, 27, .10), (20, 35, .72), (12, 43, .08)], 3.0, "man-left-arm", "#262522", .30),
    ribbon([(42, 27, .10), (51, 35, .72), (60, 42, .08)], 2.4, "man-right-arm", "#77746a", .30, True),
    ribbon([(33, 44, .10), (29, 54, .72), (24, 64, .08)], 3.2, "man-left-leg", "#262522", .30),
    ribbon([(39, 44, .10), (44, 54, .72), (50, 63, .08)], 2.7, "man-right-leg", "#4a4943", .30),
])

write("brc", "shade", [
    mass("M 7 31 C 15 12 55 10 65 30 C 52 35 20 36 7 31 Z", "#77746a", "ink-dry"),
    contour("M 10 30 C 24 23 49 22 63 29", "#4a4943", 1.4),
    ribbon([(36, 30, .10), (36, 44, .80), (35, 61, .08)], 2.6, "shade-pole", "#262522", .22),
    ribbon([(27, 61, .10), (35, 59, .80), (43, 61, .08)], 2.0, "shade-foot", "#77746a", .24, True),
])

write("brc", "temple", [
    mass("M 36 8 L 61 29 L 56 59 L 16 59 L 11 29 Z", "#77746a", "ink-dry"),
    mass("M 18 29 L 54 29 L 52 34 L 20 34 Z", "#262522"),
    contour("M 18 56 L 22 32 M 29 57 L 31 32 M 43 57 L 41 32 M 54 56 L 50 32", "#4a4943", 2.0),
    mass("M 31 45 C 34 40 39 40 42 45 L 41 59 L 31 59 Z", "#262522"),
    GROUND,
])


# Castalia props and characters --------------------------------------------
def puppet_bust(name: str, left: bool) -> None:
    face = "M 24 20 C 28 12 42 11 48 19 C 53 26 50 38 43 42 C 34 47 22 40 20 31 C 19 26 21 22 24 20 Z"
    nose = "M 46 24 L 61 29 L 47 33 Z" if not left else "M 24 24 L 10 29 L 24 33 Z"
    eye_x = 39 if not left else 29
    write("castalia", name, [
        mass(face, "#4a4943"), mass(nose, "#262522"),
        mass("M 23 20 C 28 9 44 8 50 18 C 42 15 32 16 23 20 Z", "#262522"),
        dab(eye_x, 24, 1.4, 1.4, "#f3f0e6", "ink-dry"),
        mass("M 23 42 C 31 38 43 39 49 44 L 54 61 L 18 61 Z", "#77746a", "ink-dry"),
        contour("M 27 49 C 34 53 41 52 47 48", "#262522", 1.8), GROUND,
    ])


puppet_bust("judy-torso", True)
puppet_bust("punch-torso", False)

write("castalia", "maker-seal", [
    contour("M 36 7 C 53 7 65 20 65 36 C 65 53 52 65 36 65 C 19 65 7 52 7 36 C 7 19 20 7 36 7 Z", "#4a4943", 2.8),
    ribbon([(22, 48, .10), (34, 36, .82), (50, 20, .08)], 4.0, "seal-hammer-handle", "#262522", .28),
    mass("M 43 14 L 58 22 L 52 31 L 38 23 Z", "#77746a", "ink-dry"),
    mass("M 17 51 C 27 46 43 47 53 52 L 49 57 L 21 57 Z", "#4a4943"),
])

write("castalia", "mermaid-guide", [
    mass("M 30 11 C 35 5 45 7 48 14 C 50 21 45 27 39 27 C 35 31 29 33 25 29 C 29 24 27 17 30 11 Z", "#262522"),
    dab(39, 16, 4.6, 5.1, "#77746a", "ink-dry"),
    mass("M 30 25 C 35 22 42 23 45 29 L 45 39 C 42 44 34 44 30 39 L 27 31 Z", "#4a4943"),
    mass("M 37 40 C 38 47 29 51 30 58 C 31 64 39 67 45 62 C 42 56 43 50 49 45 C 52 42 48 38 44 39 Z", "#4a4943"),
    mass("M 43 61 C 50 56 59 57 66 62 C 59 64 54 67 51 71 C 47 68 44 65 43 61 Z", "#77746a", "ink-dry"),
    ribbon([(30, 31, .10), (21, 37, .72), (12, 34, .08)], 2.2, "mermaid-left-arm", "#262522", .30),
    ribbon([(42, 30, .10), (50, 25, .72), (57, 18, .08)], 2.0, "mermaid-guide-arm", "#77746a", .30, True),
    dab(41, 15, 1.0, 1.0, "#f3f0e6", "ink-dry"),
    contour("M 35 48 C 39 50 43 50 47 47", "#77746a", 1.2),
])

write("castalia", "pirate-ship", [
    mass("M 9 45 C 22 49 45 49 63 43 C 59 57 49 63 31 61 C 19 60 12 54 9 45 Z", "#4a4943"),
    ribbon([(35, 46, .10), (35, 29, .78), (36, 10, .08)], 2.2, "ship-mast", "#262522", .24),
    mass("M 37 14 C 48 17 55 25 57 35 C 49 34 42 31 37 27 Z", "#77746a", "ink-dry"),
    mass("M 33 18 C 25 21 19 29 17 38 C 25 36 30 32 34 27 Z", "#262522"),
    mass("M 36 9 L 50 12 L 37 18 Z", "#262522"),
    contour("M 16 48 C 28 54 48 53 59 47", "#b2afa6", 1.3),
    GROUND,
])

write("castalia", "police-box", [
    mass("M 18 18 L 55 18 L 58 62 L 15 62 Z", "#4a4943"),
    mass("M 14 14 L 59 14 L 58 21 L 15 21 Z", "#262522"),
    mass("M 28 8 L 45 8 L 48 14 L 25 14 Z", "#77746a", "ink-dry"),
    contour("M 22 27 L 33 27 L 33 39 L 22 39 Z M 40 27 L 51 27 L 51 39 L 40 39 Z M 22 45 L 33 45 L 33 58 L 22 58 Z M 40 45 L 51 45 L 51 58 L 40 58 Z", "#b2afa6", 1.4),
    dab(37, 54, 1.2, 1.2, "#262522"), GROUND,
])

def puppet_hand(name: str, mirror=False) -> None:
    art = [
        mass("M 27 56 C 20 48 18 38 21 31 L 19 19 C 19 14 24 14 25 19 L 27 29 L 27 11 C 27 6 32 6 33 11 L 33 28 L 36 9 C 37 4 42 5 42 11 L 40 30 L 45 15 C 47 10 51 12 50 17 L 47 38 C 46 49 40 58 31 60 Z", "#4a4943"),
        ribbon([(26, 35, .10), (34, 39, .72), (43, 36, .08)], 1.5, f"{name}-palm-fold", "#77746a", .28, True),
        GROUND,
    ]
    write("castalia", name, [group("translate(72 0) scale(-1 1)", art)] if mirror else art)


puppet_hand("puppet-left-hand")
puppet_hand("puppet-right-hand", True)

write("castalia", "puppet-shoe", [
    mass("M 13 46 C 21 43 27 36 31 25 L 47 29 C 46 38 50 44 61 48 C 65 53 61 59 54 60 L 19 60 C 11 59 8 51 13 46 Z", "#4a4943"),
    mass("M 30 25 L 49 27 L 48 34 L 28 32 Z", "#262522"),
    contour("M 14 51 C 27 55 46 54 60 49", "#77746a", 1.6), GROUND,
])

write("castalia", "research-submarine", [
    mass("M 9 39 C 17 27 45 23 58 33 C 68 41 60 53 47 56 C 29 60 13 53 9 45 Z", "#4a4943"),
    mass("M 27 28 L 31 19 L 45 19 L 49 27 Z", "#77746a", "ink-dry"),
    ribbon([(39, 20, .10), (39, 12, .72), (47, 11, .08)], 1.8, "sub-periscope", "#262522", .25),
    dab(25, 41, 3.2, 3.2, "#77746a", "ink-dry"), dab(39, 39, 3.2, 3.2, "#77746a", "ink-dry"), dab(52, 39, 2.8, 2.8, "#77746a", "ink-dry"),
    mass("M 9 39 L 2 34 L 3 49 L 10 45 Z", "#262522"),
    ribbon([(12, 59, .10), (29, 57, .70), (48, 60, .50), (64, 55, .08)], 1.2, "sub-water", "#77746a", .35, True),
])

def rook_flame_marks() -> list[str]:
    return [
        mass("M 22 30 L 22 20 L 29 20 L 29 25 L 34 25 L 34 20 L 41 20 L 41 25 L 47 25 L 47 20 L 54 20 L 54 31 L 49 36 L 50 56 L 56 61 L 18 61 L 23 56 L 24 36 Z", "#4a4943"),
        mass("M 37 21 C 31 14 36 7 42 3 C 41 11 48 14 43 22 Z", "#262522"),
        contour("M 24 38 C 32 35 43 36 50 39 M 23 55 C 32 52 43 53 50 55", "#77746a", 1.4),
    ]


write("castalia", "rook-flame", rook_flame_marks() + [GROUND])


# Cave rooms: a shared irregular arch plus one unmistakable room landmark. ----
def cave_base() -> list[str]:
    return [
        contour("M 10 61 C 10 34 18 12 35 8 C 53 11 63 34 63 61", "#4a4943", 3.0),
        contour("M 16 60 C 18 38 24 21 36 17 C 49 21 56 38 57 60", "#77746a", 1.5),
        contour("M 8 62 C 25 59 45 64 65 60", "#77746a", 1.2),
    ]


def cave_write(name: str, landmark: list[str]) -> None:
    write("cave_locations", name, cave_base() + landmark)


bird = [
    mass("M 22 39 C 27 31 39 30 47 35 C 52 40 48 48 41 51 C 32 54 23 49 22 43 Z", "#4a4943"),
    mass("M 45 35 L 58 39 L 46 43 Z", "#262522"),
    mass("M 27 40 C 33 35 41 37 43 43 C 38 47 31 48 27 45 Z", "#77746a", "ink-dry"),
    dab(43, 35, 1.0, 1.0, "#f3f0e6", "ink-dry"),
]
cave_write("bird-chamber", bird)
cave_write("castalia-rook-flame", [group("translate(18 22) scale(.50)", rook_flame_marks())])
cave_write("debris-room", [
    mass("M 16 55 L 24 43 L 33 55 Z M 29 57 L 40 39 L 51 57 Z M 46 56 L 55 47 L 62 58 Z", "#4a4943"),
    contour("M 19 54 L 25 49 M 34 54 L 41 46 M 50 55 L 55 51", "#77746a", 1.4),
])
cave_write("end-of-road", [
    ribbon([(19, 60, .08), (27, 48, .70), (32, 36, .08)], 2.4, "road-left", "#4a4943", .25),
    ribbon([(54, 60, .08), (45, 48, .70), (40, 36, .08)], 2.0, "road-right", "#77746a", .25, True),
    mass("M 29 29 L 44 29 L 43 39 L 30 39 Z", "#262522"),
])
cave_write("hall-of-mists", [
    ribbon([(16, 35, .08), (28, 31, .72), (42, 35, .60), (57, 31, .08)], 2.0, "mist-one", "#77746a", .45, True),
    ribbon([(14, 43, .08), (28, 40, .72), (43, 44, .62), (59, 40, .08)], 2.5, "mist-two", "#4a4943", .45),
    ribbon([(18, 51, .08), (31, 48, .72), (45, 52, .55), (56, 49, .08)], 1.4, "mist-three", "#77746a", .42, True),
])
cave_write("outside-grate", [
    mass("M 18 56 C 27 53 44 54 54 57 L 51 61 L 21 61 Z", "#4a4943"),
    contour("M 22 27 L 51 27 L 53 57 L 20 57 Z M 28 28 L 27 56 M 36 28 L 36 57 M 44 28 L 45 56 M 21 37 L 52 37 M 21 47 L 52 47", "#262522", 2.0),
])
cave_write("plover-room", bird + [dab(20, 54, 3.5, 2.8, "#77746a", "ink-dry")])


print("redrew 29 story-world glyphs for toddler recognition")
