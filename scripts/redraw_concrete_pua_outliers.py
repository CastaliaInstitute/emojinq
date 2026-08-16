#!/usr/bin/env python3
"""Redraw concrete PUA outliers with explicit toddler-scale anatomy cues."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"
INK = '#262522'
MID = '#5f5d56'


def stroke(d: str, width: float = 3.2, color: str = INK, opacity: float | None = None) -> str:
    extra = f' opacity="{opacity}"' if opacity is not None else ""
    return (
        f'<path class="ink-stroke" d="{d}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '
        f'pathLength="1" data-ink-brush-pass="loaded-contour-v2"{extra}/>'
    )


def circle(cx: float, cy: float, radius: float, color: str = INK) -> str:
    return (
        f'<circle class="ink-wash" cx="{cx}" cy="{cy}" r="{radius}" fill="{color}" '
        'data-ink-brush-pass="loaded-mass-v2"/>'
    )


def mass(d: str, color: str = INK) -> str:
    return f'<path class="ink-wash" d="{d}" fill="{color}" data-ink-brush-pass="loaded-mass-v2"/>'


ART: dict[str, list[str]] = {
    "people/diaper": [
        stroke("M14 21 Q36 15 58 21 L53 54 Q45 61 36 51 Q27 61 19 54 Z", 3.8),
        stroke("M17 29 Q36 35 55 29", 2.4, MID),
        stroke("M19 42 Q27 37 33 48 M53 42 Q45 37 39 48", 2.4),
        stroke("M14 23 L8 27 M58 23 L64 27", 3.0, MID),
    ],
    "people/stroller": [
        stroke("M18 42 Q18 22 38 18 Q53 21 55 39 Z", 4.0),
        stroke("M38 18 L38 40 M18 42 Q36 48 55 39", 2.3, MID),
        stroke("M55 38 Q60 26 66 25", 3.0),
        stroke("M22 47 L27 55 M51 44 L47 55", 2.8),
        circle(27, 58, 5), circle(48, 58, 5, MID),
    ],
    "objects/arch": [
        stroke("M10 60 V39 Q10 13 36 12 Q62 13 62 39 V60", 4.5),
        stroke("M23 60 V41 Q23 27 36 26 Q49 27 49 41 V60", 3.2, MID),
        stroke("M12 36 H23 M49 36 H61 M17 22 L27 31 M55 22 L45 31 M36 13 V26", 1.8, MID),
    ],
    "objects/beam": [
        stroke("M9 16 H63 M9 56 H63", 5.0),
        stroke("M17 22 H55 M17 50 H55", 2.0, MID),
        stroke("M36 18 V55", 5.5),
        stroke("M27 27 L45 45 M45 27 L27 45", 1.5, MID),
    ],
    "objects/chalk": [
        stroke("M15 57 L48 24", 7.0),
        stroke("M48 24 L57 15", 4.0, MID),
        stroke("M12 61 Q27 65 42 61", 1.8, MID),
        stroke("M44 52 Q51 45 59 48", 2.0),
    ],
    "objects/clay": [
        mass("M17 52 Q18 32 29 24 Q41 17 52 29 Q61 41 53 55 Q35 61 17 52 Z", MID),
        stroke("M20 50 Q35 42 53 51 M26 34 Q36 27 47 35", 2.2),
        stroke("M8 60 Q36 56 64 60", 2.5, MID),
        circle(38, 36, 3),
    ],
    "objects/doorframe": [
        stroke("M13 62 V12 H59 V62", 4.5),
        stroke("M22 62 V21 H50 V62", 3.2, MID),
        stroke("M27 28 H45 V55 H27 Z", 1.8, MID),
        circle(44, 43, 2.8),
    ],
    "objects/foundation": [
        stroke("M9 43 H63 V62 H9 Z", 4.0),
        stroke("M9 52 H63 M22 43 V52 M47 43 V52 M34 52 V62", 2.0, MID),
        stroke("M16 42 V28 L36 14 L56 28 V42", 3.2),
    ],
    "objects/frame": [
        stroke("M10 12 H62 V60 H10 Z", 5.0),
        stroke("M20 22 H52 V50 H20 Z", 2.2, MID),
        stroke("M11 13 L20 22 M61 13 L52 22 M11 59 L20 50 M61 59 L52 50", 1.8, MID),
    ],
    "objects/handle": [
        stroke("M15 10 V62 H56 V10", 3.0, MID),
        stroke("M25 34 H51 Q58 34 58 28", 5.0),
        circle(24, 34, 4),
        stroke("M48 34 V44", 2.0, MID),
    ],
    "objects/nail": [
        stroke("M18 18 L55 55", 6.0),
        stroke("M12 13 L24 25", 9.0, MID),
        mass("M55 55 L66 64 L59 50 Z"),
        stroke("M13 55 Q30 59 45 55", 1.6, MID),
    ],
    "objects/port": [
        stroke("M11 44 H60 L52 57 H20 Z", 3.8),
        stroke("M24 43 V25 H43 L52 43", 3.0, MID),
        stroke("M31 25 V15 L48 25", 2.4),
        stroke("M7 62 Q18 57 29 62 Q40 57 51 62 Q60 58 67 61", 2.3, MID),
        stroke("M61 20 V50 M56 25 H66", 2.8),
    ],
    "objects/pottery": [
        stroke("M24 14 H48 M27 16 Q23 29 19 38 Q17 56 36 60 Q55 56 53 38 Q49 28 45 16", 4.0),
        stroke("M22 31 Q36 36 50 31 M20 46 Q36 51 52 46", 2.0, MID),
        stroke("M22 29 Q10 28 13 43 Q15 50 22 48 M50 29 Q62 28 59 43 Q57 50 50 48", 2.5),
    ],
    "objects/print": [
        stroke("M16 28 H56 Q62 28 62 35 V53 H10 V35 Q10 28 16 28 Z", 4.0),
        stroke("M21 29 V11 H51 V29 M20 46 H52 V62 H20 Z", 3.0, MID),
        stroke("M27 17 H45 M27 22 H43 M27 52 H45 M27 57 H41", 1.8),
        circle(54, 36, 2.3),
    ],
    "objects/recipe": [
        stroke("M8 18 Q22 13 35 20 V59 Q22 52 8 57 Z", 3.3),
        stroke("M64 18 Q50 13 37 20 V59 Q50 52 64 57 Z", 3.3, MID),
        stroke("M15 27 H28 M15 34 H27 M44 27 H57 M44 34 H55", 1.8),
        stroke("M47 49 Q54 43 59 48 M53 44 V37", 2.5),
    ],
    "objects/roof": [
        stroke("M7 45 L34 15 L65 45", 5.0),
        stroke("M16 44 Q35 37 57 44 M24 34 Q36 29 49 34", 2.0, MID),
        stroke("M48 27 V13 H57 V36", 3.5),
    ],
    "objects/sculpture": [
        circle(36, 18, 8, MID),
        mass("M22 44 Q23 28 36 27 Q49 28 50 44 Q42 49 30 46 Z"),
        stroke("M18 47 H54 V58 H18 Z M13 62 H59", 3.5, MID),
        stroke("M32 17 Q36 20 40 17 M33 23 Q36 25 39 23", 1.4),
    ],
    "objects/stove": [
        stroke("M11 17 H61 V58 H11 Z", 4.0),
        stroke("M16 32 H56 M18 38 H54 V54 H18 Z", 2.2, MID),
        circle(22, 24, 3), circle(32, 24, 3, MID), circle(42, 24, 3), circle(52, 24, 3, MID),
        stroke("M27 45 Q36 39 45 45 V52 H27 Z", 1.8),
    ],
    "locations/barn": [
        stroke("M9 34 L36 12 L63 34 V62 H9 Z", 4.3),
        stroke("M23 62 V38 H49 V62 M23 38 L49 62 M49 38 L23 62", 2.7, MID),
        stroke("M16 30 V20 H25", 2.5),
    ],
    "locations/bench": [
        stroke("M12 24 H60 M12 34 H60 M10 43 H62", 4.0),
        stroke("M16 20 V58 M56 20 V58", 3.2, MID),
        stroke("M9 46 H63 M18 46 L14 61 M54 46 L58 61", 2.8),
    ],
    "locations/crossing": [
        stroke("M8 18 L64 55 M8 55 L64 18", 2.0, MID),
        stroke("M12 49 L20 54 M20 41 L29 47 M29 34 L38 40 M38 27 L47 33 M47 20 L56 26", 6.0),
        circle(36, 12, 4),
        stroke("M36 17 V28 M36 21 L28 27 M36 22 L44 27 M36 28 L30 36 M36 28 L42 36", 2.8),
    ],
    "locations/rug": [
        stroke("M13 15 H59 V57 H13 Z", 4.0),
        stroke("M24 27 L36 19 L48 27 L36 49 L24 27 Z", 2.4, MID),
        stroke("M13 20 L7 17 M13 29 L7 27 M13 43 L7 45 M13 52 L7 55 M59 20 L65 17 M59 29 L65 27 M59 43 L65 45 M59 52 L65 55", 1.8),
    ],
    "locations/silo": [
        stroke("M20 24 Q20 10 36 10 Q52 10 52 24 V62 H20 Z", 4.2),
        stroke("M21 26 H51 M21 39 H51 M21 52 H51", 2.0, MID),
        stroke("M31 62 V49 H42 V62", 2.5),
        stroke("M52 29 H61 V61 M56 35 H61 M56 44 H61 M56 53 H61", 2.2),
    ],
    "science/reservoir": [
        stroke("M7 27 Q18 18 29 25 Q40 32 51 23 Q60 17 66 23", 2.4, MID),
        stroke("M47 20 L55 60 H66 L60 18 Z", 5.0),
        stroke("M7 38 Q18 32 29 38 Q40 44 51 37 M7 49 Q18 43 29 49 Q40 55 53 47", 3.0),
    ],
    "science/windmill": [
        circle(36, 29, 4),
        stroke("M36 25 L27 7 L34 5 L39 25 M40 29 L60 19 L63 26 L42 33 M36 33 L46 54 L39 57 L32 35 M32 29 L12 39 L9 32 L30 25", 3.2),
        stroke("M31 34 L25 65 H47 L41 34 M28 52 H44", 3.0, MID),
    ],
}


def main() -> None:
    for source, marks in ART.items():
        target = PUA / f"{source}.svg"
        old = target.read_text(encoding="utf-8")
        codepoint = re.search(r'data-pua="([^"]+)"', old)
        if not codepoint:
            raise SystemExit(f"{target}: missing PUA code point")
        label = source.replace("/", " / ").replace("_", " ")
        has_wash = any('class="ink-wash"' in mark for mark in marks)
        style = "sumi-e-naturalist-v2" if has_wash else "sumi-e-ink-wash-v1"
        stroke_system = "filled-brush-mass-v2" if has_wash else "tapered-v1"
        target.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" '
            f'aria-label="{label}" {codepoint.group(0)} '
            f'data-castalia-style="{style}" '
            f'data-ink-stroke-system="{stroke_system}" '
            'data-naturalist-construction="explicit-toddler-anatomy-v1" '
            'data-referent-review="defining-cues-expanded-v1">'
            f'<title>{label} — explicit toddler-scale sumi-e anatomy</title>'
            f'{"".join(marks)}</svg>\n',
            encoding="utf-8",
        )
    print(f"redrew {len(ART)} concrete PUA recognition outliers")


if __name__ == "__main__":
    main()
