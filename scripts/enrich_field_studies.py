#!/usr/bin/env python3
"""Add the second, anatomical pass to the authored field-study SVGs.

The first pass establishes the gesture.  This pass supplies the small pieces
that make a gesture read as a species: belly and shoulder contours, joints,
eyes, mouths, shell divisions, feather/fin direction, and feet.  It is kept
as a separate deterministic layer so the source remains easy to animate and
review rather than becoming a per-glyph pile of opaque geometry.
"""

from __future__ import annotations

import re
from pathlib import Path

from redraw_field_studies import INK, CHARCOAL, WASH, PALE, ROOT, line, ribbon


def add(category: str, name: str, marks: list[str]) -> None:
    path = ROOT / "assets" / "pua" / category / f"{name}.svg"
    source = path.read_text()
    if 'data-field-detail="anatomy-v2"' in source:
        return
    source = source.replace(
        'data-naturalist-construction="gesture-anatomy-v2"',
        'data-naturalist-construction="gesture-anatomy-v2" data-field-detail="anatomy-v2"',
    )
    source = source.replace("</svg>", "".join(marks) + "</svg>")
    path.write_text(source)


DETAILS: dict[tuple[str, str], list[str]] = {
    ("animals", "calf"): [
        line("M 16,43 Q 28,49 44,45 Q 51,43 56,37", 1.45, CHARCOAL),
        line("M 11,29 Q 13,31 16,30 M 8,28 Q 10,27 12,28", 1.0),
        line("M 18,55 L 16,57 M 30,56 L 28,58 M 45,55 L 43,57", 1.0, INK),
        ribbon([(23, 29, .08), (29, 27, .7), (36, 28, .08)], 1.15, "calf-shoulder", PALE),
    ],
    ("animals", "colony"): [
        line("M 13,38 Q 17,40 21,37 M 32,30 Q 36,32 40,29 M 51,40 Q 55,42 58,39", 1.0, CHARCOAL),
        line("M 14,41 L 11,45 M 19,41 L 21,45 M 33,33 L 30,37 M 39,33 L 41,37 M 51,42 L 49,46 M 56,42 L 59,46", 1.0),
        line("M 9,35 L 6,34 M 58,37 L 62,36", 1.0, WASH),
    ],
    ("animals", "flock"): [
        line("M 10,30 Q 15,26 20,31 M 31,21 Q 36,17 41,22 M 52,34 Q 57,30 62,35", 1.0, CHARCOAL),
        line("M 17,33 L 21,35 M 37,24 L 41,26 M 58,36 L 62,38", 1.0),
    ],
    ("animals", "herd"): [
        line("M 8,42 Q 16,48 25,44 M 27,40 Q 37,47 47,43 M 48,42 Q 55,46 61,42", 1.35, CHARCOAL),
        line("M 9,38 L 6,36 M 31,36 L 28,34 M 55,38 L 52,36", 1.0),
        line("M 13,56 L 11,58 M 22,57 L 20,59 M 34,56 L 32,58 M 44,56 L 42,58", 1.0),
    ],
    ("animals", "lamb"): [
        line("M 14,40 Q 23,47 35,47 Q 45,47 51,40", 1.4, CHARCOAL),
        line("M 50,36 Q 54,39 59,37 M 55,34 L 57,31", 1.0),
        line("M 19,56 L 17,58 M 31,57 L 29,59 M 44,56 L 42,58", 1.0),
        ribbon([(24, 34, .08), (30, 37, .7), (38, 34, .08)], 1.1, "lamb-wool-detail", PALE),
    ],
    ("animals", "migration"): [
        line("M 8,35 Q 14,31 20,34 M 29,27 Q 35,23 41,26 M 51,35 Q 57,31 64,34", 1.0, CHARCOAL),
        line("M 16,31 Q 17,27 19,24 M 36,23 Q 37,18 39,15 M 58,30 Q 59,26 61,23", 1.0, WASH),
    ],
    ("animals", "pack"): [
        line("M 8,41 Q 17,47 27,43 M 26,40 Q 36,46 47,43 M 45,42 Q 53,46 60,42", 1.35, CHARCOAL),
        line("M 8,37 L 4,35 M 27,36 L 23,34 M 48,39 L 44,37", 1.0),
        line("M 11,54 L 9,57 M 21,55 L 19,58 M 31,54 L 29,57 M 42,54 L 40,57", 1.0),
    ],
    ("animals", "predator"): [
        line("M 14,40 Q 27,47 42,43 Q 50,41 55,37", 1.5, CHARCOAL),
        line("M 7,28 Q 9,30 12,29 M 14,27 L 16,24 M 18,30 Q 21,28 24,29", 1.0),
        line("M 20,52 L 17,57 M 42,49 L 45,55", 1.0),
        ribbon([(27, 32, .08), (34, 34, .7), (42, 32, .08)], 1.1, "predator-rib", PALE),
    ],
    ("animals", "prey"): [
        line("M 17,43 Q 27,49 39,48 Q 47,47 51,43", 1.4, CHARCOAL),
        line("M 11,33 Q 14,35 17,34 M 20,35 Q 23,32 26,34", 1.0),
        line("M 22,54 L 20,58 M 46,54 L 49,57 M 39,40 Q 44,43 48,41", 1.0),
    ],
    ("animals", "squirrel"): [
        line("M 26,43 Q 32,49 40,48 Q 47,47 49,42", 1.45, CHARCOAL),
        line("M 20,32 Q 22,34 25,33 M 25,31 Q 28,28 30,30", 1.0),
        line("M 29,38 Q 33,41 37,40 M 30,42 L 27,45 M 38,42 L 42,45", 1.0),
        line("M 21,34 Q 18,34 16,35 M 22,36 Q 18,37 16,39", .95, CHARCOAL),
    ],

    ("dinosaurs", "ankylosaurus"): [
        line("M 8,43 Q 20,49 34,47 Q 48,46 58,42", 1.5, CHARCOAL),
        line("M 7,41 L 3,39 M 12,40 Q 15,38 18,39", 1.0),
        line("M 16,54 L 14,58 M 29,54 L 27,58 M 47,53 L 50,57", 1.0),
        line("M 20,37 Q 30,34 42,37", .95, PALE),
    ],
    ("dinosaurs", "brachiosaurus"): [
        line("M 10,49 Q 22,53 35,51 Q 44,50 48,46", 1.45, CHARCOAL),
        line("M 43,25 Q 47,27 50,25 M 48,9 L 52,7", 1.0),
        line("M 13,57 L 11,59 M 23,57 L 21,59 M 38,56 L 36,58", 1.0),
        line("M 42,35 Q 44,29 47,26", .95, PALE),
    ],
    ("dinosaurs", "fossil"): [
        line("M 17,38 Q 29,43 42,39 Q 51,36 56,30", 1.25, CHARCOAL),
        line("M 25,39 L 20,34 M 30,41 L 28,47 M 40,40 L 44,46 M 47,37 L 54,41", 1.0, WASH),
        line("M 14,16 Q 31,20 49,17 M 18,25 Q 34,28 53,24", .95, PALE, True),
    ],
    ("dinosaurs", "parasaurolophus"): [
        line("M 10,43 Q 23,48 37,46 Q 50,44 61,41", 1.45, CHARCOAL),
        line("M 15,35 L 10,33 M 20,35 Q 24,32 28,33", 1.0),
        line("M 21,55 L 19,58 M 39,55 L 37,58 M 51,54 L 49,57", 1.0),
        line("M 20,28 Q 26,25 34,22", .95, PALE),
    ],
    ("dinosaurs", "pteranodon"): [
        line("M 35,38 Q 42,42 48,39 M 35,37 Q 30,40 27,44", 1.25, CHARCOAL),
        line("M 42,34 L 48,30 M 30,32 L 24,28", .95, PALE),
        line("M 38,35 L 37,42 M 42,36 L 45,42", 1.0),
    ],
    ("dinosaurs", "spinosaurus"): [
        line("M 8,43 Q 22,48 36,46 Q 49,45 58,41", 1.45, CHARCOAL),
        line("M 9,41 L 4,38 M 13,40 Q 17,37 20,38", 1.0),
        line("M 16,55 L 14,58 M 31,55 L 29,58 M 48,54 L 50,57", 1.0),
        line("M 31,32 Q 37,28 42,31", .95, PALE),
    ],
    ("dinosaurs", "stegosaurus"): [
        line("M 8,43 Q 21,49 35,47 Q 47,46 54,42", 1.5, CHARCOAL),
        line("M 16,55 L 14,58 M 29,55 L 27,58 M 44,55 L 46,58", 1.0),
        line("M 17,36 Q 30,33 42,36", .95, PALE),
    ],
    ("dinosaurs", "triceratops"): [
        line("M 12,42 Q 25,48 38,46 Q 50,45 59,41", 1.5, CHARCOAL),
        line("M 5,30 L 2,28 M 8,31 Q 11,34 15,32", 1.0),
        line("M 11,54 L 9,58 M 25,55 L 23,58 M 44,54 L 46,58", 1.0),
        line("M 21,36 Q 33,32 45,36", .95, PALE),
    ],
    ("dinosaurs", "tyrannosaurus"): [
        line("M 16,43 Q 28,49 40,46 Q 53,44 63,42", 1.5, CHARCOAL),
        line("M 8,29 L 5,27 M 11,31 Q 15,33 19,31", 1.0),
        line("M 24,54 L 22,58 M 47,54 L 49,58", 1.0),
        line("M 18,36 Q 30,33 43,36", .95, PALE),
    ],
    ("dinosaurs", "velociraptor"): [
        line("M 13,44 Q 24,49 36,47 Q 48,46 56,42", 1.35, CHARCOAL),
        line("M 7,30 L 4,28 M 11,32 Q 14,34 18,32", 1.0),
        line("M 17,51 L 11,55 M 39,50 L 47,53", 1.0),
        line("M 23,38 Q 33,34 43,38", .95, PALE),
    ],

    ("sea_creatures", "coral"): [
        line("M 29,42 Q 25,36 24,31 M 38,38 Q 42,32 43,26", 1.0, PALE),
        line("M 21,28 L 18,24 M 29,31 L 31,25 M 43,26 L 48,21", 1.0, CHARCOAL),
    ],
    ("sea_creatures", "crab"): [
        line("M 16,44 Q 27,50 40,48 Q 51,46 56,42", 1.4, CHARCOAL),
        line("M 4,35 Q 8,37 12,35 M 60,35 Q 64,37 68,35", 1.0),
        line("M 19,45 L 13,53 M 25,46 L 22,57 M 46,46 L 50,56 M 52,44 L 59,52", 1.0),
        line("M 22,37 Q 33,34 45,37", .95, PALE),
    ],
    ("sea_creatures", "dolphin"): [
        line("M 7,43 Q 20,49 34,47 Q 49,46 61,43", 1.4, CHARCOAL),
        line("M 4,38 L 2,37 M 28,35 Q 34,38 40,36", 1.0),
        line("M 45,41 Q 52,43 58,40", 1.0, PALE),
    ],
    ("sea_creatures", "jellyfish"): [
        line("M 14,34 Q 22,39 32,36 Q 43,40 52,34", 1.25, CHARCOAL),
        line("M 20,27 Q 30,23 41,27", .95, PALE),
        line("M 22,38 Q 21,43 22,47 M 37,38 Q 38,44 37,50", 1.0, WASH),
    ],
    ("sea_creatures", "lobster"): [
        line("M 16,43 Q 28,49 41,47 Q 51,45 56,42", 1.4, CHARCOAL),
        line("M 5,29 Q 9,32 13,34 M 67,29 Q 63,32 59,34", 1.0),
        line("M 20,44 L 14,52 M 29,45 L 26,56 M 43,45 L 48,55 M 51,44 L 58,51", 1.0),
    ],
    ("sea_creatures", "manta"): [
        line("M 7,44 Q 19,50 32,48 Q 45,50 57,44", 1.45, CHARCOAL),
        line("M 20,39 Q 31,34 44,39", .95, PALE),
        line("M 33,45 L 34,52 M 9,43 L 4,41 M 57,43 L 63,41", 1.0),
    ],
    ("sea_creatures", "nautilus"): [
        line("M 16,46 Q 25,51 35,49 Q 45,47 49,41", 1.2, PALE),
        line("M 32,37 Q 35,40 39,39", 1.0, CHARCOAL),
    ],
    ("sea_creatures", "octopus"): [
        line("M 22,38 Q 30,44 38,41 Q 45,40 48,36", 1.3, CHARCOAL),
        line("M 14,49 Q 17,53 21,52 M 25,54 Q 28,58 31,55 M 42,54 Q 45,58 48,54 M 53,48 Q 56,51 59,49", 1.0),
        line("M 28,28 Q 35,24 42,28", .95, PALE),
    ],
    ("sea_creatures", "seahorse"): [
        line("M 33,24 Q 38,27 42,25 M 33,31 Q 38,34 42,32 M 35,39 Q 39,42 42,39", 1.0, PALE),
        line("M 43,16 L 48,13 M 31,48 Q 26,51 22,50", 1.0, CHARCOAL),
    ],
    ("sea_creatures", "shark"): [
        line("M 6,43 Q 20,49 35,47 Q 50,46 60,42", 1.45, CHARCOAL),
        line("M 7,41 L 2,39 M 19,37 Q 20,40 19,44", 1.0),
        line("M 24,36 Q 32,34 41,37", .95, PALE),
    ],
    ("sea_creatures", "turtle"): [
        line("M 13,44 Q 25,50 38,48 Q 49,47 54,42", 1.45, CHARCOAL),
        line("M 19,37 Q 30,40 42,36 M 25,34 L 26,43 M 38,34 L 36,43", 1.0, PALE),
        line("M 7,51 L 4,54 M 56,49 L 61,52", 1.0),
    ],
    ("sea_creatures", "whale"): [
        line("M 8,44 Q 20,50 34,48 Q 49,47 63,43", 1.5, CHARCOAL),
        line("M 4,40 L 2,39 M 30,34 Q 32,38 31,42", 1.0),
        line("M 21,37 Q 31,34 42,37", .95, PALE),
    ],
}


WASHES: dict[tuple[str, str], list[str]] = {
    ("animals", "calf"): [
        ribbon([(21, 31, .08), (27, 29, .72), (34, 30, .94), (41, 32, .08)], 3.2, "calf-wash-a", WASH),
        ribbon([(32, 34, .08), (38, 35, .72), (45, 34, .08)], 1.8, "calf-wash-b", PALE),
        ribbon([(27, 28, .08), (32, 26, .72), (38, 27, .08)], 1.0, "calf-dry", CHARCOAL, True),
    ],
    ("animals", "colony"): [
        ribbon([(13, 35, .08), (17, 33, .72), (21, 35, .08)], 1.55, "colony-wash-a", WASH),
        ribbon([(32, 27, .08), (36, 25, .72), (40, 27, .08)], 1.45, "colony-wash-b", CHARCOAL),
        ribbon([(51, 37, .08), (55, 35, .72), (59, 37, .08)], 1.35, "colony-wash-c", PALE),
    ],
    ("animals", "flock"): [
        ribbon([(9, 32, .08), (14, 29, .72), (19, 31, .08)], 1.55, "flock-wash-a", WASH),
        ribbon([(30, 23, .08), (35, 20, .72), (40, 22, .08)], 1.55, "flock-wash-b", CHARCOAL),
        ribbon([(51, 36, .08), (56, 33, .72), (61, 35, .08)], 1.45, "flock-wash-c", PALE),
    ],
    ("animals", "herd"): [
        ribbon([(11, 36, .08), (16, 34, .72), (22, 36, .08)], 2.25, "herd-wash-a", WASH),
        ribbon([(30, 34, .08), (36, 31, .72), (43, 34, .08)], 2.4, "herd-wash-b", CHARCOAL),
        ribbon([(52, 38, .08), (57, 36, .72), (62, 38, .08)], 1.7, "herd-wash-c", PALE),
    ],
    ("animals", "lamb"): [
        ribbon([(17, 34, .08), (24, 30, .72), (32, 31, .94), (40, 34, .08)], 3.0, "lamb-wash-a", PALE),
        ribbon([(21, 39, .08), (29, 43, .72), (39, 42, .08)], 2.1, "lamb-wash-b", WASH),
        ribbon([(28, 31, .08), (34, 29, .72), (40, 32, .08)], 1.0, "lamb-dry", CHARCOAL, True),
    ],
    ("animals", "migration"): [
        ribbon([(9, 33, .08), (14, 30, .72), (19, 32, .08)], 1.3, "migration-wash-a", WASH),
        ribbon([(30, 25, .08), (35, 22, .72), (40, 24, .08)], 1.3, "migration-wash-b", CHARCOAL),
    ],
    ("animals", "pack"): [
        ribbon([(10, 37, .08), (16, 34, .72), (22, 36, .08)], 2.0, "pack-wash-a", CHARCOAL),
        ribbon([(28, 36, .08), (35, 33, .72), (42, 36, .08)], 2.0, "pack-wash-b", WASH),
        ribbon([(49, 40, .08), (54, 38, .72), (59, 40, .08)], 1.55, "pack-wash-c", PALE),
    ],
    ("animals", "predator"): [
        ribbon([(22, 33, .08), (29, 30, .72), (37, 32, .08)], 3.0, "predator-wash-a", CHARCOAL),
        ribbon([(31, 36, .08), (39, 38, .72), (47, 36, .08)], 1.7, "predator-wash-b", WASH),
        ribbon([(27, 31, .08), (34, 29, .72), (40, 31, .08)], 1.0, "predator-dry", PALE, True),
    ],
    ("animals", "prey"): [
        ribbon([(26, 37, .08), (32, 34, .72), (39, 37, .08)], 2.6, "prey-wash-a", WASH),
        ribbon([(32, 41, .08), (39, 44, .72), (46, 42, .08)], 1.6, "prey-wash-b", PALE),
    ],
    ("animals", "squirrel"): [
        ribbon([(30, 36, .08), (35, 33, .72), (41, 36, .08)], 2.8, "squirrel-wash-a", WASH),
        ribbon([(34, 40, .08), (39, 43, .72), (44, 41, .08)], 1.7, "squirrel-wash-b", PALE),
        ribbon([(50, 36, .08), (54, 30, .72), (54, 24, .08)], 1.5, "squirrel-tail-dry", CHARCOAL, True),
    ],

    ("dinosaurs", "ankylosaurus"): [
        ribbon([(16, 37, .08), (24, 34, .72), (34, 35, .08)], 3.0, "anky-wash-a", WASH),
        ribbon([(28, 40, .08), (38, 41, .72), (48, 39, .08)], 1.7, "anky-wash-b", PALE),
    ],
    ("dinosaurs", "brachiosaurus"): [
        ribbon([(17, 46, .08), (27, 43, .72), (37, 45, .08)], 2.8, "brachio-wash-a", WASH),
        ribbon([(43, 33, .08), (44, 26, .72), (47, 18, .08)], 1.6, "brachio-wash-b", CHARCOAL),
    ],
    ("dinosaurs", "fossil"): [
        ribbon([(20, 15, .08), (33, 14, .72), (47, 17, .08)], 1.8, "fossil-wash", PALE),
    ],
    ("dinosaurs", "parasaurolophus"): [
        ribbon([(20, 38, .08), (29, 35, .72), (39, 37, .08)], 2.6, "para-wash-a", WASH),
        ribbon([(25, 25, .08), (30, 21, .72), (37, 19, .08)], 1.4, "para-wash-b", CHARCOAL),
    ],
    ("dinosaurs", "pteranodon"): [
        ribbon([(20, 23, .08), (26, 26, .72), (31, 31, .08)], 1.8, "ptero-wash-a", WASH),
        ribbon([(45, 31, .08), (53, 25, .72), (60, 21, .08)], 1.8, "ptero-wash-b", PALE),
    ],
    ("dinosaurs", "spinosaurus"): [
        ribbon([(17, 39, .08), (27, 35, .72), (38, 37, .08)], 2.8, "spino-wash-a", WASH),
        ribbon([(31, 32, .08), (35, 25, .72), (39, 19, .08)], 1.4, "spino-wash-b", PALE),
    ],
    ("dinosaurs", "stegosaurus"): [
        ribbon([(16, 36, .08), (25, 32, .72), (35, 34, .08)], 3.0, "stego-wash-a", WASH),
        ribbon([(29, 40, .08), (38, 42, .72), (47, 39, .08)], 1.7, "stego-wash-b", PALE),
    ],
    ("dinosaurs", "triceratops"): [
        ribbon([(22, 36, .08), (31, 33, .72), (40, 35, .08)], 2.8, "trice-wash-a", WASH),
        ribbon([(32, 40, .08), (41, 42, .72), (50, 39, .08)], 1.6, "trice-wash-b", PALE),
    ],
    ("dinosaurs", "tyrannosaurus"): [
        ribbon([(25, 37, .08), (33, 34, .72), (41, 37, .08)], 2.8, "tyrant-wash-a", CHARCOAL),
        ribbon([(33, 40, .08), (42, 42, .72), (51, 39, .08)], 1.7, "tyrant-wash-b", WASH),
    ],
    ("dinosaurs", "velociraptor"): [
        ribbon([(22, 39, .08), (30, 36, .72), (39, 39, .08)], 2.2, "velo-wash-a", WASH),
        ribbon([(30, 42, .08), (37, 44, .72), (45, 42, .08)], 1.35, "velo-wash-b", PALE),
    ],

    ("sea_creatures", "coral"): [
        ribbon([(33, 50, .08), (30, 42, .72), (26, 34, .08)], 1.8, "coral-wash-a", WASH),
        ribbon([(37, 44, .08), (40, 36, .72), (43, 29, .08)], 1.4, "coral-wash-b", PALE),
    ],
    ("sea_creatures", "crab"): [
        ribbon([(21, 39, .08), (29, 35, .72), (39, 37, .08)], 2.5, "crab-wash-a", WASH),
        ribbon([(27, 43, .08), (35, 45, .72), (44, 42, .08)], 1.5, "crab-wash-b", PALE),
    ],
    ("sea_creatures", "dolphin"): [
        ribbon([(15, 39, .08), (23, 35, .72), (32, 37, .08)], 2.6, "dolphin-wash-a", WASH),
        ribbon([(29, 41, .08), (38, 43, .72), (48, 40, .08)], 1.5, "dolphin-wash-b", PALE),
    ],
    ("sea_creatures", "jellyfish"): [
        ribbon([(19, 29, .08), (27, 25, .72), (36, 27, .08)], 2.6, "jelly-wash-a", WASH),
        ribbon([(30, 31, .08), (38, 30, .72), (46, 32, .08)], 1.3, "jelly-wash-b", PALE),
    ],
    ("sea_creatures", "lobster"): [
        ribbon([(22, 39, .08), (30, 35, .72), (40, 37, .08)], 2.5, "lobster-wash-a", WASH),
        ribbon([(29, 43, .08), (38, 45, .72), (47, 42, .08)], 1.5, "lobster-wash-b", PALE),
    ],
    ("sea_creatures", "manta"): [
        ribbon([(15, 39, .08), (24, 35, .72), (34, 38, .08)], 2.4, "manta-wash-a", WASH),
        ribbon([(35, 38, .08), (45, 35, .72), (54, 40, .08)], 1.5, "manta-wash-b", PALE),
    ],
    ("sea_creatures", "nautilus"): [
        ribbon([(20, 35, .08), (28, 29, .72), (36, 29, .08)], 2.0, "nautilus-wash", WASH),
    ],
    ("sea_creatures", "octopus"): [
        ribbon([(25, 30, .08), (33, 26, .72), (41, 29, .08)], 2.4, "octopus-wash", WASH),
        ribbon([(20, 45, .08), (25, 49, .72), (30, 46, .08)], 1.3, "octopus-arm-wash", PALE),
    ],
    ("sea_creatures", "seahorse"): [
        ribbon([(34, 24, .08), (37, 30, .72), (38, 36, .08)], 1.8, "seahorse-wash", WASH),
    ],
    ("sea_creatures", "shark"): [
        ribbon([(15, 39, .08), (25, 35, .72), (35, 37, .08)], 2.7, "shark-wash-a", CHARCOAL),
        ribbon([(31, 41, .08), (40, 43, .72), (50, 40, .08)], 1.5, "shark-wash-b", PALE),
    ],
    ("sea_creatures", "turtle"): [
        ribbon([(19, 37, .08), (28, 33, .72), (38, 36, .08)], 2.8, "turtle-wash-a", WASH),
        ribbon([(27, 41, .08), (35, 44, .72), (44, 40, .08)], 1.5, "turtle-wash-b", PALE),
    ],
    ("sea_creatures", "whale"): [
        ribbon([(16, 39, .08), (26, 34, .72), (37, 36, .08)], 3.0, "whale-wash-a", CHARCOAL),
        ribbon([(31, 42, .08), (40, 44, .72), (51, 40, .08)], 1.7, "whale-wash-b", PALE),
    ],
}


def main() -> None:
    for key, marks in DETAILS.items():
        add(*key, WASHES.get(key, []) + marks)
    print(f"added anatomical and brush detail to {len(DETAILS)} field-study SVGs")


if __name__ == "__main__":
    main()
