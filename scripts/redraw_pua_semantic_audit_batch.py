#!/usr/bin/env python3
"""Redraw label-dependent PUA referents found in the semantic contact-sheet audit.

These are not decorative refinements.  Each drawing adds the parts that let a
small, unlabeled silhouette name its subject: a nail head and point, a pulley's
rope and load, a slide's ladder, a burrow's ear-and-hole relationship, and so
on.  This pass runs after canonical emoji transplants so its authored anatomy
is the final source seen by the font builder.
"""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUA = ROOT / "assets" / "pua"
INK = "#262522"
MID = "#66635b"
LIGHT = "#918e84"


def stroke(d: str, width: float = 3.0, color: str = INK) -> str:
    return (
        f'<path class="ink-stroke" d="{d}" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '
        'pathLength="1" data-ink-brush-pass="loaded-contour-v2"/>'
    )


def circle(cx: float, cy: float, radius: float, width: float = 2.6, color: str = INK) -> str:
    return (
        f'<circle class="ink-stroke" cx="{cx}" cy="{cy}" r="{radius}" fill="none" '
        f'stroke="{color}" stroke-width="{width}" pathLength="1" '
        'data-ink-brush-pass="loaded-contour-v2"/>'
    )


ART: dict[str, list[str]] = {
    "adventure/black-rod": [
        stroke("M15 58 L55 18", 7.0),
        circle(13, 60, 5, 3.0, MID), circle(57, 16, 5, 3.0),
        stroke("M23 50 L31 58 M28 45 L36 53", 2.0, LIGHT),
    ],
    "adventure/gold-nugget": [
        stroke("M12 48 L19 29 L35 17 L54 25 L63 43 L51 58 H25 Z", 4.0),
        stroke("M19 29 L35 36 L54 25 M35 36 L25 57 M35 36 L51 58 M35 17 V36", 2.0, MID),
        stroke("M57 12 V21 M52 17 H62 M12 18 L18 24 M18 18 L12 24", 1.8, LIGHT),
    ],
    "adventure/silver-chest": [
        stroke("M10 31 Q12 15 36 14 Q60 15 62 31 V61 H10 Z", 4.0),
        stroke("M10 32 H62 M20 17 V61 M52 17 V61", 2.6, MID),
        stroke("M30 38 H42 V49 H30 Z M34 38 V33 H38 V38", 2.4),
        stroke("M15 25 Q36 19 57 25", 1.8, LIGHT),
    ],
    "body/bones": [
        circle(36, 13, 7, 3.0),
        stroke("M36 20 V48 M25 27 Q36 22 47 27 M24 34 Q36 29 48 34 M27 41 Q36 37 45 41", 2.8),
        stroke("M25 27 L14 43 M47 27 L58 43 M36 48 L25 63 M36 48 L47 63", 3.2, MID),
        circle(33, 12, 1.2, 1.2, LIGHT), circle(39, 12, 1.2, 1.2, LIGHT),
    ],
    "body/stomach": [
        stroke("M31 8 V27 Q18 31 20 47 Q23 61 40 60 Q56 59 56 43 Q55 32 46 29 Q39 27 39 18", 4.4),
        stroke("M31 27 Q37 34 46 29 M25 48 Q35 54 47 48", 2.0, MID),
        stroke("M39 18 V8", 3.0, LIGHT),
    ],
    "science/fossil": [
        stroke("M10 18 Q35 7 60 20 Q67 36 58 56 Q35 66 12 54 Q4 36 10 18 Z", 3.0, MID),
        stroke("M18 37 Q27 26 40 30 Q48 32 54 38 Q47 45 38 45 Q26 45 18 37 Z", 3.8),
        stroke("M25 37 H49 M34 31 V44 M41 32 V44 M22 37 L15 31 M22 37 L15 44", 2.0, MID),
        circle(48, 36, 1.8, 1.5),
    ],
    "science/server": [
        stroke("M16 8 H56 Q60 8 60 12 V62 H12 V12 Q12 8 16 8 Z", 3.5),
        stroke("M17 17 H55 V28 H17 Z M17 32 H55 V43 H17 Z M17 47 H55 V58 H17 Z", 2.4, MID),
        circle(22, 22, 1.8, 1.5), circle(28, 22, 1.8, 1.5, MID),
        circle(22, 37, 1.8, 1.5), circle(28, 37, 1.8, 1.5, MID),
        circle(22, 52, 1.8, 1.5), circle(28, 52, 1.8, 1.5, MID),
        stroke("M37 22 H51 M37 37 H51 M37 52 H51", 1.8, LIGHT),
    ],
    "objects/axle": [
        stroke("M15 36 H57", 6.0),
        circle(13, 36, 10, 3.8), circle(59, 36, 10, 3.8, MID),
        circle(13, 36, 3, 2.2), circle(59, 36, 3, 2.2, MID),
        stroke("M21 30 H51 M21 42 H51", 1.8, LIGHT),
    ],
    "objects/nail": [
        stroke("M23 18 L57 52", 3.8),
        stroke("M14 20 L25 9 M14 20 L23 29", 6.5, MID),
        stroke("M57 52 L63 63 L52 57", 2.4),
        stroke("M27 23 L52 48", 1.5, LIGHT),
    ],
    "objects/oven": [
        stroke("M12 9 H60 V63 H12 Z", 3.8),
        stroke("M12 25 H60 M18 34 H54 V57 H18 Z", 2.6, MID),
        circle(21, 17, 2.5, 2.0), circle(31, 17, 2.5, 2.0, MID),
        circle(41, 17, 2.5, 2.0), circle(51, 17, 2.5, 2.0, MID),
        stroke("M26 42 Q36 35 46 42 V52 H26 Z", 1.8, LIGHT),
    ],
    "objects/pot": [
        stroke("M15 28 H57 L54 57 Q36 64 18 57 Z", 4.0),
        stroke("M20 23 Q36 17 52 23 M30 18 H42", 2.8, MID),
        stroke("M15 34 H8 M57 34 H64", 4.0),
        stroke("M27 12 Q23 7 27 3 M37 12 Q33 7 37 2 M47 12 Q43 7 47 3", 2.0, LIGHT),
    ],
    "objects/pulley": [
        stroke("M27 9 Q36 3 45 9", 3.0, MID),
        circle(36, 27, 13, 4.0), circle(36, 27, 4, 2.2, LIGHT),
        stroke("M23 27 V56 M49 27 V47", 3.2),
        stroke("M17 56 H29 V66 H17 Z", 2.8, MID),
        stroke("M49 47 Q55 51 59 47", 2.2, LIGHT),
    ],
    "objects/pump": [
        stroke("M25 62 V25 Q25 19 31 19 H43 V62", 4.0),
        stroke("M20 62 H49 M28 30 H40", 2.6, MID),
        stroke("M43 29 Q56 29 57 38 Q57 44 50 45 H45", 4.0),
        stroke("M34 18 V11 H55 M34 11 L17 23", 3.4),
        stroke("M51 48 Q55 53 51 57 Q47 53 51 48 Z", 1.8, LIGHT),
    ],
    "objects/rope": [
        stroke("M16 48 Q8 38 17 27 Q27 15 40 21 Q54 27 52 40 Q50 52 37 54 Q24 56 18 47", 5.0),
        stroke("M21 43 Q17 34 24 28 Q32 22 41 27 Q49 32 46 41 Q42 49 33 49 Q26 49 21 43", 2.2, MID),
        stroke("M50 43 Q58 46 62 54 M58 51 L65 48", 3.0),
    ],
    "objects/sandbox": [
        stroke("M7 39 H65 V62 H7 Z", 4.0),
        stroke("M8 42 Q22 35 35 42 Q50 35 64 42", 2.2, MID),
        stroke("M24 40 V29 H46 V40 M27 29 V21 H34 V29 M38 29 V19 H44 V29", 2.6),
        stroke("M53 38 L60 20 M57 20 H66 L61 27", 2.4, LIGHT),
    ],
    "objects/screw": [
        stroke("M19 13 H48 Q55 14 55 21 Q55 28 48 29 H19 Q12 28 12 21 Q12 14 19 13 Z", 3.0, MID),
        stroke("M21 21 H47", 2.4),
        stroke("M34 29 V62", 6.0),
        stroke("M27 35 L41 40 M27 43 L41 48 M27 51 L41 56 M29 59 L34 64 L39 59", 2.2, LIGHT),
    ],
    "objects/sign": [
        stroke("M9 13 H58 L65 25 L58 37 H9 Z", 3.8),
        stroke("M19 25 H52 M45 19 L53 25 L45 31", 2.6, MID),
        stroke("M31 38 V64", 5.0),
        stroke("M20 64 H43", 2.4, LIGHT),
    ],
    "objects/slide": [
        stroke("M18 14 H34 V26 Q35 39 55 55", 4.2),
        stroke("M55 55 H66", 3.2, MID),
        stroke("M18 15 V60 M34 25 L18 60", 3.2),
        stroke("M18 27 H29 M18 38 H34 M18 49 H40", 2.2, LIGHT),
    ],
    "objects/swing": [
        stroke("M8 63 L23 10 H49 L64 63", 4.0),
        stroke("M16 18 H56", 3.2, MID),
        stroke("M27 19 V49 M45 19 V49", 2.6),
        stroke("M25 49 Q36 54 47 49 L45 57 H27 Z", 3.0, MID),
    ],
    "objects/switch": [
        stroke("M17 8 H55 V64 H17 Z", 3.4),
        stroke("M27 20 H45 V52 H27 Z", 2.4, MID),
        stroke("M31 43 L41 27", 6.0),
        circle(22, 14, 1.4, 1.2, LIGHT), circle(50, 14, 1.4, 1.2, LIGHT),
        circle(22, 58, 1.4, 1.2, LIGHT), circle(50, 58, 1.4, 1.2, LIGHT),
    ],
    "objects/tower": [
        stroke("M17 16 H55 L51 63 H21 Z", 4.0),
        stroke("M15 16 V8 H23 V16 M28 16 V8 H36 V16 M41 16 V8 H49 V16 M54 16 V8 H62 V18", 3.0, MID),
        stroke("M29 63 V48 Q36 39 43 48 V63", 2.8),
        stroke("M31 27 H41 V37 H31 Z", 2.0, LIGHT),
    ],
    "objects/valve": [
        circle(36, 25, 15, 3.5), circle(36, 25, 4, 2.4, MID),
        stroke("M36 10 V40 M21 25 H51 M26 15 L46 35 M46 15 L26 35", 2.4, LIGHT),
        stroke("M36 40 V49 M23 49 H49 V61 H23 Z", 4.0),
        stroke("M7 55 H23 M49 55 H65", 5.0, MID),
    ],
    "objects/whistle": [
        stroke("M8 31 H37 Q47 20 58 27 Q68 34 62 46 Q57 55 44 51 L34 45 H8 Z", 4.0),
        stroke("M8 31 V45 M34 31 V43 H48", 2.6, MID),
        circle(53, 38, 5, 3.0),
        stroke("M12 37 H29 M44 49 Q47 60 59 61", 2.0, LIGHT),
    ],
    "objects/windowpane": [
        stroke("M10 8 H62 V64 H10 Z", 4.0),
        stroke("M36 9 V63 M11 36 H61", 3.0, MID),
        stroke("M16 30 Q25 19 34 25 M40 46 Q49 39 57 44", 1.8, LIGHT),
        stroke("M14 60 L20 53 M58 60 L52 53", 1.6, LIGHT),
    ],
    "locations/burrow": [
        stroke("M8 55 Q16 32 36 31 Q56 32 64 55", 3.2, MID),
        stroke("M21 55 Q21 39 36 37 Q51 39 51 55 Z", 5.0),
        stroke("M30 35 Q24 23 27 13 Q35 21 36 34 M40 35 Q46 23 44 13 Q36 21 36 34", 2.8, LIGHT),
        stroke("M6 57 Q20 53 32 57 Q46 53 66 58", 2.0, LIGHT),
    ],
    "locations/den": [
        stroke("M8 58 Q12 24 36 15 Q60 24 64 58", 4.0, MID),
        stroke("M21 58 Q21 37 36 33 Q51 37 51 58 Z", 5.0),
        circle(16, 49, 2.2, 1.6, LIGHT), circle(12, 44, 1.3, 1.2, LIGHT),
        circle(17, 41, 1.3, 1.2, LIGHT), circle(21, 45, 1.3, 1.2, LIGHT),
    ],
    "locations/net": [
        stroke("M13 27 Q29 8 50 21 Q62 33 50 49 Q31 61 15 43 Q8 35 13 27 Z", 3.5),
        stroke("M19 21 L52 47 M12 31 L43 55 M29 13 L58 38 M14 44 L50 20 M25 55 L58 29", 1.7, LIGHT),
        stroke("M50 49 L65 64", 5.0, MID),
    ],
    "locations/sidewalk": [
        stroke("M25 8 L7 64 M47 8 L65 64", 4.0),
        stroke("M22 18 H50 M18 30 H54 M14 43 H58 M10 57 H62", 2.0, MID),
        stroke("M31 22 Q35 17 39 22 Q36 27 31 22 Z M41 39 Q45 34 49 39 Q46 44 41 39 Z", 1.8, LIGHT),
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
        target.write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" role="img" '
            f'aria-label="{label}" {codepoint.group(0)} '
            'data-castalia-style="sumi-e-ink-wash-v1" '
            'data-ink-stroke-system="tapered-v1" '
            'data-naturalist-construction="manual-semantic-audit-v1" '
            'data-referent-review="defining-cues-expanded-v1" '
            'data-semantic-audit="label-independent-defining-parts-v1">'
            f'<title>{label} — manually audited toddler-scale sumi-e referent</title>'
            f'{"".join(marks)}</svg>\n',
            encoding="utf-8",
        )
    print(f"redrew {len(ART)} PUA referents from the semantic contact-sheet audit")


if __name__ == "__main__":
    main()
