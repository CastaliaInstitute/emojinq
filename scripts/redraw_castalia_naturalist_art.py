#!/usr/bin/env python3
"""Redraw the Castalia PUA family as compact sumi-e object studies."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "castalia"


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
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="castalia / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>castalia / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


write("rook-flame", [
    ribbon([(23, 57, .10), (24, 45, .72), (24, 33, .08)], 3.0, "rook-left"),
    ribbon([(49, 57, .10), (48, 45, .72), (49, 33, .08)], 2.0, "rook-right", "#77746a", dry=True),
    ribbon([(22, 57, .10), (35, 59, .92), (51, 57, .08)], 2.8, "rook-base"),
    ribbon([(24, 34, .10), (24, 27, .72), (31, 27, .90), (31, 32, .72), (39, 32, .90), (39, 27, .72), (48, 27, .08)], 1.4, "rook-crown"),
    ribbon([(36, 46, .10), (32, 39, .72), (36, 33, .94), (34, 24, .72), (39, 15, .08)], 2.7, "rook-flame-host", "#4a4943"),
    ribbon([(38, 34, .10), (43, 29, .72), (42, 23, .08)], 1.0, "rook-flame-dry", "#77746a", dry=True),
])


write("maker-seal", [
    ribbon([(36, 8, .10), (50, 11, .72), (60, 21, .94), (64, 35, .82), (59, 50, .72), (47, 60, .94), (31, 63, .82), (17, 57, .72), (9, 44, .94), (9, 28, .72), (18, 15, .08)], 2.0, "seal-ring"),
    ribbon([(18, 15, .10), (27, 9, .72), (36, 8, .08)], .85, "seal-ring-lift", "#77746a", dry=True),
    ribbon([(27, 51, .10), (28, 41, .72), (28, 32, .08)], 2.0, "seal-rook-left"),
    ribbon([(46, 51, .10), (45, 41, .72), (45, 32, .08)], 1.3, "seal-rook-right", "#77746a", dry=True),
    ribbon([(26, 51, .10), (36, 53, .92), (47, 51, .08)], 2.0, "seal-rook-base"),
    ribbon([(28, 33, .10), (33, 30, .72), (37, 33, .90), (42, 29, .72), (46, 32, .08)], 1.0, "seal-rook-crown"),
    ribbon([(37, 42, .10), (34, 36, .72), (38, 29, .94), (37, 23, .08)], 1.8, "seal-flame", "#4a4943"),
])


write("research-submarine", [
    ribbon([(14, 42, .10), (27, 36, .78), (43, 36, 1.0), (57, 41, .08)], 7.0, "submarine-hull", "#4a4943"),
    ribbon([(22, 37, .10), (31, 31, .72), (43, 32, .08)], 1.3, "submarine-deck"),
    ribbon([(38, 32, .10), (38, 24, .72), (43, 24, .08)], 1.55, "submarine-periscope"),
    dab(28, 39, 2.0, 1.8, "#262522"),
    dab(39, 38, 1.8, 1.6, "#77746a"),
    dab(49, 39, 1.6, 1.45, "#262522"),
    ribbon([(15, 41, .10), (9, 36, .72), (6, 31, .08)], 1.35, "submarine-propeller-a"),
    ribbon([(14, 42, .10), (8, 47, .72), (5, 52, .08)], 1.0, "submarine-propeller-b", "#77746a", dry=True),
    ribbon([(10, 54, .10), (25, 51, .72), (41, 54, .90), (58, 51, .08)], .72, "submarine-water", "#bcb9af", dry=True),
])


write("mermaid-guide", [
    dab(34, 16, 3.0, 3.2),
    ribbon([(34, 20, .10), (32, 29, .82), (35, 38, 1.0), (41, 45, .08)], 3.3, "mermaid-torso", "#4a4943"),
    ribbon([(40, 44, .10), (49, 48, .78), (58, 46, .94), (64, 40, .08)], 3.0, "mermaid-tail"),
    ribbon([(58, 46, .10), (65, 51, .72), (68, 57, .08)], 1.6, "mermaid-fin-a", "#77746a", dry=True),
    ribbon([(58, 47, .10), (62, 56, .72), (60, 63, .08)], 1.3, "mermaid-fin-b", "#4a4943"),
    ribbon([(33, 27, .10), (23, 31, .72), (15, 27, .08)], 1.4, "mermaid-arm-back", "#77746a", dry=True),
    ribbon([(36, 27, .10), (46, 24, .72), (55, 18, .08)], 1.7, "mermaid-guide-arm"),
    ribbon([(30, 18, .10), (24, 14, .72), (20, 9, .08)], 1.2, "mermaid-hair", "#77746a", dry=True),
])


# Punch is a sharp profile: peaked cap, long nose, compact torso.
write("punch-torso", [
    dab(35, 27, 7.0, 7.6, "#4a4943"),
    ribbon([(31, 20, .10), (37, 14, .72), (44, 10, .08)], 2.0, "punch-cap"),
    ribbon([(40, 26, .10), (50, 29, .72), (59, 33, .08)], 2.4, "punch-nose"),
    ribbon([(42, 34, .10), (48, 38, .72), (53, 37, .08)], 1.0, "punch-chin", "#77746a", dry=True),
    ribbon([(31, 34, .10), (25, 43, .82), (22, 55, .08)], 3.0, "punch-torso-left"),
    ribbon([(38, 35, .10), (44, 44, .72), (49, 56, .08)], 2.0, "punch-torso-right", "#77746a", dry=True),
    ribbon([(21, 56, .10), (34, 53, .82), (50, 57, .08)], 2.2, "punch-hem"),
    ribbon([(23, 43, .10), (34, 46, .72), (44, 44, .08)], .72, "punch-collar", "#bcb9af", dry=True),
])


# Judy faces the audience: bonnet, round face, open collar and skirt.
write("judy-torso", [
    dab(35, 26, 7.1, 7.4, "#4a4943"),
    ribbon([(25, 22, .10), (27, 14, .72), (35, 10, .94), (44, 13, .72), (48, 21, .08)], 2.0, "judy-bonnet"),
    ribbon([(27, 19, .10), (35, 17, .82), (44, 20, .08)], 1.1, "judy-bonnet-brim", "#77746a", dry=True),
    ribbon([(29, 34, .10), (25, 44, .72), (21, 56, .08)], 2.8, "judy-torso-left"),
    ribbon([(40, 34, .10), (45, 44, .72), (50, 56, .08)], 1.8, "judy-torso-right", "#77746a", dry=True),
    ribbon([(21, 56, .10), (35, 53, .92), (51, 57, .08)], 2.2, "judy-hem"),
    ribbon([(25, 40, .10), (35, 45, .92), (46, 40, .08)], 1.15, "judy-collar"),
    ribbon([(32, 29, .10), (35, 31, .72), (38, 29, .08)], .65, "judy-smile", "#bcb9af", dry=True),
])


# Mirrored puppet hands share a palm but not a repeated outline: each finger is
# a separate loaded lift, and the thumb establishes handedness.
write("puppet-left-hand", [
    ribbon([(39, 57, .10), (34, 49, .82), (31, 39, 1.0), (31, 29, .08)], 5.2, "left-palm", "#4a4943"),
    ribbon([(30, 34, .10), (24, 26, .72), (20, 17, .08)], 2.0, "left-index"),
    ribbon([(32, 32, .10), (30, 21, .72), (29, 11, .08)], 2.2, "left-middle"),
    ribbon([(35, 34, .10), (38, 23, .72), (40, 14, .08)], 1.75, "left-ring"),
    ribbon([(37, 37, .10), (45, 29, .72), (49, 22, .08)], 1.25, "left-little", "#77746a", dry=True),
    ribbon([(30, 43, .10), (20, 40, .72), (13, 35, .08)], 2.0, "left-thumb"),
    ribbon([(32, 48, .10), (38, 50, .72), (43, 48, .08)], .72, "left-palm-fold", "#bcb9af", dry=True),
])


write("puppet-right-hand", [
    ribbon([(33, 57, .10), (38, 49, .82), (41, 39, 1.0), (41, 29, .08)], 5.2, "right-palm", "#4a4943"),
    ribbon([(42, 34, .10), (48, 26, .72), (52, 17, .08)], 2.0, "right-index"),
    ribbon([(40, 32, .10), (42, 21, .72), (43, 11, .08)], 2.2, "right-middle"),
    ribbon([(37, 34, .10), (34, 23, .72), (32, 14, .08)], 1.75, "right-ring"),
    ribbon([(35, 37, .10), (27, 29, .72), (23, 22, .08)], 1.25, "right-little", "#77746a", dry=True),
    ribbon([(42, 43, .10), (52, 40, .72), (59, 35, .08)], 2.0, "right-thumb"),
    ribbon([(40, 48, .10), (34, 50, .72), (29, 48, .08)], .72, "right-palm-fold", "#bcb9af", dry=True),
])


write("puppet-shoe", [
    ribbon([(22, 23, .10), (23, 34, .82), (21, 45, .08)], 5.0, "shoe-ankle", "#4a4943"),
    ribbon([(21, 44, .10), (31, 47, .72), (42, 50, 1.0), (56, 51, .08)], 6.2, "shoe-vamp", "#4a4943"),
    ribbon([(55, 50, .10), (62, 53, .72), (65, 57, .08)], 2.0, "shoe-toe"),
    ribbon([(18, 57, .10), (33, 59, .82), (49, 58, .94), (64, 57, .08)], 2.2, "shoe-sole"),
    ribbon([(24, 29, .10), (31, 34, .72), (38, 40, .08)], .90, "shoe-upper-edge", "#77746a", dry=True),
    ribbon([(23, 47, .10), (34, 50, .72), (46, 52, .08)], .65, "shoe-highlight", "#bcb9af", dry=True),
])


write("pirate-ship", [
    ribbon([(10, 50, .10), (24, 55, .82), (41, 55, 1.0), (58, 49, .08)], 5.2, "ship-hull", "#4a4943"),
    ribbon([(34, 51, .10), (35, 37, .72), (35, 20, .08)], 2.0, "ship-mast"),
    ribbon([(35, 22, .10), (46, 27, .76), (51, 41, .94), (37, 39, .08)], 3.2, "ship-sail", "#77746a", dry=True),
    ribbon([(34, 24, .10), (24, 29, .72), (19, 41, .08)], 1.6, "ship-small-sail", "#4a4943"),
    ribbon([(35, 20, .10), (43, 17, .72), (50, 19, .08)], 1.2, "ship-pirate-flag"),
    ribbon([(15, 58, .10), (27, 56, .72), (40, 59, .90), (55, 56, .08)], .85, "ship-wave-a", "#77746a", dry=True),
    ribbon([(7, 64, .10), (19, 62, .72), (32, 64, .08)], .65, "ship-wave-b", "#bcb9af", dry=True),
])


write("police-box", [
    ribbon([(20, 60, .10), (20, 45, .72), (20, 29, .08)], 2.8, "box-left"),
    ribbon([(52, 60, .10), (51, 45, .72), (52, 29, .08)], 1.9, "box-right", "#77746a", dry=True),
    ribbon([(18, 29, .10), (35, 27, .92), (54, 29, .08)], 3.0, "box-sign-cap"),
    ribbon([(21, 60, .10), (36, 59, .92), (52, 60, .08)], 2.1, "box-base"),
    ribbon([(35, 27, .10), (35, 44, .72), (35, 59, .08)], 1.0, "box-door-seam", "#4a4943"),
    ribbon([(23, 38, .10), (29, 36, .72), (34, 38, .08)], .85, "box-panel-left", "#77746a", dry=True),
    ribbon([(38, 38, .10), (44, 36, .72), (49, 38, .08)], .85, "box-panel-right", "#bcb9af", dry=True),
    ribbon([(27, 48, .10), (30, 45, .72), (33, 48, .08)], .72, "box-lower-panel", "#77746a", dry=True),
    ribbon([(35, 25, .10), (35, 19, .72), (38, 16, .08)], 1.2, "box-lamp-stem"),
    dab(38, 15, 2.0, 1.7, "#262522"),
])


print("redrew all 11 Castalia PUA glyphs as naturalist sumi-e studies")
