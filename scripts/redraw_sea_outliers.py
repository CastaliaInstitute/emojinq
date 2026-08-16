#!/usr/bin/env python3
"""Add defining anatomy to sea-creature recognition outliers."""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/pua/sea_creatures"


def p(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(points, width, seed, color="#262421", wobble=.22):
    class_name = "ink-dry" if color in {"#77746a", "#bcb9af"} else "ink-wash"
    return svg_path(
        stroke_path(p(*points), width=width, seed=seed, wobble=wobble),
        fill=color,
        class_name=class_name,
    )


def mass(d: str, color="#4a4943") -> str:
    return f'<path class="ink-wash" d="{d}" fill="{color}" data-ink-brush-pass="loaded-mass-v2"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    cp = re.search(r'data-pua="[^"]+"', target.read_text(encoding="utf-8"))
    if not cp:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="sea_creatures / {name}" {cp.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="draw-v1" data-naturalist-construction="toddler-anatomy-v1">
<title>sea_creatures / {name} — toddler-readable anatomical sumi-e study</title>{''.join(marks)}</svg>
''', encoding="utf-8")


write("manta", [
    ribbon([(6, 35, .12), (20, 21, .72), (35, 29, 1), (51, 21, .7), (66, 35, .12)], 3.0, "manta-leading"),
    ribbon([(6, 35, .12), (20, 45, .72), (35, 39, 1), (51, 45, .7), (66, 35, .12)], 2.4, "manta-trailing", "#4a4943"),
    mass("M31 27 C33 24 39 24 42 27 L41 39 C38 43 34 43 31 39 Z", "#77746a"),
    ribbon([(36, 39, .12), (38, 49, .72), (47, 61, .08)], 1.25, "manta-tail"),
    ribbon([(32, 29, .12), (29, 24, .72), (28, 20, .08)], 1.0, "manta-cephalic-left", "#262421"),
    ribbon([(41, 29, .12), (44, 24, .72), (45, 20, .08)], .8, "manta-cephalic-right", "#77746a"),
    '<circle class="ink-wash" cx="32" cy="31" r="1.25" fill="#262421"/><circle class="ink-wash" cx="41" cy="31" r="1.25" fill="#262421"/>',
])

write("nautilus", [
    ribbon([(14, 37, .12), (17, 24, .72), (28, 15, 1), (42, 15, .82), (54, 23, .9), (59, 36, .82), (55, 49, .9), (44, 57, .82), (29, 56, .9), (17, 48, .72), (14, 37, .12)], 2.4, "nautilus-shell", "#77746a"),
    ribbon([(50, 25, .08), (43, 18, .72), (32, 19, 1), (24, 27, .9), (24, 38, .82), (31, 46, .72), (41, 45, 1), (47, 38, .72), (44, 31, .72), (37, 28, .72), (32, 32, .08)], 2.6, "nautilus-spiral"),
    mass("M50 36 C56 34 61 37 61 42 C58 46 53 47 49 44 Z", "#4a4943"),
    ribbon([(54, 42, .12), (61, 48, .72), (66, 53, .08)], .9, "nautilus-tentacle-a", "#262421"),
    ribbon([(52, 43, .12), (58, 51, .72), (61, 58, .08)], .75, "nautilus-tentacle-b", "#77746a"),
    '<circle class="ink-wash" cx="55" cy="39" r="1.1" fill="#262421"/>',
])

write("whale", [
    ribbon([(13, 40, .12), (20, 29, .72), (35, 25, 1), (50, 28, .9), (62, 36, .82), (62, 44, .72), (50, 52, .9), (33, 54, .82), (19, 49, .72), (13, 43, .12), (13, 40, .08)], 3.0, "whale-body-contour", "#77746a"),
    ribbon([(19, 39, .12), (31, 34, .72), (45, 35, 1), (57, 40, .08)], 4.0, "whale-body-wash", "#4a4943"),
    ribbon([(14, 41, .12), (8, 35, .72), (4, 31, .08)], 2.6, "whale-tail-upper", "#262421"),
    ribbon([(14, 42, .12), (8, 47, .72), (4, 51, .08)], 2.1, "whale-tail-lower", "#4a4943"),
    ribbon([(36, 50, .12), (41, 58, .72), (48, 59, .08)], 1.8, "whale-flipper", "#262421"),
    ribbon([(49, 27, .12), (51, 20, .72), (48, 14, .08)], 1.15, "whale-spout-left", "#262421"),
    ribbon([(51, 21, .12), (56, 16, .72), (60, 15, .08)], .9, "whale-spout-right", "#77746a"),
    ribbon([(54, 44, .12), (59, 45, .72), (62, 43, .08)], .7, "whale-mouth", "#bcb9af"),
    '<circle class="ink-wash" cx="56" cy="35" r="1.2" fill="#262421"/>',
])

write("seahorse", [
    ribbon([(48, 18, .12), (42, 14, .72), (35, 16, 1), (33, 22, .65), (38, 26, .12)], 1.8, "seahorse-head"),
    ribbon([(48, 18, .12), (55, 20, .7), (49, 23, .12)], 1.45, "seahorse-snout"),
    ribbon([(38, 26, .12), (31, 32, .72), (30, 42, 1), (35, 49, .65), (42, 49, .12)], 2.0, "seahorse-back"),
    ribbon([(42, 49, .12), (48, 53, .72), (45, 60, 1), (37, 60, .7), (35, 55, .12), (40, 53, .08)], 1.55, "seahorse-tail"),
    ribbon([(31, 32, .12), (24, 28, .7), (25, 39, .12), (30, 42, .08)], 1.2, "seahorse-fin", "#77746a"),
    ribbon([(39, 28, .12), (44, 34, .72), (42, 43, .12), (35, 49, .08)], 1.0, "seahorse-belly", "#4a4943"),
    '<circle class="ink-wash" cx="41" cy="19" r="1.6" fill="#262421"/>',
])

print("redrew manta, nautilus, seahorse, and whale with defining anatomy")
