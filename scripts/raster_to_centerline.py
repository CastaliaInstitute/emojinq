#!/usr/bin/env python3
"""Convert a raster ink reference into stroke-only, tapered SVG gestures.

AutoTrace is used in centerline mode so a dark brush mark becomes one SVG
gesture rather than the two contours produced by ordinary bitmap tracing.
The raster is an authoring reference only and is never embedded in the output.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import deque
from pathlib import Path

from PIL import Image, ImageOps
from svgpathtools import parse_path

from centerline_svg import pressure_segments, split_subpaths

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def crop_subject(image: Image.Image, threshold: int, margin: float) -> Image.Image:
    gray = ImageOps.exif_transpose(image).convert("L")
    reduced_scale = min(1.0, 256.0 / max(gray.size))
    reduced = gray.resize((max(1, round(gray.width * reduced_scale)), max(1, round(gray.height * reduced_scale))))
    mask = reduced.point(lambda value: 1 if value < threshold else 0, mode="L")
    pixels = mask.load()
    visited = bytearray(mask.width * mask.height)
    components: list[tuple[int, tuple[int, int, int, int]]] = []
    for y in range(mask.height):
        for x in range(mask.width):
            offset = y * mask.width + x
            if not pixels[x, y] or visited[offset]:
                continue
            queue = deque([(x, y)])
            visited[offset] = 1
            count = 0
            left = right = x
            top = bottom = y
            while queue:
                px, py = queue.popleft()
                count += 1
                left, right = min(left, px), max(right, px)
                top, bottom = min(top, py), max(bottom, py)
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, -1), (-1, 1), (1, 1)):
                    nx, ny = px + dx, py + dy
                    if not (0 <= nx < mask.width and 0 <= ny < mask.height):
                        continue
                    n_offset = ny * mask.width + nx
                    if pixels[nx, ny] and not visited[n_offset]:
                        visited[n_offset] = 1
                        queue.append((nx, ny))
            components.append((count, (left, top, right + 1, bottom + 1)))
    if not components:
        raise SystemExit("input contains no dark subject")
    _, bounds = max(components, key=lambda item: item[0])
    left, top, right, bottom = [round(value / reduced_scale) for value in bounds]
    pad = max(2, round(max(right - left, bottom - top) * margin))
    left, top = max(0, left - pad), max(0, top - pad)
    right, bottom = min(gray.width, right + pad), min(gray.height, bottom + pad)
    cropped = gray.crop((left, top, right, bottom))
    side = max(cropped.size)
    canvas = Image.new("L", (side, side), 255)
    canvas.paste(cropped, ((side - cropped.width) // 2, (side - cropped.height) // 2))
    return canvas


def recover(image: Image.Image, size: int, threshold: int, minimum: float, speckle: int) -> list[tuple[str, float]]:
    with tempfile.TemporaryDirectory(prefix="emojinq-raster-centerline-") as directory:
        directory = Path(directory)
        bitmap = directory / "ink.pbm"
        traced = directory / "centerline.svg"
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        image.point(lambda value: 0 if value < threshold else 255, mode="1").save(bitmap)
        subprocess.run([
            "autotrace", "--centerline", "--preserve-width",
            "--despeckle-level", str(max(0, min(20, speckle))),
            "--filter-iterations", "4", "--output-format", "svg",
            "--output-file", str(traced), str(bitmap),
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        root = ET.parse(traced).getroot()
        scale = 72.0 / size
        marks: list[tuple[str, float]] = []
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
        return sorted(marks, key=lambda item: item[1], reverse=True)


def emit(output: Path, label: str, marks: list[tuple[str, float]]) -> None:
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72",
        "role": "img",
        "aria-label": label,
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-raster-filter": "autotrace-centerline-v2",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = label
    group = ET.SubElement(root, f"{{{NS}}}g", {
        "fill": "none", "stroke-linecap": "round", "stroke-linejoin": "round",
    })
    for index, (d, length) in enumerate(marks):
        for segment, width in pressure_segments(d, length):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class": "ink-stroke",
                "data-ink-stroke": "tapered",
                "data-ink-role": "raster-centerline",
                "data-ink-index": str(index),
                "pathLength": "1",
                "d": segment,
                "stroke": "#262421" if index < max(3, len(marks) // 2) else "#4a4943",
                "stroke-width": f"{width:.2f}",
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(ET.tostring(root, encoding="unicode") + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--label", default=None)
    parser.add_argument("--size", type=int, default=256)
    parser.add_argument("--subject-threshold", type=int, default=225)
    parser.add_argument("--ink-threshold", type=int, default=205)
    parser.add_argument("--minimum", type=float, default=.65)
    parser.add_argument("--speckle", type=int, default=3)
    parser.add_argument("--margin", type=float, default=.055)
    args = parser.parse_args()
    with Image.open(args.input) as source:
        image = crop_subject(source, args.subject_threshold, args.margin)
    marks = recover(image, args.size, args.ink_threshold, args.minimum, args.speckle)
    if not marks:
        raise SystemExit("raster centerline recovery produced no usable marks")
    emit(args.output, args.label or args.output.stem, marks)
    print(f"recovered {len(marks)} raster centerline gestures: {args.input} -> {args.output}")


if __name__ == "__main__":
    main()
