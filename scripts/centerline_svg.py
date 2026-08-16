#!/usr/bin/env python3
"""Recover single centerline brush gestures from a filled source SVG.

This is deliberately an authoring filter. It rasterizes one source glyph,
uses AutoTrace centerline mode to avoid paired outline contours, then emits
scaled, stroke-only SVG paths. The result must still pass visual review; this
tool is not an anatomy-aware redraw system.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image
from svgpathtools import parse_path

ROOT = Path(__file__).resolve().parents[1]
SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)


def split_subpaths(d: str) -> list[str]:
    return [part.strip() for part in re.split(r"(?=M\s*[-+0-9])", d) if part.strip()]


def pressure_segments(d: str, length: float) -> list[tuple[str, float]]:
    """Return overlapping sampled pieces with a broad-nib pressure profile."""
    try:
        path = parse_path(d)
    except (TypeError, ValueError, ZeroDivisionError):
        return []
    base = max(.48, min(1.45, .56 + length / 190.0))
    if path.isclosed():
        return [(d, base)]
    pieces = 4
    sample_count = max(24, min(96, round(length * 2.4)))
    points = [path.point(index / (sample_count - 1)) for index in range(sample_count)]
    result: list[tuple[str, float]] = []
    for piece in range(pieces):
        start = max(0, round(piece * (sample_count - 1) / pieces) - 1)
        end = min(sample_count - 1, round((piece + 1) * (sample_count - 1) / pieces) + 1)
        if end <= start:
            continue
        commands = [f"M {points[start].real:.3f} {points[start].imag:.3f}"]
        commands.extend(f"L {point.real:.3f} {point.imag:.3f}" for point in points[start + 1:end + 1])
        midpoint = (piece + .5) / pieces
        pressure = .56 + .44 * (1.0 - abs(midpoint - .5) * 1.3)
        result.append((" ".join(commands), base * pressure))
    return result


def crop_square(image: Image.Image, margin: float) -> Image.Image:
    gray = image.convert("L")
    mask = gray.point(lambda value: 255 if value < 244 else 0, mode="L")
    bbox = mask.getbbox()
    if not bbox:
        raise SystemExit("source rendered without visible ink")
    left, top, right, bottom = bbox
    pad = max(2, round(max(right - left, bottom - top) * margin))
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(gray.width, right + pad)
    bottom = min(gray.height, bottom + pad)
    cropped = gray.crop((left, top, right, bottom))
    side = max(cropped.size)
    canvas = Image.new("L", (side, side), 255)
    canvas.paste(cropped, ((side - cropped.width) // 2, (side - cropped.height) // 2))
    return canvas


def trace(source: Path, *, size: int, threshold: int, minimum: float, speckle: int) -> list[tuple[str, float]]:
    with tempfile.TemporaryDirectory(prefix="emojinq-centerline-") as directory:
        directory = Path(directory)
        raster = directory / "source.png"
        mask = directory / "source.pbm"
        traced = directory / "centerline.svg"
        subprocess.run(
            ["rsvg-convert", "--background-color=#ffffff", "-w", str(size), "-h", str(size), str(source), "-o", str(raster)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        with Image.open(raster) as image:
            image = crop_square(image, .055)
            image = image.resize((size, size), Image.Resampling.LANCZOS)
            image = image.point(lambda value: 0 if value < threshold else 255, mode="1")
            image.save(mask)
        subprocess.run(
            [
                "autotrace", "--centerline", "--preserve-width",
                "--despeckle-level", str(max(0, min(20, speckle))),
                "--filter-iterations", "4", "--output-format", "svg",
                "--output-file", str(traced), str(mask),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        root = ET.parse(traced).getroot()
        marks: list[tuple[str, float]] = []
        scale = 72.0 / size
        for element in root.iter():
            if element.tag.rsplit("}", 1)[-1] != "path":
                continue
            for raw in split_subpaths(element.get("d", "")):
                try:
                    path = parse_path(raw)
                    length = path.length() * scale
                    scaled = path.scaled(scale)
                except (TypeError, ValueError, ZeroDivisionError):
                    continue
                if length >= minimum:
                    marks.append((scaled.d(), length))
        # Keep the structural gestures first, but retain short facial/detail
        # marks that are long enough to survive a 72-unit glyph.
        marks.sort(key=lambda item: item[1], reverse=True)
        return marks


def emit(source: Path, output: Path, marks: list[tuple[str, float]], label: str | None, codepoint: str | None) -> None:
    root = ET.Element(f"{{{SVG_NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": label or source.stem,
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-centerline-source": "autotrace-centerline-v1",
    })
    if codepoint:
        root.set("data-pua", codepoint)
    title = ET.SubElement(root, f"{{{SVG_NS}}}title")
    title.text = label or source.stem
    group = ET.SubElement(root, f"{{{SVG_NS}}}g", {
        "fill": "none", "stroke-linecap": "round", "stroke-linejoin": "round",
    })
    output_index = 0
    for index, (d, length) in enumerate(marks):
        # Longer structural gestures carry more body; short marks recede like
        # dry-brush detail. The overlapping pieces keep the taper continuous
        # at the joins while remaining ordinary SVG strokes.
        pieces = pressure_segments(d, length)
        color = "#262421" if index < max(3, len(marks) // 2) else "#4a4943"
        for piece_d, width in pieces:
            ET.SubElement(group, f"{{{SVG_NS}}}path", {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": "centerline-recovered",
                "data-ink-index": str(output_index),
                "pathLength": "1",
                "d": piece_d,
                "stroke": color,
                "stroke-width": f"{width:.2f}",
            })
            output_index += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--threshold", type=int, default=220)
    parser.add_argument("--minimum", type=float, default=.65)
    parser.add_argument("--speckle", type=int, default=3)
    parser.add_argument("--label")
    parser.add_argument("--codepoint")
    args = parser.parse_args()
    marks = trace(args.source, size=args.size, threshold=args.threshold, minimum=args.minimum, speckle=args.speckle)
    if not marks:
        raise SystemExit("centerline recovery produced no usable marks")
    emit(args.source, args.output, marks, args.label, args.codepoint)
    print(f"recovered {len(marks)} centerline brush gestures: {args.source} -> {args.output}")


if __name__ == "__main__":
    main()
