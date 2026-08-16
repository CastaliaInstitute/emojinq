#!/usr/bin/env python3
"""Replace geometric people/action symbols with readable sumi-e figure studies."""
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
    target = ROOT / "assets/pua/people" / f"{name}.svg"
    match = re.search(r'data-pua="([^\"]+)"', target.read_text())
    if not match:
        raise SystemExit(f"missing PUA codepoint for {name}")
    marks.append('<path class="ink-dry" fill="#77746a" d="M 8 63 C 22 61 40 64 64 60"/>')
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {match.group(0)} data-castalia-style="sumi-e-brush-art-v4" data-ink-stroke-system="filled-ribbon-v1" data-ink-animation="draw-v1" data-ink-path-units="normalized">
<title>people / {name} — authored sumi-e figure study</title>{''.join(marks)}</svg>
''')


# Care: an adult bends toward a smaller seated child; the touching hand is the
# semantic cue, while the two different body masses keep it from becoming a
# generic heart or stick figure.
write("care", [
    '<ellipse class="ink-wash" cx="23" cy="20" rx="4.5" ry="4.8" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 20 27 C 25 24 31 27 33 33 C 32 39 29 44 25 48 L 16 50 C 16 43 18 36 20 27 Z"/>',
    ribbon([(24, 32, .2), (31, 35, .72), (37, 40, 1.0), (42, 43, .2)], 1.9, "care-hand", wobble=.3),
    ribbon([(19, 44, .2), (14, 51, .72), (12, 57, .2)], 2.2, "care-knee", wobble=.3),
    '<ellipse class="ink-wash" cx="48" cy="42" rx="3.5" ry="3.7" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#77746a" d="M 44 47 C 48 44 54 46 56 51 L 54 57 L 41 57 C 41 53 42 49 44 47 Z"/>',
    ribbon([(44, 48, .2), (40, 46, .7), (37, 43, .2)], 1.2, "care-child-hand", "#262522"),
    ribbon([(20, 18, .2), (24, 16, .7), (28, 18, .2)], 1.0, "care-hair", "#262522"),
    ribbon([(22, 31, .2), (26, 35, .7), (28, 40, .2)], .8, "care-garment-fold", "#77746a"),
    ribbon([(46, 41, .2), (48, 43, .7), (51, 42, .2)], .8, "care-child-face", "#262522"),
])

# Choice: a standing figure pauses at a fork, with the two paths diverging
# beneath the body rather than literal directional arrows.
write("choice", [
    '<ellipse class="ink-wash" cx="35" cy="17" rx="4.5" ry="4.8" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 30 24 C 34 21 39 22 42 26 L 40 42 C 38 46 32 46 29 42 Z"/>',
    ribbon([(31, 28, .2), (26, 32, .72), (21, 34, .2)], 1.7, "choice-arm-left", "#262522"),
    ribbon([(40, 28, .2), (45, 32, .72), (50, 34, .2)], 1.7, "choice-arm-right", "#262522"),
    ribbon([(33, 42, .2), (29, 49, .72), (25, 56, .2)], 2.2, "choice-leg-left", "#262522"),
    ribbon([(37, 42, .2), (42, 49, .72), (48, 56, .2)], 2.2, "choice-leg-right", "#262522"),
    ribbon([(25, 56, .2), (21, 57, .7), (18, 56, .2)], 1.2, "choice-path-left", "#77746a"),
    ribbon([(48, 56, .2), (53, 57, .7), (57, 56, .2)], 1.2, "choice-path-right", "#77746a"),
    ribbon([(31, 16, .2), (35, 14, .7), (39, 16, .2)], .9, "choice-hair", "#262522"),
    ribbon([(32, 30, .2), (36, 34, .7), (39, 39, .2)], .8, "choice-garment-fold", "#77746a"),
])

# Mentor: two unequal figures, the taller one extending an open teaching hand.
write("mentor", [
    '<ellipse class="ink-wash" cx="25" cy="20" rx="4.2" ry="4.6" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 20 27 C 24 24 29 25 32 29 L 31 48 L 17 48 C 17 39 18 32 20 27 Z"/>',
    '<ellipse class="ink-wash" cx="47" cy="28" rx="3.7" ry="4.0" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#77746a" d="M 43 34 C 47 31 52 33 54 37 L 55 53 L 39 53 C 39 44 40 38 43 34 Z"/>',
    ribbon([(29, 32, .2), (35, 31, .7), (41, 35, .2)], 1.9, "mentor-teaching-hand", "#262522", .3),
    ribbon([(22, 47, .2), (18, 55, .72), (15, 58, .2)], 1.8, "mentor-leg", "#262522"),
    ribbon([(49, 52, .2), (53, 57, .72), (57, 58, .2)], 1.8, "mentor-student-leg", "#262522"),
    ribbon([(21, 19, .2), (25, 16, .7), (29, 19, .2)], .9, "mentor-hair", "#262522"),
    ribbon([(44, 28, .2), (47, 26, .7), (50, 28, .2)], .8, "mentor-student-hair", "#262522"),
    ribbon([(22, 31, .2), (26, 35, .7), (29, 40, .2)], .8, "mentor-fold", "#77746a"),
])

# Welcome: an open-chested figure with unmistakable raised arms and palms.
write("welcome", [
    '<ellipse class="ink-wash" cx="36" cy="17" rx="4.7" ry="5.0" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 30 24 C 34 21 39 21 42 25 L 43 47 C 39 51 31 51 28 47 Z"/>',
    ribbon([(31, 28, .2), (25, 23, .68), (19, 18, 1.0), (15, 14, .2)], 2.0, "welcome-arm-left", "#262522", .32),
    ribbon([(41, 28, .2), (47, 23, .68), (53, 18, 1.0), (57, 14, .2)], 2.0, "welcome-arm-right", "#262522", .32),
    ribbon([(14, 14, .2), (11, 13, .7), (9, 15, .2)], 1.0, "welcome-palm-left", "#77746a"),
    ribbon([(58, 14, .2), (61, 13, .7), (63, 15, .2)], 1.0, "welcome-palm-right", "#77746a"),
    ribbon([(32, 47, .2), (28, 55, .72), (24, 58, .2)], 2.1, "welcome-leg-left", "#262522"),
    ribbon([(39, 47, .2), (44, 55, .72), (49, 58, .2)], 2.1, "welcome-leg-right", "#262522"),
    ribbon([(31, 16, .2), (36, 13, .7), (41, 16, .2)], .9, "welcome-hair", "#262522"),
    ribbon([(32, 31, .2), (36, 34, .7), (40, 31, .2)], .8, "welcome-robe-fold", "#77746a"),
])

# Work: a seated figure, a table, and a clear writing hand; this avoids the
# generic standing-person mark used by the old source glyph.
write("work", [
    '<ellipse class="ink-wash" cx="26" cy="22" rx="4.4" ry="4.8" fill="#3c3b36"/>',
    '<path class="ink-wash" fill="#4a4943" d="M 21 29 C 25 26 31 27 34 32 L 34 43 L 20 43 C 19 38 19 33 21 29 Z"/>',
    ribbon([(29, 32, .2), (35, 36, .72), (40, 40, .2)], 1.8, "work-arm", "#262522", .3),
    '<path class="ink-wash" fill="#77746a" d="M 39 39 L 57 39 L 55 43 L 38 43 Z"/>',
    ribbon([(40, 40, .2), (44, 36, .7), (48, 34, .2)], 1.1, "work-pencil", "#262522"),
    ribbon([(21, 42, .2), (17, 51, .72), (13, 56, .2)], 2.1, "work-leg", "#262522"),
    ribbon([(32, 42, .2), (36, 50, .72), (42, 56, .2)], 2.1, "work-leg-front", "#262522"),
    ribbon([(11, 57, .2), (25, 58, .7), (43, 57, .2)], 1.2, "work-ground", "#77746a"),
    ribbon([(22, 21, .2), (26, 18, .7), (30, 21, .2)], .9, "work-hair", "#262522"),
    ribbon([(22, 31, .2), (26, 35, .7), (30, 38, .2)], .8, "work-garment-fold", "#77746a"),
])

print("redrew care, choice, mentor, welcome, and work as figure studies")
