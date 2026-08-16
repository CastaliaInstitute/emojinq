#!/usr/bin/env python3
"""Trace a raster ink reference into a clean, grayscale Emojinq SVG.

This is an authoring filter, not a promise that a generic auto-tracer
understands anatomy.  Its default mode traces centerline gestures, joins
nearby fragments, and emits a small set of tapered brush ribbons.  The result is
portable to the browser, the font builder, ESP32 rasterization, and the
bamboo laser export without carrying the source raster or SVG effects.

Run with the optional dependencies through uv, for example::

    uv run --python 3.12 --with vtracer --with pillow --with svgpathtools \
      python scripts/trace_raster_brush.py reference.png assets/pua/animals/squirrel.svg
"""

from __future__ import annotations

import argparse
from collections import deque
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    from PIL import Image, ImageFilter, ImageOps
    import vtracer
    from svgpathtools import parse_path
except ImportError as exc:  # pragma: no cover - exercised by the CLI
    raise SystemExit(
        "This filter needs Pillow, vtracer, svgpathtools, and the autotrace "
        "command. Run it with `uv run --python 3.12 --with vtracer "
        "--with pillow --with svgpathtools "
        "--with svgpathtools python "
        "scripts/trace_raster_brush.py ...`."
    ) from exc

try:
    from sumi_brush import BrushPoint, stroke_path
except ImportError as exc:  # pragma: no cover - direct invocation from repo root
    raise SystemExit("run this script from the repository so scripts/sumi_brush.py is importable") from exc


SVG_NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", SVG_NS)
# Sixteen neutral depth steps retain wash structure while staying simple
# enough for font rasterization and bamboo laser power mapping.
PALETTE = tuple((level, f"#{level:02x}{level:02x}{level:02x}") for level in range(224, 23, -16))
TRANSLATE_RE = re.compile(r"translate\(\s*([-+0-9.eE]+)[ ,]+([-+0-9.eE]+)\s*\)")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def traced_paths(image: Image.Image, *, speckle: int) -> list[tuple[str, float, float, int]]:
    """Trace grayscale tone regions and return d, translation, and luminance."""
    rgba = image.convert("RGBA")
    pixels = rgba.get_flattened_data() if hasattr(rgba, "get_flattened_data") else list(rgba.getdata())
    raw = vtracer.convert_pixels_to_svg(
        pixels,
        rgba.size,
        colormode="gray",
        filter_speckle=speckle,
        color_precision=6,
        layer_difference=16,
        corner_threshold=60,
        length_threshold=4,
        max_iterations=12,
        path_precision=4,
    )
    root = ET.fromstring(raw)
    paths: list[tuple[str, float, float, int]] = []
    for element in root.iter():
        if local(element.tag) != "path" or not element.get("d"):
            continue
        transform = TRANSLATE_RE.search(element.get("transform", ""))
        tx, ty = (float(transform.group(1)), float(transform.group(2))) if transform else (0.0, 0.0)
        paint = element.get("fill", "#000000").lstrip("#")
        try:
            red, green, blue = (int(paint[index:index + 2], 16) for index in (0, 2, 4))
            luminance = round(0.2126 * red + 0.7152 * green + 0.0722 * blue)
        except (ValueError, IndexError):
            luminance = 0
        paths.append((element.get("d", ""), tx, ty, luminance))
    return paths


def crop_ink(image: Image.Image, margin: float) -> Image.Image:
    """Remove the paper surround while retaining a small breathing margin."""
    # Keep the reference's tonal hierarchy.  Autocontrast makes a pale
    # naturalist wash collapse into a single heavy silhouette.
    gray = image.convert("L")
    # Work on a reduced mask to isolate the dominant subject. This prevents a
    # seal, caption, or stray border from defining the glyph crop.
    reduced_scale = min(1.0, 256.0 / max(gray.width, gray.height))
    reduced = gray.resize((max(1, round(gray.width * reduced_scale)), max(1, round(gray.height * reduced_scale))))
    mask = reduced.point(lambda value: 1 if value < 225 else 0, mode="L")
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
                for dx, dy in ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)):
                    nx, ny = px + dx, py + dy
                    if not (0 <= nx < mask.width and 0 <= ny < mask.height):
                        continue
                    n_offset = ny * mask.width + nx
                    if pixels[nx, ny] and not visited[n_offset]:
                        visited[n_offset] = 1
                        queue.append((nx, ny))
            components.append((count, (left, top, right + 1, bottom + 1)))
    if not components:
        raise SystemExit("input contains no dark artwork")
    _, reduced_bbox = max(components, key=lambda item: item[0])
    bbox = tuple(round(value / reduced_scale) for value in reduced_bbox)
    if bbox is None:
        raise SystemExit("input contains no dark artwork")
    left, top, right, bottom = bbox
    width, height = right - left, bottom - top
    pad = max(2, round(max(width, height) * margin))
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(gray.width, right + pad)
    bottom = min(gray.height, bottom + pad)
    return gray.crop((left, top, right, bottom))


def fit_square(image: Image.Image, size: int) -> Image.Image:
    """Put the cropped reference on a square paper field for stable geometry."""
    scale = min((size - 2) / image.width, (size - 2) / image.height)
    resized = image.resize(
        (max(1, round(image.width * scale)), max(1, round(image.height * scale))),
        Image.Resampling.LANCZOS,
    )
    canvas = Image.new("L", (size, size), 255)
    offset = ((size - resized.width) // 2, (size - resized.height) // 2)
    canvas.paste(resized, offset)
    return canvas


def autotrace_strokes(
    image: Image.Image,
    *,
    size: int,
    threshold: int,
    minimum: float,
    speckle: int,
    bridge: int,
) -> list[tuple[str, str]]:
    """Use AutoTrace centerline mode, then turn each line into a brush ribbon."""
    import subprocess
    import tempfile

    gray = image.convert("L")
    mask = gray.point(lambda value: 0 if value < threshold else 255, mode="L").convert("1")
    if bridge:
        kernel = max(3, bridge * 2 + 1)
        if kernel % 2 == 0:
            kernel += 1
        # Join nearby fragments before centerline tracing. This is a modest
        # structural bridge, not a blur: the resulting SVG still contains
        # separate tapered brush ribbons.
        mask = mask.filter(ImageFilter.MinFilter(kernel)).filter(ImageFilter.MaxFilter(kernel))
    scale = 72.0 / size
    with tempfile.TemporaryDirectory(prefix="emojinq-autotrace-") as directory:
        directory_path = Path(directory)
        bitmap = directory_path / "ink.pbm"
        traced = directory_path / "centerline.svg"
        mask.save(bitmap)
        try:
            subprocess.run(
                [
                    "autotrace", "--centerline", "--preserve-width",
                    "--despeckle-level", str(min(20, max(0, speckle))),
                    "--filter-iterations", "4", "--output-format", "svg",
                    "--output-file", str(traced), str(bitmap),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as exc:
            raise SystemExit("the stroke filter needs AutoTrace (`brew install autotrace`)") from exc
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"autotrace failed: {exc.stderr.strip()}") from exc
        root = ET.parse(traced).getroot()
        output: list[tuple[str, str]] = []
        index = 0
        for element in root.iter():
            if local(element.tag) != "path" or not element.get("d"):
                continue
            for part in re.split(r"(?=M\s*[-+0-9])", element.get("d", "")):
                part = part.strip()
                if not part:
                    continue
                try:
                    path = parse_path(part)
                    length = path.length()
                except (ValueError, ZeroDivisionError):
                    continue
                if length * scale < minimum:
                    continue
                count = max(3, min(40, round(length / 3.5)))
                points = []
                source_points = []
                for sample_index in range(count):
                    point = path.point(sample_index / (count - 1))
                    source_points.append(point)
                    points.append(BrushPoint(point.real * scale, point.imag * scale, 0.78 + 0.22 * (sample_index / (count - 1))))
                source_pixels = [
                    gray.getpixel((max(0, min(size - 1, round(point.real))), max(0, min(size - 1, round(point.imag)))))
                    for point in source_points
                ]
                mean_ink = sum(source_pixels) / len(source_pixels)
                width = max(0.45, min(1.8, 0.62 + (255.0 - mean_ink) / 150.0 + length * scale / 180.0))
                d = stroke_path(
                    points,
                    width=width,
                    seed=f"autotrace-brush-{index}",
                    wobble=0.12,
                    taper_start=0.05,
                    taper_end=0.18,
                )
                output.append((d, "#292825" if mean_ink < 150 else "#4a4741"))
                index += 1
        return output


def autotrace_outline_strokes(
    image: Image.Image,
    *,
    size: int,
    threshold: int,
    minimum: float,
    speckle: int,
    bridge: int,
    budget: int,
) -> list[tuple[str, str]]:
    """Trace the dominant silhouette contours as a small brush vocabulary."""
    import subprocess
    import tempfile

    gray = image.convert("L")
    mask = gray.point(lambda value: 0 if value < threshold else 255, mode="L").convert("1")
    if bridge:
        kernel = max(3, bridge * 2 + 1)
        if kernel % 2 == 0:
            kernel += 1
        mask = mask.filter(ImageFilter.MinFilter(kernel)).filter(ImageFilter.MaxFilter(kernel))
    scale = 72.0 / size
    with tempfile.TemporaryDirectory(prefix="emojinq-autotrace-outline-") as directory:
        directory_path = Path(directory)
        bitmap = directory_path / "ink.pbm"
        traced = directory_path / "outline.svg"
        mask.save(bitmap)
        try:
            subprocess.run(
                [
                    "autotrace", "--despeckle-level", str(min(20, max(0, speckle))),
                    "--filter-iterations", "4", "--output-format", "svg",
                    "--output-file", str(traced), str(bitmap),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError as exc:
            raise SystemExit("the stroke filter needs AutoTrace (`brew install autotrace`)") from exc
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"autotrace failed: {exc.stderr.strip()}") from exc
        root = ET.parse(traced).getroot()
        candidates: list[tuple[float, object]] = []
        for element in root.iter():
            if local(element.tag) != "path" or "#000000" not in element.get("style", "").lower():
                continue
            for part in re.split(r"(?=M\s*[-+0-9])", element.get("d", "")):
                part = part.strip()
                if not part:
                    continue
                try:
                    path = parse_path(part)
                    length = path.length()
                except (ValueError, ZeroDivisionError):
                    continue
                if length * scale >= minimum:
                    candidates.append((length, path))
        candidates.sort(key=lambda item: item[0], reverse=True)
        output: list[tuple[str, str]] = []
        for index, (length, path) in enumerate(candidates[:max(1, budget)]):
            count = max(5, min(72, round(length / 3.0)))
            points = []
            for sample_index in range(count):
                t = sample_index / (count - 1)
                point = path.point(t)
                points.append(BrushPoint(point.real * scale, point.imag * scale, 0.72 + 0.28 * (1.0 - abs(0.5 - t) * 2.0)))
            width = max(0.52, min(1.8, 0.70 + length * scale / 220.0))
            output.append((stroke_path(points, width=width, seed=f"outline-brush-{index}", wobble=0.10, taper_start=.06, taper_end=.14), "#292825"))
        return output


def emit_path(
    path_data: str,
    tx: float,
    ty: float,
    source_size: int,
    target_size: float,
    margin: float,
) -> str | None:
    """Bake the trace scale into path data; avoid SVG transforms."""
    try:
        path = parse_path(path_data).translated(complex(tx, ty))
        scaled = path.scaled(target_size / source_size)
        # A tiny component is usually paper noise or a detached tracer speck.
        xmin, xmax, ymin, ymax = scaled.bbox()
        if max(xmax - xmin, ymax - ymin) < margin:
            return None
        return scaled.d()
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="PNG/JPEG raster ink reference")
    parser.add_argument("output", type=Path, help="SVG destination")
    parser.add_argument("--size", type=int, default=256, help="tracing raster size")
    parser.add_argument("--view-size", type=float, default=72, help="SVG viewBox size")
    parser.add_argument("--mode", choices=("outline", "strokes", "masses"), default="outline")
    parser.add_argument("--stroke-threshold", type=int, default=160, help="darkness cutoff for centerline extraction")
    parser.add_argument("--min-stroke", type=float, default=1.0, help="minimum brush length in viewBox units")
    parser.add_argument("--bridge", type=int, default=3, help="join nearby raster fragments before centerline tracing")
    parser.add_argument("--stroke-budget", type=int, default=14, help="maximum number of dominant outline gestures")
    parser.add_argument("--paper-margin", type=float, default=0.055)
    parser.add_argument("--min-component", type=float, default=0.22)
    parser.add_argument("--speckle", type=int, default=8)
    parser.add_argument("--label", default=None)
    parser.add_argument("--codepoint", default=None)
    args = parser.parse_args()

    with Image.open(args.input) as source:
        image = crop_ink(ImageOps.exif_transpose(source).convert("RGB"), args.paper_margin)
    image = fit_square(image, args.size)

    root = ET.Element(
        f"{{{SVG_NS}}}svg",
        {
            "version": "1.1",
            "width": f"{args.view_size:g}",
            "height": f"{args.view_size:g}",
            "viewBox": f"0 0 {args.view_size:g} {args.view_size:g}",
            "data-castalia-style": "sumi-e-naturalist-v2",
            "data-ink-stroke-system": "filled-ribbon-v1" if args.mode in {"outline", "strokes"} else "filled-brush-mass-v2",
            "data-ink-source": "raster-trace-v1",
            "data-ink-animation": "wash-v1",
            "data-ink-path-units": "normalized",
            "data-raster-filter": "autotrace-outline-brush-v1" if args.mode == "outline" else ("autotrace-centerline-brush-v2" if args.mode == "strokes" else "vtracer-grayscale-mass-v1"),
        },
    )
    title = ET.SubElement(root, f"{{{SVG_NS}}}title")
    title.text = args.label or args.output.stem.replace("_", " ")
    if args.codepoint:
        root.set("data-codepoint", args.codepoint)

    count = 0
    if args.mode == "outline":
        for d, color in autotrace_outline_strokes(
            image, size=args.size, threshold=args.stroke_threshold, minimum=args.min_stroke,
            speckle=args.speckle, bridge=args.bridge, budget=args.stroke_budget,
        ):
            ET.SubElement(root, f"{{{SVG_NS}}}path", {
                "class": "ink-wash", "d": d, "fill": color,
                "data-ink-brush-pass": "dominant-outline-ribbon-v1",
            })
            count += 1
    elif args.mode == "strokes":
        # The default is deliberately centerline-first: a raster mass becomes
        # a set of pressure-shaped brush gestures, never a filled silhouette.
        for index, (d, color) in enumerate(
            autotrace_strokes(image, size=args.size, threshold=args.stroke_threshold, minimum=args.min_stroke, speckle=args.speckle, bridge=args.bridge)
        ):
            ET.SubElement(root, f"{{{SVG_NS}}}path", {
                "class": "ink-wash",
                "d": d,
                "fill": color,
                "data-ink-brush-pass": "skeleton-ribbon-v1",
                "data-ink-stroke-index": str(index),
            })
            count += 1
    else:
        # Optional comparison mode for source review; not the production
        # default because it turns broad wash regions into solid masses.
        traced = traced_paths(image, speckle=args.speckle)
        for raw_path, tx, ty, luminance in sorted(traced, key=lambda item: item[3], reverse=True):
            if luminance > 225:
                continue
            d = emit_path(raw_path, tx, ty, args.size, args.view_size, args.min_component)
            if not d:
                continue
            color = next((paint for limit, paint in PALETTE if luminance >= limit), PALETTE[-1][1])
            ET.SubElement(root, f"{{{SVG_NS}}}path", {"d": d, "fill": color})
            count += 1

    if not count:
        raise SystemExit("tracing produced no usable vector paths")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(ET.tostring(root, encoding="unicode") + "\n")
    print(f"traced {args.input} -> {args.output} ({count} {args.mode} brush paths)")


if __name__ == "__main__":
    main()
