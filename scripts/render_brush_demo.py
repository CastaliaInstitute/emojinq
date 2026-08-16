#!/usr/bin/env python3
"""Render a small review plate for the vector sumi brush generator."""
from pathlib import Path

from sumi_brush import BrushPoint, dry_brush_paths, stroke_path, svg_path


def main() -> None:
    stem = [BrushPoint(15, 62, .7), BrushPoint(23, 52, 1.0), BrushPoint(31, 40, 1.2), BrushPoint(40, 28, .85), BrushPoint(49, 18, .45)]
    leaf = [BrushPoint(33, 42, .5), BrushPoint(44, 38, 1.0), BrushPoint(56, 39, .75), BrushPoint(64, 34, .25)]
    crest = [BrushPoint(31, 40, .35), BrushPoint(38, 31, 1.0), BrushPoint(45, 26, .6)]
    marks = [svg_path(stroke_path(stem, width=4.0, seed="stem")), svg_path(stroke_path(leaf, width=2.7, seed="leaf")), svg_path(stroke_path(crest, width=2.0, seed="crest"))]
    marks.extend(svg_path(d, fill="#5c5b55", class_name="ink-dry") for d in dry_brush_paths(stem, width=.7, seed="stem-dry", breaks=3))
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 72" width="720" height="720" data-castalia-style="sumi-e-brush-art-v1"><rect width="72" height="72" fill="#eeeae0"/>' + ''.join(marks) + '</svg>\n'
    out = Path("build/sumi-brush-demo.svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(svg)
    print(out)


if __name__ == "__main__":
    main()
