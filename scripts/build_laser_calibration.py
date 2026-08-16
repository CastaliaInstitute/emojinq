#!/usr/bin/env python3
"""Create a small neutral-grayscale depth calibration plate for bamboo."""

from __future__ import annotations

import argparse
from pathlib import Path


LEVELS = ("#262626", "#3f3f3f", "#5a5a5a", "#777777", "#969696", "#b5b5b5", "#d4d4d4", "#eeeeee")


def build(output: Path) -> None:
    width = 800
    height = 180
    margin = 20
    gap = 8
    tile_width = (width - (2 * margin) - (gap * (len(LEVELS) - 1))) / len(LEVELS)
    rects = []
    for index, color in enumerate(LEVELS):
        x = margin + index * (tile_width + gap)
        rects.append(
            f'  <rect x="{x:.2f}" y="{margin}" width="{tile_width:.2f}" height="{height - 2 * margin}" '
            f'fill="{color}" data-laser-depth-value="{color[1:3]}" />'
        )
    svg = "\n".join(
        [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            'role="img" aria-label="Emojinq bamboo laser grayscale depth calibration" '
            'data-castalia-output="laser-grayscale-v1" '
            'data-laser-depth-encoding="neutral-luminance-linear-v1" '
            'data-laser-black="deepest" data-laser-white="lightest" data-laser-calibrate="required">',
            '  <title>Emojinq bamboo laser depth calibration — black deepest, white lightest</title>',
            *rects,
            '</svg>',
            '',
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("build/laser-calibration.svg"))
    args = parser.parse_args()
    build(args.output)
    print(f"wrote laser depth calibration plate to {args.output}")


if __name__ == "__main__":
    main()
