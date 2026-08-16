#!/usr/bin/env python3
"""Replace icon-like people concepts with restrained sumi-e figure studies.

These are deliberately authored as a few continuous pressure ribbons.  The
semantic cue is the observed human gesture or scene, not a generic circle,
heart, arrow, or stick figure.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, stroke_path, svg_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "people"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(values, width, seed, color="#262522", wobble=.24):
    return svg_path(stroke_path(points(*values), width=width, seed=seed, wobble=wobble), fill=color)


def mass(values, width, seed, color="#4a4943"):
    """A single loaded body pass; the surrounding contour stays open."""
    return ribbon(values, width, seed, color, .18)


def head(cx: float, cy: float, scale: float, seed: str, color="#262522") -> str:
    """An incomplete, pressure-led head contour rather than a filled dot."""
    return ribbon([
        (cx - 4.8 * scale, cy + 1.0 * scale, .25),
        (cx - 4.0 * scale, cy - 3.6 * scale, .68),
        (cx - 1.0 * scale, cy - 6.0 * scale, 1.0),
        (cx + 3.1 * scale, cy - 5.1 * scale, .88),
        (cx + 5.0 * scale, cy - 1.4 * scale, .58),
        (cx + 4.0 * scale, cy + 3.3 * scale, .2),
        (cx + 1.0 * scale, cy + 5.0 * scale, .24),
        (cx - 2.8 * scale, cy + 4.2 * scale, .4),
        (cx - 4.8 * scale, cy + 1.0 * scale, .18),
    ], 2.7 * scale, seed, color, .28)


def profile(cx: float, cy: float, direction: int, seed: str, color="#262522") -> str:
    """Short brow/nose/mouth observation that turns a ring into a person."""
    sign = 1 if direction >= 0 else -1
    return ribbon([
        (cx + sign * 1.2, cy - 1.7, .18),
        (cx + sign * 3.2, cy - .4, .72),
        (cx + sign * 1.3, cy + .7, .2),
    ], .9, seed + "-profile", color, .2) + ribbon([
        (cx + sign * 1.0, cy + 2.0, .2),
        (cx + sign * 2.4, cy + 2.4, .7),
        (cx + sign * 3.4, cy + 2.0, .2),
    ], .62, seed + "-mouth", color, .2)


def ground(seed: str) -> str:
    return ribbon([(8, 63, .18), (20, 61, .58), (35, 63, .86), (50, 61, .62), (64, 62, .18)], .72, seed, "#77746a", .3)


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point: {target}")
    body = "".join(marks + [ground(f"{name}-ground")])
    target.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="people / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-ink-wash-v1" data-ink-stroke-system="tapered-v1" data-ink-animation="wash-v1" data-ink-path-units="normalized">
  <title>people / {name} — observed sumi-e figure study</title>{body}
</svg>
'''
    )


# Alliance: two figures lean toward one another and meet at a clasped hand.
write("alliance", [
    head(24, 20, .9, "alliance-left-head", "#4a4943"),
    head(48, 20, .9, "alliance-right-head", "#262522"),
    profile(24, 20, 1, "alliance-left-face", "#262522"),
    profile(48, 20, -1, "alliance-right-face", "#262522"),
    mass([(22, 29, .2), (21, 36, .72), (23, 44, 1.0), (26, 50, .2)], 5.8, "alliance-left-mass", "#4a4943"),
    mass([(50, 29, .2), (51, 36, .72), (49, 44, 1.0), (46, 50, .2)], 5.8, "alliance-right-mass", "#4a4943"),
    ribbon([(20, 27, .2), (16, 33, .7), (16, 43, 1.0), (19, 53, .2)], 3.0, "alliance-left-robe", "#4a4943"),
    ribbon([(52, 27, .2), (56, 33, .7), (56, 43, 1.0), (53, 53, .2)], 3.0, "alliance-right-robe"),
    ribbon([(21, 31, .2), (27, 35, .7), (32, 39, 1.0), (36, 38, .55), (40, 34, .2)], 2.6, "alliance-left-hand"),
    ribbon([(51, 31, .2), (45, 35, .7), (40, 39, 1.0), (36, 38, .55), (32, 34, .2)], 2.35, "alliance-right-hand", "#4a4943"),
    ribbon([(21, 49, .2), (27, 55, .7), (32, 57, .2)], 2.45, "alliance-left-sleeve"),
    ribbon([(51, 49, .2), (45, 55, .7), (40, 57, .2)], 2.45, "alliance-right-sleeve", "#4a4943"),
    ribbon([(21, 17, .2), (24, 15, .7), (27, 17, .2)], 1.05, "alliance-left-hair", "#77746a"),
    ribbon([(45, 17, .2), (48, 15, .7), (51, 17, .2)], 1.05, "alliance-right-hair", "#77746a"),
])

# Compassion: a standing figure bends and steadies a seated companion.
write("compassion", [
    head(25, 18, .85, "compassion-adult-head"),
    head(48, 40, .7, "compassion-child-head", "#4a4943"),
    profile(25, 18, 1, "compassion-adult-face"),
    profile(48, 40, -1, "compassion-child-face", "#4a4943"),
    mass([(23, 27, .2), (22, 34, .72), (25, 42, 1.0), (27, 47, .2)], 6.2, "compassion-adult-mass", "#4a4943"),
    mass([(47, 46, .2), (48, 50, .72), (46, 55, .2)], 4.5, "compassion-child-mass", "#77746a"),
    ribbon([(21, 26, .2), (27, 29, .68), (31, 37, 1.0), (29, 47, .25)], 3.15, "compassion-adult-back"),
    ribbon([(28, 30, .2), (35, 34, .7), (42, 39, .9), (46, 41, .18)], 2.55, "compassion-supporting-hand", "#4a4943"),
    ribbon([(29, 42, .2), (24, 50, .68), (18, 56, .2)], 2.8, "compassion-adult-knee"),
    ribbon([(47, 46, .2), (43, 51, .75), (38, 56, .2)], 2.4, "compassion-companion-knee", "#4a4943"),
    ribbon([(52, 44, .2), (57, 48, .75), (59, 54, .2)], 1.8, "compassion-companion-arm", "#77746a"),
    ribbon([(21, 15, .2), (25, 12, .7), (29, 15, .2)], 1.1, "compassion-adult-hair", "#77746a"),
])

# Help: one figure pulls a tired companion up by both hands.
write("help", [
    head(24, 20, .88, "help-standing-head"),
    head(49, 39, .68, "help-rising-head", "#4a4943"),
    profile(24, 20, 1, "help-standing-face"),
    profile(49, 39, -1, "help-rising-face", "#4a4943"),
    mass([(21, 28, .2), (20, 36, .72), (22, 45, 1.0), (25, 51, .2)], 6.0, "help-standing-mass", "#4a4943"),
    mass([(48, 45, .2), (49, 50, .72), (46, 56, .2)], 4.7, "help-rising-mass", "#77746a"),
    ribbon([(20, 28, .2), (16, 36, .72), (18, 48, 1.0), (22, 57, .2)], 3.0, "help-standing-body"),
    ribbon([(48, 45, .2), (45, 51, .72), (43, 57, .2)], 2.3, "help-rising-body", "#4a4943"),
    ribbon([(25, 31, .2), (31, 35, .7), (37, 41, 1.0), (43, 44, .2)], 2.6, "help-left-hand"),
    ribbon([(22, 35, .2), (29, 39, .7), (37, 43, 1.0), (45, 45, .2)], 2.25, "help-right-hand", "#4a4943"),
    ribbon([(22, 47, .2), (27, 54, .72), (32, 58, .2)], 2.5, "help-standing-leg"),
    ribbon([(45, 51, .2), (50, 55, .72), (55, 57, .2)], 2.0, "help-rising-foot", "#4a4943"),
    ribbon([(20, 16, .2), (24, 13, .7), (28, 16, .2)], 1.05, "help-standing-hair", "#77746a"),
])

# Choice: a traveler pauses where one worn path divides into two curved paths.
write("choice", [
    head(36, 18, .88, "choice-traveler-head"),
    profile(36, 18, 1, "choice-traveler-face"),
    mass([(33, 27, .2), (30, 35, .72), (31, 43, 1.0), (34, 48, .2)], 6.0, "choice-traveler-mass", "#4a4943"),
    ribbon([(31, 26, .2), (27, 34, .72), (29, 44, 1.0), (34, 49, .2)], 3.0, "choice-traveler-body"),
    ribbon([(32, 31, .2), (37, 29, .72), (42, 26, .2)], 2.25, "choice-raised-hand", "#4a4943"),
    ribbon([(31, 33, .2), (27, 39, .72), (23, 43, .2)], 2.15, "choice-resting-hand", "#4a4943"),
    ribbon([(32, 45, .2), (27, 51, .72), (21, 55, .2)], 2.65, "choice-left-leg"),
    ribbon([(35, 45, .2), (41, 51, .72), (47, 55, .2)], 2.5, "choice-right-leg", "#4a4943"),
    ribbon([(21, 55, .2), (15, 57, .7), (9, 56, .2)], 1.45, "choice-left-path", "#77746a"),
    ribbon([(47, 55, .2), (54, 57, .7), (63, 55, .2)], 1.45, "choice-right-path", "#77746a"),
    ribbon([(32, 15, .2), (36, 12, .7), (40, 15, .2)], 1.05, "choice-hair", "#77746a"),
])

# Conflict: two full figures brace against one another; the diagonal torsos
# and opposing forearms carry the meaning without arrows or crossed symbols.
write("conflict", [
    head(23, 19, .82, "conflict-left-head", "#262522"),
    head(49, 19, .82, "conflict-right-head", "#4a4943"),
    profile(23, 19, 1, "conflict-left-face"),
    profile(49, 19, -1, "conflict-right-face", "#262522"),
    mass([(21, 27, .2), (19, 35, .72), (21, 45, 1.0), (24, 52, .2)], 6.4, "conflict-left-mass", "#4a4943"),
    mass([(51, 27, .2), (53, 35, .72), (51, 45, 1.0), (48, 52, .2)], 6.4, "conflict-right-mass", "#4a4943"),
    ribbon([(19, 27, .2), (15, 35, .7), (18, 47, 1.0), (25, 56, .2)], 3.25, "conflict-left-body"),
    ribbon([(53, 27, .2), (57, 35, .7), (54, 47, 1.0), (47, 56, .2)], 3.25, "conflict-right-body", "#4a4943"),
    ribbon([(24, 31, .2), (30, 33, .65), (36, 36, 1.0), (42, 33, .6), (48, 31, .2)], 2.7, "conflict-braced-arms"),
    ribbon([(26, 34, .2), (32, 37, .7), (36, 36, 1.0), (40, 37, .7), (46, 34, .2)], 1.45, "conflict-finger-break", "#77746a"),
    ribbon([(23, 48, .2), (20, 56, .75), (16, 59, .2)], 2.5, "conflict-left-foot"),
    ribbon([(49, 48, .2), (52, 56, .75), (56, 59, .2)], 2.5, "conflict-right-foot", "#4a4943"),
])

# Cooperation: two workers carry one uneven beam together.
write("cooperation", [
    head(21, 20, .8, "cooperation-left-head", "#4a4943"),
    head(51, 20, .8, "cooperation-right-head"),
    profile(21, 20, 1, "cooperation-left-face"),
    profile(51, 20, -1, "cooperation-right-face"),
    mass([(19, 28, .2), (18, 36, .72), (20, 46, 1.0), (23, 52, .2)], 5.8, "cooperation-left-mass", "#4a4943"),
    mass([(53, 28, .2), (54, 36, .72), (52, 46, 1.0), (49, 52, .2)], 5.8, "cooperation-right-mass", "#4a4943"),
    ribbon([(17, 28, .2), (14, 37, .7), (15, 49, 1.0), (19, 57, .2)], 2.9, "cooperation-left-body", "#4a4943"),
    ribbon([(55, 28, .2), (58, 37, .7), (57, 49, 1.0), (53, 57, .2)], 2.9, "cooperation-right-body"),
    ribbon([(24, 34, .2), (30, 36, .7), (35, 37, .95), (42, 36, .7), (48, 34, .2)], 2.5, "cooperation-lifted-arms", "#262522"),
    ribbon([(18, 39, .2), (27, 38, .62), (36, 39, 1.0), (45, 38, .62), (54, 39, .2)], 3.0, "cooperation-shared-beam", "#4a4943", .32),
    ribbon([(19, 48, .2), (25, 55, .72), (30, 58, .2)], 2.35, "cooperation-left-leg", "#4a4943"),
    ribbon([(53, 48, .2), (47, 55, .72), (42, 58, .2)], 2.35, "cooperation-right-leg"),
    ribbon([(18, 17, .2), (21, 14, .7), (24, 17, .2)], 1.0, "cooperation-left-hair", "#77746a"),
    ribbon([(48, 17, .2), (51, 14, .7), (54, 17, .2)], 1.0, "cooperation-right-hair", "#77746a"),
])

# Humility: a seated figure bows toward a small unadorned sprig.
write("humility", [
    head(31, 31, .82, "humility-bowed-head", "#4a4943"),
    profile(31, 31, 1, "humility-bowed-face", "#262522"),
    mass([(29, 38, .2), (35, 41, .72), (43, 44, 1.0), (49, 49, .2)], 5.8, "humility-bowed-mass", "#4a4943"),
    ribbon([(27, 38, .2), (34, 40, .7), (43, 42, 1.0), (51, 49, .2)], 3.2, "humility-curved-back"),
    ribbon([(29, 41, .2), (25, 47, .75), (23, 54, .2)], 2.5, "humility-knee", "#4a4943"),
    ribbon([(39, 43, .2), (43, 49, .72), (48, 54, .2)], 2.3, "humility-lower-leg"),
    ribbon([(29, 43, .2), (35, 47, .75), (39, 51, .2)], 1.8, "humility-fold", "#77746a"),
    ribbon([(52, 52, .2), (52, 45, .7), (52, 38, .2)], 1.35, "humility-sprig", "#4a4943"),
    ribbon([(52, 43, .2), (47, 40, .7), (45, 42, .2)], .95, "humility-leaf-left", "#77746a"),
    ribbon([(52, 47, .2), (57, 44, .7), (59, 46, .2)], .95, "humility-leaf-right", "#77746a"),
])

# Mentor: an older reader turns a page toward a younger listener.
write("mentor", [
    head(22, 19, .9, "mentor-elder-head"),
    head(49, 29, .68, "mentor-learner-head", "#4a4943"),
    profile(22, 19, 1, "mentor-elder-face"),
    profile(49, 29, -1, "mentor-learner-face", "#4a4943"),
    mass([(19, 27, .2), (18, 35, .72), (20, 45, 1.0), (23, 52, .2)], 6.0, "mentor-elder-mass", "#4a4943"),
    mass([(47, 35, .2), (47, 43, .72), (45, 52, .2)], 4.6, "mentor-learner-mass", "#77746a"),
    ribbon([(18, 27, .2), (14, 36, .7), (16, 48, 1.0), (21, 57, .2)], 3.0, "mentor-elder-robe"),
    ribbon([(46, 36, .2), (43, 43, .72), (43, 54, .2)], 2.35, "mentor-learner-body", "#4a4943"),
    ribbon([(24, 32, .2), (31, 35, .7), (37, 39, .95), (43, 40, .2)], 2.55, "mentor-open-hand"),
    ribbon([(27, 41, .2), (35, 42, .65), (42, 41, .2)], 1.65, "mentor-book-spine", "#4a4943"),
    ribbon([(28, 43, .2), (35, 47, .7), (42, 43, .2)], 1.35, "mentor-book-page", "#77746a"),
    ribbon([(21, 48, .2), (27, 56, .75), (33, 58, .2)], 2.45, "mentor-elder-knee"),
    ribbon([(45, 51, .2), (49, 56, .72), (54, 58, .2)], 2.15, "mentor-learner-foot", "#4a4943"),
    ribbon([(18, 16, .2), (22, 12, .7), (27, 16, .2)], 1.05, "mentor-elder-hair", "#77746a"),
])

# Welcome: a host stands in a doorway, one arm opening the space to a guest.
write("welcome", [
    ribbon([(17, 58, .2), (17, 27, .7), (23, 17, 1.0), (34, 14, .7), (43, 17, .2)], 2.9, "welcome-doorway"),
    ribbon([(43, 17, .2), (45, 29, .7), (44, 58, .2)], 1.9, "welcome-door-edge", "#4a4943"),
    head(35, 26, .8, "welcome-host-head"),
    profile(35, 26, 1, "welcome-host-face"),
    mass([(32, 34, .2), (31, 40, .72), (33, 47, 1.0), (36, 52, .2)], 5.8, "welcome-host-mass", "#4a4943"),
    ribbon([(30, 34, .2), (25, 38, .68), (20, 42, 1.0), (14, 42, .2)], 2.7, "welcome-open-arm"),
    ribbon([(39, 35, .2), (44, 42, .72), (49, 52, .2)], 2.55, "welcome-host-sleeve"),
    ribbon([(30, 43, .2), (27, 52, .72), (24, 58, .2)], 2.7, "welcome-host-leg"),
    ribbon([(38, 43, .2), (41, 52, .72), (44, 58, .2)], 2.45, "welcome-host-leg-right", "#4a4943"),
    ribbon([(30, 24, .2), (35, 20, .7), (40, 24, .2)], 1.05, "welcome-host-hair", "#77746a"),
    ribbon([(8, 57, .18), (11, 53, .65), (14, 48, .2)], 1.35, "welcome-guest-step", "#77746a"),
])

# Work: a craftsperson bends over a low bench with a hand tool and shavings.
write("work", [
    head(25, 21, .85, "work-craftsman-head"),
    profile(25, 21, 1, "work-craftsman-face"),
    mass([(22, 29, .2), (24, 35, .72), (29, 41, 1.0), (32, 46, .2)], 6.0, "work-craftsman-mass", "#4a4943"),
    ribbon([(20, 29, .2), (25, 32, .72), (31, 38, 1.0), (34, 46, .2)], 3.05, "work-craftsman-back"),
    ribbon([(27, 34, .2), (35, 39, .7), (42, 42, .2)], 2.4, "work-working-arm"),
    ribbon([(41, 42, .2), (47, 37, .72), (53, 32, .2)], 1.55, "work-hand-tool", "#4a4943"),
    ribbon([(36, 44, .2), (47, 45, .7), (58, 44, .2)], 2.9, "work-bench", "#4a4943"),
    ribbon([(42, 45, .2), (43, 53, .72), (42, 59, .2)], 2.0, "work-bench-leg", "#77746a"),
    ribbon([(54, 45, .2), (55, 53, .72), (56, 59, .2)], 2.0, "work-bench-leg-right", "#77746a"),
    ribbon([(22, 44, .2), (17, 51, .72), (13, 58, .2)], 2.8, "work-craftsman-leg"),
    ribbon([(29, 45, .2), (32, 52, .72), (37, 58, .2)], 2.55, "work-craftsman-leg-right", "#4a4943"),
    ribbon([(20, 18, .2), (25, 14, .7), (30, 18, .2)], 1.05, "work-craftsman-hair", "#77746a"),
    ribbon([(49, 51, .2), (52, 48, .7), (55, 51, .2)], .9, "work-shavings", "#77746a"),
])

print("redrew eight icon-like people concepts as gesture-led sumi-e studies")
