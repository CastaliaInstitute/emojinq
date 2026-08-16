#!/usr/bin/env python3
"""Convert Yuji outline glyphs into topology-preserving tapered strokes."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.morphology import skeletonize

from collapse_lines import roughen_path
from centerline_svg import pressure_segments

NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def neighbors(point: tuple[int, int], points: set[tuple[int, int]]) -> list[tuple[int, int]]:
    x, y = point
    return [
        candidate for candidate in (
            (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        ) if candidate in points
    ]


def edge_key(a: tuple[int, int], b: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
    return (a, b) if a <= b else (b, a)


def simplify(points: list[tuple[int, int]], epsilon: float = 1.2) -> list[tuple[int, int]]:
    if len(points) <= 2:
        return points
    start, end = np.array(points[0], dtype=float), np.array(points[-1], dtype=float)
    line = end - start
    length = float(np.linalg.norm(line))
    if length == 0:
        distances = [float(np.linalg.norm(np.array(point, dtype=float) - start)) for point in points]
    else:
        distances = [
            abs(float(line[0] * (np.array(point, dtype=float) - start)[1] - line[1] * (np.array(point, dtype=float) - start)[0])) / length
            for point in points
        ]
    index = max(range(len(distances)), key=distances.__getitem__)
    if distances[index] <= epsilon:
        return [points[0], points[-1]]
    return simplify(points[: index + 1], epsilon)[:-1] + simplify(points[index:], epsilon)


def trace_graph(mask: np.ndarray, minimum: float) -> list[list[tuple[int, int]]]:
    points = {(int(x), int(y)) for y, x in np.argwhere(mask)}
    adjacency = {point: neighbors(point, points) for point in points}
    nodes = {point for point in points if len(adjacency[point]) != 2}
    visited: set[tuple[tuple[int, int], tuple[int, int]]] = set()
    paths: list[list[tuple[int, int]]] = []

    # A punctuation dot can skeletonize to one pixel. Preserve it as a tiny
    # closed brush dab instead of dropping the glyph as empty.
    for point, connected in adjacency.items():
        if not connected:
            x, y = point
            paths.append([(x - 2, y), (x, y - 2), (x + 2, y), (x, y + 2), (x - 2, y)])

    def walk(start: tuple[int, int], first: tuple[int, int]) -> list[tuple[int, int]]:
        path = [start]
        previous, current = start, first
        visited.add(edge_key(previous, current))
        path.append(current)
        while current not in nodes:
            choices = [item for item in adjacency[current] if item != previous]
            if not choices:
                break
            following = choices[0]
            if edge_key(current, following) in visited:
                break
            visited.add(edge_key(current, following))
            previous, current = current, following
            path.append(current)
        return path

    for node in sorted(nodes):
        for first in adjacency[node]:
            if edge_key(node, first) in visited:
                continue
            path = simplify(walk(node, first))
            if len(path) > 1 and sum(np.linalg.norm(np.subtract(path[i], path[i - 1])) for i in range(1, len(path))) >= minimum:
                paths.append(path)

    # Closed skeleton loops have no endpoints or junctions.
    for start in sorted(points):
        for first in adjacency[start]:
            if edge_key(start, first) in visited:
                continue
            path = [start]
            previous, current = start, first
            visited.add(edge_key(previous, current))
            path.append(current)
            while current != start:
                choices = [item for item in adjacency[current] if item != previous]
                if not choices:
                    break
                following = choices[0]
                if edge_key(current, following) in visited:
                    break
                visited.add(edge_key(current, following))
                previous, current = current, following
                path.append(current)
            path = simplify(path)
            if len(path) > 1 and sum(np.linalg.norm(np.subtract(path[i], path[i - 1])) for i in range(1, len(path))) >= minimum:
                paths.append(path)
    return sorted(paths, key=len, reverse=True)


def raster_mask(source: Path, size: int) -> np.ndarray:
    with tempfile.TemporaryDirectory(prefix="emojinq-alpha-skeleton-") as directory:
        directory = Path(directory)
        clean = directory / "filled.svg"
        raster = directory / "filled.png"
        tree = ET.parse(source)
        root = tree.getroot()
        for element in list(root.iter()):
            if element.tag.rsplit("}", 1)[-1] == "defs":
                root.remove(element)
            if element.get("d"):
                element.set("fill", "#111111")
                element.attrib.pop("stroke", None)
                element.attrib.pop("style", None)
        tree.write(clean, encoding="utf-8")
        subprocess.run([
            "rsvg-convert", "--background-color=#ffffff", "-w", str(size), "-h", str(size),
            "-o", str(raster), str(clean),
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        image = Image.open(raster).convert("L")
    mask = np.asarray(image) < 200
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return mask
    left, right = max(0, xs.min() - 10), min(size, xs.max() + 11)
    top, bottom = max(0, ys.min() - 10), min(size, ys.max() + 11)
    cropped = mask[top:bottom, left:right]
    side = max(cropped.shape)
    square = np.zeros((side, side), dtype=bool)
    yoff, xoff = (side - cropped.shape[0]) // 2, (side - cropped.shape[1]) // 2
    square[yoff:yoff + cropped.shape[0], xoff:xoff + cropped.shape[1]] = cropped
    return skeletonize(square)


def emit(source: Path, output: Path, size: int, minimum: float, width_scale: float = 1.0) -> int:
    skeleton = raster_mask(source, size)
    paths = trace_graph(skeleton, minimum)
    if not paths:
        raise SystemExit(f"no skeleton paths recovered from {source}")
    root = ET.Element(f"{{{NS}}}svg", {
        "viewBox": "0 0 72 72", "role": "img",
        "aria-label": source.stem,
        "data-castalia-style": "sumi-e-ink-wash-v1",
        "data-ink-stroke-system": "tapered-v1",
        "data-ink-animation": "draw-v1",
        "data-ink-path-units": "normalized",
        "data-ink-coverage": "complete",
        "data-ink-pressure": "loaded-middle-v1",
        "data-alpha-filter": "skeleton-topology-v1",
    })
    ET.SubElement(root, f"{{{NS}}}title").text = source.stem
    group = ET.SubElement(root, f"{{{NS}}}g", {"fill": "none", "stroke-linecap": "round", "stroke-linejoin": "round"})
    output_index = 0
    # The largest structural paths are darkest; shorter branches recede like
    # dry brush, while every mark remains a real animatable SVG stroke.
    for path_index, points in enumerate(paths):
        d = "M " + " ".join(f"{x * 72 / (skeleton.shape[1] - 1):.3f},{y * 72 / (skeleton.shape[0] - 1):.3f}" for x, y in points)
        d = roughen_path(d, path_index * 97 + len(points), amount=0.08)
        length = sum(np.linalg.norm(np.subtract(points[i], points[i - 1])) for i in range(1, len(points))) * 72 / (skeleton.shape[0] - 1)
        for segment, width in pressure_segments(d, length):
            ET.SubElement(group, f"{{{NS}}}path", {
                "class": "ink-stroke", "data-ink-stroke": "tapered",
                "data-ink-role": "alpha-centerline", "data-ink-index": str(output_index),
                "pathLength": "1", "d": segment,
                "stroke": "#262421" if path_index < max(3, len(paths) // 2) else "#4a4943",
                "stroke-width": f"{width * width_scale:.2f}",
            })
            output_index += 1
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=False)
    return len(paths)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--size", type=int, default=384)
    parser.add_argument("--minimum", type=float, default=2.2)
    parser.add_argument("--width-scale", type=float, default=1.0)
    args = parser.parse_args()
    print(
        f"recovered {emit(args.source, args.output, args.size, args.minimum, args.width_scale)} "
        f"skeleton gestures: {args.source}"
    )


if __name__ == "__main__":
    main()
