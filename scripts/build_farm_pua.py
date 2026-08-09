#!/usr/bin/env python3
"""Generate the farm PUA glyph set (F1300+) as tapered-ink SVGs.

Each glyph is described as a set of brush strokes: a centerline polyline
with a width profile. Strokes are smoothed with Catmull-Rom, jittered
slightly for a hand feel, and emitted as filled tapered outlines — the
same visual system (sumi-e-ink-wash-v1 / tapered-v1) as the rest of the
PUA library. Deterministic per glyph, so rebuilds are reproducible.

Usage: python3 scripts/build_farm_pua.py            # writes assets/pua/farm/
       python3 scripts/build_farm_pua.py --manifest # also updates assets/pua/manifest.json
"""

from __future__ import annotations

import argparse
import json
import math
import random
import zlib
from pathlib import Path

INK = "#262522"
CANVAS = 72
STYLE = "sumi-e-ink-wash-v1"
STROKE_SYSTEM = "tapered-v1"
BLOCK_START = 0xF1400

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "assets" / "pua" / "farm"
MANIFEST = ROOT / "assets" / "pua" / "manifest.json"


# ── geometry ──────────────────────────────────────────────────────────

def catmull_rom(pts, samples_per_seg=14, closed=False):
    if closed:
        ext = [pts[-1]] + list(pts) + [pts[0], pts[1]]
    else:
        ext = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(ext) - 2):
        p0, p1, p2, p3 = ext[i - 1], ext[i], ext[i + 1], ext[i + 2]
        for s in range(samples_per_seg):
            t = s / samples_per_seg
            t2, t3 = t * t, t * t * t
            x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t +
                       (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 +
                       (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
            y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t +
                       (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 +
                       (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
            out.append((x, y))
    if not closed:
        out.append(tuple(pts[-1]))
    return out


def interp_widths(widths, n):
    if len(widths) == 1:
        return [widths[0]] * n
    out = []
    for i in range(n):
        t = i / (n - 1) * (len(widths) - 1)
        k = min(int(t), len(widths) - 2)
        f = t - k
        out.append(widths[k] * (1 - f) + widths[k + 1] * f)
    return out


def stroke_outline(pts, widths, rng, closed=False, jitter=0.35, wobble=0.08):
    """Centerline + widths → filled outline polygon(s)."""
    center = catmull_rom(pts, closed=closed)
    n = len(center)
    ws = interp_widths(widths, n)
    # tangents → normals
    left, right = [], []
    for i in range(n):
        a = center[max(0, i - 1)] if not closed else center[(i - 1) % n]
        b = center[min(n - 1, i + 1)] if not closed else center[(i + 1) % n]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        w = ws[i] * (1 + rng.uniform(-wobble, wobble))
        jx = nx * rng.uniform(-jitter, jitter)
        jy = ny * rng.uniform(-jitter, jitter)
        cx, cy = center[i][0] + jx, center[i][1] + jy
        left.append((cx + nx * w / 2, cy + ny * w / 2))
        right.append((cx - nx * w / 2, cy - ny * w / 2))
    if closed:
        return [left, list(reversed(right))]
    return [left + list(reversed(right))]


def dot(cx, cy, r, rng, segs=10):
    pts = []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        rr = r * (1 + rng.uniform(-0.12, 0.12))
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return [pts]


def poly_to_d(poly):
    d = "M " + " L ".join(f"{x:.2f},{y:.2f}" for x, y in poly) + " Z"
    return d


# ── stroke shorthand ──────────────────────────────────────────────────
# S(points, widths)            open tapered stroke
# L(points, width_or_widths)   closed loop stroke (outline ring)
# D(cx, cy, r)                 filled dot

def S(pts, widths):
    return ("stroke", pts, widths)

def L(pts, widths):
    return ("loop", pts, widths if isinstance(widths, list) else [widths])

def D(cx, cy, r):
    return ("dot", cx, cy, r)


GLYPHS = {
    "carrot": [
        S([(33, 28), (36, 40), (39, 52), (41, 63)], [13, 10, 6, 1.2]),
        S([(29, 38), (35, 39)], [1.6, 0.6]),
        S([(31, 48), (37, 49)], [1.4, 0.5]),
        S([(34, 26), (30, 16), (26, 10)], [2.5, 1.8, 0.6]),
        S([(36, 26), (36, 14), (37, 8)], [2.8, 2.0, 0.7]),
        S([(38, 26), (43, 16), (47, 11)], [2.5, 1.8, 0.6]),
    ],
    "tomato": [
        L([(36, 27), (46, 31), (51, 41), (46, 52), (36, 56), (26, 52), (21, 41), (26, 31)], 2.2),
        S([(36, 27), (27, 22)], [2.6, 0.6]),
        S([(36, 27), (32, 19)], [2.6, 0.6]),
        S([(36, 27), (40, 19)], [2.6, 0.6]),
        S([(36, 27), (45, 22)], [2.6, 0.6]),
        S([(36, 26), (36, 18)], [2.6, 0.9]),
    ],
    "corn": [
        L([(36, 17), (43, 24), (45, 38), (42, 52), (36, 58), (30, 52), (27, 38), (29, 24)], 2.2),
        D(33, 28, 1.3), D(39, 28, 1.3),
        D(32, 35, 1.3), D(38, 35, 1.3),
        D(33, 42, 1.3), D(39, 42, 1.3),
        D(34, 49, 1.3), D(38, 49, 1.2),
        S([(31, 56), (23, 46), (24, 32)], [3.0, 2.2, 0.7]),
        S([(41, 56), (49, 46), (48, 32)], [3.0, 2.2, 0.7]),
    ],
    "strawberry": [
        L([(36, 28), (45, 31), (48, 40), (42, 52), (36, 58), (30, 52), (24, 40), (27, 31)], 2.2),
        D(32, 38, 0.95), D(40, 38, 0.95), D(36, 44, 0.95),
        D(31, 47, 0.9), D(41, 47, 0.9), D(36, 52, 0.85),
        S([(36, 28), (28, 25)], [1.8, 0.5]),
        S([(36, 28), (33, 22)], [1.8, 0.5]),
        S([(36, 28), (39, 22)], [1.8, 0.5]),
        S([(36, 28), (44, 25)], [1.8, 0.5]),
        S([(36, 26), (37, 18)], [2.0, 0.7]),
    ],
    "wheat": [
        S([(34, 64), (36, 44), (37, 26), (37, 13)], [1.8, 1.5, 1.3, 0.8]),
        S([(36.7, 18), (30, 13)], [3.8, 0.5]), S([(37, 18), (44, 14)], [3.8, 0.5]),
        S([(36.9, 24), (30, 19)], [3.8, 0.5]), S([(37, 24), (44, 20)], [3.8, 0.5]),
        S([(37, 30), (30, 25)], [3.8, 0.5]), S([(37, 30), (44, 26)], [3.8, 0.5]),
        S([(36.8, 36), (31, 31)], [3.6, 0.5]), S([(37, 36), (43, 32)], [3.6, 0.5]),
        S([(37, 13), (33, 6)], [0.9, 0.3]),
        S([(37, 13), (38, 5)], [0.9, 0.3]),
        S([(37, 13), (42, 7)], [0.9, 0.3]),
    ],
    "cow": [
        L([(14, 28), (34, 24), (52, 26), (60, 32), (61, 44), (54, 50), (24, 50), (13, 42)], 2.4),
        L([(6, 30), (14, 26), (19, 31), (18, 42), (11, 45), (5, 39)], 2.2),
        S([(8, 26), (4, 20)], [2.0, 0.6]),
        S([(15, 24), (18, 18)], [2.0, 0.6]),
        S([(18, 28), (23, 26)], [1.8, 0.5]),
        S([(22, 50), (22, 64)], [2.6, 1.8]),
        S([(29, 50), (29, 64)], [2.6, 1.8]),
        S([(49, 50), (49, 64)], [2.6, 1.8]),
        S([(56, 49), (56, 63)], [2.6, 1.8]),
        S([(61, 34), (66, 46), (65, 55)], [1.6, 1.1, 2.8]),
        D(42, 35, 5.0),
        D(30, 43, 3.0),
        S([(44, 50), (48, 55)], [3.6, 2.4]),
        D(11, 33, 1.2),
        S([(6, 39), (12, 41)], [1.2, 0.5]),
    ],
    "chicken": [
        L([(16, 40), (24, 31), (38, 28), (48, 32), (56, 22), (58, 30), (50, 44), (38, 51), (24, 50)], 2.4),
        L([(19, 15), (26, 12), (30, 17), (27, 22), (21, 22)], 2.0),
        S([(21, 22), (22, 31)], [1.8, 1.2]),
        S([(27, 22), (28, 30)], [1.8, 1.2]),
        S([(24, 13), (23, 8)], [2.2, 0.6]),
        S([(27, 12.5), (28, 7.5)], [2.2, 0.6]),
        S([(19, 17), (13, 19)], [2.4, 0.4]),
        S([(21, 21.5), (20, 25.5)], [1.6, 0.4]),
        S([(30, 36), (40, 38), (46, 43)], [2.2, 1.6, 0.5]),
        S([(32, 51), (31, 62)], [1.6, 1.1]),
        S([(31, 62), (26, 64)], [1.0, 0.3]),
        S([(31, 62), (33, 65)], [1.0, 0.3]),
        S([(31, 62), (36, 63.5)], [1.0, 0.3]),
        S([(40, 50), (40, 61)], [1.6, 1.1]),
        S([(40, 61), (35.5, 63.5)], [1.0, 0.3]),
        S([(40, 61), (42, 64.5)], [1.0, 0.3]),
        S([(40, 61), (45, 62.5)], [1.0, 0.3]),
        D(23, 16.5, 1.1),
    ],
    "pig": [
        L([(12, 38), (24, 28), (48, 27), (60, 34), (61, 45), (50, 52), (24, 52), (12, 46)], 2.4),
        L([(6, 36), (12, 34), (13, 42), (7, 43)], 2.0),
        D(8.8, 38.5, 0.75), D(11, 38.5, 0.75),
        S([(13, 44), (18, 46)], [1.2, 0.4]),
        S([(22, 29), (26, 20), (31, 27)], [2.2, 1.7, 0.6]),
        S([(32, 28), (36, 21), (40, 27)], [2.0, 1.5, 0.5]),
        S([(24, 52), (24, 64)], [2.4, 1.7]),
        S([(31, 52), (31, 64)], [2.4, 1.7]),
        S([(46, 52), (46, 64)], [2.4, 1.7]),
        S([(53, 51), (53, 63)], [2.4, 1.7]),
        S([(61, 38), (67, 35), (69, 40), (65, 44), (62, 41)], [1.4, 1.1, 0.9, 0.7, 0.4]),
        D(19, 35, 1.2),
    ],
    "bee": [
        L([(22, 40), (31, 33), (45, 33), (53, 40), (45, 47), (31, 47)], 2.2),
        S([(33, 34), (32, 46)], [2.6, 2.2]),
        S([(40, 33.5), (40, 47)], [2.6, 2.2]),
        S([(46, 35), (46, 45)], [2.2, 1.8]),
        D(18, 40, 3.2),
        S([(16, 37), (11, 30)], [0.9, 0.3]),
        S([(19, 36), (17, 29)], [0.9, 0.3]),
        S([(33, 33), (28, 24), (24, 18.5)], [2.4, 5.6, 0.8]),
        S([(41, 32.5), (40.5, 22), (42.5, 16)], [2.4, 5.6, 0.8]),
        S([(53, 40), (59, 41)], [1.4, 0.3]),
        D(12, 50, 0.85), D(8.5, 55, 0.75), D(6, 60, 0.65),
    ],
    "milk": [
        L([(28, 26), (42, 26), (44, 30), (41, 34), (45, 42), (45, 55), (40, 60), (30, 60),
           (25, 55), (25, 42), (29, 34), (26, 30)], 2.2),
        S([(45, 38), (52, 42), (50, 52), (45, 54)], [2.0, 2.2, 2.0, 1.4]),
        S([(28, 26), (23.5, 22.5)], [2.2, 0.7]),
        S([(29, 33), (33.5, 31), (38, 33), (41.5, 31)], [1.1, 0.9, 0.7, 0.4]),
    ],
    "egg": [
        L([(36, 26), (43, 31), (46, 42), (43, 52), (36, 56), (29, 52), (26, 42), (29, 31)], 2.2),
        S([(27, 60.5), (34, 61.5)], [1.2, 0.4]),
        S([(38, 61.5), (45, 60.5)], [1.2, 0.4]),
    ],
    "meat": [
        L([(24, 26), (33, 25), (41, 32), (44, 40), (38, 46), (28, 43), (20, 34)], 2.2),
        S([(28, 31), (34, 36)], [1.5, 0.5]),
        S([(43, 43), (51, 51)], [2.8, 2.2]),
        D(54, 50, 2.6),
        D(50, 55.5, 2.6),
    ],
    "honey": [
        L([(28, 30), (44, 30), (48, 38), (47, 48), (42, 54), (30, 54), (25, 48), (24, 38)], 2.2),
        S([(27, 34), (36, 36), (45, 34)], [1.5, 2.0, 1.5]),
        S([(31, 28.5), (41, 28.5)], [2.5, 2.5]),
        D(36, 25, 2.0),
        S([(46.5, 37), (48, 44)], [2.0, 0.6]),
    ],
    "flour": [
        L([(30, 22), (42, 22), (41, 27), (49, 34), (51, 47), (45, 59), (27, 59), (21, 47),
           (23, 34), (31, 27)], 2.2),
        S([(30, 21), (26, 15)], [2.4, 0.6]),
        S([(42, 21), (46.5, 15.5)], [2.4, 0.6]),
        S([(28.5, 24.5), (43.5, 23.5)], [1.9, 1.9]),
        S([(31, 40), (30, 52)], [1.2, 0.4]),
        S([(41, 40), (42, 52)], [1.2, 0.4]),
        D(18.5, 61, 0.9), D(53.5, 61.5, 0.8),
    ],
}

ORDER = ["cow", "chicken", "pig", "bee", "carrot", "tomato", "corn", "strawberry",
         "wheat", "milk", "egg", "meat", "honey", "flour"]

# ── flora: the wilderness variety set (F1410+) ────────────────────────

FLORA_BLOCK = 0xF1410
FLORA_DIR = ROOT / "assets" / "pua" / "flora"

FLORA_GLYPHS = {
    "birch": [
        S([(35, 62), (36, 40), (34, 18)], [2.5, 2.0, 1.5]),
        S([(33, 52), (37.5, 52)], [1.2, 0.5]),
        S([(33.5, 44), (38, 44)], [1.2, 0.5]),
        S([(33, 34), (37, 34.5)], [1.1, 0.4]),
        S([(31, 17), (23, 9)], [5.5, 1.0]),
        S([(35, 16), (34, 5)], [6.0, 1.0]),
        S([(38, 17), (46, 10)], [5.5, 1.0]),
        S([(33, 22), (27, 17)], [3.5, 0.8]),
        S([(37, 22), (43, 17)], [3.5, 0.8]),
    ],
    "willow": [
        S([(36, 62), (35, 44), (38, 30)], [3.0, 2.5, 2.0]),
        S([(38, 26), (28, 32), (24, 46)], [2.5, 1.8, 0.4]),
        S([(38, 26), (33, 34), (31, 48)], [2.5, 1.8, 0.4]),
        S([(38, 26), (40, 36), (39, 50)], [2.5, 1.8, 0.4]),
        S([(38, 26), (45, 33), (47, 47)], [2.5, 1.8, 0.4]),
        S([(38, 26), (50, 30), (54, 42)], [2.5, 1.8, 0.4]),
    ],
    "poplar": [
        L([(36, 10), (42, 22), (43, 40), (40, 52), (36, 56), (32, 52), (29, 40), (30, 22)], 2.2),
        S([(36, 56), (36, 63)], [2.5, 1.8]),
        S([(36, 18), (36, 46)], [1.0, 0.4]),
    ],
    "maple": [
        S([(36, 63), (36, 46)], [3.0, 2.2]),
        L([(36, 14), (44, 18), (51, 26), (48, 34), (40, 43), (30, 42), (23, 33), (24, 22), (30, 17)], 2.2),
    ],
    "apple": [
        S([(36, 63), (36, 46)], [3.0, 2.2]),
        S([(36, 50), (28, 43)], [2.0, 1.2]),
        S([(36, 50), (44, 43)], [2.0, 1.2]),
        L([(36, 18), (46, 22), (49, 32), (44, 42), (28, 42), (23, 32), (26, 22)], 2.2),
        D(28, 27, 1.6), D(42, 24, 1.6), D(31, 36, 1.6), D(43, 35, 1.6),
    ],
    "snag": [
        S([(36, 63), (35, 30)], [3.5, 2.0]),
        S([(35, 38), (26, 28)], [2.0, 0.6]),
        S([(26, 28), (24, 21)], [1.2, 0.4]),
        S([(35, 32), (44, 22)], [2.0, 0.6]),
        S([(44, 22), (48, 15)], [1.2, 0.4]),
        S([(35, 30), (33, 20)], [1.6, 0.5]),
    ],
    "bush": [
        L([(26, 48), (36, 42), (47, 46), (50, 54), (40, 59), (26, 58), (21, 53)], 2.2),
        S([(27, 61), (45, 61.5)], [1.2, 0.4]),
    ],
    "berrybush": [
        L([(26, 48), (36, 42), (47, 46), (50, 54), (40, 59), (26, 58), (21, 53)], 2.2),
        D(32, 50, 1.3), D(40, 48, 1.3), D(44, 53, 1.3), D(35, 55, 1.3),
        S([(27, 61), (45, 61.5)], [1.2, 0.4]),
    ],
    "fern": [
        S([(36, 60), (34, 46), (27, 34), (29, 29)], [2.0, 1.6, 0.8, 0.3]),
        S([(36, 60), (42, 48), (48, 38), (46, 33)], [2.0, 1.6, 0.8, 0.3]),
        S([(36, 60), (28, 52), (20, 48)], [1.8, 1.2, 0.3]),
        S([(36, 60), (44, 54), (51, 52)], [1.6, 1.1, 0.3]),
    ],
    "grass": [
        S([(36, 60), (30, 48), (26, 40)], [1.8, 1.2, 0.3]),
        S([(36, 60), (34, 46), (33, 38)], [1.8, 1.2, 0.3]),
        S([(36, 60), (39, 47), (42, 38)], [1.8, 1.2, 0.3]),
        S([(36, 60), (44, 52), (49, 44)], [1.6, 1.1, 0.3]),
        S([(36, 60), (28, 55), (23, 50)], [1.4, 1.0, 0.3]),
    ],
    "reed": [
        S([(32, 62), (33, 40), (33, 26)], [1.6, 1.3, 1.0]),
        S([(33, 26), (33, 15.5)], [4.5, 3.8]),
        S([(41, 62), (40, 44), (40, 32)], [1.5, 1.2, 0.9]),
        S([(40, 32), (40, 22.5)], [4.0, 3.4]),
        S([(36, 62), (44, 44), (48, 32)], [1.8, 1.2, 0.3]),
    ],
    "stump": [
        L([(28, 42), (44, 42), (45, 54), (43, 58), (29, 58), (27, 54)], 2.2),
        L([(28, 42), (36, 38.5), (44, 42), (36, 45.5)], 1.8),
        S([(33, 42), (39, 42)], [1.0, 0.5]),
        S([(28, 56), (23, 60.5)], [2.0, 0.6]),
        S([(44, 56), (49, 60.5)], [2.0, 0.6]),
    ],
}

FLORA_ORDER = ["birch", "willow", "poplar", "maple", "apple", "snag",
               "bush", "berrybush", "fern", "grass", "reed", "stump"]


CATEGORIES = [
    ("farm", GLYPHS, ORDER, BLOCK_START, OUT_DIR),
    ("flora", FLORA_GLYPHS, FLORA_ORDER, FLORA_BLOCK, FLORA_DIR),
]


def build_svg(name, glyphs, order, block, category):
    rng = random.Random(zlib.crc32((category + "/" + name).encode()))
    cp = block + order.index(name)
    polys = []
    for item in glyphs[name]:
        if item[0] == "stroke":
            polys.extend(stroke_outline(item[1], item[2], rng))
        elif item[0] == "loop":
            widths = item[2] * len(item[1]) if len(item[2]) == 1 else item[2]
            polys.extend(stroke_outline(item[1], widths, rng, closed=True))
        elif item[0] == "dot":
            polys.extend(dot(item[1], item[2], item[3], rng))
    d = " ".join(poly_to_d(p) for p in polys)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS} {CANVAS}" role="img" '
        f'aria-label="{category} / {name}" data-pua="U+{cp:05X}" '
        f'data-castalia-style="{STYLE}" data-ink-stroke-system="{STROKE_SYSTEM}">'
        f'<title>{category} / {name} — tapered-stroke synthesis</title>'
        f'<path d="{d}" fill="{INK}"/></svg>'
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", action="store_true", help="update assets/pua/manifest.json")
    args = parser.parse_args()

    for category, glyphs, order, block, out_dir in CATEGORIES:
        out_dir.mkdir(parents=True, exist_ok=True)
        for name in order:
            (out_dir / f"{name}.svg").write_text(build_svg(name, glyphs, order, block, category))
        print(f"wrote {len(order)} glyphs → {out_dir}")

    if args.manifest:
        entries = json.loads(MANIFEST.read_text())
        for category, glyphs, order, block, out_dir in CATEGORIES:
            entries = [e for e in entries if not e.get("label", "").startswith(category + "/")]
            for i, name in enumerate(order):
                cp = block + i
                entries.append({
                    "name": f"{cp:05X}",
                    "source": f"{category}/{name}.svg",
                    "codepoints": [cp],
                    "label": f"{category}/{name}",
                })
        MANIFEST.write_text(json.dumps(entries, indent=2) + "\n")
        print(f"manifest updated: {len(entries)} entries")


if __name__ == "__main__":
    main()
