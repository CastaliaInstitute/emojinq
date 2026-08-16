#!/usr/bin/env python3
"""Draw the weakest body PUA glyphs as compact vector sumi-e studies.

These are not replacement pictograms.  Each study is built from a few loaded
brush masses and tapered gestures that describe the observed structure or
action.  The geometry remains closed SVG paths so it can be animated, turned
into a font, and exported as grayscale engraving depth.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "pua" / "body"


def points(*values: tuple[float, float, float]) -> list[BrushPoint]:
    return [BrushPoint(*value) for value in values]


def ribbon(
    values: list[tuple[float, float, float]],
    width: float,
    seed: str,
    color: str = "#262522",
    dry: bool = False,
) -> str:
    color = {
        "#dedbd4": "#85827a",
        "#bcb9af": "#6f6c65",
        "#77746a": "#5f5c55",
    }.get(color.lower(), color)
    width = max(width * 1.18, 1.05)
    d = stroke_path(points(*values), width=width, seed=seed, wobble=.22, taper_start=.12, taper_end=.10)
    brush_pass = "dry-edge-v1" if dry else "loaded-ribbon-v2"
    class_name = "ink-dry" if dry else "ink-wash"
    return f'<path class="{class_name}" d="{d}" fill="{color}" data-ink-brush-pass="{brush_pass}"/>'


def dry_fragments(values: list[tuple[float, float, float]], width: float, seed: str, color: str = "#77746a") -> list[str]:
    marks = []
    for index, d in enumerate(dry_brush_paths(points(*values), width=width, seed=seed, breaks=2)):
        marks.append(f'<path class="ink-dry" d="{d}" fill="{color}" data-ink-brush-pass="dry-fragment-v1" data-ink-fragment="{index}"/>')
    return marks


def mass(d: str, color: str = "#4a4943", detail: str = "loaded-mass-v2") -> str:
    # Pale washes disappear as tone when SVGs become monochrome font
    # outlines.  Preserve them as dry contour scaffolds so the compiled glyph
    # keeps its negative space; the loaded ribbons inside carry the subject.
    if color.lower() in {"#77746a", "#bcb9af", "#dedbd4"}:
        contour_color = {
            "#dedbd4": "#85827a",
            "#bcb9af": "#6f6c65",
            "#77746a": "#5f5c55",
        }[color.lower()]
        return (
            f'<path class="ink-dry" d="{d}" fill="none" stroke="{contour_color}" '
            'stroke-width="2.05" stroke-linecap="round" stroke-linejoin="round" '
            'pathLength="1" data-ink-brush-pass="dry-contour-v2"/>'
        )
    return f'<path class="ink-wash" fill="{color}" d="{d}" data-ink-brush-pass="{detail}"/>'


def dab(cx: float, cy: float, rx: float, ry: float, color: str = "#262522") -> str:
    return f'<ellipse class="ink-wash" cx="{cx:.2f}" cy="{cy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="{color}" data-ink-brush-pass="loaded-dab-v1"/>'


def write(name: str, marks: list[str]) -> None:
    target = OUT / f"{name}.svg"
    source = target.read_text()
    codepoint = re.search(r'data-pua="([^"]+)"', source)
    if not codepoint:
        raise SystemExit(f"missing PUA code point in {target}")
    target.write_text(f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" aria-label="body / {name}" {codepoint.group(0)} data-castalia-style="sumi-e-naturalist-v2" data-ink-stroke-system="filled-brush-mass-v2" data-ink-animation="wash-v1" data-ink-path-units="normalized">
<title>body / {name} — naturalist sumi-e brush study</title>{''.join(marks)}</svg>
''')


# Breath: two uneven lung masses with a trachea and branching bronchi.
write("breath", [
    mass("M 34 23 C 29 19 22 19 18 23 C 13 28 13 38 17 45 C 20 51 27 52 31 47 C 35 42 36 31 34 23 Z", "#bcb9af"),
    mass("M 38 23 C 43 19 50 19 54 23 C 59 28 59 38 55 45 C 52 51 45 52 41 47 C 37 42 36 31 38 23 Z", "#77746a"),
    ribbon([(36, 9, .12), (36, 15, .70), (36, 23, .95), (34, 28, .10)], 2.8, "breath-trachea"),
    ribbon([(36, 23, .18), (31, 27, .78), (26, 34, .94), (22, 41, .08)], 1.7, "breath-left-bronchus", "#262522"),
    ribbon([(36, 23, .18), (41, 27, .78), (46, 34, .94), (50, 41, .08)], 1.7, "breath-right-bronchus", "#262522"),
    ribbon([(30, 29, .12), (25, 34, .72), (22, 39, .08)], .62, "breath-left-vein", "#dedbd4", True),
    ribbon([(42, 29, .12), (47, 34, .72), (50, 39, .08)], .62, "breath-right-vein", "#dedbd4", True),
    ribbon([(18, 25, .10), (15, 32, .72), (17, 41, .08)], .85, "breath-left-rim", "#4a4943", True),
    ribbon([(54, 25, .10), (57, 32, .72), (55, 41, .08)], .85, "breath-right-rim", "#262522", True),
    ribbon([(28, 34, .10), (25, 39, .72), (26, 44, .08)], .55, "breath-left-leaflet", "#dedbd4", True),
    ribbon([(44, 34, .10), (47, 39, .72), (46, 44, .08)], .55, "breath-right-leaflet", "#bcb9af", True),
])

# Bounce: an imperfect ball and two separate upward/downward brush gestures.
write("bounce", [
    mass("M 36 11 C 46 10 55 17 57 28 C 59 39 53 50 43 54 C 33 58 21 52 18 42 C 14 31 19 19 28 14 C 31 12 34 11 36 11 Z", "#bcb9af"),
    ribbon([(20, 38, .16), (24, 46, .78), (33, 51, .92), (43, 50, .10)], 1.5, "bounce-lower-contour", "#262522"),
    ribbon([(29, 15, .12), (37, 19, .70), (46, 18, .94), (52, 22, .08)], 1.2, "bounce-upper-contour", "#77746a", True),
    mass("M 46 22 C 52 27 54 36 51 43 C 49 48 45 50 42 51 C 47 46 49 40 48 33 C 47 28 44 25 41 23 Z", "#77746a", "shaded-brush-mass-v1"),
    ribbon([(24, 23, .10), (20, 30, .72), (21, 37, .08)], .72, "bounce-left-edge", "#dedbd4", True),
    ribbon([(22, 8, .10), (27, 5, .66), (33, 4, .08)], 2.0, "bounce-rise-l", "#4a4943"),
    ribbon([(43, 5, .10), (48, 7, .66), (52, 11, .08)], 1.35, "bounce-rise-r", "#77746a", True),
])

# Digestion: a stomach-like reservoir feeding an irregular gut loop.
write("digestion", [
    mass("M 32 7 C 34 4 39 4 41 7 C 44 11 42 15 38 16 C 34 17 31 14 31 10 C 31 9 31 8 32 7 Z", "#bcb9af"),
    mass("M 27 19 C 32 16 41 16 46 20 C 50 29 49 43 44 52 C 39 57 30 56 26 50 C 22 41 22 28 27 19 Z", "#bcb9af"),
    mass("M 32 29 C 37 26 43 28 45 33 C 47 38 43 44 38 45 C 33 45 29 41 29 36 C 29 33 30 31 32 29 Z", "#5f5c55"),
    mass("M 27 14 C 23 17 23 24 28 28 C 33 31 33 35 28 39 C 23 43 22 50 26 54 C 30 58 37 57 40 52 C 43 47 39 43 35 39 C 31 35 33 31 39 28 C 45 25 47 20 44 16 C 41 12 37 12 34 16 C 32 18 30 14 27 14 Z", "#bcb9af"),
    ribbon([(31, 18, .10), (29, 24, .74), (34, 29, .96), (39, 32, .10)], 2.1, "digestion-entry"),
    ribbon([(39, 33, .12), (45, 36, .76), (46, 42, .96), (41, 47, .08)], 1.7, "digestion-loop", "#262522"),
    ribbon([(39, 48, .12), (35, 52, .76), (30, 51, .08)], 1.15, "digestion-exit", "#77746a", True),
    ribbon([(26, 18, .10), (25, 23, .72), (28, 27, .08)], 1.1, "digestion-stomach-rim", "#262522", True),
    ribbon([(28, 42, .10), (27, 48, .72), (31, 53, .08)], .72, "digestion-inner-fold", "#dedbd4", True),
    *dry_fragments([(21, 25, .12), (25, 29, .72), (27, 35, .92), (25, 42, .08)], .72, "digestion-edge"),
])

# Nerves: a central nerve bundle with irregular peripheral branches.
write("nerves", [
    mass("M 31 9 C 33 5 39 5 42 9 C 44 13 42 17 38 18 C 34 19 30 16 30 12 C 30 11 30 10 31 9 Z", "#bcb9af"),
    mass("M 27 20 C 32 17 40 17 45 21 C 49 28 49 39 45 46 C 42 51 31 51 27 46 C 23 38 23 28 27 20 Z", "#bcb9af"),
    ribbon([(27, 26, .12), (20, 33, .72), (13, 40, .08)], 1.4, "nerves-body-arm-left", "#77746a", True),
    ribbon([(45, 26, .12), (52, 33, .72), (59, 40, .08)], 1.4, "nerves-body-arm-right", "#77746a", True),
    ribbon([(31, 47, .12), (27, 54, .72), (23, 62, .08)], 1.55, "nerves-body-leg-left", "#77746a", True),
    ribbon([(41, 47, .12), (45, 54, .72), (49, 62, .08)], 1.55, "nerves-body-leg-right", "#77746a", True),
    ribbon([(36, 9, .10), (35, 18, .72), (36, 28, .96), (35, 39, .90), (37, 50, .72), (36, 62, .08)], 2.35, "nerves-spine"),
    ribbon([(35, 19, .12), (29, 23, .70), (23, 27, .94), (16, 29, .08)], 1.35, "nerves-left-upper"),
    ribbon([(36, 24, .12), (42, 28, .72), (49, 32, .94), (57, 34, .08)], 1.25, "nerves-right-upper", "#4a4943"),
    ribbon([(35, 33, .12), (28, 37, .70), (21, 42, .94), (14, 49, .08)], 1.45, "nerves-left-lower"),
    ribbon([(36, 37, .12), (43, 42, .72), (50, 47, .94), (58, 51, .08)], 1.35, "nerves-right-lower", "#4a4943"),
    ribbon([(35, 48, .12), (29, 51, .70), (24, 56, .08)], .88, "nerves-left-tip", "#77746a", True),
    ribbon([(37, 48, .12), (43, 53, .70), (49, 57, .08)], .88, "nerves-right-tip", "#77746a", True),
])

# Pull: a taut rope held by a compact hand/forearm; no arrow or magnet symbol.
write("pull", [
    dab(20, 18, 3.8, 4.1, "#262522"),
    mass("M 16 25 C 20 22 27 23 30 27 C 33 33 31 41 27 45 C 23 48 17 45 15 40 C 14 34 14 29 16 25 Z", "#4a4943"),
    ribbon([(24, 42, .12), (19, 49, .72), (13, 55, .96), (9, 56, .08)], 2.35, "pull-leg-back", "#262522"),
    ribbon([(28, 41, .12), (33, 48, .72), (39, 53, .96), (44, 54, .08)], 2.35, "pull-leg-front", "#262522"),
    ribbon([(25, 28, .10), (32, 32, .72), (39, 34, .96), (46, 34, .08)], 2.35, "pull-arm", "#262522"),
    mass("M 44 30 C 47 28 51 29 53 32 C 54 35 52 38 49 38 L 45 37 C 43 35 42 32 44 30 Z", "#77746a"),
    ribbon([(51, 34, .10), (58, 34, .72), (65, 35, .08)], 1.35, "pull-rope", "#4a4943", True),
    ribbon([(10, 26, .10), (7, 23, .72), (5, 20, .08)], .75, "pull-effort", "#77746a", True),
])

# Pulse: a living heart mass with one vessel and a single rhythmic trace.
write("pulse", [
    mass("M 36 54 C 32 50 20 42 17 34 C 14 26 19 20 26 21 C 31 21 34 25 36 29 C 39 24 43 20 48 21 C 55 22 58 29 55 36 C 52 44 42 50 36 54 Z", "#77746a"),
    ribbon([(36, 29, .12), (33, 25, .74), (29, 23, .08)], 1.9, "pulse-left-cleft"),
    ribbon([(36, 29, .12), (40, 25, .74), (45, 23, .08)], 1.9, "pulse-right-cleft"),
    ribbon([(44, 21, .10), (48, 15, .72), (50, 9, .08)], 1.45, "pulse-vessel", "#262522"),
    ribbon([(13, 60, .10), (22, 57, .72), (30, 60, .96), (37, 57, .94), (45, 60, .08)], 1.2, "pulse-trace", "#4a4943"),
    ribbon([(25, 34, .10), (29, 39, .72), (34, 43, .08)], .72, "pulse-inner-fold-l", "#dedbd4", True),
    ribbon([(47, 34, .10), (43, 39, .72), (38, 43, .08)], .72, "pulse-inner-fold-r", "#bcb9af", True),
])

# Roll: a rounded seed/stone with one wrapping brush sweep and trailing dry marks.
write("roll", [
    mass("M 25 18 C 35 13 48 17 53 27 C 58 37 54 49 44 54 C 34 59 22 55 18 46 C 13 36 16 24 25 18 Z", "#bcb9af"),
    ribbon([(21, 27, .12), (28, 22, .72), (39, 23, .96), (47, 29, .84), (49, 37, .08)], 2.0, "roll-sweep"),
    ribbon([(48, 37, .10), (45, 44, .72), (38, 48, .08)], 1.35, "roll-sweep-tail", "#262522"),
    *dry_fragments([(10, 23, .10), (14, 26, .70), (17, 30, .08)], 1.0, "roll-motion-a"),
    *dry_fragments([(11, 48, .10), (15, 45, .70), (19, 43, .08)], .92, "roll-motion-b"),
])

# Blood: a heavy drop with a small spreading cap and a dry internal flow.
write("blood", [
    mass("M 36 9 C 32 16 24 24 23 34 C 22 44 28 52 36 54 C 44 52 50 44 49 35 C 48 25 40 16 36 9 Z", "#77746a"),
    ribbon([(36, 12, .10), (34, 22, .72), (36, 31, .96), (33, 42, .08)], 2.2, "blood-flow"),
    ribbon([(31, 28, .10), (27, 33, .72), (27, 39, .08)], .72, "blood-left-vein", "#dedbd4", True),
    ribbon([(40, 30, .10), (44, 35, .72), (44, 40, .08)], .72, "blood-right-vein", "#bcb9af", True),
])

# Bones: a single observed long bone, with swollen joints and a dry edge.
write("bones", [
    mass("M 16 20 C 14 17 16 13 20 12 C 23 11 26 13 28 16 L 44 43 C 46 46 49 47 52 46 C 56 45 59 47 60 50 C 61 54 58 58 54 59 C 50 60 47 58 44 55 L 28 29 C 26 26 23 25 20 26 C 16 27 13 24 13 22 C 13 21 14 20 16 20 Z", "#4a4943"),
    ribbon([(20, 17, .10), (26, 21, .72), (34, 33, .95), (45, 51, .08)], 1.0, "bones-shaft", "#262522", True),
    ribbon([(18, 18, .10), (21, 20, .72), (24, 23, .08)], .65, "bones-joint-l", "#dedbd4", True),
    ribbon([(49, 51, .10), (53, 53, .72), (57, 51, .08)], .65, "bones-joint-r", "#77746a", True),
])

# Clap: two overlapping palms, with separated finger gestures and a dry impact.
write("clap", [
    mass("M 18 47 C 18 39 21 31 26 25 C 28 23 31 24 31 27 L 29 36 L 33 29 C 34 26 37 26 38 29 L 36 39 C 40 34 44 33 46 35 C 48 37 46 40 43 43 L 34 51 C 29 55 21 53 18 47 Z", "#4a4943"),
    mass("M 54 47 C 54 39 51 31 46 25 C 44 23 41 24 41 27 L 43 36 L 39 29 C 38 26 35 26 34 29 L 36 39 C 32 34 28 33 26 35 C 24 37 26 40 29 43 L 38 51 C 43 55 51 53 54 47 Z", "#68665f"),
    ribbon([(21, 19, .10), (25, 16, .72), (30, 17, .08)], 1.25, "clap-impact-l", "#262522"),
    ribbon([(42, 17, .10), (47, 16, .72), (51, 19, .08)], 1.25, "clap-impact-r", "#262522"),
    ribbon([(36, 21, .10), (36, 16, .72), (36, 11, .08)], .95, "clap-impact-center", "#77746a", True),
    ribbon([(22, 38, .10), (25, 34, .72), (28, 31, .08)], .8, "clap-left-finger-cut-one", "#dedbd4", True),
    ribbon([(24, 44, .10), (28, 40, .72), (32, 37, .08)], .8, "clap-left-finger-cut-two", "#dedbd4", True),
    ribbon([(50, 38, .10), (47, 34, .72), (44, 31, .08)], .8, "clap-right-finger-cut-one", "#bcb9af", True),
    ribbon([(48, 44, .10), (44, 40, .72), (40, 37, .08)], .8, "clap-right-finger-cut-two", "#bcb9af", True),
])

# Crawl: a low human/animal gesture with a loaded back and four weight-bearing limbs.
write("crawl", [
    mass("M 18 31 C 25 27 36 27 45 31 C 51 34 56 38 61 37 C 64 37 65 40 62 42 C 57 46 50 44 44 42 C 35 40 27 43 20 46 C 15 48 12 45 13 40 C 14 36 15 33 18 31 Z", "#bcb9af"),
    mass("M 13 30 C 11 28 12 25 15 24 C 18 23 21 25 22 28 L 20 33 C 18 35 15 34 13 30 Z", "#4a4943"),
    ribbon([(25, 40, .10), (21, 45, .72), (18, 52, .96), (14, 55, .08)], 2.45, "crawl-front-leg"),
    ribbon([(35, 40, .10), (32, 46, .72), (31, 53, .96), (28, 56, .08)], 2.2, "crawl-middle-leg", "#4a4943"),
    ribbon([(45, 41, .10), (49, 47, .72), (55, 51, .96), (60, 54, .08)], 2.15, "crawl-rear-leg"),
    ribbon([(20, 34, .10), (16, 38, .72), (12, 42, .08)], 1.75, "crawl-front-arm", "#262522"),
    ribbon([(28, 37, .10), (25, 42, .72), (23, 47, .08)], 1.45, "crawl-under-arm", "#77746a", True),
])

# Grab: an open palm curling around a small seed; each finger is a separate taper.
write("grab", [
    mass("M 23 49 C 18 45 17 38 20 33 L 27 22 C 29 19 32 20 32 23 L 29 34 L 34 23 C 35 20 38 21 38 24 L 35 35 L 40 26 C 41 23 44 24 44 27 L 41 38 L 45 32 C 47 29 50 31 49 34 L 45 44 C 41 52 31 55 23 49 Z", "#bcb9af"),
    mass("M 45 45 C 49 41 54 40 57 43 C 60 46 59 51 55 53 C 51 55 47 52 45 49 Z", "#4a4943"),
    ribbon([(28, 37, .10), (32, 40, .72), (38, 41, .08)], .78, "grab-palm-fold", "#262522", True),
    ribbon([(25, 45, .10), (30, 48, .72), (36, 48, .08)], .68, "grab-wrist-fold", "#77746a", True),
])

# Kick: the lifted lower leg and foot are one strong gesture, with a small motion wash.
write("kick", [
    mass("M 24 18 C 21 23 22 30 26 34 C 30 38 36 38 40 35 C 43 32 42 27 38 24 L 34 20 C 31 17 27 16 24 18 Z", "#bcb9af"),
    ribbon([(35, 34, .12), (41, 38, .72), (47, 39, .96), (53, 35, .08)], 3.4, "kick-thigh"),
    mass("M 51 32 C 55 29 60 30 62 33 C 64 36 62 39 59 40 L 52 40 C 49 39 49 35 51 32 Z", "#4a4943"),
    ribbon([(57, 36, .10), (62, 38, .72), (67, 37, .08)], 2.5, "kick-foot"),
    ribbon([(26, 34, .10), (22, 43, .72), (18, 53, .08)], 2.2, "kick-planted-leg", "#262522"),
    ribbon([(58, 25, .10), (63, 22, .72), (68, 23, .08)], .95, "kick-motion-a", "#77746a", True),
    ribbon([(60, 28, .10), (65, 28, .72), (69, 30, .08)], .72, "kick-motion-b", "#77746a", True),
])

# Muscles: a flexed arm built from a loaded upper-arm mass and tendon ribbons.
write("muscles", [
    mass("M 22 53 C 20 44 21 34 24 27 C 27 20 32 17 38 19 C 43 21 45 27 42 33 C 40 37 40 42 45 45 C 51 48 56 46 59 49 C 62 52 60 57 55 58 L 31 58 C 27 58 24 56 22 53 Z", "#77746a"),
    ribbon([(28, 25, .10), (31, 31, .72), (32, 38, .96), (29, 46, .08)], 1.7, "muscles-biceps"),
    ribbon([(37, 23, .10), (39, 29, .72), (37, 35, .08)], 1.15, "muscles-inner-fold", "#dedbd4", True),
    ribbon([(30, 47, .10), (38, 50, .72), (48, 51, .08)], 1.25, "muscles-forearm", "#262522"),
])

# Shake: an open hand with two loose motion strokes rather than a symbol.
write("shake", [
    mass("M 26 52 C 21 48 20 42 22 36 L 25 24 C 26 21 29 21 30 24 L 29 35 L 33 20 C 34 17 37 18 37 21 L 35 35 L 39 20 C 40 17 43 18 43 21 L 41 36 L 45 25 C 46 22 49 23 49 26 L 46 40 C 45 47 40 53 34 54 C 31 54 28 53 26 52 Z", "#4a4943"),
    ribbon([(28, 45, .10), (34, 47, .72), (40, 45, .08)], .78, "shake-palm-fold", "#262522", True),
    ribbon([(18, 29, .10), (14, 26, .72), (12, 22, .08)], 1.0, "shake-motion-l", "#77746a", True),
    ribbon([(51, 31, .10), (56, 28, .72), (59, 24, .08)], 1.0, "shake-motion-r", "#77746a", True),
])

# Skin: a familiar open hand, with palm creases and freckles as surface cues.
write("skin", [
    mass("M 23 55 C 18 50 17 42 20 36 L 23 22 C 24 19 28 20 28 23 L 27 35 L 31 17 C 32 14 36 15 36 19 L 34 35 L 39 16 C 40 13 44 15 44 18 L 41 36 L 46 22 C 47 19 51 21 50 25 L 47 43 C 46 52 39 58 31 59 C 28 59 25 57 23 55 Z", "#4a4943"),
    ribbon([(25, 44, .10), (32, 47, .72), (40, 44, .08)], 1.3, "skin-palm-crease", "#dedbd4", True),
    ribbon([(27, 50, .10), (33, 53, .72), (38, 51, .08)], 1.0, "skin-wrist-crease", "#bcb9af", True),
    dab(30, 38, 1.0, .9, "#77746a"),
    dab(38, 40, .8, .7, "#77746a"),
    dab(43, 34, .7, .7, "#77746a"),
])

# Stomach: a warm reservoir with a clear inlet, outlet, and one inner fold.
write("stomach", [
    mass("M 25 17 C 30 13 37 14 40 18 C 43 22 42 27 39 30 C 36 33 38 36 42 40 C 48 46 46 54 39 57 C 31 61 23 56 21 50 C 19 44 23 39 27 35 C 31 32 30 29 27 26 C 23 23 22 20 25 17 Z", "#bcb9af"),
    ribbon([(31, 10, .10), (32, 15, .72), (33, 19, .08)], 1.8, "stomach-inlet"),
    ribbon([(40, 50, .10), (47, 53, .72), (54, 51, .08)], 1.4, "stomach-outlet", "#262522"),
    ribbon([(25, 35, .10), (31, 39, .72), (36, 47, .08)], 1.15, "stomach-fold", "#77746a", True),
    ribbon([(29, 20, .10), (35, 24, .72), (39, 28, .08)], .78, "stomach-inner-rim", "#dedbd4", True),
])

# Walk: an abbreviated human gesture, made from a weighted torso and swinging limbs.
write("walk", [
    dab(34, 14, 4.2, 4.6, "#262522"),
    mass("M 29 22 C 33 19 39 20 41 24 C 44 30 42 37 39 41 C 35 44 29 42 27 37 C 26 31 27 25 29 22 Z", "#4a4943"),
    ribbon([(31, 39, .12), (26, 47, .72), (20, 54, .96), (14, 56, .08)], 2.5, "walk-leg-back"),
    ribbon([(37, 39, .12), (42, 46, .72), (49, 51, .96), (58, 52, .08)], 2.5, "walk-leg-front", "#262522"),
    ribbon([(29, 26, .10), (24, 32, .72), (20, 37, .08)], 1.45, "walk-arm-back", "#77746a", True),
    ribbon([(39, 26, .10), (45, 31, .72), (50, 35, .08)], 1.5, "walk-arm-front", "#262522"),
    ribbon([(13, 56, .10), (18, 57, .72), (23, 55, .08)], 1.25, "walk-foot-back", "#77746a", True),
    ribbon([(56, 52, .10), (61, 54, .72), (65, 52, .08)], 1.25, "walk-foot-front", "#262522"),
])

# Wave: a broad loaded crest, a receding trough, and a few dry sea marks.
write("wave", [
    mass("M 8 48 C 16 47 19 40 23 33 C 28 24 35 19 43 21 C 51 23 53 31 59 34 C 63 36 66 35 67 32 C 68 42 63 50 56 54 C 45 60 31 58 20 55 C 15 54 11 52 8 48 Z", "#77746a"),
    ribbon([(9, 48, .10), (18, 49, .72), (27, 45, .96), (35, 37, .94), (42, 29, .08)], 2.15, "wave-crest"),
    ribbon([(43, 29, .10), (50, 31, .72), (57, 36, .96), (64, 36, .08)], 1.45, "wave-break", "#262522"),
    ribbon([(15, 54, .10), (26, 52, .72), (39, 54, .96), (51, 51, .08)], .82, "wave-recede", "#dedbd4", True),
    ribbon([(20, 59, .10), (31, 58, .72), (43, 59, .08)], .62, "wave-dry-line", "#bcb9af", True),
])

# Push: a braced, leaning figure with two hands visibly meeting a heavy stone.
write("push", [
    mass("M 17 16 C 19 12 24 12 27 15 C 29 17 28 20 26 22 L 22 24 C 19 22 17 20 17 16 Z", "#262522"),
    ribbon([(23, 23, .10), (24, 26, .72), (25, 29, .08)], 1.7, "push-neck", "#77746a"),
    mass("M 17 26 C 21 23 27 24 30 28 C 33 33 33 39 30 44 C 27 47 21 46 18 41 C 16 36 15 30 17 26 Z", "#4a4943"),
    ribbon([(26, 41, .10), (22, 48, .72), (16, 56, .96), (11, 57, .08)], 2.8, "push-leg-back"),
    ribbon([(29, 41, .10), (34, 48, .72), (40, 53, .96), (46, 54, .08)], 2.8, "push-leg-front", "#262522"),
    ribbon([(25, 29, .10), (31, 30, .72), (38, 32, .96), (46, 34, .08)], 3.3, "push-arm-upper", "#262522"),
    ribbon([(24, 35, .10), (31, 36, .72), (38, 38, .96), (46, 39, .08)], 3.0, "push-arm-lower", "#77746a"),
    mass("M 49 25 C 56 22 63 25 65 31 C 67 38 64 46 58 50 C 52 53 46 48 45 42 C 44 35 45 28 49 25 Z", "#77746a"),
    ribbon([(50, 30, .10), (57, 33, .72), (61, 40, .08)], .85, "push-stone-grain", "#bcb9af", True),
    ribbon([(29, 28, .10), (35, 31, .72), (41, 33, .08)], .9, "push-sleeve-fold", "#bcb9af", True),
    ribbon([(29, 36, .10), (35, 38, .72), (42, 39, .08)], .78, "push-sleeve-fold-2", "#dedbd4", True),
    ribbon([(46, 34, .10), (49, 35, .72), (52, 35, .08)], .62, "push-fingers", "#dedbd4", True),
])

# Reach: a rising figure with a long shoulder-to-hand gesture and a small leaf.
write("reach", [
    mass("M 19 15 C 21 12 26 13 28 16 C 29 19 27 22 24 23 L 21 22 C 19 20 18 18 19 15 Z", "#262522"),
    ribbon([(23, 23, .10), (24, 26, .72), (25, 29, .08)], 1.7, "reach-neck", "#77746a"),
    mass("M 19 25 C 23 22 29 24 31 28 C 33 34 31 40 27 44 C 24 46 19 43 18 38 C 17 33 17 28 19 25 Z", "#4a4943"),
    ribbon([(25, 41, .10), (21, 48, .72), (16, 56, .96), (12, 58, .08)], 2.5, "reach-leg-back"),
    ribbon([(28, 41, .10), (33, 48, .72), (39, 53, .96), (45, 55, .08)], 2.5, "reach-leg-front", "#262522"),
    ribbon([(25, 29, .10), (31, 28, .72), (37, 24, .96), (44, 19, .08)], 3.0, "reach-arm", "#262522"),
    ribbon([(24, 34, .10), (20, 38, .72), (18, 42, .08)], 1.45, "reach-other-arm", "#77746a", True),
    mass("M 52 12 C 56 9 62 10 64 13 C 62 17 57 18 53 16 Z", "#77746a"),
    ribbon([(45, 19, .10), (50, 16, .72), (56, 14, .08)], .85, "reach-fingers", "#bcb9af", True),
    ribbon([(28, 29, .10), (34, 27, .72), (40, 22, .08)], .78, "reach-shoulder-fold", "#bcb9af", True),
    ribbon([(29, 37, .10), (34, 39, .72), (39, 41, .08)], .68, "reach-torso-fold", "#dedbd4", True),
])

# Walk: a weighted torso, counter-swinging arms, and one long planted stride.
write("walk", [
    mass("M 32 10 C 34 7 39 8 41 11 C 43 14 41 17 38 19 L 35 19 C 32 17 31 14 32 10 Z", "#262522"),
    ribbon([(36, 18, .10), (36, 21, .72), (36, 24, .08)], 1.7, "walk-neck", "#77746a"),
    mass("M 29 22 C 33 19 39 20 42 24 C 45 30 43 37 39 42 C 35 45 29 42 27 37 C 26 31 27 25 29 22 Z", "#4a4943"),
    ribbon([(32, 39, .10), (27, 47, .72), (21, 54, .96), (14, 57, .08)], 3.5, "walk-leg-back"),
    ribbon([(37, 39, .10), (42, 46, .72), (50, 51, .96), (59, 52, .08)], 3.5, "walk-leg-front", "#262522"),
    ribbon([(30, 26, .10), (24, 32, .72), (20, 38, .08)], 1.85, "walk-arm-back", "#77746a"),
    ribbon([(40, 26, .10), (46, 31, .72), (51, 37, .08)], 1.85, "walk-arm-front", "#262522"),
    ribbon([(13, 57, .10), (18, 58, .72), (24, 56, .08)], 1.5, "walk-foot-back", "#77746a", True),
    ribbon([(57, 52, .10), (62, 54, .72), (66, 52, .08)], 1.5, "walk-foot-front", "#262522"),
    ribbon([(32, 25, .10), (35, 31, .72), (35, 37, .08)], .72, "walk-torso-fold", "#bcb9af", True),
    ribbon([(29, 28, .10), (32, 34, .72), (31, 39, .08)], .72, "walk-coat-fold-l", "#77746a", True),
    ribbon([(40, 28, .10), (38, 34, .72), (39, 39, .08)], .68, "walk-coat-fold-r", "#dedbd4", True),
    ribbon([(23, 48, .10), (27, 51, .72), (31, 50, .08)], .62, "walk-knee-fold", "#bcb9af", True),
])

print("redrew the body PUA set as vector naturalist brush studies")
