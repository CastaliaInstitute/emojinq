#!/usr/bin/env python3
"""Find likely detached fragments in PUA SVG studies.

This is intentionally a report-only audit. It rasterizes each SVG, identifies
connected ink components, and flags glyphs where substantial ink sits outside
the bounding box of the dominant subject. It does not rewrite artwork: the
result is a review queue for selective vector cleanup.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from collections import deque
from pathlib import Path

from PIL import Image


def components(svg: Path, size: int) -> list[tuple[int, int, int, int, int]]:
    with tempfile.NamedTemporaryFile(suffix=".png") as tmp:
        subprocess.run(
            ["rsvg-convert", "-w", str(size), "-h", str(size), "-o", tmp.name, str(svg)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        alpha = Image.open(tmp.name).convert("RGBA").getchannel("A")

    pixels = alpha.load()
    seen: set[tuple[int, int]] = set()
    found: list[tuple[int, int, int, int, int]] = []
    for y in range(size):
        for x in range(size):
            if pixels[x, y] < 32 or (x, y) in seen:
                continue
            queue = deque([(x, y)])
            seen.add((x, y))
            area = 0
            x0 = y0 = size
            x1 = y1 = 0
            while queue:
                xx, yy = queue.popleft()
                area += 1
                x0, x1 = min(x0, xx), max(x1, xx)
                y0, y1 = min(y0, yy), max(y1, yy)
                for nx, ny in ((xx - 1, yy), (xx + 1, yy), (xx, yy - 1), (xx, yy + 1)):
                    if 0 <= nx < size and 0 <= ny < size and pixels[nx, ny] >= 32 and (nx, ny) not in seen:
                        seen.add((nx, ny))
                        queue.append((nx, ny))
            found.append((area, x0, y0, x1, y1))
    return sorted(found, reverse=True)


def audit(svg: Path, size: int, margin: int, minimum: int) -> dict[str, object] | None:
    found = components(svg, size)
    if len(found) < 2:
        return None
    dominant = found[0]
    def intentional_baseline(item: tuple[int, int, int, int, int]) -> bool:
        """Recognize the shared low, dry ground wash used by study glyphs.

        These strokes are intentionally disconnected from the subject. They
        should not drown out the actual detached-fragment review queue.
        Keep the test deliberately narrow: broad, low marks only.
        """
        _, x0, y0, x1, y1 = item
        return (
            y0 >= int(size * 0.80)
            and (y1 - y0) <= max(8, size // 20)
            and (x1 - x0) >= int(size * 0.38)
        )

    outside = [
        item
        for item in found[1:]
        if item[0] >= minimum
        and not intentional_baseline(item)
        and (
            item[3] < dominant[1] - margin
            or item[1] > dominant[3] + margin
            or item[4] < dominant[2] - margin
            or item[2] > dominant[4] + margin
        )
    ]
    if not outside:
        return None
    return {
        "svg": svg.as_posix(),
        "dominant_area": dominant[0],
        "dominant_bbox": dominant[1:],
        "detached_area": sum(item[0] for item in outside),
        "detached_components": len(outside),
        "detached_bboxes": [item[1:] for item in outside[:12]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("assets/pua"))
    parser.add_argument("--size", type=int, default=128)
    parser.add_argument("--margin", type=int, default=5)
    parser.add_argument("--minimum", type=int, default=8)
    parser.add_argument("--json", type=Path, help="also write the report as JSON")
    args = parser.parse_args()

    reports = []
    for svg in sorted(args.root.rglob("*.svg")):
        if svg.parent.name == "references":
            continue
        report = audit(svg, args.size, args.margin, args.minimum)
        if report:
            reports.append(report)

    for report in sorted(reports, key=lambda item: int(item["detached_area"]), reverse=True):
        print(
            f"{report['svg']}: {report['detached_components']} detached components, "
            f"{report['detached_area']} px² outside dominant subject"
        )
    print(f"PUA artifact audit: {len(reports)} flagged glyphs")
    if args.json:
        args.json.write_text(json.dumps(reports, indent=2) + "\n")


if __name__ == "__main__":
    main()
