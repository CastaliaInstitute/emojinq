#!/usr/bin/env python3
"""Add sparse species anatomy to the dinosaur and sea-creature brush plates.

These are field-plate marks, not generic hatching: each follows a structure
that identifies the subject and remains visible when the glyph is engraved.
"""

from __future__ import annotations

import re
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path

ROOT = Path(__file__).resolve().parents[1]


def points(values):
    return [BrushPoint(*value) for value in values]


def mark(values, width, seed, color="#262522", dry=False):
    path = stroke_path(points(values), width=width, seed=f"plate-detail-{seed}", wobble=.28, taper_start=.10, taper_end=.18)
    cls = "ink-dry" if dry else "ink-wash"
    brush = "dry-fragment-v1" if dry else "loaded-ribbon-v2"
    return f'<path class="{cls}" d="{path}" fill="{color}" data-ink-brush-pass="{brush}"/>'


def fragments(values, width, seed, color="#77746a"):
    return [
        f'<path class="ink-dry" d="{path}" fill="{color}" data-ink-brush-pass="dry-fragment-v1"/>'
        for path in dry_brush_paths(points(values), width=width, seed=f"plate-detail-{seed}", breaks=2)
    ]


DETAILS = {
    "dinosaurs": {
        "ankylosaurus": [
            mark([(20, 35, .08), (28, 32, .65), (37, 33, .9), (46, 36, .08)], .62, "anky-armor", "#262522", True),
            mark([(28, 42, .08), (35, 45, .72), (44, 44, .08)], .56, "anky-belly", "#bcb9af", True),
            mark([(55, 42, .08), (60, 44, .72), (64, 42, .08)], .72, "anky-club", "#262522", True),
        ],
        "brachiosaurus": [
            mark([(48, 42, .08), (50, 34, .64), (50, 26, .92), (53, 17, .08)], .62, "brachio-neck-fold", "#262522", True),
            mark([(23, 48, .08), (32, 46, .72), (41, 48, .08)], .55, "brachio-rib", "#262522", True),
            mark([(53, 12, .08), (58, 12, .72), (63, 13, .08)], .55, "brachio-jaw", "#262522", True),
        ],
        "fossil": [
            mark([(18, 31, .08), (27, 27, .72), (36, 28, .08)], .55, "fossil-fracture-a", "#77746a", True),
            mark([(38, 50, .08), (46, 47, .72), (54, 49, .08)], .55, "fossil-fracture-b", "#77746a", True),
            *fragments([(21, 45, .08), (29, 40, .62), (38, 36, .9), (49, 31, .08)], .7, "fossil-spine", "#4a4943"),
        ],
        "parasaurolophus": [
            mark([(45, 38, .08), (51, 31, .62), (56, 23, .9), (60, 16, .08)], .62, "para-crest-ridge", "#262522", True),
            mark([(23, 39, .08), (31, 41, .72), (40, 39, .08)], .55, "para-rib", "#262522", True),
            mark([(53, 19, .08), (58, 16, .72), (63, 15, .08)], .5, "para-jaw", "#bcb9af", True),
        ],
        "pteranodon": [
            mark([(35, 31, .08), (27, 26, .62), (18, 20, .9), (9, 18, .08)], .62, "ptera-wing-finger-a", "#262522", True),
            mark([(38, 31, .08), (47, 26, .62), (57, 20, .9), (66, 18, .08)], .62, "ptera-wing-finger-b", "#262522", True),
            mark([(34, 35, .08), (38, 39, .72), (42, 42, .08)], .55, "ptera-breast", "#77746a", True),
        ],
        "spinosaurus": [
            mark([(23, 35, .08), (31, 31, .62), (40, 33, .9), (48, 36, .08)], .62, "spino-sail-rib", "#262522", True),
            mark([(28, 42, .08), (36, 45, .72), (44, 43, .08)], .56, "spino-flank", "#bcb9af", True),
            mark([(14, 40, .08), (19, 41, .72), (24, 40, .08)], .48, "spino-jaw", "#dedbd4", True),
        ],
        "stegosaurus": [
            mark([(20, 34, .08), (28, 36, .62), (38, 35, .9), (48, 37, .08)], .62, "stego-plate-edge", "#262522", True),
            mark([(28, 42, .08), (37, 45, .72), (46, 43, .08)], .56, "stego-belly", "#bcb9af", True),
            mark([(51, 42, .08), (58, 45, .72), (64, 43, .08)], .5, "stego-tail", "#262522", True),
        ],
        "triceratops": [
            mark([(20, 27, .08), (28, 30, .62), (38, 29, .9), (43, 34, .08)], .62, "trike-frill", "#262522", True),
            mark([(22, 43, .08), (31, 46, .72), (41, 44, .08)], .56, "trike-belly", "#bcb9af", True),
            mark([(20, 27, .08), (24, 24, .72), (28, 25, .08)], .52, "trike-brow", "#dedbd4", True),
        ],
        "tyrannosaurus": [
            mark([(10, 37, .08), (16, 39, .72), (23, 38, .08)], .6, "tyranno-jaw", "#dedbd4", True),
            mark([(27, 35, .08), (35, 36, .72), (44, 38, .08)], .6, "tyranno-rib", "#bcb9af", True),
            mark([(12, 39, .08), (15, 41, .72), (18, 39, .08)], .45, "tyranno-teeth", "#dedbd4", True),
        ],
        "velociraptor": [
            mark([(28, 37, .08), (35, 35, .62), (43, 37, .9), (49, 40, .08)], .58, "velo-feather-ridge", "#262522", True),
            mark([(27, 44, .08), (33, 47, .72), (40, 45, .08)], .52, "velo-belly", "#bcb9af", True),
            mark([(24, 52, .08), (28, 50, .72), (31, 51, .08)], .62, "velo-sickle", "#262522", True),
        ],
    },
    "sea_creatures": {
        "coral": [
            mark([(35, 50, .08), (30, 42, .62), (25, 34, .9), (24, 25, .08)], .58, "coral-branch-a", "#262522", True),
            mark([(39, 48, .08), (45, 41, .62), (51, 33, .9), (52, 24, .08)], .56, "coral-branch-b", "#4a4943", True),
        ],
        "crab": [
            mark([(23, 39, .08), (30, 35, .62), (38, 36, .9), (47, 39, .08)], .65, "crab-carapace", "#262522", True),
            mark([(25, 44, .08), (32, 47, .72), (41, 45, .08)], .5, "crab-belly", "#bcb9af", True),
            mark([(14, 35, .08), (10, 38, .72), (8, 42, .08)], .7, "crab-claw", "#262522", True),
        ],
        "dolphin": [
            mark([(14, 42, .08), (24, 37, .62), (35, 38, .9), (46, 42, .08)], .62, "dolphin-flank", "#262522", True),
            mark([(42, 38, .08), (47, 30, .72), (51, 26, .08)], .7, "dolphin-dorsal", "#262522", True),
            mark([(17, 43, .08), (22, 40, .72), (28, 41, .08)], .48, "dolphin-rostrum", "#bcb9af", True),
        ],
        "jellyfish": [
            mark([(18, 31, .08), (27, 26, .62), (38, 25, .9), (50, 29, .08)], .65, "jelly-bell", "#262522", True),
            mark([(23, 39, .08), (22, 48, .72), (24, 58, .08)], .52, "jelly-tentacle-a", "#77746a", True),
            mark([(39, 39, .08), (41, 50, .72), (39, 61, .08)], .52, "jelly-tentacle-b", "#262522", True),
        ],
        "lobster": [
            mark([(23, 38, .08), (31, 34, .62), (40, 35, .9), (50, 39, .08)], .62, "lobster-shell", "#262522", True),
            mark([(25, 43, .08), (33, 47, .72), (42, 46, .08)], .52, "lobster-segment", "#bcb9af", True),
            mark([(12, 31, .08), (8, 29, .72), (5, 33, .08)], .7, "lobster-claw", "#262522", True),
        ],
        "manta": [
            mark([(13, 43, .08), (24, 38, .62), (35, 41, .9), (51, 39, .08)], .6, "manta-wing", "#262522", True),
            mark([(29, 43, .08), (36, 47, .72), (44, 43, .08)], .52, "manta-belly", "#bcb9af", True),
        ],
        "nautilus": [
            mark([(25, 46, .08), (31, 39, .62), (39, 34, .9), (47, 34, .08)], .72, "nautilus-spiral", "#262522", True),
            mark([(24, 30, .08), (34, 26, .72), (46, 28, .08)], .48, "nautilus-growth", "#77746a", True),
        ],
        "octopus": [
            mark([(29, 33, .08), (35, 28, .62), (43, 30, .9), (48, 35, .08)], .62, "octopus-mantle", "#262522", True),
            mark([(22, 43, .08), (20, 50, .72), (16, 55, .08)], .5, "octopus-arm-a", "#bcb9af", True),
            mark([(44, 42, .08), (50, 48, .72), (58, 50, .08)], .5, "octopus-arm-b", "#bcb9af", True),
        ],
        "seahorse": [
            mark([(35, 27, .08), (31, 34, .62), (34, 41, .9), (42, 45, .08)], .58, "seahorse-ridge", "#262522", True),
            mark([(38, 46, .08), (35, 52, .72), (37, 57, .08)], .5, "seahorse-belly", "#bcb9af", True),
        ],
        "shark": [
            mark([(11, 42, .08), (22, 36, .62), (35, 36, .9), (49, 40, .08)], .64, "shark-flank", "#262522", True),
            mark([(24, 40, .08), (29, 43, .72), (35, 40, .08)], .5, "shark-gill", "#dedbd4", True),
            mark([(40, 35, .08), (43, 27, .72), (47, 34, .08)], .68, "shark-dorsal", "#262522", True),
        ],
        "turtle": [
            mark([(19, 39, .08), (28, 32, .62), (39, 32, .9), (50, 38, .08)], .66, "turtle-shell", "#262522", True),
            mark([(26, 36, .08), (34, 43, .72), (43, 36, .08)], .52, "turtle-scute", "#bcb9af", True),
        ],
        "whale": [
            mark([(14, 42, .08), (25, 36, .62), (38, 37, .9), (52, 41, .08)], .7, "whale-flank", "#262522", True),
            mark([(32, 34, .08), (35, 27, .72), (38, 21, .08)], .6, "whale-spout", "#77746a", True),
            mark([(22, 46, .08), (31, 49, .72), (42, 47, .08)], .5, "whale-belly", "#bcb9af", True),
        ],
    },
}


def enrich(category: str, name: str, marks: list[str]) -> None:
    path = ROOT / "assets" / "pua" / category / f"{name}.svg"
    source = path.read_text()
    if 'data-naturalist-detail="v1"' in source:
        return
    source = source.replace('data-ink-path-units="normalized"', 'data-ink-path-units="normalized" data-naturalist-detail="v1"')
    path.write_text(source.replace("</svg>", "".join(marks) + "</svg>"))


for category, names in DETAILS.items():
    for name, marks in names.items():
        enrich(category, name, marks)

print("added species-specific field-plate detail to dinosaur and sea-creature SVGs")
