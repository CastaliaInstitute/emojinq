#!/usr/bin/env python3
"""Replace stick-figure body actions with readable sumi-e gesture studies."""
from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]


def p(*v: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*x) for x in v]


def ribbon(points, width, seed, color="#262522", wobble=.28):
    return svg_path(stroke_path(p(*points), width=width, seed=seed, wobble=wobble), fill=color)


def write(name: str, marks: list[str]) -> None:
    target = ROOT / "assets/pua/body" / f"{name}.svg"
    match = re.search(r'data-pua="([^"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="body / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>body / {name} — authored sumi-e brush study</title>{''.join(marks)}</svg>
''')


# Push: a compact person with two arms visibly braced against a heavy boulder.
write("push", [
    '<ellipse class="ink-wash" cx="24" cy="21" rx="4.2" ry="4.8" fill="#3c3b36"/>',
    ribbon([(24, 27, .2), (25, 34, .7), (24, 42, 1.0), (22, 48, .2)], 3.4, "push-torso", "#4a4943", .3),
    ribbon([(22, 46, .2), (17, 51, .7), (14, 56, .2)], 2.4, "push-leg-back", "#262522", .3),
    ribbon([(25, 45, .2), (30, 51, .7), (35, 55, .2)], 2.4, "push-leg-front", "#262522", .3),
    ribbon([(24, 31, .2), (31, 32, .7), (38, 34, 1.0), (43, 34, .2)], 2.25, "push-arm-upper", "#262522", .3),
    ribbon([(24, 37, .2), (31, 38, .7), (38, 39, 1.0), (43, 39, .2)], 2.25, "push-arm-lower", "#262522", .3),
    ribbon([(43, 25, .2), (52, 23, .7), (60, 28, 1.0), (61, 38, .75), (58, 48, .2), (50, 52, .2), (44, 47, .7), (43, 25, .2)], 2.35, "push-boulder", "#3c3b36", .29),
    ribbon([(10, 58, .2), (24, 59, .7), (39, 57, 1.0), (52, 57, .2)], 1.15, "push-ground", "#77746a"),
])

# Reach: a person leaning toward a clearly separate object, with an open hand between them.
write("reach", [
    '<ellipse class="ink-wash" cx="20" cy="18" rx="4.8" ry="5.1" fill="#3c3b36"/>',
    ribbon([(21, 24, .2), (25, 29, .72), (25, 36, 1.0), (22, 44, .2)], 3.0, "reach-torso", "#4a4943", .3),
    ribbon([(21, 44, .2), (17, 50, .72), (15, 57, .2)], 2.3, "reach-leg-back", "#262522", .3),
    ribbon([(24, 43, .2), (29, 50, .72), (35, 56, .2)], 2.3, "reach-leg-front", "#262522", .3),
    ribbon([(24, 28, .2), (29, 31, .7), (34, 35, 1.0), (39, 33, .72), (44, 28, .2)], 2.35, "reach-arm", "#262522", .36),
    '<ellipse class="ink-wash" cx="50" cy="25" rx="3.8" ry="3.0" fill="#4a4943"/>',
    ribbon([(51, 23, .2), (55, 20, .7), (58, 21, .2)], 1.0, "reach-finger-one", "#77746a", .32),
    ribbon([(52, 25, .2), (56, 23, .7), (59, 24, .2)], 1.0, "reach-finger-two", "#77746a", .32),
    ribbon([(52, 27, .2), (55, 26, .7), (58, 27, .2)], 1.0, "reach-finger-three", "#77746a", .32),
    ribbon([(23, 31, .2), (20, 36, .7), (19, 41, .2)], 1.5, "reach-other-arm", "#77746a", .3),
    '<ellipse class="ink-wash" cx="62" cy="27" rx="3.2" ry="2.8" fill="#262522"/>',
    ribbon([(58, 27, .2), (60, 26, .7), (62, 27, .2)], 1.0, "reach-object-glint", "#77746a"),
])

# Walk: a compact walking person with a head, torso, swinging arms, and a wide stride.
write("walk", [
    '<ellipse class="ink-wash" cx="35" cy="14" rx="4.7" ry="5.0" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 30 22 C 33 20 39 20 42 23 C 44 28 43 35 40 40 C 37 43 31 42 28 38 C 27 32 28 26 30 22 Z"/>',
    ribbon([(35, 22, .2), (36, 28, .72), (35, 36, 1.0), (34, 41, .2)], 1.5, "walk-body-seam", "#262522", .3),
    ribbon([(34, 38, .2), (29, 45, .7), (25, 53, .95), (19, 56, .2)], 2.7, "walk-leg-back", wobble=.3),
    ribbon([(36, 38, .2), (41, 45, .7), (48, 51, 1.0), (56, 53, .2)], 2.7, "walk-leg-front", wobble=.3),
    ribbon([(34, 25, .2), (28, 31, .7), (25, 36, .2)], 1.55, "walk-arm-back", "#77746a"),
    ribbon([(38, 25, .2), (44, 30, .7), (48, 34, .2)], 1.55, "walk-arm-front", "#77746a"),
    ribbon([(19, 56, .2), (23, 57, .7), (28, 56, .2)], 1.8, "walk-foot-back", "#262522", .32),
    ribbon([(54, 53, .2), (59, 54, .7), (64, 53, .2)], 1.8, "walk-foot-front", "#262522", .32),
])

print("redrew push, reach, and walk as gesture-based brush studies")
